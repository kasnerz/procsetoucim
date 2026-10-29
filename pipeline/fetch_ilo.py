"""Download the ILO GenAI exposure files into data/ilo/ (skips files that already exist)."""
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DATA

BASE = "https://raw.githubusercontent.com/pgmyrek/2025_GenAI_scores_ISCO08/main/"
FILES = ["Final_Scores_ISCO08_Gmyrek_et_al_2025.xlsx", "DATA_DICTIONARY.md"]


def fetch():
    d = DATA / "ilo"
    d.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        p = d / f
        if p.exists() and p.stat().st_size > 0:
            continue
        print("downloading", f)
        with urllib.request.urlopen(BASE + f, timeout=120) as r:
            p.write_bytes(r.read())


if __name__ == "__main__":
    fetch()
