import os
import subprocess as sp

# Important directories
trancheOutput = "" 

# Task 1: Get rid of undocked ligand files
def removeLigandFiles():
    directories = os.listdir(trancheOutput)
    for directory in directories:
        if "outFiles" not in str(directory) and str(directory).startswith(".") == False:
            targetDirectory = os.path.join(trancheOutput, directory)
            os.chdir(targetDirectory)
            for element in os.listdir(targetDirectory):
                if "docked" in element:
                    print(f"\n\n WARNING: Docked file detected in {directory}, halting removal!!!\n\n")
                    os.chdir(trancheOutput)
                    break
                elif "subSet" in element:    
                    sp.run(f"rm -r {element}", shell=True)
                else:     
                    sp.run(f"rm {element}", shell=True)
            os.chdir(trancheOutput)

    return 1

# Task 2: Bring all subtranches into a single tranche
def condensePDBQT():
    directories = os.listdir(trancheOutput)
    for directory in directories:
        if "outFiles" in str(directory) and str(directory).startswith(".") == False:
            tranche = str(directory)[:6]

            trancheDirectory = os.path.join(trancheOutput, tranche)
            ligandSubDirectory = os.path.join(trancheOutput, directory)

            os.chdir(ligandSubDirectory)
            for file in os.listdir(ligandSubDirectory):
                if ".pdbqt" in str(file):
                    currentLigandPath = os.path.join(ligandSubDirectory, file)
                    destinationPath = os.path.join(trancheDirectory, file)
                    os.replace(currentLigandPath, destinationPath)
    
            try:
                os.rmdir(os.path.join(trancheOutput, directory))
            except OSError:
                print("Directory not empty!")
          
    return 1

# Task 3: Confirm everything is set for merging:
def checkWork(remove = 0, condense = 0):
    if remove == 0 or condense == 0:
        print("\n\nPlease ensure you have run both the removal and the condense functions!\n\n")
        return 0

    directories = os.listdir(trancheOutput)
    nTranches=0
    for directory in directories:
        if str(directory).startswith(".") == False:
            nTranches +=1
            if len(str(directory))!= 6:
                print(f"{os.path.join(trancheOutput, directory)} is not 6 characters long")
                return 0 
            elif ".pdbqt" in directory:
                print(f"{os.path.join(trancheOutput, directory)} is a file")
                return 0
            
            n = 0
            for file in os.listdir(os.path.join(trancheOutput, directory)):
                if str(file).startswith(".") == False:
                    if ".pdbqt" not in file or "docked" not in file:
                        print(f"{os.path.join(trancheOutput, directory, file)} is either not a .pdbqt file or is not a docked file")
                        return 0 
                    n +=1

            print(f"{n} ligand files detected")    

    print(f"Checks complete, {nTranches} tranches recorded")   
    return 1


# Task 4: Merge all .pdbqt into a single mol2 for that tranche
def pdbqtToMol2(proceed = 0):
    if proceed == 0:
        print("Prerequisites not met, terminating...")
        return
    
    directories = os.listdir(trancheOutput) 
    for directory in directories:
        if str(directory).startswith(".") == False:
            os.chdir(os.path.join(trancheOutput, directory))
    
            outputFile = directory+"_Tranche_docked.mol2"
            #sp.run(f"obabel *.pdbqt -O {outputFile}",shell=True)
            result = sp.run(f"obabel *.pdbqt -O {outputFile}",shell=True, stdout=sp.PIPE, stderr=sp.PIPE, text=True)
            result.check_returncode()
            warning_message="=============================="
            warning_count=result.stderr.count(warning_message)
            print(f"Completed mol2 conversion for {directory} with {warning_count} warnings")
        
            os.mkdir(os.path.join(trancheOutput, directory, directory+"pdbqtFilesDocked"))
            pdbqtOutDirectory = str(directory)+"pdbqtFilesDocked"
            sp.run(f"mv *.pdbqt {os.path.join(trancheOutput, directory, pdbqtOutDirectory)}", shell=True)
            os.chdir(trancheOutput)

    return 

# Bonus: zip all pdbqts
def zipPDBQTS():
    directories = os.listdir(trancheOutput) 
    for directory in directories:
        if str(directory).startswith(".") == False:
            os.chdir(os.path.join(trancheOutput, directory))
            for file in os.listdir(os.path.join(trancheOutput, directory)):
                if str(file).startswith(".") == False and "pdbqtFilesDocked" in str(file):
                    command = f"zip -r {directory}.zip {os.path.join(trancheOutput, directory, file)}"
                    sp.run(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
                    os.chdir(os.path.join(trancheOutput, directory, file))
                    sp.run("rm *", shell=True)
                    sp.run(f"cd {os.path.join(trancheOutput, directory)}", shell=True)
                    sp.run(f"rmdir {os.path.join(trancheOutput, directory, file)}", shell=True)
            os.chdir(trancheOutput)

#removeValue = removeLigandFiles()
#condenseValue = condensePDBQT()   
#proceed = checkWork(removeValue, condenseValue)

#pdbqtToMol2(proceed)

zipPDBQTS()
