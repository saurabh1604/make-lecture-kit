# Cheat-sheet — read this first, every run

The fast-start reference. Read this in full; it tells you which parts of the big
reference files (`companion_style.md`, `lecture_style.md`, `intuition_playbook.md`)
you actually need for *this* lecture, so you don't read them cover to cover.

## The seven rules, one line each

1. **Easy language.** Plain words, ≤22-word sentences, define every term on first
   use. → `plain_language.md`.
2. **Simple things stay simple.** Right-size the explanation to the idea; lead
   with the most intuitive way in. → `plain_language.md` §8.
3. **One analogy, one story-world.** A single everyday world for the whole
   lecture, with 5–10 recurring nicknames. → `plain_language.md` §9,
   `intuition_playbook.md` §A.
4. **Math intuition, step by step.** Every symbol named, nothing skipped.
5. **Fully solved examples.** Every slide/transcript example worked in full,
   real numbers, never "it can be shown that."
6. **Interaction uncovers intuition.** Every control reveals something; a
   procedure gets the goal game (`lecture_style.md` §6 Recipe J).
7. **Lead with the whole idea, open by doing.** One-liner first, headline
   titles, never agenda-first.

Plus the no-clutter/no-overflow contract: nothing overlaps or runs off the page.

## Concept → figure/recipe lookup

Use this table to jump straight to what you need instead of reading the full
guides. "PDF helper" is a `scripts/figstyle.py` function (`companion_style.md`
§5 has the full concept→plot map); "HTML recipe" is a letter in
`lecture_style.md` §6 (grep `^### Recipe` in that file to jump to it).

| The concept is… | PDF helper | HTML recipe |
|---|---|---|
| a 1-D function / derivative / Taylor approx | `function_plot(..., tangent_at=)` | A |
| a loss landscape / 2-var function (2-D view) | `contour(...)` | A/E |
| shape near a min/max/saddle, or 3-D descent | `surface3d(..., path=)` | H (rotatable 3-D) |
| gradient descent / optimization dynamics | `gradient_descent(..., noise=)` | A (animated point) |
| a discrete probability distribution | `pmf_bar(...)` | D |
| a Gaussian / area = probability | `shaded_normal(...)` | D |
| embeddings / vectors / dot product | `vectors2d(...)` | B |
| a matrix / transition / attention table | `heatmap(...)` | E (shaded overlay) |
| a pipeline / algorithm / agent loop | `flow([...])` | C (staged/animated nodes) |
| a small network of nodes lighting up (forward/backward pass) | — | C |
| a sentence / tagged sequence (NLP), a truth table, clickable tokens | `annotated_sequence(...)` | F (DOM, non-canvas) |
| comparing several methods/quantities | `bars(...)` | D |
| the lecture's overview / how bands connect | — | G (clickable journey map) |
| a step-by-step procedure to practice | — | J (goal game) |
| a correct-but-static plot that should explain itself (labels, auto-play) | — | I (annotate & animate an existing lab) |
| a static or step-through calculation | — | §5 Way A/B (no recipe letter — worked example) |

## How to fetch more detail on demand

Do **not** `Read` `companion_style.md` or `lecture_style.md` whole. The mandatory
core of each is a short, named list of sections — not "most of the file":

- `companion_style.md`: **§0, §1, §2, §4, §6** only (~240 of its ~545 lines — under half).
- `lecture_style.md`: **§0, §1, §2, §4, §5, §10.1** only (~275 of its ~930 lines — under a third).

Everything else is fetch-on-demand:

1. For the 2–4 recipe letters or plot types this lecture's concepts actually
   need, jump straight to them: `grep -n '^### Recipe' references/lecture_style.md`
   lists every recipe with its line number; open just those sections (e.g. with
   the Read tool's `offset`/`limit`, or `sed -n 'START,ENDp' file`).
2. For a specific figure's plot API, or the closing arc, or the chrome/script
   internals (already correct in the template you copy — you only need these if
   you're modifying chrome, not building a fresh lecture): `grep -n '^## \|^### '
   <file>` to list every section with its line number, then open only the one
   you're about to act on.
3. Skim `intuition_playbook.md` for the analogy pattern that fits your topic's
   story-world; you don't need every entry.

**If you're about to `Read` either big file with no offset/limit and no specific
section in mind, stop.** That's over-reading, not thoroughness — it's the exact
cost this cheat-sheet exists to avoid, and it has been observed happening in
practice, not just as a hypothetical risk.

This is a discipline, not a shortcut past quality: every rule above still
applies in full. It only changes how much of the reference text you load into
context to apply it.
