# Changelog

All notable changes to **make-lecture-kit**. This kit is built to keep improving:
every upgrade bumps `VERSION`, adds an entry here, and must pass
`python3 scripts/selfcheck.py`. See `references/upgrading.md` for the loop.

Format follows *Keep a Changelog*; versions follow semantic versioning.

## [2.6.0] — 2026-06-29

### Changed
- **The reusable lessons are now wired into the workflow, so every generated kit
  benefits — not just Session 9.** Docs-only (no script/template behaviour change):
  an agent following `SKILL.md` now discovers and applies the 3-D and
  figure-intuition techniques wherever the *content* calls for them, instead of
  them living only in one worked lecture.
  - `SKILL.md` step 4 (companion) now points to `surface3d(path=...)` for 3-D
    landscapes and `gradient_descent(noise=...)` for SGD, plus the rule "every
    figure must teach the intuition its caption claims."
  - `SKILL.md` step 5 (lecture) now points to the `lecture_style.md` recipe catalog
    (§6 A–I, incl. **Recipe H** 3-D surfaces and **Recipe G** journey map) and the
    §12 signature layer — to apply where the lecture earns them, never by rote.
  - `references/companion_style.md` gains **§5.1 "Make the figure TEACH its one
    idea"** — generic legibility recipes (name the quantity, tie annotations to the
    curve, shade meaning, halo paths, magnify small effects honestly, show
    stochasticity honestly, go 3-D for shape).
  - `references/lecture_style.md` Recipe H generalised: 3-D is for *any* `z=f(x,y)`
    surface in any subject, not only loss landscapes.

### Notes
- `selfcheck.py` green (7/7). No specific lecture content is hardcoded into the
  template — the techniques live as instructions the LLM learns from and applies
  per lecture.

## [2.5.0] — 2026-06-29

### Added
- **`references/lecture_style.md` now documents the Session-9 visual upgrades as reusable
  recipes**, so every generated lecture can use them, not just Session 9:
  - **Recipe G** — a clickable big-picture **journey map** (canvas navigation: hover-highlight
    and click-to-jump to each band; nodes coloured from CSS vars to follow the theme).
  - **Recipe H** — pure-canvas 3-D made **non-convex**: a convex↔bumpy surface toggle with two
    start presets, so the student feels that the start decides which local minimum you reach.
    Includes the double-well surface model and the domain-clamp that keeps a big step on-grid.
  - **Recipe I** — **annotate + animate** a lab: a downhill direction arrow at the moving point,
    on-canvas landmark labels, and an `auto ▶` toggle that animates a run and stops at convergence.
  - **§12** gains a persistent **colour-legend** upgrade, plus the non-convex landscape and
    animated-lab patterns and the delegated "check yourself" recall-card handler.
- **New §10.1 — "Verify every demo actually runs."** A head-less harness pattern (stub the DOM +
  canvas, `eval` the page script, fire `load`, assert no `console.error`). The registry's `try/catch`
  turns a runtime throw into a silent blank panel, so a syntax check alone misses it; this codifies
  the fix for the `X.inv` blank-lab bug as a repeatable gate.

### Changed
- **§11 ship checklist** adds two gates: *demos verified (not just parsed)* and *colour legend +
  consistent accents*.

### Notes
- Docs-only change (guidance under `references/`); no script or template behaviour changed.
  `selfcheck.py` stays green (7/7). The patterns are already live in the gitignored
  `output/session9-gradient-descent/lecture.html`, which is the worked reference for all three recipes.

## [2.4.0] — 2026-06-29

### Added
- **Interactive 3-D in the lecture template** (`templates/lecture.html`): a new
  pure-canvas "roll the ball into the bowl" gradient-descent lab (`bowlCanvas`) —
  a rotatable 3-D loss surface with a live descent trail, drawn with only the 2-D
  canvas API. No chart/3-D library; still one self-contained file with MathJax as
  the only external dependency. Documented as a reusable pattern in
  `references/lecture_style.md` so generated lectures can copy it.
- **3-D + SGD figure helpers in `scripts/figstyle.py`**:
  - `surface3d(...)` redesigned — lit surface + faint wireframe, an optional floor
    "shadow" contour, and an optional `path=[(x,y), ...]` descent trail lifted onto
    the surface (the iconic ball-in-the-bowl PDF figure).
  - `gradient_descent(...)` gains `noise=` (turns batch GD into a visibly wandering
    SGD walk), `mark_min=`, a white-halo trail, and faint contour lines so the path
    always reads on the colour map.

### Changed
- **Sharper figures kit-wide** (`scripts/figstyle.py`): export DPI 150 → 220 for
  crisp text and lines, heavier default line weight with rounded joins, and
  white-facecolor saving. The bundled example and every session companion rebuild
  clean (no overfull boxes).
- The concept→plot map (`references/companion_style.md` §5) now documents
  `surface3d(path=...)` and `gradient_descent(noise=...)`.

### Notes
- `selfcheck.py` stays green (7/7). Local `output/` companions (gitignored) were
  regenerated to verify the new look — sessions 4, 5, 7, and 9 recompiled with no
  overfull boxes. Session 9's figures were also reworked locally so each conveys
  its intuition (SGD visibly wanders vs. batch glides, least-squares gaps labelled,
  bracketing tied to the curve, directional derivative shaded). Those live under
  the gitignored `output/`, so they stay in your working copy.

## [2.3.1] — 2026-06-29

### Fixed
- **`README.md` "What's inside" map now lists `templates/assets/`.** The
  `templates/assets/bits-logo.png` brand asset bundled in v2.3.0 was missing from
  the file tree, so the map no longer listed every shipped file. The tree now
  shows the `assets/` folder and the logo — the same kind of docs-completeness fix
  as v2.2.2. Docs-only change; no behaviour change.

## [2.3.0] — 2026-06-27

### Added
- **BITS Pilani branding on every generated kit**, so both deliverables look
  right for BITS WILP courses:
  - *Companion PDF* (`templates/companion.tex`): a white **"WILP, BITS Pilani"**
    wordmark in the navy title banner, an optional logo shown in a white chip
    beside it, a "Prepared for the Work Integrated Learning Programmes (WILP),
    BITS Pilani." credit line under the banner, and "WILP, BITS Pilani" in the
    running footer.
  - *Interactive lecture* (`templates/lecture.html`): the same wordmark + logo
    slot in the sidebar brand, a hero credit line, and the institute name in the
    `<title>`.
- **`templates/assets/bits-logo.png` — the BITS Pilani logo is bundled** (the
  transparent emblem extracted from the course slides) and shown in a white chip
  on the PDF banner and in the HTML sidebar. Replace that single file to change
  it; if it is removed, both templates fall back to the text wordmark
  automatically — an `\IfFileExists` guard in the template and an `onerror` hide
  in the HTML.

### Changed
- **`SKILL.md`** now instructs the agent to keep the BITS brand block intact
  while filling the per-lecture course/session/title fields.

### Notes
- Verified: the branded template compiles to a clean 3-page sample (no overfull
  boxes); `lint.py`, `lint_tex.py`, and `selfcheck.py` show no new failures.

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
