#Script for PCA by time and clusters plots
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import tick_params

#user imputs
CONDITIONS = "" #Name of yor systems
MASTER_CSV = f"{CONDITIONS}_dPCA_master.csv"

#LOAD CSV
df = pd.read_csv(MASTER_CSV)
print(df.head())
print()
print(df.columns)

#PCA time
fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
#scatter plot
sc = ax.scatter(df["PC1"], df["PC2"], c=df["frame"], cmap="viridis", s=65, alpha=0.7, linewidths=0)

#legend
cbar = fig.colorbar(sc, ax=ax)
cbar.set_label("Number of Frames (ns)", fontsize=14, fontweight="bold")
cbar.ax.tick_params(labelsize=14)

ax.set_xlabel("PC1 variance : 6.56%", fontsize=14, fontweight="bold") #change according to pca variance (logfile)
ax.set_ylabel("PC2 variance : 3.29%",fontsize=14, fontweight="bold")
ax.set_title(f"dPCA - Conformational Sampling by Time (ns) {CONDITIONS}", fontsize=14, fontweight="bold")
ax.tick_params(labelsize=14)

plt.tight_layout()
plt.bbox_inches="tight"
plt.savefig(f"{CONDITIONS}_dPCA_time.png", dpi=800)
plt.show()

#PCA cluster
fig2, ax = plt.subplots(figsize=(12, 8), dpi=150)
#Get colormap
cmap = plt.get_cmap("Dark2_r")
clusters = sorted(df["cluster"].unique())
norm = plt.Normalize(min(clusters), max(clusters))
# Main scatter
sc = ax.scatter(
    df["PC1"], df["PC2"],
    c=df["cluster"],
    cmap=cmap,
    s=65,
    alpha=0.7,
    linewidths=0
)

# Colorbar (Cluster #)
cbar = fig2.colorbar(sc, ax=ax)
cbar.set_label("Cluster Number", fontsize=14, fontweight="bold")
cbar.ax.tick_params(labelsize=14)

#legend
handles = []
labels = []

for c in sorted(df["cluster"].unique()):
    count = (df["cluster"] == c).sum()

    # create dummy handle for legend
    color = cmap(norm(c))
    handles.append(
        plt.Line2D([], [], marker='o', linestyle='', markersize=8, color=color)
    )
    labels.append(f"Cluster {c} ({count} frames)")

# Add legend
ax.legend(handles, labels, title="Clusters", loc="best", fontsize=10)

# Labels
ax.set_xlabel("PC1", fontsize=14, fontweight="bold")
ax.set_ylabel("PC2", fontsize=14, fontweight="bold")
ax.set_title(f"dPCA - Conformational Sampling by cluster {CONDITIONS}", fontsize=14, fontweight="bold")
ax.tick_params(labelsize=14)

plt.tight_layout()
plt.bbox_inches="tight"
plt.savefig(f"{CONDITIONS}_dPCA_clusters.png", dpi=800)
plt.show()