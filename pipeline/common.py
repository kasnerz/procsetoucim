"""Shared paths and helpers for the pipeline."""
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
CONTENT = ROOT / "content"
CACHE = DATA / "cache"
RVP_JSON = DATA / "rvp" / "data_final_rvp_zv_full_mp_20251216.json"

CEDEFOP_CITATION = (
    "European Centre for the Development of Vocational Training (Cedefop). "
    "Cedefop Skills Forecast 2026, Thessaloniki: Greece, "
    "Downloaded from: https://www.cedefop.europa.eu/en/projects/skills-forecast"
)


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size:,} B)")


def read_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


_BLOCK = {"p", "li", "ul", "ol", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "table"}
_SPACES = dict.fromkeys(map(ord, "           "), " ")
_SPACES.update(dict.fromkeys(map(ord, "​﻿­"), None))


class _Stripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in _BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in _BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def clean_text(s: str) -> str:
    s = s.replace("&nbsp;", " ").translate(_SPACES)
    return re.sub(r"[ \t]+", " ", s)


def html_to_text(html: str | None) -> str:
    """Strip HTML to plain text; paragraph/list/br boundaries become single newlines."""
    if not html:
        return ""
    p = _Stripper()
    p.feed(html)
    p.close()
    text = clean_text("".join(p.parts))
    lines = [ln.strip() for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def fold(s: str) -> str:
    """Lowercase and strip diacritics for searching."""
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))
