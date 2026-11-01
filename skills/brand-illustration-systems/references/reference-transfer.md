# Reference transfer: recreate a piece, then apply its direction to a new subject

Use this when the user shares a single illustration (not a whole system) and asks you to recreate it, explain how it
works, or "do this, but for a laptop / our product / our brand". The reference is the preferred direction, so skip the
three-direction stage for the style itself. Offer three **subject compositions** instead if the user wants options.

A finished transfer has three parts: a **decomposition** (the rules, written down), a **recreation** that proves the
rules are complete, and a **transfer** that proves they generalise. If the recreation needs rules the decomposition
doesn't contain, the decomposition is wrong. Fix it before you transfer.

## 1. Decompose in seven layers

Work from the largest decisions to the smallest. Write each layer as rules, not adjectives.

| Layer | What to record | Example (flat editorial figure with gifts) |
|---|---|---|
| 1. Field | Canvas ratio, background treatment, how much of the canvas the subject fills | Square; one uniform butter-yellow field; figure fills about two-thirds |
| 2. Large shapes | The subject reduced to 5–12 primitives, with their exaggeration | Face and arms as pink wedges, hair as two black teardrops, torso as a curled disc around a counter-shape, legs as sweeping ribbons, mitten hands |
| 3. Palette roles | Each colour's job, not just its hex | Yellow = negative space; black = structure and anchor; blue, green, pink, mint, cyan = subjects and patterns |
| 4. Pattern owners | Which pattern belongs to which plane, and its scale | Broad black/blue stripes = sweater; mint dots = front trousers; green dots on navy = back leg; thin black/white stripes = gift lid; large white dots = pink box; thin green contour = hair |
| 5. Depth | How things sit in front of each other with no shading | Overlap only: hair over face, arms across torso, legs crossing, objects cropped by the canvas. No shadows, no gradients |
| 6. Rewards | The small secondary objects and what they do for the composition | Hearts, snowflakes, leaves, ribbons and a cat distribute colour around the silhouette and reward a second look |
| 7. Rendering | Edges, outlines, texture, projection | Crisp vector edges, no outlines, frontal flat projection; black shapes act as boundaries where needed |

Then separate three things that are easy to blur together:

- **Subject recognition:** what makes the subject readable (silhouette, proportions, one or two key details).
- **Brand geometry:** the shape language (wedges, teardrops, ribbons, counter-shapes).
- **Surface pattern:** what fills the planes.

A good transfer keeps the second and third and rebuilds the first for the new subject.

## 2. Recreate to check the rules

Rebuild the reference from the written rules, as vector where possible. Compare side by side at the same size and list
mismatches by layer. An image model can produce a quick visual check, but label it exploration. In the run this
method comes from, the model added a soft glow to a field that was perfectly uniform. Image models drift on exactly the
things a flat style depends on.

**Study, not shipping.** A close recreation of a living illustrator's piece is a study for understanding. Never ship
it, publish it as the brand's work or present it as original. If the user wants that exact look for production,
recommend commissioning the illustrator.

## 3. Transfer roles, not objects

Write a role map before drawing. Every element of the reference has a **role** in the composition. Find the element
of the new subject that can play that role.

| Reference element | Its role | Laptop element |
|---|---|---|
| Black hair with green contour | Dark anchor shape carrying the finest line pattern | Black screen with thin green contour lines |
| Striped sweater curling round a counter-shape | Largest patterned plane; makes the main curve | An app window or cable loop with the broad stripes, curving round open space |
| Pink face and hands | Large calm colour planes that rest the eye | Pink trackpad, or a pink case |
| Dotted trouser ribbon | Long sweeping movement across the canvas | Charging cable as a sweeping ribbon with the dot pattern |
| Boots with white cuffs | Terminal shapes that end a movement | Connector with a white collar |
| Gift lid stripes | Narrow, busy texture on a small plane | Keyboard |
| Gifts, cat, snowflakes, hearts | Rewards: secondary objects that spread colour | **New props from the laptop's world:** a mug, sticky notes, headphones, a plant, a notification heart |

Rules:

- **Keep pattern owners stable.** Once a pattern belongs to a role (broad stripes = the main curve), it keeps that role
  in every new subject. Don't redistribute patterns at random.
- **Replace the rewards.** Copying the reference's props (gifts, cat, cake) into a new subject is the most common
  failure: the result reads as the old picture with a laptop pasted in. Props must come from the new subject's world.
  Keep their role (small, scattered, colour-spreading), not their identity.
- **Keep the projection.** If the reference is frontal and flat, the new subject is frontal and flat too. Don't let a
  three-quarter perspective creep in because the subject is usually drawn that way.
- **Keep the silhouette clean.** A transferred pattern ribbon must not cross the subject's key recognition feature
  (for a laptop: the hinge line, the screen edge, the keyboard deck).

## 4. Checks before showing

| Check | How | Pass when |
|---|---|---|
| Large-shape test | `render_png.py --silhouette` (all fills black) and `--grey` | The subject is recognisable as a silhouette, and composition still works before pattern and colour |
| Pattern-owner test | Compare the role map with the artwork | Every pattern sits on the role it owns in the reference |
| Prop test | List every secondary object | None is carried over from the reference unless it belongs to the new subject's world |
| Projection test | Compare horizon and angle | Same projection as the reference |
| Flat-field test | `raster_check.py image.png` for raster exploration; for vector, the background is one solid `<rect>` | Field variation under the threshold; no glow, vignette or gradient |
| Palette test | `raster_check.py` reports dominant colours; `system_audit.py --family pattern` for SVG | Same palette roles as the reference, no stray hues |

## Worked example: what the Codex laptop run got right and wrong

**Right:** the seven-layer decomposition; pattern owners mostly transferred by role (screen took the hair's contour
lines, keyboard took the gift-lid stripes, cable took the dotted-trouser ribbon); the laptop reads from its silhouette;
a background correction pass after spotting the glow.

**Wrong:** the gift, cat, cake, hearts and snowflakes were copied from the reference, which broke its own "transfer roles,
not objects" rule; the laptop slipped into three-quarter perspective while the reference is frontal; the striped
ribbon crossed the keyboard, the laptop's key recognition feature; and the output was raster only, so it was exploration
rather than a reusable system. Rebuild the transfer as vector from the role map before calling it done.
