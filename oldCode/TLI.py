import os
import sys
import pandas as pd
import timeit

'''
Tranche-Ligand Index will take all our tranche folders from using vinaSplit.py, go through the ligands, and finally 
read out all the ligand names and tranches into a CSV file.
'''

ligandBaseDir = "/home/maunger/testPSPDocking/tranches" 
outPutDirectory = "/home/maunger/testPSPDocking"
trancheLigandDB = pd.DataFrame(columns=["Index", "TranchePath", "LigandPath", "LigandName", "OutDirectory"])

def getTrancheLigand():

    trancheList = (tranche for tranche in os.listdir(ligandBaseDir) if tranche.startswith(".") == False)
    tranchePaths = [os.path.join(ligandBaseDir, x) for x in trancheList]
    ligands = [os.listdir(path) for path in tranchePaths]
    
    trancheTuple = [t[:6] for ligandList in ligands for t in ligandList]
    tranchePathList = [os.path.join(ligandBaseDir, t) for t in trancheTuple]
    trancheLigandDB.TranchePath=tranchePathList

    ligandList = [l for ligandList in ligands for l in ligandList] 
    ligandPathList = [os.path.join(ligandBaseDir, str(l[:6]), l) for l in ligandList]
    trancheLigandDB.LigandPath = ligandPathList
    trancheLigandDB.LigandName = ligandList

    outDirectories = [os.path.join(ligandBaseDir, str(t[:6]+"_outFiles")) for ligandList in ligands for t in ligandList]
    trancheLigandDB.OutDirectory = outDirectories

    trancheLigandDB.Index = tuple(range(1,len(trancheLigandDB.LigandName)+1))

    outFilePath = os.path.join(outPutDirectory, "trancheLigandData.csv")
    trancheLigandDB.to_csv(outFilePath, index=False)

getTrancheLigand()
 
