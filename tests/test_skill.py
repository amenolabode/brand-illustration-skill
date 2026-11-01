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


def svg(body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><defs>{defs}</defs>{body}</svg>'


class AuditTests(unittest.TestCase):
    def check(self, text):
        with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
            f.write(text)
        try:
            return audit.audit(f.name)
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

    def test_contrast_maths(self):
        self.assertAlmostEqual(audit.contrast("#000000", "#FFFFFF"), 21.0, places=1)


class SkillContractTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
            self.text = f.read()

    def test_frontmatter(self):
        m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", self.text, re.S)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "brand-illustration-systems")
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_asks_for_preferred_direction_and_shows_three(self):
        self.assertIn("Do you already have a direction in mind?", self.text)
        self.assertIn("three directions", self.text.lower())
        self.assertIn("checkpoint", self.text.lower())

    def test_referenced_files_exist(self):
        for rel in set(re.findall(r"`((?:references|scripts|templates)/[\w./-]+)`", self.text)):
            self.assertTrue(os.path.exists(os.path.join(SKILL, rel)), rel)


if __name__ == "__main__":
    unittest.main()
