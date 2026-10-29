"""Save a batch of drafted occupation notes and check them (prompts/jobnotes-v2.md).

    uv run python -I authoring/save_jobnotes.py DRAFT.json [--by claude-sonnet-5-5]

DRAFT.json: {"<slug>": {"<occupation id>": "<note>", ...}, ...}, one file per subagent batch. Merges the notes into
content/jobnotes/<slug>.json (notes already there stay), then checks the new notes and that every current top
occupation of these cards has one. Prints only problems. Rerun after fixing DRAFT.json; it overwrites its own notes.
"""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
C = ROOT / "content"
VERSION = "jobnotes-v2"
BANNED = ["nejen", "nejde o", "nejde jen", "klíčov", "zásadní", "nedílн", "efektivn", "v dnešní době", "!", " – ", " — ",
          "ESCO", "ChatGPT", "naučil", "naučila"]


def sentences(t):
    return len(re.findall(r"[.?!](?:\s|$)(?=[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ0-9]|$)", t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--by", default="claude-sonnet-5-5")
    a = ap.parse_args()
    draft = json.loads(pathlib.Path(a.draft).read_text(encoding="utf-8"))
    measures = json.loads((C / "measures.json").read_text(encoding="utf-8"))
    probs, saved = [], 0
    for slug, notes in draft.items():
        if slug not in measures:
            probs.append(f"{slug}: unknown card"); continue
        p = C / "jobnotes" / f"{slug}.json"
        cur = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"notes": {}}
        merged = {**cur["notes"], **{k: v.strip() for k, v in notes.items()}}
        p.write_text(json.dumps({"draftedBy": a.by, "promptVersion": VERSION, "notes": merged}, ensure_ascii=False, indent=1) + "\n",
                     encoding="utf-8")
        saved += len(notes)
        top = measures[slug]["topOccupations"][:8]
        missing = [o for o in top if o not in merged]
        if missing:
            probs.append(f"{slug}: no note for {', '.join(missing)}")
        for o, t in notes.items():
            if o not in top:
                probs.append(f"{slug}/{o}: not a current top occupation")
            q = []
            if not 1 <= sentences(t) <= 2:
                q.append(f"{sentences(t)} sentences")
            if not 60 <= len(t) <= 260:
                q.append(f"{len(t)} chars")
            q += [f"'{b.strip()}'" for b in BANNED if b in re.sub(r"klíčov\w+ slov\w*", "", t)]
            q += [f"'{m}'" for m in re.findall(r"\b(?:sám|sama|mu|nepoškodil|naučil\w*)\b", t, re.I)]  # gendered forms
            if q:
                probs.append(f"{slug}/{o}: {', '.join(q)}")
    print(f"saved {saved} notes")
    print("\n".join(probs) if probs else "0 problems")


if __name__ == "__main__":
    main()
