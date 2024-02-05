import os 
import chardet

'''
This is a script to take in the large PDBQT files and parse them out into individual ligands. 
Chardet seems to have some issues (something with the import), not exactly sure, but I can 
always hard-code in the encoding. 

I'm creating a shell script to go with this so we can just execute that and it will unpack
the ZINC files, then have this read them and break them out into all our ligands. 


* The ZINC pdbqt files are encoded in:

Windows-1252
ascii
'''

pathway = '/Users/mtmunger/Documents/Lab/test' #Will need to change on POD

def readFiles(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as decode:
                contentBytes = decode.read()
            fileEncoding = chardet.detect(contentBytes)['encoding']
            decode.close()

            outFolder = filename + "_ligands"
            outDirectory = os.path.join(pathway, outFolder)
            os.makedirs(outDirectory, exist_ok=True)
            
            with open(file_path, 'r', encoding=fileEncoding) as inFile:
                findMolecules(inFile, outDirectory)
            inFile.close()
         
def findMolecules(file, outputDirectory = pathway):
    content = file.readlines()
    end = False
    outList = []
    for lineIndex in range(len(content)):
        if content[lineIndex].startswith("MODEL"):
            name = str(content[lineIndex + 1])
        elif content[lineIndex].startswith("ENDMDL"):
            end = True
        outList.append(content[lineIndex])

        if end == True:
            ligandFileName = name[15:]
            ligandFileName = ligandFileName.strip() + ".pdbqt"
            outDir = os.path.join(outputDirectory, ligandFileName)
            with open(outDir, 'w') as outFile:
                outFile.writelines(outList)
            outFile.close()
            outList = []
            end = False

readFiles(pathway)