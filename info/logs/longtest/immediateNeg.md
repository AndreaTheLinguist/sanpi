
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `longtest.conll/` for `immediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:26:46 EDT 2021`
 
```
## Starting context: `without_relay`
- time stamp: `Wed Oct  6 01:26:46 EDT 2021`
- data directory: `data/immediateNeg/longtest.without_relay`
- hits table: `hits/immediateNeg/longtest_without_relay`
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
Fatal error: out of memory
Aborted
```
### Running grew search on `longtest.conll`...
```
1 total file(s) to be searched.
-> searching longtest.conll/nyt_eng_199805.conllu:
grew grep -pattern playground/Pat/immediateNeg/without_relay.pat -i longtest.conll/nyt_eng_199805.conllu > data/immediateNeg/longtest.without_relay/nyt_eng_199805.raw.json
1.44 minutes on nyt_eng_199805.conllu

Total grew search time: 1.44 minutes
==============================================

```
### Running `FillJson.py` script on json files in `longtest.without_relay` from conll files in `longtest.conll`...
```
-> Processing nyt_eng_199805...
   -> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.0 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified json directory does not contain any processed json files.
```  
 
## Finished at: `Wed Oct  6 01:28:14 EDT 2021`
  + All raw data in `data/immediateNeg/longtest.without_relay/...`
  + All hit tabulations in `hits/immediateNeg/...`

  + Total time to populate hits/immediateNeg: 00:01:31
