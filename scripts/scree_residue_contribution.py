#SCREE PLOT AND RESIDUE CONTRIBUTION BAR CHART script

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# USER INPUTS                    
CONDITION      = ""  # set your condition name here (matches CSV prefix, eg AbANT_Plazomicin)
TOP_N_RESIDUES = 20  # define how many residues to show (20 is a good default, 10 can be considered)
DPI            = 800      

SCREE        = f"{CONDITION}_dPCA_explained_var.csv"
LOADINGS_CSV = f"{CONDITION}_dPCA_loadings.csv"

# 1. SCREE PLOT
print("\n Scree plot")

scree_df = pd.read_csv(SCREE)
print(scree_df)

pcs     = scree_df["PC"].tolist()
var_pct = scree_df["explained_variance_ratio"] * 100
cum_pct = scree_df["cumulative_variance"] * 100

fig, ax1 = plt.subplots(figsize=(7, 5), dpi=150)
ax2 = ax1.twinx()

ax1.plot(pcs, var_pct, c="blue",  label="Explained",  marker="o", alpha=0.8)
ax2.plot(pcs, cum_pct, c="red",   label="Cumulative", marker="o", alpha=0.8)
ax2.axhline(90, color="grey", linestyle="--", linewidth=0.8, alpha=0.6)

ax1.set_xlabel("Principal Component",    fontsize=14, fontweight="bold")   
ax1.set_ylabel("Explained Variance (%)", fontsize=14, fontweight="bold",   
               color="blue", labelpad=10, alpha=0.8)
ax2.set_ylabel("Cumulative Variance (%)", fontsize=14, fontweight="bold", 
               color="red", alpha=0.8)
ax1.tick_params(labelsize=14)
ax2.tick_params(labelsize=14)
ax1.set_title(f"Scree Plot – dPCA\n{CONDITION}")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False)

plt.tight_layout()
plt.savefig(f"{CONDITION}_scree.png", dpi=800, bbox_inches="tight")
plt.show()

# 2. RESIDUE CONTRIBUTION BAR CHART
print("\n Residue contribution")

def feature_to_residue(name: str) -> str:
    """
    Extract residue label from a dihedral feature name.

    Expected formats produced by the dPCA pipeline:
        sin_phi_ALA_23   →  ALA23
        cos_psi_GLY_5    →  GLY5
    Handles both 3-part and 4-part underscore splits gracefully.
    """
    parts = name.split("_")
    if len(parts) >= 4:
        return parts[2] + parts[3]   # RESNAME + RESID
    elif len(parts) == 3:
        return parts[2]              # just the last part
    return name                      

# Load loadings (feature names as row index)
load_df = pd.read_csv(LOADINGS_CSV, index_col=0)   
print(load_df.head())

# Map features to residue labels 
load_df["residue"] = [feature_to_residue(f) for f in load_df.index]

# Sum absolute loadings per residue for PC1 and PC2 
res_contrib = (
    load_df
    .groupby("residue")[["PC1", "PC2"]]
    .agg(lambda x: x.abs().sum())
    .reset_index()
)

# Sort by PC1 contribution, keep top N
res_contrib = (
    res_contrib
    .sort_values("PC1", ascending=False)
    .head(TOP_N_RESIDUES)
    .reset_index(drop=True)
)

# Grouped bar chart 
fig, ax = plt.subplots(figsize=(9, 5))
x     = np.arange(len(res_contrib))
width = 0.35

ax.bar(x - width / 2, res_contrib["PC1"], width,
       color="blue", alpha=0.8, label="PC1")
ax.bar(x + width / 2, res_contrib["PC2"], width,
       color="red", alpha=0.8, label="PC2")

ax.set_xticks(x)
ax.set_xticklabels(res_contrib["residue"], rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Summed |Loading|")
ax.set_title(f"Top {TOP_N_RESIDUES} Residue Contributions to PC1 & PC2\n{CONDITION}")
ax.legend(frameon=False)

plt.tight_layout()
plt.savefig(f"{CONDITION}_plot_residue_contribution.png", dpi=DPI)
plt.show()