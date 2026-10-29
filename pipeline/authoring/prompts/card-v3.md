# Prompt card-v3: tools, "Proč se to učíš", "Jak se to učit s AI"

**Replaced by `card-v4.md` (2026-10-19). Kept for the record.**

Used by: subagents that, for each card of their goals, (1) judge the four tools (`tools-v2`, binary scale) in
`pipeline/authoring/cards/<goal>.json` and (2) write `content/comments/<slug>.json` (`comment-v3`).
The texts (Steps 2 and 3) are always written by **Opus** subagents (`model: opus`, user 2026-10-18: the highest-quality
model writes everything a reader reads). Re-running only the texts: tell the agent "texts only, skip Step 1".
Inputs from `authoring/comment_inputs.py --by-goal`. Replaces comment-v2 (side comment) and the three-step tool scale.

---

## Context

Website "Proč se to učím?" (Czech, for elementary-school kids aged about 8–15, parents read along). Each card is one
concrete thing kids learn, simplified from points of the Czech curriculum (RVP). The card page answers the question
in the site's name: why am I learning this, and does a tool make it unnecessary?

## Input

Your batch file: a list of goals. Per goal: `outcome`, `sourceFile` (the card source to edit), `subject`, `stage`,
`goal`, `buildsToward` (later goals that build on it), and `cards`. Per card: `slug`, `title`, `rvpPoints`,
`tools` (the current verdicts; in Step 1 you judge them again), `work` (numbers from data, see below),
`topOccupations` (ESCO jobs needing the card's skills, with a note on how they use it).

## Step 1: tools (edit `tools` in the source file, nothing else)

Four tools: `chatbot` (AI chatbot), `internet` (Internet a další zdroje: search, Wikipedia, language reference,
encyclopedia), `aplikace` (single-purpose apps: translator, spell-checker, maps, photo math solver, plant
identification, spreadsheet, drawing or music app, fitness tracker), `klasicky` (calculator, ruler, compass,
thermometer, paper map, dictionary, instrument, ball, microscope).

Verdict is **binary**: `pomuze` (Pomůže ti) or `nepomuze` (Nepomůže). No tool does anything *for* you: you are the one
who exists in the real world, in real time, with your body, hands, voice and judgement. So the question is strictly:
**while you learn and do this yourself, does this tool really help?**
- `pomuze` only when the tool concretely helps you: explains, gives material or examples, checks your result, measures,
  lets you practise, shows what you could not see. Being able to produce the answer is not enough by itself: say what
  the help is (a calculator checks your written division; a chatbot explains the rule and gives practice sentences).
- `nepomuze` when the activity is physical, social or personal and happens in the real world (sorting waste with your
  hands, running, singing in front of the class, behaving in nature, handwriting, talking to a friend), or when the
  tool has nothing useful to offer for it. "A chatbot can describe how to sort waste" does not make it help you sort.
- Be strict and honest both ways. Do not mark `pomuze` just because the tool is related to the topic.
`why`: one Czech sentence, tykání, max ~100 characters, gender-neutral (never "sám/sama"), concrete: what exactly it
does for you, or why it does not help (e.g. `nepomuze`: "Odpad třídíš rukama ty, chatbot ho nevytřídí."). Tool types, not brands.

## Step 2: "Proč se to učíš" (`comment`)

This is the heart of the card. 3–5 sentences, Czech, one paragraph, about 300–650 characters.
- Go straight to why it is in the curriculum and what it is good for: concrete situations where you need it (everyday
  life, later school subjects from `buildsToward`, jobs from `topOccupations` when the link is real), and for whom it
  matters most to master it well.
- Relate it to the tools where that is relevant: if tools handle much of it, say what is still worth having in your
  own head and why (checking a result, knowing what to ask, doing it without a device, understanding). Where tools are
  beside the point (PE, singing, art, feelings, behaviour), do not force them in: say plainly what it is good for
  (health, joy, getting along with people, confidence).
- Honest and neutral: if something is of little use outside school, say so as plainly as when it is essential.
- At most one statistic, only from `work`, rounded as given. No other numbers, dates or facts you cannot trace to the
  input. No predictions beyond `trend2035` ("míst spíš přibude" only when it is above 1.5).
- Do not start with "Učíš se to, protože" and do not start every card the same way.

## Step 3: "Jak se to učit s AI" (`learnWithAi`)

1–3 sentences, Czech, about 120–350 characters: a concrete way to use an AI chatbot (or an AI app) to learn or
practise this, so that you still do the thinking or the doing. E.g. "Požádej chatbota, ať ti vymyslí deset vět
s chybějícími čárkami. Doplň je a nech si vysvětlit, kde je chyba." Good patterns: let it generate practice tasks and check your answers; let it
explain a step you do not get, in simpler words; let it quiz you; let it play a role (a tourist asking the way in
English); ask it to find the mistake in your own text but fix it yourself; let it suggest a training plan.
- Remind to check facts when the AI could be wrong (dates, places, plants from a photo, calculations in long problems).
- For `stage` "do konce 5. třídy" phrase it for doing together with a parent or teacher ("Zkuste s rodičem…",
  "Poproste chatbota…"), since chatbots are generally meant for older users.
- When AI genuinely offers little (pure physical activity), say what small thing it can do (plan, remind, explain the
  rules) in one sentence, without exaggerating.

## Numbers in `work`

`occupations` (ESCO occupations listing the skill as essential), `people` (estimated Czech workers in them),
`peopleShare` (% of all Czech workers), `highAiExposure` (% of those workers in jobs where the ILO expects generative
AI to change many tasks), `trend2035` (Cedefop employment change 2025→2035, %), `buildsOnIt` (later RVP goals that build
on this one). ESCO lists a skill only where it is essential, so everyday skills are used by far more people than shown.

## Voice (all text)

Kids first, tykání, parents can read along. Gender-neutral for the reader (no "sám/sama", no past participles like
"naučil ses", "spletl ses"); avoid gendered job nouns ("lidé na stavbě", "kdo řídí autobus"). Tool types, never brands.
Read the **whole** of `/home/zdenek/projects/rvp/docs/anti-ai-slop-cz.md` first (all sections, not only the start), and before
finishing run its checklist over every text you wrote and rewrite what breaks it; your final report must confirm this. In particular: no "nejen X, ale i Y", no "nejde o X,
ale o Y", no question-and-answer tricks, no grand claims, no exclamation marks, no em/en dashes as sentence breaks,
no habitual lists of three, no empty words (klíčový, zásadní, nedílný, efektivně, v dnešní době), no closing moral.

## Output and checks

- Card source: edit only `tools` of each card in your goals' `sourceFile` (Python json.load / json.dump with
  ensure_ascii=False, indent=2, trailing newline). Set the top-level `"toolsVersion": "tools-v2"`.
- `/home/zdenek/projects/rvp/content/comments/<slug>.json`:
  `{"draftedBy": "claude-opus-5-5", "promptVersion": "comment-v3", "comment": "...", "learnWithAi": "..."}`
- Run, from `/home/zdenek/projects/rvp/pipeline`:
  `uv run python -I authoring/build_cards.py --check <your goal codes>`,
  `uv run python -I authoring/lint_cards.py <your goal codes>`,
  `uv run python -I authoring/lint_comments.py --slugs <your slugs, space-separated>`
  and fix until all pass (a lint hit that is clearly a false positive may stay; list it).
- Touch no other files. Reply with the number of cards done per goal, how many verdicts changed to `nepomuze`, and
  one line for anything doubtful.
