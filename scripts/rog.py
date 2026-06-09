# Radius of gyration (ROG) plots for AbANT and SaANT MD simulations
# Data exported from ANT-MDS-Database via Desmond/Maestro simulation event analysis
# CSV format: semicolon-delimited, comma decimal separator

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- USER INPUTS ---
CSV_FILE = "ROG.csv"
X_LABEL  = "Time (ns)"
Y_LABEL  = "Cα-ROG (Å)"

df = pd.read_csv(CSV_FILE, sep=";", decimal=",")
df.columns = df.columns.str.strip()
df = df.rename(columns={"Time": "time"})
print(df.head(), "\n")


def plot_rog(df, systems, labels, outfile, legend_loc="upper right"):
    stats = {col: {"mean": np.mean(df[col]), "std": np.std(df[col])} for col in systems}
    legend_handles = []
    fig, ax = plt.subplots(figsize=(9, 5))

    for col, color in systems.items():
        ax.plot(df["time"], df[col], color=color, linewidth=1.1)
        m, sd = stats[col]["mean"], stats[col]["std"]
        ax.axhline(m, color=color, linestyle="--", linewidth=1.2)
        ax.axhspan(m - sd, m + sd, color=color, alpha=0.08)
        legend_handles.append(
            mpatches.Patch(color=color, label=f"{labels[col]}  (mean={m:.2f}, SD={sd:.2f} Å)")
        )

    ax.set_xlabel(X_LABEL, fontsize=18, fontweight="bold")
    ax.set_ylabel(Y_LABEL, fontsize=18, fontweight="bold")
    ax.tick_params(axis="both", labelsize=15)
    ax.set_xlim(df["time"].min(), df["time"].max())
    ax.legend(handles=legend_handles, fontsize=10, framealpha=0.1,
              loc=legend_loc, title="Dashed = mean  |  Band = ± SD", title_fontsize=9.5)
    plt.tight_layout()
    fig.savefig(outfile, dpi=800, bbox_inches="tight")
    plt.show()


# AbANT-positive controls
plot_rog(df,
    systems={
        "AbANT_Apo":               "black",
        "AbANT_Spectinomycin":     "orange",
        "AbANT_AMP-Spectinomycin": "fuchsia",
        "AbANT_ATP":               "indigo",
    },
    labels={
        "AbANT_Apo":               "APO",
        "AbANT_Spectinomycin":     "Spectinomycin",
        "AbANT_AMP-Spectinomycin": "AMP-Spectinomycin",
        "AbANT_ATP":               "ATP",
    },
    outfile="AbANT_ROG_Pos.controls.png"
)

# AbANT-Apo+ligand
plot_rog(df,
    systems={
        "AbANT_Apo":        "black",
        "AbANT_Plazomicin": "lime",
        "AbANT_Apigenin":   "red",
    },
    labels={
        "AbANT_Apo":        "APO",
        "AbANT_Plazomicin": "Plazomicin",
        "AbANT_Apigenin":   "Apigenin-7-O-gentibioside",
    },
    outfile="AbANT_ROG.png",
    legend_loc="upper left"
)

# SaANT-positive controls
plot_rog(df,
    systems={
        "SaANT_Apo":               "black",
        "SaANT_Spectinomycin":     "orange",
        "SaANT_AMP-Spectinomycin": "fuchsia",
        "SaANT_ATP":               "indigo",
    },
    labels={
        "SaANT_Apo":               "APO",
        "SaANT_Spectinomycin":     "Spectinomycin",
        "SaANT_AMP-Spectinomycin": "AMP-Spectinomycin",
        "SaANT_ATP":               "ATP",
    },
    outfile="SaANT_ROG_Pos.controls.png",
    legend_loc="upper left"
)

# SaANT-Apo+ligand
plot_rog(df,
    systems={
        "SaANT_Apo":           "black",
        "SaANT_Plazomicin":    "lime",
        "SaANT_Gallocatechin": "dodgerblue",
    },
    labels={
        "SaANT_Apo":           "APO",
        "SaANT_Plazomicin":    "Plazomicin",
        "SaANT_Gallocatechin": "Gallocatechin",
    },
    outfile="SaANT_ROG.png",
    legend_loc="upper left"
)
