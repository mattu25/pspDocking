import os
import sys

'''
This script is supposed to be how we can extract the information from the grid parameter file and put it into
a format that can be easily read and turned into a vina call. 
'''

pathway = '/Users/mtmunger/Documents/Lab/proteinDesign'

def getVinaParameters(filename):
    filePath = os.path.join(pathway, filename)
    with open(filePath, 'r') as gridFile:
        information = gridFile.readlines()
    gridFile.close()

    #Pull key information from lines
    points, spacing, center = [information[i] for i in [0, 2, 6]]

    # Unpack elements into objects that can be saved in txt
    points = points.split(sep = " ")[1:4]
    spacing = float(spacing.split(sep = " ")[1])
    center = center.split(sep = " ")[1:4]

    for val in range(len(points)):
        points[val] = float(points[val]) * spacing
    
    center = [float(x) for x in center] #Convert all center values to floats

    keyInfo = [points, center]

    newFile = os.path.join(pathway, "dockingParameters.txt")
    with open(newFile, "w") as outFile:
        for value in keyInfo:
            outFile.write(f"{value}\n")
    outFile.close()

if __name__ == "__main__":
    functionCall = sys.argv[1] #The function I am calling is the second argument of what I am writting in terminal
    if len(sys.argv) < 3:
        print("Insufficient Arguments")
    else:
        function_name = sys.argv[1]
        argument1 = sys.argv[2]

        try:
            function = getattr(sys.modules[__name__], function_name)
            function(filename=argument1) #return value of named object
        
        except AttributeError:
            print("Invalid or Non-Existant Function")