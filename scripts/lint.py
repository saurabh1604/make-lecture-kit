#!/usr/bin/env python3
"""Quality gate for a generated lecture / visualizer .html file.

Pure standard library (html.parser + re). No third-party deps, no network.

Usage:
    python3 scripts/lint.py <file.html>

Checks (each reported as PASS / WARN / FAIL):
  * <meta viewport> present.
  * MathJax present if the document uses \\( ... \\) or $$ ... $$ math.
  * Every <script src> / <link href> points at an allowlisted CDN.
  * No leaked secrets (sk-ant-, AKIA..., api_key, Authorization: Bearer).
  * Interactivity present (addEventListener / oninput / onclick, ideally a
    drawing/plotting lib). A lecture page with zero interactions FAILS.
  * Overflow guards present (overflow-wrap / word-break / table-layout:fixed /
    a .math-scroll wrapper).
  * Readability heuristic: visible sentences longer than ~28 words are flagged;
    too many => FAIL. The longest few are printed.
  * Suspiciously long unbroken tokens (>40 non-space chars) flagged as overflow risk.
  * WARN when position:fixed / position:absolute is used on large content blocks.

Exit code is non-zero if any check FAILs.
"""

import sys
import os
import re
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _plain_language as PL  # shared word lists + readability, also used by lint_tex.py

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Hosts we trust to serve external libraries.
ALLOWED_CDN_HOSTS = (
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "cdn.plot.ly",
)

# Tunables for the readability heuristic. The ceiling matches plain_language.md
# (aim 15 words, hard ceiling 22) so the HTML and the companion are held to the
# same bar.
SENTENCE_WORD_WARN = PL.WORD_CEILING   # sentences longer than this (22) are flagged
SENTENCE_FAIL_RATIO = 0.15       # > this fraction of long sentences => FAIL
SENTENCE_FAIL_ABS = 12           # ...or this many long sentences => FAIL
LONG_TOKEN_CHARS = 40            # unbroken run of non-space chars => overflow risk
LARGE_BLOCK_CHARS = 600          # text length that makes a positioned block "large"

# Secret patterns we never want to ship in a keyless, self-contained file.
SECRET_PATTERNS = [
    ("anthropic key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}")),
    ("openai-style key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("aws access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("api_key literal", re.compile(r"""api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]""", re.I)),
    ("bearer token", re.compile(r"Authorization\s*:\s*Bearer\s+\S+", re.I)),
]

# Tags whose text content is code/markup, not human-readable prose.
NON_PROSE_TAGS = {"script", "style", "noscript", "template", "code", "pre", "svg"}


# --------------------------------------------------------------------------- #
# Result accounting
# --------------------------------------------------------------------------- #

class Report:
    """Collects PASS/WARN/FAIL lines and tracks counts for the summary."""

    LEVELS = ("PASS", "WARN", "FAIL")

    def __init__(self):
        self.rows = []          # (level, name, message)
        self.counts = {lvl: 0 for lvl in self.LEVELS}

    def add(self, level, name, message=""):
        assert level in self.LEVELS, level
        self.rows.append((level, name, message))
        self.counts[level] += 1

    def passed(self, name, message=""):
        self.add("PASS", name, message)

    def warned(self, name, message=""):
        self.add("WARN", name, message)

    def failed(self, name, message=""):
        self.add("FAIL", name, message)

    def print_all(self):
        glyph = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}
        for level, name, message in self.rows:
            line = f"{glyph[level]} {name}"
            print(line)
            if message:
                for sub in message.splitlines():
                    print(f"         {sub}")

    @property
    def has_fail(self):
        return self.counts["FAIL"] > 0


# --------------------------------------------------------------------------- #
# HTML extraction
# --------------------------------------------------------------------------- #

class DocParser(HTMLParser):
    """Pulls out the structured facts each check needs in a single pass."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.has_viewport = False
        self.script_srcs = []          # external script URLs
        self.link_hrefs = []           # external stylesheet/href URLs
        self.has_mathjax_tag = False   # a <script src=...mathjax...> tag
        self.event_attrs = []          # inline on* handler names found
        self.canvas = False
        self.svg = False
        # Visible-prose collection.
        self._suppress_depth = 0       # >0 while inside a non-prose tag
        self._prose_chunks = []
        # Positioned large blocks: collect (tag, style) for post-analysis.
        self._open_positioned = []     # stack of [tag, style, text_len, is_positioned]
        self._large_positioned = []

    # -- helpers ----------------------------------------------------------- #
    @staticmethod
    def _attr(attrs, key):
        for k, v in attrs:
            if k == key:
                return v or ""
        return None

    # -- tag handling ------------------------------------------------------ #
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrd = dict(attrs)

        if tag == "meta":
            name = (attrd.get("name") or "").lower()
            if name == "viewport":
                self.has_viewport = True

        if tag == "script":
            src = attrd.get("src")
            if src:
                self.script_srcs.append(src)
                if "mathjax" in src.lower():
                    self.has_mathjax_tag = True

        if tag == "link":
            href = attrd.get("href")
            if href:
                self.link_hrefs.append(href)

        if tag == "canvas":
            self.canvas = True
        if tag == "svg":
            self.svg = True

        # Inline event handlers anywhere.
        for k, _v in attrs:
            if k and k.lower().startswith("on"):
                self.event_attrs.append(k.lower())

        # Track positioned blocks for the large-block-positioning warning.
        style = (attrd.get("style") or "")
        is_positioned = bool(re.search(r"position\s*:\s*(fixed|absolute)", style, re.I))
        self._open_positioned.append([tag, style, 0, is_positioned])

        # Suppress prose collection inside code/script/style/etc.
        if tag in NON_PROSE_TAGS:
            self._suppress_depth += 1

    BLOCK_TAGS = {
        "p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th",
        "figcaption", "button", "label", "a", "div", "section", "blockquote",
    }

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in NON_PROSE_TAGS and self._suppress_depth > 0:
            self._suppress_depth -= 1

        # A closing block element ends any sentence in progress — without this,
        # headings, buttons, and list items glue together into fake
        # mega-sentences that break the readability stats.
        if tag in self.BLOCK_TAGS and self._prose_chunks \
                and self._prose_chunks[-1] != "\n":
            self._prose_chunks.append("\n")

        # Pop the most recent matching positioned block (best-effort; HTML may
        # be imperfect, so guard against an empty stack).
        for i in range(len(self._open_positioned) - 1, -1, -1):
            if self._open_positioned[i][0] == tag:
                entry = self._open_positioned.pop(i)
                if entry[3] and entry[2] >= LARGE_BLOCK_CHARS:
                    self._large_positioned.append((entry[0], entry[2]))
                break

    def handle_data(self, data):
        if self._suppress_depth == 0:
            stripped = data.strip()
            if stripped:
                self._prose_chunks.append(stripped)
        # Credit text length to all currently-open blocks (rough, but fine for
        # spotting big positioned containers).
        n = len(data.strip())
        if n:
            for entry in self._open_positioned:
                entry[2] += n

    @property
    def prose(self):
        return " ".join(self._prose_chunks)

    @property
    def large_positioned_blocks(self):
        return self._large_positioned


# --------------------------------------------------------------------------- #
# Individual checks
# --------------------------------------------------------------------------- #

def check_viewport(parser, report):
    if parser.has_viewport:
        report.passed("meta viewport", "Responsive viewport meta tag present.")
    else:
        report.failed(
            "meta viewport",
            'Missing <meta name="viewport" content="width=device-width, '
            'initial-scale=1.0">. Page will not be mobile-responsive.',
        )


def check_mathjax(raw, parser, report):
    uses_inline = "\\(" in raw or "\\[" in raw
    uses_display = "$$" in raw
    needs_math = uses_inline or uses_display
    if not needs_math:
        report.passed("MathJax", "No \\( \\) or $$ math detected; MathJax not required.")
        return
    if parser.has_mathjax_tag or "MathJax" in raw:
        report.passed("MathJax", "Math notation found and MathJax is loaded.")
    else:
        report.failed(
            "MathJax",
            "Document uses \\( ... \\) or $$ ... $$ math but no MathJax script "
            "was found. Equations will render as raw text.",
        )


def _host_of(url):
    """Best-effort host extraction without urllib edge cases."""
    u = url.strip()
    if u.startswith("//"):
        u = "http:" + u
    m = re.match(r"[a-zA-Z][a-zA-Z0-9+.\-]*://([^/]+)", u)
    if not m:
        return None  # relative / data: / inline
    host = m.group(1).lower()
    # strip credentials and port
    host = host.split("@")[-1].split(":")[0]
    return host


def check_cdn_allowlist(parser, report):
    urls = [("script", s) for s in parser.script_srcs]
    urls += [("link", h) for h in parser.link_hrefs]

    offenders = []
    insecure = []
    checked_remote = 0
    for kind, url in urls:
        host = _host_of(url)
        if host is None:
            # Relative path, data:, or inline reference — fine for self-contained.
            continue
        checked_remote += 1
        is_http = url.strip().lower().startswith("http://")
        if host not in ALLOWED_CDN_HOSTS:
            offenders.append(f"{kind} -> {url}  (host: {host})")
            continue
        if is_http:
            # Allowlisted host but plain http:// — flag as a warning.
            insecure.append(f"{kind} -> {url}")

    if offenders:
        report.failed(
            "CDN allowlist",
            "Disallowed external resource host(s) found "
            f"(allowed: {', '.join(ALLOWED_CDN_HOSTS)}):\n  "
            + "\n  ".join(offenders),
        )
    elif checked_remote == 0:
        report.passed("CDN allowlist", "No remote resources (fully self-contained).")
    else:
        msg = f"All {checked_remote} remote resource(s) on the CDN allowlist."
        if insecure:
            report.warned(
                "CDN allowlist",
                msg + "\nHowever, some use http:// (prefer https://):\n  "
                + "\n  ".join(insecure),
            )
        else:
            report.passed("CDN allowlist", msg)


def check_secrets(raw, report):
    hits = []
    for label, pat in SECRET_PATTERNS:
        for m in pat.finditer(raw):
            snippet = m.group(0)
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            hits.append(f"{label}: {snippet}")
    if hits:
        # De-dup while preserving order.
        seen, uniq = set(), []
        for h in hits:
            if h not in seen:
                seen.add(h)
                uniq.append(h)
        report.failed(
            "secrets",
            "Possible secret(s) detected — must not ship in a keyless file:\n  "
            + "\n  ".join(uniq),
        )
    else:
        report.passed("secrets", "No secret-like patterns found.")


def check_interactivity(raw, parser, report):
    has_listener = "addEventListener" in raw
    inline_handlers = sorted(set(parser.event_attrs))
    has_plot = (
        "Plotly" in raw
        or parser.canvas
        or "getContext" in raw
        or re.search(r"\bd3\b", raw) is not None
    )

    interactive = has_listener or bool(parser.event_attrs)
    signals = []
    if has_listener:
        signals.append("addEventListener")
    if inline_handlers:
        signals.append("inline " + "/".join(inline_handlers))
    if has_plot:
        bits = []
        if "Plotly" in raw:
            bits.append("Plotly")
        if parser.canvas or "getContext" in raw:
            bits.append("canvas")
        if re.search(r"\bd3\b", raw):
            bits.append("d3")
        signals.append("drawing: " + "+".join(bits))

    if interactive and has_plot:
        report.passed("interactivity", "Interactions wired: " + "; ".join(signals))
    elif interactive and not has_plot:
        report.warned(
            "interactivity",
            "Event handlers found (" + "; ".join(signals) + ") but no Plotly/"
            "canvas/d3 visual. A lecture page should let learners *move* a plot.",
        )
    else:
        report.failed(
            "interactivity",
            "No interactions found (no addEventListener / oninput / onclick). "
            "A lecture/visualizer page must have >=1 working interaction.",
        )


def check_overflow_guards(raw, report):
    guards = {
        "overflow-wrap": "overflow-wrap" in raw,
        "word-break": "word-break" in raw,
        "table-layout:fixed": bool(re.search(r"table-layout\s*:\s*fixed", raw, re.I)),
        ".math-scroll": "math-scroll" in raw,
        "overflow-x:auto": bool(re.search(r"overflow-x\s*:\s*auto", raw, re.I)),
    }
    present = [name for name, ok in guards.items() if ok]
    if present:
        report.passed("overflow guards", "Present: " + ", ".join(present) + ".")
    else:
        report.failed(
            "overflow guards",
            "No overflow guards found. Add overflow-wrap/word-break on prose, "
            "table-layout:fixed on tables, and a .math-scroll wrapper "
            "(overflow-x:auto) around wide equations.",
        )


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"\S+")


def check_readability(parser, report):
    prose = parser.prose
    if not prose.strip():
        report.warned("readability", "No visible prose extracted; cannot assess.")
        return

    # Math is not prose: strip \( \), \[ \], and $$ $$ spans so formula-heavy
    # sentences aren't penalised for symbol tokens.
    prose = re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$", " ", prose,
                   flags=re.DOTALL)

    # Block boundaries (newlines from the parser) end sentences; then split
    # each line on sentence punctuation.
    sentences = []
    for line in prose.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            sentences.extend(s for s in _SENTENCE_SPLIT.split(line) if s.strip())
    if not sentences:
        sentences = [re.sub(r"\s+", " ", prose).strip()]

    long_ones = []
    for s in sentences:
        wc = len(_WORD.findall(s))
        if wc > SENTENCE_WORD_WARN:
            long_ones.append((wc, s))

    total = len(sentences)
    n_long = len(long_ones)
    ratio = n_long / total if total else 0.0
    long_ones.sort(reverse=True)
    longest_preview = "\n".join(
        f"{wc}w: " + (s[:120] + ("..." if len(s) > 120 else ""))
        for wc, s in long_ones[:3]
    )

    base = (
        f"{total} sentences; {n_long} over {SENTENCE_WORD_WARN} words "
        f"({ratio*100:.0f}%)."
    )
    if n_long == 0:
        report.passed("readability", base + " Sentences are short and clear.")
    elif n_long >= SENTENCE_FAIL_ABS or ratio > SENTENCE_FAIL_RATIO:
        report.failed(
            "readability",
            base + " Too many long sentences for a smart-beginner audience.\n"
            "Longest:\n" + longest_preview,
        )
    else:
        report.warned(
            "readability",
            base + " A few long sentences — consider splitting.\n"
            "Longest:\n" + longest_preview,
        )


def _math_stripped_prose(parser):
    """Visible prose with \\( \\), \\[ \\], $$ $$ spans removed (not prose)."""
    return re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$", " ",
                  parser.prose, flags=re.DOTALL)


def check_plain_words(parser, report):
    """Banned hand-waving (FAIL) + fancy words / literary flourishes (WARN).

    Shares its lists with the companion linter via _plain_language.py, so the
    HTML and the PDF are held to the same plain-English bar.
    """
    prose = _math_stripped_prose(parser)
    hand = PL.find_handwaving(prose)
    if hand:
        listing = ", ".join(f'"{p}" x{c}' for p, c in hand)
        report.failed("hand-waving",
                      "Banned hand-waving (show the step instead): " + listing)
    else:
        report.passed("hand-waving", "No banned hand-waving phrases.")

    fancy = PL.find_fancy(prose)
    flo = PL.find_flourishes(prose)
    total = sum(c for _, _, c in fancy) + sum(c for _, c in flo)
    if total == 0:
        report.passed("word choice", "Plain words throughout.")
        return
    bits = []
    if fancy:
        bits.append("fancy: " + ", ".join(
            f"{w}->{s} x{c}" for w, s, c in fancy[:8]))
    if flo:
        bits.append("flourish: " + ", ".join(
            f'"{p}" x{c}' for p, c in flo[:6]))
    msg = "\n".join(bits)
    if total >= 12:
        report.failed("word choice",
                      f"{total} fancy/flourish hits — swap for plain words "
                      "(plain_language.md §3).\n" + msg)
    else:
        report.warned("word choice",
                      f"{total} fancy/flourish hit(s) — prefer plain words.\n" + msg)


def check_reading_level(parser, report):
    """Flesch reading-ease estimate (WARN if the prose reads hard)."""
    prose = _math_stripped_prose(parser)
    score, nwords, nsent = PL.flesch_reading_ease(prose)
    if nwords < 80:
        report.passed("reading level", f"Flesch ~{score} ({nwords} words).")
        return
    note = (f"Flesch reading-ease ~{score} ({nwords} words, {nsent} "
            "sentences); higher is easier, >=60 ~ plain English.")
    if score < 45:
        report.warned("reading level",
                      note + " Reads hard — shorten sentences, swap long words.")
    else:
        report.passed("reading level", note)


def check_long_tokens(parser, report):
    """Flag unbroken runs of non-space characters in visible prose."""
    prose = parser.prose
    risky = []
    for tok in _WORD.findall(prose):
        # Ignore URLs and obvious math; focus on word-like blobs.
        if len(tok) > LONG_TOKEN_CHARS and not tok.startswith(("http://", "https://")):
            risky.append(tok)
    risky = sorted(set(risky), key=len, reverse=True)
    if not risky:
        report.passed(
            "long tokens",
            f"No unbroken tokens longer than {LONG_TOKEN_CHARS} chars in prose.",
        )
    else:
        preview = "\n".join(
            (t[:60] + "...") + f" ({len(t)} chars)" for t in risky[:3]
        )
        report.warned(
            "long tokens",
            f"{len(risky)} long unbroken token(s) (>{LONG_TOKEN_CHARS} chars) "
            "may cause horizontal overflow:\n" + preview,
        )


def check_positioned_blocks(parser, report):
    blocks = parser.large_positioned_blocks
    if not blocks:
        report.passed(
            "positioned blocks",
            "No large content blocks use position:fixed/absolute.",
        )
    else:
        desc = ", ".join(f"<{t}> ~{n} chars" for t, n in blocks[:5])
        report.warned(
            "positioned blocks",
            "position:fixed/absolute on large content block(s) can overlap or "
            "overflow on small screens: " + desc,
        )


def check_template_hygiene(raw, report):
    """Catch the two bugs that have actually shipped before:
    (1) an HTML comment containing a nested marker, which ends the comment
        early and leaks the rest as visible text;
    (2) {{PLACEHOLDER}} text left outside comments, which renders literally.
    """
    problems = []

    # (1) nested markers inside comments
    pos, n_comments = 0, 0
    while True:
        start = raw.find("<!--", pos)
        if start < 0:
            break
        end = raw.find("-->", start + 4)
        if end < 0:
            problems.append(
                f"comment opened at offset {start} is never closed")
            break
        body = raw[start + 4:end]
        if "<!--" in body:
            line = raw[:start].count("\n") + 1
            problems.append(
                f"comment at line {line} contains a nested '<!--' — the inner "
                "comment's '-->' will end the outer one early and leak text")
        pos = end + 3
        n_comments += 1

    # (2) visible {{...}} placeholders (strip comments, scripts, styles first)
    visible = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    visible = re.sub(r"<script\b.*?</script>", "", visible,
                     flags=re.DOTALL | re.IGNORECASE)
    visible = re.sub(r"<style\b.*?</style>", "", visible,
                     flags=re.DOTALL | re.IGNORECASE)
    leftovers = re.findall(r"\{\{[^}]{0,60}\}?\}?", visible)
    if leftovers:
        sample = "; ".join(t.strip()[:40] for t in leftovers[:5])
        problems.append(
            f"{len(leftovers)} visible {{{{placeholder}}}} token(s) would "
            f"render as literal text: {sample}")

    if problems:
        report.failed("template hygiene", "\n".join(problems))
    else:
        report.passed(
            "template hygiene",
            f"{n_comments} comment(s) well-formed; no visible placeholders.",
        )


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def lint_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()

    parser = DocParser()
    try:
        parser.feed(raw)
        parser.close()
    except Exception as exc:  # noqa: BLE001 - keep the linter robust on bad HTML
        print(f"[WARN] HTML parser raised {exc!r}; continuing with partial data.")

    report = Report()
    check_template_hygiene(raw, report)
    check_viewport(parser, report)
    check_mathjax(raw, parser, report)
    check_cdn_allowlist(parser, report)
    check_secrets(raw, report)
    check_interactivity(raw, parser, report)
    check_overflow_guards(raw, report)
    check_readability(parser, report)
    check_plain_words(parser, report)
    check_reading_level(parser, report)
    check_long_tokens(parser, report)
    check_positioned_blocks(parser, report)
    return report


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 scripts/lint.py <file.html>", file=sys.stderr)
        return 2

    path = argv[1]
    if not os.path.isfile(path):
        print(f"Error: no such file: {path}", file=sys.stderr)
        return 2

    print("=" * 68)
    print(f"Linting: {path}")
    print("=" * 68)

    report = lint_file(path)
    report.print_all()

    print("-" * 68)
    c = report.counts
    print(f"Summary: {c['PASS']} PASS, {c['WARN']} WARN, {c['FAIL']} FAIL")
    if report.has_fail:
        print("Result: FAIL (one or more checks failed).")
        return 1
    if c["WARN"]:
        print("Result: PASS WITH WARNINGS.")
        return 0
    print("Result: PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
