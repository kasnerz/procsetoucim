"""Print an RVP outcome for card drafting: goal, numbered points per level, illustration titles, related cards.

    uv run python -I authoring/show_outcome.py CODE [CODE...]
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUTCOMES = json.loads((ROOT / "content" / "rvp" / "outcomes.json").read_text(encoding="utf-8"))
SRC = pathlib.Path(__file__).resolve().parent / "cards"


def existing():
    out = {}
    for p in sorted(SRC.glob("*.json")):
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        out[s["outcome"]] = [(c["slug"], c["title"]) for c in s["cards"]]
    return out


have = existing()
for code in sys.argv[1:]:
    o = OUTCOMES[code.upper()]
    print(f"# {o['code']}  {o['subject']['name']} · {o['stageLabel']} · {(o['okruh'] or {}).get('name', '')}")
    print(f"Goal: {o['text']}")
    if o.get("rationale"):
        print(f"Rationale: {o['rationale'][:600]}")
    for l in o["levels"]:
        print(f"\n## {l['name']}")
        for i, line in enumerate([x.strip() for x in l["text"].split("\n") if x.strip()], 1):
            print(f"  {i}. {line}")
    titles = [i["title"] for i in o["illustrations"] if i["title"]]
    if titles:
        print("\nIllustration titles (exact, for `inspiration` and rule P5):")
        for t in titles:
            print(f"  - {t}")
    rel = [c for c in o["prev"] + o["next"] + o["related"] if c in have]
    if rel:
        print("\nExisting cards in linked goals (for O1 refs, avoid duplicates):")
        for c in dict.fromkeys(rel):
            print(f"  {c}: " + "; ".join(f"{s} ({t})" for s, t in have[c]))
    print()
