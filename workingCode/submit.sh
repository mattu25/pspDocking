#!/bin/bash
#SBATCH --job-name=testJob
#SBATCH --time=8:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

python3 submitJobs.py
