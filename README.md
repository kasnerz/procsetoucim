<p align="center"><img src="docs/scene.svg" width="520" alt="Panáčci, kteří běhají, hrají na kytaru, čtou mapu a volí, a nad nimi čip s nápisem AI"></p>

# Proč se to učím?

Web [procsetoucim.cz](https://procsetoucim.cz) ukazuje, k čemu je dobré umět věci ze základní školy, i když je zvládne AI. AI modely prošly nové RVP pro základní vzdělávání bod po bodu a z každého bodu vznikla karta: proč se to učit, jestli při tom pomůže AI chatbot, internet, aplikace nebo klasický nástroj, která povolání tu dovednost potřebují a jak se to učit s pomocí AI. Texty karet napsala AI, údaje o povoláních pocházejí z veřejných dat (ESCO, Cedefop, ILO). Postup popisuje stránka [O projektu](https://procsetoucim.cz/o-projektu/).


## Repozitář

- `site/` – web v Astru (`npm install`, `npm run dev`)
- `pipeline/` – skripty, které ze zdrojových dat sestaví `content/`, a návody pro psaní karet
- `content/` – karty, texty od AI a odhady, jak moc které povolání dovednost využívá
- `feedback/` – server pro připomínky z webu
- `docs/` – metodika karet a podmínky použití dat

Zdrojová data (`data/`) v repozitáři nejsou. Data Cedefop Skills Forecast se podle podmínek nesmí dál šířit, a proto chybí i z nich sestavený soubor `content/labour/isco2.json`; bez něj se web sestaví bez údajů o skupinách povolání. Data jsou k dispozici po registraci na [webu Cedefop](https://www.cedefop.europa.eu/en/projects/skills-forecast).

## Zdroje a licence

- RVP ZV: NPI ČR, otevřená data (16. 12. 2025), [prohlednout.rvp.cz](https://prohlednout.rvp.cz/)
- ESCO – European Skills, Competences, Qualifications and Occupations, v1.2.1 (Evropská komise)
- European Centre for the Development of Vocational Training (Cedefop). Cedefop Skills Forecast 2026, Thessaloniki: Greece, Downloaded from: https://www.cedefop.europa.eu/en/projects/skills-forecast
- Gmyrek, P. a kol. (2025): Generative AI and Jobs: A Refined Global Index of Occupational Exposure. ILO Working Paper 140, data [CC BY 4.0](https://github.com/pgmyrek/2025_GenAI_scores_ISCO08)
- Ikony [Matita](https://github.com/matita-dev/icons) (MIT), písma Grandstander a Outfit (SIL OFL 1.1)
- `docs/anti-ai-slop-cz*.md`: © 2026 Filip Dřímalka, MIT, [nowork-ai/anti-ai-slop-cz](https://github.com/nowork-ai/anti-ai-slop-cz)

## Licence

Kód je pod licencí [MIT](LICENSE), obsah (karty, texty, data v `content/`, kresby) pod [CC BY-SA 4.0](LICENSE-content). Logo webu do licence nespadá, výjimky vypisuje [LICENSE-content](LICENSE-content).
