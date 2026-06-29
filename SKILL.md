---
name: make-lecture-kit
description: >-
  Turn ANY lecture (a slide deck in PDF or PPTX, notes, or just a topic) into two
  beginner-friendly study artifacts in an output/ folder: a professionally typeset
  companion PDF (LaTeX, navy banner, colour-coded callout boxes, matplotlib figures,
  every slide example worked in full) and a complete, very interactive HTML lecture
  you can play with. Plain easy English, analogies before the math, step-by-step
  intuition, worked examples, and interactions (including 3-D plots) that uncover
  each idea. No API keys and the student installs nothing: your agent session
  (Claude, Codex, Jules, Cursor, or any coding assistant) writes the .tex, makes the
  figures, compiles the PDF, and builds the page. Trigger on requests like: turn a
  lecture or slides into a companion PDF and an interactive lecture; make a study PDF
  for a topic; or explain a hard topic simply with worked examples.
---

# make-lecture-kit (student edition)

Give this skill a lecture and it produces, into `output/<session>/`:

1. **`companion.pdf`** — a real, professionally typeset study companion (built
   from `companion.tex` + matplotlib figures with LaTeX). Colour-coded callout
   boxes, clean math, worked examples in full. This is the primary deliverable.
2. **`lecture.html`** — a complete, very detailed, very interactive lecture: the
   *entire* lecture rebuilt as a story-driven web page, every concept covered in
   depth, with working interactions that let the learner *play* with each idea
   and watch the intuition appear.

**The student installs nothing and manages no toolchain.** You — the host agent
(Claude Code, Claude Cowork, OpenAI Codex, Google Jules, Cursor, or any other
agentic coding assistant) — author everything and compile the PDF yourself. Most
agent sandboxes already have TeX Live + matplotlib, so the PDF compiles directly.
Everything here is plain `SKILL.md` + standard LaTeX + standard-library Python, so
it runs the same on every platform. No API keys, no secrets, ever.

---

## The five non-negotiable rules (this is what makes it good)

Read `references/quality_rubric.md` fully first; self-score against it before you finish.

1. **Easy language.** Simple, common words. Short sentences (aim 15 words, ceiling 22). Define every new term the first time; spell out every symbol and acronym. Write for a smart person meeting this topic for the *first* time. No academic fog, no literary flourishes, no hand-waving. The binding rulebook is `references/plain_language.md`; the linters enforce it.
2. **Analogies that stick.** Every tricky idea gets a relatable, real-life analogy in plain language *before* the math (the "Everyday picture" box).
3. **Math intuition, simply detailed.** Build every formula up step by step — nothing skipped, every symbol named. Explain *why*, not just *what*.
4. **Fully solved examples, generously.** Wherever an example helps a concept land, include one (often more than one). Work **every slide example out in full**, every step, real numbers. Never "it can be shown that".
5. **Interaction uncovers intuition (visualizer).** Each control must *reveal* something — move a slider and watch the idea change, step through and see the derivation build, toggle and expose the picture. Not decoration.

Plus the **no-clutter / no-overflow contract**: nothing overlaps, no text runs off the page (no Overfull `\hbox`; wrap long math in `align`/`split`; wide tables via `adjustbox`/`booktabs`), worked examples stay coherent, the HTML is fully responsive.

---

## Workflow

### 1. Read the references first
- `references/plain_language.md` — **the easy-English rulebook (read first):** plain-word
  swaps, banned hand-waving, sentence ceiling, reading-level target. The linters enforce it.
- `references/quality_rubric.md` — the bar + the ship checklist (both deliverables)
- `references/companion_style.md` — how to expand slides into the LaTeX companion
- `references/lecture_style.md` — how to build the complete interactive lecture
- `references/intuition_playbook.md` — analogies, mental models, ML/AI connections

### 2. Read the input lecture
The input is usually a **slide deck** (PDF/PPTX) — but may be notes or just a topic. Read it with your own document ability (or a PDF/PPTX skill). List **every concept** to teach and **every slide example** to work out in full, in a sensible order (simple → hard, prerequisites first).

### 3. Pick a slug and make the output folder
Choose a short kebab slug (e.g. `session6-distributions`, `eigenvectors`) and create `output/<slug>/` and `output/<slug>/figures/`.

### 4. Author the companion → `output/<slug>/companion.pdf`
1. Copy `templates/companion.tex` to `output/<slug>/companion.tex`. Fill the banner/header placeholders (`{{COURSE_SHORT}}`, `{{SESSION}}`, `{{LECTURE_TITLE}}`). **Keep the BITS brand as shipped:** the "WILP, BITS Pilani" banner wordmark, the footer line, the credit line under the banner, and the optional `assets/bits-logo.png` logo slot are fixed institute branding — only the course/session/title fields change.
2. For **each** concept, walk the full teaching spine in plain words, using the colour-coded callout boxes:
   > **Hook** (real-life) → **`\begin{intuition}`** (analogy + mental model) → **the math, step by step** → **`\begin{worked}` fully-solved example(s)** with real numbers → **`\begin{everyday}`** real-world picture → ML/AI connection → a **figure** (visual intuition) → **`\begin{watchout}`** pitfalls → **`\begin{keytake}`** recap.
   Work out **every example from the slides** in full.
3. Make figures — **draw a plot wherever a concept is visual** (a function, a loss surface, a distribution, a vector, a matrix, a process, a tagged sequence, a comparison, or any worked example whose numbers can be drawn). This is the default, not a nice-to-have. Write `output/<slug>/figures/*.py` that `import figstyle` and call the helper matching the concept — `contour`/`surface3d` for landscapes, `function_plot(...tangent_at=)` for derivatives/Taylor, `gradient_descent` for optimization, `pmf_bar`/`shaded_normal` for distributions, `vectors2d` for embeddings, `heatmap` for matrices, `flow` for pipelines/agent loops, `annotated_sequence` for tagged sentences, `bars` for comparisons. Save PNGs and reference them with `\housefig{figures/xyz.png}{caption with a one-line "how to read it"}`. See `references/companion_style.md` §5 for the full concept→plot map. Reach for 3-D where a concept is a **surface/landscape** in *any* subject — `surface3d(f, xlim, ylim, path=[...])` draws the lit "ball-in-the-bowl" with the descent path on it — and `gradient_descent(..., noise=)` for an SGD wander. **Every figure must teach the intuition its caption claims:** §5.1 lists the legibility recipes (name the quantity on the plot, tie annotations to the curve, shade the meaning, magnify small effects honestly, go 3-D for shape). Cover the caption — if a beginner can't read the idea off the picture, fix the figure.
4. Compile to PDF (run from the skill root, so figure scripts can import
   `figstyle` from `scripts/`):
   ```bash
   python3 scripts/build_pdf.py output/<slug>/companion.tex
   ```
   `build_pdf.py` runs the figure scripts, compiles with `latexmk`/`pdflatex`, writes `output/<slug>/companion.pdf`, reports any Overfull-box / reference warnings, and then runs `scripts/lint_tex.py` on the source — the companion's language + layout gate (long sentences, fancy words, banned hand-waving, raw `Step`-label enumerates, un-resized wide tables). Fix every FAIL and rebuild. Use the `steps` environment for all worked-example steps so "Step N." never spills outside its box. If the environment has no TeX engine, `build_pdf.py` prints clear guidance (most agent sandboxes have TeX Live; otherwise install TinyTeX) and leaves the `.tex` + figures ready — it never fails silently. You can also run the language gate alone: `python3 scripts/lint_tex.py output/<slug>/companion.tex`.

### 5. Author the complete lecture → `output/<slug>/lecture.html`
Start from `templates/lecture.html` (a working 3-chapter demo — its chapters set the depth bar; replace them with the real lecture's chapters). Rebuild the **entire** lecture as a connected **story** — a grouped sidebar TOC, one chapter per concept, cover **everything**, drop nothing. Each concept gets the full detailed treatment *and* a **bespoke hand-drawn `<canvas>` lab** with 2+ working controls that *uncover* the intuition (slider→watch the idea change, step→build it up, toggle→reveal the structure) — use the template's `makeSlider`/`setupCanvas` helpers; don't reach for chart libraries. Match each lab to a recipe in `references/lecture_style.md` §6 (A–I) — including **Recipe H** for a rotatable pure-canvas **3-D surface** (any `z=f(x,y)`, no library) and **Recipe G** for a clickable big-picture map — and, where the content earns it, layer on the **§12 signature upgrades** (a non-convex 3-D landscape that makes *local minima* real, animated/annotated labs, per-band recall cards, a persistent colour legend). Apply these where the *lecture* calls for them, never by rote. All math via MathJax (the only external dependency). Dark, clean, responsive, nothing overlapping. Then gate it:
```bash
python3 scripts/lint.py output/<slug>/lecture.html
```
`lint.py` fails on template-hygiene leaks (broken comments, leftover `{{placeholders}}`), possible overflow, long sentences, fancy-word / banned hand-waving prose, prose that reads above ~grade 9, blocked math, missing interactivity, any non-CDN dependency, or leaked secrets. Fix every FAIL and re-run until it passes. Also replace the `<title>` tag and every demo-chapter remnant — the shipped page must be entirely about the student's lecture. **Keep the BITS brand:** the sidebar "WILP, BITS Pilani" wordmark + logo slot and the hero credit line stay; set `<title>` to "WILP, BITS Pilani · &lt;lecture title&gt;".

### 6. Finish honestly
Tell the learner what landed in `output/<slug>/` and which checks passed. If `build_pdf.py` couldn't compile here (no TeX engine in this environment), say so plainly and give the exact next step — **don't claim a `companion.pdf` exists if it doesn't.** Then self-score against `references/quality_rubric.md`.

---

## Maintaining, versioning & distribution

This kit is a living skill — it is meant to keep improving, and everyone using it
should be able to pull the latest. Three pieces make that safe and easy:

- **`VERSION` + `CHANGELOG.md`** — the current version and what changed each release.
- **`scripts/selfcheck.py`** — one command that verifies the whole kit is healthy
  (files present, scripts compile, figures render, both linters run, the bundled
  example passes). Run it after any change; it must be green before you ship.
- **`scripts/update.py`** — how end users fetch the latest. It does `git pull` if the
  kit was cloned, otherwise downloads the published zip named in `update_source.txt`.
  Generating companions stays fully offline; only this command touches the network,
  and only on purpose. A user's `output/` is never overwritten.

**The upgrade + release loop is in `references/upgrading.md`** (make the change →
`selfcheck.py` → bump `VERSION` + `CHANGELOG.md` → publish). To hand the kit to others,
package it as a folder/zip (place it where the agent reads skills) or, for Cowork, as
a `.skill` bundle (a zip of the kit with `SKILL.md` at its root) that installs with one
click. To distribute updates, publish via a git repo or a stable zip URL so students
run `python3 scripts/update.py` and always have the newest version.

## Works everywhere
Plain `SKILL.md`, standard LaTeX, matplotlib, and standard-library Python — runs unchanged on **any agentic coding platform**: **Claude Code**, **Claude Cowork**, **OpenAI Codex**, **Google Jules**, **Cursor**, and the like. Nothing is platform-specific: no proprietary tools, no API keys, no network at author time. See `README.md` for the one-line install in each. The companion PDF compiles wherever TeX Live exists (most agent sandboxes have it; otherwise TinyTeX); the lecture page needs only a browser.
