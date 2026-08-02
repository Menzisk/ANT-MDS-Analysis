import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

CSV_FILE = "lig_wrt_protein.csv"
X_LABEL  = "Time (ns)"
Y_LABEL_LEFT  = "Ligand RMSD wrt Protein (Å)"
Y_LABEL_RIGHT = "Ligand RMSD wrt Protein (Å)"   # same units, separate scale

df = pd.read_csv(CSV_FILE, sep=";", decimal=",")
df.columns = df.columns.str.strip()
df = df.rename(columns={"Time (ns)": "time"})
print(df.head(), "\n")


def plot_rmsd(df, systems, labels, outfile,
              right_axis_cols=None,
              legend_loc="best"):
    """
    systems        : {col_name: color}
    labels         : {col_name: display_label}
    right_axis_cols: set/list of col_names to plot on right y-axis.
                     If None or empty, all series go on the left axis.
    """
    if right_axis_cols is None:
        right_axis_cols = set()
    else:
        right_axis_cols = set(right_axis_cols)

    left_cols  = [c for c in systems if c not in right_axis_cols]
    right_cols = [c for c in systems if c in right_axis_cols]

    #stats = {col: {"mean": np.mean(df[col]), "std": np.std(df[col])}
             #for col in systems}

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx() if right_cols else None

    #legend_handles = []

    def _draw(ax, col, color):
        #m, sd = stats[col]["mean"], stats[col]["std"]
        ax.plot(df["time"], df[col], color=color, linewidth=1.3)
        #ax.axhline(m, color=color, linestyle="--", linewidth=1.2)
        #ax.axhspan(m - sd, m + sd, color=color, alpha=0.08)
        #legend_handles.append(
            #mpatches.Patch(color=color,
                           #label=f"{labels[col]}  (mean={m:.2f}, SD={sd:.2f} Å)")
        #)

    for col in left_cols:
        _draw(ax1, col, systems[col])

    for col in right_cols:
        _draw(ax2, col, systems[col])

    # Left axis 
    ax1.set_xlabel(X_LABEL, fontsize=18, fontweight="bold")
    ax1.set_ylabel(Y_LABEL_LEFT, fontsize=18, fontweight="bold")
    ax1.tick_params(axis="both", labelsize=15)
    ax1.set_xlim(df["time"].min(), df["time"].max())

    # Right axis 
    if ax2 is not None:
        ax2.set_ylabel(Y_LABEL_RIGHT, fontsize=18, fontweight="bold")
        ax2.tick_params(axis="y", labelsize=15)
        # Optional: add a subtle label to distinguish axes
        ax2.yaxis.label.set_color("dimgray")

    # ── Legend (single, on ax1) ────────────────────────────────────
    #ax1.legend(handles=legend_handles, fontsize=10, framealpha=0.1,
               #loc=legend_loc,
               #title="Dashed = mean  |  Band = ± SD  |  * = right axis",
               #title_fontsize=9.5)

    plt.tight_layout()
    fig.savefig(outfile, dpi=800, bbox_inches="tight")
    plt.show()


# AbANT positive controls 
plot_rmsd(
    df,
    systems={
        "AbANT_Spectinomycin_Lig_wrt_Protein":     "orange",
        "AbANT_AMP_Spectinomycin_Lig_wrt_Protein": "fuchsia",
        "AbANT_ATP_Lig_wrt_Protein":               "indigo",
    },
    labels={
        "AbANT_Spectinomycin_Lig_wrt_Protein":     "Spectinomycin",
        "AbANT_AMP_Spectinomycin_Lig_wrt_Protein": "AMP-Spectinomycin *",
        "AbANT_ATP_Lig_wrt_Protein":               "ATP *",
    },
    right_axis_cols=[
        "AbANT_AMP_Spectinomycin_Lig_wrt_Protein",
        "AbANT_ATP_Lig_wrt_Protein",
    ],
    outfile="AbANT_lig_wrt_protein_Pos.controls.png",
    legend_loc="best",
)
# AbANT-Apo+ligand
plot_rmsd(df,
    systems={
        #"AbANT_Apo":        "black",
        "AbANT_Plazomicin_Lig_wrt_Protein": "lime",
        "AbANT_Apigenin_Lig_wrt_Protein":   "red",
    },
    labels={
        #"AbANT_Apo":        "APO",
        "AbANT_Plazomicin_Lig_wrt_Protein": "Plazomicin *",
        "AbANT_Apigenin_Lig_wrt_Protein":   "Apigenin-7-O-gentibioside",
    },
right_axis_cols=[
        "AbANT_Plazomicin_Lig_wrt_Protein",
    ],
    outfile="AbANT_lig_wrt_.png",
    legend_loc="best"

)

# SaANT-positive controls
plot_rmsd(df,
    systems={
        #"SaANT_Apo":               "black",
        "SaANT_Spectinomycin_Lig_wrt_Protein":     "orange",
        "SaANT_AMP_Spectinomycin_Lig_wrt_Protein": "fuchsia",
        "SaANT_ATP_Lig_wrt_Protein":               "indigo",
    },
    labels={
        #"SaANT_Apo":               "APO",
        "SaANT_Spectinomycin_Lig_wrt_Protein":     "Spectinomycin",
        "SaANT_AMP_Spectinomycin_Lig_wrt_Protein": "AMP-Spectinomycin",
        "SaANT_ATP_Lig_wrt_Protein":               "ATP",
    },
    outfile="SaANT_lig_wrt_protein_Pos.controls.png",
    legend_loc="best"
)

# SaANT-Apo+ligand
plot_rmsd(df,
    systems={
        #"SaANT_Apo":           "black",
        "SaANT_Plazomicin_Lig_wrt_Protein":    "lime",
        "SaANT_Gallocatechin_Lig_wrt_Protein": "dodgerblue",
    },
    labels={
        #"SaANT_Apo":           "APO",
        "SaANT_Plazomicin_Lig_wrt_Protein":    "Plazomicin",
        "SaANT_Gallocatechin_Lig_wrt_Protein": "Gallocatechin",
    },
    outfile="SaANT_lig_wrt_protein.png",
    legend_loc="best"
)