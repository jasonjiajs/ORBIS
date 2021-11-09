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
- Progress made on downloading the datasets. The previous RP did it using chunky on Stata, and I've tried that. It works but takes a long time + is buggy, probably because it's based on a Stata package. The way I was exploring was: to 1) unzip the file and extract the .txt files on Mercury, 2) split it into smaller chunks, 3) convert it in .csv, 4) do filtering and merging, and 5) compile it all together.
- To unzip files: I installed 7z on Mercury, because Mercury doesn't by itself have any unzipping program. Consider the following codes to download 7z, given by Ernesto Vargas, a Data Scientist at Booth:

```
# create new folder
mkdir -p ~/Software/p7zip

# navigate to new folder
cd ~/Software/p7zip

# download file
wget https://sourceforge.net/projects/p7zip/files/p7zip/16.02/p7zip_16.02_x86_linux_bin.tar.bz2/download

# unzip file - make sure you're in a compute node before doing this.
tar -xvjf download

# show p7zip help page
~/Software/p7zip/p7zip_16.02/bin/7z

# extract .rar file
~/Software/p7zip/p7zip_16.02/bin/7z x file.rar
```

- To extract files, consider the following codes (from my own experimentation):

```
~/Software/p7zip/p7zip_16.02/bin/7z x /home/jasonjia/testfile.rar3.rar
~/Software/p7zip/p7zip_16.02/bin/7z x /home/jasonjia/testfor7z/  -o/home/jasonjia
~/Software/p7zip/p7zip_16.02/bin/7z x /project/FMC_Data/Orbis_Historical/Descriptive\ data\ Dec\ text/  -o/project/kh_mercury_1/OrbisRaw/
```

- To split files, consider the following codes (from my own experimentation):

```
split -l 100000 --verbose BvD_ID_and_Name.txt BvD_ID_and_Name_
split -l 100000 -a 5 -d --verbose All_addresses.txt All_addresses_
```

- Some other codes (from Ernesto):

"Alternatively, you can use your ~/.bash_profile to create an alias, or to add the folder to your path. Either approach allows you to use the `7z` command outside of the directory where you installed it. For example, you can add the line:
```
alias 7z=/home/jasonjia/Software/p7zip/p7zip_16.02/bin/7z
```
OR, you can add the following line to add the install directory to your PATH:
```
PATH=/home/jasonjia/Software/p7zip/p7zip_16.02/bin:${PATH}
```
In either case, you can then simply use the `7z` command from anywhere. Note that after editing your ~/.bash_profile, you will have to log out and log back in once so that the changes take effect."


**Steps (roughly)**
1. Extract the data from .rar to .txt.
2. Process .txt to .csv (or .dta)
3. Filter the different datasets for German firms and merge the datasets.
