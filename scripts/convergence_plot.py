import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- Config ---
CSV_FILE     = "convergance.csv"
FRACTION_COL = "Fraction"
OUTPUT_PNG   = "dPCA_convergence.png"
THRESHOLD    = 0.90  # fixed: was 0.75

df           = pd.read_csv(CSV_FILE, sep=None, engine='python')
FRACTION_COL = next((c for c in df.columns if c.lower() == FRACTION_COL.lower()), FRACTION_COL)
systems      = [c for c in df.columns if c != FRACTION_COL]
fractions    = df[FRACTION_COL].values

COLORS = {
    "Apo":          "black",
    "Holo":         "red",
    "pT231":        "blue",
    "pSer64":       "green",
    "pSer64_pT231": "orange",
}
COLOR_MAP = {k.lower(): v for k, v in COLORS.items()}

fig, ax = plt.subplots(figsize=(10, 7))

for system in systems:
    color = COLORS.get(system) or COLOR_MAP.get(system.lower())
    ax.plot(fractions, df[system].values,
            marker="o", linewidth=1.8, markersize=5,
            label=system, color=color)

# Convergence threshold reference line
ax.axhline(y=THRESHOLD, color="gray", linestyle="--",
           linewidth=1.0, label=f"Threshold ({THRESHOLD})")

# Axes — fixed: was set_xlim(1.0, 1.0) which collapsed the x-axis
ax.set_xlim(0.00, 1.05)
ax.set_ylim(0.0, 1.05)
ax.set_xticks([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
ax.set_xticklabels(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"])
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
ax.tick_params(labelsize=15)

ax.set_xlabel("Fraction of trajectory", fontsize=15)
ax.set_ylabel("Subspace overlap", fontsize=15)
ax.set_title("dPCA Convergence — Subspace Overlap", fontweight="bold", fontsize=15)
ax.legend(frameon=True, fontsize=11)
ax.grid(True, linestyle="--", alpha=0.1)

plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=800, bbox_inches="tight")
plt.show()
print(f"Saved: {OUTPUT_PNG}")
