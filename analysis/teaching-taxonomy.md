# Taxonomie způsobů výuky a procvičování – podklad pro rubriku „Proč se to učím?"

Datum: 2026-10-18. Legenda: **[Z]** = přímo ze zdroje, **[S]** = moje syntéza/návrh, **[?]** = z paměti nebo sekundárního zdroje, nebylo ověřeno na primárním dokumentu.

Omezení: WebFetch vracel 403/404 u EEF, SAGE (Dunlosky), UNESCO a npi.cz PDF. Hodnocení Dunlosky, ICAP, Bastani, UNESCO a NPI AI vycházejí ze shrnutí ve vyhledávači (APS press release, ASU, PNAS/SSRN abstrakt, MŠMT). Před zveřejněním je potřeba ověřit citace v primárním textu. Čísla EEF jsou nejméně spolehlivá, protože se aktualizují průběžně.

## 1. Co říkají české zdroje

### 1.1 Nový RVP ZV (lokální soubor, ověřeno přímo)
Soubor: `/home/zdenek/projects/rvp/data_final_rvp_zv_full_mp_20251216.json`. Skripty jsou v `/tmp/claude-1000/-home-zdenek-projects-rvp/5376c4f1-10bf-4054-bc5c-f6519b8e4426/scratchpad/teaching-taxonomy/` (g.py, h.py, k.py).

- **Žádný uzavřený seznam metod výuky tam není.** RVP rozlišuje „vzdělávací strategie školy" a „vzdělávací strategie učitele" (kap. 3.1.3). Strategie učitele jsou „konkrétní didaktické postupy (výukové metody, organizační formy práce, výukové situace, výukové prostředky, způsoby hodnocení a reflexe)". Pro rubriku je to jen rámec, ne klasifikace. [Z]
- **Pedagogický konstruktivismus:** nová témata se propojují s předchozími znalostmi a žáci je aplikují ve škole i v životě. Dále se zmiňují projektová a bloková výuka, vrstevnické učení, tandemová výuka, aktivní a kooperativní učení, prožitkové učení, badatelské aktivity, učení založené na praktické zkušenosti a individualizace. [Z, 3.1.3 metodický komentář]
- **Formativní hodnocení (kap. 5):** společné cíle a kritéria, průběžná popisná zpětná vazba, sebehodnocení a vrstevnické hodnocení, „práce s chybou tak, aby byla chyba vnímána jako nedílná součást učení", diagnostické portfolio. Sumativní hodnocení až na konci celku. [Z]
- **Klíčová kompetence k učení:** u každého uzlového bodu je „VZDĚLÁVACÍ STRATEGIE UČITELE" jako seznam výroků v 1. osobě. Příklady: sekvence navazujících hodin, kritéria vytvářená se žáky, „nechávám žáky samostatně objevovat", „dávám prostor žákům učit se mezi sebou", sdílení „procvičovacích digitálních programů", reflexe toho, co žákům pomáhá. Je tam i growth mindset („Mé schopnosti nejsou fixní…") a vysvětlení, proč se obsah učí. [Z, klicoveKompetence/0, „Umění se učit", „Smysl a cíl učení"]
- Tyto výroky jsou dobrý zdroj české terminologie a citací „RVP říká…". Chybí v nich ale důkazní váha, tedy co je účinnější.
- **Digitální kompetence a AI:** jen 30 zásahů na regex AI/generativní, převážně v průřezových tématech (ilustrace „AI jsme my": kritický odstup od výstupů AI) a v digitální kompetenci (vyhledávání informací, tvorba obsahu). RVP neobsahuje taxonomii „AI jako tutor × AI jako autor úkolu". [Z, částečně prověřeno – zkontrolovat zbývající zásahy]

### 1.2 Další české zdroje
| Zdroj | Co jsem zjistil | Stav |
|---|---|---|
| Maňák & Švec, *Výukové metody*, Paido 2003, ISBN 80-7315-039-5 | Klasifikace metod podle více hledisek (didaktické: zdroj poznání; psychologické: aktivita a samostatnost žáka). Kapitoly jsou v encyklopedii Portál 2009 „Formy a metody výuky". Přesné členění jsem neověřil. Z paměti [?]: klasické metody slovní / názorně demonstrační / dovednostně praktické (Maňák-Švec) a „komplexní" metody (frontální, skupinová, projektová, kooperativní, …). | [?] Kniha je placená, není open license. |
| Skalková, *Obecná didaktika* | Nepodařilo se potvrdit. Klasifikace podle fází výuky (motivační, expoziční, fixační, diagnostické, aplikační) – z paměti [?]. | [?] |
| ČŠI, *Kritéria hodnocení podmínek, průběhu a výsledků vzdělávání* | Čtyřstupňová škála (výborný/očekávaný/vyžaduje zlepšení/nevyhovující) a oblast „Výuka" s kritérii (např. 4.1 plánování). Nenašel jsem přesné znění pozorovacích kategorií pro 2024/25. Dokument je schvalován MŠMT a veřejný na csicr.cz. | částečně; kritéria 2020/21: https://csicr.cz/html/2020/Kriteria_hodnoceni_2020_2021/resources/_pdfs_/Kriteria-hodnoceni_2020-2021-popis-kriteria_cistopis_52.pdf |
| NPI ČR / MŠMT – AI | 28. 8. 2024 NPI vydalo tři materiály o AI (doporučení pro ředitele, učitele, žáky a rodiče; sedm bodů, školy je mohou upravit). 2025: FAQ „AI a právo ve škole", „AI jako asistent učitele" a plakát na https://digitalizace.rvp.cz/. Právní stanovisko: absolutní zákaz AI ve výuce není právně podložen, je třeba dodržet AI Act, GDPR a školský zákon; zjistit věkové limity aplikací. Program základka.ai (ČAUI) pro všechny učitele ZŠ 2025/26. Přesné znění sedmi bodů jsem nezískal. | URL: https://msmt.gov.cz/npi-vydalo-navody-pro-pedagogy-jak-na-umelou-inteligenci-ve (v mém pokusu „stránka nenalezena" – ověřit), https://digitalizace.rvp.cz/files/2025-faq-ai-a-pravo-ve-skole.pdf, https://digitalizace.rvp.cz/files/2025-faq-ai-umela-inteligence-jako-asistent-ucitele.pdf, https://revize.edu.cz/files/ai-doporuceni-online-a4.pdf |
| MŠMT Strategie 2030+, Pedagogický slovník, Metodický portál RVP.CZ | Nestihl jsem prověřit. | neprověřeno |

**Závěr pro Česko:** české oficiální zdroje poskytují *terminologii a legitimitu* (RVP: konstruktivismus, formativní hodnocení, práce s chybou, kooperace), ale ne *hodnocení účinnosti*. Důkazní váhu musí dodat mezinárodní syntézy.

## 2. Mezinárodní syntézy

| Zdroj | Obsah | Licence/dostupnost |
|---|---|---|
| **Dunlosky et al. 2013**, *Improving Students' Learning With Effective Learning Techniques*, PSPI 14(1), DOI 10.1177/1529100612453266 | 10 technik. **Vysoká užitečnost:** practice testing, distributed practice. **Střední:** elaborative interrogation, self-explanation, interleaved practice. **Nízká:** summarization, highlighting/underlining, keyword mnemonic, imagery for text, rereading. [Z přes APS press release; v monografii je mnemotechnika a imagery také „low"] | Článek je v SAGE (placený/otevřený podle přístupu); citovat, ne kopírovat. |
| **EEF Teaching and Learning Toolkit** | Přes 30 „strands" s dodatečnými měsíci pokroku, cenou a jistotou důkazu. Průběžně aktualizováno. Zjištěné hodnoty (sekundárně): feedback +6 (EEF píše i o +8 u kvalitní zpětné vazby), metacognition and self-regulation +7 nebo +8 (aktualizace 2025 hlásí +8), reading comprehension strategies +6, peer tutoring +5. [?] | https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit (403 pro bota). Licence: pravděpodobně OGL/CC-BY – ověřit. Cizí alternativa: Evidence for Learning (AU). |
| **Rosenshine, Principles of Instruction** (American Educator 2012) | 10 principů: denní opakování, nový obsah po malých krocích, mnoho otázek, modelování, řízená praxe, kontrola porozumění, vysoká úspěšnost, opory pro těžké úlohy, samostatná praxe, týdenní a měsíční opakování. Zdroje potvrzují jen první polovinu, zbytek z paměti [?]. | AFT, volně na webu. |
| **ICAP, Chi & Wylie 2014**, Educational Psychologist 49(4) | Pasivní < aktivní < konstruktivní ≤ interaktivní (P<A<C≤I). Příklady: pasivní = poslouchat, aktivní = podtrhávat/manipulovat, konstruktivní = generovat nový výstup (mapa, vlastní vysvětlení), interaktivní = dialog s vrstevníkem se vzájemnou konstrukcí. Kontrolní studie: jedna laboratorní studie (n=161) ICAP nepotvrdila (kognitivní zátěž). [Z přes ASU/shrnutí] | https://csi.asu.edu/wp-content/uploads/2018/01/ChiWylie2014ICAP.pdf |
| **Hattie, Visible Learning** | Kritika: míchání nesourodých studií (meta-meta-analýza), svévolný práh d=0,4, chyby ve znaménku (class size), nesrovnatelnost effect sizes (Simpson 2020, Slavin, Kraft). **Doporučení: jako zdroj pro rubriku nepoužít, nanejvýš jako doplněk.** [?] | Placená kniha. |
| **Deans for Impact, The Science of Learning** (2015) | Nepovedlo se stáhnout. [?] Shrnuje kognitivní vědu do praxe: retrieval, spacing, feedback, prior knowledge. | Volně ke stažení – ověřit. |
| **UNESCO 2023, Guidance for generative AI in education and research** | Lidsky-centrovaný přístup, ochrana dat, školení učitelů, doporučení vlád; věkový limit 13 let „zvážit" (UNESCO sama poznamenává, že řada lidí navrhuje 16). [Z přes zpravodajství] | https://unesdoc.unesco.org/ark:/48223/pf0000386693 (403). Licence CC BY-SA 3.0 IGO [?]. |
| **Bastani et al. 2025, PNAS 122(26)** „Generative AI without guardrails can harm learning" | RCT, zhruba 1000 středoškoláků (Turecko, matematika). GPT Base: +48 % výkon při procvičování, ale **−17 %** na testu bez AI. GPT Tutor (tipy, ne odpovědi): +127 % při procvičování a ztráty z velké části odstraněny. Krátkodobé. [Z přes abstrakt/Wharton] | https://papers.ssrn.com/abstract=4895486 |
| **Frameworky** SAMR, Bloom revised (Anderson & Krathwohl 2001) | Nehodnotím účinnost. Bloom revised: pamatovat, rozumět, aplikovat, analyzovat, hodnotit, tvořit – užitečný pro označení *kognitivní úrovně* úkolu. SAMR (nahrazení/rozšíření/úprava/předefinování) popisuje roli technologie, ne účinnost učení. [?] | Obojí volně citovatelné. |

## 3. Návrh taxonomie (12 kategorií) [S]

Princip: kategorie jsou *činnosti žáka*, ne předměty. Každá je navázána na důkaz. Ke každé uvádím hodnocení (nejlepší dostupný zdroj) a příklady z české ZŠ. Hodnocení „vysoké/střední/nízké" je syntéza z Dunlosky + ICAP + EEF; není to jedno měřítko.

| # | Kategorie (CZ) | Definice | Důkaz | Příklady |
|---|---|---|---|---|
| 1 | **Sebetestování (vybavování z paměti)** | Žák si bez předlohy vybavuje, co umí, a hned zjistí, zda měl pravdu. | Dunlosky: *practice testing* – vysoká užitečnost [Z] | Malá násobilka na kartičkách nebo ústně „zpaměti"; pravopisný diktát bez předlohy; mini-kvíz na začátku hodiny |
| 2 | **Rozložené opakování** | Stejné učivo se vrací v krátkých dávkách v rostoucích odstupech. | Dunlosky: *distributed practice* – vysoká [Z] | Pět minut násobilky denně místo hodiny v neděli večer; vyjmenovaná slova opakovaná každý týden |
| 3 | **Prokládané procvičování** | Střídání typů úloh, ne desítky stejných za sebou. | Dunlosky: *interleaved practice* – střední [Z] | Smíšený cvičný list: i/y po b, l, m, p, s, v, z, nikoli 30× po „b"; matematika: sčítání, odčítání a násobení v jedné sadě |
| 4 | **Vysvětlování a „proč?"** | Žák vlastními slovy vysvětluje postup nebo odpovídá na „proč to platí?" | Dunlosky: *self-explanation*, *elaborative interrogation* – střední [Z]; ICAP konstruktivní [Z] | „Vysvětli bráchovi, proč se píše ‚mýdlo' s ý"; zdůvodnění postupu u slovní úlohy |
| 5 | **Tvorba vlastního výstupu** | Žák z látky vytvoří něco nového: mapu, vlastní text, úlohu, model. | ICAP konstruktivní > aktivní > pasivní [Z, sporné ve studii s kognitivní zátěží] | Myšlenková mapa k vlastivědě; vlastní slovní úloha; slohová práce s kritérii a přepracováním |
| 6 | **Řízená praxe s okamžitou zpětnou vazbou** | Učitel/rodič/aplikace ukáže, kde je chyba, a žák ji opraví. | EEF Feedback ≈ +6 měsíců (+8 u kvalitní) [?]; RVP: formativní hodnocení, práce s chybou [Z]; Rosenshine: řízená praxe [Z] | Učitel prochází lavice při cvičení; oprava chyb s komentářem místo samé známky |
| 7 | **Postupné odhalování (modelování a malé kroky)** | Ukázka vyřešeného příkladu, pak částečně vyřešené, pak samostatné. | Rosenshine: modelování, malé kroky, opory [Z/?]; EEF: ? | Učitel nahlas řeší dělení se zbytkem, pak žák dopočítá krok; vzorový odstavec slohu |
| 8 | **Strategie čtení a metakognice** | Žák plánuje, sleduje a hodnotí své učení, učí se strategie (predikce, ptaní se, shrnutí vlastními slovy). | EEF metacognition +7/+8 [?], reading comprehension strategies +6 [?]; RVP „Umění se učit" [Z] | Čtenářské strategie (předvídání, otázky k textu); sebehodnocení „Co jsem se naučil, co ještě ne" |
| 9 | **Učení ve dvojicích a skupinách** | Žáci si vysvětlují a diskutují nad společným úkolem. | ICAP interaktivní (nejvyšší očekávaný efekt) [Z]; EEF peer tutoring ≈ +5 [?]; RVP: kooperativní a vrstevnické učení [Z] | Čtenářská dvojice; skupinový pokus ve fyzice; žáci si navzájem zkoušejí násobilku |
| 10 | **Praktické bádání a projekt** | Žák používá znalost při reálném problému, pozorování nebo projektu. | RVP: badatelské, prožitkové, projektové [Z]. Účinnost závisí na vedení (nemám pro ni číslo) | Pozorování klíčení semínek; projekt „Naše obec"; vyrobit rozpočet třídního výletu |
| 11 | **AI jako tutor/zkoušející** | Chatbot klade otázky, dává nápovědu, kontroluje odpovědi žáka, ale nepíše hotové řešení. Žák nejdřív přemýšlí sám. | Bastani 2025: tutor s „guardrails" nepoškodil výsledek, na rozdíl od volného GPT [Z přes abstrakt]; nepřímo kategorie 1 a 6; NPI/UNESCO: lidsky-centrovaný přístup, kontrola dospělým [Z] | Žák napíše: „Zeptej se mě na vyjmenovaná slova po B a nic mi neprozrazuj." AI vysvětlí chybu u slovní úlohy, ale nezadá výsledek |
| 12 | **Kritická práce s výstupem AI/zdroje** | Žák ověřuje, opravuje a hodnotí text AI, zdroje a vyhledávání. | RVP: kritický odstup od výstupů AI, digitální kompetence [Z]; NPI: odpovědnost za výstupy [Z přes shrnutí] | Najít chyby ve vygenerovaném referátu; porovnat odpověď AI s učebnicí |

**Poznámka k rozsahu:** kategorie 1–4 jsou kognitivně nejlépe podložené (laboratorní a třídní studie), 8–9 mají silné syntézy EEF, 10–12 mají slabší nebo jiný typ důkazu (rámcové, politické, jednotlivé RCT). V rubrice to musí být vidět (štítek „síla důkazu").

## 4. Anti-patterny (méně účinné způsoby) [S s citacemi]

| Anti-pattern | Proč je slabé | Zdroj |
|---|---|---|
| **Opakované čtení / „přečíst si to ještě jednou"** | Nízká užitečnost; vytváří dojem znalosti. Přechod na sebetestování. | Dunlosky 2013 – rereading low [Z] |
| **Zvýrazňování a podtrhávání** | Nízká užitečnost; v ICAP jen „aktivní". | Dunlosky 2013 – highlighting low [Z]; Chi & Wylie 2014 [Z] |
| **Přepisování a opisování (např. „opiš 10× vyjmenovaná slova")** | Motoricky aktivní, ale ne konstruktivní; v Dunlosky samostatně nehodnoceno, zařazuji pod „rereading/aktivní". Opisování bez vybavování je [S]. | ICAP (aktivní) [Z]; použití na opisování [S] |
| **Shrnutí bez zkoušení (vypracovat výpisky)** | Nízká užitečnost, pokud žák nezvládá techniku shrnutí; fungují, jen když se pak testuje. | Dunlosky 2013 – summarization low [Z] |
| **Memorování bez porozumění (např. biflování definic, pravidlo bez příkladů)** | Nemá přímo rating v Dunlosky; je v rozporu s RVP (pedagogický konstruktivismus, propojování s prior knowledge) a s ICAP (pasivní/aktivní). Výjimka: automatizace faktů (násobilka), kde se doporučuje kategorie 1–2. | RVP 3.1.3 [Z]; ICAP [Z]; rozlišení [S] |
| **Nacvičování jednoho typu úloh dokola (30× stejné i/y)** | Zdánlivý úspěch při procvičování, horší přenos. | Dunlosky – interleaving [Z] |
| **Nahuštění před testem (cramming)** | Hodnota nízká dlouhodobě; distributed practice vyšší. | Dunlosky – distributed practice [Z] |
| **Nechat AI vypracovat úkol (domácí úkol, sloh, matematiku)** | RCT: výkon při procvičování vzrostl, na testu bez AI klesl o 17 %. Žák nezíská schopnost, kterou úkol trénoval. | Bastani 2025 [Z přes abstrakt] |
| **AI, která dává hotová řešení místo nápovědy** | Totéž; „tutor" s nápovědami škodu odstranil. | Bastani 2025 [Z] |
| **Slepá důvěra ve výstup AI** | Odporuje cíli kritického odstupu; riziko chyb a stereotypů. | RVP, průřezová témata – ilustrace „AI jsme my" [Z] |
| **Známka bez zpětné vazby** | RVP vyžaduje popisnou zpětnou vazbu a práci s chybou. | RVP kap. 5 [Z]; EEF feedback [?] |

## 5. Jak použít jako rubriku

Pro každou školní činnost (např. „doplňování i/y") uvést: (a) **dobré způsoby** – kategorie 1–4/6 + konkrétní příklad, (b) **horší způsoby** – anti-pattern, (c) **AI-varianta** – kategorie 11 vs. anti-pattern „AI vypracuje", (d) štítek důkazu: „vysoká/střední/nízká užitečnost (Dunlosky)", „+X měsíců (EEF)", „RVP", „jedna RCT". Nepoužívat holé čísla EEF bez data aktualizace.

Doporučené další kroky: stáhnout primární dokumenty (EEF, Dunlosky PDF, Rosenshine, UNESCO, NPI) přes jiný nástroj než WebFetch; ověřit licenci EEF (OGL) a UNESCO (CC BY-SA IGO); získat Maňák & Švec 2003 z knihovny; projít ČŠI kritéria 2024/25.
