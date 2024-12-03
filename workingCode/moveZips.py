import os
import subprocess as sp

directory = ""

for tranche in os.listdir(directory):
    filesDirectory = os.path.join(directory, tranche)
    for file in os.listdir(filesDirectory):
        if ".zip" in str(file):
            os.chdir(filesDirectory)
            move = f"mv {tranche}.zip [target directory]"
            sp.run(move, shell=True)
            
            
