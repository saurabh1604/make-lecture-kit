---
name: make-lecture-kit
description: >-
  Turn ANY learning input — a single topic, a list of topics, notes or study
  material, PDFs, or slide decks (PPT/PPTX) — into two beginner-friendly study
  artifacts in an output/ folder: a professionally typeset companion PDF (LaTeX,
  a calm one-accent design, labelled callout boxes, clean matplotlib figures) and a complete, very interactive
  HTML lecture. Everything is explained with intuition first: everyday analogies,
  real-life examples, and step-by-step walkthroughs of fully worked examples, in
  plain English anyone can follow. Slides are optional; with only a topic, the kit
  designs the syllabus and examples itself. No API keys and the learner installs
  nothing: the agent session (Claude, Codex, Jules, Cursor, or any coding
  assistant) writes the .tex, makes the figures, compiles the PDF, and builds the
  page. Trigger on requests like: explain a topic simply with a companion PDF and
  an interactive page; make study material for these topics; turn my notes, PDF or
  slides into a study kit; or explain a hard topic with worked examples.
---

# make-lecture-kit

Give this skill **anything a learner wants to understand** — a topic, a list of
topics, notes, a book chapter, a PDF, a slide deck — and it produces, into
`output/<slug>/`:

1. **`companion.pdf`** — a professionally typeset study companion (built from
   `companion.tex` + matplotlib figures with LaTeX). A calm, one-accent design, labelled callout boxes,
   clean math, everyday analogies, and every example walked through step by step.
2. **`lecture.html`** — a complete, very interactive lecture: the whole topic
   rebuilt as a story-driven web page, every concept covered in depth, with working
   interactions that let the learner *play* with each idea and watch the intuition
   appear.

**No slides needed.** With only a topic, you design the teaching plan, the
analogies and the worked examples yourself (`references/source_modes.md`). With
material, the material is the floor, not the ceiling: you cover all of it and fill
in the steps, intuition and examples it leaves out.

**The learner installs nothing and manages no toolchain.** You — the host agent
(Claude Code, Claude Cowork, OpenAI Codex, Google Jules, Cursor, or any other
agentic coding assistant) — author everything and compile the PDF yourself. Most
agent sandboxes already have TeX Live + matplotlib, so the PDF compiles directly.
Everything here is plain `SKILL.md` + standard LaTeX + standard-library Python, so
it runs the same on every platform. No API keys, no secrets, ever. The kit carries
**no institute branding**: the header shows a series name and the topic title only.

---

## The seven non-negotiable rules (this is what makes it good)

Read `references/quality_rubric.md` fully first; self-score against it before you finish.

1. **Easy language.** Simple, common words. Short sentences (aim 15 words, ceiling 22). Define every new term the first time; spell out every symbol and acronym. Write for a smart person meeting this topic for the *first* time. No academic fog, no literary flourishes, no hand-waving. The binding rulebook is `references/plain_language.md`; the linters enforce it.
2. **Simple things stay simple.** Match the size of the explanation to the size of the idea. Before writing any concept, find the **single most intuitive way in** — the best everyday example, the clearest picture — and lead with it. If an idea is easy, say it in two or three short sentences and move on: no stacked analogies, no ceremony, no five-step build-up for a one-step idea. Save the depth for where the difficulty really lives. Never make a simple thing look hard to seem thorough. (The right-sizing rules live in `references/plain_language.md` §8.)
3. **Analogies that stick — in ONE story-world.** Every tricky idea gets a relatable, real-life analogy in plain language *before* the math (the "Everyday picture" box). One analogy — the best one — not a pile. Pick a single story-world for the whole lecture (a detective case, a kitchen, a factory) and draw analogies from inside it; give recurring objects short plain nicknames ("clues", "silent moves", "the staircase"), used consistently in both artifacts and decoded in a closing `friendly → textbook` table (`plain_language.md` §9, `intuition_playbook.md` §A).
4. **Math intuition, simply detailed.** Build every formula up step by step — nothing skipped, every symbol named. Explain *why*, not just *what*. For a topic with little or no math (history, biology, law, design), the same rule applies to the **mechanism**: walk the cause → effect chain one plain step at a time, and use timelines, tables and diagrams where you would have used equations.
5. **Fully solved examples, generously — walked through step by step.** Every concept gets at least one worked example (hard ones get two or more), with simple, clean numbers and every step shown and explained in one plain line. Work **every example in the source material** out in full; when there is no source, **design** the examples yourself (`source_modes.md` §3) and compute every number with code. Mix real-life examples with exam-style ones. Never "it can be shown that".
6. **Interaction uncovers intuition (visualizer).** Each control must *reveal* something — move a slider and watch the idea change, step through and see the derivation build, toggle and expose the picture. Not decoration. When the lecture's heart is a **procedure**, go beyond watching: build the **goal game** (`lecture_style.md` §6 Recipe J) — the student performs the algorithm's legal moves on a live board, with a win detector, a hint, and a reset.
7. **Lead with the whole idea — and open by doing.** Every section/chapter starts with its **one-liner**: the whole idea in one or two plain sentences (PDF: `\secsub{...}`; HTML: the lead's first sentence) — reading only titles + one-liners should give the lecture's skeleton. Titles are **headlines** that state the claim ("The undo button — and how it breaks"), never bare labels ("The Inverse"). And the artifact itself opens by **doing**: the first section hands the student the central skill in miniature, before any definitions, then names what they just did — never an agenda-first opening. Close like a coach: a short self-test with hidden answers, then the whole lecture on one **pocket card** (`companion_style.md` §8; `lecture_style.md` §12.9).

Plus the **quiet-design contract**: ink plus ONE accent colour everywhere (PDF, page and canvases); figures use at most two colours, no title inside the image, few labels, lots of air; boxes are told apart by their label, not by colour (`companion_style.md` §0, `lecture_style.md` §9). And the **no-clutter / no-overflow contract**: nothing overlaps, no text runs off the page (no Overfull `\hbox`; wrap long math in `align`/`split`; wide tables via `adjustbox`/`booktabs`), worked examples stay coherent, the HTML is fully responsive.

---

## Workflow

### 1. Read the references first
- `references/plain_language.md` — **the easy-English rulebook (read first):** plain-word
  swaps, banned hand-waving, sentence ceiling, reading-level target. The linters enforce it.
- `references/quality_rubric.md` — the bar + the ship checklist (both deliverables)
- `references/companion_style.md` — how to write the LaTeX companion
- `references/lecture_style.md` — how to build the complete interactive lecture
- `references/source_modes.md` — **how to turn any input (topic, topic list, notes, PDF, slides) into the concept inventory**
- `references/intuition_playbook.md` — analogies, mental models, real-world and ML/AI connections

### 2. Understand the input → build the concept inventory
Read **`references/source_modes.md`** and follow the mode that matches what the user gave you:

| Input | What you do |
|---|---|
| **One topic** | Design the syllabus yourself: the one question it answers, scope, prerequisites, a simple → hard concept ladder, fact-checked content, and your own worked examples with clean numbers. |
| **A list of topics** | Order by prerequisites; one kit per topic (default, `output/<series>/<nn>-<topic>/`) or one combined kit when the topics are short, linked steps. Say which. |
| **Notes / study material / PDFs / PPTs / DOCX** | Read every page. Extract every concept, formula and example. Then fill the gaps: missing steps, missing intuition, assumed prerequisites, and examples for concepts that have none. |
| **A mix** | Documents are the main source; the topic list sets the scope. |

Fix the audience (default: a smart first-timer; adapt if the user states a level). Then write the **concept inventory** (`source_modes.md` §7): every concept with the question it answers, easy/hard, prerequisites, the best everyday way in, its examples (from the source ✦ or designed ✧), a figure/lab idea — plus the story-world + nickname lexicon, the symbol list, the common misconceptions, and a **"where it's used"** link per concept in the topic's own field. An easy concept gets a short, direct treatment (rule 2); a hard one gets the full spine with room to breathe.

### 3. Pick a slug and make the output folder
Choose a short kebab slug (e.g. `eigenvectors`, `probability-distributions`, `photosynthesis`) and create `output/<slug>/` and `output/<slug>/figures/`. For a series, use `output/<series>/<nn>-<topic>/`.

### 4. Author the companion → `output/<slug>/companion.pdf`
1. Copy `templates/companion.tex` to `output/<slug>/companion.tex`. Fill the banner/header placeholders: `{{SERIES_NAME}}` (a course name the user gave, the subject area, or simply "Study Companion"), `{{TOPIC_TITLE}}`, `{{ONE_LINE_SUBTITLE}}`, and `{{META_LINE}}` (what it was built from + the promise, e.g. "Built from: your notes on X · Every example worked out in full" or "From first principles · Every example worked out in full"). Add no institute names or logos unless the user asks for them.
2. For **each** concept, walk the full teaching spine in plain words, using the labelled callout boxes:
   > **`\secsub{one-liner}`** (the whole idea, right under the headline title) → **Hook** (real-life) → **`\begin{intuition}`** (analogy + mental model) → **the math, step by step** → **`\begin{worked}` fully-solved example(s)** with real numbers → **`\begin{everyday}`** real-world picture → **`\begin{waitwhat}`** only where the material earns an honest surprise → **where it's used** (in the topic's own field — ML/AI for an ML topic, medicine for biology, money for finance, daily life otherwise) → a **figure** (visual intuition) → **`\begin{watchout}`** pitfalls → **`\begin{keytake}`** recap.
   Work out **every source example** in full, plus the examples you designed for concepts that had none. Open the whole companion by **doing** (rule 7), and end with the closing arc: self-test (`\flipanswer` upside-down answers) → one-page pocket card → glossary with nickname decoder → symbol cheat-sheet (`companion_style.md` §8).
3. Make figures — **draw a plot wherever a concept is visual** (a function, a loss surface, a distribution, a vector, a matrix, a process, a tagged sequence, a comparison, or any worked example whose numbers can be drawn). This is the default, not a nice-to-have. Write `output/<slug>/figures/*.py` that `import figstyle` and call the helper matching the concept — `contour`/`surface3d` for landscapes, `function_plot(...tangent_at=)` for derivatives/Taylor, `gradient_descent` for optimization, `pmf_bar`/`shaded_normal` for distributions, `vectors2d` for embeddings, `heatmap` for matrices, `flow` for pipelines/agent loops, `annotated_sequence` for tagged sentences, `bars` for comparisons. Save PNGs and reference them with `\housefig{figures/xyz.png}{caption with a one-line "how to read it"}`. See `references/companion_style.md` §5 for the full concept→plot map. Reach for 3-D where a concept is a **surface/landscape** in *any* subject — `surface3d(f, xlim, ylim, path=[...])` draws the lit "ball-in-the-bowl" with the descent path on it — and `gradient_descent(..., noise=)` for an SGD wander. **Every figure must teach the intuition its caption claims:** §5.1 lists the legibility recipes (name the quantity on the plot, tie annotations to the curve, shade the meaning, magnify small effects honestly, go 3-D for shape). Cover the caption — if a beginner can't read the idea off the picture, fix the figure.
4. Compile to PDF (run from the skill root, so figure scripts can import
   `figstyle` from `scripts/`):
   ```bash
   python3 scripts/build_pdf.py output/<slug>/companion.tex
   ```
   `build_pdf.py` runs the figure scripts, compiles with `latexmk`/`pdflatex`, writes `output/<slug>/companion.pdf`, reports any Overfull-box / reference warnings, and then runs `scripts/lint_tex.py` on the source — the companion's language + layout gate (long sentences, fancy words, banned hand-waving, raw `Step`-label enumerates, un-resized wide tables). Fix every FAIL and rebuild. Use the `steps` environment for all worked-example steps so "Step N." never spills outside its box. If the environment has no TeX engine, `build_pdf.py` prints clear guidance (most agent sandboxes have TeX Live; otherwise install TinyTeX) and leaves the `.tex` + figures ready — it never fails silently. You can also run the language gate alone: `python3 scripts/lint_tex.py output/<slug>/companion.tex`.

### 5. Author the complete lecture → `output/<slug>/lecture.html`
Start from `templates/lecture.html` (a working 3-chapter demo — its chapters set the depth bar; replace them with the real chapters from your concept inventory). Build the **entire** topic as a connected **story** — a grouped sidebar TOC, one chapter per concept, cover **everything**, drop nothing. Each concept gets the full detailed treatment *and* a **bespoke hand-drawn `<canvas>` lab** with 2+ working controls that *uncover* the intuition (slider→watch the idea change, step→build it up, toggle→reveal the structure) — use the template's `makeSlider`/`setupCanvas` helpers; don't reach for chart libraries. Match each lab to a recipe in `references/lecture_style.md` §6 (A–J) — including **Recipe H** for a rotatable pure-canvas **3-D surface** (any `z=f(x,y)`, no library), **Recipe G** for a clickable big-picture map, and **Recipe J**, the goal game, when the lecture's heart is a procedure — and, where the content earns it, layer on the **§12 signature upgrades** (a non-convex 3-D landscape that makes *local minima* real, animated/annotated labs, per-band recall cards, a persistent colour legend, the final-boss quiz + one-card-to-keep ending). Apply these where the *lecture* calls for them, never by rote. Math via MathJax (the only external dependency) — or, when the lecture's notation is genuinely one-dimensional, the zero-dependency hand-styled option in `lecture_style.md` §7.3. Quiet theme (ink + one accent, light by default, dark on a click; canvases read their colours from the theme tokens), clean, responsive, nothing overlapping. Then gate it:
```bash
python3 scripts/lint.py output/<slug>/lecture.html
```
`lint.py` fails on template-hygiene leaks (broken comments, leftover `{{placeholders}}`), possible overflow, long sentences, fancy-word / banned hand-waving prose, prose that reads above ~grade 9, blocked math, missing interactivity, any non-CDN dependency, or leaked secrets. Fix every FAIL and re-run until it passes. Also replace the `<title>` tag (just the topic title), the sidebar brand text (the series name, or "Study Kit"), the hero `.source-line` (what it was built from), and every demo-chapter remnant — the shipped page must be entirely about the learner's topic.

### 6. Finish honestly
Tell the learner what landed in `output/<slug>/`, which input mode you used (and any assumption you made about scope or audience), and which checks passed. If `build_pdf.py` couldn't compile here (no TeX engine in this environment), say so plainly and give the exact next step — **don't claim a `companion.pdf` exists if it doesn't.** Then self-score against `references/quality_rubric.md`.

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
click. To distribute updates, publish via a git repo or a stable zip URL so learners
run `python3 scripts/update.py` and always have the newest version.

## Works everywhere
Plain `SKILL.md`, standard LaTeX, matplotlib, and standard-library Python — runs unchanged on **any agentic coding platform**: **Claude Code**, **Claude Cowork**, **OpenAI Codex**, **Google Jules**, **Cursor**, and the like. Nothing is platform-specific: no proprietary tools, no API keys, no network at author time. See `README.md` for the one-line install in each. The companion PDF compiles wherever TeX Live exists (most agent sandboxes have it; otherwise TinyTeX); the lecture page needs only a browser.
