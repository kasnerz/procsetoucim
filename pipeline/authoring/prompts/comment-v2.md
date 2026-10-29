# Prompt comment-v2: the card comment ("Komentář")

Used by: subagents drafting `content/comments/<slug>.json`. Inputs come from `authoring/comment_inputs.py`
(one JSON batch per agent). Replaces the one-paragraph comments of sample-v1 (written inline with the cards).

---

## Task

Website "Proč se to učím?" (Czech, for elementary-school kids aged about 8–15 and their parents). Each card is one concrete thing
kids learn, simplified from one or more points of the Czech curriculum (RVP). For each card in your batch, write the
card's comment, shown on the card page under the heading "Komentář" and marked as written by AI.

## Input (per card in your batch file)

- `slug`, `title`, `subject`, `stage` (e.g. "do 5. třídy"), `goal` (the RVP goal the card belongs to)
- `rvpPoints`: the official curriculum sentences the card simplifies (`quote` = the part used)
- `tools`: the card's verdict for each of the four tool categories (AI chatbot, Internet a další zdroje, Aplikace,
  Klasický nástroj) with the reason. Verdicts: "Udělá to za tebe", "Pomůže ti", "Nepomůže".
- `work`: numbers computed from data (ESCO, Cedefop, ILO), see "Numbers" below
- `topOccupations`: up to 8 ESCO occupations that need the card's skills, each with a short note on how they use it
- `buildsToward`: later RVP goals that build on this card's goal
- `earlierComment`: the previous comment (for context only; do not copy it, write a new one)

## Output

For each card write `/home/zdenek/projects/rvp/content/comments/<slug>.json`:
```json
{"draftedBy": "claude-sonnet-5-5", "promptVersion": "comment-v2", "comment": "<text>"}
```
Valid UTF-8 JSON, check with `python3 -I -m json.tool <file>`.

## Structure of the comment (mandatory)

Czech, at most 5 sentences, about 350–700 characters, one paragraph.

1. **What it is (1–2 sentences).** Describe the activity in detail and concretely: what exactly you do, with what, on
   what kind of material, what the result looks like. Use plain words a 10-year-old understands. Not a restatement of
   the title: add the detail the title leaves out (e.g. for "Písemné dělení": "Dělíš velké číslo jednocifernou… pod
   sebou na papíře, krok po kroku od nejvyšší číslice, a na konci ti může zbýt zbytek.").
2. **How useful it is (3–4 sentences).** Your own assessment of how useful it is today and for future occupations,
   drawing on the rest of the card:
   - the tools: what a tool really does for you here and what is still left to you (understanding, checking the
     result, choosing, doing it with your hands or body, doing it fast without a device);
   - the work numbers and the occupations: who needs it at work and how (pick one or two telling examples from
     `topOccupations`, in plain words; use them only when the link is real, never present a weak link as strong);
   - what builds on it (`buildsToward`), when it matters, e.g. it is a step toward fractions or toward writing longer texts.
   Give concrete everyday or work examples where they help. Say plainly when something is not very useful any more
   (e.g. long lists learned by heart), just as plainly as when it is essential.

## Numbers

`work` has: `occupations` (ESCO occupations that list the skill as essential), `people` (estimated Czech workers in
them), `peopleShare` (share of all Czech workers, %), `highAiExposure` (share of those workers in jobs where the ILO
expects generative AI to change many tasks, %), `trend2035` (Cedefop forecast of employment change in those jobs
2025→2035, %), `buildsOnIt` (number of later RVP goals that build on this one).
- You may use at most one statistic, only from `work`, rounded the way the input shows it. Never any other statistic,
  date or fact you cannot trace to the input. (Small worked examples in the description, like 49 + 31, are fine.)
- No predictions beyond the data. "Míst v těch povoláních spíš přibude" is fine when `trend2035` > 1.5; do not
  promise that a job will exist or disappear.
- ESCO lists a skill only where it is essential, so many more people use simple skills (reading, counting) than
  the numbers show. Do not conclude "hardly anyone needs it" from a small `peopleShare` for an everyday skill.

## Voice

- Kids first, tykání, parents can read along. Neutral analysis, not advocacy and not advertising.
- Avoid gendered forms for the reader: no "sám/sama", no past tense participles like "naučil ses"; use present tense
  and neutral wording ("umíš", "musíš poznat", "zvládneš").
- Avoid gendered job nouns: "lidé na stavbě", "v kanceláři", "kdo řídí autobus", "zdravotní sestry a ošetřovatelé" is fine.
- Name tool types, not brands: "chatbot" (never ChatGPT, Gemini…), kalkulačka, mapová aplikace, slovník, tabulkový program.
- Read `/home/zdenek/projects/rvp/docs/anti-ai-slop-cz.md` first and follow it. In particular: no "nejen X, ale i Y"
  and no "nejde o X, ale o Y", no question-and-answer tricks, no grand claims, no exclamation marks, no em/en dashes
  as sentence breaks (use commas or full stops), no habitual lists of three, no empty words (klíčový, zásadní, nedílný,
  efektivně, v dnešní době, v digitálním světě), no closing moral ("A to se hodí vždycky."). Vary sentence length.
- Do not start every comment the same way (not always "Učíš se…").

## Example (card "Odhad výsledku a zaokrouhlování", style only)

"Než něco spočítáš přesně, zaokrouhlíš čísla na desítky nebo stovky a v hlavě odhadneš, kolik asi vyjde. Třeba 49 + 31
je zhruba 50 + 30, tedy kolem 80. Kalkulačka i chatbot spočítají přesný výsledek rychleji než ty, jenže překlep
v zadání nepoznají. Odhad je tvoje kontrola, že výsledek dává smysl. U pokladny, na stavbě při objednávání materiálu
nebo při nákupu ho lidé používají pořád, většinou aniž by o tom přemýšleli."

When done, reply with the list of files written and one line per card where the inputs looked wrong or contradictory.
