
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `apwtest.conll/` for `nonimmediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:13:57 EDT 2021`
 
```
## Starting context: `with_relay`
- time stamp: `Wed Oct  6 01:13:57 EDT 2021`
- data directory: `data/nonimmediateNeg/apwtest.with_relay`
- hits table: `hits/nonimmediateNeg/apwtest_with_relay`
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
### Running grew search on `apwtest.conll`...
```
2 total file(s) to be searched.
-> searching apwtest.conll/apw_eng_199911.conllu:
grew grep -pattern playground/Pat/nonimmediateNeg/with_relay.pat -i apwtest.conll/apw_eng_199911.conllu > data/nonimmediateNeg/apwtest.with_relay/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching apwtest.conll/apw_eng_200412.conllu:
grew grep -pattern playground/Pat/nonimmediateNeg/with_relay.pat -i apwtest.conll/apw_eng_200412.conllu > data/nonimmediateNeg/apwtest.with_relay/apw_eng_200412.raw.json
0.85 minutes on apw_eng_200412.conllu

Total grew search time: 0.86 minutes
==============================================

```
### Running `FillJson.py` script on json files in `apwtest.with_relay` from conll files in `apwtest.conll`...
```
-> Processing apw_eng_200412...
   => 40 hit results filled from 66780 total original sentences in 8.36 seconds
-> Writing output file...
-> Processing apw_eng_199911...
   => 4 hit results filled from 1147 total original sentences in 0.17 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.14 minutes
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing apw_eng_199911.json...
-> Processing apw_eng_200412.json...

^_^ Finished tabulating data for 44 sentence(s) from all json files in /home/andrea/litotes/data/nonimmediateNeg/apwtest.with_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                         | neg_word   | colloc   | sent_text                                                                                                                                                                                                        |
|:-------------------------------|:-----------|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| apw_eng_20041201_0324_5:0-4-5  | no         | ?        | No further details were immediately available on the agreement or the detainees .                                                                                                                                |
| apw_eng_20041201_0272_2:3-5-6  | no         | ?        | Anti-personnel mines are no longer as effective as in the past because warfare has changed considerably since World War II and armies are more mobile than in the past , Kenyan Brig. Gen. Emiliano Tonui said . |
| apw_eng_20041206_0195_4:0-3-4  | no         | ?        | No one was immediately available for comment at Telecom Italia on Monday .                                                                                                                                       |
| apw_eng_20041206_0193_3:0-4-5  | no         | ?        | No additional details were immediately available .                                                                                                                                                               |
| apw_eng_20041224_0195_9:0-9-10 | no         | ?        | No official at the U.S. Embassy in Pakistan was immediately available for comment .                                                                                                                              |
```

Time elapsed: 0.087 seconds
====================================

```  
 
## Finished at: `Wed Oct  6 01:14:58 EDT 2021`
  + All raw data in `data/nonimmediateNeg/apwtest.with_relay/...`
  + All hit tabulations in `hits/nonimmediateNeg/...`

  + Total time to populate hits/nonimmediateNeg: 00:01:03
