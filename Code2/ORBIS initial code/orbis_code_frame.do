/* =======================================================
This code serves to primarily clean ORBIS data from large txt files
======================================================== */

**** local some useful directory ****
local chunk_dir = "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Txt\chunky"
local dta_dir = "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Dta"
local raw_dir = "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Txt"


**** local files want to clean file_name ****
local files = "Bankers_current\Industry-Global_financials_and_ratios-USD-Globalfolder"
local final_file = "Industry-Global_financials_and_ratios-USD-Globalfolder_processed"


**** This is where we would put the chunky text files *****
cd "`chunk_dir'"  


**** Use chunky to analyze the basic text files at first glance ****

chunky using "`raw_dir'/`files'.txt", peek(50)

chunky using "`raw_dir'/`files'.txt", analyze

**** Now use chunky to split the large txt into small chunks which would be loaded into STATA ****

chunky using "`raw_dir'/`files'.txt", chunksize(100MB)


**** Run the loop inside the chunky files, and after open each chunk and save as dta, erase the file ****

local fn: dir . files "*.txt"


local chunk_num = 0



foreach file_name in `fn' {
        /*********************** 
        Step I: Load data using bindquote option, because some data may suffer from quote problems, save into intermediate data as dta, erase txt files
        ************************/
                import delimited "`file_name'", delimiter(tab) case(preserve) encoding(UTF-8) bindquote(nobind) stringcols(_all) clear
                local chunk_num = `chunk_num' + 1
                

                **** Note that only chunk1 contains variable names, so we would keep an empty file consisting only of variable names and after all the files are generated, erase the file.
                **** For chunk_num > 1 , append the chunk to this name first to get the ideal variable name
                if `chunk_num'==1 {
                        **** use local to store variable names and use to rename later files 
                        local var_num = 0
                        foreach var of varlist _all {
                                local var_num = `var_num' + 1
                                local var_name`var_num' = "`var'"
                        }
                }
                else {
                        **** rename variables ****
                        qui des
                        forval j=1(1)`r(k)' {
                                rename v`j' `var_name`j''
                        }
                }
                
               
                **** save intermediate data sets and erase raw chunk ****
                save "`dta_dir'/Intermediate/`final_file'_`chunk_num'", replace
                erase "`file_name'"
        
       
       
        /****************************
        Step II: This code chunk would be used to keep and clean the ideal data in each small chunk, which differs on demand.
         Note that some data sets are extremely big with many variables, as a result, we should try to drop unused variables when we feel that there is no use of such variables
        ****************************/ 
        gen country_iso = substr(BvDIDnumber,1,2)
        keep if country_iso == "DE"
        
        save "`dta_dir'/Intermediate/`final_file'_`chunk_num'", replace
        
        
        
        /***************************
        Step III: If the dta file is still too large after Step II to be append, use this step to split the files and save to each country file folder in the intermediate data set and then drop the large raw data
        ****************************/
        
        
        
        
}       



****************************** Now append all the data sets in the intermediate data (or in country sub-folders), and erase all the files in the intermediate **************************
clear

forval i=1(1)`chunk_num' {
        append using "`dta_dir'/Intermediate/`final_file'_`i'"
        erase "`dta_dir'/Intermediate/`final_file'_`i'.dta"
}

save "`dta_dir'/Final/`final_file'", replace








