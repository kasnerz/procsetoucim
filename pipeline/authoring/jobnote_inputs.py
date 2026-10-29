"""Batches of (card, top occupations) for drafting occupation notes (prompts/jobnotes-v2.md).

    uv run python -I authoring/jobnote_inputs.py OUT_DIR [--notes 60] [--missing]

--missing: only the current top occupations that have no note yet (cards with none missing are left out).
Batches hold about --notes notes each (whole cards), kept compact so an agent reads a batch in one go (~40 KB).
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
C = ROOT / "content"


def read(p, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--notes", type=int, default=60)
    ap.add_argument("--missing", action="store_true")
    a = ap.parse_args()
    measures = read(C / "measures.json", {})
    occs = read(C / "esco" / "occupations.json", {})
    skills = read(C / "esco" / "skills.json", {})
    isco2 = read(C / "labour" / "isco2.json", {})
    levels = ["Skoro nevyužívá", "Využívá zřídka", "Využívá občas", "Využívá často", "Využívá neustále"]
    cards = []
    for f in sorted((C / "activities").glob("*.json")):
        for act in read(f):
            top = [i for i in measures.get(act["slug"], {}).get("topOccupations", []) if i in occs]
            have = read(C / "jobnotes" / f"{act['slug']}.json", {"notes": {}})["notes"]
            if a.missing:
                top = [i for i in top if i not in have]
            if not top:
                continue
            rel = read(C / "relevance" / f"{act['slug']}.json", {"scores": {}})["scores"]
            rows = []
            for i in top:
                o = occs[i]
                sk = [skills[u] for u in act["escoSkills"] if u in skills]
                rows.append({
                    "id": i, "label": o["label"], "description": o["description"][:380],
                    "group": isco2.get(o["isco2"], {}).get("label", ""),
                    "needsSkills": [s["label"] for s in sk if i in s["essentialFor"]],
                    "needsDirectly": [s["label"] for s in sk if i in s["essentialForDirect"]],
                    **({"use": levels[max(0, min(4, round(rel[i]["use"])))]} if i in rel else {}),
                })
            cards.append({"slug": act["slug"], "title": act["title"],
                          "rvpPoints": [s["point"] for s in act["levelSource"]], "occupations": rows})
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for p in out.glob("batch*.json"):
        p.unlink()
    n, batch, size = 0, [], 0
    for c in cards + [None]:
        if c is None or (batch and size + len(c["occupations"]) > a.notes):
            if batch:
                n += 1
                (out / f"batch{n}.json").write_text(json.dumps(batch, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            batch, size = [], 0
        if c is not None:
            batch.append(c); size += len(c["occupations"])
    print(f"{len(cards)} cards, {sum(len(c['occupations']) for c in cards)} notes in {n} batches -> {out}")


if __name__ == "__main__":
    main()
