#!/usr/bin/env python3
"""Coverage gate — checks a generated kit against its own concept manifest.

The rubric's own ship checklist admits coverage (every concept present, nothing
dropped) is the check most likely to fail, yet nothing used to verify it except
a manual eyeball sweep. This script is that automation: it compares the
`concepts.json` manifest an agent writes during step 2 of SKILL.md against the
sections and worked examples actually shipped in `companion.tex` and/or
`lecture.html`.

IMPORTANT — what this does NOT do: it cannot check the manifest itself against
the original lecture material (this kit has, and keeps, no PDF/PPTX parser). A
manifest that was shrunk to match a thin draft will still pass. This is a
self-consistency check (the agent's own output vs. its own plan), not a truth
oracle. Use it to catch an accidental drop between "I planned N concepts" and
"I shipped M sections," not to verify the plan was complete in the first place.

Usage:
    python3 scripts/check_coverage.py <dir-containing-concepts.json-and-artifacts>

The target directory should contain `concepts.json` and, typically,
`companion.tex` and/or `lecture.html` (quick mode may ship only one). Missing
`concepts.json` is a WARN, not a FAIL, so this stays non-blocking for anyone who
hasn't adopted the manifest step yet. Missing individual artifacts are skipped
(WARN), not FAILed, so a companion-only or lecture-only directory still works.

Exit code is non-zero if any check FAILs.
"""

import json
import os
import re
import sys

# --------------------------------------------------------------------------- #
# Result accounting (same shape as lint.py / lint_tex.py)
# --------------------------------------------------------------------------- #
class Report:
    LEVELS = ("PASS", "WARN", "FAIL")

    def __init__(self):
        self.rows = []
        self.counts = {lvl: 0 for lvl in self.LEVELS}

    def add(self, level, name, message=""):
        self.rows.append((level, name, message))
        self.counts[level] += 1

    def passed(self, n, m=""): self.add("PASS", n, m)
    def warned(self, n, m=""): self.add("WARN", n, m)
    def failed(self, n, m=""): self.add("FAIL", n, m)

    def print_all(self):
        glyph = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}
        for level, name, message in self.rows:
            print(f"{glyph[level]} {name}")
            if message:
                for sub in message.splitlines():
                    print(f"         {sub}")

    @property
    def has_fail(self):
        return self.counts["FAIL"] > 0


# --------------------------------------------------------------------------- #
# Counting helpers
# --------------------------------------------------------------------------- #
def count_tex_sections(raw):
    """Non-starred \\section{...} count (starred = Glossary/Further reading etc,
    same exclusion rule lint_tex.py's check_figure_coverage already uses)."""
    body_m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", raw, re.DOTALL)
    body = body_m.group(1) if body_m else raw
    body = re.sub(r"(?<!\\)%.*", "", body)
    return len([m for m in re.finditer(r"\\section(\*)?\{([^}]*)\}", body)
                if m.group(1) != "*"])


def count_tex_worked(raw):
    """Worked-example boxes. Matches \\begin{worked...} so both the shipped
    `worked` environment and a differently-named local variant (e.g. a
    standalone specimen defining its own `workedbox`) both count — the box
    NAME is a template detail, the box existing is what coverage cares about."""
    body_m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", raw, re.DOTALL)
    body = body_m.group(1) if body_m else raw
    body = re.sub(r"(?<!\\)%.*", "", body)
    return len(re.findall(r"\\begin\{worked\w*\}", body))


def count_html_sections(raw):
    return len(re.findall(r"<section\b[^>]*\bid=", raw))


def count_html_labs(raw):
    return len(re.findall(r"class=\"[^\"]*\blab\b[^\"]*\"", raw))


def band(n_have, n_want, warn_tol, name_have, name_want):
    """Shared PASS/WARN/FAIL banding: exact match PASS, within tolerance WARN,
    further off FAIL."""
    diff = abs(n_have - n_want)
    msg = f"manifest lists {n_want} {name_want}; {name_have} has {n_have}."
    if diff == 0:
        return "PASS", msg
    if diff <= warn_tol:
        return "WARN", msg + " Close enough to be a legitimate merge/split — verify by eye."
    return "FAIL", msg + " That's more than a rounding difference — something was likely dropped."


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def check_dir(target):
    report = Report()

    manifest_path = os.path.join(target, "concepts.json")
    concepts = None
    if not os.path.isfile(manifest_path):
        report.warned(
            "manifest",
            f"No concepts.json in {target} — coverage cannot be checked. "
            "Write it during step 2 of SKILL.md (companion_style.md §1 step 5).",
        )
    else:
        try:
            with open(manifest_path, encoding="utf-8") as fh:
                concepts = json.load(fh)
            if not isinstance(concepts, list) or not concepts:
                report.failed("manifest", "concepts.json must be a non-empty JSON array.")
                concepts = None
            else:
                report.passed("manifest", f"{len(concepts)} concept(s) catalogued.")
        except (json.JSONDecodeError, OSError) as exc:
            report.failed("manifest", f"concepts.json is not valid JSON: {exc}")

    n_concepts = len(concepts) if concepts else None
    n_examples = (sum(int(c.get("n_examples", 0)) for c in concepts)
                  if concepts else None)

    tex_path = os.path.join(target, "companion.tex")
    if not os.path.isfile(tex_path):
        report.warned("companion coverage", "No companion.tex in this directory — skipped.")
    elif n_concepts is None:
        report.warned("companion coverage", "No manifest to check companion.tex against — skipped.")
    else:
        raw = open(tex_path, encoding="utf-8", errors="replace").read()
        n_sec = count_tex_sections(raw)
        level, msg = band(n_sec, n_concepts, warn_tol=2,
                           name_have="companion.tex", name_want="concept(s)")
        report.add(level, "companion sections vs. manifest", msg)

        n_worked = count_tex_worked(raw)
        if n_worked < n_examples:
            report.failed(
                "companion worked examples vs. manifest",
                f"manifest promises {n_examples} worked example(s); companion.tex has "
                f"{n_worked}. A promised example was dropped.",
            )
        else:
            report.passed(
                "companion worked examples vs. manifest",
                f"manifest promises {n_examples}; companion.tex has {n_worked}.",
            )

    html_path = os.path.join(target, "lecture.html")
    if not os.path.isfile(html_path):
        report.warned("lecture coverage", "No lecture.html in this directory — skipped.")
    elif n_concepts is None:
        report.warned("lecture coverage", "No manifest to check lecture.html against — skipped.")
    else:
        raw = open(html_path, encoding="utf-8", errors="replace").read()
        n_sec = count_html_sections(raw)
        level, msg = band(n_sec, n_concepts, warn_tol=2,
                           name_have="lecture.html", name_want="concept(s)")
        report.add(level, "lecture sections vs. manifest", msg)

        n_labs = count_html_labs(raw)
        if n_labs < n_examples:
            report.warned(
                "lecture labs vs. manifest",
                f"manifest promises {n_examples} worked example(s); lecture.html has "
                f"{n_labs} .lab block(s). One lab can legitimately replay more than one "
                "example — verify by eye.",
            )
        else:
            report.passed(
                "lecture labs vs. manifest",
                f"manifest promises {n_examples}; lecture.html has {n_labs} .lab block(s).",
            )

    return report


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 scripts/check_coverage.py <output/slug dir>", file=sys.stderr)
        return 2
    target = argv[1]
    if not os.path.isdir(target):
        print(f"Error: no such directory: {target}", file=sys.stderr)
        return 2

    print("=" * 68)
    print(f"Checking coverage: {target}")
    print("=" * 68)
    report = check_dir(target)
    report.print_all()
    print("-" * 68)
    c = report.counts
    print(f"Summary: {c['PASS']} PASS, {c['WARN']} WARN, {c['FAIL']} FAIL")
    if report.has_fail:
        print("Result: FAIL (fix every FAIL, then re-run).")
        return 1
    if c["WARN"]:
        print("Result: PASS WITH WARNINGS.")
        return 0
    print("Result: PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
