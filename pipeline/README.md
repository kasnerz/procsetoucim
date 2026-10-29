# Pipeline

Python (uv). Reads `data/` (raw sources, not in git; the RVP JSON is `data/rvp/data_final_rvp_zv_full_mp_20251216.json`), writes `content/` (see `docs/content-schema.md`).

```
cd pipeline
uv sync
uv run python -I build_all.py          # everything (downloads ILO files into data/ilo/ if missing)
uv run python -I find_skill.py "počít" --limit 30   # search ESCO skills
```

`-I` is required in practice only for safety (no script dir / env on sys.path); entry scripts add their own directory to `sys.path`. Nothing from `data/` is executed. The Cedefop zip is read with `zipfile`, never extracted.

## Modules and outputs

| File | Output |
|---|---|
| `build_rvp.py` | `content/rvp/outcomes.json` (475 outcomes: 362 obory, 24 gramotnosti, 66 kompetence, 23 průřezová), `content/rvp/structure.json` |
| `build_labour.py` | `content/labour/isco2.json` (Czechia, ISCO-08 2-digit, 40 groups) |
| `esco_index.py` | library: ESCO + ILO index (cache `data/cache/esco_index.json`, rebuilt when sources change), `load_index()`, `compute_measures(skill_uris, outcome_code)` |
| `build_esco.py` | reads `content/activities/*.json` (missing/empty is fine, bad files are skipped with a warning); writes `content/esco/occupations.json`, `content/esco/skills.json`, `content/measures.json`, `content/meta.json` |
| `find_skill.py` | CLI skill search (label, then altLabel, then description; diacritics/case-insensitive; within a tier sorted by number of occupations where essential) |
| `fetch_ilo.py` | downloads ILO xlsx + data dictionary |

`structure.json`: `{areas: [{code,name,subjects:[{code,name,okruhy:[{code,name,outcomes:[codes]}]}]}], literacies|competences|themes: [{code,name,components:[{code,name,outcomes}],outcomes}]}`. Order is RVP order. Outcomes sit in `components` (slozky) when they exist, in `outcomes` otherwise (themes).

## Outcomes: text, areas

HTML is stripped with `html.parser`; `p/li/ul/br/div/h*` boundaries become a single `\n`, entities decoded, nbsp/thin/narrow spaces turned into plain spaces. `levels` follow `urovneMetodickePodpory` order in the data (Minimální doporučená úroveň, Splněno, Na začátku, ...); illustrations are flattened with their level name. For non-subject kinds: `area` is a synthetic group (ZG "Základní gramotnosti", KK "Klíčové kompetence", PT "Průřezová témata"), `subject` the literacy/competence/theme, `okruh` the component (slozka) or null.

## prev / next direction (important)

In the source, `predchazejici...` and `nasledujici...` are not usable as given. Measured over all 475 outcomes:

- ZV5 outcomes list ZV9 outcomes as predchazejici (161x) and as nasledujici (177x); ZV9 outcomes likewise list ZV5 ones in both lists.
- The relation is mutual: if A lists B as predchazejici, B lists A as predchazejici too (322/322 resolvable cases); the same holds for nasledujici (354/354). So the two lists do not encode direction.
- Content check: ZV5 "Monitoruje své procesy učení" vs ZV9 "Řídí vlastní procesy učení"; ZV5 "popisuje působení autora na čtenáře" vs ZV9 "posuzuje autorské záměry" - ZV9 clearly builds on ZV5.
- nasledujici also holds codes `...-PV1-...` (later, post-ZV stage) that are not in the ZV file.

Rule used: take the union of both lists as an undirected gradation link, orient by stage (ZV3 < ZV5 < ZV9). `next` = linked outcomes of a later stage (build on this one), `prev` = linked outcomes of an earlier stage (this builds on them). Same-stage links do not occur. Codes not in the file (PV1 etc., 259 link entries) are dropped. `foundationCount` = distinct outcomes reachable transitively via `next` (max 8). `related` keeps only codes present in the file. `transfer` = related outcomes whose code starts with `K` or `ZG` (competences and literacies).

## Labour (Cedefop)

`Employment_occupation_detail.xlsx` (sheet Data, "Czech Republic") is the most detailed occupation breakdown that includes Czechia: ISCO-08 2-digit, 40 groups with data (41 incl. group 95, empty). Total employment 2025 (sum of groups) = 5 419 000. Labels from ESCO `ISCOGroups_cs.csv`. `reliable` = both 2025 and 2035 >= 10 000 (groups 14, 63, 95 are not). `changePct` is null when 2025 is 0. 2025 and 2035 are forecasts (last historical year 2023). Only aggregated per-group numbers are written; raw rows, files and the zip never leave `data/`. Cite with the exact string in `content/meta.json` (`citations.cedefop`); figures are indicative only. Armed forces (ISCO 0) are not in the Cedefop table, so ESCO occupations in group 01-03 never carry weight.

## ESCO and ILO

- ESCO cs CSVs are read with the `csv` module (embedded newlines). The source has a few duplicate URIs (3043 occupation rows -> 3039 unique, 13960 skill rows -> 13939); the last row wins.
- Occupation `label`: preferred label split on `/`, de-duplicated, joined with ", " (`lékař, lékařka`; identical forms collapse to one). `labelAlt` = altLabels not already in the label. Long occupation names therefore give long labels.
- ILO: per ISCO-08 4-digit, `score` = `mean_score_2025`, `gradient` = `potential25` without the "Exposed: " prefix. Strings in the data: `Gradient 1`..`Gradient 4`, `Minimal Exposure`, `Not Exposed`. ESCO `iscoGroup` is joined on the 4-digit code; no fallback to coarser levels, so unmatched occupations get `ilo: null` (2956 of 3039 matched, as ILO covers 427 of ~430 ISCO unit groups only partially).

## Measures (`compute_measures`)

- Skill expansion: every referenced skill is expanded to itself plus all transitive narrower skills from `broaderRelationsSkillPillar_cs.csv` (only `KnowledgeSkillCompetence` rows, no SkillGroups). An occupation needs the activity if any skill in the expanded set is *essential* for it. Needed because transversal skills such as "provádět výpočty" have almost no direct occupation links. `skills.json`: `essentialFor` = expanded, `essentialForDirect` = direct only, `narrowerCount` = number of descendants. `find_skill.py --expand` prints both counts. The `topOccupations` ratio also uses the expanded set.
- `occupationCount`: ESCO occupations having at least one skill of the expanded set as *essential*.
- `employmentShare`: for each ISCO-2 group, employment2025 x (needing occupations in group / all ESCO occupations in group), summed, divided by the sum of all groups' employment2025. This assumes employment is spread evenly over ESCO occupations of a group (ESCO occupations are not weighted by real size) - it is an indicator, not a headcount.
- `highExposureShare`: same weights, restricted to occupations with Gradient 3 or 4, divided by the weight of needing occupations that have an ILO match (unmatched ones are left out of the denominator). Null if none matched.
- `trendPct`: same weights applied to group employment2035 / employment2025, as a percentage.
- `topOccupations`: 8 occupations by (essential skills in the set / all essential skills of the occupation), desc; ties by label, then id. Occupations with very few essential skills therefore rank high; this is by the schema's definition.
- `foundationCount`, `transferCount` copied from the outcome's `graph` (0 if the outcome is unknown).

## Occupation relevance (`relevance.py`)

ESCO says which occupations need a card's skill; a decision model (Jev 1.14 via OpenRouter, ~$0.5 for all cards) judges
how much each of them uses it (`use`, 0-4) and, once per occupation,
whether a 10-year-old knows the job (`known`). Results are committed in `content/relevance/`; `compute_measures` then
orders occupations by them and drops jobs with `use` < 1 from the examples. Only missing pairs are sent.

```bash
uv run python -I relevance.py estimate                    # pairs, tokens, cost; no key needed
uv run python -I relevance.py run --slugs SLUG ... --max-cost 0.2
uv run python -I relevance.py show SLUG                   # eyeball one card
uv run python -I build_esco.py                            # re-rank with the scores
```
Key: `$OPENROUTER_API_KEY` or `pipeline/.openrouter-key` (gitignored). Job notes follow the top occupations, so
re-ranking can leave new top jobs without a note (`authoring/jobnote_inputs.py --missing`).

## Caveats

- ESCO skill labels are Czech machine/human translations; the relations file only has English labels, so joins use URIs.
- Reachable occupations in `content/esco/occupations.json` = those with a referenced skill as essential, plus any `topOccupations` (a subset of the same).
- Remind before public launch: inform Cedefop (skills-forecast@cedefop.europa.eu), see `docs/data-terms.md`.

## Cards (authoring)

Order when cards change (each drafting step is done by AI subagents with a prompt from `authoring/prompts/`):

```
uv run python -I authoring/show_outcome.py CODE           # goal, points, illustrations, linked cards
#   draft authoring/cards/<code>.json                     (prompts/cards-v2.md)
uv run python -I authoring/build_cards.py --check CODE    # validate one goal, write nothing
uv run python -I authoring/build_cards.py                 # validate all, write content/activities + coverage
uv run python -I build_all.py                             # numbers, occupations
uv run python -I authoring/jobnote_inputs.py DIR --missing    # then draft content/jobnotes (prompts/jobnotes-v2.md, jobnote-writer agents)
uv run python -I authoring/comment_inputs.py DIR --missing --by-goal --size 20   # batches must stay under ~40 KB so an agent reads each in one go; then tools + texts (prompts/card-v5.md; texts by Opus card-writer agents, each saves its draft with authoring/save_texts.py)
uv run python -I authoring/lint_cards.py; uv run python -I authoring/lint_comments.py
```

`build_cards.py` asserts the method in `docs/activity-method.md` (quotes match exactly one RVP point, rules P1–P5,
every point covered or set aside, known ESCO skills, unique slugs, O1 refs exist).
