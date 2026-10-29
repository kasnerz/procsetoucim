"""content/activities/*.json -> content/esco/{occupations,skills,groups}.json, content/measures.json, content/meta.json."""
import csv
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CEDEFOP_CITATION, CONTENT, DATA, write_json
from esco_index import compute_measures, load_index


def load_activities() -> list[dict]:
    acts = []
    for p in sorted((CONTENT / "activities").glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:  # file being written in parallel, etc.
            print(f"WARNING: skipping {p.name}: {e}")
            continue
        if isinstance(data, dict):
            data = [data]
        for a in data:
            a["_file"] = p.name
            acts.append(a)
    return acts


def build():
    idx = load_index()
    acts = load_activities()
    seen_slugs, skill_uris, measures = set(), set(), {}
    for a in acts:
        slug = a.get("slug")
        if not slug:
            print(f"WARNING: activity without slug in {a['_file']}")
            continue
        if slug in seen_slugs:
            print(f"WARNING: duplicate slug {slug}")
        seen_slugs.add(slug)
        uris = [u for u in a.get("escoSkills", []) if u]
        unknown = [u for u in uris if u not in idx.skills]
        if unknown:
            print(f"WARNING: {slug}: unknown ESCO skill URIs {unknown}")
        uris = [u for u in uris if u in idx.skills]
        skill_uris.update(uris)
        measures[slug] = compute_measures(uris, a.get("outcome"), idx, slug=slug)

    reach = {}
    skills_out = {}
    for u in sorted(skill_uris):
        s = idx.skills[u]
        ess = sorted(idx.essential_occupations([u]))
        direct = idx.essential.get(u, [])
        for oid in ess:
            reach[oid] = idx.occupations[oid]
        skills_out[u] = {"uri": u, "label": s["label"], "description": s["description"],
                         "essentialFor": ess, "essentialForDirect": sorted(direct),
                         "narrowerCount": len(idx.expand([u])) - 1,
                         "optionalFor": len(idx.optional.get(u, []))}
    for m in measures.values():  # topOccupations are always a subset of reachable ones
        for oid in m["topOccupations"]:
            reach[oid] = idx.occupations[oid]
    occ_out = {oid: reach[oid] for oid in sorted(reach)}

    write_json(CONTENT / "esco" / "occupations.json", occ_out)
    write_json(CONTENT / "esco" / "skills.json", skills_out)
    # ISCO-08 major (1-digit) and sub-major (2-digit) groups: the occupation areas on the site.
    with open(DATA / "esco" / "ISCOGroups_cs.csv", encoding="utf-8", newline="") as f:
        groups = {r["code"]: r["preferredLabel"].strip() for r in csv.DictReader(f) if len(r["code"]) <= 2}
    write_json(CONTENT / "esco" / "groups.json", dict(sorted(groups.items())))
    all_occ = {slug: m.pop("allOccupations") for slug, m in measures.items()}
    write_json(CONTENT / "measures.json", measures)
    write_json(CONTENT / "activity-occupations.json", all_occ)

    isco2 = idx.isco2
    meta = {
        "buildDate": date.today().isoformat(),
        "counts": {"activities": len(measures), "skills": len(skills_out), "occupations": len(occ_out),
                   "escoOccupationsTotal": len(idx.occupations), "escoOccupationsWithIlo":
                   sum(1 for o in idx.occupations.values() if o["ilo"])},
        "sources": {
            "rvp": {"name": "RVP ZV (NPI ČR, otevřená data, 16. 12. 2025)",
                    "url": "https://prohlednout.rvp.cz/"},
            "esco": {"name": "ESCO – European Skills, Competences, Qualifications and Occupations, v1.2.1",
                     "version": "1.2.1", "language": "cs",
                     "url": "https://esco.ec.europa.eu/"},
            "ilo": {"name": "ILO GenAI exposure index 2025 (ISCO-08, 4-digit), Gmyrek et al. 2025, ILO Working Paper 140",
                    "url": "https://github.com/pgmyrek/2025_GenAI_scores_ISCO08", "licence": "CC BY 4.0"},
            "cedefop": {"name": "Cedefop Skills Forecast 2026 (Employment by detailed occupation, ISCO-08 2-digit)",
                        "url": "https://www.cedefop.europa.eu/en/projects/skills-forecast",
                        "note": "Indicative only. Cells under 10 000 people are flagged unreliable. "
                                "Employment 2025 and 2035 are forecasts (last historical year 2023)."},
        },
        "citations": {
            "cedefop": CEDEFOP_CITATION,
            "ilo": "Gmyrek, P., Berg, J., Kamiński, K., Konopczyński, F., Ładna, A., Nafradi, B., Rosłaniec, K., "
                   "Troszyński, M. (2025). Generative AI and Jobs: A 2025 Update. ILO Working Paper 140. "
                   "Data: https://github.com/pgmyrek/2025_GenAI_scores_ISCO08 (CC BY 4.0).",
            "esco": "ESCO – European Skills, Competences, Qualifications and Occupations, v1.2.1. "
                    "© European Union, https://esco.ec.europa.eu/",
            "rvp": "Rámcový vzdělávací program pro základní vzdělávání (nový RVP ZV), NPI ČR / MŠMT, "
                   "otevřená data k 16. 12. 2025. Výstupy: https://prohlednout.rvp.cz/ovu/<kód výsledku>",
        },
        "labour": {"employmentTotal2025": sum(g["employment2025"] for g in isco2.values()),
                   "employmentTotal2035": sum(g["employment2035"] for g in isco2.values()),
                   "iscoLevel": 2, "country": "Czechia"},
    }
    write_json(CONTENT / "meta.json", meta)
    print(f"{len(measures)} activities, {len(skills_out)} skills, {len(occ_out)} occupations")


if __name__ == "__main__":
    build()
