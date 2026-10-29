"""How relevant a card's skill is for each occupation that needs it, scored by a decision model (Jev via OpenRouter).

    uv run python -I relevance.py estimate                       # pairs, tokens and cost, no API calls
    uv run python -I relevance.py run [--slugs S ...] [--max-cost 2] [--workers 16]
    uv run python -I relevance.py show SLUG [--n 15]             # ranking for one card, to eyeball

ESCO decides which occupations need a card's skill (essential, incl. narrower skills); the model only judges how much.
Per (card, occupation) pair it answers one question; per occupation one more (asked once, cached):
  use    score 0-4  how much the job uses the skill as pupils learn it (the relevance shown on the card)
  known  score 0-2  a 10-year-old in Czechia knows what the job is (ranking only, never shown)
Scores are probability-weighted means of the levels, so they are continuous (2.7 of 4).

Output, committed so the site build needs no API: content/relevance/<slug>.json
  {"model", "promptVersion", "scores": {occId: {"use": 2.7}}}
(A "core" yes/no question was dropped after the pilot, user 2026-10-19: almost every answer fell between 0.2 and
0.6, so it did not separate jobs. Pilot files may still carry it; it is ignored.)
and content/relevance/_known.json {"model", "promptVersion", "scores": {occId: 1.6}}.
Only missing pairs (or ones of an older promptVersion) are sent. The key comes from $OPENROUTER_API_KEY or
pipeline/.openrouter-key (gitignored).
"""
import argparse
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONTENT, write_json
from esco_index import load_index

MODEL = "typesafe/jev-1.14"
VERSION = "relevance-v1"
URL = "https://openrouter.ai/api/v1/systemone"
OUT = CONTENT / "relevance"
PRICE_PER_TOKEN = 0.042 / 1e6  # OpenRouter list price, input only; output is free

PAIR_QUESTIONS = {
    "use": {
        "type": "score",
        "instructions": "How much does a person in this occupation use this school skill in everyday work? Judge the "
                        "skill as pupils learn it (school_skill and what_pupils_learn), not a loosely related ability.",
        "criteria": [
            "Not at all: the work has nothing to do with it",
            "Rarely: needed now and then, on the side",
            "Sometimes: a regular but small part of the work",
            "Often: used on most working days",
            "Constantly: it is at the core of what this job does",
        ],
    },
}
KNOWN_QUESTION = {
    "known": {
        "type": "score",
        "instructions": "Would a typical 10-year-old child in Czechia know what this job is?",
        "criteria": ["No, they would not know it", "Vaguely, they have heard of it", "Yes, it is a familiar job"],
    },
}


def api_key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY", "").strip()
    f = Path(__file__).resolve().parent / ".openrouter-key"
    if not k and f.exists():
        k = f.read_text(encoding="utf-8").strip()
    if not k:
        sys.exit("No key: set OPENROUTER_API_KEY or put it in pipeline/.openrouter-key")
    return k


def load_cards() -> list[dict]:
    outcomes = json.loads((CONTENT / "rvp" / "outcomes.json").read_text(encoding="utf-8"))
    cards = []
    for p in sorted((CONTENT / "activities").glob("*.json")):
        for a in json.loads(p.read_text(encoding="utf-8")):
            o = outcomes.get(a["outcome"], {})
            cards.append({**a, "_subject": o.get("subject", {}).get("name", ""), "_stage": o.get("stageLabel", "")})
    return cards


def card_state(a: dict) -> dict:
    return {"school_skill": a["title"], "what_pupils_learn": [s["point"] for s in a.get("levelSource", [])],
            "school_subject": a["_subject"], "grade": a["_stage"]}


def occ_state(o: dict) -> dict:
    return {"occupation": o["label"], "occupation_description": o["description"][:700]}


def read(p: Path) -> dict:
    d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return d if d.get("promptVersion") == VERSION and d.get("model") == MODEL else {"scores": {}}


class Client:
    def __init__(self, key: str, max_cost: float):
        self.key, self.max_cost, self.cost, self.tokens, self.lock = key, max_cost, 0.0, 0, threading.Lock()

    def ask(self, state: dict, questions: dict) -> dict:
        body = json.dumps({"model": MODEL, "state": state, "questions": questions}, ensure_ascii=False).encode()
        for attempt in range(6):
            if self.cost >= self.max_cost:
                raise RuntimeError(f"budget of ${self.max_cost} reached")
            req = urllib.request.Request(URL, data=body, headers={
                "Authorization": f"Bearer {self.key}", "Content-Type": "application/json",
                "HTTP-Referer": "https://procsetoucim.internal.quxt.eu", "X-Title": "Proc se to ucim"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    res = json.loads(r.read())
                u = res.get("usage", {})
                with self.lock:
                    self.tokens += u.get("input_tokens", 0)
                    self.cost += u.get("cost") if u.get("cost") is not None else u.get("input_tokens", 0) * PRICE_PER_TOKEN
                return res["answers"]
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 524, 529) and attempt < 5:
                    time.sleep(2 ** attempt)
                    continue
                raise RuntimeError(f"HTTP {e.code}: {e.read()[:300]!r}")
            except (urllib.error.URLError, TimeoutError, ConnectionError):
                if attempt < 5:
                    time.sleep(2 ** attempt)
                    continue
                raise


def plan(idx, cards, slugs=None):
    """Pairs still to score, per card, and occupations still lacking `known`."""
    todo, occs = {}, set()
    for a in cards:
        if slugs and a["slug"] not in slugs:
            continue
        need = idx.essential_occupations([u for u in a.get("escoSkills", []) if u in idx.skills])
        done = read(OUT / f"{a['slug']}.json")["scores"]
        miss = sorted(o for o in need if o not in done)
        if miss:
            todo[a["slug"]] = miss
        occs.update(need)
    known = read(OUT / "_known.json")["scores"]
    return todo, sorted(o for o in occs if o not in known)


def estimate(idx, cards):
    todo, known = plan(idx, cards)
    pairs = sum(len(v) for v in todo.values())
    # Calibrated on the first full run (2026-10-19): ~1.7 characters of this JSON per Jev input token.
    by_card = {a["slug"]: a for a in cards}
    tok = sum(len(json.dumps({"s": {**card_state(by_card[s]), **occ_state(idx.occupations[o])}, "q": PAIR_QUESTIONS},
                             ensure_ascii=False)) // 1.7 for s, os_ in todo.items() for o in os_)
    tok += sum(len(json.dumps({"s": occ_state(idx.occupations[o]), "q": KNOWN_QUESTION}, ensure_ascii=False)) // 1.7 for o in known)
    print(f"{pairs} pairs in {len(todo)} cards, {len(known)} occupations for 'known'")
    print(f"~{tok / 1e6:.1f}M input tokens, ~${tok * PRICE_PER_TOKEN:.2f} at list price ({MODEL})")


def run(idx, cards, slugs, max_cost, workers):
    client = Client(api_key(), max_cost)
    todo, known_todo = plan(idx, cards, slugs)
    by_card = {a["slug"]: a for a in cards}
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"{sum(len(v) for v in todo.values())} pairs in {len(todo)} cards, {len(known_todo)} occupations for 'known'")

    known = read(OUT / "_known.json")
    known["scores"] = dict(known["scores"])
    with ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(client.ask, occ_state(idx.occupations[o]), KNOWN_QUESTION): o for o in known_todo}
        for f in as_completed(futs):
            known["scores"][futs[f]] = round(f.result()["known"]["score"], 3)
    write_json(OUT / "_known.json", {"model": MODEL, "promptVersion": VERSION, "scores": dict(sorted(known["scores"].items()))})

    for n, (slug, occs) in enumerate(todo.items(), 1):
        out = read(OUT / f"{slug}.json")
        scores = dict(out["scores"])
        cs = card_state(by_card[slug])
        with ThreadPoolExecutor(workers) as ex:
            futs = {ex.submit(client.ask, {**cs, **occ_state(idx.occupations[o])}, PAIR_QUESTIONS): o for o in occs}
            for f in as_completed(futs):
                ans = f.result()
                scores[futs[f]] = {"use": round(ans["use"]["score"], 3)}
        write_json(OUT / f"{slug}.json", {"model": MODEL, "promptVersion": VERSION, "scores": dict(sorted(scores.items()))})
        print(f"[{n}/{len(todo)}] {slug}: {len(occs)} pairs, total ${client.cost:.3f}, {client.tokens} tokens")
    print(f"done: ${client.cost:.3f}, {client.tokens} input tokens")


def show(idx, slug, n):
    from esco_index import compute_measures
    a = next(c for c in load_cards() if c["slug"] == slug)
    m = compute_measures(a["escoSkills"], a["outcome"], idx, slug=slug)
    rel = read(OUT / f"{slug}.json")["scores"]
    known = read(OUT / "_known.json")["scores"]
    print(f"{slug}: {a['title']}  (shown on the card: first 4)")
    for i, o in enumerate(m["allOccupations"][:n], 1):
        s = rel.get(o, {})
        print(f"{i:3} use {s.get('use', float('nan')):.2f} "
              f"known {known.get(o, float('nan')):.2f}  {'*' if o in m['topOccupations'][:4] else ' '} {idx.occupations[o]['label']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["estimate", "run", "show"])
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--slugs", nargs="*")
    ap.add_argument("--max-cost", type=float, default=2.0, help="stop when this many dollars are spent (default 2)")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--n", type=int, default=15)
    a = ap.parse_args()
    idx = load_index()
    if a.cmd == "estimate":
        estimate(idx, load_cards())
    elif a.cmd == "run":
        run(idx, load_cards(), set(a.slugs) if a.slugs else None, a.max_cost, a.workers)
    else:
        show(idx, a.slug, a.n)


if __name__ == "__main__":
    main()
