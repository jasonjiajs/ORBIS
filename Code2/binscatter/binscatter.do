clear
use "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Dta\Final\Industry-Global_financials_and_ratios-USD-Interim_processed.dta" 
gen missingRD=1 if missing(RD)
replace missingRD=0 if !missing(RD)

destring(Totalassets), replace
histogram Totalassets, discrete

egen Totalassetsgroup = cut(Totalassets), group(20) label
mean missingRD, over(Totalassetsgroup)

ssc install binscatter
gen log10Totalassets = log10(Totalassets)
binscatter missingRD log10Totalassets, nquantiles(100) line(none) savegraph("C:\Users\jasonjia\Dropbox\ORBIS\Output\missingRD_Totalassets100bins.jpg") replace

binscatter missingRD log10Totalassets, nquantiles(20) line(none) savegraph("C:\Users\jasonjia\Dropbox\ORBIS\Output\missingRD_Totalassets20bins.jpg") replace

//
clear

use "C:\Users\jasonjia\Dropbox\ORBIS\Output\Firm_description\Dta\Final\global_mergedwith_trade_and_industry.dta"
gen missingRD=1 if missing(RD)
replace missingRD=0 if !missing(RD)

gen missingPrimarycode=1 if missing(Primarycodesinthisclassification)
replace missingPrimarycode=0 if !missing(Primarycodesinthisclassification)

gen missingSecondarycode=1 if missing(Secondarycodesinthisclassificati)
replace missingSecondarycode=0 if !missing(Secondarycodesinthisclassificati)

gen missingNACEmain=1 if missing(NACERev2mainsection)
replace missingNACEmain=0 if !missing(NACERev2mainsection)

gen missingNACEsecondary=1 if missing(NACERev2Secondarycodes)
replace missingNACEsecondary=0 if !missing(NACERev2Secondarycodes)

gen missingBvDmajorsector=1 if missing(BvDmajorsector)
replace missingBvDmajorsector=0 if !missing(BvDmajorsector)

gen missingPdts=1 if missing(Productsservices)
replace missingPdts=0 if !missing(Productsservices)

gen missingTradeDesc=1 if missing(TradedescriptionEnglish)
replace missingTradeDesc=0 if !missing(TradedescriptionEnglish)

destring Totalassets, replace
gen log10Totalassets = log10(Totalassets)

binscatter missingRD missingPrimarycode missingSecondarycode missingNACEmain missingPdts missingTradeDesc log10Totalassets, nquantiles(20) line(none) xtitle(log10Totalassets) ytitle(% Missing) savegraph("missing_variablesofinterest20bins.jpg") replace  

binscatter missingRD missingPrimarycode missingSecondarycode missingNACEmain missingPdts missingTradeDesc log10Totalassets, nquantiles(100) line(none) xtitle(log10Totalassets) ytitle(% Missing) savegraph("missing_variablesofinterest100bins.jpg") replace  
/* binscatter missingRD log10Totalassets, nquantiles(20) line(none) savegraph("missingRD.jpg")
binscatter missingPrimarycode log10Totalassets, nquantiles(20) line(none) savegraph("missingPrimarycode.jpg")
binscatter missingSecondarycode log10Totalassets, nquantiles(20) line(none) savegraph("missingSecondarycode.jpg")
binscatter missingNACEmain log10Totalassets, nquantiles(20) line(none) savegraph("missingNACEmain.jpg")
binscatter missingNACEsecondary log10Totalassets, nquantiles(20) line(none) savegraph("missingNACEsecondary.jpg")
binscatter missingBvDmajorsector log10Totalassets, nquantiles(20) line(none) savegraph("missingBvDmajorsector.jpg")
binscatter missingPdts log10Totalassets, nquantiles(20) line(none) savegraph("missingPdts.jpg")
binscatter missingTradeDesc log10Totalassets, nquantiles(20) line(none) savegraph("missingTradeDesc.jpg") */
