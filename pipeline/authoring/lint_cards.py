"""Form checks on card sources beyond build_cards.py (wording only).

    uv run python -I authoring/lint_cards.py [CODE...]
"""
import json
import pathlib
import re
import sys

SRC = pathlib.Path(__file__).resolve().parent / "cards"
codes = {c.upper() for c in sys.argv[1:]}
bad = 0
for p in sorted(SRC.glob("*.json")):
    s = json.loads(p.read_text(encoding="utf-8"))
    if codes and s["outcome"] not in codes:
        continue
    for c in s["cards"]:
        probs = []
        for t, v in c["tools"].items():
            w = v["why"]
            if re.search(r"\bsám\b|\bsami\b|š(?: \w+)? sama\b|\bnaučil", w):
                probs.append(f"{t}: gendered: {w}")
            if len(w) > 110:
                probs.append(f"{t}: {len(w)} chars")
            if re.search(r"[!–—…]|ChatGPT|Gemini", w):
                probs.append(f"{t}: punctuation/brand: {w}")
        if len(c["title"]) > 70 or "?" in c["title"]:
            probs.append(f"title: {c['title']}")
        if probs:
            bad += 1
            print(f"{s['outcome']} {c['slug']}:\n  " + "\n  ".join(probs))
print(f"{bad} cards with problems")
