# upgrading.md — keep make-lecture-kit improving (safely)

This kit is meant to evolve. Here is a simple, repeatable loop to upgrade it without
breaking it — and it works the same on **Claude, Codex, Jules, Cursor, or any agent**,
because the only tools involved are standard Python and LaTeX.

---

## The upgrade loop

1. **Make the change** — a new figure helper, a clearer rule, a tighter linter check,
   a new callout, whatever improves the output.
2. **Run the health check:**
   ```bash
   python3 scripts/selfcheck.py
   ```
   It must end in **PASS**: every script compiles, `figstyle` renders, both linters
   run, the bundled example still passes, and all required files are present.
3. **If you changed authoring behaviour, regenerate the example** (or any lecture in
   `output/`) and eyeball the PDF + HTML.
4. **Record it:** bump `VERSION` and add a dated entry to `CHANGELOG.md`.
5. **Re-export the skill** (see SKILL.md → "Packaging & versioning").

That is the whole cycle. `selfcheck.py` is the safety net that lets you upgrade
fearlessly: if it stays green, the kit still works everywhere.

---

## Copy-paste upgrade prompts (hand these to your agent)

> Run these in a chat that has the `make-lecture-kit` folder attached/installed.

- **Find & make the next improvement**
  > "Read SKILL.md and everything in references/. Suggest the 3 highest-value
  > improvements to this kit, then implement the first one. Run
  > `scripts/selfcheck.py`, bump VERSION, and add a CHANGELOG entry."

- **Add a new plot type**
  > "Add a new `figstyle` plotter for &lt;X&gt;, matching the style of the existing
  > helpers and the concept→plot map in companion_style §5. Self-check and changelog."

- **Make the language even simpler**
  > "Add &lt;words/phrases&gt; to `references/plain_language.md` and the shared word
  > lists in `scripts/_plain_language.py`. Re-run both linters, self-check, changelog."

- **Raise the bar**
  > "Review a freshly generated companion + lecture against
  > `references/quality_rubric.md`. Implement the single highest-impact fix.
  > Self-check and changelog."

---

## Guardrails — don't regress these

- **Keyless & self-contained.** The HTML is one file; MathJax from a CDN is its only
  external dependency. No API keys, no `fetch` to private hosts, no `type="module"`.
- **Cross-platform.** Standard LaTeX + standard-library Python only. No proprietary
  tools, nothing that ties the kit to one assistant.
- **The seven non-negotiable rules** (incl. "simple things stay simple" and "lead with the whole idea in one line") and the **no-overflow contract**
  (`references/quality_rubric.md`).
- **Worked-example steps use the `steps` environment** so labels stay inside boxes.
- **Plain language** stays enforced (`plain_language.md` + the two linters).

If a change would break any of these, it is not an upgrade — rework it.

---

## Publish once, so every student can fetch the latest

The point of versioning is that **all your students pull updates themselves** — you
never re-send files. Pick whichever host you like; the kit ships an updater
(`scripts/update.py`) that works with both.

**Option A — a git repo (simplest for updates).**
1. Put the `make-lecture-kit/` folder in a public git repo (e.g. GitHub).
2. Students **clone it once** into their skills location, then run
   `python3 scripts/update.py` (it runs `git pull`) — or `git pull` directly.
3. You upgrade by committing + pushing. Done.

**Option B — a published zip (no git needed by students).**
1. Host two files at one stable base URL: `VERSION` and `make-lecture-kit.zip`
   (GitHub Releases / GitHub Pages / S3 / your course site — any static host).
2. Set that base URL in **`update_source.txt`** *before* you zip and publish, so the
   URL travels inside the kit.
3. Students run `python3 scripts/update.py`: it compares `VERSION`, and if yours is
   newer, downloads and installs the new zip (their `output/` is never touched).

`update.py` understands a GitHub repo URL directly (it reads `VERSION` over *raw*
and downloads the branch's auto-generated zip), so **you never build or host a zip** —
you just push. `update_source.txt` already points at
`https://github.com/saurabh1604/make-lecture-kit` (rename there if you use a different
repo name).

**First time only** (run on your own machine, where your GitHub login lives):
```bash
cd make-lecture-kit
git init -b main && git add -A && git commit -m "release v$(cat VERSION)"
git remote add origin https://github.com/saurabh1604/make-lecture-kit.git
# create the empty repo on github.com first (or: gh repo create saurabh1604/make-lecture-kit --public)
git push -u origin main
```

**Every upgrade after that:**
```bash
# 1) make the change   2) bump VERSION   3) add a CHANGELOG entry
./publish.sh           # self-checks, commits "release vX.Y.Z", and pushes
```

Tell students once: *"to get the latest, run `python3 scripts/update.py`"* (or
`git pull` if they cloned). They can preview with `python3 scripts/update.py --check`.

## Optional: a regular cadence

If your assistant supports scheduling (e.g. Claude Cowork), set a monthly task:

> "Review make-lecture-kit against `references/quality_rubric.md` and propose one
> improvement. Implement it, run `scripts/selfcheck.py`, bump VERSION, and add a
> CHANGELOG entry."

On Codex / Jules (no scheduler), just run that same prompt at the start of any session
where you touch the kit. Either way, the kit keeps getting a little better over time —
and `selfcheck.py` keeps it honest.
