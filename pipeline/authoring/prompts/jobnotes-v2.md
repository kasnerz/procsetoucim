# Prompt jobnotes-v2: short notes "how this occupation uses this school skill"

Used by: Sonnet subagents (agent type `jobnote-writer`) drafting notes for `content/jobnotes/<slug>.json`. Inputs from
`authoring/jobnote_inputs.py --missing` (one batch per agent); saved by `authoring/save_jobnotes.py`. Replaces
jobnotes-v1 (user 2026-10-19: occupations are now ranked by a relevance score, the input says how much the job uses
the skill; one draft file per batch; short anti-slop rules).

---

Website "Proč se to učím?" (Czech, for elementary-school kids and their parents). Each card is one concrete thing kids learn
(from the Czech curriculum RVP). For each card we show example occupations (from the EU database ESCO) that list a related
skill as essential, ordered by how much the job uses it. You write ONE short note per (card, occupation): how a person
in that job uses what the card is about.

## Input
Your batch file (JSON list). Per card: `slug`, `title`, `rvpPoints` (the official curriculum sentences the card simplifies),
`occupations` (only the ones still missing a note): `id`, `label`, `description` (ESCO, Czech, shortened), `group`
(ISCO group), `needsSkills` (ESCO skills of this card the job lists as essential), `needsDirectly` (skills listed
directly, not only via a narrower skill; empty = the link is indirect), `use` (a model's estimate of how much the job
uses the card's skill, as shown on the card: "Využívá neustále / často / občas / zřídka").

## Output
Write all notes of your batch with ONE Write to the draft path your caller names:
```json
{"<slug>": {"<occupation id>": "<note>", "...": "..."}, "...": {}}
```
Every listed occupation needs a note. Then run, from `/home/zdenek/projects/rvp/pipeline`:
`uv run python -I authoring/save_jobnotes.py <draft>`. It merges the notes into `content/jobnotes/<slug>.json` (keeping
the notes already there) and prints only problems. Fix the draft with Edit and rerun until clean.

## How to write a note
- Czech, plain words a 10–14-year-old understands. 1–2 sentences, 80–220 characters.
- Say concretely what in this job uses the card's activity, grounded in the ESCO description. Example for card
  "Odhad výsledku a zaokrouhlování" and a shop assistant: "U pokladny rychle odhadne, jestli součet sedí, a pozná překlep dřív, než zákazník zaplatí."
- Be honest when the link is weak or partial: say which part they use and which not. Match `use`: a note for
  "Využívá zřídka" must not sound like the skill is central, and one for "Využívá neustále" should show why it is. Example: "Počítá hlavně s penězi a množstvím zboží. Dlouhé dělení na papíře v práci nepotřebuje, má pokladnu."
- Neutral analysis, not advertising. No invented numbers, no predictions about the future, no claims ESCO does not support.
- Gender-neutral throughout (labels are like "Kurýr/kurýrka"). No gendered job nouns, and no masculine or feminine
  forms for the worker either: no "on/ona", "mu/jí", "sám/sama", no past tense or participles ("nepoškodil",
  "zvyklý"). Write in the present tense with a neutral subject: "V této práci se…", "Tady…", "Kdo tu pracuje…", or
  start with the activity ("Při plánování tras…"). Do not start every note the same way.
- Read `/home/zdenek/projects/rvp/docs/anti-ai-slop-cz-kratka.md` (short anti-slop rules) first and follow it. In particular: no "nejen X, ale i Y",
  no question-and-answer tricks, no grand claims, no exclamation marks, no em/en dashes as sentence breaks (use commas or
  full stops), no habitual lists of three, no empty words (klíčový, zásadní, nedílný, efektivně, v dnešní době).
- Do not mention AI unless the ESCO description does.

When done, reply briefly: notes saved, lint status, and at most five lines on cards where the occupations looked
unrelated. Do not repeat the notes.
