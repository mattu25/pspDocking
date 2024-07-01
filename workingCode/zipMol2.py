import os
import subprocess as sp

dockedTrancheDirectory = "/anvil/projects/x-mca05s027/Matthews_work/trancheOutFiles"
def zipMol2():
    tranches = os.listdir(dockedTrancheDirectory)
    mol2Directory = os.path.join(dockedTrancheDirectory,"mol2Compressed")
    os.mkdir(mol2Directory)
    for tranche in tranches:
        if str(tranche).startswith(".") == False:
            for file in os.listdir(os.path.join(dockedTrancheDirectory, tranche)):
                if ".mol2" in str(file):
                    command = f"cp {os.path.join(dockedTrancheDirectory, tranche, file)} {mol2Directory}"
                    sp.run(command, shell=True)

    os.chdir(mol2Directory)
    sp.run("zip mol2Files.zip *.mol2", shell=True)
    sp.run("rm *.mol2", shell=True)

zipMol2()