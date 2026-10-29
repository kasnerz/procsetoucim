import { occupations, isco2, occupationCards, cardsWord } from "../lib/data";

// Documents for the occupation search on /povolani/ (client-side MiniSearch, same component as the main search).
export function GET() {
  const docs = Object.values(occupations).map((o) => {
    const n = occupationCards.get(o.id)?.length ?? 0;
    return {
      id: `p:${o.id}`,
      type: "p",
      title: o.label,
      aliases: (o.labelAlt ?? []).slice(0, 8).join(" "),
      context: isco2[o.isco2]?.label ?? "",
      meta: [n > 0 ? `${n} ${cardsWord(n)}` : "", isco2[o.isco2]?.label].filter(Boolean).join(" · "),
      href: `povolani/${o.id}/`,
    };
  });
  return new Response(JSON.stringify(docs), { headers: { "Content-Type": "application/json" } });
}
