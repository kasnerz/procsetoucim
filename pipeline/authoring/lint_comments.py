"""Check drafted comments against prompts/card-v5.md (form only; content needs a human).

    uv run python -I authoring/lint_comments.py [--version comment-v5] [--slugs SLUG...]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
VERSION = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "comment-v5"
ONLY = set(sys.argv[sys.argv.index("--slugs") + 1:]) if "--slugs" in sys.argv else None
BANNED = ["nejen", "nejde o", "nejde jen", "klíčov", "zásadní", "nedílн", "efektivn", "v dnešní době", "digitálním světě",
          "ESCO", "ILO", "Cedefop", "ChatGPT", "Gemini", "Photomath", "Mapy.com", "naučil", "naučila", "!", " – ", " — ", "…"]
slugs = [a["slug"] for f in sorted((ROOT / "content" / "activities").glob("*.json"))
         for a in json.loads(f.read_text(encoding="utf-8"))]
bad = 0
if ONLY:
    slugs = [s for s in slugs if s in ONLY]


def sentences(t):
    return len(re.findall(r"[.?!](?:\s|$)(?=[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ0-9]|$)", t))


for s in slugs:
    p = ROOT / "content" / "comments" / f"{s}.json"
    if not p.exists():
        print(f"{s}: missing"); bad += 1; continue
    c = json.loads(p.read_text(encoding="utf-8"))
    t = c["comment"]
    probs = []
    if c.get("promptVersion") != VERSION:
        probs.append(f"version {c.get('promptVersion')}")
    n = sentences(t)
    if not 3 <= n <= 5:
        probs.append(f"{n} sentences")
    if not 250 <= len(t) <= 720:
        probs.append(f"{len(t)} chars")
    raw = c.get("learnWithAi", [])
    if not isinstance(raw, list) or len(raw) != 3:
        probs.append("learnWithAi is not a list of three")
        raw = raw if isinstance(raw, list) else [raw]
    lw = [t["text"] if isinstance(t, dict) else t for t in raw]
    titles = [t.get("title", "") if isinstance(t, dict) else "" for t in raw]
    for k, ti in enumerate(titles, 1):
        if not ti:
            probs.append(f"tip {k}: no title"); continue
        if not 2 <= len(ti.split()) <= 6 or len(ti) > 45:
            probs.append(f"title {k}: {len(ti.split())} words, {len(ti)} chars")
        if ti[0] != ti[0].upper() or re.search(r"[.:?!]$|[:?!]", ti):
            probs.append(f"title {k}: form '{ti}'")
        if re.match(r"(?:Zkus|Nech|Požádej|Popros|Zeptej|Napiš|Zkuste|Poproste|Nechte)\b", ti):
            probs.append(f"title {k}: a command '{ti}'")
    if titles and all(titles) and len({ti.split()[0].lower() for ti in titles}) < len(titles):
        probs.append("two titles start the same way")
    if sum(bool(re.search(r"\b(?:AI|chatbot\w*)\b", ti)) for ti in titles) > 1:
        probs.append("AI/chatbot in more than one title")
    for k, tip in enumerate(lw, 1):
        if not 1 <= sentences(tip) <= 2 or not 60 <= len(tip) <= 260:
            probs.append(f"tip {k}: {sentences(tip)} sentences, {len(tip)} chars")
    if len({tip.split()[0].lower() for tip in lw if tip.split()}) < len(lw):
        probs.append("two tips start the same way")
    both = t + " " + " ".join(lw) + " " + " ".join(titles)
    both_ = re.sub(r"klíčov\w+ slov\w*", "", both)  # "klíčová slova" (keywords) is a term, not the empty word
    probs += [f"'{b.strip()}'" for b in BANNED if b in both_]
    probs += [f"'{m}'" for m in re.findall(r"\w+š (?:sám|sama)\b|\b(?:spletl|spletla) ses?\b", both)]
    if probs:
        bad += 1
        print(f"{s}: {', '.join(probs)}")
print(f"{len(slugs)} cards, {bad} with problems")
