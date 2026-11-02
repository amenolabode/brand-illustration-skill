// Layered-savings illustration system.
// Every asset is generated from the same tokens, pattern tiles and construction
// functions, so the system is reproducible and scales as vector.
// Run: node build.mjs
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const OUT = dirname(fileURLToPath(import.meta.url));
const write = (name, svg) => writeFileSync(join(OUT, name), svg.trim() + '\n');

// ---------------------------------------------------------------- tokens
// One anchor hue (iron oxide, the pigment that bands real sedimentary rock),
// one ink for depth, and pale faces. Same role structure as the reference:
// signal / depth / quiet faces.
const C = {
  paper: '#FBF6EC',
  ferric: '#E2531F', // anchor: signal, editorial field, newest deposit
  ferricDeep: '#A9391A',
  basalt: '#2B2236', // depth and structure
  basaltSoft: '#4A3D5A',
  bone: '#FFFBF2',
  sand: '#F7E6C4',
  clay: '#F7D6C7',
  lichen: '#E0ECD6',
  slate: '#DDE4EF',
};
// Pattern line = one step darker than its face. Low contrast, like engraving.
const LINE = { sand: '#E2BF83', clay: '#E9A88C', lichen: '#AFCB99', slate: '#A6B8D4', bone: '#E6D7BA' };
const FACES = ['sand', 'clay', 'lichen', 'slate', 'bone'];

// ---------------------------------------------------------------- pattern
// "Bedding": four undulating bedding planes per 96x36 tile, each with its own
// amplitude and phase, plus one band of sand grains. Periodic in x and y so it
// tiles seamlessly. This is the source-world equivalent of a fine security-print mesh.
const TILE_W = 96, TILE_H = 36;
const BEDS = [
  { y: 5, a: 1.6, ph: 0 },
  { y: 12, a: 2.4, ph: 1.3 },
  { y: 21, a: 1.2, ph: 2.6 },
  { y: 30, a: 2.0, ph: 4.0 },
];
function rng(seed) {
  return () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
}
const bedPaths = BEDS.map(({ y, a, ph }) => {
  let d = '';
  for (let x = 0; x <= TILE_W; x += 3) {
    const yy = y + a * Math.sin((2 * Math.PI * x) / TILE_W + ph);
    d += `${x ? 'L' : 'M'}${x} ${yy.toFixed(2)}`;
  }
  return d;
});
const r = rng(7);
const GRAINS = Array.from({ length: 11 }, () => [2 + r() * 92, 24 + r() * 3.4, 0.6 + r() * 0.5]);

function beddingPattern(id, face, { scale = 1, sw = 1.1, grains = true } = {}) {
  const line = LINE[face];
  return `<pattern id="${id}" patternUnits="userSpaceOnUse" width="${TILE_W}" height="${TILE_H}" patternTransform="scale(${scale})">
    <rect width="${TILE_W}" height="${TILE_H}" fill="${C[face]}"/>
    <g fill="none" stroke="${line}" stroke-width="${sw}" stroke-linecap="round">${bedPaths.map((d) => `<path d="${d}"/>`).join('')}</g>
    ${grains ? `<g fill="${line}">${GRAINS.map(([x, y, rr]) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rr.toFixed(2)}"/>`).join('')}</g>` : ''}
  </pattern>`;
}
// "Lamina": straight parallel hatching, the quiet variant (shale, edges, core).
function laminaPattern(id, face, line, gap = 5) {
  return `<pattern id="${id}" patternUnits="userSpaceOnUse" width="20" height="${gap}">
    <rect width="20" height="${gap}" fill="${face}"/><path d="M0 ${gap / 2}H20" stroke="${line}" stroke-width="1"/>
  </pattern>`;
}
const allBedding = (prefix, opts) => FACES.map((f) => beddingPattern(`${prefix}-${f}`, f, opts)).join('');

const svgOpen = (w, h, extra = '') =>
  `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" ${extra}>`;

// ---------------------------------------------------------------- 1. pattern spec
function patternSpec() {
  const s = 4; // enlarged tile
  return `${svgOpen(TILE_W * s * 2 + 40, TILE_H * s + 40)}
  <defs>${beddingPattern('p-big', 'sand', { scale: s, sw: 1.1 })}</defs>
  <rect width="100%" height="100%" fill="${C.paper}"/>
  <rect x="20" y="20" width="${TILE_W * s * 2}" height="${TILE_H * s}" fill="url(#p-big)" rx="6"/>
  <rect x="20" y="20" width="${TILE_W * s}" height="${TILE_H * s}" fill="none" stroke="${C.ferric}" stroke-width="1.5" stroke-dasharray="6 5" rx="6"/>
</svg>`;
}

// ---------------------------------------------------------------- 2. editorial objects
// Oblique extrusion toward lower-right. The sidewall is built from stacked
// offset copies in alternating basalt tones, so every object's edge reads as a
// cross-section of deposited layers. Faces carry bedding with exactly one
// fault: the right block is displaced 7 units down, never erased.
const SHAPES = {
  bulb: `<circle cx="100" cy="84" r="46"/><rect x="78" y="108" width="44" height="32" rx="6"/><rect x="84" y="138" width="32" height="20" rx="8"/>`,
  question: `<path d="M72 80C72 58 86 46 102 46C120 46 132 58 132 74C132 92 116 98 108 106C102 112 100 118 100 126" fill="none" stroke="currentColor" stroke-width="26" stroke-linecap="round"/><circle cx="100" cy="160" r="15"/>`,
  heart: `<path d="M100 162C42 124 36 70 70 56C86 50 98 60 100 72C102 60 114 50 130 56C164 70 158 124 100 162Z"/>`,
  shield: `<path d="M100 38L152 56V100C152 132 130 152 100 166C70 152 48 132 48 100V56Z"/>`,
  chart: `<rect x="46" y="118" width="28" height="44" rx="4"/><rect x="86" y="90" width="28" height="72" rx="4"/><rect x="126" y="56" width="28" height="106" rx="4"/>`,
  transfer: `<path d="M40 66H124V48L160 77L124 106V88H40Z"/><path d="M160 114H76V96L40 125L76 154V136H160Z"/>`,
  document: `<rect x="58" y="38" width="84" height="124" rx="10"/>`,
  naira: `<rect x="60" y="44" width="20" height="116" rx="3"/><rect x="120" y="44" width="20" height="116" rx="3"/><path d="M60 44H80L140 160H120Z"/><rect x="44" y="84" width="112" height="11" rx="3"/><rect x="44" y="108" width="112" height="11" rx="3"/>`,
};
const OBJECT_FACE = { bulb: 'sand', question: 'slate', heart: 'clay', shield: 'lichen', chart: 'sand', transfer: 'slate', document: 'bone', naira: 'clay' };
const OBJECT_DETAIL = {
  bulb: `<g stroke="${C.basalt}" stroke-width="3" stroke-linecap="round"><path d="M84 118H116M84 128H116"/></g>`,
  chart: `<rect x="46" y="118" width="28" height="9" rx="4" fill="${C.ferric}"/><rect x="86" y="90" width="28" height="9" rx="4" fill="${C.ferric}"/><rect x="126" y="56" width="28" height="9" rx="4" fill="${C.ferric}"/>`,
  document: `<g fill="${C.basaltSoft}"><rect x="74" y="58" width="36" height="6" rx="3" fill="${C.ferric}"/><rect x="74" y="78" width="52" height="4" rx="2"/><rect x="74" y="90" width="52" height="4" rx="2"/><rect x="74" y="102" width="40" height="4" rx="2"/></g>`,
};
const FAULT = { a: [112, 0], b: [88, 200], throw: 7 };

function editorialDefs(prefix) {
  const symbols = Object.entries(SHAPES)
    .map(([k, s]) => `<symbol id="${prefix}-s-${k}" overflow="visible"><g fill="currentColor">${s}</g></symbol>
      <mask id="${prefix}-m-${k}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="260" height="260"><use href="#${prefix}-s-${k}" color="#fff"/></mask>`)
    .join('');
  const [ax, ay] = FAULT.a, [bx, by] = FAULT.b;
  return `${allBedding(`${prefix}-bed`, { scale: 1.15, sw: 1.15 })}${symbols}
    <clipPath id="${prefix}-fL"><polygon points="-40,-40 ${ax},${ay - 40} ${bx},${by + 40} -40,240"/></clipPath>
    <clipPath id="${prefix}-fR"><polygon points="${ax},${ay - 40} 240,-40 240,240 ${bx},${by + 40}"/></clipPath>`;
}

function editorialObject(prefix, key, { depth = 18, step = 0.78 } = {}) {
  const face = OBJECT_FACE[key];
  let wall = '';
  for (let i = depth; i >= 1; i--) {
    const band = Math.floor((i - 1) / 4.5) % 2 ? C.basalt : C.basaltSoft;
    wall += `<use href="#${prefix}-s-${key}" color="${band}" transform="translate(${(i * step).toFixed(2)} ${(i * step).toFixed(2)})"/>`;
  }
  const fill = `url(#${prefix}-bed-${face})`;
  const [ax, ay] = FAULT.a, [bx, by] = FAULT.b;
  return `${wall}
    <g mask="url(#${prefix}-m-${key})">
      <g clip-path="url(#${prefix}-fL)"><rect x="-20" y="-20" width="240" height="240" fill="${fill}"/></g>
      <g clip-path="url(#${prefix}-fR)"><rect x="-20" y="-20" width="240" height="240" fill="${fill}" transform="translate(0 ${FAULT.throw})"/></g>
      <path d="M${ax} ${ay}L${bx} ${by}" stroke="${LINE[face]}" stroke-width="1.6"/>
    </g>
    ${OBJECT_DETAIL[key] || ''}`;
}

function storyCovers() {
  const P = 'ed', W = 1200, H = 640, cell = 280, ox = 40, oy = 40;
  const keys = ['bulb', 'question', 'heart', 'shield', 'chart', 'transfer', 'document', 'naira'];
  const objs = keys
    .map((k, i) => {
      const cx = ox + (i % 4) * cell + cell / 2, cy = oy + Math.floor(i / 4) * cell + cell / 2;
      return `<g transform="translate(${cx - 128} ${cy - 128}) scale(1.28)">${editorialObject(P, k)}</g>`;
    })
    .join('');
  return `${svgOpen(W, H)}<defs>${editorialDefs(P)}</defs>
  <rect width="${W}" height="${H}" fill="${C.ferric}"/>${objs}</svg>`;
}

// ---------------------------------------------------------------- 3. product icons
// Flat, silhouette-first. Ferric carries the subject, basalt the detail, and
// the pale back plate is the only place bedding appears. Three scale states:
// L0 display (bedding on plate), L1 standard (plain plate), L2 micro (subject only).
function plate(P, level, face, shape) {
  if (level === 2) return '';
  const fill = level === 0 ? `url(#${P}-bed-${face})` : C[face];
  return shape.replace('FILL', fill);
}
const hex = (cx, cy, rr) =>
  Array.from({ length: 6 }, (_, k) => {
    const a = ((-90 + 60 * k) * Math.PI) / 180;
    return `${(cx + rr * Math.cos(a)).toFixed(1)},${(cy + rr * Math.sin(a)).toFixed(1)}`;
  }).join(' ');

const ICONS = {
  vault: (P, L) => `${plate(P, L, 'slate', `<rect x="8" y="20" width="70" height="68" rx="7" fill="FILL"/>`)}
    <rect x="18" y="10" width="70" height="68" rx="7" fill="${C.ferric}"/>
    ${L < 2 ? `<rect x="13" y="24" width="9" height="12" rx="2.5" fill="${C.basalt}"/><rect x="13" y="52" width="9" height="12" rx="2.5" fill="${C.basalt}"/>` : ''}
    <circle cx="54" cy="44" r="17" fill="${C.bone}" stroke="${C.basalt}" stroke-width="${L === 2 ? 6 : 4}"/>
    ${L < 2 ? `<g stroke="${C.basalt}" stroke-width="3" stroke-linecap="round"><path d="M54 30V58M40 44H68"/></g><circle cx="54" cy="44" r="5.5" fill="${C.ferric}"/>` : ''}`,
  crystal: (P, L) => `${plate(P, L, 'sand', `<polygon points="${hex(42, 54, 38)}" fill="FILL"/>`)}
    <polygon points="${hex(52, 44, 38)}" fill="${C.ferric}"/>
    ${L < 2 ? `<polygon points="${hex(52, 44, 23)}" fill="${C.bone}"/>` : ''}
    <path d="M41 45L49 53L63 37" fill="none" stroke="${L < 2 ? C.basalt : C.bone}" stroke-width="${L === 2 ? 8 : 5.5}" stroke-linecap="round" stroke-linejoin="round"/>`,
  target: (P, L) => `${plate(P, L, 'clay', `<circle cx="54" cy="54" r="36" fill="FILL"/>`)}
    <g class="rings">
      <circle class="ring r1" cx="44" cy="46" r="35" fill="${C.ferric}"/>
      <circle class="ring r2" cx="44" cy="46" r="24" fill="${C.bone}"/>
      <circle class="ring r3" cx="44" cy="46" r="15" fill="${C.ferric}"/>
      ${L < 2 ? `<circle class="ring r4" cx="44" cy="46" r="6" fill="${C.basalt}"/>` : ''}
    </g>
    ${L < 2 ? `<g class="arrow"><path d="M44 46L80 10" stroke="${C.basalt}" stroke-width="4" stroke-linecap="round"/><path d="M72 8L86 4L82 18Z" fill="${C.basalt}"/></g>` : ''}`,
  community: (P, L) => `${plate(P, L, 'lichen', `<rect x="6" y="28" width="62" height="58" rx="8" fill="FILL"/>`)}
    ${L < 2 ? `<g fill="${C.basalt}"><circle cx="24" cy="44" r="8.5"/><path d="M8 84C8 70 15 63 24 63C33 63 40 70 40 84Z"/><circle cx="72" cy="44" r="8.5"/><path d="M56 84C56 70 63 63 72 63C81 63 88 70 88 84Z"/></g>` : `<g fill="${C.basalt}"><circle cx="20" cy="46" r="10"/><circle cx="76" cy="46" r="10"/></g>`}
    <circle cx="48" cy="36" r="13" fill="${C.ferric}" stroke="${C.paper}" stroke-width="3"/>
    <path d="M24 88C24 70 35 60 48 60C61 60 72 70 72 88Z" fill="${C.ferric}" stroke="${C.paper}" stroke-width="3"/>`,
  statements: (P, L) => `${L < 2 ? `<g transform="rotate(-14 48 50)">${plate(P, L, 'sand', `<rect x="22" y="14" width="50" height="66" rx="7" fill="FILL"/>`)}</g>
    <g transform="rotate(10 48 50)">${plate(P, L, 'clay', `<rect x="24" y="14" width="50" height="66" rx="7" fill="FILL"/>`)}</g>` : ''}
    <rect x="24" y="18" width="48" height="64" rx="7" fill="${C.ferric}"/>
    <circle cx="48" cy="40" r="${L === 2 ? 10 : 8}" fill="none" stroke="${C.bone}" stroke-width="${L === 2 ? 5 : 3.5}"/>
    ${L < 2 ? `<g fill="${C.bone}"><rect x="34" y="58" width="28" height="4" rx="2"/><rect x="34" y="67" width="20" height="4" rx="2"/></g>` : ''}`,
  recurring: (P, L) => `${plate(P, L, 'lichen', `<rect x="6" y="22" width="66" height="64" rx="7" fill="FILL"/>`)}
    <rect x="14" y="16" width="66" height="64" rx="7" fill="${C.sand}"/>
    <path d="M14 23A7 7 0 0 1 21 16H73A7 7 0 0 1 80 23V34H14Z" fill="${C.ferric}"/>
    <g fill="${C.basalt}"><rect x="28" y="8" width="6" height="16" rx="3"/><rect x="60" y="8" width="6" height="16" rx="3"/></g>
    ${L < 2 ? `<g class="days" fill="${C.basalt}" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-weight="800" font-size="27" text-anchor="middle"><text class="d d1" x="42" y="67">8</text><text class="d d2" x="42" y="67">9</text><text class="d d3" x="42" y="67">10</text></g>` : ''}
    <circle cx="74" cy="74" r="${L === 2 ? 18 : 16}" fill="${C.ferric}" stroke="${C.paper}" stroke-width="3"/>
    <g class="spin"><path d="M65 76A9 9 0 1 0 68 67" fill="none" stroke="${C.bone}" stroke-width="${L === 2 ? 4.5 : 3.5}" stroke-linecap="round"/><path d="M63 62L71 64L66 71Z" fill="${C.bone}"/></g>`,
};
const ICON_ORDER = [
  ['vault', 'Reserve'],
  ['crystal', 'Verified'],
  ['target', 'Goal'],
  ['community', 'Circles'],
  ['statements', 'Statements'],
  ['recurring', 'Auto-save'],
];
const ICON_CSS = `<style>
  .ring{transform-box:fill-box;transform-origin:center;animation:deposit 4.8s cubic-bezier(.2,.8,.2,1) infinite}
  .r1{animation-delay:0s}.r2{animation-delay:.18s}.r3{animation-delay:.36s}.r4{animation-delay:.54s}
  @keyframes deposit{0%,62%{transform:scale(1);opacity:1}68%{transform:scale(.2);opacity:0}84%,100%{transform:scale(1);opacity:1}}
  .d{animation:day 4.8s steps(1) infinite}.d2,.d3{opacity:0}.d1{animation-delay:0s}.d2{animation-delay:1.6s}.d3{animation-delay:3.2s}
  @keyframes day{0%{opacity:1}33.33%,100%{opacity:0}}
  .spin{transform-box:view-box;transform-origin:74px 74px;animation:spin 1.6s cubic-bezier(.6,0,.3,1) infinite}
  @keyframes spin{0%,60%{transform:rotate(0)}100%{transform:rotate(360deg)}}
  @media (prefers-reduced-motion:reduce){.ring,.spin{animation:none}.d{animation:none}.d1{opacity:1}}
</style>`;

function productIcons() {
  const P = 'ic', W = 1200, H = 500;
  const sizes = [{ L: 0, px: 120, y: 84 }, { L: 1, px: 48, y: 318 }, { L: 2, px: 24, y: 436 }];
  const colW = W / 6;
  let body = '';
  for (const { L, px, y } of sizes) {
    ICON_ORDER.forEach(([k], i) => {
      const s = px / 96, x = colW * i + colW / 2 - px / 2;
      body += `<g transform="translate(${x} ${y}) scale(${s})">${ICONS[k](P, L)}</g>`;
    });
  }
  const label = (t, y, size = 13, fill = C.basaltSoft, weight = 500) =>
    `<text y="${y}" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-size="${size}" font-weight="${weight}" fill="${fill}" text-anchor="middle">${t}</text>`;
  const names = ICON_ORDER.map(([, n], i) => `<g transform="translate(${colW * i + colW / 2} 0)">${label(n, 242, 15, C.basalt, 600)}</g>`).join('');
  const rowLabels = [['Display · bedding on plate', 52], ['Standard · plain plate', 300], ['Micro · silhouette only', 418]]
    .map(([t, y]) => `<text x="40" y="${y}" font-family="Inter, 'Helvetica Neue', Arial, sans-serif" font-size="11" letter-spacing=".08em" fill="${C.basaltSoft}" opacity=".7">${t.toUpperCase()}</text>`)
    .join('');
  return `${svgOpen(W, H)}<defs>${allBedding(`${P}-bed`, { scale: 0.62, sw: 1.5 })}</defs>${ICON_CSS}
  <rect width="${W}" height="${H}" fill="${C.paper}"/>
  <path d="M40 272H${W - 40}M40 392H${W - 40}" stroke="${LINE.bone}" stroke-width="1"/>
  ${body}${names}${rowLabels}</svg>`;
}

// ---------------------------------------------------------------- 4. technical scene
// True isometric. Flat plane geometry is drawn once and projected with an SVG
// matrix, so the bedding pattern and grid project correctly. Three states,
// like the reference: wireframe on grid -> neutral volume -> material.
// The account surface sits on four strata plates: the balance is built from deposits.
const ISO = (ox, oy, z) => `matrix(0.866 0.5 -0.866 0.5 ${ox} ${oy - z})`;
const MODES = {
  wire: { bg: C.paper, grid: true, top: C.bone, side: C.bone, stroke: C.basalt, card: C.bone, ui: 'none', uiStroke: C.basalt, strata: Array(4).fill(C.bone), strataSide: C.bone, avatar: Array(3).fill('none') },
  volume: { bg: '#ECE8EE', top: '#FFFFFF', side: '#BDB5C6', card: '#FFFFFF', cardSide: '#D3CDDA', ui: '#D9D3E0', strata: ['#DCD7E2', '#D3CDDA', '#CAC3D2', '#C1B9CA'], strataSide: '#A79EB2', avatar: ['#D9D3E0', '#D9D3E0', '#D9D3E0'] },
  material: { bg: C.paper, top: 'url(#ts-bed-slate)', side: C.basaltSoft, card: C.bone, cardSide: LINE.bone, ui: LINE.slate, strata: ['url(#ts-lam-sand)', 'url(#ts-lam-clay)', 'url(#ts-lam-lichen)', 'url(#ts-lam-slate)'], strataSide: C.basalt, avatar: ['url(#ts-bed-clay)', 'url(#ts-bed-lichen)', C.ferric] },
};

function techDefs() {
  return `${allBedding('ts-bed', { scale: 0.7, sw: 1.3 })}
    ${['sand', 'clay', 'lichen', 'slate'].map((f) => laminaPattern(`ts-lam-${f}`, C[f], LINE[f], 4)).join('')}
    <pattern id="ts-grid" patternUnits="userSpaceOnUse" width="20" height="20"><path d="M20 0V20H0" fill="none" stroke="#C9D3E3" stroke-width=".9" vector-effect="non-scaling-stroke"/></pattern>`;
}

function slab(ox, oy, { x, y, w, h, z, t, rx = 10, top, side, stroke, inner = '' }) {
  const st = stroke ? `stroke="${stroke}" stroke-width="1" vector-effect="non-scaling-stroke"` : '';
  let s = '';
  if (stroke) {
    s += `<rect transform="${ISO(ox, oy, z - t)}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${side}" ${st}/>`;
  } else {
    for (let k = t; k >= 1; k -= 1) s += `<rect transform="${ISO(ox, oy, z - k)}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${side}"/>`;
  }
  s += `<g transform="${ISO(ox, oy, z)}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${top}" ${st}/>${inner}</g>`;
  return s;
}

function techScene(mode, { w = 760, h = 560 } = {}) {
  const m = MODES[mode];
  const ox = w / 2, oy = 286;
  const st = mode === 'wire' ? C.basalt : null;
  const uiSt = mode === 'wire' ? `stroke="${C.basalt}" stroke-width="1" vector-effect="non-scaling-stroke"` : '';
  let s = `<rect width="${w}" height="${h}" fill="${m.bg}"/>`;
  if (m.grid) s += `<rect transform="${ISO(ox, oy, 0)}" x="-700" y="-700" width="1400" height="1400" fill="url(#ts-grid)"/>`;
  // strata plates beneath the account, deepest first
  for (let i = 3; i >= 0; i--) {
    s += slab(ox, oy, { x: -84, y: -144, w: 168, h: 288, z: -26 - i * 15, t: 6, rx: 14, top: m.strata[i], side: m.strataSide, stroke: st });
  }
  // account surface
  const notch = `<rect x="-20" y="-132" width="40" height="8" rx="4" fill="${mode === 'material' ? C.basaltSoft : mode === 'volume' ? '#D3CDDA' : 'none'}" ${uiSt}/>`;
  s += slab(ox, oy, { x: -84, y: -144, w: 168, h: 288, z: 0, t: 8, rx: 16, top: m.top, side: m.side, stroke: st, inner: notch });
  // floating cards, back to front
  const cards = [
    { x: -66, y: -112, z: 92 },
    { x: -60, y: -34, z: 62 },
    { x: -54, y: 44, z: 32 },
  ];
  cards.forEach((c, i) => {
    // drop line to the surface
    const X = ox + 0.866 * (c.x + 140 - (c.y + 64)), Y = oy + 0.5 * (c.x + 140 + c.y + 64);
    s += `<path d="M${X.toFixed(1)} ${(Y - c.z).toFixed(1)}V${Y.toFixed(1)}" stroke="${mode === 'material' ? C.ferric : C.basalt}" stroke-width="1" stroke-dasharray="2 4" opacity="${mode === 'material' ? 0.9 : 0.45}"/>`;
    const inner = `<circle cx="${c.x + 24}" cy="${c.y + 32}" r="13" fill="${m.avatar[i]}" ${uiSt}/>
      <rect x="${c.x + 48}" y="${c.y + 20}" width="52" height="8" rx="4" fill="${i === 2 && mode === 'material' ? C.ferric : m.ui}" ${uiSt}/>
      <rect x="${c.x + 48}" y="${c.y + 36}" width="78" height="8" rx="4" fill="${m.ui}" ${uiSt}/>`;
    s += slab(ox, oy, { x: c.x, y: c.y, w: 140, h: 64, z: c.z, t: 5, rx: 10, top: m.card, side: m.cardSide || m.side, stroke: st, inner });
  });
  return s;
}

function technical() {
  const w = 760, h = 560;
  const css = `<style>
    .st{animation:cycle 4.5s steps(1) infinite}.s1,.s2{opacity:0}.s1{animation-delay:1.5s}.s2{animation-delay:3s}.s3{animation-delay:0s}
    @keyframes cycle{0%{opacity:1}33.33%,100%{opacity:0}}
    @media (prefers-reduced-motion:reduce){.st{animation:none}.s3{opacity:1}}
  </style>`;
  const animated = `${svgOpen(w, h)}<defs>${techDefs()}</defs>${css}
    <g class="st s1">${techScene('wire')}</g><g class="st s2">${techScene('volume')}</g><g class="st s3">${techScene('material')}</g></svg>`;
  const states = `${svgOpen(w * 3, h)}<defs>${techDefs()}</defs>
    ${['wire', 'volume', 'material'].map((md, i) => `<g transform="translate(${i * w} 0)">${techScene(md)}</g>`).join('')}</svg>`;
  return { animated, states };
}

// ---------------------------------------------------------------- 5. deposition motion
// Native motion: deposit -> settle -> fault -> hold. Each layer falls and
// settles on the last; the newest layer is always ferric. The fault displaces
// the right block without erasing the record.
function deposition() {
  const W = 600, H = 600, cycle = 8;
  const layers = ['bone', 'slate', 'lichen', 'clay', 'sand', 'ferric'];
  const lw = 260, lh = 34, x0 = (W - lw) / 2 - 10, yBottom = 420, depth = 14, step = 0.8;
  let defs = allBedding('dp-bed', { scale: 0.9, sw: 1.2 });
  let css = '';
  let stack = '';
  layers.forEach((f, i) => {
    const y = yBottom - (i + 1) * lh;
    const appear = ((0.3 + i * 0.55) / cycle) * 100, land = appear + 5, bounce = land + 1.6;
    css += `@keyframes dp${i}{0%,${appear.toFixed(1)}%{transform:translateY(-${y + 60}px);opacity:0}${land.toFixed(1)}%{transform:translateY(3px);opacity:1}${bounce.toFixed(1)}%,93%{transform:translateY(0);opacity:1}99%,100%{transform:translateY(0);opacity:0}}.l${i}{animation:dp${i} ${cycle}s cubic-bezier(.5,0,.2,1) -5.6s infinite}`;
    const face = f === 'ferric' ? C.ferric : `url(#dp-bed-${f})`;
    let wall = '';
    for (let k = depth; k >= 1; k--) wall += `<rect x="${x0 + k * step}" y="${y + k * step}" width="${lw}" height="${lh}" rx="6" fill="${k % 7 < 4 ? C.basaltSoft : C.basalt}"/>`;
    // lower layers paint last: their faces hide the underside of the slab above
    stack = `<g class="l l${i}">${wall}<rect x="${x0}" y="${y}" width="${lw}" height="${lh}" rx="6" fill="${face}"/></g>` + stack;
  });
  const fx1 = W / 2 + 26, fx2 = W / 2 - 14;
  const faultIn = ((0.3 + 6 * 0.55 + 0.5) / cycle) * 100;
  css += `@keyframes fault{0%,${faultIn.toFixed(1)}%{transform:translateY(0)}${(faultIn + 4).toFixed(1)}%,93%{transform:translateY(12px)}100%{transform:translateY(0)}}.fault{animation:fault ${cycle}s cubic-bezier(.7,0,.2,1) -5.6s infinite}
    @media (prefers-reduced-motion:reduce){.l{animation:none!important;opacity:1}.fault{animation:none;transform:translateY(12px)}}`;
  defs += `<clipPath id="dp-L"><polygon points="0,0 ${fx1},0 ${fx2},${H} 0,${H}"/></clipPath><clipPath id="dp-R"><polygon points="${fx1},0 ${W},0 ${W},${H} ${fx2},${H}"/></clipPath>`;
  return `${svgOpen(W, H)}<defs>${defs}</defs><style>${css}</style>
    <rect width="${W}" height="${H}" fill="${C.paper}"/>
    <ellipse cx="${W / 2}" cy="${yBottom + 34}" rx="170" ry="10" fill="${LINE.bone}"/>
    <g clip-path="url(#dp-L)">${stack}</g>
    <g clip-path="url(#dp-R)"><g class="fault">${stack}</g></g></svg>`;
}

// ---------------------------------------------------------------- write
write('00-pattern-bedding.svg', patternSpec());
const t = technical();
write('01-technical-scene.svg', t.animated);
write('01-technical-scene-states.svg', t.states);
write('02-product-icons.svg', productIcons());
write('03-story-covers.svg', storyCovers());
write('04-deposition-motion.svg', deposition());
console.log('built', OUT);
