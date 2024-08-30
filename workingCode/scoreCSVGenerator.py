import os
import pandas as pd
import numpy as np
import subprocess as sp
from openbabel import openbabel # type: ignore

scoreDirectory = "/home/maunger/gninaScoring/completeScores"
pdbqtDirectory = "/home/maunger/gninaScoring/pdbqtZips"
submitDirectory = "/home/maunger/gninaScoring/scripts"

scoreDirectoryFiles = [l for l in os.listdir(scoreDirectory) if l.startswith(".") == False]

def generateScoreArray(ligandNumber, Affinity, CNNaffinity, CNNvariance, Intramolecular_energy):
    ligandNumber = ligandNumber[1:,:]
    Affinity = Affinity[1:,:]
    CNNaffinity = CNNaffinity[1:,:]
    CNNvariance = CNNvariance[1:,:]
    Intramolecular_energy = Intramolecular_energy[1:,:]

    maxCNNaffinity = np.max(CNNaffinity, axis=1)
    poseIndexes = np.argmax(CNNaffinity, axis=1)

    maxCNNaffinityReshaped = np.reshape(maxCNNaffinity, (len(poseIndexes), 1))
    poseAffinity = np.reshape(Affinity[np.arange(len(poseIndexes)), poseIndexes], (len(poseIndexes), 1))
    poseCNNvariance = np.reshape(CNNvariance[np.arange(len(poseIndexes)), poseIndexes], (len(poseIndexes), 1))
    poseIntramolecular_energy = np.reshape(Intramolecular_energy[np.arange(len(poseIndexes)), poseIndexes],(len(poseIndexes), 1) )

    poseLigandNumber = np.reshape(ligandNumber[np.arange(len(poseIndexes)), poseIndexes], (len(poseIndexes), 1))
    poseLigandNumber = poseLigandNumber.astype(int)

    poseNumbers = np.reshape(poseIndexes, (-1,1))

    maxCompoundArray = np.concatenate((poseLigandNumber, poseNumbers, maxCNNaffinityReshaped, poseAffinity, poseCNNvariance, poseIntramolecular_energy), axis=1)
    nonzero_rows = np.any(maxCompoundArray != 0, axis=1)
    filteredCompoundData = maxCompoundArray[nonzero_rows]
    filteredCompoundData[:,1] = filteredCompoundData[:,1] + 1

    return filteredCompoundData

def unZip(pdbqtDirectory, tranche):
    pathToZip = os.path.join(pdbqtDirectory, tranche+".zip")
    potentialFile = os.path.join(pdbqtDirectory, tranche+"pdbqtFilesDocked")
    if os.path.exists(pathToZip) == True:
        os.chdir(pdbqtDirectory)
        command = f"unzip {pathToZip}"
        try: 
            sp.run(command, shell=True)
            roots = []
            dirsList = []
            filesList = []
            for root, dirs, files in os.walk(os.path.join(pdbqtDirectory, "anvil")):
                roots.append(root)
                dirsList.append(dirs)
                filesList.append(files)
            zippedPath = os.path.join("anvil",(dirsList[0][0]), (dirsList[1][0]), (dirsList[2][0]), (dirsList[3][0]), (dirsList[4][0]), (dirsList[5][0]))
            destinationDirectory = os.path.join(pdbqtDirectory,dirsList[5][0])

            if os.path.exists(destinationDirectory) == False or os.listdir(destinationDirectory) == []:
                os.mkdir(destinationDirectory)
                os.chdir(os.path.join(pdbqtDirectory, zippedPath))
                moveCommand = f"mv *.pdbqt {os.path.join(pdbqtDirectory, dirsList[5][0])}"
                sp.run(moveCommand, shell=True)
                os.chdir(pdbqtDirectory)
                sp.run("rm -r anvil", shell=True)
                sp.run(f"rm {tranche}.zip", shell=True)
                return destinationDirectory
            
            else:
                print(f"Skipping {tranche}, new directory is not empty or already exists")

        except FileNotFoundError:
            print(f"Skipping {tranche}, no zip file present and no correpsonding files")
            return False
        
    elif os.path.exists(potentialFile) == True and os.path.exists(pathToZip) == False:
        print("Proceeding")
        return potentialFile
    
    else:
        print(f"Skipping {tranche}, no zip file present and no correpsonding files")
        return False

def reZip(pdbqtDirectory, tranche):
    file = os.path.join(pdbqtDirectory, tranche+"pdbqtFilesDocked")
    os.chdir(pdbqtDirectory)
    command = f"zip -r {tranche}_out.zip {file}"
    sp.run(command, shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    os.chdir(file)
    sp.run("rm *", shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    os.chdir(pdbqtDirectory)

    return

def writeCompoundDB():

    if os.path.exists(os.path.join(submitDirectory, "scoreData.csv")):
        scoreData = pd.read_csv(os.path.join(submitDirectory, "scoreData.csv"))
    else:
        scoreData = pd.DataFrame(columns=["Compound_Name",
                                        "File_Name",
                                        "Pose_Number", 
                                        "Affinity", 
                                        "CNNaffinity", 
                                        "CNNvariance", 
                                        "Intramolecular_energy",
                                        "SMILES"])
    
    for scoreFile in scoreDirectoryFiles:
        with open(os.path.join(scoreDirectory, scoreFile), "r") as file:
            fileLines = file.readlines()
        
        n = int(sum(1 for line in fileLines if "ZINC" in line)/9)
        compoundIndex = 0
        x = 0

        Affinity, CNNaffinity, CNNvariance, Intramolecular_energy, ligandNumber = [np.zeros((n+100,9)) for z in range(5)]
        
        compoundNames = []
        for i in range(len(fileLines)):
            if "ZINC" in fileLines[i]:
                if fileLines[i][:20] == fileLines[i-7][:20]:
                    x += 1
                    if x >= 9:
                        compoundIndex += 1
                        compoundNames.append(fileLines[i][2:19])
                        x = 0

                    ligandNumber[compoundIndex, x] = compoundIndex
                    Affinity[compoundIndex, x] = float((fileLines[i-6].split(" "))[1])
                    CNNaffinity[compoundIndex, x] = float((fileLines[i-4].split(" "))[1])
                    CNNvariance[compoundIndex, x] = float((fileLines[i-3].split(" "))[1])
                    Intramolecular_energy[compoundIndex, x] = float((fileLines[i-2].split(" "))[2])

                else:
                    compoundIndex += 1

                    compoundNames.append(fileLines[i][2:19])
                    ligandNumber[compoundIndex, 0] = int(compoundIndex)
                    Affinity[compoundIndex, 0] = float((fileLines[i-6].split(" "))[1])
                    CNNaffinity[compoundIndex, 0] = float((fileLines[i-4].split(" "))[1])
                    CNNvariance[compoundIndex, 0] = float((fileLines[i-3].split(" "))[1])
                    Intramolecular_energy[compoundIndex, 0] = float((fileLines[i-2].split(" "))[2])
                
                    x = 0

        trancheScoreData = generateScoreArray(ligandNumber, Affinity, CNNaffinity, CNNvariance, Intramolecular_energy)
        
        # Find Ligand names:
        ligandNames = []
        for ligandNumber in trancheScoreData[:,0]:
            if ligandNumber < 10:
                number = "000"+str(ligandNumber).split(".")[0]
            elif ligandNumber < 100:
                number = "00"+str(ligandNumber).split(".")[0]
            elif ligandNumber < 1000:
                number = "0"+str(ligandNumber).split(".")[0]
            elif ligandNumber < 10000:
                number = str(ligandNumber).split(".")[0]
            
            compound = str(scoreFile[:6])+f".xaa_ligand_{number}_docked.pdbqt"
            ligandNames.append(compound)

        smilesInfo = []
        for i in range(len(ligandNames)):
            tranche = str(ligandNames[i])[:6]+"pdbqtFilesDocked"
            file = ligandNames[i]
            compound = compoundNames[i]
            pose = trancheScoreData[i,1]
            
            tranchePath = unZip(pdbqtDirectory, tranche[:6])
            if tranchePath == False:
                continue

            filePath = os.path.join(tranchePath, file)
          
            # Open mol2 file
            try:
                with open(filePath, "r") as pdbqt:
                    pdbqtLines = pdbqt.readlines()
            
                    model = f"MODEL {int(pose)}"
                    startIndex = 0
                    endIndex = 0
                    for j in range(len(pdbqtLines)):
                        line = pdbqtLines[j].strip()
                        if line.startswith(model):
                            startIndex = j
                        elif line.startswith("ENDMDL"):
                            endIndex = j+1
                            break

                    poseData = "".join(pdbqtLines[startIndex:endIndex])

                    obConversion = openbabel.OBConversion()
                    obConversion.SetInAndOutFormats("pdbqt", "smi")

                    mol = openbabel.OBMol()
                    obConversion.ReadString(mol, poseData)

                    smiles = obConversion.WriteString(mol)
                    smilesInfo.append(smiles[:-17])

            except FileNotFoundError:
                smilesInfo.append("No SMILES Found")

        reZip(pdbqtDirectory, tranche[:6])

        temporaryDf = pd.DataFrame(columns=["Compound_Name",
                                            "File_Name",
                                            "Pose_Number", 
                                            "Affinity", 
                                            "CNNaffinity", 
                                            "CNNvariance", 
                                            "Intramolecular_energy",
                                            "SMILES"])
        
        temporaryDf["Compound_Name"] = compoundNames
        temporaryDf["File_Name"] = ligandNames
        temporaryDf["Pose_Number"] = trancheScoreData[:,1]
        temporaryDf["Affinity"] = trancheScoreData[:,3]
        temporaryDf["CNNaffinity"] = trancheScoreData[:,2]
        temporaryDf["CNNvariance"] = trancheScoreData[:,4]
        temporaryDf["Intramolecular_energy"] = trancheScoreData[:,5]
        temporaryDf["SMILES"] = smilesInfo
        
        scoreData.reset_index(drop=True, inplace=True)
        temporaryDf.reset_index(drop=True, inplace=True)

        # Ensure temporaryDf has the same columns as scoreData
        temporaryDf = temporaryDf.reindex(columns=scoreData.columns)

        # Concatenate DataFrames
        scoreData = pd.concat([scoreData, temporaryDf], ignore_index=True)


    scoreData.to_csv("scoreData.csv", index=False)

    return

writeCompoundDB()
