import os
import sys
import pandas as pd

trancheFolder = "/home/maunger/testPSPDocking/tranches" 
outPutDirectory = "/home/maunger/testPSPDocking"

ligandData = pd.read_csv(os.path.join(outPutDirectory, "trancheLigandData.csv"))

