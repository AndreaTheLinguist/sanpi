
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
