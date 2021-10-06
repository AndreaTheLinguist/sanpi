
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `longtest.conll/` for `nonimmediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:24:37 EDT 2021`
 
```
## Starting context: `with_relay`
- time stamp: `Wed Oct  6 01:24:37 EDT 2021`
- data directory: `data/nonimmediateNeg/longtest.with_relay`
- hits table: `hits/nonimmediateNeg/longtest_with_relay`
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
### Running grew search on `longtest.conll`...
```
1 total file(s) to be searched.
-> searching longtest.conll/nyt_eng_199805.conllu:
grew grep -pattern playground/Pat/nonimmediateNeg/with_relay.pat -i longtest.conll/nyt_eng_199805.conllu > data/nonimmediateNeg/longtest.with_relay/nyt_eng_199805.raw.json
5.46 minutes on nyt_eng_199805.conllu

Total grew search time: 5.46 minutes
==============================================

```
### Running `FillJson.py` script on json files in `longtest.with_relay` from conll files in `longtest.conll`...
```
-> Processing nyt_eng_199805...
   => 324 hit results filled from 260410 total original sentences in 26.83 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.45 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_199805.json...

^_^ Finished tabulating data for 324 sentence(s) from all json files in /home/andrea/litotes/data/nonimmediateNeg/longtest.with_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                          | neg_word   | colloc   | sent_text                                                                                                                                                  |
|:--------------------------------|:-----------|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19980520_0371_12:3-6-7  | nor        | ?        | And neither white nor black seems much interested in genuine integration .                                                                                 |
| nyt_eng_19980514_0401_45:3-6-7  | neither    | ?        | Television footage suggested neither general was entirely accurate , but the panic and the rattle of gunfire in the scenes left unclear who was shooting . |
| nyt_eng_19980520_0267_12:0-3-4  | no         | ?        | No one is more excited than I am about the Net , the most revolutionary communications medium of the century .                                             |
| nyt_eng_19980512_0029_44:6-9-10 | no         | ?        | In my observation of him , no detail is too minute not to emphasize and cover to make our wide receivers better ,  -RDQ-  Jones said .                     |
| nyt_eng_19980523_0202_6:0-7-8   | no         | ?        | No one , it seems , is more sociable than a 5-year-old .                                                                                                   |
```

Time elapsed: 0.157 seconds
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```  
 
## Finished at: `Wed Oct  6 01:30:32 EDT 2021`
  + All raw data in `data/nonimmediateNeg/longtest.with_relay/...`
  + All hit tabulations in `hits/nonimmediateNeg/...`

  + Total time to populate hits/nonimmediateNeg: 00:05:56
