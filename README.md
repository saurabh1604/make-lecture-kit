# make-lecture-kit — turn any lecture into an easy, visual, interactive study kit

Give it a lecture (slides, notes, or just a topic) and your AI assistant
produces two things into an `output/` folder:

- **`companion.pdf`** — a real, professionally typeset study companion in plain,
  easy English, with analogies and fully-worked examples (built with LaTeX +
  figures, the way the originals were made).
- **`lecture.html`** — a complete, very detailed, very interactive lecture: the
  whole lecture rebuilt as a story-driven page where you *play* with every idea
  and watch the intuition appear.

**No API keys. You install nothing.** Your own agent session writes the source,
makes the figures, and compiles the PDF for you. It works first-class on **all
three major assistants — Claude, OpenAI Codex, and Google Jules** (plus Cursor,
Gemini CLI, and the like) because it ships both open skill formats: a plain
**`SKILL.md`** (Claude and Codex auto-discover it) and an **`AGENTS.md`** at the
repo root (Jules, Codex, Cursor, Gemini CLI, and the wider
[agents.md](https://agents.md) ecosystem read it natively). Nothing is
platform-specific — standard LaTeX plus standard-library Python — and the
companion PDF compiles wherever TeX is available (most agent sandboxes have it
built in).

---

## Install (pick your assistant)

Everything lives in one repo: **https://github.com/saurabh1604/make-lecture-kit**.
Cloning is best — it makes staying current a single command (see the next
section). Prefer not to use git? Download the ZIP from that page and unzip it
wherever the steps below say to clone.

### Claude Code
```bash
git clone https://github.com/saurabh1604/make-lecture-kit ~/.claude/skills/make-lecture-kit
```
Claude Code auto-discovers any skill in `~/.claude/skills/`. (For one project
only, clone into `<your-project>/.claude/skills/` instead.) Then ask:
*"Use make-lecture-kit on this lecture PDF."*

### OpenAI Codex
```bash
git clone https://github.com/saurabh1604/make-lecture-kit ~/.agents/skills/make-lecture-kit
```
Codex auto-discovers `SKILL.md` skills in `~/.agents/skills/` (and in
`.agents/skills/` inside a repo). List them with `/skills`, invoke explicitly
with `$make-lecture-kit`, or just say: *"Use the make-lecture-kit skill on the
attached lecture."* (No-git option: in Codex run `$skill-installer` and point it
at the repo.)

### Google Jules
Jules runs on a GitHub repo and reads **`AGENTS.md`** at the repo root
automatically. Two ways to use it:

- **Fastest:** in Jules, connect the `saurabh1604/make-lecture-kit` repo, then
  ask *"Use make-lecture-kit to turn this lecture into a companion PDF and an
  interactive lecture."* Jules reads `AGENTS.md` → `SKILL.md` and follows it.
- **In your own repo:** drop the `make-lecture-kit/` folder into your project
  (or copy its `AGENTS.md` to your repo root) and point Jules at that repo.

### Claude Cowork
Add the `make-lecture-kit` folder as a skill via **Settings → Capabilities**
(the "add skill" flow), or save it from the shared `.skill` file. Then just ask
for a lecture kit in chat.

### Cursor / Gemini CLI / any other agent
The kit is platform-neutral. Clone it or drop the folder into your project; the
root `AGENTS.md` (and `SKILL.md`) tell the agent exactly what to do. Then ask:
*"use make-lecture-kit on the attached lecture."*

### Or don't install at all
Drop the `make-lecture-kit` folder into a chat with any agent and say: *"Use this
skill to turn my lecture into a companion PDF and an interactive lecture."*

---

## Staying updated

Your instructor improves the kit over time (every change bumps `VERSION` and adds
a `CHANGELOG.md` line). Pulling the latest takes one command — and **your own
work in `output/` is never touched.**

- **Cloned it** (Claude Code, Codex, Cursor): pull in the folder you cloned into —
  ```bash
  cd ~/.claude/skills/make-lecture-kit      # or ~/.agents/skills/make-lecture-kit
  git pull                                   # or:  python3 scripts/update.py
  ```
  `python3 scripts/update.py --check` previews what's new without changing
  anything.
- **Downloaded the ZIP:** run `python3 scripts/update.py` — it reads the latest
  `VERSION` straight from GitHub and installs the new kit over your copy
  (keeping `output/`).
- **Google Jules:** nothing to do — Jules re-clones the repo for every task, so it
  always runs the newest version. (If you forked the repo, click **Sync fork** on
  GitHub now and then.)
- **Claude Cowork:** re-add the newer folder/`.skill`, or use the Claude Code
  clone above to get the one-command updater.

---

## Use

Attach your lecture file (PDF/PPTX) if you have one — results are much better —
then tell your assistant any of these (more in `references/prompts.md`):

- "Use make-lecture-kit on this lecture PDF."
- "Make a study PDF and a complete interactive lecture for **eigenvectors**."
- "Explain **backpropagation** simply, with worked examples and an interactive lecture."

You'll get a new folder `output/<topic>/` containing `companion.pdf` (the typeset
study companion) and `lecture.html` (the complete interactive lecture), alongside
the `companion.tex` source and the `figures/` used to build it.

Behind the scenes, your assistant reads `SKILL.md` and follows its workflow
(read the style references, expand every slide, work every example in full,
build the page and the PDF, then run the quality gates). You don't do any of
that — just give it a lecture.

> **About the PDF:** it compiles instantly in Claude Cowork and Codex sandboxes
> (TeX Live is built in). On a bare machine without TeX, the assistant will say
> so plainly, leave the ready-to-compile `companion.tex` + figures, and tell you
> the one-line TinyTeX install to finish the job.

---

## What's inside

```
make-lecture-kit/
├─ START_HERE.md                read this first (1-minute setup)
├─ README.md                    this file
├─ SKILL.md                     the instructions your AI follows (Claude, Codex)
├─ AGENTS.md                    same kit, read natively by Jules / Codex / Cursor
├─ VERSION                      current version (the updater compares this)
├─ CHANGELOG.md                 what changed in each version
├─ update_source.txt            where scripts/update.py pulls updates from
├─ templates/
│  ├─ companion.tex             LaTeX study-companion template (→ PDF)
│  └─ lecture.html              complete interactive lecture template
├─ references/
│  ├─ plain_language.md         the easy-English rulebook (both linters enforce it)
│  ├─ quality_rubric.md         the quality bar + ship checklist (both)
│  ├─ companion_style.md        how to expand slides into the companion
│  ├─ lecture_style.md          how to build the complete interactive lecture
│  ├─ intuition_playbook.md     analogies, mental models, ML/AI links
│  ├─ prompts.md                copy-paste prompts for students
│  └─ upgrading.md              the improve-the-kit loop (for instructors)
├─ scripts/
│  ├─ figstyle.py               matplotlib house style + reusable plotters
│  ├─ build_pdf.py              run figures + compile companion.tex → PDF
│  ├─ _plain_language.py        shared word lists used by both linters
│  ├─ lint.py                   lecture HTML quality gate (readability, no-overflow, keyless)
│  ├─ lint_tex.py               companion PDF-source language + layout gate
│  ├─ selfcheck.py              verify the whole kit is healthy
│  └─ update.py                 pull the latest kit (keeps your output/)
├─ examples/
│  ├─ sample_companion.tex      a finished example to show the quality bar
│  └─ figures/
│     └─ example_normal_curve.py  copy-adaptable house-style figure script
└─ output/                      your generated kits land here (the skill
                                creates one subfolder per lecture — don't
                                edit this folder by hand)
```

The companion uses LaTeX + matplotlib (already present in Cowork/Codex
sandboxes); the helper scripts are standard-library Python. Nothing phones home,
nothing needs an API key.

---

## The promise

Built around five rules: **easy words**, **relatable analogies**,
**step-by-step math intuition**, **generous fully-solved examples**, and
**interactions that uncover the intuition** — with a hard no-clutter,
no-overflow guarantee so text never runs off the page or screen.
