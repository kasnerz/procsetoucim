# Tool categories for "Is there a tool that can do it better than a kid?"

Analysis for the *Proč se to učím?* site. English prose, Czech badge labels.
Input: `data/rvp/data_final_rvp_zv_full_mp_20251216.json` (RVP ZV, NPI, 16 Dec 2025).
Per-outcome table: `tools-coverage.csv` (362 subject outcomes).
Scripts and raw per-outcome notes: `/tmp/claude-1000/-home-zdenek-projects-rvp/5376c4f1-10bf-4054-bc5c-f6519b8e4426/scratchpad/tools-analysis/` (`notes.txt` is the hand-coded source, `build.py` produces the CSV and the numbers below).

## 1. Summary

Proposal: **8 badges**.

| # | Badge (CZ) | In one line | Outcomes tagged | of which "líp" |
|---|---|---|---|---|
| 1 | **AI chatbot** | writes, explains, summarises, analyses, converses (text, voice, reads images) | 155 | 95 |
| 2 | **Vyhledávání** | finds sources, facts, data and official info; helps check them | 39 | 27 |
| 3 | **Překladač a korektor** | converts or fixes text you supply: translates, corrects spelling/grammar, reads aloud | 42 | 35 |
| 4 | **Výpočty a grafy** | calculates, solves, constructs, plots, simulates (calculator to GeoGebra to spreadsheet) | 57 | 45 |
| 5 | **Mapy a navigace** | locates, routes, layers geographic data, maps the sky | 17 | 11 |
| 6 | **Měření a určování** | sensors and cameras observing reality: measure, track, identify species/objects/sounds | 42 | 16 |
| 7 | **Programování** | writes, explains and debugs code, trains simple models, drives robots and automation | 12 | 9 |
| 8 | **Digitální tvorba** | makes or edits images, video, music and 3D models (generators and editors) | 19 | 4 |

Headline numbers (362 subject outcomes, judged at the "Splněno" level descriptor):

- **182 (50 %)** outcomes: at least one tool does it **better** than a kid at the described level.
- **85 (23 %)**: best tool is **comparable** (does a meaningful part, or as well, but not better).
- **1**: a tool attempts it but is **worse** ("zatím ne").
- **94 (26 %)**: **no tool** meaningfully performs the outcome (body, own experience, relationships, hands-on work).
- **46 (13 %)** verdicts flagged as genuinely uncertain.
- Without the chatbot badge, 137 outcomes would still have a "líp" from another category; in 45 the chatbot is the only "líp".
- Subject split is stark: Matematika 91 % "líp", foreign languages 79–89 %, Chemie 79 %; Tělesná výchova 15 %, Osobnostní a sociální výchova 5 %, Polytechnická výchova 0 % (but 6/8 "srovnatelně").

"Líp" says nothing about whether the skill is still worth learning; that is the separate dimension (b). A calculator beating a 5th grader at decimals is exactly as true as it was in 1985.

## 2. Method

1. **Read every subject outcome** (362, all `tematickeOkruhy`) with its `zneni`, the full *Splněno* descriptor and all illustration titles. Competence, literacy and cross-curricular outcomes (113) were skimmed for coverage of the categories, not coded.
2. For each outcome I wrote a free-form note on which kind of tool could produce the described performance, using **fine-grained function tags** invented as I went, not a fixed list. Final tag counts (number of outcomes where the tag occurs):

   `llm 154 · search 35 · trans 35 · solver 29 · sheet 19 · sens 16 · map 15 · calc 14 · id 14 · code 12 · track 12 · img 11 · geo 9 · fact 7 · sim 7 · spell 6 · cad 5 · media 4 · stt 3 · sec 3 · sky 2 · tts 1 · music 1`

3. **Clustered** the tags into badges by three tests: a parent can tell the badges apart from the label alone; the badge covers outcomes that would otherwise get no badge; the category should still make sense in 2029 even if the products change. Mapping used (`build.py`):

   | Badge | Fine tags merged |
   |---|---|
   | AI chatbot | llm, stt |
   | Vyhledávání | search, fact |
   | Překladač a korektor | trans, spell, tts |
   | Výpočty a grafy | calc, solver, geo, sheet, sim |
   | Mapy a navigace | map, sky |
   | Měření a určování | sens, track, id |
   | Programování | code |
   | Digitální tvorba | img, media, music, cad |
   | (no badge) | sec (password managers, security check-ups; 3 outcomes) |

4. **Verdict per badge per outcome**, three levels, always *tool vs. a kid performing at the level the Splněno descriptor describes* (not vs. an adult expert, not vs. the minimum level):
   - **líp**: given the task as stated, the tool produces the observable performance more accurately, faster or more completely than a kid at that level.
   - **srovnatelně**: the tool does a substantial part as well as the kid, or does it equally well, but a core part stays with the kid (live interaction, hands-on execution, own content).
   - **zatím ne**: a tool attempts this exact performance but is reliably worse today.
   - **žádný nástroj**: no tool meaningfully performs it. Used for movement, own experience and reflection, values, relationships, behaviour in real situations, hands-on craft. A chatbot *can* fake a reading diary or a reflection; that is noted, but faking is not performing.
   When several fine tags map to one badge, the best verdict wins. The row-level "best" is the best across badges.
5. **Single rater, AI-drafted.** All verdicts were coded by one AI model (this analysis) from the RVP text. They are estimates, not measurements, and the site should say so (CLAUDE.md rule 8). The `uncertain` flag marks rows where a second rater could reasonably land one level apart.

## 3. The categories

### 3.1 AI chatbot
- **Definition:** a general AI assistant you talk or write to that produces new text, explanations, analyses or answers, and can read photos, documents and audio you give it.
- **Tools (2026):** ChatGPT, Gemini, Claude, Microsoft Copilot; voice modes of the same; AI tutors built on them; transcription-plus-summary (meeting/lecture notes).
- **Reliable:** fluent Czech and English writing at any school register; summarising and paraphrasing; explaining concepts in history, civics, geography, chemistry, biology at ZŠ level; analysing a given text, contract or model situation; drafting presentations, plans, CVs; describing a photo or artwork with correct terminology.
- **Weak:** judging source reliability and intent (propaganda, breaking news, fake news in a field); anything requiring local or personal knowledge (your school, your town, your feelings); spatial reasoning (nets of solids, positions in space); confident factual errors; inherited biases (it can itself be the manipulator the RVP wants kids to spot); live presence in a real conversation.
- **Scale anchors:** *líp* = "explain causes of colonialism", "summarise a text", "find missing items in a work contract". *srovnatelně* = "analyse manipulation", "propose a socially useful action", "evaluate an information system you use". *zatím ne* = taking part in a live face-to-face conversation (CJL ZV5-001).

### 3.2 Vyhledávání
- **Definition:** tools that find existing sources, facts, data and official information, and help check where a claim comes from.
- **Tools (2026):** Google, Seznam, Wikipedie, AI answers in search engines (Google AI Mode, Perplexity), Portál občana and municipal sites, ČHMÚ and other open-data portals, digitised archives and old photos, citace.com, reverse image search (Google Lens, TinEye), Demagog.cz.
- **Reliable:** finding office hours, agendas, life-situation guides; locating primary data (air quality, river flow); citations; finding local cultural events and institutions; first pass at "who published this".
- **Weak:** ranking quality (SEO and AI-generated pages); deciding what is true when sources disagree; AI answer boxes blur into the chatbot and inherit its errors.
- **Why separate from the chatbot:** the RVP repeatedly distinguishes *finding and citing sources* from *producing an answer* (CJL ZV9-009, DEJ ZV9-002/013, CHE ZV9-013, KRP-KRP, KDI-DAT). Keeping the badge lets a card say "the tool finds the sources; weighing them is still you". Convergence with chatbots is real; see §4.

### 3.3 Překladač a korektor
- **Definition:** tools that take text or speech *you* supply and convert or fix it: translate between languages, correct spelling and grammar, read aloud with standard pronunciation.
- **Tools (2026):** DeepL, Google Překladač (camera, conversation mode), Microsoft Translator, live translation in earbuds; Korektor, spell-check in Word, Google Docs and phone keyboards; text-to-speech in translators and operating systems.
- **Reliable:** A1–A2 reception tasks (menus, timetables, short texts, slow speech, subtitles); producing short texts, emails and forms in a foreign language; Czech morphology, syntax and punctuation checks; correct pronunciation as a model.
- **Weak:** real-time face-to-face conversation (latency, turn-taking, social awkwardness); idiom, register and tone in sensitive situations; the content still has to come from you (your feelings, your weekend).
- **Why spelling is merged here, not with the chatbot:** the data has only 6 outcomes where a spelling/grammar checker is the relevant tool, always in Czech. Its function is the same as the translator's: it transforms your text without adding content. That gives parents a useful line: *Překladač a korektor* = "fixes or converts what you wrote"; *AI chatbot* = "writes it for you".

### 3.4 Výpočty a grafy
- **Definition:** software that calculates, solves equations and word problems, constructs geometry, plots data and functions, and runs numeric simulations.
- **Tools (2026):** calculator and unit converters; Photomath, Microsoft Math Solver, Wolfram|Alpha (photo or typed problem to step-by-step solution); GeoGebra, Desmos; Excel, Google Sheets (with AI formula help); PhET simulations; chatbots in math mode.
- **Reliable:** everything arithmetic and algebraic at ZŠ level, including multi-step word problems with distractors; exact constructions and transformations; probability and enumeration; charts and averages; graphical solution of equations.
- **Weak:** chatbots and photo solvers on spatial tasks (nets, cross-sections, 3D positions) where dynamic geometry is needed instead; turning a messy real situation into a model when nobody has written it as a word problem; sanity-checking a result against reality.
- **Why calculators, solvers, GeoGebra and spreadsheets are one badge:** in 32/32 math outcomes at least one of them applies, and in 29 the verdict is "líp" regardless of which sub-tool. Splitting into "Kalkulačka" vs "Řešič" would put two badges with the same verdict on almost every math row. The cards can still name the right sub-tool in the explanation (calculator for decimals, GeoGebra for constructions, spreadsheet for data).

### 3.5 Mapy a navigace
- **Definition:** digital maps and geographic tools that locate places, plan routes, show layers (terrain, soil, history, aerial photos) and let you build your own maps; includes star maps.
- **Tools (2026):** Mapy.com, Google Maps, Geoportál ČÚZK with archive aerial photos, ArcGIS Online / StoryMaps, My Maps; Stellarium, sky-map apps.
- **Reliable:** route by parameters (shortest, least climb); finding and comparing places; historical change of landscape and settlements; thematic maps; constellations.
- **Weak:** needs signal and battery; does not build the *mental* map the RVP asks for (GEO ZV9-013); interpretation of what a change means is still yours.

### 3.6 Měření a určování
- **Definition:** tools that observe the real world for you: digital instruments and phone sensors that measure, wearables and apps that track body and food, and camera/microphone apps that identify what you point them at.
- **Tools (2026):** phyphox and other phone-sensor apps (motion, sound, light, magnetic field), digital scales, thermometers, multimeters, pH meters; smartwatches, Strava, training apps, Kalorické tabulky and food-scanning apps; Flora Incognita, PlantNet, iNaturalist/Seek, Merlin Bird ID, BirdNET, Google Lens, Shazam.
- **Reliable:** measuring motion, noise and time more precisely than eyes, ears and a stopwatch; logging training regularity, duration, intensity; nutrient totals; identifying plants and birds, often to species when the RVP asks only for the group.
- **Weak:** rocks and minerals (much less reliable than plants); designing the experiment and handling materials safely; the movement, effort, cooking or experiment itself.
- **Why sensors, trackers and photo ID are one badge:** separately they would be 16, 12 and 14 outcomes, all in science, health and PE, all with the same logic ("the phone perceives; you act and interpret"). Merged they form one badge parents can read at a glance.

### 3.7 Programování
- **Definition:** tools that write, explain and debug code, train simple machine-learning models, and program robots and automated devices.
- **Tools (2026):** chatbots and coding assistants (GitHub Copilot and similar), Scratch and micro:bit MakeCode, Teachable Machine, LEGO/robot kits, Arduino-based automation (smart pot, automatic watering).
- **Reliable:** generating and debugging text code at any ZŠ level; explaining what an algorithm does; decomposing a problem; training and evaluating a toy classifier.
- **Weak:** block languages are less directly supported than text code; testing with real users; framing the problem in the first place; physical building of the robot.

### 3.8 Digitální tvorba
- **Definition:** tools that make or edit images, video, music and 3D models, from AI generators to ordinary editors and 3D printing.
- **Tools (2026):** image generation in ChatGPT/Gemini, Adobe Firefly, Canva; CapCut, Stop Motion Studio, AI video generators; Suno, BandLab, loopers; Tinkercad and 3D printers.
- **Reliable:** polished images, infographics, posters, short edited videos and full songs from a prompt; precise 3D-printed parts.
- **Weak:** the outcomes are about *your* creative intent, experimenting with real materials in space, and reflecting on your process. Tools deliver output, not intent. Hence 15 of 19 verdicts are "srovnatelně" and 4 of the 6 VFV ones are flagged uncertain.

## 4. Decisions worth defending

**Generative AI is not one badge.** Three reasons from the data:
1. "AI" is inside almost every category: photo solvers, translators, plant ID, spell-checkers and map routing all run on machine learning. A single "AI" badge would mean either everything or only chatbots.
2. Text and media generation hit different outcomes: the chatbot appears across 16 of 18 subjects (155 outcomes); media generation clusters in art, crafts and a few creative CJL outcomes (19). One badge would hide that split.
3. They fail differently. A chatbot's risk is a wrong fact or a biased judgement; an image or song generator makes no factual claims, and its issue is authorship and intent. The explanation text a parent needs differs.

So the split is by **output and function** (text/reasoning vs. media), not by "AI vs. not AI". I considered splitting the chatbot further ("explains" vs. "writes"); rejected, because it is the same tool and parents would not tell the badges apart.

**Vyhledávání stays separate although it is converging with chatbots.** Its distinct value is in the source-criticism outcomes, where the right message is "finding is easy, judging is yours". If AI answer engines fully replace link lists by ~2028, merging the two is the obvious first simplification (would bring the set to 7).

**Rejected or absorbed candidates:**
- *Kalkulačka* as its own badge: absorbed into Výpočty a grafy (see 3.4).
- *Kontrola pravopisu* alone: 6 outcomes, absorbed into Překladač a korektor.
- *Rozpoznávání z fotky* alone (14) and *Měřicí přístroje/senzory* alone (16): merged into Měření a určování.
- *Simulace* (7, mostly "srovnatelně"): absorbed into Výpočty a grafy; planetarium apps went to Mapy.
- *Řeč* (dictation, TTS): too few to stand alone; dictation/transcription sits with the chatbot (it usually comes with summarising), TTS with the translator.
- *Zdraví a sport* (trackers, nutrition): 12 outcomes; absorbed into Měření a určování.
- *Bezpečnost* (password managers, privacy check-ups): 3 outcomes, no badge; mentioned in the row notes (INF ZV5-010, INF ZV9-013, VZB ZV9-010).

## 5. Aggregates

### 5.1 Per subject

"≥1 líp" = at least one badge with verdict líp. "best srovn." = best verdict is srovnatelně. "žádný" = no tool.

| Subject | n | ≥1 líp | best srovn. | zatím ne | žádný | uncertain |
|---|---|---|---|---|---|---|
| Matematika | 32 | 29 (91 %) | 3 | 0 | 0 | 3 |
| Další cizí jazyk | 9 | 8 (89 %) | 1 | 0 | 0 | 1 |
| Chemie | 14 | 11 (79 %) | 3 | 0 | 0 | 1 |
| Anglický jazyk | 28 | 22 (79 %) | 5 | 0 | 1 | 6 |
| Geografie | 18 | 13 (72 %) | 4 | 0 | 1 | 3 |
| Český jazyk a literatura | 25 | 18 (72 %) | 3 | 1 | 3 | 9 |
| Dějepis | 18 | 11 (61 %) | 4 | 0 | 3 | 4 |
| Výchova k občanství | 15 | 9 (60 %) | 3 | 0 | 3 | 2 |
| Informatika | 24 | 14 (58 %) | 8 | 0 | 2 | 6 |
| Fyzika | 14 | 8 (57 %) | 6 | 0 | 0 | 0 |
| Přírodopis | 18 | 10 (56 %) | 6 | 0 | 2 | 1 |
| Člověk a jeho svět | 35 | 16 (46 %) | 9 | 0 | 10 | 0 |
| Výchova ke zdraví a bezpečí | 17 | 3 (18 %) | 4 | 0 | 10 | 0 |
| Tělesná výchova | 34 | 5 (15 %) | 1 | 0 | 28 | 0 |
| Výtvarná a filmová výchova | 16 | 2 (12 %) | 9 | 0 | 5 | 4 |
| Hudební, taneční a dramatická výchova | 16 | 2 (12 %) | 5 | 0 | 9 | 5 |
| Osobnostní a sociální výchova | 21 | 1 (5 %) | 5 | 0 | 15 | 1 |
| Polytechnická výchova a praktické činnosti | 8 | 0 (0 %) | 6 | 0 | 2 | 0 |
| **All** | **362** | **182 (50 %)** | **85** | **1** | **94** | **46** |

By stage: ZV5 (end of grade 5) 47/112 = 42 % "líp", 41 no tool; ZV9 135/250 = 54 % "líp", 53 no tool. The higher share at ZV9 comes from knowledge-heavy subjects that start at grade 6 (Dějepis, Chemie, Geografie...), not from tools being better at harder material.

Reading the pattern neutrally: tools are strongest where the outcome's observable product is **text, numbers or a lookup**, and weakest where it is **a body, a relationship, a hands-on result or a personal stance**. Several subjects with high "líp" shares (math, languages) are also where the RVP itself stresses modelling, interaction and judgement; §7 discusses why the verdict there is about the task as written, not about the purpose of learning it.

### 5.2 Per category

| Badge | Outcomes | líp | srovnatelně | zatím ne | Sole badge on row | Main subjects |
|---|---|---|---|---|---|---|
| AI chatbot | 155 | 95 | 59 | 1 | 63 | CJL 21, INF 16, AJ 15, GEO 14 |
| Výpočty a grafy | 57 | 45 | 12 | 0 | 33 | MAT 32, FYZ 8, INF 5, ČJS 5 |
| Překladač a korektor | 42 | 35 | 7 | 0 | 20 | AJ 25, DCJ 9, CJL 8 |
| Měření a určování | 42 | 16 | 26 | 0 | 17 | ČJS 8, FYZ 7, PŘ 6, TV 5 |
| Vyhledávání | 39 | 27 | 12 | 0 | 7 | ČJS 8, DěJ 6, CJL 5, VkO 5 |
| Digitální tvorba | 19 | 4 | 15 | 0 | 10 | VFV 6, Polytech. 5, CJL 3 |
| Mapy a navigace | 17 | 11 | 6 | 0 | 3 | GEO 8, ČJS 5 |
| Programování | 12 | 9 | 3 | 0 | 5 | INF 8, MAT 2, Polytech. 2 |

Badges per row: 0 → 94, 1 → 158, 2 → 105, 3 → 5. Every badge is the *sole* badge on at least 3 rows, so none is redundant; Vyhledávání and Mapy are the most often co-assigned with the chatbot.

## 6. Uncertain verdicts (46)

Grouped by why a second rater could disagree:

- **Live interaction via translator** (AJ ZV5-005, ZV9-014/015/017/018; DCJ ZV9-006): conversation modes and earbuds work, but whether that is "comparable" to an A2 kid talking directly is a judgement call.
- **Source criticism and manipulation** (CJL ZV5-006, ZV9-009, ZV9-013; DěJ ZV9-002/003/013; VkO ZV9-003, ZV9-010; GEO ZV9-015; CHE ZV9-013): tools find and label, but judging credibility is their weakest point and they can be the source of the problem.
- **Spatial geometry** (MAT ZV5-006, ZV5-007, ZV9-008): dynamic geometry is strong, chatbots weak; the verdict depends on which tool a kid actually uses.
- **Creative work** (VFV ZV5-001, ZV9-001/002/003; HTD ZV9-002; CJL ZV9-015/016): technical polish vs. own intent.
- **Music perception** (HTD ZV5-004/006, ZV9-006/007): audio-analysis AI is improving fast; today "srovnatelně" is generous for some sub-skills.
- **Tool-operation outcomes** (INF ZV9-004, INF ZV5-005; GEO ZV9-013): the outcome is to operate a tool or to hold an internal map; see §7.3–7.4.
- **Others**: CJL ZV5-001, ZV5-004, ZV9-001, ZV9-002; AJ ZV9-012; INF ZV5-002/003, ZV9-003, ZV9-014; DěJ ZV9-004; GEO ZV9-009; PŘ ZV9-015 (rock ID); OSV ZV9-004 (self-presentation).

## 7. Edge cases

1. **The tool computes, the outcome is about modelling.** Many math outcomes say *modeluje* (MAT ZV5-002 fractions with pizza, ZV5-004 negatives via thermometer and debt, ZV9-017 expressions for situations). Photo solvers and chatbots now handle the whole pre-written word problem, including setting up the expression, so the verdict is "líp". What no tool does is notice that a real, unwritten situation is a fractions problem in the first place. The coding rates the task as the RVP writes it; the note says where the modelling sits. This is the most important caveat for the site's math cards.
2. **The tool translates, the outcome is about interaction.** Reception and written production in AJ/DCJ are "líp" across the board at A1–A2. Interaction outcomes (*zapojí se do rozhovoru*, *diskutuje*) are "srovnatelně" and uncertain: an interpreter app technically conveys meaning, but the RVP describes turn-taking, spontaneity and reacting to a partner, which the app mediates rather than performs.
3. **The tool is the medium.** Some outcomes are *about using* a tool: GIS (GEO ZV9-002), choosing apps and managing files (INF ZV5-008/009), measuring performance with an app (TV ZV5-008, ZV9-008), training a model (INF ZV9-004). "Better than a kid" is ill-posed when the kid's job is to operate the tool. Coding: where an agent or automation could do it end-to-end, the badge gets a verdict and a note; where using digital tech is the outcome itself (INF ZV5-008/009), "žádný nástroj" with the note "tools are the subject, not a substitute".
4. **Proxy performance vs. internal capacity.** Reading comprehension (CJL ZV5-005), mental maps (GEO ZV9-013), "own words" (ČJS ZV5-014), notes from a lecture (AJ ZV9-019). The tool produces the visible output better, but the outcome describes something in the kid's head. Verdict follows the observable performance; the note flags the gap. Dimension (b) should pick these up.
5. **Your content, the tool's words.** "Describe your feelings / your weekend / your opinion" in English (AJ ZV9-009/010/011): a translator delivers the English, the content must come from the kid. Rated "líp" for the language part, with a note.
6. **Faking is not performing.** Reading diaries, reflections and value ladders (CJL ZV5-008, VFV ZV9-005, VkO ZV9-002 ...) are "žádný nástroj" even though a chatbot will happily write one. Worth one sentence on the site: the tool can hand in the text but cannot have the experience.
7. **AI as the object of the outcome.** DěJ ZV9-003 asks kids to compare history in film, literature and *AI products*; CJL ZV9-013 and PTS outcomes ask them to spot manipulation. The tool that would "do" the outcome is part of what is being examined.
8. **Simulation vs. experiment.** Physics, chemistry and ČJS outcomes ask for own experiments. Virtual labs (PhET) and sensors are "srovnatelně": they replace measuring or visualising, not designing and running a safe experiment.
9. **Instructions vs. action.** First aid, fire, traffic and emergencies: the Záchranka app sends your location and guides you, warning systems alert. They do not bandage, evacuate or ride the bike. All "žádný nástroj" with a note.
10. **Tool choice changes the verdict.** Spatial geometry is strong with GeoGebra and weak with a chatbot (MAT ZV9-008: chatbot "zatím ne", 3D geometry app "srovnatelně"); plant ID is excellent, rock ID poor. Per-category verdicts are more honest than a single "AI can do this" flag, which is an argument for category badges.
11. **Above the level asked.** Plant ID apps identify species when PŘ ZV9-012 asks only for broader groups; the comparison is still with the kid at the outcome's level.

## 8. Competence and literacy outcomes (skimmed, not coded)

The 113 non-subject outcomes fit the same 8 badges without new categories:
- *Logicko-matematická* (MRF, POM, MUV, MOD): checking results and finding patterns → Výpočty a grafy "líp"; "vyvíjí/inovuje matematické modely" (MOD ZV9) is a clear "srovnatelně/uncertain".
- *Čtenářská a pisatelská*: reading and writing for experience and self-reflection → mostly "žádný nástroj"; analysing author intent (KCP) → AI chatbot.
- *Digitální kompetence*: KDI-DAT (search and judge data) → Vyhledávání + chatbot, weak on reliability; KDI-TDO (generate digital content) → Digitální tvorba + chatbot; KDI-VIN (use tech to make work efficient) is a "tool is the medium" case.
- *Řešení problémů*: KRP-VED/BAD (data-based decisions, research plans) → chatbot "srovnatelně"; KRP-KRP (verify information) → Vyhledávání, tools weak.
- Personal, social, civic, cultural, entrepreneurial competences and the cross-curricular themes are overwhelmingly "žádný nástroj"; the exceptions are media-analysis outcomes (PTS ZV5-002, ZV9-002/003) → chatbot "srovnatelně".

## 9. Notes for using this on the site

- Show the badge with its verdict word, not just an icon: "AI chatbot: zvládne líp" reads very differently from "Digitální tvorba: srovnatelně".
- For "žádný nástroj" show it explicitly; a quarter of the curriculum is a finding, not a gap.
- Per CLAUDE.md, each card should state that the verdict is an AI-drafted estimate from the RVP text, dated (tools as of 2026), and link the uncertain flag where set.
- The CSV `note` column is English working notes, not site copy.
