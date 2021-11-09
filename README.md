# ORBIS
Extracting German firm info from ORBIS (Samuel taking over, Jason handing over)

**Task:**
Kilian Huber  1:45 PM
Hi @Jason Jia, I have shared with you a Box folder called "BvD Firm Data." There is a subfolder called "Orbis." Into this folder, please copy an Orbis file containing the following variables for all firms located in Germany (no other country). The file can be in CSV, Stata, or another file format.
- BvD ID
- Crefonumber (if available, should be similar to BvD ID)
- Firm name
- Industry code WZ2008 at 1-digit level
- Industry code WZ2008 at 3-digit level
- Industry code WZ2008 at 4-digit level
- Industry code US SIC - main and additional field
- Revenue 2010-2020
- Employment 2010 - 2020
- Zip code (also called PLZ in German)
- City name of location
- Country name
- Import share
- Export share

**Previous Work:**
- Compiling information and understanding the data 
- Progress made on downloading the datasets

**Steps (roughly)**
1. Extract the data from .rar to .txt.
2. Process .txt to .csv (or .dta)
3. Filter the different datasets for German firms and merge the datasets.
