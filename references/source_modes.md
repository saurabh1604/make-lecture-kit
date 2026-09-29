# source_modes.md — any input in, one concept inventory out

The kit never needs slides. A learner may hand you **a single topic**, **a list of
topics**, **notes or study material**, **PDFs**, **slide decks**, or any mix. This
guide turns every one of those into the same thing: a **concept inventory** — the one
plan that the companion PDF and the interactive lecture are both built from.

Do this step fully before writing any prose. Everything later reads from the inventory.

---

## 1. Name the input mode

| Mode | What the user gave you | Your job |
|---|---|---|
| **A. One topic** | "eigenvectors", "how vaccines work", "the French Revolution" | Design the whole teaching plan yourself (§3). |
| **B. A list of topics** | a syllabus, a unit list, "topics 3–7 of my course" | Plan a series: one kit per topic, or one combined kit (§4). |
| **C. Notes / study material** | pasted text, a web page, handwritten-note photos, a Word file | Extract, then fill the gaps (§5). |
| **D. Documents** | PDF (book chapter, paper, handout), PPT/PPTX deck, DOCX | Read every page, extract, then fill the gaps (§5). |
| **E. A mix** | "these topics, and here are my notes / slides" | Documents are the main source; the topic list sets the scope (§6). |

Read documents with whatever the platform gives you: a PDF skill or `pdftotext`, a
PPTX skill or `python-pptx`, a DOCX skill or `pandoc`. Look at images and scanned
pages directly. If a file cannot be read, say so and ask for another format — never
guess at its contents.

## 2. Fix the audience and depth

Default audience: **a smart person meeting this topic for the first time.** No
prior knowledge is assumed beyond what the inventory lists as prerequisites.

If the user states a level (school student, first-year undergraduate, working
professional, exam in a week, interview prep), adapt the depth, the examples and the
"where it's used" links to it. Ask **one** short question only when the answer would
change the plan a lot (for example, "a 1-hour intro or a full unit?"). Otherwise pick
the sensible default, state it in one line, and carry on.

---

## 3. Mode A — only a topic: build the syllabus yourself

With no source, the teaching plan is yours to design. Keep it honest and simple.

1. **The one question.** Write the single question this topic answers, in plain
   words ("How do we find the directions a matrix only stretches, never turns?").
   It becomes the spine of the opening "do it first" section.
2. **Scope.** Decide what is in and what is out. A topic kit is usually
   **6–15 concepts**. Park advanced side-roads in a short "where to go next" note.
3. **Prerequisites.** List what the reader must already know. If a prerequisite is
   likely shaky for the audience, add a short warm-up section ("What you need first")
   — simple, with one example, never a lecture of its own.
4. **The concept ladder.** Order the concepts simple → hard, so idea *N* leans only
   on ideas before it. For each, note the question it answers and mark it **easy** or
   **hard** (easy ideas get short treatment — `plain_language.md` §8).
5. **Check the facts.** If you have web search, use it to confirm definitions,
   formulas, standard notation, dates and names. Where textbooks use different
   conventions, pick one and say so in a `watchout` box. Never invent statistics,
   quotes or citations.
6. **Design the examples.** There are no source examples, so every one is yours:
   - at least **one worked example per concept**, **two or more** for hard ones;
   - **clean, simple numbers** that make the idea visible, not heavy setup;
   - one **running example** that threads through several concepts, so the reader
     meets familiar numbers again as the ideas stack up;
   - a mix of **real-life** examples (a shop, a phone battery, a cricket score) and
     **exam-style** ones (a definite number to compute).
   Compute every number with code before you write it down.
7. **Misconceptions.** List the 3–6 mistakes beginners really make. Each becomes a
   `watchout` box in the right section.

## 4. Mode B — a list of topics

1. **Order them** by prerequisites, not by the order they were typed.
2. **One kit per topic, or one combined kit?**
   - **One kit per topic** (the default) when topics are independent, or when all
     of them together would be more than ~20 concepts. Output goes to
     `output/<series>/<nn>-<topic>/` (`01-vectors`, `02-matrices`, …), each folder
     with its own `companion.pdf` + `lecture.html`.
   - **One combined kit** when the topics are short, tightly linked steps of one
     story (e.g. "mean, median, mode"). One folder, one section band per topic.
   Tell the user which you chose in one line.
3. **Keep a series consistent:** one `SERIES_NAME`, one story-world, one nickname
   lexicon, the same running example where it fits. A later kit may say "remember
   the shop from kit 1" — that is a feature.
4. Plan each topic with §3 (or §5 if material is attached for it).

## 5. Modes C and D — notes, study material, PDFs, decks

1. **Read everything.** Every page, slide, note, speaker note, figure caption and
   footnote. Skim-reading is how examples get dropped.
2. **Extract into the inventory** (§7): every concept, every definition, every
   formula and symbol, and **every example in the material**. Each source example is
   a **promise**: it gets a full worked example, every step, real numbers.
3. **The material is the floor, not the ceiling.** Source material is usually terse.
   Fill what it leaves out:
   - the missing **steps** in any derivation or calculation;
   - the missing **intuition** and everyday picture;
   - a **prerequisite** it quietly assumes;
   - a worked example for any concept that has none (design it as in §3 step 6).
4. **Keep the material's notation** so the reader can move between it and the kit.
   If the notation is confusing, keep it anyway and decode it once.
5. **Re-explain, don't copy.** Never paste the source's sentences or figures. Say it
   more simply, and redraw every figure with `figstyle` / canvas.
6. **Fix errors gently.** If the material has a mistake, use the correct version and
   add a short `watchout` noting the difference.
7. **Big sources.** A whole book or a 100-page PDF is too much for one kit. Split
   by chapter or by natural unit, treat it as Mode B, and tell the user the plan.

## 6. Mode E — a mix

The documents are the main source (§5). The topic list decides the scope: cover the
listed topics, use the material for each, and design from scratch (§3) for any topic
the material does not cover. Say which topics came from where in the inventory.

---

## 7. The concept inventory (write it down before any prose)

One table, plus four short lists. Keep it in your working notes (not in `output/`).

| # | Concept (headline) | Question it answers | Easy / hard | Needs | Best way in (everyday picture) | Examples (✦ from source, ✧ designed) | Figure / lab idea |
|---|---|---|---|---|---|---|---|
| 1 | You already know how to … | … | easy | — | … | ✧ running example, part 1 | slider: … |
| 2 | … | … | hard | 1 | … | ✦ source ex. 2, ✧ one more | 3-D surface: … |

Then:

- **Story-world + lexicon** — one everyday world for the whole kit and 5–10 plain
  nicknames for recurring objects (`plain_language.md` §9).
- **Symbols** — every symbol, in order of first use, with its plain name.
- **Misconceptions** — the traps, each tied to a concept row.
- **Where it's used** — for each concept, one concrete place the idea matters, in the
  field the topic belongs to (ML/AI for an ML topic, medicine for a biology topic,
  money for a finance topic, daily life for a general topic).

**Coverage rule:** every concept gets a section/chapter; every ✦ source example is
worked in full; every concept has at least one worked example (✦ or ✧). Count them
before you start, and tick them off before you ship.

**Accuracy rule:** when you design the content, correctness is on you. Compute every
number with code. Check every formula and fact against a trustworthy reference when
you can. If you are unsure of a fact, leave it out or say plainly that it is uncertain.
