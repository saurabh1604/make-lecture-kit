#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keyless build orchestrator for a study companion.

Turns a single companion ``.tex`` (plus its matplotlib figure scripts) into a
real PDF, with zero secrets and zero network calls at author time. The only
network touch is an *optional* ``pip install matplotlib`` if matplotlib is
missing -- and even that is best-effort and never fatal.

Usage
-----
    python3 scripts/build_pdf.py <companion.tex> [--figdir DIR] [--out OUTPATH]

What it does, in order
----------------------
  1. Ensure matplotlib is importable; if not, try a quiet pip install and
     report. If it still cannot be imported, warn that figures will not render
     but keep going (the template carries a TikZ fallback).
  2. Run every ``*.py`` figure script found in --figdir (default:
     ``<texdir>/figures``) so the PNGs land next to the .tex.
  3. Detect a TeX engine: prefer ``latexmk``; otherwise ``pdflatex`` run TWICE
     (so references / ToC settle). Compile the .tex and copy the resulting PDF
     to --out (default: ``output/<texstem>/companion.pdf``), creating dirs.
  4. Parse the ``.log`` for Overfull boxes, undefined control sequences, and
     unresolved references; print a concise QA report. The summary is informative
     but never hard-crashes the build.
  5. If NO TeX engine is found, do NOT fail silently: print clear, friendly
     install guidance, leave the .tex and PNGs in place, and exit 0.

Pure standard library + subprocess. Handles spaces in paths. Never crashes:
unexpected errors are caught, reported, and turned into a non-fatal exit.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import traceback
from typing import List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Tiny pretty-printing helpers (ANSI only when attached to a real terminal).
# ---------------------------------------------------------------------------
def _supports_colour() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM", "") not in ("", "dumb")


_COLOUR = _supports_colour()


def _wrap(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOUR else text


def info(msg: str) -> None:
    print(_wrap("36", "[build]") + " " + msg, flush=True)


def good(msg: str) -> None:
    print(_wrap("32", "[ ok ]") + " " + msg, flush=True)


def warn(msg: str) -> None:
    print(_wrap("33", "[warn]") + " " + msg, flush=True)


def err(msg: str) -> None:
    print(_wrap("31", "[err ]") + " " + msg, flush=True)


def rule(label: str = "") -> None:
    bar = "-" * 64
    print(_wrap("90", bar))
    if label:
        print(_wrap("1", label))


# ---------------------------------------------------------------------------
# Subprocess helper -- list-form args (no shell) so spaces in paths are safe.
# ---------------------------------------------------------------------------
def run(cmd: Sequence[str], cwd: Optional[str] = None,
        timeout: Optional[int] = None) -> Tuple[int, str]:
    """Run ``cmd`` (a list) and return ``(returncode, combined_output)``.

    Never raises on a non-zero exit; a missing binary or a timeout is folded
    into a sentinel return code so callers can react instead of crashing.
    """
    try:
        proc = subprocess.run(
            list(cmd),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout or ""
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired as exc:
        out = exc.output or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return 124, out + f"\n[timeout after {timeout}s: {cmd[0]}]"
    except Exception as exc:  # pragma: no cover -- defensive, never crash
        return 1, f"error running {cmd[0]}: {exc}"


# ---------------------------------------------------------------------------
# Step 1 -- make sure matplotlib is importable (best effort, never fatal).
# ---------------------------------------------------------------------------
def ensure_matplotlib() -> bool:
    """Return True if matplotlib can be imported (after an optional install)."""
    if importlib.util.find_spec("matplotlib") is not None:
        good("matplotlib is available.")
        return True

    warn("matplotlib not found -- attempting a quiet 'pip install matplotlib'.")
    code, out = run(
        [sys.executable, "-m", "pip", "install", "--quiet", "matplotlib"],
        timeout=600,
    )
    if code == 0 and importlib.util.find_spec("matplotlib") is not None:
        good("matplotlib installed.")
        return True

    warn("could not install matplotlib (offline or restricted environment).")
    if out.strip():
        # Show only the tail so we do not flood the log.
        tail = "\n".join(out.strip().splitlines()[-5:])
        print(_wrap("90", tail))
    warn("Figures will NOT render. Continuing -- the template's TikZ fallback "
         "will stand in for any missing PNGs.")
    return False


# ---------------------------------------------------------------------------
# Step 2 -- run every figure script so PNGs are written next to the .tex.
# ---------------------------------------------------------------------------
def render_figures(figdir: str, have_mpl: bool) -> None:
    """Execute every ``*.py`` in ``figdir`` so its PNG lands beside the .tex.

    Scripts run with ``figdir`` on ``sys.path`` (via PYTHONPATH) and with
    ``figdir`` as the working directory, so ``import figstyle`` resolves and a
    script that saves to ``os.path.dirname(__file__)`` writes into ``figdir``.
    """
    if not os.path.isdir(figdir):
        warn(f"figure dir not found: {figdir} -- skipping figure render.")
        return

    scripts = sorted(
        os.path.join(figdir, f)
        for f in os.listdir(figdir)
        if f.endswith(".py") and f != "figstyle.py"
    )
    if not scripts:
        info(f"no figure scripts (*.py) in {figdir} -- nothing to render.")
        return
    if not have_mpl:
        warn(f"skipping {len(scripts)} figure script(s): matplotlib unavailable.")
        return

    # Put the figdir, its parent, and the kit's own scripts/ dir on the path, so
    # `import figstyle` works at any output depth (output/<slug>/figures or
    # output/<series>/<nn>-<topic>/figures) without per-script path hacks.
    env = dict(os.environ)
    parent = os.path.dirname(os.path.abspath(figdir))
    kit_scripts = os.path.dirname(os.path.abspath(__file__))
    extra = os.pathsep.join([os.path.abspath(figdir), parent, kit_scripts])
    env["PYTHONPATH"] = (
        extra + os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else extra
    )
    env.setdefault("MPLBACKEND", "Agg")  # headless-safe even if a script forgets

    info(f"rendering {len(scripts)} figure script(s) from {figdir} ...")
    ok = 0
    for script in scripts:
        name = os.path.basename(script)
        try:
            proc = subprocess.run(
                [sys.executable, os.path.abspath(script)],
                cwd=os.path.abspath(figdir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=300,
            )
            if proc.returncode == 0:
                good(f"  {name}")
                ok += 1
            else:
                warn(f"  {name} exited {proc.returncode}")
                tail = "\n".join((proc.stdout or "").strip().splitlines()[-6:])
                if tail:
                    print(_wrap("90", "    " + tail.replace("\n", "\n    ")))
        except subprocess.TimeoutExpired:
            warn(f"  {name} timed out (300s) -- skipped.")
        except Exception as exc:  # never let one bad script kill the build
            warn(f"  {name} raised: {exc}")

    info(f"figures rendered: {ok}/{len(scripts)} succeeded.")


# ---------------------------------------------------------------------------
# Step 3 -- detect a TeX engine and compile.
# ---------------------------------------------------------------------------
def find_engine() -> Optional[Tuple[str, str]]:
    """Return ``(kind, path)`` for the best available engine, or ``None``.

    Preference order: latexmk (handles passes + cleanup), then pdflatex.
    """
    latexmk = shutil.which("latexmk")
    if latexmk:
        return ("latexmk", latexmk)
    pdflatex = shutil.which("pdflatex")
    if pdflatex:
        return ("pdflatex", pdflatex)
    return None


def compile_tex(engine: Tuple[str, str], texpath: str) -> Tuple[bool, str]:
    """Compile ``texpath`` with the chosen engine. Return ``(ok, logtext)``.

    Compilation runs inside the .tex's own directory so ``\\input`` /
    ``\\includegraphics`` relative paths resolve. ``ok`` reflects whether a PDF
    was actually produced -- LaTeX often exits non-zero on mere warnings, so we
    trust the artifact over the return code.
    """
    kind, exe = engine
    texdir = os.path.dirname(os.path.abspath(texpath)) or "."
    texfile = os.path.basename(texpath)
    stem = os.path.splitext(texfile)[0]
    expected_pdf = os.path.join(texdir, stem + ".pdf")

    # Remove a stale PDF so a later "exists?" check is meaningful.
    if os.path.exists(expected_pdf):
        try:
            os.remove(expected_pdf)
        except OSError:
            pass

    if kind == "latexmk":
        info("compiling with latexmk (-pdf, nonstopmode) ...")
        # NB: latexmk has no "-halt-on-error=false" option and aborts with
        # "Bad options specified" if given one — which silently produced no PDF.
        # nonstopmode already keeps the engine going through errors; we also tell
        # latexmk not to stop the whole run via -f (force).
        code, out = run(
            [exe, "-pdf", "-f", "-interaction=nonstopmode",
             "-file-line-error", texfile],
            cwd=texdir, timeout=600,
        )
        combined = out
    else:
        # pdflatex: two passes for refs / ToC.
        combined = ""
        for i in (1, 2):
            info(f"compiling with pdflatex (pass {i}/2, nonstopmode) ...")
            code, out = run(
                [exe, "-interaction=nonstopmode",
                 "-file-line-error", texfile],
                cwd=texdir, timeout=600,
            )
            combined += f"\n===== pdflatex pass {i} =====\n" + out

    # Prefer the on-disk .log; fall back to captured stdout.
    logpath = os.path.join(texdir, stem + ".log")
    logtext = combined
    if os.path.exists(logpath):
        try:
            with open(logpath, "r", encoding="utf-8", errors="replace") as fh:
                logtext = fh.read()
        except OSError:
            pass

    produced = os.path.exists(expected_pdf) and os.path.getsize(expected_pdf) > 0
    if produced:
        good(f"PDF produced: {expected_pdf}")
    else:
        err("no PDF was produced -- see the QA report below for the cause.")
    return produced, logtext


# ---------------------------------------------------------------------------
# Step 4 -- parse the log into a concise QA report.
# ---------------------------------------------------------------------------
def qa_report(logtext: str) -> int:
    """Scan ``logtext`` for the usual offenders and print a tidy summary.

    Returns a small integer 'issue score' (count of flagged lines) for the
    caller to surface -- it is purely informational and never aborts the build.
    """
    overfull_h = re.findall(r"^Overfull \\hbox .*$", logtext, re.MULTILINE)
    overfull_v = re.findall(r"^Overfull \\vbox .*$", logtext, re.MULTILINE)
    undefined = re.findall(
        r"^.*Undefined control sequence.*$", logtext, re.MULTILINE
    )
    ref_warn = re.findall(
        r"^LaTeX Warning: (?:Reference|Citation) .*$", logtext, re.MULTILINE
    )
    rerun = re.findall(
        r"^LaTeX Warning:.*[Rr]erun.*$", logtext, re.MULTILINE
    )
    missing_fig = re.findall(
        r"^.*(?:File `[^']+' not found|Missing.*graphics).*$",
        logtext, re.MULTILINE,
    )

    rule("QA report")

    def section(title: str, items: List[str], cap: int = 6) -> None:
        if not items:
            good(f"{title}: none")
            return
        warn(f"{title}: {len(items)}")
        for line in items[:cap]:
            print(_wrap("90", "    " + line.strip()))
        if len(items) > cap:
            print(_wrap("90", f"    ... and {len(items) - cap} more"))

    section("Overfull \\hbox (text running into the margin)", overfull_h)
    section("Overfull \\vbox (content past the page bottom)", overfull_v)
    section("Undefined control sequences", undefined)
    section("Unresolved references / citations", ref_warn)
    section("Missing graphics files", missing_fig)
    if rerun:
        warn("LaTeX asked for another run (refs/ToC may be one pass behind).")

    score = (len(overfull_h) + len(overfull_v) + len(undefined)
             + len(ref_warn) + len(missing_fig))
    rule()
    if score == 0:
        good("QA: clean -- no overfull boxes, undefined macros, or bad refs.")
    else:
        warn(f"QA: {score} item(s) flagged above. Build still completed; "
             "review if the layout looks off.")
    return score


# ---------------------------------------------------------------------------
# Step 5 -- friendly guidance when no TeX engine exists.
# ---------------------------------------------------------------------------
def no_engine_guidance(texpath: str, figdir: str) -> None:
    rule("No TeX engine found")
    err("Neither 'latexmk' nor 'pdflatex' is on PATH, so the PDF cannot be "
        "compiled here. Nothing was deleted -- your .tex and any rendered "
        "PNGs are ready to compile the moment a TeX engine is available.")
    print()
    info("Where TeX is usually already present:")
    print("    * Claude Cowork / Codex sandboxes ship a full TeX Live -- if you")
    print("      are in one, just re-run this exact command; the engine is there.")
    print()
    info("Install TeX on a bare machine, then re-run this script:")
    print()
    print(_wrap("1", "  TinyTeX (small, fast, recommended):"))
    if os.name == "nt":
        print('    # Windows (PowerShell):')
        print("    "
              "powershell -NoProfile -ExecutionPolicy Bypass "
              "-Command \"& {iwr -useb https://yihui.org/tinytex/install-bin-windows.bat "
              "-OutFile install.bat; ./install.bat}\"")
    else:
        print("    curl -sL https://yihui.org/tinytex/install-bin-unix.sh | sh")
        print("    # then make sure ~/.TinyTeX/bin/* is on your PATH, e.g.:")
        print('    tlmgr path add')
    print()
    print(_wrap("1", "  Or a full TeX Live distribution:"))
    print("    * macOS:        brew install --cask mactex-no-gui")
    print("    * Debian/Ubuntu: sudo apt-get install texlive-full latexmk")
    print("    * Fedora:        sudo dnf install texlive-scheme-full latexmk")
    print("    * Windows:       https://www.tug.org/texlive/ (or MiKTeX)")
    print()
    info("Then simply re-run:")
    print(f'    python3 "{os.path.abspath(sys.argv[0])}" "{os.path.abspath(texpath)}"')
    print()
    info(f"Leaving artifacts in place: {os.path.dirname(os.path.abspath(texpath)) or '.'}")
    if os.path.isdir(figdir):
        pngs = [f for f in os.listdir(figdir) if f.lower().endswith(".png")]
        if pngs:
            good(f"{len(pngs)} figure PNG(s) already rendered in {figdir}.")
    rule()


# ---------------------------------------------------------------------------
# Step 4b -- run the companion language + layout gate (non-fatal, informative).
# ---------------------------------------------------------------------------
def run_tex_lint(texpath: str) -> None:
    """Run scripts/lint_tex.py on the source and surface its report.

    Informative only -- like the rest of build_pdf, it never aborts the build.
    A clean companion should clear it with zero FAILs (long sentences, fancy
    words, banned hand-waving, raw 'Step'-label enumerates, wide tables).
    """
    here = os.path.dirname(os.path.abspath(__file__))
    linter = os.path.join(here, "lint_tex.py")
    if not os.path.isfile(linter):
        return
    rule("Language & layout gate (lint_tex.py)")
    code, out = run([sys.executable, linter, os.path.abspath(texpath)],
                    timeout=120)
    if out.strip():
        print(out.rstrip())
    if code == 1:
        warn("lint_tex reported FAIL(s) above -- fix them and rebuild for a "
             "clean, easy-to-read companion.")
    elif code == 0:
        good("language & layout gate: no blocking issues.")


# ---------------------------------------------------------------------------
# Orchestration.
# ---------------------------------------------------------------------------
def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="build_pdf.py",
        description="Keyless build orchestrator for a study companion.",
    )
    parser.add_argument("tex", help="path to the companion .tex file")
    parser.add_argument(
        "--figdir", default=None,
        help="folder of *.py figure scripts (default: <texdir>/figures)",
    )
    parser.add_argument(
        "--out", default=None,
        help="output PDF path (default: output/<texstem>/companion.pdf)",
    )
    args = parser.parse_args(argv)

    texpath = os.path.abspath(args.tex)
    if not os.path.isfile(texpath):
        err(f"tex file not found: {texpath}")
        return 2  # genuine bad-input error -- the one case worth a nonzero exit

    texdir = os.path.dirname(texpath) or "."
    stem = os.path.splitext(os.path.basename(texpath))[0]
    figdir = os.path.abspath(args.figdir) if args.figdir \
        else os.path.join(texdir, "figures")
    outpath = os.path.abspath(args.out) if args.out \
        else os.path.join(texdir, stem + ".pdf")

    rule(f"Building companion: {os.path.basename(texpath)}")
    info(f"tex    : {texpath}")
    info(f"figdir : {figdir}")
    info(f"out    : {outpath}")

    try:
        # Step 1
        have_mpl = ensure_matplotlib()

        # Step 2
        render_figures(figdir, have_mpl)
        # Some pipelines drop figure scripts right next to the .tex instead of
        # in a figures/ subfolder. Render those too, if the folders differ.
        if os.path.abspath(figdir) != os.path.abspath(texdir):
            sibling = [f for f in os.listdir(texdir)
                       if f.endswith(".py") and f != "figstyle.py"]
            if sibling:
                render_figures(texdir, have_mpl)

        # Step 3 / Step 5
        engine = find_engine()
        if engine is None:
            no_engine_guidance(texpath, figdir)
            return 0  # graceful: guidance given, artifacts preserved

        info(f"using TeX engine: {engine[0]} ({engine[1]})")
        produced, logtext = compile_tex(engine, texpath)

        # Step 4
        qa_report(logtext)

        # Step 4b -- language + layout gate on the .tex source.
        run_tex_lint(texpath)

        # Copy the produced PDF to the requested output location.
        produced_pdf = os.path.join(texdir, stem + ".pdf")
        if produced and os.path.exists(produced_pdf):
            if os.path.abspath(produced_pdf) == os.path.abspath(outpath):
                good(f"companion PDF -> {outpath}")
            else:
                os.makedirs(os.path.dirname(outpath) or ".", exist_ok=True)
                try:
                    shutil.copyfile(produced_pdf, outpath)
                    good(f"companion PDF -> {outpath}")
                except OSError as exc:
                    warn(f"could not copy PDF to {outpath}: {exc}")
                warn(f"the compiled PDF is still here: {produced_pdf}")
        else:
            err("build finished without a PDF. The QA report above explains "
                "why; fix the flagged issue and re-run.")
            return 0  # non-fatal by contract -- artifacts/log are left in place

        rule("Done")
        return 0

    except KeyboardInterrupt:
        err("interrupted by user.")
        return 130
    except Exception:  # absolute last line of defence: never crash ugly
        err("unexpected error -- but artifacts were left in place:")
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
