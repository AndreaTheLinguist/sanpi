
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `playground/nyFeb2010.conll/` for `nonimmediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:09:30 EDT 2021`
 
```
## Starting context: `with_relay`
- time stamp: `Wed Oct  6 01:09:30 EDT 2021`
- data directory: `data/nonimmediateNeg/nyFeb2010.with_relay`
- hits table: `hits/nonimmediateNeg/nyFeb2010_with_relay`
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
### Running grew search on `nyFeb2010.conll`...
```
1 total file(s) to be searched.
-> searching nyFeb2010.conll/nyt_eng_201002.conllu:
grew grep -pattern playground/Pat/nonimmediateNeg/with_relay.pat -i playground/nyFeb2010.conll/nyt_eng_201002.conllu > data/nonimmediateNeg/nyFeb2010.with_relay/nyt_eng_201002.raw.json
1.22 minutes on nyt_eng_201002.conllu

Total grew search time: 1.22 minutes
==============================================

```
### Running `FillJson.py` script on json files in `nyFeb2010.with_relay` from conll files in `nyFeb2010.conll`...
```
-> Processing nyt_eng_201002...
   => 256 hit results filled from 190244 total original sentences in 23.48 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.39 minutes
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_201002.json...

^_^ Finished tabulating data for 256 sentence(s) from all json files in /home/andrea/litotes/data/nonimmediateNeg/nyFeb2010.with_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                            | neg_word   | colloc   | sent_text                                                                                                                                                             |
|:----------------------------------|:-----------|:---------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_20100227_0117_6:12-15-16  | no         | ?        | They are coming off a 3-13 season , and looking back , no one seems quite sure how they managed to win three .                                                        |
| nyt_eng_20100211_0088_58:12-14-15 | no         | ?        | Hu Yong , a Beijing-based media expert , said the government was no longer as worried as it once was about the economic impact of electronic communication controls . |
| nyt_eng_20100214_0011_35:5-14-15  | few        | ?        | Yet few designers -- and few men , for that matter -- are as deeply uneasy about their bodies as was McQueen .                                                        |
| nyt_eng_20100224_0053_45:1-7-8    | no         | ?        | -- No position in baseball is more physically demanding than catcher .                                                                                                |
| nyt_eng_20100208_0192_24:0-3-4    | no         | ?        | No victory was too small .                                                                                                                                            |
```

Time elapsed: 0.118 seconds
====================================

```  
 
## Finished at: `Wed Oct  6 01:11:07 EDT 2021`
  + All raw data in `data/nonimmediateNeg/nyFeb2010.with_relay/...`
  + All hit tabulations in `hits/nonimmediateNeg/...`

  + Total time to populate hits/nonimmediateNeg: 00:01:47
