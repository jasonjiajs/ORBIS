/*********************************************
This do file is to load all the txt files from outtxt
**********************************************/


* Set directory
local computer = 1    /* 1: Bill's computer   2: Your computer*/

if `computer' == 1 {
	local directory="C:\Users\stang10\Dropbox\data sample\outtxt"
} 
else {
	/* your directory here */
}


cd "`directory'"

local outputdir = "`directory'" + "\output_data"

* get a list of all txt files
local fn: dir . files "*.txt"


* set a local for file_count
local file_count = 0


foreach file_name of local fn {
	import delimited "`file_name'", delimiter(tab) varnames(nonames) encoding(UTF-8) clear
	ren v1 year
	ren v2 month
	ren v3 country_district
	ren v4 country_district_notes
	ren v5 position
	ren v6 politician
	ren v7 ref_track
	
	local file_count = `file_count'+1
	
	* save tempfile for appending 
	tempfile data_`file_count'
	save `data_`file_count''	
}

use `data_1', clear

forval t = 2(1)`file_count' {
	append using `data_`t'', force
}

* save country note for reference
preserve
keep if ref_track == -1
drop ref_track position politician
save "`outputdir'\country_district_note.dta",replace
restore

* save main data set
drop if ref_track == -1
drop country_district_notes
save "`outputdir'\chief_state_0119.dta",replace



* Read position data
import delimited "record_file\record.txt", delimiter(tab) varnames(nonames) encoding(UTF-8) clear

ren v1 year
ren v2 month
ren v3 country_district
ren v4 no_position

save "`outputdir'\position_record.dta",replace
