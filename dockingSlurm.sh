#!/bin/bash
#SBATCH --job-name=testJob
#SBATCH --time=08:00:00
#SBATCH --nodes=5
#SBATCH --cpus-per-task=1
#SBATCH --array=1-194
#SBATCH --mail-user="matthew_unger@lifesci.ucsb.edu"
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=/home/maunger/testPSPDocking/tranches/slurmOut

export PATH="/home/maunger/softwares/autodock_vina_1_1_2_linux_x86/bin:$PATH"

ligandBaseDir="/home/maunger/testPSPDocking/tranches"

ligandCSV="/home/maunger/testPSPDocking/trancheLigandData.csv"
length=$(tail -n 1 "$ligandCSV" | cut -d "," -f 1)

nodes=$(($length / 40))

index=${SLURM_ARRAY_TASK_ID}

while IFS=, read -r idx tranche ligand; do
	if [[ $index -eq $idx ]]; then
		trancheName=$(echo "$tranche")
		ligandName=$(echo "$ligand")
		ligandPath="$ligandBaseDir/$trancheName/$ligandName"
		outPath="$ligandBaseDir/${trancheName}_outFiles"
		mkdir -p "$outPath"
		
		vina --receptor /home/maunger/testPSPDocking/tauSLS.pdbqt --ligand "$ligandPath" --center_x 179.991 --center_y 178.728 --center_z 172.492 --size_x 19.1166666667 --size_y 20.3416666667 --size_z 31.35 --out "$outPath/${ligandName%.*}_docked.pdbqt"
		
		break
	fi
done < "$ligandCSV"


