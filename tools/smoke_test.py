#!/usr/bin/env python3
"""Smoke-test every script in the skill the way an agent runs them (used by CI on Windows, macOS and Linux).

  python tools/smoke_test.py      # PNG rendering and the Node template run only when Chrome / Node are available

Each script runs in a subprocess with the platform's default console encoding, so crashes such as
UnicodeEncodeError are caught. Standard library only.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "brand-illustration-systems")
SCRIPTS = os.path.join(SKILL, "scripts")
EXAMPLE = os.path.join(ROOT, "examples", "bedrock")

GOOD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">
<defs><pattern id="p" patternUnits="userSpaceOnUse" width="24" height="12">
<rect width="24" height="12" fill="#F7E6C4"/><path d="M0 6H24" stroke="#E2BF83" stroke-width="1"/></pattern></defs>
<rect x="10" y="20" width="70" height="68" rx="7" fill="url(#p)"/>
<rect x="18" y="10" width="70" height="68" rx="7" fill="#E2531F"/></svg>
"""
BAD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">
<defs><filter id="s"><feDropShadow dx="2" dy="2" stdDeviation="2"/></filter>
<pattern id="p" patternUnits="userSpaceOnUse" width="24" height="12">
<rect width="24" height="12" fill="#F7E6C4"/><path d="M0 6H24" stroke="#2B2236" stroke-width="6"/></pattern></defs>
<rect width="96" height="96" fill="url(#p)" filter="url(#s)"/>
<circle cx="20" cy="20" r="8" fill="#E2531F"/><circle cx="50" cy="20" r="8" fill="#1F7AE0"/>
<circle cx="80" cy="20" r="8" fill="#2DB34A"/></svg>
"""

failures = []


def run(name, args, expect=(), code=0, cwd=None):
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    p = subprocess.run(args, cwd=cwd or ROOT, env=env, capture_output=True)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    problems = []
    if p.returncode != code:
        problems.append(f"exit code {p.returncode}, expected {code}")
    if "Traceback (most recent call last)" in out:
        problems.append("traceback")
    for e in expect:
        if os.path.isabs(e):
            if not os.path.exists(e):
                problems.append(f"missing file {e}")
        elif e not in out:
            problems.append(f"output lacks {e!r}")
    print(f"[{'ok  ' if not problems else 'FAIL'}] {name}")
    if problems:
        failures.append(name)
        print("       " + "; ".join(problems))
        print("       " + out.strip().replace("\n", "\n       ")[-2000:])
    return out


def py(script, *args):
    return [sys.executable, os.path.join(SCRIPTS, script), *args]


def main():
    tmp = tempfile.mkdtemp(prefix="bis-smoke-")
    good, bad = os.path.join(tmp, "good.svg"), os.path.join(tmp, "bad.svg")
    for path, txt in ((good, GOOD), (bad, BAD)):
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)

    run("audit: clean asset passes", py("system_audit.py", good), ["[PASS]"])
    run("audit: v1-style asset fails", py("system_audit.py", bad),
        ["[FAIL]", "filter found", "saturated hues", "reads as bands", "contrast"], code=1)
    run("audit: json output", py("system_audit.py", good, "--json"), ['"file"'])
    run("audit: bedrock example has no failures", py("system_audit.py", *[
        os.path.join(EXAMPLE, f) for f in sorted(os.listdir(EXAMPLE)) if f.endswith(".svg")]))

    spec = {
        "brand": "Smoke", "tenet": "Testing — with non-ASCII “quotes”.", "recommend": 1,
        "directions": [
            {"name": n, "source": "Test source", "idea": "One idea.", "chain": "a → b → c", "motion": "settle",
             "risk": "None.", "palette": ["#E2531F", "#2B2236", "#F7E6C4"],
             "pattern": "good.svg", "pictogram": "good.svg", "object": "good.svg"}
            for n in ("Alpha", "Beta", "Gamma")
        ],
    }
    spec_path = os.path.join(tmp, "directions.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False)
    sheet = os.path.join(tmp, "directions.html")
    run("direction sheet", py("direction_sheet.py", spec_path, "-o", sheet), ["3 directions", sheet])
    bad_spec = os.path.join(tmp, "bad.json")
    with open(bad_spec, "w", encoding="utf-8") as f:
        json.dump({"directions": spec["directions"][:1]}, f)
    run("direction sheet rejects one direction", py("direction_sheet.py", bad_spec, "-o", sheet), ["expected 2-4"], code=1)

    which = run("render: list renderers", py("render_png.py", "--which"))
    if "chrome" in which:
        run("render: html sheet", py("render_png.py", sheet, "--out-dir", tmp, "--width", "1400"),
            [os.path.join(tmp, "directions.png")])
    if any(r in which for r in ("chrome", "rsvg-convert", "cairosvg", "inkscape")):
        run("render: svg", py("render_png.py", good, "--out-dir", tmp, "--width", "256"), [os.path.join(tmp, "good.png")])
    else:
        print("[skip] render: no renderer on this machine")

    node = shutil.which("node")
    if node:
        out_dir = os.path.join(tmp, "template")
        run("template: node build", [node, os.path.join(SKILL, "templates", "build-template.mjs"), out_dir],
            [os.path.join(out_dir, "03-story-covers.svg")])
        run("template: output passes audit", py("system_audit.py", os.path.join(out_dir, "03-story-covers.svg")), ["[PASS]"])
    else:
        print("[skip] template: node not installed")

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(failures)} failure(s)" if failures else "\nall smoke tests passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
