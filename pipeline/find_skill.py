"""Search ESCO skills (Czech labels + descriptions), case/diacritics-insensitive.

    uv run python -I find_skill.py "počít" [--limit 30]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CACHE, fold
from esco_index import load_index

import json

FOLD_CACHE = CACHE / "skills_folded.json"


def folded_skills(idx):
    src = CACHE / "esco_index.json"
    if FOLD_CACHE.exists() and FOLD_CACHE.stat().st_mtime >= src.stat().st_mtime:
        return json.loads(FOLD_CACHE.read_text(encoding="utf-8"))
    out = {u: [fold(s["label"]), fold("\n".join(s["alt"])), fold(s["description"])] for u, s in idx.skills.items()}
    FOLD_CACHE.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--expand", action="store_true",
                    help="also show narrower-skill count and essential occupations incl. narrower skills")
    a = ap.parse_args()
    idx = load_index()
    q = fold(a.query.strip())
    hits = []
    for u, (lab, alt, desc) in folded_skills(idx).items():
        tier = 0 if q in lab else 1 if q in alt else 2 if q in desc else None
        if tier is None:
            continue
        hits.append((tier, -len(idx.essential.get(u, ())), idx.skills[u]["label"], u))
    hits.sort()
    print(f"{len(hits)} matches (showing {min(a.limit, len(hits))}); tier: label < altLabel < description")
    for tier, neg, _, u in hits[: a.limit]:
        s = idx.skills[u]
        extra = ""
        if a.expand:
            extra = (f" | narrower skills {len(idx.expand([u])) - 1}"
                     f" | essential in {len(idx.essential_occupations([u]))} occupations incl. narrower")
        print(f"{u}\n  {s['label']} | {s['skillType']} | {s['reuseLevel']} | essential in {-neg} occupations"
              f" (direct){extra} | match: {('label', 'alt', 'description')[tier]}")


if __name__ == "__main__":
    main()
