import os
import pandas as pd

mol2Directory = ""
mol2FinalDirectory = ""

def makeMol2CSV():
    mol2DB = pd.DataFrame(columns=["Path", "Score_File", "Out"])
    for file in os.listdir(mol2Directory):
        if file.startswith(".") == False:
            mol2Path = os.path.join(mol2Directory, file)
            scoreFile = os.path.join(mol2Directory, str(file)[:6]+"_scores.txt")
            mol2UpdatedPath = os.path.join(mol2FinalDirectory, file)
            mol2Info = (mol2Path, scoreFile, mol2UpdatedPath)
            mol2DB.iloc[len(mol2DB)] = mol2Info

    mol2DB.to_csv("mol2Data.csv", index=False)
    return

