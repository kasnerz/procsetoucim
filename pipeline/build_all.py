"""Run the whole pipeline: uv run python -I build_all.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_esco
import build_labour
import build_rvp
import fetch_ilo
from esco_index import load_index

if __name__ == "__main__":
    fetch_ilo.fetch()
    build_rvp.build()
    build_labour.build()
    load_index()
    build_esco.build()
