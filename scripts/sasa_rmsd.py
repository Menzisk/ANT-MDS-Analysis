# Ligand-RMSD and Ligand-SASA plots for AbANT and SaANT MD simulations
# Data exported from ANT-MDS-Database via Desmond/Maestro simulation event analysis
# CSV format: semicolon-delimited, comma decimal separator

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- USER INPUTS ---
CSV_FILE = "Ligand_RMSD_SASA.csv"
X_LABEL  = "Time (ns)"
Y_RMSD   = "Ligand-RMSD (Å)"
Y_SASA   = "Ligand-SASA (Å²)"

df = pd.read_csv(CSV_FILE, sep=";", decimal=",")
df.columns = df.columns.str.strip()
df = df.rename(columns={"Time": "time"})
print(df.head(), "\n")


def plot_ligand(df, systems, labels, ylabel, outfile, legend_loc="upper left"):
    stats = {col: {"mean": np.mean(df[col]), "std": np.std(df[col])} for col in systems}
    legend_handles = []
    fig, ax = plt.subplots(figsize=(9, 5))

    for col, color in systems.items():
        ax.plot(df["time"], df[col], color=color, linewidth=1.1)
        m, sd = stats[col]["mean"], stats[col]["std"]
        ax.axhline(m, color=color, linestyle="--", linewidth=1.2)
        ax.axhspan(m - sd, m + sd, color=color, alpha=0.08)
        legend_handles.append(
            mpatches.Patch(color=color, label=f"{labels[col]}  (mean={m:.2f}, SD={sd:.2f})")
        )

    ax.set_xlabel(X_LABEL, fontsize=18, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=18, fontweight="bold")
    ax.tick_params(axis="both", labelsize=15)
    ax.set_xlim(df["time"].min(), df["time"].max())
    ax.legend(handles=legend_handles, fontsize=10, framealpha=0.1,
              loc=legend_loc, title="Dashed = mean  |  Band = ± SD", title_fontsize=9.5)
    plt.tight_layout()
    fig.savefig(outfile, dpi=800, bbox_inches="tight")
    plt.show()


#AbANT Ligand-RMSD
plot_ligand(df,
    systems={"AbANT_Spectinomycin": "orange", "AbANT_AMP-Spectinomycin": "fuchsia", "AbANT_ATP": "indigo"},
    labels={"AbANT_Spectinomycin": "Spectinomycin", "AbANT_AMP-Spectinomycin": "AMP-Spectinomycin", "AbANT_ATP": "ATP"},
    ylabel=Y_RMSD, outfile="AbANT_Ligand_RMSD_Pos.controls.png"
)

plot_ligand(df,
    systems={"AbANT_Plazomicin": "lime", "AbANT_Apigenin": "red"},
    labels={"AbANT_Plazomicin": "Plazomicin", "AbANT_Apigenin": "Apigenin-7-O-gentibioside"},
    ylabel=Y_RMSD, outfile="AbANT_Ligand_RMSD.png"
)

#AbANT Ligand-SASA
plot_ligand(df,
    systems={"AbANT_Spectinomycin_SASA": "orange", "AbANT_AMP-Spectinomycin_SASA": "fuchsia", "AbANT_ATP_SASA": "indigo"},
    labels={"AbANT_Spectinomycin_SASA": "Spectinomycin", "AbANT_AMP-Spectinomycin_SASA": "AMP-Spectinomycin", "AbANT_ATP_SASA": "ATP"},
    ylabel=Y_SASA, outfile="AbANT_SASA_RMSD_Pos.controls.png", legend_loc="lower left"
)

plot_ligand(df,
    systems={"AbANT_Plazomicin_SASA": "lime", "AbANT_Apigenin_SASA": "red"},
    labels={"AbANT_Plazomicin_SASA": "Plazomicin", "AbANT_Apigenin_SASA": "Apigenin-7-O-gentibioside"},
    ylabel=Y_SASA, outfile="AbANT_SASA_RMSD.png"
)

#SaANT Ligand-RMSD
plot_ligand(df,
    systems={"SaANT_Spectinomycin": "orange", "SaANT_AMP-Spectinomycin": "fuchsia", "SaANT_ATP": "indigo"},
    labels={"SaANT_Spectinomycin": "Spectinomycin", "SaANT_AMP-Spectinomycin": "AMP-Spectinomycin", "SaANT_ATP": "ATP"},
    ylabel=Y_RMSD, outfile="SaANT_Ligand_RMSD_Pos.controls.png"
)

plot_ligand(df,
    systems={"SaANT_Plazomicin": "lime", "SaANT_Gallocatechin": "dodgerblue"},
    labels={"SaANT_Plazomicin": "Plazomicin", "SaANT_Gallocatechin": "Gallocatechin"},
    ylabel=Y_RMSD, outfile="SaANT_Ligand_RMSD.png"
)

#SaANT Ligand-SASA
plot_ligand(df,
    systems={"SaANT_Spectinomycin_SASA": "orange", "SaANT_AMP-Spectinomycin_SASA": "fuchsia", "SaANT_ATP_SASA": "indigo"},
    labels={"SaANT_Spectinomycin_SASA": "Spectinomycin", "SaANT_AMP-Spectinomycin_SASA": "AMP-Spectinomycin", "SaANT_ATP_SASA": "ATP"},
    ylabel=Y_SASA, outfile="SaANT_SASA_RMSD_Pos.controls.png"
)

plot_ligand(df,
    systems={"SaANT_Plazomicin_SASA": "lime", "SaANT_Gallocatechin_SASA": "dodgerblue"},
    labels={"SaANT_Plazomicin_SASA": "Plazomicin", "SaANT_Gallocatechin_SASA": "Gallocatechin"},
    ylabel=Y_SASA, outfile="SaANT_SASA_RMSD.png"
)
