"""Cedefop Skills Forecast 2026 -> content/labour/isco2.json (aggregates for Czechia only).

Per ISCO-08 2-digit group: employment 2025 and 2035, job openings 2026-2035 (Cedefop's definition: expansion demand,
the change in employment, plus replacement demand, people leaving the group) and employment by qualification in 2035."""
import csv
import io
import sys
import zipfile
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CONTENT, DATA, write_json

ZIP = DATA / "cedefop" / "cedefopskillsforecast2026.zip"
MEMBER = "Employment_occupation_detail.xlsx"
REPLACEMENT = "Replacement_demand_occupation_detail.xlsx"
QUALIFICATION = "Employment_occupation_detail_qualification.xlsx"
QUAL_KEYS = {"4 High": "high", "3 Medium_vocational": "mediumVocational", "2 Medium_general": "mediumGeneral", "1 Low": "low"}
COUNTRY = "Czech Republic"
RELIABLE_MIN = 10_000


def isco2_labels_cs() -> dict[str, str]:
    out = {}
    with open(DATA / "esco" / "ISCOGroups_cs.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if len(r["code"]) == 2:
                out[r["code"]] = r["preferredLabel"].strip()
    return out


def _sheet(z: zipfile.ZipFile, member: str) -> list[tuple]:
    wb = openpyxl.load_workbook(io.BytesIO(z.read(member)), read_only=True, data_only=True)
    return list(wb["Data"].iter_rows(values_only=True))


def _code(c) -> str | None:
    if c is None or str(c).strip().lower() == "total":
        return None
    return str(int(c)).zfill(2)


def build():
    with zipfile.ZipFile(ZIP) as z:
        rows = _sheet(z, MEMBER)
        rep_rows = _sheet(z, REPLACEMENT)
        qual_rows = _sheet(z, QUALIFICATION)
    rh = list(rep_rows[0])
    replacement = {_code(r[2]): sum(r[rh.index(y)] or 0 for y in range(2026, 2036))
                   for r in rep_rows[1:] if r[0] == COUNTRY and _code(r[2])}
    qh = list(qual_rows[0])
    qual = {}
    for r in qual_rows[1:]:
        if r[0] == COUNTRY and _code(r[2]) and r[3] in QUAL_KEYS:
            qual.setdefault(_code(r[2]), {})[QUAL_KEYS[r[3]]] = int(round(r[qh.index(2035)] or 0))
    head = list(rows[0])
    i25, i35 = head.index(2025), head.index(2035)
    labels = isco2_labels_cs()
    out, total25 = {}, 0
    for r in rows[1:]:
        if r[0] != COUNTRY:
            continue
        code = r[2]
        if code is None or str(code).strip().lower() == "total":
            continue
        code = str(int(code)).zfill(2)
        e25, e35 = int(round(r[i25] or 0)), int(round(r[i35] or 0))
        total25 += e25
        out[code] = {
            "code": code,
            "label": labels.get(code) or r[1],
            "employment2025": e25,
            "employment2035": e35,
            "changePct": round((e35 / e25 - 1) * 100, 1) if e25 > 0 else None,
            "reliable": e25 >= RELIABLE_MIN and e35 >= RELIABLE_MIN,
            "replacement2026to2035": int(round(replacement.get(code, 0))),
            "openings2026to2035": int(round(replacement.get(code, 0))) + e35 - e25,
            "qualification2035": {k: qual.get(code, {}).get(k, 0) for k in QUAL_KEYS.values()},
        }
    out = dict(sorted(out.items()))
    write_json(CONTENT / "labour" / "isco2.json", out)
    print(f"Czechia: {len(out)} ISCO-08 2-digit groups, employment 2025 = {total25:,}, "
          f"unreliable groups: {[c for c, v in out.items() if not v['reliable']]}")
    return out


if __name__ == "__main__":
    build()
