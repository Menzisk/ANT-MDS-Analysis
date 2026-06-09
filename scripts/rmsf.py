# Cα-RMSF plots for AbANT and SaANT MD simulations
# Data exported from ANT-MDS-Database via Desmond/Maestro simulation event analysis
# CSV format: semicolon-delimited, comma decimal separator

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

#USER INPUTS
CSV_FILE = "RMSF.csv"
X_LABEL  = "Residue"
Y_LABEL  = "Cα-RMSF (Å)"

df = pd.read_csv(CSV_FILE, sep=";", decimal=",")
df.columns = df.columns.str.strip()
df = df.rename(columns={"Residue Number 1": "residue.abant",
                         "Residue Number 2": "residue.saant"})
print(df.head(), "\n")


def plot_rmsf(df, x_col, systems, labels, outfile, legend_loc="upper left"):
    stats = {col: {"mean": np.mean(df[col]), "std": np.std(df[col])} for col in systems}
    legend_handles = []
    fig, ax = plt.subplots(figsize=(9, 5))

    for col, color in systems.items():
        ax.plot(df[x_col], df[col], color=color, linewidth=1.1)
        m, sd = stats[col]["mean"], stats[col]["std"]
        ax.axhline(m, color=color, linestyle="--", linewidth=1.2)
        ax.axhspan(m - sd, m + sd, color=color, alpha=0.08)
        legend_handles.append(
            mpatches.Patch(color=color, label=f"{labels[col]}  (mean={m:.2f}, SD={sd:.2f} Å)")
        )

    ax.set_xlabel(X_LABEL, fontsize=18, fontweight="bold")
    ax.set_ylabel(Y_LABEL, fontsize=18, fontweight="bold")
    ax.tick_params(axis="both", labelsize=15)
    ax.set_xlim(df[x_col].min(), df[x_col].max())
    ax.legend(handles=legend_handles, fontsize=10, framealpha=0.1,
              loc=legend_loc, title="Dashed = mean  |  Band = ± SD", title_fontsize=9.5)
    plt.tight_layout()
    fig.savefig(outfile, dpi=800, bbox_inches="tight")
    plt.show()


#AbANT-positive controls
plot_rmsf(df, "residue.abant",
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
    outfile="AbANT_RMSF_Pos.controls.png"
)

# AbANT-Apo+ligand
plot_rmsf(df, "residue.abant",
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
    outfile="AbANT_RMSF.png"
)

# SaANT-positive controls
plot_rmsf(df, "residue.saant",
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
    outfile="SaANT_RMSF_Pos.controls.png",
    legend_loc="upper right"
)

# SaANT-Apo+ligand
plot_rmsf(df, "residue.saant",
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
    outfile="SaANT_RMSF.png",
    legend_loc="upper right"
)
