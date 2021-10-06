
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `longtest.conll/` for `NegRaise` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:28:20 EDT 2021`
 
```
Output directory data/NegRaise already exists and contains these relevant files:
data/NegRaise/longtest.negraise/nyt_eng_199805.raw.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on longtest again and overwrite any corresponding files? y/n 
= Corpus longtest will be searched again. Corresponding files in data/NegRaise will be overwritten.
```
## Starting context: `negraise`
- time stamp: `Wed Oct  6 01:28:23 EDT 2021`
- data directory: `data/NegRaise/longtest.negraise`
- hits table: `hits/NegRaise/longtest_negraise`
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
Fatal error: out of memory
Aborted
```
### Running grew search on `longtest.conll`...
```
1 total file(s) to be searched.
-> searching longtest.conll/nyt_eng_199805.conllu:
grew grep -pattern playground/Pat/NegRaise/negraise.pat -i longtest.conll/nyt_eng_199805.conllu > data/NegRaise/longtest.negraise/nyt_eng_199805.raw.json
1.26 minutes on nyt_eng_199805.conllu

Total grew search time: 1.26 minutes
==============================================

```
### Running `FillJson.py` script on json files in `longtest.negraise` from conll files in `longtest.conll`...
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
 
## Finished at: `Wed Oct  6 01:29:40 EDT 2021`
  + All raw data in `data/NegRaise/longtest.negraise/...`
  + All hit tabulations in `hits/NegRaise/...`

  + Total time to populate hits/NegRaise: 00:01:21
