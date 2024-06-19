import os
import pandas as pd

directory = "/Users/mtmunger/Documents/lab/tranches"

def makeTrancheCSV():
    directoryDF = pd.DataFrame(columns=["Index", "Tranche", "Status"])
    n = 1
    for direc in os.listdir(directory):
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


#makeTrancheCSV()
checkCompletedTranches()