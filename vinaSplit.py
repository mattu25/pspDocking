import os

'''
I forgot vina_split could do everything we wanted, so I've now just written a script that can run vina split
on all files in a directory. 
'''

ligandDirectory = '/Users/mtmunger/Documents/Lab/test'
vinaPathway = '/Users/mtmunger/Documents/Lab/proteinDesign/Autodock_Vina/autodock_vina_1_1_2_mac_catalina_64bit/bin'

def vinaSplit():
    baseCommandSplit = "./vina_split"
    files = [f for f in os.listdir(ligandDirectory) if f.startswith(".") == False]
    for filename in files:
        file_path = os.path.join(ligandDirectory, filename)
        if os.path.isfile(file_path):
            outFolder = filename[:len(filename)-10] + "_PDBQT_Files" 
            new_directory = os.path.join(ligandDirectory, outFolder)
            os.mkdir(new_directory) # Create a new directory to put all ligand files into

            new_file = os.path.join(new_directory, filename)
            os.replace(file_path, new_file) # Move pdbqt file that's about to be parsed into new directory
            
            split = " ".join([baseCommandSplit, "--input", new_file]) # Define split command

            os.chdir(vinaPathway)
            os.system(split)


def vinaDock():
    baseCommandDock = "./vina"
    pass