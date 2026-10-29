"""Batches of card context for drafting the card texts (prompts/card-v5.md).

    uv run python -I authoring/comment_inputs.py OUT_DIR [--size 10] [--missing] [--version comment-v5] [--by-goal] [--titles]

Reads content/ (activities, measures, occupations, jobnotes, comments, outcomes); writes OUT_DIR/batchN.json.
--missing: only cards without a comment of --version.
--titles: only cards whose AI suggestions have no titles yet, with just what the titles need ("titles only").
"""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
C = ROOT / "content"
VERDICT = {"za-tebe": "Udělá to za tebe", "pomuze": "Pomůže ti", "nepomuze": "Nepomůže"}
TOOL = {"chatbot": "AI chatbot", "internet": "Internet a další zdroje", "aplikace": "Aplikace", "klasicky": "Klasický nástroj"}


def read(p, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=10)
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--version", default="comment-v5")
    ap.add_argument("--titles", action="store_true", help="titles-only batches for suggestions without a title")
    ap.add_argument("--by-goal", action="store_true", help="batches of whole goals (for card-v5: tools + texts)")
    a = ap.parse_args()
    outcomes = read(C / "rvp" / "outcomes.json")
    measures = read(C / "measures.json", {})
    occs = read(C / "esco" / "occupations.json", {})
    cards = []
    for f in sorted((C / "activities").glob("*.json")):
        for act in read(f):
            old = read(C / "comments" / f"{act['slug']}.json")
            if a.missing and old and old.get("promptVersion") == a.version:
                continue
            o = outcomes[act["outcome"]]
            if a.titles:
                tips = (old or {}).get("learnWithAi", [])
                if isinstance(tips, list) and tips and any(isinstance(t, str) or not t.get("title") for t in tips):
                    cards.append({"slug": act["slug"], "title": act["title"], "stage": o["stageLabel"],
                                  "tips": [t if isinstance(t, str) else t["text"] for t in tips]})
                continue
            m = measures.get(act["slug"], {})
            notes = read(C / "jobnotes" / f"{act['slug']}.json", {"notes": {}})["notes"]
            hi = m.get("exposureMix", {}).get("high")
            cards.append({
                "slug": act["slug"],
                "title": act["title"],
                "subject": o["subject"]["name"],
                "stage": o["stageLabel"],
                "goal": o["text"],
                # Kept small: quote only where the card uses part of the point, notes only where they exist.
                "rvpPoints": [{"point": s["point"], **({"quote": s["quote"]} if s["quote"] != s["point"] else {})} for s in act["levelSource"]],
                "outcome": act["outcome"],
                "tools": {TOOL[t]: f'{VERDICT.get(v["verdict"], v["verdict"])}: {v["why"]}' for t, v in act["tools"].items()},
                "work": {
                    "occupations": m.get("occupationCount"),
                    "people": m.get("employment"),
                    "peopleShare": round(100 * m["employmentShare"], 1) if m.get("employmentShare") is not None else None,
                    "highAiExposure": round(100 * hi) if hi is not None else None,
                    "trend2035": m.get("trendPct"),
                    "buildsOnIt": m.get("foundationCount"),
                },
                "topOccupations": [{"label": occs[i]["label"], **({"note": notes[i]} if notes.get(i) else {})} for i in m.get("topOccupations", []) if i in occs],
                "buildsToward": [outcomes[c]["text"] for c in o["next"] if c in outcomes],
                "earlierComment": (old or {}).get("comment", ""),
            })
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for p in out.glob("batch*.json"):
        p.unlink()
    n = 0
    if a.by_goal:
        goals = {}
        for c in cards:
            o = outcomes[c["outcome"]]
            g = goals.setdefault(c["outcome"], {
                "outcome": c["outcome"], "sourceFile": str(ROOT / "pipeline" / "authoring" / "cards" / f"{c['outcome'].lower()}.json"),
                "subject": c["subject"], "stage": c["stage"], "goal": c["goal"], "buildsToward": c["buildsToward"], "cards": []})
            g["cards"].append({"slug": c["slug"], "title": c["title"], "rvpPoints": c["rvpPoints"], "tools": c["tools"],
                               "work": c["work"], "topOccupations": c["topOccupations"]})
        batch, size = [], 0
        for g in goals.values():
            batch.append(g); size += len(g["cards"])
            if size >= a.size:
                n += 1
                (out / f"batch{n}.json").write_text(json.dumps(batch, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
                batch, size = [], 0
        if batch:
            n += 1
            (out / f"batch{n}.json").write_text(json.dumps(batch, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{len(cards)} cards in {len(goals)} goals, {n} batches -> {out}")
        return
    for i in range(0, len(cards), a.size):
        n += 1
        (out / f"batch{n}.json").write_text(json.dumps(cards[i:i + a.size], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(cards)} cards in {n} batches -> {out}")


if __name__ == "__main__":
    main()
