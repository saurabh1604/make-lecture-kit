#!/usr/bin/env python3
"""selfcheck.py — one-command health check for make-lecture-kit.

Run this after ANY change to confirm the kit still works, on any platform:

    python3 scripts/selfcheck.py

It verifies: required files present, every script compiles, the shared word-list
module imports, figstyle renders, both linters run and the bundled example passes,
and VERSION is recorded in CHANGELOG. Exit code is non-zero if any hard check FAILs.

Pure standard library + subprocess. No network, no third-party deps. This is the
safety net that lets you keep upgrading the kit fearlessly (see
references/upgrading.md).
"""

import ast
import glob
import importlib.util
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # kit root


def kp(*parts):
    return os.path.join(ROOT, *parts)


class Report:
    def __init__(self):
        self.rows = []
        self.counts = {"PASS": 0, "WARN": 0, "FAIL": 0}

    def add(self, level, name, msg=""):
        self.rows.append((level, name, msg))
        self.counts[level] += 1

    def __getattr__(self, _):
        raise AttributeError

    def passed(self, n, m=""): self.add("PASS", n, m)
    def warned(self, n, m=""): self.add("WARN", n, m)
    def failed(self, n, m=""): self.add("FAIL", n, m)

    def print_all(self):
        g = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}
        for level, name, msg in self.rows:
            print(f"{g[level]} {name}")
            if msg:
                for line in str(msg).splitlines():
                    print(f"         {line}")

    @property
    def has_fail(self):
        return self.counts["FAIL"] > 0


REQUIRED = [
    "SKILL.md", "AGENTS.md", "README.md", "START_HERE.md", "VERSION",
    "CHANGELOG.md",
    "references/plain_language.md", "references/companion_style.md",
    "references/lecture_style.md", "references/intuition_playbook.md",
    "references/quality_rubric.md", "references/prompts.md",
    "references/upgrading.md",
    "templates/companion.tex", "templates/lecture.html",
    "scripts/figstyle.py", "scripts/build_pdf.py", "scripts/lint.py",
    "scripts/lint_tex.py", "scripts/_plain_language.py", "scripts/selfcheck.py",
    "scripts/update.py", "update_source.txt",
    "examples/sample_companion.tex",
]


def check_structure(r):
    missing = [f for f in REQUIRED if not os.path.isfile(kp(*f.split("/")))]
    if missing:
        r.failed("structure", "missing file(s): " + ", ".join(missing))
    else:
        r.passed("structure", f"all {len(REQUIRED)} required files present")


def check_compiles(r):
    bad = []
    for f in sorted(glob.glob(kp("scripts", "*.py"))):
        try:
            ast.parse(open(f, encoding="utf-8").read())
        except SyntaxError as exc:
            bad.append(f"{os.path.basename(f)}: {exc}")
    if bad:
        r.failed("python compiles", "\n".join(bad))
    else:
        r.passed("python compiles", "every script in scripts/ parses")


def check_shared_module(r):
    try:
        sys.path.insert(0, kp("scripts"))
        import _plain_language as pl  # noqa
        ok = (hasattr(pl, "FANCY_WORDS") and hasattr(pl, "HANDWAVE_PHRASES")
              and callable(getattr(pl, "flesch_reading_ease", None)))
        if ok:
            r.passed("shared word lists",
                     f"_plain_language OK ({len(pl.FANCY_WORDS)} word swaps, "
                     f"ceiling {pl.WORD_CEILING})")
        else:
            r.failed("shared word lists", "_plain_language missing expected members")
    except Exception as exc:  # noqa: BLE001
        r.failed("shared word lists", f"import failed: {exc}")


def check_figstyle(r):
    if importlib.util.find_spec("matplotlib") is None:
        r.warned("figstyle render",
                 "matplotlib not installed here; skipped (present in agent "
                 "sandboxes). Figures will render where TeX/matplotlib exist.")
        return
    with tempfile.TemporaryDirectory() as td:
        res = subprocess.run([sys.executable, kp("scripts", "figstyle.py"), td],
                             capture_output=True, text=True, timeout=180)
        pngs = glob.glob(os.path.join(td, "*.png"))
        if res.returncode == 0 and pngs:
            r.passed("figstyle render", f"{len(pngs)} demo plot(s) rendered cleanly")
        else:
            tail = (res.stderr or res.stdout or "no output").strip()[-240:]
            r.failed("figstyle render", "figstyle self-test failed:\n" + tail)


def _run(script, target):
    return subprocess.run(
        [sys.executable, kp("scripts", script), kp(*target.split("/"))],
        capture_output=True, text=True, timeout=180)


def check_linters(r):
    # lint_tex on the bundled example — it is the quality bar, so it must PASS.
    res = _run("lint_tex.py", "examples/sample_companion.tex")
    last = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else ""
    if "Result: PASS" in res.stdout:
        r.passed("lint_tex (example)", last or "example passes")
    else:
        r.failed("lint_tex (example)",
                 "the bundled example must pass lint_tex:\n" + res.stdout[-300:])

    # lint.py just needs to RUN and produce a report (the only bundled HTML is the
    # template, which intentionally carries scaffold placeholders).
    res = _run("lint.py", "templates/lecture.html")
    if "Summary:" in res.stdout:
        r.passed("lint.py (runs)",
                 "HTML linter executes and reports "
                 "(template carries scaffold placeholders by design)")
    else:
        r.failed("lint.py (runs)", "HTML linter did not produce a report")


def check_version(r):
    try:
        ver = open(kp("VERSION"), encoding="utf-8").read().strip()
    except OSError:
        r.failed("version", "VERSION file missing")
        return
    chg = ""
    if os.path.isfile(kp("CHANGELOG.md")):
        chg = open(kp("CHANGELOG.md"), encoding="utf-8").read()
    if ver and ver in chg:
        r.passed("version", f"VERSION {ver} is recorded in CHANGELOG.md")
    elif ver:
        r.warned("version", f"VERSION {ver} not found in CHANGELOG.md — add an entry")
    else:
        r.failed("version", "VERSION file is empty")


def main():
    print("=" * 68)
    print(f"make-lecture-kit self-check  ({ROOT})")
    print("=" * 68)
    r = Report()
    check_structure(r)
    check_compiles(r)
    check_shared_module(r)
    check_figstyle(r)
    check_linters(r)
    check_version(r)
    r.print_all()
    print("-" * 68)
    c = r.counts
    print(f"Summary: {c['PASS']} PASS, {c['WARN']} WARN, {c['FAIL']} FAIL")
    if r.has_fail:
        print("Result: FAIL — fix the items above before shipping/upgrading.")
        return 1
    if c["WARN"]:
        print("Result: PASS WITH WARNINGS — kit is healthy.")
        return 0
    print("Result: PASS — kit is healthy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
