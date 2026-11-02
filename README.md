# Brand Illustration Systems: a skill for Claude and other AI agents

[![Tests](https://github.com/amenolabode/brand-illustration-skill/actions/workflows/test.yml/badge.svg)](https://github.com/amenolabode/brand-illustration-skill/actions/workflows/test.yml)

![Bedrock example: eight editorial objects built from one rule set](docs/images/03-story-covers.png)

An **Agent Skill** that turns Claude, or any agent that supports skills (Codex, Cursor, Gemini CLI, GitHub Copilot),
into a disciplined brand illustrator. Give it any brand and it maps where illustrations will live, finds ideas in the
brand's own assets, a source world or a cast of characters, and draws them in whichever **rendering family** fits:
flat, character-led, expressive line, soft 3D, pattern-led, technical, a brand device or collage.

- **Method:** intake that asks for your preferred direction first, then strategy with "X but not Y" tone fences, a
  **touchpoint map** (empty states, onboarding, success, errors, heroes) with emotional temperature, and three
  directions that differ in family, not just colour. The full system is built only after you pick.
- **Variety by design:** the three options must use different rendering families (unless you fix one, e.g. "line
  and energy like Monzo"), and at most one may be pattern-led. Lessons from Klarna, Monzo, Cash App, Revolut, Duolingo,
  Mailchimp, Atlassian, Robinhood, Dropbox and Cowrywise are distilled as principles, never as looks to copy.
- **Vector-first production:** spots, scenes, icons and motion generated from one set of tokens and construction
  rules. 3D comes as a scene kit plus renders. No raster "style samples" passed off as a system.
- **Dependency-free tools:** an audit that catches the failures that break illustration systems, a three-direction
  overview sheet, and a renderer so the agent looks at its own work.

**Contents:** [How it works](#how-it-works) · [Install](#install) · [Use](#use) · [Example](#example-bedrock) ·
[Rendering families](#rendering-families) · [What the audit catches](#what-the-audit-catches) · [What's inside](#whats-inside) · [Development](#development)

---

## How it works

```mermaid
flowchart LR
    A[Intake<br/>preferred direction?<br/>≤ 5 questions] --> B[Strategy<br/>tenet · tone fences]
    B --> T[Touchpoint map<br/>tiers · temperature ·<br/>2 proof moments]
    T --> C[Ideas × families<br/>brand assets · source world ·<br/>story or cast]
    C --> D[Three directions<br/>different families<br/>signature · spot · scene]
    D --> E{{Checkpoint<br/>overview sheet,<br/>recommend, stop}}
    E -- "you pick and say build" --> F[System by tier<br/>micro · spots · scenes ·<br/>hero · motion · spec]
    E -- "you want changes" --> C
```

**It asks before it assumes.** The first intake question is always *"Do you already have a direction in mind?"*:

| Your answer | What the three options become |
|---|---|
| **Yes, a style or brand**, e.g. "flat like Atlassian's spots", "3D like Cash App" | The family is fixed; three different ideas and signatures within it |
| **Yes, a source**, e.g. "Adire textiles" or "topographic maps" | Three **translations** of your source in different families. Alternatives are suggested in one line, never swapped in. |
| **Partly**: a feeling, references, things to avoid | Three families that respect your constraints |
| **No** | Three different families, at least one quiet (flat, technical) and one expressive (character, line, 3D) |

**It always stops at the checkpoint.** The three directions are presented on one overview sheet, with each
direction's signature element and the same product spot and scene in each so the comparison is fair, plus palette, meaning chain, motion verb,
an honest risk and a recommendation. Nothing else is built until you choose.

---

## Install

### Claude Code: plugin marketplace (recommended)
```
/plugin marketplace add amenolabode/brand-illustration-skill
/plugin install brand-illustration-systems@brand-illustration-skill
```

### Claude Code: manual
```bash
git clone https://github.com/amenolabode/brand-illustration-skill.git
cp -r brand-illustration-skill/skills/brand-illustration-systems ~/.claude/skills/        # personal
# or: cp -r brand-illustration-skill/skills/brand-illustration-systems .claude/skills/    # per project
```

### Claude.ai / Claude Desktop
Run `python3 tools/package_skill.py` (or download the zip from Releases) and upload
`dist/brand-illustration-systems.zip` under **Settings → Capabilities → Skills**.

### Codex, Cursor, Gemini CLI and other agents
The skill is a plain folder with a `SKILL.md`, so copy it into your agent's skills directory:

| Agent | Personal (all projects) | Per project |
|---|---|---|
| Codex CLI | `~/.codex/skills/brand-illustration-systems` | `.codex/skills/brand-illustration-systems` |
| Cursor | `~/.cursor/skills/brand-illustration-systems` | `.cursor/skills/brand-illustration-systems` |
| Gemini CLI | `~/.gemini/skills/brand-illustration-systems` | `.gemini/skills/brand-illustration-systems` |
| Shared across agents | `~/.agents/skills/brand-illustration-systems` | `.agents/skills/` + symlinks from each agent's folder |

To use one copy for every agent in a project, keep it in `.agents/skills/` and symlink the others to it:
```bash
for a in .claude .codex .cursor; do mkdir -p $a/skills && ln -s ../../.agents/skills/brand-illustration-systems $a/skills/; done
```
`agents/openai.yaml` supplies Codex's display metadata. `.claude-plugin/` is used only by Claude Code.

The skill works best with a model that can view images, because it renders its drafts to PNG and checks them before
showing you anything.

---

## Use

Just describe the brand. The skill picks itself up from its description:

> We're Bedrock, a savings app. Small, regular contributions become a durable foundation. We need an illustration
> system for the app and marketing.

> Make our illustrations from Adire textile patterns. We're a Lagos savings cooperative.

> We're Tally, a bill-splitting app. Flat and friendly, like Atlassian's spot illustrations.

> These are Cowrywise's illustrations. What inspired the patterns, and how would I rebuild them?

> Recreate this illustration, explain how you did it, then apply the direction to a laptop.

> Add a "Withdraw" icon and a "Pension" cover to our existing system (spec attached).

It works in five modes: **Design** (new system), **Reverse-engineer** (analyse a reference system), **Transfer**
(recreate one illustration and apply its direction to a new subject), **Extend** (new assets for an existing system)
and **Audit** (critique illustrations or a direction).

**Transfer** breaks a reference into seven layers (field, large shapes, palette roles, pattern owners, depth, reward
objects, rendering), then rebuilds it as vector and scores the rebuild against the reference with `match_score.py`,
measuring what doesn't match (ring centres, stripe periods, dot lattices, contour tapers) until the misses are craft
rather than missing rules. In the study behind this mode, the score went from 76.6% to 90.3% on figure pixels, and
every jump came from a rule the first description didn't have. The rules then become a kit
(`templates/flat_editorial_kit.py`), and three compositions of the new subject are built with it. Each element's
*role* is mapped onto the new subject. The striped jumper's role (the largest patterned curve) might go to a laptop's cable loop, and the
reference's props are replaced with props from the laptop's world rather than copied. A close recreation is treated as
a study, never a deliverable.

---

## Rendering families

| Family | Looks like | Studied in |
|---|---|---|
| Flat spot | Simple geometric shapes, one accent, product-sized | Atlassian spots, Klarna in-product, Duolingo |
| Character-led | A cast with fixed proportions and personalities | Duolingo, Monzo |
| Expressive line | Hand-drawn line, imperfect and human | Monzo, Cash App 2D, Dropbox |
| Soft 3D | Rendered materials, light, camera | Cash App Evergreen, Revolut |
| Pattern-led surface | Objects carry a source-world pattern | Cowrywise, Bedrock |
| Technical | Grids, notation, isometric construction | Robinhood |
| Brand device | One recurring shape or object carries the story | Mailchimp's Cube, Klarna's type-built shapes |
| Collage | Mixed photo, texture and drawing | Atlassian marketing |

Each has construction rules, the touchpoints it suits, how it reduces to small sizes and how it fails
(`references/style-families.md`). Families can pair by tier, e.g. flat spots in product and 3D heroes in marketing.

**Starter templates.** `templates/flat-spot-template.mjs` builds flat spots with a primitive-built character, in
celebratory, functional and sensitive moments, plus a phone-frame context render:

![Flat spot template: payment sent, empty state, card frozen, in a phone frame](docs/images/flat-spot-template.png)

`templates/build-template.mjs` builds a pattern-led system (the Bedrock example below).

**Why the families exist.** An early run for a brand called Scan produced three directions that were all a patterned
object on a coloured square. The skill had only one worked example, a pattern slot on its sheet and an audit that
warned when a pattern was missing. Those were all removed or made family-aware.

---

## Example: Bedrock (pattern-led)

A fictional savings brand, *"wealth is deposited layer by layer"*, built on sedimentary stratigraphy. The whole family
is generated by [`examples/bedrock/build.mjs`](examples/bedrock/build.mjs) from one palette, one 96×36 bedding tile
and three construction functions. Open [`examples/bedrock/index.html`](examples/bedrock/index.html) for the spec page.

**Technical scene:** isometric, wireframe → volume → material. The account rests on strata plates.
![Technical scene in three states](docs/images/01-technical-scene-states.png)

**Pictograms:** flat, generated at three tiers from one definition.
![Six pictograms at display, standard and micro sizes](docs/images/02-product-icons.png)

**How this skill was hardened.** The first Bedrock run used an image model. The meaning chain was right, but the
output had thick stripes over every shape, one clay material across all modes, five equal-weight colours, rendered
lighting, a crack in a different place on every object, and a GIF sliced from a storyboard. That run self-certified
because it checked its prompts, not its pixels. The spec page shows v1 and v2 side by side. Those failures became the
skill's rules, its red-flag list and `system_audit.py`.

---

## What the audit catches

`python3 scripts/system_audit.py --family flat|editorial|character|line|3d|pattern|technical|device|collage assets/*.svg`

The rules follow the family: a filter is a failure in a flat spot but fine in a 3D or collage asset.

| Family | Rasters | Filters | Gradients | Saturated hues |
|---|---|---|---|---|
| flat, technical, device, pattern | FAIL | FAIL | WARN | 1 |
| editorial (bold flat figurative) | FAIL | FAIL | one allowed, more WARN | 4 |
| character | FAIL | WARN | WARN | 2 |
| line | WARN | WARN | allowed | 2 |
| 3d / collage | allowed | allowed | allowed | 2 / 3 |

Every family: live `<text>` warns, and any `<pattern>` whose lines read as bands or contrast too strongly warns.
Only the pattern family warns when there is no pattern.

Two more checks:

- `render_png.py --silhouette` renders every shape black with the background removed (the large-shape test), and
  `--grey` renders it in greyscale.
- `raster_check.py image.png` checks image-model exploration for what flat styles depend on. It FAILs a background
  with a glow, vignette or gradient, WARNs one that is noisy rather than one solid fill, and lists the dominant
  colours. It also WARNs when the PNG carries a non-sRGB colour profile, because hexes sampled from it are wrong.
- `match_score.py recreation.svg reference.png` scores a vector rebuild against its reference: agreement, IoU per
  colour, the worst regions and a diff image.

---

## What's inside

```
skills/brand-illustration-systems/
├── SKILL.md                         workflow, checkpoint, chat format, red flags
├── agents/openai.yaml               Codex display metadata
├── references/
│   ├── intake.md                    the preferred-direction question, brief questions, assumptions
│   ├── touchpoints.md               inventory, tiers, emotional temperature, proof moments
│   ├── style-families.md            the eight rendering families
│   ├── reference-systems.md         case notes on Klarna, Monzo, Cash App, Revolut, Duolingo and others
│   ├── direction-options.md         making three options truly different; sheet spec
│   ├── research-and-translation.md  source research, scorecard, worksheet, reference analysis
│   ├── reference-transfer.md        recreate one illustration and apply it to a new subject
│   ├── system-spec-and-validation.md  production spec, proof matrix, failure diagnoses
│   ├── production-prompts.md        production route per family, exploration-only prompts, known failures
│   └── cowrywise-example.md         a full analysis of one pattern-led reference system
├── scripts/
│   ├── direction_sheet.py           three-option overview sheet (HTML) from JSON
│   ├── system_audit.py              family-aware audit for SVGs
│   ├── raster_check.py              flat-field and palette check for raster exploration
│   ├── render_png.py                SVG/HTML → PNG (Chrome, rsvg-convert, cairosvg, Inkscape); silhouette, grey
│   └── match_score.py               score a vector recreation against its reference (Transfer)
└── templates/
    ├── flat-spot-template.mjs       flat spots + primitive character + phone-frame context
    ├── build-template.mjs           pattern-led: tokens → pattern → per-mode construction → motion
    └── flat_editorial_kit.py        flat editorial grammar: stripes, radial rings, dot ribbons, contours, overlaps
examples/bedrock/                    complete worked run with spec page
evals/evals.json                     behaviour evals (intake, varied families, fixed family, translations, build, analysis, transfer)
tools/                               smoke test and packaging
tests/                               unit tests
```

---

## Development

```bash
python3 tools/smoke_test.py                  # runs every script the way an agent does
python3 -m unittest discover -s tests -v     # audit logic and SKILL.md contract
python3 tools/package_skill.py               # dist/brand-illustration-systems.zip
```

CI runs both on Linux, macOS and Windows. Contributions are welcome: new reference analyses, rendering families, templates,
audit checks and worked examples, especially from non-Western source worlds, with provenance documented.

## License

[MIT](LICENSE). Brand names in the reference analyses belong to their owners and are discussed for study only.
