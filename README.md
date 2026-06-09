# ANT-MDS-Analysis

Computational analysis outputs and scripts for the structural dynamics study of
ANT(3″)-Ia aminoglycoside nucleotidyltransferase orthologues from
*Acinetobacter baumannii* (AbANT) and *Staphylococcus aureus* (SaANT).

## Systems

| Orthologue | Systems |
|---|---|
| AbANT | Apo, Spectinomycin, Plazomicin, AMP-Spectinomycin, Apigenin, ATP |
| SaANT | Apo, Spectinomycin, Plazomicin, AMP-Spectinomycin, Gallocatechin, ATP |

## Repository Contents

- `scripts/` — dPCA, FEL, DCCM, and trj2xtc pipelines and MD simulation property plots           (RMSD, RMSF, ROG, Ligand-RMSD, Ligand-SASA, interaction heatmaps
- `results/[orthologue]/[system]/dPCA/` — All dPCA outputs including
  cluster representative PDBs, projection CSVs, FEL data, eigenvalues,
  silhouette scores, loadings, scree, and log files
- `results/[orthologue]/[system]/DCCM/` — DCCM correlation matrix CSV

## Trajectory Data
Full trajectory PDB files are stored in the companion repository:
[ANT-MDS-Database](https://github.com/Menzisk/ANT-MDS-Database)

## Reference
Manuscript in preparation. Sikakane M. et al., 2026.
