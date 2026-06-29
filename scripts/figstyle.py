#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""House matplotlib style for ISM Companion figures.

This module is the single source of truth for what the companion's figures
look like. Per-lecture figure scripts (the little ``*.py`` files that live in
a lecture's ``figures/`` folder) import it and call the helpers below, so every
plot across every session shares one muted, slide-friendly look.

Pure matplotlib + numpy + stdlib. No other third-party dependencies.

----------------------------------------------------------------------
How a per-lecture figure script uses this (the host agent writes these)
----------------------------------------------------------------------

    # figures/fig_bernoulli.py  -- run from anywhere; saves next to the .tex
    import os
    from figstyle import use_house_style, pmf_bar, PALETTE

    use_house_style()                      # set the global look once
    here = os.path.dirname(os.path.abspath(__file__))
    out  = os.path.join(here, "fig_bernoulli.png")

    pmf_bar(
        xs=[0, 1],
        ps=[0.4, 0.6],
        title="Bernoulli(p=0.6): one shot, two outcomes",
        xlabel="outcome", ylabel="probability",
        out=out,                           # <-- writing the PNG is what matters
    )

The build orchestrator (``build_pdf.py``) discovers and runs every ``*.py`` in
the figures folder, so each script only needs to *save* its PNG. The functions
also RETURN the Matplotlib figure, which is handy for interactive tinkering.

Design notes (kept deliberately close to the gold-standard PDF):
  * muted palette that matches the five callout-box colours in the .tex
  * thin, de-emphasised top/right spines; soft horizontal grid only
  * a short BOLD title baked into the plot itself (the slides have these)
  * sizes tuned for full-textwidth A4 (~ 7.0 x 3.2 inches) at dpi 150
  * tight_layout so nothing is clipped when \includegraphics scales it
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple

import matplotlib

# Use a non-interactive backend so this works headless (sandboxes, CI, servers).
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (must come after backend choice)
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402


# ---------------------------------------------------------------------------
# (b) Palette -- one muted colour per callout-box family in the companion.
#     Frame colours mirror the .tex taxonomy so figures and boxes feel unified.
# ---------------------------------------------------------------------------
PALETTE: Dict[str, str] = {
    # the five teaching colours (match the tcolorbox pill tabs)
    "blue":   "#2C5AA0",  # The intuition
    "green":  "#2E7D52",  # Worked example
    "amber":  "#C8881E",  # Everyday picture  (a touch deeper than #8A5A1E for lines)
    "red":    "#B23A48",  # Watch out
    "purple": "#6A4C93",  # Key takeaway
    # supporting tones
    "ink":    "#21355E",  # the navy banner / heading colour -> use for titles
    "muted":  "#5B6470",  # secondary text, secondary lines
    "grid":   "#D9DEE8",  # soft grid lines
    "fill":   "#EAF0F7",  # very light wash for shaded regions / soft bars
}

# A stable, muted cycle for multi-series ``curve`` plots.
_CYCLE: Tuple[str, ...] = (
    PALETTE["blue"], PALETTE["green"], PALETTE["amber"],
    PALETTE["red"], PALETTE["purple"], PALETTE["muted"],
)

# A house colormap for contours / surfaces / heatmaps: cool navy lows ->
# warm amber highs, so a landscape reads at a glance (matches the palette and
# the look of the reference practice-set plots).
HOUSE_CMAP = LinearSegmentedColormap.from_list(
    "house", ["#21355E", "#2C5AA0", "#3E8E9C", "#9FBF8F", "#C8881E"])


# ---------------------------------------------------------------------------
# (a) The house style.
# ---------------------------------------------------------------------------
def use_house_style() -> None:
    """Set global matplotlib rcParams to match the gold-standard figures.

    Idempotent: call it once at the top of every figure script (calling it
    again is harmless). It tweaks only rcParams, so it never opens a window.
    """
    plt.rcParams.update({
        # --- canvas / output ---
        "figure.figsize": (7.0, 3.2),   # full A4 textwidth, slide-friendly aspect
        "figure.dpi": 220,              # high-res: crisp text + lines in the PDF
        "savefig.dpi": 220,
        "savefig.bbox": "tight",        # belt-and-braces against clipped labels
        "savefig.pad_inches": 0.05,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.facecolor": "white",
        "path.simplify": True,
        "agg.path.chunksize": 10000,

        # --- typography (readable, neutral sans; degrades gracefully) ---
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
        "font.size": 10.5,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlepad": 9.0,
        "axes.labelsize": 10.5,
        "axes.labelcolor": PALETTE["ink"],
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,

        # --- spines: keep left+bottom, drop top+right, soften colour ---
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": PALETTE["muted"],
        "axes.linewidth": 0.8,
        "axes.titlecolor": PALETTE["ink"],

        # --- ticks: short, quiet ---
        "xtick.color": PALETTE["muted"],
        "ytick.color": PALETTE["muted"],
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,

        # --- grid: faint horizontal guide lines only ---
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.8,
        "grid.alpha": 0.9,

        # --- legend: clean, frameless-ish ---
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "legend.borderaxespad": 0.4,

        # --- lines ---
        "lines.linewidth": 2.4,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "lines.antialiased": True,
        "patch.antialiased": True,
        # --- figure title (suptitle) weight, if used ---
        "figure.titlesize": 13,
        "figure.titleweight": "bold",
    })


def _new_axes(figsize: Optional[Tuple[float, float]] = None):
    """Create a fig/ax pair under the house style and return ``(fig, ax)``."""
    use_house_style()
    fig, ax = plt.subplots(figsize=figsize or plt.rcParams["figure.figsize"])
    return fig, ax


def _finish(fig, ax, title: str, out: Optional[str]):
    """Apply the shared title + layout, optionally save, and return ``fig``."""
    if title:
        ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    # de-emphasise the kept spines a touch more
    for side in ("left", "bottom"):
        if side in ax.spines:
            ax.spines[side].set_color(PALETTE["muted"])
    fig.tight_layout()
    if out:
        fig.savefig(out)
        # free memory when batch-rendering many figures in one process
        plt.close(fig)
    return fig


# ---------------------------------------------------------------------------
# (c) Reusable plotters.
#     Each returns the figure and, when given ``out``, saves a PNG to it.
# ---------------------------------------------------------------------------
def pmf_bar(
    xs: Sequence,
    ps: Sequence[float],
    title: str,
    *,
    xlabel: str = "outcome",
    ylabel: str = "probability",
    color: str = PALETTE["blue"],
    annotate: bool = True,
    out: Optional[str] = None,
):
    """Bar chart of a probability mass function (discrete distribution).

    Parameters
    ----------
    xs        : the outcomes / support (any labels; cast to str on the axis).
    ps        : matching probabilities (same length as ``xs``).
    title     : short bold title baked into the plot.
    xlabel/ylabel : axis labels.
    color     : bar colour (defaults to the 'blue' teaching tone).
    annotate  : write each probability above its bar.
    out       : if given, save a PNG there.

    Example
    -------
    >>> pmf_bar([0, 1], [0.4, 0.6], "Bernoulli(p=0.6): one shot, two outcomes")
    """
    xs = list(xs)
    ps = [float(p) for p in ps]
    if len(xs) != len(ps):
        raise ValueError("pmf_bar: xs and ps must have the same length")

    fig, ax = _new_axes()
    positions = np.arange(len(xs))
    bars = ax.bar(positions, ps, width=0.6, color=color,
                  edgecolor="white", linewidth=0.8, zorder=3)

    ax.set_xticks(positions)
    ax.set_xticklabels([str(x) for x in xs])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    top = max(ps) if ps else 1.0
    ax.set_ylim(0, top * 1.18 if top > 0 else 1.0)

    if annotate:
        for rect, p in zip(bars, ps):
            ax.annotate(
                f"{p:.2f}",
                xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom",
                fontsize=9.5, color=PALETTE["ink"], fontweight="bold",
            )

    return _finish(fig, ax, title, out)


def curve(
    x: Sequence[float],
    ys_dict: Mapping[str, Sequence[float]],
    title: str,
    *,
    xlabel: str = "x",
    ylabel: str = "y",
    colors: Optional[Mapping[str, str]] = None,
    fill_below: Optional[str] = None,
    out: Optional[str] = None,
):
    """Line plot of one or more curves sharing an x-axis.

    Parameters
    ----------
    x         : shared x-values.
    ys_dict   : ``{label: y_values}`` -- one line per entry, auto-legended
                (the legend is hidden when there is only one unlabeled line).
    title     : short bold title.
    xlabel/ylabel : axis labels.
    colors    : optional ``{label: colour}`` overrides; otherwise a muted cycle.
    fill_below: if set to one of the labels, lightly shade under that curve.
    out       : if given, save a PNG there.

    Example
    -------
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 200)
    >>> curve(x, {"lambda=1": np.exp(-x), "lambda=0.5": np.exp(-0.5*x)},
    ...       "Exponential densities for two rates", xlabel="t", ylabel="f(t)")
    """
    x = np.asarray(x, dtype=float)
    fig, ax = _new_axes()

    labels = list(ys_dict.keys())
    for i, label in enumerate(labels):
        y = np.asarray(ys_dict[label], dtype=float)
        if colors and label in colors:
            c = colors[label]
        else:
            c = _CYCLE[i % len(_CYCLE)]
        ax.plot(x, y, color=c, label=label, zorder=3)
        if fill_below is not None and label == fill_below:
            ax.fill_between(x, y, color=c, alpha=0.12, zorder=2)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Only show a legend when it carries information (multiple / named series).
    show_legend = len(labels) > 1 or (
        len(labels) == 1 and not str(labels[0]).startswith("_")
    )
    if show_legend:
        ax.legend(loc="best")

    return _finish(fig, ax, title, out)


def shaded_normal(
    mu: float,
    sigma: float,
    lo: float,
    hi: float,
    title: str,
    *,
    xlabel: str = "x",
    ylabel: str = "density",
    color: str = PALETTE["blue"],
    shade: str = PALETTE["blue"],
    label_area: bool = True,
    out: Optional[str] = None,
):
    """Normal (Gaussian) density curve with the area on ``[lo, hi]`` shaded.

    This is the classic "probability = area under the curve" picture. The
    shaded slice's probability is computed exactly with the error function and
    written onto the plot, so worked examples line up with the figure.

    Parameters
    ----------
    mu, sigma : mean and standard deviation (sigma > 0).
    lo, hi    : shade the region between these x-values (use +/- math.inf for tails).
    title     : short bold title.
    xlabel/ylabel : axis labels.
    color     : curve colour.
    shade     : fill colour for the highlighted slice.
    label_area: annotate the shaded probability P(lo < X < hi).
    out       : if given, save a PNG there.

    Example
    -------
    >>> shaded_normal(0, 1, -1, 1, "Standard normal: about 68% within 1 sigma")
    """
    if sigma <= 0:
        raise ValueError("shaded_normal: sigma must be positive")
    if lo > hi:
        lo, hi = hi, lo

    fig, ax = _new_axes()

    # Plot the full curve across +/- 4 sigma.
    left, right = mu - 4 * sigma, mu + 4 * sigma
    xs = np.linspace(left, right, 400)
    pdf = (1.0 / (sigma * math.sqrt(2 * math.pi))) * np.exp(
        -0.5 * ((xs - mu) / sigma) ** 2
    )
    ax.plot(xs, pdf, color=color, zorder=3)

    # Shade the requested slice (clip the +/-inf tails to the drawn window).
    s_lo = left if lo == -math.inf else max(lo, left)
    s_hi = right if hi == math.inf else min(hi, right)
    mask = (xs >= s_lo) & (xs <= s_hi)
    ax.fill_between(xs[mask], pdf[mask], color=shade, alpha=0.22, zorder=2)

    # Thin guide lines at the slice edges (skip infinite ones).
    for edge in (lo, hi):
        if math.isfinite(edge) and left <= edge <= right:
            ax.axvline(edge, color=PALETTE["muted"], linewidth=0.9,
                       linestyle=(0, (4, 3)), zorder=1)

    # Exact area via the standard-normal CDF (error function -> no SciPy needed).
    def _cdf(v: float) -> float:
        if v == -math.inf:
            return 0.0
        if v == math.inf:
            return 1.0
        return 0.5 * (1.0 + math.erf((v - mu) / (sigma * math.sqrt(2))))

    area = _cdf(hi) - _cdf(lo)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)

    if label_area:
        cx = np.clip((s_lo + s_hi) / 2.0, left, right)
        ax.annotate(
            f"area = {area:.3f}",
            xy=(cx, ax.get_ylim()[1] * 0.45),
            ha="center", va="center",
            fontsize=10, color=PALETTE["ink"], fontweight="bold",
        )

    return _finish(fig, ax, title, out)


# ---------------------------------------------------------------------------
# (d) Richer plotters for math / stats / ML intuition.
#     These cover the visual vocabulary of the reference practice sets:
#     curves with tangents, contour maps and 3-D surfaces with the critical
#     points marked, gradient-descent paths, matrices as heatmaps, vectors as
#     arrows, pipelines as flow diagrams, and tagged sequences. Pick the one
#     that matches the concept (see companion_style.md "When to draw a plot").
# ---------------------------------------------------------------------------
def bars(labels, values, title, *, xlabel="", ylabel="value", colors=None,
         annotate=True, fmt="{:.2f}", ymax=None, out=None):
    """Generic labelled bar chart: comparisons, weights, probabilities, counts."""
    fig, ax = _new_axes()
    vals = [float(v) for v in values]
    nb = len(vals)
    if colors is None:
        colors = [_CYCLE[i % len(_CYCLE)] for i in range(nb)]
    elif isinstance(colors, str):
        colors = [colors] * nb
    rects = ax.bar(range(nb), vals, width=0.62, color=colors,
                   edgecolor="white", linewidth=0.8, zorder=3)
    ax.set_xticks(range(nb))
    ax.set_xticklabels([str(l) for l in labels])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    top = max(vals) if vals else 1.0
    ax.set_ylim(0, ymax if ymax is not None else (top * 1.18 if top > 0 else 1.0))
    if annotate:
        for r, v in zip(rects, vals):
            ax.annotate(fmt.format(v),
                        xy=(r.get_x() + r.get_width() / 2, v),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9.5,
                        color=PALETTE["ink"], fontweight="bold")
    return _finish(fig, ax, title, out)


def function_plot(f, xlim, title, *, n=400, xlabel="x", ylabel="y", color=None,
                  tangent_at=None, marks=None, fill=False, out=None):
    """Plot y = f(x). Optionally draw the tangent at x0 and mark points.

    tangent_at : x0 -> draw the tangent (slope via central difference). Perfect
                 for derivatives and the first-order Taylor picture.
    marks      : list of (x, label) -> dot + label on the curve.
    """
    color = color or PALETTE["blue"]
    fig, ax = _new_axes()
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.array([f(x) for x in xs], dtype=float)
    ax.plot(xs, ys, color=color, zorder=3)
    if fill:
        ax.fill_between(xs, ys, color=color, alpha=0.12, zorder=2)
    if tangent_at is not None:
        x0 = float(tangent_at)
        h = (xlim[1] - xlim[0]) * 1e-4
        slope = (f(x0 + h) - f(x0 - h)) / (2 * h)
        y0 = f(x0)
        span = (xlim[1] - xlim[0]) * 0.22
        tx = np.linspace(x0 - span, x0 + span, 2)
        ax.plot(tx, y0 + slope * (tx - x0), color=PALETTE["amber"], lw=2.0,
                ls=(0, (5, 3)), zorder=4)
        ax.scatter([x0], [y0], color=PALETTE["amber"], zorder=5, s=34)
        ax.annotate(f"slope = {slope:.2f}", xy=(x0, y0), xytext=(6, 8),
                    textcoords="offset points", color=PALETTE["ink"],
                    fontweight="bold", fontsize=9.5)
    for x, label in (marks or []):
        ax.scatter([x], [f(x)], color=PALETTE["red"], zorder=5, s=30)
        ax.annotate(label, xy=(x, f(x)), xytext=(5, 6),
                    textcoords="offset points", color=PALETTE["ink"], fontsize=9.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _finish(fig, ax, title, out)


def _label_on_dark(ax, x, y, text):
    """A readable label over a coloured field: white text on an ink pill."""
    ax.annotate(text, xy=(x, y), xytext=(6, 6), textcoords="offset points",
                color="white", fontweight="bold", fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.22", fc=PALETTE["ink"],
                          ec="none", alpha=0.78))


def contour(f, xlim, ylim, title, *, n=160, levels=18, points=None,
            xlabel="x", ylabel="y", colorbar=True, out=None):
    """Filled contour (heat) map of f(x, y), with critical points marked.

    points : list of (x, y, label, marker), e.g. (0, 0, "saddle", "X").
    This is the canonical optimization picture: see the whole landscape and
    where the minima / maxima / saddle points sit (as in the reference set).
    """
    use_house_style()
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    cf = ax.contourf(X, Y, Z, levels=levels, cmap=HOUSE_CMAP)
    ax.contour(X, Y, Z, levels=levels, colors="white", linewidths=0.4, alpha=0.45)
    if colorbar:
        fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    for (px, py, label, marker) in (points or []):
        ax.scatter([px], [py], marker=marker, s=95, color="white",
                   edgecolor=PALETTE["ink"], linewidth=1.7, zorder=5)
        _label_on_dark(ax, px, py, label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(False)
    ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    fig.tight_layout()
    if out:
        fig.savefig(out)
        plt.close(fig)
    return fig


def surface3d(f, xlim, ylim, title, *, n=80, xlabel="x", ylabel="y",
              zlabel="f(x, y)", view=(30, -54), path=None, project_floor=True,
              cmap=None, out=None):
    """3-D surface of f(x, y) — shows the SHAPE: a bowl, a saddle, a ridge.

    The surface is sculpted with a faint white wireframe for depth, and (by
    default) a soft filled-contour "shadow" is projected on the floor so the
    landscape reads from above and below at once.

    path : optional list/array of (x, y) points — e.g. a gradient-descent run.
           It is lifted onto the surface and drawn as a glowing red/amber trail
           (start ring + minimum star), so the descent is visible in 3-D. This
           is the iconic "ball rolling into the bowl" picture.
    project_floor : drop a faint contour map onto the base plane under the surface.
    """
    use_house_style()
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the 3d projection)
    cmap = cmap or HOUSE_CMAP
    fig = plt.figure(figsize=(6.6, 4.6))
    ax = fig.add_subplot(111, projection="3d")
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    zmin, zmax = float(np.min(Z)), float(np.max(Z))
    zspan = (zmax - zmin) or 1.0

    ax.plot_surface(X, Y, Z, cmap=cmap, rcount=n, ccount=n, linewidth=0,
                    antialiased=True, alpha=0.92, zorder=2)
    # faint mesh for sculpted depth
    ax.plot_wireframe(X, Y, Z, rcount=16, ccount=16, color="white",
                      linewidth=0.35, alpha=0.22, zorder=3)

    base = zmin - 0.28 * zspan
    if project_floor:
        ax.contourf(X, Y, Z, levels=18, cmap=cmap, alpha=0.32,
                    offset=base, zdir="z")

    if path is not None:
        P = np.asarray(path, dtype=float)
        zp = np.array([float(f(px, py)) for px, py in P]) + 0.015 * zspan
        ax.plot(P[:, 0], P[:, 1], zp, color="white", lw=4.2, zorder=10)
        ax.plot(P[:, 0], P[:, 1], zp, "-o", color=PALETTE["red"],
                mfc=PALETTE["amber"], mec="white", lw=2.0, ms=4.5, zorder=11)
        ax.scatter([P[0, 0]], [P[0, 1]], [zp[0]], color="white",
                   edgecolor=PALETTE["red"], s=70, lw=1.8, zorder=12)
        ax.scatter([P[-1, 0]], [P[-1, 1]], [zp[-1]], marker="*", s=200,
                   color="white", edgecolor=PALETTE["green"], lw=1.6, zorder=12)

    ax.set_zlim(base, zmax)
    # clean, light panes + faint 3-D grid
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((0, 0, 0, 0.08))
        try:
            axis._axinfo["grid"]["color"] = (0, 0, 0, 0.07)
            axis._axinfo["grid"]["linewidth"] = 0.6
        except Exception:  # noqa: BLE001
            pass
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.view_init(elev=view[0], azim=view[1])
    ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    fig.tight_layout()
    if out:
        fig.savefig(out)
        plt.close(fig)
    return fig


def gradient_descent(f, grad, start, lr, steps, xlim, ylim, title, *,
                     n=200, levels=20, xlabel="x", ylabel="y", noise=0.0,
                     seed=0, mark_min=None, label=None, out=None):
    """Contour map + the path a gradient-descent run takes (dots joined up).

    grad : function (x, y) -> (gx, gy). Slide ``lr`` to feel convergence vs
    overshoot. The breadcrumb trail makes the dynamics visible.
    noise : if > 0, add Gaussian jitter (this fraction of the gradient's size)
            to each step — turns batch GD into a wandering SGD-style walk.
    mark_min : optional (x, y) of the true minimum to star.
    The path is drawn with a white "halo" underneath so it reads on any colour.
    """
    use_house_style()
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    ax.contourf(X, Y, Z, levels=levels, cmap=HOUSE_CMAP, alpha=0.92)
    ax.contour(X, Y, Z, levels=levels, colors="white", linewidths=0.35,
               alpha=0.40)
    p = np.array(start, dtype=float)
    path = [p.copy()]
    for _ in range(int(steps)):
        g = np.array(grad(p[0], p[1]), dtype=float)
        if noise:
            g = g + noise * (np.linalg.norm(g) + 1e-9) * rng.standard_normal(2)
        p = p - lr * g
        path.append(p.copy())
    path = np.array(path)
    # white halo first, coloured trail on top -> always legible
    ax.plot(path[:, 0], path[:, 1], color="white", lw=4.4, alpha=0.95, zorder=4,
            solid_capstyle="round")
    ax.plot(path[:, 0], path[:, 1], "-o", color=PALETTE["red"], mec="white",
            mfc=PALETTE["amber"], lw=2.0, ms=5, zorder=5, label=label)
    ax.scatter([path[0, 0]], [path[0, 1]], color="white",
               edgecolor=PALETTE["red"], linewidth=1.8, s=85, zorder=6)
    if mark_min is not None:
        ax.scatter([mark_min[0]], [mark_min[1]], marker="*", s=190,
                   color="white", edgecolor=PALETTE["green"], linewidth=1.6,
                   zorder=7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(False)
    if label:
        ax.legend(loc="best")
    ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    fig.tight_layout()
    if out:
        fig.savefig(out)
        plt.close(fig)
    return fig


def vectors2d(vectors, title, *, xlim=None, ylim=None,
              xlabel="dimension 1", ylabel="dimension 2", out=None):
    """Arrows from the origin. vectors: list of (x, y, label, colour).

    For embeddings, dot products, basis images, any "direction = meaning" idea.
    """
    use_house_style()
    import matplotlib.patches as mpatches
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    xs_all, ys_all = [0.0], [0.0]
    for (x, y, label, col) in vectors:
        ax.add_patch(mpatches.FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>",
                     mutation_scale=14, color=col, lw=2.2, zorder=3))
        ax.annotate(label, xy=(x, y),
                    xytext=(x * 1.04 + 0.02, y * 1.04 + 0.02),
                    color=col, fontweight="bold", fontsize=11)
        xs_all.append(x)
        ys_all.append(y)
    pad = 0.3
    ax.set_xlim(xlim or (min(xs_all) - pad, max(xs_all) + pad))
    ax.set_ylim(ylim or (min(ys_all) - pad, max(ys_all) + pad))
    ax.axhline(0, color=PALETTE["grid"], lw=0.8)
    ax.axvline(0, color=PALETTE["grid"], lw=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(False)
    return _finish(fig, ax, title, out)


def heatmap(matrix, title, *, row_labels=None, col_labels=None, annotate=True,
            fmt="{:.0f}", xlabel="", ylabel="", out=None):
    """A matrix as a heatmap with annotated cells.

    For transition tables, attention matrices, weight/confusion matrices.
    """
    use_house_style()
    M = np.array(matrix, dtype=float)
    fig, ax = plt.subplots(figsize=(0.9 * M.shape[1] + 2.2, 0.7 * M.shape[0] + 1.8))
    im = ax.imshow(M, cmap=HOUSE_CMAP, aspect="auto")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if col_labels is not None:
        ax.set_xticks(range(M.shape[1]))
        ax.set_xticklabels(col_labels)
    if row_labels is not None:
        ax.set_yticks(range(M.shape[0]))
        ax.set_yticklabels(row_labels)
    mid = (float(M.min()) + float(M.max())) / 2.0
    if annotate:
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                v = M[i, j]
                ax.text(j, i, fmt.format(v), ha="center", va="center",
                        color="white" if v < mid else PALETTE["ink"],
                        fontsize=9.5, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    fig.tight_layout()
    if out:
        fig.savefig(out)
        plt.close(fig)
    return fig


def flow(steps, title, *, direction="lr", color=None, out=None):
    """Box-and-arrow flow diagram for a pipeline / algorithm / agent loop.

    steps : list of short strings (use a ``\\n`` to wrap long ones).
    direction : "lr" (left to right) or "tb" (top to bottom).
    """
    color = color or PALETTE["blue"]
    use_house_style()
    import matplotlib.patches as mpatches
    k = max(1, len(steps))
    horiz = direction == "lr"
    fig, ax = plt.subplots(figsize=(7.0, 1.9) if horiz else (4.4, 1.0 * k + 0.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(cx, cy, w, h, text):
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.010,rounding_size=0.018",
            fc=PALETTE["fill"], ec=color, lw=1.6, zorder=3))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=9.0,
                color=PALETTE["ink"], zorder=4)

    if horiz:
        slot = 0.96 / k
        w, h, cy = slot * 0.80, 0.46, 0.5
        for i, s in enumerate(steps):
            cx = 0.02 + slot * (i + 0.5)
            box(cx, cy, w, h, s)
            if i < k - 1:
                ax.add_patch(mpatches.FancyArrowPatch(
                    (cx + w / 2, cy), (cx + slot - w / 2, cy),
                    arrowstyle="-|>", mutation_scale=13, color=color, lw=1.8))
    else:
        slot = 0.96 / k
        w, h, cx = 0.8, slot * 0.62, 0.5
        for i, s in enumerate(steps):
            cy = 0.98 - slot * (i + 0.5)
            box(cx, cy, w, h, s)
            if i < k - 1:
                ax.add_patch(mpatches.FancyArrowPatch(
                    (cx, cy - h / 2), (cx, cy - slot + h / 2),
                    arrowstyle="-|>", mutation_scale=13, color=color, lw=1.8))
    ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    fig.tight_layout()
    if out:
        fig.savefig(out)
        plt.close(fig)
    return fig


def annotated_sequence(tokens, title, *, tags=None, highlight=None,
                       arrows=None, out=None):
    """A sentence/sequence strip: tokens in boxes, optional tags beneath, and
    optional curved arrows above (forward/backward reading, attention links).

    tokens    : list of words.
    tags      : optional per-token labels drawn beneath each token.
    highlight : optional iterable of indices to colour (the focus word).
    arrows    : optional list of (i, j, kind), kind in {"fwd", "bwd"} -> a curved
                arrow from token i to token j, above the strip.
    """
    use_house_style()
    import matplotlib.patches as mpatches
    n = max(1, len(tokens))
    hi = set(highlight or [])
    fig, ax = plt.subplots(figsize=(min(7.0, 1.15 * n + 1.0), 2.5))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis("off")
    cy, bw, bh = 0.42, 0.84, 0.30
    centres = []
    for i, tok in enumerate(tokens):
        cx = i + 0.5
        centres.append(cx)
        focus = i in hi
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - bw / 2, cy - bh / 2), bw, bh,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            fc="#E4F2EA" if focus else PALETTE["fill"],
            ec=PALETTE["green"] if focus else PALETTE["muted"],
            lw=2.0 if focus else 1.0, zorder=3))
        ax.text(cx, cy, tok, ha="center", va="center", fontsize=10.5,
                color=PALETTE["ink"], fontweight="bold" if focus else "normal", zorder=4)
        if tags and i < len(tags) and tags[i]:
            ax.text(cx, cy - bh / 2 - 0.12, tags[i], ha="center", va="top",
                    fontsize=9.0, color=PALETTE["blue"], fontweight="bold")
    for (i, j, kind) in (arrows or []):
        col = PALETTE["blue"] if kind == "fwd" else PALETTE["red"]
        rad = -0.45 if kind == "fwd" else 0.45
        ax.add_patch(mpatches.FancyArrowPatch(
            (centres[i], cy + bh / 2), (centres[j], cy + bh / 2),
            connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
            mutation_scale=13, color=col, lw=1.8, zorder=2))
    ax.set_title(title, color=PALETTE["ink"], fontweight="bold")
    fig.tight_layout()
    if out:
        fig.savefig(out)
        plt.close(fig)
    return fig


# ---------------------------------------------------------------------------
# Self-test: ``python3 figstyle.py [outdir]`` renders one of each plotter.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import sys

    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)

    pmf_bar([0, 1], [0.4, 0.6],
            "Bernoulli(p=0.6): one shot, two outcomes",
            out=os.path.join(outdir, "demo_pmf.png"))

    x = np.linspace(0, 8, 240)
    curve(x, {"rate 1.0": np.exp(-x), "rate 0.5": np.exp(-0.5 * x)},
          "Exponential densities for two rates",
          xlabel="t", ylabel="f(t)", fill_below="rate 1.0",
          out=os.path.join(outdir, "demo_curve.png"))

    shaded_normal(0, 1, -1, 1,
                  "Standard normal: about 68% within one sigma",
                  out=os.path.join(outdir, "demo_normal.png"))

    print("figstyle self-test wrote 3 PNGs to:", os.path.abspath(outdir))
