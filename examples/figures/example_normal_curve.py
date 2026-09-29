#!/usr/bin/env python3
"""Example companion figure: Normal curve with the 68-95-99.7 bands.

Copy-adapt this for any per-lecture figure script. The only contract with the
build orchestrator (scripts/build_pdf.py) is: when run, save a PNG next to
yourself. Everything stylistic comes from scripts/figstyle.py.
"""
import math
import os
import sys

# --- 1) Import the house style robustly ------------------------------------
# Resolve scripts/ relative to THIS FILE (never the cwd). For real kits in
# output/<slug>/figures/, scripts/build_pdf.py already puts the kit's scripts/
# on PYTHONPATH, so a plain `from figstyle import ...` works at any depth.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(os.path.join(_HERE, "..", "..", "scripts")))

from figstyle import use_house_style, PALETTE  # noqa: E402
import numpy as np                             # noqa: E402
import matplotlib.pyplot as plt                # noqa: E402  (figstyle already set the headless Agg backend)


def main() -> None:
    # --- 2) Apply the shared look once (idempotent) -------------------------
    use_house_style()  # fonts, bold ink titles, soft grid, spines, size, dpi

    # --- 3) Draw: standard normal pdf with nested 1/2/3-sigma bands ---------
    # (For a SINGLE shaded slice, prefer the ready-made helper instead:
    #  from figstyle import shaded_normal; shaded_normal(0, 1, -1, 1, "...", out=...))
    mu, sigma = 0.0, 1.0
    xs = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    pdf = np.exp(-0.5 * ((xs - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))

    fig, ax = plt.subplots()                  # rcParams give the house figsize
    ax.plot(xs, pdf, color=PALETTE["blue"], zorder=3)

    # Widest band first so the narrower, darker ones layer on top. Each band:
    # shade it, label it in the bold ink colour, dash-mark its edges in grey.
    for k, share, alpha, label_xy in [(3, "99.7%", 0.10, (2.62, 0.034)),
                                      (2, "95%",   0.16, (1.55, 0.048)),
                                      (1, "68%",   0.24, (0.00, 0.150))]:
        mask = (xs >= mu - k * sigma) & (xs <= mu + k * sigma)
        ax.fill_between(xs[mask], pdf[mask], color=PALETTE["blue"],
                        alpha=alpha, zorder=2)
        ax.annotate(share, xy=label_xy, ha="center", va="center",
                    fontsize=10, color=PALETTE["ink"], fontweight="bold")
        for edge in (mu - k * sigma, mu + k * sigma):
            ax.axvline(edge, color=PALETTE["muted"], linewidth=0.9,
                       linestyle=(0, (4, 3)), zorder=1)

    # House style bakes a short BOLD title into the plot itself.
    ax.set_title("Normal(0, 1): the 68-95-99.7 rule as nested areas")
    ax.set_xlabel("x (in units of sigma)")
    ax.set_ylabel("density")
    ax.set_ylim(bottom=0)

    # --- 4) Save the PNG NEXT TO THIS SCRIPT (the part that matters) --------
    out = os.path.join(_HERE, "example_normal_curve.png")
    fig.tight_layout()
    fig.savefig(out)                          # rcParams: dpi 150, tight bbox
    plt.close(fig)                            # free memory in batch builds
    print("wrote", out)


if __name__ == "__main__":
    main()
