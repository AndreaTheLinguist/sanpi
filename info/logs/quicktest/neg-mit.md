
# Running `script/makeTable.sh`
## >> Searching `quicktest.conll/` for `neg-mit` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Tue Aug  3 00:14:19 EDT 2021`
 
```
## Starting context: `almost-no-one_subj`
- time stamp: `Tue Aug  3 00:14:19 EDT 2021`
- data directory: `data/neg-mit/quicktest.almost-no-one_subj`
- hits table: `hits/neg-mit/quicktest_almost-no-one_subj`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma="one"]; 
  N [lemma="no"];
  det: S -[det]-> N;
  A [lemma="almost"];
  A < N;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```  
```  
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/neg-mit/quicktest.almost-no-one_subj/nyt_eng_199912.raw.json
0.06 minutes on nyt_eng_199912.conllu
Total grew search time: 0.06 minutes
```
### Running `FillJson.py` script on json files in `quicktest.almost-no-one_subj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.
Time elapsed: 0.0 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `almost-no_det-of-subj`
- time stamp: `Tue Aug  3 00:14:24 EDT 2021`
- data directory: `data/neg-mit/quicktest.almost-no_det-of-subj`
- hits table: `hits/neg-mit/quicktest_almost-no_det-of-subj`
```{js}
pattern{
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma <> "one"]; 
  N [lemma="no"];
  ALMOST [lemma="almost"];
  ALMOST < N;
  det: S -[det]-> N;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```  
```  
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/neg-mit/quicktest.almost-no_det-of-subj/nyt_eng_199912.raw.json
0.07 minutes on nyt_eng_199912.conllu
Total grew search time: 0.07 minutes
```
### Running `FillJson.py` script on json files in `quicktest.almost-no_det-of-subj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.
Time elapsed: 0.0 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `almost-nobody_subj`
- time stamp: `Tue Aug  3 00:14:28 EDT 2021`
- data directory: `data/neg-mit/quicktest.almost-nobody_subj`
- hits table: `hits/neg-mit/quicktest_almost-nobody_subj`
```{js}
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  NS [lemma="nobody"]; 
  A [lemma="almost"]; 
  A < NS;
  subj: ADJ -[nsubj|nsubjpass]-> NS;
  NS << BE;
}
```  
```  
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/neg-mit/quicktest.almost-nobody_subj/nyt_eng_199912.raw.json
0.07 minutes on nyt_eng_199912.conllu
Total grew search time: 0.07 minutes
```
### Running `FillJson.py` script on json files in `quicktest.almost-nobody_subj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.
Time elapsed: 0.0 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `almost-none_subj`
- time stamp: `Tue Aug  3 00:14:33 EDT 2021`
- data directory: `data/neg-mit/quicktest.almost-none_subj`
- hits table: `hits/neg-mit/quicktest_almost-none_subj`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S [lemma="none"]; 
  ALMOST [lemma="almost"];
  ALMOST < S;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```  
```  
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/neg-mit/quicktest.almost-none_subj/nyt_eng_199912.raw.json
0.08 minutes on nyt_eng_199912.conllu
Total grew search time: 0.08 minutes
```
### Running `FillJson.py` script on json files in `quicktest.almost-none_subj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.
Time elapsed: 0.0 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `few_det-of-subj`
- time stamp: `Tue Aug  3 00:14:38 EDT 2021`
- data directory: `data/neg-mit/quicktest.few_det-of-subj`
- hits table: `hits/neg-mit/quicktest_few_det-of-subj`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S []; 
  FEW [lemma="few"];
  S -[amod]-> FEW;
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```  
```  
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/neg-mit/quicktest.few_det-of-subj/nyt_eng_199912.raw.json
0.08 minutes on nyt_eng_199912.conllu
Total grew search time: 0.08 minutes
```
### Running `FillJson.py` script on json files in `quicktest.few_det-of-subj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.
Time elapsed: 0.0 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `few_subj`
- time stamp: `Tue Aug  3 00:14:43 EDT 2021`
- data directory: `data/neg-mit/quicktest.few_subj`
- hits table: `hits/neg-mit/quicktest_few_subj`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  FEW [lemma="few"];
  sub: ADJ -[nsubj|nsubjpass]-> FEW;
  FEW << BE
}
```  
```  
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/neg-mit/quicktest.few_subj/nyt_eng_199912.raw.json
0.07 minutes on nyt_eng_199912.conllu
Total grew search time: 0.07 minutes
```
### Running `FillJson.py` script on json files in `quicktest.few_subj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.
Time elapsed: 0.0 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
 
## Finished at: `Tue Aug  3 00:14:48 EDT 2021`
  + All raw data in `data/neg-mit/quicktest.few_subj/...`
  + All hit tabulations in `hits/neg-mit/...`

  + Total time to populate hits/neg-mit: 00:00:29
