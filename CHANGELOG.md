# Changelog

All notable changes to **make-lecture-kit**. This kit is built to keep improving:
every upgrade bumps `VERSION`, adds an entry here, and must pass
`python3 scripts/selfcheck.py`. See `references/upgrading.md` for the loop.

Format follows *Keep a Changelog*; versions follow semantic versioning.

## [2.2.2] — 2026-06-18

### Fixed
- **`README.md` "What's inside" map now lists every shipped file.** Two required
  files (verified present by `selfcheck.py`) were missing from the tree:
  `references/plain_language.md` — the easy-English rulebook that `SKILL.md` calls
  "read first" and that both linters enforce — and `scripts/_plain_language.py`,
  the shared word-list module those linters import. Docs-only change; no behaviour
  change.

## [2.2.1] — 2026-06-15

### Fixed
- **`scripts/figstyle.py` no longer emits `SyntaxWarning: invalid escape sequence
  '\i'`.** The module docstring contains LaTeX commands (`\includegraphics`) but
  was not a raw string, so Python warned on every run (seen during `selfcheck` /
  `publish.sh`) and a future Python would make it a hard `SyntaxError`. The
  docstring is now an `r"""…"""` raw string. No behaviour change.

## [2.2.0] — 2026-06-15

### Fixed
- **Each top-level topic now starts on a fresh page in the companion PDF.** A
  section heading could previously land at the bottom of a page with its content
  spilling across the break, splitting a topic in two. The template now clears
  the page before every section after the first (the first stays under the title
  banner) via a one-shot `\sectionbreak` flag in `templates/companion.tex` —
  robust regardless of titlesec's counter timing, and verified to coexist with
  the breakable `tcolorbox` callouts and `fancyhdr`. Documented in
  `references/companion_style.md` (visual contract).

## [2.1.0] — 2026-06-15

### Added
- **`AGENTS.md` at the repo root**, so the kit is discovered *natively* on all
  three target platforms. Google Jules reads `AGENTS.md` per task; OpenAI Codex,
  Cursor, and Gemini CLI read it too — alongside the existing `SKILL.md` that
  Claude and Codex auto-load. One repo now works first-class on Claude, Codex,
  and Jules.

### Changed
- **Install + "Staying updated" instructions rewritten** in `README.md` and
  `START_HERE.md` for Claude (Code + Cowork), Codex, and Jules: clone straight
  into the platform's skills folder (`~/.claude/skills`, `~/.agents/skills`),
  connect the repo for Jules, and stay current with one `git pull` /
  `python3 scripts/update.py` (Jules updates automatically by re-cloning).
- Refreshed the "What's inside" map to list `AGENTS.md`, `VERSION`,
  `CHANGELOG.md`, `update_source.txt`, and the `lint_tex.py` / `selfcheck.py` /
  `update.py` scripts.

## [2.0.0] — 2026-06-15

### Fixed
- **Worked-example "Step N." labels no longer spill outside the callout box.** A
  dedicated `steps` list reserves enough label width; the old raw `enumerate`
  overflowed its label past the frame. The linter now hard-fails the old pattern.
- **Cross-platform compile.** `bbding` is now optional (falls back to pifont
  `\ding{43}/{46}`), so the PDF builds on minimal TeX installs. And `build_pdf.py`
  no longer passes `latexmk` an option it rejects — that bug silently produced no
  PDF whenever latexmk was the chosen engine.

### Added
- **`references/plain_language.md`** — one shared rulebook for easy English
  (sentence ceiling, plain-word swaps, banned hand-waving, reading-level target),
  enforced by both linters.
- **`scripts/lint_tex.py`** — a language + layout gate for the companion PDF (which
  had none); wired into `build_pdf.py`.
- **Rich figure helpers in `figstyle.py`** — `contour`, `surface3d`,
  `function_plot` (+ tangent), `gradient_descent`, `vectors2d`, `heatmap`, `flow`,
  `annotated_sequence`, `bars`, plus a house colormap.
- **A "when to draw a plot" criterion + concept→plot map** (`companion_style.md`
  §5) and a **figure-coverage** check in `lint_tex.py`.
- **Glossary + symbol cheat-sheet** as a standard closing section (`companion_style`
  §8 + template).
- **Interactive HTML "signature" layer** (`lecture_style.md` §12): per-band recall
  checks, copy buttons, an end-of-lecture synthesis interactive.
- **`scripts/selfcheck.py`**, **`references/upgrading.md`**, **`VERSION`**, and this
  changelog — a safe, repeatable way to keep upgrading the kit.

### Changed
- **`scripts/lint.py`** tightened: 22-word sentence ceiling, shared word lists,
  reading-level estimate.
- **Platform-agnostic** wording and packaging throughout (Claude Code, Claude
  Cowork, OpenAI Codex, Google Jules, Cursor, or any agentic coding assistant).

## [1.0.0]

- Initial kit: companion PDF + complete interactive HTML lecture, five colour-coded
  callout boxes, the quality rubric, `figstyle.py`, `build_pdf.py`, and `lint.py`.
