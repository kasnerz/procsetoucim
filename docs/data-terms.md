# Data sources: terms of use

## Cedefop Skills Forecast 2026 (`data/cedefop/`)

The user accepted these terms on download (2026-10-18). They bind everything we build.

- **Never redistribute the dataset.** The raw zip/xlsx files stay out of git and out of the built site. Ship only derived, aggregated figures we need for specific pages. Anyone who wants the data goes through Cedefop's pre-registration: https://www.cedefop.europa.eu/en/projects/skills-forecast
- **Exact citation**, wherever a figure, chart or table uses it (site pages, methods page, any export):
  > European Centre for the Development of Vocational Training (Cedefop). Cedefop Skills Forecast 2026, Thessaloniki: Greece, Downloaded from: https://www.cedefop.europa.eu/en/projects/skills-forecast
- **Indicative only.** Present as trends and patterns, never as precise numbers. Detailed estimates have large and uncertain error margins.
- **Cells with fewer than 10,000 people:** flag as unreliable. Do not build a claim on them.
- Employment (National Accounts, workplace basis) and labour supply (LFS, residence basis) use different definitions. Do not compare or subtract them.
- Detailed occupational shares are forecast from few LFS years. Some cells are empty or unreliable, and Cedefop has not validated every series. Say so on the methods page.
- **Copyright stays with Cedefop.**
- **When the site goes public, the user must inform Cedefop** (skills-forecast@cedefop.europa.eu). Cedefop may reproduce our public outputs on its portal. Remind the user before any public launch.

## ILO GenAI exposure index 2025

Gmyrek et al. 2025, ILO Working Paper 140. Data: https://github.com/pgmyrek/2025_GenAI_scores_ISCO08, CC BY 4.0, attribution required.

## ESCO v1.2.1

European Commission. Free reuse with attribution (ESCO is published under the Commission's reuse policy). Cite "ESCO – European Skills, Competences, Qualifications and Occupations, v1.2.1".

## RVP ZV (new, 2025) and RVP ZV 2023 (old)

NPI ČR / MŠMT. Official documents. Link individual outcomes to https://prohlednout.rvp.cz/ovu/{kod-lowercase}.

## CERMAT tests

All rights reserved. Use only to identify task types and link to them. Never copy tasks.

## Umíme to and other exercise sites

Their terms forbid copying content. Link out only.

## Icons

Matita icons (https://github.com/matita-dev/icons), MIT licence, via `@iconify-json/matita`. Credited on /o-projektu/. A few extra icons in `site/src/icons/sketch.json` are our own drawings in the same style.

## Fonts

Grandstander, Outfit and Mynerve: SIL Open Font License 1.1, self-hosted via Fontsource packages (files in the build, no external font provider).

## How the site applies the Cedefop terms (2026-10-20)

- Trends appear only as words ("spíš přibude"), never as percentages. (Arrows on occupation rows were dropped 2026-10-29.)
- Figures are shown per ISCO 2-digit group, the finest level of the forecast, in the group box on occupation and group pages (`components/GroupBox.astro`): employment 2025/2035, job openings 2026–2035 (replacement demand summed over 2026–2035 plus the change in employment, Cedefop's definition) and employment by qualification in 2035, all as coarse headcounts.
- Headcounts are rounded coarsely: to 10,000 above 100,000 people, to 5,000 below, and "méně než 10 tisíc" under 10,000 (`peopleAbout` in `site/src/lib/data.ts`).
- Groups under 10,000 people get no trend at all: no arrow, and the occupation page says the forecast is too uncertain.
- The exact citation is printed as a source line (`site/src/components/CedefopSource.astro`) on every page that shows Cedefop figures. Exceptions (user 2026-10-20): the home page shows no Cedefop figures any more (since 2026-10-29: the occupation picks show the ILO level, the numbers section ranks cards and occupations by our tool verdicts and the Jev estimate), so it needs no Cedefop source line; the forecast box on occupation pages shows the short form "Zdroj: Cedefop Skills Forecast 2026, Thessaloniki: Greece" as a link, with the full citation in its tooltip. The card footer (user 2026-10-25: one line on AI, one on sources) uses the same short form, linked, with the full citation in its tooltip; the full citation stays on the "O projektu" page.
- The card figures (people needing a skill, the trend for those jobs) are our estimate from Cedefop group data and say so.
- The site went online on 2026-10-20 as semi-public (link only, not indexed). The user still has to inform Cedefop (skills-forecast@cedefop.europa.eu).

## Cedefop website and Skills Intelligence charts (checked 2026-10-29)

The Skills Intelligence pages (https://www.cedefop.europa.eu/en/tools/skills-intelligence/) let anyone export a chart as CSV/XLSX without the Skills Forecast pre-registration. Cedefop's legal notice (https://www.cedefop.europa.eu/en/content/legal-noticedisclaimer): "© Cedefop. Reproduction is authorised, provided the source is acknowledged, save where otherwise stated." So exported figures may be used with a source line, unless the chart says otherwise. Each chart names its own dataset and source (e.g. monthly gross income: EU-SILC, Eurostat); cite that source too, and for Eurostat data follow its reuse policy (free reuse with acknowledgement, Commission Decision 2011/833/EU). Charts that show Skills Forecast figures stay under the forecast's rules above (indicative only, the exact citation, cells under 10,000 flagged).
