"""Unit tests for the skill's scripts and its SKILL.md contract. Run: python -m unittest discover -s tests -v"""
import importlib.util
import os
import re
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "brand-illustration-systems")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKILL, "scripts", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit = load("system_audit")
raster = load("raster_check")
render = load("render_png")


def svg(body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><defs>{defs}</defs>{body}</svg>'


class AuditTests(unittest.TestCase):
    def check(self, text, family="flat"):
        with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
            f.write(text)
        try:
            return audit.audit(f.name, family=family)
        finally:
            os.unlink(f.name)

    def test_raster_fails(self):
        r = self.check(svg('<image href="data:image/png;base64,AAAA" width="10" height="10"/>'))
        self.assertTrue(any("raster" in m for m in r["fail"]))

    def test_drop_shadow_fails(self):
        r = self.check(svg('<rect width="9" height="9" filter="url(#f)"/>', '<filter id="f"><feDropShadow/></filter>'))
        self.assertTrue(any("filter" in m for m in r["fail"]))

    def test_one_anchor_ok_three_warn(self):
        one = self.check(svg('<rect width="9" height="9" fill="#E2531F"/><rect width="9" height="9" fill="#F7E6C4"/>'))
        self.assertFalse(any("saturated" in m for m in one["warn"]))
        three = self.check(svg('<rect fill="#E2531F"/><rect fill="#1F7AE0"/><rect fill="#2DB34A"/>'))
        self.assertTrue(any("3 saturated hues" in m for m in three["warn"]))

    def test_heavy_and_contrasty_pattern_warns(self):
        p = ('<pattern id="p" width="24" height="12"><rect width="24" height="12" fill="#F7E6C4"/>'
             '<path d="M0 6H24" stroke="#2B2236" stroke-width="6"/></pattern>')
        r = self.check(svg('<rect width="96" height="96" fill="url(#p)"/>', p))
        self.assertTrue(any("reads as bands" in m for m in r["warn"]))
        self.assertTrue(any("contrast" in m for m in r["warn"]))

    def test_fine_tonal_pattern_passes(self):
        p = ('<pattern id="p" width="96" height="36"><rect width="96" height="36" fill="#F7E6C4"/>'
             + "".join(f'<path d="M0 {y}H96" stroke="#E2BF83" stroke-width="1.1"/>' for y in (5, 12, 21, 30))
             + "</pattern>")
        r = self.check(svg('<rect width="96" height="96" fill="url(#p)"/><rect fill="#E2531F"/>', p))
        self.assertEqual(r["fail"], [])
        self.assertEqual(r["warn"], [])

    def test_family_profiles(self):
        grad = svg('<rect width="9" height="9" fill="url(#g)"/>',
                   '<linearGradient id="g"><stop stop-color="#fff"/><stop offset="1" stop-color="#ccc"/></linearGradient>')
        self.assertTrue(any("gradient" in m for m in self.check(grad, "flat")["warn"]))
        self.assertFalse(any("gradient" in m for m in self.check(grad, "3d")["warn"] + self.check(grad, "3d")["fail"]))
        two = svg('<rect fill="#E2531F"/><rect fill="#1F7AE0"/>')
        self.assertTrue(any("saturated" in m for m in self.check(two, "flat")["warn"]))
        self.assertFalse(any("saturated" in m for m in self.check(two, "character")["warn"]))

    def test_missing_pattern_only_matters_for_pattern_family(self):
        plain = svg('<rect width="9" height="9" fill="#E2531F"/>')
        self.assertFalse(any("pattern" in m for m in self.check(plain, "flat")["warn"]))
        self.assertTrue(any("pattern" in m for m in self.check(plain, "pattern")["warn"]))

    def test_contrast_maths(self):
        self.assertAlmostEqual(audit.contrast("#000000", "#FFFFFF"), 21.0, places=1)


class RasterCheckTests(unittest.TestCase):
    def png(self, color, w=60, h=60):
        import struct
        import zlib
        raw = b"".join(b"\x00" + bytes(v for x in range(w) for v in color(x, y)) for y in range(h))
        chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
        f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_solid_field_passes(self):
        r = raster.check(self.png(lambda x, y: (0, 0, 0) if 20 < x < 40 and 20 < y < 40 else (250, 240, 140)))
        self.assertEqual(r["fail"] + r["warn"], [])

    def test_gradient_field_fails(self):
        r = raster.check(self.png(lambda x, y: (250, 220 + x // 3, 140)))
        self.assertTrue(any("glow" in m for m in r["fail"]))

    def test_noisy_field_warns(self):
        r = raster.check(self.png(lambda x, y: (250, 240 + (x * 7 + y * 13) % 5, 140)))
        self.assertTrue(any("not one solid colour" in m for m in r["warn"]))


class RenderHelperTests(unittest.TestCase):
    def test_strip_field_removes_only_full_canvas_rects(self):
        txt = '<rect width="100" height="80" fill="#fff"/><rect x="5" width="100" height="80"/><rect width="10" height="10"/>'
        out = render.strip_field(txt, 100, 80)
        self.assertNotIn('fill="#fff"', out)
        self.assertIn('x="5"', out)
        self.assertIn('width="10"', out)


class SkillContractTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
            self.text = f.read()

    def test_frontmatter(self):
        m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", self.text, re.S)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "brand-illustration-systems")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_project_first_intake_and_three_directions(self):
        self.assertIn("What is the brand or project", self.text)
        self.assertLess(self.text.index("What is the brand or project"), self.text.index("style, source, reference"))
        self.assertIn("three directions", self.text.lower())
        self.assertIn("checkpoint", self.text.lower())

    def test_constructive_method_is_part_of_contract(self):
        low = self.text.lower()
        for step in ("model the subject", "compose the action", "build the skeleton", "block the masses",
                     "add volume and depth", "apply brand grammar", "reduce and verify"):
            self.assertIn(step, low)
        with open(os.path.join(SKILL, "references", "constructive-illustration.md"), encoding="utf-8") as f:
            construction = f.read().lower()
        for concept in ("contacts", "human riding a bicycle", "silhouette", "pattern-led"):
            self.assertIn(concept, construction)

    def test_references_do_not_determine_outcome(self):
        low = self.text.lower()
        self.assertIn("references are evidence, not recipes", low)
        self.assertIn("do not inherit props, composition, palette, metaphor", low)

    def test_design_research_is_isolated_from_examples(self):
        low = self.text.lower()
        self.assertIn("example-isolation contract", low)
        self.assertIn("generate the metaphor longlist before selecting a rendering family", low)
        self.assertIn("project fact → shared behaviour → candidate source", low)
        with open(os.path.join(SKILL, "references", "research-and-translation.md"), encoding="utf-8") as f:
            research = f.read().lower()
        self.assertIn("start closed-book", research)
        self.assertIn("research the source itself", research)
        self.assertIn("pattern is one possible output, not the goal", research)
        self.assertFalse(os.path.exists(os.path.join(SKILL, "references", "security-print-example.md")))
        self.assertFalse(os.path.exists(os.path.join(SKILL, "templates", "build-template.mjs")))
        self.assertFalse(os.path.exists(os.path.join(SKILL, "templates", "flat-spot-template.mjs")))
        self.assertFalse(os.path.exists(os.path.join(SKILL, "templates", "flat_editorial_kit.py")))
        with open(os.path.join(SKILL, "references", "reference-transfer.md"), encoding="utf-8") as f:
            transfer = f.read().lower()
        self.assertIn("new project-local kit", transfer)
        self.assertIn("do not begin from a previous reference's kit", transfer)

    def test_directions_vary_family(self):
        low = self.text.lower()
        self.assertIn("rendering family", low)
        self.assertRegex(low, r"at most one\s+may be pattern-led")
        with open(os.path.join(SKILL, "references", "style-families.md"), encoding="utf-8") as f:
            fam = f.read().lower()
        for name in ("flat", "character", "line", "3d", "pattern", "technical", "device", "collage"):
            self.assertIn(name, fam)

    def test_referenced_files_exist(self):
        for rel in set(re.findall(r"`((?:references|scripts|templates)/[\w./-]+)`", self.text)):
            self.assertTrue(os.path.exists(os.path.join(SKILL, rel)), rel)


if __name__ == "__main__":
    unittest.main()
