# plain_language.md — the ONE source of truth for "easy English"

Both deliverables (the companion **PDF** and the interactive **HTML**) must read like a
patient friend explaining the idea at a kitchen table — not like a journal paper. This file
is the single, shared rulebook for that voice. The other style guides point here; the two
linters (`scripts/lint.py` for HTML, `scripts/lint_tex.py` for the companion) enforce the
lists below automatically. **Read it before writing a word, and run the linters before you
ship.**

> The bar in one line: *a smart 16-year-old, or a tired student the night before the exam,
> reads any paragraph once and gets it.* Keep the depth and the math — change only the words
> and the shape, never the rigor.

---

## 1. The hard rules (non-negotiable)

1. **Short sentences.** Aim for **15 words**; the hard ceiling is **22**. One idea per
   sentence. If you used "and", "which", "; ", or a comma to bolt two ideas together, split it.
2. **Common words.** Use the plainest word that is still correct. If a 10-year-old wouldn't
   know the word and a simpler one exists, swap it (see the table in §3). Technical terms are
   fine — but *define each one the first time*, in plain words, inline.
3. **Define on first use, every time.** First mention of a term: *italicise it, give a
   one-line plain meaning, then the symbol, then a number.* Example: "the *learning rate*
   (how big a step we take), written \(\eta\), say \(\eta=0.1\)."
4. **Spell out every symbol and acronym on first use.** "\(\lambda\) (the Greek letter
   lambda)"; "POS (part of speech)". Never let a naked symbol or acronym appear cold.
5. **Analogy before algebra.** Every tricky idea meets the reader in the real world *before*
   it meets them in symbols.
6. **Active voice, present tense, "we" and "you".** "We add the bias." not "The bias is
   added." "You read the tag off the first piece." not "The tag is read off…".
7. **No hand-waving.** Never skip a step. Banned outright: see §4.
8. **No literary fog.** This is a study aid, not an essay. No extended metaphors that hide
   the mechanism, no "the field has since dissolved into…" flourishes. Say the plain thing.
9. **Show, don't pile up prose.** If three sentences would be a clearer *table, list, or
   labelled picture*, make the table/list/picture (see §6).
10. **Target reading level: US grade 9 or below** (Flesch Reading Ease ≥ 60). The linters
    estimate this and flag prose that drifts above it.
11. **Right-size it — simple things stay simple.** Match the length of an explanation to
    the size of the idea. An easy idea gets two or three short sentences, one picture at
    most, and no ceremony. Find the most intuitive way in, lead with it once, and move on.
    Depth belongs where the difficulty really is. (Full rules in §8.)

---

## 2. The rewrite move (terse slide → plain teaching prose)

The slide is a telegram. Expand it; don't transcribe it. The pattern:

> **hook question → plain answer in one breath → name the pieces → the formula, built up →
> a number.**

Real before/after, taken from this very course (Session 7, POS tagging):

| ✗ Too hard / too literary (before) | ✓ Plain and clear (after) |
|---|---|
| "This session is the modern story: how deep learning took the task to near-human accuracy, and how the job has since dissolved into the machinery of large language models." | "Older methods hand-built the rules. This session shows the modern way: deep learning pushed accuracy close to a human's. Today, tagging is just one small job inside a large language model." |
| "A tagger's real work is disambiguation: using the neighbours to decide which job a word is doing here." | "So the tagger's real job is to choose. It reads the words nearby to decide which role a word is playing this time. (The fancy name for this is *disambiguation* — picking the right meaning.)" |
| "To turn scores into probabilities we exponentiate and divide by the total over every possible sequence — the partition function \(Z\)." | "Now we turn scores into probabilities. Two steps. First, make every score positive with \(e^{\text{score}}\). Then divide by the total of all of them, a number we call \(Z\)." |
| "Each rung of the ladder is really 'how many of those context-only errors did we just erase?'" | "So ask one question at each step: how many of those mistakes did this new method fix?" |

Keep the math identical. Only the *words around it* get simpler and shorter.

---

## 3. Plain-word swaps (the linters flag the left column)

Prefer the right-hand word. These are the common offenders; the linters warn on the left
column and suggest the right. (Use judgment — a flagged word is occasionally the only correct
one; the gate fails only when many pile up.)

| Don't write | Write instead |
|---|---|
| utilize / utilise / employ (= use) | use |
| leverage | use |
| facilitate | help |
| demonstrate | show |
| illustrate (= show) | show |
| obtain | get |
| require | need |
| sufficient | enough |
| numerous / a multitude of / myriad / plethora | many / a lot |
| additional | more / extra |
| approximately | about |
| prior to | before |
| subsequently | then / later |
| in order to | to |
| commence | start |
| terminate | end / stop |
| furthermore / moreover | also |
| thus / hence / therefore / consequently / whence | so |
| nevertheless / nonetheless | but / still |
| regarding / pertaining to | about |
| aforementioned | this / that |
| possess | have |
| comprise / encompass | include / have |
| elucidate / expound | explain |
| ascertain / determine (= find out) | find out |
| endeavour | try |
| crucial / pivotal / paramount | key / important |
| robust | strong / reliable |
| novel (= new) | new |
| ubiquitous | everywhere |
| salient | key / main |
| methodology | method |
| utilization | use |
| dichotomy | split / contrast |
| in essence / essentially / fundamentally | (usually just delete it) |
| it is important to note that | (delete; just say the thing) |

**Banned flourish phrases** (vague, "literary", or filler — the linter flags them):
"dissolve into", "the machinery of", "earns its keep", "the chase for", "at the heart of"
(unless literal), "a tapestry of", "the dance of", "lies at the intersection of", "in the
realm of", "needless to say", "it goes without saying", "suffice it to say".

---

## 4. Hand-waving — banned outright (these FAIL the linter)

Never write any of these. If a step is "easy", it costs one line to show it — so show it.

- "it can be shown that", "it can be proven that", "it follows that" (without the step)
- "it is easy to see", "it is clear that", "clearly", "obviously", "evidently", "plainly"
- "trivially", "trivial to", "as is well known", "of course" (when skipping a step)
- "left to the reader", "the details are omitted", "after some algebra", "after simplification"
- "intuitively obvious", "it should be apparent"

The fix is always the same: **replace the hand-wave with the one or two lines it was hiding.**

---

## 5. Sentence-shape checklist (apply to every paragraph)

- [ ] Longest sentence ≤ 22 words; most ≤ 15.
- [ ] No sentence carries two ideas. (Split on "and", "but", ";", or a mid-sentence comma.)
- [ ] Every term is defined the first time, inline, in plain words.
- [ ] Every symbol and acronym is spelled out on first use.
- [ ] No word from the §3 left column survives without a reason.
- [ ] No phrase from §4 appears at all.
- [ ] Active voice; "we"/"you"; present tense.
- [ ] An analogy or plain restatement comes *before* the first formula of the concept.

---

## 6. "Easier ways to represent the slides" — show it, don't say it

Dense prose is the enemy of a study aid. Wherever the content allows, **turn paragraphs into
a picture, a table, or a short labelled list.** This keeps full depth while making the page
scannable. Reach for:

- **A comparison table** instead of a paragraph contrasting two or more things. (Methods vs.
  context-used vs. accuracy; greedy vs. CRF; zero-shot vs. few-shot.)
- **A labelled diagram / figure** for any pipeline or flow (PDF: a `\housefig` matplotlib
  PNG or inline TikZ; HTML: a bespoke `<canvas>`). One clear message per picture, with a
  one-line "how to read it".
- **A "ladder" or numbered list** for a sequence of stages, each rung one short line.
- **A worked example in `steps`** (PDF) / a step-through (HTML) for anything numeric — every
  number shown, the answer highlighted.
- **A tiny glossary line** the first time a cluster of symbols appears, instead of a wall of
  definitions in a paragraph.

Rule of thumb: *if a sentence is really a list of parallel items, make it a list. If a
paragraph is really comparing things, make it a table.*

---

## 7. How the linters use this file

- **`scripts/lint.py`** (HTML) and **`scripts/lint_tex.py`** (companion `.tex`) both:
  - flag visible sentences over the word ceiling (and FAIL if too many are long);
  - flag every §4 hand-waving phrase as a hard FAIL;
  - flag §3 fancy words and §3 flourish phrases (WARN; many → FAIL);
  - estimate a Flesch reading-ease score and warn when prose reads above ~grade 9.
- `lint_tex.py` additionally guards the **layout** rules that keep the PDF clean — most
  importantly that worked-example steps use the `steps` environment so "Step N." can never
  spill outside a callout box (see `companion_style.md` §6 and the template).

Run them, read the report, fix every FAIL, and re-run until clean. Boring-but-clear always
beats clever-but-dense.

---

## 8. Simple things stay simple (right-sizing)

Plain words are half the job. The other half is **not over-explaining**. A simple idea
buried under three analogies and a five-step build-up stops being simple — length is its
own kind of fog. So: match the size of the explanation to the size of the idea.

The right-sizing rules:

1. **Find the most intuitive way in first.** Before writing a concept, ask: *what is the
   one example, picture, or sentence that makes this click?* Write that first. Everything
   else supports it. If you can't name the best way in, you're not ready to write.
2. **One analogy — the best one.** Never stack analogies. And if the idea is already an
   everyday thing (a table of numbers, adding two shopping lists), skip the analogy:
   the thing is its own picture.
3. **If two sentences cover it, stop at two.** The teaching spine (hook → intuition →
   math → example → …) is a *maximum* scaffold, not a minimum word count. For an easy
   concept every part shrinks: a one-line hook, a two-line intuition, straight to the
   example.
4. **No ceremony.** No long wind-ups, no "before we begin", no re-deriving what the
   reader just saw one section ago. Get to the idea, land it, bridge on.
5. **Spend depth where the difficulty lives.** The reader's attention is a budget. A
   lecture has two or three genuinely hard ideas; give *those* the full treatment, and
   keep the easy ideas quick so the hard ones stand out.

The test for every explanation: *would a good teacher say this across a kitchen table,
or is it performing thoroughness?* Cut until it sounds like the teacher.

## 9. Friendly names — the lexicon (name it once, use it everywhere)

Formal terms are heavy to carry: "the null-space vector", "row-echelon form",
"an inconsistent augmented system". Great teaching coins **one short plain
nickname per recurring object** and then uses it everywhere, so the reader
thinks in pictures while learning the official words on the side.

The rules:

1. **Coin 5–10 nicknames per lecture, before writing** (part of ingest). Each is
   short, concrete, and honest about what the thing does: equations = *clues*,
   unknowns = *hidden numbers* or *dials*, null vectors = *silent moves* (change
   every dial, land in the same place), echelon form = *the staircase*, the
   inverse = *the undo button*, a redundant equation = *an echo*.
2. **Introduce each nickname exactly once, beside the formal term** — "this is
   called the \vocab{null space}; we'll call these *silent moves*" — then use
   the nickname in prose, figure labels, canvas labels, and readouts alike.
   The formal term reappears at exam-relevant moments so it also sticks.
3. **Be consistent.** One nickname per object, the same nickname in the PDF, the
   HTML, every figure, and every demo. A lexicon that drifts is worse than none.
4. **Decode at the end.** Close with a small `friendly → textbook` table so the
   reader can open any textbook and recognise old friends. The nickname is a
   ramp, not a replacement.
5. **Don't force it.** A term that is already plain (a *row*, a *table*) needs
   no nickname; and never coin a cute name that hides what the object really
   is. The nickname must make the *behaviour* visible, or it earns no place.

Nicknames work best inside **one story-world** (a detective case, a kitchen, a
factory) chosen for the whole lecture — see `intuition_playbook.md` §A. The
linters do not check this section; the rubric does.
