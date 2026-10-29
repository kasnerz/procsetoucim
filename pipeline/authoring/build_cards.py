"""Card sources (authoring/cards/<outcome>.json) -> content/activities/<outcome>.json + content/coverage/<outcome>.json.

Each card is a simplified RVP point. The method (docs/activity-method.md) in short:
  P1 zkrácení      the point becomes a short name of what you do
  P2 běžná slova   technical wording replaced by plain words (or explained in the name)
  P3 rozdělení     a point with several activities is split when tools would rate them differently
  P4 sloučení      points of the same goal that describe the same thing (or its simpler step) are merged
  P5 příklady      a concrete example in the name must appear in the RVP point or in an RVP illustration title
Every point of a covered goal is either turned into card(s) or set aside with a reason:
  O1 the same point is covered under another goal (refs = card slugs)
  O2 an attitude or way of learning, not something you do
  O3 a summary of the whole goal; the concrete things are in its other points

The comment shown on a card ("Komentář") is drafted in a separate pass after the occupation numbers exist
(authoring/prompts/card-v5.md -> content/comments/<slug>.json).

Run: uv run python -I authoring/build_cards.py               validate all sources, write content/
     uv run python -I authoring/build_cards.py --check CODE..  validate only these outcomes, write nothing
     (other sources are read only for slugs; unreadable ones are skipped, so parallel drafting is safe)
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
from esco_index import compute_measures, load_index  # noqa: E402

SRC = pathlib.Path(__file__).resolve().parent / "cards"
OUT = ROOT / "content" / "activities"
COV = ROOT / "content" / "coverage"
OUTCOMES = json.loads((ROOT / "content" / "rvp" / "outcomes.json").read_text(encoding="utf-8"))

RULES = {"P1", "P2", "P3", "P4", "P5"}
TOOLS = ("chatbot", "internet", "aplikace", "klasicky")
VERDICTS = {"pomuze", "nepomuze"}  # tools-v2: binary (no tool does it for you)
LEVEL_ORDER = ["Na začátku", "Na cestě", "Splněno", "Minimální doporučená úroveň"]


def points_of(outcome):
    """RVP points of an outcome: one per non-empty line of each level description."""
    out = []
    for l in OUTCOMES[outcome]["levels"]:
        for line in l["text"].split("\n"):
            if line.strip():
                out.append((l["name"], line.strip()))
    return out


def card(src, c, skills):
    outcome = src["outcome"]
    slug = c["slug"]
    pts = points_of(outcome)
    ls = []
    for s in c["sources"]:
        hits = [p for lv, p in pts if lv == s["level"] and s["quote"] in p]
        assert len(hits) == 1, f"{slug}: {s['level']} quote matches {len(hits)} points: {s['quote']!r}"
        ls.append({"level": s["level"], "point": hits[0], "quote": s["quote"]})
    assert set(c["rules"]) <= RULES and "P1" in c["rules"], f"{slug}: bad rules {c['rules']}"
    ill = {i["title"]: i["url"] for i in OUTCOMES[outcome]["illustrations"] if i["title"]}
    insp = []
    for t in c.get("inspiration", []):
        assert t in ill, f"{slug}: illustration {t!r} not in {outcome}"
        insp.append({"title": t, "url": ill[t]})
    assert set(c["tools"]) == set(TOOLS), f"{slug}: tools must be exactly {TOOLS}"
    for t in TOOLS:
        v = c["tools"][t]
        assert v["verdict"] in VERDICTS and v["why"].strip(), f"{slug}: bad tool {t}: {v}"
    assert c["skills"], f"{slug}: no ESCO skills"
    for u in c["skills"]:
        assert u in skills, f"{slug}: unknown ESCO skill {u}"
    assert c["title"].strip() and c["aliases"], f"{slug}: title and aliases required"
    return {
        "slug": slug,
        "title": c["title"],
        "aliases": c["aliases"],
        "outcome": outcome,
        "levelSource": ls,
        "rules": c["rules"],
        "inspiration": insp,
        "tools": {t: {"verdict": c["tools"][t]["verdict"], "why": c["tools"][t]["why"]} for t in TOOLS},
        "escoSkills": c["skills"],
        "review": {"draftedBy": src["draftedBy"], "promptVersion": src["promptVersion"], "reviewed": src.get("reviewed", False)},
    }


def main():
    check = [c.upper() for c in sys.argv[sys.argv.index("--check") + 1:]] if "--check" in sys.argv else None
    idx = load_index()
    skills = idx.skills
    sources = []
    for p in sorted(SRC.glob("*.json")):
        try:
            sources.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError as e:
            if check is None or p.stem.upper() in check:
                sys.exit(f"{p.name}: invalid JSON: {e}")
    if check is not None:
        for c in check:
            assert any(s["outcome"] == c for s in sources), f"no source for {c} in {SRC}"
    errors = []
    built = {}
    for src in sources:
        code = src["outcome"]
        assert code in OUTCOMES, f"unknown outcome {code}"
        assert code not in built, f"two sources for {code}"
        try:
            built[code] = [card(src, c, skills) for c in src["cards"]]
        except AssertionError as e:
            errors.append(f"{code}: {e}")
    slugs = [a["slug"] for acts in built.values() for a in acts]
    dup = {s for s in slugs if slugs.count(s) > 1}
    if dup:
        errors.append(f"duplicate slugs: {sorted(dup)}")

    coverage = {}
    for src in sources:
        code = src["outcome"]
        if code not in built:
            continue
        aside = src.get("aside", [])
        try:
            for x in aside:
                assert x["code"] in {"O1", "O2", "O3"} and (x["code"] != "O1" or x["refs"]), f"bad aside {x}"
                for r in x.get("refs", []):
                    assert r in slugs, f"aside ref {r} unknown"
            rows = []
            for level, point in points_of(code):
                cards = [a["slug"] for a in built[code] if any(s["level"] == level and s["point"] == point for s in a["levelSource"])]
                sk = [x for x in aside if x["level"] == level and point.startswith(x["start"])]
                assert not (cards and sk), f"point both covered and set aside: {point[:60]}"
                assert cards or sk, f"point not covered: [{level}] {point}"
                assert len(sk) <= 1, f"point set aside twice: {point[:60]}"
                rows.append({"level": level, "point": point, "cards": cards,
                             "aside": {"code": sk[0]["code"], "refs": sk[0].get("refs", [])} if sk else None})
            rows.sort(key=lambda r: LEVEL_ORDER.index(r["level"]))
            coverage[code] = {"outcome": code, "promptVersion": src["promptVersion"], "points": rows}
        except AssertionError as e:
            errors.append(f"{code}: {e}")

    if check is not None:
        errors = [e for e in errors if e.split(":")[0] in check or e.startswith("duplicate")]
        if errors:
            print("\n".join(errors), file=sys.stderr)
            sys.exit(1)
        for c in check:
            print(f"{c}: OK, {len(built[c])} cards, {len(coverage[c]['points'])} points, "
                  f"{sum(1 for p in coverage[c]['points'] if p['aside'])} set aside")
            print("  top occupations per card (check they really use the card; if not, change the skills):")
            for a in built[c]:
                m = compute_measures(a["escoSkills"], c, idx)
                top = ", ".join(idx.occupations[i]["label"][:45] for i in m["topOccupations"][:5])
                print(f"  {a['slug']}: {m['occupationCount']} occupations; {top}")
        return
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    OUT.mkdir(parents=True, exist_ok=True)
    COV.mkdir(parents=True, exist_ok=True)
    for d in (OUT, COV):
        for p in d.glob("*.json"):
            if p.stem.upper() not in built:
                p.unlink()
    for code, acts in built.items():
        (OUT / f"{code.lower()}.json").write_text(json.dumps(acts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (COV / f"{code.lower()}.json").write_text(json.dumps(coverage[code], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_pts = sum(len(c["points"]) for c in coverage.values())
    n_aside = sum(1 for c in coverage.values() for p in c["points"] if p["aside"])
    print(f"wrote {len(slugs)} activities in {len(built)} outcomes; {n_pts} RVP points, {n_aside} set aside")


if __name__ == "__main__":
    main()
