#!/usr/bin/env python3
"""Build the three-direction overview sheet shown at the checkpoint.

  python3 direction_sheet.py directions.json -o directions.html

The JSON spec (see references/direction-options.md) lists 2-4 directions, each with a name, source, idea,
meaning chain, motion verb, risk, palette (hex list) and three SVG paths: pattern, pictogram and object. Paths are
relative to the JSON file. Every SVG is embedded as a data URI, so the HTML is self-contained and the SVGs' ids
cannot collide. Render it with render_png.py to get the image you show the user.
Standard library only.
"""
import argparse
import base64
import html
import json
import os
import sys

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F6F4EF;color:#1D1A22;font:15px/1.5 Inter,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:1560px;margin:0 auto;padding:40px 40px 48px}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:28px}
h1{margin:0;font-size:30px;letter-spacing:-.02em}
.tenet{color:#5E5866;max-width:70ch;margin:6px 0 0}
.meta{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#8A8392}
.grid{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:20px}
.col{background:#fff;border:1px solid #E4E0D8;border-radius:18px;overflow:hidden;display:flex;flex-direction:column}
.col.rec{border:2px solid #1D1A22}
.head{padding:18px 20px 14px;border-bottom:1px solid #EEEAE3}
.letter{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:#1D1A22;color:#fff;font-weight:700;font-size:13px;margin-right:10px}
.name{font-size:20px;font-weight:750;letter-spacing:-.01em}
.source{color:#6E6776;font-size:13px;margin-top:4px}
.badge{float:right;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:#1D1A22;color:#fff;padding:4px 9px;border-radius:99px}
.pattern{height:120px;background-size:cover;background-position:center;border-bottom:1px solid #EEEAE3}
.assets{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid #EEEAE3}
.assets figure{margin:0;padding:16px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;gap:10px;min-height:250px}
.assets figure+figure{border-left:1px solid #EEEAE3}
.assets img.big{width:100%;max-width:180px;height:auto}
.micro{display:flex;align-items:center;gap:8px;font-size:11px;color:#8A8392}
figcaption{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8A8392}
.palette{display:flex;height:28px}
.palette i{flex:1}
.text{padding:16px 20px 20px;display:grid;gap:10px}
.text p{margin:0}
.k{display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#8A8392;font-weight:700}
.grey img{filter:grayscale(1)}
"""


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("ascii")


def need(d, key, i):
    if key not in d or d[key] in ("", None):
        sys.exit(f"direction {i + 1} is missing '{key}'")
    return d[key]


def column(d, i, base, recommended):
    esc = lambda s: html.escape(str(s))
    paths = {}
    for key in ("pattern", "pictogram", "object"):
        p = os.path.join(base, need(d, key, i))
        if not os.path.isfile(p):
            sys.exit(f"direction {i + 1}: file not found for '{key}': {p}")
        paths[key] = data_uri(p)
    swatches = "".join(f'<i style="background:{esc(c)}" title="{esc(c)}"></i>' for c in d.get("palette", []))
    letter = "ABCD"[i]
    rows = [("Idea", d.get("idea")), ("Meaning chain", d.get("chain")), ("Moves like", d.get("motion")), ("Risk", d.get("risk"))]
    text = "".join(f'<p><span class="k">{k}</span>{esc(v)}</p>' for k, v in rows if v)
    return f"""
<section class="col{' rec' if recommended else ''}{' grey' if d.get('greyscale') else ''}">
  <div class="head">{'<span class="badge">Recommended</span>' if recommended else ''}
    <div><span class="letter">{letter}</span><span class="name">{esc(need(d, 'name', i))}</span></div>
    <div class="source">{esc(d.get('source', ''))}</div>
  </div>
  <div class="pattern" style="background-image:url('{paths['pattern']}')" role="img" aria-label="Pattern tile"></div>
  <div class="assets">
    <figure><figcaption>Pictogram</figcaption><img class="big" src="{paths['pictogram']}" alt="Pictogram"><div class="micro">24 px <img src="{paths['pictogram']}" width="24" height="24" alt=""></div></figure>
    <figure><figcaption>Editorial object</figcaption><img class="big" src="{paths['object']}" alt="Editorial object"><div class="micro">&nbsp;</div></figure>
  </div>
  <div class="palette">{swatches}</div>
  <div class="text">{text}</div>
</section>"""


def build(spec, base):
    dirs = spec.get("directions") or []
    if not 2 <= len(dirs) <= 4:
        sys.exit(f"expected 2-4 directions, got {len(dirs)} (three is the norm)")
    rec = spec.get("recommend")
    cols = "".join(column(d, i, base, i == rec) for i, d in enumerate(dirs))
    brand = html.escape(spec.get("brand", "Directions"))
    tenet = html.escape(spec.get("tenet", ""))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{brand}: illustration directions</title><style>{CSS}</style></head>
<body><div class="wrap">
<header><div><div class="meta">Illustration system · {len(dirs)} directions</div><h1>{brand}</h1><p class="tenet">{tenet}</p></div></header>
<div class="grid" style="--n:{len(dirs)}">{cols}</div>
</div></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("spec", help="directions JSON")
    ap.add_argument("-o", "--out", default="directions.html")
    a = ap.parse_args()
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    out = build(spec, os.path.dirname(os.path.abspath(a.spec)))
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {a.out} ({len(spec['directions'])} directions)")


if __name__ == "__main__":
    main()
