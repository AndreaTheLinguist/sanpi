
# Running `./script/makeTable.sh`
_Checking for requirements..._
```
pyconll located in /home/andrea/anaconda3/bin/python3
pandas located in /home/andrea/anaconda3/bin/python3
grew located in /home/andrea/.opam/4.11.1/bin/grew
```
## >> Searching `playground/nyFeb2010.conll/` for `immediateNeg` patterns
 
- started by: `andrea`
- run from: `/home/andrea/litotes`
- timestamp: `Wed Oct  6 01:12:38 EDT 2021`
 
```
## Starting context: `without_relay`
- time stamp: `Wed Oct  6 01:12:38 EDT 2021`
- data directory: `data/immediateNeg/nyFeb2010.without_relay`
- hits table: `hits/immediateNeg/nyFeb2010_without_relay`
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
```
### Running grew search on `nyFeb2010.conll`...
```
1 total file(s) to be searched.
-> searching nyFeb2010.conll/nyt_eng_201002.conllu:
grew grep -pattern playground/Pat/immediateNeg/without_relay.pat -i playground/nyFeb2010.conll/nyt_eng_201002.conllu > data/immediateNeg/nyFeb2010.without_relay/nyt_eng_201002.raw.json
4.11 minutes on nyt_eng_201002.conllu

Total grew search time: 4.11 minutes
==============================================

```
### Running `FillJson.py` script on json files in `nyFeb2010.without_relay` from conll files in `nyFeb2010.conll`...
```
-> Processing nyt_eng_201002...
   => 1470 hit results filled from 190244 total original sentences in 22.82 seconds
-> Writing output file...
Finished processing all corresponding json and conll files.

Time elapsed: 0.38 minutes
====================================

```
### Tabulating hits via `tabulateHits.py`...
```
-> Processing nyt_eng_201002.json...

^_^ Finished tabulating data for 1470 sentence(s) from all json files in /home/andrea/litotes/data/immediateNeg/nyFeb2010.without_relay.
-> Writing tables to csv files...
```
#### Data Sample

| hit_id                            | neg_word   | colloc   | sent_text                                                                                                                                                                                                     |
|:----------------------------------|:-----------|:---------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| nyt_eng_20100214_0145_20:37-38-39 | not        | ?        | But Vinny Lecavalier , without a point in five games and minus-7 in three , has disappeared , and Ryan Malone -LRB- zero goals in 11 games -RRB- and Alex Tanguay -LRB- one in 12 -RRB- are not much better . |
| nyt_eng_20100212_0050_32:6-7-8    | not        | ?        | The underworld , incidentally , is n't very frightening , at least until Hades -LRB- Steve Coogan -RRB- , its seemingly genial host , reveals his monstrous side .                                            |
| nyt_eng_20100219_0124_62:19-21-22 | not        | ?        | It will just be harder now because the scrutiny will ratchet , and those huge galleries at tournaments might not be so Tiger-friendly .                                                                       |
| nyt_eng_20100204_0137_34:7-8-9    | not        | ?        | And the experimental combined system itself was not fully automated .                                                                                                                                         |
| nyt_eng_20100217_0096_9:20-21-22  | not        | ?        | Good rule of thumb  -COL-  If they offer you a role that requires messed-up teeth , the role 's probably not that good , anyway .                                                                             |
```

Time elapsed: 0.354 seconds
====================================

script/tabulateHits.py:117: FutureWarning: The default value of regex will change from True to False in a future version. In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
  df.columns = (df.columns.str.replace('.', '_')
```  
 
## Finished at: `Wed Oct  6 01:17:09 EDT 2021`
  + All raw data in `data/immediateNeg/nyFeb2010.without_relay/...`
  + All hit tabulations in `hits/immediateNeg/...`

  + Total time to populate hits/immediateNeg: 00:06:02
