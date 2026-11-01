#!/usr/bin/env python3
"""Package the skill as a zip for upload (e.g. claude.ai → Settings → Capabilities → Skills).

  python tools/package_skill.py          # dist/brand-illustration-systems.zip
"""
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "brand-illustration-systems"
SKILL = os.path.join(ROOT, "skills", NAME)
DIST = os.path.join(ROOT, "dist")
SKIP = {"__pycache__", ".DS_Store"}


def main():
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, f"{NAME}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(SKILL):
            dirnames[:] = [d for d in dirnames if d not in SKIP]
            for fn in filenames:
                if fn in SKIP or fn.endswith(".pyc"):
                    continue
                full = os.path.join(dirpath, fn)
                z.write(full, os.path.join(NAME, os.path.relpath(full, SKILL)))
    print(f"{out}  {os.path.getsize(out) / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
