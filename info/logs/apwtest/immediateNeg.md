
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `apwtest.conll/` for `immediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:15:08 EDT 2021`
 
```
## Starting context: `without_relay`
- time stamp: `Wed Oct  6 01:15:08 EDT 2021`
- data directory: `data/immediateNeg/apwtest.without_relay`
- hits table: `hits/immediateNeg/apwtest_without_relay`
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
### Running grew search on `apwtest.conll`...
```
2 total file(s) to be searched.
-> searching apwtest.conll/apw_eng_199911.conllu:
grew grep -pattern playground/Pat/immediateNeg/without_relay.pat -i apwtest.conll/apw_eng_199911.conllu > data/immediateNeg/apwtest.without_relay/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching apwtest.conll/apw_eng_200412.conllu:
grew grep -pattern playground/Pat/immediateNeg/without_relay.pat -i apwtest.conll/apw_eng_200412.conllu > data/immediateNeg/apwtest.without_relay/apw_eng_200412.raw.json
0.51 minutes on apw_eng_200412.conllu

Total grew search time: 0.52 minutes
==============================================

```
### Running `FillJson.py` script on json files in `apwtest.without_relay` from conll files in `apwtest.conll`...
```
-> Processing apw_eng_200412...
   => 336 hit results filled from 66780 total original sentences in 7.2 seconds
-> Writing output file...
-> Processing apw_eng_199911...
   => 6 hit results filled from 1147 total original sentences in 0.13 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.12 minutes
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing apw_eng_199911.json...
-> Processing apw_eng_200412.json...

^_^ Finished tabulating data for 342 sentence(s) from all json files in /home/andrea/litotes/data/immediateNeg/apwtest.without_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                            | neg_word   | colloc   | sent_text                                                                                                                                                                                                                                                                                      |
|:----------------------------------|:-----------|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| apw_eng_19991101_0031_5:9-10-11   | not        | ?        | It was not clear why the Ingush border was not fully open .                                                                                                                                                                                                                                    |
| apw_eng_20041201_0380_24:26-28-29 | not        | ?        | Moreover , the National Weather Service is not forecasting a particularly frigid winter and so , while heating oil supplies are tight , the situation does not seem as bad as it did in late October , when oil prices had a peak settlement price of $ 55.17 a barrel .                       |
| apw_eng_20041203_0187_3:41-42-43  | not        | ?        | With midfielders Luis Figo and Jose Maria  -LBQ-  Guti  -RDQ-  Gutierrez suspended and Zinedine Zidane slowly recovering from back trouble , Madrid coach Mariano Garcia Remon will rely heavily on Beckham against 15th-placed Villarreal to feed a forward line he 's not so worried about . |
| apw_eng_20041224_0083_3:6-7-8     | not        | ?        | Some U.N. diplomats and staff were n't so certain .                                                                                                                                                                                                                                            |
| apw_eng_20041221_0281_8:6-7-8     | not        | ?        | The cause of the accident was not immediately clear .                                                                                                                                                                                                                                          |
```

Time elapsed: 0.156 seconds
====================================

```  
 
## Finished at: `Wed Oct  6 01:15:48 EDT 2021`
  + All raw data in `data/immediateNeg/apwtest.without_relay/...`
  + All hit tabulations in `hits/immediateNeg/...`

  + Total time to populate hits/immediateNeg: 00:00:50
