import os
import sys

ligandDirectory = '/home/maunger/testPSPDocking/tranches'
vinaPathway = '/home/maunger/softwares/autodock_vina_1_1_2_linux_x86/bin'

def vinaSplit():
	baseCommandSplit = "./vina_split"
	files = [f for f in os.listdir(ligandDirectory) if f.startswith(".") == False]
	for filename in files:
		file_path = os.path.join(ligandDirectory, filename)
		if os.path.isfile(file_path):
			outFolder = filename[:len(filename)-10]
			new_directory = os.path.join(ligandDirectory, outFolder)
			os.mkdir(new_directory)
			new_file = os.path.join(new_directory, filename)
			os.replace(file_path, new_file)
			split = " ".join([baseCommandSplit, "--input", new_file])
			os.chdir(vinaPathway)
			os.system(split)
			move = " ".join(["mv", new_file,"/home/maunger/testPSPDocking/originalXAA"])
			os.system(move)

if __name__ == "__main__":
    functionCall = sys.argv[1] #The function I am calling is the second argument of what I am writting in terminal
    try:
        getattr(sys.modules[__name__], functionCall)() #return value of named object
    except AttributeError:
        print("Invalid or Non-Existant Function")
 
        