// STARTER TEMPLATE: flat spot illustrations with a primitive-built character.
// Family: flat geometric spot + light character (see references/style-families.md §1–2).
// Replace the tokens, the ownable rule and the moments with your direction's. Keep the structure: one token set,
// one character builder with fixed proportions, spots per touchpoint moment with an emotional temperature, a
// signature sheet, and one in-context render (phone frame) so spots are judged where they live.
// Audit with --family character (skin tones count as a second hue); spots without figures pass --family flat.
// Run: node flat-spot-template.mjs [out-dir]   (default: current directory; no dependencies)
import { writeFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';

const OUT = resolve(process.argv[2] || process.cwd());
mkdirSync(OUT, { recursive: true });
const write = (name, svg) => writeFileSync(join(OUT, name), svg.trim() + '\n');

// ---------------------------------------------------------------- tokens
// One accent, one ink, neutrals, and a small set of figure colours.
const C = {
  paper: '#FFFFFF',
  mist: '#F1F2F6', // ground and quiet backgrounds
  cloud: '#E3E6EE',
  slate: '#9AA1B2',
  ink: '#1F2430', // hair, details, never outlines
  accent: '#5B5BF7', // the one saturated colour: the "answer" in every scene
  accentSoft: '#DCDCFE',
  warm: '#FFC9A8',
  skin: ['#8D5A3B', '#E0A57E', '#F5D0B5'],
};

// The ownable rule for this example: limbs are single capsules of one fixed width (LIMB) with round ends, heads are
// perfect circles that float a gap above the body (no neck), and hands are oversized dots. Change it for your brand.
const LIMB = 13, HEAD = 17, GAP = 4, HAND = 8;

const svg = (w, h, body) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${body}</svg>`;

// ---------------------------------------------------------------- character builder
// Poses are limb end-points relative to the shoulder/hip; proportions never change.
const POSES = {
  stand: { la: [-10, 34], ra: [10, 34], ll: [-8, 46], rl: [8, 46] },
  cheer: { la: [-26, -26], ra: [26, -26], ll: [-12, 46], rl: [12, 46] },
  wave: { la: [-10, 34], ra: [24, -22], ll: [-8, 46], rl: [8, 46] },
  reach: { la: [-10, 34], ra: [34, 6], ll: [-10, 46], rl: [10, 46] },
};

function figure({ x, y, pose = 'stand', skin = C.skin[1], shirt = C.accent, legs = C.ink, hair = C.ink }) {
  const p = POSES[pose];
  const sh = [x, y + 8], hip = [x, y + 52]; // shoulder and hip centres; y = top of body
  const limb = (from, d, color) =>
    `<path d="M${from[0]} ${from[1]}l${d[0]} ${d[1]}" stroke="${color}" stroke-width="${LIMB}" stroke-linecap="round"/>`;
  const hand = (from, d) => `<circle cx="${from[0] + d[0]}" cy="${from[1] + d[1]}" r="${HAND}" fill="${skin}"/>`;
  const hx = x, hy = y - GAP - HEAD;
  return `<g>
    ${limb([hip[0] - 7, hip[1]], p.ll, legs)}${limb([hip[0] + 7, hip[1]], p.rl, legs)}
    ${limb([sh[0] - 12, sh[1]], p.la, shirt)}${limb([sh[0] + 12, sh[1]], p.ra, shirt)}
    <rect x="${x - 19}" y="${y}" width="38" height="58" rx="19" fill="${shirt}"/>
    ${hand([sh[0] - 12, sh[1]], p.la)}${hand([sh[0] + 12, sh[1]], p.ra)}
    <circle cx="${hx}" cy="${hy}" r="${HEAD}" fill="${skin}"/>
    <path d="M${hx - HEAD} ${hy - 2}A${HEAD} ${HEAD} 0 0 1 ${hx + HEAD} ${hy - 2}Q${hx + 4} ${hy - 9} ${hx - HEAD} ${hy - 2}Z" fill="${hair}"/>
  </g>`;
}

const ground = (cx, cy, rx) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${rx * 0.12}" fill="${C.mist}"/>`;
const spark = (x, y, s, fill) => `<path d="M${x} ${y - s}L${x + s * 0.28} ${y - s * 0.28}L${x + s} ${y}L${x + s * 0.28} ${y + s * 0.28}L${x} ${y + s}L${x - s * 0.28} ${y + s * 0.28}L${x - s} ${y}L${x - s * 0.28} ${y - s * 0.28}Z" fill="${fill}"/>`;
const check = (cx, cy, r) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${C.accent}"/><path d="M${cx - r * 0.42} ${cy}l${r * 0.3} ${r * 0.3}l${r * 0.55} ${-r * 0.6}" fill="none" stroke="#fff" stroke-width="${r * 0.22}" stroke-linecap="round" stroke-linejoin="round"/>`;

// ---------------------------------------------------------------- spots by touchpoint moment
const SPOTS = {
  // celebratory: the most expression, the character, the accent as the answer
  'spot-payment-sent': svg(240, 240, `
    ${ground(120, 206, 84)}
    ${figure({ x: 98, y: 112, pose: 'cheer', skin: C.skin[0] })}
    <g transform="rotate(-12 172 82)"><rect x="140" y="62" width="64" height="40" rx="8" fill="${C.accentSoft}"/><rect x="148" y="74" width="26" height="5" rx="2.5" fill="${C.accent}"/><rect x="148" y="84" width="40" height="5" rx="2.5" fill="${C.cloud}"/></g>
    ${check(196, 64, 15)}
    ${spark(46, 70, 9, C.accent)}${spark(160, 140, 6, C.warm)}${spark(64, 40, 5, C.slate)}`),
  // functional: calm, no character, one accent detail
  'spot-empty': svg(240, 240, `
    ${ground(120, 196, 80)}
    <path d="M58 118H182L170 190H70Z" fill="${C.cloud}"/>
    <path d="M58 118L78 86H162L182 118Z" fill="${C.mist}"/>
    <rect x="96" y="118" width="48" height="14" rx="7" fill="${C.paper}"/>
    <circle cx="164" cy="74" r="20" fill="none" stroke="${C.ink}" stroke-width="7"/>
    <path d="M178 88L194 104" stroke="${C.ink}" stroke-width="9" stroke-linecap="round"/>
    <circle cx="164" cy="74" r="7" fill="${C.accent}"/>`),
  // sensitive: restraint. No character, no sparkle, accent only on the action that fixes it.
  'spot-card-frozen': svg(240, 240, `
    ${ground(120, 192, 78)}
    <rect x="52" y="78" width="136" height="88" rx="12" fill="${C.cloud}"/>
    <rect x="52" y="96" width="136" height="16" fill="${C.slate}"/>
    <rect x="66" y="128" width="40" height="8" rx="4" fill="${C.paper}"/>
    <rect x="90" y="54" width="60" height="50" rx="10" fill="${C.ink}"/>
    <path d="M104 54V44a16 16 0 0 1 32 0V54" fill="none" stroke="${C.ink}" stroke-width="8"/>
    <circle cx="120" cy="76" r="6" fill="${C.accent}"/><rect x="117" y="78" width="6" height="12" rx="3" fill="${C.accent}"/>`),
};

// ---------------------------------------------------------------- scene
const scene = svg(640, 360, `
  <rect width="640" height="360" fill="${C.paper}"/>
  <circle cx="470" cy="150" r="130" fill="${C.mist}"/>
  ${ground(320, 300, 230)}
  ${figure({ x: 230, y: 180, pose: 'reach', skin: C.skin[2], shirt: C.ink, legs: C.slate })}
  <rect x="300" y="190" width="96" height="106" rx="18" fill="${C.accentSoft}"/>
  <rect x="300" y="240" width="96" height="56" rx="18" fill="${C.accent}"/>
  <rect x="316" y="176" width="64" height="18" rx="9" fill="${C.cloud}"/>
  <path d="M460 296V120" stroke="${C.ink}" stroke-width="6" stroke-linecap="round"/>
  <path d="M463 122H520L506 140L520 158H463Z" fill="${C.accent}"/>
  ${spark(540, 90, 10, C.warm)}${spark(150, 120, 7, C.accent)}`);

// ---------------------------------------------------------------- signature: character construction sheet
const label = (x, y, t) => `<text x="${x}" y="${y}" font-family="Inter, Helvetica, Arial, sans-serif" font-size="11" fill="${C.slate}">${t}</text>`;
const signature = svg(640, 240, `
  <rect width="640" height="240" fill="${C.paper}"/>
  ${['stand', 'wave', 'cheer', 'reach'].map((pose, i) => figure({ x: 90 + i * 150, y: 92, pose, skin: C.skin[i % 3], shirt: i === 2 ? C.accent : C.ink, legs: i === 2 ? C.ink : C.slate })).join('')}
  ${label(40, 228, `limb ${LIMB} · head r${HEAD} · gap ${GAP} · hand r${HAND} · one accent per scene`)}`);

// ---------------------------------------------------------------- in context: the spot inside a phone screen
function inPhone(spotName, title) {
  const inner = SPOTS[spotName].replace(/^<svg[^>]*>|<\/svg>$/g, '');
  return svg(300, 560, `
    <rect x="6" y="6" width="288" height="548" rx="44" fill="${C.ink}"/>
    <rect x="16" y="16" width="268" height="528" rx="36" fill="${C.paper}"/>
    <rect x="118" y="26" width="64" height="18" rx="9" fill="${C.ink}"/>
    <g transform="translate(30 110)">${inner}</g>
    <text x="150" y="384" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif" font-size="20" font-weight="700" fill="${C.ink}">${title}</text>
    <rect x="70" y="402" width="160" height="10" rx="5" fill="${C.cloud}"/>
    <rect x="96" y="420" width="108" height="10" rx="5" fill="${C.cloud}"/>
    <rect x="36" y="474" width="228" height="48" rx="24" fill="${C.accent}"/>`);
}

// ---------------------------------------------------------------- write
for (const [name, s] of Object.entries(SPOTS)) write(`${name}.svg`, s);
write('scene-onboarding.svg', scene);
write('signature-character.svg', signature);
write('context-payment-sent.svg', inPhone('spot-payment-sent', 'Money sent'));
console.log('built', OUT);
