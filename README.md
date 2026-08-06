
![AMBER18](https://img.shields.io/badge/AMBER-18-orange?style=flat-square)
![Schrödinger](https://img.shields.io/badge/Schr%C3%B6dinger-Maestro%2FDesmond-red?style=flat-square)
![MD Simulation](https://img.shields.io/badge/MD-Molecular%20Dynamics-blueviolet?style=flat-square)
![HPC](https://img.shields.io/badge/HPC-Lengau%20Cluster-informational?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)

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

- `scripts/` — MD simulation property plots (RMSD, RMSF, ROG, Ligand-RMSD, Ligand-SASA, interaction heatmaps)
- `results/[orthologue]/[system]/dPCA/` — All dPCA outputs including
  cluster representative PDBs, projection CSVs, FEL data, eigenvalues,
  silhouette scores, loadings and scree
- `results/[orthologue]/[system]/DCCM/` — DCCM correlation matrix CSV

## Pipeline Availability

The core dPCA, FEL, DCCM, and trajectory-conversion (trj2xtc) pipelines are maintained in a private repository as part of ongoing unpublished research. These are available on request for collaboration or review purposes (co-authorship terms apply).

## Trajectory Data
Full trajectory PDB files are stored in the companion repository:
[ANT-MDS-Database](https://github.com/Menzisk/ANT-MDS-Database)

## Reference
Manuscript in preparation. Sikakane M. et al., 2026.
