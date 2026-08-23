"""
Pairplot of PC1-4 from your actual dPCA run, coloured by
the cluster labels THE pipeline already computed (silhouette-optimized
KMeans, k=). Uses the real output files from dpca_pipeline.py directly
-- no re-fitting of PCA or clustering here, just visualization of what
the pipeline already produced.

Inputs (from repo's ANT-MDS-Analysis dPCA_and_DCCM/AbANT/Apigenin/dPCA/ folder):
  - AbANT_Apigenin_dPCA_projections.csv  (PC1..PC10 per frame)
  - AbANT_Apigenin_dPCA_clusters.csv     (frame, PC1, PC2, cluster)
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CONDITION      = "AbPlazomicin"
PROJECTIONS_CSV = f"{CONDITION}_dPCA_projections.csv"
CLUSTERS_CSV = f"{CONDITION}_dPCA_clusters.csv"
OUT_PATH = f"{CONDITION}_dpca_pairplot.png"
N_COMPONENTS = 4  # how many PCs to include in the pairplot

sns.set_theme(style="ticks")

proj = pd.read_csv(PROJECTIONS_CSV)
clus = pd.read_csv(CLUSTERS_CSV)
assert len(proj) == len(clus), "projections and clusters files have different row counts"

pc_cols = [f"PC{i}" for i in range(1, N_COMPONENTS + 1)]
df = proj[pc_cols].copy()
df["cluster"] = clus["cluster"].values

# Relabel clusters by mean PC1 (low -> high) purely so the legend reads
# in a consistent order across figures; the underlying cluster
# assignments are untouched.
mean_pc1 = df.groupby("cluster")["PC1"].mean().sort_values()
order_map = {old: f"cluster {i}" for i, old in enumerate(mean_pc1.index)}
df["state"] = df["cluster"].map(order_map)
hue_order = [order_map[k] for k in mean_pc1.index]

g = sns.pairplot(df, vars=pc_cols, hue="state", hue_order=hue_order, palette="deep")
g.figure.suptitle(
    f"{CONDITION} dPCA (PC1-{N_COMPONENTS}), coloured by cluster (k={len(hue_order)})",
    y=1.02,
)
g.savefig(OUT_PATH, dpi=800, bbox_inches="tight")
print(f"Saved {OUT_PATH}")
print(df["state"].value_counts())
plt.show()
plt.close()