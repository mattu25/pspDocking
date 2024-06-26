import os
import subprocess as sp

# Important directories
trancheOutput = "/Users/mtmunger/Documents/lab/VinaRuns/06_17_24Run1/trancheOutput" 


# Task 1: Get rid of undocked ligand files
def removeLigandFiles():
    files = os.listdir(trancheOutput)
    for file in files:
        if "outFiles" not in str(file) and str(file).startswith(".") == False:
            os.chdir(os.path.join(trancheOutput, file))
            print(f"\nRemoving old files for {file}\n")
            sp.run("rm -r *", shell=True)
            #os.removedirs(os.path.join(trancheOutput, file))            
            print("\nComplete\n")
            os.chdir(trancheOutput)
    return

removeLigandFiles()

# Task 2: Bring all subtranches into a single tranche

# Task 3: Merge all .pdbqt into a single mol2 for that tranche