import os
import subprocess as sp

homeDirectory = ""
xaaDirectory = ""
dockedDirectory = ""

def removeFiles():
    undockedCompounds = []
    for file in os.listdir(xaaDirectory):
        subsetZero = file[:6] + "_subSet_000_outFiles"
        subsetFull = file[:6] + "_fullSet_outFiles"
        
        subsetZeroDirectory = os.path.join(dockedDirectory, subsetZero)
        subsetFullDirectory = os.path.join(dockedDirectory, subsetFull)

        if os.path.exists(subsetZeroDirectory) == False or os.path.exists(subsetFullDirectory) == False: 
            try:
                sp.run(f"rm -r {os.path.join(dockedDirectory, file[:6])}", shell=True)
            except FileNotFoundError:
                print(f"{file[:6]} does not exist in docked folder")
            
            undockedCompounds.append(file[:6])

    return undockedCompounds

def moveXAA(xaaToMove):
    os.chdir(homeDirectory)
    dockedXAAFolder = os.path.join(homeDirectory, "dockedXAA")
    os.makedirs(dockedXAAFolder, exist_ok=True)
    os.chdir(xaaDirectory)
    for file in os.listdir(xaaDirectory):
        if file[:6] in xaaToMove:
            sp.run(f"mv {file} {dockedXAAFolder}", shell=True)

def moveXAACorrection():
    trancheList = []
    for file in os.listdir(dockedDirectory):
        if file[:6] not in trancheList:
            trancheList.append(file[:6])

    os.chdir(homeDirectory)
    dockedXAAFolder = os.path.join(homeDirectory, "dockedXAA")
    os.chdir(xaaDirectory)
    for xaa in os.listdir(xaaDirectory):
        if xaa[:6] in trancheList:
            sp.run(f"mv {xaa} {dockedXAAFolder}", shell=True)



x = removeFiles()
print(len(x))
print("IJABMO" in x)
print("IJBARO" in x)
print("IJBBMM" in x)

#moveXAA(x)
moveXAACorrection()



