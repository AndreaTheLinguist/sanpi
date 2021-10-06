
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `playground/nyFeb2010.conll/` for `NegRaise` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:20:23 EDT 2021`
 
```
## Starting context: `negraise`
- time stamp: `Wed Oct  6 01:20:23 EDT 2021`
- data directory: `data/NegRaise/nyFeb2010.negraise`
- hits table: `hits/NegRaise/nyFeb2010_negraise`
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
### Running grew search on `nyFeb2010.conll`...
```
1 total file(s) to be searched.
-> searching nyFeb2010.conll/nyt_eng_201002.conllu:
grew grep -pattern playground/Pat/NegRaise/negraise.pat -i playground/nyFeb2010.conll/nyt_eng_201002.conllu > data/NegRaise/nyFeb2010.negraise/nyt_eng_201002.raw.json
3.72 minutes on nyt_eng_201002.conllu

Total grew search time: 3.73 minutes
==============================================

```
### Running `FillJson.py` script on json files in `nyFeb2010.negraise` from conll files in `nyFeb2010.conll`...
```
-> Processing nyt_eng_201002...
   -> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.0 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified json directory does not contain any processed json files.
```  
 
## Finished at: `Wed Oct  6 01:24:08 EDT 2021`
  + All raw data in `data/NegRaise/nyFeb2010.negraise/...`
  + All hit tabulations in `hits/NegRaise/...`

  + Total time to populate hits/NegRaise: 00:03:47
