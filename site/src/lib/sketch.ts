// Hand-drawn shapes generated at build time. Every shape is seeded by a string, so it looks the
// same on every build and differs between boxes.

export function rng(seed: string): () => number {
  let h = 2166136261;
  for (const c of seed) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  return () => {
    h = (h + 0x6d2b79f5) | 0;
    let t = h;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const f = (n: number) => +n.toFixed(2);

/**
 * Outline of a piece of paper as a CSS polygon. One or two edges are torn (dense, jagged points),
 * the others are cut (a few points, barely wavy). Depths are in px, so tall boxes tear like short ones.
 */
export function tear(seed: string, depth = 5): string {
  const r = rng(seed);
  const tornCount = 1 + Math.floor(r() * 2);
  const sides = [0, 1, 2, 3].sort(() => r() - 0.5).slice(0, tornCount);
  const pts: string[] = [];
  const edge = (side: number) => {
    const torn = sides.includes(side);
    const step = () => (torn ? 1.8 + r() * 3.2 : 14 + r() * 16);
    const d = () => (torn ? 0.6 + r() * depth : r() * 1.4);
    // Every side starts exactly at its corner: starting part-way along (as before) cut the corners off
    // diagonally, by up to 15 % of the side, and on long pieces that cut into the text.
    for (let p = 0; p < 100; p += step()) {
      const v = f(p), dd = f(d());
      if (side === 0) pts.push(`${v}% ${dd}px`);
      if (side === 1) pts.push(`calc(100% - ${dd}px) ${v}%`);
      if (side === 2) pts.push(`${f(100 - p)}% calc(100% - ${dd}px)`);
      if (side === 3) pts.push(`${dd}px ${f(100 - p)}%`);
    }
  };
  [0, 1, 2, 3].forEach(edge);
  return `polygon(${pts.join(",")})`;
}

/** A slightly bent line with jittered ends, as an SVG path fragment. */
export function line(x1: number, y1: number, x2: number, y2: number, r: () => number, wob = 1.2): string {
  const j = () => (r() - 0.5) * wob;
  const mx = (x1 + x2) / 2 + j() * 1.5, my = (y1 + y2) / 2 + j() * 1.5;
  return `M${f(x1 + j())},${f(y1 + j())} Q${f(mx)},${f(my)} ${f(x2 + j())},${f(y2 + j())}`;
}

/** Rectangle drawn as four overshooting strokes. */
export function rect(x: number, y: number, w: number, h: number, r: () => number, wob = 1.2): string {
  const o = () => r() * 2;
  return [
    line(x - o(), y, x + w + o(), y, r, wob),
    line(x + w, y - o(), x + w, y + h + o(), r, wob),
    line(x + w + o(), y + h, x - o(), y + h, r, wob),
    line(x, y + h + o(), x, y - o(), r, wob),
  ].join(" ");
}

/** Closed rectangle path (for fills), corners jittered a little. */
export function rectFill(x: number, y: number, w: number, h: number, r: () => number, wob = 1): string {
  const j = () => (r() - 0.5) * wob;
  return `M${f(x + j())},${f(y + j())} L${f(x + w + j())},${f(y + j())} L${f(x + w + j())},${f(y + h + j())} L${f(x + j())},${f(y + h + j())} Z`;
}

/** Circle drawn in one go, ending a little past where it started. */
export function circle(cx: number, cy: number, rad: number, r: () => number, wob = 0.04): string {
  const n = 10, start = r() * Math.PI * 2, over = 0.35 + r() * 0.3;
  const pts: [number, number][] = [];
  for (let i = 0; i <= n + 1; i++) {
    const a = start + (i / n) * (Math.PI * 2 + over);
    const rr = rad * (1 + (r() - 0.5) * wob * 2);
    pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
  }
  // Catmull-Rom through the points.
  let d = `M${f(pts[0][0])},${f(pts[0][1])}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    d += ` C${f(p1[0] + (p2[0] - p0[0]) / 6)},${f(p1[1] + (p2[1] - p0[1]) / 6)} ${f(p2[0] - (p3[0] - p1[0]) / 6)},${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])},${f(p2[1])}`;
  }
  return d;
}

/** Pie wedge from 12 o'clock, clockwise, for a fraction 0..1. */
export function wedge(cx: number, cy: number, rad: number, frac: number): string {
  const a = Math.max(frac, 0.006) * Math.PI * 2;
  if (frac >= 0.999) return `M${cx},${cy - rad} A${rad},${rad} 0 1 1 ${cx - 0.01},${cy - rad} Z`;
  const x = cx + Math.sin(a) * rad, y = cy - Math.cos(a) * rad;
  return `M${cx},${cy} L${cx},${cy - rad} A${rad},${rad} 0 ${a > Math.PI ? 1 : 0} 1 ${f(x)},${f(y)} Z`;
}

