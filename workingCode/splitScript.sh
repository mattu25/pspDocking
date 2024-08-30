#!/bin/bash
#SBATCH --job-name=testJob
#SBATCH --time=05:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4

python3 vinaSplit1000.py
