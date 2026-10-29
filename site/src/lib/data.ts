import fs from "node:fs";
import path from "node:path";

// The site only reads content/. See docs/content-schema.md.
const CONTENT = path.resolve(process.cwd(), "..", "content");

function read<T>(rel: string, fallback: T): T {
  try {
    return JSON.parse(fs.readFileSync(path.join(CONTENT, rel), "utf8")) as T;
  } catch {
    return fallback;
  }
}

/** tools-v2: binary. No tool does it for you; the question is whether it helps while you do it. */
export type Verdict = "pomuze" | "nepomuze";
export type RuleId = "P1" | "P2" | "P3" | "P4" | "P5";
export type AsideId = "O1" | "O2" | "O3";
export type ToolId = "chatbot" | "internet" | "aplikace" | "klasicky";

export interface Outcome {
  code: string;
  kind: "obor" | "gramotnost" | "kompetence" | "prurezove";
  area: { code: string; name: string };
  subject: { code: string; name: string };
  okruh: { code: string; name: string } | null;
  stage: "ZV3" | "ZV5" | "ZV9";
  stageLabel: string;
  text: string;
  rationale?: string;
  levels: { name: string; text: string }[];
  illustrations: { level: string; title: string; text: string; url: string }[];
  prev: string[];
  next: string[];
  related: string[];
  url: string;
  graph: { foundationCount: number; transferCount: number; transfer: string[] };
}

export interface Activity {
  slug: string;
  title: string;
  aliases: string[];
  outcome: string;
  /** Official RVP points the card simplifies: the full point, and the part used when only part of it is. */
  levelSource: { level: string; point: string; quote: string }[];
  /** Simplification rules applied (see RULES and docs/activity-method.md). */
  rules: RuleId[];
  inspiration?: { title: string; url: string }[];
  /** AI-written "Proč se to učíš" text, the heart of the card (content/comments/<slug>.json, prompt card-v5). */
  comment: string;
  /** AI-written suggestions how to learn or practise it with AI ("Jak se to učit s AI"), three since card-v4, each
   *  with a short title since card-v5 (older ones have an empty title). */
  learnWithAi: { title: string; text: string }[];
  commentBy?: { draftedBy: string; promptVersion: string };
  tools: Record<ToolId, { verdict: Verdict; why: string }>;
  escoSkills: string[];
  review: { draftedBy: string; promptVersion: string; reviewed: boolean };
}

export interface Occupation {
  id: string;
  uri: string;
  label: string;
  labelAlt: string[];
  description: string;
  isco4: string;
  isco2: string;
  ilo: { score: number; gradient: string } | null;
  collections: { research: boolean; green: CollectionHits; digital: CollectionHits };
}
/** How many of the occupation's ESCO skills (essential and optional) are in an ESCO collection, with up to 3 of them. */
export interface CollectionHits { count: number; of: number; examples: string[] }

export interface Measures {
  occupationCount: number;
  employmentShare: number;
  highExposureShare: number;
  trendPct: number;
  topOccupations: string[];
  foundationCount: number;
  transferCount: number;
  employment: number;
  byMajor: Record<string, number>;
  exposureMix: Record<Exposure, number> | null;
}
export type Exposure = "high" | "medium" | "low" | "none";

export interface Isco2 {
  code: string;
  label: string;
  employment2025: number;
  employment2035: number;
  changePct: number;
  reliable: boolean;
  /** Cedefop job openings 2026-2035: replacement demand (people leaving) plus the change in employment. */
  replacement2026to2035: number;
  openings2026to2035: number;
  qualification2035: Record<Qualification, number>;
}
export type Qualification = "high" | "mediumVocational" | "mediumGeneral" | "low";
/** Cedefop's four qualification levels (ISCED 5-8, 3-4 vocational, 3-4 general, 0-2) in Czech school terms. */
export const QUALIFICATIONS: { id: Qualification; label: string; acc: string; fill: string }[] = [
  { id: "high", label: "vysoká nebo vyšší odborná škola", acc: "vysokou nebo vyšší odbornou školu", fill: "f-blue-solid" },
  { id: "mediumVocational", label: "střední odborná škola nebo učiliště", acc: "střední odbornou školu nebo učiliště", fill: "f-blue" },
  { id: "mediumGeneral", label: "gymnázium", acc: "gymnázium", fill: "f-light" },
  { id: "low", label: "základní škola", acc: "jen základní školu", fill: "f-empty" },
];

export const outcomes = read<Record<string, Outcome>>("rvp/outcomes.json", {});
export const occupations = read<Record<string, Occupation>>("esco/occupations.json", {});
export const skills = read<Record<string, { uri: string; label: string; description: string; essentialFor: string[]; optionalFor: number }>>("esco/skills.json", {});
export const measures = read<Record<string, Measures>>("measures.json", {});
export const isco2 = read<Record<string, Isco2>>("labour/isco2.json", {});
/** ISCO-08 major (1-digit) and sub-major (2-digit) group labels from ESCO; the 2-digit groups are the site's
 *  "skupiny povolání", the level of the Cedefop forecast. */
export const groups = read<Record<string, string>>("esco/groups.json", {});
export const meta = read<Record<string, any>>("meta.json", {});

function loadActivities(): Activity[] {
  const dir = path.join(CONTENT, "activities");
  let files: string[] = [];
  try {
    files = fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort();
  } catch {
    return [];
  }
  return files.flatMap((f) => read<Activity[]>(path.join("activities", f), [])).map((a) => {
    const c = read<{ draftedBy: string; promptVersion: string; comment: string; learnWithAi?: (string | { title: string; text: string })[] | string } | null>(path.join("comments", `${a.slug}.json`), null);
    return { ...a, comment: c?.comment ?? "", learnWithAi: [c?.learnWithAi ?? []].flat().filter(Boolean).map((t) => (typeof t === "string" ? { title: "", text: t } : t)), commentBy: c ? { draftedBy: c.draftedBy, promptVersion: c.promptVersion } : undefined };
  });
}

export const activities = loadActivities();

/** Every RVP point of a covered goal: the cards made from it, or why it was set aside. */
export interface Coverage {
  outcome: string;
  points: { level: string; point: string; cards: string[]; aside: { code: AsideId; refs: string[] } | null }[];
}
export const coverage: Record<string, Coverage> = Object.fromEntries(
  activities
    .map((a) => a.outcome)
    .filter((c, i, arr) => arr.indexOf(c) === i)
    .map((c) => [c, read<Coverage | null>(path.join("coverage", `${c.toLowerCase()}.json`), null)])
    .filter(([, v]) => v),
);

/** All occupations that need a card's skills, most relevant first. */
export const activityOccupations = read<Record<string, string[]>>("activity-occupations.json", {});
/** Occupation id -> slugs of the cards whose skills it needs (inverse of activityOccupations). */
export const occupationCards = new Map<string, string[]>();
for (const [slug, ids] of Object.entries(activityOccupations)) for (const id of ids) occupationCards.set(id, [...(occupationCards.get(id) ?? []), slug]);
/** "karta" / "karty" / "karet" after a number. */
export const cardsWord = (n: number) => (n === 1 ? "karta" : n >= 2 && n <= 4 ? "karty" : "karet");

/** AI notes on how an occupation uses a card's activity. */
export function jobNotes(slug: string): { draftedBy: string; notes: Record<string, string> } {
  return read(path.join("jobnotes", `${slug}.json`), { draftedBy: "", notes: {} });
}
/** How much each occupation uses a card's skill, 0-4 (decision model Jev, pipeline/relevance.py); {} when not scored. */
export function relevance(slug: string): Record<string, number> {
  const d = read<{ scores: Record<string, { use: number }> }>(path.join("relevance", `${slug}.json`), { scores: {} });
  return Object.fromEntries(Object.entries(d.scores).map(([k, v]) => [k, v.use]));
}
/** The rounded use score as words: index 0-4. */
export const USE_LEVELS = ["Skoro nevyužívá", "Využívá zřídka", "Využívá občas", "Využívá často", "Využívá neustále"];
export const useLevel = (x: number) => Math.max(0, Math.min(4, Math.round(x)));
export const activityBySlug = new Map(activities.map((a) => [a.slug, a]));

export function activitiesFor(outcomeCode: string): Activity[] {
  return activities.filter((a) => a.outcome === outcomeCode);
}

/** `desc`: one line for previews; `about`: the full commentary on the tool page (user 2026-10-20). */
export const TOOLS: { id: ToolId; name: string; icon: string; short: string; desc: string; about: string }[] = [
  {
    id: "chatbot",
    name: "AI chatbot",
    icon: "chat-dots",
    short: "Pomůže ti s tím chatbot?",
    desc: "Napíšeš mu zadání a odpoví celými větami. Třeba ChatGPT, Gemini nebo Claude.",
    about: "Chatbot spočítá příklad nebo napíše sloh, takže to může vypadat, že už se nic učit nemusíš. To, co máš v hlavě, ale použiješ hned a bez telefonu, a jen díky tomu poznáš, když se chatbot splete, což se mu stává. Při učení je z něj dobrý pomocník: vymyslí ti příklady na procvičení a jinými slovy vysvětlí krok, kterému nerozumíš. U věcí, které děláš tělem, rukama nebo s lidmi, ti poradí nanejvýš postup a pravidla, protože cvičit, vyrábět a domlouvat se musíš ty.",
  },
  {
    id: "internet",
    name: "Internet a další zdroje",
    icon: "globe",
    short: "Pomůže ti, co najdeš na internetu?",
    desc: "Hotové informace, které si dohledáš: vyhledávač, Wikipedie, Internetová jazyková příručka, encyklopedie.",
    about: "Na internetu najdeš skoro všechno, jenže hledání chvíli trvá a bez základních znalostí těžko poznáš, který zdroj je spolehlivý a který si vymýšlí. Co už víš, to nemusíš hledat, a nesmysl odhalíš rychleji. Při učení je internet hlavně zásobárna materiálu, třeba videa s pokusy, mapy, ukázky z knih nebo pravidla pravopisu. Přečíst si o něčem ale ještě neznamená umět to udělat.",
  },
  {
    id: "aplikace",
    name: "Aplikace",
    icon: "smartphone",
    short: "Pomůže ti aplikace?",
    desc: "Programy na jednu věc: překladač, kontrola pravopisu, mapy a navigace, Photomath, určování rostlin.",
    about: "Aplikace umí jednu věc a obvykle ji umí dobře: překladač přeloží větu, kontrola pravopisu podtrhne chybu, navigace najde cestu a Photomath vyřeší příklad z fotky. Je lákavé nechat je pracovat místo sebe. Když ale nevíš, proč navigace vede oklikou nebo proč překladač vybral zrovna tohle slovo, jejich chybu neopravíš a bez telefonu si neporadíš. Při učení se hodí jako trenér a kontrola: Photomath ukáže postup krok za krokem, aplikace na určování rostlin ti dá tip, který ověříš v atlase, a sportovní aplikace zaznamená, kolik toho naběháš.",
  },
  {
    id: "klasicky",
    name: "Klasický nástroj",
    icon: "calculator",
    short: "Pomůže ti obyčejný nástroj?",
    desc: "Kalkulačka, pravítko, kružítko, teploměr, papírová mapa nebo slovník.",
    about: "Tyhle nástroje fungují bez internetu a dělají přesně to, co jim řekneš. Musíš ovšem vědět, co s nimi chceš udělat a jak výsledek přečíst. Kalkulačka spočítá 48 krát 25 rychleji než ty, ale jestli má vyjít kolem tisíce, nebo kolem sta, poznáš jen s odhadem v hlavě. V tělocviku, hudebce nebo výtvarce jsou nástroje pomůcky jako míč, stopky nebo štětec, se kterými trénuješ, i když za tebe nic neudělají.",
  },
];
export const toolById = new Map(TOOLS.map((t) => [t.id, t]));

export const VERDICT: Record<Verdict, string> = {
  pomuze: "Pomůže ti",
  nepomuze: "Nepomůže",
};


export const STAGES: { code: Outcome["stage"]; label: string; years: string }[] = [
  { code: "ZV3", label: "do konce 3. třídy", years: "1.–3. třída" },
  { code: "ZV5", label: "do konce 5. třídy", years: "4.–5. třída" },
  { code: "ZV9", label: "do konce 9. třídy", years: "6.–9. třída" },
];

export interface SubjectGroup {
  code: string;
  name: string;
  areaName: string;
  okruhy: { code: string; name: string; outcomes: Outcome[] }[];
  outcomes: Outcome[];
}

/** Subjects in RVP order, built from outcomes.json (kind "obor" only). */
export function subjects(): SubjectGroup[] {
  const map = new Map<string, SubjectGroup>();
  for (const o of Object.values(outcomes)) {
    if (o.kind !== "obor") continue;
    const key = o.subject.code;
    if (!map.has(key)) map.set(key, { code: key, name: o.subject.name, areaName: o.area.name, okruhy: [], outcomes: [] });
    const g = map.get(key)!;
    g.outcomes.push(o);
    const ok = o.okruh ?? { code: "0", name: o.subject.name };
    let og = g.okruhy.find((x) => x.code === ok.code);
    if (!og) g.okruhy.push((og = { code: ok.code, name: ok.name, outcomes: [] }));
    og.outcomes.push(o);
  }
  return [...map.values()];
}

export function subjectSlug(code: string): string {
  return code.toLowerCase();
}
export function outcomeSlug(code: string): string {
  return code.toLowerCase();
}

export function pct(x: number | undefined | null, digits = 0): string {
  if (x === undefined || x === null || Number.isNaN(x)) return "–";
  return (x * 100).toLocaleString("cs-CZ", { maximumFractionDigits: digits, minimumFractionDigits: digits }) + " %";
}

/** ILO generative-AI exposure as a level: 3 hodně, 2 středně, 1 málo, 0 skoro nemění, -1 no estimate. */
export function iloLevel(o: Occupation | undefined): number {
  if (!o || !o.ilo) return -1;
  const g = o.ilo.gradient.toLowerCase();
  return g.includes("4") || g.includes("3") ? 3 : g.includes("1") || g.includes("2") ? 2 : g.includes("minimal") ? 1 : 0;
}
export function iloWords(o: Occupation | undefined): string | null {
  if (!o || !o.ilo) return null;
  const g = o.ilo.gradient.toLowerCase();
  if (g.includes("4") || g.includes("3")) return "AI ji mění hodně";
  if (g.includes("1") || g.includes("2")) return "AI ji mění středně";
  if (g.includes("minimal")) return "AI ji mění málo";
  return "AI ji skoro nemění";
}

/** Badges from ESCO collections. Green and digital need at least a fifth of the occupation's skills in the collection. */
export const BADGE_SHARE = 0.2;
export function escoBadges(o: Occupation): ("research" | "green" | "digital")[] {
  const c = o.collections;
  const enough = (h: CollectionHits) => h.count > 0 && h.count >= BADGE_SHARE * h.of;
  return [
    ...(c.research ? ["research" as const] : []),
    ...(enough(c.green) ? ["green" as const] : []),
    ...(enough(c.digital) ? ["digital" as const] : []),
  ];
}

// Hand-drawn icons: names from src/icons/sketch.json or Matita.
const SUBJECT_ICON: Record<string, string> = {
  CJL: "book", AJA: "chats", DCJ: "message-square", MAT: "math",
  INF: "laptop", CJS: "sun", DEJ: "hourglass", VKO: "users",
  GEO: "compass", FYZ: "zap", CHE: "flask", PRI: "leaf",
  VFV: "palette", HTD: "music", VZB: "heart", TEV: "ball",
  OSV: "smile", TCH: "scissors",
};
export function subjectIcon(code: string): string {
  return SUBJECT_ICON[code] ?? "book";
}

/** Teacher's marks: plus, minus. */
export const VERDICT_ICON: Record<Verdict, string> = {
  pomuze: "plus",
  nepomuze: "minus",
};

/** CZ-ISCO major groups, shortened for chart labels. */
export const ISCO1: Record<string, string> = {
  "1": "Řídící pracovníci", "2": "Specialisté", "3": "Technici a odborní pracovníci", "4": "Úředníci",
  "5": "Služby a prodej", "6": "Zemědělství, lesnictví a rybářství", "7": "Řemeslníci a opraváři",
  "8": "Obsluha strojů a montéři", "9": "Pomocní pracovníci", "0": "Armáda",
};
/** A pencil icon for each CZ-ISCO 2-digit group (treemap boxes and the group page, user 2026-10-29). */
export const ISCO2_ICON: Record<string, string> = {
  "01": "star", "02": "shield-check", "03": "flag",
  "11": "globe", "12": "briefcase", "13": "chart-line", "14": "key",
  "21": "flask", "22": "heart", "23": "book", "24": "chart-bar", "25": "code", "26": "quote",
  "31": "drafting-compass", "32": "activity", "33": "calculator", "34": "palette", "35": "monitor",
  "41": "file-text", "42": "phone", "43": "hash", "44": "mail",
  "51": "smile", "52": "shopping-cart", "53": "helping-hand", "54": "eye",
  "61": "leaf", "62": "compass", "63": "home",
  "71": "ruler", "72": "settings", "73": "brush", "74": "zap", "75": "scissors",
  "81": "sliders", "82": "package", "83": "truck",
  "91": "droplet", "92": "sun", "93": "move", "94": "flame", "95": "wallet", "96": "trash",
};
/** CZ-ISCO 2-digit groups, our short names for small treemap boxes (the major group's name stands above them). */
export const ISCO2_SHORT: Record<string, string> = {
  "01": "Důstojníci", "02": "Poddůstojníci", "03": "Další hodnosti",
  "11": "Nejvyšší vedení", "12": "Vedení firem a úřadů", "13": "Vedení výroby, IT a škol", "14": "Vedení hotelů a obchodů",
  "21": "Věda a technika", "22": "Zdravotnictví", "23": "Učitelé", "24": "Obchod a správa", "25": "IT", "26": "Právo a kultura",
  "31": "Věda a technika", "32": "Zdravotnictví", "33": "Obchod a správa", "34": "Právo, kultura, sport", "35": "IT",
  "41": "Administrativa", "42": "Přepážky a informace", "43": "Čísla a logistika", "44": "Ostatní",
  "51": "Osobní služby", "52": "Prodej", "53": "Osobní péče", "54": "Ochrana a ostraha",
  "61": "Zemědělství", "62": "Lesnictví a rybářství", "63": "Samozásobitelé",
  "71": "Stavby", "72": "Kovy a stroje", "73": "Umělecká řemesla", "74": "Elektro", "75": "Potraviny, dřevo, textil",
  "81": "Stacionární stroje", "82": "Montáž", "83": "Řidiči",
  "91": "Úklid", "92": "Zemědělství", "93": "Stavby, výroba, doprava", "94": "Kuchyně", "95": "Pouliční prodej", "96": "Odpady",
};

/** ILO exposure buckets: chart label and fill. */
export const EXPOSURE: { id: Exposure; label: string; fill: string }[] = [
  { id: "high", label: "mění hodně", fill: "f-red-solid" },
  { id: "medium", label: "středně", fill: "f-red" },
  { id: "low", label: "málo", fill: "f-light" },
  { id: "none", label: "skoro nemění", fill: "f-empty" },
];

/** "asi 85 tisíc lidí" style rounding for people counts. */
/** The exact citation the Cedefop terms require wherever its figures appear (docs/data-terms.md). */
export const CEDEFOP_CITE = "European Centre for the Development of Vocational Training (Cedefop). Cedefop Skills Forecast 2026, Thessaloniki: Greece, Downloaded from: https://www.cedefop.europa.eu/en/projects/skills-forecast";
/** Headcounts from the Cedefop forecast, rounded coarsely: the terms allow only indicative figures (user 2026-10-20).
 *  "asi 190 tisíc", "asi 45 tisíc", "méně než 10 tisíc" (below 10,000 people a cell is unreliable). */
export function peopleAbout(n: number): string {
  if (n >= 1_000_000) return `asi ${(Math.round(n / 100_000) / 10).toLocaleString("cs-CZ")} milionu`;
  if (n >= 100_000) return `asi ${(Math.round(n / 10_000) * 10).toLocaleString("cs-CZ")} tisíc`;
  if (n >= 10_000) return `asi ${(Math.round(n / 5_000) * 5).toLocaleString("cs-CZ")} tisíc`;
  return "méně než 10 tisíc";
}
export function people(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toLocaleString("cs-CZ", { maximumFractionDigits: 1 })} milionu`;
  if (n >= 10_000) return `${Math.round(n / 1000).toLocaleString("cs-CZ")} tisíc`;
  if (n >= 1000) return `${(Math.round(n / 100) / 10).toLocaleString("cs-CZ")} tisíce`;
  return n.toLocaleString("cs-CZ");
}

/** What the AI level on occupation rows and cards means (tooltip and source lines). */
export const AI_LEVEL_TITLE = "Jak moc práci mění generativní AI, odhad Mezinárodní organizace práce (ILO)";
/** The legend under lists and cards with the AI circle. */
export const AI_LEVEL_LEGEND = "";

/** Signed percent change, e.g. "+2,1 %". */
export function signedPct(x: number | null | undefined): string {
  if (x === null || x === undefined) return "–";
  return `${x > 0 ? "+" : x < 0 ? "−" : ""}${Math.abs(x).toLocaleString("cs-CZ", { maximumFractionDigits: 1 })} %`;
}

/** Simplification rules (public names; full text on /o-projektu/#pravidla). */
export const RULES: Record<RuleId, { name: string; text: string }> = {
  P1: { name: "Zkrácení", text: "Z věty v RVP uděláme krátký název toho, co děláš. Nic nepřidáme." },
  P2: { name: "Běžná slova", text: "Odborné výrazy nahradíme slovy, kterým rozumíš, nebo je vysvětlíme v názvu. Pojmy, které se učíš, necháme." },
  P3: { name: "Rozdělení", text: "Když bod obsahuje víc činností a nástroje by je hodnotily různě, rozdělíme ho na víc karet." },
  P4: { name: "Sloučení", text: "Body téhož cíle, které popisují stejnou věc nebo její jednodušší krok, spojíme do jedné karty." },
  P5: { name: "Příklady z RVP", text: "Konkrétní příklad v názvu musí být v bodu RVP nebo v názvu ukázky úlohy z RVP." },
};
export const ASIDE: Record<AsideId, string> = {
  O1: "Stejný bod je rozebraný u jiného cíle.",
  O2: "Popisuje postoj nebo způsob učení, ne věc, kterou se dá udělat.",
  O3: "Shrnuje celý cíl. Konkrétní věci jsou v ostatních bodech.",
};

/** Chart fills for the three verdicts. */
export const VERDICT_FILL: Record<Verdict, string> = { pomuze: "f-blue", nepomuze: "f-empty" };
export const VERDICTS: Verdict[] = ["pomuze", "nepomuze"];
export function verdictSegs(id: ToolId, list: Activity[] = activities) {
  return VERDICTS.map((v) => ({ value: list.filter((a) => a.tools[id].verdict === v).length, label: VERDICT[v], fill: VERDICT_FILL[v] }));
}
