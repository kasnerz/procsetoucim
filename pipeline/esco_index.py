"""ESCO + ILO + Cedefop index and the `content/measures` computation.

Usage from other scripts:
    from esco_index import load_index, compute_measures
    idx = load_index()
    m = compute_measures(skill_uris, outcome_code)
"""
import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CACHE, CONTENT, DATA, clean_text, fold, read_json

ESCO_DIR = DATA / "esco"
ILO_XLSX = DATA / "ilo" / "Final_Scores_ISCO08_Gmyrek_et_al_2025.xlsx"
CACHE_FILE = CACHE / "esco_index.json"
HIGH_GRADIENTS = {"Gradient 3", "Gradient 4"}
csv.field_size_limit(10**8)


def uuid_of(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]


def split_label(raw: str) -> tuple[str, list[str]]:
    label, forms = _split_label(raw)
    return (label[:1].upper() + label[1:]), forms


def _split_label(raw: str) -> tuple[str, list[str]]:
    """ESCO cs labels look like 'lékař/lékařka' or 'kurýr pro rozvoz/kurýrka pro rozvoz'.
    Returns (compact label, list of the distinct forms). Two forms that differ only in some words
    are merged word-wise: 'kurýr/kurýrka pro rozvoz zásilek na kole'."""
    parts = [p.strip() for p in raw.split("/") if p.strip()]
    uniq = list(dict.fromkeys(parts))
    if not uniq:
        return raw.strip(), []
    if len(uniq) == 1:
        return uniq[0], uniq
    if len(uniq) == 2:
        a, b = uniq[0].split(), uniq[1].split()
        pre = 0
        while pre < min(len(a), len(b)) and a[pre] == b[pre]:
            pre += 1
        suf = 0
        while suf < min(len(a), len(b)) - pre and a[-1 - suf] == b[-1 - suf]:
            suf += 1
        mid_a = " ".join(a[pre:len(a) - suf]); mid_b = " ".join(b[pre:len(b) - suf])
        if mid_a and mid_b and len(mid_a.split()) <= 2 and len(mid_b.split()) <= 2:
            words = a[:pre] + [f"{mid_a}/{mid_b}"] + (a[len(a) - suf:] if suf else [])
            return " ".join(words), uniq
    return ", ".join(uniq), uniq


def _lines(s: str) -> list[str]:
    return [x.strip() for x in s.splitlines() if x.strip()]


def _read_csv(name):
    with open(ESCO_DIR / name, encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)


def _load_ilo() -> dict[str, dict]:
    import openpyxl
    wb = openpyxl.load_workbook(ILO_XLSX, read_only=True, data_only=True)
    rows = wb.active.iter_rows(values_only=True)
    head = list(next(rows))
    ic, im, ip = head.index("ISCO_08"), head.index("mean_score_2025"), head.index("potential25")
    out = {}
    for r in rows:
        if r[ic] is None or str(r[ic]) in out:
            continue
        pot = str(r[ip]).strip()
        grad = pot.split(":")[-1].strip()  # 'Exposed: Gradient 3' -> 'Gradient 3'; 'Not Exposed' stays
        out[str(r[ic]).zfill(4)] = {"score": round(float(r[im]), 3), "gradient": grad}
    return out


def _sources_mtime() -> float:
    files = [p for p in ESCO_DIR.glob("*.csv")] + [ILO_XLSX, Path(__file__)]
    return max(p.stat().st_mtime for p in files if p.exists())


def build_cache() -> dict:
    ilo = _load_ilo()
    occs = {}
    for r in _read_csv("occupations_cs.csv"):
        oid = uuid_of(r["conceptUri"])
        label, forms = split_label(r["preferredLabel"])
        alts = []
        for a in _lines(r["altLabels"]):
            if a not in forms and a not in alts:
                alts.append(a)
        isco4 = r["iscoGroup"].strip().zfill(4)
        occs[oid] = {
            "id": oid, "uri": r["conceptUri"], "label": label, "labelAlt": alts,
            "description": clean_text(r["description"]).strip(), "isco4": isco4, "isco2": isco4[:2],
            "ilo": ilo.get(isco4),
        }
    skills = {}
    for r in _read_csv("skills_cs.csv"):
        skills[r["conceptUri"]] = {
            "uri": r["conceptUri"], "label": r["preferredLabel"].strip(),
            "alt": _lines(r["altLabels"]), "description": clean_text(r["description"]).strip(),
            "skillType": r["skillType"], "reuseLevel": r["reuseLevel"],
        }
    ess = defaultdict(list)    # skill uri -> [occ id]
    opt = defaultdict(list)
    occ_ess = defaultdict(list)  # occ id -> [skill uri]
    for r in _read_csv("occupationSkillRelations_cs.csv"):
        oid = uuid_of(r["occupationUri"])
        if oid not in occs or r["skillUri"] not in skills:
            continue
        if r["relationType"] == "essential":
            ess[r["skillUri"]].append(oid)
            occ_ess[oid].append(r["skillUri"])
        else:
            opt[r["skillUri"]].append(oid)
    # ESCO collections on the occupation page: research occupations are tagged directly; for green and digital we
    # count the occupation's skills (essential and optional, as ESCO's own greenShare does) that are in the collection.
    research = {r["conceptUri"] for r in _read_csv("researchOccupationsCollection_cs.csv")}
    in_coll = {k: {r["conceptUri"] for r in _read_csv(f"{k}SkillsCollection_cs.csv")} for k in ("green", "digital")}
    occ_all = defaultdict(list)  # occ id -> [skill uri], essential first
    for oid in occ_ess:
        occ_all[oid].extend(occ_ess[oid])
    for u, oids in opt.items():
        for oid in oids:
            occ_all[oid].append(u)
    for oid, o in occs.items():
        uris = occ_all.get(oid, [])
        coll = {"research": o["uri"] in research}
        for k, members in in_coll.items():
            hits = [u for u in uris if u in members]
            coll[k] = {"count": len(hits), "of": len(uris), "examples": [skills[u]["label"] for u in hits[:3]]}
        o["collections"] = coll
    narrower = defaultdict(list)  # skill uri -> direct narrower skills (skills only, no SkillGroups)
    for r in _read_csv("broaderRelationsSkillPillar_cs.csv"):
        if r["conceptType"] == "KnowledgeSkillCompetence" and r["conceptUri"] in skills:
            narrower[r["broaderUri"]].append(r["conceptUri"])
    return {"occupations": occs, "skills": skills, "essential": ess, "optional": opt,
            "occEssential": occ_ess, "narrower": narrower, "iloCount": len(ilo)}


class Index:
    def __init__(self, d: dict):
        self.occupations = d["occupations"]
        self.skills = d["skills"]
        self.essential = d["essential"]          # skill uri -> [occ id]
        self.optional = d["optional"]
        self.occ_essential = d["occEssential"]   # occ id -> [skill uri]
        self.narrower = d["narrower"]
        self.group_size = defaultdict(int)       # isco2 -> number of ESCO occupations
        for o in self.occupations.values():
            self.group_size[o["isco2"]] += 1
        self._isco2 = None
        self._outcomes = None

    def expand(self, uris) -> set:
        """Skills themselves plus all transitive narrower skills (SkillGroups excluded)."""
        out, stack = set(), list(uris)
        while stack:
            u = stack.pop()
            if u in out:
                continue
            out.add(u)
            stack.extend(self.narrower.get(u, ()))
        return out

    def essential_occupations(self, uris) -> set:
        needing = set()
        for u in self.expand(uris):
            needing.update(self.essential.get(u, ()))
        return needing

    @property
    def isco2(self) -> dict:
        if self._isco2 is None:
            self._isco2 = read_json(CONTENT / "labour" / "isco2.json")
        return self._isco2

    @property
    def outcomes(self) -> dict:
        if self._outcomes is None:
            p = CONTENT / "rvp" / "outcomes.json"
            self._outcomes = read_json(p) if p.exists() else {}
        return self._outcomes


def load_index(rebuild: bool = False) -> Index:
    CACHE.mkdir(parents=True, exist_ok=True)
    if not rebuild and CACHE_FILE.exists() and CACHE_FILE.stat().st_mtime >= _sources_mtime():
        with open(CACHE_FILE, encoding="utf-8") as f:
            return Index(json.load(f))
    d = build_cache()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    return Index(d)


def exposure_bucket(gradient: str) -> str:
    """ILO potential25 label -> high / medium / low / none (same reading as the site's iloWords)."""
    g = gradient.lower()
    if "4" in g or "3" in g:
        return "high"
    if "1" in g or "2" in g:
        return "medium"
    if "minimal" in g:
        return "low"
    return "none"


def _relevance(name: str | None) -> dict:
    """Decision-model scores from relevance.py (content/relevance/<name>.json), {} when not scored."""
    if not name:
        return {}
    p = CONTENT / "relevance" / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8"))["scores"] if p.exists() else {}


def compute_measures(skill_uris, outcome_code=None, idx: Index | None = None, slug: str | None = None) -> dict:
    """The `content/measures` fields for one activity (see docs/content-schema.md).

    occupationCount  ESCO occupations with >=1 of the skills (or any narrower skill) as essential
    employmentShare  sum over ISCO-2 groups g of emp2025[g] * (needing[g] / esco_occupations[g]),
                     divided by total CZ employment 2025 (sum of all groups in isco2.json)
    highExposureShare  the same weights, restricted to the fraction of needing occupations with
                     ILO potential25 in Gradient 3/4; denominator = weights of needing occupations
                     that have an ILO match
    trendPct         employment-weighted 2025->2035 change using the same weights
    topOccupations   8 example occupations; max 2 per group. With relevance scores (content/relevance/<slug>.json,
                     relevance.py): by how much the job uses the skill, then how well kids know the job,
                     then common jobs; jobs that barely use it (use < 1 of 4) are left out. Without scores: by skill
                     specificity (see below), then direct, then common jobs
    relevance        {occId: 0-1} for topOccupations (use / 4), when scored
    allOccupations   every needing occupation in the same order without the per-group cap (written to
                     content/activity-occupations.json by build_esco, not kept in measures.json)
    employment       the weighted employment itself (people, 2025), rounded to hundreds
    byMajor          share of total CZ employment per ISCO-1 major group ("1".."9", "0"), same weights
    exposureMix      shares of the ILO-matched weights by bucket: high (Gradient 3/4), medium (Gradient 1/2),
                     low (Minimal Exposure), none (Not Exposed)
    """
    idx = idx or load_index()
    skills = idx.expand(skill_uris)  # skill + all narrower skills (see README)
    needing = idx.essential_occupations(skill_uris)
    isco2 = idx.isco2
    total = sum(g["employment2025"] for g in isco2.values()) or 1

    by_group = defaultdict(list)
    for oid in needing:
        by_group[idx.occupations[oid]["isco2"]].append(oid)

    w_sum = w_2035 = hi_w = ilo_w = 0.0
    major = defaultdict(float)
    mix = {"high": 0.0, "medium": 0.0, "low": 0.0, "none": 0.0}
    for g, oids in by_group.items():
        grp = isco2.get(g)
        if not grp or not grp["employment2025"]:
            continue
        per_occ = grp["employment2025"] / idx.group_size[g]  # employment attributed to each ESCO occupation
        w = per_occ * len(oids)
        w_sum += w
        w_2035 += w * (grp["employment2035"] / grp["employment2025"])
        major[g[0]] += w
        for oid in oids:
            ilo = idx.occupations[oid]["ilo"]
            if ilo:
                ilo_w += per_occ
                if ilo["gradient"] in HIGH_GRADIENTS:
                    hi_w += per_occ
                mix[exposure_bucket(ilo["gradient"])] += per_occ

    # Examples for kids: rank by how specifically the card's skills point to the occupation. Each card
    # skill an occupation needs adds 1/log2(2 + occupations needing that skill), so a subject skill
    # ("vytvářet umělecká díla", 34 occupations) outweighs a broad one ("spolupracovat s kolegy", 72)
    # and occupations needing several of the skills come first. Ties: direct (not only via a narrower
    # skill), then large ISCO-2 groups (common jobs). At most 2 per group for variety.
    direct = set()
    for u in skill_uris:
        direct.update(idx.essential.get(u, ()))
    spec = defaultdict(float)
    for u in skill_uris:
        occ_u = idx.essential_occupations([u])
        for oid in occ_u:
            spec[oid] += 1 / math.log2(2 + len(occ_u))

    def per_occ(oid):
        g = idx.occupations[oid]["isco2"]
        grp = isco2.get(g)
        return grp["employment2025"] / idx.group_size[g] if grp and idx.group_size[g] else 0.0

    rel = _relevance(slug)
    if rel and all(o in rel for o in needing):
        known = _relevance("_known")
        ordered = sorted(needing, key=lambda o: (-rel[o]["use"], -known.get(o, 0), -per_occ(o),
                                                 idx.occupations[o]["label"], o))
        eligible = [o for o in ordered if rel[o]["use"] >= 1]
    else:
        rel = None
        ordered = sorted(needing, key=lambda o: (-round(spec[o], 3), o not in direct, -per_occ(o), idx.occupations[o]["label"], o))
        eligible = ordered
    ranked, per_group = [], defaultdict(int)
    for o in eligible:
        g = idx.occupations[o]["isco2"]
        if per_group[g] < 2:
            ranked.append(o); per_group[g] += 1
        if len(ranked) == 8:
            break
    graph = (idx.outcomes.get(outcome_code or "") or {}).get("graph", {})
    return {
        "occupationCount": len(needing),
        "employmentShare": round(w_sum / total, 4),
        "highExposureShare": round(hi_w / ilo_w, 4) if ilo_w else None,
        "trendPct": round((w_2035 / w_sum - 1) * 100, 1) if w_sum else None,
        "topOccupations": ranked[:8],
        **({"relevance": {o: round(rel[o]["use"] / 4, 3) for o in ranked[:8]}} if rel else {}),
        "allOccupations": ordered,
        "employment": int(round(w_sum, -2)),
        "byMajor": {k: round(v / total, 4) for k, v in sorted(major.items())},
        "exposureMix": {k: round(v / ilo_w, 4) for k, v in mix.items()} if ilo_w else None,
        "foundationCount": graph.get("foundationCount", 0),
        "transferCount": graph.get("transferCount", 0),
    }


if __name__ == "__main__":
    ix = load_index(rebuild=True)
    n = sum(1 for o in ix.occupations.values() if o["ilo"])
    print(f"occupations {len(ix.occupations)}, with ILO match {n}; skills {len(ix.skills)}")
