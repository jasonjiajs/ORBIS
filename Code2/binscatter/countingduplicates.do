use "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Dta\Final\Industry-Global_financials_and_ratios-USD-Interim_processed.dta" 

* BvDIDnumber Nationalindustryclassificationus Primarycodesinthisclassification Primarycodeinnationalindustrycla Secondarycodesinthisclassificati Secondarycodeinnationalindustryc NACERev2mainsection NACERev2Corecode4digits NACErev2corecodetextdescription NACERev2Primarycodes NACErev2primarycodetextdescripti NACERev2Secondarycodes NACErev2secondarycodetextdescrip NAICSCorecode4digits NAICScorecodetextdescription NAICSPrimarycodes NAICSPrimarycodestextdescription NAICSSecondarycodes NAICSSecondarycodestextdescripti USSICCorecode3digits USSICcorecodetextdescription USSICPrimarycodes USSICprimarycodetextdescription USSICSecondarycodes USSICsecondarycodetextdescriptio BvDmajorsector country_iso


* drop if missing(RDexpensesOperatingrevenue, Numberofemployees, Totalassets, Fixedassets, Intangiblefixedassets, Tangiblefixedassets, Otherfixedassets, Currentassets)

drop if missing(Nationalindustryclassificationus, Primarycodesinthisclassification, Primarycodeinnationalindustrycla, Secondarycodesinthisclassificati, Secondarycodeinnationalindustryc, NACERev2mainsection, NACErev2corecodetextdescription, NACERev2Primarycodes)
duplicates report BvDIDnumber
duplicates tag BvDIDnumber, gen(dup_id)
* drop if dup_id ==0

generate order = _n
sort BvDID order
by BvDID: gen y = _n == 1 
sort order
replace y = sum(y)
drop order
list BvDID y


use "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Dta\Final\Industry_classifications_processed.dta"
