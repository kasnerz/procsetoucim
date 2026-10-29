"""RVP ZV JSON -> content/rvp/outcomes.json + structure.json."""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONTENT, RVP_JSON, html_to_text, read_json, write_json, clean_text

STAGE_LABEL = {"ZV3": "do konce 3. třídy", "ZV5": "do konce 5. třídy", "ZV9": "do konce 9. třídy"}
STAGE_RANK = {"ZV3": 3, "ZV5": 5, "ZV9": 9}
STAGES = set(STAGE_LABEL)


def ref(code, name):
    return {"code": str(code), "name": clean_text(name or "").strip()}


def build():
    d = read_json(RVP_JSON)
    raw = {}      # code -> dict
    order = []

    def add_node_outcomes(node, kind, area, subject, okruh, out_codes):
        for ub in node.get("uzloveBody", []):
            stage = ub["kod"]
            if stage not in STAGES:
                continue
            for r in ub.get("ocekavaneVysledkyUceni", []):
                code = r["kod"]
                levels, illus = [], []
                for lv in r.get("urovneMetodickePodpory", []):
                    levels.append({"name": lv["nazev"], "text": html_to_text(lv.get("charakteristika"))})
                    for il in lv.get("ilustrace", []):
                        illus.append({
                            "level": lv["nazev"],
                            "title": clean_text(html.unescape(il.get("nazev", ""))).strip(),
                            "text": html_to_text(il.get("charakteristika")),
                            "url": il.get("url") or "",
                        })
                raw[code] = {
                    "code": code, "kind": kind, "area": area, "subject": subject, "okruh": okruh,
                    "stage": stage, "stageLabel": STAGE_LABEL[stage],
                    "text": clean_text(r["zneni"]).strip(),
                    "rationale": html_to_text(r.get("popisAZduvodneni")),
                    "levels": levels, "illustrations": illus,
                    "_links": list(r.get("predchazejiciOcekavaneVysledkyUceni", []))
                              + list(r.get("nasledujiciOcekavaneVysledkyUceni", [])),
                    "_related": list(r.get("souvisejiciOcekavaneVysledkyUceni", [])),
                }
                order.append(code)
                out_codes.append(code)

    structure = {"areas": [], "literacies": [], "competences": [], "themes": []}

    for ob in d["vzdelavaciOblasti"]:
        area = ref(ob["kod"], ob["nazev"])
        sa = {**area, "subjects": []}
        for vo in ob.get("vzdelavaciObory", []):
            subj = ref(vo["kod"], vo["nazev"])
            ss = {**subj, "okruhy": []}
            for to in vo.get("tematickeOkruhy", []):
                okr = ref(to["kod"], to["nazev"])
                codes = []
                add_node_outcomes(to, "obor", area, subj, okr, codes)
                ss["okruhy"].append({**okr, "outcomes": codes})
            sa["subjects"].append(ss)
        structure["areas"].append(sa)

    def grouped(items, slozky_key, kind, area_ref, target):
        for it in items:
            subj = ref(it["kod"], it["nazev"])
            entry = {**subj, "components": [], "outcomes": []}
            for sl in it.get(slozky_key, []):
                comp = ref(sl["kod"], sl["nazev"])
                codes = []
                add_node_outcomes(sl, kind, area_ref, subj, comp, codes)
                entry["components"].append({**comp, "outcomes": codes})
            add_node_outcomes(it, kind, area_ref, subj, None, entry["outcomes"])
            target.append(entry)

    grouped(d["zakladniGramotnosti"], "slozkyZakladniGramotnosti", "gramotnost",
            {"code": "ZG", "name": "Základní gramotnosti"}, structure["literacies"])
    grouped(d["klicoveKompetence"], "slozkyKlicoveKompetence", "kompetence",
            {"code": "KK", "name": "Klíčové kompetence"}, structure["competences"])
    pt = d["prurezovaTemata"]
    pt = pt if isinstance(pt, list) else [pt]
    grouped(pt, "slozkyPrurezovehoTematu", "prurezove",
            {"code": "PT", "name": "Průřezová témata"}, structure["themes"])

    # --- graph direction -------------------------------------------------
    # The data's predchazejici/nasledujici lists are not usable as-is (see README):
    # ZV5<->ZV9 pairs appear in BOTH lists of BOTH outcomes. We therefore take the union
    # of the two lists as an undirected "gradation link" and orient it by stage.
    out = {}
    dropped_unknown = 0
    for code in order:
        r = raw[code]
        prev, nxt = [], []
        for x in dict.fromkeys(r["_links"]):
            if x not in raw:
                dropped_unknown += 1
                continue
            a, b = STAGE_RANK[r["stage"]], STAGE_RANK[raw[x]["stage"]]
            if b > a:
                nxt.append(x)
            elif b < a:
                prev.append(x)
            # same-stage gradation links do not occur in the data
        related = [x for x in dict.fromkeys(r["_related"]) if x in raw and x != code]
        out[code] = r
        r["prev"], r["next"], r["related"] = sorted(prev), sorted(nxt), related

    for code, r in out.items():
        # transitive closure via next
        seen, stack = set(), list(r["next"])
        while stack:
            c = stack.pop()
            if c in seen:
                continue
            seen.add(c)
            stack.extend(out[c]["next"])
        transfer = [x for x in r["related"] if x.startswith("K") or x.startswith("ZG")]
        r["url"] = f"https://prohlednout.rvp.cz/ovu/{code.lower()}"
        r["graph"] = {"foundationCount": len(seen), "transferCount": len(transfer), "transfer": transfer}
        r.pop("_links"); r.pop("_related")

    # key order per schema
    keys = ["code", "kind", "area", "subject", "okruh", "stage", "stageLabel", "text", "rationale",
            "levels", "illustrations", "prev", "next", "related", "url", "graph"]
    out = {c: {k: r[k] for k in keys} for c, r in out.items()}
    write_json(CONTENT / "rvp" / "outcomes.json", out)
    write_json(CONTENT / "rvp" / "structure.json", structure)
    print(f"{len(out)} outcomes; links to codes outside the dataset dropped: {dropped_unknown}")
    return out


if __name__ == "__main__":
    build()
