
# Running `script/makeTable.sh`
_Checking for required packages..._
```
pyconll package not found:
pip3 install pyconll
Requirement already satisfied: pyconll in /home/arh234/.local/lib/python3.8/site-packages (3.1.0)
 
pandas package not found:
pip3 install pandas
Requirement already satisfied: pandas in /home/arh234/.local/lib/python3.8/site-packages (1.3.1)
Requirement already satisfied: pytz>=2017.3 in /home/arh234/.local/lib/python3.8/site-packages (from pandas) (2021.1)
Requirement already satisfied: python-dateutil>=2.7.3 in /home/arh234/.local/lib/python3.8/site-packages (from pandas) (2.8.2)
Requirement already satisfied: numpy>=1.17.3 in /home/arh234/.local/lib/python3.8/site-packages (from pandas) (1.21.1)
Requirement already satisfied: six>=1.5 in /usr/lib/python3/dist-packages (from python-dateutil>=2.7.3->pandas) (1.14.0)
```
## >> Searching `Apw.conll` for `neg-mit` patterns
 
- started by: `arh234`
- run from: `/home/arh234/snpa`
- timestamp: `Tue Aug  3 15:07:18 EDT 2021`
 
```
## Starting context: `almost-no-one_subj`
- time stamp: `Tue Aug  3 15:07:18 EDT 2021`
- data directory: `data/neg-mit/Apw.almost-no-one_subj`
- hits table: `hits/neg-mit/Apw_almost-no-one_subj`
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
 WARNING : [Conll, File Apw.conll/apw_eng_199608.conllu] No blank line at the end of the file
```
### Running grew search on `Apw.conll`...
```
193 total file(s) to be searched.
-> searching Apw.conll/apw_eng_199411.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199411.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199411.raw.json
1.62 minutes on apw_eng_199411.conllu
-> searching Apw.conll/apw_eng_199412.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199412.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199412.raw.json
2.43 minutes on apw_eng_199412.conllu
-> searching Apw.conll/apw_eng_199501.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199501.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199501.raw.json
2.45 minutes on apw_eng_199501.conllu
-> searching Apw.conll/apw_eng_199502.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199502.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199502.raw.json
2.22 minutes on apw_eng_199502.conllu
-> searching Apw.conll/apw_eng_199503.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199503.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199503.raw.json
2.56 minutes on apw_eng_199503.conllu
-> searching Apw.conll/apw_eng_199504.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199504.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199504.raw.json
2.55 minutes on apw_eng_199504.conllu
-> searching Apw.conll/apw_eng_199505.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199505.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199505.raw.json
3.2 minutes on apw_eng_199505.conllu
-> searching Apw.conll/apw_eng_199506.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199506.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199506.raw.json
3.38 minutes on apw_eng_199506.conllu
-> searching Apw.conll/apw_eng_199507.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199507.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199507.raw.json
3.22 minutes on apw_eng_199507.conllu
-> searching Apw.conll/apw_eng_199508.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199508.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199508.raw.json
3.14 minutes on apw_eng_199508.conllu
-> searching Apw.conll/apw_eng_199509.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199509.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199509.raw.json
3.03 minutes on apw_eng_199509.conllu
-> searching Apw.conll/apw_eng_199510.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199510.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199510.raw.json
2.13 minutes on apw_eng_199510.conllu
-> searching Apw.conll/apw_eng_199511.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199511.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199511.raw.json
2.1 minutes on apw_eng_199511.conllu
-> searching Apw.conll/apw_eng_199512.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199512.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199512.raw.json
2.05 minutes on apw_eng_199512.conllu
-> searching Apw.conll/apw_eng_199601.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199601.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199601.raw.json
2.15 minutes on apw_eng_199601.conllu
-> searching Apw.conll/apw_eng_199602.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199602.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199602.raw.json
1.98 minutes on apw_eng_199602.conllu
-> searching Apw.conll/apw_eng_199603.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199603.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199603.raw.json
2.25 minutes on apw_eng_199603.conllu
-> searching Apw.conll/apw_eng_199604.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199604.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199604.raw.json
2.15 minutes on apw_eng_199604.conllu
-> searching Apw.conll/apw_eng_199605.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199605.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199605.raw.json
2.22 minutes on apw_eng_199605.conllu
-> searching Apw.conll/apw_eng_199606.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199606.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199606.raw.json
1.93 minutes on apw_eng_199606.conllu
-> searching Apw.conll/apw_eng_199607.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199607.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199607.raw.json
1.99 minutes on apw_eng_199607.conllu
-> searching Apw.conll/apw_eng_199608.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199608.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199608.raw.json
1.59 minutes on apw_eng_199608.conllu
-> searching Apw.conll/apw_eng_199609.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199609.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199609.raw.json
1.82 minutes on apw_eng_199609.conllu
-> searching Apw.conll/apw_eng_199610.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199610.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199610.raw.json
1.99 minutes on apw_eng_199610.conllu
-> searching Apw.conll/apw_eng_199611.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199611.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199611.raw.json
2.05 minutes on apw_eng_199611.conllu
-> searching Apw.conll/apw_eng_199612.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199612.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199612.raw.json
2.14 minutes on apw_eng_199612.conllu
-> searching Apw.conll/apw_eng_199701.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199701.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199701.raw.json
2.29 minutes on apw_eng_199701.conllu
-> searching Apw.conll/apw_eng_199702.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199702.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199702.raw.json
2.1 minutes on apw_eng_199702.conllu
-> searching Apw.conll/apw_eng_199703.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199703.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199703.raw.json
2.44 minutes on apw_eng_199703.conllu
-> searching Apw.conll/apw_eng_199704.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199704.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199704.raw.json
2.31 minutes on apw_eng_199704.conllu
-> searching Apw.conll/apw_eng_199705.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199705.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199705.raw.json
2.4 minutes on apw_eng_199705.conllu
-> searching Apw.conll/apw_eng_199706.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199706.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199706.raw.json
2.34 minutes on apw_eng_199706.conllu
-> searching Apw.conll/apw_eng_199707.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199707.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199707.raw.json
2.44 minutes on apw_eng_199707.conllu
-> searching Apw.conll/apw_eng_199708.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199708.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199708.raw.json
2.28 minutes on apw_eng_199708.conllu
-> searching Apw.conll/apw_eng_199709.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199709.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199709.raw.json
2.58 minutes on apw_eng_199709.conllu
-> searching Apw.conll/apw_eng_199710.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199710.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199710.raw.json
2.44 minutes on apw_eng_199710.conllu
-> searching Apw.conll/apw_eng_199711.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199711.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199711.raw.json
3.03 minutes on apw_eng_199711.conllu
-> searching Apw.conll/apw_eng_199712.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199712.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199712.raw.json
3.81 minutes on apw_eng_199712.conllu
-> searching Apw.conll/apw_eng_199801.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199801.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199801.raw.json
3.95 minutes on apw_eng_199801.conllu
-> searching Apw.conll/apw_eng_199802.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199802.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199802.raw.json
4.15 minutes on apw_eng_199802.conllu
-> searching Apw.conll/apw_eng_199803.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199803.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199803.raw.json
4.33 minutes on apw_eng_199803.conllu
-> searching Apw.conll/apw_eng_199804.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199804.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199804.raw.json
4.12 minutes on apw_eng_199804.conllu
-> searching Apw.conll/apw_eng_199805.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199805.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199805.raw.json
4.15 minutes on apw_eng_199805.conllu
-> searching Apw.conll/apw_eng_199806.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199806.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199806.raw.json
3.86 minutes on apw_eng_199806.conllu
-> searching Apw.conll/apw_eng_199807.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199807.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199807.raw.json
2.4 minutes on apw_eng_199807.conllu
-> searching Apw.conll/apw_eng_199808.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199808.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199808.raw.json
2.46 minutes on apw_eng_199808.conllu
-> searching Apw.conll/apw_eng_199809.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199809.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199809.raw.json
2.65 minutes on apw_eng_199809.conllu
-> searching Apw.conll/apw_eng_199810.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199810.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199810.raw.json
2.6 minutes on apw_eng_199810.conllu
-> searching Apw.conll/apw_eng_199811.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199811.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199811.raw.json
2.49 minutes on apw_eng_199811.conllu
-> searching Apw.conll/apw_eng_199812.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199812.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199812.raw.json
2.96 minutes on apw_eng_199812.conllu
-> searching Apw.conll/apw_eng_199901.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199901.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199901.raw.json
2.81 minutes on apw_eng_199901.conllu
-> searching Apw.conll/apw_eng_199902.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199902.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199902.raw.json
2.51 minutes on apw_eng_199902.conllu
-> searching Apw.conll/apw_eng_199903.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199903.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199903.raw.json
3.12 minutes on apw_eng_199903.conllu
-> searching Apw.conll/apw_eng_199904.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199904.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199904.raw.json
2.94 minutes on apw_eng_199904.conllu
-> searching Apw.conll/apw_eng_199905.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199905.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199905.raw.json
3.04 minutes on apw_eng_199905.conllu
-> searching Apw.conll/apw_eng_199906.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199906.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199906.raw.json
3.1 minutes on apw_eng_199906.conllu
-> searching Apw.conll/apw_eng_199907.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199907.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199907.raw.json
2.87 minutes on apw_eng_199907.conllu
-> searching Apw.conll/apw_eng_199908.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199908.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199908.raw.json
1.95 minutes on apw_eng_199908.conllu
-> searching Apw.conll/apw_eng_199909.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199909.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199909.raw.json
1.6 minutes on apw_eng_199909.conllu
-> searching Apw.conll/apw_eng_199910.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199910.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199910.raw.json
2.04 minutes on apw_eng_199910.conllu
-> searching Apw.conll/apw_eng_199911.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_199911.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching Apw.conll/apw_eng_200001.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200001.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200001.raw.json
1.89 minutes on apw_eng_200001.conllu
-> searching Apw.conll/apw_eng_200002.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200002.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200002.raw.json
1.74 minutes on apw_eng_200002.conllu
-> searching Apw.conll/apw_eng_200003.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200003.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200003.raw.json
1.47 minutes on apw_eng_200003.conllu
-> searching Apw.conll/apw_eng_200004.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200004.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200004.raw.json
1.22 minutes on apw_eng_200004.conllu
-> searching Apw.conll/apw_eng_200005.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200005.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200005.raw.json
1.36 minutes on apw_eng_200005.conllu
-> searching Apw.conll/apw_eng_200006.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200006.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200006.raw.json
1.17 minutes on apw_eng_200006.conllu
-> searching Apw.conll/apw_eng_200007.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200007.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200007.raw.json
1.18 minutes on apw_eng_200007.conllu
-> searching Apw.conll/apw_eng_200008.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200008.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200008.raw.json
1.11 minutes on apw_eng_200008.conllu
-> searching Apw.conll/apw_eng_200009.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200009.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200009.raw.json
1.17 minutes on apw_eng_200009.conllu
-> searching Apw.conll/apw_eng_200010.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200010.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200010.raw.json
4.79 minutes on apw_eng_200010.conllu
-> searching Apw.conll/apw_eng_200011.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200011.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200011.raw.json
5.24 minutes on apw_eng_200011.conllu
-> searching Apw.conll/apw_eng_200012.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200012.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200012.raw.json
4.98 minutes on apw_eng_200012.conllu
-> searching Apw.conll/apw_eng_200101.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200101.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200101.raw.json
5.1 minutes on apw_eng_200101.conllu
-> searching Apw.conll/apw_eng_200102.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200102.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200102.raw.json
4.4 minutes on apw_eng_200102.conllu
-> searching Apw.conll/apw_eng_200103.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200103.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200103.raw.json
5.33 minutes on apw_eng_200103.conllu
-> searching Apw.conll/apw_eng_200104.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200104.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200104.raw.json
4.87 minutes on apw_eng_200104.conllu
-> searching Apw.conll/apw_eng_200105.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200105.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200105.raw.json
5.42 minutes on apw_eng_200105.conllu
-> searching Apw.conll/apw_eng_200106.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200106.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200106.raw.json
5.27 minutes on apw_eng_200106.conllu
-> searching Apw.conll/apw_eng_200107.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200107.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200107.raw.json
5.15 minutes on apw_eng_200107.conllu
-> searching Apw.conll/apw_eng_200108.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200108.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200108.raw.json
2.88 minutes on apw_eng_200108.conllu
-> searching Apw.conll/apw_eng_200109.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200109.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200109.raw.json
3.95 minutes on apw_eng_200109.conllu
-> searching Apw.conll/apw_eng_200110.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200110.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200110.raw.json
4.02 minutes on apw_eng_200110.conllu
-> searching Apw.conll/apw_eng_200111.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200111.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200111.raw.json
3.63 minutes on apw_eng_200111.conllu
-> searching Apw.conll/apw_eng_200112.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200112.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200112.raw.json
3.43 minutes on apw_eng_200112.conllu
-> searching Apw.conll/apw_eng_200201.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200201.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200201.raw.json
3.84 minutes on apw_eng_200201.conllu
-> searching Apw.conll/apw_eng_200202.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200202.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200202.raw.json
3.72 minutes on apw_eng_200202.conllu
-> searching Apw.conll/apw_eng_200203.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200203.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200203.raw.json
3.96 minutes on apw_eng_200203.conllu
-> searching Apw.conll/apw_eng_200204.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200204.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200204.raw.json
4.1 minutes on apw_eng_200204.conllu
-> searching Apw.conll/apw_eng_200205.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200205.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200205.raw.json
4.1 minutes on apw_eng_200205.conllu
-> searching Apw.conll/apw_eng_200206.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200206.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200206.raw.json
3.96 minutes on apw_eng_200206.conllu
-> searching Apw.conll/apw_eng_200207.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200207.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200207.raw.json
4.1 minutes on apw_eng_200207.conllu
-> searching Apw.conll/apw_eng_200208.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200208.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200208.raw.json
3.74 minutes on apw_eng_200208.conllu
-> searching Apw.conll/apw_eng_200209.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200209.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200209.raw.json
4.04 minutes on apw_eng_200209.conllu
-> searching Apw.conll/apw_eng_200210.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200210.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200210.raw.json
4.45 minutes on apw_eng_200210.conllu
-> searching Apw.conll/apw_eng_200211.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200211.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200211.raw.json
3.96 minutes on apw_eng_200211.conllu
-> searching Apw.conll/apw_eng_200212.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200212.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200212.raw.json
3.01 minutes on apw_eng_200212.conllu
-> searching Apw.conll/apw_eng_200301.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200301.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200301.raw.json
4.35 minutes on apw_eng_200301.conllu
-> searching Apw.conll/apw_eng_200302.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200302.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200302.raw.json
4.39 minutes on apw_eng_200302.conllu
-> searching Apw.conll/apw_eng_200303.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200303.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200303.raw.json
5.03 minutes on apw_eng_200303.conllu
-> searching Apw.conll/apw_eng_200304.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200304.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200304.raw.json
4.49 minutes on apw_eng_200304.conllu
-> searching Apw.conll/apw_eng_200305.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200305.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200305.raw.json
4.25 minutes on apw_eng_200305.conllu
-> searching Apw.conll/apw_eng_200306.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200306.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200306.raw.json
3.33 minutes on apw_eng_200306.conllu
-> searching Apw.conll/apw_eng_200307.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200307.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200307.raw.json
1.49 minutes on apw_eng_200307.conllu
-> searching Apw.conll/apw_eng_200308.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200308.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200308.raw.json
3.89 minutes on apw_eng_200308.conllu
-> searching Apw.conll/apw_eng_200309.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200309.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200309.raw.json
4.44 minutes on apw_eng_200309.conllu
-> searching Apw.conll/apw_eng_200310.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200310.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200310.raw.json
5.24 minutes on apw_eng_200310.conllu
-> searching Apw.conll/apw_eng_200311.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200311.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200311.raw.json
4.46 minutes on apw_eng_200311.conllu
-> searching Apw.conll/apw_eng_200312.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200312.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200312.raw.json
4.14 minutes on apw_eng_200312.conllu
-> searching Apw.conll/apw_eng_200401.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200401.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200401.raw.json
2.52 minutes on apw_eng_200401.conllu
-> searching Apw.conll/apw_eng_200402.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200402.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200402.raw.json
3.41 minutes on apw_eng_200402.conllu
-> searching Apw.conll/apw_eng_200403.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200403.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200403.raw.json
5.35 minutes on apw_eng_200403.conllu
-> searching Apw.conll/apw_eng_200404.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200404.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200404.raw.json
4.74 minutes on apw_eng_200404.conllu
-> searching Apw.conll/apw_eng_200405.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200405.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200405.raw.json
0.94 minutes on apw_eng_200405.conllu
-> searching Apw.conll/apw_eng_200406.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200406.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200406.raw.json
0.88 minutes on apw_eng_200406.conllu
-> searching Apw.conll/apw_eng_200407.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200407.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200407.raw.json
2.13 minutes on apw_eng_200407.conllu
-> searching Apw.conll/apw_eng_200408.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200408.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200408.raw.json
1.83 minutes on apw_eng_200408.conllu
-> searching Apw.conll/apw_eng_200409.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200409.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200409.raw.json
2.07 minutes on apw_eng_200409.conllu
-> searching Apw.conll/apw_eng_200410.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200410.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200410.raw.json
2.32 minutes on apw_eng_200410.conllu
-> searching Apw.conll/apw_eng_200411.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200411.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200411.raw.json
1.72 minutes on apw_eng_200411.conllu
-> searching Apw.conll/apw_eng_200412.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200412.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200412.raw.json
0.61 minutes on apw_eng_200412.conllu
-> searching Apw.conll/apw_eng_200501.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200501.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200501.raw.json
1.68 minutes on apw_eng_200501.conllu
-> searching Apw.conll/apw_eng_200502.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200502.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200502.raw.json
1.57 minutes on apw_eng_200502.conllu
-> searching Apw.conll/apw_eng_200503.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200503.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200503.raw.json
2.35 minutes on apw_eng_200503.conllu
-> searching Apw.conll/apw_eng_200504.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200504.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200504.raw.json
1.57 minutes on apw_eng_200504.conllu
-> searching Apw.conll/apw_eng_200505.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200505.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200505.raw.json
2.18 minutes on apw_eng_200505.conllu
-> searching Apw.conll/apw_eng_200506.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200506.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200506.raw.json
2.33 minutes on apw_eng_200506.conllu
-> searching Apw.conll/apw_eng_200507.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200507.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200507.raw.json
1.46 minutes on apw_eng_200507.conllu
-> searching Apw.conll/apw_eng_200508.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200508.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200508.raw.json
2.09 minutes on apw_eng_200508.conllu
-> searching Apw.conll/apw_eng_200509.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200509.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200509.raw.json
2.39 minutes on apw_eng_200509.conllu
-> searching Apw.conll/apw_eng_200510.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200510.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200510.raw.json
2.27 minutes on apw_eng_200510.conllu
-> searching Apw.conll/apw_eng_200511.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200511.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200511.raw.json
2.34 minutes on apw_eng_200511.conllu
-> searching Apw.conll/apw_eng_200512.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200512.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200512.raw.json
2.21 minutes on apw_eng_200512.conllu
-> searching Apw.conll/apw_eng_200601.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200601.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200601.raw.json
2.28 minutes on apw_eng_200601.conllu
-> searching Apw.conll/apw_eng_200602.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200602.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200602.raw.json
1.92 minutes on apw_eng_200602.conllu
-> searching Apw.conll/apw_eng_200603.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200603.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200603.raw.json
2.48 minutes on apw_eng_200603.conllu
-> searching Apw.conll/apw_eng_200604.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200604.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200604.raw.json
2.02 minutes on apw_eng_200604.conllu
-> searching Apw.conll/apw_eng_200605.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200605.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200605.raw.json
2.66 minutes on apw_eng_200605.conllu
-> searching Apw.conll/apw_eng_200606.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200606.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200606.raw.json
2.33 minutes on apw_eng_200606.conllu
-> searching Apw.conll/apw_eng_200607.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200607.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200607.raw.json
2.3 minutes on apw_eng_200607.conllu
-> searching Apw.conll/apw_eng_200608.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200608.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200608.raw.json
2.09 minutes on apw_eng_200608.conllu
-> searching Apw.conll/apw_eng_200609.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200609.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200609.raw.json
2.01 minutes on apw_eng_200609.conllu
-> searching Apw.conll/apw_eng_200610.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200610.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200610.raw.json
4.78 minutes on apw_eng_200610.conllu
-> searching Apw.conll/apw_eng_200611.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200611.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200611.raw.json
4.92 minutes on apw_eng_200611.conllu
-> searching Apw.conll/apw_eng_200612.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200612.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200612.raw.json
1.73 minutes on apw_eng_200612.conllu
-> searching Apw.conll/apw_eng_200701.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200701.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200701.raw.json
4.89 minutes on apw_eng_200701.conllu
-> searching Apw.conll/apw_eng_200702.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200702.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200702.raw.json
4.35 minutes on apw_eng_200702.conllu
-> searching Apw.conll/apw_eng_200703.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200703.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200703.raw.json
4.85 minutes on apw_eng_200703.conllu
-> searching Apw.conll/apw_eng_200704.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200704.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200704.raw.json
4.52 minutes on apw_eng_200704.conllu
-> searching Apw.conll/apw_eng_200705.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200705.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200705.raw.json
4.71 minutes on apw_eng_200705.conllu
-> searching Apw.conll/apw_eng_200706.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200706.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200706.raw.json
4.56 minutes on apw_eng_200706.conllu
-> searching Apw.conll/apw_eng_200707.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200707.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200707.raw.json
4.33 minutes on apw_eng_200707.conllu
-> searching Apw.conll/apw_eng_200708.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200708.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200708.raw.json
4.54 minutes on apw_eng_200708.conllu
-> searching Apw.conll/apw_eng_200709.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200709.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200709.raw.json
4.72 minutes on apw_eng_200709.conllu
-> searching Apw.conll/apw_eng_200710.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200710.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200710.raw.json
4.55 minutes on apw_eng_200710.conllu
-> searching Apw.conll/apw_eng_200711.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200711.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200711.raw.json
4.22 minutes on apw_eng_200711.conllu
-> searching Apw.conll/apw_eng_200712.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200712.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200712.raw.json
3.56 minutes on apw_eng_200712.conllu
-> searching Apw.conll/apw_eng_200801.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200801.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200801.raw.json
4.64 minutes on apw_eng_200801.conllu
-> searching Apw.conll/apw_eng_200802.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200802.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200802.raw.json
4.52 minutes on apw_eng_200802.conllu
-> searching Apw.conll/apw_eng_200803.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200803.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200803.raw.json
4.42 minutes on apw_eng_200803.conllu
-> searching Apw.conll/apw_eng_200804.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200804.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200804.raw.json
4.25 minutes on apw_eng_200804.conllu
-> searching Apw.conll/apw_eng_200805.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200805.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200805.raw.json
4.54 minutes on apw_eng_200805.conllu
-> searching Apw.conll/apw_eng_200806.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200806.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200806.raw.json
4.42 minutes on apw_eng_200806.conllu
-> searching Apw.conll/apw_eng_200807.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200807.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200807.raw.json
3.82 minutes on apw_eng_200807.conllu
-> searching Apw.conll/apw_eng_200808.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200808.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200808.raw.json
3.9 minutes on apw_eng_200808.conllu
-> searching Apw.conll/apw_eng_200809.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200809.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200809.raw.json
3.94 minutes on apw_eng_200809.conllu
-> searching Apw.conll/apw_eng_200810.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200810.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200810.raw.json
3.88 minutes on apw_eng_200810.conllu
-> searching Apw.conll/apw_eng_200811.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200811.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200811.raw.json
2.98 minutes on apw_eng_200811.conllu
-> searching Apw.conll/apw_eng_200812.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200812.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200812.raw.json
2.48 minutes on apw_eng_200812.conllu
-> searching Apw.conll/apw_eng_200901.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200901.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200901.raw.json
3.18 minutes on apw_eng_200901.conllu
-> searching Apw.conll/apw_eng_200902.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200902.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200902.raw.json
3.07 minutes on apw_eng_200902.conllu
-> searching Apw.conll/apw_eng_200903.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200903.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200903.raw.json
3.46 minutes on apw_eng_200903.conllu
-> searching Apw.conll/apw_eng_200904.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200904.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200904.raw.json
3.79 minutes on apw_eng_200904.conllu
-> searching Apw.conll/apw_eng_200905.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200905.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200905.raw.json
3.62 minutes on apw_eng_200905.conllu
-> searching Apw.conll/apw_eng_200906.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200906.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200906.raw.json
3.71 minutes on apw_eng_200906.conllu
-> searching Apw.conll/apw_eng_200907.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200907.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200907.raw.json
2.31 minutes on apw_eng_200907.conllu
-> searching Apw.conll/apw_eng_200908.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200908.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200908.raw.json
2.54 minutes on apw_eng_200908.conllu
-> searching Apw.conll/apw_eng_200909.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200909.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200909.raw.json
2.46 minutes on apw_eng_200909.conllu
-> searching Apw.conll/apw_eng_200910.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200910.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200910.raw.json
2.44 minutes on apw_eng_200910.conllu
-> searching Apw.conll/apw_eng_200911.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200911.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200911.raw.json
2.42 minutes on apw_eng_200911.conllu
-> searching Apw.conll/apw_eng_200912.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_200912.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_200912.raw.json
2.53 minutes on apw_eng_200912.conllu
-> searching Apw.conll/apw_eng_201001.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201001.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201001.raw.json
3.04 minutes on apw_eng_201001.conllu
-> searching Apw.conll/apw_eng_201002.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201002.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201002.raw.json
2.05 minutes on apw_eng_201002.conllu
-> searching Apw.conll/apw_eng_201003.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201003.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201003.raw.json
2.23 minutes on apw_eng_201003.conllu
-> searching Apw.conll/apw_eng_201004.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201004.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201004.raw.json
2.28 minutes on apw_eng_201004.conllu
-> searching Apw.conll/apw_eng_201005.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201005.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201005.raw.json
2.19 minutes on apw_eng_201005.conllu
-> searching Apw.conll/apw_eng_201006.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201006.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201006.raw.json
2.25 minutes on apw_eng_201006.conllu
-> searching Apw.conll/apw_eng_201007.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201007.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201007.raw.json
1.84 minutes on apw_eng_201007.conllu
-> searching Apw.conll/apw_eng_201008.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201008.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201008.raw.json
2.9 minutes on apw_eng_201008.conllu
-> searching Apw.conll/apw_eng_201009.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201009.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201009.raw.json
3.27 minutes on apw_eng_201009.conllu
-> searching Apw.conll/apw_eng_201010.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201010.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201010.raw.json
3.25 minutes on apw_eng_201010.conllu
-> searching Apw.conll/apw_eng_201011.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201011.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201011.raw.json
3.5 minutes on apw_eng_201011.conllu
-> searching Apw.conll/apw_eng_201012.conllu:
grew grep -pattern Pat/neg-mit/almost-no-one_subj.pat -i Apw.conll/apw_eng_201012.conllu > data/neg-mit/Apw.almost-no-one_subj/apw_eng_201012.raw.json
2.83 minutes on apw_eng_201012.conllu

Total grew search time: 587.41 minutes
==============================================

```
### Running `FillJson.py` script on json files in `Apw.almost-no-one_subj` from conll files in `Apw.conll`...
```
-> Processing apw_eng_200608...
-> Skipping. (file is empty)
-> Processing apw_eng_200605...
-> Skipping. (file is empty)
-> Processing apw_eng_200708...
-> Skipping. (file is empty)
-> Processing apw_eng_200601...
-> Skipping. (file is empty)
-> Processing apw_eng_199905...
-> Skipping. (file is empty)
-> Processing apw_eng_200012...
-> Skipping. (file is empty)
-> Processing apw_eng_200701...
-> Skipping. (file is empty)
-> Processing apw_eng_200309...
-> Skipping. (file is empty)
-> Processing apw_eng_200902...
-> Skipping. (file is empty)
-> Processing apw_eng_199706...
-> Skipping. (file is empty)
-> Processing apw_eng_199508...
-> Skipping. (file is empty)
-> Processing apw_eng_201009...
-> Skipping. (file is empty)
-> Processing apw_eng_200906...
-> Skipping. (file is empty)
-> Processing apw_eng_199805...
-> Skipping. (file is empty)
-> Processing apw_eng_200808...
-> Skipping. (file is empty)
-> Processing apw_eng_200306...
-> Skipping. (file is empty)
-> Processing apw_eng_199604...
-> Skipping. (file is empty)
-> Processing apw_eng_200505...
-> Skipping. (file is empty)
-> Processing apw_eng_199904...
-> Skipping. (file is empty)
-> Processing apw_eng_200102...
-> Skipping. (file is empty)
-> Processing apw_eng_200209...
-> Skipping. (file is empty)
-> Processing apw_eng_200512...
-> Skipping. (file is empty)
-> Processing apw_eng_201010...
-> Skipping. (file is empty)
-> Processing apw_eng_199708...
-> Skipping. (file is empty)
-> Processing apw_eng_200503...
-> Skipping. (file is empty)
-> Processing apw_eng_200508...
-> Skipping. (file is empty)
-> Processing apw_eng_200305...
-> Skipping. (file is empty)
-> Processing apw_eng_200104...
-> Skipping. (file is empty)
-> Processing apw_eng_200408...
-> Skipping. (file is empty)
-> Processing apw_eng_200006...
-> Skipping. (file is empty)
-> Processing apw_eng_199512...
-> Skipping. (file is empty)
-> Processing apw_eng_199809...
-> Skipping. (file is empty)
-> Processing apw_eng_200711...
-> Skipping. (file is empty)
-> Processing apw_eng_200804...
-> Skipping. (file is empty)
-> Processing apw_eng_200506...
-> Skipping. (file is empty)
-> Processing apw_eng_199411...
-> Skipping. (file is empty)
-> Processing apw_eng_199507...
-> Skipping. (file is empty)
-> Processing apw_eng_200205...
-> Skipping. (file is empty)
-> Processing apw_eng_200507...
-> Skipping. (file is empty)
-> Processing apw_eng_201003...
-> Skipping. (file is empty)
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
-> Processing apw_eng_200907...
-> Skipping. (file is empty)
-> Processing apw_eng_199611...
-> Skipping. (file is empty)
-> Processing apw_eng_199504...
-> Skipping. (file is empty)
-> Processing apw_eng_199909...
-> Skipping. (file is empty)
-> Processing apw_eng_200301...
-> Skipping. (file is empty)
-> Processing apw_eng_200109...
-> Skipping. (file is empty)
-> Processing apw_eng_199710...
-> Skipping. (file is empty)
-> Processing apw_eng_199901...
-> Skipping. (file is empty)
-> Processing apw_eng_200409...
-> Skipping. (file is empty)
-> Processing apw_eng_199605...
-> Skipping. (file is empty)
-> Processing apw_eng_200510...
-> Skipping. (file is empty)
-> Processing apw_eng_200304...
-> Skipping. (file is empty)
-> Processing apw_eng_200905...
-> Skipping. (file is empty)
-> Processing apw_eng_201002...
-> Skipping. (file is empty)
-> Processing apw_eng_200302...
-> Skipping. (file is empty)
-> Processing apw_eng_200405...
-> Skipping. (file is empty)
-> Processing apw_eng_200703...
-> Skipping. (file is empty)
-> Processing apw_eng_199711...
-> Skipping. (file is empty)
-> Processing apw_eng_200909...
-> Skipping. (file is empty)
-> Processing apw_eng_199612...
-> Skipping. (file is empty)
-> Processing apw_eng_201005...
-> Skipping. (file is empty)
-> Processing apw_eng_201011...
-> Skipping. (file is empty)
-> Processing apw_eng_200311...
-> Skipping. (file is empty)
-> Processing apw_eng_200609...
-> Skipping. (file is empty)
-> Processing apw_eng_199704...
-> Skipping. (file is empty)
-> Processing apw_eng_200207...
-> Skipping. (file is empty)
-> Processing apw_eng_199509...
-> Skipping. (file is empty)
-> Processing apw_eng_199810...
-> Skipping. (file is empty)
-> Processing apw_eng_200502...
-> Skipping. (file is empty)
-> Processing apw_eng_200009...
-> Skipping. (file is empty)
-> Processing apw_eng_200011...
-> Skipping. (file is empty)
-> Processing apw_eng_200112...
-> Skipping. (file is empty)
-> Processing apw_eng_199603...
-> Skipping. (file is empty)
-> Processing apw_eng_200602...
-> Skipping. (file is empty)
-> Processing apw_eng_199804...
-> Skipping. (file is empty)
-> Processing apw_eng_200712...
-> Skipping. (file is empty)
-> Processing apw_eng_200010...
-> Skipping. (file is empty)
-> Processing apw_eng_200702...
-> Skipping. (file is empty)
-> Processing apw_eng_200406...
-> Skipping. (file is empty)
-> Processing apw_eng_200003...
-> Skipping. (file is empty)
-> Processing apw_eng_200208...
-> Skipping. (file is empty)
-> Processing apw_eng_199807...
-> Skipping. (file is empty)
-> Processing apw_eng_200308...
-> Skipping. (file is empty)
-> Processing apw_eng_200008...
-> Skipping. (file is empty)
-> Processing apw_eng_200307...
-> Skipping. (file is empty)
-> Processing apw_eng_200509...
-> Skipping. (file is empty)
-> Processing apw_eng_200501...
-> Skipping. (file is empty)
-> Processing apw_eng_200710...
-> Skipping. (file is empty)
-> Processing apw_eng_200807...
-> Skipping. (file is empty)
-> Processing apw_eng_200908...
-> Skipping. (file is empty)
-> Processing apw_eng_199505...
-> Skipping. (file is empty)
-> Processing apw_eng_199910...
-> Skipping. (file is empty)
-> Processing apw_eng_199906...
-> Skipping. (file is empty)
-> Processing apw_eng_200401...
-> Skipping. (file is empty)
-> Processing apw_eng_199602...
-> Skipping. (file is empty)
-> Processing apw_eng_199601...
-> Skipping. (file is empty)
-> Processing apw_eng_199703...
-> Skipping. (file is empty)
-> Processing apw_eng_200811...
-> Skipping. (file is empty)
-> Processing apw_eng_200312...
-> Skipping. (file is empty)
-> Processing apw_eng_200211...
-> Skipping. (file is empty)
-> Processing apw_eng_200411...
-> Skipping. (file is empty)
-> Processing apw_eng_201007...
-> Skipping. (file is empty)
-> Processing apw_eng_200106...
-> Skipping. (file is empty)
-> Processing apw_eng_200404...
-> Skipping. (file is empty)
-> Processing apw_eng_200709...
-> Skipping. (file is empty)
-> Processing apw_eng_201006...
-> Skipping. (file is empty)
-> Processing apw_eng_200007...
-> Skipping. (file is empty)
-> Processing apw_eng_200107...
-> Skipping. (file is empty)
-> Processing apw_eng_199707...
-> Skipping. (file is empty)
-> Processing apw_eng_200802...
-> Skipping. (file is empty)
-> Processing apw_eng_200606...
-> Skipping. (file is empty)
-> Processing apw_eng_200903...
-> Skipping. (file is empty)
-> Processing apw_eng_199510...
-> Skipping. (file is empty)
-> Processing apw_eng_200806...
-> Skipping. (file is empty)
-> Processing apw_eng_199608...
-> Skipping. (file is empty)
-> Processing apw_eng_199610...
-> Skipping. (file is empty)
-> Processing apw_eng_200805...
-> Skipping. (file is empty)
-> Processing apw_eng_199511...
-> Skipping. (file is empty)
-> Processing apw_eng_200604...
-> Skipping. (file is empty)
-> Processing apw_eng_199709...
-> Skipping. (file is empty)
-> Processing apw_eng_199609...
-> Skipping. (file is empty)
-> Processing apw_eng_200005...
-> Skipping. (file is empty)
-> Processing apw_eng_200812...
-> Skipping. (file is empty)
-> Processing apw_eng_200108...
-> Skipping. (file is empty)
-> Processing apw_eng_200206...
-> Skipping. (file is empty)
-> Processing apw_eng_199907...
-> Skipping. (file is empty)
-> Processing apw_eng_199908...
-> Skipping. (file is empty)
-> Processing apw_eng_200403...
-> Skipping. (file is empty)
-> Processing apw_eng_200204...
-> Skipping. (file is empty)
-> Processing apw_eng_200110...
-> Skipping. (file is empty)
-> Processing apw_eng_200910...
-> Skipping. (file is empty)
-> Processing apw_eng_199503...
-> Skipping. (file is empty)
-> Processing apw_eng_200607...
-> Skipping. (file is empty)
-> Processing apw_eng_199902...
-> Skipping. (file is empty)
-> Processing apw_eng_200706...
-> Skipping. (file is empty)
-> Processing apw_eng_200610...
-> Skipping. (file is empty)
-> Processing apw_eng_200612...
-> Skipping. (file is empty)
-> Processing apw_eng_200810...
-> Skipping. (file is empty)
-> Processing apw_eng_200212...
-> Skipping. (file is empty)
-> Processing apw_eng_201004...
-> Skipping. (file is empty)
-> Processing apw_eng_199803...
-> Skipping. (file is empty)
-> Processing apw_eng_199701...
-> Skipping. (file is empty)
-> Processing apw_eng_200603...
-> Skipping. (file is empty)
-> Processing apw_eng_200705...
-> Skipping. (file is empty)
-> Processing apw_eng_200904...
-> Skipping. (file is empty)
-> Processing apw_eng_201008...
-> Skipping. (file is empty)
-> Processing apw_eng_200002...
-> Skipping. (file is empty)
-> Processing apw_eng_200105...
-> Skipping. (file is empty)
-> Processing apw_eng_200203...
-> Skipping. (file is empty)
-> Processing apw_eng_200210...
-> Skipping. (file is empty)
-> Processing apw_eng_201001...
-> Skipping. (file is empty)
-> Processing apw_eng_199412...
-> Skipping. (file is empty)
-> Processing apw_eng_199712...
-> Skipping. (file is empty)
-> Processing apw_eng_200111...
-> Skipping. (file is empty)
-> Processing apw_eng_200402...
-> Skipping. (file is empty)
-> Processing apw_eng_199811...
-> Skipping. (file is empty)
-> Processing apw_eng_200504...
-> Skipping. (file is empty)
-> Processing apw_eng_200001...
-> Skipping. (file is empty)
-> Processing apw_eng_199802...
-> Skipping. (file is empty)
-> Processing apw_eng_199606...
-> Skipping. (file is empty)
-> Processing apw_eng_200911...
-> Skipping. (file is empty)
-> Processing apw_eng_200004...
-> Skipping. (file is empty)
-> Processing apw_eng_201012...
-> Skipping. (file is empty)
-> Processing apw_eng_199502...
-> Skipping. (file is empty)
-> Processing apw_eng_199705...
-> Skipping. (file is empty)
-> Processing apw_eng_200303...
-> Skipping. (file is empty)
-> Processing apw_eng_200202...
-> Skipping. (file is empty)
-> Processing apw_eng_199607...
-> Skipping. (file is empty)
-> Processing apw_eng_200901...
-> Skipping. (file is empty)
-> Processing apw_eng_200511...
-> Skipping. (file is empty)
-> Processing apw_eng_199801...
-> Skipping. (file is empty)
-> Processing apw_eng_200809...
-> Skipping. (file is empty)
-> Processing apw_eng_200101...
-> Skipping. (file is empty)
-> Processing apw_eng_199812...
-> Skipping. (file is empty)
-> Processing apw_eng_199806...
-> Skipping. (file is empty)
-> Processing apw_eng_200704...
-> Skipping. (file is empty)
-> Processing apw_eng_200801...
-> Skipping. (file is empty)
-> Processing apw_eng_199903...
-> Skipping. (file is empty)
-> Processing apw_eng_199702...
-> Skipping. (file is empty)
-> Processing apw_eng_200103...
-> Skipping. (file is empty)
-> Processing apw_eng_200407...
-> Skipping. (file is empty)
-> Processing apw_eng_200412...
-> Skipping. (file is empty)
-> Processing apw_eng_200310...
-> Skipping. (file is empty)
-> Processing apw_eng_200201...
-> Skipping. (file is empty)
-> Processing apw_eng_200410...
-> Skipping. (file is empty)
-> Processing apw_eng_200611...
-> Skipping. (file is empty)
-> Processing apw_eng_199501...
-> Skipping. (file is empty)
-> Processing apw_eng_200707...
-> Skipping. (file is empty)
-> Processing apw_eng_199808...
-> Skipping. (file is empty)
-> Processing apw_eng_200912...
-> Skipping. (file is empty)
-> Processing apw_eng_199506...
-> Skipping. (file is empty)
-> Processing apw_eng_200803...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.01 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `almost-no_det-of-subj`
- time stamp: `Wed Aug  4 00:54:44 EDT 2021`
- data directory: `data/neg-mit/Apw.almost-no_det-of-subj`
- hits table: `hits/neg-mit/Apw_almost-no_det-of-subj`
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
 WARNING : [Conll, File Apw.conll/apw_eng_199608.conllu] No blank line at the end of the file
```
### Running grew search on `Apw.conll`...
```
193 total file(s) to be searched.
-> searching Apw.conll/apw_eng_199411.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199411.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199411.raw.json
1.71 minutes on apw_eng_199411.conllu
-> searching Apw.conll/apw_eng_199412.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199412.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199412.raw.json
2.46 minutes on apw_eng_199412.conllu
-> searching Apw.conll/apw_eng_199501.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199501.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199501.raw.json
2.58 minutes on apw_eng_199501.conllu
-> searching Apw.conll/apw_eng_199502.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199502.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199502.raw.json
2.21 minutes on apw_eng_199502.conllu
-> searching Apw.conll/apw_eng_199503.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199503.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199503.raw.json
2.66 minutes on apw_eng_199503.conllu
-> searching Apw.conll/apw_eng_199504.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199504.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199504.raw.json
2.53 minutes on apw_eng_199504.conllu
-> searching Apw.conll/apw_eng_199505.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199505.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199505.raw.json
3.21 minutes on apw_eng_199505.conllu
-> searching Apw.conll/apw_eng_199506.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199506.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199506.raw.json
3.41 minutes on apw_eng_199506.conllu
-> searching Apw.conll/apw_eng_199507.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199507.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199507.raw.json
3.14 minutes on apw_eng_199507.conllu
-> searching Apw.conll/apw_eng_199508.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199508.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199508.raw.json
3.19 minutes on apw_eng_199508.conllu
-> searching Apw.conll/apw_eng_199509.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199509.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199509.raw.json
2.98 minutes on apw_eng_199509.conllu
-> searching Apw.conll/apw_eng_199510.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199510.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199510.raw.json
2.14 minutes on apw_eng_199510.conllu
-> searching Apw.conll/apw_eng_199511.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199511.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199511.raw.json
2.1 minutes on apw_eng_199511.conllu
-> searching Apw.conll/apw_eng_199512.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199512.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199512.raw.json
1.99 minutes on apw_eng_199512.conllu
-> searching Apw.conll/apw_eng_199601.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199601.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199601.raw.json
2.11 minutes on apw_eng_199601.conllu
-> searching Apw.conll/apw_eng_199602.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199602.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199602.raw.json
1.94 minutes on apw_eng_199602.conllu
-> searching Apw.conll/apw_eng_199603.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199603.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199603.raw.json
2.26 minutes on apw_eng_199603.conllu
-> searching Apw.conll/apw_eng_199604.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199604.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199604.raw.json
2.18 minutes on apw_eng_199604.conllu
-> searching Apw.conll/apw_eng_199605.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199605.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199605.raw.json
2.18 minutes on apw_eng_199605.conllu
-> searching Apw.conll/apw_eng_199606.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199606.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199606.raw.json
1.87 minutes on apw_eng_199606.conllu
-> searching Apw.conll/apw_eng_199607.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199607.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199607.raw.json
2.03 minutes on apw_eng_199607.conllu
-> searching Apw.conll/apw_eng_199608.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199608.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199608.raw.json
1.65 minutes on apw_eng_199608.conllu
-> searching Apw.conll/apw_eng_199609.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199609.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199609.raw.json
1.91 minutes on apw_eng_199609.conllu
-> searching Apw.conll/apw_eng_199610.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199610.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199610.raw.json
2.01 minutes on apw_eng_199610.conllu
-> searching Apw.conll/apw_eng_199611.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199611.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199611.raw.json
2.04 minutes on apw_eng_199611.conllu
-> searching Apw.conll/apw_eng_199612.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199612.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199612.raw.json
2.1 minutes on apw_eng_199612.conllu
-> searching Apw.conll/apw_eng_199701.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199701.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199701.raw.json
2.3 minutes on apw_eng_199701.conllu
-> searching Apw.conll/apw_eng_199702.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199702.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199702.raw.json
2.11 minutes on apw_eng_199702.conllu
-> searching Apw.conll/apw_eng_199703.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199703.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199703.raw.json
2.49 minutes on apw_eng_199703.conllu
-> searching Apw.conll/apw_eng_199704.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199704.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199704.raw.json
2.34 minutes on apw_eng_199704.conllu
-> searching Apw.conll/apw_eng_199705.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199705.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199705.raw.json
2.4 minutes on apw_eng_199705.conllu
-> searching Apw.conll/apw_eng_199706.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199706.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199706.raw.json
2.32 minutes on apw_eng_199706.conllu
-> searching Apw.conll/apw_eng_199707.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199707.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199707.raw.json
2.45 minutes on apw_eng_199707.conllu
-> searching Apw.conll/apw_eng_199708.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199708.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199708.raw.json
2.31 minutes on apw_eng_199708.conllu
-> searching Apw.conll/apw_eng_199709.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199709.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199709.raw.json
2.46 minutes on apw_eng_199709.conllu
-> searching Apw.conll/apw_eng_199710.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199710.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199710.raw.json
2.45 minutes on apw_eng_199710.conllu
-> searching Apw.conll/apw_eng_199711.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199711.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199711.raw.json
2.88 minutes on apw_eng_199711.conllu
-> searching Apw.conll/apw_eng_199712.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199712.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199712.raw.json
3.76 minutes on apw_eng_199712.conllu
-> searching Apw.conll/apw_eng_199801.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199801.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199801.raw.json
3.99 minutes on apw_eng_199801.conllu
-> searching Apw.conll/apw_eng_199802.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199802.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199802.raw.json
4.11 minutes on apw_eng_199802.conllu
-> searching Apw.conll/apw_eng_199803.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199803.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199803.raw.json
4.35 minutes on apw_eng_199803.conllu
-> searching Apw.conll/apw_eng_199804.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199804.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199804.raw.json
4.2 minutes on apw_eng_199804.conllu
-> searching Apw.conll/apw_eng_199805.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199805.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199805.raw.json
4.18 minutes on apw_eng_199805.conllu
-> searching Apw.conll/apw_eng_199806.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199806.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199806.raw.json
3.8 minutes on apw_eng_199806.conllu
-> searching Apw.conll/apw_eng_199807.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199807.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199807.raw.json
2.45 minutes on apw_eng_199807.conllu
-> searching Apw.conll/apw_eng_199808.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199808.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199808.raw.json
2.37 minutes on apw_eng_199808.conllu
-> searching Apw.conll/apw_eng_199809.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199809.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199809.raw.json
2.59 minutes on apw_eng_199809.conllu
-> searching Apw.conll/apw_eng_199810.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199810.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199810.raw.json
2.64 minutes on apw_eng_199810.conllu
-> searching Apw.conll/apw_eng_199811.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199811.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199811.raw.json
2.47 minutes on apw_eng_199811.conllu
-> searching Apw.conll/apw_eng_199812.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199812.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199812.raw.json
2.93 minutes on apw_eng_199812.conllu
-> searching Apw.conll/apw_eng_199901.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199901.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199901.raw.json
2.67 minutes on apw_eng_199901.conllu
-> searching Apw.conll/apw_eng_199902.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199902.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199902.raw.json
2.71 minutes on apw_eng_199902.conllu
-> searching Apw.conll/apw_eng_199903.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199903.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199903.raw.json
3.18 minutes on apw_eng_199903.conllu
-> searching Apw.conll/apw_eng_199904.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199904.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199904.raw.json
2.94 minutes on apw_eng_199904.conllu
-> searching Apw.conll/apw_eng_199905.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199905.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199905.raw.json
3.01 minutes on apw_eng_199905.conllu
-> searching Apw.conll/apw_eng_199906.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199906.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199906.raw.json
3.13 minutes on apw_eng_199906.conllu
-> searching Apw.conll/apw_eng_199907.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199907.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199907.raw.json
2.84 minutes on apw_eng_199907.conllu
-> searching Apw.conll/apw_eng_199908.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199908.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199908.raw.json
1.89 minutes on apw_eng_199908.conllu
-> searching Apw.conll/apw_eng_199909.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199909.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199909.raw.json
1.59 minutes on apw_eng_199909.conllu
-> searching Apw.conll/apw_eng_199910.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199910.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199910.raw.json
1.88 minutes on apw_eng_199910.conllu
-> searching Apw.conll/apw_eng_199911.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_199911.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching Apw.conll/apw_eng_200001.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200001.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200001.raw.json
1.91 minutes on apw_eng_200001.conllu
-> searching Apw.conll/apw_eng_200002.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200002.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200002.raw.json
1.72 minutes on apw_eng_200002.conllu
-> searching Apw.conll/apw_eng_200003.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200003.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200003.raw.json
1.43 minutes on apw_eng_200003.conllu
-> searching Apw.conll/apw_eng_200004.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200004.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200004.raw.json
1.23 minutes on apw_eng_200004.conllu
-> searching Apw.conll/apw_eng_200005.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200005.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200005.raw.json
1.36 minutes on apw_eng_200005.conllu
-> searching Apw.conll/apw_eng_200006.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200006.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200006.raw.json
1.18 minutes on apw_eng_200006.conllu
-> searching Apw.conll/apw_eng_200007.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200007.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200007.raw.json
1.18 minutes on apw_eng_200007.conllu
-> searching Apw.conll/apw_eng_200008.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200008.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200008.raw.json
1.08 minutes on apw_eng_200008.conllu
-> searching Apw.conll/apw_eng_200009.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200009.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200009.raw.json
1.17 minutes on apw_eng_200009.conllu
-> searching Apw.conll/apw_eng_200010.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200010.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200010.raw.json
4.75 minutes on apw_eng_200010.conllu
-> searching Apw.conll/apw_eng_200011.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200011.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200011.raw.json
5.31 minutes on apw_eng_200011.conllu
-> searching Apw.conll/apw_eng_200012.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200012.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200012.raw.json
4.9 minutes on apw_eng_200012.conllu
-> searching Apw.conll/apw_eng_200101.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200101.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200101.raw.json
5.03 minutes on apw_eng_200101.conllu
-> searching Apw.conll/apw_eng_200102.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200102.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200102.raw.json
4.3 minutes on apw_eng_200102.conllu
-> searching Apw.conll/apw_eng_200103.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200103.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200103.raw.json
5.19 minutes on apw_eng_200103.conllu
-> searching Apw.conll/apw_eng_200104.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200104.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200104.raw.json
4.99 minutes on apw_eng_200104.conllu
-> searching Apw.conll/apw_eng_200105.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200105.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200105.raw.json
5.35 minutes on apw_eng_200105.conllu
-> searching Apw.conll/apw_eng_200106.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200106.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200106.raw.json
5.46 minutes on apw_eng_200106.conllu
-> searching Apw.conll/apw_eng_200107.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200107.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200107.raw.json
5.21 minutes on apw_eng_200107.conllu
-> searching Apw.conll/apw_eng_200108.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200108.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200108.raw.json
2.99 minutes on apw_eng_200108.conllu
-> searching Apw.conll/apw_eng_200109.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200109.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200109.raw.json
4.04 minutes on apw_eng_200109.conllu
-> searching Apw.conll/apw_eng_200110.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200110.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200110.raw.json
4.07 minutes on apw_eng_200110.conllu
-> searching Apw.conll/apw_eng_200111.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200111.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200111.raw.json
3.68 minutes on apw_eng_200111.conllu
-> searching Apw.conll/apw_eng_200112.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200112.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200112.raw.json
3.41 minutes on apw_eng_200112.conllu
-> searching Apw.conll/apw_eng_200201.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200201.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200201.raw.json
3.79 minutes on apw_eng_200201.conllu
-> searching Apw.conll/apw_eng_200202.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200202.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200202.raw.json
3.63 minutes on apw_eng_200202.conllu
-> searching Apw.conll/apw_eng_200203.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200203.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200203.raw.json
4.1 minutes on apw_eng_200203.conllu
-> searching Apw.conll/apw_eng_200204.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200204.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200204.raw.json
4.19 minutes on apw_eng_200204.conllu
-> searching Apw.conll/apw_eng_200205.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200205.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200205.raw.json
4.21 minutes on apw_eng_200205.conllu
-> searching Apw.conll/apw_eng_200206.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200206.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200206.raw.json
4.17 minutes on apw_eng_200206.conllu
-> searching Apw.conll/apw_eng_200207.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200207.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200207.raw.json
4.12 minutes on apw_eng_200207.conllu
-> searching Apw.conll/apw_eng_200208.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200208.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200208.raw.json
3.69 minutes on apw_eng_200208.conllu
-> searching Apw.conll/apw_eng_200209.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200209.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200209.raw.json
4.02 minutes on apw_eng_200209.conllu
-> searching Apw.conll/apw_eng_200210.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200210.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200210.raw.json
4.45 minutes on apw_eng_200210.conllu
-> searching Apw.conll/apw_eng_200211.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200211.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200211.raw.json
3.91 minutes on apw_eng_200211.conllu
-> searching Apw.conll/apw_eng_200212.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200212.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200212.raw.json
2.99 minutes on apw_eng_200212.conllu
-> searching Apw.conll/apw_eng_200301.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200301.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200301.raw.json
4.18 minutes on apw_eng_200301.conllu
-> searching Apw.conll/apw_eng_200302.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200302.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200302.raw.json
4.23 minutes on apw_eng_200302.conllu
-> searching Apw.conll/apw_eng_200303.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200303.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200303.raw.json
5.12 minutes on apw_eng_200303.conllu
-> searching Apw.conll/apw_eng_200304.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200304.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200304.raw.json
4.35 minutes on apw_eng_200304.conllu
-> searching Apw.conll/apw_eng_200305.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200305.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200305.raw.json
4.2 minutes on apw_eng_200305.conllu
-> searching Apw.conll/apw_eng_200306.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200306.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200306.raw.json
3.39 minutes on apw_eng_200306.conllu
-> searching Apw.conll/apw_eng_200307.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200307.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200307.raw.json
1.4 minutes on apw_eng_200307.conllu
-> searching Apw.conll/apw_eng_200308.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200308.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200308.raw.json
3.97 minutes on apw_eng_200308.conllu
-> searching Apw.conll/apw_eng_200309.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200309.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200309.raw.json
4.55 minutes on apw_eng_200309.conllu
-> searching Apw.conll/apw_eng_200310.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200310.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200310.raw.json
5.25 minutes on apw_eng_200310.conllu
-> searching Apw.conll/apw_eng_200311.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200311.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200311.raw.json
4.56 minutes on apw_eng_200311.conllu
-> searching Apw.conll/apw_eng_200312.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200312.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200312.raw.json
4.18 minutes on apw_eng_200312.conllu
-> searching Apw.conll/apw_eng_200401.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200401.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200401.raw.json
2.45 minutes on apw_eng_200401.conllu
-> searching Apw.conll/apw_eng_200402.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200402.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200402.raw.json
3.37 minutes on apw_eng_200402.conllu
-> searching Apw.conll/apw_eng_200403.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200403.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200403.raw.json
5.44 minutes on apw_eng_200403.conllu
-> searching Apw.conll/apw_eng_200404.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200404.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200404.raw.json
4.72 minutes on apw_eng_200404.conllu
-> searching Apw.conll/apw_eng_200405.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200405.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200405.raw.json
0.94 minutes on apw_eng_200405.conllu
-> searching Apw.conll/apw_eng_200406.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200406.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200406.raw.json
0.9 minutes on apw_eng_200406.conllu
-> searching Apw.conll/apw_eng_200407.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200407.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200407.raw.json
2.16 minutes on apw_eng_200407.conllu
-> searching Apw.conll/apw_eng_200408.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200408.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200408.raw.json
1.88 minutes on apw_eng_200408.conllu
-> searching Apw.conll/apw_eng_200409.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200409.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200409.raw.json
2.02 minutes on apw_eng_200409.conllu
-> searching Apw.conll/apw_eng_200410.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200410.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200410.raw.json
2.32 minutes on apw_eng_200410.conllu
-> searching Apw.conll/apw_eng_200411.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200411.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200411.raw.json
1.69 minutes on apw_eng_200411.conllu
-> searching Apw.conll/apw_eng_200412.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200412.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200412.raw.json
0.61 minutes on apw_eng_200412.conllu
-> searching Apw.conll/apw_eng_200501.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200501.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200501.raw.json
1.73 minutes on apw_eng_200501.conllu
-> searching Apw.conll/apw_eng_200502.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200502.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200502.raw.json
1.5 minutes on apw_eng_200502.conllu
-> searching Apw.conll/apw_eng_200503.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200503.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200503.raw.json
2.33 minutes on apw_eng_200503.conllu
-> searching Apw.conll/apw_eng_200504.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200504.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200504.raw.json
1.62 minutes on apw_eng_200504.conllu
-> searching Apw.conll/apw_eng_200505.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200505.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200505.raw.json
2.11 minutes on apw_eng_200505.conllu
-> searching Apw.conll/apw_eng_200506.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200506.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200506.raw.json
2.27 minutes on apw_eng_200506.conllu
-> searching Apw.conll/apw_eng_200507.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200507.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200507.raw.json
1.56 minutes on apw_eng_200507.conllu
-> searching Apw.conll/apw_eng_200508.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200508.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200508.raw.json
1.97 minutes on apw_eng_200508.conllu
-> searching Apw.conll/apw_eng_200509.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200509.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200509.raw.json
2.47 minutes on apw_eng_200509.conllu
-> searching Apw.conll/apw_eng_200510.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200510.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200510.raw.json
2.3 minutes on apw_eng_200510.conllu
-> searching Apw.conll/apw_eng_200511.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200511.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200511.raw.json
2.31 minutes on apw_eng_200511.conllu
-> searching Apw.conll/apw_eng_200512.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200512.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200512.raw.json
2.28 minutes on apw_eng_200512.conllu
-> searching Apw.conll/apw_eng_200601.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200601.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200601.raw.json
2.39 minutes on apw_eng_200601.conllu
-> searching Apw.conll/apw_eng_200602.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200602.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200602.raw.json
1.93 minutes on apw_eng_200602.conllu
-> searching Apw.conll/apw_eng_200603.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200603.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200603.raw.json
2.61 minutes on apw_eng_200603.conllu
-> searching Apw.conll/apw_eng_200604.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200604.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200604.raw.json
1.97 minutes on apw_eng_200604.conllu
-> searching Apw.conll/apw_eng_200605.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200605.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200605.raw.json
2.64 minutes on apw_eng_200605.conllu
-> searching Apw.conll/apw_eng_200606.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200606.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200606.raw.json
2.41 minutes on apw_eng_200606.conllu
-> searching Apw.conll/apw_eng_200607.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200607.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200607.raw.json
2.36 minutes on apw_eng_200607.conllu
-> searching Apw.conll/apw_eng_200608.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200608.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200608.raw.json
2.1 minutes on apw_eng_200608.conllu
-> searching Apw.conll/apw_eng_200609.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200609.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200609.raw.json
2.06 minutes on apw_eng_200609.conllu
-> searching Apw.conll/apw_eng_200610.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200610.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200610.raw.json
4.94 minutes on apw_eng_200610.conllu
-> searching Apw.conll/apw_eng_200611.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200611.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200611.raw.json
5.03 minutes on apw_eng_200611.conllu
-> searching Apw.conll/apw_eng_200612.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200612.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200612.raw.json
1.68 minutes on apw_eng_200612.conllu
-> searching Apw.conll/apw_eng_200701.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200701.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200701.raw.json
4.89 minutes on apw_eng_200701.conllu
-> searching Apw.conll/apw_eng_200702.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200702.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200702.raw.json
4.51 minutes on apw_eng_200702.conllu
-> searching Apw.conll/apw_eng_200703.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200703.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200703.raw.json
5.12 minutes on apw_eng_200703.conllu
-> searching Apw.conll/apw_eng_200704.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200704.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200704.raw.json
4.64 minutes on apw_eng_200704.conllu
-> searching Apw.conll/apw_eng_200705.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200705.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200705.raw.json
4.93 minutes on apw_eng_200705.conllu
-> searching Apw.conll/apw_eng_200706.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200706.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200706.raw.json
4.56 minutes on apw_eng_200706.conllu
-> searching Apw.conll/apw_eng_200707.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200707.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200707.raw.json
4.48 minutes on apw_eng_200707.conllu
-> searching Apw.conll/apw_eng_200708.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200708.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200708.raw.json
4.52 minutes on apw_eng_200708.conllu
-> searching Apw.conll/apw_eng_200709.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200709.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200709.raw.json
4.67 minutes on apw_eng_200709.conllu
-> searching Apw.conll/apw_eng_200710.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200710.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200710.raw.json
4.6 minutes on apw_eng_200710.conllu
-> searching Apw.conll/apw_eng_200711.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200711.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200711.raw.json
4.26 minutes on apw_eng_200711.conllu
-> searching Apw.conll/apw_eng_200712.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200712.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200712.raw.json
3.58 minutes on apw_eng_200712.conllu
-> searching Apw.conll/apw_eng_200801.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200801.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200801.raw.json
4.52 minutes on apw_eng_200801.conllu
-> searching Apw.conll/apw_eng_200802.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200802.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200802.raw.json
4.34 minutes on apw_eng_200802.conllu
-> searching Apw.conll/apw_eng_200803.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200803.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200803.raw.json
4.52 minutes on apw_eng_200803.conllu
-> searching Apw.conll/apw_eng_200804.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200804.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200804.raw.json
4.28 minutes on apw_eng_200804.conllu
-> searching Apw.conll/apw_eng_200805.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200805.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200805.raw.json
4.4 minutes on apw_eng_200805.conllu
-> searching Apw.conll/apw_eng_200806.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200806.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200806.raw.json
4.45 minutes on apw_eng_200806.conllu
-> searching Apw.conll/apw_eng_200807.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200807.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200807.raw.json
3.87 minutes on apw_eng_200807.conllu
-> searching Apw.conll/apw_eng_200808.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200808.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200808.raw.json
3.96 minutes on apw_eng_200808.conllu
-> searching Apw.conll/apw_eng_200809.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200809.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200809.raw.json
4.05 minutes on apw_eng_200809.conllu
-> searching Apw.conll/apw_eng_200810.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200810.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200810.raw.json
3.73 minutes on apw_eng_200810.conllu
-> searching Apw.conll/apw_eng_200811.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200811.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200811.raw.json
3.0 minutes on apw_eng_200811.conllu
-> searching Apw.conll/apw_eng_200812.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200812.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200812.raw.json
2.49 minutes on apw_eng_200812.conllu
-> searching Apw.conll/apw_eng_200901.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200901.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200901.raw.json
3.21 minutes on apw_eng_200901.conllu
-> searching Apw.conll/apw_eng_200902.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200902.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200902.raw.json
3.16 minutes on apw_eng_200902.conllu
-> searching Apw.conll/apw_eng_200903.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200903.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200903.raw.json
3.34 minutes on apw_eng_200903.conllu
-> searching Apw.conll/apw_eng_200904.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200904.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200904.raw.json
3.83 minutes on apw_eng_200904.conllu
-> searching Apw.conll/apw_eng_200905.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200905.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200905.raw.json
3.57 minutes on apw_eng_200905.conllu
-> searching Apw.conll/apw_eng_200906.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200906.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200906.raw.json
3.84 minutes on apw_eng_200906.conllu
-> searching Apw.conll/apw_eng_200907.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200907.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200907.raw.json
2.34 minutes on apw_eng_200907.conllu
-> searching Apw.conll/apw_eng_200908.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200908.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200908.raw.json
2.53 minutes on apw_eng_200908.conllu
-> searching Apw.conll/apw_eng_200909.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200909.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200909.raw.json
2.49 minutes on apw_eng_200909.conllu
-> searching Apw.conll/apw_eng_200910.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200910.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200910.raw.json
2.48 minutes on apw_eng_200910.conllu
-> searching Apw.conll/apw_eng_200911.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200911.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200911.raw.json
2.48 minutes on apw_eng_200911.conllu
-> searching Apw.conll/apw_eng_200912.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_200912.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_200912.raw.json
2.57 minutes on apw_eng_200912.conllu
-> searching Apw.conll/apw_eng_201001.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201001.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201001.raw.json
2.92 minutes on apw_eng_201001.conllu
-> searching Apw.conll/apw_eng_201002.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201002.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201002.raw.json
1.96 minutes on apw_eng_201002.conllu
-> searching Apw.conll/apw_eng_201003.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201003.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201003.raw.json
2.16 minutes on apw_eng_201003.conllu
-> searching Apw.conll/apw_eng_201004.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201004.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201004.raw.json
2.16 minutes on apw_eng_201004.conllu
-> searching Apw.conll/apw_eng_201005.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201005.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201005.raw.json
2.24 minutes on apw_eng_201005.conllu
-> searching Apw.conll/apw_eng_201006.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201006.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201006.raw.json
2.22 minutes on apw_eng_201006.conllu
-> searching Apw.conll/apw_eng_201007.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201007.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201007.raw.json
1.85 minutes on apw_eng_201007.conllu
-> searching Apw.conll/apw_eng_201008.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201008.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201008.raw.json
2.98 minutes on apw_eng_201008.conllu
-> searching Apw.conll/apw_eng_201009.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201009.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201009.raw.json
3.3 minutes on apw_eng_201009.conllu
-> searching Apw.conll/apw_eng_201010.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201010.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201010.raw.json
3.36 minutes on apw_eng_201010.conllu
-> searching Apw.conll/apw_eng_201011.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201011.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201011.raw.json
3.34 minutes on apw_eng_201011.conllu
-> searching Apw.conll/apw_eng_201012.conllu:
grew grep -pattern Pat/neg-mit/almost-no_det-of-subj.pat -i Apw.conll/apw_eng_201012.conllu > data/neg-mit/Apw.almost-no_det-of-subj/apw_eng_201012.raw.json
2.9 minutes on apw_eng_201012.conllu

Total grew search time: 589.06 minutes
==============================================

```
### Running `FillJson.py` script on json files in `Apw.almost-no_det-of-subj` from conll files in `Apw.conll`...
```
-> Processing apw_eng_200307...
-> Skipping. (file is empty)
-> Processing apw_eng_200308...
-> Skipping. (file is empty)
-> Processing apw_eng_200504...
-> Skipping. (file is empty)
-> Processing apw_eng_199509...
-> Skipping. (file is empty)
-> Processing apw_eng_199502...
-> Skipping. (file is empty)
-> Processing apw_eng_200911...
-> Skipping. (file is empty)
-> Processing apw_eng_199909...
-> Skipping. (file is empty)
-> Processing apw_eng_200608...
-> Skipping. (file is empty)
-> Processing apw_eng_199607...
-> Skipping. (file is empty)
-> Processing apw_eng_200511...
-> Skipping. (file is empty)
-> Processing apw_eng_200301...
-> Skipping. (file is empty)
-> Processing apw_eng_199506...
-> Skipping. (file is empty)
-> Processing apw_eng_200806...
-> Skipping. (file is empty)
-> Processing apw_eng_200107...
-> Skipping. (file is empty)
-> Processing apw_eng_199812...
-> Skipping. (file is empty)
-> Processing apw_eng_201009...
-> Skipping. (file is empty)
-> Processing apw_eng_200304...
-> Skipping. (file is empty)
-> Processing apw_eng_200302...
-> Skipping. (file is empty)
-> Processing apw_eng_200203...
-> Skipping. (file is empty)
-> Processing apw_eng_200310...
-> Skipping. (file is empty)
-> Processing apw_eng_199505...
-> Skipping. (file is empty)
-> Processing apw_eng_200404...
-> Skipping. (file is empty)
-> Processing apw_eng_200501...
-> Skipping. (file is empty)
-> Processing apw_eng_200709...
-> Skipping. (file is empty)
-> Processing apw_eng_201007...
-> Skipping. (file is empty)
-> Processing apw_eng_200410...
-> Skipping. (file is empty)
-> Processing apw_eng_199903...
-> Skipping. (file is empty)
-> Processing apw_eng_200904...
-> Skipping. (file is empty)
-> Processing apw_eng_199501...
-> Skipping. (file is empty)
-> Processing apw_eng_200805...
-> Skipping. (file is empty)
-> Processing apw_eng_200803...
-> Skipping. (file is empty)
-> Processing apw_eng_200906...
-> Skipping. (file is empty)
-> Processing apw_eng_200704...
-> Skipping. (file is empty)
-> Processing apw_eng_200611...
-> Skipping. (file is empty)
-> Processing apw_eng_199508...
-> Skipping. (file is empty)
-> Processing apw_eng_200902...
-> Skipping. (file is empty)
-> Processing apw_eng_199707...
-> Skipping. (file is empty)
-> Processing apw_eng_200405...
-> Skipping. (file is empty)
-> Processing apw_eng_199902...
-> Skipping. (file is empty)
-> Processing apw_eng_200406...
-> Skipping. (file is empty)
-> Processing apw_eng_199503...
-> Skipping. (file is empty)
-> Processing apw_eng_199910...
-> Skipping. (file is empty)
-> Processing apw_eng_200101...
-> Skipping. (file is empty)
-> Processing apw_eng_200809...
-> Skipping. (file is empty)
-> Processing apw_eng_199801...
-> Skipping. (file is empty)
-> Processing apw_eng_200006...
-> Skipping. (file is empty)
-> Processing apw_eng_199705...
-> Skipping. (file is empty)
-> Processing apw_eng_200204...
-> Skipping. (file is empty)
-> Processing apw_eng_200808...
-> Skipping. (file is empty)
-> Processing apw_eng_200412...
-> Skipping. (file is empty)
-> Processing apw_eng_199709...
-> Skipping. (file is empty)
-> Processing apw_eng_199905...
-> Skipping. (file is empty)
-> Processing apw_eng_200506...
-> Skipping. (file is empty)
-> Processing apw_eng_199810...
-> Skipping. (file is empty)
-> Processing apw_eng_199504...
-> Skipping. (file is empty)
-> Processing apw_eng_200905...
-> Skipping. (file is empty)
-> Processing apw_eng_200002...
-> Skipping. (file is empty)
-> Processing apw_eng_201010...
-> Skipping. (file is empty)
-> Processing apw_eng_200306...
-> Skipping. (file is empty)
-> Processing apw_eng_200711...
-> Skipping. (file is empty)
-> Processing apw_eng_199802...
-> Skipping. (file is empty)
-> Processing apw_eng_201005...
-> Skipping. (file is empty)
-> Processing apw_eng_200003...
-> Skipping. (file is empty)
-> Processing apw_eng_200205...
-> Skipping. (file is empty)
-> Processing apw_eng_200801...
-> Skipping. (file is empty)
-> Processing apw_eng_200804...
-> Skipping. (file is empty)
-> Processing apw_eng_200004...
-> Skipping. (file is empty)
-> Processing apw_eng_199602...
-> Skipping. (file is empty)
-> Processing apw_eng_200908...
-> Skipping. (file is empty)
-> Processing apw_eng_199809...
-> Skipping. (file is empty)
-> Processing apw_eng_200210...
-> Skipping. (file is empty)
-> Processing apw_eng_200109...
-> Skipping. (file is empty)
-> Processing apw_eng_200407...
-> Skipping. (file is empty)
-> Processing apw_eng_200104...
-> Skipping. (file is empty)
-> Processing apw_eng_200312...
-> Skipping. (file is empty)
-> Processing apw_eng_200403...
-> Skipping. (file is empty)
-> Processing apw_eng_200712...
-> Skipping. (file is empty)
-> Processing apw_eng_200010...
-> Skipping. (file is empty)
-> Processing apw_eng_199804...
-> Skipping. (file is empty)
-> Processing apw_eng_200303...
-> Skipping. (file is empty)
-> Processing apw_eng_200206...
-> Skipping. (file is empty)
-> Processing apw_eng_200606...
-> Skipping. (file is empty)
-> Processing apw_eng_200610...
-> Skipping. (file is empty)
-> Processing apw_eng_199703...
-> Skipping. (file is empty)
-> Processing apw_eng_200612...
-> Skipping. (file is empty)
-> Processing apw_eng_200212...
-> Skipping. (file is empty)
-> Processing apw_eng_200106...
-> Skipping. (file is empty)
-> Processing apw_eng_200103...
-> Skipping. (file is empty)
-> Processing apw_eng_200108...
-> Skipping. (file is empty)
-> Processing apw_eng_200802...
-> Skipping. (file is empty)
-> Processing apw_eng_199605...
-> Skipping. (file is empty)
-> Processing apw_eng_199706...
-> Skipping. (file is empty)
-> Processing apw_eng_200009...
-> Skipping. (file is empty)
-> Processing apw_eng_199606...
-> Skipping. (file is empty)
-> Processing apw_eng_199808...
-> Skipping. (file is empty)
-> Processing apw_eng_200309...
-> Skipping. (file is empty)
-> Processing apw_eng_199704...
-> Skipping. (file is empty)
-> Processing apw_eng_199803...
-> Skipping. (file is empty)
-> Processing apw_eng_201001...
-> Skipping. (file is empty)
-> Processing apw_eng_199907...
-> Skipping. (file is empty)
-> Processing apw_eng_201003...
-> Skipping. (file is empty)
-> Processing apw_eng_200110...
-> Skipping. (file is empty)
-> Processing apw_eng_200807...
-> Skipping. (file is empty)
-> Processing apw_eng_200706...
-> Skipping. (file is empty)
-> Processing apw_eng_200102...
-> Skipping. (file is empty)
-> Processing apw_eng_200201...
-> Skipping. (file is empty)
-> Processing apw_eng_201004...
-> Skipping. (file is empty)
-> Processing apw_eng_199601...
-> Skipping. (file is empty)
-> Processing apw_eng_199908...
-> Skipping. (file is empty)
-> Processing apw_eng_199512...
-> Skipping. (file is empty)
-> Processing apw_eng_199507...
-> Skipping. (file is empty)
-> Processing apw_eng_200007...
-> Skipping. (file is empty)
-> Processing apw_eng_200011...
-> Skipping. (file is empty)
-> Processing apw_eng_200605...
-> Skipping. (file is empty)
-> Processing apw_eng_200510...
-> Skipping. (file is empty)
-> Processing apw_eng_200708...
-> Skipping. (file is empty)
-> Processing apw_eng_201012...
-> Skipping. (file is empty)
-> Processing apw_eng_200502...
-> Skipping. (file is empty)
-> Processing apw_eng_200105...
-> Skipping. (file is empty)
-> Processing apw_eng_200509...
-> Skipping. (file is empty)
-> Processing apw_eng_200707...
-> Skipping. (file is empty)
-> Processing apw_eng_199904...
-> Skipping. (file is empty)
-> Processing apw_eng_199906...
-> Skipping. (file is empty)
-> Processing apw_eng_200609...
-> Skipping. (file is empty)
-> Processing apw_eng_200602...
-> Skipping. (file is empty)
-> Processing apw_eng_200910...
-> Skipping. (file is empty)
-> Processing apw_eng_199604...
-> Skipping. (file is empty)
-> Processing apw_eng_200202...
-> Skipping. (file is empty)
-> Processing apw_eng_200811...
-> Skipping. (file is empty)
-> Processing apw_eng_199711...
-> Skipping. (file is empty)
-> Processing apw_eng_200705...
-> Skipping. (file is empty)
-> Processing apw_eng_200909...
-> Skipping. (file is empty)
-> Processing apw_eng_200507...
-> Skipping. (file is empty)
-> Processing apw_eng_199702...
-> Skipping. (file is empty)
-> Processing apw_eng_200607...
-> Skipping. (file is empty)
-> Processing apw_eng_199807...
-> Skipping. (file is empty)
-> Processing apw_eng_200603...
-> Skipping. (file is empty)
-> Processing apw_eng_200402...
-> Skipping. (file is empty)
-> Processing apw_eng_200311...
-> Skipping. (file is empty)
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
-> Processing apw_eng_200408...
-> Skipping. (file is empty)
-> Processing apw_eng_200701...
-> Skipping. (file is empty)
-> Processing apw_eng_200903...
-> Skipping. (file is empty)
-> Processing apw_eng_200305...
-> Skipping. (file is empty)
-> Processing apw_eng_200111...
-> Skipping. (file is empty)
-> Processing apw_eng_199701...
-> Skipping. (file is empty)
-> Processing apw_eng_199805...
-> Skipping. (file is empty)
-> Processing apw_eng_201002...
-> Skipping. (file is empty)
-> Processing apw_eng_199710...
-> Skipping. (file is empty)
-> Processing apw_eng_199611...
-> Skipping. (file is empty)
-> Processing apw_eng_199712...
-> Skipping. (file is empty)
-> Processing apw_eng_200208...
-> Skipping. (file is empty)
-> Processing apw_eng_200005...
-> Skipping. (file is empty)
-> Processing apw_eng_199510...
-> Skipping. (file is empty)
-> Processing apw_eng_200112...
-> Skipping. (file is empty)
-> Processing apw_eng_199411...
-> Skipping. (file is empty)
-> Processing apw_eng_199806...
-> Skipping. (file is empty)
-> Processing apw_eng_200702...
-> Skipping. (file is empty)
-> Processing apw_eng_200810...
-> Skipping. (file is empty)
-> Processing apw_eng_200209...
-> Skipping. (file is empty)
-> Processing apw_eng_200207...
-> Skipping. (file is empty)
-> Processing apw_eng_200503...
-> Skipping. (file is empty)
-> Processing apw_eng_200601...
-> Skipping. (file is empty)
-> Processing apw_eng_199412...
-> Skipping. (file is empty)
-> Processing apw_eng_199511...
-> Skipping. (file is empty)
-> Processing apw_eng_200401...
-> Skipping. (file is empty)
-> Processing apw_eng_200901...
-> Skipping. (file is empty)
-> Processing apw_eng_199610...
-> Skipping. (file is empty)
-> Processing apw_eng_199901...
-> Skipping. (file is empty)
-> Processing apw_eng_200604...
-> Skipping. (file is empty)
-> Processing apw_eng_199811...
-> Skipping. (file is empty)
-> Processing apw_eng_200505...
-> Skipping. (file is empty)
-> Processing apw_eng_200411...
-> Skipping. (file is empty)
-> Processing apw_eng_200907...
-> Skipping. (file is empty)
-> Processing apw_eng_200008...
-> Skipping. (file is empty)
-> Processing apw_eng_200001...
-> Skipping. (file is empty)
-> Processing apw_eng_199708...
-> Skipping. (file is empty)
-> Processing apw_eng_199608...
-> Skipping. (file is empty)
-> Processing apw_eng_200012...
-> Skipping. (file is empty)
-> Processing apw_eng_200512...
-> Skipping. (file is empty)
-> Processing apw_eng_199612...
-> Skipping. (file is empty)
-> Processing apw_eng_200703...
-> Skipping. (file is empty)
-> Processing apw_eng_200710...
-> Skipping. (file is empty)
-> Processing apw_eng_201006...
-> Skipping. (file is empty)
-> Processing apw_eng_200211...
-> Skipping. (file is empty)
-> Processing apw_eng_199609...
-> Skipping. (file is empty)
-> Processing apw_eng_199603...
-> Skipping. (file is empty)
-> Processing apw_eng_200409...
-> Skipping. (file is empty)
-> Processing apw_eng_200912...
-> Skipping. (file is empty)
-> Processing apw_eng_200812...
-> Skipping. (file is empty)
-> Processing apw_eng_201008...
-> Skipping. (file is empty)
-> Processing apw_eng_201011...
-> Skipping. (file is empty)
-> Processing apw_eng_200508...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.01 minutes
====================================

Error: specified corpus directory does not contain any processed json files.
```
### Tabulating hits via `tabulateHits.py`...
```
```  
## Starting context: `almost-nobody_subj`
- time stamp: `Wed Aug  4 10:43:49 EDT 2021`
- data directory: `data/neg-mit/Apw.almost-nobody_subj`
- hits table: `hits/neg-mit/Apw_almost-nobody_subj`
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
 WARNING : [Conll, File Apw.conll/apw_eng_199608.conllu] No blank line at the end of the file
```
### Running grew search on `Apw.conll`...
```
193 total file(s) to be searched.
-> searching Apw.conll/apw_eng_199411.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199411.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199411.raw.json
1.67 minutes on apw_eng_199411.conllu
-> searching Apw.conll/apw_eng_199412.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199412.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199412.raw.json
2.43 minutes on apw_eng_199412.conllu
-> searching Apw.conll/apw_eng_199501.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199501.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199501.raw.json
2.52 minutes on apw_eng_199501.conllu
-> searching Apw.conll/apw_eng_199502.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199502.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199502.raw.json
2.2 minutes on apw_eng_199502.conllu
-> searching Apw.conll/apw_eng_199503.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199503.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199503.raw.json
2.63 minutes on apw_eng_199503.conllu
-> searching Apw.conll/apw_eng_199504.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199504.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199504.raw.json
2.51 minutes on apw_eng_199504.conllu
-> searching Apw.conll/apw_eng_199505.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199505.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199505.raw.json
3.25 minutes on apw_eng_199505.conllu
-> searching Apw.conll/apw_eng_199506.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199506.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199506.raw.json
3.37 minutes on apw_eng_199506.conllu
-> searching Apw.conll/apw_eng_199507.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199507.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199507.raw.json
3.17 minutes on apw_eng_199507.conllu
-> searching Apw.conll/apw_eng_199508.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199508.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199508.raw.json
3.13 minutes on apw_eng_199508.conllu
-> searching Apw.conll/apw_eng_199509.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199509.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199509.raw.json
3.0 minutes on apw_eng_199509.conllu
-> searching Apw.conll/apw_eng_199510.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199510.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199510.raw.json
2.21 minutes on apw_eng_199510.conllu
-> searching Apw.conll/apw_eng_199511.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199511.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199511.raw.json
2.07 minutes on apw_eng_199511.conllu
-> searching Apw.conll/apw_eng_199512.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199512.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199512.raw.json
2.01 minutes on apw_eng_199512.conllu
-> searching Apw.conll/apw_eng_199601.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199601.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199601.raw.json
2.1 minutes on apw_eng_199601.conllu
-> searching Apw.conll/apw_eng_199602.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199602.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199602.raw.json
1.92 minutes on apw_eng_199602.conllu
-> searching Apw.conll/apw_eng_199603.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199603.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199603.raw.json
2.19 minutes on apw_eng_199603.conllu
-> searching Apw.conll/apw_eng_199604.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199604.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199604.raw.json
2.09 minutes on apw_eng_199604.conllu
-> searching Apw.conll/apw_eng_199605.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199605.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199605.raw.json
2.12 minutes on apw_eng_199605.conllu
-> searching Apw.conll/apw_eng_199606.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199606.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199606.raw.json
1.83 minutes on apw_eng_199606.conllu
-> searching Apw.conll/apw_eng_199607.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199607.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199607.raw.json
1.99 minutes on apw_eng_199607.conllu
-> searching Apw.conll/apw_eng_199608.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199608.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199608.raw.json
1.67 minutes on apw_eng_199608.conllu
-> searching Apw.conll/apw_eng_199609.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199609.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199609.raw.json
1.84 minutes on apw_eng_199609.conllu
-> searching Apw.conll/apw_eng_199610.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199610.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199610.raw.json
1.97 minutes on apw_eng_199610.conllu
-> searching Apw.conll/apw_eng_199611.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199611.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199611.raw.json
2.0 minutes on apw_eng_199611.conllu
-> searching Apw.conll/apw_eng_199612.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199612.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199612.raw.json
2.11 minutes on apw_eng_199612.conllu
-> searching Apw.conll/apw_eng_199701.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199701.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199701.raw.json
2.3 minutes on apw_eng_199701.conllu
-> searching Apw.conll/apw_eng_199702.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199702.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199702.raw.json
2.1 minutes on apw_eng_199702.conllu
-> searching Apw.conll/apw_eng_199703.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199703.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199703.raw.json
2.37 minutes on apw_eng_199703.conllu
-> searching Apw.conll/apw_eng_199704.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199704.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199704.raw.json
2.29 minutes on apw_eng_199704.conllu
-> searching Apw.conll/apw_eng_199705.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199705.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199705.raw.json
2.32 minutes on apw_eng_199705.conllu
-> searching Apw.conll/apw_eng_199706.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199706.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199706.raw.json
2.3 minutes on apw_eng_199706.conllu
-> searching Apw.conll/apw_eng_199707.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199707.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199707.raw.json
2.44 minutes on apw_eng_199707.conllu
-> searching Apw.conll/apw_eng_199708.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199708.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199708.raw.json
2.3 minutes on apw_eng_199708.conllu
-> searching Apw.conll/apw_eng_199709.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199709.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199709.raw.json
2.43 minutes on apw_eng_199709.conllu
-> searching Apw.conll/apw_eng_199710.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199710.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199710.raw.json
2.4 minutes on apw_eng_199710.conllu
-> searching Apw.conll/apw_eng_199711.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199711.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199711.raw.json
2.91 minutes on apw_eng_199711.conllu
-> searching Apw.conll/apw_eng_199712.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199712.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199712.raw.json
3.78 minutes on apw_eng_199712.conllu
-> searching Apw.conll/apw_eng_199801.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199801.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199801.raw.json
3.94 minutes on apw_eng_199801.conllu
-> searching Apw.conll/apw_eng_199802.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199802.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199802.raw.json
4.02 minutes on apw_eng_199802.conllu
-> searching Apw.conll/apw_eng_199803.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199803.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199803.raw.json
4.18 minutes on apw_eng_199803.conllu
-> searching Apw.conll/apw_eng_199804.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199804.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199804.raw.json
3.99 minutes on apw_eng_199804.conllu
-> searching Apw.conll/apw_eng_199805.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199805.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199805.raw.json
3.94 minutes on apw_eng_199805.conllu
-> searching Apw.conll/apw_eng_199806.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199806.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199806.raw.json
3.68 minutes on apw_eng_199806.conllu
-> searching Apw.conll/apw_eng_199807.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199807.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199807.raw.json
2.35 minutes on apw_eng_199807.conllu
-> searching Apw.conll/apw_eng_199808.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199808.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199808.raw.json
2.34 minutes on apw_eng_199808.conllu
-> searching Apw.conll/apw_eng_199809.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199809.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199809.raw.json
2.48 minutes on apw_eng_199809.conllu
-> searching Apw.conll/apw_eng_199810.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199810.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199810.raw.json
2.47 minutes on apw_eng_199810.conllu
-> searching Apw.conll/apw_eng_199811.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199811.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199811.raw.json
2.39 minutes on apw_eng_199811.conllu
-> searching Apw.conll/apw_eng_199812.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199812.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199812.raw.json
2.89 minutes on apw_eng_199812.conllu
-> searching Apw.conll/apw_eng_199901.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199901.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199901.raw.json
2.6 minutes on apw_eng_199901.conllu
-> searching Apw.conll/apw_eng_199902.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199902.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199902.raw.json
2.38 minutes on apw_eng_199902.conllu
-> searching Apw.conll/apw_eng_199903.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199903.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199903.raw.json
2.98 minutes on apw_eng_199903.conllu
-> searching Apw.conll/apw_eng_199904.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199904.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199904.raw.json
2.73 minutes on apw_eng_199904.conllu
-> searching Apw.conll/apw_eng_199905.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199905.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199905.raw.json
2.89 minutes on apw_eng_199905.conllu
-> searching Apw.conll/apw_eng_199906.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199906.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199906.raw.json
3.07 minutes on apw_eng_199906.conllu
-> searching Apw.conll/apw_eng_199907.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199907.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199907.raw.json
2.74 minutes on apw_eng_199907.conllu
-> searching Apw.conll/apw_eng_199908.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199908.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199908.raw.json
1.83 minutes on apw_eng_199908.conllu
-> searching Apw.conll/apw_eng_199909.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199909.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199909.raw.json
1.52 minutes on apw_eng_199909.conllu
-> searching Apw.conll/apw_eng_199910.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199910.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199910.raw.json
1.78 minutes on apw_eng_199910.conllu
-> searching Apw.conll/apw_eng_199911.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_199911.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching Apw.conll/apw_eng_200001.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200001.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200001.raw.json
1.84 minutes on apw_eng_200001.conllu
-> searching Apw.conll/apw_eng_200002.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200002.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200002.raw.json
1.65 minutes on apw_eng_200002.conllu
-> searching Apw.conll/apw_eng_200003.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200003.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200003.raw.json
1.4 minutes on apw_eng_200003.conllu
-> searching Apw.conll/apw_eng_200004.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200004.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200004.raw.json
1.17 minutes on apw_eng_200004.conllu
-> searching Apw.conll/apw_eng_200005.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200005.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200005.raw.json
1.32 minutes on apw_eng_200005.conllu
-> searching Apw.conll/apw_eng_200006.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200006.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200006.raw.json
1.14 minutes on apw_eng_200006.conllu
-> searching Apw.conll/apw_eng_200007.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200007.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200007.raw.json
1.13 minutes on apw_eng_200007.conllu
-> searching Apw.conll/apw_eng_200008.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200008.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200008.raw.json
1.07 minutes on apw_eng_200008.conllu
-> searching Apw.conll/apw_eng_200009.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200009.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200009.raw.json
1.13 minutes on apw_eng_200009.conllu
-> searching Apw.conll/apw_eng_200010.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200010.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200010.raw.json
4.65 minutes on apw_eng_200010.conllu
-> searching Apw.conll/apw_eng_200011.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200011.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200011.raw.json
5.01 minutes on apw_eng_200011.conllu
-> searching Apw.conll/apw_eng_200012.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200012.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200012.raw.json
4.73 minutes on apw_eng_200012.conllu
-> searching Apw.conll/apw_eng_200101.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200101.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200101.raw.json
4.89 minutes on apw_eng_200101.conllu
-> searching Apw.conll/apw_eng_200102.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200102.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200102.raw.json
4.16 minutes on apw_eng_200102.conllu
-> searching Apw.conll/apw_eng_200103.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200103.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200103.raw.json
4.94 minutes on apw_eng_200103.conllu
-> searching Apw.conll/apw_eng_200104.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200104.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200104.raw.json
4.75 minutes on apw_eng_200104.conllu
-> searching Apw.conll/apw_eng_200105.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200105.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200105.raw.json
4.95 minutes on apw_eng_200105.conllu
-> searching Apw.conll/apw_eng_200106.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200106.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200106.raw.json
5.03 minutes on apw_eng_200106.conllu
-> searching Apw.conll/apw_eng_200107.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200107.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200107.raw.json
4.79 minutes on apw_eng_200107.conllu
-> searching Apw.conll/apw_eng_200108.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200108.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200108.raw.json
2.8 minutes on apw_eng_200108.conllu
-> searching Apw.conll/apw_eng_200109.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200109.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200109.raw.json
3.84 minutes on apw_eng_200109.conllu
-> searching Apw.conll/apw_eng_200110.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200110.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200110.raw.json
3.89 minutes on apw_eng_200110.conllu
-> searching Apw.conll/apw_eng_200111.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200111.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200111.raw.json
3.48 minutes on apw_eng_200111.conllu
-> searching Apw.conll/apw_eng_200112.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200112.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200112.raw.json
3.3 minutes on apw_eng_200112.conllu
-> searching Apw.conll/apw_eng_200201.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200201.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200201.raw.json
3.66 minutes on apw_eng_200201.conllu
-> searching Apw.conll/apw_eng_200202.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200202.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200202.raw.json
3.5 minutes on apw_eng_200202.conllu
-> searching Apw.conll/apw_eng_200203.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200203.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200203.raw.json
3.87 minutes on apw_eng_200203.conllu
-> searching Apw.conll/apw_eng_200204.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200204.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200204.raw.json
3.92 minutes on apw_eng_200204.conllu
-> searching Apw.conll/apw_eng_200205.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200205.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200205.raw.json
3.91 minutes on apw_eng_200205.conllu
-> searching Apw.conll/apw_eng_200206.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200206.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200206.raw.json
3.93 minutes on apw_eng_200206.conllu
-> searching Apw.conll/apw_eng_200207.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200207.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200207.raw.json
3.85 minutes on apw_eng_200207.conllu
-> searching Apw.conll/apw_eng_200208.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200208.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200208.raw.json
3.46 minutes on apw_eng_200208.conllu
-> searching Apw.conll/apw_eng_200209.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200209.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200209.raw.json
3.88 minutes on apw_eng_200209.conllu
-> searching Apw.conll/apw_eng_200210.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200210.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200210.raw.json
4.23 minutes on apw_eng_200210.conllu
-> searching Apw.conll/apw_eng_200211.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200211.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200211.raw.json
3.75 minutes on apw_eng_200211.conllu
-> searching Apw.conll/apw_eng_200212.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200212.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200212.raw.json
2.93 minutes on apw_eng_200212.conllu
-> searching Apw.conll/apw_eng_200301.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200301.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200301.raw.json
4.21 minutes on apw_eng_200301.conllu
-> searching Apw.conll/apw_eng_200302.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200302.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200302.raw.json
4.12 minutes on apw_eng_200302.conllu
-> searching Apw.conll/apw_eng_200303.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200303.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200303.raw.json
4.69 minutes on apw_eng_200303.conllu
-> searching Apw.conll/apw_eng_200304.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200304.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200304.raw.json
4.15 minutes on apw_eng_200304.conllu
-> searching Apw.conll/apw_eng_200305.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200305.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200305.raw.json
4.12 minutes on apw_eng_200305.conllu
-> searching Apw.conll/apw_eng_200306.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200306.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200306.raw.json
3.29 minutes on apw_eng_200306.conllu
-> searching Apw.conll/apw_eng_200307.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200307.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200307.raw.json
1.4 minutes on apw_eng_200307.conllu
-> searching Apw.conll/apw_eng_200308.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200308.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200308.raw.json
3.77 minutes on apw_eng_200308.conllu
-> searching Apw.conll/apw_eng_200309.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200309.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200309.raw.json
4.25 minutes on apw_eng_200309.conllu
-> searching Apw.conll/apw_eng_200310.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200310.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200310.raw.json
5.13 minutes on apw_eng_200310.conllu
-> searching Apw.conll/apw_eng_200311.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200311.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200311.raw.json
4.44 minutes on apw_eng_200311.conllu
-> searching Apw.conll/apw_eng_200312.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200312.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200312.raw.json
4.04 minutes on apw_eng_200312.conllu
-> searching Apw.conll/apw_eng_200401.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200401.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200401.raw.json
2.36 minutes on apw_eng_200401.conllu
-> searching Apw.conll/apw_eng_200402.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200402.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200402.raw.json
3.16 minutes on apw_eng_200402.conllu
-> searching Apw.conll/apw_eng_200403.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200403.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200403.raw.json
5.14 minutes on apw_eng_200403.conllu
-> searching Apw.conll/apw_eng_200404.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200404.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200404.raw.json
4.59 minutes on apw_eng_200404.conllu
-> searching Apw.conll/apw_eng_200405.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200405.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200405.raw.json
0.9 minutes on apw_eng_200405.conllu
-> searching Apw.conll/apw_eng_200406.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200406.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200406.raw.json
0.83 minutes on apw_eng_200406.conllu
-> searching Apw.conll/apw_eng_200407.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200407.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200407.raw.json
2.05 minutes on apw_eng_200407.conllu
-> searching Apw.conll/apw_eng_200408.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200408.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200408.raw.json
1.8 minutes on apw_eng_200408.conllu
-> searching Apw.conll/apw_eng_200409.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200409.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200409.raw.json
1.92 minutes on apw_eng_200409.conllu
-> searching Apw.conll/apw_eng_200410.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200410.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200410.raw.json
2.18 minutes on apw_eng_200410.conllu
-> searching Apw.conll/apw_eng_200411.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200411.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200411.raw.json
1.59 minutes on apw_eng_200411.conllu
-> searching Apw.conll/apw_eng_200412.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200412.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200412.raw.json
0.6 minutes on apw_eng_200412.conllu
-> searching Apw.conll/apw_eng_200501.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200501.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200501.raw.json
1.65 minutes on apw_eng_200501.conllu
-> searching Apw.conll/apw_eng_200502.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200502.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200502.raw.json
1.45 minutes on apw_eng_200502.conllu
-> searching Apw.conll/apw_eng_200503.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200503.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200503.raw.json
2.18 minutes on apw_eng_200503.conllu
-> searching Apw.conll/apw_eng_200504.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200504.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200504.raw.json
1.58 minutes on apw_eng_200504.conllu
-> searching Apw.conll/apw_eng_200505.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200505.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200505.raw.json
2.04 minutes on apw_eng_200505.conllu
-> searching Apw.conll/apw_eng_200506.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200506.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200506.raw.json
2.16 minutes on apw_eng_200506.conllu
-> searching Apw.conll/apw_eng_200507.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200507.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200507.raw.json
1.44 minutes on apw_eng_200507.conllu
-> searching Apw.conll/apw_eng_200508.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200508.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200508.raw.json
1.91 minutes on apw_eng_200508.conllu
-> searching Apw.conll/apw_eng_200509.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200509.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200509.raw.json
2.36 minutes on apw_eng_200509.conllu
-> searching Apw.conll/apw_eng_200510.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200510.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200510.raw.json
2.21 minutes on apw_eng_200510.conllu
-> searching Apw.conll/apw_eng_200511.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200511.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200511.raw.json
2.19 minutes on apw_eng_200511.conllu
-> searching Apw.conll/apw_eng_200512.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200512.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200512.raw.json
2.2 minutes on apw_eng_200512.conllu
-> searching Apw.conll/apw_eng_200601.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200601.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200601.raw.json
2.26 minutes on apw_eng_200601.conllu
-> searching Apw.conll/apw_eng_200602.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200602.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200602.raw.json
1.82 minutes on apw_eng_200602.conllu
-> searching Apw.conll/apw_eng_200603.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200603.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200603.raw.json
2.48 minutes on apw_eng_200603.conllu
-> searching Apw.conll/apw_eng_200604.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200604.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200604.raw.json
1.9 minutes on apw_eng_200604.conllu
-> searching Apw.conll/apw_eng_200605.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200605.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200605.raw.json
2.49 minutes on apw_eng_200605.conllu
-> searching Apw.conll/apw_eng_200606.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200606.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200606.raw.json
2.31 minutes on apw_eng_200606.conllu
-> searching Apw.conll/apw_eng_200607.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200607.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200607.raw.json
2.23 minutes on apw_eng_200607.conllu
-> searching Apw.conll/apw_eng_200608.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200608.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200608.raw.json
2.0 minutes on apw_eng_200608.conllu
-> searching Apw.conll/apw_eng_200609.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200609.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200609.raw.json
1.92 minutes on apw_eng_200609.conllu
-> searching Apw.conll/apw_eng_200610.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200610.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200610.raw.json
4.72 minutes on apw_eng_200610.conllu
-> searching Apw.conll/apw_eng_200611.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200611.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200611.raw.json
4.72 minutes on apw_eng_200611.conllu
-> searching Apw.conll/apw_eng_200612.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200612.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200612.raw.json
1.63 minutes on apw_eng_200612.conllu
-> searching Apw.conll/apw_eng_200701.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200701.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200701.raw.json
4.67 minutes on apw_eng_200701.conllu
-> searching Apw.conll/apw_eng_200702.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200702.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200702.raw.json
4.37 minutes on apw_eng_200702.conllu
-> searching Apw.conll/apw_eng_200703.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200703.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200703.raw.json
4.72 minutes on apw_eng_200703.conllu
-> searching Apw.conll/apw_eng_200704.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200704.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200704.raw.json
4.39 minutes on apw_eng_200704.conllu
-> searching Apw.conll/apw_eng_200705.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200705.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200705.raw.json
4.69 minutes on apw_eng_200705.conllu
-> searching Apw.conll/apw_eng_200706.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200706.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200706.raw.json
4.42 minutes on apw_eng_200706.conllu
-> searching Apw.conll/apw_eng_200707.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200707.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200707.raw.json
4.17 minutes on apw_eng_200707.conllu
-> searching Apw.conll/apw_eng_200708.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200708.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200708.raw.json
4.23 minutes on apw_eng_200708.conllu
-> searching Apw.conll/apw_eng_200709.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200709.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200709.raw.json
4.39 minutes on apw_eng_200709.conllu
-> searching Apw.conll/apw_eng_200710.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200710.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200710.raw.json
4.34 minutes on apw_eng_200710.conllu
-> searching Apw.conll/apw_eng_200711.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200711.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200711.raw.json
4.07 minutes on apw_eng_200711.conllu
-> searching Apw.conll/apw_eng_200712.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200712.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200712.raw.json
3.48 minutes on apw_eng_200712.conllu
-> searching Apw.conll/apw_eng_200801.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200801.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200801.raw.json
4.2 minutes on apw_eng_200801.conllu
-> searching Apw.conll/apw_eng_200802.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200802.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200802.raw.json
4.13 minutes on apw_eng_200802.conllu
-> searching Apw.conll/apw_eng_200803.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200803.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200803.raw.json
4.13 minutes on apw_eng_200803.conllu
-> searching Apw.conll/apw_eng_200804.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200804.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200804.raw.json
4.0 minutes on apw_eng_200804.conllu
-> searching Apw.conll/apw_eng_200805.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200805.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200805.raw.json
4.13 minutes on apw_eng_200805.conllu
-> searching Apw.conll/apw_eng_200806.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200806.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200806.raw.json
4.18 minutes on apw_eng_200806.conllu
-> searching Apw.conll/apw_eng_200807.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200807.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200807.raw.json
3.58 minutes on apw_eng_200807.conllu
-> searching Apw.conll/apw_eng_200808.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200808.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200808.raw.json
3.68 minutes on apw_eng_200808.conllu
-> searching Apw.conll/apw_eng_200809.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200809.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200809.raw.json
3.78 minutes on apw_eng_200809.conllu
-> searching Apw.conll/apw_eng_200810.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200810.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200810.raw.json
3.55 minutes on apw_eng_200810.conllu
-> searching Apw.conll/apw_eng_200811.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200811.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200811.raw.json
2.77 minutes on apw_eng_200811.conllu
-> searching Apw.conll/apw_eng_200812.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200812.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200812.raw.json
2.38 minutes on apw_eng_200812.conllu
-> searching Apw.conll/apw_eng_200901.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200901.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200901.raw.json
2.98 minutes on apw_eng_200901.conllu
-> searching Apw.conll/apw_eng_200902.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200902.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200902.raw.json
2.9 minutes on apw_eng_200902.conllu
-> searching Apw.conll/apw_eng_200903.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200903.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200903.raw.json
3.24 minutes on apw_eng_200903.conllu
-> searching Apw.conll/apw_eng_200904.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200904.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200904.raw.json
3.61 minutes on apw_eng_200904.conllu
-> searching Apw.conll/apw_eng_200905.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200905.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200905.raw.json
3.38 minutes on apw_eng_200905.conllu
-> searching Apw.conll/apw_eng_200906.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200906.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200906.raw.json
3.46 minutes on apw_eng_200906.conllu
-> searching Apw.conll/apw_eng_200907.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200907.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200907.raw.json
2.23 minutes on apw_eng_200907.conllu
-> searching Apw.conll/apw_eng_200908.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200908.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200908.raw.json
2.39 minutes on apw_eng_200908.conllu
-> searching Apw.conll/apw_eng_200909.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200909.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200909.raw.json
2.33 minutes on apw_eng_200909.conllu
-> searching Apw.conll/apw_eng_200910.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200910.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200910.raw.json
2.33 minutes on apw_eng_200910.conllu
-> searching Apw.conll/apw_eng_200911.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200911.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200911.raw.json
2.26 minutes on apw_eng_200911.conllu
-> searching Apw.conll/apw_eng_200912.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_200912.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_200912.raw.json
2.4 minutes on apw_eng_200912.conllu
-> searching Apw.conll/apw_eng_201001.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201001.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201001.raw.json
2.85 minutes on apw_eng_201001.conllu
-> searching Apw.conll/apw_eng_201002.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201002.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201002.raw.json
1.92 minutes on apw_eng_201002.conllu
-> searching Apw.conll/apw_eng_201003.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201003.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201003.raw.json
2.12 minutes on apw_eng_201003.conllu
-> searching Apw.conll/apw_eng_201004.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201004.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201004.raw.json
2.09 minutes on apw_eng_201004.conllu
-> searching Apw.conll/apw_eng_201005.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201005.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201005.raw.json
2.11 minutes on apw_eng_201005.conllu
-> searching Apw.conll/apw_eng_201006.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201006.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201006.raw.json
2.2 minutes on apw_eng_201006.conllu
-> searching Apw.conll/apw_eng_201007.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201007.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201007.raw.json
1.77 minutes on apw_eng_201007.conllu
-> searching Apw.conll/apw_eng_201008.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201008.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201008.raw.json
2.83 minutes on apw_eng_201008.conllu
-> searching Apw.conll/apw_eng_201009.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201009.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201009.raw.json
3.13 minutes on apw_eng_201009.conllu
-> searching Apw.conll/apw_eng_201010.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201010.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201010.raw.json
3.22 minutes on apw_eng_201010.conllu
-> searching Apw.conll/apw_eng_201011.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201011.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201011.raw.json
3.33 minutes on apw_eng_201011.conllu
-> searching Apw.conll/apw_eng_201012.conllu:
grew grep -pattern Pat/neg-mit/almost-nobody_subj.pat -i Apw.conll/apw_eng_201012.conllu > data/neg-mit/Apw.almost-nobody_subj/apw_eng_201012.raw.json
2.64 minutes on apw_eng_201012.conllu

Total grew search time: 563.78 minutes
==============================================

```
### Running `FillJson.py` script on json files in `Apw.almost-nobody_subj` from conll files in `Apw.conll`...
```
-> Processing apw_eng_200707...
-> Skipping. (file is empty)
-> Processing apw_eng_199603...
-> Skipping. (file is empty)
-> Processing apw_eng_199608...
-> Skipping. (file is empty)
-> Processing apw_eng_200212...
-> Skipping. (file is empty)
-> Processing apw_eng_200702...
-> Skipping. (file is empty)
-> Processing apw_eng_200601...
-> Skipping. (file is empty)
-> Processing apw_eng_201007...
-> Skipping. (file is empty)
-> Processing apw_eng_199606...
-> Skipping. (file is empty)
-> Processing apw_eng_200606...
-> Skipping. (file is empty)
-> Processing apw_eng_201001...
-> Skipping. (file is empty)
-> Processing apw_eng_200006...
-> Skipping. (file is empty)
-> Processing apw_eng_199509...
-> Skipping. (file is empty)
-> Processing apw_eng_200604...
-> Skipping. (file is empty)
-> Processing apw_eng_199709...
-> Skipping. (file is empty)
-> Processing apw_eng_199904...
-> Skipping. (file is empty)
-> Processing apw_eng_199811...
-> Skipping. (file is empty)
-> Processing apw_eng_200806...
-> Skipping. (file is empty)
-> Processing apw_eng_200807...
-> Skipping. (file is empty)
-> Processing apw_eng_200307...
-> Skipping. (file is empty)
-> Processing apw_eng_200107...
-> Skipping. (file is empty)
-> Processing apw_eng_201012...
-> Skipping. (file is empty)
-> Processing apw_eng_200303...
-> Skipping. (file is empty)
-> Processing apw_eng_199501...
-> Skipping. (file is empty)
-> Processing apw_eng_200311...
-> Skipping. (file is empty)
-> Processing apw_eng_200802...
-> Skipping. (file is empty)
-> Processing apw_eng_199910...
-> Skipping. (file is empty)
-> Processing apw_eng_200012...
-> Skipping. (file is empty)
-> Processing apw_eng_200509...
-> Skipping. (file is empty)
-> Processing apw_eng_200104...
-> Skipping. (file is empty)
-> Processing apw_eng_201003...
-> Skipping. (file is empty)
-> Processing apw_eng_200209...
-> Skipping. (file is empty)
-> Processing apw_eng_199802...
-> Skipping. (file is empty)
-> Processing apw_eng_200003...
-> Skipping. (file is empty)
-> Processing apw_eng_200312...
-> Skipping. (file is empty)
-> Processing apw_eng_200904...
-> Skipping. (file is empty)
-> Processing apw_eng_200505...
-> Skipping. (file is empty)
-> Processing apw_eng_199602...
-> Skipping. (file is empty)
-> Processing apw_eng_200205...
-> Skipping. (file is empty)
-> Processing apw_eng_199701...
-> Skipping. (file is empty)
-> Processing apw_eng_200101...
-> Skipping. (file is empty)
-> Processing apw_eng_200407...
-> Skipping. (file is empty)
-> Processing apw_eng_200302...
-> Skipping. (file is empty)
-> Processing apw_eng_199708...
-> Skipping. (file is empty)
-> Processing apw_eng_199611...
-> Skipping. (file is empty)
-> Processing apw_eng_200705...
-> Skipping. (file is empty)
-> Processing apw_eng_200711...
-> Skipping. (file is empty)
-> Processing apw_eng_200208...
-> Skipping. (file is empty)
-> Processing apw_eng_200804...
-> Skipping. (file is empty)
-> Processing apw_eng_200910...
-> Skipping. (file is empty)
-> Processing apw_eng_200002...
-> Skipping. (file is empty)
-> Processing apw_eng_200108...
-> Skipping. (file is empty)
-> Processing apw_eng_200901...
-> Skipping. (file is empty)
-> Processing apw_eng_200304...
-> Skipping. (file is empty)
-> Processing apw_eng_200408...
-> Skipping. (file is empty)
-> Processing apw_eng_200109...
-> Skipping. (file is empty)
-> Processing apw_eng_200305...
-> Skipping. (file is empty)
-> Processing apw_eng_199906...
-> Skipping. (file is empty)
-> Processing apw_eng_200902...
-> Skipping. (file is empty)
-> Processing apw_eng_200510...
-> Skipping. (file is empty)
-> Processing apw_eng_200405...
-> Skipping. (file is empty)
-> Processing apw_eng_199604...
-> Skipping. (file is empty)
-> Processing apw_eng_200908...
-> Skipping. (file is empty)
-> Processing apw_eng_199712...
-> Skipping. (file is empty)
-> Processing apw_eng_199511...
-> Skipping. (file is empty)
-> Processing apw_eng_200010...
-> Skipping. (file is empty)
-> Processing apw_eng_200409...
-> Skipping. (file is empty)
-> Processing apw_eng_199909...
-> Skipping. (file is empty)
-> Processing apw_eng_200110...
-> Skipping. (file is empty)
-> Processing apw_eng_199801...
-> Skipping. (file is empty)
-> Processing apw_eng_200005...
-> Skipping. (file is empty)
-> Processing apw_eng_199905...
-> Skipping. (file is empty)
-> Processing apw_eng_201005...
-> Skipping. (file is empty)
-> Processing apw_eng_199903...
-> Skipping. (file is empty)
-> Processing apw_eng_200905...
-> Skipping. (file is empty)
-> Processing apw_eng_199508...
-> Skipping. (file is empty)
-> Processing apw_eng_199711...
-> Skipping. (file is empty)
-> Processing apw_eng_200310...
-> Skipping. (file is empty)
-> Processing apw_eng_200411...
-> Skipping. (file is empty)
-> Processing apw_eng_199703...
-> Skipping. (file is empty)
-> Processing apw_eng_200501...
-> Skipping. (file is empty)
-> Processing apw_eng_200808...
-> Skipping. (file is empty)
-> Processing apw_eng_200609...
-> Skipping. (file is empty)
-> Processing apw_eng_200809...
-> Skipping. (file is empty)
-> Processing apw_eng_200602...
-> Skipping. (file is empty)
-> Processing apw_eng_200008...
-> Skipping. (file is empty)
-> Processing apw_eng_200004...
-> Skipping. (file is empty)
-> Processing apw_eng_200701...
-> Skipping. (file is empty)
-> Processing apw_eng_200605...
-> Skipping. (file is empty)
-> Processing apw_eng_200805...
-> Skipping. (file is empty)
-> Processing apw_eng_199806...
-> Skipping. (file is empty)
-> Processing apw_eng_200603...
-> Skipping. (file is empty)
-> Processing apw_eng_200105...
-> Skipping. (file is empty)
-> Processing apw_eng_199605...
-> Skipping. (file is empty)
-> Processing apw_eng_200907...
-> Skipping. (file is empty)
-> Processing apw_eng_200007...
-> Skipping. (file is empty)
-> Processing apw_eng_199706...
-> Skipping. (file is empty)
-> Processing apw_eng_201002...
-> Skipping. (file is empty)
-> Processing apw_eng_200001...
-> Skipping. (file is empty)
-> Processing apw_eng_199807...
-> Skipping. (file is empty)
-> Processing apw_eng_199412...
-> Skipping. (file is empty)
-> Processing apw_eng_199505...
-> Skipping. (file is empty)
-> Processing apw_eng_200412...
-> Skipping. (file is empty)
-> Processing apw_eng_199908...
-> Skipping. (file is empty)
-> Processing apw_eng_200903...
-> Skipping. (file is empty)
-> Processing apw_eng_199612...
-> Skipping. (file is empty)
-> Processing apw_eng_200306...
-> Skipping. (file is empty)
-> Processing apw_eng_200308...
-> Skipping. (file is empty)
-> Processing apw_eng_200210...
-> Skipping. (file is empty)
-> Processing apw_eng_199507...
-> Skipping. (file is empty)
-> Processing apw_eng_199710...
-> Skipping. (file is empty)
-> Processing apw_eng_199901...
-> Skipping. (file is empty)
-> Processing apw_eng_199609...
-> Skipping. (file is empty)
-> Processing apw_eng_200103...
-> Skipping. (file is empty)
-> Processing apw_eng_200612...
-> Skipping. (file is empty)
-> Processing apw_eng_199512...
-> Skipping. (file is empty)
-> Processing apw_eng_200710...
-> Skipping. (file is empty)
-> Processing apw_eng_201010...
-> Skipping. (file is empty)
-> Processing apw_eng_200703...
-> Skipping. (file is empty)
-> Processing apw_eng_201009...
-> Skipping. (file is empty)
-> Processing apw_eng_200610...
-> Skipping. (file is empty)
-> Processing apw_eng_199510...
-> Skipping. (file is empty)
-> Processing apw_eng_200810...
-> Skipping. (file is empty)
-> Processing apw_eng_200207...
-> Skipping. (file is empty)
-> Processing apw_eng_200508...
-> Skipping. (file is empty)
-> Processing apw_eng_199506...
-> Skipping. (file is empty)
-> Processing apw_eng_200404...
-> Skipping. (file is empty)
-> Processing apw_eng_200502...
-> Skipping. (file is empty)
-> Processing apw_eng_199411...
-> Skipping. (file is empty)
-> Processing apw_eng_200406...
-> Skipping. (file is empty)
-> Processing apw_eng_200511...
-> Skipping. (file is empty)
-> Processing apw_eng_200309...
-> Skipping. (file is empty)
-> Processing apw_eng_200504...
-> Skipping. (file is empty)
-> Processing apw_eng_199502...
-> Skipping. (file is empty)
-> Processing apw_eng_199503...
-> Skipping. (file is empty)
-> Processing apw_eng_200812...
-> Skipping. (file is empty)
-> Processing apw_eng_200201...
-> Skipping. (file is empty)
-> Processing apw_eng_201004...
-> Skipping. (file is empty)
-> Processing apw_eng_199803...
-> Skipping. (file is empty)
-> Processing apw_eng_199607...
-> Skipping. (file is empty)
-> Processing apw_eng_200111...
-> Skipping. (file is empty)
-> Processing apw_eng_200811...
-> Skipping. (file is empty)
-> Processing apw_eng_200803...
-> Skipping. (file is empty)
-> Processing apw_eng_200202...
-> Skipping. (file is empty)
-> Processing apw_eng_199707...
-> Skipping. (file is empty)
-> Processing apw_eng_199804...
-> Skipping. (file is empty)
-> Processing apw_eng_200607...
-> Skipping. (file is empty)
-> Processing apw_eng_200911...
-> Skipping. (file is empty)
-> Processing apw_eng_199805...
-> Skipping. (file is empty)
-> Processing apw_eng_199907...
-> Skipping. (file is empty)
-> Processing apw_eng_200401...
-> Skipping. (file is empty)
-> Processing apw_eng_199902...
-> Skipping. (file is empty)
-> Processing apw_eng_199705...
-> Skipping. (file is empty)
-> Processing apw_eng_200801...
-> Skipping. (file is empty)
-> Processing apw_eng_199610...
-> Skipping. (file is empty)
-> Processing apw_eng_200708...
-> Skipping. (file is empty)
-> Processing apw_eng_199504...
-> Skipping. (file is empty)
-> Processing apw_eng_200106...
-> Skipping. (file is empty)
-> Processing apw_eng_200507...
-> Skipping. (file is empty)
-> Processing apw_eng_201008...
-> Skipping. (file is empty)
-> Processing apw_eng_199809...
-> Skipping. (file is empty)
-> Processing apw_eng_200712...
-> Skipping. (file is empty)
-> Processing apw_eng_200704...
-> Skipping. (file is empty)
-> Processing apw_eng_200102...
-> Skipping. (file is empty)
-> Processing apw_eng_200403...
-> Skipping. (file is empty)
-> Processing apw_eng_200611...
-> Skipping. (file is empty)
-> Processing apw_eng_199704...
-> Skipping. (file is empty)
-> Processing apw_eng_199810...
-> Skipping. (file is empty)
-> Processing apw_eng_200206...
-> Skipping. (file is empty)
-> Processing apw_eng_200909...
-> Skipping. (file is empty)
-> Processing apw_eng_200706...
-> Skipping. (file is empty)
-> Processing apw_eng_199808...
-> Skipping. (file is empty)
-> Processing apw_eng_200410...
-> Skipping. (file is empty)
-> Processing apw_eng_201006...
-> Skipping. (file is empty)
-> Processing apw_eng_199702...
-> Skipping. (file is empty)
-> Processing apw_eng_200203...
-> Skipping. (file is empty)
-> Processing apw_eng_201011...
-> Skipping. (file is empty)
-> Processing apw_eng_199812...
-> Skipping. (file is empty)
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
-> Processing apw_eng_200906...
-> Skipping. (file is empty)
-> Processing apw_eng_200301...
-> Skipping. (file is empty)
-> Processing apw_eng_200506...
-> Skipping. (file is empty)
-> Processing apw_eng_200608...
-> Skipping. (file is empty)
-> Processing apw_eng_200204...
-> Skipping. (file is empty)
-> Processing apw_eng_200709...
-> Skipping. (file is empty)
-> Processing apw_eng_200512...
-> Skipping. (file is empty)
-> Processing apw_eng_200011...
-> Skipping. (file is empty)
-> Processing apw_eng_200912...
-> Skipping. (file is empty)
-> Processing apw_eng_200402...
-> Skipping. (file is empty)
-> Processing apw_eng_199601...
-> Skipping. (file is empty)
-> Processing apw_eng_200009...
-> Skipping. (file is empty)
-> Processing apw_eng_200503...
-> Skipping. (file is empty)
-> Processing apw_eng_200112...
-> Skipping. (file is empty)
-> Processing apw_eng_200211...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.0 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `almost-none_subj`
- time stamp: `Wed Aug  4 20:07:36 EDT 2021`
- data directory: `data/neg-mit/Apw.almost-none_subj`
- hits table: `hits/neg-mit/Apw_almost-none_subj`
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
 WARNING : [Conll, File Apw.conll/apw_eng_199608.conllu] No blank line at the end of the file
```
### Running grew search on `Apw.conll`...
```
193 total file(s) to be searched.
-> searching Apw.conll/apw_eng_199411.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199411.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199411.raw.json
1.62 minutes on apw_eng_199411.conllu
-> searching Apw.conll/apw_eng_199412.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199412.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199412.raw.json
2.34 minutes on apw_eng_199412.conllu
-> searching Apw.conll/apw_eng_199501.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199501.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199501.raw.json
2.41 minutes on apw_eng_199501.conllu
-> searching Apw.conll/apw_eng_199502.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199502.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199502.raw.json
2.09 minutes on apw_eng_199502.conllu
-> searching Apw.conll/apw_eng_199503.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199503.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199503.raw.json
2.47 minutes on apw_eng_199503.conllu
-> searching Apw.conll/apw_eng_199504.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199504.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199504.raw.json
2.4 minutes on apw_eng_199504.conllu
-> searching Apw.conll/apw_eng_199505.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199505.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199505.raw.json
3.07 minutes on apw_eng_199505.conllu
-> searching Apw.conll/apw_eng_199506.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199506.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199506.raw.json
3.24 minutes on apw_eng_199506.conllu
-> searching Apw.conll/apw_eng_199507.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199507.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199507.raw.json
3.0 minutes on apw_eng_199507.conllu
-> searching Apw.conll/apw_eng_199508.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199508.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199508.raw.json
3.01 minutes on apw_eng_199508.conllu
-> searching Apw.conll/apw_eng_199509.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199509.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199509.raw.json
2.88 minutes on apw_eng_199509.conllu
-> searching Apw.conll/apw_eng_199510.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199510.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199510.raw.json
2.03 minutes on apw_eng_199510.conllu
-> searching Apw.conll/apw_eng_199511.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199511.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199511.raw.json
1.99 minutes on apw_eng_199511.conllu
-> searching Apw.conll/apw_eng_199512.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199512.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199512.raw.json
1.9 minutes on apw_eng_199512.conllu
-> searching Apw.conll/apw_eng_199601.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199601.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199601.raw.json
2.02 minutes on apw_eng_199601.conllu
-> searching Apw.conll/apw_eng_199602.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199602.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199602.raw.json
1.9 minutes on apw_eng_199602.conllu
-> searching Apw.conll/apw_eng_199603.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199603.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199603.raw.json
2.16 minutes on apw_eng_199603.conllu
-> searching Apw.conll/apw_eng_199604.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199604.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199604.raw.json
2.06 minutes on apw_eng_199604.conllu
-> searching Apw.conll/apw_eng_199605.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199605.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199605.raw.json
2.11 minutes on apw_eng_199605.conllu
-> searching Apw.conll/apw_eng_199606.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199606.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199606.raw.json
1.79 minutes on apw_eng_199606.conllu
-> searching Apw.conll/apw_eng_199607.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199607.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199607.raw.json
1.93 minutes on apw_eng_199607.conllu
-> searching Apw.conll/apw_eng_199608.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199608.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199608.raw.json
1.56 minutes on apw_eng_199608.conllu
-> searching Apw.conll/apw_eng_199609.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199609.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199609.raw.json
1.79 minutes on apw_eng_199609.conllu
-> searching Apw.conll/apw_eng_199610.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199610.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199610.raw.json
1.95 minutes on apw_eng_199610.conllu
-> searching Apw.conll/apw_eng_199611.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199611.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199611.raw.json
1.92 minutes on apw_eng_199611.conllu
-> searching Apw.conll/apw_eng_199612.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199612.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199612.raw.json
2.05 minutes on apw_eng_199612.conllu
-> searching Apw.conll/apw_eng_199701.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199701.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199701.raw.json
2.26 minutes on apw_eng_199701.conllu
-> searching Apw.conll/apw_eng_199702.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199702.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199702.raw.json
1.99 minutes on apw_eng_199702.conllu
-> searching Apw.conll/apw_eng_199703.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199703.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199703.raw.json
2.29 minutes on apw_eng_199703.conllu
-> searching Apw.conll/apw_eng_199704.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199704.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199704.raw.json
2.18 minutes on apw_eng_199704.conllu
-> searching Apw.conll/apw_eng_199705.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199705.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199705.raw.json
2.28 minutes on apw_eng_199705.conllu
-> searching Apw.conll/apw_eng_199706.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199706.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199706.raw.json
2.28 minutes on apw_eng_199706.conllu
-> searching Apw.conll/apw_eng_199707.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199707.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199707.raw.json
2.32 minutes on apw_eng_199707.conllu
-> searching Apw.conll/apw_eng_199708.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199708.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199708.raw.json
2.24 minutes on apw_eng_199708.conllu
-> searching Apw.conll/apw_eng_199709.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199709.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199709.raw.json
2.36 minutes on apw_eng_199709.conllu
-> searching Apw.conll/apw_eng_199710.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199710.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199710.raw.json
2.32 minutes on apw_eng_199710.conllu
-> searching Apw.conll/apw_eng_199711.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199711.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199711.raw.json
2.83 minutes on apw_eng_199711.conllu
-> searching Apw.conll/apw_eng_199712.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199712.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199712.raw.json
3.57 minutes on apw_eng_199712.conllu
-> searching Apw.conll/apw_eng_199801.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199801.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199801.raw.json
3.77 minutes on apw_eng_199801.conllu
-> searching Apw.conll/apw_eng_199802.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199802.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199802.raw.json
3.87 minutes on apw_eng_199802.conllu
-> searching Apw.conll/apw_eng_199803.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199803.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199803.raw.json
4.06 minutes on apw_eng_199803.conllu
-> searching Apw.conll/apw_eng_199804.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199804.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199804.raw.json
3.87 minutes on apw_eng_199804.conllu
-> searching Apw.conll/apw_eng_199805.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199805.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199805.raw.json
3.82 minutes on apw_eng_199805.conllu
-> searching Apw.conll/apw_eng_199806.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199806.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199806.raw.json
3.59 minutes on apw_eng_199806.conllu
-> searching Apw.conll/apw_eng_199807.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199807.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199807.raw.json
2.3 minutes on apw_eng_199807.conllu
-> searching Apw.conll/apw_eng_199808.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199808.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199808.raw.json
2.24 minutes on apw_eng_199808.conllu
-> searching Apw.conll/apw_eng_199809.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199809.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199809.raw.json
2.43 minutes on apw_eng_199809.conllu
-> searching Apw.conll/apw_eng_199810.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199810.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199810.raw.json
2.48 minutes on apw_eng_199810.conllu
-> searching Apw.conll/apw_eng_199811.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199811.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199811.raw.json
2.36 minutes on apw_eng_199811.conllu
-> searching Apw.conll/apw_eng_199812.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199812.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199812.raw.json
2.81 minutes on apw_eng_199812.conllu
-> searching Apw.conll/apw_eng_199901.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199901.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199901.raw.json
2.59 minutes on apw_eng_199901.conllu
-> searching Apw.conll/apw_eng_199902.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199902.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199902.raw.json
2.37 minutes on apw_eng_199902.conllu
-> searching Apw.conll/apw_eng_199903.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199903.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199903.raw.json
3.01 minutes on apw_eng_199903.conllu
-> searching Apw.conll/apw_eng_199904.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199904.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199904.raw.json
2.74 minutes on apw_eng_199904.conllu
-> searching Apw.conll/apw_eng_199905.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199905.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199905.raw.json
2.91 minutes on apw_eng_199905.conllu
-> searching Apw.conll/apw_eng_199906.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199906.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199906.raw.json
2.95 minutes on apw_eng_199906.conllu
-> searching Apw.conll/apw_eng_199907.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199907.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199907.raw.json
2.76 minutes on apw_eng_199907.conllu
-> searching Apw.conll/apw_eng_199908.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199908.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199908.raw.json
1.82 minutes on apw_eng_199908.conllu
-> searching Apw.conll/apw_eng_199909.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199909.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199909.raw.json
1.56 minutes on apw_eng_199909.conllu
-> searching Apw.conll/apw_eng_199910.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199910.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199910.raw.json
1.8 minutes on apw_eng_199910.conllu
-> searching Apw.conll/apw_eng_199911.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_199911.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching Apw.conll/apw_eng_200001.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200001.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200001.raw.json
1.8 minutes on apw_eng_200001.conllu
-> searching Apw.conll/apw_eng_200002.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200002.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200002.raw.json
1.63 minutes on apw_eng_200002.conllu
-> searching Apw.conll/apw_eng_200003.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200003.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200003.raw.json
1.37 minutes on apw_eng_200003.conllu
-> searching Apw.conll/apw_eng_200004.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200004.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200004.raw.json
1.18 minutes on apw_eng_200004.conllu
-> searching Apw.conll/apw_eng_200005.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200005.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200005.raw.json
1.28 minutes on apw_eng_200005.conllu
-> searching Apw.conll/apw_eng_200006.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200006.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200006.raw.json
1.15 minutes on apw_eng_200006.conllu
-> searching Apw.conll/apw_eng_200007.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200007.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200007.raw.json
1.11 minutes on apw_eng_200007.conllu
-> searching Apw.conll/apw_eng_200008.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200008.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200008.raw.json
1.06 minutes on apw_eng_200008.conllu
-> searching Apw.conll/apw_eng_200009.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200009.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200009.raw.json
1.14 minutes on apw_eng_200009.conllu
-> searching Apw.conll/apw_eng_200010.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200010.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200010.raw.json
4.66 minutes on apw_eng_200010.conllu
-> searching Apw.conll/apw_eng_200011.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200011.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200011.raw.json
5.05 minutes on apw_eng_200011.conllu
-> searching Apw.conll/apw_eng_200012.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200012.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200012.raw.json
4.78 minutes on apw_eng_200012.conllu
-> searching Apw.conll/apw_eng_200101.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200101.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200101.raw.json
4.82 minutes on apw_eng_200101.conllu
-> searching Apw.conll/apw_eng_200102.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200102.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200102.raw.json
4.25 minutes on apw_eng_200102.conllu
-> searching Apw.conll/apw_eng_200103.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200103.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200103.raw.json
5.06 minutes on apw_eng_200103.conllu
-> searching Apw.conll/apw_eng_200104.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200104.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200104.raw.json
4.73 minutes on apw_eng_200104.conllu
-> searching Apw.conll/apw_eng_200105.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200105.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200105.raw.json
5.01 minutes on apw_eng_200105.conllu
-> searching Apw.conll/apw_eng_200106.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200106.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200106.raw.json
5.06 minutes on apw_eng_200106.conllu
-> searching Apw.conll/apw_eng_200107.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200107.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200107.raw.json
4.79 minutes on apw_eng_200107.conllu
-> searching Apw.conll/apw_eng_200108.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200108.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200108.raw.json
2.75 minutes on apw_eng_200108.conllu
-> searching Apw.conll/apw_eng_200109.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200109.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200109.raw.json
3.68 minutes on apw_eng_200109.conllu
-> searching Apw.conll/apw_eng_200110.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200110.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200110.raw.json
3.81 minutes on apw_eng_200110.conllu
-> searching Apw.conll/apw_eng_200111.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200111.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200111.raw.json
3.46 minutes on apw_eng_200111.conllu
-> searching Apw.conll/apw_eng_200112.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200112.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200112.raw.json
3.2 minutes on apw_eng_200112.conllu
-> searching Apw.conll/apw_eng_200201.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200201.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200201.raw.json
3.64 minutes on apw_eng_200201.conllu
-> searching Apw.conll/apw_eng_200202.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200202.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200202.raw.json
3.5 minutes on apw_eng_200202.conllu
-> searching Apw.conll/apw_eng_200203.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200203.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200203.raw.json
3.81 minutes on apw_eng_200203.conllu
-> searching Apw.conll/apw_eng_200204.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200204.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200204.raw.json
3.86 minutes on apw_eng_200204.conllu
-> searching Apw.conll/apw_eng_200205.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200205.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200205.raw.json
3.96 minutes on apw_eng_200205.conllu
-> searching Apw.conll/apw_eng_200206.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200206.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200206.raw.json
3.81 minutes on apw_eng_200206.conllu
-> searching Apw.conll/apw_eng_200207.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200207.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200207.raw.json
3.88 minutes on apw_eng_200207.conllu
-> searching Apw.conll/apw_eng_200208.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200208.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200208.raw.json
3.43 minutes on apw_eng_200208.conllu
-> searching Apw.conll/apw_eng_200209.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200209.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200209.raw.json
3.84 minutes on apw_eng_200209.conllu
-> searching Apw.conll/apw_eng_200210.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200210.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200210.raw.json
4.25 minutes on apw_eng_200210.conllu
-> searching Apw.conll/apw_eng_200211.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200211.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200211.raw.json
3.7 minutes on apw_eng_200211.conllu
-> searching Apw.conll/apw_eng_200212.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200212.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200212.raw.json
2.84 minutes on apw_eng_200212.conllu
-> searching Apw.conll/apw_eng_200301.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200301.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200301.raw.json
4.07 minutes on apw_eng_200301.conllu
-> searching Apw.conll/apw_eng_200302.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200302.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200302.raw.json
4.03 minutes on apw_eng_200302.conllu
-> searching Apw.conll/apw_eng_200303.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200303.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200303.raw.json
4.67 minutes on apw_eng_200303.conllu
-> searching Apw.conll/apw_eng_200304.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200304.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200304.raw.json
4.12 minutes on apw_eng_200304.conllu
-> searching Apw.conll/apw_eng_200305.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200305.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200305.raw.json
4.07 minutes on apw_eng_200305.conllu
-> searching Apw.conll/apw_eng_200306.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200306.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200306.raw.json
3.22 minutes on apw_eng_200306.conllu
-> searching Apw.conll/apw_eng_200307.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200307.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200307.raw.json
1.36 minutes on apw_eng_200307.conllu
-> searching Apw.conll/apw_eng_200308.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200308.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200308.raw.json
3.7 minutes on apw_eng_200308.conllu
-> searching Apw.conll/apw_eng_200309.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200309.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200309.raw.json
4.27 minutes on apw_eng_200309.conllu
-> searching Apw.conll/apw_eng_200310.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200310.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200310.raw.json
5.03 minutes on apw_eng_200310.conllu
-> searching Apw.conll/apw_eng_200311.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200311.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200311.raw.json
4.33 minutes on apw_eng_200311.conllu
-> searching Apw.conll/apw_eng_200312.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200312.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200312.raw.json
3.93 minutes on apw_eng_200312.conllu
-> searching Apw.conll/apw_eng_200401.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200401.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200401.raw.json
2.35 minutes on apw_eng_200401.conllu
-> searching Apw.conll/apw_eng_200402.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200402.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200402.raw.json
3.14 minutes on apw_eng_200402.conllu
-> searching Apw.conll/apw_eng_200403.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200403.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200403.raw.json
5.17 minutes on apw_eng_200403.conllu
-> searching Apw.conll/apw_eng_200404.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200404.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200404.raw.json
4.5 minutes on apw_eng_200404.conllu
-> searching Apw.conll/apw_eng_200405.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200405.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200405.raw.json
0.89 minutes on apw_eng_200405.conllu
-> searching Apw.conll/apw_eng_200406.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200406.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200406.raw.json
0.84 minutes on apw_eng_200406.conllu
-> searching Apw.conll/apw_eng_200407.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200407.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200407.raw.json
2.06 minutes on apw_eng_200407.conllu
-> searching Apw.conll/apw_eng_200408.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200408.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200408.raw.json
1.81 minutes on apw_eng_200408.conllu
-> searching Apw.conll/apw_eng_200409.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200409.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200409.raw.json
1.92 minutes on apw_eng_200409.conllu
-> searching Apw.conll/apw_eng_200410.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200410.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200410.raw.json
2.18 minutes on apw_eng_200410.conllu
-> searching Apw.conll/apw_eng_200411.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200411.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200411.raw.json
1.59 minutes on apw_eng_200411.conllu
-> searching Apw.conll/apw_eng_200412.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200412.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200412.raw.json
0.6 minutes on apw_eng_200412.conllu
-> searching Apw.conll/apw_eng_200501.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200501.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200501.raw.json
1.63 minutes on apw_eng_200501.conllu
-> searching Apw.conll/apw_eng_200502.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200502.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200502.raw.json
1.43 minutes on apw_eng_200502.conllu
-> searching Apw.conll/apw_eng_200503.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200503.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200503.raw.json
2.16 minutes on apw_eng_200503.conllu
-> searching Apw.conll/apw_eng_200504.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200504.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200504.raw.json
1.57 minutes on apw_eng_200504.conllu
-> searching Apw.conll/apw_eng_200505.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200505.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200505.raw.json
2.07 minutes on apw_eng_200505.conllu
-> searching Apw.conll/apw_eng_200506.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200506.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200506.raw.json
2.15 minutes on apw_eng_200506.conllu
-> searching Apw.conll/apw_eng_200507.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200507.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200507.raw.json
1.45 minutes on apw_eng_200507.conllu
-> searching Apw.conll/apw_eng_200508.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200508.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200508.raw.json
1.91 minutes on apw_eng_200508.conllu
-> searching Apw.conll/apw_eng_200509.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200509.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200509.raw.json
2.33 minutes on apw_eng_200509.conllu
-> searching Apw.conll/apw_eng_200510.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200510.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200510.raw.json
2.21 minutes on apw_eng_200510.conllu
-> searching Apw.conll/apw_eng_200511.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200511.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200511.raw.json
2.15 minutes on apw_eng_200511.conllu
-> searching Apw.conll/apw_eng_200512.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200512.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200512.raw.json
2.15 minutes on apw_eng_200512.conllu
-> searching Apw.conll/apw_eng_200601.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200601.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200601.raw.json
2.24 minutes on apw_eng_200601.conllu
-> searching Apw.conll/apw_eng_200602.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200602.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200602.raw.json
1.82 minutes on apw_eng_200602.conllu
-> searching Apw.conll/apw_eng_200603.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200603.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200603.raw.json
2.44 minutes on apw_eng_200603.conllu
-> searching Apw.conll/apw_eng_200604.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200604.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200604.raw.json
1.9 minutes on apw_eng_200604.conllu
-> searching Apw.conll/apw_eng_200605.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200605.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200605.raw.json
2.45 minutes on apw_eng_200605.conllu
-> searching Apw.conll/apw_eng_200606.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200606.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200606.raw.json
2.3 minutes on apw_eng_200606.conllu
-> searching Apw.conll/apw_eng_200607.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200607.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200607.raw.json
2.19 minutes on apw_eng_200607.conllu
-> searching Apw.conll/apw_eng_200608.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200608.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200608.raw.json
1.98 minutes on apw_eng_200608.conllu
-> searching Apw.conll/apw_eng_200609.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200609.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200609.raw.json
1.92 minutes on apw_eng_200609.conllu
-> searching Apw.conll/apw_eng_200610.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200610.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200610.raw.json
4.66 minutes on apw_eng_200610.conllu
-> searching Apw.conll/apw_eng_200611.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200611.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200611.raw.json
4.69 minutes on apw_eng_200611.conllu
-> searching Apw.conll/apw_eng_200612.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200612.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200612.raw.json
1.59 minutes on apw_eng_200612.conllu
-> searching Apw.conll/apw_eng_200701.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200701.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200701.raw.json
4.69 minutes on apw_eng_200701.conllu
-> searching Apw.conll/apw_eng_200702.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200702.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200702.raw.json
4.17 minutes on apw_eng_200702.conllu
-> searching Apw.conll/apw_eng_200703.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200703.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200703.raw.json
4.65 minutes on apw_eng_200703.conllu
-> searching Apw.conll/apw_eng_200704.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200704.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200704.raw.json
4.33 minutes on apw_eng_200704.conllu
-> searching Apw.conll/apw_eng_200705.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200705.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200705.raw.json
4.52 minutes on apw_eng_200705.conllu
-> searching Apw.conll/apw_eng_200706.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200706.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200706.raw.json
4.3 minutes on apw_eng_200706.conllu
-> searching Apw.conll/apw_eng_200707.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200707.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200707.raw.json
4.1 minutes on apw_eng_200707.conllu
-> searching Apw.conll/apw_eng_200708.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200708.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200708.raw.json
4.3 minutes on apw_eng_200708.conllu
-> searching Apw.conll/apw_eng_200709.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200709.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200709.raw.json
4.35 minutes on apw_eng_200709.conllu
-> searching Apw.conll/apw_eng_200710.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200710.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200710.raw.json
4.27 minutes on apw_eng_200710.conllu
-> searching Apw.conll/apw_eng_200711.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200711.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200711.raw.json
3.96 minutes on apw_eng_200711.conllu
-> searching Apw.conll/apw_eng_200712.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200712.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200712.raw.json
3.29 minutes on apw_eng_200712.conllu
-> searching Apw.conll/apw_eng_200801.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200801.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200801.raw.json
4.15 minutes on apw_eng_200801.conllu
-> searching Apw.conll/apw_eng_200802.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200802.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200802.raw.json
4.1 minutes on apw_eng_200802.conllu
-> searching Apw.conll/apw_eng_200803.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200803.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200803.raw.json
4.06 minutes on apw_eng_200803.conllu
-> searching Apw.conll/apw_eng_200804.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200804.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200804.raw.json
3.93 minutes on apw_eng_200804.conllu
-> searching Apw.conll/apw_eng_200805.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200805.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200805.raw.json
4.1 minutes on apw_eng_200805.conllu
-> searching Apw.conll/apw_eng_200806.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200806.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200806.raw.json
4.04 minutes on apw_eng_200806.conllu
-> searching Apw.conll/apw_eng_200807.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200807.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200807.raw.json
3.53 minutes on apw_eng_200807.conllu
-> searching Apw.conll/apw_eng_200808.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200808.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200808.raw.json
3.57 minutes on apw_eng_200808.conllu
-> searching Apw.conll/apw_eng_200809.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200809.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200809.raw.json
3.65 minutes on apw_eng_200809.conllu
-> searching Apw.conll/apw_eng_200810.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200810.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200810.raw.json
3.46 minutes on apw_eng_200810.conllu
-> searching Apw.conll/apw_eng_200811.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200811.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200811.raw.json
2.71 minutes on apw_eng_200811.conllu
-> searching Apw.conll/apw_eng_200812.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200812.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200812.raw.json
2.28 minutes on apw_eng_200812.conllu
-> searching Apw.conll/apw_eng_200901.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200901.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200901.raw.json
2.93 minutes on apw_eng_200901.conllu
-> searching Apw.conll/apw_eng_200902.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200902.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200902.raw.json
2.91 minutes on apw_eng_200902.conllu
-> searching Apw.conll/apw_eng_200903.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200903.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200903.raw.json
3.21 minutes on apw_eng_200903.conllu
-> searching Apw.conll/apw_eng_200904.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200904.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200904.raw.json
3.54 minutes on apw_eng_200904.conllu
-> searching Apw.conll/apw_eng_200905.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200905.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200905.raw.json
3.36 minutes on apw_eng_200905.conllu
-> searching Apw.conll/apw_eng_200906.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200906.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200906.raw.json
3.47 minutes on apw_eng_200906.conllu
-> searching Apw.conll/apw_eng_200907.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200907.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200907.raw.json
2.21 minutes on apw_eng_200907.conllu
-> searching Apw.conll/apw_eng_200908.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200908.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200908.raw.json
2.36 minutes on apw_eng_200908.conllu
-> searching Apw.conll/apw_eng_200909.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200909.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200909.raw.json
2.3 minutes on apw_eng_200909.conllu
-> searching Apw.conll/apw_eng_200910.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200910.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200910.raw.json
2.3 minutes on apw_eng_200910.conllu
-> searching Apw.conll/apw_eng_200911.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200911.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200911.raw.json
2.27 minutes on apw_eng_200911.conllu
-> searching Apw.conll/apw_eng_200912.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_200912.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_200912.raw.json
2.38 minutes on apw_eng_200912.conllu
-> searching Apw.conll/apw_eng_201001.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201001.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201001.raw.json
2.81 minutes on apw_eng_201001.conllu
-> searching Apw.conll/apw_eng_201002.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201002.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201002.raw.json
1.91 minutes on apw_eng_201002.conllu
-> searching Apw.conll/apw_eng_201003.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201003.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201003.raw.json
2.1 minutes on apw_eng_201003.conllu
-> searching Apw.conll/apw_eng_201004.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201004.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201004.raw.json
2.06 minutes on apw_eng_201004.conllu
-> searching Apw.conll/apw_eng_201005.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201005.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201005.raw.json
2.06 minutes on apw_eng_201005.conllu
-> searching Apw.conll/apw_eng_201006.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201006.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201006.raw.json
2.17 minutes on apw_eng_201006.conllu
-> searching Apw.conll/apw_eng_201007.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201007.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201007.raw.json
1.78 minutes on apw_eng_201007.conllu
-> searching Apw.conll/apw_eng_201008.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201008.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201008.raw.json
2.78 minutes on apw_eng_201008.conllu
-> searching Apw.conll/apw_eng_201009.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201009.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201009.raw.json
3.02 minutes on apw_eng_201009.conllu
-> searching Apw.conll/apw_eng_201010.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201010.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201010.raw.json
3.12 minutes on apw_eng_201010.conllu
-> searching Apw.conll/apw_eng_201011.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201011.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201011.raw.json
3.26 minutes on apw_eng_201011.conllu
-> searching Apw.conll/apw_eng_201012.conllu:
grew grep -pattern Pat/neg-mit/almost-none_subj.pat -i Apw.conll/apw_eng_201012.conllu > data/neg-mit/Apw.almost-none_subj/apw_eng_201012.raw.json
2.66 minutes on apw_eng_201012.conllu

Total grew search time: 554.81 minutes
==============================================

```
### Running `FillJson.py` script on json files in `Apw.almost-none_subj` from conll files in `Apw.conll`...
```
-> Processing apw_eng_200305...
-> Skipping. (file is empty)
-> Processing apw_eng_200207...
-> Skipping. (file is empty)
-> Processing apw_eng_200706...
-> Skipping. (file is empty)
-> Processing apw_eng_200206...
-> Skipping. (file is empty)
-> Processing apw_eng_200307...
-> Skipping. (file is empty)
-> Processing apw_eng_199701...
-> Skipping. (file is empty)
-> Processing apw_eng_201011...
-> Skipping. (file is empty)
-> Processing apw_eng_199604...
-> Skipping. (file is empty)
-> Processing apw_eng_200702...
-> Skipping. (file is empty)
-> Processing apw_eng_200805...
-> Skipping. (file is empty)
-> Processing apw_eng_200811...
-> Skipping. (file is empty)
-> Processing apw_eng_200308...
-> Skipping. (file is empty)
-> Processing apw_eng_199411...
-> Skipping. (file is empty)
-> Processing apw_eng_201006...
-> Skipping. (file is empty)
-> Processing apw_eng_199610...
-> Skipping. (file is empty)
-> Processing apw_eng_200802...
-> Skipping. (file is empty)
-> Processing apw_eng_200501...
-> Skipping. (file is empty)
-> Processing apw_eng_200002...
-> Skipping. (file is empty)
-> Processing apw_eng_201003...
-> Skipping. (file is empty)
-> Processing apw_eng_200804...
-> Skipping. (file is empty)
-> Processing apw_eng_200902...
-> Skipping. (file is empty)
-> Processing apw_eng_199812...
-> Skipping. (file is empty)
-> Processing apw_eng_200609...
-> Skipping. (file is empty)
-> Processing apw_eng_200107...
-> Skipping. (file is empty)
-> Processing apw_eng_201004...
-> Skipping. (file is empty)
-> Processing apw_eng_200407...
-> Skipping. (file is empty)
-> Processing apw_eng_201005...
-> Skipping. (file is empty)
-> Processing apw_eng_200710...
-> Skipping. (file is empty)
-> Processing apw_eng_200106...
-> Skipping. (file is empty)
-> Processing apw_eng_201010...
-> Skipping. (file is empty)
-> Processing apw_eng_199802...
-> Skipping. (file is empty)
-> Processing apw_eng_200003...
-> Skipping. (file is empty)
-> Processing apw_eng_199710...
-> Skipping. (file is empty)
-> Processing apw_eng_199806...
-> Skipping. (file is empty)
-> Processing apw_eng_200102...
-> Skipping. (file is empty)
-> Processing apw_eng_200204...
-> Skipping. (file is empty)
-> Processing apw_eng_200711...
-> Skipping. (file is empty)
-> Processing apw_eng_200508...
-> Skipping. (file is empty)
-> Processing apw_eng_200110...
-> Skipping. (file is empty)
-> Processing apw_eng_200808...
-> Skipping. (file is empty)
-> Processing apw_eng_200909...
-> Skipping. (file is empty)
-> Processing apw_eng_201002...
-> Skipping. (file is empty)
-> Processing apw_eng_200403...
-> Skipping. (file is empty)
-> Processing apw_eng_199611...
-> Skipping. (file is empty)
-> Processing apw_eng_200203...
-> Skipping. (file is empty)
-> Processing apw_eng_199907...
-> Skipping. (file is empty)
-> Processing apw_eng_199704...
-> Skipping. (file is empty)
-> Processing apw_eng_199706...
-> Skipping. (file is empty)
-> Processing apw_eng_199512...
-> Skipping. (file is empty)
-> Processing apw_eng_199703...
-> Skipping. (file is empty)
-> Processing apw_eng_200311...
-> Skipping. (file is empty)
-> Processing apw_eng_199502...
-> Skipping. (file is empty)
-> Processing apw_eng_200904...
-> Skipping. (file is empty)
-> Processing apw_eng_199510...
-> Skipping. (file is empty)
-> Processing apw_eng_200701...
-> Skipping. (file is empty)
-> Processing apw_eng_199602...
-> Skipping. (file is empty)
-> Processing apw_eng_200612...
-> Skipping. (file is empty)
-> Processing apw_eng_200809...
-> Skipping. (file is empty)
-> Processing apw_eng_199601...
-> Skipping. (file is empty)
-> Processing apw_eng_201009...
-> Skipping. (file is empty)
-> Processing apw_eng_200306...
-> Skipping. (file is empty)
-> Processing apw_eng_200408...
-> Skipping. (file is empty)
-> Processing apw_eng_200411...
-> Skipping. (file is empty)
-> Processing apw_eng_200603...
-> Skipping. (file is empty)
-> Processing apw_eng_200807...
-> Skipping. (file is empty)
-> Processing apw_eng_200301...
-> Skipping. (file is empty)
-> Processing apw_eng_200901...
-> Skipping. (file is empty)
-> Processing apw_eng_199801...
-> Skipping. (file is empty)
-> Processing apw_eng_200409...
-> Skipping. (file is empty)
-> Processing apw_eng_200712...
-> Skipping. (file is empty)
-> Processing apw_eng_199603...
-> Skipping. (file is empty)
-> Processing apw_eng_199909...
-> Skipping. (file is empty)
-> Processing apw_eng_200103...
-> Skipping. (file is empty)
-> Processing apw_eng_200505...
-> Skipping. (file is empty)
-> Processing apw_eng_200604...
-> Skipping. (file is empty)
-> Processing apw_eng_200907...
-> Skipping. (file is empty)
-> Processing apw_eng_200509...
-> Skipping. (file is empty)
-> Processing apw_eng_200905...
-> Skipping. (file is empty)
-> Processing apw_eng_199503...
-> Skipping. (file is empty)
-> Processing apw_eng_199808...
-> Skipping. (file is empty)
-> Processing apw_eng_200109...
-> Skipping. (file is empty)
-> Processing apw_eng_201007...
-> Skipping. (file is empty)
-> Processing apw_eng_200303...
-> Skipping. (file is empty)
-> Processing apw_eng_200008...
-> Skipping. (file is empty)
-> Processing apw_eng_199501...
-> Skipping. (file is empty)
-> Processing apw_eng_200010...
-> Skipping. (file is empty)
-> Processing apw_eng_200405...
-> Skipping. (file is empty)
-> Processing apw_eng_200507...
-> Skipping. (file is empty)
-> Processing apw_eng_199903...
-> Skipping. (file is empty)
-> Processing apw_eng_200009...
-> Skipping. (file is empty)
-> Processing apw_eng_200607...
-> Skipping. (file is empty)
-> Processing apw_eng_200611...
-> Skipping. (file is empty)
-> Processing apw_eng_199901...
-> Skipping. (file is empty)
-> Processing apw_eng_200210...
-> Skipping. (file is empty)
-> Processing apw_eng_200410...
-> Skipping. (file is empty)
-> Processing apw_eng_199807...
-> Skipping. (file is empty)
-> Processing apw_eng_200104...
-> Skipping. (file is empty)
-> Processing apw_eng_200105...
-> Skipping. (file is empty)
-> Processing apw_eng_200202...
-> Skipping. (file is empty)
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
-> Processing apw_eng_200012...
-> Skipping. (file is empty)
-> Processing apw_eng_199910...
-> Skipping. (file is empty)
-> Processing apw_eng_200108...
-> Skipping. (file is empty)
-> Processing apw_eng_200503...
-> Skipping. (file is empty)
-> Processing apw_eng_200708...
-> Skipping. (file is empty)
-> Processing apw_eng_200111...
-> Skipping. (file is empty)
-> Processing apw_eng_200801...
-> Skipping. (file is empty)
-> Processing apw_eng_200412...
-> Skipping. (file is empty)
-> Processing apw_eng_200006...
-> Skipping. (file is empty)
-> Processing apw_eng_200201...
-> Skipping. (file is empty)
-> Processing apw_eng_199504...
-> Skipping. (file is empty)
-> Processing apw_eng_200608...
-> Skipping. (file is empty)
-> Processing apw_eng_199811...
-> Skipping. (file is empty)
-> Processing apw_eng_199906...
-> Skipping. (file is empty)
-> Processing apw_eng_199908...
-> Skipping. (file is empty)
-> Processing apw_eng_200309...
-> Skipping. (file is empty)
-> Processing apw_eng_199606...
-> Skipping. (file is empty)
-> Processing apw_eng_199607...
-> Skipping. (file is empty)
-> Processing apw_eng_199712...
-> Skipping. (file is empty)
-> Processing apw_eng_200312...
-> Skipping. (file is empty)
-> Processing apw_eng_200704...
-> Skipping. (file is empty)
-> Processing apw_eng_200205...
-> Skipping. (file is empty)
-> Processing apw_eng_201008...
-> Skipping. (file is empty)
-> Processing apw_eng_200209...
-> Skipping. (file is empty)
-> Processing apw_eng_200304...
-> Skipping. (file is empty)
-> Processing apw_eng_199708...
-> Skipping. (file is empty)
-> Processing apw_eng_200803...
-> Skipping. (file is empty)
-> Processing apw_eng_200510...
-> Skipping. (file is empty)
-> Processing apw_eng_200911...
-> Skipping. (file is empty)
-> Processing apw_eng_201001...
-> Skipping. (file is empty)
-> Processing apw_eng_200908...
-> Skipping. (file is empty)
-> Processing apw_eng_199506...
-> Skipping. (file is empty)
-> Processing apw_eng_200606...
-> Skipping. (file is empty)
-> Processing apw_eng_199809...
-> Skipping. (file is empty)
-> Processing apw_eng_200602...
-> Skipping. (file is empty)
-> Processing apw_eng_200903...
-> Skipping. (file is empty)
-> Processing apw_eng_199904...
-> Skipping. (file is empty)
-> Processing apw_eng_200806...
-> Skipping. (file is empty)
-> Processing apw_eng_200910...
-> Skipping. (file is empty)
-> Processing apw_eng_199507...
-> Skipping. (file is empty)
-> Processing apw_eng_199905...
-> Skipping. (file is empty)
-> Processing apw_eng_200310...
-> Skipping. (file is empty)
-> Processing apw_eng_200406...
-> Skipping. (file is empty)
-> Processing apw_eng_200705...
-> Skipping. (file is empty)
-> Processing apw_eng_200004...
-> Skipping. (file is empty)
-> Processing apw_eng_200810...
-> Skipping. (file is empty)
-> Processing apw_eng_200211...
-> Skipping. (file is empty)
-> Processing apw_eng_200512...
-> Skipping. (file is empty)
-> Processing apw_eng_200601...
-> Skipping. (file is empty)
-> Processing apw_eng_200101...
-> Skipping. (file is empty)
-> Processing apw_eng_199511...
-> Skipping. (file is empty)
-> Processing apw_eng_200707...
-> Skipping. (file is empty)
-> Processing apw_eng_200812...
-> Skipping. (file is empty)
-> Processing apw_eng_200005...
-> Skipping. (file is empty)
-> Processing apw_eng_199505...
-> Skipping. (file is empty)
-> Processing apw_eng_200212...
-> Skipping. (file is empty)
-> Processing apw_eng_199803...
-> Skipping. (file is empty)
-> Processing apw_eng_199902...
-> Skipping. (file is empty)
-> Processing apw_eng_200001...
-> Skipping. (file is empty)
-> Processing apw_eng_199810...
-> Skipping. (file is empty)
-> Processing apw_eng_200506...
-> Skipping. (file is empty)
-> Processing apw_eng_199805...
-> Skipping. (file is empty)
-> Processing apw_eng_200402...
-> Skipping. (file is empty)
-> Processing apw_eng_200502...
-> Skipping. (file is empty)
-> Processing apw_eng_200112...
-> Skipping. (file is empty)
-> Processing apw_eng_200511...
-> Skipping. (file is empty)
-> Processing apw_eng_199609...
-> Skipping. (file is empty)
-> Processing apw_eng_199608...
-> Skipping. (file is empty)
-> Processing apw_eng_200504...
-> Skipping. (file is empty)
-> Processing apw_eng_200404...
-> Skipping. (file is empty)
-> Processing apw_eng_200007...
-> Skipping. (file is empty)
-> Processing apw_eng_200703...
-> Skipping. (file is empty)
-> Processing apw_eng_199605...
-> Skipping. (file is empty)
-> Processing apw_eng_199612...
-> Skipping. (file is empty)
-> Processing apw_eng_200709...
-> Skipping. (file is empty)
-> Processing apw_eng_200302...
-> Skipping. (file is empty)
-> Processing apw_eng_199508...
-> Skipping. (file is empty)
-> Processing apw_eng_199709...
-> Skipping. (file is empty)
-> Processing apw_eng_199711...
-> Skipping. (file is empty)
-> Processing apw_eng_200011...
-> Skipping. (file is empty)
-> Processing apw_eng_200401...
-> Skipping. (file is empty)
-> Processing apw_eng_199412...
-> Skipping. (file is empty)
-> Processing apw_eng_200912...
-> Skipping. (file is empty)
-> Processing apw_eng_199509...
-> Skipping. (file is empty)
-> Processing apw_eng_199702...
-> Skipping. (file is empty)
-> Processing apw_eng_199707...
-> Skipping. (file is empty)
-> Processing apw_eng_200208...
-> Skipping. (file is empty)
-> Processing apw_eng_200610...
-> Skipping. (file is empty)
-> Processing apw_eng_200906...
-> Skipping. (file is empty)
-> Processing apw_eng_199705...
-> Skipping. (file is empty)
-> Processing apw_eng_200605...
-> Skipping. (file is empty)
-> Processing apw_eng_201012...
-> Skipping. (file is empty)
-> Processing apw_eng_199804...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 0.0 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
Error: specified corpus directory does not contain any processed json files.
```  
## Starting context: `few_det-of-subj`
- time stamp: `Thu Aug  5 05:22:26 EDT 2021`
- data directory: `data/neg-mit/Apw.few_det-of-subj`
- hits table: `hits/neg-mit/Apw_few_det-of-subj`
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
 WARNING : [Conll, File Apw.conll/apw_eng_199608.conllu] No blank line at the end of the file
```
### Running grew search on `Apw.conll`...
```
193 total file(s) to be searched.
-> searching Apw.conll/apw_eng_199411.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199411.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199411.raw.json
1.61 minutes on apw_eng_199411.conllu
-> searching Apw.conll/apw_eng_199412.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199412.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199412.raw.json
2.36 minutes on apw_eng_199412.conllu
-> searching Apw.conll/apw_eng_199501.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199501.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199501.raw.json
2.41 minutes on apw_eng_199501.conllu
-> searching Apw.conll/apw_eng_199502.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199502.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199502.raw.json
2.09 minutes on apw_eng_199502.conllu
-> searching Apw.conll/apw_eng_199503.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199503.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199503.raw.json
2.5 minutes on apw_eng_199503.conllu
-> searching Apw.conll/apw_eng_199504.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199504.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199504.raw.json
2.4 minutes on apw_eng_199504.conllu
-> searching Apw.conll/apw_eng_199505.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199505.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199505.raw.json
2.99 minutes on apw_eng_199505.conllu
-> searching Apw.conll/apw_eng_199506.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199506.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199506.raw.json
3.24 minutes on apw_eng_199506.conllu
-> searching Apw.conll/apw_eng_199507.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199507.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199507.raw.json
2.98 minutes on apw_eng_199507.conllu
-> searching Apw.conll/apw_eng_199508.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199508.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199508.raw.json
2.97 minutes on apw_eng_199508.conllu
-> searching Apw.conll/apw_eng_199509.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199509.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199509.raw.json
2.84 minutes on apw_eng_199509.conllu
-> searching Apw.conll/apw_eng_199510.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199510.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199510.raw.json
2.04 minutes on apw_eng_199510.conllu
-> searching Apw.conll/apw_eng_199511.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199511.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199511.raw.json
2.01 minutes on apw_eng_199511.conllu
-> searching Apw.conll/apw_eng_199512.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199512.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199512.raw.json
1.89 minutes on apw_eng_199512.conllu
-> searching Apw.conll/apw_eng_199601.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199601.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199601.raw.json
2.01 minutes on apw_eng_199601.conllu
-> searching Apw.conll/apw_eng_199602.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199602.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199602.raw.json
1.87 minutes on apw_eng_199602.conllu
-> searching Apw.conll/apw_eng_199603.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199603.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199603.raw.json
2.13 minutes on apw_eng_199603.conllu
-> searching Apw.conll/apw_eng_199604.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199604.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199604.raw.json
2.06 minutes on apw_eng_199604.conllu
-> searching Apw.conll/apw_eng_199605.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199605.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199605.raw.json
2.09 minutes on apw_eng_199605.conllu
-> searching Apw.conll/apw_eng_199606.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199606.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199606.raw.json
1.78 minutes on apw_eng_199606.conllu
-> searching Apw.conll/apw_eng_199607.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199607.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199607.raw.json
1.91 minutes on apw_eng_199607.conllu
-> searching Apw.conll/apw_eng_199608.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199608.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199608.raw.json
1.55 minutes on apw_eng_199608.conllu
-> searching Apw.conll/apw_eng_199609.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199609.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199609.raw.json
1.78 minutes on apw_eng_199609.conllu
-> searching Apw.conll/apw_eng_199610.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199610.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199610.raw.json
1.9 minutes on apw_eng_199610.conllu
-> searching Apw.conll/apw_eng_199611.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199611.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199611.raw.json
1.9 minutes on apw_eng_199611.conllu
-> searching Apw.conll/apw_eng_199612.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199612.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199612.raw.json
2.0 minutes on apw_eng_199612.conllu
-> searching Apw.conll/apw_eng_199701.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199701.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199701.raw.json
2.18 minutes on apw_eng_199701.conllu
-> searching Apw.conll/apw_eng_199702.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199702.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199702.raw.json
1.98 minutes on apw_eng_199702.conllu
-> searching Apw.conll/apw_eng_199703.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199703.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199703.raw.json
2.26 minutes on apw_eng_199703.conllu
-> searching Apw.conll/apw_eng_199704.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199704.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199704.raw.json
2.16 minutes on apw_eng_199704.conllu
-> searching Apw.conll/apw_eng_199705.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199705.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199705.raw.json
2.25 minutes on apw_eng_199705.conllu
-> searching Apw.conll/apw_eng_199706.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199706.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199706.raw.json
2.22 minutes on apw_eng_199706.conllu
-> searching Apw.conll/apw_eng_199707.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199707.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199707.raw.json
2.34 minutes on apw_eng_199707.conllu
-> searching Apw.conll/apw_eng_199708.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199708.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199708.raw.json
2.21 minutes on apw_eng_199708.conllu
-> searching Apw.conll/apw_eng_199709.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199709.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199709.raw.json
2.37 minutes on apw_eng_199709.conllu
-> searching Apw.conll/apw_eng_199710.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199710.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199710.raw.json
2.31 minutes on apw_eng_199710.conllu
-> searching Apw.conll/apw_eng_199711.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199711.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199711.raw.json
2.79 minutes on apw_eng_199711.conllu
-> searching Apw.conll/apw_eng_199712.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199712.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199712.raw.json
3.56 minutes on apw_eng_199712.conllu
-> searching Apw.conll/apw_eng_199801.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199801.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199801.raw.json
3.79 minutes on apw_eng_199801.conllu
-> searching Apw.conll/apw_eng_199802.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199802.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199802.raw.json
3.87 minutes on apw_eng_199802.conllu
-> searching Apw.conll/apw_eng_199803.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199803.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199803.raw.json
4.03 minutes on apw_eng_199803.conllu
-> searching Apw.conll/apw_eng_199804.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199804.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199804.raw.json
3.86 minutes on apw_eng_199804.conllu
-> searching Apw.conll/apw_eng_199805.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199805.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199805.raw.json
3.84 minutes on apw_eng_199805.conllu
-> searching Apw.conll/apw_eng_199806.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199806.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199806.raw.json
3.51 minutes on apw_eng_199806.conllu
-> searching Apw.conll/apw_eng_199807.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199807.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199807.raw.json
2.26 minutes on apw_eng_199807.conllu
-> searching Apw.conll/apw_eng_199808.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199808.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199808.raw.json
2.21 minutes on apw_eng_199808.conllu
-> searching Apw.conll/apw_eng_199809.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199809.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199809.raw.json
2.41 minutes on apw_eng_199809.conllu
-> searching Apw.conll/apw_eng_199810.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199810.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199810.raw.json
2.42 minutes on apw_eng_199810.conllu
-> searching Apw.conll/apw_eng_199811.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199811.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199811.raw.json
2.3 minutes on apw_eng_199811.conllu
-> searching Apw.conll/apw_eng_199812.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199812.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199812.raw.json
2.8 minutes on apw_eng_199812.conllu
-> searching Apw.conll/apw_eng_199901.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199901.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199901.raw.json
2.57 minutes on apw_eng_199901.conllu
-> searching Apw.conll/apw_eng_199902.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199902.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199902.raw.json
2.36 minutes on apw_eng_199902.conllu
-> searching Apw.conll/apw_eng_199903.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199903.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199903.raw.json
2.94 minutes on apw_eng_199903.conllu
-> searching Apw.conll/apw_eng_199904.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199904.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199904.raw.json
2.72 minutes on apw_eng_199904.conllu
-> searching Apw.conll/apw_eng_199905.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199905.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199905.raw.json
2.87 minutes on apw_eng_199905.conllu
-> searching Apw.conll/apw_eng_199906.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199906.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199906.raw.json
2.92 minutes on apw_eng_199906.conllu
-> searching Apw.conll/apw_eng_199907.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199907.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199907.raw.json
2.7 minutes on apw_eng_199907.conllu
-> searching Apw.conll/apw_eng_199908.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199908.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199908.raw.json
1.82 minutes on apw_eng_199908.conllu
-> searching Apw.conll/apw_eng_199909.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199909.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199909.raw.json
1.5 minutes on apw_eng_199909.conllu
-> searching Apw.conll/apw_eng_199910.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199910.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199910.raw.json
1.81 minutes on apw_eng_199910.conllu
-> searching Apw.conll/apw_eng_199911.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_199911.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching Apw.conll/apw_eng_200001.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200001.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200001.raw.json
1.76 minutes on apw_eng_200001.conllu
-> searching Apw.conll/apw_eng_200002.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200002.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200002.raw.json
1.61 minutes on apw_eng_200002.conllu
-> searching Apw.conll/apw_eng_200003.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200003.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200003.raw.json
1.34 minutes on apw_eng_200003.conllu
-> searching Apw.conll/apw_eng_200004.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200004.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200004.raw.json
1.16 minutes on apw_eng_200004.conllu
-> searching Apw.conll/apw_eng_200005.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200005.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200005.raw.json
1.31 minutes on apw_eng_200005.conllu
-> searching Apw.conll/apw_eng_200006.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200006.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200006.raw.json
1.13 minutes on apw_eng_200006.conllu
-> searching Apw.conll/apw_eng_200007.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200007.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200007.raw.json
1.1 minutes on apw_eng_200007.conllu
-> searching Apw.conll/apw_eng_200008.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200008.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200008.raw.json
1.04 minutes on apw_eng_200008.conllu
-> searching Apw.conll/apw_eng_200009.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200009.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200009.raw.json
1.11 minutes on apw_eng_200009.conllu
-> searching Apw.conll/apw_eng_200010.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200010.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200010.raw.json
4.51 minutes on apw_eng_200010.conllu
-> searching Apw.conll/apw_eng_200011.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200011.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200011.raw.json
4.85 minutes on apw_eng_200011.conllu
-> searching Apw.conll/apw_eng_200012.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200012.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200012.raw.json
4.64 minutes on apw_eng_200012.conllu
-> searching Apw.conll/apw_eng_200101.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200101.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200101.raw.json
4.75 minutes on apw_eng_200101.conllu
-> searching Apw.conll/apw_eng_200102.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200102.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200102.raw.json
4.14 minutes on apw_eng_200102.conllu
-> searching Apw.conll/apw_eng_200103.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200103.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200103.raw.json
4.98 minutes on apw_eng_200103.conllu
-> searching Apw.conll/apw_eng_200104.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200104.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200104.raw.json
4.63 minutes on apw_eng_200104.conllu
-> searching Apw.conll/apw_eng_200105.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200105.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200105.raw.json
4.97 minutes on apw_eng_200105.conllu
-> searching Apw.conll/apw_eng_200106.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200106.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200106.raw.json
4.95 minutes on apw_eng_200106.conllu
-> searching Apw.conll/apw_eng_200107.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200107.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200107.raw.json
4.77 minutes on apw_eng_200107.conllu
-> searching Apw.conll/apw_eng_200108.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200108.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200108.raw.json
2.69 minutes on apw_eng_200108.conllu
-> searching Apw.conll/apw_eng_200109.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200109.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200109.raw.json
3.63 minutes on apw_eng_200109.conllu
-> searching Apw.conll/apw_eng_200110.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200110.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200110.raw.json
3.8 minutes on apw_eng_200110.conllu
-> searching Apw.conll/apw_eng_200111.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200111.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200111.raw.json
3.39 minutes on apw_eng_200111.conllu
-> searching Apw.conll/apw_eng_200112.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200112.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200112.raw.json
3.2 minutes on apw_eng_200112.conllu
-> searching Apw.conll/apw_eng_200201.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200201.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200201.raw.json
3.61 minutes on apw_eng_200201.conllu
-> searching Apw.conll/apw_eng_200202.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200202.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200202.raw.json
3.45 minutes on apw_eng_200202.conllu
-> searching Apw.conll/apw_eng_200203.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200203.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200203.raw.json
3.77 minutes on apw_eng_200203.conllu
-> searching Apw.conll/apw_eng_200204.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200204.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200204.raw.json
3.79 minutes on apw_eng_200204.conllu
-> searching Apw.conll/apw_eng_200205.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200205.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200205.raw.json
3.84 minutes on apw_eng_200205.conllu
-> searching Apw.conll/apw_eng_200206.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200206.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200206.raw.json
3.77 minutes on apw_eng_200206.conllu
-> searching Apw.conll/apw_eng_200207.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200207.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200207.raw.json
3.81 minutes on apw_eng_200207.conllu
-> searching Apw.conll/apw_eng_200208.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200208.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200208.raw.json
3.42 minutes on apw_eng_200208.conllu
-> searching Apw.conll/apw_eng_200209.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200209.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200209.raw.json
3.76 minutes on apw_eng_200209.conllu
-> searching Apw.conll/apw_eng_200210.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200210.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200210.raw.json
4.2 minutes on apw_eng_200210.conllu
-> searching Apw.conll/apw_eng_200211.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200211.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200211.raw.json
3.75 minutes on apw_eng_200211.conllu
-> searching Apw.conll/apw_eng_200212.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200212.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200212.raw.json
2.82 minutes on apw_eng_200212.conllu
-> searching Apw.conll/apw_eng_200301.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200301.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200301.raw.json
4.05 minutes on apw_eng_200301.conllu
-> searching Apw.conll/apw_eng_200302.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200302.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200302.raw.json
3.97 minutes on apw_eng_200302.conllu
-> searching Apw.conll/apw_eng_200303.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200303.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200303.raw.json
4.67 minutes on apw_eng_200303.conllu
-> searching Apw.conll/apw_eng_200304.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200304.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200304.raw.json
4.07 minutes on apw_eng_200304.conllu
-> searching Apw.conll/apw_eng_200305.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200305.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200305.raw.json
4.02 minutes on apw_eng_200305.conllu
-> searching Apw.conll/apw_eng_200306.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200306.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200306.raw.json
3.21 minutes on apw_eng_200306.conllu
-> searching Apw.conll/apw_eng_200307.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200307.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200307.raw.json
1.35 minutes on apw_eng_200307.conllu
-> searching Apw.conll/apw_eng_200308.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200308.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200308.raw.json
3.7 minutes on apw_eng_200308.conllu
-> searching Apw.conll/apw_eng_200309.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200309.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200309.raw.json
4.23 minutes on apw_eng_200309.conllu
-> searching Apw.conll/apw_eng_200310.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200310.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200310.raw.json
5.0 minutes on apw_eng_200310.conllu
-> searching Apw.conll/apw_eng_200311.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200311.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200311.raw.json
4.3 minutes on apw_eng_200311.conllu
-> searching Apw.conll/apw_eng_200312.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200312.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200312.raw.json
3.99 minutes on apw_eng_200312.conllu
-> searching Apw.conll/apw_eng_200401.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200401.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200401.raw.json
2.33 minutes on apw_eng_200401.conllu
-> searching Apw.conll/apw_eng_200402.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200402.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200402.raw.json
3.14 minutes on apw_eng_200402.conllu
-> searching Apw.conll/apw_eng_200403.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200403.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200403.raw.json
5.11 minutes on apw_eng_200403.conllu
-> searching Apw.conll/apw_eng_200404.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200404.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200404.raw.json
4.48 minutes on apw_eng_200404.conllu
-> searching Apw.conll/apw_eng_200405.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200405.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200405.raw.json
0.9 minutes on apw_eng_200405.conllu
-> searching Apw.conll/apw_eng_200406.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200406.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200406.raw.json
0.83 minutes on apw_eng_200406.conllu
-> searching Apw.conll/apw_eng_200407.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200407.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200407.raw.json
2.02 minutes on apw_eng_200407.conllu
-> searching Apw.conll/apw_eng_200408.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200408.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200408.raw.json
1.79 minutes on apw_eng_200408.conllu
-> searching Apw.conll/apw_eng_200409.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200409.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200409.raw.json
1.91 minutes on apw_eng_200409.conllu
-> searching Apw.conll/apw_eng_200410.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200410.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200410.raw.json
2.16 minutes on apw_eng_200410.conllu
-> searching Apw.conll/apw_eng_200411.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200411.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200411.raw.json
1.56 minutes on apw_eng_200411.conllu
-> searching Apw.conll/apw_eng_200412.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200412.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200412.raw.json
0.58 minutes on apw_eng_200412.conllu
-> searching Apw.conll/apw_eng_200501.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200501.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200501.raw.json
1.63 minutes on apw_eng_200501.conllu
-> searching Apw.conll/apw_eng_200502.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200502.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200502.raw.json
1.4 minutes on apw_eng_200502.conllu
-> searching Apw.conll/apw_eng_200503.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200503.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200503.raw.json
2.14 minutes on apw_eng_200503.conllu
-> searching Apw.conll/apw_eng_200504.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200504.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200504.raw.json
1.55 minutes on apw_eng_200504.conllu
-> searching Apw.conll/apw_eng_200505.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200505.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200505.raw.json
2.02 minutes on apw_eng_200505.conllu
-> searching Apw.conll/apw_eng_200506.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200506.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200506.raw.json
2.14 minutes on apw_eng_200506.conllu
-> searching Apw.conll/apw_eng_200507.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200507.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200507.raw.json
1.42 minutes on apw_eng_200507.conllu
-> searching Apw.conll/apw_eng_200508.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200508.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200508.raw.json
1.9 minutes on apw_eng_200508.conllu
-> searching Apw.conll/apw_eng_200509.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200509.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200509.raw.json
2.33 minutes on apw_eng_200509.conllu
-> searching Apw.conll/apw_eng_200510.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200510.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200510.raw.json
2.17 minutes on apw_eng_200510.conllu
-> searching Apw.conll/apw_eng_200511.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200511.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200511.raw.json
2.14 minutes on apw_eng_200511.conllu
-> searching Apw.conll/apw_eng_200512.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200512.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200512.raw.json
2.16 minutes on apw_eng_200512.conllu
-> searching Apw.conll/apw_eng_200601.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200601.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200601.raw.json
2.26 minutes on apw_eng_200601.conllu
-> searching Apw.conll/apw_eng_200602.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200602.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200602.raw.json
1.82 minutes on apw_eng_200602.conllu
-> searching Apw.conll/apw_eng_200603.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200603.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200603.raw.json
2.42 minutes on apw_eng_200603.conllu
-> searching Apw.conll/apw_eng_200604.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200604.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200604.raw.json
1.89 minutes on apw_eng_200604.conllu
-> searching Apw.conll/apw_eng_200605.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200605.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200605.raw.json
2.44 minutes on apw_eng_200605.conllu
-> searching Apw.conll/apw_eng_200606.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200606.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200606.raw.json
2.29 minutes on apw_eng_200606.conllu
-> searching Apw.conll/apw_eng_200607.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200607.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200607.raw.json
2.2 minutes on apw_eng_200607.conllu
-> searching Apw.conll/apw_eng_200608.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200608.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200608.raw.json
1.96 minutes on apw_eng_200608.conllu
-> searching Apw.conll/apw_eng_200609.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200609.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200609.raw.json
1.91 minutes on apw_eng_200609.conllu
-> searching Apw.conll/apw_eng_200610.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200610.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200610.raw.json
4.61 minutes on apw_eng_200610.conllu
-> searching Apw.conll/apw_eng_200611.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200611.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200611.raw.json
4.65 minutes on apw_eng_200611.conllu
-> searching Apw.conll/apw_eng_200612.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200612.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200612.raw.json
1.61 minutes on apw_eng_200612.conllu
-> searching Apw.conll/apw_eng_200701.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200701.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200701.raw.json
4.67 minutes on apw_eng_200701.conllu
-> searching Apw.conll/apw_eng_200702.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200702.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200702.raw.json
4.12 minutes on apw_eng_200702.conllu
-> searching Apw.conll/apw_eng_200703.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200703.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200703.raw.json
4.65 minutes on apw_eng_200703.conllu
-> searching Apw.conll/apw_eng_200704.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200704.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200704.raw.json
4.33 minutes on apw_eng_200704.conllu
-> searching Apw.conll/apw_eng_200705.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200705.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200705.raw.json
4.58 minutes on apw_eng_200705.conllu
-> searching Apw.conll/apw_eng_200706.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200706.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200706.raw.json
4.31 minutes on apw_eng_200706.conllu
-> searching Apw.conll/apw_eng_200707.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200707.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200707.raw.json
4.12 minutes on apw_eng_200707.conllu
-> searching Apw.conll/apw_eng_200708.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200708.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200708.raw.json
4.18 minutes on apw_eng_200708.conllu
-> searching Apw.conll/apw_eng_200709.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200709.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200709.raw.json
4.33 minutes on apw_eng_200709.conllu
-> searching Apw.conll/apw_eng_200710.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200710.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200710.raw.json
4.21 minutes on apw_eng_200710.conllu
-> searching Apw.conll/apw_eng_200711.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200711.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200711.raw.json
3.94 minutes on apw_eng_200711.conllu
-> searching Apw.conll/apw_eng_200712.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200712.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200712.raw.json
3.28 minutes on apw_eng_200712.conllu
-> searching Apw.conll/apw_eng_200801.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200801.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200801.raw.json
4.16 minutes on apw_eng_200801.conllu
-> searching Apw.conll/apw_eng_200802.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200802.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200802.raw.json
4.04 minutes on apw_eng_200802.conllu
-> searching Apw.conll/apw_eng_200803.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200803.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200803.raw.json
4.08 minutes on apw_eng_200803.conllu
-> searching Apw.conll/apw_eng_200804.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200804.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200804.raw.json
3.93 minutes on apw_eng_200804.conllu
-> searching Apw.conll/apw_eng_200805.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200805.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200805.raw.json
4.09 minutes on apw_eng_200805.conllu
-> searching Apw.conll/apw_eng_200806.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200806.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200806.raw.json
4.05 minutes on apw_eng_200806.conllu
-> searching Apw.conll/apw_eng_200807.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200807.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200807.raw.json
3.56 minutes on apw_eng_200807.conllu
-> searching Apw.conll/apw_eng_200808.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200808.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200808.raw.json
3.63 minutes on apw_eng_200808.conllu
-> searching Apw.conll/apw_eng_200809.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200809.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200809.raw.json
3.75 minutes on apw_eng_200809.conllu
-> searching Apw.conll/apw_eng_200810.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200810.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200810.raw.json
3.54 minutes on apw_eng_200810.conllu
-> searching Apw.conll/apw_eng_200811.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200811.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200811.raw.json
2.77 minutes on apw_eng_200811.conllu
-> searching Apw.conll/apw_eng_200812.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200812.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200812.raw.json
2.28 minutes on apw_eng_200812.conllu
-> searching Apw.conll/apw_eng_200901.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200901.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200901.raw.json
2.96 minutes on apw_eng_200901.conllu
-> searching Apw.conll/apw_eng_200902.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200902.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200902.raw.json
2.93 minutes on apw_eng_200902.conllu
-> searching Apw.conll/apw_eng_200903.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200903.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200903.raw.json
3.19 minutes on apw_eng_200903.conllu
-> searching Apw.conll/apw_eng_200904.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200904.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200904.raw.json
3.58 minutes on apw_eng_200904.conllu
-> searching Apw.conll/apw_eng_200905.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200905.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200905.raw.json
3.41 minutes on apw_eng_200905.conllu
-> searching Apw.conll/apw_eng_200906.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200906.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200906.raw.json
3.52 minutes on apw_eng_200906.conllu
-> searching Apw.conll/apw_eng_200907.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200907.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200907.raw.json
2.25 minutes on apw_eng_200907.conllu
-> searching Apw.conll/apw_eng_200908.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200908.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200908.raw.json
2.36 minutes on apw_eng_200908.conllu
-> searching Apw.conll/apw_eng_200909.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200909.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200909.raw.json
2.25 minutes on apw_eng_200909.conllu
-> searching Apw.conll/apw_eng_200910.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200910.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200910.raw.json
2.3 minutes on apw_eng_200910.conllu
-> searching Apw.conll/apw_eng_200911.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200911.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200911.raw.json
2.25 minutes on apw_eng_200911.conllu
-> searching Apw.conll/apw_eng_200912.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_200912.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_200912.raw.json
2.37 minutes on apw_eng_200912.conllu
-> searching Apw.conll/apw_eng_201001.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201001.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201001.raw.json
2.83 minutes on apw_eng_201001.conllu
-> searching Apw.conll/apw_eng_201002.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201002.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201002.raw.json
1.9 minutes on apw_eng_201002.conllu
-> searching Apw.conll/apw_eng_201003.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201003.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201003.raw.json
2.09 minutes on apw_eng_201003.conllu
-> searching Apw.conll/apw_eng_201004.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201004.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201004.raw.json
2.04 minutes on apw_eng_201004.conllu
-> searching Apw.conll/apw_eng_201005.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201005.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201005.raw.json
2.03 minutes on apw_eng_201005.conllu
-> searching Apw.conll/apw_eng_201006.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201006.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201006.raw.json
2.07 minutes on apw_eng_201006.conllu
-> searching Apw.conll/apw_eng_201007.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201007.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201007.raw.json
1.72 minutes on apw_eng_201007.conllu
-> searching Apw.conll/apw_eng_201008.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201008.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201008.raw.json
2.71 minutes on apw_eng_201008.conllu
-> searching Apw.conll/apw_eng_201009.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201009.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201009.raw.json
2.98 minutes on apw_eng_201009.conllu
-> searching Apw.conll/apw_eng_201010.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201010.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201010.raw.json
3.1 minutes on apw_eng_201010.conllu
-> searching Apw.conll/apw_eng_201011.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201011.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201011.raw.json
3.18 minutes on apw_eng_201011.conllu
-> searching Apw.conll/apw_eng_201012.conllu:
grew grep -pattern Pat/neg-mit/few_det-of-subj.pat -i Apw.conll/apw_eng_201012.conllu > data/neg-mit/Apw.few_det-of-subj/apw_eng_201012.raw.json
2.64 minutes on apw_eng_201012.conllu

Total grew search time: 550.62 minutes
==============================================

```
### Running `FillJson.py` script on json files in `Apw.few_det-of-subj` from conll files in `Apw.conll`...
```
-> Processing apw_eng_200111...
   => 3 hit results filled from 371348 total original sentences in 43.48 seconds
-> Writing output file...
-> Processing apw_eng_200301...
   => 8 hit results filled from 522079 total original sentences in 53.63 seconds
-> Writing output file...
-> Processing apw_eng_200805...
   => 2 hit results filled from 500348 total original sentences in 52.95 seconds
-> Writing output file...
-> Processing apw_eng_201011...
   => 3 hit results filled from 340494 total original sentences in 41.18 seconds
-> Writing output file...
-> Processing apw_eng_199709...
   => 8 hit results filled from 264766 total original sentences in 30.55 seconds
-> Writing output file...
-> Processing apw_eng_199512...
-> Skipping. (file is empty)
-> Processing apw_eng_200405...
-> Skipping. (file is empty)
-> Processing apw_eng_201008...
   => 3 hit results filled from 292035 total original sentences in 35.47 seconds
-> Writing output file...
-> Processing apw_eng_200109...
   => 10 hit results filled from 401352 total original sentences in 47.56 seconds
-> Writing output file...
-> Processing apw_eng_199703...
   => 7 hit results filled from 264519 total original sentences in 29.41 seconds
-> Writing output file...
-> Processing apw_eng_199808...
   => 7 hit results filled from 254664 total original sentences in 28.85 seconds
-> Writing output file...
-> Processing apw_eng_199612...
   => 2 hit results filled from 236714 total original sentences in 25.86 seconds
-> Writing output file...
-> Processing apw_eng_200004...
-> Skipping. (file is empty)
-> Processing apw_eng_199611...
-> Skipping. (file is empty)
-> Processing apw_eng_200203...
   => 4 hit results filled from 413600 total original sentences in 48.37 seconds
-> Writing output file...
-> Processing apw_eng_200311...
   => 3 hit results filled from 532321 total original sentences in 55.83 seconds
-> Writing output file...
-> Processing apw_eng_200807...
   => 3 hit results filled from 415105 total original sentences in 45.99 seconds
-> Writing output file...
-> Processing apw_eng_200306...
-> Skipping. (file is empty)
-> Processing apw_eng_199704...
-> Skipping. (file is empty)
-> Processing apw_eng_200607...
   => 2 hit results filled from 242373 total original sentences in 28.19 seconds
-> Writing output file...
-> Processing apw_eng_200305...
   => 13 hit results filled from 522746 total original sentences in 52.86 seconds
-> Writing output file...
-> Processing apw_eng_200506...
   => 4 hit results filled from 236253 total original sentences in 27.7 seconds
-> Writing output file...
-> Processing apw_eng_201003...
   => 4 hit results filled from 220617 total original sentences in 27.0 seconds
-> Writing output file...
-> Processing apw_eng_199906...
   => 7 hit results filled from 329537 total original sentences in 37.99 seconds
-> Writing output file...
-> Processing apw_eng_200511...
   => 5 hit results filled from 228655 total original sentences in 27.46 seconds
-> Writing output file...
-> Processing apw_eng_201009...
-> Skipping. (file is empty)
-> Processing apw_eng_199804...
   => 5 hit results filled from 484375 total original sentences in 50.64 seconds
-> Writing output file...
-> Processing apw_eng_199504...
   => 3 hit results filled from 280156 total original sentences in 30.71 seconds
-> Writing output file...
-> Processing apw_eng_200106...
   => 2 hit results filled from 751043 total original sentences in 64.67 seconds
-> Writing output file...
-> Processing apw_eng_199412...
   => 4 hit results filled from 275635 total original sentences in 29.65 seconds
-> Writing output file...
-> Processing apw_eng_200102...
   => 2 hit results filled from 580638 total original sentences in 51.64 seconds
-> Writing output file...
-> Processing apw_eng_200801...
   => 5 hit results filled from 489641 total original sentences in 51.94 seconds
-> Writing output file...
-> Processing apw_eng_200703...
   => 4 hit results filled from 545787 total original sentences in 57.0 seconds
-> Writing output file...
-> Processing apw_eng_200806...
   => 4 hit results filled from 501365 total original sentences in 50.7 seconds
-> Writing output file...
-> Processing apw_eng_199511...
   => 1 hit results filled from 232954 total original sentences in 25.04 seconds
-> Writing output file...
-> Processing apw_eng_200402...
-> Skipping. (file is empty)
-> Processing apw_eng_200709...
   => 2 hit results filled from 503440 total original sentences in 54.92 seconds
-> Writing output file...
-> Processing apw_eng_200605...
   => 4 hit results filled from 261725 total original sentences in 30.22 seconds
-> Writing output file...
-> Processing apw_eng_199610...
   => 2 hit results filled from 222915 total original sentences in 23.7 seconds
-> Writing output file...
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
-> Processing apw_eng_199601...
   => 4 hit results filled from 239768 total original sentences in 25.01 seconds
-> Writing output file...
-> Processing apw_eng_201012...
-> Skipping. (file is empty)
-> Processing apw_eng_200309...
   => 5 hit results filled from 517593 total original sentences in 52.94 seconds
-> Writing output file...
-> Processing apw_eng_200104...
-> Skipping. (file is empty)
-> Processing apw_eng_200610...
   => 2 hit results filled from 502029 total original sentences in 56.84 seconds
-> Writing output file...
-> Processing apw_eng_199509...
-> Skipping. (file is empty)
-> Processing apw_eng_200205...
   => 5 hit results filled from 420016 total original sentences in 48.57 seconds
-> Writing output file...
-> Processing apw_eng_200712...
   => 3 hit results filled from 391549 total original sentences in 41.61 seconds
-> Writing output file...
-> Processing apw_eng_200901...
   => 2 hit results filled from 317496 total original sentences in 37.42 seconds
-> Writing output file...
-> Processing apw_eng_199811...
   => 10 hit results filled from 259993 total original sentences in 29.58 seconds
-> Writing output file...
-> Processing apw_eng_200005...
   => 1 hit results filled from 143837 total original sentences in 16.41 seconds
-> Writing output file...
-> Processing apw_eng_200604...
   => 7 hit results filled from 202289 total original sentences in 23.92 seconds
-> Writing output file...
-> Processing apw_eng_200504...
   => 2 hit results filled from 175752 total original sentences in 19.64 seconds
-> Writing output file...
-> Processing apw_eng_200401...
   => 6 hit results filled from 288609 total original sentences in 29.85 seconds
-> Writing output file...
-> Processing apw_eng_199503...
   => 1 hit results filled from 292602 total original sentences in 31.75 seconds
-> Writing output file...
-> Processing apw_eng_200503...
   => 2 hit results filled from 240695 total original sentences in 27.07 seconds
-> Writing output file...
-> Processing apw_eng_200906...
-> Skipping. (file is empty)
-> Processing apw_eng_200912...
-> Skipping. (file is empty)
-> Processing apw_eng_200211...
   => 8 hit results filled from 491643 total original sentences in 46.78 seconds
-> Writing output file...
-> Processing apw_eng_199411...
-> Skipping. (file is empty)
-> Processing apw_eng_199609...
   => 3 hit results filled from 208534 total original sentences in 22.06 seconds
-> Writing output file...
-> Processing apw_eng_200412...
   => 1 hit results filled from 66780 total original sentences in 7.24 seconds
-> Writing output file...
-> Processing apw_eng_199701...
   => 8 hit results filled from 254244 total original sentences in 26.82 seconds
-> Writing output file...
-> Processing apw_eng_200509...
   => 4 hit results filled from 252467 total original sentences in 28.74 seconds
-> Writing output file...
-> Processing apw_eng_200803...
   => 2 hit results filled from 504156 total original sentences in 50.58 seconds
-> Writing output file...
-> Processing apw_eng_200601...
-> Skipping. (file is empty)
-> Processing apw_eng_199507...
   => 1 hit results filled from 337637 total original sentences in 37.08 seconds
-> Writing output file...
-> Processing apw_eng_200408...
   => 2 hit results filled from 210307 total original sentences in 22.29 seconds
-> Writing output file...
-> Processing apw_eng_199606...
   => 2 hit results filled from 208887 total original sentences in 22.29 seconds
-> Writing output file...
-> Processing apw_eng_200210...
   => 21 hit results filled from 547369 total original sentences in 53.22 seconds
-> Writing output file...
-> Processing apw_eng_200108...
   => 3 hit results filled from 304566 total original sentences in 33.85 seconds
-> Writing output file...
-> Processing apw_eng_201004...
   => 4 hit results filled from 217948 total original sentences in 25.65 seconds
-> Writing output file...
-> Processing apw_eng_200009...
   => 2 hit results filled from 124647 total original sentences in 13.84 seconds
-> Writing output file...
-> Processing apw_eng_200101...
   => 4 hit results filled from 658781 total original sentences in 59.4 seconds
-> Writing output file...
-> Processing apw_eng_200502...
-> Skipping. (file is empty)
-> Processing apw_eng_200810...
   => 1 hit results filled from 365833 total original sentences in 44.08 seconds
-> Writing output file...
-> Processing apw_eng_200411...
   => 1 hit results filled from 176180 total original sentences in 19.84 seconds
-> Writing output file...
-> Processing apw_eng_200206...
   => 7 hit results filled from 417879 total original sentences in 48.12 seconds
-> Writing output file...
-> Processing apw_eng_200708...
   => 6 hit results filled from 492115 total original sentences in 53.53 seconds
-> Writing output file...
-> Processing apw_eng_200910...
   => 2 hit results filled from 237390 total original sentences in 28.48 seconds
-> Writing output file...
-> Processing apw_eng_199607...
   => 3 hit results filled from 226339 total original sentences in 24.15 seconds
-> Writing output file...
-> Processing apw_eng_200008...
   => 3 hit results filled from 118530 total original sentences in 13.18 seconds
-> Writing output file...
-> Processing apw_eng_200011...
   => 4 hit results filled from 680092 total original sentences in 61.33 seconds
-> Writing output file...
-> Processing apw_eng_200510...
   => 2 hit results filled from 233906 total original sentences in 27.21 seconds
-> Writing output file...
-> Processing apw_eng_200704...
   => 2 hit results filled from 505054 total original sentences in 54.75 seconds
-> Writing output file...
-> Processing apw_eng_200809...
   => 5 hit results filled from 385353 total original sentences in 45.91 seconds
-> Writing output file...
-> Processing apw_eng_200903...
-> Skipping. (file is empty)
-> Processing apw_eng_201010...
   => 2 hit results filled from 336943 total original sentences in 38.95 seconds
-> Writing output file...
-> Processing apw_eng_200907...
   => 4 hit results filled from 234261 total original sentences in 27.73 seconds
-> Writing output file...
-> Processing apw_eng_199809...
   => 5 hit results filled from 271149 total original sentences in 30.62 seconds
-> Writing output file...
-> Processing apw_eng_199708...
   => 6 hit results filled from 257824 total original sentences in 28.09 seconds
-> Writing output file...
-> Processing apw_eng_200501...
   => 5 hit results filled from 183872 total original sentences in 20.47 seconds
-> Writing output file...
-> Processing apw_eng_200207...
   => 4 hit results filled from 493487 total original sentences in 48.94 seconds
-> Writing output file...
-> Processing apw_eng_199805...
   => 8 hit results filled from 486174 total original sentences in 49.08 seconds
-> Writing output file...
-> Processing apw_eng_199510...
   => 5 hit results filled from 237216 total original sentences in 25.96 seconds
-> Writing output file...
-> Processing apw_eng_199608...
   => 1 hit results filled from 183436 total original sentences in 19.5 seconds
-> Writing output file...
-> Processing apw_eng_200507...
-> Skipping. (file is empty)
-> Processing apw_eng_200609...
-> Skipping. (file is empty)
-> Processing apw_eng_200007...
   => 1 hit results filled from 122479 total original sentences in 13.84 seconds
-> Writing output file...
-> Processing apw_eng_199801...
   => 9 hit results filled from 469278 total original sentences in 47.76 seconds
-> Writing output file...
-> Processing apw_eng_199707...
   => 4 hit results filled from 274132 total original sentences in 29.67 seconds
-> Writing output file...
-> Processing apw_eng_199711...
   => 2 hit results filled from 330740 total original sentences in 35.54 seconds
-> Writing output file...
-> Processing apw_eng_200208...
   => 3 hit results filled from 453026 total original sentences in 43.23 seconds
-> Writing output file...
-> Processing apw_eng_200307...
   => 5 hit results filled from 168441 total original sentences in 17.33 seconds
-> Writing output file...
-> Processing apw_eng_200404...
   => 10 hit results filled from 556081 total original sentences in 56.75 seconds
-> Writing output file...
-> Processing apw_eng_199802...
   => 1 hit results filled from 485186 total original sentences in 49.18 seconds
-> Writing output file...
-> Processing apw_eng_200303...
   => 7 hit results filled from 587201 total original sentences in 59.26 seconds
-> Writing output file...
-> Processing apw_eng_200310...
   => 2 hit results filled from 606436 total original sentences in 63.17 seconds
-> Writing output file...
-> Processing apw_eng_200702...
   => 5 hit results filled from 478880 total original sentences in 53.03 seconds
-> Writing output file...
-> Processing apw_eng_199806...
   => 1 hit results filled from 422120 total original sentences in 45.47 seconds
-> Writing output file...
-> Processing apw_eng_200701...
   => 13 hit results filled from 543943 total original sentences in 59.3 seconds
-> Writing output file...
-> Processing apw_eng_201001...
   => 13 hit results filled from 308772 total original sentences in 35.89 seconds
-> Writing output file...
-> Processing apw_eng_200812...
-> Skipping. (file is empty)
-> Processing apw_eng_200811...
   => 10 hit results filled from 290865 total original sentences in 35.38 seconds
-> Writing output file...
-> Processing apw_eng_199909...
   => 2 hit results filled from 167276 total original sentences in 19.01 seconds
-> Writing output file...
-> Processing apw_eng_200112...
   => 4 hit results filled from 350413 total original sentences in 40.27 seconds
-> Writing output file...
-> Processing apw_eng_200105...
   => 1 hit results filled from 728729 total original sentences in 62.72 seconds
-> Writing output file...
-> Processing apw_eng_199807...
   => 2 hit results filled from 260597 total original sentences in 28.94 seconds
-> Writing output file...
-> Processing apw_eng_200904...
-> Skipping. (file is empty)
-> Processing apw_eng_201006...
   => 3 hit results filled from 227311 total original sentences in 26.97 seconds
-> Writing output file...
-> Processing apw_eng_199907...
   => 11 hit results filled from 308319 total original sentences in 34.5 seconds
-> Writing output file...
-> Processing apw_eng_199602...
   => 13 hit results filled from 221029 total original sentences in 23.75 seconds
-> Writing output file...
-> Processing apw_eng_200705...
   => 3 hit results filled from 522700 total original sentences in 57.4 seconds
-> Writing output file...
-> Processing apw_eng_200710...
   => 4 hit results filled from 496362 total original sentences in 53.77 seconds
-> Writing output file...
-> Processing apw_eng_199902...
   => 4 hit results filled from 266925 total original sentences in 29.43 seconds
-> Writing output file...
-> Processing apw_eng_199604...
   => 2 hit results filled from 242462 total original sentences in 25.68 seconds
-> Writing output file...
-> Processing apw_eng_200308...
   => 3 hit results filled from 471868 total original sentences in 46.35 seconds
-> Writing output file...
-> Processing apw_eng_200611...
   => 5 hit results filled from 513961 total original sentences in 57.28 seconds
-> Writing output file...
-> Processing apw_eng_200808...
   => 3 hit results filled from 419590 total original sentences in 45.51 seconds
-> Writing output file...
-> Processing apw_eng_200002...
-> Skipping. (file is empty)
-> Processing apw_eng_200407...
   => 3 hit results filled from 223683 total original sentences in 25.79 seconds
-> Writing output file...
-> Processing apw_eng_200110...
   => 4 hit results filled from 411385 total original sentences in 47.75 seconds
-> Writing output file...
-> Processing apw_eng_199910...
-> Skipping. (file is empty)
-> Processing apw_eng_199710...
   => 2 hit results filled from 263541 total original sentences in 29.02 seconds
-> Writing output file...
-> Processing apw_eng_201002...
   => 6 hit results filled from 207700 total original sentences in 23.93 seconds
-> Writing output file...
-> Processing apw_eng_200612...
   => 1 hit results filled from 179461 total original sentences in 20.05 seconds
-> Writing output file...
-> Processing apw_eng_200902...
   => 1 hit results filled from 311293 total original sentences in 36.42 seconds
-> Writing output file...
-> Processing apw_eng_200410...
-> Skipping. (file is empty)
-> Processing apw_eng_200212...
   => 1 hit results filled from 368406 total original sentences in 36.29 seconds
-> Writing output file...
-> Processing apw_eng_200312...
   => 1 hit results filled from 488561 total original sentences in 50.64 seconds
-> Writing output file...
-> Processing apw_eng_200409...
-> Skipping. (file is empty)
-> Processing apw_eng_201007...
-> Skipping. (file is empty)
-> Processing apw_eng_200010...
   => 8 hit results filled from 609903 total original sentences in 57.8 seconds
-> Writing output file...
-> Processing apw_eng_199605...
   => 2 hit results filled from 244175 total original sentences in 26.36 seconds
-> Writing output file...
-> Processing apw_eng_200706...
   => 2 hit results filled from 487947 total original sentences in 53.86 seconds
-> Writing output file...
-> Processing apw_eng_201005...
   => 2 hit results filled from 217021 total original sentences in 26.08 seconds
-> Writing output file...
-> Processing apw_eng_200908...
   => 8 hit results filled from 252526 total original sentences in 29.71 seconds
-> Writing output file...
-> Processing apw_eng_200603...
   => 2 hit results filled from 271558 total original sentences in 30.78 seconds
-> Writing output file...
-> Processing apw_eng_200304...
   => 2 hit results filled from 529214 total original sentences in 52.33 seconds
-> Writing output file...
-> Processing apw_eng_200006...
-> Skipping. (file is empty)
-> Processing apw_eng_199702...
   => 4 hit results filled from 234112 total original sentences in 25.41 seconds
-> Writing output file...
-> Processing apw_eng_199501...
   => 2 hit results filled from 285984 total original sentences in 30.44 seconds
-> Writing output file...
-> Processing apw_eng_200012...
   => 5 hit results filled from 646296 total original sentences in 58.38 seconds
-> Writing output file...
-> Processing apw_eng_200508...
   => 2 hit results filled from 218299 total original sentences in 24.19 seconds
-> Writing output file...
-> Processing apw_eng_199803...
   => 4 hit results filled from 510291 total original sentences in 51.38 seconds
-> Writing output file...
-> Processing apw_eng_200204...
   => 1 hit results filled from 410879 total original sentences in 48.06 seconds
-> Writing output file...
-> Processing apw_eng_199904...
   => 9 hit results filled from 305847 total original sentences in 34.36 seconds
-> Writing output file...
-> Processing apw_eng_200406...
-> Skipping. (file is empty)
-> Processing apw_eng_200302...
   => 5 hit results filled from 510838 total original sentences in 51.45 seconds
-> Writing output file...
-> Processing apw_eng_199508...
   => 3 hit results filled from 345561 total original sentences in 37.77 seconds
-> Writing output file...
-> Processing apw_eng_200602...
   => 2 hit results filled from 195866 total original sentences in 22.78 seconds
-> Writing output file...
-> Processing apw_eng_200911...
   => 2 hit results filled from 235123 total original sentences in 28.16 seconds
-> Writing output file...
-> Processing apw_eng_199908...
   => 3 hit results filled from 205618 total original sentences in 22.88 seconds
-> Writing output file...
-> Processing apw_eng_200905...
   => 5 hit results filled from 351728 total original sentences in 42.07 seconds
-> Writing output file...
-> Processing apw_eng_200202...
   => 8 hit results filled from 378007 total original sentences in 44.12 seconds
-> Writing output file...
-> Processing apw_eng_199905...
   => 2 hit results filled from 321831 total original sentences in 36.56 seconds
-> Writing output file...
-> Processing apw_eng_200707...
   => 2 hit results filled from 479109 total original sentences in 52.53 seconds
-> Writing output file...
-> Processing apw_eng_200001...
   => 4 hit results filled from 193637 total original sentences in 22.82 seconds
-> Writing output file...
-> Processing apw_eng_199705...
-> Skipping. (file is empty)
-> Processing apw_eng_200606...
   => 2 hit results filled from 250232 total original sentences in 29.03 seconds
-> Writing output file...
-> Processing apw_eng_200711...
   => 5 hit results filled from 465709 total original sentences in 51.09 seconds
-> Writing output file...
-> Processing apw_eng_199505...
   => 3 hit results filled from 339942 total original sentences in 38.02 seconds
-> Writing output file...
-> Processing apw_eng_200802...
   => 7 hit results filled from 475152 total original sentences in 51.89 seconds
-> Writing output file...
-> Processing apw_eng_199506...
   => 2 hit results filled from 367416 total original sentences in 40.79 seconds
-> Writing output file...
-> Processing apw_eng_199903...
   => 7 hit results filled from 330889 total original sentences in 37.73 seconds
-> Writing output file...
-> Processing apw_eng_200505...
   => 2 hit results filled from 222524 total original sentences in 25.99 seconds
-> Writing output file...
-> Processing apw_eng_200512...
   => 1 hit results filled from 235238 total original sentences in 27.39 seconds
-> Writing output file...
-> Processing apw_eng_200209...
   => 2 hit results filled from 494144 total original sentences in 48.79 seconds
-> Writing output file...
-> Processing apw_eng_200608...
   => 3 hit results filled from 216402 total original sentences in 25.15 seconds
-> Writing output file...
-> Processing apw_eng_200909...
   => 2 hit results filled from 239137 total original sentences in 29.05 seconds
-> Writing output file...
-> Processing apw_eng_200003...
-> Skipping. (file is empty)
-> Processing apw_eng_200103...
-> Skipping. (file is empty)
-> Processing apw_eng_199810...
   => 3 hit results filled from 266434 total original sentences in 30.83 seconds
-> Writing output file...
-> Processing apw_eng_199603...
   => 2 hit results filled from 251662 total original sentences in 27.08 seconds
-> Writing output file...
-> Processing apw_eng_199502...
   => 10 hit results filled from 244262 total original sentences in 26.41 seconds
-> Writing output file...
-> Processing apw_eng_199712...
   => 4 hit results filled from 439289 total original sentences in 45.09 seconds
-> Writing output file...
-> Processing apw_eng_199812...
   => 2 hit results filled from 317619 total original sentences in 35.6 seconds
-> Writing output file...
-> Processing apw_eng_200201...
   => 11 hit results filled from 397280 total original sentences in 46.37 seconds
-> Writing output file...
-> Processing apw_eng_200804...
-> Skipping. (file is empty)
-> Processing apw_eng_200403...
   => 6 hit results filled from 637253 total original sentences in 65.91 seconds
-> Writing output file...
-> Processing apw_eng_199901...
   => 2 hit results filled from 292996 total original sentences in 32.81 seconds
-> Writing output file...
-> Processing apw_eng_199706...
   => 2 hit results filled from 257826 total original sentences in 28.24 seconds
-> Writing output file...
-> Processing apw_eng_200107...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 99.69 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing apw_eng_200111.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20011106_1441_13:7 discarded.
-> Processing apw_eng_200301.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030117_0737_18:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030117_0701_17:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030117_0695_17:4 discarded.
-> Processing apw_eng_200805.json...
-> Processing apw_eng_201011.json...
-> Processing apw_eng_199709.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970927_0849_13:28 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970913_0778_15:32 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970913_0763_15:32 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970913_0760_15:32 discarded.
-> Processing apw_eng_201008.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100806_0201_9:5 discarded.
-> Processing apw_eng_200109.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010926_0344_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010923_0481_8:6 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010903_1389_46:9 discarded.
-> Processing apw_eng_199703.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970322_0584_13:6 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970316_1018_17:17 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970304_0863_4:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970304_0533_4:5 discarded.
-> Processing apw_eng_199808.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980808_0691_14:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980808_0629_3:8 discarded.
-> Processing apw_eng_199612.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19961221_0812_1:7 discarded.
-> Processing apw_eng_200203.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020303_0636_6:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020301_0675_18:4 discarded.
-> Processing apw_eng_200311.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20031107_0527_11:5 discarded.
-> Processing apw_eng_200807.json...
-> Processing apw_eng_200607.json...
-> Processing apw_eng_200305.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030519_0031_47:24 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030518_0484_46:24 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030508_0007_27:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030508_0005_27:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030507_0459_10:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030507_0404_11:7 discarded.
-> Processing apw_eng_200506.json...
-> Processing apw_eng_201003.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100310_0423_34:31 discarded.
-> Processing apw_eng_199906.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990630_0028_3:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990613_0575_4:8 discarded.
-> Processing apw_eng_200511.json...
-> Processing apw_eng_199804.json...
-> Processing apw_eng_199504.json...
-> Processing apw_eng_200106.json...
-> Processing apw_eng_199412.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19941220_0030_4:8 discarded.
-> Processing apw_eng_200102.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010211_0501_3:7 discarded.
-> Processing apw_eng_200801.json...
-> Processing apw_eng_200703.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   Same sentence, but different adverb tokens.
  + Hit apw_eng_20070316_0412_19:22 recorded as is.
-> Processing apw_eng_200806.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080606_1363_5:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080606_1335_5:10 discarded.
-> Processing apw_eng_199511.json...
-> Processing apw_eng_200709.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070904_1507_3:5 discarded.
-> Processing apw_eng_200605.json...
-> Processing apw_eng_199610.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19961002_0472_17:9 discarded.
-> Processing apw_eng_199601.json...
-> Processing apw_eng_200309.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030917_0656_1:12 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030906_0020_4:5 discarded.
-> Processing apw_eng_200610.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20061029_0502_9:8 discarded.
-> Processing apw_eng_200205.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020530_0047_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020516_1050_24:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020516_0722_19:8 discarded.
-> Processing apw_eng_200712.json...
-> Processing apw_eng_200901.json...
-> Processing apw_eng_199811.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981127_0222_8:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981117_0578_7:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981111_0329_17:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981111_0280_15:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981110_1359_4:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981101_0524_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981101_0400_5:5 discarded.
-> Processing apw_eng_200005.json...
-> Processing apw_eng_200604.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20060420_0019_11:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20060402_0727_4:28 discarded.
-> Processing apw_eng_200504.json...
-> Processing apw_eng_200401.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040108_0060_8:8 discarded.
-> Processing apw_eng_199503.json...
-> Processing apw_eng_200503.json...
-> Processing apw_eng_200211.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021124_0276_8:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021124_0270_4:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021120_0607_6:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021120_0187_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021117_0008_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021114_0051_8:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021103_0193_9:5 discarded.
-> Processing apw_eng_199609.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960905_1034_4:7 discarded.
-> Processing apw_eng_200412.json...
-> Processing apw_eng_199701.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970129_0750_12:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970129_0697_12:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970129_0628_12:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970122_1384_20:7 discarded.
-> Processing apw_eng_200509.json...
-> Processing apw_eng_200803.json...
-> Processing apw_eng_199507.json...
-> Processing apw_eng_200408.json...
-> Processing apw_eng_199606.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960605_0458_3:4 discarded.
-> Processing apw_eng_200210.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0716_2:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0683_3:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0646_6:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0631_13:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0623_13:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0600_12:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0597_12:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0509_12:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0498_14:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0339_23:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0240_24:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0210_19:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0202_19:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021018_0185_19:8 discarded.
-> Processing apw_eng_200108.json...
-> Processing apw_eng_201004.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100410_0040_34:4 discarded.
-> Processing apw_eng_200009.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20000917_0095_8:5 discarded.
-> Processing apw_eng_200101.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010119_0834_18:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010119_0430_18:8 discarded.
-> Processing apw_eng_200810.json...
-> Processing apw_eng_200411.json...
-> Processing apw_eng_200206.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020627_0230_4:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020616_0044_9:5 discarded.
-> Processing apw_eng_200708.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070830_1020_53:9 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070817_1388_9:38 discarded.
-> Processing apw_eng_200910.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20091006_0496_3:5 discarded.
-> Processing apw_eng_199607.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960725_0821_19:12 discarded.
-> Processing apw_eng_200008.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20000826_0166_10:5 discarded.
-> Processing apw_eng_200011.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20001120_0492_6:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20001119_0631_5:5 discarded.
-> Processing apw_eng_200510.json...
-> Processing apw_eng_200704.json...
-> Processing apw_eng_200809.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080925_1345_9:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080925_1310_4:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080911_0884_12:11 discarded.
-> Processing apw_eng_201010.json...
-> Processing apw_eng_200907.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090715_0218_2:4 discarded.
-> Processing apw_eng_199809.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980925_0328_6:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980911_0142_4:5 discarded.
-> Processing apw_eng_199708.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970818_0270_3:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970818_0187_3:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970814_0873_31:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970814_0859_31:7 discarded.
-> Processing apw_eng_200501.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20050106_0380_4:7 discarded.
-> Processing apw_eng_200207.json...
-> Processing apw_eng_199805.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980523_0552_8:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980513_0395_6:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980513_0347_6:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980513_0266_3:5 discarded.
-> Processing apw_eng_199510.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19951023_0047_21:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19951022_1126_15:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19951022_0172_2:13 discarded.
-> Processing apw_eng_199608.json...
-> Processing apw_eng_200007.json...
-> Processing apw_eng_199801.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980117_0159_5:25 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980117_0044_5:25 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980117_0040_5:25 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980116_0246_10:20 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980110_0493_4:5 discarded.
-> Processing apw_eng_199707.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970718_0418_1:4 discarded.
-> Processing apw_eng_199711.json...
-> Processing apw_eng_200208.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020807_0666_28:31 discarded.
-> Processing apw_eng_200307.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030726_0056_14:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030725_0730_7:8 discarded.
-> Processing apw_eng_200404.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040418_0432_19:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040418_0427_19:7 discarded.
-> Processing apw_eng_199802.json...
-> Processing apw_eng_200303.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030304_0241_4:5 discarded.
-> Processing apw_eng_200310.json...
-> Processing apw_eng_200702.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070203_0893_24:8 discarded.
-> Processing apw_eng_199806.json...
-> Processing apw_eng_200701.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070128_0779_27:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070128_0716_27:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070128_0572_22:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070101_0702_19:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070101_0698_17:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070101_0581_9:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070101_0543_9:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070101_0505_9:13 discarded.
-> Processing apw_eng_201001.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100129_1081_12:12 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100129_1050_12:12 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100129_0745_7:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100129_0730_7:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100105_0927_24:35 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100105_0662_24:35 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100105_0661_24:35 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100105_0626_15:23 discarded.
-> Processing apw_eng_200811.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20081129_0748_20:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20081129_0705_20:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20081117_0142_14:9 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20081117_0083_14:9 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20081117_0063_12:9 discarded.
-> Processing apw_eng_199909.json...
-> Processing apw_eng_200112.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20011214_0149_2:11 discarded.
-> Processing apw_eng_200105.json...
-> Processing apw_eng_199807.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980716_0496_3:4 discarded.
-> Processing apw_eng_201006.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100630_0036_4:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100629_0958_4:5 discarded.
-> Processing apw_eng_199907.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990704_0935_40:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990704_0683_38:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990704_0548_35:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990704_0411_12:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990704_0336_8:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990703_0961_20:9 discarded.
-> Processing apw_eng_199602.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0858_41:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0789_42:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0640_39:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0577_40:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0515_44:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0468_38:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0424_33:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0360_25:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0252_17:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960207_0227_12:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960201_0251_24:15 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19960201_0205_24:15 discarded.
-> Processing apw_eng_200705.json...
-> Processing apw_eng_200710.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20071016_1193_26:7 discarded.
-> Processing apw_eng_199902.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990221_0209_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990219_0846_2:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990214_0075_4:5 discarded.
-> Processing apw_eng_199604.json...
-> Processing apw_eng_200308.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030803_0189_15:7 discarded.
-> Processing apw_eng_200611.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20061126_0349_10:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20061126_0301_3:4 discarded.
-> Processing apw_eng_200808.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080829_0030_33:15 discarded.
-> Processing apw_eng_200407.json...
-> Processing apw_eng_200110.json...
-> Processing apw_eng_199710.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19971014_1337_4:4 discarded.
-> Processing apw_eng_201002.json...
-> Processing apw_eng_200612.json...
-> Processing apw_eng_200902.json...
-> Processing apw_eng_200212.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021226_0077_5:5 discarded.
-> Processing apw_eng_200312.json...
-> Processing apw_eng_200010.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20001025_0486_12:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20001024_0623_4:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20001019_0197_10:24 discarded.
-> Processing apw_eng_199605.json...
-> Processing apw_eng_200706.json...
-> Processing apw_eng_201005.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100512_0953_13:22 discarded.
-> Processing apw_eng_200908.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090831_0737_20:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090831_0626_16:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090831_0617_14:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090831_0417_12:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090802_0498_33:5 discarded.
-> Processing apw_eng_200603.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20060314_0253_6:5 discarded.
-> Processing apw_eng_200304.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030416_0277_2:8 discarded.
-> Processing apw_eng_199702.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970221_1234_4:17 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970202_0847_13:8 discarded.
-> Processing apw_eng_199501.json...
-> Processing apw_eng_200012.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20001219_0422_7:5 discarded.
-> Processing apw_eng_200508.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20050821_0021_21:4 discarded.
-> Processing apw_eng_199803.json...
-> Processing apw_eng_200204.json...
-> Processing apw_eng_199904.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990430_1058_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990426_1067_8:22 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990426_1057_8:22 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990426_1044_7:22 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990426_1027_7:22 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990426_1016_5:22 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990426_1006_5:22 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990408_1152_5:5 discarded.
-> Processing apw_eng_200302.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030221_0092_4:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030221_0082_4:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20030221_0054_4:8 discarded.
-> Processing apw_eng_199508.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950814_0804_6:4 discarded.
-> Processing apw_eng_200602.json...
-> Processing apw_eng_200911.json...
-> Processing apw_eng_199908.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990806_1019_6:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990806_0135_8:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990806_0120_8:7 discarded.
-> Processing apw_eng_200905.json...
-> Processing apw_eng_200202.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020225_0296_5:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020209_0575_26:11 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020209_0529_24:11 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020209_0441_19:11 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020209_0241_18:11 discarded.
-> Processing apw_eng_199905.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990504_1343_6:9 discarded.
-> Processing apw_eng_200707.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070703_1217_8:19 discarded.
-> Processing apw_eng_200001.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20000131_0199_20:26 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20000129_0060_9:26 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20000128_0204_8:26 discarded.
-> Processing apw_eng_200606.json...
-> Processing apw_eng_200711.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20071120_1110_24:17 discarded.
-> Processing apw_eng_199505.json...
-> Processing apw_eng_200802.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080222_0584_28:30 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080214_1784_7:7 discarded.
-> Processing apw_eng_199506.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950604_0325_14:27 discarded.
-> Processing apw_eng_199903.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990327_0953_4:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990326_1010_10:13 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990312_1048_19:6 discarded.
-> Processing apw_eng_200505.json...
-> Processing apw_eng_200512.json...
-> Processing apw_eng_200209.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020907_0227_7:7 discarded.
-> Processing apw_eng_200608.json...
-> Processing apw_eng_200909.json...
-> Processing apw_eng_199810.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981031_0489_5:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19981007_0238_4:5 discarded.
-> Processing apw_eng_199603.json...
-> Processing apw_eng_199502.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0322_24:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0214_11:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0207_11:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0106_10:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0100_9:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0037_10:8 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950209_0020_9:8 discarded.
-> Processing apw_eng_199712.json...
-> Processing apw_eng_199812.json...
-> Processing apw_eng_200201.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020128_1725_2:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020128_1720_2:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020128_0022_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020127_1158_5:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020105_0487_5:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020105_0476_4:4 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20020105_0436_3:4 discarded.
-> Processing apw_eng_200403.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040316_0762_18:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040316_0623_17:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040316_0593_15:7 discarded.
-> Processing apw_eng_199901.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990111_0790_6:5 discarded.
-> Processing apw_eng_199706.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19970625_1297_7:15 discarded.

^_^ Finished collecting sentence data from all json files.
    -> Writing tables to csv files...
```
```

Time elapsed: 0.077 seconds
====================================

```  
## Starting context: `few_subj`
- time stamp: `Thu Aug  5 16:12:46 EDT 2021`
- data directory: `data/neg-mit/Apw.few_subj`
- hits table: `hits/neg-mit/Apw_few_subj`
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
 WARNING : [Conll, File Apw.conll/apw_eng_199608.conllu] No blank line at the end of the file
```
### Running grew search on `Apw.conll`...
```
193 total file(s) to be searched.
-> searching Apw.conll/apw_eng_199411.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199411.conllu > data/neg-mit/Apw.few_subj/apw_eng_199411.raw.json
1.59 minutes on apw_eng_199411.conllu
-> searching Apw.conll/apw_eng_199412.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199412.conllu > data/neg-mit/Apw.few_subj/apw_eng_199412.raw.json
2.34 minutes on apw_eng_199412.conllu
-> searching Apw.conll/apw_eng_199501.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199501.conllu > data/neg-mit/Apw.few_subj/apw_eng_199501.raw.json
2.41 minutes on apw_eng_199501.conllu
-> searching Apw.conll/apw_eng_199502.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199502.conllu > data/neg-mit/Apw.few_subj/apw_eng_199502.raw.json
2.08 minutes on apw_eng_199502.conllu
-> searching Apw.conll/apw_eng_199503.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199503.conllu > data/neg-mit/Apw.few_subj/apw_eng_199503.raw.json
2.49 minutes on apw_eng_199503.conllu
-> searching Apw.conll/apw_eng_199504.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199504.conllu > data/neg-mit/Apw.few_subj/apw_eng_199504.raw.json
2.4 minutes on apw_eng_199504.conllu
-> searching Apw.conll/apw_eng_199505.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199505.conllu > data/neg-mit/Apw.few_subj/apw_eng_199505.raw.json
3.0 minutes on apw_eng_199505.conllu
-> searching Apw.conll/apw_eng_199506.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199506.conllu > data/neg-mit/Apw.few_subj/apw_eng_199506.raw.json
3.23 minutes on apw_eng_199506.conllu
-> searching Apw.conll/apw_eng_199507.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199507.conllu > data/neg-mit/Apw.few_subj/apw_eng_199507.raw.json
2.98 minutes on apw_eng_199507.conllu
-> searching Apw.conll/apw_eng_199508.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199508.conllu > data/neg-mit/Apw.few_subj/apw_eng_199508.raw.json
2.97 minutes on apw_eng_199508.conllu
-> searching Apw.conll/apw_eng_199509.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199509.conllu > data/neg-mit/Apw.few_subj/apw_eng_199509.raw.json
2.86 minutes on apw_eng_199509.conllu
-> searching Apw.conll/apw_eng_199510.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199510.conllu > data/neg-mit/Apw.few_subj/apw_eng_199510.raw.json
2.03 minutes on apw_eng_199510.conllu
-> searching Apw.conll/apw_eng_199511.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199511.conllu > data/neg-mit/Apw.few_subj/apw_eng_199511.raw.json
1.98 minutes on apw_eng_199511.conllu
-> searching Apw.conll/apw_eng_199512.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199512.conllu > data/neg-mit/Apw.few_subj/apw_eng_199512.raw.json
1.89 minutes on apw_eng_199512.conllu
-> searching Apw.conll/apw_eng_199601.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199601.conllu > data/neg-mit/Apw.few_subj/apw_eng_199601.raw.json
2.0 minutes on apw_eng_199601.conllu
-> searching Apw.conll/apw_eng_199602.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199602.conllu > data/neg-mit/Apw.few_subj/apw_eng_199602.raw.json
1.84 minutes on apw_eng_199602.conllu
-> searching Apw.conll/apw_eng_199603.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199603.conllu > data/neg-mit/Apw.few_subj/apw_eng_199603.raw.json
2.12 minutes on apw_eng_199603.conllu
-> searching Apw.conll/apw_eng_199604.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199604.conllu > data/neg-mit/Apw.few_subj/apw_eng_199604.raw.json
2.05 minutes on apw_eng_199604.conllu
-> searching Apw.conll/apw_eng_199605.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199605.conllu > data/neg-mit/Apw.few_subj/apw_eng_199605.raw.json
2.06 minutes on apw_eng_199605.conllu
-> searching Apw.conll/apw_eng_199606.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199606.conllu > data/neg-mit/Apw.few_subj/apw_eng_199606.raw.json
1.77 minutes on apw_eng_199606.conllu
-> searching Apw.conll/apw_eng_199607.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199607.conllu > data/neg-mit/Apw.few_subj/apw_eng_199607.raw.json
1.89 minutes on apw_eng_199607.conllu
-> searching Apw.conll/apw_eng_199608.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199608.conllu > data/neg-mit/Apw.few_subj/apw_eng_199608.raw.json
1.54 minutes on apw_eng_199608.conllu
-> searching Apw.conll/apw_eng_199609.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199609.conllu > data/neg-mit/Apw.few_subj/apw_eng_199609.raw.json
1.77 minutes on apw_eng_199609.conllu
-> searching Apw.conll/apw_eng_199610.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199610.conllu > data/neg-mit/Apw.few_subj/apw_eng_199610.raw.json
1.9 minutes on apw_eng_199610.conllu
-> searching Apw.conll/apw_eng_199611.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199611.conllu > data/neg-mit/Apw.few_subj/apw_eng_199611.raw.json
1.89 minutes on apw_eng_199611.conllu
-> searching Apw.conll/apw_eng_199612.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199612.conllu > data/neg-mit/Apw.few_subj/apw_eng_199612.raw.json
1.96 minutes on apw_eng_199612.conllu
-> searching Apw.conll/apw_eng_199701.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199701.conllu > data/neg-mit/Apw.few_subj/apw_eng_199701.raw.json
2.13 minutes on apw_eng_199701.conllu
-> searching Apw.conll/apw_eng_199702.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199702.conllu > data/neg-mit/Apw.few_subj/apw_eng_199702.raw.json
1.96 minutes on apw_eng_199702.conllu
-> searching Apw.conll/apw_eng_199703.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199703.conllu > data/neg-mit/Apw.few_subj/apw_eng_199703.raw.json
2.26 minutes on apw_eng_199703.conllu
-> searching Apw.conll/apw_eng_199704.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199704.conllu > data/neg-mit/Apw.few_subj/apw_eng_199704.raw.json
2.18 minutes on apw_eng_199704.conllu
-> searching Apw.conll/apw_eng_199705.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199705.conllu > data/neg-mit/Apw.few_subj/apw_eng_199705.raw.json
2.25 minutes on apw_eng_199705.conllu
-> searching Apw.conll/apw_eng_199706.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199706.conllu > data/neg-mit/Apw.few_subj/apw_eng_199706.raw.json
2.22 minutes on apw_eng_199706.conllu
-> searching Apw.conll/apw_eng_199707.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199707.conllu > data/neg-mit/Apw.few_subj/apw_eng_199707.raw.json
2.34 minutes on apw_eng_199707.conllu
-> searching Apw.conll/apw_eng_199708.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199708.conllu > data/neg-mit/Apw.few_subj/apw_eng_199708.raw.json
2.23 minutes on apw_eng_199708.conllu
-> searching Apw.conll/apw_eng_199709.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199709.conllu > data/neg-mit/Apw.few_subj/apw_eng_199709.raw.json
2.35 minutes on apw_eng_199709.conllu
-> searching Apw.conll/apw_eng_199710.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199710.conllu > data/neg-mit/Apw.few_subj/apw_eng_199710.raw.json
2.29 minutes on apw_eng_199710.conllu
-> searching Apw.conll/apw_eng_199711.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199711.conllu > data/neg-mit/Apw.few_subj/apw_eng_199711.raw.json
2.8 minutes on apw_eng_199711.conllu
-> searching Apw.conll/apw_eng_199712.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199712.conllu > data/neg-mit/Apw.few_subj/apw_eng_199712.raw.json
3.56 minutes on apw_eng_199712.conllu
-> searching Apw.conll/apw_eng_199801.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199801.conllu > data/neg-mit/Apw.few_subj/apw_eng_199801.raw.json
3.73 minutes on apw_eng_199801.conllu
-> searching Apw.conll/apw_eng_199802.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199802.conllu > data/neg-mit/Apw.few_subj/apw_eng_199802.raw.json
3.84 minutes on apw_eng_199802.conllu
-> searching Apw.conll/apw_eng_199803.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199803.conllu > data/neg-mit/Apw.few_subj/apw_eng_199803.raw.json
4.06 minutes on apw_eng_199803.conllu
-> searching Apw.conll/apw_eng_199804.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199804.conllu > data/neg-mit/Apw.few_subj/apw_eng_199804.raw.json
3.83 minutes on apw_eng_199804.conllu
-> searching Apw.conll/apw_eng_199805.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199805.conllu > data/neg-mit/Apw.few_subj/apw_eng_199805.raw.json
3.81 minutes on apw_eng_199805.conllu
-> searching Apw.conll/apw_eng_199806.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199806.conllu > data/neg-mit/Apw.few_subj/apw_eng_199806.raw.json
3.55 minutes on apw_eng_199806.conllu
-> searching Apw.conll/apw_eng_199807.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199807.conllu > data/neg-mit/Apw.few_subj/apw_eng_199807.raw.json
2.32 minutes on apw_eng_199807.conllu
-> searching Apw.conll/apw_eng_199808.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199808.conllu > data/neg-mit/Apw.few_subj/apw_eng_199808.raw.json
2.23 minutes on apw_eng_199808.conllu
-> searching Apw.conll/apw_eng_199809.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199809.conllu > data/neg-mit/Apw.few_subj/apw_eng_199809.raw.json
2.39 minutes on apw_eng_199809.conllu
-> searching Apw.conll/apw_eng_199810.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199810.conllu > data/neg-mit/Apw.few_subj/apw_eng_199810.raw.json
2.41 minutes on apw_eng_199810.conllu
-> searching Apw.conll/apw_eng_199811.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199811.conllu > data/neg-mit/Apw.few_subj/apw_eng_199811.raw.json
2.31 minutes on apw_eng_199811.conllu
-> searching Apw.conll/apw_eng_199812.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199812.conllu > data/neg-mit/Apw.few_subj/apw_eng_199812.raw.json
2.8 minutes on apw_eng_199812.conllu
-> searching Apw.conll/apw_eng_199901.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199901.conllu > data/neg-mit/Apw.few_subj/apw_eng_199901.raw.json
2.59 minutes on apw_eng_199901.conllu
-> searching Apw.conll/apw_eng_199902.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199902.conllu > data/neg-mit/Apw.few_subj/apw_eng_199902.raw.json
2.39 minutes on apw_eng_199902.conllu
-> searching Apw.conll/apw_eng_199903.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199903.conllu > data/neg-mit/Apw.few_subj/apw_eng_199903.raw.json
2.96 minutes on apw_eng_199903.conllu
-> searching Apw.conll/apw_eng_199904.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199904.conllu > data/neg-mit/Apw.few_subj/apw_eng_199904.raw.json
2.69 minutes on apw_eng_199904.conllu
-> searching Apw.conll/apw_eng_199905.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199905.conllu > data/neg-mit/Apw.few_subj/apw_eng_199905.raw.json
2.87 minutes on apw_eng_199905.conllu
-> searching Apw.conll/apw_eng_199906.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199906.conllu > data/neg-mit/Apw.few_subj/apw_eng_199906.raw.json
2.93 minutes on apw_eng_199906.conllu
-> searching Apw.conll/apw_eng_199907.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199907.conllu > data/neg-mit/Apw.few_subj/apw_eng_199907.raw.json
2.71 minutes on apw_eng_199907.conllu
-> searching Apw.conll/apw_eng_199908.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199908.conllu > data/neg-mit/Apw.few_subj/apw_eng_199908.raw.json
1.82 minutes on apw_eng_199908.conllu
-> searching Apw.conll/apw_eng_199909.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199909.conllu > data/neg-mit/Apw.few_subj/apw_eng_199909.raw.json
1.51 minutes on apw_eng_199909.conllu
-> searching Apw.conll/apw_eng_199910.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199910.conllu > data/neg-mit/Apw.few_subj/apw_eng_199910.raw.json
1.79 minutes on apw_eng_199910.conllu
-> searching Apw.conll/apw_eng_199911.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_199911.conllu > data/neg-mit/Apw.few_subj/apw_eng_199911.raw.json
0.01 minutes on apw_eng_199911.conllu
-> searching Apw.conll/apw_eng_200001.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200001.conllu > data/neg-mit/Apw.few_subj/apw_eng_200001.raw.json
1.79 minutes on apw_eng_200001.conllu
-> searching Apw.conll/apw_eng_200002.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200002.conllu > data/neg-mit/Apw.few_subj/apw_eng_200002.raw.json
1.62 minutes on apw_eng_200002.conllu
-> searching Apw.conll/apw_eng_200003.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200003.conllu > data/neg-mit/Apw.few_subj/apw_eng_200003.raw.json
1.34 minutes on apw_eng_200003.conllu
-> searching Apw.conll/apw_eng_200004.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200004.conllu > data/neg-mit/Apw.few_subj/apw_eng_200004.raw.json
1.15 minutes on apw_eng_200004.conllu
-> searching Apw.conll/apw_eng_200005.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200005.conllu > data/neg-mit/Apw.few_subj/apw_eng_200005.raw.json
1.28 minutes on apw_eng_200005.conllu
-> searching Apw.conll/apw_eng_200006.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200006.conllu > data/neg-mit/Apw.few_subj/apw_eng_200006.raw.json
1.11 minutes on apw_eng_200006.conllu
-> searching Apw.conll/apw_eng_200007.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200007.conllu > data/neg-mit/Apw.few_subj/apw_eng_200007.raw.json
1.11 minutes on apw_eng_200007.conllu
-> searching Apw.conll/apw_eng_200008.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200008.conllu > data/neg-mit/Apw.few_subj/apw_eng_200008.raw.json
1.04 minutes on apw_eng_200008.conllu
-> searching Apw.conll/apw_eng_200009.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200009.conllu > data/neg-mit/Apw.few_subj/apw_eng_200009.raw.json
1.11 minutes on apw_eng_200009.conllu
-> searching Apw.conll/apw_eng_200010.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200010.conllu > data/neg-mit/Apw.few_subj/apw_eng_200010.raw.json
4.54 minutes on apw_eng_200010.conllu
-> searching Apw.conll/apw_eng_200011.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200011.conllu > data/neg-mit/Apw.few_subj/apw_eng_200011.raw.json
4.83 minutes on apw_eng_200011.conllu
-> searching Apw.conll/apw_eng_200012.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200012.conllu > data/neg-mit/Apw.few_subj/apw_eng_200012.raw.json
4.61 minutes on apw_eng_200012.conllu
-> searching Apw.conll/apw_eng_200101.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200101.conllu > data/neg-mit/Apw.few_subj/apw_eng_200101.raw.json
4.75 minutes on apw_eng_200101.conllu
-> searching Apw.conll/apw_eng_200102.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200102.conllu > data/neg-mit/Apw.few_subj/apw_eng_200102.raw.json
4.15 minutes on apw_eng_200102.conllu
-> searching Apw.conll/apw_eng_200103.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200103.conllu > data/neg-mit/Apw.few_subj/apw_eng_200103.raw.json
4.98 minutes on apw_eng_200103.conllu
-> searching Apw.conll/apw_eng_200104.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200104.conllu > data/neg-mit/Apw.few_subj/apw_eng_200104.raw.json
4.63 minutes on apw_eng_200104.conllu
-> searching Apw.conll/apw_eng_200105.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200105.conllu > data/neg-mit/Apw.few_subj/apw_eng_200105.raw.json
4.93 minutes on apw_eng_200105.conllu
-> searching Apw.conll/apw_eng_200106.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200106.conllu > data/neg-mit/Apw.few_subj/apw_eng_200106.raw.json
5.03 minutes on apw_eng_200106.conllu
-> searching Apw.conll/apw_eng_200107.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200107.conllu > data/neg-mit/Apw.few_subj/apw_eng_200107.raw.json
4.79 minutes on apw_eng_200107.conllu
-> searching Apw.conll/apw_eng_200108.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200108.conllu > data/neg-mit/Apw.few_subj/apw_eng_200108.raw.json
2.66 minutes on apw_eng_200108.conllu
-> searching Apw.conll/apw_eng_200109.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200109.conllu > data/neg-mit/Apw.few_subj/apw_eng_200109.raw.json
3.75 minutes on apw_eng_200109.conllu
-> searching Apw.conll/apw_eng_200110.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200110.conllu > data/neg-mit/Apw.few_subj/apw_eng_200110.raw.json
3.71 minutes on apw_eng_200110.conllu
-> searching Apw.conll/apw_eng_200111.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200111.conllu > data/neg-mit/Apw.few_subj/apw_eng_200111.raw.json
3.34 minutes on apw_eng_200111.conllu
-> searching Apw.conll/apw_eng_200112.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200112.conllu > data/neg-mit/Apw.few_subj/apw_eng_200112.raw.json
3.09 minutes on apw_eng_200112.conllu
-> searching Apw.conll/apw_eng_200201.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200201.conllu > data/neg-mit/Apw.few_subj/apw_eng_200201.raw.json
3.52 minutes on apw_eng_200201.conllu
-> searching Apw.conll/apw_eng_200202.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200202.conllu > data/neg-mit/Apw.few_subj/apw_eng_200202.raw.json
3.52 minutes on apw_eng_200202.conllu
-> searching Apw.conll/apw_eng_200203.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200203.conllu > data/neg-mit/Apw.few_subj/apw_eng_200203.raw.json
3.79 minutes on apw_eng_200203.conllu
-> searching Apw.conll/apw_eng_200204.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200204.conllu > data/neg-mit/Apw.few_subj/apw_eng_200204.raw.json
3.87 minutes on apw_eng_200204.conllu
-> searching Apw.conll/apw_eng_200205.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200205.conllu > data/neg-mit/Apw.few_subj/apw_eng_200205.raw.json
3.81 minutes on apw_eng_200205.conllu
-> searching Apw.conll/apw_eng_200206.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200206.conllu > data/neg-mit/Apw.few_subj/apw_eng_200206.raw.json
3.79 minutes on apw_eng_200206.conllu
-> searching Apw.conll/apw_eng_200207.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200207.conllu > data/neg-mit/Apw.few_subj/apw_eng_200207.raw.json
3.82 minutes on apw_eng_200207.conllu
-> searching Apw.conll/apw_eng_200208.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200208.conllu > data/neg-mit/Apw.few_subj/apw_eng_200208.raw.json
3.44 minutes on apw_eng_200208.conllu
-> searching Apw.conll/apw_eng_200209.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200209.conllu > data/neg-mit/Apw.few_subj/apw_eng_200209.raw.json
3.69 minutes on apw_eng_200209.conllu
-> searching Apw.conll/apw_eng_200210.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200210.conllu > data/neg-mit/Apw.few_subj/apw_eng_200210.raw.json
4.21 minutes on apw_eng_200210.conllu
-> searching Apw.conll/apw_eng_200211.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200211.conllu > data/neg-mit/Apw.few_subj/apw_eng_200211.raw.json
3.72 minutes on apw_eng_200211.conllu
-> searching Apw.conll/apw_eng_200212.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200212.conllu > data/neg-mit/Apw.few_subj/apw_eng_200212.raw.json
2.79 minutes on apw_eng_200212.conllu
-> searching Apw.conll/apw_eng_200301.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200301.conllu > data/neg-mit/Apw.few_subj/apw_eng_200301.raw.json
4.0 minutes on apw_eng_200301.conllu
-> searching Apw.conll/apw_eng_200302.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200302.conllu > data/neg-mit/Apw.few_subj/apw_eng_200302.raw.json
3.99 minutes on apw_eng_200302.conllu
-> searching Apw.conll/apw_eng_200303.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200303.conllu > data/neg-mit/Apw.few_subj/apw_eng_200303.raw.json
4.58 minutes on apw_eng_200303.conllu
-> searching Apw.conll/apw_eng_200304.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200304.conllu > data/neg-mit/Apw.few_subj/apw_eng_200304.raw.json
4.13 minutes on apw_eng_200304.conllu
-> searching Apw.conll/apw_eng_200305.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200305.conllu > data/neg-mit/Apw.few_subj/apw_eng_200305.raw.json
4.0 minutes on apw_eng_200305.conllu
-> searching Apw.conll/apw_eng_200306.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200306.conllu > data/neg-mit/Apw.few_subj/apw_eng_200306.raw.json
3.22 minutes on apw_eng_200306.conllu
-> searching Apw.conll/apw_eng_200307.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200307.conllu > data/neg-mit/Apw.few_subj/apw_eng_200307.raw.json
1.36 minutes on apw_eng_200307.conllu
-> searching Apw.conll/apw_eng_200308.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200308.conllu > data/neg-mit/Apw.few_subj/apw_eng_200308.raw.json
3.7 minutes on apw_eng_200308.conllu
-> searching Apw.conll/apw_eng_200309.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200309.conllu > data/neg-mit/Apw.few_subj/apw_eng_200309.raw.json
4.14 minutes on apw_eng_200309.conllu
-> searching Apw.conll/apw_eng_200310.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200310.conllu > data/neg-mit/Apw.few_subj/apw_eng_200310.raw.json
4.92 minutes on apw_eng_200310.conllu
-> searching Apw.conll/apw_eng_200311.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200311.conllu > data/neg-mit/Apw.few_subj/apw_eng_200311.raw.json
4.28 minutes on apw_eng_200311.conllu
-> searching Apw.conll/apw_eng_200312.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200312.conllu > data/neg-mit/Apw.few_subj/apw_eng_200312.raw.json
3.95 minutes on apw_eng_200312.conllu
-> searching Apw.conll/apw_eng_200401.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200401.conllu > data/neg-mit/Apw.few_subj/apw_eng_200401.raw.json
2.3 minutes on apw_eng_200401.conllu
-> searching Apw.conll/apw_eng_200402.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200402.conllu > data/neg-mit/Apw.few_subj/apw_eng_200402.raw.json
3.11 minutes on apw_eng_200402.conllu
-> searching Apw.conll/apw_eng_200403.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200403.conllu > data/neg-mit/Apw.few_subj/apw_eng_200403.raw.json
5.08 minutes on apw_eng_200403.conllu
-> searching Apw.conll/apw_eng_200404.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200404.conllu > data/neg-mit/Apw.few_subj/apw_eng_200404.raw.json
4.48 minutes on apw_eng_200404.conllu
-> searching Apw.conll/apw_eng_200405.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200405.conllu > data/neg-mit/Apw.few_subj/apw_eng_200405.raw.json
0.89 minutes on apw_eng_200405.conllu
-> searching Apw.conll/apw_eng_200406.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200406.conllu > data/neg-mit/Apw.few_subj/apw_eng_200406.raw.json
0.82 minutes on apw_eng_200406.conllu
-> searching Apw.conll/apw_eng_200407.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200407.conllu > data/neg-mit/Apw.few_subj/apw_eng_200407.raw.json
2.01 minutes on apw_eng_200407.conllu
-> searching Apw.conll/apw_eng_200408.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200408.conllu > data/neg-mit/Apw.few_subj/apw_eng_200408.raw.json
1.76 minutes on apw_eng_200408.conllu
-> searching Apw.conll/apw_eng_200409.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200409.conllu > data/neg-mit/Apw.few_subj/apw_eng_200409.raw.json
1.89 minutes on apw_eng_200409.conllu
-> searching Apw.conll/apw_eng_200410.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200410.conllu > data/neg-mit/Apw.few_subj/apw_eng_200410.raw.json
2.14 minutes on apw_eng_200410.conllu
-> searching Apw.conll/apw_eng_200411.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200411.conllu > data/neg-mit/Apw.few_subj/apw_eng_200411.raw.json
1.58 minutes on apw_eng_200411.conllu
-> searching Apw.conll/apw_eng_200412.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200412.conllu > data/neg-mit/Apw.few_subj/apw_eng_200412.raw.json
0.58 minutes on apw_eng_200412.conllu
-> searching Apw.conll/apw_eng_200501.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200501.conllu > data/neg-mit/Apw.few_subj/apw_eng_200501.raw.json
1.59 minutes on apw_eng_200501.conllu
-> searching Apw.conll/apw_eng_200502.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200502.conllu > data/neg-mit/Apw.few_subj/apw_eng_200502.raw.json
1.4 minutes on apw_eng_200502.conllu
-> searching Apw.conll/apw_eng_200503.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200503.conllu > data/neg-mit/Apw.few_subj/apw_eng_200503.raw.json
2.1 minutes on apw_eng_200503.conllu
-> searching Apw.conll/apw_eng_200504.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200504.conllu > data/neg-mit/Apw.few_subj/apw_eng_200504.raw.json
1.54 minutes on apw_eng_200504.conllu
-> searching Apw.conll/apw_eng_200505.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200505.conllu > data/neg-mit/Apw.few_subj/apw_eng_200505.raw.json
2.01 minutes on apw_eng_200505.conllu
-> searching Apw.conll/apw_eng_200506.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200506.conllu > data/neg-mit/Apw.few_subj/apw_eng_200506.raw.json
2.13 minutes on apw_eng_200506.conllu
-> searching Apw.conll/apw_eng_200507.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200507.conllu > data/neg-mit/Apw.few_subj/apw_eng_200507.raw.json
1.44 minutes on apw_eng_200507.conllu
-> searching Apw.conll/apw_eng_200508.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200508.conllu > data/neg-mit/Apw.few_subj/apw_eng_200508.raw.json
1.89 minutes on apw_eng_200508.conllu
-> searching Apw.conll/apw_eng_200509.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200509.conllu > data/neg-mit/Apw.few_subj/apw_eng_200509.raw.json
2.31 minutes on apw_eng_200509.conllu
-> searching Apw.conll/apw_eng_200510.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200510.conllu > data/neg-mit/Apw.few_subj/apw_eng_200510.raw.json
2.14 minutes on apw_eng_200510.conllu
-> searching Apw.conll/apw_eng_200511.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200511.conllu > data/neg-mit/Apw.few_subj/apw_eng_200511.raw.json
2.12 minutes on apw_eng_200511.conllu
-> searching Apw.conll/apw_eng_200512.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200512.conllu > data/neg-mit/Apw.few_subj/apw_eng_200512.raw.json
2.15 minutes on apw_eng_200512.conllu
-> searching Apw.conll/apw_eng_200601.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200601.conllu > data/neg-mit/Apw.few_subj/apw_eng_200601.raw.json
2.24 minutes on apw_eng_200601.conllu
-> searching Apw.conll/apw_eng_200602.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200602.conllu > data/neg-mit/Apw.few_subj/apw_eng_200602.raw.json
1.78 minutes on apw_eng_200602.conllu
-> searching Apw.conll/apw_eng_200603.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200603.conllu > data/neg-mit/Apw.few_subj/apw_eng_200603.raw.json
2.4 minutes on apw_eng_200603.conllu
-> searching Apw.conll/apw_eng_200604.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200604.conllu > data/neg-mit/Apw.few_subj/apw_eng_200604.raw.json
1.87 minutes on apw_eng_200604.conllu
-> searching Apw.conll/apw_eng_200605.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200605.conllu > data/neg-mit/Apw.few_subj/apw_eng_200605.raw.json
2.38 minutes on apw_eng_200605.conllu
-> searching Apw.conll/apw_eng_200606.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200606.conllu > data/neg-mit/Apw.few_subj/apw_eng_200606.raw.json
2.35 minutes on apw_eng_200606.conllu
-> searching Apw.conll/apw_eng_200607.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200607.conllu > data/neg-mit/Apw.few_subj/apw_eng_200607.raw.json
2.18 minutes on apw_eng_200607.conllu
-> searching Apw.conll/apw_eng_200608.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200608.conllu > data/neg-mit/Apw.few_subj/apw_eng_200608.raw.json
1.93 minutes on apw_eng_200608.conllu
-> searching Apw.conll/apw_eng_200609.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200609.conllu > data/neg-mit/Apw.few_subj/apw_eng_200609.raw.json
1.84 minutes on apw_eng_200609.conllu
-> searching Apw.conll/apw_eng_200610.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200610.conllu > data/neg-mit/Apw.few_subj/apw_eng_200610.raw.json
4.65 minutes on apw_eng_200610.conllu
-> searching Apw.conll/apw_eng_200611.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200611.conllu > data/neg-mit/Apw.few_subj/apw_eng_200611.raw.json
4.59 minutes on apw_eng_200611.conllu
-> searching Apw.conll/apw_eng_200612.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200612.conllu > data/neg-mit/Apw.few_subj/apw_eng_200612.raw.json
1.55 minutes on apw_eng_200612.conllu
-> searching Apw.conll/apw_eng_200701.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200701.conllu > data/neg-mit/Apw.few_subj/apw_eng_200701.raw.json
4.57 minutes on apw_eng_200701.conllu
-> searching Apw.conll/apw_eng_200702.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200702.conllu > data/neg-mit/Apw.few_subj/apw_eng_200702.raw.json
4.05 minutes on apw_eng_200702.conllu
-> searching Apw.conll/apw_eng_200703.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200703.conllu > data/neg-mit/Apw.few_subj/apw_eng_200703.raw.json
4.65 minutes on apw_eng_200703.conllu
-> searching Apw.conll/apw_eng_200704.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200704.conllu > data/neg-mit/Apw.few_subj/apw_eng_200704.raw.json
4.25 minutes on apw_eng_200704.conllu
-> searching Apw.conll/apw_eng_200705.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200705.conllu > data/neg-mit/Apw.few_subj/apw_eng_200705.raw.json
4.49 minutes on apw_eng_200705.conllu
-> searching Apw.conll/apw_eng_200706.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200706.conllu > data/neg-mit/Apw.few_subj/apw_eng_200706.raw.json
4.29 minutes on apw_eng_200706.conllu
-> searching Apw.conll/apw_eng_200707.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200707.conllu > data/neg-mit/Apw.few_subj/apw_eng_200707.raw.json
4.04 minutes on apw_eng_200707.conllu
-> searching Apw.conll/apw_eng_200708.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200708.conllu > data/neg-mit/Apw.few_subj/apw_eng_200708.raw.json
4.13 minutes on apw_eng_200708.conllu
-> searching Apw.conll/apw_eng_200709.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200709.conllu > data/neg-mit/Apw.few_subj/apw_eng_200709.raw.json
4.28 minutes on apw_eng_200709.conllu
-> searching Apw.conll/apw_eng_200710.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200710.conllu > data/neg-mit/Apw.few_subj/apw_eng_200710.raw.json
4.28 minutes on apw_eng_200710.conllu
-> searching Apw.conll/apw_eng_200711.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200711.conllu > data/neg-mit/Apw.few_subj/apw_eng_200711.raw.json
3.95 minutes on apw_eng_200711.conllu
-> searching Apw.conll/apw_eng_200712.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200712.conllu > data/neg-mit/Apw.few_subj/apw_eng_200712.raw.json
3.33 minutes on apw_eng_200712.conllu
-> searching Apw.conll/apw_eng_200801.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200801.conllu > data/neg-mit/Apw.few_subj/apw_eng_200801.raw.json
4.18 minutes on apw_eng_200801.conllu
-> searching Apw.conll/apw_eng_200802.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200802.conllu > data/neg-mit/Apw.few_subj/apw_eng_200802.raw.json
4.05 minutes on apw_eng_200802.conllu
-> searching Apw.conll/apw_eng_200803.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200803.conllu > data/neg-mit/Apw.few_subj/apw_eng_200803.raw.json
4.07 minutes on apw_eng_200803.conllu
-> searching Apw.conll/apw_eng_200804.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200804.conllu > data/neg-mit/Apw.few_subj/apw_eng_200804.raw.json
3.92 minutes on apw_eng_200804.conllu
-> searching Apw.conll/apw_eng_200805.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200805.conllu > data/neg-mit/Apw.few_subj/apw_eng_200805.raw.json
4.09 minutes on apw_eng_200805.conllu
-> searching Apw.conll/apw_eng_200806.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200806.conllu > data/neg-mit/Apw.few_subj/apw_eng_200806.raw.json
4.08 minutes on apw_eng_200806.conllu
-> searching Apw.conll/apw_eng_200807.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200807.conllu > data/neg-mit/Apw.few_subj/apw_eng_200807.raw.json
3.56 minutes on apw_eng_200807.conllu
-> searching Apw.conll/apw_eng_200808.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200808.conllu > data/neg-mit/Apw.few_subj/apw_eng_200808.raw.json
3.64 minutes on apw_eng_200808.conllu
-> searching Apw.conll/apw_eng_200809.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200809.conllu > data/neg-mit/Apw.few_subj/apw_eng_200809.raw.json
3.69 minutes on apw_eng_200809.conllu
-> searching Apw.conll/apw_eng_200810.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200810.conllu > data/neg-mit/Apw.few_subj/apw_eng_200810.raw.json
3.53 minutes on apw_eng_200810.conllu
-> searching Apw.conll/apw_eng_200811.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200811.conllu > data/neg-mit/Apw.few_subj/apw_eng_200811.raw.json
2.75 minutes on apw_eng_200811.conllu
-> searching Apw.conll/apw_eng_200812.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200812.conllu > data/neg-mit/Apw.few_subj/apw_eng_200812.raw.json
2.29 minutes on apw_eng_200812.conllu
-> searching Apw.conll/apw_eng_200901.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200901.conllu > data/neg-mit/Apw.few_subj/apw_eng_200901.raw.json
2.94 minutes on apw_eng_200901.conllu
-> searching Apw.conll/apw_eng_200902.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200902.conllu > data/neg-mit/Apw.few_subj/apw_eng_200902.raw.json
2.89 minutes on apw_eng_200902.conllu
-> searching Apw.conll/apw_eng_200903.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200903.conllu > data/neg-mit/Apw.few_subj/apw_eng_200903.raw.json
3.18 minutes on apw_eng_200903.conllu
-> searching Apw.conll/apw_eng_200904.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200904.conllu > data/neg-mit/Apw.few_subj/apw_eng_200904.raw.json
3.56 minutes on apw_eng_200904.conllu
-> searching Apw.conll/apw_eng_200905.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200905.conllu > data/neg-mit/Apw.few_subj/apw_eng_200905.raw.json
3.4 minutes on apw_eng_200905.conllu
-> searching Apw.conll/apw_eng_200906.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200906.conllu > data/neg-mit/Apw.few_subj/apw_eng_200906.raw.json
3.47 minutes on apw_eng_200906.conllu
-> searching Apw.conll/apw_eng_200907.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200907.conllu > data/neg-mit/Apw.few_subj/apw_eng_200907.raw.json
2.21 minutes on apw_eng_200907.conllu
-> searching Apw.conll/apw_eng_200908.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200908.conllu > data/neg-mit/Apw.few_subj/apw_eng_200908.raw.json
2.38 minutes on apw_eng_200908.conllu
-> searching Apw.conll/apw_eng_200909.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200909.conllu > data/neg-mit/Apw.few_subj/apw_eng_200909.raw.json
2.29 minutes on apw_eng_200909.conllu
-> searching Apw.conll/apw_eng_200910.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200910.conllu > data/neg-mit/Apw.few_subj/apw_eng_200910.raw.json
2.29 minutes on apw_eng_200910.conllu
-> searching Apw.conll/apw_eng_200911.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200911.conllu > data/neg-mit/Apw.few_subj/apw_eng_200911.raw.json
2.27 minutes on apw_eng_200911.conllu
-> searching Apw.conll/apw_eng_200912.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_200912.conllu > data/neg-mit/Apw.few_subj/apw_eng_200912.raw.json
2.36 minutes on apw_eng_200912.conllu
-> searching Apw.conll/apw_eng_201001.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201001.conllu > data/neg-mit/Apw.few_subj/apw_eng_201001.raw.json
2.8 minutes on apw_eng_201001.conllu
-> searching Apw.conll/apw_eng_201002.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201002.conllu > data/neg-mit/Apw.few_subj/apw_eng_201002.raw.json
1.89 minutes on apw_eng_201002.conllu
-> searching Apw.conll/apw_eng_201003.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201003.conllu > data/neg-mit/Apw.few_subj/apw_eng_201003.raw.json
2.08 minutes on apw_eng_201003.conllu
-> searching Apw.conll/apw_eng_201004.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201004.conllu > data/neg-mit/Apw.few_subj/apw_eng_201004.raw.json
2.06 minutes on apw_eng_201004.conllu
-> searching Apw.conll/apw_eng_201005.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201005.conllu > data/neg-mit/Apw.few_subj/apw_eng_201005.raw.json
2.06 minutes on apw_eng_201005.conllu
-> searching Apw.conll/apw_eng_201006.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201006.conllu > data/neg-mit/Apw.few_subj/apw_eng_201006.raw.json
2.14 minutes on apw_eng_201006.conllu
-> searching Apw.conll/apw_eng_201007.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201007.conllu > data/neg-mit/Apw.few_subj/apw_eng_201007.raw.json
1.75 minutes on apw_eng_201007.conllu
-> searching Apw.conll/apw_eng_201008.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201008.conllu > data/neg-mit/Apw.few_subj/apw_eng_201008.raw.json
2.72 minutes on apw_eng_201008.conllu
-> searching Apw.conll/apw_eng_201009.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201009.conllu > data/neg-mit/Apw.few_subj/apw_eng_201009.raw.json
3.04 minutes on apw_eng_201009.conllu
-> searching Apw.conll/apw_eng_201010.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201010.conllu > data/neg-mit/Apw.few_subj/apw_eng_201010.raw.json
3.12 minutes on apw_eng_201010.conllu
-> searching Apw.conll/apw_eng_201011.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201011.conllu > data/neg-mit/Apw.few_subj/apw_eng_201011.raw.json
3.26 minutes on apw_eng_201011.conllu
-> searching Apw.conll/apw_eng_201012.conllu:
grew grep -pattern Pat/neg-mit/few_subj.pat -i Apw.conll/apw_eng_201012.conllu > data/neg-mit/Apw.few_subj/apw_eng_201012.raw.json
2.64 minutes on apw_eng_201012.conllu

Total grew search time: 548.91 minutes
==============================================

```
### Running `FillJson.py` script on json files in `Apw.few_subj` from conll files in `Apw.conll`...
```
-> Processing apw_eng_200507...
-> Skipping. (file is empty)
-> Processing apw_eng_200611...
-> Skipping. (file is empty)
-> Processing apw_eng_200610...
-> Skipping. (file is empty)
-> Processing apw_eng_200704...
   => 3 hit results filled from 505054 total original sentences in 54.9 seconds
-> Writing output file...
-> Processing apw_eng_199608...
-> Skipping. (file is empty)
-> Processing apw_eng_199807...
   => 2 hit results filled from 260597 total original sentences in 28.77 seconds
-> Writing output file...
-> Processing apw_eng_201010...
   => 1 hit results filled from 336943 total original sentences in 39.34 seconds
-> Writing output file...
-> Processing apw_eng_200410...
-> Skipping. (file is empty)
-> Processing apw_eng_199904...
-> Skipping. (file is empty)
-> Processing apw_eng_199712...
   => 2 hit results filled from 439289 total original sentences in 45.76 seconds
-> Writing output file...
-> Processing apw_eng_200004...
-> Skipping. (file is empty)
-> Processing apw_eng_199906...
   => 1 hit results filled from 329537 total original sentences in 37.55 seconds
-> Writing output file...
-> Processing apw_eng_199706...
-> Skipping. (file is empty)
-> Processing apw_eng_201004...
-> Skipping. (file is empty)
-> Processing apw_eng_200010...
-> Skipping. (file is empty)
-> Processing apw_eng_200609...
   => 4 hit results filled from 208300 total original sentences in 24.52 seconds
-> Writing output file...
-> Processing apw_eng_199603...
-> Skipping. (file is empty)
-> Processing apw_eng_200801...
   => 3 hit results filled from 489641 total original sentences in 53.71 seconds
-> Writing output file...
-> Processing apw_eng_200201...
   => 1 hit results filled from 397280 total original sentences in 46.45 seconds
-> Writing output file...
-> Processing apw_eng_199605...
   => 4 hit results filled from 244175 total original sentences in 25.84 seconds
-> Writing output file...
-> Processing apw_eng_200006...
   => 1 hit results filled from 123538 total original sentences in 13.63 seconds
-> Writing output file...
-> Processing apw_eng_200906...
-> Skipping. (file is empty)
-> Processing apw_eng_201007...
-> Skipping. (file is empty)
-> Processing apw_eng_200208...
   => 1 hit results filled from 453026 total original sentences in 41.85 seconds
-> Writing output file...
-> Processing apw_eng_201001...
-> Skipping. (file is empty)
-> Processing apw_eng_201006...
-> Skipping. (file is empty)
-> Processing apw_eng_199612...
   => 9 hit results filled from 236714 total original sentences in 25.17 seconds
-> Writing output file...
-> Processing apw_eng_200212...
-> Skipping. (file is empty)
-> Processing apw_eng_200406...
-> Skipping. (file is empty)
-> Processing apw_eng_200102...
-> Skipping. (file is empty)
-> Processing apw_eng_200302...
   => 1 hit results filled from 510838 total original sentences in 50.45 seconds
-> Writing output file...
-> Processing apw_eng_200705...
-> Skipping. (file is empty)
-> Processing apw_eng_200811...
-> Skipping. (file is empty)
-> Processing apw_eng_200608...
   => 2 hit results filled from 216402 total original sentences in 24.03 seconds
-> Writing output file...
-> Processing apw_eng_200502...
-> Skipping. (file is empty)
-> Processing apw_eng_200905...
-> Skipping. (file is empty)
-> Processing apw_eng_200211...
-> Skipping. (file is empty)
-> Processing apw_eng_200710...
   => 1 hit results filled from 496362 total original sentences in 55.07 seconds
-> Writing output file...
-> Processing apw_eng_200901...
-> Skipping. (file is empty)
-> Processing apw_eng_200202...
-> Skipping. (file is empty)
-> Processing apw_eng_199804...
-> Skipping. (file is empty)
-> Processing apw_eng_200904...
-> Skipping. (file is empty)
-> Processing apw_eng_200505...
-> Skipping. (file is empty)
-> Processing apw_eng_201005...
   => 7 hit results filled from 217021 total original sentences in 26.63 seconds
-> Writing output file...
-> Processing apw_eng_200506...
-> Skipping. (file is empty)
-> Processing apw_eng_199412...
   => 1 hit results filled from 275635 total original sentences in 30.08 seconds
-> Writing output file...
-> Processing apw_eng_199902...
-> Skipping. (file is empty)
-> Processing apw_eng_199702...
-> Skipping. (file is empty)
-> Processing apw_eng_200308...
-> Skipping. (file is empty)
-> Processing apw_eng_200802...
   => 2 hit results filled from 475152 total original sentences in 51.44 seconds
-> Writing output file...
-> Processing apw_eng_200109...
   => 1 hit results filled from 401352 total original sentences in 44.15 seconds
-> Writing output file...
-> Processing apw_eng_199810...
-> Skipping. (file is empty)
-> Processing apw_eng_200702...
-> Skipping. (file is empty)
-> Processing apw_eng_200504...
   => 3 hit results filled from 175752 total original sentences in 19.07 seconds
-> Writing output file...
-> Processing apw_eng_200103...
   => 1 hit results filled from 678001 total original sentences in 61.53 seconds
-> Writing output file...
-> Processing apw_eng_199703...
-> Skipping. (file is empty)
-> Processing apw_eng_200012...
   => 1 hit results filled from 646296 total original sentences in 58.97 seconds
-> Writing output file...
-> Processing apw_eng_200401...
-> Skipping. (file is empty)
-> Processing apw_eng_201003...
   => 2 hit results filled from 220617 total original sentences in 26.47 seconds
-> Writing output file...
-> Processing apw_eng_199903...
-> Skipping. (file is empty)
-> Processing apw_eng_199704...
   => 1 hit results filled from 249509 total original sentences in 27.86 seconds
-> Writing output file...
-> Processing apw_eng_199604...
   => 3 hit results filled from 242462 total original sentences in 26.71 seconds
-> Writing output file...
-> Processing apw_eng_200708...
-> Skipping. (file is empty)
-> Processing apw_eng_201009...
   => 1 hit results filled from 316729 total original sentences in 38.52 seconds
-> Writing output file...
-> Processing apw_eng_200601...
   => 4 hit results filled from 245144 total original sentences in 28.55 seconds
-> Writing output file...
-> Processing apw_eng_200503...
-> Skipping. (file is empty)
-> Processing apw_eng_200809...
-> Skipping. (file is empty)
-> Processing apw_eng_200810...
-> Skipping. (file is empty)
-> Processing apw_eng_199901...
   => 4 hit results filled from 292996 total original sentences in 33.21 seconds
-> Writing output file...
-> Processing apw_eng_200706...
   => 3 hit results filled from 487947 total original sentences in 54.77 seconds
-> Writing output file...
-> Processing apw_eng_200210...
   => 5 hit results filled from 547369 total original sentences in 54.58 seconds
-> Writing output file...
-> Processing apw_eng_199711...
   => 2 hit results filled from 330740 total original sentences in 36.14 seconds
-> Writing output file...
-> Processing apw_eng_200803...
-> Skipping. (file is empty)
-> Processing apw_eng_200203...
   => 1 hit results filled from 413600 total original sentences in 48.49 seconds
-> Writing output file...
-> Processing apw_eng_200304...
-> Skipping. (file is empty)
-> Processing apw_eng_200709...
   => 8 hit results filled from 503440 total original sentences in 56.04 seconds
-> Writing output file...
-> Processing apw_eng_200303...
-> Skipping. (file is empty)
-> Processing apw_eng_200602...
-> Skipping. (file is empty)
-> Processing apw_eng_199501...
   => 2 hit results filled from 285984 total original sentences in 30.93 seconds
-> Writing output file...
-> Processing apw_eng_199805...
   => 2 hit results filled from 486174 total original sentences in 49.45 seconds
-> Writing output file...
-> Processing apw_eng_200605...
   => 1 hit results filled from 261725 total original sentences in 31.21 seconds
-> Writing output file...
-> Processing apw_eng_200603...
-> Skipping. (file is empty)
-> Processing apw_eng_200107...
   => 1 hit results filled from 719645 total original sentences in 61.51 seconds
-> Writing output file...
-> Processing apw_eng_199611...
-> Skipping. (file is empty)
-> Processing apw_eng_200209...
-> Skipping. (file is empty)
-> Processing apw_eng_200110...
-> Skipping. (file is empty)
-> Processing apw_eng_199709...
-> Skipping. (file is empty)
-> Processing apw_eng_199812...
-> Skipping. (file is empty)
-> Processing apw_eng_200206...
   => 2 hit results filled from 417879 total original sentences in 48.5 seconds
-> Writing output file...
-> Processing apw_eng_200508...
   => 1 hit results filled from 218299 total original sentences in 24.54 seconds
-> Writing output file...
-> Processing apw_eng_201002...
-> Skipping. (file is empty)
-> Processing apw_eng_200101...
   => 1 hit results filled from 658781 total original sentences in 60.46 seconds
-> Writing output file...
-> Processing apw_eng_200311...
   => 7 hit results filled from 532321 total original sentences in 55.95 seconds
-> Writing output file...
-> Processing apw_eng_200411...
-> Skipping. (file is empty)
-> Processing apw_eng_200009...
-> Skipping. (file is empty)
-> Processing apw_eng_200812...
-> Skipping. (file is empty)
-> Processing apw_eng_199505...
-> Skipping. (file is empty)
-> Processing apw_eng_200902...
   => 6 hit results filled from 311293 total original sentences in 37.24 seconds
-> Writing output file...
-> Processing apw_eng_200607...
-> Skipping. (file is empty)
-> Processing apw_eng_199801...
   => 1 hit results filled from 469278 total original sentences in 48.42 seconds
-> Writing output file...
-> Processing apw_eng_199708...
   => 1 hit results filled from 257824 total original sentences in 28.49 seconds
-> Writing output file...
-> Processing apw_eng_200808...
   => 1 hit results filled from 419590 total original sentences in 46.31 seconds
-> Writing output file...
-> Processing apw_eng_200908...
   => 3 hit results filled from 252526 total original sentences in 30.11 seconds
-> Writing output file...
-> Processing apw_eng_201011...
   => 3 hit results filled from 340494 total original sentences in 40.06 seconds
-> Writing output file...
-> Processing apw_eng_200911...
-> Skipping. (file is empty)
-> Processing apw_eng_199705...
-> Skipping. (file is empty)
-> Processing apw_eng_199509...
-> Skipping. (file is empty)
-> Processing apw_eng_200112...
-> Skipping. (file is empty)
-> Processing apw_eng_200707...
-> Skipping. (file is empty)
-> Processing apw_eng_200712...
   => 2 hit results filled from 391549 total original sentences in 40.79 seconds
-> Writing output file...
-> Processing apw_eng_200305...
-> Skipping. (file is empty)
-> Processing apw_eng_200512...
-> Skipping. (file is empty)
-> Processing apw_eng_200606...
   => 2 hit results filled from 250232 total original sentences in 27.97 seconds
-> Writing output file...
-> Processing apw_eng_200301...
-> Skipping. (file is empty)
-> Processing apw_eng_200807...
-> Skipping. (file is empty)
-> Processing apw_eng_200011...
-> Skipping. (file is empty)
-> Processing apw_eng_199502...
-> Skipping. (file is empty)
-> Processing apw_eng_199710...
   => 1 hit results filled from 263541 total original sentences in 28.22 seconds
-> Writing output file...
-> Processing apw_eng_200111...
   => 3 hit results filled from 371348 total original sentences in 41.98 seconds
-> Writing output file...
-> Processing apw_eng_200407...
   => 1 hit results filled from 223683 total original sentences in 24.75 seconds
-> Writing output file...
-> Processing apw_eng_199510...
-> Skipping. (file is empty)
-> Processing apw_eng_199512...
-> Skipping. (file is empty)
-> Processing apw_eng_199908...
-> Skipping. (file is empty)
-> Processing apw_eng_199609...
-> Skipping. (file is empty)
-> Processing apw_eng_200307...
-> Skipping. (file is empty)
-> Processing apw_eng_200403...
   => 2 hit results filled from 637253 total original sentences in 63.32 seconds
-> Writing output file...
-> Processing apw_eng_200104...
   => 1 hit results filled from 657531 total original sentences in 57.28 seconds
-> Writing output file...
-> Processing apw_eng_199602...
   => 1 hit results filled from 221029 total original sentences in 23.07 seconds
-> Writing output file...
-> Processing apw_eng_200703...
-> Skipping. (file is empty)
-> Processing apw_eng_200105...
   => 1 hit results filled from 728729 total original sentences in 61.83 seconds
-> Writing output file...
-> Processing apw_eng_200805...
-> Skipping. (file is empty)
-> Processing apw_eng_200108...
-> Skipping. (file is empty)
-> Processing apw_eng_199607...
-> Skipping. (file is empty)
-> Processing apw_eng_199504...
   => 3 hit results filled from 280156 total original sentences in 30.03 seconds
-> Writing output file...
-> Processing apw_eng_200309...
-> Skipping. (file is empty)
-> Processing apw_eng_200007...
-> Skipping. (file is empty)
-> Processing apw_eng_200806...
-> Skipping. (file is empty)
-> Processing apw_eng_199508...
   => 1 hit results filled from 345561 total original sentences in 37.22 seconds
-> Writing output file...
-> Processing apw_eng_200312...
-> Skipping. (file is empty)
-> Processing apw_eng_200701...
   => 1 hit results filled from 543943 total original sentences in 56.94 seconds
-> Writing output file...
-> Processing apw_eng_200409...
-> Skipping. (file is empty)
-> Processing apw_eng_200408...
   => 1 hit results filled from 210307 total original sentences in 22.01 seconds
-> Writing output file...
-> Processing apw_eng_200907...
-> Skipping. (file is empty)
-> Processing apw_eng_199911...
-> Skipping. (file is empty)
-> Processing apw_eng_200510...
   => 1 hit results filled from 233906 total original sentences in 26.51 seconds
-> Writing output file...
-> Processing apw_eng_199811...
   => 2 hit results filled from 259993 total original sentences in 28.54 seconds
-> Writing output file...
-> Processing apw_eng_199511...
-> Skipping. (file is empty)
-> Processing apw_eng_199910...
-> Skipping. (file is empty)
-> Processing apw_eng_200804...
   => 5 hit results filled from 481942 total original sentences in 48.88 seconds
-> Writing output file...
-> Processing apw_eng_199808...
   => 2 hit results filled from 254664 total original sentences in 27.62 seconds
-> Writing output file...
-> Processing apw_eng_200207...
   => 1 hit results filled from 493487 total original sentences in 47.4 seconds
-> Writing output file...
-> Processing apw_eng_201008...
-> Skipping. (file is empty)
-> Processing apw_eng_199411...
   => 2 hit results filled from 184672 total original sentences in 19.69 seconds
-> Writing output file...
-> Processing apw_eng_199907...
   => 2 hit results filled from 308319 total original sentences in 33.24 seconds
-> Writing output file...
-> Processing apw_eng_200412...
-> Skipping. (file is empty)
-> Processing apw_eng_200501...
   => 1 hit results filled from 183872 total original sentences in 19.8 seconds
-> Writing output file...
-> Processing apw_eng_199503...
   => 1 hit results filled from 292602 total original sentences in 30.55 seconds
-> Writing output file...
-> Processing apw_eng_200005...
   => 1 hit results filled from 143837 total original sentences in 15.75 seconds
-> Writing output file...
-> Processing apw_eng_200509...
   => 1 hit results filled from 252467 total original sentences in 28.33 seconds
-> Writing output file...
-> Processing apw_eng_201012...
-> Skipping. (file is empty)
-> Processing apw_eng_199707...
   => 1 hit results filled from 274132 total original sentences in 28.59 seconds
-> Writing output file...
-> Processing apw_eng_200511...
-> Skipping. (file is empty)
-> Processing apw_eng_199701...
-> Skipping. (file is empty)
-> Processing apw_eng_200402...
-> Skipping. (file is empty)
-> Processing apw_eng_200903...
-> Skipping. (file is empty)
-> Processing apw_eng_199506...
   => 2 hit results filled from 367416 total original sentences in 38.88 seconds
-> Writing output file...
-> Processing apw_eng_200204...
-> Skipping. (file is empty)
-> Processing apw_eng_200001...
-> Skipping. (file is empty)
-> Processing apw_eng_199507...
   => 5 hit results filled from 337637 total original sentences in 36.72 seconds
-> Writing output file...
-> Processing apw_eng_199806...
   => 3 hit results filled from 422120 total original sentences in 44.86 seconds
-> Writing output file...
-> Processing apw_eng_199601...
-> Skipping. (file is empty)
-> Processing apw_eng_200003...
-> Skipping. (file is empty)
-> Processing apw_eng_200205...
   => 1 hit results filled from 420016 total original sentences in 48.59 seconds
-> Writing output file...
-> Processing apw_eng_200909...
   => 1 hit results filled from 239137 total original sentences in 28.39 seconds
-> Writing output file...
-> Processing apw_eng_199809...
   => 5 hit results filled from 271149 total original sentences in 30.53 seconds
-> Writing output file...
-> Processing apw_eng_200002...
-> Skipping. (file is empty)
-> Processing apw_eng_200711...
   => 2 hit results filled from 465709 total original sentences in 50.56 seconds
-> Writing output file...
-> Processing apw_eng_200910...
-> Skipping. (file is empty)
-> Processing apw_eng_199909...
-> Skipping. (file is empty)
-> Processing apw_eng_200404...
   => 3 hit results filled from 556081 total original sentences in 56.79 seconds
-> Writing output file...
-> Processing apw_eng_199606...
-> Skipping. (file is empty)
-> Processing apw_eng_200306...
-> Skipping. (file is empty)
-> Processing apw_eng_200106...
   => 8 hit results filled from 751043 total original sentences in 64.39 seconds
-> Writing output file...
-> Processing apw_eng_199905...
   => 1 hit results filled from 321831 total original sentences in 36.05 seconds
-> Writing output file...
-> Processing apw_eng_200008...
-> Skipping. (file is empty)
-> Processing apw_eng_200405...
-> Skipping. (file is empty)
-> Processing apw_eng_200912...
-> Skipping. (file is empty)
-> Processing apw_eng_199802...
   => 2 hit results filled from 485186 total original sentences in 48.74 seconds
-> Writing output file...
-> Processing apw_eng_200612...
   => 3 hit results filled from 179461 total original sentences in 19.9 seconds
-> Writing output file...
-> Processing apw_eng_199610...
   => 1 hit results filled from 222915 total original sentences in 24.14 seconds
-> Writing output file...
-> Processing apw_eng_199803...
-> Skipping. (file is empty)
-> Processing apw_eng_200310...
-> Skipping. (file is empty)
-> Processing apw_eng_200604...
-> Skipping. (file is empty)
Finished processing all corresponding json and conll files.

Time elapsed: 54.71 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing apw_eng_200704.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070413_0774_18:12 discarded.
-> Processing apw_eng_199807.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980711_0763_7:7 discarded.
-> Processing apw_eng_201010.json...
-> Processing apw_eng_199712.json...
-> Processing apw_eng_199906.json...
-> Processing apw_eng_200609.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20060920_1733_4:10 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20060920_1609_4:10 discarded.
-> Processing apw_eng_200801.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080129_1294_20:22 discarded.
-> Processing apw_eng_200201.json...
-> Processing apw_eng_199605.json...
-> Processing apw_eng_200006.json...
-> Processing apw_eng_200208.json...
-> Processing apw_eng_199612.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19961223_0277_2:46 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19961223_0255_2:46 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19961215_0951_8:6 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19961215_0807_3:6 discarded.
-> Processing apw_eng_200302.json...
-> Processing apw_eng_200608.json...
-> Processing apw_eng_200710.json...
-> Processing apw_eng_201005.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100523_0065_41:9 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100523_0054_40:9 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100523_0026_38:9 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20100523_0024_35:9 discarded.
-> Processing apw_eng_199412.json...
-> Processing apw_eng_200802.json...
-> Processing apw_eng_200109.json...
-> Processing apw_eng_200504.json...
-> Processing apw_eng_200103.json...
-> Processing apw_eng_200012.json...
-> Processing apw_eng_201003.json...
-> Processing apw_eng_199704.json...
-> Processing apw_eng_199604.json...
-> Processing apw_eng_201009.json...
-> Processing apw_eng_200601.json...
-> Processing apw_eng_199901.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990130_0621_14:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990130_0602_14:5 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990130_0599_14:5 discarded.
-> Processing apw_eng_200706.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070625_1009_1:12 discarded.
-> Processing apw_eng_200210.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20021015_0824_7:35 discarded.
-> Processing apw_eng_199711.json...
-> Processing apw_eng_200203.json...
-> Processing apw_eng_200709.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070910_1056_7:27 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070905_0600_2:7 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20070904_1507_2:7 discarded.
-> Processing apw_eng_199501.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950118_0006_1:13 discarded.
-> Processing apw_eng_199805.json...
-> Processing apw_eng_200605.json...
-> Processing apw_eng_200107.json...
-> Processing apw_eng_200206.json...
-> Processing apw_eng_200508.json...
-> Processing apw_eng_200101.json...
-> Processing apw_eng_200311.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20031130_0499_4:12 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20031130_0489_4:12 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20031125_0080_20:9 discarded.
-> Processing apw_eng_200902.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090223_1103_19:26 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090212_0781_22:4 discarded.
-> Processing apw_eng_199801.json...
-> Processing apw_eng_199708.json...
-> Processing apw_eng_200808.json...
-> Processing apw_eng_200908.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20090802_0567_28:16 discarded.
-> Processing apw_eng_201011.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20101117_0735_20:5 discarded.
-> Processing apw_eng_200712.json...
-> Processing apw_eng_200606.json...
-> Processing apw_eng_199710.json...
-> Processing apw_eng_200111.json...
-> Processing apw_eng_200407.json...
-> Processing apw_eng_200403.json...
-> Processing apw_eng_200104.json...
-> Processing apw_eng_199602.json...
-> Processing apw_eng_200105.json...
-> Processing apw_eng_199504.json...
-> Processing apw_eng_199508.json...
-> Processing apw_eng_200701.json...
-> Processing apw_eng_200408.json...
-> Processing apw_eng_200510.json...
-> Processing apw_eng_199811.json...
-> Processing apw_eng_200804.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080406_0873_26:20 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20080406_0585_15:20 discarded.
-> Processing apw_eng_199808.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980804_0565_4:13 discarded.
-> Processing apw_eng_200207.json...
-> Processing apw_eng_199411.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19941130_0159_25:17 discarded.
-> Processing apw_eng_199907.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19990722_1288_22:3 discarded.
-> Processing apw_eng_200501.json...
-> Processing apw_eng_199503.json...
-> Processing apw_eng_200005.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20000531_0214_18:18 discarded.
-> Processing apw_eng_200509.json...
-> Processing apw_eng_199707.json...
-> Processing apw_eng_199506.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950628_0995_20:6 discarded.
-> Processing apw_eng_199507.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950714_1234_37:6 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950714_1228_37:6 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950714_1225_37:6 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19950714_1205_37:6 discarded.
-> Processing apw_eng_199806.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980603_1049_9:18 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980603_0392_2:18 discarded.
-> Processing apw_eng_200205.json...
-> Processing apw_eng_200909.json...
-> Processing apw_eng_199809.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980915_1089_1:16 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_19980915_1063_1:16 discarded.
-> Processing apw_eng_200711.json...
-> Processing apw_eng_200404.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20040422_0625_6:22 discarded.
-> Processing apw_eng_200106.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010615_1086_31:21 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010615_1057_31:21 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010615_1055_31:21 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010615_0989_31:21 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010615_0988_31:21 discarded.
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20010615_0938_3:21 discarded.
-> Processing apw_eng_199905.json...
-> Processing apw_eng_199802.json...
-> Processing apw_eng_200612.json...
-> Exact text match to previous records. Checking token word strings...
   [comparing to previous match 1]
   + adverb label and index match...
       and adjective label also matches.
  + Hit apw_eng_20061201_1470_1:18 discarded.
-> Processing apw_eng_199610.json...

^_^ Finished collecting sentence data from all json files.
    -> Writing tables to csv files...
```
```

Time elapsed: 0.05 seconds
====================================

```  
 
## Finished at: `Fri Aug  6 02:16:23 EDT 2021`
  + All raw data in `data/neg-mit/Apw.few_subj/...`
  + All hit tabulations in `hits/neg-mit/...`

  + Total time to populate hits/neg-mit: 11:09:09
