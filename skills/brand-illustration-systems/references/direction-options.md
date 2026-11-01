# Three direction options

The checkpoint shows three options so the user can steer cheaply before the expensive proof family is built. Three is
enough to show range without diluting attention. The options must be genuinely different.

## When the user had no direction (answers b or c)

Choose three source worlds that differ in **behaviour**, not just in subject. Behaviour is the operation the source
performs, which then drives form, depth and motion.

| Behaviour family | Example sources | Typical grammar |
|---|---|---|
| Accumulate / stack | Sedimentary strata, tree rings, coral, ledger ruling | Bands, layered edges, growth from a base |
| Interlace / weave | Textiles, basketry, guilloché, circuit routing | Crossing line families, over-under, lattices |
| Branch / flow | Rivers, root systems, transit maps, veins | Continuous lines, junctions, directional motion |
| Fold / cut | Origami, paper engineering, packaging nets | Planes, creases, unfolding motion |
| Register / print | Risograph, letterpress, security print, screen print | Offset layers, halftones, misregistration |
| Orbit / measure | Instruments, sundials, star charts, gauges | Concentric rings, ticks, rotational motion |

Choose the three from **different rows**. If two candidates share a row, keep the stronger one and replace the other.

## When the user named a direction (answer a)

All three options are translations of their source. Vary along these axes, and make each option a clear position on
at least two of them:

| Axis | One end | Other end |
|---|---|---|
| Grammar emphasis | Pattern-led (the source lives in surface linework) | Structure-led (the source shapes silhouettes and depth; little surface pattern) |
| Depth model | Flat | Isometric / extruded |
| Density | Sparse, one gesture | Intricate, engraving-like |
| Literalness | Recognisable source motifs | Abstracted rules only |
| Colour | Single anchor + pale faces | Two-tone print-like |

Name each option by its position, for example "Strata · Engraved" (pattern-led, intricate, flat), "Strata · Built"
(structure-led, extruded, sparse) and "Strata · Core" (literal cross-sections, isometric).

If you believe a different source world is clearly stronger, add one line after the three options: "If you're open
to it, <source> may fit better because <reason>." Never replace their direction unasked.

## What each direction sample contains

Keep the samples lean and comparable, with the same subjects in each:

- **Name** and **source world** (or translation position).
- **Idea:** one sentence. If it needs a paragraph, it is not ready.
- **Meaning chain:** tenet → source behaviour → visual rule.
- **Palette:** anchor, ink and 3–5 faces, with hex values.
- **Pattern tile:** an SVG showing the source primitives.
- **Pictogram:** the same subject for all three, flat, at display size plus a 24 px micro version.
- **Editorial object:** the same subject for all three, in the direction's depth model.
- **Motion verb:** how it moves, one or two words.
- **Risk:** one honest weakness (small-size legibility, cultural sensitivity, category overlap).

## The overview sheet

`scripts/direction_sheet.py` builds one HTML page (and you render it to PNG) from a JSON spec:

```json
{
  "brand": "Bedrock",
  "tenet": "Small, regular contributions become a durable foundation.",
  "recommend": 0,
  "directions": [
    {
      "name": "Strata",
      "source": "Sedimentary stratigraphy",
      "idea": "Every object is built from visible deposited layers.",
      "chain": "wealth compounds → sediment accumulates → objects gain layers",
      "motion": "deposit, settle",
      "risk": "Banding can read as 'retro stripes' if line weight drifts up.",
      "palette": ["#E2531F", "#2B2236", "#F7E6C4", "#F7D6C7", "#E0ECD6"],
      "pattern": "a/pattern.svg",
      "pictogram": "a/goal.svg",
      "object": "a/bulb.svg"
    }
  ]
}
```

Paths are relative to the JSON file. The sheet shows each direction as a column with its pattern tile, pictogram at
display and 24 px, editorial object, palette strip, idea, chain, motion and risk, and marks the recommended one. Add
`"greyscale": true` to a direction to show its forms without colour, if colour would distract.

## Judging the three before you show them

- Cover the names: could someone tell the three apart from the pictogram alone? If not, they are one direction.
- Does each one shape at least two of silhouette, depth and motion, not only surface?
- Is your recommendation the one that best fits the tenet, rather than the prettiest?
- Run `system_audit.py` on every sample, and fix failures before showing anything.
