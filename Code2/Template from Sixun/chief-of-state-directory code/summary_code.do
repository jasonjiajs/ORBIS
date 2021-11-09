** This code is used to summarize the data chief_state_0019 and position_record



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



** Figure 1, Figure 2: Time Trend of Country and District count, and Position count
use "`outputdir'\position_record.dta",clear

drop if no_position == 0

bysort year month: gen no_country_district = _N
bysort year month: egen total_position = sum(no_position)

drop country_district no_position

duplicates drop 

sort year month

* Period Indicator
gen period = _n

* save a period set
preserve
keep year month period
save "`outputdir'\period.dta",replace
restore


tsset period

* Draw line plots
tsline no_country_district, xtitle("") xscale(noline) xlabel(none) ytitle("Country and District")


graph export "`outputdir'\co_dis_num.png", as(png) name("Graph") replace

tsline total_position, xtitle("") xscale(noline) xlabel(none) ytitle("Positions Count")

graph export "`outputdir'\posi_num.png", as(png) name("Graph") replace



** Table 1 Change between month and month   VERSUS    Change between year and year
**　Position and position matched
use "`outputdir'\chief_state_0119.dta", clear

merge m:1 year month using "`outputdir'\period.dta"
drop _merge


* Sort by country_district and position
sort country_district position period

* Generate an indicator if one position is also in the last month
by country_district position: gen exist_last_month = (period[_n-1]==period-1)
replace exist_last_month = . if period==1

by country_district position: gen change_last_month = (politician[_n-1]!=politician) if exist_last_month == 1


* Now consider the change in one year
sort country_district position month year
by country_district position month: gen exist_last_year = (year[_n-1]==year-1)
replace exist_last_year = . if year==2001
by country_district position month: gen change_last_year = (politician[_n-1]!=politician) if exist_last_year == 1


eststo clear

* Now generate the monthly change data
* The ratio of position remaining between month and the change in politician
preserve
bysort year month: gen total_position = _N
bysort year month: egen total_hold = sum(exist_last_month)

replace total_hold = . if total_hold == 0
bysort year month: egen total_change = sum(change_last_month)
gen hold_ratio = total_hold / total_position
gen change_ratio = total_change / total_hold
duplicates drop year month, force

eststo month_change: qui estpost summarize hold_ratio change_ratio

restore


* Now generate the yearly change data
* Note that I do this for multiple times each year, i.e., 2002 Jan VS 2001 Jan; 2002 Feb VS 2001 Feb
preserve
bysort month year: gen total_position = _N
bysort month year: egen total_hold = sum(exist_last_year)

replace total_hold = . if total_hold == 0
bysort month year: egen total_change = sum(change_last_year)
gen hold_ratio = total_hold / total_position
gen change_ratio = total_change / total_hold
duplicates drop year month, force

eststo year_change: qui estpost summarize hold_ratio change_ratio

restore

esttab using "`outputdir'\table1.tex", cells("mean sd") label nonumbers mtitles("Monthly_Change" "Year_Change") booktabs title(Summary Table\label{tab1}}) replace





