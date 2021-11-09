clear

use "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Dta\Final\Industry-Global_financials_and_ratios-USD-Interim-2019_processed.dta" 

gsort BvDIDnumber -Closingdate
quietly by BvDIDnumber:  gen dup = cond(_N==1,0,_n)

tabulate dup
drop if dup>1

merge 1:1 BvDIDnumber using Trade_description_processed

drop if _merge!=3
drop _merge

save global_mergedwith_trade, replace

//

clear

use Industry_classifications_processed
sort BvDIDnumber, stable
quietly by BvDIDnumber:  gen dup = cond(_N==1,0,_n)
tabulate dup
drop if dup>1

save industry_dupremoved, replace



//

clear

use global_mergedwith_trade

merge 1:1 BvDIDnumber using industry_dupremoved

drop if _merge!=3
drop _merge
save global_mergedwith_trade_and_industry, replace
