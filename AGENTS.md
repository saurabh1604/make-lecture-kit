# AGENTS.md — make-lecture-kit

This repository **is** an agent skill. If you are an AI coding agent (Google
Jules, OpenAI Codex, Claude, Cursor, Gemini CLI, or similar), read this file,
then read **`SKILL.md`** and follow it exactly. `SKILL.md` is the authoritative
workflow; this file is the quick map that agents which key off `AGENTS.md`
(Jules especially) read first.

## What you do here

Turn lecture material — an attached slide deck (PDF/PPTX), a full session
transcript (doc/docx/pdf/txt), instructor notes, a textbook excerpt, just a topic,
or several of these together — into two artifacts inside `output/<topic>/`. When
more than one source is given, `SKILL.md` step 2 / `references/companion_style.md`
§1 step 0 has the rule for which one drives structure.

- **`companion.pdf`** — a typeset LaTeX study companion: plain easy English,
  analogies before the math, every example worked in full. Built from
  `templates/companion.tex`.
- **`lecture.html`** — a complete, very interactive lecture page. Built from
  `templates/lecture.html`.

Typical user triggers: *"use make-lecture-kit on this lecture"*, *"make a study
PDF and an interactive lecture for &lt;topic&gt;"*.

## How to run it

1. Read `SKILL.md`, starting with `references/cheatsheet.md` (the fast-start
   reference), then the style guides in `references/` — pull the big guides
   (`companion_style.md`, `lecture_style.md`) up only for the sections this
   lecture actually needs, not cover to cover.
2. Write the companion source + figures, then build the PDF:
   ```bash
   python3 scripts/build_pdf.py output/<topic>/companion.tex
   ```
   (This runs the figure scripts, compiles with `latexmk`/`pdflatex`, and then
   runs the companion language/layout gate `scripts/lint_tex.py` automatically.
   Add `--changed-only` on later rebuilds to skip figure scripts that haven't
   changed.) On a fix iteration, patch the flagged line/snippet with `Edit`
   rather than rewriting the whole file.
3. Quality gates — all must pass before you tell the user you are done:
   ```bash
   python3 scripts/lint.py           output/<topic>/lecture.html   # HTML gate (incl. canvas-wiring)
   python3 scripts/lint_tex.py       output/<topic>/companion.tex  # PDF-source gate
   python3 scripts/check_coverage.py output/<topic>                # concepts.json vs. shipped sections
   python3 scripts/selfcheck.py                                    # the kit is healthy
   ```
   Fix every FAIL and re-run until clean. `check_coverage.py` is a self-consistency
   check against the manifest you wrote in step 2 of `SKILL.md`, not a truth check
   against the original material.
4. `references/lecture_style.md` §10.1 documents an optional, deeper Node-based
   check that actually executes every canvas demo's JS — use it if your
   environment has Node, but it is never required.

Everything is standard-library Python + standard LaTeX (TeX Live ships in most
agent sandboxes). **No API keys, and generating needs no network.** Only
`scripts/update.py` touches the network, and only when run on purpose. If there
is no TeX engine, `build_pdf.py` says so plainly and leaves the ready-to-compile
`.tex` + figures — do not claim a `companion.pdf` exists if it was not built.

## Rules

- Write in plain, easy English; explain the intuition before you formalize it;
  work examples out in full. The linters enforce sentence length, plain words,
  and reading level.
- Explain simple things simply. Right-size every explanation (see
  `references/plain_language.md` §8): lead with the most intuitive way in, use at
  most one analogy, and never inflate an easy idea to look thorough.
- Never let text overflow a page, box, or screen — the gates hard-fail this.
- Generate into `output/` only. **Never edit `output/` by hand**, and never
  overwrite a student's existing work there.

## Staying current

This repo is the single source of truth; `VERSION` is the current version and
`CHANGELOG.md` lists what changed. To update a local copy:

```bash
git pull                      # if cloned, or:
python3 scripts/update.py     # works for zip downloads too; keeps your output/
```

Cloud agents that re-clone the repo for each task (e.g. **Jules**) always get the
latest automatically — there is nothing to update.
