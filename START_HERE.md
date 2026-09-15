# Start here

## What this is

Your teacher made this kit for you. Give it any lecture — slides, notes, or
just a topic — and your AI assistant turns it into a beautiful study PDF
(`companion.pdf`) and a complete interactive lecture page (`lecture.html`).
No accounts, no API keys, nothing to configure.

## Set it up in 1 minute

Pick the assistant you use and copy-paste:

**Claude Code**
```bash
git clone https://github.com/saurabh1604/make-lecture-kit ~/.claude/skills/make-lecture-kit
```

**OpenAI Codex**
```bash
git clone https://github.com/saurabh1604/make-lecture-kit ~/.agents/skills/make-lecture-kit
```

**Google Jules**
Connect the `saurabh1604/make-lecture-kit` repo in Jules and ask away — it reads
the repo's `AGENTS.md` automatically. (Or drop the folder into your own repo.)

**Claude Cowork**
Add the `make-lecture-kit` folder as a skill (Settings → Capabilities, "add
skill") — or simply drag the folder into your chat.

**Cursor or another agent?**
Clone it, or drop the folder into your project; the root `AGENTS.md` and
`SKILL.md` tell the agent what to do.

**Don't want to install anything?**
Just drop the whole `make-lecture-kit` folder into a chat with Claude, Codex,
Jules, or any agent and ask away.

> No git? Download the ZIP from
> [the repo page](https://github.com/saurabh1604/make-lecture-kit) and unzip it
> where the command above would have cloned it.

## Use it

Attach your lecture material if you have it — slides (PDF or PPTX), a session
transcript, or notes; you can attach more than one at once — results are much
better — then say something like:

- "Use make-lecture-kit on the attached lecture slides."
- "Make a study PDF and a complete interactive lecture for eigenvectors."
- "Explain backpropagation simply, with fully worked examples and an
  interactive lecture."

More ready-made prompts: `references/prompts.md`.

## What you get

Everything lands in a new folder, `output/<your-topic>/`:

- **`lecture.html`** — double-click it; it opens in your browser. Move the
  sliders, step through the math, toggle things on and off. That's the point.
- **`companion.pdf`** — your study document: plain English, analogies before
  the math, every example worked out in full. Print it, scribble on it.

If the PDF didn't compile on your machine (no LaTeX installed), the assistant
will say so plainly and tell you exactly what to do next — your
`companion.tex` source and figures are still there, ready to compile.

## Stay updated

Your teacher ships improvements over time. Getting the latest takes one command,
and your own work in `output/` is kept:

```bash
cd ~/.claude/skills/make-lecture-kit     # or wherever you cloned it
git pull                                  # or:  python3 scripts/update.py
```

On **Google Jules** there's nothing to do — it always runs the latest from the
repo. To just peek at what's new: `python3 scripts/update.py --check`.

## If something goes wrong

- Ask: "Run `scripts/lint.py` on my lecture.html and show me what it says."
- Ask: "lint reported FAILs — fix every FAIL and re-run until it passes."
- Weak or generic result? Re-ask with the actual lecture file attached.

Happy studying.
