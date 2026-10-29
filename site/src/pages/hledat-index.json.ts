import { activities, outcomes } from "../lib/data";

// Documents for client-side MiniSearch. Activities first; outcomes so every RVP goal is findable.
export function GET() {
  const docs = [
    ...activities.map((a) => {
      const o = outcomes[a.outcome];
      return {
        id: `a:${a.slug}`,
        type: "a",
        title: a.title,
        aliases: a.aliases.join(" "),
        context: [o?.subject.name, o?.okruh?.name, ...a.levelSource.map((s) => s.point)].filter(Boolean).join(" "),
        meta: o ? `${o.subject.name} · ${o.stageLabel}` : "",
        href: `aktivita/${a.slug}/`,
      };
    }),
    ...Object.values(outcomes).map((o) => ({
      id: `o:${o.code}`,
      type: "o",
      title: o.text,
      aliases: "",
      context: `${o.subject.name} ${o.okruh?.name ?? ""}`,
      meta: `Cíl z RVP · ${o.subject.name} · ${o.stageLabel}`,
      href: `vystup/${o.code.toLowerCase()}/`,
    })),
  ];
  return new Response(JSON.stringify(docs), { headers: { "Content-Type": "application/json" } });
}
