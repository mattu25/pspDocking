#!/bin/bash
#SBATCH --job-name=testJob
#SBATCH --time=0:20:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --array=1-690

index=$((SLURM_ARRAY_TASK_ID + 11365))
ligandCSV=~/ligandData.csv

ligandPathways=($(awk -F',' '{print $3}' "$ligandCSV"))
ligandNames=($(awk -F',' '{print $4}' "$ligandCSV"))
outPathways=($(awk -F',' '{print $5}' "$ligandCSV"))

mkdir -p "${outPathways[$index]}"

./vina --receptor tauSLS.pdbqt --ligand "${ligandPathways[$index]}" --center_x 179.991 --center_y 178.728 --center_z 172.492 --size_x 19.1166666667 --size_y 20.3416666667 --size_z 31.35 --out "${outPathways[$index]}/${ligandNames[$index]}_docked.pdbqt"
