// Hand-drawn icons at build time: our own sketch set (src/icons/sketch.json) first, then Matita (MIT).
import { getIconData, iconToSVG, replaceIDs } from "@iconify/utils";
import matita from "@iconify-json/matita/icons.json";
import sketch from "../icons/sketch.json";
import { TOOLS, VERDICT_ICON } from "./data";

export function iconSvg(name: string): { viewBox: string; body: string } {
  const data = getIconData(sketch as any, name) ?? getIconData(matita as any, name);
  if (!data) throw new Error(`Icon ${name} not found in sketch or matita`);
  const svg = iconToSVG(data, { height: "auto" });
  return { viewBox: svg.attributes.viewBox, body: replaceIDs(svg.body) };
}

// Icons drawn by reference (<Icon use />): defined once per page as <symbol id="i-NAME"> in Base.astro.
export const SYMBOL_ICONS = [...TOOLS.map((t) => t.icon), ...Object.values(VERDICT_ICON)];

export const iconSymbols = SYMBOL_ICONS.map((n) => {
  const { viewBox, body } = iconSvg(n);
  return `<symbol id="i-${n}" viewBox="${viewBox}">${body}</symbol>`;
}).join("");
