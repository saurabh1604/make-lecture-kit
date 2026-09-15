# Prompt cookbook — copy, paste, study

Ready-made prompts for **make-lecture-kit**. Copy one into your chat
(Claude Code, Claude Cowork, or OpenAI Codex), swap in your topic, and go.
Attach your lecture material whenever you have it — slides (PDF/PPTX), a session
transcript (doc/docx/pdf/txt), or notes; the kit gets much better when the
assistant can read the real material, and you can attach more than one at once
(see prompt 9).

---

## 1. The full kit from your slides

**When to use:** you have the lecture slides and want everything — the study PDF and the interactive lecture.

```text
Use make-lecture-kit on the attached lecture slides. Build the full kit:
the companion PDF and the complete interactive lecture. Cover every
concept, work every example from the slides out in full, and keep the
language simple — this is my first time seeing this topic.
```

## 2. Companion PDF only

**When to use:** you just want the printable study document, not the web page.

```text
Use make-lecture-kit, but only the companion part: turn the attached
lecture into companion.pdf — plain English, an everyday analogy before
each piece of math, and every slide example fully worked with real
numbers. Skip the interactive lecture for now.
```

## 3. Interactive lecture only

**When to use:** you want the play-with-it web page, not the PDF.

```text
Use make-lecture-kit, but only the interactive lecture part: rebuild the
attached lecture as lecture.html — the whole lecture as a story, with an
interactive lab (sliders, steps, toggles) for every key idea. Run the
lint and fix any FAILs before you finish. Skip the PDF for now.
```

## 4. Make it simpler

**When to use:** the kit exists, but parts of it still read like a textbook.

```text
The make-lecture-kit output you made is still too hard for me in places.
Go through both the companion and the interactive lecture and simplify:
shorter sentences, simpler everyday words, define every term the first
time it appears, and add a relatable analogy before each block of math.
Then rebuild both files.
```

## 5. More worked examples for one topic

**When to use:** one concept only clicks for you through examples.

```text
In the make-lecture-kit output for this lecture, add two or three more
fully worked examples for <topic X> — different numbers each time, every
step shown, nothing skipped. Add them to both the companion and the
matching chapter of the interactive lecture, then rebuild both.
```

## 6. Expand confusing math step by step

**When to use:** a specific derivation or formula loses you halfway through.

```text
The math in the <section Y> part of the make-lecture-kit companion
confuses me. Expand it step by step: name every symbol, show every
single step from one line to the next, and say in one plain sentence
why each step is taken. Then recompile the PDF.
```

## 7. Exam-prep edition

**When to use:** exam soon — you need the examinable core plus practice.

```text
Use make-lecture-kit on the attached lecture, but make it an exam-prep
edition: focus on what's examinable, flag the formulas and results I
must know cold, keep all the fully worked examples, and add practice
questions with complete solutions at the end of the companion.
```

## 8. Fix-it: lint reported FAILs

**When to use:** `scripts/lint.py` flagged problems in your lecture.html.

```text
lint.py reported FAILs on my make-lecture-kit lecture page. For each FAIL,
grep for the exact snippet it printed and fix just that block — don't
rewrite the whole file. Re-run python3 scripts/lint.py
output/<my-topic>/lecture.html until it passes. Show me the final lint
output.
```

## 9. Multiple sources at once

**When to use:** you have slides *and* something extra — a transcript of the
session, or the instructor's own notes — and want both used.

```text
Use make-lecture-kit on the attached lecture slides. I'm also attaching
the full session transcript (and instructor notes) — use the slides for
structure and the definitive list of examples, and mine the transcript
for extra explanations, asides, and examples the slides don't show. If
they disagree on a fact or number, go with the slides and say so.
```

## 10. Quick mode

**When to use:** you need something fast and don't need the full interactive
lecture or the full polish layer.

```text
Use make-lecture-kit in quick mode: full coverage of every concept and
every worked example, but keep it to one interaction per chapter in the
interactive lecture and skip the signature-upgrades layer — I need this
fast.
```

---

**Tip:** when a kit already exists, follow-up prompts edit the same
`output/<your-topic>/` folder and rebuild it — you never start over.
