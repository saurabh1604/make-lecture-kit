# The Intuition Playbook

*The secret sauce for making hard math/ML topics click — and turning each idea into a
working interaction. Keep this open while authoring either the companion PDF or the
interactive lecture HTML. Every rule below comes with a concrete worked example so you can
copy the pattern, not just the principle.*

Audience model: **smart but new.** They are clever and motivated. They have NOT yet seen
this notation. Never assume the prior; always build it. Boring-but-correct beats
clever-but-confusing.

---

## 0. The five-part shape every concept must take

Author each concept in this fixed order. It is the skeleton for one chapter/section.

1. **Hook** — the section's **one-liner first** (the whole idea in one plain sentence),
   then a one-line question or surprise that the concept answers.
2. **Plain intuition + analogy** — what it *is*, in kitchen-table words, then one sticky
   real-life analogy.
3. **Math, built step by step** — every symbol named on first use, nothing skipped.
4. **One fully worked example** — real numbers, every line shown, no "it can be shown".
5. **Visual + interaction** — a picture, plus a thing the learner *moves* to feel it.
   Then: **ML/AI connection**, **watch-out (pitfall)**, **one-line bridge** to the next.

If a section is missing any of 1–5, it is not done.

**Experience before vocabulary, wherever possible.** The strongest order is: the learner
*does or sees the thing* → then gets its official name ("What you just did, in official
words"). A term attached to a memory needs no memorising; a term introduced cold is one
more thing to hold. This is why a lecture's very first chapter should hand the student
the central skill in miniature before any definitions appear.

**Right-size every part** (`plain_language.md` §8): the five-part shape is a *ceiling*,
not a floor. For a genuinely easy concept each part shrinks — a one-line hook, a two-line
intuition, one small example — and the analogy may be skipped when the idea is already an
everyday thing. Always enter through the most intuitive door you can find, and spend the
depth where the difficulty really lives.

---

## A. Generating sticky real-life analogies

A good analogy maps **structure**, not surface. Pick an everyday system whose *relationships*
mirror the math's relationships. Then state the mapping explicitly, then state where it
breaks (analogies that overstay their welcome cause bugs in the student's head).

**One analogy per idea — the best one.** Two analogies for the same idea compete and
confuse. And when the idea is already everyday (a table of numbers, adding two lists),
skip the analogy entirely: the thing is its own picture (`plain_language.md` §8).

**One STORY-WORLD per lecture — a recurring cast, not a parade of strangers.** Before
authoring, pick a single everyday world whose relationships mirror the whole lecture's
relationships, and draw the per-concept analogies from *inside* it wherever they fit.
A linear-systems lecture can live entirely in a detective case: equations are *clues*,
unknowns are *hidden numbers*, a redundant equation is an *echo*, an impossible one is a
*lying witness*, and the running example (the factory order) is *the case* being solved.
Each new concept then arrives as a new scene in a familiar story instead of a cold start —
the reader reuses everything they already know about the world. Give the recurring
objects the short plain nicknames from `plain_language.md` §9 and keep them identical in
the PDF, the HTML, the figures, and the demos. Reach outside the story-world only when a
concept genuinely doesn't fit it — a strained in-world analogy is worse than a fresh one.

**Hunt the honest surprise.** Somewhere in most lectures hides a consequence that sounds
impossible but is true — *change every dial and land in the same place* (null vectors),
*the same clue heard twice adds nothing* (rank), *a tiny wobble in one number flips the
answer completely* (conditioning). Find it by asking: "which fact here would make a
newcomer say 'wait — really?'" Give that fact a loud, dedicated moment (the companion's
`waitwhat` box; a highlighted beat in the HTML), state it concretely with the lecture's
own numbers, and then show why it's true. One real surprise per lecture, well landed,
does more for memory than ten "interestingly"s — and if a concept has no honest
surprise, never manufacture one.

### The analogy bank (patterns you can reuse)

| Math object | Everyday analogy | Mapping (what lines up) |
|---|---|---|
| **Vector** | An arrow / a recipe of ingredients | direction+length, OR a list of amounts |
| **Dot product** | "How much do two arrows agree?" / shadow length | sign = agree/disagree; 0 = unrelated |
| **Matrix** | A machine that bends a sheet of stretchy graph paper | input grid in, transformed grid out |
| **Eigenvector** | The one direction the machine only stretches, never turns | axis that survives the transform |
| **Gradient** | The steepest-uphill arrow a hiker feels underfoot | local direction of fastest increase |
| **Derivative** | Your speedometer reading at one instant | rate of change right *now* |
| **Probability distribution** | How a bag of marbles is split by color | total = 1; each share = a chance |
| **Variance** | How spread-out darts are around the bullseye | small = tight cluster, big = scattered |
| **Expectation** | The long-run average payout of a slot machine | weighted average outcome |
| **Bayes' rule** | A detective updating a hunch as clues arrive | prior belief → evidence → new belief |
| **Logarithm** | Counting digits / "how many times you fold paper" | turns multiplying into adding |
| **Determinant** | The area/volume scaling factor of the machine | 0 = squashed flat (info lost) |
| **Convexity** | A bowl you drop a marble into | one bottom, marble always finds it |
| **Norm / distance** | How far apart two towns are | size of a vector / gap between points |
| **Inner-product space** | A room with a built-in ruler and protractor | lets you measure length and angle |
| **Markov chain** | A board game where your next square depends only on the current one | memoryless hop |
| **Entropy** | Average surprise of tomorrow's weather | bits needed to encode the outcome |

### Recipe for inventing a fresh analogy

1. Name the **core relationship** in the math ("X grows fast where the surface is steep").
2. Find a daily system with that **same relationship** ("a ball rolls fast on a steep hill").
3. Write the **mapping table** (steepness ↔ gradient magnitude; ball ↔ parameter).
4. State the **break point** ("but a real ball has momentum; plain gradient descent does
   not — that's why we *add* momentum later").

> **Worked analogy — Gradient descent as a foggy mountain descent.**
> *Relationship:* to reach the valley you repeatedly step downhill. *Daily system:* a hiker
> in thick fog who can only feel the slope under their boots. *Mapping:* slope-under-boots ↔
> negative gradient; step size ↔ learning rate; the valley ↔ the loss minimum; fog ↔ "we
> can't see the global shape, only local". *Break point:* if steps are too big the hiker
> overshoots the valley and climbs the far wall — that's a learning rate that diverges.

---

## B. Building the right mental model

A mental model is the *picture the student keeps* after they forget the formula. Choose one
dominant model per concept and stay consistent with it across the whole lecture.

- **Pick ONE canonical picture** and reuse it. For linear algebra, the recurring picture is
  "a grid of graph paper being transformed". Don't switch metaphors mid-lecture.
- **Concrete before abstract.** Show a 2×2 numeric matrix acting on the points (1,0) and
  (0,1) *before* writing the general \(A\mathbf{x}\). Let them see the two basis arrows move.
- **Name the invariant.** Every concept protects something. Eigenvectors protect a
  *direction*. A probability distribution protects *total mass = 1*. Orthogonal maps protect
  *length*. Say the invariant out loud — it's the load-bearing idea.
- **Smallest interesting case.** 2D before nD. A coin (Bernoulli) before a softmax over
  50,000 tokens. One data point before a batch. Then generalize in one explicit step.
- **Two views, one truth.** Pair an *algebraic* view (the symbols) with a *geometric* view
  (the picture) and show they say the same thing. Students lock in when both views click.

> **Worked mental model — eigenvectors.**
> Canonical picture: the stretchy-graph-paper machine \(A\). Most arrows get *both* rotated
> and stretched. The eigenvectors are the rare arrows that come out pointing the *same* way,
> only longer or shorter; the eigenvalue is *how much* longer. Invariant protected: their
> direction. Smallest case: \(A=\begin{bmatrix}2&0\\0&3\end{bmatrix}\) stretches x by 2 and y
> by 3 — the axes themselves are the eigenvectors, so you literally *see* it before any
> general proof.

---

## C. Deriving a memorable VISUAL intuition

For each common math object, here is **what to plot or animate** so the picture does the
teaching. Default to canvas/Plotly for plots, D3/SVG for structured diagrams.

| Object | Plot / animation that reveals it | The "aha" the visual delivers |
|---|---|---|
| **Vector** | Arrow from origin; tip draggable | direction + magnitude are one thing |
| **Vector add** | Tip-to-tail arrows + the resultant | "walk one path, then the next" |
| **Dot product** | Project one arrow onto another; show the shadow + angle | sign & size = agreement |
| **Matrix transform** | Animate a unit grid + the two basis arrows under \(A\) | columns of \(A\) = where basis lands |
| **Eigenvector** | Sweep a test arrow around the circle; highlight when input ∥ output | the non-turning directions pop out |
| **Determinant** | Shade the unit square; watch its area change under \(A\) | det = area scale; det 0 = collapse |
| **Gradient** | Contour/heatmap of \(f\) + arrow field pointing uphill | gradient ⟂ contours, points steepest-up |
| **Gradient descent** | Marble path stepping down a contour map; slider = learning rate | too-big rate → zig-zag/divergence |
| **Derivative** | Curve + tangent line at a draggable point; show the slope number | slope = instantaneous rate |
| **Probability dist.** | Bar chart (discrete) / shaded area (continuous); bars sum to 1 | total mass is conserved |
| **Variance** | Scatter of samples + a band of ±1σ that widens with σ | spread you can literally see |
| **Gaussian** | Bell curve with μ, σ sliders; shade the area under it | μ moves it, σ fattens it |
| **Bayes update** | Prior bar → likelihood bar → posterior bar, animated | evidence reshapes belief |
| **Matrix** | Heatmap of cell values; hover a cell to highlight its row·col | structure you can scan |
| **Softmax** | Bars of logits → bars of probabilities as a "temperature" slider moves | sharpening vs. flattening |

**Visual craft rules.** Always label axes and units. Always show the *current number*
next to the moving picture (slope = 1.73, σ = 0.5). Animate a *change*, not a static
final state — the change is the lesson. Keep one color per concept and reuse the lecture
palette (gradients violet, intuition teal, etc.).

> **Worked visual — the derivative.** Draw \(f(x)=x^2\). Put a draggable point at \(x=a\).
> Draw the secant from \(a\) to \(a+h\); add an \(h\)-slider. As the slider drives \(h\to 0\)
> the secant visibly rotates into the tangent, and the printed slope number marches from a
> crude estimate to exactly \(2a\). The student *watches* the limit happen.

---

## D. ALWAYS finding the ML/AI connection

Every math/CS idea earns its place by powering something in modern ML. Make the bridge
explicit — name the model or training step where this exact object shows up. Use this lookup;
each row is a ready-to-paste "why this matters" paragraph seed.

| Math/CS concept | ML/AI payoff (the bridge to state) |
|---|---|
| **Eigenvectors / eigenvalues** | **PCA** keeps the top-eigenvalue directions (max variance); **spectral clustering** uses the graph Laplacian's eigenvectors; eigen-decay explains why **embeddings** compress. |
| **Gradients** | **Backpropagation** is the chain rule computing \(\partial \text{loss}/\partial \text{weights}\); every optimizer step is "move against the gradient". |
| **Probability / likelihood** | **Generative models** maximize data likelihood; training a classifier minimizes **cross-entropy** = negative log-likelihood; sampling from an LLM = drawing from a distribution. |
| **Linear algebra (matmul, projection)** | **Embeddings** are learned vectors; **attention** is scaled dot-products \(QK^\top\) then softmax then a weighted sum \( \cdot V\); a linear layer is one matrix multiply. |
| **Variance / bias** | The **bias–variance tradeoff** explains under/overfitting; **regularization** (L2/dropout) trades a little bias for much less variance. |
| **Bayes' rule** | **Naive Bayes** classifiers; **Bayesian** posteriors and uncertainty; the prior↔regularizer correspondence (MAP = MLE + prior). |
| **Convexity** | Convex losses (linear/logistic regression) have **one** global minimum — gradient descent is guaranteed to find it; non-convex nets explain local minima talk. |
| **Distance / norms** | **k-NN**, **cosine similarity** for retrieval/RAG, **contrastive learning** pulls similars close and pushes dissimilars apart; L2 vs L1 penalties. |
| **Entropy / KL divergence** | **Cross-entropy loss**; **KL** measures how far a predicted distribution is from the target; the core of **VAEs** and distillation. |
| **Matrix factorization / SVD** | **Recommender systems** (latent factors), **LSA** topic models, low-rank **LoRA** fine-tuning. |
| **Determinant / Jacobian** | **Normalizing flows** track volume change via \(\log\lvert\det J\rvert\); change-of-variables in density estimation. |
| **Markov chains** | Language models as next-token transitions; **MCMC** sampling; PageRank. |

**Connection recipe:** (1) name the ML task, (2) point at the exact spot the object appears,
(3) say what would *break* without it.

> **Worked connection — dot product → attention.** Task: a transformer deciding which
> earlier words matter for the current word. The model computes a **dot product** between a
> query vector and every key vector — exactly "how much do these two arrows agree?" Big dot
> product = high relevance. Softmax turns those agreements into weights; the output is a
> weighted sum of value vectors. Without the dot product there is no notion of relevance, and
> attention collapses to a plain average.

---

## E. "Explain like the student is smart but new" — phrasings

> The binding word-level rulebook is **`references/plain_language.md`** (plain-word swaps,
> banned hand-waving, sentence ceiling, reading level), enforced by the linters. This section
> gives the *phrasing patterns* that hit that bar.

Swap jargon-first sentences for these patterns. Aim for 15 words a sentence (hard ceiling 22);
define each term the first time; one idea per sentence.

- **Define-then-use:** "A *norm* is just the length of a vector. We write it \(\lVert v\rVert\)."
- **Name-the-symbol:** "Here \(\eta\) (eta) is the **learning rate** — how big each step is."
- **Why-before-how:** "We want the steepest way down. The gradient is exactly that arrow."
- **Concrete number first:** "Take \(x=3\). Then \(f(x)=9\). Now watch what a small nudge does."
- **Contrast pair:** "Small variance = darts cluster. Big variance = darts scatter."
- **Permission to be confused:** "This looks heavy. It's three easy steps. Here's step one."
- **Callback:** "Remember the foggy-hill hiker? The gradient is the slope under their boots."
- **No hand-waving ban-list:** never write "clearly", "obviously", "it can be shown",
  "trivially", "left to the reader". If it's clear, show it in one line anyway.

**Term-on-first-use template:** *italicize the term, give the one-line plain meaning, give the
symbol, give a number.* Example: "An *eigenvalue* (how much an eigenvector stretches), written
\(\lambda\), might be \(\lambda=2\) — meaning 'twice as long'."

> **Rewrite example.**
> Jargon: "The objective is the expected negative log-likelihood under the empirical
> distribution." →
> Plain: "We score the model by its average *surprise* on the training data. Lower surprise =
> better fit. *Surprise* of a guess is \(-\log p\): confident-and-right is near 0,
> confident-and-wrong blows up."

---

## F. Turning each idea into an INTERACTION

> Applies to the interactive **lecture HTML** only (see `lecture_style.md`). The companion
> **PDF has no JavaScript** — it uses static matplotlib figures and LaTeX callouts.

The interaction must **reveal the intuition**, not decorate the page. Ask: *what should the
learner move, and what hidden truth pops out when they move it?* Each major concept needs
**2+ working interactions**. The gold standard draws every visual on a bespoke `<canvas>`
with the plain 2D context — prefer that; it keeps the page keyless (only MathJax loaded) and
fully under your control.

### Interaction archetypes (pick 2 per concept)

1. **Live slider → plot.** One parameter drives a chart that redraws on `input`.
   *Reveals:* cause→effect. (σ-slider fattens a Gaussian; learning-rate slider makes the
   descent path zig-zag.)
2. **Step-through derivation/animation.** A "Next step" button uncovers one line of math or
   one animation frame at a time. *Reveals:* a scary formula is a short sequence of easy moves.
3. **Toggle / hover reveal.** A switch overlays a hidden structure (contour lines, the
   eigenvector axes, the ±1σ band). *Reveals:* the structure that was "always there".
4. **Drag a point / arrow.** The learner drags the vector tip or the tangent point; numbers
   update live. *Reveals:* the object is alive, not a fixed picture.
5. **Tiny "try it" calculator.** Type numbers into a 2×2 matrix; it prints det, eigenvalues,
   the transformed grid. *Reveals:* the formula is a button they can press on *their* numbers.
6. **Before/after compare.** A toggle flips between two regimes (underfit vs overfit; L1 vs
   L2). *Reveals:* the tradeoff by direct contrast.

### Mapping objects → the right interaction

| Concept | Move this… | …to feel this |
|---|---|---|
| Gradient descent | learning-rate slider + step button | convergence vs. overshoot/divergence |
| Derivative | drag the point; shrink \(h\) | secant becomes tangent; slope = \(f'(a)\) |
| Matrix transform | edit the 4 entries | columns of \(A\) = images of the basis |
| Eigenvector | sweep an input arrow | which directions don't turn |
| Gaussian | μ, σ sliders + "shade area" toggle | location vs. spread; area = probability |
| Bayes | drag the prior bar | how much evidence shifts belief |
| Softmax | temperature slider | sharpen vs. flatten the distribution |
| Bias–variance | model-complexity slider | train error ↓ while test error U-turns |
| PCA | rotate the data cloud | the top component = max-spread axis |

**Wiring rules (must work from `file://`):** prefer a bespoke `<canvas>` drawn with the 2D
context (MathJax is the only external load needed); Plotly/d3 are optional extras. Load any
library as a UMD/global `<script>` tag (`cdnjs`, `cdn.jsdelivr.net`, `cdn.plot.ly`) — **never**
`type="module"` (it breaks on `file://`). Bind with
`addEventListener` / `oninput` / `onclick`. Redraw on every input event. Always print the
current numeric value beside the visual. Re-typeset math after dynamic insertion with
`MathJax.typesetPromise()`. Make controls stack on mobile; wrap wide math in `.eqbox`.

> **Worked interaction — feel the learning rate.** Show a contour map of a simple bowl loss.
> Put a marble at a start point and a slider for \(\eta\) from 0.01 to 1.2. A "Step" button
> applies one gradient-descent update and drops a dot at the new position, drawing the path.
> At \(\eta=0.1\) the path glides smoothly to the center. At \(\eta=0.9\) it zig-zags. At
> \(\eta=1.1\) it spirals *outward* and diverges. The student discovers the stability limit
> by themselves — no formula needed, though you then show the formula that predicts it.

---

## G. Quick authoring checklist (per concept)

- [ ] Hook line that poses the question this concept answers.
- [ ] Plain intuition (no jargon) + one sticky analogy with its break point named.
- [ ] Every symbol introduced and named; math built line by line.
- [ ] One fully worked example with real numbers and every step shown.
- [ ] A visual that animates the *change*, with the live number printed.
- [ ] 2+ interactions that reveal intuition (slider, step-through, toggle, drag, calculator).
- [ ] Explicit ML/AI connection (task → exact spot → what breaks without it).
- [ ] A watch-out / common pitfall.
- [ ] A one-line bridge to the next concept.
- [ ] Easy language: sentences < ~20 words, terms defined on first use.

*If every box is checked for every slide in the deck, the lecture is complete.*
