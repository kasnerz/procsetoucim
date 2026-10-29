# Prompt cards-v1: turning an RVP goal into cards

**Replaced by `cards-v2.md` (2026-10-20, binary tool verdicts).** Kept as the record of how the first 40 goals were drafted.

Used by: subagents drafting `pipeline/authoring/cards/<outcome>.json`. Method: `docs/activity-method.md`.
Validator: `authoring/build_cards.py --check CODE`. Comments are not part of this step (see `comment-v2.md`).

---

## Context

Website "Proč se to učím?" (Czech, for elementary-school kids aged about 8–15 and their parents). It takes what kids
learn in the new Czech curriculum (RVP ZV) and, for each concrete thing, shows whether tools can do it for you, and
which occupations need it (ESCO). A **card** is one concrete thing a kid learns, simplified from one or more
**points** of the curriculum. Every point of a goal must end up in a card or be set aside with a reason.

## Your job

For each goal (outcome) code given to you:

1. Print it: `cd /home/zdenek/projects/rvp/pipeline && uv run python -I authoring/show_outcome.py CODE`
   It lists the goal, its points per level (each line = one point), illustration titles and cards that already
   exist in linked goals.
2. Read two finished examples to match their style and granularity:
   `pipeline/authoring/cards/mat-mat-001-zv5-001.json` and `pipeline/authoring/cards/jjk-cjl-001-zv5-003.json`.
3. Decide the cards (rules below), choose ESCO skills, write the source file
   `/home/zdenek/projects/rvp/pipeline/authoring/cards/<code lowercased>.json`.
4. Validate: `uv run python -I authoring/build_cards.py --check CODE` and fix until it prints OK. It also prints the
   top occupations per card: if they plainly do not use the activity, pick better skills.
   Never run `build_cards.py` without `--check` and never edit other goals' files.

## Simplification rules (record the ones you apply in `rules`)

- **P1 Zkrácení** (always): the point becomes a short name of what the kid does. A noun phrase, 2–8 words, Czech,
  e.g. "Písemné dělení", "Legenda, měřítko a směrová růžice", "Kontrola vlastního textu". Nothing is added.
- **P2 Běžná slova**: technical wording replaced by plain words a 10-year-old understands ("regiony Česka" → "kraje
  Česka"). Subject terms that are themselves the learning content stay (zlomek, legenda, podmět).
- **P3 Rozdělení**: a point listing several activities is split into several cards when the four tools would rate them
  differently. **Split until uniform**: within one card, each tool's verdict must hold for everything the card asks.
  A calculator does "sčítání záporných čísel", it does not do "modeluje záporná čísla pomocí reálných situací".
- **P4 Sloučení**: points of the same goal that describe the same thing, or its simpler step at a lower level, are merged
  into one card (list every merged point in `sources`).
- **P5 Příklady jen z RVP**: a concrete example in the card name must appear in the source point or in an illustration
  title of that goal (put the illustration title in `inspiration`).

Aim for cards a kid recognises as "that's what we do in class". Typical goal: 4–10 cards. Do not make a card from a
point that only repeats another one; merge it (P4) or set it aside.

## Setting a point aside (`aside`)

- **O1**: the same point is already covered by a card under another goal (`refs` = those card slugs; see "Existing
  cards in linked goals"). Use it where a 9th-grade goal repeats a 5th-grade point.
- **O2**: it describes an attitude, a feeling or a way of learning, not something you do ("uvědomuje si…",
  "projevuje zájem…", "buduje si vztah…"). Do not overuse: if there is a doable activity inside, make a card.
- **O3**: a summary of the whole goal, the concrete things are in its other points (typical for the minimum level).
`start` = the beginning of the point text (enough to identify it uniquely, exact characters).

## The four tools and the verdicts

Tool categories (always all four):
- `chatbot` AI chatbot: you type a task, it answers in full sentences (ChatGPT, Gemini, Claude).
- `internet` Internet a další zdroje: ready information you look up (search engine, Wikipedia, language reference, encyclopedia).
- `aplikace` Aplikace: single-purpose programs (translator, spell-checker, maps and navigation, photo math solver,
  plant identification, spreadsheet, drawing app, music app, fitness tracker).
- `klasicky` Klasický nástroj: non-digital or simple tools (calculator, ruler, compass, thermometer, paper map,
  dictionary, musical instrument, ball, microscope).

Verdicts: `za-tebe` (Udělá to za tebe: the tool produces the result the task asks for), `pomuze` (Pomůže ti: it helps,
but you still do the main part), `nepomuze` (Nepomůže: no real help, or the point is that you do it yourself, with your
body, voice, hands, judgement or feelings).
Be realistic about current tools in 2026: chatbots write, summarise, translate, explain and solve textbook problems
well, also from a photo; they cannot run, sing in front of the class, mix chemicals or feel for you. Be honest in both
directions: do not say "nepomůže" just because using the tool would be cheating, the question is what it can do.
`why`: one short sentence in Czech, tykání, max ~90 characters, gender-neutral (never "sám/sama", "musíš ty" instead;
no past participles like "naučil ses"), concrete ("Z fotky předměty spočítá, u velkého počtu ale
chybuje."). Name tool types, not brands, except well-known reference sources (Wikipedie, Internetová jazyková příručka).

## ESCO skills (`skills`, full URIs)

The skills decide which occupations the card links to. Find them with
`uv run python -I find_skill.py "hledaný výraz" --limit 20 --expand` (Czech, diacritics-insensitive; try several
stems, e.g. "graf", "tabul", "zdrav", "první pomoc", "kresl"). Choose 1–3 skills that really describe the activity.
Prefer skills that are essential in at least a few occupations (incl. narrower). Avoid skills that pull in unrelated
jobs (check the occupation count is plausible; "provádět výpočty" for any arithmetic is fine, "matematika" for
counting apples is not). The same skills may be shared by several cards of one goal when that is honest.
Avoid broad transversal skills ("spolupracovat s kolegy", "používat komunikační techniky", "řešit problémy pomocí
kritického myšlení", "dát najevo empatii", "dodržovat pracovní postupy") unless the card is literally about that and
nothing more specific exists: they link to dozens of unrelated jobs (an airport director for a group art project).
A subject skill ("vytvářet umělecká díla", "dějiny") is better even when it links to fewer occupations.
Already used skills (reuse when they fit): see the `skills` arrays in the existing card files.

## File format

```json
{
  "outcome": "CODE",
  "draftedBy": "claude-sonnet-5-5",
  "promptVersion": "cards-v1",
  "reviewed": false,
  "cards": [
    {
      "slug": "kebab-case-unique-czech-without-diacritics",
      "title": "Název karty",
      "aliases": ["3–6 search phrases a kid might type", "synonyms", "school words"],
      "sources": [{"level": "Na začátku", "quote": "exact substring of ONE point of that level"}],
      "rules": ["P1", "P2"],
      "tools": {
        "chatbot":  {"verdict": "za-tebe",  "why": "..."},
        "internet": {"verdict": "pomuze",   "why": "..."},
        "aplikace": {"verdict": "pomuze",   "why": "..."},
        "klasicky": {"verdict": "nepomuze", "why": "..."}
      },
      "skills": ["http://data.europa.eu/esco/skill/..."],
      "inspiration": ["exact illustration title, optional"]
    }
  ],
  "aside": [{"level": "Splněno", "start": "Uvědomuje si", "code": "O2", "refs": []}]
}
```
Levels are exactly: "Na začátku", "Na cestě", "Splněno", "Minimální doporučená úroveň". A `quote` may be the whole point
or the part the card uses; it must match exactly one point of that level (copy characters exactly, incl. non-breaking
spaces turned into normal spaces as printed). Slugs must be unique across all goals (the validator checks).

## Czech writing

Read `/home/zdenek/projects/rvp/docs/anti-ai-slop-cz.md` first. Titles are plain noun phrases, no questions, no colon
chains unless clarifying ("Záporná čísla kolem nás: teploměr a dluh" is the maximum). Tykání in `why`. No exclamation
marks, no dashes as sentence breaks.

When done, reply with: per goal, the number of cards and asides, and one line for anything doubtful (a point you were
unsure how to treat, skills that link to odd occupations).
