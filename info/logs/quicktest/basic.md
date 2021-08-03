
# Running `script/makeTable.sh`
## >> Searching `quicktest.conll/` for `basic` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Tue Aug  3 00:10:47 EDT 2021`
 
```
Output directory data/basic already exists and contains these relevant files:
data/basic/quicktest.be-ADV-ADJ_predicate-adj/nyt_eng_199912.json
data/basic/quicktest.be-ADV-ADJ_predicate-adj/nyt_eng_199912.raw.json
data/basic/quicktest.S-be-ADV-ADJ_subj-control/nyt_eng_199912.json
data/basic/quicktest.S-be-ADV-ADJ_subj-control/nyt_eng_199912.raw.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on quicktest again and overwrite any corresponding files? y/n 
= Corpus quicktest will be searched again. Corresponding files in data/basic will be overwritten.
```
## Starting context: `ADV-ADJ_prefilter`
- time stamp: `Tue Aug  3 00:10:50 EDT 2021`
- data directory: `data/basic/quicktest.ADV-ADJ_prefilter`
- hits table: `hits/basic/quicktest_ADV-ADJ_prefilter`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ];
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
}
```  
```  
 starting scripts ====================================
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/basic/ADV-ADJ_prefilter.pat -i quicktest.conll/nyt_eng_199912.conllu > data/basic/quicktest.ADV-ADJ_prefilter/nyt_eng_199912.raw.json
0.06 minutes on nyt_eng_199912.conllu
Total grew search time: 0.06 minutes
```
### Running `FillJson.py` script on json files in `quicktest.ADV-ADJ_prefilter` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
   => 765 hit results filled from 9810 total original sentences in 1.24 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.
Time elapsed: 0.02 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_199912.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0178_24:36 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0178_4:14 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0177_15:24 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0172_1:38 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0151_38:34 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0147_2:30 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0142_23:11 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0142_23:14 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0141_33:26 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0141_26:36 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0139_25:22 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0113_5:29 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0110_2:19 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0110_2:30 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0106_9:29 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0105_30:27 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0100_2:19 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0100_1:3 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0098_2:16 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0093_16:29 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0093_7:16 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0089_15:45 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0087_26:20 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0081_50:1 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0079_12:27 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0074_2:20 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0070_11:21 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0070_11:28 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0068_40:19 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0059_40:10 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0056_8:24 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0053_3:23 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0053_3:37 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0047_4:21 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0031_36:18 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0025_49:37 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0025_34:37 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0021_15:33 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0020_31:16 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0018_24:23 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0017_42:47 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0017_35:23 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0015_32:24 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0013_30:9 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0011_55:9 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0106_9:13 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0093_33:17 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991201_0071_2:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0067_30:15 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0064_13:46 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0056_33:24 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0042_24:12 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991201_0031_1:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0024_36:28 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0009_4:10 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0006_1:21 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0004_16:8 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0004_16:12 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0002_18:5 recorded as is.

^_^ Finished collecting sentence data from all json files.
    -> Writing tables to csv files...
```
#### Data Sample

| hit_id                      | colloc         | sent_text                                                                                                                                                                                                                                      |
|:----------------------------|:---------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19991201_0104_8:14  | too_high       | Jake Winebaum , a co-founder of Ecompanies , said the price was not too high for a brand name , given that Web-based companies are spending more than $ 1 million for a 30-second commercial during the Super Bowl to make their names known . |
| nyt_eng_19991206_0143_11:16 | always_welcome | Churches and newspapers , theaters and dance palaces -LRB- in which black customers were not always welcome -RRB- flourished when Seventh Avenue , as Lewis exults , was  -LBQ-  the great black way .  -RDQ-                                  |
| nyt_eng_19991206_0178_24:11 | too_clear-eyed | There are times when  -LBQ-  Scenes  -RDQ-  can seem almost too clear-eyed ; there 's a sense that Perl is both the reporter and the reported upon , and that she 's speaking at a slightly cool remove from what 's happening to her .        |
| nyt_eng_19991206_0091_37:7  | newly_bereaved | There is no knowing how a newly bereaved person feels .                                                                                                                                                                                        |
| nyt_eng_19991206_0159_26:11 | too_fervent    | Police have already deported foreigners believed to be a little too fervent about the end of time .                                                                                                                                            |
```
```
#### Duplicates Sample

| hit_id                      | colloc              | sent_text                                                                                                                                                                               |
|:----------------------------|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19991201_0031_1:10  | surprisingly_strong | Southern California is powering into 2000 thanks to a surprisingly strong economy that is being fueled in part by Asia 's recovery , according to a forecast to be released Wednesday . |
| nyt_eng_19991206_0100_1:3   | probably_inevitable | It was probably inevitable that the World Wide Web would bloom with sites for dieters .                                                                                                 |
| nyt_eng_19991206_0081_50:1  | more_nn             | MORE nn                                                                                                                                                                                 |
| nyt_eng_19991201_0071_2:7   | so_lively           | And no little old driver , so lively and quick .                                                                                                                                        |
| nyt_eng_19991206_0068_40:19 | only_popular        | But to the surprise of professional dietitians , many of these sites have turned out to be not only popular but effective .                                                             |
```
Time elapsed: 0.076 seconds
```  
## Starting context: `S-be-ADV-ADJ_subj-control`
- time stamp: `Tue Aug  3 00:10:55 EDT 2021`
- data directory: `data/basic/quicktest.S-be-ADV-ADJ_subj-control`
- hits table: `hits/basic/quicktest_S-be-ADV-ADJ_subj-control`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  BE [lemma="be"];
  cop: ADJ -[cop]-> BE;
  S  []; 
  sub: ADJ -[nsubj|nsubjpass]-> S;
  S << BE
}
```  
```  
 starting scripts ====================================
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/basic/S-be-ADV-ADJ_subj-control.pat -i quicktest.conll/nyt_eng_199912.conllu > data/basic/quicktest.S-be-ADV-ADJ_subj-control/nyt_eng_199912.raw.json
0.12 minutes on nyt_eng_199912.conllu
Total grew search time: 0.12 minutes
```
### Running `FillJson.py` script on json files in `quicktest.S-be-ADV-ADJ_subj-control` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
   => 274 hit results filled from 9810 total original sentences in 1.06 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.
Time elapsed: 0.02 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_199912.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0110_2:10 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0100_1:3 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0093_16:29 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0025_49:37 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0093_33:17 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0056_33:24 recorded as is.

^_^ Finished collecting sentence data from all json files.
    -> Writing tables to csv files...
```
#### Data Sample

| hit_id                      | colloc         | sent_text                                                                                                          |
|:----------------------------|:---------------|:-------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19991206_0060_65:5  | also_serious   | But the book is also serious to the core , as Stern is , despite all his affability of manner .                    |
| nyt_eng_19991206_0076_26:3  | also_important | It 's also important to consider that items could still be priced , for instance , $ 19.99 instead of $ 20 .       |
| nyt_eng_19991206_0122_19:5  | too_much       | Throughout , he 's too much like a snake-oil salesman , never reaching the necessary catharsis of Nash 's script . |
| nyt_eng_19991201_0065_66:10 | pretty_bizarre | The idea of using bugs to eat grease was pretty bizarre .  -RDQ-                                                   |
| nyt_eng_19991206_0091_51:15 | so_young       | -LBQ-  It was less scary to think we would forget her because we were so young .  -RDQ-                            |
```
```
#### Duplicates Sample

| hit_id                    | colloc              | sent_text                                                                               |
|:--------------------------|:--------------------|:----------------------------------------------------------------------------------------|
| nyt_eng_19991206_0100_1:3 | probably_inevitable | It was probably inevitable that the World Wide Web would bloom with sites for dieters . |
```
Time elapsed: 0.052 seconds
```  
## Starting context: `be-ADV-ADJ_predicate-adj`
- time stamp: `Tue Aug  3 00:11:04 EDT 2021`
- data directory: `data/basic/quicktest.be-ADV-ADJ_predicate-adj`
- hits table: `hits/basic/quicktest_be-ADV-ADJ_predicate-adj`
```{js}
pattern {
  ADV [xpos=RB, lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"];
  ADJ [xpos=JJ]; 
  ADV < ADJ;
  mod: ADJ -[advmod]-> ADV;
  BE [lemma="be"];
  cop: ADJ -[cop]-> BE;
}
```  
```  
 starting scripts ====================================
```
### Running grew search on `quicktest.conll`...
```
1 total file(s) to be searched.
-> searching quicktest.conll/nyt_eng_199912.conllu:
grew grep -pattern Pat/basic/be-ADV-ADJ_predicate-adj.pat -i quicktest.conll/nyt_eng_199912.conllu > data/basic/quicktest.be-ADV-ADJ_predicate-adj/nyt_eng_199912.raw.json
0.07 minutes on nyt_eng_199912.conllu
Total grew search time: 0.07 minutes
```
### Running `FillJson.py` script on json files in `quicktest.be-ADV-ADJ_predicate-adj` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
   => 300 hit results filled from 9810 total original sentences in 1.11 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.
Time elapsed: 0.02 minutes
```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_199912.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0110_2:19 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0100_2:19 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0100_1:3 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0093_16:29 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit nyt_eng_19991206_0068_40:19 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0025_49:37 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991206_0013_30:9 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0093_33:17 recorded as is.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit nyt_eng_19991201_0056_33:24 recorded as is.

^_^ Finished collecting sentence data from all json files.
    -> Writing tables to csv files...
```
#### Data Sample

| hit_id                      | colloc              | sent_text                                                                                                                               |
|:----------------------------|:--------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19991201_0004_16:4  | as_explosive        | He 's almost as explosive , just as braided , nearly as many tattoos and capable of taking over a game .                                |
| nyt_eng_19991206_0025_43:9  | decidedly_brit      | Julian Barnes , whose penchant for satire is decidedly Brit , fancied his birthplace a theme park in  -LBQ-  England , England .  -RDQ- |
| nyt_eng_19991206_0101_1:3   | probably_inevitable | It was probably inevitable that the World Wide Web would bloom with sites for dieters .                                                 |
| nyt_eng_19991206_0056_19:19 | effectively_over    | Eventually , it was released at just over two hours and the career of Erich von Stroheim was effectively over .                         |
| nyt_eng_19991206_0015_26:9  | almost_volcanic     | -LBQ-  The sex drive in a man is almost volcanic in its latent ability to erupt at the slightest provocation .  -RDQ-                   |
```
```
#### Duplicates Sample

| hit_id                      | colloc              | sent_text                                                                                                                   |
|:----------------------------|:--------------------|:----------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_19991206_0068_40:19 | only_popular        | But to the surprise of professional dietitians , many of these sites have turned out to be not only popular but effective . |
| nyt_eng_19991206_0100_1:3   | probably_inevitable | It was probably inevitable that the World Wide Web would bloom with sites for dieters .                                     |
| nyt_eng_19991206_0100_2:19  | only_popular        | But to the surprise of professional dietitians , many of these sites have turned out to be not only popular but effective . |
```
Time elapsed: 0.051 seconds
```  
 
## Finished at: `Tue Aug  3 00:11:10 EDT 2021`
  + All raw data in `data/basic/quicktest.be-ADV-ADJ_predicate-adj/...`
  + All hit tabulations in `hits/basic/...`

  + Total time to populate hits/basic: 00:00:24
