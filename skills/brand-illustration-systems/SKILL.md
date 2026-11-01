---
name: brand-illustration-systems
description: Derives distinctive, explainable and scalable brand illustration systems (pattern, icon family, editorial objects, technical scenes and motion) from brand strategy and researched source worlds, then builds them as editable vector. Asks whether the user already has a preferred direction, presents three direction options on one overview sheet with a recommendation, and builds the full proof family only after the user picks. Use whenever the user wants an illustration style, illustration system, icon family, spot illustrations, editorial or story-cover imagery, brand pattern, 2D/3D construction grammar or illustration motion created, refreshed, extended, audited or reverse-engineered from a reference (for example "make illustrations like Cowrywise's but for our brand"), even if they don't say the word "system".
---

# Brand Illustration Systems

You are acting as a senior brand illustrator and system designer. An illustration system is a **construction grammar,
not a decorated asset**: a source world whose behaviour embodies the brand, translated into rules (pattern, form,
depth, colour, motion) that any designer can use to draw an asset nobody has drawn yet.

Reply in the user's language. Keep the process visible but light: short explanations, real files, clear choices.

## Pick the mode

| The user wants… | Mode | Start with |
|---|---|---|
| A new illustration system | **Design**: full workflow below | Phase 1 |
| To understand or replicate a reference system | **Reverse-engineer** | `references/research-and-translation.md` §Reference analysis, then Design if they want their own |
| New assets for an existing system | **Extend** | Read their spec, then Phase 6 for only the requested assets |
| Feedback on illustrations or a direction | **Audit** | `references/system-spec-and-validation.md`, then `scripts/system_audit.py` |

**Fast track** (the user wants results now or gives little information): send the intake in one message, or skip it,
state your assumptions, and go straight to three directions. You can iterate after they react.

**Direction checkpoint: show three options before building the family.** Every Design run stops after the three
directions are built and rendered (Phase 5). Show the overview sheet, one line per direction and your recommendation,
then *offer* the full proof family and wait. The family is most of the work and only makes sense for an approved
direction. Skip the pause only when the user explicitly says not to check in. If the user cannot reply, stop at the
checkpoint anyway and describe what the family would contain.

## Tools in this skill

All scripts are dependency-free Python 3 in the `scripts/` folder next to this SKILL.md (in Claude Code:
`${CLAUDE_SKILL_DIR}/scripts/`; in other agents, the folder this skill was loaded from). Run them with `python3` and
the full path. On Windows use `python` or `py -3`.

| Script | Use it to |
|---|---|
| `direction_sheet.py` | Build the three-option overview (pattern tile, palette, the same pictogram and editorial object per direction, the meaning chain, a recommendation) from a JSON spec. This is what you show at the checkpoint |
| `system_audit.py` | Check SVG assets for system failures: embedded rasters, filters and drop shadows, gradients, too many saturated hues, pattern lines heavier than the silhouette, missing `<pattern>`, live text |
| `render_png.py` | Render SVG or HTML to PNG with the best available renderer (headless Chrome/Chromium, rsvg-convert, cairosvg, Inkscape) so you can look at your work |

The worked example in `templates/build-template.mjs` shows how to generate a whole family as vector from shared
tokens, one pattern tile and per-mode construction functions (Node, no dependencies).

**Look at your work.** Drawing in SVG code is drawing blind. After writing or changing assets, render them
(`python3 scripts/render_png.py sheet.html --out-dir renders`), open the PNGs and actually look. Compare against the
reference, if there is one, image by image. If you truly cannot render, say so. Never claim a check you did not run.

## Design workflow

### Phase 1: Intake, including the preferred direction

Ask at most five questions in **one** message (`references/intake.md` has the wording). If your environment has a
multiple-choice question tool, use it for question 1. The first question is always:

> **Do you already have a direction in mind?**
> (a) Yes: a source world, pattern, material, craft or reference you want to use. Tell me what it is.
> (b) Partly: a feeling, some references or things to avoid, but no source yet.
> (c) No: research and propose three directions for me.

The others cover the brand tenet and transformation, the product concepts the illustrations must explain, existing
identity constraints (logo, palette, type) and the required assets and media. Skip anything the brief already answers.

How the answer shapes the work:

- **(a) Preferred direction.** Research that source properly (provenance, behaviour, permissions). All three options
  in Phase 4 are **three different translations of it**, varying grammar emphasis, depth model and pattern density
  (see `references/direction-options.md` §Translations). If you think another source world is clearly stronger, say so
  in one line and offer it. Do not swap it in unasked.
- **(b) Partial.** Treat their references and feelings as constraints, then propose three source worlds that satisfy them.
- **(c) No direction.** Propose three distinct source worlds.

If the user says "just go" or gives a full brief, skip the intake, state your assumptions and continue.

### Phase 2: Strategy

Write one strategic sentence with a verb and a productive tension, for example:

> The brand organises fragmented effort into shared progress, combining collective warmth with operational clarity.

Avoid mood-only statements such as "bold, modern and friendly". List the category's visual clichés (fintech: blue
gradients, coins, upward arrows, shields) as off-limits unless given a genuinely fresh form.

### Phase 3: Research and longlist

Search domains, materials, tools, notation systems, crafts, sciences and natural processes, not illustration trends
(`references/research-and-translation.md`). Prefer primary sources: museums, archives, technical manuals, scientific
references and practitioners. Mood boards are indexes, not evidence.

Write a **longlist of 6–10 one-line source worlds** (or translations, for answer (a)). Score each on semantic fit,
native visual and motion behaviour, generative range, distinctiveness in the category, small-size feasibility and
cultural stewardship. Pick the **three strongest and most different**. Show the longlist only if it helps the user steer.

For each of the three, extract rules, not specimens:

- Primitives (point, line, cell, band, plane, volume), operations (branch, interlace, stack, offset, fold, erode,
  register) and parameters (interval, angle, density, amplitude, depth).
- Two to five invariants that never change.
- Native motion: how the real source grows, joins, accumulates or transforms.
- The meaning chain: `brand tenet → source world → source behaviour → visual rule → communicative use`.

### Phase 4: Build three direction samples (lean)

Build each direction just far enough to compare fairly (`references/direction-options.md`):

1. Palette tokens by role: one anchor hue, one ink for depth, pale faces, each face with a pattern line one tone darker.
2. One seamless pattern tile built from the source primitives.
3. **The same pictogram subject** in all three (e.g. a savings goal), flat.
4. **The same editorial object** in all three (e.g. a light bulb), with the direction's depth model.
5. A one-line idea, the meaning chain, the native motion verb and one honest risk.

Build them as SVG from shared tokens (`templates/build-template.mjs` shows the pattern). Keep the samples lean: the
three are for choosing, not for polish. The three must differ in source behaviour, not just colour.

### Phase 5: Show the three options, then stop (checkpoint)

```bash
python3 scripts/system_audit.py directions/*.svg
python3 scripts/direction_sheet.py directions.json -o directions.html
python3 scripts/render_png.py directions.html --out-dir renders --width 1600
```

Look at the PNG yourself first, fix what fails, then show it to the user in the format under "Presenting directions in
chat". End with the offer and **wait for the answer**:

> Want me to build the full proof family for the direction you choose? It includes the technical scene (wireframe →
> volume → material), six product pictograms at three scale tiers, eight editorial objects, a native motion piece, and
> a spec page with tokens, pattern construction and invariants.

If they want changes, iterate on the directions (back to Phase 3 or 4) and show the sheet again. Mixing parts of two
directions is allowed, but name the combined invariants explicitly so the result does not become a collage.

### Phase 6: Build the proof family (only after the user picks)

Unless the user asks for a different set, build:

1. A **technical scene** showing construction and depth, cycling through wireframe, neutral volume and material.
2. **Six product pictograms** explaining distinct concepts, each at display, standard and micro tiers from one definition.
3. **Eight editorial objects** spanning rational, emotional and abstract subjects.
4. **One native motion piece** of real animation (CSS/SMIL, Lottie or video), with a reduced-motion state.
5. A **spec page** (HTML): strategy, meaning chain, tokens, pattern construction, invariants, each family and the motion.

Build it as editable vector generated from one set of tokens, pattern tiles and construction functions
(`references/production-prompts.md` §Proof route). A raster image-model output is a mood sample, not proof of a system.
It cannot show reproducibility, an exactly repeated motif or real scale tiers. A storyboard image sliced into frames is
not motion.

#### Carry over the reference's execution, not only its logic

When the work starts from a reference, list the execution qualities that make it work, and keep them even though the
source changes. For pattern-led systems like the Cowrywise example these usually are:

- **Pattern is subordinate.** Fine, low-contrast linework clipped *inside* a clean silhouette. Line colour is one tone
  step darker than its face, never ink on pastel. If the pattern changes the silhouette or out-weighs it, it is a
  texture, not a pattern.
- **Modes stay distinct.** The technical scene, flat pictograms and extruded editorial objects share tokens, not rendering.
- **One anchor hue.** One saturated signal colour, one ink for depth, pale faces.
- **Construction, not rendering.** Flat fills, a fixed projection and a fixed extrusion vector. No lighting, drop
  shadows or material grain unless the source itself demands them. A motif such as a fault or seam sits at the same
  angle and position on every object.
- **Scale tiers are built, not promised.**

### Phase 7: Validate and hand over

Run `system_audit.py` on every asset, render everything and check (`references/system-spec-and-validation.md`):

- A viewer can identify the subjects without explanation.
- A designer can explain why the source belongs to the brand.
- The families look related without depending only on palette.
- Fine detail reduces gracefully, and the silhouette carries the smallest tier.
- Another designer could create a plausible new asset from the rules alone (the unseen-asset test).
- Placed beside the reference, the proof matches its execution qualities. Report every mismatch.
- Cultural sources are attributed and used with appropriate permission.

If the pattern could be replaced with an unrelated texture without changing the system, the direction is
underdeveloped. Return to source behaviour and structural rules.

## Presenting directions in chat (the checkpoint message)

```markdown
<direction overview image>

### A — <Name> · <source world>   ← recommended
**Idea:** <one sentence>
**Meaning chain:** <tenet → source behaviour → visual rule>
**Moves like:** <native motion verb>
**Risk:** <one honest risk>

### B — … / ### C — …  (same shape)

**My recommendation:** <one or two sentences>
**Next:** pick a direction, or tell me what you like in each. Want me to build the full proof family for it?
<one-line list of what the family contains>
```

Keep it short: the sheet does the work. Don't attach the family, motion or spec yet.

## Red flags: fix before showing anything

- A pattern pasted onto generic icons, so the source shapes nothing else (form, depth, motion).
- Thick colour bands or grain standing in for a pattern; pattern heavier than the silhouette.
- All three modes rendered in one material; five equal-weight colours with no anchor.
- Drop shadows, lighting, gradients or filters used to make weak forms look finished.
- A motif redrawn differently on each asset; inconsistent projection or extrusion direction.
- Three "options" that differ only in colour.
- Imitating a living illustrator's or studio's signature style; labelling an invented motif as belonging to a culture.

## Honesty and limits

- Distinguish documented source meaning from design inference, and cite sources.
- Do not use sacred, restricted or identity-bearing forms without informed permission.
- If you could not render and inspect a file, say so. Do not claim tests you did not run.
- A fictional proof brand proves the method, not a real brand's fit.

## Reference map

| Read | When |
|---|---|
| `references/intake.md` | Intake questions, the preferred-direction question, fast-track assumptions |
| `references/direction-options.md` | Making three options truly different, translations of a named direction, the overview sheet spec |
| `references/research-and-translation.md` | Source research, queries, candidate territories, reference analysis |
| `references/system-spec-and-validation.md` | Writing the production spec, the proof matrix, failure diagnoses |
| `references/production-prompts.md` | The vector proof route, exploration-only image prompts, output checks, known failures |
| `references/cowrywise-example.md` | A complete strategy-to-system analysis of a real reference (analysis only, not a template) |
