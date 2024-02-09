import os
import sys
import pandas as pd
import timeit

'''
Tranche-Ligand Index will take all our tranche folders from using vinaSplit.py, go through the ligands, and finally 
read out all the ligand names and tranches into a CSV file.
'''

# Directory with tranches
trancheFolder = "/Users/mtmunger/Documents/Lab/testSimple" #Where all the tranches you want to index are
outPutDirectory = "/Users/mtmunger/Documents/Lab"
trancheLigandDB = pd.DataFrame(columns=["Index", "Tranche", "Ligand"])

def getTrancheLigand():

    trancheList = (tranche for tranche in os.listdir(trancheFolder) if tranche.startswith(".") == False)
    tranchePaths = (os.path.join(trancheFolder, x) for x in trancheList)
    
    ligands = [os.listdir(path) for path in tranchePaths]

    ligandTuple = (l[11:-6] for ligandList in ligands for l in ligandList)
    trancheLigandDB.Ligand = tuple(ligandTuple)

    trancheTuple = (t[:6] for ligandList in ligands for t in ligandList)
    trancheLigandDB.Tranche = tuple(trancheTuple)

    trancheLigandDB.Index = tuple(range(1,len(trancheLigandDB.Ligand)+1))

    outFilePath = os.path.join(outPutDirectory, "trancheLigandData.csv")
    trancheLigandDB.to_csv(outFilePath, index=False)

getTrancheLigand()

