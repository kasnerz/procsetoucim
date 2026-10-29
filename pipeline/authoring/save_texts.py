"""Save a batch of drafted card texts and check them (prompts/card-v5.md, Steps 2 and 3).

    uv run python -I authoring/save_texts.py DRAFT.json [--by claude-opus-5-5]

DRAFT.json, one file per subagent batch, so an agent writes all its texts in one go, either
  full texts:  {"<slug>": {"comment": "...", "learnWithAi": [{"title": "...", "text": "..."}, ...]}, ...}
  titles only: {"<slug>": ["title 1", "title 2", "title 3"], ...}  (adds titles to the existing suggestions, in order;
               the texts keep their version, noted as "textsFrom")
Writes content/comments/<slug>.json for every known slug, then runs lint_comments.py on them and prints only the
problems. Rerun after fixing DRAFT.json; it overwrites.
"""
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
VERSION = "comment-v5"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--by", default="claude-opus-5-5")
    a = ap.parse_args()
    draft = json.loads(pathlib.Path(a.draft).read_text(encoding="utf-8"))
    known = {act["slug"] for f in (ROOT / "content" / "activities").glob("*.json")
             for act in json.loads(f.read_text(encoding="utf-8"))}
    unknown = sorted(set(draft) - known)
    if unknown:
        print("unknown slugs (not saved):", " ".join(unknown))
    slugs = [s for s in draft if s in known]
    for s in slugs:
        d, p = draft[s], ROOT / "content" / "comments" / f"{s}.json"
        if isinstance(d, list):
            old = json.loads(p.read_text(encoding="utf-8"))
            tips = [t if isinstance(t, str) else t["text"] for t in old["learnWithAi"]]
            if len(d) != len(tips):
                print(f"{s}: {len(d)} titles for {len(tips)} suggestions (not saved)")
                continue
            out = {"draftedBy": old["draftedBy"], "promptVersion": VERSION,
                   "textsFrom": old.get("textsFrom", old["promptVersion"]), "comment": old["comment"],
                   "learnWithAi": [{"title": t.strip(), "text": x} for t, x in zip(d, tips)]}
        else:
            out = {"draftedBy": a.by, "promptVersion": VERSION, "comment": d["comment"].strip(),
                   "learnWithAi": [{"title": t["title"].strip(), "text": t["text"].strip()} for t in d["learnWithAi"]]}
        p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not slugs:
        return
    r = subprocess.run([sys.executable, "-I", str(ROOT / "pipeline" / "authoring" / "lint_comments.py"), "--slugs", *slugs],
                       capture_output=True, text=True)
    print(f"saved {len(slugs)}")
    print(r.stdout.strip() or r.stderr.strip())


if __name__ == "__main__":
    main()
