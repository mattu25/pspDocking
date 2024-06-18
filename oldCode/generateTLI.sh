#!/bin/bash
#SBATCH --job-name=testJob
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mail-user="matthew_unger@lifesci.ucsb.edu"
#SBATCH --mail-type=BEGIN,END,FAIL

python /home/maunger/testPSPDocking/TLI.py
