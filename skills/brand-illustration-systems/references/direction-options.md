# Three direction options

The checkpoint shows three options so the user can steer cheaply before the system is built. They must be different
enough that a person could tell them apart with the names covered.

## What makes a direction

`direction = idea + rendering family (+ optional signature device)`

- **Idea:** from the brand's own assets, a source world, or a story or cast (SKILL.md Phase 4).
- **Family:** one of the eight in `style-families.md`, or a pairing by tier (e.g. flat spots in product + 3D heroes).
- **Signature:** the one ownable element: a pattern, a character, a line quality, a material, a device, a notation.

Two directions with different ideas but the same family usually look alike. That is what went wrong when every Scan
option became a patterned object on a coloured square. **Vary the family first, then the idea.**

## Choosing the three

| User's answer | How the three differ |
|---|---|
| No direction | Three different families, each with its best-fitting idea. Cover at least one "quiet" family (flat or technical) and one "expressive" family (character, line or 3D) so the user sees range |
| Named a style or admired brand ("like Monzo") | Same family, three different ideas and signatures; extract the reference's lesson (`reference-systems.md`), never its look |
| Named a source ("Adire textiles") | Three translations in different families: e.g. pattern-led surface, flat spot shapes derived from the motif's geometry, and a character or device built from its making process |
| Partly (feelings, dislikes) | Three families that all respect the constraints |

At most one direction may be pattern-led unless the user asked for pattern. If your recommendation is the pattern-led
one, check that you are not anchoring on the examples in this skill.

## What each sample contains

Use the same subjects in every direction:

- **Name**, **family**, **idea source**.
- **Idea:** one sentence. **Looks like:** one sentence on line, shape, colour and depth.
- **Signature element:** pattern tile / character head or turnaround / line and brush swatch / material and light
  swatch / device in three states / grid and annotation sample.
- **Spot moment:** the same product moment (from the touchpoint map), ideally inside a phone frame or real component,
  plus a 48 px reduced version if the family produces icons.
- **Scene or hero moment:** the same one in all three.
- **Palette** (hex), **tone fences met**, **motion verb**, **one honest risk**.

## The overview sheet

`scripts/direction_sheet.py` builds one HTML page from JSON (paths relative to the JSON file):

```json
{
  "brand": "Bedrock",
  "tenet": "Small, regular contributions become a durable foundation.",
  "moments": {"spot": "Payment sent", "scene": "Onboarding: set your first goal"},
  "recommend": 1,
  "directions": [
    {
      "name": "Strata",
      "family": "Pattern-led surface",
      "source": "Sedimentary stratigraphy",
      "idea": "Every object is built from visible deposited layers.",
      "looks": "Pale objects with fine bedding lines, layered extruded edges, one iron-oxide accent.",
      "chain": "wealth compounds → sediment accumulates → objects gain layers",
      "motion": "deposit, settle",
      "risk": "Can become 'patterned object on a square' if compositions don't vary.",
      "palette": ["#E2531F", "#2B2236", "#F7E6C4"],
      "signature": "a/signature.svg",
      "spot": "a/spot.svg",
      "scene": "a/scene.svg"
    }
  ]
}
```

`signature`, `spot` and `scene` may be SVG, PNG or JPG (label raster exploration in `looks`). When `spot` is a phone frame, add `micro` (the bare spot) for the 48 px check, or
`"no_micro": true` for families that never reduce. The older keys `pattern`, `pictogram` and `object` are still
accepted. Add `"greyscale": true` to compare forms without colour.

## Judging the three before you show them

- Cover the names: are the three distinguishable from the spot alone? If not, change a family.
- Does each one fit the touchpoints, especially the sensitive moments?
- Is the recommendation the best fit for the tone fences, not the prettiest or the most familiar?
- Does any direction look like a known brand's system? If so, push it until it doesn't.
- Run `system_audit.py --family <family>` on every SVG and fix failures.
