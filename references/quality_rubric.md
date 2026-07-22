# quality_rubric.md — Shared quality bar for the Companion PDF AND the Lecture HTML

Two artifacts, one standard. The **companion PDF** is the written study doc; the **lecture HTML** is the
interactive experience. They are siblings of the same lecture and must teach the **same concepts at the
same depth** in the same easy voice. This rubric scores both, flags what's missing, and lists the things
that must **never** ship.

Use it twice: once while drafting (as a spec), once at the end (as a gate). Both artifacts must clear
**85/100** to ship. Any red-list item below is an automatic fail regardless of score.

---

## A. How to score (0–100)

Score each category, sum, then apply the red-list. Columns marked **(HTML)** apply only to the lecture
page; **(PDF)** only to the companion; unmarked rows apply to both.

| # | Category | Weight | What full marks looks like |
|---|----------|:------:|----------------------------|
| 1 | **Completeness / coverage** | 16 | Every concept in the lecture is present, one section/chapter each, in teaching order. Every slide example is worked in full. Nothing dropped, nothing merged away. |
| 2 | **Teaching spine (9 steps)** | 12 | Every concept has all 9 steps: Hook → Intuition → Formalize → Worked Example → Real-World → ML/AI → Visual → Pitfalls → Recap+Bridge. Right callout per step. |
| 3 | **Easy language** | 12 | Short sentences (aim 15, ceiling 22 words). Plain words — no fancy-word offenders or literary fog (`plain_language.md` §3). No banned hand-waving (§4). Each term defined on first use; every symbol/acronym spelled out. Analogy before algebra. Reads at ~grade 9. A smart beginner never gets lost. **Right-sized** (`plain_language.md` §8): simple ideas told simply and briefly, via the most intuitive way in — no manufactured complexity. |
| 4 | **Relatable analogies** | 8 | Every tricky idea has one concrete, plain-language analogy that actually maps to the math (not a vibe). |
| 5 | **Step-by-step math intuition** | 12 | Every formula built up from scratch; every symbol named the moment it appears; no leaps. Wide math contained (HTML: `.eqbox`; PDF: `align`/`split`), never overflowing. |
| 6 | **Generous worked examples** | 14 | At least one fully-solved example per concept, with **real numbers** and **every step shown**. Final numbers highlighted. Zero "it can be shown that". |
| 7 | **Interactivity that uncovers intuition (HTML)** | 12 | Every major concept has 2+ working interactions that reveal the idea (not decoration). All run from `file://`. (PDF: redistribute this weight to #5 and #6.) |
| 8 | **No-clutter / no-overflow contract** | 8 | Clean and unbroken 360→1440px (HTML) / clean A4 (PDF). Nothing overlaps; no horizontal overflow; everything breathes. (Enumerated in Section C.) |
| 9 | **Readability** | 4 | Typographic hierarchy, generous spacing, scannable. Eye always knows where to go. |
| 10 | **Story / flow** | 2 | Hook opener; each concept bridges to the next; the whole reads as one lecture, not a pile of parts. |
|   | **Total** | **100** | |

**Banding:** 95–100 exemplary · 85–94 ship · 70–84 revise (fix the lowest two categories) · <70 rebuild.
For the PDF, move category #7's 12 points to #5 (+6) and #6 (+6), since it has no live interaction.

---

## B. Per-concept detailed spine (must hold for EVERY concept in BOTH artifacts)

For each concept, verify all are present and pull their weight:

0. **One-liner + headline title** — the section/chapter opens with the whole idea in one
   or two plain sentences (PDF: `\secsub{...}` under the heading; HTML: the `.lead`'s
   first sentence), and the title is a **claim/action/payoff**, not a bare topic label
   ("The undo button — and how it breaks", not "The Inverse"). Reading only titles +
   one-liners should hand over the lecture's skeleton.
1. **Hook** — 3–5 sentences, a scene/story, makes the reader want the idea. No math yet.
2. **Intuition** — the idea in plain words + one analogy. PDF: `intuition` box. HTML: a `.note`.
3. **Formalize** — math built step by step; **every symbol named**; headline equation set off
   clearly. Wide math contained (HTML: `.eqbox`; PDF: `align`/`split`).
4. **Worked Example** — the slide's example, **every step, real numbers**, final number bold.
   PDF: `worked` box with "Step n." list. HTML: a `.key`/`.card` with numbered steps — and ideally
   a step-through/calculator lab that replays these exact steps live.
5. **Real-World** — an everyday situation using this exact idea. PDF: `everyday` box.
6. **ML / AI Connection** — where it lands in ML/AI, concrete and short. **Mandatory in every concept.**
7. **Visual Intuition** — a figure wherever the concept is visual (a function,
   surface/landscape, distribution, vector, matrix, process, tagged sequence,
   comparison, or any worked example whose numbers can be drawn). Pick the plot
   that matches the concept (companion_style §5 concept→plot map). PDF: a
   matplotlib `\housefig` (or inline tikz) + a "how to read it" caption line.
   HTML: the bespoke canvas `.lab` + a one-line "what to look for".
8. **Pitfalls** — 2–4 traps, each one short sentence. PDF: `watchout` box.
9. **Recap + Bridge** — one-line recap + one-line hand-off. PDF: `keytake` box closes the section.

If a concept is missing any of these (especially **Worked Example** or **ML/AI**), category #2 cannot score
above half, and #1 likely loses points too.

---

## C. The no-clutter / no-overflow contract (checkable items)

Every item is a yes/no. Any "no" drops category #8 to zero and may trip the red-list.

**Shared (both artifacts)**
- [ ] No text overflows its container; long tokens wrap (`overflow-wrap:anywhere; word-break:break-word`).
- [ ] No element overlaps another; nothing is clipped or hidden behind another box.
- [ ] Wide display math is contained and scrolls **in its own box**, never the page
      (`.eqbox{overflow-x:auto}`, `mjx-container[display="true"]{overflow-x:auto;max-width:100%}`).
- [ ] Tables wrapped in an `overflow-x:auto` container; cells wrap (`word-break:break-word`).
- [ ] Code blocks wrap or scroll in-box (`pre{overflow-x:auto}`, `code{white-space:pre-wrap}`).
- [ ] Generous, consistent spacing between sections, callouts, and figures — the page breathes.
- [ ] Callouts/figures/worked examples are never split awkwardly (PDF: `break-inside:avoid`).

**Lecture HTML only**
- [ ] **Responsive 360→1440px:** no horizontal page scroll at any width (`html,body{overflow-x:hidden}` as
      backstop, real cause fixed).
- [ ] Two-column layouts collapse to one column on mobile (grid breakpoint ~768px).
- [ ] Controls (sliders, buttons, inputs) **stack/wrap** on mobile (`flex-wrap:wrap`); none overflow.
- [ ] Every chart/canvas **resizes** with the viewport (Plotly `{responsive:true}`; canvas re-reads
      `clientWidth` on `resize`).
- [ ] Sticky nav wraps or collapses on small screens; never overflows or overlaps content.

**Companion PDF only**
- [ ] Clean A4 print: margins respected, no content bleeding off the page, page breaks fall sensibly.
- [ ] Figures sized to fit the column; no cut-off SVGs.
- [ ] Worked-example **steps use the `steps` environment** — every "Step N." label sits
      inside the callout, never spilling past its left frame.
- [ ] Every table/equation/figure **inside a callout** fits the box width (`\resizebox` /
      `align` as needed); nothing pokes out of a box.

---

## D. Easy-language audit (sample 5 paragraphs at random)

The binding rules are in `references/plain_language.md`; the linters (`lint.py` for HTML,
`lint_tex.py` for the companion) check them automatically. For each sampled paragraph, all
must be true:
- [ ] Most sentences ≤ 15 words; none over ~22; the longest is split, not run-on.
- [ ] Plain words throughout — no fancy-word offenders (`plain_language.md` §3) and no
      literary flourishes ("dissolve into", "the machinery of", …).
- [ ] No banned hand-waving (`plain_language.md` §4): "clearly", "obviously", "it can be
      shown", "left to the reader", etc.
- [ ] Every technical term is defined on first use, inline, in plain words; every symbol and
      acronym is spelled out the first time.
- [ ] An analogy or plain restatement appears before the first formula of the concept.
- [ ] A smart beginner with no prior exposure could follow it cold; it reads at ~grade 9.
- [ ] The explanation is **right-sized** (`plain_language.md` §8): an easy idea is told in a
      few short sentences with at most one analogy — no stacked analogies, no ceremony,
      no padded build-up that makes a simple thing look hard.

If 2+ sampled paragraphs fail, category #3 cannot exceed half. Any banned hand-waving phrase
is also a red-list item (Section H).

---

## E. Worked-example audit (check EVERY worked example)

- [ ] States the concrete inputs (numbers) up front.
- [ ] Shows **every** arithmetic/algebraic step — no skipped lines, no "it can be shown that".
- [ ] Names every symbol used in the computation.
- [ ] Highlights/bolds the result of each step and the final answer.
- [ ] Ends with a one-sentence "so what" tying the number to the intuition.
- [ ] (HTML) If an interaction replays the example, the static steps and the interactive steps **agree**.

A single worked example with a skipped step fails category #6 below ship threshold.

---

## F. Interactivity audit (HTML only — check EVERY interaction)

- [ ] It **runs** when the file is opened by double-click from `file://` (no module errors, no console
      throws).
- [ ] It **uncovers an idea**: name the one thing the student understands after using it that they didn't
      before. If you can't name it, the interaction is decoration — cut or replace it.
- [ ] It updates **live** and stays smooth (one `draw(state)` function per canvas, redrawn on input;
      `requestAnimationFrame` for animation loops).
- [ ] Injected math is re-typeset (`MathJax.typesetPromise([node])`).
- [ ] Each major concept has **2+** such interactions.
- [ ] The interaction is initialized on load (no blank widget before first input).

---

## G. Self-contained / dependency audit (HTML only)

- [ ] **One** `.html` file; opens by double-click; no build step, no server, no backend.
- [ ] All external libs from **cdn.jsdelivr.net / cdnjs.cloudflare.com / unpkg.com / cdn.plot.ly** only.
- [ ] **No** `type="module"` script tags (they break on `file://`). UMD/global scripts only.
- [ ] **No** API keys, **no** `fetch` to private/localhost hosts, **no** secrets.
- [ ] MathJax is **v3** from CDN and renders all math.

---

## H. DO NOT SHIP IF (red-list — any one is an automatic fail)

- A concept from the lecture is **left out**, or a slide example is **not worked in full**.
- A worked example **skips steps** or says **"it can be shown that"**.
- Any **text overflow, clutter, or overlap**; any **horizontal page scroll** at any width (HTML); any
  content **bleeding off** the A4 page (PDF).
- (HTML) Any interaction is **broken** (errors on `file://`) or **decorative only** (reveals no idea).
- **Math does not render** (MathJax misconfigured / not loaded).
- (HTML) Any **non-CDN** or **keyed** dependency, a `type="module"` script, or a `fetch` to a private host.
- The **ML/AI connection is missing** from any concept.
- Sentences are long and jargon-dense such that a smart beginner gets lost (category #3 < half).
- Any **banned hand-waving phrase** ("it can be shown", "clearly", "obviously", "left to the
  reader", …) appears anywhere (`plain_language.md` §4).
- (PDF) A worked-example **"Step N." label spills outside its callout box**, or any content
  (table, equation, figure) **overflows a box frame** or the page margin.

---

## I. Ship checklist (final gate — tick all, then ship)

- [ ] **Coverage:** every concept present, one section/chapter each, teaching order; every slide example
      worked in full.
- [ ] **Spine:** all steps in every concept (incl. the opening one-liner), correct callout per step,
      ML/AI in every one.
- [ ] **Opens by doing:** the first section/chapter hands over the central skill in miniature before any
      definitions — no agenda-first opening.
- [ ] **Easy language:** sampled paragraphs pass Section D.
- [ ] **Analogies:** every tricky idea has a concrete, mapping analogy; one story-world carries them, and
      the nickname lexicon (`plain_language.md` §9) is consistent across BOTH artifacts and decoded at
      the end.
- [ ] **Closing arc:** PDF ends self-test (hidden answers) → one-page pocket card → glossary + symbols;
      HTML ends final-boss quiz → the one card to keep. The honest surprise (`waitwhat` / highlighted
      beat) appears only where the material earns it.
- [ ] **Math:** built step by step, every symbol named, wide math contained.
- [ ] **Worked examples:** every one passes Section E.
- [ ] **Interactivity (HTML):** every one passes Section F; 2+ per major concept.
- [ ] **No-overflow contract:** every box in Section C ticked.
- [ ] **Readability & flow:** hierarchy clean; hook opener; bridges between concepts; reads as one lecture.
- [ ] **Self-contained (HTML):** Section G all green; opened, clicked every control, console clean.
- [ ] **Score ≥ 85/100** and **zero red-list items**.

Coverage, worked-example completeness, and working+revealing interactions are the three that fail most
often. Verify those first; the rest tend to follow.

---

## J. Worked scoring examples (calibration)

Use these to calibrate the harshness of the gate. Numbers are illustrative, not arithmetic to memorize.

**Example 1 — a draft that *looks* finished but must NOT ship.**
A lecture HTML covers all 7 concepts, has pretty sliders, and renders math. But concept 5's worked example
jumps from the setup straight to the answer ("it can be shown that the determinant is 14"), and the softmax
slider only animates colors — it never changes the probabilities.
- #1 Completeness 14/16 (one example not fully worked), #6 Worked examples 6/14 (a skipped-step example),
  #7 Interactivity 6/12 (one decorative interaction). Raw total ≈ 86.
- **Verdict: FAIL.** Two red-list items: a worked example that skips steps ("it can be shown that") and a
  decorative-only interaction. Red-list overrides the score. Fix both, then re-score.

**Example 2 — a companion PDF that ships.**
All 6 concepts present in teaching order; each has the full 9-step spine; every example computed number by
number with the final answers bold; analogies map cleanly; inline SVG figures read clearly; clean A4 with no
bleed; short sentences throughout.
- #1 16, #2 12, #3 11, #4 8, #5 (+6) 18, #6 (+6) 19, #8 8, #9 4, #10 2 ≈ **98/100**, zero red-list.
- **Verdict: SHIP.** The one lost point in #3 is a single long sentence — note it, but it clears threshold.

**Example 3 — borderline, REVISE.**
A lecture HTML covers everything with working, revealing interactions, but the prose leans on jargon
("the posterior is proportional to the likelihood times the prior" with none of the three terms defined),
and three equations overflow the page sideways on a 360px phone.
- #3 Easy language 5/12, #5 Math 7/12, #8 No-overflow 0/8 (horizontal overflow). Raw total ≈ 78.
- **Verdict: FAIL on red-list** (horizontal page scroll) AND below 85. Define the terms, wrap the three
  equations in `.eqbox`, re-test at 360px, re-score.

---

## K. Reviewer workflow (how to run this rubric in one pass)

1. **Coverage sweep first.** Put the deck beside the artifact. Tick each slide → its section. A single
   missing concept or unworked example is an instant fail; stop and send it back before scoring anything
   else.
2. **Walk one concept end to end.** Verify all 9 spine steps and the right callout per step. Read its worked
   example against Section E. This catches most spine and example defects in minutes.
3. **Sample easy language (Section D).** Pick 5 random paragraphs. Long sentences and undefined jargon are
   the usual leak.
4. **(HTML) Click every control.** Open from `file://`, watch the console, resize to 360px and to 1440px.
   Confirm each interaction *reveals* something — say the idea out loud. Confirm no horizontal scroll and no
   overlap. (PDF) Print to A4 and check for bleed and bad breaks.
5. **Run the dependency audit (Section G, HTML).** Search for `type="module"`, non-allowed hosts, `fetch`,
   and keys.
6. **Tally categories, apply the red-list (Section H), then the ship gate (Section I).** Red-list beats
   score every time.

One disciplined pass in this order finds the failures that matter without re-reading the whole artifact
five times.
