
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `playground/nyDec2010.conll/` for `immediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:10:12 EDT 2021`
 
```
Output directory data/immediateNeg already exists and contains these relevant files:
data/immediateNeg/nyDec2010.without_relay/nyt_eng_201012.raw.json
 
--> Run grew search on nyDec2010 again and overwrite any corresponding files? y/n * If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 

= Corpus nyDec2010 will be searched again. Corresponding files in data/immediateNeg will be overwritten.
```
## Starting context: `without_relay`
- time stamp: `Wed Oct  6 01:10:40 EDT 2021`
- data directory: `data/immediateNeg/nyDec2010.without_relay`
- hits table: `hits/immediateNeg/nyDec2010_without_relay`
```{js}
pattern { 
    ADJ [xpos=JJ|JJR|JJS]; 
    ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
    mod: ADJ -[advmod]-> ADV;  
    ADV < ADJ;
    NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
    neg: ADJ -> NEG;
    NEG << ADV;
}
```  
```  
```
### Running grew search on `nyDec2010.conll`...
```
1 total file(s) to be searched.
-> searching nyDec2010.conll/nyt_eng_201012.conllu:
grew grep -pattern playground/Pat/immediateNeg/without_relay.pat -i playground/nyDec2010.conll/nyt_eng_201012.conllu > data/immediateNeg/nyDec2010.without_relay/nyt_eng_201012.raw.json
1.46 minutes on nyt_eng_201012.conllu

Total grew search time: 1.46 minutes
==============================================

```
### Running `FillJson.py` script on json files in `nyDec2010.without_relay` from conll files in `nyDec2010.conll`...
```
-> Processing nyt_eng_201012...
   => 1644 hit results filled from 227205 total original sentences in 25.67 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.43 minutes
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_201012.json...

^_^ Finished tabulating data for 1644 sentence(s) from all json files in /home/andrea/litotes/data/immediateNeg/nyDec2010.without_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                            | neg_word   | colloc   | sent_text                                                                                                                                   |
|:----------------------------------|:-----------|:---------|:--------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_20101227_0148_15:7-8-9    | not        | ?        | On the surface , Android 2.3 is not radically different from the previous version , 2.2 or Froyo .                                          |
| nyt_eng_20101229_0102_16:20-22-23 | not        | ?        | There was a time when the Saudi government 's architecture and urban planning efforts , especially around Mecca , did not seem so callous . |
| nyt_eng_20101201_0042_20:22-23-24 | not        | ?        | With the holidays approaching , the call for parental help at school has reached a fever pitch , but this demand is not just seasonal .     |
| nyt_eng_20101215_0035_49:14-15-16 | not        | ?        | -LBQ-  At the end of November , everything goes on sale and it 's not even cold yet .                                                       |
| nyt_eng_20101205_0148_15:4-5-6    | not        | ?        | While the sites are not yet profitable , Abrams said most of them should start earning money in February .                                  |
```

Time elapsed: 0.359 seconds
====================================

```  
 
## Finished at: `Wed Oct  6 01:12:34 EDT 2021`
  + All raw data in `data/immediateNeg/nyDec2010.without_relay/...`
  + All hit tabulations in `hits/immediateNeg/...`

  + Total time to populate hits/immediateNeg: 00:02:34
