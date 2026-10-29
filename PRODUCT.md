# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Astro, static output. Client-side search (MiniSearch). Content comes from a Python pipeline (`pipeline/`) into JSON (`content/`) read at build time. Public at procsetoucim.quxt.eu since 2026-10-20 (static nginx container behind caddy + cloudflared; also on the tailnet at procsetoucim.internal.quxt.eu).

## Users

Czech elementary-school kids (grades 1–9) first; their parents read along. Two situations:

- **Lookup:** the kid is doing homework or just had a lesson and asks "proč se to učím?" about one concrete thing (vyjmenovaná slova, malá násobilka, měřítko mapy). They type it in and want a straight answer.
- **Browsing:** a kid or parent wants to see what school asks for in a subject or year, and how much of it still makes sense when tools and AI exist.

Phone and desktop matter equally.

## Product Purpose

Answer "Why am I learning this?" for every concrete thing taught in Czech elementary school, now that calculators, apps, the internet and AI chatbots can do part of it. For each item: the official RVP point it simplifies, can a tool do it for you, how many people need it at work, and which (future) jobs use it. Conclusions are left to the reader. The site speaks to the worry many Czech parents have about kids and AI without mentioning it.

Success: a kid gets an honest answer in under a minute; a parent understands what the curriculum asks for and where it is out of step with reality.

## Positioning

The answer to "why learn this" comes first, in plain kid language. Behind every answer sits the official curriculum (new RVP ZV, deep-linked to prohlednout.rvp.cz) and public data (ESCO occupations, ILO AI exposure, Cedefop forecast), with the method open. It is an analysis, not advocacy: when something looks not very useful, the site says so as plainly as when it is essential.

## Operating Context

- Kids read on phones during or after homework; parents on phone or laptop.
- Entry is usually search (lookup) or a subject/year list (browsing).
- Content is generated and reviewed in batches. Coverage grows gradually: a few topics first, the full curriculum later. Pages must look complete with partial coverage.

## Capabilities and Constraints

- Activities are derived from the new RVP level descriptions; RVP illustrations are inspiration; the old RVP is not used.
- Linked entities: RVP outcome → concrete activities → ESCO skills → occupations. Overview pages by subject × year, tool, traffic light, occupation.
- Per activity: the official RVP point(s) and the simplification rules used; tool verdicts (AI chatbot / Internet a další zdroje / Aplikace / Klasický nástroj) rated *Pomůže ti / Nepomůže* (no tool does it for you); "Proč se to učíš" (AI-written, the heart of the card) and "Jak se to učit s AI" (three AI-written suggestions, marked); job-market numbers (share of workers, occupation groups, AI exposure, Cedefop trend) and example occupations with AI notes. The former "Potřebuješ to umět?" scale was dropped as too subjective.
- Every card states what is data, what is an estimate, and what AI drafted. Every card has a feedback form ("Připomínka ke kartě": chyba / návrh / vlastní znění of one part, a revision starts from the current text), stored by `feedback/server.py`.
- Practice tips: deferred, not in scope now.
- Summary numbers page: deferred until data is reviewed.
- Static site; the only backend is the small feedback service (stdlib Python + SQLite behind nginx `/api/`). No accounts, no tracking; feedback stores no IP addresses.
- Cedefop data terms apply (see `docs/data-terms.md`): only derived aggregates, exact citation, indicative wording.

## Brand Commitments

- Name: **Proč se to učím?**
- Fully in Czech, informal (tykání), simple language. Anti-slop rules in `docs/anti-ai-slop-cz.md`.
- Warm and approachable, like a school sketchbook: near-white dotted page, torn pieces of flat, almost white paper (plain, squared, ruled), hand-drawn icons, outlines and hatched charts, dark blue and dark red accents (Czech tricolore), purple for AI-written text. Numbers are promoted with simple charts. The subjects are a hand-drawn school floor plan. Fonts: Sofia Sans Extra Condensed + Commissioner. No eyebrow labels above headings, minimal captions, no entrance animations, simplest hover only.
- Light theme only.
- Never mention the mesic.ai competition on the site.

## Evidence on Hand

- `data/rvp/data_final_rvp_zv_full_mp_20251216.json`: new RVP ZV (475 outcomes, 1,730 illustrations, dependency graph).
- `data/esco/`: ESCO v1.2.1 (Czech).
- `data/cedefop/`: Cedefop Skills Forecast 2026 (restricted, never redistributed).
- ILO GenAI exposure 2025 (GitHub, CC BY 4.0), to be downloaded.
- `analysis/tools-coverage.csv`: first outcome-level tool estimate (8 categories, to be remapped to 4).
- No testimonials, users, or usage numbers exist. Do not invent any.

## Product Principles

1. The kid's question first, the data one click behind it.
2. Say it plainly in both directions: "Základ" and "Spíš zbytečné" get the same tone.
3. Concrete over abstract: name the actual exercise, not the competence.
4. Every claim traceable to a source or labelled as our estimate.
5. Partial coverage is shown honestly, never padded.

## Accessibility & Inclusion

WCAG 2.2 AA. Chart colours and marks always paired with a text label. Readable for young readers: simple words, short sentences, generous type.
