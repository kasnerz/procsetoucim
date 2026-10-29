# How an RVP point becomes a card

Source of truth: `pipeline/authoring/cards/<outcome>.json`, validated by `pipeline/authoring/build_cards.py` (asserts every rule below). Drafting prompts: `pipeline/authoring/prompts/` (`cards-v2`, `card-v5`, `jobnotes-v2`). Public Czech version: `/metodika/#pravidla`.

## Input

The new RVP ZV (NPI open data, 16 Dec 2025). Each expected outcome (cíl) has level descriptions
(`Na začátku`, `Na cestě`, `Splněno`, `Minimální doporučená úroveň`). Every non-empty line of a level
description is one **point** (bod). Illustrations (ukázky úloh) are inspiration only. The old RVP 2023 is not used.

## Simplification rules

A card is a simplified point. Each card stores its source points verbatim (`levelSource[].point`, plus
`quote` when only part of the point is used) and the rules applied (`rules`).

| Code | Name (cs) | Rule |
|---|---|---|
| P1 | Zkrácení | The point becomes a short name of what the kid does (noun phrase). Nothing is added. Every card uses P1. |
| P2 | Běžná slova | Technical wording is replaced by plain words or explained in the name ("regiony Česka" → "kraje Česka"). Subject terms that are themselves the learning content (zlomek, legenda) stay. |
| P3 | Rozdělení | A point listing several activities is split into several cards when the four tools would rate them differently ("sčítá, odčítá, násobí a dělí pamětně i písemně" → zpaměti / písemné sčítání / písemné násobení / písemné dělení). |
| P4 | Sloučení | Points of the same goal that describe the same thing, or its simpler step at a lower level, are merged into one card ("Pracuje s legendou a směrovou růžicí" + "Čte mapu… legendu a měřítko" → "Legenda, měřítko a směrová růžice"). |
| P5 | Příklady jen z RVP | A concrete example in the card name must appear in the source point or in an RVP illustration title of that goal. Examples in the AI comment are allowed and marked as AI text. |

Split until uniform: within one card, each tool's verdict must hold for everything the card asks.

## Coverage

Every point of a covered goal is either turned into card(s) or set aside with a reason. The authoring
script fails if a point is neither, or both. Output: `content/coverage/<outcome>.json`.

| Code | Reason |
|---|---|
| O1 | The same point is covered under another goal (`refs` = card slugs). Used where the 9th-grade goal repeats 5th-grade points word for word. |
| O2 | Describes an attitude or way of learning, not something you do ("uvědomuje si vztah…"). |
| O3 | A summary of the whole goal; the concrete things are in its other points (typically the minimum level). |

## What is AI-drafted

Card names, rule assignment, tool verdicts and their reasons, ESCO skill choice (`cards-v1`, from 2026-10-20 `cards-v2` with binary verdicts from the start); binary tool verdicts, "Proč se to učíš" and "Jak se to učit s AI" (`card-v4`, written after the numbers exist, so they can draw on them; titles of the suggestions added with `card-v5`); occupation notes (`jobnotes-v1`, then `jobnotes-v2`). The first 56 cards were drafted by Claude Opus, later goals by Claude Sonnet subagents with the same rules and validator. The two card texts are always written by Claude Opus subagents.
Everything is drafted by Claude and marked on the site; `review.reviewed` records human review.
Numbers about work (ESCO, Cedefop, ILO) are computed by the pipeline, without AI.
