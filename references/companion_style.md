# Companion Style — the authoring guide

Read this **before** writing a single line of a companion. A companion is the
plain-English book that walks beside a terse lecture deck. The slides give the
formulas; **this reader gives the why.** It expands every slide concept into the
full teaching treatment and works **every** slide example out in full, step by
step, in easy English.

The look is fixed and non-negotiable: a navy title banner, a `fancyhdr` running
header, numbered ruled section headings, and **five** coloured callout boxes
with pill tabs. The compilable specimen at `examples/sample_companion.tex` is the
quality bar — when in doubt, match it. The figure helper is
`scripts/figstyle.py`. The full template preamble lives in
`templates/companion.tex`.

---

## 0. The non-negotiable visual contract

| Element | Spec |
|---|---|
| Header (every page) | left `ISM Companion`, right `Session N · <Lecture Title>`, thin rule below |
| Footer | centred page number |
| Title banner (page 1) | full-width dark-navy `tcolorbox` (`#21355E`), white text: tracked uppercase label → very large bold title → light subtitle → thin white rule → small meta line |
| Intro | one paragraph **"How to use this companion."** explaining the colour code |
| Sections | sans, bold, navy, **numbered** (`1  The big idea: …`), horizontal rule beneath; **each new top-level topic starts on a fresh page** (automatic via the template's `\sectionbreak` — the first section stays under the banner, every later one clears the page so a topic never splits across a break) |
| Body | justified serif (lmodern), `parskip` spacing, `microtype`, math via `amsmath`, tables via `booktabs` |
| Figures | full-textwidth matplotlib PNGs, centred, **bold title baked into the plot** |

### The FIVE callout boxes — exact taxonomy (quote it, don't improvise)

| Box | Pill label | Glyph | Frame hex | Tint | Use it for |
|---|---|---|---|---|---|
| Intuition | `The intuition` | ☞ `\ding{43}` | `#2C5AA0` blue | `blue!4` | the idea in plain words, before any math |
| Everyday | `Everyday picture` | ★ `\ding{72}` | `#8A5A1E` amber | `orange!7` | the real-life analogy for a tricky idea |
| Worked | `Worked example: <caption>` | ✎ `\ding{46}` | `#2E7D52` green | `green!5` | a problem solved with real numbers, every step |
| Watch out | `Watch out` | ✗ `\ding{55}` | `#B23A48` red | `red!4` | the common mistake / trap |
| Key takeaway | `Key takeaway` | ✓ `\ding{52}` | `#6A4C93` purple | `violet!6` | the one line to remember |

Box style (from the template): `enhanced, breakable`, rounded corners,
`boxrule=0.6pt`, **pill tab** via `attach boxed title to top
left={xshift=6mm,yshift=-3mm}`, `boxed title style={colback=<frame>, rounded
corners}`, `coltitle=white`, `fonttitle=\bfseries\sffamily\small`. Never change
the colours, labels, or glyphs — they are the reader's mental index.

---

## 1. Ingest the slide deck (do this first, in full)

You cannot expand what you have not catalogued. Before writing:

1. **Read the source.** Open the `.pdf` or `.pptx`. If it is `.pptx`, use the
   `pptx` skill to extract text and notes; if `.pdf`, use the `pdf` skill. Read
   **every** slide, including the agenda and any "example" one-liners.
2. **List every concept.** One line each, in slide order. A concept is anything
   that earns a definition, a formula, or a named idea. This becomes your
   section list.
3. **List every slide example.** Each terse "e.g. λ=3, find P(X=2)" is a
   **promise** you must keep: it gets a full `worked` box with every step. Mark
   which concept each example belongs to.
4. **List every formula and symbol.** You will name every symbol on first use,
   so collect them now.
5. **Write the spine.** For each concept, plan the order in §2. Confirm the
   count: *number of `worked` boxes ≥ number of slide examples.* If a slide has
   three examples, the companion has at least three worked boxes for it.

Output of this step is a checklist. Do not start prose until the checklist is
complete. A dropped slide example is a failed companion.

---

## 2. Map each concept onto the teaching spine

Every concept follows the same gentle arc. Not every concept needs every box,
but the order never changes:

1. **Open in plain words** — one or two body sentences saying what this is and
   why we care. No jargon yet.
2. **The intuition box** (blue ☞) — the idea stated simply, the mental model.
3. **The everyday picture box** (amber ★) — the analogy. **Mandatory for any
   tricky idea.** Put it *before* the math, so the reader meets the concept in
   the world before meeting it in symbols.
4. **Formalize** — introduce the formula in body text. Name **every** symbol
   the first time it appears (see §3). Build it up, never drop it whole.
5. **The worked example box(es)** (green ✎) — solve the slide example(s) in
   full (see §4). One box per example; keep each box coherent.
6. **The watch-out box** (red ✗) — the trap a beginner falls into here.
7. **The ML/AI connection** (see §7) — a short body paragraph, `\textbf{Where
   this shows up in ML.}`, on how the idea appears in machine learning.
8. **The key-takeaway box** (purple ✓) — the single line to remember. Always
   last for the concept.

**When to use which box** (decide fast):
- Explaining *what something means*? → **intuition** (blue).
- Reaching for "it's like…"? → **everyday** (amber).
- Touching real numbers? → **worked** (green).
- About to say "be careful" / "a common error is"? → **watch out** (red).
- Compressing to one sentence? → **key takeaway** (purple).

Do not stack two boxes of the same colour back to back. Do not put math
derivations inside the intuition or everyday boxes — those stay word-only.

---

## 3. The EASY-LANGUAGE mandate

**`references/plain_language.md` is the binding rulebook — read it first.** It holds the
hard rules, the plain-word swap table, the banned hand-waving phrases, and the reading-level
target, and `scripts/lint_tex.py` enforces them on your `.tex`. The essentials:

- **Short sentences: aim 15 words, hard ceiling 22.** One idea per sentence.
- **Plainest correct word.** Swap fancy words for common ones (full table in
  `plain_language.md` §3): *use* not *utilize*, *so* not *thus/hence*, *about* not
  *approximately*, *many* not *numerous*, *show* not *demonstrate*.
- **Define every term on first use,** inline, in plain words; spell out every symbol and
  acronym the first time ("POS, part of speech"; "\(\lambda\), the Greek letter lambda").
- **No hand-waving, ever.** "It can be shown that", "clearly", "obviously", "left to the
  reader" are banned (full list in `plain_language.md` §4) — show the line instead.
- **No literary fog.** This is a study aid; say the plain mechanism, not "the job dissolved
  into the machinery of…".
- Prefer "average" to "expectation" on first contact, then add the technical word in
  parentheses.

Rewrite every dense slide sentence. Before → after:

- **Before:** "X ~ Poisson(λ) models the number of arrivals in a fixed interval
  under independence and stationarity assumptions."
  **After:** "A Poisson count answers one question: how many rare events happen
  in a fixed window? It needs just one number, λ, the average count."

- **Before:** "The MLE is obtained by setting the score function to zero."
  **After:** "To find the best-fit value, we find where the slope of the
  likelihood is zero. That slope is called the *score*."

- **Before:** "The estimator is unbiased and consistent."
  **After:** "On average this estimate hits the truth (it is *unbiased*), and it
  gets better as we collect more data (it is *consistent*)."

Rules of thumb: one idea per sentence; active voice; spell out the first use of
every Greek letter ("λ, the Greek letter lambda"); replace "thus/hence/whence"
with "so"; never write "clearly" or "obviously" — if it were obvious the
companion would not exist.

---

## 4. Write a FULLY worked example

This is the heart of the companion. **Show every algebraic step with real
numbers.** Never write "it can be shown that", "after simplification", or "the
details are left to the reader". If you skipped a step, you failed.

Put it in a `worked` box with a short caption in the pill label, and the dedicated
**`steps`** list (defined in the template; it styles the labels as "Step 1.", "Step 2.", …).
**Always use `\begin{steps}…\end{steps}`, never a raw
`\begin{enumerate}[label=\textbf{Step \arabic*.}]`.** The raw enumerate inherits the small
global `leftmargin`, which is too narrow for the wide "Step N." label, so the label spills
*out of the left edge of the callout box* — the exact bug that must never ship. The `steps`
list reserves enough label width to keep every "Step N." inside the box.

Skeleton:

```latex
\begin{worked}{<short caption, e.g. help-desk calls in one hour>}
<One plain sentence restating the problem and the target.>
\begin{steps}
  \item \textbf{Write down what we know.} State each given value: lambda = 3, k = 2.
  \item \textbf{Plug into the formula.} Substitute the numbers literally:
        \[ P(X=2) = \frac{3^{2}\,e^{-3}}{2!}. \]
  \item \textbf{Work out each piece.} 3^2 = 9; 2! = 2; e^{-3} = 0.049787.
  \item \textbf{Combine.}
        \[ P(X=2) = \frac{9 \times 0.049787}{2} = 0.224042. \]
        So about \textbf{22.4\%}.
  \item \textbf{Sense-check.} Is it between 0 and 1? Does it sit near the peak? Yes.
\end{steps}
<One sentence naming any trick used (e.g. the "1 - P(0)" shortcut).>
\end{worked}
```

Discipline for worked examples:
- **Every** intermediate number appears. Carry 4–6 significant figures, then
  round the final answer and **bold** it.
- One step does one thing. If a step has two computations, split it.
- End with a **sense-check**: range, units, "is it near the mean?", a sanity
  bound. This teaches judgement, not just arithmetic.
- Keep a single worked example **coherent** — it may break across pages
  (`breakable`), but do not interleave unrelated prose inside it.

---

## 5. Figures: draw a plot wherever it makes the idea easier to see

A maths/stats/ML idea is almost always **easier to grasp as a picture than as
prose.** So the default is: **most concepts get a figure.** A figure is *required*
(not optional) whenever the concept is any of these:

> a function or curve · a 2-variable surface or loss landscape · a probability
> distribution · a vector / geometric object · a matrix or table of numbers · a
> step-by-step process or pipeline · a sequence with per-item labels · a
> comparison of methods/quantities · **any worked example whose numbers can be
> drawn.**

If you can answer "what would this look like?", draw it. Only skip a figure when a
concept is genuinely non-visual (a definition, a naming convention).

### When to draw WHAT — concept → plot (all in `scripts/figstyle.py`)

| The concept is… | Draw… | Helper |
|---|---|---|
| a 1-D function, derivative, **Taylor** approx | curve, with the **tangent** at a point | `function_plot(f, xlim, ..., tangent_at=x0)` |
| a **loss landscape / Hessian / 2-var function** | a filled **contour** map, critical points marked | `contour(f, xlim, ylim, points=[(x,y,"saddle","X")])` |
| the **shape** near a min/max/saddle, or **descent in 3-D** | a **3-D surface** (lit + wireframe; optional descent **path** lifted onto it + a floor "shadow" contour) | `surface3d(f, xlim, ylim, path=[(x,y), ...])` |
| **gradient descent / optimization dynamics** | the descent **path** on a contour (white-halo trail, start ring, min star); add `noise=` for an **SGD** wander | `gradient_descent(f, grad, start, lr, steps, xlim, ylim, noise=0.0, mark_min=(x,y))` |
| a **probability distribution** (discrete) | a PMF **bar** chart (bars sum to 1) | `pmf_bar(xs, ps, ...)` |
| a **Gaussian / area = probability** | a bell curve with the slice **shaded** | `shaded_normal(mu, sigma, lo, hi, ...)` |
| **embeddings / vectors / dot product** | **arrows** from the origin | `vectors2d([(x,y,"king",col), ...])` |
| a **matrix / transition / attention table** | a **heatmap** with annotated cells | `heatmap(M, row_labels=, col_labels=)` |
| a **pipeline / algorithm / agent loop** | a box-and-arrow **flow** diagram | `flow(["Read","Plan","Call tool", ...])` |
| a **sentence / sequence with tags** (NLP) | a token **strip** with tags + arrows | `annotated_sequence(tokens, tags=, arrows=)` |
| comparing **several methods/quantities** | a labelled **bar** chart | `bars(labels, values, ...)` |
| any other one-off | `use_house_style()` then plain matplotlib | — |

Every helper bakes in the house look (muted palette, the navy `HOUSE_CMAP` for
contours/surfaces/heatmaps, thin spines, a bold ink title) and writes a PNG when
you pass `out=`. **Keyless, offline, no network at author time.**

### 5.1 Make the figure TEACH its one idea (legibility recipes)

Picking the right helper is half the job; the figure must actually *show* the
intuition its caption claims. If the caption says "SGD wanders" but the path looks
straight, or "the gaps" but no gap is visible, the figure failed — redraw it.
These reusable moves turn a correct-but-flat plot into one that teaches, and they
apply in **any** subject:

- **Name the quantity on the picture.** Label the thing the caption is about — each
  residual "gap", the slope, the shaded area, the step size — don't make the reader
  infer it. A short on-plot label beats a sentence underneath.
- **Tie every annotation to the curve.** An interval, a bracket, a band: draw a thin
  drop-line from it up to the point on the curve it refers to, and shade the region
  it covers, so it reads as *part of* the picture, not a floating bar.
- **Shade meaning.** Colour the regions that carry the idea (uphill vs downhill, the
  probability slice, the chosen half) so colour itself does teaching work.
- **Make any path legible.** Draw a trajectory with a white "halo" under the coloured
  trail, a start ring, and a goal star, so it reads on any background —
  `gradient_descent(...)` already does this.
- **If the real effect is too small to see, magnify it honestly.** When good data
  makes the point tiny (a near-perfect fit → invisible gaps) or the variance is
  small, add a zoomed **inset** on one instance, or **state the size** ("gap = 0.18").
  Never fake a bigger effect — show the small one at a scale where it reads.
- **Show stochasticity as stochasticity.** When a "noisy" method barely wanders on
  this particular data, render its noise honestly with `gradient_descent(noise=...)`
  (a visibly jagged walk that still drifts to the minimum); note in the caption that
  the noise is stylised.
- **Go 3-D for shape.** For a landscape / bowl / saddle use
  `surface3d(f, xlim, ylim, path=[...])`: the lit surface + floor-shadow shows the
  *shape* and the lifted path shows the *dynamics* (the "ball rolling into the bowl").
  3-D suits any `z=f(x,y)` — a loss surface, a 2-var function, a probability
  surface — not just optimization.

The test for every figure: cover the caption and ask a beginner what the picture
says. If their answer isn't the caption's idea, fix the figure, not the caption.

### Per-lecture figure script (the real API)

Write one small script per lecture in `output/<slug>/figures/`. Import `figstyle`
robustly, call the helper that matches the concept, and save the PNG next to the
script. `build_pdf.py` runs every `*.py` it finds there.

```python
# figures/make_figures.py
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for up in ("../../../scripts", "../../scripts"):           # find the kit's scripts/
    p = os.path.normpath(os.path.join(HERE, up))
    if os.path.isdir(p): sys.path.insert(0, p); break
import figstyle as F

# A distribution -> a PMF bar chart (bars peak near the mean):
import numpy as np
from math import exp, factorial
k = np.arange(0, 11)
p = [3**i * exp(-3) / factorial(i) for i in k]
F.bars([int(i) for i in k], p, "Poisson(lambda=3): counts peak near the mean",
       xlabel="k (number of events)", ylabel="P(X=k)", fmt="{:.2f}",
       out=os.path.join(HERE, "fig_poisson.png"))

# A loss landscape -> a contour with the saddle marked:
F.contour(lambda x, y: x**2 - y**2, (-2, 2), (-2, 2),
          "f = x^2 - y^2: a saddle at the origin",
          points=[(0, 0, "saddle", "X")],
          out=os.path.join(HERE, "fig_saddle.png"))
```

### Putting the figure in the `.tex`

Include it at full text width via the template helper, and **always add a one-line
"how to read it"** to the caption — the caption should tell the reader what to
notice, not just name the plot:

```latex
\housefig{figures/fig_saddle.png}{The loss surface near the origin. It curves UP
along x and DOWN along y, so the origin is a saddle, not a minimum — that is what
the mixed-sign eigenvalues mean.}
```

`\housefig{path}{caption}` centres a `\includegraphics[width=\linewidth]{...}`, so
an image never overflows. If there is truly no toolchain, a small inline TikZ
sketch (see the specimen) is an acceptable stand-in for a simple bar/curve — but
prefer a real `figstyle` PNG. One clear message per figure; label axes and units.

---

## 6. LaTeX anti-overflow discipline

**Never ship an Overfull `\hbox`.** The reader prints this; overflow is visible
and ugly. Defences:

- **Long math:** never one overlong line. Break with `align` / `split` /
  `multline`. Each `&=` continuation wraps at the margin:
  ```latex
  \begin{aligned}
    P(X \ge 1) &= 1 - P(X = 0) \\
               &= 1 - 0.049787 = 0.950213.
  \end{aligned}
  ```
- **Wide tables:** wrap in `\resizebox{\linewidth}{!}{...}` or
  `\begin{adjustbox}{max width=\linewidth}...\end{adjustbox}`. Build the table
  with `booktabs` (`\toprule \midrule \bottomrule`), no vertical rules.
- **Long URLs / tokens:** `\url{...}` (xurl lets them break anywhere); add
  `\allowbreak` inside long inline identifiers in prose.
- **Figures:** always `width=\linewidth` so an image never exceeds the text.
- **Callouts:** all five are `breakable`, so they flow onto the next page
  cleanly — but keep one worked example **coherent** (§4); do not let an
  example split mid-derivation if you can group it.
- **Steps must stay INSIDE the box.** Use the `steps` environment for worked
  examples (never a raw `enumerate` with a `Step` label) — otherwise the wide
  "Step N." label overflows the callout's left frame. This is a hard fail.
- **Content does not auto-shrink to a box.** A wide table or long equation
  *inside* a callout still overflows the frame unless you wrap it
  (`\resizebox{\linewidth}{!}{…}` / `adjustbox`) or break it (`align`/`split`).
  The box gives padding, not magic shrinking.
- Compile **twice** (header / `hyperref` / refs) and scan the log for
  `Overfull`. Then run `python3 scripts/lint_tex.py <companion.tex>` — it flags
  long sentences, banned hand-waving, fancy words, raw `Step`-label enumerates,
  and `\resizebox`-less wide tables. Fix every FAIL before declaring done.

---

## 7. The ML/AI-connection habit

**Every concept gets one.** After the math, add a short body paragraph led by
`\textbf{Where this shows up in ML.}` connecting the idea to machine learning or
AI — a model, a loss, a layer, a trick. Keep it concrete and one paragraph.

Examples of the move:
- Poisson → Poisson regression for count targets (`λ = e^{βᵀx}`), the Poisson
  NLL loss, photon-noise image models.
- Gaussian → the squared-error loss is the Gaussian NLL; weight init; the
  reparameterisation trick in VAEs.
- Bias/variance → why regularisation, dropout, and ensembles work.

If a concept has no honest ML hook, say so in one line rather than inventing a
forced one — but this is rare; most statistics concepts have a real connection.

---

## 8. Close with a glossary + symbol cheat-sheet

End every companion (right before *Further reading*) with a **quick-reference page**:
two compact tables a student can scan the night before an exam. It costs little and
turns the companion into a revision tool.

- **Glossary** — every term you defined, one plain line each, alphabetical-ish or in
  teaching order. Same plain wording as the body (`plain_language.md`).
- **Symbol cheat-sheet** — every symbol that appeared, with its meaning and where it
  came from. This is the table students reach for most.

Pattern (a starred section so it stays out of the numbering, plus two light tables):

```latex
\section*{Glossary \& symbols}
\addcontentsline{toc}{section}{Glossary \& symbols}

\noindent\textbf{Key terms.}
\begin{description}[leftmargin=8.5em,style=nextline,font=\normalfont\bfseries\color{navy}]
  \item[embedding] a word's address in ``meaning space''; similar words sit close.
  \item[softmax] turns a list of scores into probabilities that add to 1.
  % ...one line per term you defined...
\end{description}

\medskip
\noindent\textbf{Symbols at a glance.}
\begin{center}\small
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Symbol} & \textbf{Meaning} \\
\midrule
$\sigma(z)$ & the sigmoid, $1/(1+e^{-z})$; squashes any number into $(0,1)$ \\
$h_t$       & the hidden state (what the LSTM reads out) at step $t$ \\
$Z$         & the partition function (the total used to normalise to a probability) \\
\bottomrule
\end{tabular}
\end{center}
```

Keep the symbol table under `\linewidth` (two columns; wrap the meaning text). List
**only** symbols the lecture actually used, in the order they appeared.

## 9. Final self-review checklist (mirror the rubric)

Before you ship, confirm **every** line:

- [ ] **Banner** present on page 1: navy `#21355E`, tracked uppercase label,
      huge bold title, light subtitle, white rule, meta line (`Session N (dates)
      · Read alongside the lecture slides · Every slide example worked out in
      full`).
- [ ] **Header** every page: `ISM Companion` left, `Session N · <Title>` right,
      rule below; **footer** centred page number.
- [ ] **"How to use this companion."** intro paragraph explains all five colours.
- [ ] **Sections** numbered, sans, navy, ruled (`1  The big idea: …`).
- [ ] **All five callout types** used at least once, with the **exact** labels,
      glyphs, frames (`#2C5AA0 / #8A5A1E / #2E7D52 / #B23A48 / #6A4C93`) and
      tints (`blue!4 / orange!7 / green!5 / red!4 / violet!6`).
- [ ] **Every slide concept** expanded; **every slide example** worked in full,
      every step, real numbers, no "it can be shown that".
- [ ] **Easy language** (per `plain_language.md`): sentences ≤ 22 words, plain
      words (no fancy-word offenders), no banned hand-waving, every term defined
      on first use, every Greek letter named. `lint_tex.py` clean.
- [ ] **Every tricky idea** has an everyday-picture analogy **before** the math.
- [ ] **Every formula** built up with **every symbol named**.
- [ ] **Each concept** has an ML/AI connection.
- [ ] **Worked steps use `\begin{steps}`** — every "Step N." sits inside the box,
      never spilling past the frame.
- [ ] **No Overfull `\hbox`** in the log; wide math in `align/split`, wide tables
      in `adjustbox`/`booktabs` (or `\resizebox`), figures at `width=\linewidth`;
      nothing inside a callout exceeds the box width.
- [ ] **Figures** are house-styled via `\housefig{path}{caption}`, full-width, bold baked-in title.
- [ ] **Worked examples coherent** — none split mid-derivation awkwardly.
- [ ] **A figure wherever the concept is visual** (§5 criterion): function/surface/
      distribution/vector/matrix/process/sequence/comparison, and every worked
      example whose numbers can be drawn. `lint_tex.py` "figure coverage" is clean
      (or every flagged section is genuinely non-visual).
- [ ] **Glossary + symbol cheat-sheet** closing section present (§8).
- [ ] Compiles to a **real PDF**, keyless, twice through `pdflatex`.

If any box is unchecked, the companion is not done. Boring beats brilliant: a
deterministic, complete, plain-English reader that keeps every promise on the
slides beats a clever, partial one.
