
# Running `script/makeTable.sh`
_Checking for required packages..._
```
pyconll package not found:
pip3 install pyconll
Requirement already satisfied: pyconll in /home/arh234/.local/lib/python3.8/site-packages (3.1.0)
 
pandas package not found:
pip3 install pandas
Requirement already satisfied: pandas in /home/arh234/.local/lib/python3.8/site-packages (1.3.1)
Requirement already satisfied: numpy>=1.17.3 in /home/arh234/.local/lib/python3.8/site-packages (from pandas) (1.21.1)
Requirement already satisfied: python-dateutil>=2.7.3 in /home/arh234/.local/lib/python3.8/site-packages (from pandas) (2.8.2)
Requirement already satisfied: pytz>=2017.3 in /home/arh234/.local/lib/python3.8/site-packages (from pandas) (2021.1)
Requirement already satisfied: six>=1.5 in /usr/lib/python3/dist-packages (from python-dateutil>=2.7.3->pandas) (1.14.0)
```
## >> Searching `quicktest.conll/` for `devel` patterns
 
- started by: `arh234`
- run from: `/home/arh234/snpa`
- timestamp: `Tue Aug  3 14:30:56 EDT 2021`
 
```
Output directory data/devel already exists and contains these relevant files:
data/devel/quicktest.try_this/nyt_eng_199912.raw.json
data/devel/quicktest.try_this/nyt_eng_199912.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on quicktest again and overwrite any corresponding files? y/n 
= New quicktest corpus searches will NOT be run. Current files in data/devel will be used.
```
## Starting context: `try_this`
- time stamp: `Tue Aug  3 14:31:01 EDT 2021`
- data directory: `data/devel/quicktest.try_this`
- hits table: `hits/devel/quicktest_try_this`
```{js}
pattern {
  ADV [xpos=RB,  lemma <> "not"|"hardly"|"scarcely"|"never"|"rarely"|"barely"|"seldom"|"no"];
  ADJ [xpos=JJ]; 
  BE [lemma="be"];
  ADV < ADJ;
  advmod: ADJ -[advmod]-> ADV;
  cop: ADJ -[cop]-> BE;
  S  []; 
  subj: ADJ -[nsubj|nsubjpass]-> S;
  S << BE;
  NOT [lemma = "not"];
  neg: ADJ -[neg]-> NOT;
}
```  
```  
```
### Running `FillJson.py` script on json files in `quicktest.try_this` from conll files in `quicktest.conll`...
```
-> Processing nyt_eng_199912...
   => 17 hit results filled from 9810 total original sentences in 1.08 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.02 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_199912.json...

^_^ Finished collecting sentence data from all json files.
    -> Writing tables to csv files...
```

Time elapsed: 0.021 seconds
====================================

```  
 
## Finished at: `Tue Aug  3 14:31:02 EDT 2021`
  + All raw data in `data/devel/quicktest.try_this/...`
  + All hit tabulations in `hits/devel/...`

  + Total time to populate hits/devel: 00:00:11
