import os
import subprocess as sp
import pandas as pd

def runGnina():
    mol2Data = pd.read_csv("~/mol2Data.csv")
    for i in range(len(mol2Data["Path"])):
        outFile = mol2Data['Score_File'].iloc[i]
        mol2 = mol2Data['Path'].iloc[i]
        command = f"apptainer exec --nv [path to gnina] --score_only -r tauSLS.pdqbt -l {mol2}"
        sp.run(command, shell=True)

        newMol2Dir = mol2Data['Out'].iloc[i]
        os.replace(mol2, newMol2Dir)
    return

runGnina()
