---
version: 1
slug: "site-src-pages-aktivita-slug-astro"
primary_target: "site/src/pages/aktivita/[slug].astro"
related_targets: []
---

# Activity page (aktivita)

Scope: one concrete school activity, e.g. "Písemné násobení". Sets the visual world for the whole site; home, overviews, outcome and occupation pages inherit it.
Mode: Read.
Audience and job: a kid (parents read along) asks "proč se to učím?" about one thing and wants a straight answer in under a minute, then may follow where it leads.
Content: the card name, the official RVP point(s) it simplifies with the rules used, an AI comment (marked), four tool categories with verdicts, example occupations with AI notes and a link to all of them, job-market numbers (share of workers, occupation groups, AI exposure, Cedefop trend, RVP links), later school topics, sources and method.
Constraints: light only, near-white ground, cool greys; accents dark blue, dark red, purple for AI text; no eyebrow labels; no entrance motion, colour/underline hover only; WCAG 2.2 AA; Czech, tykání.

## Direction contract

THESIS: Each card is one A4 sheet from a school sketchbook: the official sentence taped on, the plain-language name above it, and the numbers drawn by hand next to it. Honest and approachable for kids, refusing both the edtech mascot-and-gradient default and the cold official-portal grid.

OWN-WORLD: The sketchbook. Torn pieces of flat, cool paper tones (grey, recycled grey, blue-grey; no gradients) (plain, squared for numbers, ruled with a red margin line for lists) with seeded torn edges, a faint offset shadow and a slight tilt; a piece on a piece is white. Everything drawn by hand: Matita pencil icons standing bare, pencil box outlines, hatched pies and bars, a blue pen stroke under headings, a dark-red marker swipe for emphasis, teacher's marks (✓ + −) in red pen for tool verdicts, purple sparkle for AI-written text. The logo is a hand-drawn signpost with a blue and a red plate. Condensed titles, calm body face.

STORY: The kid reads the card name, sees the official RVP sentence it comes from, reads the comment, sees which tools do it for them and how many people need it at work, and opens an occupation. A parent checks the rules and the footnotes and sees what is data, what is computed and what AI wrote.

FIRST VIEWPORT: Logo and a light text menu in the top area (no bar); a plain breadcrumb; one large sheet: centered title; the official point as a white taped clipping (the used part marked), collapsed by default behind an "Oficiální znění v RVP" toggle, with the simplification rules inside; "Proč se to učíš" on its own piece of paper in full ink and larger type (the heart of the card). Below it, full width like the other sections: "Kdo to využívá" (jobs) and the squared numbers sheet side by side, then the tools table, then "Jak se to učit s AI" as three white scraps pinned in a row (user 2026-10-19). Primary action: opening an occupation or the goal page.

FORM: Sešit: user-pinned redesign (2026-10-18) of the chosen direction (originally Směrovka, position 1 on my ordered list of 7). seed:4327cdd220166c61

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Memorable moment

The taped clipping of the official RVP sentence under the plain-language name, with the rules that turned one into the other.

## Unresolved

- ESCO links for cards tied only to generic skills ("provádět výpočty") produce loosely related example occupations; the AI notes say so, but the selection could be improved.
- The 56 sample cards and 448 occupation notes are not reviewed by a human yet.
