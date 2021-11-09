from pathlib import Path
import pandas as pd

homepath = str(Path.home())
print("The home path detected is {}.".format(homepath))

if r"C:\Users\jasonjia" in homepath:
    windows = True
    print("Detected Windows home path - using Jason's Dropbox folders")
    inputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ORBIS\Output\test") 
    outputfolder = Path(r"C:\Users\jasonjia\Dropbox\Projects\ORBIS\Output\test")
    
else:
    windows = False
    print("Assuming Mercury home path - using Mercury folders")
    inputfolder = Path(r"('/project/kh_mercury_1/OrbisRaw/DescriptiveDataDec")
    outputfolder = Path(r"('/project/kh_mercury_1/OrbisRaw/DescriptiveDataDec")

outputsuffix = ''

for txtfile in inputfolder.iterdir():
    filestem = txtfile.stem
    if txtfile.suffix == '':
        outputfile = filestem + outputsuffix + '.csv'
        outputpath = Path(outputfolder / outputfile)
        pd = pd.read_csv(txtfile, sep = '\t')
        pd.to_csv(outputpath, index = None)
        print("Converted to csv: {}".format(txtfile))