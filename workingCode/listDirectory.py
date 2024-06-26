import os
import subprocess as sp
import pandas as pd


unmodifiedDirectory = "~/tranches" #Directory where tranches are stored
directory = "/Users/mtmunger/Documents/lab/trancheOutput" #D
dockedDirectory = ""

def makeTrancheCSV():
    directoryDF = pd.DataFrame(columns=["Index", "Tranche", "Status"])
    n = 1
    for direc in os.listdir(unmodifiedDirectory):
        if direc.startswith(".") == False and str(direc)[:6]!= "select": 
            tranche = str(direc)[:6]
            trancheInfoTuple = (n, tranche, "")
            directoryDF.loc[len(directoryDF)] = trancheInfoTuple
            n += 1 

    directoryDF.to_csv("/Users/mtmunger/Documents/lab/trancheList.csv", index=False)
    return

def checkCompletedTranches():
    trancheDF = pd.read_csv("/Users/mtmunger/Documents/lab/trancheList.csv")
    directoryList = os.listdir(directory)

    trancheDF["Status"] = trancheDF["Status"].astype(str)
    completeTranches = []
    for tranche in directoryList:
        if tranche.startswith(".") == False:
            completeTranches.append(tranche[:6])

    trancheDF.loc[trancheDF["Tranche"].isin(completeTranches), "Status"] = "Complete"

    trancheDF.to_csv("/Users/mtmunger/Documents/lab/trancheList.csv", index=False)
    return

def organizeDirectory():
    trancheDF = pd.read_csv("/Users/mtmunger/Documents/lab/trancheList.csv")
    directoryList = os.listdir(directory)

    for i in len(range(trancheDF)):
        if trancheDF["Status"].iloc[i] == "Complete":
            trancheName = str(trancheDF["Tranche"].iloc[i])
            fileName = trancheName+".xaa.pdbqt"
            currentPath = os.path.join(directory, fileName)
            updatedPath = os.path.join(dockedDirectory, fileName)
            move = " ".join(["mv", currentPath, updatedPath])
            sp.call(move, shell=True)


#makeTrancheCSV()
checkCompletedTranches()