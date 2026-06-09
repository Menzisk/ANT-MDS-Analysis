# Protein-ligand contact heatmaps for AbANT Plazomicin MD simulation
# Contact data (.dat files) exported directly from Desmond/Maestro interaction analysis
# Each file contains frame-by-frame H-bond, hydrophobic, ionic, and water-bridge contacts

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#USER INPUTS
SIM_LENGTH_NS = 1000
N_FRAMES      = 1000
SYSTEM_NAME   = "AbANT Plazomicin"

NS_PER_FRAME = SIM_LENGTH_NS / N_FRAMES

files = {
    "PL-Contacts_HBond.dat":       "H-Bond",
    "PL-Contacts_Hydrophobic.dat": "Hydrophobic",
    "PL-Contacts_Ionic.dat":       "Ionic",
    "PL-Contacts_WaterBridge.dat": "WaterBridge",
}

frames = []
for filename, contact_type in files.items():
    df = pd.read_csv(filename, sep=r'\s+', skiprows=1, header=None)
    df = df.rename(columns={0: "Frame", 1: "Residue_num", 3: "ResName"})
    df["contact_type"]  = contact_type
    df["time_ns"]       = df["Frame"] * NS_PER_FRAME
    df["residue_label"] = df["ResName"] + df["Residue_num"].astype(str)
    df = df[["Frame", "time_ns", "ResName", "Residue_num", "residue_label", "contact_type"]]
    frames.append(df)
    print(f"Loaded {contact_type}: {len(df)} rows")

df_all = pd.concat(frames, ignore_index=True)
print(f"\nCombined: {len(df_all)} rows")
print(f"Residues: {sorted(df_all['residue_label'].unique())}\n")

df_hbond       = df_all[df_all["contact_type"] == "H-Bond"]
df_hydrophobic = df_all[df_all["contact_type"] == "Hydrophobic"]
df_ionic       = df_all[df_all["contact_type"] == "Ionic"]
df_waterbridge = df_all[df_all["contact_type"] == "WaterBridge"]

def plot_heatmap(df, title, filename, cmap="YlOrRd"):
    counts = df.groupby(["time_ns", "residue_label"]).size().reset_index(name="contacts")
    matrix = counts.pivot(index="residue_label", columns="time_ns", values="contacts").fillna(0)
    matrix = matrix.loc[sorted(matrix.index, key=lambda x: int(''.join(filter(str.isdigit, x))))]

    fig, ax = plt.subplots(figsize=(14, 7))
    heatmap = ax.imshow(matrix.values, aspect="auto", origin="lower", cmap=cmap)

    cbar = fig.colorbar(heatmap, ax=ax)
    cbar.ax.tick_params(axis="both", labelsize=15)
    cbar.set_label("Number of contacts", fontsize=18, fontweight="bold")

    tick_positions = np.linspace(0, matrix.shape[1] - 1, 11, dtype=int)
    tick_labels    = np.linspace(0, SIM_LENGTH_NS, 11, dtype=int)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([str(t) for t in tick_labels], fontsize=15)
    ax.set_xlabel("Time (ns)", fontsize=20, fontweight="bold")

    ax.set_yticks(np.arange(len(matrix.index)))
    ax.set_yticklabels(matrix.index, fontsize=15)
    ax.set_ylabel("Residue", fontsize=20, fontweight="bold")

    ax.set_title(title, fontsize=20, fontweight="bold")
    plt.tight_layout()
    plt.savefig(filename, dpi=800, bbox_inches="tight")
    plt.show()
    print(f"Saved: {filename}")

plots = [
    (df_all,         "All Contacts",          "heatmap_combined.png",    "YlOrRd"),
    (df_hbond,       "H-Bond Contacts",       "heatmap_hbond.png",       "PuBuGn"),
    (df_hydrophobic, "Hydrophobic Contacts",  "heatmap_hydrophobic.png", "RdPu"),
    (df_ionic,       "Ionic Contacts",        "heatmap_ionic.png",       "OrRd"),
    (df_waterbridge, "Water Bridge Contacts", "heatmap_waterbridge.png", "ocean_r"),
]

for df, title, filename, cmap in plots:
    plot_heatmap(df, f"{title} — {SYSTEM_NAME}", filename, cmap)