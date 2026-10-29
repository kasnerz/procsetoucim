# Content schema

The pipeline (`pipeline/`, Python, run with `uv run`) writes JSON into `content/`. The Astro site (`site/`) only reads `content/`. Hand-written and AI-drafted content lives in `content/activities/` and is never overwritten by the pipeline.

## Hand/AI-written

### `content/activities/<outcome-code-lowercase>.json`

One file per RVP outcome, array of cards. Written by `pipeline/authoring/build_cards.py` from `pipeline/authoring/cards/<outcome>.json` (method: `docs/activity-method.md`).

```jsonc
[
  {
    "slug": "pisemne-nasobeni",            // unique across the site, ascii, used in /aktivita/<slug>
    "title": "Písemné násobení",           // simplified RVP point, noun phrase
    "aliases": ["násobení pod sebou"],      // how kids/parents phrase it, for search
    "outcome": "MAT-MAT-001-ZV5-001",       // exactly one new-RVP outcome
    "levelSource": [                         // the official points this card simplifies
      { "level": "Na cestě", "point": "<the full line of the level description>", "quote": "<the part used, = point when whole>" }
    ],
    "rules": ["P1", "P3"],                   // simplification rules applied (P1 always)
    "inspiration": [{ "title": "Slovní úlohy z reálného světa", "url": "" }],  // RVP illustrations (optional)
    "tools": {
      "chatbot":  { "verdict": "pomuze|nepomuze", "why": "one sentence, may name concrete tools" },
      "internet": { "verdict": "...", "why": "..." },
      "aplikace": { "verdict": "...", "why": "..." },
      "klasicky": { "verdict": "...", "why": "..." }
    },
    "escoSkills": ["http://data.europa.eu/esco/skill/..."],  // 1–4 skill URIs
    "review": { "draftedBy": "claude-opus-5-5", "promptVersion": "cards-v1", "reviewed": false }
  }
]
```

### `content/coverage/<outcome-code-lowercase>.json`

Every point of a covered outcome and what became of it (written by the same authoring script, which fails on gaps).

```jsonc
{ "outcome": "CJS-CJS-001-ZV5-002", "promptVersion": "cards-v1",
  "points": [ { "level": "Na cestě", "point": "Pracuje s legendou a směrovou růžicí.", "cards": ["legenda-a-meritko"], "aside": null },
              { "level": "Minimální doporučená úroveň", "point": "…", "cards": [], "aside": { "code": "O3", "refs": [] } } ] }
```

### `content/comments/<slug>.json`

The two AI texts of a card (prompt `pipeline/authoring/prompts/card-v5.md`, drafted after the numbers exist).

```json
{ "draftedBy": "claude-opus-5-5", "promptVersion": "comment-v5",
  "comment": "Proč se to učíš: 3–5 sentences, why it is in the curriculum and what it is good for",
  "learnWithAi": [{ "title": "Short noun phrase, 2–5 words", "text": "Jak se to učit s AI: 1–2 sentences" }, "…", "…"] }
```

`textsFrom` (e.g. `comment-v4`) marks files where only the titles were added later and the texts keep that version.

### `content/jobnotes/<slug>.json`

AI notes on how each of a card's top occupations uses it (drafted by Sonnet subagents from ESCO descriptions; prompt in the session scratchpad, version `jobnotes-v1`).

```jsonc
{ "draftedBy": "claude-sonnet-5-5", "promptVersion": "jobnotes-v1", "notes": { "<occupation uuid>": "1–2 sentences, 80–220 chars" } }
```

## Pipeline-generated

### `content/rvp/outcomes.json`

All outcomes from the new RVP JSON (subjects, literacies, key competences, cross-curricular themes).

```jsonc
{
  "MAT-MAT-001-ZV5-001": {
    "code": "MAT-MAT-001-ZV5-001",
    "kind": "obor|gramotnost|kompetence|prurezove",
    "area": { "code": "MAT", "name": "Matematika a její aplikace" },
    "subject": { "code": "MAT", "name": "Matematika" },       // for non-subject kinds: the literacy/competence/theme
    "okruh": { "code": "1", "name": "Číslo a početní operace" },  // null if none
    "stage": "ZV3|ZV5|ZV9",
    "stageLabel": "do konce 5. třídy",
    "text": "Řeší problémy s přirozenými čísly…",
    "rationale": "plain text of popisAZduvodneni",
    "levels": [ { "name": "Na začátku", "text": "plain text" } ],   // in RVP order
    "illustrations": [ { "level": "Splněno", "title": "...", "text": "plain text", "url": "" } ],
    "prev": ["..."], "next": ["..."], "related": ["..."],
    "url": "https://prohlednout.rvp.cz/ovu/mat-mat-001-zv5-001",
    "graph": {
      "foundationCount": 0,   // number of distinct outcomes reachable transitively via `next`
      "transferCount": 0,     // related outcomes that are key competences or literacies (K*, ZG*)
      "transfer": ["KKK-VYJ-000-ZV5-001"]
    }
  }
}
```

### `content/rvp/structure.json`

Areas → subjects → okruhy → outcome codes, in RVP order, plus literacies / competences / themes. Used for navigation.

### `content/esco/occupations.json`

Only occupations reachable from skills referenced in `content/activities/` (keeps the site small).

```jsonc
{
  "<uuid>": {
    "id": "<uuid>", "uri": "...",
    "label": "účetní",                  // Czech preferred label, readable (split "x/y" forms into masculine/feminine)
    "labelAlt": ["..."], "description": "Czech description",
    "isco4": "2411", "isco2": "24",
    "ilo": { "score": 0.41, "gradient": "Gradient 2" } // from ILO 2025 (potential25), null if missing
  }
}
```

### `content/esco/skills.json`

Skills referenced in activities: `{ uri: { uri, label, description, essentialFor: [occupation ids], optionalFor: count } }`.

### `content/labour/isco2.json` (derived from Cedefop; aggregates only, never raw rows)

```jsonc
{
  "24": { "code": "24", "label": "Business and administration professionals (Czech label if available)",
          "employment2025": 123000, "employment2035": 130000, "changePct": 5.7,
          "reliable": true }   // false if either value < 10,000 (Cedefop caution rule)
}
```

### `content/activity-occupations.json`

`{ "<slug>": ["<occupation uuid>", ...] }`: every ESCO occupation that needs one of the card's skills (or a narrower one) as essential, ordered like `topOccupations` (direct first, then large ISCO-2 groups) without the per-group cap.

### `content/measures/<slug>.json` or one `content/measures.json`

Per activity, computed from its `escoSkills`:

```jsonc
{
  "pisemne-nasobeni": {
    "occupationCount": 412,          // ESCO occupations with at least one of the skills as essential
    "employmentShare": 0.38,         // Σ_isco2 employment2025 × (share of ESCO occupations in that group needing the skill) / total CZ employment
    "highExposureShare": 0.12,       // part of that employment in occupations with ILO gradient 3–4
    "trendPct": 2.1,                 // employment-weighted Cedefop change 2025→2035 across those groups (indicative)
    "topOccupations": ["<uuid>", "..."],  // 8 most specific: occupations where the skill is a large share of their essential skills
    "employment": 2059000,           // the weighted employment itself (people, 2025), rounded to hundreds
    "byMajor": {"2": 0.07, "4": 0.05},   // share of total CZ employment per ISCO-1 major group, same weights
    "exposureMix": {"high": 0.12, "medium": 0.4, "low": 0.3, "none": 0.18},  // ILO buckets of the matched weights
    "foundationCount": 7, "transferCount": 3   // copied from the outcome's graph
  }
}
```

### `content/meta.json`

Build date, source versions, citations (exact Cedefop citation string from `docs/data-terms.md`).
