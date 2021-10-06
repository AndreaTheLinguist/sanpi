
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `apwtest.conll/` for `NegRaise` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:19:36 EDT 2021`
 
```
Output directory data/NegRaise already exists and contains these relevant files:
data/NegRaise/apwtest.negraise/apw_eng_200412.raw.json
data/NegRaise/apwtest.negraise/apw_eng_199911.raw.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on apwtest again and overwrite any corresponding files? y/n 
= Corpus apwtest will be searched again. Corresponding files in data/NegRaise will be overwritten.
```
## Starting context: `negraise`
- time stamp: `Wed Oct  6 01:19:42 EDT 2021`
- data directory: `data/NegRaise/apwtest.negraise`
- hits table: `hits/NegRaise/apwtest_negraise`
```{js}
  pattern { 
      ADJ [xpos=JJ|JJR|JJS]; 
      ADV [lemma<>"not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"];
      mod: ADJ -[advmod]-> ADV;  
      ADV < ADJ;
      NEG [lemma="not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"
        |"no"|"nothing"|"none"|"nobody"|"neither"|"without"|"few"|"nor"];  
      NR [lemma="think"|"believe"|"want"|"seem"|"suppose"|"expect"|"imagine"|"likely"|"probable"|"appear"|"look"
        |"intend"|"choose"|"plan"|"wish"|"suggest"|"advise"|"advisable"
        |"desirable"|"should"|"ought"|"better"|"most"|"usually"];
      negraise: NR -> ADJ;
      neg: NR -> NEG;
      NEG << ADV;
}
```  
```  
```
### Running grew search on `apwtest.conll`...
```
2 total file(s) to be searched.
-> searching apwtest.conll/apw_eng_199911.conllu:
grew grep -pattern playground/Pat/NegRaise/negraise.pat -i apwtest.conll/apw_eng_199911.conllu > data/NegRaise/apwtest.negraise/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching apwtest.conll/apw_eng_200412.conllu:
grew grep -pattern playground/Pat/NegRaise/negraise.pat -i apwtest.conll/apw_eng_200412.conllu > data/NegRaise/apwtest.negraise/apw_eng_200412.raw.json
0.77 minutes on apw_eng_200412.conllu

Total grew search time: 0.78 minutes
==============================================

```
### Running `FillJson.py` script on json files in `apwtest.negraise` from conll files in `apwtest.conll`...
```
-> Processing apw_eng_200412...
   => 20 hit results filled from 66780 total original sentences in 14.71 seconds
-> Writing output file...
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.25 minutes
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing apw_eng_200412.json...

^_^ Finished tabulating data for 20 sentence(s) from all json files in /home/andrea/litotes/data/NegRaise/apwtest.negraise.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                           | neg_word   | colloc   | sent_text                                                                                                                                                                                                                                            |
|:---------------------------------|:-----------|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| apw_eng_20041201_0092_2:21-30-31 | not        | ?        | Burned out at the end of a long season with that featured 20-plus tournaments and not enough rest , Scott did n't want to know his golf clubs and was more interested in surfing in the ocean near the Hyatt Regency resort course than practicing . |
| apw_eng_20041204_0226_10:7-12-13 | not        | ?        | For my first flight , I could n't have imagined it being much better .                                                                                                                                                                               |
| apw_eng_20041204_0226_10:7-12-13 | not        | ?        | For my first flight , I could n't have imagined it being much better .                                                                                                                                                                               |
| apw_eng_20041204_0226_10:7-12-13 | not        | ?        | For my first flight , I could n't have imagined it being much better .                                                                                                                                                                               |
| apw_eng_20041203_0406_3:5-7-8    | not        | ?        | First , the economy does n't look as rosy as it did a month ago .                                                                                                                                                                                    |
```

Time elapsed: 0.127 seconds
====================================

```  
 
## Finished at: `Wed Oct  6 01:20:44 EDT 2021`
  + All raw data in `data/NegRaise/apwtest.negraise/...`
  + All hit tabulations in `hits/NegRaise/...`

  + Total time to populate hits/NegRaise: 00:01:09
