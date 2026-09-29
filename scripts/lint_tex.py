#!/usr/bin/env python3
"""Quality gate for a generated companion **.tex** (the printable study PDF).

The HTML had `lint.py`; the companion had nothing — yet it is the primary
deliverable. This is its language + layout gate. Pure standard library; shares
its word lists with the HTML linter via `_plain_language.py`, so both gates
agree. No third-party deps, no network. Runs on any agent platform.

Usage:
    python3 scripts/lint_tex.py <companion.tex>

Checks (PASS / WARN / FAIL):
  * Easy language (on extracted prose, math stripped):
      - sentences longer than the ceiling are flagged; too many => FAIL;
      - banned hand-waving ("it can be shown", "clearly", …) => FAIL;
      - fancy words / literary flourishes => WARN, many => FAIL;
      - Flesch reading-ease estimate => WARN if it reads hard.
  * Layout / no-overflow (on raw TeX):
      - worked-example steps that use a raw `enumerate` with a "Step" label
        (the label spills OUTSIDE the callout box) => FAIL; use `steps`.
      - wide `tabular` not wrapped in `\\resizebox`/`adjustbox` => WARN.
      - very long single-line display math (`\\[ … \\]`) => WARN (use align/split).
      - leftover visible `{{PLACEHOLDER}}` tokens => FAIL.
      - a hard `\\usepackage{bbding}` with no `\\IfFileExists` guard => WARN
        (bbding is missing on some TeX installs and would abort the build).
  * If a sibling `<stem>.log` exists, parse it for Overfull boxes:
      - any Overfull \\hbox wider than ~2pt (visibly into the margin) => FAIL.

Exit code is non-zero if any check FAILs.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _plain_language as PL  # noqa: E402


# --------------------------------------------------------------------------- #
# Result accounting (same shape as lint.py)
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
# TeX -> prose extraction (approximate, good enough for language scanning)
# --------------------------------------------------------------------------- #
_KEEP_CONTENT_CMDS = (
    "textbf", "textit", "emph", "texttt", "textsf", "textsc", "vocab", "tg",
    "text", "section", "subsection", "subsubsection", "caption", "underline",
    "mbox", "textcolor",
)


def _strip_environment(s, name):
    return re.sub(
        r"\\begin\{" + name + r"\*?\}.*?\\end\{" + name + r"\*?\}",
        " ", s, flags=re.DOTALL,
    )


def tex_to_prose(raw):
    """Return readable body prose with comments, math, and markup removed."""
    # Body only.
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", raw, re.DOTALL)
    s = m.group(1) if m else raw

    # Drop line comments (an unescaped %).
    s = re.sub(r"(?<!\\)%.*", " ", s)

    # Headings and the \secsub one-liner are their own "sentences": a title has
    # no full stop, so without a paragraph break it would glue onto the next
    # sentence and trip the length check. Put each heading line in its own
    # paragraph. The title banner's four fields are labels, not prose: drop them.
    s = re.sub(r"^[ \t]*(\\(?:sub)*section\*?\{.*)$", r"\n\n\1\n\n", s, flags=re.M)
    s = re.sub(r"(\\secsub\{)", r"\n\n\1", s)
    s = re.sub(r"\\titlebanner\s*((\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})\s*){4}", "\n\n", s)

    # Drop math: environments, display, and inline.
    for env in ("equation", "align", "aligned", "gather", "multline",
                "split", "eqnarray", "array", "tabular", "tikzpicture",
                "minipage", "center"):
        s = _strip_environment(s, env)
    s = re.sub(r"\\\[.*?\\\]", " ", s, flags=re.DOTALL)
    s = re.sub(r"\\\(.*?\\\)", " ", s, flags=re.DOTALL)
    s = re.sub(r"(?<!\\)\$\$.*?\$\$", " ", s, flags=re.DOTALL)
    s = re.sub(r"(?<!\\)\$[^$]*\$", " ", s)

    # \textcolor{c}{X} -> X  (drop the colour arg first).
    s = re.sub(r"\\textcolor\{[^}]*\}", "", s)

    # Commands whose brace content IS prose: unwrap a few passes (nesting).
    cmd_re = re.compile(r"\\(" + "|".join(_KEEP_CONTENT_CMDS) + r")\*?\{")
    for _ in range(6):
        out, i, changed = [], 0, False
        while i < len(s):
            mm = cmd_re.match(s, i)
            if mm:
                j = mm.end()
                depth, start = 1, j
                while j < len(s) and depth:
                    if s[j] == "{":
                        depth += 1
                    elif s[j] == "}":
                        depth -= 1
                    j += 1
                out.append(s[start:j - 1])  # inner content
                i = j
                changed = True
            else:
                out.append(s[i])
                i += 1
        s = "".join(out)
        if not changed:
            break

    # Environment ARGUMENTS that are not body prose: the worked-box caption is a
    # pill-tab label, not a sentence — drop "\begin{worked}{...}" wholesale so the
    # caption does not glue onto the first real sentence inside the box.
    s = re.sub(r"\\begin\{worked\}\s*\{[^}]*\}", " ", s)

    # Drop figure/href/url/includegraphics/housefig payloads.
    s = re.sub(r"\\housefig\{[^}]*\}\{[^}]*\}", " ", s)
    s = re.sub(r"\\href\{[^}]*\}", " ", s)
    s = re.sub(r"\\url\{[^}]*\}", " ", s)
    s = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", " ", s)

    # Environment markers, list items, and leftover commands.
    s = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", " ", s)
    s = re.sub(r"\\item(\[[^\]]*\])?", " ", s)
    s = re.sub(r"\\[A-Za-z@]+\*?(\[[^\]]*\])?", " ", s)  # remaining macros
    s = re.sub(r"[{}]", " ", s)
    s = s.replace("~", " ").replace("\\\\", " ").replace("&", " ")
    s = re.sub(r"``|''", '"', s)
    # Distinguish a real paragraph break (a BLANK line) from a mere LaTeX source
    # line-wrap (a single newline mid-paragraph). Only the former ends a
    # sentence; the latter must become a space, or long sentences get split into
    # short fragments and slip past the length check.
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n[ \t]*\n+", "\x00", s)   # blank line(s) -> paragraph sentinel
    s = s.replace("\n", " ")                   # remaining single newline -> space
    s = s.replace("\x00", "\n")              # restore paragraph breaks
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


# Split after . ! ? — allowing one closing quote (straight or curly) between the
# punctuation and the space, so '...well." That...' splits into two sentences.
_SENT_SPLIT = re.compile(r"""(?<=[.!?])["”’']?\s+""")
_WORD = re.compile(r"\S+")


def split_sentences(prose):
    out = []
    for line in prose.split("\n"):
        line = line.strip()
        if not line:
            continue
        out.extend(s for s in _SENT_SPLIT.split(line) if s.strip())
    return out


# --------------------------------------------------------------------------- #
# Language checks
# --------------------------------------------------------------------------- #
def check_sentences(prose, report):
    sents = split_sentences(prose)
    if not sents:
        report.warned("readability", "No prose extracted; cannot assess.")
        return
    long_ones = [(len(_WORD.findall(s)), s) for s in sents
                 if len(_WORD.findall(s)) > PL.WORD_CEILING]
    total, n_long = len(sents), len(long_ones)
    ratio = n_long / total if total else 0.0
    long_ones.sort(reverse=True)
    preview = "\n".join(f"{wc}w: " + (s[:110] + ("…" if len(s) > 110 else ""))
                        for wc, s in long_ones[:4])
    base = f"{total} sentences; {n_long} over {PL.WORD_CEILING} words ({ratio*100:.0f}%)."
    if n_long == 0:
        report.passed("sentence length", base + " Short and clear.")
    elif n_long >= 12 or ratio > 0.15:
        report.failed("sentence length",
                      base + " Too many long sentences for a smart beginner.\n"
                      "Split the longest:\n" + preview)
    else:
        report.warned("sentence length",
                      base + " A few long sentences — consider splitting.\n" + preview)


def check_handwaving(prose, report):
    hits = PL.find_handwaving(prose)
    if hits:
        listing = ", ".join(f'"{p}" ×{c}' for p, c in hits)
        report.failed("hand-waving",
                      "Banned hand-waving found (show the step instead): "
                      + listing)
    else:
        report.passed("hand-waving", "No banned hand-waving phrases.")


def check_word_choice(prose, report):
    fancy = PL.find_fancy(prose)
    flo = PL.find_flourishes(prose)
    total = sum(c for _, _, c in fancy) + sum(c for _, c in flo)
    if total == 0:
        report.passed("word choice", "Plain words throughout.")
        return
    bits = []
    if fancy:
        bits.append("fancy words: " + ", ".join(
            f"{w}→{sug} ×{c}" for w, sug, c in fancy[:8]))
    if flo:
        bits.append("flourishes: " + ", ".join(
            f'"{p}" ×{c}' for p, c in flo[:6]))
    msg = "\n".join(bits)
    if total >= 12:
        report.failed("word choice",
                      f"{total} fancy/flourish hits — swap for plain words "
                      "(plain_language.md §3).\n" + msg)
    else:
        report.warned("word choice",
                      f"{total} fancy/flourish hit(s) — prefer plain words.\n" + msg)


def check_reading_level(prose, report):
    score, nwords, nsent = PL.flesch_reading_ease(prose)
    if nwords < 80:
        report.passed("reading level", f"Flesch ~{score} ({nwords} words).")
        return
    note = (f"Flesch reading-ease ~{score} "
            f"({nwords} words, {nsent} sentences). Higher is easier; "
            "≥60 ≈ plain English.")
    if score < 45:
        report.warned("reading level", note + " Reads hard — shorten sentences, "
                      "swap long words, add plain restatements.")
    else:
        report.passed("reading level", note)


# --------------------------------------------------------------------------- #
# Layout / no-overflow checks (on raw TeX)
# --------------------------------------------------------------------------- #
def _body(raw):
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", raw, re.DOTALL)
    return m.group(1) if m else raw


def _strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def check_step_lists(raw, report):
    body = _strip_comments(_body(raw))
    # A raw enumerate whose options mention "Step" — the label overflows the box.
    bad = re.findall(r"\\begin\{enumerate\}\s*\[[^\]]*Step[^\]]*\]", body)
    if bad:
        report.failed(
            "worked-example steps",
            f"{len(bad)} worked example(s) use a raw enumerate with a 'Step' "
            "label. The wide 'Step N.' label spills OUTSIDE the callout box. "
            "Use the dedicated environment instead:\n"
            "  \\begin{steps} ... \\end{steps}")
    else:
        uses_steps = "\\begin{steps}" in body
        report.passed(
            "worked-example steps",
            "Steps use the safe `steps` environment."
            if uses_steps else
            "No raw 'Step'-label enumerates (labels stay inside their boxes).")


def check_wide_tables(raw, report):
    src = _strip_comments(_body(raw))
    risky = []
    for m in re.finditer(r"\\begin\{tabular\}\s*(\[[^\]]*\])?\s*\{([^}]*)\}", src):
        colspec = m.group(2)
        ncols = len(re.findall(r"[lcrp]", colspec))
        if ncols < 5:
            continue
        window = src[max(0, m.start() - 220):m.start()]
        wrapped = ("resizebox" in window or "adjustbox" in window
                   or "\\begin{adjustbox}" in window)
        if not wrapped:
            risky.append(ncols)
    if risky:
        report.warned(
            "wide tables",
            f"{len(risky)} wide tabular(s) (≥5 cols) not wrapped in "
            "\\resizebox/adjustbox — they may run off the page. Wrap with "
            "\\resizebox{\\linewidth}{!}{…} or size columns to fit.")
    else:
        report.passed("wide tables", "No unwrapped wide tables.")


def check_long_display_math(raw, report):
    long_disp = []
    for m in re.finditer(r"\\\[(.*?)\\\]", _strip_comments(_body(raw)), flags=re.DOTALL):
        inner = m.group(1)
        if "\\\\" in inner or "split" in inner or "aligned" in inner:
            continue  # already broken across lines
        if len(inner.strip()) > 140:
            long_disp.append(len(inner.strip()))
    if long_disp:
        report.warned(
            "display math width",
            f"{len(long_disp)} long single-line display equation(s) "
            "(>140 chars) — may overflow the margin. Break with align/split.")
    else:
        report.passed("display math width", "No over-long single-line equations.")


def check_figure_coverage(raw, report):
    """Nudge: a concept section with math or a worked example but NO figure.

    Maths/stats/ML ideas land far faster as a picture. This is a WARN (not every
    section is visual), pointing at the concept->plot map in companion_style §5.
    """
    body = _strip_comments(_body(raw))
    secs = list(re.finditer(r"\\section(\*)?\{([^}]*)\}", body))
    if not secs:
        report.passed("figure coverage", "No \\section concepts to check.")
        return
    figureless = []
    n_concept = 0
    for idx, m in enumerate(secs):
        starred = m.group(1) == "*"
        if starred:
            continue  # Further reading / Glossary etc. need no figure
        n_concept += 1
        start = m.end()
        end = secs[idx + 1].start() if idx + 1 < len(secs) else len(body)
        chunk = body[start:end]
        has_fig = ("\\housefig" in chunk or "\\begin{figure}" in chunk
                   or "\\begin{tikzpicture}" in chunk)
        has_math = bool(re.search(
            r"\\\[|\\begin\{(?:equation|align|gather|multline)\*?\}|\$\$", chunk))
        has_worked = "\\begin{worked}" in chunk
        if (has_math or has_worked) and not has_fig:
            figureless.append(re.sub(r"\s+", " ", m.group(2)).strip()[:46])
    if not figureless:
        report.passed("figure coverage",
                      f"Every visual concept section ({n_concept}) has a figure.")
    else:
        listing = "\n  - ".join(figureless[:8])
        report.warned(
            "figure coverage",
            f"{len(figureless)} of {n_concept} concept section(s) have math or a "
            "worked example but NO figure. A plot usually makes these click "
            "(companion_style.md §5 concept->plot map):\n  - " + listing)


def check_placeholders(raw, report):
    body = _body(raw)
    # Strip comments so commented {{...}} scaffolding doesn't count.
    visible = re.sub(r"(?<!\\)%.*", "", body)
    left = re.findall(r"\{\{[^}]{0,60}\}\}", visible)
    if left:
        sample = "; ".join(t[:40] for t in left[:5])
        report.failed("placeholders",
                      f"{len(left)} visible {{{{placeholder}}}} token(s) would "
                      f"print literally: {sample}")
    else:
        report.passed("placeholders", "No leftover {{placeholders}}.")


def check_bbding_guard(raw, report):
    if "\\usepackage{bbding}" in raw and "IfFileExists{bbding.sty}" not in raw:
        report.warned(
            "bbding dependency",
            "Hard \\usepackage{bbding} with no \\IfFileExists guard. bbding is "
            "missing on some TeX installs (TinyTeX / some sandboxes) and would "
            "abort the build. Guard it and fall back to pifont \\ding{43}/{46}.")
    else:
        report.passed("bbding dependency", "No unguarded bbding dependency.")


def check_overfull_log(texpath, report):
    stem = os.path.splitext(texpath)[0]
    logpath = stem + ".log"
    if not os.path.isfile(logpath):
        report.passed("overfull boxes",
                      "No .log beside the .tex yet (compile to check margins).")
        return
    with open(logpath, "r", encoding="utf-8", errors="replace") as fh:
        log = fh.read()
    hbox = re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", log)
    vbox = re.findall(r"Overfull \\vbox \(([\d.]+)pt too high\)", log)
    bad_h = [float(x) for x in hbox if float(x) > 2.0]   # >2pt = visible
    if bad_h:
        report.failed(
            "overfull boxes",
            f"{len(bad_h)} Overfull \\hbox over 2pt (text into the margin); "
            f"widest {max(bad_h):.1f}pt. Wrap wide math/tables; this is the "
            "'content outside the box' symptom.")
    elif hbox or vbox:
        report.warned("overfull boxes",
                      f"{len(hbox)} tiny Overfull \\hbox (<2pt, usually "
                      f"invisible) and {len(vbox)} Overfull \\vbox.")
    else:
        report.passed("overfull boxes", "Clean log — no overfull boxes.")


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def lint_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    prose = tex_to_prose(raw)

    report = Report()
    # language
    check_sentences(prose, report)
    check_handwaving(prose, report)
    check_word_choice(prose, report)
    check_reading_level(prose, report)
    # layout
    check_step_lists(raw, report)
    check_wide_tables(raw, report)
    check_long_display_math(raw, report)
    check_figure_coverage(raw, report)
    check_placeholders(raw, report)
    check_bbding_guard(raw, report)
    check_overfull_log(path, report)
    return report


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 scripts/lint_tex.py <companion.tex>", file=sys.stderr)
        return 2
    path = argv[1]
    if not os.path.isfile(path):
        print(f"Error: no such file: {path}", file=sys.stderr)
        return 2

    print("=" * 68)
    print(f"Linting companion source: {path}")
    print("=" * 68)
    report = lint_file(path)
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
