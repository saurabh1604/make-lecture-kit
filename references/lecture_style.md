# lecture_style.md — How to author a COMPLETE interactive lecture HTML at the gold-standard bar

This is the build manual for the **interactive lecture HTML** — the touchable sibling of the companion PDF.
The companion is the written study doc; this file is the **experience**: same lecture, same concepts, same
depth, but every concept is also something the student can *drag*, *flip*, and *watch move*.

> **The quality bar is one file: `nlp-lecture5-v2.html`.** Open it, scroll it top to bottom, click every ⚡
> panel, run the guided tour, flip the theme. That page *is* the spec. This guide just teaches you to
> reproduce its level on a new topic. When in doubt, do what `nlp-lecture5-v2.html` does. Read it before you
> write a single tag.

The output is **ONE self-contained `.html`** that opens by double-click from `file://`. **The only external
dependency is MathJax from cdnjs.** No Plotly, no D3, no Tailwind, no Google Fonts, no API keys, no backend.
**Every visual is hand-drawn on a plain 2D `<canvas>`.** That is not a limitation — it is the whole point:
hand-drawn canvas is what lets each interactive *reveal its specific idea* instead of being a generic chart.
Canvas is not limited to 2-D: for a **loss landscape / bowl / saddle**, the template ships a tiny
pure-canvas **3-D** pattern (the "roll the ball into the bowl" lab — `bowlCanvas`): sample `z=f(x,y)`,
project each point by azimuth+elevation, depth-sort the quads (painter's algorithm), colour by height,
then drag to rotate. Copy that block for any 3-D surface — still no chart/3-D library, still one file.

---

## 0. Non-negotiable mindset

- This is a **complete lecture**, NOT a one-concept "visualizer". `nlp-lecture5-v2.html` has **21 chapters**
  (00–20) for one 60-minute deck. A real lecture is **~12–20 chapters**. If the deck has 15 concepts, the
  page has 15 chapters grouped in the sidebar. **Drop nothing.**
- Every interaction must **uncover the intuition**. The test: *"What does the student understand after
  touching this that they didn't before?"* If the answer is "nothing, it just looks nice" — cut it. In the
  gold standard, you flip XOR bits and *watch h₂ stay silent until both are on*; you crank η and *watch the
  ball overshoot and diverge*. Move it → the idea changes.
- **Bespoke beats generic.** Do NOT reach for a chart library. Each concept gets its *own* hand-drawn
  canvas built for *that* idea: a neuron diagram whose edges thicken with weight, a softmax bar race, a loss
  bowl with a rolling ball, a sliding window over a sentence. A generic line plot teaches almost nothing.
- **Easy language is law.** Smart-beginner audience. Short sentences (under ~20 words). Define each term the
  first time you use it. Analogy before algebra.
- **Nothing overflows, nothing overlaps, ever** — from a 360px phone to a 1440px monitor.
- **Cleanliness is non-negotiable.** A leaked HTML comment once embarrassed us. No comment may contain a
  nested `-->`. No `{{PLACEHOLDER}}` may survive into the shipped file. Every JS helper is defined before
  use. MathJax actually typesets. (Full contract in §10.)

---

## 1. Read the deck → enumerate EVERY concept → one chapter each, grouped in the sidebar

The input is a terse slide deck: a title, an agenda, concept slides (bullets, a definition, maybe a formula,
a one-line example). Your first action is **mechanical enumeration** — coverage before polish.

1. List the **title** and **agenda** verbatim. The agenda is your chapter spine and your nav.
2. Walk the deck slide by slide. Each distinct **concept** → exactly one chapter. Sub-bullets that define a
   sub-idea become sub-sections (`<h3>`) *inside* that chapter, not new chapters.
3. Order chapters in **teaching order**: the order that lets idea *N* lean on idea *N−1*. Prerequisites
   first. This is usually deck order; reorder when a later slide is a prerequisite for an earlier one.
4. Record **every slide example.** Each one MUST be worked out in full in its chapter (§5).
5. **Group the chapters into 4–6 named bands** in the sidebar, exactly like the gold standard. Its bands are
   a model you can re-skin per topic:

   | Band (gold standard) | Holds | Re-skin idea for other topics |
   |---|---|---|
   | **Foundations** | the atom + its parts (unit, activations, first worked example) | "Basics", "Setup", "The object" |
   | **The XOR Story** | the central puzzle that motivates everything | "The Problem", "The Story", "Motivation" |
   | **Feedforward Networks** | the core machinery built from the atom | "The Machinery", "Core Method" |
   | **NLP Applications** | where the idea earns its keep | "Applications", "In Practice" |
   | **Training** | how the thing learns / is solved / is computed | "Solving it", "Estimation", "Algorithms" |
   | **Beyond** | scaling up, history, what's next | "Extensions", "Frontier", "Wrap-up" |

6. Produce a **coverage checklist** before coding: `concept → chapter id → band → its slide example →
   bespoke interactive`. Tick it off at the end. If a concept is on a slide and not in the checklist, you
   missed it. A 12–18-slide deck → **12–20 chapters** across 4–6 bands. Merging two slides that teach the
   *same* idea is fine. **Silently dropping one is not.**

The sidebar markup mirrors the gold standard exactly — grouped, numbered, scroll-spy:

```html
<nav class="toc" id="toc">
  <div class="grp">Foundations</div>
  <a href="#intro"><span class="n">00</span> Overview</a>
  <a href="#neuron"><span class="n">01</span> The Neural Unit</a>
  <a href="#activations"><span class="n">02</span> Activation Functions</a>
  <div class="grp">The XOR Story</div>
  <a href="#xor"><span class="n">04</span> The XOR Problem</a>
  <!-- ...one anchor per chapter, numbered, grouped... -->
</nav>
```

---

## 2. The per-chapter spine + which component to use when

Every chapter follows the **same spine**: a story arc from hook to bridge. Keep it identical across
chapters so the page reads as one lecture; only the topic differs. Map each step to the component palette
(the exact CSS classes that exist in `nlp-lecture5-v2.html`):

| # | Step | What it does | Component |
|---|------|--------------|-----------|
| 1 | **Hook** | `.kicker` + `<h2>` + a `.lead` paragraph: a scene that makes the student *want* the idea. No math yet. | `.kicker`, `h2`, `p.lead` |
| 2 | **Intuition + analogy** | the idea in plain words; one concrete analogy *before* any symbol. | `.note` (violet) for the analogy aside |
| 3 | **Math, step by step** | build the formula one symbol at a time; name every symbol; headline equations in scrollable plates. | `<p>` build-up + `.eqbox` per equation |
| 4 | **Fully worked example** | the slide's example, real numbers, every step — often a step-through interactive. | `.card` "setup" + `.card` "walk it" with a `.readout` |
| 5 | **Bespoke interactive** | the ⚡ panel that lets the student move the idea. **The heart.** | `.lab` (carries the "⚡ INTERACTIVE" badge) |
| 6 | **ML / AI connection** | where this lands in ML/AI, concrete and short. **Mandatory every chapter.** | `.note` or inline `<p>` |
| 7 | **Pitfall / key insight** | the trap or the one big takeaway, in one sharp sentence. | `.key` (amber) |
| 8 | **Bridge** | one line that hands off to the next chapter. | closing `<p>` or `.note` "Summary & bridge" |

The component palette, verbatim from the gold standard — use these and only these:

- **`.card`** — neutral container for setups, sub-points, side-by-side comparisons (often inside `.grid2`/`.grid3`).
- **`.lab`** — the interactive block. It auto-renders an "⚡ INTERACTIVE" badge via `::before`. Every live
  demo lives in a `.lab`. Inside: an `<h4>` title starting with ⚡, a one-line `.muted` "what to look for",
  the controls, the `<canvas>`, and a `.readout`.
- **`.note`** (violet left-border) — asides, analogies, "why does this work", gentle warnings, bridges.
- **`.key`** (amber left-border) — the one load-bearing insight or pitfall of the chapter. Use sparingly.
- **`.eqbox`** — a scrollable dark plate for one display equation. Wide math scrolls *inside* it.
- **`.readout`** — the mono "console" that prints the live computation, with `<span class="hl">` (amber)
  and `<span class="g">` (green) to highlight intermediate and final numbers.
- **`.ctrl`** — one labeled slider row: `<label>` + `<input type=range>` + `<span class="val">`.
- **`.chips`** — a row of `.btn` toggle buttons (one carries `.active`).
- **`.grid2` / `.grid3`** — responsive columns that collapse to one column under 880px.
- **`.kicker`** — the small cyan "01 · The building block" eyebrow above each `<h2>`.

The interactive (step 5) is the thing that makes this the *lecture* and not the *PDF*. It can also be
*woven into* steps 3–4 (a step-through that builds the derivation; a calculator that runs the example) — the
gold standard's §03 worked example *is* a Next-button stepper.

---

## 3. The EASY-LANGUAGE mandate — terse slide line → short plain sentences

**`references/plain_language.md` is the binding rulebook (read it first).** `scripts/lint.py`
enforces it on the shipped HTML: sentence length, fancy-word swaps, banned hand-waving, and a
reading-level estimate. Slides are telegram-style; your job is to **expand** each line into
plain teaching prose, then make it pass the gate.

**Rewrite rules**
- Cut jargon, or define it the instant it appears: "a *bias* (a number that shifts the whole curve left or right)".
- **Aim 15 words per sentence; hard ceiling 22.** Split any longer sentence into two. One idea each.
- **Plainest correct word** (see `plain_language.md` §3): *use* not *utilize*, *so* not *thus*,
  *about* not *approximately*, *show* not *demonstrate*. No literary flourishes.
- **Never hand-wave** ("clearly", "obviously", "it can be shown", "left to the reader" are banned — `plain_language.md` §4).
- Replace symbols-in-prose with words on first mention, then introduce the symbol: "the learning rate, written \(\eta\)".
- Lead with the analogy; the gold standard calls a hidden neuron an *"at least one is on" detector* before it shows \(h_1=\text{ReLU}(x_1+x_2)\).
- **Show, don't pile up prose** (`plain_language.md` §6): a comparison becomes a table; a
  pipeline becomes a labelled canvas; a sequence of stages becomes a short numbered list.

**Before / after** (the right column is the gold-standard register):

| Slide line (terse) | Lecture HTML (easy) |
|---|---|
| "Unit: y = f(w·x + b); f nonlinear." | "A single unit takes some numbers in, mixes them with **weights**, adds one extra number called the **bias**, and pushes the result through a bend called the **activation**. That's the entire atom of deep learning. Drag the sliders and watch \(z\) build up term by term." |
| "XOR not linearly separable (Minsky 1969)." | "Here's the question that nearly killed neural networks: can one unit do basic logic? AND and OR are easy. XOR — fire only when the inputs **differ** — is not. The two 'yes' corners sit on opposite diagonals, so **no single straight line** can fence them off. Try it yourself below; you'll cap out at 3 of 4." |
| "Softmax: pᵢ = e^{zᵢ}/Σⱼ e^{zⱼ}." | "Softmax turns a list of raw scores into probabilities that add to 1. Two moves: make every score positive by raising \(e\) to it, then divide by the total so the parts sum to one. Big score → big share. Push a slider and watch one bar quietly steal probability from the rest." |
| "GD update: w ← w − η ∂L/∂w." | "Gradient descent is 'walk downhill, one careful step at a time'. The slope under your feet is \(\partial L/\partial w\). Step the *opposite* way (downhill); \(\eta\) is how big a step you dare. Too big and you leap past the valley and bounce; too small and you crawl. Crank η below and watch the ball overshoot." |

If a smart beginner with no prior exposure could not follow a paragraph cold, rewrite it.

---

## 4. Building the math step by step (every symbol named, in `.eqbox`)

Never drop a finished formula on the reader. Build it. The gold standard's §01 introduces the unit in two
moves — first the weighted sum, then the activation — each in its own `.eqbox`, each preceded by a sentence
naming the new symbols:

```html
<h3>Step 1 — the weighted sum</h3>
<p>Given inputs \(x_1\dots x_n\), the unit has matching weights \(w_1\dots w_n\) and a single bias \(b\).
   It forms the <strong>weighted sum</strong> \(z\):</p>
<div class="eqbox">$$ z \;=\; b + \sum_{i=1}^{n} w_i x_i $$</div>
<p>More compact as a <strong>dot product</strong> of the weight vector \(\mathbf{w}\) and input vector
   \(\mathbf{x}\), plus the scalar bias:</p>
<div class="eqbox">$$ z \;=\; \mathbf{w}\cdot\mathbf{x} + b $$</div>
```

Rules:
- One display equation per `.eqbox`. Wide math (matrices, multi-step chains) scrolls horizontally *inside*
  the box — never the page.
- Name each symbol the instant it appears: "where \(g\) is the hidden activation, applied *element-wise*."
- Introduce notation explicitly when depth grows (the gold standard's §09 spends a whole `.card` defining
  the `W[ℓ]`, `a[ℓ]`, `z[ℓ]`, `a[0]=x` convention before using it).
- Inline math uses `\( \)`; display uses `$$ $$`. Both are configured in the MathJax block (§9).

---

## 5. Writing a FULLY worked example in HTML (every step, real numbers)

Every chapter has at least one worked example — the slide's own, computed end to end. **Zero "it can be
shown that."** The gold standard does this two ways; use whichever fits.

**Way A — a static, fully-shown calculation.** State the numbers up front, show every arithmetic step, bold
the result of each step, end with a one-sentence "so what." The §03 sanity-check note is the model:

> the dot product \(0.2(0.5)+0.3(0.6)+0.9(0.1)=0.1+0.18+0.09=0.37\). Add the bias \(0.5\) to get \(z=0.87\),
> and \(\sigma(0.87)\approx0.7045\) — a confident-ish "yes."

**Way B — a Next-button stepper that reveals one step at a time** (this is what §03 actually ships). Pre-write
the steps in an array; reveal up to `i`; the static steps and any live demo must agree on the same numbers.

```html
<div class="card">
  <h4>Walk it</h4>
  <div class="chips"><button class="btn" id="exStep">▶ Next step</button>
                     <button class="btn" id="exReset">↺ Reset</button></div>
  <div class="readout" id="exOut" style="min-height:150px"></div>
</div>
<script>
window.__demos.push(function(){
  const out=$('#exOut'); if(!out)return;
  const w=[0.2,0.3,0.9], x=[0.5,0.6,0.1], b=0.5;
  const t=w.map((wi,i)=>wi*x[i]);
  const dot=t.reduce((a,v)=>a+v,0), z=dot+b, y=sigmoid(z);
  const steps=[
    'Step 0 — given:\n  w = [0.2, 0.3, 0.9]\n  x = [0.5, 0.6, 0.1]\n  b = 0.5',
    'Step 1 — multiply element-wise (wᵢ·xᵢ):\n  0.2·0.5 = <span class="hl">0.10</span>\n  0.3·0.6 = <span class="hl">0.18</span>\n  0.9·0.1 = <span class="hl">0.09</span>',
    'Step 2 — sum the products (the dot product w·x):\n  0.10 + 0.18 + 0.09 = <span class="g">'+fmt(dot,2)+'</span>',
    'Step 3 — add the bias b:\n  z = w·x + b = '+fmt(dot,2)+' + 0.5 = <span class="g">'+fmt(z,2)+'</span>',
    'Step 4 — apply the activation (sigmoid):\n  y = σ(z) = <span class="g">'+fmt(y,4)+'</span>'
  ];
  let i=0;
  function render(){let s='';for(let k=0;k<=i;k++)s+=(k?'\n\n':'')+steps[k];out.innerHTML=s;}
  render();
  $('#exStep').addEventListener('click',()=>{if(i<steps.length-1){i++;render();}});
  $('#exReset').addEventListener('click',()=>{i=0;render();});
});
</script>
```

The `.readout` uses `\n` newlines (its CSS is `white-space:pre-wrap`), `<span class="hl">` for intermediate
numbers (amber) and `<span class="g">` for final answers (green). Mirror the worked numbers in the chapter's
bespoke interactive so the student can change them and watch the same arithmetic update.

---

## 6. BESPOKE CANVAS RECIPES — the heart of the quality

This is what separates a gold-standard page from a deck of widgets. **Every visual is a plain 2D
`<canvas>`, hand-drawn, built for its one idea.** No chart library. The patterns below are lifted from
`nlp-lecture5-v2.html`; copy and adapt them.

### 6.0 The DPR-aware canvas + draw-loop skeleton (use for ALL of them)

Three universal rules: (a) set the backing store to `cssWidth × devicePixelRatio` so lines are crisp on
retina; (b) keep ALL drawing inside one `draw(state)` function; (c) call `draw()` once on init and again on
every input. The gold standard registers each demo in a global `window.__demos` array and runs them all on
load (§8), so a demo that fails to find its canvas just returns and never throws.

```js
/* a tiny DPR helper — call once per canvas, and again on resize */
function fitCanvas(c){
  const dpr = Math.min(window.devicePixelRatio || 1, 2);   // cap at 2: cheap redraws
  const cssW = c.clientWidth || c.width;                   // CSS px the canvas occupies
  const cssH = c.height;                                   // logical height from the attribute
  c.width  = Math.round(cssW * dpr);
  c.height = Math.round(cssH * dpr);
  const ctx = c.getContext('2d');
  ctx.setTransform(dpr,0,0,dpr,0,0);                        // now draw in CSS px; DPR is automatic
  return { ctx, W: cssW, H: cssH };
}
```

> The gold standard takes the simpler route — it sets a large `width="880"` attribute plus
> `style="width:100%;height:auto"`, letting the browser downscale (already crisp on most screens). The
> `fitCanvas` helper above is the fully DPR-correct version; prefer it for anything with thin 1px lines or
> small text. **Every canvas keeps `style="max-width:100%"` (or `width:100%`) so it never causes horizontal
> overflow**, and re-reads its size on `resize` if you use `fitCanvas`.

The skeleton every demo follows:

```js
window.__demos.push(function(){
  const c = $('#myCanvas'); if(!c) return;          // bail quietly if this chapter isn't present
  const ctx = c.getContext('2d');
  const W = c.width, H = c.height;                   // (or use fitCanvas for DPR)
  function draw(){
    ctx.clearRect(0,0,W,H);
    /* read every control, compute state, paint state, print to .readout */
  }
  $$('#someControl').forEach(el=>el.addEventListener('input', draw));
  draw();                                            // never leave the canvas blank
});
```

A reusable data↔pixel mapper appears in almost every recipe (define it once per demo):
```js
const pad=46;
const PX=v=>pad+v*(W-2*pad);          // data x∈[0,1] → pixel x
const PY=v=>H-pad-v*(H-2*pad);        // data y∈[0,1] → pixel y (note the flip)
```

### Recipe A — function plot + draggable / animated point
*For: activation functions, loss curves, any \(y=f(x)\).* Draw the axes, sweep `x` pixel-by-pixel to trace
the curve, then drop a marker at the selected `x` and print \(f(x)\). Wire a slider **and** pointer-move so
the student can scrub it. *Uncovers:* the exact value and slope at a point — e.g. that ReLU's derivative is
flat 1 for \(z>0\) while sigmoid's slope dies. (Gold standard: §02 activation plotter, §15 loss bowl.)

```js
function curve(f){
  ctx.beginPath();
  for(let px=pad; px<=W-pad; px++){
    const z = xmin + (px-pad)/(W-2*pad)*(xmax-xmin);   // pixel → data
    const y = Y(f(z));
    px===pad ? ctx.moveTo(px,y) : ctx.lineTo(px,y);
  }
  ctx.stroke();
}
/* selected point */
ctx.beginPath(); ctx.arc(X(zsel), Y(f(zsel)), 5, 0, 7); ctx.fill();
/* scrub by hover, mapping mouse px → data, accounting for CSS scaling */
c.addEventListener('mousemove', e=>{
  const r=c.getBoundingClientRect();
  const px=(e.clientX-r.left)*(W/r.width);            // CSS px → backing px
  zsel=clamp(xmin+(px-pad)/(W-2*pad)*(xmax-xmin), xmin, xmax);
  draw();
});
```

For an **animated** point (gradient descent), keep a `requestAnimationFrame`/`setInterval` `step()` that
mutates `w ← w − η·g`, pushes it onto a `trail[]`, and redraws — so the student watches the ball roll, leave
a breadcrumb trail, and (at high η) overshoot or diverge.

### Recipe B — vector / arrow / edge field (a small network whose edges encode weights)
*For: a neuron diagram, a forward pass, any "arrows carry numbers".* Draw nodes as filled+stroked circles
at fixed positions; draw edges as lines whose **color encodes sign** (cyan positive, pink negative) and
**width encodes magnitude**. Label each edge with its weight. *Uncovers:* a weighted sum is literally
"arrows of different strengths feeding a node." (Gold standard: §01 neuron, §06 XOR network, §14 forward/backward.)

```js
function edge(a,b,wt){
  const pos = wt>=0, m=Math.min(1,Math.abs(wt));
  ctx.strokeStyle = pos ? 'rgba(56,240,216,'+(0.25+0.6*m)+')'   // cyan = +
                        : 'rgba(255,110,129,'+(0.25+0.6*m)+')'; // pink = −
  ctx.lineWidth = 1 + 3*m;
  ctx.beginPath(); ctx.moveTo(a.x+18,a.y); ctx.lineTo(b.x-22,b.y); ctx.stroke();
  ctx.fillStyle='#93a4c8'; ctx.font='11px monospace';
  ctx.fillText('w='+fmt(wt,2),(a.x+b.x)/2-16,(a.y+b.y)/2-6);
}
function node(p,col,txt){
  ctx.beginPath(); ctx.arc(p.x,p.y,22,0,7);
  ctx.fillStyle='#0e1729'; ctx.fill();
  ctx.strokeStyle=col; ctx.lineWidth=2.5; ctx.stroke();
  ctx.fillStyle='#fff'; ctx.font='bold 13px monospace'; ctx.textAlign='center';
  ctx.fillText(txt,p.x,p.y+4); ctx.textAlign='left';
}
```
For a **forward pass** the same canvas can light edges/nodes as activation flows through, driven by a
"push input" button (`data-in="1,0"`) that recomputes every value and recolors the live path.

### Recipe C — a small network of nodes that light up (animated or staged)
*For: hero banners, "which layers are active", forward-then-backward.* Same node/edge primitives as B, but
either (i) animated with `requestAnimationFrame` and a phase `t` so connections pulse and nodes breathe
(gold standard hero), or (ii) staged by a Next button so each press lights the next layer / reverses the
arrows for the backward pass (§14). *Uncovers:* the directional, layered flow of computation.

```js
let t=0;
function frame(){
  ctx.clearRect(0,0,W,H); t+=0.018;
  /* edges: opacity pulses with sin(t + index) */
  /* nodes: radius = base + sin(t*1.4+i), with shadowBlur glow */
  requestAnimationFrame(frame);
}
frame();
```

### Recipe D — a distribution / bar set that reshapes from sliders
*For: softmax, a Gaussian, any "scores → shape".* Read the slider values into an array, compute the derived
quantity (probabilities, densities), and draw bars/curve from it. Print the full computation to the
`.readout` so the numbers and the picture agree. *Uncovers:* how raising one input "steals" mass from the
others, and that the parts always sum to 1. (Gold standard: §08 softmax calculator.)

```js
const z = init.map((_,i)=>parseFloat($('#sm'+i).value));   // slider logits
const ex = z.map(Math.exp), S = ex.reduce((a,v)=>a+v,0), p = ex.map(v=>v/S);
const bw=(W-2*pad)/z.length;
p.forEach((pi,i)=>{
  const x=pad+i*bw+bw*0.18, w=bw*0.64, h=pi*(H-2*pad);
  ctx.fillStyle=pal[i%pal.length]; ctx.fillRect(x, H-pad-h, w, h);
  ctx.fillStyle='#fff'; ctx.textAlign='center';
  ctx.fillText((pi*100).toFixed(1)+'%', x+w/2, H-pad-h-8); ctx.textAlign='left';
});
$('#smOut').innerHTML =
  'sum Σ e^zⱼ = <span class="hl">'+fmt(S,3)+'</span>\n'+
  'check Σ probs = <span class="g">'+fmt(p.reduce((a,v)=>a+v,0),4)+'</span>  ✓';
```

### Recipe E — a toggle that overlays / shades a hidden structure
*For: decision boundaries, separable-vs-not, "which region is class 1".* Buttons in a `.chips` row switch
`mode`; `draw()` re-shades the plane by sampling a grid of pixels and coloring each by the model's
prediction, then overlays the boundary line(s). *Uncovers:* "this model carves the space *like this*" — e.g.
one straight cut (logistic regression) vs. a bent region (a 2-layer net). (Gold standard: §05 perceptron
line, §07 LR-vs-MLP.)

```js
const step=11;                                   // coarse grid = cheap shading
for(let px=pad; px<W-pad; px+=step)
  for(let py=pad; py<H-pad; py+=step){
    const x=(px-pad)/(W-2*pad), y=1-(py-pad)/(H-2*pad);
    ctx.fillStyle = COL[ pred(mode,x,y) ] + '0.10)';   // class colour, low alpha
    ctx.fillRect(px,py,step,step);
  }
/* overlay the boundary on top */
ctx.strokeStyle='#ffcb6b'; ctx.lineWidth=2.4;
ctx.beginPath(); ctx.moveTo(PX(0.5),PY(0)); ctx.lineTo(PX(0.5),PY(1)); ctx.stroke();
```
A **draggable line** variant (§05): three sliders set \(w_1,w_2,b\); redraw the line
\(w_1x_1+w_2x_2+b=0\) and count how many of the four points are classified right — letting the student *feel*
that no line ever gets XOR past 3/4.

### Recipe F — clickable cells / switches / tokens (non-canvas, still bespoke)
Some ideas read better as styled DOM than as canvas: the XOR bit-switches (§06), the sliding-window sentence
(§13), the truth tables. These are still bespoke interactives — clickable `.bitsw` switches, a row of
`<span>`s that recolor as the window slides, a `<table>` whose current row gets `.cur`. Drive them the same
way: a `render(state)` that rewrites the DOM and a `.readout` that prints the computation.

### Recipe G — a clickable "big-picture" journey map (canvas navigation)
*For: the overview up top.* Lay the lecture's bands as numbered nodes along a downhill path; hover
highlights a node, clicking jumps to that band. It shows the *shape* before the details and doubles as
navigation. *Uncovers:* how the whole lecture hangs together. Store the node centres **inside** `draw`
(in CSS px) so the hit-test always matches the current size; map the mouse with `getBoundingClientRect()`;
colour each node from a CSS var so it follows the theme.

```js
window.__demos.push(function(){
  const c=$('#mapCanvas'); if(!c) return;
  const css=getComputedStyle(document.documentElement);
  const col=v=>(css.getPropertyValue(v)||'').trim()||'#38f0d8';
  const stops=[{t:'The problem',hash:'#opt',c:'--cyan2'} /* …one per band… */];
  let hover=-1, nodes=[];
  const cv=setupCanvas(c,(ctx,W,H)=>{
    const padX=64, top=54, bot=H-44;
    nodes=stops.map((s,i)=>{const fx=i/(stops.length-1);
      return {x:padX+fx*(W-2*padX), y:top+(bot-top)*(0.16*fx+0.84*fx*fx), s};});
    /* draw the path, then each node: circle + number + label; ring nodes[hover] */
  });
  const pick=ev=>{const r=c.getBoundingClientRect(), mx=ev.clientX-r.left, my=ev.clientY-r.top;
    let b=-1,bd=1e9; nodes.forEach((n,i)=>{const d=(n.x-mx)**2+(n.y-my)**2; if(d<bd){bd=d;b=i;}});
    return bd<1100?b:-1;};
  c.addEventListener('mousemove',ev=>{const h=pick(ev); if(h!==hover){hover=h; c.style.cursor=h>=0?'pointer':'default'; cv.redraw();}});
  c.addEventListener('click',ev=>{const h=pick(ev); if(h>=0) location.hash=nodes[h].s.hash;});
  cv.redraw();
});
```

### Recipe H — pure-canvas 3-D surface, and making it NON-CONVEX
*For: any `z=f(x,y)` surface — a loss landscape, a 2-var function, a probability or attention surface, in any subject — and especially the "local minima — the start matters" idea.* Sample
`z=f(x,y)`, project each point by azimuth+elevation, depth-sort the quads (painter's algorithm), colour by
height, then **drag to rotate** — all with the 2-D canvas API (the `bowlCanvas` block in
`templates/lecture.html` is the full projector). The teaching win is to ship **two** surfaces behind a
toggle: a **convex** bowl (one minimum) and a **non-convex** one with **two valleys**, plus two start
presets so nearly identical starts roll into *different* valleys. *Uncovers:* why initialisation matters and
what a "local minimum" really is. Only `f`, its gradient, and the markers change between modes:

```js
let mode='convex';
const SURF={
  convex:{ f:(x,y)=>0.42*x*x+0.16*y*y, gx:(x,y)=>0.84*x, gy:(x,y)=>0.32*y,
           mins:[[0,0]], hill:null, A:{x:2.7,y:2.8}, B:{x:-2.6,y:-2.5} },
  bumpy:{  f:(x,y)=>0.06*(x*x-4)*(x*x-4)+0.18*y*y,      // double well: minima at x = ±2
           gx:(x,y)=>0.24*x*(x*x-4), gy:(x,y)=>0.36*y,
           mins:[[-2,0],[2,0]], hill:[0,0], A:{x:-0.7,y:2.7}, B:{x:0.7,y:2.7} }
};
const S=()=>SURF[mode];
const f=(x,y)=>S().f(x,y), gx=(x,y)=>S().gx(x,y), gy=(x,y)=>S().gy(x,y);
// clamp the ball to the domain so a big rate can't fling it off the grid:
function step(){p={x:clamp(p.x-lr*gx(p.x,p.y),-R,R), y:clamp(p.y-lr*gy(p.x,p.y),-R,R)}; /* … */}
```

Draw every `S().mins` as a green dot and `S().hill` (if any) as a red dot; the readout names which valley
the ball settled in (a `nearestMin()` helper). The PDF twin is `figstyle.surface3d(f, xlim, ylim, title,
path=[...])`, which lifts a descent path onto the surface for the companion.

### Recipe I — annotate & animate a lab (arrows, labels, auto-play)
*For: turning a correct-but-static plot into one that explains itself.* Three cheap moves add most of the
"intuitive":
- **A direction arrow at the moving point.** On a curve, draw a short arrow in the downhill direction
  (`dir = slope>0 ? -1 : +1`) with a "downhill" label, so the student sees *which way* the next step goes.
- **On-canvas labels for landmarks** (each minimum, the target) so the picture is legible without the prose.
- **An `auto ▶` toggle** that animates the loop and **stops itself at convergence** — keep manual
  `step`/`run` too, and never autostart (respect reduced motion):

```js
let auto=null;
function setAuto(on){const b=$('#xAuto');
  if(on){ if(auto) return; b.textContent='⏸ stop'; b.classList.add('active');
    auto=setInterval(()=>{ if(Math.abs(df(x))<0.08){ setAuto(false); return; } step(); },320); }
  else { clearInterval(auto); auto=null; b.textContent='auto ▶'; b.classList.remove('active'); }}
```

### Wiring rules for every recipe
- **One `draw(state)` / `render(state)`** does *all* painting; controls only mutate state then call it.
- **Smoothness:** for continuous inputs use the natural `input` event and keep `draw()` cheap; for
  animations use `requestAnimationFrame`, not nested timers. Cap DPR at 2 so redraws stay fast.
- **Initialize on load** — call `draw()` at the end of the demo so the panel is never blank before first input.
- **Print numbers, not just pixels.** Every interactive pairs its canvas with a `.readout` that shows the
  live arithmetic, using `.hl`/`.g` spans. The picture builds intuition; the console keeps it honest.
- **Toggle buttons:** clear `.active` on siblings, set it on the clicked one, update `mode`, redraw.
- **Map mouse → data** through `getBoundingClientRect()` and the canvas/CSS scale factor (`W/r.width`),
  never raw `clientX`.

---

## 7. The chrome: sidebar scroll-spy TOC, progress bar, MathJax, theme toggle, guided tour

All of this exists, working, in `nlp-lecture5-v2.html`. Copy it. Don't reinvent it.

### 7.1 Layout shell + sidebar
A CSS grid `grid-template-columns:288px 1fr`. The sidebar is `position:sticky; top:0; height:100vh;
overflow-y:auto`, holding the grouped TOC from §1. On mobile, collapse the grid to a single column.

### 7.2 Scroll-spy TOC + progress bar (one scroll handler)
A fixed `.progress > i#progbar` whose width tracks scroll fraction, and `.toc a.active` that follows the
section in view. One `onScroll` does both:

```js
const tocLinks=$$('#toc a');
const sections=tocLinks.map(a=>$(a.getAttribute('href')));
function onScroll(){
  const st=window.scrollY, h=document.body.scrollHeight-window.innerHeight;
  $('#progbar').style.width=(100*st/h)+'%';
  let idx=0;
  sections.forEach((sec,i)=>{ if(sec && sec.offsetTop-120<=st) idx=i; });
  tocLinks.forEach((a,i)=>a.classList.toggle('active', i===idx));
}
window.addEventListener('scroll', onScroll, {passive:true});
```

### 7.3 MathJax — configure first, typeset last
Load **only** MathJax, from cdnjs, with `startup:{typeset:false}`, then typeset once after every demo has
built its DOM (so injected math renders). This is the single external dependency.

```html
<script>
window.MathJax = {
  tex: { inlineMath: [['\\(','\\)']], displayMath: [['$$','$$'],['\\[','\\]']] },
  svg: { fontCache: 'global' },
  startup: { typeset: false }
};
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-svg.min.js"></script>
```
```js
window.addEventListener('load',()=>{
  runDemos(); initTheme(); initReveal(); initStory(); onScroll();
  if(window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise();   // typeset AFTER demos build DOM
});
```
> Note: the new `templates/lecture.html` sets `startup:{typeset:true}` because it has no DOM-injected math.
> If any chapter injects math into the page from JS, use `typeset:false` + a manual `typesetPromise()` as
> above (the gold-standard pattern), and re-typeset only the changed node after dynamic updates:
> `MathJax.typesetPromise([node])`.

### 7.4 Theme toggle (light/dark, persisted in localStorage)
A pre-paint inline script reads the saved theme before first render (no flash); a top-right button flips
`data-theme="light"` on `<html>` and saves it. The `[data-theme="light"]` block restyles **page chrome
only** — interactive consoles, `.lab` panels, and `.eqbox` plates stay dark so canvases keep their contrast.

```html
<script>(function(){try{var t=localStorage.getItem('lecTheme');
  if(t==='light')document.documentElement.setAttribute('data-theme','light');}catch(e){}})();</script>
```

### 7.5 Guided tour (optional but expected at this bar)
A `STORY[]` array — one `{id, t, x}` per chapter — drives a bottom "story card" with prev/play/next/exit and
a spotlight that scrolls to and rings each section's heading. Auto-advances on a timer; arrow keys and space
also drive it. Lift `STORY`, `startStory/endStory/nextStory/prevStory/togglePlay`, and the `.storycard` /
`.spot` markup straight from the gold standard, and write **one story line per chapter** in the same warm,
"here's what to try" voice:

```js
const STORY=[
 {id:'intro', t:'Welcome', x:'We go from one idea all the way to the payoff — intuition first, then the exact math. Use ▶/◀ or arrow keys; space pauses.'},
 {id:'neuron', t:'The neural unit', x:'Everything starts here: a weighted sum, a bias, a squash. Drag the sliders to watch z and y form live.'},
 /* ...one entry per chapter, ending on the summary... */
];
```

### 7.6 Scroll-reveal (optional)
An `IntersectionObserver` fades `.reveal` elements in. **Critical caveat from the gold standard:** never put
`.reveal` (opacity/transform) on anything containing a `<canvas>` — promoting the canvas to its own layer can
freeze/blank the demo. Skip `.lab` blocks and any element holding a canvas.

---

## 8. The script architecture (demo registry + shared helpers)

Define shared helpers **once**, before any demo uses them (cleanliness rule: every helper defined before
use). The gold standard's header block:

```js
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const fmt=(x,d=3)=>{ if(Math.abs(x)<1e-9)x=0; return x.toFixed(d); };
const sigmoid=z=>1/(1+Math.exp(-z));
const relu=z=>Math.max(0,z);
const dsig=z=>{const s=sigmoid(z);return s*(1-s);};
/* ...whatever math your topic needs... */

window.__demos=[];                                  // every chapter pushes its init here
function runDemos(){ window.__demos.forEach(f=>{ try{f();}catch(e){console.error(e);} }); }
```
Each chapter's demo is a self-contained `window.__demos.push(function(){ ... })` that bails (`if(!c)return`)
when its canvas is absent — so a missing chapter never throws and the page degrades gracefully. `runDemos()`
fires on `load` (§7.3). This registry pattern is why the gold standard has 20+ independent interactives in
one file with zero cross-talk.

---

## 9. House idiom — the exact tokens (the gold-standard palette)

This is the rich dark theme of `nlp-lecture5-v2.html` — **not** the older Slate palette. Put these in
`:root`:

```css
:root{
  --bg:#070b16; --bg2:#0b1120; --panel:#0e1729; --panel2:#121d36; --line:#1f2d4d;
  --ink:#e7edf9; --muted:#93a4c8; --dim:#64759c;
  --cyan:#38f0d8; --cyan2:#19c4ff; --violet:#9b8cff; --pink:#ff6ec7;
  --amber:#ffcb6b; --green:#62e88a; --red:#ff6b81;
  --glow:0 0 18px rgba(56,240,216,.45); --r:16px;
  --mono:'SFMono-Regular',ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace;
}
```
- **Accent meanings** (keep consistent across all canvases): cyan `#38f0d8`/`#19c4ff` = inputs & primary
  accent & positive weights; violet `#9b8cff` = hidden/intermediate; pink `#ff6ec7` = output; amber
  `#ffcb6b` = the key/boundary/highlight; green `#62e88a` = "fired"/correct/final; red `#ff6b81` =
  negative/wrong.
- **Fonts:** system UI sans for prose (`Inter, system-ui, ...`) and a mono stack for all numbers/consoles —
  **loaded from the OS, no Google Fonts fetch.** Keeps the file truly self-contained.
- **Component CSS** (`.card`, `.lab` + its ⚡ badge, `.note`, `.key`, `.eqbox`, `.readout`, `.ctrl` with the
  glowing thumb, `.btn`, `.chips`, `.grid2/3`, `.toc`, `.progress`, `.topbtn`, `.storycard`, `.spot`) is all
  in the gold standard's `<style>`. **Copy that stylesheet wholesale** and re-theme only if the topic
  genuinely needs it. The slider thumb glow, the ⚡ badge, the `.readout` console, and the `[data-theme=light]`
  overrides are load-bearing — don't drop them.

The only external `<script>` in the whole file is MathJax from cdnjs. If you find yourself adding any other
CDN, stop — hand-draw it on canvas instead.

---

## 10. No-overflow / responsive + CLEANLINESS contract

The page must be clean and unbroken from **360px to 1440px**, and ship without a single leaked artifact.

**No-overflow / responsive**
- **Canvases:** every `<canvas>` carries `style="width:100%;height:auto"` (or `max-width:100%`) so it scales
  down and never pushes the page sideways. Re-read size on `resize` if using `fitCanvas`.
- **Wide math:** every display equation sits in an `.eqbox` (which is `overflow-x:auto`) so long matrices
  scroll *inside the box*, never the page. Also clamp containers: `mjx-container[display="true"]{overflow-x:auto;max-width:100%}`.
- **Prose:** long tokens wrap (`overflow-wrap:anywhere`); never set a `px` width on a prose container.
- **Controls stack on mobile:** `.ctrl` rows and `.chips` already `flex-wrap`; `.grid2`/`.grid3` collapse to
  one column under 880px (`@media(max-width:880px){.grid2,.grid3{grid-template-columns:1fr}}`).
- **Sidebar:** collapses to a single-column layout under the mobile breakpoint; never overlaps content.
- **Page-level backstop:** keep `overflow-x` controlled — but fix the real cause, don't rely on the clip.
- Mentally test at 360px: do `.ctrl`/`.chips` wrap? does the widest matrix scroll in its `.eqbox`? does the
  canvas shrink? does the sidebar collapse? If any "no", fix before shipping.

**Cleanliness (a leaked comment already embarrassed us — these are hard fails)**
- **No HTML comment may contain a nested `-->` or `<!--`.** When you describe markup inside a comment,
  paraphrase it; never paste literal comment delimiters into a comment. Section-divider comments like
  `<!-- ============ 06 SOLVING XOR ============ -->` are fine; comments *quoting other comments* are not.
- **No visible `{{PLACEHOLDER}}` anywhere a reader could see it.** The new `templates/lecture.html` ships
  with `{{FORMULA}}`, `{{param}}`, `{{slug}}`, `{{init}}` deliberately — those are scaffold tokens you MUST
  replace with real content. Grep the final file for `{{` and `}}`; if either survives, you are not done.
- **All JS valid, every helper defined before use.** No reference to a function or `const` that appears
  later in the file. Demos go in the `__demos` registry; shared helpers go in the header block above them.
- **MathJax actually typesets.** After loading, confirm equations render as math, not raw `\(...\)` source.
  If you inject math from JS, you must call `typesetPromise()` (§7.3).
- **Opens from `file://` by double-click.** No `type="module"`, no `fetch`, no localhost, no keys, one file.

### 10.1 Verify every demo actually RUNS — a syntax check is not enough

The registry pattern (§8) wraps each demo in `try/catch`, so a demo that throws does **not** crash the
page — it silently leaves a **blank panel** (empty canvas + empty `.readout`). A real bug we shipped once:
a shared curve-drawer called `X.inv(px)`, but three demos defined `X` without an `.inv`. They parsed fine
(`node --check` passed) yet drew nothing. Lesson: **execute every demo before shipping, don't just lint the
syntax.** Two cheap ways:

- Open the file, watch the console, and click through every lab — no errors, no blank panels.
- Run a head-less harness: stub `document` / `window` / `canvas.getContext` (a `Proxy` of no-ops), plus
  `getComputedStyle`, `localStorage`, `requestAnimationFrame`, `location`, `matchMedia`; `eval` the page's
  main `<script>`; fire the saved `load` handler so `runDemos()` runs; then assert no `console.error` fired.
  A ~60-line Node script does this and catches exactly the class of bug above.

```js
// harness.js (sketch): node harness.js lecture.html  ->  "ALL DEMOS RAN WITH NO ERRORS"
const errs=[]; console.error=(...a)=>errs.push(a.join(' '));
const ctx=new Proxy({},{get:(t,p)=>p in t?t[p]:()=>{}, set:(t,p,v)=>{t[p]=v;return true;}});
const el=()=>({style:{},dataset:{},classList:{add(){},remove(){},toggle(){return false;}},
  getContext:()=>ctx, getBoundingClientRect:()=>({width:440,height:330,left:0,top:0}),
  addEventListener(){}, appendChild(c)=>c, querySelectorAll:()=>[], closest:()=>null,
  width:440,height:330, set innerHTML(_){}, set textContent(_){}});
global.window={addEventListener:(e,cb)=>{if(e==='load')global.__load=cb;}, devicePixelRatio:1,
  requestAnimationFrame:()=>0, setInterval:()=>0, clearInterval(){}, localStorage:{getItem:()=>null,setItem(){}},
  matchMedia:()=>({matches:false})};
Object.assign(global,{document:{querySelector:el,querySelectorAll:()=>[],createElement:el,addEventListener(){},
  documentElement:el(),body:{scrollHeight:2000}}, getComputedStyle:()=>({getPropertyValue:()=>'#38f0d8'}),
  location:{hash:''}, requestAnimationFrame:window.requestAnimationFrame, setInterval:window.setInterval,
  clearInterval:window.clearInterval, localStorage:window.localStorage, matchMedia:window.matchMedia});
eval(BIG_SCRIPT); global.__load && global.__load();   // runs runDemos()
console.log(errs.length? 'DEMO ERRORS: '+errs.join(' | ') : 'ALL DEMOS RAN WITH NO ERRORS');
```

---

## 11. Ship checklist (final gate — mirrors quality_rubric.md)

Tick every box; any red-list item is an automatic fail regardless of polish. The full rubric lives in
`references/quality_rubric.md` (clear **85/100**, zero red-list items, to ship).

- [ ] **Coverage:** every concept/slide from the deck has its own chapter, in teaching order, grouped into
      4–6 named sidebar bands. ~12–20 chapters for a real lecture. **Nothing dropped.**
- [ ] **Spine:** every chapter runs hook → intuition+analogy → math step by step → fully worked example →
      bespoke interactive → ML/AI → pitfall/key → bridge, using the right component each step.
- [ ] **Easy language:** short sentences, each term defined on first use, analogy before algebra. A smart
      beginner never gets lost. (Sample 5 paragraphs.)
- [ ] **Worked examples:** every slide example computed in full, every step shown, real numbers, final
      number highlighted in the `.readout`. **Zero "it can be shown that."**
- [ ] **Math builds up:** every symbol named the moment it appears; one equation per `.eqbox`; wide math
      scrolls in-box.
- [ ] **Bespoke interactives:** every major concept has its own hand-drawn canvas (or bespoke DOM) demo that
      **reveals** the idea — name the one thing it uncovers. **No generic charts, no decoration.** Each pairs
      a canvas with a `.readout`, initializes on load, and runs from `file://`.
- [ ] **Chrome:** grouped scroll-spy sidebar TOC, top progress bar, MathJax manual typeset, theme toggle
      (persisted, page-chrome only), optional guided tour with one story line per chapter.
- [ ] **House idiom:** the `#070b16` dark palette + the gold-standard component classes (`.card/.lab/.note/
      .key/.eqbox/.readout/.ctrl/.btn/.chips/.grid2/3`), consistent accent meanings, OS fonts only.
- [ ] **No overflow:** clean 360→1440px; canvases scale; `.eqbox` math scrolls in-box; `.ctrl`/`.chips` wrap;
      grids collapse; sidebar collapses; no horizontal page scroll.
- [ ] **Cleanliness:** no nested `-->`/`<!--` inside any comment; zero surviving `{{...}}`; every helper
      defined before use; MathJax renders; nothing throws in the console.
- [ ] **Demos verified, not just parsed:** every `window.__demos` entry actually *runs* — a syntax check is
      not enough. A missing method, a typo'd id, or a helper used before it is defined throws only at runtime
      and leaves a blank panel. Click through every lab (console clean) or run the head-less harness (§10.1).
- [ ] **Colour legend + consistent accents:** a `.legendbar` near the top fixes the meaning of each accent,
      and every canvas obeys those same meanings (§9). Colour itself should carry information.
- [ ] **Self-contained:** ONE `.html`, opens by double-click, MathJax-from-cdnjs as the **only** external
      dependency, every other visual hand-drawn on canvas. No Plotly/D3/Tailwind/Google-Fonts/keys/fetch.

Coverage, worked-example completeness, and bespoke-revealing interactives are the three that fail most
often — verify them first. **And before you call it done: open `nlp-lecture5-v2.html` beside your page. If
yours feels thinner, it is. Go back.**

---

## 12. The "out of this world" layer — signature upgrades (still keyless, still one file)

The spine above earns the 85. These additions take a good page to a page students *remember*.
All are hand-built — **no new dependency** (MathJax stays the only external script), all open from
`file://`, all responsive, all skippable on mobile. Add them on top, never in place of, §1–11.

1. **"Check yourself" active recall (one per band).** After a band of chapters, a small card asks
   one question and hides the answer behind a **Reveal** button; revealing shows the answer *and the
   one-line why*. Recall, not re-reading, is what makes it stick. Pure DOM + a click handler; the
   answer lives in a hidden `<div>` you toggle.
2. **A "big picture" map up top.** A single bespoke `<canvas>` (or a clean grid of `.card`s) that shows
   the whole lecture as one diagram — the rungs/stages and how each leans on the last — with each node
   linking to its chapter (`onclick → location.hash`). The student sees the shape before the details
   and can jump anywhere. Re-skin the hero canvas you already have.
3. **A synthesis interactive at the end.** One last `.lab` that ties the whole lecture together — e.g.
   a slider that sweeps the *one axis the lecture was really about* (here: how much context a method
   uses) and lights up which method/row it lands on, with the trade-off printed live. It rewards
   finishing and cements the through-line.
4. **Copy buttons on prompts/code/long equations.** A tiny `navigator.clipboard.writeText` button on
   each `<pre>`/prompt block. Keyless, two lines of JS, and students actually use it.
5. **Polish that signals quality.** Respect `prefers-reduced-motion` (you already gate `.reveal`);
   give buttons/sliders visible `:focus-visible` outlines; make the guided tour reachable by keyboard;
   keep tap targets ≥ 40px on mobile. None of this is decoration — it is the difference between "a
   page" and "a tool".
6. **A non-convex 3-D landscape.** Beyond the convex bowl, ship a bumpy surface with two valleys and two
   start presets, so the student *feels* that the starting point decides which local minimum you reach
   (**Recipe H**). It is the single most effective way to make "local minima" real.
7. **Animated, annotated labs.** A direction arrow at the moving point, on-canvas landmark labels, and an
   `auto ▶` that animates a run and stops at convergence (**Recipe I**). Motion plus a labelled "which way"
   turns a static plot into an explanation.
8. **A persistent colour legend.** One `.legendbar` near the top fixes the meaning of each accent (cyan =
   step/input, amber = the key number, green = converged/minimum, red = diverges/error, violet =
   direction/hidden). Keep those meanings identical in every canvas so colour carries information.

**Concrete patterns for the above** (proven in Session 9 — *Gradient Descent*): the journey map is
**Recipe G**, the convex↔bumpy 3-D toggle is **Recipe H**, the arrows / labels / `auto ▶` are **Recipe I**.
The "check yourself" card (item 1) is pure DOM with one delegated handler:

```html
<div class="recall"><div class="q">A question?</div>
  <button class="btn" data-recall>Reveal answer</button>
  <div class="ans">The answer, plus the one-line why.</div></div>
```
```js
function initRecall(){ $$('[data-recall]').forEach(b=>b.addEventListener('click',function(){
  const open=this.closest('.recall').classList.toggle('open');
  this.textContent=open?'Hide answer':'Reveal answer'; })); }   // call in the load handler
```
CSS: `.recall .ans{display:none}` and `.recall.open .ans{display:block}`. MathJax still typesets a hidden
answer, so it renders correctly the moment it is revealed.

Keep every addition honest by the same test as every interaction (§0): *name the one thing the student
gains.* If an upgrade does not help them learn or navigate, cut it.
