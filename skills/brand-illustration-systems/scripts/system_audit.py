#!/usr/bin/env python3
"""Audit SVG illustration assets for the failures that break a system.

  python3 system_audit.py assets/*.svg            # human-readable report
  python3 system_audit.py assets/*.svg --json     # machine-readable

FAIL  embedded raster images; filters (drop shadows, blur, lighting)
WARN  gradients; live <text>; more than one saturated anchor hue; pattern lines heavy relative to their gaps;
      pattern line contrast too high against its face (ink on pastel); no <pattern> at all
Exit code 1 if any file has a FAIL. Standard library only.
"""
import argparse
import colorsys
import json
import re
import sys
import xml.etree.ElementTree as ET

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def local(tag):
    return tag.rsplit("}", 1)[-1]


def norm_hex(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h.upper()


def rgb(h):
    h = norm_hex(h)[1:]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def paint(el, prop):
    v = el.get(prop)
    style = el.get("style", "")
    m = re.search(rf"{prop}\s*:\s*([^;]+)", style)
    if m:
        v = m.group(1)
    return v.strip() if v else None


def num(v, default=None):
    try:
        return float(re.match(r"[-\d.]+", str(v)).group(0))
    except (AttributeError, TypeError, ValueError):
        return default


def saturated_hues(colors):
    """Cluster strongly saturated mid-lightness colours by hue (30 degree buckets)."""
    hues = []
    for c in colors:
        h, l, s = colorsys.rgb_to_hls(*rgb(c))
        if s >= 0.55 and 0.28 <= l <= 0.72:
            deg = h * 360
            if not any(min(abs(deg - x), 360 - abs(deg - x)) < 30 for x in hues):
                hues.append(deg)
    return hues


def audit(path, max_anchor=1):
    res = {"file": path, "fail": [], "warn": [], "info": []}
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as e:
        res["fail"].append(f"cannot parse: {e}")
        return res
    els = list(root.iter())
    tags = [local(e.tag) for e in els]
    raw = open(path, encoding="utf-8", errors="replace").read()

    if "image" in tags or "data:image/png" in raw or "data:image/jpeg" in raw:
        res["fail"].append("embedded raster image: a system proof must be vector")
    if "filter" in tags or any(e.get("filter") for e in els) or re.search(r"filter\s*:\s*(drop-shadow|blur|url)", raw):
        res["fail"].append("filter found (drop shadow / blur / lighting): use construction, not rendering")
    if "linearGradient" in tags or "radialGradient" in tags:
        res["warn"].append("gradient found: allowed only if the source world demands it")
    if "text" in tags:
        res["warn"].append("live <text>: outline it, or confirm the font ships with the asset")

    colors = {norm_hex(m.group(0)) for m in HEX.finditer(raw)}
    hues = saturated_hues(colors)
    if len(hues) > max_anchor:
        res["warn"].append(f"{len(hues)} saturated hues (around {', '.join(f'{h:.0f}°' for h in hues)}): "
                           f"keep one anchor and let the faces stay pale")

    patterns = [e for e in els if local(e.tag) == "pattern"]
    if not patterns:
        res["warn"].append("no <pattern>: is the source grammar living only in hand-drawn texture?")
    for p in patterns:
        pid = p.get("id", "?")
        h = num(p.get("height"))
        face = None
        for c in p.iter():
            if local(c.tag) == "rect":
                f = paint(c, "fill")
                if f and HEX.fullmatch(f):
                    face = norm_hex(f)
                    break
        strokes = []
        for c in p.iter():
            st, sw = paint(c, "stroke"), num(paint(c, "stroke-width"), 1.0)
            if st and HEX.fullmatch(st) and local(c.tag) in ("path", "line", "polyline", "circle", "ellipse"):
                strokes.append((norm_hex(st), sw))
        if strokes and h:
            gap = h / len(strokes)
            sw = max(w for _, w in strokes)
            if sw / gap > 0.35:
                res["warn"].append(f"pattern '{pid}': stroke {sw:g} with about {gap:g} between lines "
                                   f"({sw / gap:.0%} of the gap); linework this heavy reads as bands")
        if strokes and face:
            cr = contrast(strokes[0][0], face)
            if cr > 2.2:
                res["warn"].append(f"pattern '{pid}': line {strokes[0][0]} on face {face} has contrast {cr:.1f}:1; "
                                   f"use one tone step darker than the face (about 1.2-2:1)")

    res["info"].append(f"{len(patterns)} pattern(s)")
    res["info"].append(f"{len(els)} elements, {len(colors)} colours")
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-anchor", type=int, default=1, help="saturated hues allowed (default 1)")
    a = ap.parse_args()
    results = [audit(f, a.max_anchor) for f in a.files]
    if a.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            status = "FAIL" if r["fail"] else "WARN" if r["warn"] else "PASS"
            print(f"[{status}] {r['file']}")
            for k in ("fail", "warn", "info"):
                for msg in r[k]:
                    print(f"   {k:<4}  {msg}")
    sys.exit(1 if any(r["fail"] for r in results) else 0)


if __name__ == "__main__":
    main()
