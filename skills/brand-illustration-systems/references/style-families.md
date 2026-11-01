# Rendering families

A direction is **an idea expressed through a rendering family**. The source world or metaphor supplies the idea; the
family decides how it is drawn. Surface pattern (the Cowrywise approach) is only one family. Choose the family from the
brand's touchpoints and personality, not from the last reference you saw.

Each entry lists what it is, who does it, when it fits, how it is constructed, how it reduces, and its failure mode.
"Documented" means a brand or agency has published it; "observed" means it is visible in the brand's public work but not
formally documented. Re-verify before citing either to a client.

## 1. Flat geometric spot

**What:** a few solid shapes, no outline, minimal or no shading, generous negative space, one accent colour.
**Who:** Atlassian spot illustrations (documented: one concept per spot, for empty and error states and celebrations;
colourful for emphasis, neutral for routine moments). Duolingo's shape language (documented: few vector shapes, clear
silhouettes, fewest details needed, exaggeration, white negative space so art doesn't fight the UI).
**Fits:** product UI with many states; brands that value clarity and speed; large libraries produced by many hands.
**Construction:** a primitive set (circle, rounded rect, capsule, triangle), fixed corner radii, 2–4 colours per
illustration plus neutrals, one accent per scene, shadow as a flat darker shape or none.
**Reduces:** excellently; it is already near icon level.
**Fails when:** it becomes the generic "corporate flat" look with faceless people. Give it one ownable rule: an
exaggerated proportion, a signature cut, a borrowed letterform curve, a colour habit.

## 2. Character / mascot-led

**What:** a recurring character or cast carries emotion and story.
**Who:** Duolingo's Duo and supporting cast (observed: characters composed with speech bubbles and backgrounds into
scenes). Mailchimp's Freddie (documented by Buck as the mascot that a later device had to complement, not compete with).
Headspace's rounded, closed-eye figures (observed; Headspace states it has no official mascot).
**Fits:** consumer brands that need warmth, habit, encouragement or humour; education, health, community.
**Construction:** a character sheet: head-to-body ratio, construction shapes, poses, expressions, what never changes
(silhouette, eyes, colour); rules for groups; how far the character can deform in motion.
**Reduces:** the head or a signature feature works as an avatar, but full poses don't reduce to icons.
**Fails when:** the character is cute but off-tone for money or serious moments. Define where it must not appear (fraud,
loss, disputes).

## 3. Expressive line / editorial hand

**What:** drawn line with personality: hand-made wobble, pencil or ink texture, editorial wit.
**Who:** Monzo's 2022 suite by illustrator Ola Dobrzyńska (documented: brief was personality, movement and energy, and
to avoid flat geometry and generic people; 90 illustrations; made for global use). Cash App's 2D spot system by Buck
(documented: influenced by drawings in sophisticated editorial magazines; "charming but not cute, simple but not
plain"; mapped to in-app surfaces). Dropbox (observed: commissioned artists, pencil texture with layered colour).
**Fits:** brands that want humanity and wit over polish; marketing and editorial-heavy brands.
**Construction:** line weight range, line character (wobble, taper, pencil grain), whether fills misregister from line,
colour as flat shapes under the line, a figure-drawing convention.
**Reduces:** poorly below about 64 px. Pair it with a separate icon set.
**Fails when:** each illustrator's hand drifts. Lock the brush, weight and figure conventions, and keep a reference board.

## 4. Soft 3D / rendered objects

**What:** modelled objects with soft lighting, rounded forms, a "collectible" quality.
**Who:** Cash App's Evergreen system by Buck (documented: a 3D illustration library delivered with source files, plus 3D
brand guidelines; reported at over 650 icons and assets). Revolut (documented in hiring material: simple 3D illustrations
and animations to help people understand product actions). Klarna's promotional 3D work (observed).
**Fits:** fintech and consumer apps that want tactility and premium feel; feature marketing; app-store art.
**Construction:** a fixed camera (lens, angle), a lighting rig, material library (matte, gloss, frosted), corner bevel
radius, a colour-to-material map, a ground and shadow rule. The production kit is the 3D scene file, not the renders.
**Reduces:** to flat icon equivalents only if designed in parallel.
**Fails when:** the lighting or camera varies by artist, or it slides into generic "3D emoji" stock. Specify the rig.
**Agent note:** without a 3D tool, approximate with SVG gradients for direction samples and label them as
approximations. An image model may explore it, labelled as exploration. The production family needs a real scene kit.

## 5. Pattern-led surface

**What:** fine pattern or linework clipped inside clean silhouettes; the pattern carries the brand.
**Who:** Cowrywise by Dá Design Studio (documented: colourful guilloché-inspired patterns, 3D language for "looking at
things from all sides"). See `cowrywise-example.md`.
**Fits:** brands with a strong material or cultural source (security print, textiles, cartography); editorial covers.
**Construction:** a seamless tile from source primitives; line one tone darker than its face; pattern never
outweighs the silhouette; pattern-free reduced state.
**Reduces:** the pattern drops away at small sizes, leaving the silhouette.
**Two variants:**
- *Pattern on the object* (Cowrywise): one source pattern fills the silhouettes of objects.
- *Patterned planes* (cut-paper editorial): a flat, frontal figure built from oversized geometric shapes, where each
  plane owns its own simple pattern (broad stripes on the jumper, dots on the trousers, fine contour lines on the
  hair). Patterns are assigned by role, depth comes from overlap and counter-shapes, and small reward objects spread
  the palette. See `reference-transfer.md` for the full decomposition.

**Fails when:** every asset becomes "patterned object on a coloured square". That is one composition, not a system.
Vary scale, crop and scene type, and don't make pattern the default for every brand.

## 6. Technical / diagrammatic

**What:** drawing borrowed from charts, schematics, blueprints, maps or UI wireframes.
**Who:** Robinhood's 2024 identity (documented by Porto Rocha: a highly technical illustration style inspired by
financial graphs; black-and-white palette with a neon accent). Atlassian's low-fi UI (documented: basic shapes, sharp
corners, mostly grey, for onboarding and feature tours; never real screenshots in product).
**Fits:** tools for experts, investing, developer products, B2B; explaining flows and features.
**Construction:** grid, line weights by hierarchy, annotation conventions, how data is abstracted, one accent for the
"answer".
**Reduces:** well as line icons.
**Fails when:** it becomes cold or reads as real data. Keep it abstract, and allow one human or emotional cue.

## 7. Brand device / recurring object

**What:** one ownable object or shape that transforms to tell many stories, often derived from the logo or typeface.
**Who:** Mailchimp's "The Cube" by Buck (documented: an illustration mark that "unfolds" to tell any story, mainly a
transitional device between type and UI, complementing the mascot). Klarna's in-product system by Animade (documented:
built on the curvature of Klarna's typography and its italic moments, extrapolated from palette, photography and tone).
**Fits:** brands with a strong logo or typeface; product suites that need one visual thread; motion-heavy brands.
**Construction:** the device's geometry, its allowed transformations (fold, split, stack, orbit), how it hands off to
type and UI, where it never appears.
**Reduces:** the device itself is the reduced state.
**Fails when:** the device is forced into every image. It is a thread, not wallpaper.

## 8. Collage / mixed media

**What:** cut-out photography, scanned textures and graphic shapes combined.
**Who:** Atlassian (documented: collage reserved for marketing pages, never in product). Klarna's 2024 art direction
(documented direction: "magic from the mundane", built around photography and motion rather than illustration).
**Fits:** campaigns, editorial, social, brands with photographic equity.
**Construction:** cut-out rules (edge treatment, shadow or none), texture library, colour overlay rules, crop grid.
**Reduces:** not at all. Pair it with another family for product.
**Fails when:** it's used in product UI, or rights for photography are unclear.

## Combining families by touchpoint

Strong systems often assign families to tiers instead of forcing one look everywhere:

- Atlassian: flat spots (product states), low-fi UI (onboarding), ambient pattern (backgrounds), collage (marketing only).
- Mailchimp: mascot (brand warmth) + Cube device (product capability).
- Cash App: 2D editorial spots (in-app) + 3D library (marketing and features).

A direction may therefore be a **pairing**, such as "flat spots in product + 3D heroes in marketing", provided both
share tokens, an idea and at least one construction rule.

## Choosing families for the three directions

1. List the touchpoints and their tiers (`touchpoints.md`).
2. Score each family against the brand: tone (serious ↔ playful), production capacity (one designer ↔ agency and 3D
   team), smallest required size, motion ambition, existing equity (logo, typeface, mascot, photography).
3. Pick three directions that **differ in family** (or in family pairing). At most one of the three may be pattern-led,
   unless the user asked for pattern.
4. Each direction still needs an idea from the brand. A family alone is a style, not a direction.
