"""Flat editorial kit: a reusable vector grammar for bold flat figurative illustration (Transfer mode).

Recovered by rebuilding a flat editorial reference shape by shape and scoring it with scripts/match_score.py
(see references/reference-transfer.md). The defaults are that study's palette and measured proportions; they are a
starting grammar, not a house style. For a brand, re-measure your own reference, then swap ROLES hexes and P values
and keep the roles: which colour owns which pattern is what makes the style read.

Every size is a fraction of the canvas width, so any canvas shares proportions with the measured study.
Standard library only. Import it (or copy it next to your build script), build a Canvas, add shapes, save():

  from flat_editorial_kit import Canvas, ribbon, heart
  cv = Canvas(1200, palette={'field': '#F2EBDD', 'main': '#2B59C3'})
  cv.stripes(body_path); cv.dots(ribbon(points, 60, 90)); cv.save('spot.svg')

  python3 flat_editorial_kit.py out.svg     # writes a small demo spot
"""
import math
import sys

# Palette by role, not by name. Swap the hexes for a brand; keep the roles.
ROLES = dict(field='#FFF47C',   # negative space: one flat colour, never shaded
             anchor='#000000',  # structure: the darkest, biggest calm shapes; overlaps turn this colour
             main='#0081C7',    # the largest patterned plane (stripes) and long ribbons (dots)
             calm='#FCB4C6',    # skin-like rest planes: hands, faces, soft objects
             light='#FFFFFF',   # cuffs, highlights, dots on calm planes
             cool='#7AF5FD',    # cool props: boots, ribbons, steam, flakes
             accent='#03AC61',  # fine contours, leaves, ribbons on boxes
             pop='#84FDAA',     # dots on main, icing, small highlights
             deep='#06466E')    # the one shaded plane, pushed back with a gradient

# Proportions measured on the study (2252 px wide), as fractions of canvas width.
P = dict(stripe=62 / 2252,          # broad horizontal stripe on the main plane
         sleeve=59 / 2252,          # vertical stripe on a straight sleeve
         dot_r=8.9 / 2252,          # dot radius on ribbons
         dot_step=47.62 / 2252,     # along a dot column
         dot_col=38.6 / 2252,       # between dot columns
         dot_shift=-9.4 / 2252,     # odd columns shift along by this
         dot_angle=-33.55,          # columns run at 56.45 degrees; the grid never bends with the form
         polka_r=29 / 2252,         # big white dots on calm boxes
         polka_dx=150 / 2252, polka_dy=62 / 2252,
         pin=31.73 / 2252,          # thin black/white stripe period on small busy planes
         contour=(6 / 2252, 12 / 2252))  # tapered contour width, thin start to thick end


def f(v):
    return f"{v:.1f}".rstrip('0').rstrip('.')


def pt(cx, cy, r, a):
    return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))


def poly(points):
    return 'M' + ' L'.join(f"{f(x)},{f(y)}" for x, y in points) + ' Z'


def sector(cx, cy, R, r, a0, a1):
    if a1 - a0 >= 359.9:
        m = (a0 + a1) / 2
        return sector(cx, cy, R, r, a0, m) + ' ' + sector(cx, cy, R, r, m, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = pt(cx, cy, R, a0); x1, y1 = pt(cx, cy, R, a1)
    if r <= 0:
        return f"M{f(cx)},{f(cy)} L{f(x0)},{f(y0)} A{f(R)},{f(R)} 0 {large} 1 {f(x1)},{f(y1)} Z"
    x2, y2 = pt(cx, cy, r, a1); x3, y3 = pt(cx, cy, r, a0)
    return (f"M{f(x0)},{f(y0)} A{f(R)},{f(R)} 0 {large} 1 {f(x1)},{f(y1)} L{f(x2)},{f(y2)} "
            f"A{f(r)},{f(r)} 0 {large} 0 {f(x3)},{f(y3)} Z")


def smooth(points, closed=True, t=0.5, corners=()):
    p = points; n = len(p); d = f"M{f(p[0][0])},{f(p[0][1])}"
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = p[(i - 1) % n], p[i], p[(i + 1) % n], p[(i + 2) % n]
        if not closed:
            p0 = p[max(i - 1, 0)]; p3 = p[min(i + 2, n - 1)]
        k1 = 0 if i in corners else t / 3
        k2 = 0 if (i + 1) % n in corners else t / 3
        c1 = (p1[0] + (p2[0] - p0[0]) * k1, p1[1] + (p2[1] - p0[1]) * k1)
        c2 = (p2[0] - (p3[0] - p1[0]) * k2, p2[1] - (p3[1] - p1[1]) * k2)
        d += f" C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d + (" Z" if closed else "")


def _bez(p0, p1, p2, p3, n=24):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1])
            for t in (i / n for i in range(n + 1))]


def spine(points, n=16):
    """Densify a centreline through the given points (Catmull-Rom), for ribbons and contours."""
    out = []
    for i in range(len(points) - 1):
        p0 = points[max(i - 1, 0)]; p1 = points[i]; p2 = points[i + 1]; p3 = points[min(i + 2, len(points) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out += _bez(p1, c1, c2, p2, n)[(1 if i else 0):]
    return out


def ribbon(points, w0, w1=None):
    """Filled band along a centreline; width runs w0 -> w1. Ribbons carry dots; contours are thin ribbons."""
    w1 = w0 if w1 is None else w1
    c = spine(points); n = len(c); L, R = [], []
    for i, (x, y) in enumerate(c):
        a = c[max(i - 1, 0)]; b = c[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; m = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((x - dy / m * w, y + dx / m * w)); R.append((x + dy / m * w, y - dx / m * w))
    return poly(L + R[::-1])


def heart(cx, cy, s, rot=0):
    q = s / 2
    pts = [(0, q * .95), (-q * .93, -q * .02), (0, -q * .6), (q * .93, -q * .02)]
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    P_ = [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
    r = f(q * .5)
    return (f"M{f(P_[0][0])},{f(P_[0][1])} L{f(P_[1][0])},{f(P_[1][1])} A{r},{r} 0 0 1 {f(P_[2][0])},{f(P_[2][1])} "
            f"A{r},{r} 0 0 1 {f(P_[3][0])},{f(P_[3][1])} Z")


def capsule(x, y, w, h, rot=0, cx=None, cy=None):
    t = f' transform="rotate({rot} {f(cx if cx is not None else x + w / 2)} {f(cy if cy is not None else y + h / 2)})"' if rot else ''
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(min(w, h) / 2)}"{t}'


class Canvas:
    def __init__(self, w, h=None, palette=None):
        self.w, self.h = w, h or w
        self.c = dict(ROLES, **(palette or {}))
        self.defs, self.body, self._n = [], [], 0
        self.s = lambda k: P[k] * self.w            # proportion -> px on this canvas
        self.add(f'<rect width="{self.w}" height="{self.h}" fill="{self.c["field"]}"/>')

    def add(self, s):
        self.body.append(s)

    def fill(self, d, role, extra=''):
        self.add(f'<path d="{d}" fill="{self.c.get(role, role)}"{extra}/>')

    def clip(self, d):
        self._n += 1; i = f"k{self._n}"
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return f'clip-path="url(#{i})"'

    def group(self, d, inner):
        self.add(f'<g {self.clip(d)}>{inner}</g>')

    # ---- surface patterns, each owned by one role
    def stripes(self, d, horizontal=True, start=None, base='main', ink='anchor', width=None):
        """Broad stripes (main plane). Horizontal on bodies; vertical on straight sleeves."""
        w = width or self.s('stripe'); o = start if start is not None else 0
        if horizontal:
            bands = ''.join(f'<rect x="0" y="{f(o + 2 * w * i)}" width="{self.w}" height="{f(w)}" fill="{self.c[ink]}"/>'
                            for i in range(-1, int(self.h / w) + 2))
        else:
            bands = ''.join(f'<rect x="{f(o + 2 * w * i)}" y="0" width="{f(w)}" height="{self.h}" fill="{self.c[ink]}"/>'
                            for i in range(-1, int(self.w / w) + 2))
        self.group(d, f'<path d="{d}" fill="{self.c[base]}"/>{bands}')

    def radial(self, cx, cy, R, r, a0, a1, step, base='main', ink='anchor', phase=0):
        """A ring (sleeve curled into a circle). Its stripes are radial: stripes follow the primitive they sit on."""
        d = sector(cx, cy, R, r, a0, a1)
        bands = ''.join(f'<path d="{sector(cx, cy, R + 4, max(r - 4, 0), a, a + step / 2)}" fill="{self.c[ink]}"/>'
                        for a in [a0 + phase + step * i for i in range(int((a1 - a0) / step) + 2)])
        self.group(d, f'<path d="{d}" fill="{self.c[base]}"/>{bands}')
        return d

    def dots(self, d, base='main', ink='pop', origin=(0, 0)):
        """Ribbon dots: fixed-direction columns at 56.45 degrees, odd columns nudged; never bent to the form."""
        a = math.radians(P['dot_angle']); n = (math.cos(a), math.sin(a)); u = (-n[1], n[0])
        L, sp, sh, r = self.s('dot_step'), self.s('dot_col'), self.s('dot_shift'), self.s('dot_r')
        pts = []
        span = int(1.6 * max(self.w, self.h) / min(L, sp))
        for k in range(-span, span):
            for m in range(-span, span):
                v = m * L + (sh if k % 2 else 0); s = k * sp
                x = origin[0] + s * n[0] + v * u[0]; y = origin[1] + s * n[1] + v * u[1]
                if -r <= x <= self.w + r and -r <= y <= self.h + r:
                    pts.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>')
        self.group(d, f'<path d="{d}" fill="{self.c[base]}"/><g fill="{self.c[ink]}">{"".join(pts)}</g>')

    def polka(self, d, base='calm', ink='light', origin=(0, 0), r=None):
        """Big half-drop dots on calm boxes."""
        r = r or self.s('polka_r'); dx, dy = self.s('polka_dx'), self.s('polka_dy')
        pts = []
        for j in range(-2, int(self.h / dy) + 3):
            for i in range(-2, int(self.w / dx) + 3):
                x = origin[0] + i * dx + (dx * .48 if j % 2 else 0); y = origin[1] + j * dy
                pts.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>')
        self.group(d, f'<path d="{d}" fill="{self.c[base]}"/><g fill="{self.c[ink]}">{"".join(pts)}</g>')

    def pinstripe(self, x, y, w, h, vertical=True):
        """Thin black/white stripes for a small busy plane (gift lid, keyboard)."""
        p = self.s('pin'); ink = p * 0.46
        bars = ''.join(f'<rect x="{f(x + p * i + p * .44)}" y="{f(y)}" width="{f(ink)}" height="{f(h)}"/>' if vertical else
                       f'<rect x="{f(x)}" y="{f(y + p * i + p * .44)}" width="{f(w)}" height="{f(ink)}"/>'
                       for i in range(int((w if vertical else h) / p) + 1))
        d = poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
        self.group(d, f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{self.c["light"]}"/>'
                      f'<g fill="{self.c["anchor"]}">{bars}</g>')

    def contour(self, points, role='accent', thin_first=True, size=None):
        """Brush contour on an anchor shape: tapers thin -> thick toward the shape's outer edge.
        Pass size = the width of the shape it sits on: contours scale with their shape (2.5% -> 5%), not the canvas;
        canvas-scaled contours vanish on small spots."""
        a, b = (size * .025, size * .05) if size else self.s('contour')
        self.fill(ribbon(points, a if thin_first else b, b if thin_first else a), role)

    def overlap(self, d_under, d_over, role='anchor'):
        """Where two shapes overlap, the overlap is the anchor colour (hair over face, heart over heart)."""
        self.group(d_under, f'<path d="{d_over}" fill="{self.c[role]}"/>')

    def deep_gradient(self, cx, cy, r):
        """The one shaded plane: a radial from darker than `deep` at the core to lighter at the rim. Fill a shape
        that passes behind another with it; nothing else in the piece is shaded."""
        h = self.c['deep'].lstrip('#'); rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        tone = lambda k: '#' + ''.join(f"{max(0, min(255, round(v * k))):02X}" for v in rgb)
        self._n += 1; i = f"g{self._n}"
        self.defs.append(f'<radialGradient id="{i}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" gradientUnits="userSpaceOnUse">'
                         f'<stop offset="0" stop-color="{tone(0.62)}"/><stop offset=".55" stop-color="{tone(0.95)}"/>'
                         f'<stop offset="1" stop-color="{tone(1.35)}"/></radialGradient>')
        return f"url(#{i})"

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')

    def save(self, path):
        open(path, 'w').write(self.svg())
        return path


def demo(path):
    """A mug with a dotted ribbon of steam passing behind a striped body: every role in one small spot."""
    cv = Canvas(800)
    w = cv.w
    tail = ribbon([(w * .18, w * .92), (w * .30, w * .62), (w * .52, w * .52), (w * .70, w * .30)], w * .09, w * .06)
    cv.fill(tail, cv.deep_gradient(w * .4, w * .6, w * .5))
    body = smooth([(w * .34, w * .40), (w * .66, w * .40), (w * .63, w * .78), (w * .37, w * .78)], corners=(0, 1, 2, 3))
    cv.stripes(body, start=w * .40)
    handle = sector(w * .66, w * .58, w * .13, w * .06, -90, 90)
    cv.fill(handle, 'anchor')
    cv.add(capsule(w * .30, w * .36, w * .40, w * .06) + f' fill="{cv.c["light"]}"/>')
    steam = ribbon([(w * .46, w * .34), (w * .40, w * .22), (w * .52, w * .12), (w * .46, w * .02)], w * .07, w * .04)
    cv.dots(steam, base='cool', ink='light')
    big, small = heart(w * .47, w * .6, w * .16, -8), heart(w * .54, w * .655, w * .1, 12)
    cv.fill(big, 'calm'); cv.fill(small, 'calm')
    cv.overlap(big, small)
    cv.contour([(w * .70, w * .49), (w * .76, w * .58), (w * .70, w * .67)], size=w * .26)
    return cv.save(path)


if __name__ == '__main__':
    print(demo(sys.argv[1] if len(sys.argv) > 1 else 'flat-editorial-demo.svg'))
