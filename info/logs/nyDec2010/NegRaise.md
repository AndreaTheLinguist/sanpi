
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `playground/nyDec2010.conll/` for `NegRaise` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:20:02 EDT 2021`
 
```
Output directory data/NegRaise already exists and contains these relevant files:
data/NegRaise/nyDec2010.negraise/nyt_eng_201012.raw.json
 
* If pattern or corpus files have not changed since these files were created, skipping the grew corpus search is recommended (n).
 
--> Run grew search on nyDec2010 again and overwrite any corresponding files? y/n 
= Corpus nyDec2010 will be searched again. Corresponding files in data/NegRaise will be overwritten.
```
## Starting context: `negraise`
- time stamp: `Wed Oct  6 01:20:03 EDT 2021`
- data directory: `data/NegRaise/nyDec2010.negraise`
- hits table: `hits/NegRaise/nyDec2010_negraise`
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
```
### Running grew search on `nyDec2010.conll`...
```
1 total file(s) to be searched.
-> searching nyDec2010.conll/nyt_eng_201012.conllu:
grew grep -pattern playground/Pat/NegRaise/negraise.pat -i playground/nyDec2010.conll/nyt_eng_201012.conllu > data/NegRaise/nyDec2010.negraise/nyt_eng_201012.raw.json
4.91 minutes on nyt_eng_201012.conllu

Total grew search time: 4.91 minutes
==============================================

```
### Running `FillJson.py` script on json files in `nyDec2010.negraise` from conll files in `nyDec2010.conll`...
```
-> Processing nyt_eng_201012...
   => 212 hit results filled from 227205 total original sentences in 30.31 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.51 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_201012.json...

^_^ Finished tabulating data for 212 sentence(s) from all json files in /home/andrea/litotes/data/NegRaise/nyDec2010.negraise.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                            | neg_word   | colloc   | sent_text                                                                                                                                                                                                                                      |
|:----------------------------------|:-----------|:---------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_20101215_0029_10:3-13-14  | not        | ?        | -LBQ-  I do n't think that the home team in most cases has as big of an advantage as they used to have because of competitive balance in the league ,  -RDQ-  said Gil Brandt , an analyst for NFL.com and former Dallas Cowboys executive .   |
| nyt_eng_20101215_0039_24:16-20-21 | not        | ?        | -LBQ-  I had to confess that I do think about an audience , and I do n't think that 's so bad ,  -RDQ-  she said .                                                                                                                             |
| nyt_eng_20101214_0215_18:3-5-6    | never      | ?        | Stuffed animals had never looked so heartbreaking .                                                                                                                                                                                            |
| nyt_eng_20101222_0123_14:23-27-28 | not        | ?        | The stakes Sunday will be similar to 2008 when New York beat the Packers 23-20 in overtime , even if the weather is not expected to be as blustery as it was then .                                                                            |
| nyt_eng_20101220_0008_5:3-19-20   | not        | ?        | -LBQ-  We did n't think they were going to come this year with all the rain ; they 're so awesome !  -RDQ-  exclaimed Elsey Fernandez after the hogs and a pickup full of tarp-covered toys pulled up to drop off presents for her grandkids . |
```

Time elapsed: 0.19 seconds
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```  
 
## Finished at: `Wed Oct  6 01:25:29 EDT 2021`
  + All raw data in `data/NegRaise/nyDec2010.negraise/...`
  + All hit tabulations in `hits/NegRaise/...`

  + Total time to populate hits/NegRaise: 00:05:29
