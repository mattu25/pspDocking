import os

trancheDirectory = ""

os.chdir(trancheDirectory)
for file in os.listdir(trancheDirectory):
    if len(file) > 6:
        os.makedirs(file[:6], exist_ok=True)

