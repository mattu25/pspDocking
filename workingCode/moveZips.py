import os
import subprocess as sp

directory = "/home/maunger/gninaScoring/pdbqtZips/trancheOutFiles"

for tranche in os.listdir(directory):
    filesDirectory = os.path.join(directory, tranche)
    for file in os.listdir(filesDirectory):
        if ".zip" in str(file):
            os.chdir(filesDirectory)
            move = f"mv {tranche}.zip /home/maunger/gninaScoring/pdbqtZips"
            sp.run(move, shell=True)
            
            
