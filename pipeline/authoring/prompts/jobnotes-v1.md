# Prompt jobnotes-v1: short notes "how this occupation uses this school skill"

**Replaced by `jobnotes-v2.md` (2026-10-19). Kept for the record.**

Used by: subagents drafting `content/jobnotes/<slug>.json`. Inputs from `authoring/jobnote_inputs.py` (one batch per agent).

---

Website "Proč se to učím?" (Czech, for elementary-school kids and their parents). Each card is one concrete thing kids learn
(from the Czech curriculum RVP). For each card we show example occupations (from the EU database ESCO) that list a related
skill as essential. You write ONE short note per (card, occupation): how a person in that job uses what the card is about.

## Input
Your batch file (JSON list). Per card: `slug`, `title`, `rvpPoints` (the official curriculum sentences the card simplifies),
`occupations`: `id`, `label`, `description` (ESCO, Czech), `group` (ISCO group), `needsSkills` (ESCO
skills of this card the job lists as essential), `needsDirectly` (skills listed directly, not only via a narrower skill;
empty = the link is indirect and probably weaker).

## Output
For each card write `/home/zdenek/projects/rvp/content/jobnotes/<slug>.json`:
```json
{"draftedBy": "claude-sonnet-5-5", "promptVersion": "jobnotes-v1", "notes": {"<occupation id>": "<note>", "...": "..."}}
```
Every occupation id of the card must have a note. Write valid UTF-8 JSON (check it with `python3 -I -m json.tool <file>`).

## How to write a note
- Czech, plain words a 10–14-year-old understands. 1–2 sentences, 80–220 characters.
- Say concretely what in this job uses the card's activity, grounded in the ESCO description. Example for card
  "Odhad výsledku a zaokrouhlování" and a shop assistant: "U pokladny rychle odhadne, jestli součet sedí, a pozná překlep dřív, než zákazník zaplatí."
- Be honest when the link is weak or partial (especially when `needsDirectly` is empty): say which part they use and
  which not. Example: "Počítá hlavně s penězi a množstvím zboží. Dlouhé dělení na papíře v práci nepotřebuje, má pokladnu."
- Neutral analysis, not advertising. No invented numbers, no predictions about the future, no claims ESCO does not support.
- Avoid gendered job nouns (labels are like "Kurýr/kurýrka"): write "V této práci…", "Tady…", or start with the activity
  ("Při plánování tras…"). Do not start every note the same way.
- Read `/home/zdenek/projects/rvp/docs/anti-ai-slop-cz.md` first and follow it. In particular: no "nejen X, ale i Y",
  no question-and-answer tricks, no grand claims, no exclamation marks, no em/en dashes as sentence breaks (use commas or
  full stops), no habitual lists of three, no empty words (klíčový, zásadní, nedílný, efektivně, v dnešní době).
- Do not mention AI unless the ESCO description does.

When done, reply with the list of files written and any card where the occupations looked unrelated (one line each).
