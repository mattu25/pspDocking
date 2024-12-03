import os
import subprocess as sp
import pandas as pd

'''
Function:
    Read through the ligand data csv to calculate the exact array sizes and indicies needed for 
    submitting the slurm script.
'''

# Directory where the folder for each tranche is. Will also double as base directory for subtranches
generalTrancheDirectory = "~/trancheOutput" 
submissionDirectory = "~/submissionScripts"

# Step 1: Read in CSV, get information for each subtranche
ligandData = pd.read_csv(os.path.join(submissionDirectory, "ligandData.csv"))
grouped_ligandData = ligandData.groupby("SubTranche")

subTrancheInfo = []
batch = 0
for groupName, groupDF in grouped_ligandData:
    groupInfo = [groupName, groupDF.Index.min(), groupDF.Index.max(), batch] #Name, min index, max index
    subTrancheInfo.append(groupInfo)
    batch += 1
    
#print(subTrancheInfo)

# Step 2: 
for group in subTrancheInfo: 
    scriptOptions = f'''#!/bin/bash
#SBATCH --job-name=testJob
#SBATCH --time=0:15:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --array=1-{group[2]-group[1]+1}
#SBATCH --mail-user=""
#SBATCH --mail-type=BEGIN,END,FAIL

index=$((SLURM_ARRAY_TASK_ID + {group[1]-1}))
ligandCSV={os.path.join(submissionDirectory, "ligandData.csv")}
'''
    with open("submissionScript.sh", "r") as file:
        lines=file.readlines()

    lines[:12] = scriptOptions

    #print(lines)

    with open("submissionScript.sh", "w") as file:
        file.writelines(lines)
    
    activateScript = "chmod +x submissionScript.sh"
    sp.call(activateScript, shell=True)

    runCommand = "sbatch submissionScript.sh"
    sp.call(runCommand, shell=True) # Use this to run my sbatch command after I've updated the script
