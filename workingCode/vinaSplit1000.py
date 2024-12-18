import os
import subprocess as sp
import pandas as pd

'''
Function:
    1. Split all tranches in trancheXAA directory into subtranches containing no more than 1000 compounds
    2. Move original XAA file (the file that was split) into splitXAAOriginal so it isn't in the way
    3. Write a csv file with paths to all ligands so a SLURM script can easily iterate over the files
'''

# Configure directories (need to specify paths for each, file names just given)
trancheXAAOrigin = "~/trancheXAA"
trancheOutput = "~/trancheOutput"
trancheXAAOut = "~/splitXAAOriginal"
vinaPathway = '~/bin'
ldOutputDirectory = "~/submissionScripts"

# Define function to split tranches into subtranches
def splitTranches():
    baseCommandSplit = f"{vinaPathway}/vina_split"
    for file in os.listdir(trancheXAAOrigin):
        if file.endswith(".pdbqt") == True:
            trancheFilePath = os.path.join(trancheOutput, str(file)[:6])
            os.mkdir(trancheFilePath) # Make new directory within output folder for this tranche
            
            old_file_path = os.path.join(trancheXAAOrigin, file) # Establish current path of tranche
            new_file_path = os.path.join(trancheFilePath, file) # Establish new path for tranche
            os.replace(old_file_path, new_file_path) # Move the tranche to the new directory

            split = " ".join([baseCommandSplit, "--input", new_file_path])
            sp.call(split, shell=True) # Call vina split

            os.chdir(trancheFilePath)
            currentDirList = os.listdir(trancheFilePath)
            if len(currentDirList) > 999: 
                subLists = []
                currentDirList.remove(str(file))
                for i in range(0, len(currentDirList), 1000):
                    x = currentDirList[i:i + 1000]
                    print(len(x))
                    subLists.append(x)

                for i, sublist in enumerate(subLists):
                    subsetValue = "00"+str(i)
                    if i >= 10: # if i is greater than 10, we can rewrite it to keep it within the character limit
                        subsetValue = "0"+str(i)  
                    elif i >= 100: 
                        subsetValue = str(i)  

                    newsublistPathway = os.path.join(trancheFilePath, str(file)[:6]+"_subSet_"+subsetValue)
                    os.mkdir(newsublistPathway)
                    for compound in sublist:
                        oldCompoundPathway = os.path.join(trancheFilePath, compound)
                        newCompoundPathway = os.path.join(newsublistPathway, compound)
                        os.replace(oldCompoundPathway, newCompoundPathway)
        
            finalXAAPath = os.path.join(trancheXAAOut, file) 
            os.replace(new_file_path, finalXAAPath)

# Define function to write the csv file
def writeLigandData():
    trancheLigandDB = pd.DataFrame(columns=["Index", "SubTranche", "LigandPath", "LigandName", "OutDirectory"])
    n = 1
    for root, dirs, files in os.walk(trancheOutput):
        for file in files:
            if file.startswith(".") == False:
                ligandPath = os.path.join(root, file)
                ligandName = str(file)[:-6]
                subTranche = str(root)[-17:]
                
                if "subSet" in subTranche: # See if there is a subset, if so, then we can just use subTranche from above
                    outDirectory = os.path.join(trancheOutput, subTranche+"_outFiles")

                else: # If no subset, then we need the full file name to represent the output directory
                    subTranche = str(root)[-6:]+"_fullSet"
                    outDirectory = os.path.join(trancheOutput, subTranche+"_outFiles")
            
                fileTuple = (n, subTranche, ligandPath, ligandName, outDirectory)
                trancheLigandDB.loc[len(trancheLigandDB)] = fileTuple
                n += 1
    
    outFilePath = os.path.join(ldOutputDirectory, "ligandData.csv")
    trancheLigandDB.to_csv(outFilePath, index=False)

# Function calls
splitTranches()
writeLigandData()