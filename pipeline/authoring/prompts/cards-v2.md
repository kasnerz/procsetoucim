# Prompt cards-v2: turning an RVP goal into cards

Used by: subagents drafting `pipeline/authoring/cards/<outcome>.json`. Method: `docs/activity-method.md`.
Validator: `authoring/build_cards.py --check CODE`. Texts are not part of this step (see `card-v5.md`).
Replaces cards-v1 (2026-10-20: binary tool verdicts `tools-v2` as in card-v5 Step 1).

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

Verdict is **binary** (`tools-v2`, user 2026-10-18): `pomuze` (Pomůže ti) or `nepomuze` (Nepomůže). No tool does
anything *for* you: you are the one who exists in the real world, in real time, with your body, hands, voice and
judgement. So the question is strictly: **while you learn and do this yourself, does this tool really help?**
- `pomuze` only when the tool concretely helps you: explains, gives material or examples, checks your result, measures,
  lets you practise, shows what you could not see. Being able to produce the answer is not enough by itself: say what
  the help is (a calculator checks your written division; a chatbot explains the rule and gives practice sentences).
- `nepomuze` when the activity is physical, social or personal and happens in the real world (sorting waste with your
  hands, running, singing in front of the class, behaving in nature, handwriting, talking to a friend), or when the
  tool has nothing useful to offer for it. "A chatbot can describe how to sort waste" does not make it help you sort.
- Be strict and honest both ways. Do not mark `pomuze` just because the tool is related to the topic.
Split cards (P3) until each tool's verdict holds for everything the card asks.
`why`: one Czech sentence, tykání, max ~100 characters, gender-neutral (never "sám/sama", "musíš ty" instead;
no past participles like "naučil ses"), concrete: what exactly it does for you, or why it does not help
("Odpad třídíš rukama ty, chatbot ho nevytřídí."). Name tool types, not brands, except well-known reference sources
(Wikipedie, Internetová jazyková příručka).

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
  "promptVersion": "cards-v2",
  "toolsVersion": "tools-v2",
  "reviewed": false,
  "cards": [
    {
      "slug": "kebab-case-unique-czech-without-diacritics",
      "title": "Název karty",
      "aliases": ["3–6 search phrases a kid might type", "synonyms", "school words"],
      "sources": [{"level": "Na začátku", "quote": "exact substring of ONE point of that level"}],
      "rules": ["P1", "P2"],
      "tools": {
        "chatbot":  {"verdict": "pomuze",   "why": "..."},
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
