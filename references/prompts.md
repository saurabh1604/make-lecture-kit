# Prompt cookbook — copy, paste, learn

Ready-made prompts for **make-lecture-kit**. Copy one into your chat (Claude Code,
Claude Cowork, OpenAI Codex, Jules, Cursor…), swap in your topic, and go. You do
**not** need slides: a topic name is enough. If you do have notes, a PDF, a book
chapter or a deck, attach it — the kit will cover all of it and fill the gaps.

---

## 1. Just a topic

**When to use:** you want to understand something and have no material.

```text
Use make-lecture-kit on the topic: <eigenvectors>. I'm meeting it for the
first time. Build the companion PDF and the interactive lecture. Start with
an everyday picture, use real-life examples, and walk me through each
worked example step by step.
```

## 1b. A list of topics

**When to use:** a syllabus, a unit, or a few related topics.

```text
Use make-lecture-kit on these topics: <vectors, matrices, determinants,
eigenvectors>. Order them so each builds on the last, and make one kit per
topic in a series with the same story-world and running example.
```

## 1c. Your own material (notes, PDF, book chapter, slides)

**When to use:** you have study material and want it explained simply.

```text
Use make-lecture-kit on the attached <notes / PDF / slides>. Cover every
idea and every example in it, fill in the steps and intuition it skips,
and add worked examples for anything that has none. Keep the language
simple — this is my first time seeing this topic.
```

## 1d. Set the level

```text
Use make-lecture-kit on <photosynthesis> for <a Class 10 student /
a first-year undergrad / a working professional with 30 minutes>.
```

## 2. Companion PDF only

**When to use:** you just want the printable study document, not the web page.

```text
Use make-lecture-kit, but only the companion part: turn <my topic /
the attached material> into companion.pdf — plain English, an everyday
analogy before each piece of math, and every example fully worked with
real numbers. Skip the interactive lecture for now.
```

## 3. Interactive lecture only

**When to use:** you want the play-with-it web page, not the PDF.

```text
Use make-lecture-kit, but only the interactive lecture part: build
<my topic / the attached material> as lecture.html — the whole topic as
a story, with an interactive lab (sliders, steps, toggles) for every key idea. Run the
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
Use make-lecture-kit on <my topic / the attached material>, but make it
an exam-prep edition: focus on what's examinable, flag the formulas and results I
must know cold, keep all the fully worked examples, and add practice
questions with complete solutions at the end of the companion.
```

## 8. Fix-it: lint reported FAILs

**When to use:** `scripts/lint.py` flagged problems in your lecture.html.

```text
lint.py reported FAILs on my make-lecture-kit lecture page. Fix every
FAIL — overflow, readability, math, interactivity, whatever it flags —
and re-run python3 scripts/lint.py output/<my-topic>/lecture.html until
it passes. Show me the final lint output.
```

---

**Tip:** when a kit already exists, follow-up prompts edit the same
`output/<your-topic>/` folder and rebuild it — you never start over.
