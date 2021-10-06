
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `playground/nyDec2010.conll/` for `nonimmediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:08:00 EDT 2021`
 
```
Output directory data/nonimmediateNeg already exists and contains these relevant files:
data/nonimmediateNeg/nyDec2010.with_relay/nyt_eng_201012.raw.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on nyDec2010 again and overwrite any corresponding files? y/n 
= Corpus nyDec2010 will be searched again. Corresponding files in data/nonimmediateNeg will be overwritten.
```
## Starting context: `with_relay`
- time stamp: `Wed Oct  6 01:08:10 EDT 2021`
- data directory: `data/nonimmediateNeg/nyDec2010.with_relay`
- hits table: `hits/nonimmediateNeg/nyDec2010_with_relay`
```{js}
pattern { 
    ADJ [xpos=JJ|JJR|JJS]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    NEG [lemma="hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
    relay: ADJ -> RELAY; 
    neg: RELAY -> NEG;
    NEG << ADV;
}
```  
```  
```
### Running grew search on `nyDec2010.conll`...
```
1 total file(s) to be searched.
-> searching nyDec2010.conll/nyt_eng_201012.conllu:
grew grep -pattern playground/Pat/nonimmediateNeg/with_relay.pat -i playground/nyDec2010.conll/nyt_eng_201012.conllu > data/nonimmediateNeg/nyDec2010.with_relay/nyt_eng_201012.raw.json
1.43 minutes on nyt_eng_201012.conllu

Total grew search time: 1.43 minutes
==============================================

```
### Running `FillJson.py` script on json files in `nyDec2010.with_relay` from conll files in `nyDec2010.conll`...
```
-> Processing nyt_eng_201012...
   => 228 hit results filled from 227205 total original sentences in 23.28 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.39 minutes
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_201012.json...

^_^ Finished tabulating data for 228 sentence(s) from all json files in /home/andrea/litotes/data/nonimmediateNeg/nyDec2010.with_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                            | neg_word   | colloc   | sent_text                                                                                                                                                                                                                                                 |
|:----------------------------------|:-----------|:---------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_20101221_0101_17:6-11-12  | no         | ?        | After Amar ' e Stoudemire , no other player has been as critical to the team 's resurgence .                                                                                                                                                              |
| nyt_eng_20101211_0044_81:1-6-7    | no         | ?        | Perhaps no business in finance is as profitable today as derivatives .                                                                                                                                                                                    |
| nyt_eng_20101201_0042_37:6-35-36  | no         | ?        | Under the headline  -LBQ-  Just Say NO to Volunteering ,  -RDQ-  Sarah Auerswald , a former PTA president in Los Angeles , wrote in June ,  -LBQ-  What I am about to say is not very PC , so get ready  -COL-  Moms , stop volunteering so much .  -RDQ- |
| nyt_eng_20101201_0006_33:19-27-28 | neither    | ?        | He knows about the championships , and he knows about the draft picks , and he probably knows that neither the team nor the coaching job is as good as it used to be .                                                                                    |
| nyt_eng_20101222_0067_43:17-21-22 | no         | ?        | And yet , as word of this seeped across frozen towns like this one Wednesday , almost no one seemed even mildly surprised .                                                                                                                               |
```

Time elapsed: 0.114 seconds
====================================

```  
 
## Finished at: `Wed Oct  6 01:10:00 EDT 2021`
  + All raw data in `data/nonimmediateNeg/nyDec2010.with_relay/...`
  + All hit tabulations in `hits/nonimmediateNeg/...`

  + Total time to populate hits/nonimmediateNeg: 00:02:02
