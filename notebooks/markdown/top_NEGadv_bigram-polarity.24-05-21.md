```python
import re
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, print_iter, print_md_table
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.general import PKL_SUFF, confirm_dir, timestamp_today
from source.utils.sample import sample_pickle as sp

K = 6
BK = max(K+2, 10)
DATE = timestamp_today()
FOCUS = adjust_assoc_columns(['f', 'E11', 'unexpected_f',
                              'am_p1_given2', 'conservative_log_ratio',
                              'am_log_likelihood',
                              #   't_score', 'mutual_information', 'am_odds_ratio_disc',
                              'N', 'f1', 'f2', 'l1', 'l2'])
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 80)

NEG_HITS_PATH = POST_PROC_DIR.joinpath(
    'RBdirect/trigger-bigrams_frq-thrMIN-7.35f.pkl.gz')
PRE_FILTERED_NEG_HITS = NEG_HITS_PATH.with_name(NEG_HITS_PATH.name.replace('trigger', f'onlyTop{K}_NEG-ADV'))
if not NEG_HITS_PATH.is_file():
    NEG_HITS_PATH = NEG_HITS_PATH.with_name(
        'trigger-bigrams_thr0-001p.35f.pkl.gz')
    
```


```python
def nb_show_table(df, n_dec:int=2, 
                   adjust_columns:bool=True, 
                   outpath:Path=None) -> None: 
    _df = df.copy()
    if adjust_columns: 
        _df = adjust_assoc_columns(_df)

    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index ]
    table = _df.convert_dtypes().to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    if outpath:
        outpath.write_text(table)

    print(f'\n{table}\n')
    
def force_ints(_df):
    count_cols = _df.filter(regex=r'total|^[fN]').columns
    _df.loc[:, count_cols] = _df.loc[:, count_cols].astype('int')
    # _df[count_cols] = _df[:, count_cols].astype('int64')
    # print(_df.dtypes.to_frame('dtypes'))
    return _df

```


```python
adv_am = []
while not any(adv_am):
    try:
        adv_am = pd.read_csv(
            TOP_AM_DIR / f'Top{K}_NEG-ADV_combined.35f-7c_{DATE}.csv').set_index('adv')
    except FileNotFoundError:
        DATE = DATE[:-1]+str(int(DATE[-1])-1)

bigram_am = pd.read_csv(TOP_AM_DIR / f'Top{K}_NEG-ADV_top-{BK}-bigrams.{DATE}.csv').set_index('key')
```


```python
nb_show_table(bigram_am.round(2).nlargest(BK*2, ['dP1','LRC','G2']), outpath=TOP_AM_DIR / f'Top{K}_NEG-ADV_top{BK*2}bigrams-overall.md')
```

    
    |                                   |    `f` |   `dP1` |   `LRC` |      `G2` |        `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`    | `l2`                   | `adj`      |   `adj_total` | `adv`       |   `adv_total` |
    |:----------------------------------|-------:|--------:|--------:|----------:|-----------:|----------:|-------:|----------:|------------:|:--------|:-----------------------|:-----------|--------------:|:------------|--------------:|
    | **NEGany~exactly_surprising**     |    441 |    0.96 |    7.34 |  2,863.35 | 86,330,752 | 3,226,213 |    444 |     16.59 |      424.41 | NEGATED | exactly_surprising     | surprising |       150,067 | exactly     |        61,599 |
    | **NEGany~yet_clear**              | 10,553 |    0.95 |   10.26 | 67,924.56 | 86,330,752 | 3,226,213 | 10,693 |    399.60 |   10,153.40 | NEGATED | yet_clear              | clear      |       491,108 | yet         |       101,707 |
    | **NEGany~exactly_cheap**          |    693 |    0.95 |    8.28 |  4,443.27 | 86,330,752 | 3,226,213 |    704 |     26.31 |      666.69 | NEGATED | exactly_cheap          | cheap      |        83,765 | exactly     |        61,599 |
    | **NEGany~that_uncommon**          |    804 |    0.94 |    8.39 |  5,136.91 | 86,330,752 | 3,226,213 |    819 |     30.61 |      773.39 | NEGATED | that_uncommon          | uncommon   |        61,767 | that        |       250,392 |
    | **NEGany~yet_eligible**           |    459 |    0.94 |    7.72 |  2,929.15 | 86,330,752 | 3,226,213 |    468 |     17.49 |      441.51 | NEGATED | yet_eligible           | eligible   |        49,578 | yet         |       101,707 |
    | **NEGany~yet_official**           |    353 |    0.94 |    7.33 |  2,236.98 | 86,330,752 | 3,226,213 |    362 |     13.53 |      339.47 | NEGATED | yet_official           | official   |         9,778 | yet         |       101,707 |
    | **NEGany~exactly_subtle**         |    264 |    0.94 |    6.92 |  1,671.02 | 86,330,752 | 3,226,213 |    271 |     10.13 |      253.87 | NEGATED | exactly_subtle         | subtle     |        56,845 | exactly     |        61,599 |
    | **NEGany~yet_ready**              |  7,611 |    0.93 |    9.23 | 48,012.06 | 86,330,752 | 3,226,213 |  7,838 |    292.91 |    7,318.09 | NEGATED | yet_ready              | ready      |       240,297 | yet         |       101,707 |
    | **NEGany~exactly_new**            |  1,378 |    0.93 |    8.54 |  8,697.93 | 86,330,752 | 3,226,213 |  1,418 |     52.99 |    1,325.01 | NEGATED | exactly_new            | new        |       321,311 | exactly     |        61,599 |
    | **NEGany~necessarily_indicative** |  1,406 |    0.93 |    8.37 |  8,811.69 | 86,330,752 | 3,226,213 |  1,456 |     54.41 |    1,351.59 | NEGATED | necessarily_indicative | indicative |        12,760 | necessarily |        56,694 |
    | **NEGany~exactly_easy**           |  1,069 |    0.93 |    8.37 |  6,747.64 | 86,330,752 | 3,226,213 |  1,100 |     41.11 |    1,027.89 | NEGATED | exactly_easy           | easy       |       771,307 | exactly     |        61,599 |
    | **NEGany~yet_certain**            |    874 |    0.93 |    8.12 |  5,491.41 | 86,330,752 | 3,226,213 |    903 |     33.75 |      840.25 | NEGATED | yet_certain            | certain    |       104,544 | yet         |       101,707 |
    | **NEGany~necessarily_surprising** |    343 |    0.93 |    7.22 |  2,150.86 | 86,330,752 | 3,226,213 |    355 |     13.27 |      329.73 | NEGATED | necessarily_surprising | surprising |       150,067 | necessarily |        56,694 |
    | **NEGany~exactly_sure**           |  8,860 |    0.92 |    8.63 | 54,750.58 | 86,330,752 | 3,226,213 |  9,301 |    347.58 |    8,512.42 | NEGATED | exactly_sure           | sure       |       844,981 | exactly     |        61,599 |
    | **NEGany~yet_complete**           |  2,220 |    0.92 |    8.42 | 13,815.98 | 86,330,752 | 3,226,213 |  2,314 |     86.48 |    2,133.52 | NEGATED | yet_complete           | complete   |       107,018 | yet         |       101,707 |
    | **NEGany~yet_sure**               |  1,990 |    0.92 |    8.37 | 12,379.79 | 86,330,752 | 3,226,213 |  2,075 |     77.54 |    1,912.46 | NEGATED | yet_sure               | sure       |       844,981 | yet         |       101,707 |
    | **NEGany~exactly_clear**          |  1,759 |    0.92 |    8.30 | 10,937.16 | 86,330,752 | 3,226,213 |  1,835 |     68.57 |    1,690.43 | NEGATED | exactly_clear          | clear      |       491,108 | exactly     |        61,599 |
    | **NEGany~that_surprising**        |  1,141 |    0.92 |    8.14 |  7,115.30 | 86,330,752 | 3,226,213 |  1,187 |     44.36 |    1,096.64 | NEGATED | that_surprising        | surprising |       150,067 | that        |       250,392 |
    | **NEGany~that_common**            |  1,216 |    0.92 |    8.12 |  7,564.08 | 86,330,752 | 3,226,213 |  1,268 |     47.39 |    1,168.61 | NEGATED | that_common            | common     |       556,435 | that        |       250,392 |
    | **NEGany~that_unusual**           |    983 |    0.92 |    7.94 |  6,096.13 | 86,330,752 | 3,226,213 |  1,028 |     38.42 |      944.58 | NEGATED | that_unusual           | unusual    |       108,584 | that        |       250,392 |
    



```python
if PRE_FILTERED_NEG_HITS.is_file(): 
    neg_hits_table = pd.read_pickle(PRE_FILTERED_NEG_HITS)
else:
    neg_hits_table = pd.read_pickle(NEG_HITS_PATH).filter(regex=r'^[nab].*lower|text|str|head')
    neg_hits_table = neg_hits_table.drop_duplicates(['text_window', 'bigram_lower', 'neg_form_lower'])
    word_cols = neg_hits_table.filter(regex=r'head|lower').columns
    neg_hits_table[word_cols] = neg_hits_table[word_cols].astype('category')
    neg_hits_table = neg_hits_table.loc[neg_hits_table.adv_form_lower.isin(adv_am.index), :]
# sourcery skip: use-fstring-for-concatenation
if 'all_forms_lower' not in neg_hits_table.columns: 
    neg_hits_table['all_forms_lower'] = (
        neg_hits_table.neg_form_lower.astype('string') 
        + '_' 
        + neg_hits_table.bigram_lower.astype('string')
        ).astype('category')
nb_show_table(neg_hits_table.sample(3).filter(like='lower'), adjust_columns=False)
```

    
    |                                           | `neg_form_lower`   | `adv_form_lower`   | `adj_form_lower`   | `bigram_lower`     | `all_forms_lower`      |
    |:------------------------------------------|:-------------------|:-------------------|:-------------------|:-------------------|:-----------------------|
    | **pcc_eng_17_101.5116_x1624646_42:6-8-9** | n't                | any                | easier             | any_easier         | n't_any_easier         |
    | **nyt_eng_19950213_0364_60:4-5-6**        | not                | terribly           | different          | terribly_different | not_terribly_different |
    | **nyt_eng_20100420_0065_13:15-16-17**     | n't                | terribly           | beastly            | terribly_beastly   | n't_terribly_beastly   |
    



```python
if not PRE_FILTERED_NEG_HITS.is_file():
    neg_hits_table.to_pickle(PRE_FILTERED_NEG_HITS)
```


```python
neg_hits_table.filter(like='lower').loc[neg_hits_table.adv_form_lower=='exactly',:]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>neg_form_lower</th>
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>bigram_lower</th>
      <th>all_forms_lower</th>
    </tr>
    <tr>
      <th>hit_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>pcc_eng_09_001.0244_x0000400_05:08-09-10</th>
      <td>n't</td>
      <td>exactly</td>
      <td>full</td>
      <td>exactly_full</td>
      <td>n't_exactly_full</td>
    </tr>
    <tr>
      <th>pcc_eng_09_001.2416_x0003918_19:5-6-7</th>
      <td>not</td>
      <td>exactly</td>
      <td>consistent</td>
      <td>exactly_consistent</td>
      <td>not_exactly_consistent</td>
    </tr>
    <tr>
      <th>pcc_eng_09_001.2755_x0004474_37:4-5-6</th>
      <td>not</td>
      <td>exactly</td>
      <td>celebratory</td>
      <td>exactly_celebratory</td>
      <td>not_exactly_celebratory</td>
    </tr>
    <tr>
      <th>pcc_eng_09_001.2765_x0004492_04:10-11-12</th>
      <td>n't</td>
      <td>exactly</td>
      <td>friendly</td>
      <td>exactly_friendly</td>
      <td>n't_exactly_friendly</td>
    </tr>
    <tr>
      <th>pcc_eng_09_001.3782_x0006136_05:4-5-6</th>
      <td>not</td>
      <td>exactly</td>
      <td>wrong</td>
      <td>exactly_wrong</td>
      <td>not_exactly_wrong</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>pcc_eng_05_108.06724_x1741920_18:39-40-41</th>
      <td>not</td>
      <td>exactly</td>
      <td>usable</td>
      <td>exactly_usable</td>
      <td>not_exactly_usable</td>
    </tr>
    <tr>
      <th>pcc_eng_05_108.07016_x1742413_22:13-15-16</th>
      <td>never</td>
      <td>exactly</td>
      <td>clear</td>
      <td>exactly_clear</td>
      <td>never_exactly_clear</td>
    </tr>
    <tr>
      <th>pcc_eng_05_108.07406_x1743020_22:5-6-7</th>
      <td>n't</td>
      <td>exactly</td>
      <td>prolific</td>
      <td>exactly_prolific</td>
      <td>n't_exactly_prolific</td>
    </tr>
    <tr>
      <th>pcc_eng_05_108.08248_x1744422_16:3-4-5</th>
      <td>n't</td>
      <td>exactly</td>
      <td>flawless</td>
      <td>exactly_flawless</td>
      <td>n't_exactly_flawless</td>
    </tr>
    <tr>
      <th>pcc_eng_05_108.08962_x1745617_58:4-5-6</th>
      <td>not</td>
      <td>exactly</td>
      <td>equal</td>
      <td>exactly_equal</td>
      <td>not_exactly_equal</td>
    </tr>
  </tbody>
</table>
<p>42058 rows × 5 columns</p>
</div>




```python
def embolden(series,
            bold_regex=None):
    bold_regex = bold_regex or r" (n[o']t) "
    return series.apply(
        lambda x: re.sub(bold_regex,
                        r' __`\1`__ ', x, flags=re.I))
```


```python
def collect_examples(amdf: pd.DataFrame,
                     hits_df: pd.DataFrame,
                     adv: str = 'exactly',
                     n_bigrams: int = BK,
                     n_examples: int = 50,
                     metric: str = 'LRC') -> dict:
    df = amdf.copy().filter(like=f'~{adv}_', axis=0).nlargest(n_bigrams, metric)
    examples = {}
    for i, bigram in enumerate(df['l2'].unique(), start=1):
        bigram_text = bigram.replace("_"," ")
        print(f'\n{i}. _{bigram_text}_')
        ex_for_bigram = sp(
            data=hits_df, print_sample=False,
            sample_size=n_examples,  sort_by='all_forms_lower',
            filters=[f'bigram_lower=={bigram}'],
            columns=['END::lower', 'text_window', 'token_str'])
        excerpt = embolden(ex_for_bigram.sample(min(len(ex_for_bigram), 5))['token_str'], f' ({bigram_text}) ').to_frame()
        excerpt.index = '`'+excerpt.index.astype('string')+'`'
        nb_show_table(excerpt)
        # print('\n   > ', [f'> {}' for i in ex_for_bigram.sample(3).index])
        examples[bigram] = ex_for_bigram
    return examples


def save_examples(adverb, bigram_am, neg_hits_table):
    output_dir = TOP_AM_DIR / 'neg_bigram_examples' / adverb
    table_csv_path = output_dir / f'{adverb}_{BK}mostNEG-bigrams_AMscores_{timestamp_today()}.csv'
    confirm_dir(output_dir)
    this_adv_amdf = bigram_am.filter(like=f'~{adverb}_', axis=0).sort_values('LRC', ascending=False)
    this_adv_amdf.to_csv(table_csv_path)
    
    nb_show_table(this_adv_amdf.filter(['N','f1','adv_total'])
                  .set_index(this_adv_amdf.l1 + f'_{adverb}').drop_duplicates(), 
                  n_dec=0, 
                  outpath=output_dir / f'{adverb}_MarginalFreqs_{timestamp_today()}.md')
    nb_show_table(this_adv_amdf.filter(regex=r'^([dLGeu]|f2?$|adj_total)'), n_dec=2, 
                  outpath=table_csv_path.with_suffix('.md'))
    examples = collect_examples(bigram_am, neg_hits_table,
                                adv=adverb, metric='LRC')

    print(f'\nSaving Samples in {output_dir}/...')

    paths = []
    for key, df in examples.items():
        out_path = output_dir.joinpath(f'{key}_50ex.csv')
        df.to_csv(out_path)
        paths.append(out_path)
    print_iter(paths, header='\nSamples saved as...', bullet='1.')
    

```


```python
for rank, adverb in enumerate(adv_am.index, start=1): 
    print(f'\n## {rank}. *{adverb}*')
    save_examples(adverb, bigram_am, neg_hits_table)
```

    
    ## 1. *exactly*
    
    |                     |        `N` |      `f1` |   `adv_total` |
    |:--------------------|-----------:|----------:|--------------:|
    | **NEGATED_exactly** | 86,330,752 | 3,226,213 |        61,599 |
    | **NEGMIR_exactly**  |  2,032,082 |   293,963 |         1,114 |
    
    
    |                               |   `f` |   `dP1` |   `LRC` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:------------------------------|------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~exactly_sure**       | 8,860 |    0.92 |    8.63 | 54,750.58 |  9,301 |    347.58 |    8,512.42 |       844,981 |
    | **NEGany~exactly_new**        | 1,378 |    0.93 |    8.54 |  8,697.93 |  1,418 |     52.99 |    1,325.01 |       321,311 |
    | **NEGany~exactly_easy**       | 1,069 |    0.93 |    8.37 |  6,747.64 |  1,100 |     41.11 |    1,027.89 |       771,307 |
    | **NEGany~exactly_clear**      | 1,759 |    0.92 |    8.30 | 10,937.16 |  1,835 |     68.57 |    1,690.43 |       491,108 |
    | **NEGany~exactly_cheap**      |   693 |    0.95 |    8.28 |  4,443.27 |    704 |     26.31 |      666.69 |        83,765 |
    | **NEGany~exactly_surprising** |   441 |    0.96 |    7.34 |  2,863.35 |    444 |     16.59 |      424.41 |       150,067 |
    | **NEGany~exactly_happy**      |   441 |    0.90 |    7.16 |  2,694.69 |    468 |     17.49 |      423.51 |       528,511 |
    | **NEGany~exactly_ideal**      |   418 |    0.90 |    7.08 |  2,546.29 |    445 |     16.63 |      401.37 |        42,701 |
    | **NEGany~exactly_subtle**     |   264 |    0.94 |    6.92 |  1,671.02 |    271 |     10.13 |      253.87 |        56,845 |
    | **NEGany~exactly_great**      |   308 |    0.90 |    6.82 |  1,875.62 |    328 |     12.26 |      295.74 |       380,889 |
    | **NEGmir~exactly_clear**      |    52 |    0.80 |    2.13 |    178.73 |     55 |      7.96 |       44.04 |         8,639 |
    | **NEGmir~exactly_sure**       |   148 |    0.85 |    2.09 |    560.65 |    149 |     21.55 |      126.45 |        11,297 |
    
    
    1. _exactly sure_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_sure`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                    |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_045.9136_x0726708_18:5-6-7`**    | Initially , they were n't __`exactly sure`__ what I would do or how I would do it .                                                                                                                                            |
    | **`pcc_eng_04_051.0966_x0809301_6:5-6-7`**     | Well , I am not __`exactly sure`__ I hit the nail on the head with this one , but I gave it my best effort .                                                                                                                   |
    | **`pcc_eng_25_096.3651_x1543269_24:29-30-31`** | Now what 's a bit puzzling about this is that I am linked to a lot more people in Boulder than just these ten , so I 'm not __`exactly sure`__ why other people are n't matching .                                             |
    | **`pcc_eng_29_007.5424_x0105818_30:11-16-17`** | Because the plans for Long Island are so preliminary , none of the participants is __`exactly sure`__ what they picture for its future , but are certain that whatever 's put in place , will be done to honor the Cherokees . |
    | **`pcc_eng_23_034.2012_x0536022_27:3-4-5`**    | I 'm not __`exactly sure`__ when I became aware of Reiki .                                                                                                                                                                     |
    
    
    2. _exactly new_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_new`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_108.4837_x1738650_150:4-5-6`**   | The arguments are no __`exactly new`__ , but , coming from The Economist they are sure to have an impact .                                                                                                                                                                                                 |
    | **`nyt_eng_19940826_0270_23:6-7-8`**           | now , dead parents are n't __`exactly new`__ in entertainment .                                                                                                                                                                                                                                            |
    | **`pcc_eng_12_004.7115_x0059778_30:19-20-21`** | Hero or traitor , he has given the nation much to consider , even if the questions are n't __`exactly new`__ .                                                                                                                                                                                             |
    | **`pcc_eng_02_075.7079_x1207991_5:49-50-51`**  | It would be nice if there was some kind of test to enable automated promotions from newbie to Jr. For example , I 've been reading these forums for quite a long time , but I did n't registered until I needed to post , so I 'm not __`exactly new`__ .                                                  |
    | **`pcc_eng_17_064.2291_x1021307_08:13-14-15`** | Ok , so Scarlett Johansson as Natasha Romanoff / Black Widow is n't __`exactly new`__ , we 've seen her reprise the role many a time in Marvel 's cinematic universe , but this time around , in Captain America : Civil War , Black Widow is taking her butt kicking and badassery to a whole new level . |
    
    
    3. _exactly easy_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_easy`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                  |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_098.1335_x1570370_16:14-15-16`** | Except that complying with SOX , as it 's sometimes known , is n't __`exactly easy`__ and ca n't be done without some degree of human intervention .                                                                         |
    | **`pcc_eng_10_054.0064_x0857267_5:13-14-15`**  | I have n't attempted circles yet and I 've heard they 're not __`exactly easy`__ .                                                                                                                                           |
    | **`pcc_eng_18_041.6305_x0657382_26:6-7-8`**    | I 'm sure it was n't __`exactly easy`__ to end a years - long relationship ( the couple had been together since they were about 14 ) , but they did what was personally best for them , and that 's what 's most important . |
    | **`pcc_eng_25_061.2550_x0976054_16:7-8-9`**    | Meeting the demands of customers is n't __`exactly easy`__ , and without a detailed and understandable overview of your inventory and supply , it can be difficult to project the ongoing needs of your business .           |
    | **`pcc_eng_02_071.6897_x1143297_20:08-09-10`** | The journey to the big leagues was n't __`exactly easy`__ for the Bethlehem native .                                                                                                                                         |
    
    
    4. _exactly clear_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_clear`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                      |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_031.9383_x0500313_055:36-37-38`** | So I was treated to a driving tour of much of Vegas thanks to an Uber driver who had a couple of pick ups to make in all four corners of the city and was n't __`exactly clear`__ on the best routes to get there .                                                                              |
    | **`pcc_eng_11_053.2994_x0846029_04:3-4-5`**     | Wilber is not __`exactly clear`__ on the topic himself .                                                                                                                                                                                                                                         |
    | **`nyt_eng_19981029_0102_4:5-6-7`**             | and though it 's not __`exactly clear`__ from the publicity what , exactly , director and studio are fighting about -LRB- other than Kaye 's vague claims that the studio cut is not the film he set out to make -RRB- my view of the movie tells me Kaye certainly has a reason to be unhappy . |
    | **`pcc_eng_06_045.5914_x0721388_04:12-13-14`**  | And how exactly Tim at Sera- Apps did the rooting is n't __`exactly clear`__ , but he did get a screen that shows he 's been granted superuser rights .                                                                                                                                          |
    | **`pcc_eng_00_007.3341_x0102220_03:21-22-23`**  | There are very few visual remains witnessing the Jewish presence in Slovenia in the early centuries , so it is not __`exactly clear`__ when the Jews settled within the Slovenian region .                                                                                                       |
    
    
    5. _exactly cheap_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_cheap`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19980420_1315_31:13-14-15`**        | by most standards , domestic air travel in Malaysia is affordable though not __`exactly cheap`__ .                                                                                                         |
    | **`pcc_eng_14_083.7593_x1337661_58:3-4-5`**    | Transistors were n't __`exactly cheap`__ , and certainly not readily - available , at the time this thing was built .                                                                                      |
    | **`pcc_eng_03_085.8111_x1373290_53:7-8-9`**    | This makes sense as it 's not __`exactly cheap`__ , and its almost unapologetically unhealthy .                                                                                                            |
    | **`pcc_eng_02_063.8676_x1016828_06:35-36-37`** | Rodriguez obviously has off the field issues that may scare some away , even the Yankees , and he is owed the remainder of his $ 11.5 million salary this season so he is n't __`exactly cheap`__ either . |
    | **`pcc_eng_12_019.9456_x0306566_12:10-11-12`** | At nine pounds a copy , the book was not __`exactly cheap`__ .                                                                                                                                             |
    
    
    6. _exactly surprising_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_surprising`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                       |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_003.6264_x0042369_48:5-6-7`**    | Eddie 's wife , not __`exactly surprising`__ given the brothers ' similar paths in life , is Deb .                                                                                                                                                                                                                |
    | **`pcc_eng_27_023.1877_x0358704_05:34-35-36`** | As five , they never really experienced much success compared to the other groups who debuted during their time , such as Beast and CN Blue , and while disappointing , it 's not __`exactly surprising`__ that the members have other plans beside renewing their contract and staying on as a member of MBLAQ . |
    | **`pcc_eng_29_081.5917_x1301819_20:3-7-8`**    | It is not , however , __`exactly surprising`__ .                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_13_001.7711_x0012369_14:3-4-5`**    | That 's not __`exactly surprising`__ , as Iran is on the cusp of reaping serious economic benefits if / when sanctions will be suspended .                                                                                                                                                                        |
    | **`pcc_eng_26_076.1137_x1214167_16:32-33-34`** | Mass means different things to different riders ; that the NYT Mag and others do n't really seem able to fathom a movement that is n't lobbying politicians for influence is n't __`exactly surprising`__ .                                                                                                       |
    
    
    7. _exactly happy_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_happy`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                             |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20051005_0211_34:16-17-18`**        | resolutions to challenges like this do n't come easily , and often , they 're not __`exactly happy`__ . |
    | **`pcc_eng_20_051.0249_x0808139_13:09-10-11`** | Those are love songs , but they are n't __`exactly happy`__ .                                           |
    | **`pcc_eng_10_034.2598_x0537890_036:3-4-5`**   | I was n't __`exactly happy`__ with the girls I was dating either .                                      |
    | **`pcc_eng_14_089.5874_x1431975_07:3-4-5`**    | Drake is not __`exactly happy`__ with his record label and he took to Twitter to express that .         |
    | **`pcc_eng_29_067.0731_x1067492_12:7-8-9`**    | The ending in the book is n't __`exactly happy`__ either                                                |
    
    
    8. _exactly ideal_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_ideal`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                     |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_095.2265_x1523766_30:08-09-10`** | But the conditions for these procedures were not __`exactly ideal`__ .                                                                                          |
    | **`pcc_eng_18_006.5801_x0090409_7:25-26-27`**  | The newly - announced Civilization Beyond Earth will be arriving on Linux , although the port is being handled Aspyr Media , which is not __`exactly ideal`__ . |
    | **`apw_eng_20011111_0255_23:5-6-7`**           | `` The conditions were n't __`exactly ideal`__ for a great game , '' Farina said .                                                                              |
    | **`nyt_eng_20060212_0219_28:1-2-3`**           | not __`exactly ideal`__ .                                                                                                                                       |
    | **`pcc_eng_05_037.9835_x0598919_04:08-09-10`** | For filmmaking , my current city is n't __`exactly ideal`__ .                                                                                                   |
    
    
    9. _exactly subtle_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_subtle`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                     |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_024.6585_x0382709_098:17-18-19`** | Adam 's next appearance will be in the season five finale , in which he is not __`exactly subtle`__ about the state of his brother 's soul .                                                                    |
    | **`pcc_eng_29_082.1890_x1311301_29:1-2-3`**     | Not __`exactly subtle`__ , but Kelly handles most of it with a light touch , which fails him only in depicting the uptight gym teacher ( Beth Grant ) .                                                         |
    | **`pcc_eng_02_051.8639_x0822874_31:3-4-5`**     | She 's not __`exactly subtle`__ , after all , when .                                                                                                                                                            |
    | **`pcc_eng_12_062.7056_x0997811_062:15-16-17`** | Doris 's ridiculously over- the- top : " Bye , mom " , was not __`exactly subtle`__ .                                                                                                                           |
    | **`pcc_eng_28_008.1741_x0115843_54:29-30-31`**  | You would n't think that philosophical fiction by Ayn Rand would be material to inspire a game 's world , but similarities to " Atlas Shrugged " are n't __`exactly subtle`__ in 2K 's cynical sci-fi shooter . |
    
    
    10. _exactly great_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==exactly_great`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                               |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20090416_0145_17:4-5-6`**           | `` Times are n't __`exactly great`__ as we speak , '' Michael J. Cavanagh , the bank 's finance chief , said in a brief interview .                                                       |
    | **`pcc_eng_00_042.5530_x0671410_20:13-14-15`** | The Little Ice Age shows us that huddling in the chill is n't __`exactly great`__ for our mood either , or for our collective sense of well - being .                                     |
    | **`pcc_eng_22_017.5344_x0266656_15:20-21-22`** | He finished the regular season with 2,119 yards , 17 touchdowns and four interceptions -- good numbers , but not __`exactly great`__ .                                                    |
    | **`pcc_eng_12_087.5610_x1398789_04:13-14-15`** | Also , the provisions usually run out and the living conditions are not __`exactly great`__ .                                                                                             |
    | **`pcc_eng_03_094.1906_x1508887_80:1-5-6`**    | Not that it was __`exactly great`__ the whole time , but it started off quite warm , I think about 6 degrees celsius , and damp , kind of what you might expect of Scotland in November . |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_sure_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_new_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_easy_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_clear_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_cheap_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_surprising_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_happy_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_ideal_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_subtle_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_great_50ex.csv
    
    ## 2. *necessarily*
    
    |                         |        `N` |      `f1` |   `adv_total` |
    |:------------------------|-----------:|----------:|--------------:|
    | **NEGATED_necessarily** | 86,330,752 | 3,226,213 |        56,694 |
    | **NEGMIR_necessarily**  |  2,032,082 |   293,963 |         1,681 |
    
    
    |                                       |   `f` |   `dP1` |   `LRC` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:--------------------------------------|------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~necessarily_indicative**     | 1,406 |    0.93 |    8.37 |  8,811.69 |  1,456 |     54.41 |    1,351.59 |        12,760 |
    | **NEGany~necessarily_representative** |   496 |    0.91 |    7.31 |  3,044.27 |    524 |     19.58 |      476.42 |        25,187 |
    | **NEGany~necessarily_easy**           |   914 |    0.88 |    7.26 |  5,448.34 |    996 |     37.22 |      876.78 |       771,307 |
    | **NEGany~necessarily_surprising**     |   343 |    0.93 |    7.22 |  2,150.86 |    355 |     13.27 |      329.73 |       150,067 |
    | **NEGany~necessarily_true**           | 3,238 |    0.82 |    6.89 | 18,199.76 |  3,786 |    141.48 |    3,096.52 |       348,994 |
    | **NEGany~necessarily_interested**     |   422 |    0.87 |    6.77 |  2,500.26 |    463 |     17.30 |      404.70 |       364,497 |
    | **NEGany~necessarily_related**        |   742 |    0.84 |    6.74 |  4,271.76 |    842 |     31.47 |      710.53 |       137,661 |
    | **NEGany~necessarily_illegal**        |   280 |    0.87 |    6.48 |  1,659.90 |    307 |     11.47 |      268.53 |        44,028 |
    | **NEGany~necessarily_new**            |   483 |    0.82 |    6.36 |  2,728.73 |    561 |     20.96 |      462.04 |       321,311 |
    | **NEGany~necessarily_available**      |   213 |    0.89 |    6.36 |  1,280.24 |    230 |      8.60 |      204.40 |       866,272 |
    | **NEGmir~necessarily_wrong**          |   213 |    0.77 |    4.19 |    693.55 |    233 |     33.71 |      179.29 |        24,007 |
    | **NEGmir~necessarily_true**           |    53 |    0.49 |    1.64 |    105.71 |     83 |     12.01 |       40.99 |         8,402 |
    | **NEGmir~necessarily_bad**            |    50 |    0.47 |    1.48 |     93.65 |     82 |     11.86 |       38.14 |        12,841 |
    
    
    1. _necessarily indicative_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_indicative`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_13_057.0880_x0906423_19:23-24-25`** | For that reason , we must remember that to drive or carry technology which places one in a position of power is not __`necessarily indicative`__ of a violent disposition .                                                            |
    | **`pcc_eng_18_033.0315_x0518508_52:29-30-31`** | Investors should take cognisance of the fact that there are risks involved in buying or selling any financial product and that past performance of a financial product is not __`necessarily indicative`__ of its future performance . |
    | **`pcc_eng_27_067.7679_x1079363_18:4-5-6`**    | Past results are not __`necessarily indicative`__ of futures results .                                                                                                                                                                 |
    | **`pcc_eng_06_005.4857_x0072631_047:7-8-9`**   | Where a person was born is not __`necessarily indicative`__ of where they will live , such as Robert Griffin III being born in Okinawa , Japan .                                                                                       |
    | **`pcc_eng_17_062.4610_x0992784_04:6-7-8`**    | Historic loan default rates are not __`necessarily indicative`__ of future default rates .                                                                                                                                             |
    
    
    2. _necessarily representative_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_representative`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                          |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_010.0565_x0146891_085:35-36-37`** | The ACLU , which has campaigned to close Guantanamo since the first terrorism suspects arrived in January 2002 , distributed the letter signed by 31 different relatives saying the views expressed Monday were " not __`necessarily representative`__ of all victims ' families . " |
    | **`pcc_eng_05_083.7342_x1338981_30:27-28-29`**  | The views and opinions expressed by the SOI Industry Consortium through officers in the SOI Industry Consortium or in this presentation or other communication vehicles are not __`necessarily representative`__ of the views and opinions of individual members .                   |
    | **`pcc_eng_23_046.5173_x0735515_44:33-34-35`**  | But , in Heath 's defense , he seems to spend a lot of time around philosophers , economists and business school types , which are often more classically liberal , and not __`necessarily representative`__ of where elite opinion is overall .                                     |
    | **`pcc_eng_13_004.1910_x0051457_12:10-11-12`**  | Any opinion expressed by one of our volunteers is not __`necessarily representative`__ of the policies or practices of the society as a whole .                                                                                                                                      |
    | **`pcc_eng_test_3.04763_x42109_08:42-43-44`**   | What I earn is merely enough to cover food and transport expenses in London over a week , but I value the experience for the insight it may provide into the lives and realities of many around the country , and not __`necessarily representative`__ of my own .                   |
    
    
    3. _necessarily easy_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_easy`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                      |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_058.5952_x0931314_15:3-4-5`**    | This is not __`necessarily easy`__ for my introverted self , but I believe it is critically important for the future of our society and communities for inclusion to become part of the fabric of our everyday life and personal relationships . |
    | **`pcc_eng_14_058.4600_x0928793_38:09-10-11`** | His other goal in a demanding marathon is n't __`necessarily easy`__ .                                                                                                                                                                           |
    | **`pcc_eng_08_040.0451_x0632027_06:11-12-13`** | She was all about daring to make choices that are not __`necessarily easy`__ .                                                                                                                                                                   |
    | **`pcc_eng_23_061.2161_x0972861_15:11-12-13`** | Despite all this , the boundary between the two is not __`necessarily easy`__ to trace , because multiple factors tend to blur together .                                                                                                        |
    | **`pcc_eng_26_027.6884_x0431372_38:10-11-12`** | While this is a simple requirement , it is not __`necessarily easy`__ .                                                                                                                                                                          |
    
    
    4. _necessarily surprising_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_surprising`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                         |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19990522_0150_44:17-18-19`**        | seen in this way , sports becomes a very serious business indeed _ and it is not __`necessarily surprising`__ , if no less alarming , that one 's failure to live up to the sports ideal can generate tremendous frustration and insecurity . ''    |
    | **`nyt_eng_20020315_0359_28:09-10-11`**        | the fact that Miramax is cutting back is not __`necessarily surprising`__ .                                                                                                                                                                         |
    | **`pcc_eng_07_061.2760_x0974345_05:5-6-7`**    | While the news was not __`necessarily surprising`__ , it still comes as a major blow for Sunderland head coach Paolo Di Canio , who is already operating without the services of 11 - goal Fletcher .                                               |
    | **`pcc_eng_11_001.3997_x0006423_15:09-10-11`** | " While the younger age at hospitalization was not __`necessarily surprising`__ , the magnitude of the difference was indeed surprising , " Ickovics said .                                                                                         |
    | **`pcc_eng_02_096.3349_x1541473_07:3-4-5`**    | This is not __`necessarily surprising`__ , as the character factors into the original Ragnarok storyline and certain imagery from Ragnarok 's trailer ( such as Thor surrounded by pools of fire ) lines up with the possibility of him appearing . |
    
    
    5. _necessarily true_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_true`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                              |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_069.0611_x1101530_059:4-8-9`**   | Turns out that neither of them are __`necessarily true`__ .                                                              |
    | **`pcc_eng_26_004.7679_x0060699_24:19-20-21`** | One mistake that most people make is to assume that weight loss equals fat loss and that 's not __`necessarily true`__ . |
    | **`pcc_eng_25_028.9308_x0451989_11:09-10-11`** | The myth " firmer is better " is not necessarily true                                                                    |
    | **`pcc_eng_08_104.8171_x1681020_11:5-6-7`**    | However , it is not __`necessarily true`__ that a root can be given by a continuous single - valued function .           |
    | **`pcc_eng_16_082.7613_x1323428_04:16-17-18`** | They have a reputation as being the great killers of the ocean but this is not __`necessarily true`__ .                  |
    
    
    6. _necessarily interested_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_interested`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_096.0361_x1538769_19:08-09-10`** | That 's Oliver , and he was n't __`necessarily interested`__ in photos .                                                                                                                                                      |
    | **`pcc_eng_16_021.3826_x0330067_4:4-5-6`**     | If you were n't __`necessarily interested`__ in the beeronomics of just the                                                                                                                                                   |
    | **`pcc_eng_19_080.7516_x1288564_169:3-4-5`**   | We are not __`necessarily interested`__ in stories that lift up the Bible as the true Word of God , a necessary and inspired holy book , or the Truth .                                                                       |
    | **`pcc_eng_22_047.9469_x0758626_15:21-22-23`** | Even if some particular AI were to pass the Turing test , it would n't necessarily be extraordinarily intelligent , nor __`necessarily interested`__ in becoming so , nor necessarily have a clue how to design one that is . |
    | **`nyt_eng_19940711_0177_36:14-15-16`**        | they 're for a woman with a good deal of confidence who 's not __`necessarily interested`__ in the latest , hottest , newest , but goes for timeless fashion . ''                                                             |
    
    
    7. _necessarily related_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_related`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                               |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_071.9168_x1146420_36:7-8-9`**     | While certainly price and quality are not __`necessarily related`__ , Mr. Goldstein shows a common ignorance of Economics in his argument for pricing wines based on the cost of production .                                                                             |
    | **`pcc_eng_26_058.8985_x0936232_35:15-16-17`**  | The result is artificial variations in backscatter intensity caused by the bathymetry that are not __`necessarily related`__ to differences in seabed materials .                                                                                                         |
    | **`pcc_eng_14_016.4135_x0248962_14:2-6-7`**     | " Not that those were __`necessarily related`__ to spreading disinformation or to spreading information about the election , but they were fake accounts and we are using those technical tools to reduce the chance that they might be used to spread disinformation . " |
    | **`pcc_eng_05_100.9476_x1616738_27:28-29-30`**  | I do not mean the same errors , but only that the first lines of the output is the same , though I suspecct that it is not __`necessarily related`__ .                                                                                                                    |
    | **`pcc_eng_08_050.4941_x0801248_095:30-31-32`** | A couple years ago , a friend and mentor , the director of Track & Field at Boise State Corey Ihmels asked me a similar type of question , not __`necessarily related`__ to the Drake Relays , but saying , " Hey , what are you going to do ?                            |
    
    
    8. _necessarily illegal_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_illegal`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_066.9190_x1066362_05:26-27-28`** | For example , in order to prove liability ( and not just that the company misinformed the public , which under most circumstances , is not __`necessarily illegal`__ ) , you have to prove that the specific emissions from a specific company caused a specific detrimental outcome .        |
    | **`nyt_eng_19981203_0359_11:08-09-10`**        | `` What is illegal in Zimbabwe is not __`necessarily illegal`__ in South Africa . ''                                                                                                                                                                                                          |
    | **`apw_eng_20060826_0037_13:4-5-6`**           | the practice is n't __`necessarily illegal`__ , but most funds have policies forbidding it because heavy fund-share trading typically dilutes the profits of longer-term shareholders in the fund .                                                                                           |
    | **`apw_eng_20070425_0881_44:19-20-21`**        | the practice , which was commonly used across Silicon Valley as a retainment or recruiting tool , is not __`necessarily illegal`__ in itself but could create legal problems if it is not properly disclosed , leading potentially to inflated corporate profits and underpayments in taxes . |
    | **`pcc_eng_29_041.5113_x0654269_40:08-09-10`** | While at face value some items are not __`necessarily illegal`__ , Schlaf said , the manner in which they are used may constitute grounds for confiscation .                                                                                                                                  |
    
    
    9. _necessarily new_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_new`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_077.0110_x1228313_099:6-7-8`**   | Of course this perspective is not __`necessarily new`__ .                                                                                                                                                                                                 |
    | **`pcc_eng_01_097.5459_x1560810_40:12-13-14`** | From the perspective of the federal government action , there 's nothing __`necessarily new`__ going on here .                                                                                                                                            |
    | **`pcc_eng_18_035.5918_x0559995_05:21-22-23`** | While some critics are claiming that the actress is being pretentious , experts say the concept of conscious uncoupling is n't __`necessarily new`__ .                                                                                                    |
    | **`pcc_eng_24_030.5837_x0478409_17:08-09-10`** | This means that we are faced with not __`necessarily new`__ challenges , but varying degrees , speeds , and shifts of existing social processes connected to different political , economic , and cultural systems ( ibid . ) .                           |
    | **`pcc_eng_28_071.2936_x1137302_14:31-32-33`** | The Q&A article in this issue , from James Ferrell Jr on cooperativity 4 , belongs to the category of Q&A articles that we have commissioned on concepts that are not __`necessarily new`__ or even topical , but may be a source of confusion for many . |
    
    
    10. _necessarily available_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==necessarily_available`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_092.5940_x1481436_09:6-7-8`**     | Reminder : products mentioned are not __`necessarily available`__ for purchase -- some were show demos , others remain in development or in beta testing . |
    | **`pcc_eng_04_078.0088_x1243976_18:08-09-10`**  | Cooking for two opens doors that are n't __`necessarily available`__ when cooking for larger crowds with more limiting tastes .                            |
    | **`pcc_eng_11_044.4325_x0702866_060:21-22-23`** | It 's also opened up big opportunities for us : sometimes , the people you want on your team are n't __`necessarily available`__ for a full-time gig .     |
    | **`pcc_eng_26_070.8662_x1129456_33:6-7-8`**     | 2 . Public transportation is n't __`necessarily available`__ for everyone .                                                                                |
    | **`pcc_eng_05_052.0769_x0826622_43:7-8-9`**     | Note : All diagnostic methods are not __`necessarily available`__ in all countries .                                                                       |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_indicative_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_representative_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_easy_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_surprising_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_true_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_interested_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_related_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_illegal_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_new_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_available_50ex.csv
    
    ## 3. *before*
    
    |                   |       `N` |    `f1` |   `adv_total` |
    |:------------------|----------:|--------:|--------------:|
    | **NEGMIR_before** | 2,032,082 | 293,963 |           294 |
    
    
    |                             |   `f` |   `dP1` |   `LRC` |   `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:----------------------------|------:|--------:|--------:|-------:|-------:|----------:|------------:|--------------:|
    | **NEGmir~before_available** |   177 |    0.84 |    3.99 | 654.92 |    180 |     26.04 |      150.96 |        14,919 |
    
    
    1. _before available_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==before_available`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                         |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_075.9533_x1211785_003:12-13-14`** | Everytime consumer behavior evolves , marketers have new opportunities that were never __`before available`__ .                                                                                                                     |
    | **`pcc_eng_22_072.1338_x1149691_03:21-22-23`**  | " More importantly , " they wrote , " West Valley residents now have access to a level of care never __`before available`__ in the region , particularly heart care , medical imaging services , surgical care and pediatric care . |
    | **`pcc_eng_17_028.7729_x0449419_3:30-31-32`**   | The Definitive Collection : 1947 - 1966 marks the 60th anniversary of Ralph and Carter Stanley 's first recordings together and includes three previously unreleased tracks and two songs never __`before available`__ on a CD .    |
    | **`pcc_eng_05_077.3955_x1236504_16:08-09-10`**  | This includes a great deal of music never __`before available`__ in any format .                                                                                                                                                    |
    | **`pcc_eng_06_048.8545_x0774260_25:24-25-26`**  | This collection , curated by Palais Schaumburg founder Holger Hiller , includes tracks from two Populare Mechanik cassettes from the early 1980s , never __`before available`__ on CD or vinyl .                                    |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/before/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/before/before_available_50ex.csv
    
    ## 4. *that*
    
    |                  |        `N` |      `f1` |   `adv_total` |
    |:-----------------|-----------:|----------:|--------------:|
    | **NEGATED_that** | 86,330,752 | 3,226,213 |       250,392 |
    | **NEGMIR_that**  |  2,032,082 |   293,963 |         7,472 |
    
    
    |                             |   `f` |   `dP1` |   `LRC` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:----------------------------|------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~that_uncommon**    |   804 |    0.94 |    8.39 |  5,136.91 |    819 |     30.61 |      773.39 |        61,767 |
    | **NEGany~that_surprising**  | 1,141 |    0.92 |    8.14 |  7,115.30 |  1,187 |     44.36 |    1,096.64 |       150,067 |
    | **NEGany~that_common**      | 1,216 |    0.92 |    8.12 |  7,564.08 |  1,268 |     47.39 |    1,168.61 |       556,435 |
    | **NEGany~that_hard**        | 9,966 |    0.88 |    7.96 | 59,642.82 | 10,818 |    404.27 |    9,561.73 |       430,990 |
    | **NEGany~that_complicated** | 1,208 |    0.91 |    7.95 |  7,450.89 |  1,270 |     47.46 |    1,160.54 |       180,071 |
    | **NEGany~that_unusual**     |   983 |    0.92 |    7.94 |  6,096.13 |  1,028 |     38.42 |      944.58 |       108,584 |
    | **NEGany~that_impressed**   |   684 |    0.91 |    7.57 |  4,207.58 |    721 |     26.94 |      657.06 |       113,281 |
    | **NEGany~that_exciting**    |   805 |    0.90 |    7.48 |  4,892.83 |    859 |     32.10 |      772.90 |       236,396 |
    | **NEGany~that_expensive**   | 1,800 |    0.87 |    7.32 | 10,585.14 |  1,992 |     74.44 |    1,725.56 |       444,946 |
    | **NEGany~that_interested**  | 2,435 |    0.86 |    7.27 | 14,187.96 |  2,724 |    101.80 |    2,333.20 |       364,497 |
    | **NEGmir~that_simple**      |   478 |    0.74 |    4.48 |  1,483.32 |    540 |     78.12 |      399.88 |        27,835 |
    | **NEGmir~that_easy**        |   458 |    0.68 |    3.91 |  1,278.04 |    558 |     80.72 |      377.28 |        21,775 |
    | **NEGmir~that_big**         |   113 |    0.66 |    2.99 |    308.12 |    140 |     20.25 |       92.75 |         9,564 |
    | **NEGmir~that_good**        |   449 |    0.47 |    2.65 |    848.28 |    732 |    105.89 |      343.11 |        38,252 |
    | **NEGmir~that_close**       |    60 |    0.71 |    2.53 |    177.72 |     70 |     10.13 |       49.87 |        15,958 |
    | **NEGmir~that_interested**  |    62 |    0.67 |    2.45 |    171.51 |     76 |     10.99 |       51.01 |        10,913 |
    | **NEGmir~that_popular**     |    65 |    0.63 |    2.34 |    167.47 |     84 |     12.15 |       52.85 |         6,409 |
    | **NEGmir~that_hard**        |    59 |    0.63 |    2.25 |    152.67 |     76 |     10.99 |       48.01 |         8,168 |
    | **NEGmir~that_serious**     |    50 |    0.59 |    1.93 |    120.37 |     68 |      9.84 |       40.16 |        10,801 |
    | **NEGmir~that_great**       |   288 |    0.36 |    1.93 |    406.36 |    575 |     83.18 |      204.82 |         6,821 |
    
    
    1. _that uncommon_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_uncommon`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_108.03669_x1737463_52:16-17-18`** | I get so sad whenever I drop a bit of matcha ... which sadly is n't __`that uncommon`__ , it 's always drifting off the edge of my spoon . |
    | **`pcc_eng_16_065.5278_x1044456_08:19-20-21`**  | However , in spite of these benefits , the absence of a recognized coaching culture is surprisingly , not __`that uncommon`__ .            |
    | **`pcc_eng_03_022.0557_x0340574_05:07-09-10`**  | Calls from ships in distress are not all __`that uncommon`__ in the outermost spirals of the Milky Way .                                   |
    | **`pcc_eng_14_049.8034_x0788647_3:18-19-20`**   | Spraying your pillow with your man's cologne or sleeping in his T-shirt because it smells delicious is n't __`that uncommon`__ .           |
    | **`pcc_eng_05_004.0777_x0050006_74:4-6-7`**     | This one was n't actually __`that uncommon`__ at all .                                                                                     |
    
    
    2. _that surprising_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_surprising`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                           |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_016.1552_x0244725_14:25-26-27`** | So , when Hollywood decided to move forward with two Fifty Shades sequels -- Fifty Shades Darker and Fifty Shades Freed -- it was n't __`that surprising`__ either .                                                                                                  |
    | **`pcc_eng_20_089.0219_x1422017_49:20-21-22`** | The simple fact is that little is done even when the USDA is on the case , which is not __`that surprising`__ for an agency with a well - greased revolving door between itself and the businesses it regulates .                                                     |
    | **`nyt_eng_19981113_0497_22:5-7-8`**           | that Rose survives is n't all __`that surprising`__ .                                                                                                                                                                                                                 |
    | **`pcc_eng_20_034.6392_x0543869_12:5-6-7`**    | " These findings are n't __`that surprising`__ , " said Society CEO Clyde " Bud " Chumbley , MD , MBA .                                                                                                                                                               |
    | **`pcc_eng_20_032.6395_x0511609_02:18-19-20`** | Ending not with a bang , but not exactly a whimper either , breakup last month was n't __`that surprising`__ , as the band had seemed to be on autopilot in recent years , but it nevertheless marked the end of one of the most remarkable careers in rock history . |
    
    
    3. _that common_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_common`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_093.1210_x1490444_44:5-6-7`**     | Wood shake roofs were not __`that common`__ in Phoenix from the 1950s to the 1970s .                                                                                                                                                                       |
    | **`pcc_eng_14_005.6524_x0075388_3:10-11-12`**   | Use your common sense ( even though it is n't __`that common`__ anymore ) .                                                                                                                                                                                |
    | **`pcc_eng_10_107.07413_x1725982_13:36-37-38`** | In a sign of Hollywood 's possible future , the festival 's co-director Cameron Bailey backed that up speaking to a packed premiere audience about China 's part in the movie , " It 's not __`that common`__ yet but this is the future of filmmaking . " |
    | **`pcc_eng_14_085.9674_x1373425_7:07-09-10`**   | But custom portable retro consoles are n't all __`that common`__ , and they are awesome ( there 's no denying that ) , and so what 's a gamer to do ?                                                                                                      |
    | **`pcc_eng_06_036.6020_x0575677_049:7-8-9`**    | 4 . ) Short sales are not __`that common`__ .                                                                                                                                                                                                              |
    
    
    4. _that hard_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_hard`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                    |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_005.0083_x0064655_2:17-18-19`**  | The thing is if you really want to quit after the first 3 days it 's not __`that hard`__ .                                                     |
    | **`pcc_eng_23_051.6032_x0817427_17:13-14-15`** | Nayari Castillo of Venezuela has some tales that are on the surface not __`that hard`__ to navigate , as she has long text accompanying them . |
    | **`pcc_eng_20_088.7180_x1417126_4:10-11-12`**  | Of course when I finally did it it was n't __`that hard`__ , but damnit , only if I figured that you had to knock down the barrel .            |
    | **`pcc_eng_09_013.8935_x0208897_10:4-5-6`**    | It 's really not __`that hard`__ to imagine what could have happend .                                                                          |
    | **`pcc_eng_14_063.6464_x1012492_09:13-14-15`** | When you go into a film expecting a twist it 's usually not __`that hard`__ to spot it fairly early on .                                       |
    
    
    5. _that complicated_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_complicated`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_033.4805_x0525381_04:15-16-17`** | There was a time when one could repair an electrical appliance because they were not __`that complicated`__ .                                                                                                               |
    | **`pcc_eng_00_092.9950_x1487520_10:4-5-6`**    | These principles are not __`that complicated`__ , especially if you have enough time to comprehend and practice them .                                                                                                      |
    | **`pcc_eng_23_007.9163_x0111709_66:08-09-10`** | Then again , the story itself is not __`that complicated`__ -- but it 's a very good story , really bleak like you said but with beautiful moments throughout .                                                             |
    | **`pcc_eng_08_011.4964_x0169741_3:5-6-7`**     | Sure , it 's not __`that complicated`__ , but I like to make sure I 'm not blasting a ton of hot water only to blast a ton of cold water to make the temperature bearable .                                                 |
    | **`pcc_eng_22_069.9489_x1114345_07:17-18-19`** | " If we are unable to accomplish something that we think is as important and really not __`that complicated`__ in a reasonable period of time then I think we should sit down and decide how we go forward , " Slive said . |
    
    
    6. _that unusual_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_unusual`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                               |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_087.5686_x1399362_33:11-12-13`**  | A 5 % fed funds rate , remember , is not __`that unusual`__ in the historical context .                                                                                                                                   |
    | **`nyt_eng_19990427_0218_22:23-25-26`**         | Sade 's biographers agree that the Sade of real life may have been sexually adventurous and perverse but that his behavior was not all __`that unusual`__ by the standards of the 18th-century French aristocracy .       |
    | **`pcc_eng_08_105.8326_x1697430_067:09-10-11`** | First , the process we are witnessing is not __`that unusual`__ for complex political negotiations - they take time , and in the beginning both sides typically weigh up their options and their opponents first .        |
    | **`pcc_eng_10_007.5594_x0105865_014:08-09-10`** | While the number of new items is n't __`that unusual`__ in historical terms , retailers saw 45 more comics and 110 more new graphic novels over the last three months than they got in the corresponding months of 2016 . |
    | **`pcc_eng_16_104.5722_x1676432_13:20-21-22`**  | I highly recommend this - it is great quality but the combos are n't for me as they are not __`that unusual`__ .                                                                                                          |
    
    
    7. _that impressed_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_impressed`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                          |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20081121_0103_8:3-5-6`**             | they are n't all __`that impressed`__ with the way their former company is run , or the rest of the industry for that matter , and even though bankruptcy could hurt their pensions , they 're not sure that is n't the best thing in the long run . |
    | **`pcc_eng_20_011.7971_x0174116_038:5-6-7`**    | Frankly , I was n't __`that impressed`__ with the toys in it this year .                                                                                                                                                                             |
    | **`pcc_eng_20_093.7959_x1499115_080:14-15-16`** | Some NBA scouts were convinced he was a sleeper , while others were n't __`that impressed`__ .                                                                                                                                                       |
    | **`pcc_eng_05_022.0051_x0340318_6:3-4-5`**      | Hubby was n't __`that impressed`__ though - said " why not just bake a potato ? "                                                                                                                                                                    |
    | **`pcc_eng_10_018.9425_x0289982_26:6-7-8`**     | At first , I was n't __`that impressed`__ with " The Seventh Sacrament " : it read like a decent but not extraordinary novel .                                                                                                                       |
    
    
    8. _that exciting_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_exciting`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                         |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_048.8855_x0775069_03:21-22-23`** | This FOTD was done super quick ( we 're talking 5 minutes ... maybe 10 ) so it 's really not __`that exciting`__ ...                                                                                                                                                                |
    | **`pcc_eng_21_061.8460_x0983558_15:6-8-9`**    | Oatmeal box pinhole cameras were n't all __`that exciting`__ , so I had an old camera my Grandfather brought back from WWII and asked the teacher if I could use it for class .                                                                                                     |
    | **`nyt_eng_20070609_0105_23:31-32-33`**        | `` I think maybe there 's a little smirk on the coach 's face , '' Barry said , `` and on the organization 's face , that it 's not __`that exciting`__ to people outside of San Antonio , that we 're doing it quietly , something special , right here , and we get to enjoy it . |
    | **`pcc_eng_28_015.8718_x0240761_28:08-10-11`** | " To be honest , it 's not been __`that exciting`__ so far .                                                                                                                                                                                                                        |
    | **`pcc_eng_28_083.0095_x1326585_117:4-5-6`**   | It really is n't __`that exciting`__ .                                                                                                                                                                                                                                              |
    
    
    9. _that expensive_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_expensive`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                               |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_092.9188_x1486643_10:26-28-29`** | Fast boats are the only best choice to avoid a long day trip from Bali to Lombok , the fast boat ticket to Lombok are not at __`that expensive`__ as you have found in some ways you have searched , here |
    | **`pcc_eng_15_079.5067_x1268562_16:7-8-9`**    | 3 ) Expenses : Malaysia is not __`that expensive`__ as it is perceived to be .                                                                                                                            |
    | **`pcc_eng_24_094.6717_x1514992_18:08-09-10`** | You have to consider that it is not __`that expensive`__ to obtain the records .                                                                                                                          |
    | **`pcc_eng_12_026.9786_x0420388_37:10-11-12`** | Oh and before you start , the supplies are n't __`that expensive`__ at all .                                                                                                                              |
    | **`pcc_eng_05_046.5450_x0737167_2:5-6-7`**     | The parts usually are n't __`that expensive`__ .                                                                                                                                                          |
    
    
    10. _that interested_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==that_interested`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                     |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19981214_0293_2:22-23-24`**          | Leaning in the open doorway of his videotape rental store in downtown Jerusalem , Azriel Danieli shrugged , `` I 'm not __`that interested`__ . ''                                                                              |
    | **`pcc_eng_05_103.8274_x1663229_28:11-12-13`**  | Proof he was nice , and also proof he was n't __`that interested`__ in intellectual stuff .                                                                                                                                     |
    | **`pcc_eng_23_061.7631_x0981841_2:11-12-13`**   | She 's hot as hell but her husband still is n't __`that interested`__ , so this blonde wife with big titties fucks another man and we 're invited to watch .                                                                    |
    | **`pcc_eng_17_014.2065_x0213577_149:17-18-19`** | Zellner has become difficult for the Redskins coaches to reach and the feeling is he is n't __`that interested`__ in cashing Snyder-bucks .                                                                                     |
    | **`pcc_eng_06_107.8065_x1727702_67:20-21-22`**  | You may also find that a teen is not that fazed by a break - up because they were n't __`that interested`__ in the relationship , they were the one who ended it and they feel good about that , or a myriad of other reasons . |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_uncommon_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_surprising_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_common_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_hard_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_complicated_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_unusual_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_impressed_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_exciting_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_expensive_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_interested_50ex.csv
    
    ## 5. *remotely*
    
    |                      |        `N` |      `f1` |   `adv_total` |
    |:---------------------|-----------:|----------:|--------------:|
    | **NEGATED_remotely** | 86,330,752 | 3,226,213 |        22,194 |
    | **NEGMIR_remotely**  |  2,032,082 |   293,963 |         2,717 |
    
    
    |                                 |   `f` |   `dP1` |   `LRC` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:--------------------------------|------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~remotely_true**        |   250 |    0.56 |    4.46 | 1,089.49 |    420 |     15.70 |      234.30 |       348,994 |
    | **NEGmir~remotely_close**       |   219 |    0.59 |    3.02 |   524.61 |    299 |     43.25 |      175.75 |        15,958 |
    | **NEGany~remotely_close**       |   696 |    0.23 |    2.92 | 1,722.76 |  2,558 |     95.59 |      600.41 |       480,288 |
    | **NEGany~remotely_interested**  |   333 |    0.23 |    2.72 |   808.74 |  1,252 |     46.79 |      286.21 |       364,497 |
    | **NEGmir~remotely_true**        |    61 |    0.73 |    2.59 |   184.98 |     70 |     10.13 |       50.87 |         8,402 |
    | **NEGmir~remotely_similar**     |    71 |    0.43 |    1.62 |   123.23 |    123 |     17.79 |       53.21 |         7,887 |
    | **NEGmir~remotely_interesting** |    57 |    0.45 |    1.52 |   102.91 |     96 |     13.89 |       43.11 |        14,240 |
    
    
    1. _remotely true_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==remotely_true`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                              |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_042.4610_x0670020_18:4-5-6`**     | ( That 's not __`remotely true`__ . )                                                                                                                                    |
    | **`pcc_eng_06_042.1771_x0666034_15:6-7-8`**     | Clearly , that 's also not __`remotely true`__ .                                                                                                                         |
    | **`pcc_eng_02_088.3626_x1412471_029:06-11-12`** | Even in Star Trek , none of the above is __`remotely true`__ .                                                                                                           |
    | **`pcc_eng_19_065.3149_x1038393_37:7-8-9`**     | Again , even though that 's not __`remotely true`__ .                                                                                                                    |
    | **`pcc_eng_19_065.3149_x1038393_07:30-31-32`**  | I spend more time trying to convince them that facts are , you know , facts while they inundate me with a long list of talking points that are n't __`remotely true`__ . |
    
    
    2. _remotely close_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==remotely_close`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_040.2916_x0635554_05:41-43-44`** | But Brian Encino of Baldwin , NY , does n't have an opinion one way or the other on whether or not the abuse happened as Dylan described it , or whether Allen is telling the truth when he says nothing even __`remotely close`__ to what she describes in her letter ever happened . |
    | **`pcc_eng_11_018.6892_x0286106_050:5-6-7`**   | The terrorist threat is n't __`remotely close`__ to the kind of threat America faced during the Cold War , Flynn added : " These [ terrorist attacks ] are really horrible when they happen .                                                                                          |
    | **`pcc_eng_13_079.3166_x1265797_61:29-31-32`** | So I really have to wonder about a tank that 's willing to take the risk with a group in Heroics and be at 405 defense possibly and not even __`remotely close`__ to being uncrittable .                                                                                               |
    | **`pcc_eng_27_089.8627_x1437334_16:7-8-9`**    | If nothing else , it 's not __`remotely close`__ to Wooten .                                                                                                                                                                                                                           |
    | **`pcc_eng_09_013.3232_x0199629_38:3-5-6`**    | She 's not even __`remotely close`__ to Chariot 's level , and she no longer has the Shiny Rod to aid her in times of need .                                                                                                                                                           |
    
    
    3. _remotely interested_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==remotely_interested`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_063.6215_x1013312_44:41-42-43`** | When I get an email from someone who is actually interested in Online Honesty , I 'm pretty excited , and I make it my # 1 priority to solve whatever problem this person has , even if they 're not __`remotely interested`__ in buying anything from me . |
    | **`pcc_eng_03_025.7575_x0400784_11:1-2-3`**    | Not __`remotely interested`__ in who won Sports personality as I do n't care but I expect they had all the candidates lined up for a possible presentation wherever they were .                                                                             |
    | **`pcc_eng_06_070.0544_x1117320_1:11-15-16`**  | I will admit when I first saw these I was not at all even __`remotely interested`__ .                                                                                                                                                                       |
    | **`pcc_eng_24_090.2563_x1443555_03:25-26-27`** | They are not as easy to track down in the UK , but then the converse is true of Seville oranges - Italians are n't __`remotely interested`__ in them .                                                                                                      |
    | **`pcc_eng_12_020.5934_x0317075_23:1-2-3`**    | Not __`remotely interested`__ in cooking , Just Feed                                                                                                                                                                                                        |
    
    
    4. _remotely similar_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==remotely_similar`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                           |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_002.8203_x0029425_148:24-26-27`** | Unlike Hillary , who actually took active steps to silence her husband 's accusers of sexual assault and rape , Ivanka has done nothing even __`remotely similar`__ . |
    | **`pcc_eng_14_016.1238_x0244270_18:08-09-10`**  | The way these compounds are made is not __`remotely similar`__ to the metabolic processes that plants and animals use to create them .                                |
    | **`pcc_eng_08_042.2886_x0668193_073:1-8-9`**    | None of the wines I tasted were __`remotely similar`__ , even those from the same block in the vineyard .                                                             |
    | **`pcc_eng_12_091.5684_x1463390_35:1-2-3`**     | Nothing __`remotely similar`__ can be said of real terrorists who believe that targeting civilians is the road to heaven . "                                          |
    | **`pcc_eng_18_056.7936_x0903081_001:10-11-12`** | Bush is not a war criminal , he is not __`remotely similar`__ to Adolf Hitler , he has persued policies that are in no way comparable to those of Adolf Hitler .      |
    
    
    5. _remotely interesting_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==remotely_interesting`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                          |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_006.6013_x0090234_138:23-25-26`** | It is to be said however , that the introductory essay is too long , drawn out and in my opinion , not even __`remotely interesting`__ .                             |
    | **`pcc_eng_11_018.4118_x0281650_24:3-4-5`**     | There 's nothing __`remotely interesting`__ about Connect 's black cherry - lime flavor , the eight nutrients it contains or the obligatory caffeine that 's added . |
    | **`pcc_eng_16_094.4093_x1512135_25:13-14-15`**  | When everything in the gossip world has gone stale and there 's nothing __`remotely interesting`__ to write about , she suddenly appears .                           |
    | **`pcc_eng_00_103.2426_x1653675_20:5-6-7`**     | To the bar where nothing __`remotely interesting`__ ever happens ! "                                                                                                 |
    | **`pcc_eng_24_028.3484_x0442212_8:3-5-6`**      | She was n't even __`remotely interesting`__ when she was Tate .                                                                                                      |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_true_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_close_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_interested_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_similar_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_interesting_50ex.csv
    
    ## 6. *yet*
    
    |                 |        `N` |      `f1` |   `adv_total` |
    |:----------------|-----------:|----------:|--------------:|
    | **NEGATED_yet** | 86,330,752 | 3,226,213 |       101,707 |
    
    
    |                          |    `f` |   `dP1` |   `LRC` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:-------------------------|-------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~yet_clear**     | 10,553 |    0.95 |   10.26 | 67,924.56 | 10,693 |    399.60 |   10,153.40 |       491,108 |
    | **NEGany~yet_ready**     |  7,611 |    0.93 |    9.23 | 48,012.06 |  7,838 |    292.91 |    7,318.09 |       240,297 |
    | **NEGany~yet_complete**  |  2,220 |    0.92 |    8.42 | 13,815.99 |  2,314 |     86.48 |    2,133.52 |       107,018 |
    | **NEGany~yet_sure**      |  1,990 |    0.92 |    8.37 | 12,379.79 |  2,075 |     77.54 |    1,912.46 |       844,981 |
    | **NEGany~yet_certain**   |    874 |    0.93 |    8.12 |  5,491.41 |    903 |     33.75 |      840.25 |       104,544 |
    | **NEGany~yet_eligible**  |    459 |    0.94 |    7.72 |  2,929.15 |    468 |     17.49 |      441.51 |        49,578 |
    | **NEGany~yet_available** |  7,481 |    0.87 |    7.69 | 44,196.15 |  8,238 |    307.86 |    7,173.14 |       866,272 |
    | **NEGany~yet_final**     |    659 |    0.91 |    7.45 |  4,028.75 |    699 |     26.12 |      632.88 |         9,657 |
    | **NEGany~yet_public**    |    496 |    0.91 |    7.36 |  3,055.97 |    522 |     19.51 |      476.49 |        41,602 |
    | **NEGany~yet_official**  |    353 |    0.94 |    7.33 |  2,236.98 |    362 |     13.53 |      339.47 |         9,778 |
    
    
    1. _yet clear_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_clear`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                           |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_074.4530_x1188748_22:4-5-6`**    | It is also not __`yet clear`__ whether the site received any legal notice from entertainment industry groups as there were sections on Hollywood and Foreign movies . |
    | **`nyt_eng_19961115_0585_21:13-14-15`**        | which will still leave her plenty of money , although it is not __`yet clear`__ how much .                                                                            |
    | **`apw_eng_20090828_0058_18:13-14-15`**        | whether that 's enough to try to fight Alinghi 's venue is not __`yet clear`__ .                                                                                      |
    | **`pcc_eng_03_016.6172_x0252784_03:13-14-15`** | While the deal is above the threshold requiring approval , it is not __`yet clear`__ which agency will handle it .                                                    |
    | **`pcc_eng_13_002.1603_x0018657_31:5-6-7`**    | Meanwhile , it 's not __`yet clear`__ whether the House will take up a similar measure .                                                                              |
    
    
    2. _yet ready_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_ready`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                     |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_005.3299_x0069976_57:37-38-39`**  | A local resident reveals that many of the builders are using ground water for construction , and plan to provide power through DG sets after the residents move in , as the DHBVN supply system is not __`yet ready`__ in the new sectors - particularly along the Expressway . |
    | **`pcc_eng_21_100.6809_x1610544_571:16-17-18`** | We are glad to hear that he is back at home now but he is not __`yet ready`__ to return to work .                                                                                                                                                                               |
    | **`pcc_eng_18_007.5604_x0106197_13:1-2-3`**     | Not __`yet ready`__ to venture out ?                                                                                                                                                                                                                                            |
    | **`pcc_eng_09_012.8737_x0192315_06:12-13-14`**  | Fordo 's final 644 machines have also been installed but are not __`yet ready`__ to be put into operation .                                                                                                                                                                     |
    | **`pcc_eng_13_106.7400_x1708585_5:28-29-30`**   | In the letter , Roeh listed numerous reasons why attempts to evict the residents from their homes should end , including the fact that alternative housing was not __`yet ready`__ .                                                                                            |
    
    
    3. _yet complete_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_complete`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                      |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_044.4840_x0703552_03:14-15-16`** | They 're pretty good savings and worth looking into if your collection is n't __`yet complete`__ .                                                                                               |
    | **`pcc_eng_07_007.1847_x0100167_03:12-13-14`** | " Although the economy continues to improve , the recovery is not __`yet complete`__ , " she told the Senate Banking Committee , delivering the Fed 's semi-annual economic report to Congress . |
    | **`pcc_eng_18_091.5325_x1466155_002:4-5-6`**   | This chronology is not __`yet complete`__ , however , more information shall be added as and when possible .                                                                                     |
    | **`pcc_eng_19_045.7764_x0722788_6:09-10-11`**  | Their mission to fix contact center communications was not __`yet complete`__ , so they started from the ground - up with a platform of their own .                                              |
    | **`pcc_eng_29_041.5006_x0654097_14:6-7-8`**    | The so-called counter-terrorism playbook is not __`yet complete`__ , an official said this week .                                                                                                |
    
    
    4. _yet sure_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_sure`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_033.8527_x0530266_48:25-26-27`** | She said she is determined not to complain , and laughed while saying she 's nicknamed the artificial limb " this sucker " -- not __`yet sure`__ whether it 's her friend or enemy .                                                                                                       |
    | **`pcc_eng_28_106.6866_x1709146_26:08-09-10`** | Whether or not she will succeed is not __`yet sure`__ but former Prime Monster George Papandreou 's assertion in Berlin in 2010 that the eurozone needed Greece more than Greece needed the eurozone , as audacious as it was at the time , is proving to have been remarkably prescient . |
    | **`pcc_eng_07_004.8477_x0062123_20:4-5-6`**    | The researchers are n't __`yet sure`__ whether one approach to nut cracking is really better than another , but they plan to continue studying the Cote d'Ivoire chimpanzees to find out .                                                                                                 |
    | **`pcc_eng_19_026.2550_x0407755_66:08-09-10`** | It 's possible , but I 'm not __`yet sure`__ ...                                                                                                                                                                                                                                           |
    | **`pcc_eng_10_070.7150_x1126900_12:5-6-7`**    | Azevedo said he was not __`yet sure`__ if he would be able to call a meeting of the council this weekend .                                                                                                                                                                                 |
    
    
    5. _yet certain_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_certain`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19941215_0227_14:11-12-13`**        | the wreck also will be preserved , although it was not __`yet certain`__ how , Carlsson said .                                                                                                                                                                                |
    | **`pcc_eng_11_061.9389_x0986214_7:3-4-5`**     | It is not __`yet certain`__ whether Lionel Messi will feature in the match but rumours suggests that he has been declared fit to play by the team medical which is a good news for Barcelona Fans and a boost for the team .                                                  |
    | **`apw_eng_20040216_0567_21:5-6-7`**           | `` I am still not __`yet certain`__ where I will play Sun , '' said China coach Arie Haan , according to footballasia.com .                                                                                                                                                   |
    | **`nyt_eng_19970127_0283_15:3-4-5`**           | researchers are not __`yet certain`__ that both responses are needed , but , according to Corey , the approach makes intuitive sense .                                                                                                                                        |
    | **`pcc_eng_24_073.6704_x1175575_11:20-22-23`** | On DC 's latest injury report , the duo were upgraded to questionable , but a specific timeline is n't quite __`yet certain`__ -- Quaranta has missed less time , and said that he could be back in less than two weeks , while Mc Tavish must take a more patient approach . |
    
    
    6. _yet eligible_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_eligible`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_108.5926_x1740767_04:21-22-23`**  | One major provision of the plan , dubbed the age tax , is particularly troublesome for older Americans who are n't __`yet eligible`__ for Medicare and get their insurance through the open marketplace .                                                                                                                                                                                  |
    | **`pcc_eng_03_006.6425_x0091248_38:19-20-21`**  | If your dog barks , growls , or is aggressive to people or dogs , your dog is not __`yet eligible`__ for Basic Manners .                                                                                                                                                                                                                                                                   |
    | **`pcc_eng_01_052.6618_x0835082_22:33-34-35`**  | Q : What do you think the likelihood is of some change to that metric in the near future , if not for all retirees , at least for those who are not __`yet eligible`__ ?                                                                                                                                                                                                                   |
    | **`pcc_eng_22_063.7831_x1015007_060:31-32-33`** | The prompt disposal of temporary records whose authorized retention periods have expired , the timely and systematic transfer to economical storage of records no longer needed in office space but not __`yet eligible`__ for final disposition , and the identification and transfer of permanent records to the National Archives for preservation and for reference and research use . |
    | **`pcc_eng_23_082.9303_x1323923_12:30-31-32`**  | We also work with platforms , groups and forums at EU level to influence the content of future funding calls , to increase the likelihood that projects that are not __`yet eligible`__ for existing funding packages might get the opportunity in the future .                                                                                                                            |
    
    
    7. _yet available_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_available`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                    |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_100.8171_x1616136_08:4-5-6`**    | The ad is not __`yet available`__ at Apple.com but can be seen via a You Tube capture at the end of this report .                                              |
    | **`apw_eng_19971123_0970_15:18-19-20`**        | the officer said a post-mortem examination and toxicology tests began Monday at the morgue but results were not __`yet available`__ .                          |
    | **`pcc_eng_13_101.2826_x1620432_03:09-10-11`** | Carey 's office said that autopsy results were not __`yet available`__ , but " it appeared Mr. Maldonado was the victim of a stabbing . "                      |
    | **`pcc_eng_15_009.2072_x0132575_03:7-8-9`**    | a wiki from this time is not __`yet available`__ , including Glenn Miller , Count Basie , Duke Ellington and Tommy Dorsey , as well as Benny Goodman himself . |
    | **`pcc_eng_05_010.4745_x0153716_03:12-13-14`** | " Due to circumstances beyond my control , the record is not __`yet available`__ in stores , " Ras said .                                                      |
    
    
    8. _yet final_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_final`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                  |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_059.6631_x0947610_16:08-09-10`** | The cover art as shown above is not __`yet final`__ , but this certainly still serves as a pretty nice preview of what fans can expect when they get their hands on the first issue of this Diablo series .                                                                                                                                                                                                  |
    | **`apw_eng_20090311_0637_8:4-5-6`**            | the results were n't __`yet final`__ because some skiers were still to race .                                                                                                                                                                                                                                                                                                                                |
    | **`apw_eng_20070904_0389_3:14-15-16`**         | he asked not to be named because the decision on a candidate was not __`yet final`__ .                                                                                                                                                                                                                                                                                                                       |
    | **`apw_eng_20080128_0951_2:69-70-71`**         | as the House planned a vote Tuesday on a plan that would speed rebates of up to $ 600 -LRB- euro407 -RRB- to most income earners -- more for couples and families with children -- the Senate was planning to draft its own measure with the add-ons , said senior Senate aides in both Democratic and Republoican parties , speaking on condition of anonymity because the package is not __`yet final`__ . |
    | **`apw_eng_20080323_0590_2:18-19-20`**         | the person spoke to the Associated Press on condition of anonymity on Sunday because the contract was not __`yet final`__ .                                                                                                                                                                                                                                                                                  |
    
    
    9. _yet public_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_public`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_041.2816_x0651339_08:29-30-31`** | It has now filed a supplementary protest with the Government Accountability Office ( GAO ) - a move first reported by US outlet Nextgov , and which is not __`yet public`__ but is likely to be an exchange of information and documents . |
    | **`pcc_eng_05_073.8540_x1179055_04:16-17-18`** | It will link into both College Street and Westmorland Street , although exactly how is not __`yet public`__ .                                                                                                                              |
    | **`pcc_eng_18_062.3547_x0993311_30:26-27-28`** | Several board members spoke during Monday 's meeting about Sanchez - Macias ' resignation , alluding to information the board said it has but is not __`yet public`__ .                                                                    |
    | **`pcc_eng_27_008.6331_x0122869_09:20-21-22`** | Ahlstrom 's wife relayed this information to Ahlstrom and , after confirming on the Internet that the information was not __`yet public`__ , Ahlstrom purchased 2,000 shares of BDM stock .                                                |
    | **`apw_eng_20090825_0079_3:16-17-18`**         | a senior administration official discussed the nomination on the condition of anonymity because it was not __`yet public`__ .                                                                                                              |
    
    
    10. _yet official_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==yet_official`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                             |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_095.7984_x1533214_06:08-09-10`** | He calls the trade , which is n't __`yet official`__ , a " coup " for both sides .                                                                                                                                                                                                                                                      |
    | **`pcc_eng_12_028.4029_x0443577_31:15-16-17`** | He referred to Shelly as his " ex -wife , " though that 's not __`yet official`__ .                                                                                                                                                                                                                                                     |
    | **`pcc_eng_08_062.5526_x0996928_10:17-18-19`** | Luke Scott has also been reported to be in the fold , but that deal is not __`yet official`__ .                                                                                                                                                                                                                                         |
    | **`apw_eng_20080425_0239_2:33-34-35`**         | the official is close to the Economy Ministry , but asked not to be identified further because he is not authorized to speak on behalf of the government and the announcement is not __`yet official`__ .                                                                                                                               |
    | **`pcc_eng_18_051.0810_x0810860_02:14-15-16`** | Though a 2012 referendum to reverse Maine 's 2009 same-sex -marriage repeal is not __`yet official`__ , the National Organization for Marriage ( NOM ) has already contributed approximately $ 32,000 to the Stand for Marriage Maine Political Action Committee ( PAC ) , according to a campaign disclosure report filed last month . |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_clear_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_ready_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_complete_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_sure_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_certain_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_eligible_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_available_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_final_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_public_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_official_50ex.csv
    
    ## 7. *ever*
    
    |                     |        `N` |       `f1` |   `adv_total` |
    |:--------------------|-----------:|-----------:|--------------:|
    | **NEGATED_ever**    | 86,330,752 |  3,226,213 |       124,592 |
    | **NEGMIR_ever**     |  2,032,082 |    293,963 |         5,179 |
    | **COMPLEMENT_ever** | 86,330,752 | 83,102,035 |       124,592 |
    
    
    |                           |   `f` |   `dP1` |   `LRC` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:--------------------------|------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~ever_simple**    |   212 |    0.77 |    5.54 | 1,142.04 |    262 |      9.79 |      202.21 |       427,167 |
    | **NEGany~ever_easy**      |   430 |    0.63 |    5.06 | 2,030.58 |    641 |     23.95 |      406.05 |       771,307 |
    | **NEGmir~ever_good**      |   300 |    0.84 |    5.05 | 1,103.09 |    306 |     44.27 |      255.73 |        38,252 |
    | **NEGmir~ever_easy**      |   368 |    0.85 |    4.66 | 1,399.10 |    370 |     53.52 |      314.48 |        21,775 |
    | **NEGany~ever_good**      |   332 |    0.40 |    3.76 | 1,178.00 |    756 |     28.25 |      303.75 |     2,037,285 |
    | **NEGmir~ever_able**      |   136 |    0.77 |    3.73 |   441.74 |    149 |     21.55 |      114.45 |         8,177 |
    | **NEGany~ever_perfect**   |   217 |    0.37 |    3.48 |   736.05 |    527 |     19.69 |      197.31 |       164,519 |
    | **NEGmir~ever_wrong**     |   102 |    0.82 |    3.34 |   361.62 |    106 |     15.33 |       86.67 |        24,007 |
    | **NEGmir~ever_perfect**   |   207 |    0.85 |    2.58 |   788.18 |    208 |     30.09 |      176.91 |         4,239 |
    | **NEGmir~ever_true**      |    51 |    0.75 |    2.35 |   160.72 |     57 |      8.25 |       42.75 |         8,402 |
    | **NEGmir~ever_free**      |    69 |    0.83 |    2.18 |   249.22 |     71 |     10.27 |       58.73 |         5,605 |
    | **NEGmir~ever_worth**     |    53 |    0.80 |    2.16 |   182.49 |     56 |      8.10 |       44.90 |         6,182 |
    | **NEGmir~ever_likely**    |   103 |    0.46 |    2.00 |   192.81 |    169 |     24.45 |       78.55 |        15,433 |
    | **NEGany~ever_able**      |   234 |    0.13 |    1.81 |   363.95 |  1,398 |     52.24 |      181.76 |       428,268 |
    | **COM~ever_more**         | 6,763 |    0.03 |    1.72 |   331.84 |  6,792 |  6,537.98 |      225.02 |     1,032,280 |
    | **COM~ever_present**      | 7,602 |    0.03 |    1.70 |   354.47 |  7,639 |  7,353.31 |      248.69 |       127,265 |
    | **NEGmir~ever_available** |    50 |    0.82 |    1.69 |   177.01 |     52 |      7.52 |       42.48 |        14,919 |
    | **COM~ever_popular**      | 4,485 |    0.04 |    1.67 |   283.43 |  4,492 |  4,324.00 |      161.00 |       828,951 |
    | **COM~ever_closer**       | 6,880 |    0.04 |    1.52 |   501.08 |  6,882 |  6,624.62 |      255.38 |        70,294 |
    
    
    1. _ever simple_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_simple`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                           |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19970203_0537_7:1-3-4`**             | nothing is __`ever simple`__ or straightforward on a Bjork album .                                                                                                                                                                                                    |
    | **`pcc_eng_06_100.1203_x1603307_17:22-24-25`**  | Terroir Insight : Domaine Georges-Roumier , Charmes - Chambertin " Aux Mazoyeres " Domaine Georges Roumier , Charmes - Chambertin ... nothing is __`ever simple`__ in Burgundy - and writing about this wine does involve a bit of good Bourgundian name complexity . |
    | **`pcc_eng_28_047.2422_x0748245_071:5-6-7`**    | With MS things are never __`ever simple`__ - if this virus was involved it may be activated by another virus such as EBV etc .                                                                                                                                        |
    | **`pcc_eng_27_030.5534_x0476989_155:10-12-13`** | With Adam it was never easy ; with him nothing was __`ever simple`__ .                                                                                                                                                                                                |
    | **`pcc_eng_21_085.7538_x1369985_067:1-3-4`**    | Nothing 's __`ever simple`__ anymore .                                                                                                                                                                                                                                |
    
    
    2. _ever easy_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_easy`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                         |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_074.1907_x1182863_25:07-10-11`** | And as the saying goes " Nothing great is __`ever easy`__ " .                                                                                                                                                                                       |
    | **`pcc_eng_27_007.3231_x0101675_2:1-5-6`**     | Nothing worth doing is __`ever easy`__ , so the adage goes .                                                                                                                                                                                        |
    | **`pcc_eng_18_055.2097_x0877705_42:12-15-16`** | I would venture to guess it was n't easy , but nothing worthwhile is __`ever easy`__ .                                                                                                                                                              |
    | **`pcc_eng_03_083.4948_x1335957_021:1-3-4`**   | Nothing is __`ever easy`__ when it comes to showbiz , so making it into LME is just the beginning of Kyoko 's quest to defeat / kill Sho Fuwa .                                                                                                     |
    | **`pcc_eng_24_063.1845_x1006106_57:4-5-6`**    | But there 's nothing __`ever easy`__ about lying half - naked on a table with an impossibly full bladder and feeling that unnerving twist of the speculum , fearful that a single sneeze or a cough could derail everything you 've worked toward . |
    
    
    3. _ever good_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_good`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20010524_0179_32:1-3-4`**           | nothing was __`ever good`__ enough .                                                                                                                                                                                                                       |
    | **`pcc_eng_08_057.9054_x0921631_048:5-6-7`**   | They 're good but not __`ever good`__ enough , and it gives them such an inferiority complex .                                                                                                                                                             |
    | **`pcc_eng_28_037.6052_x0591963_05:14-15-16`** | If we feel like what we 're doing and where we are is n't __`ever good`__ enough , it 's not surprising .                                                                                                                                                  |
    | **`pcc_eng_27_078.3089_x1250018_02:09-11-12`** | Nothing 's how it ever should be , nothing 's __`ever good`__ enough I 'm tired of hearing all the reasons why you really had it tough                                                                                                                     |
    | **`pcc_eng_26_068.7169_x1094819_04:47-49-50`** | If it were n't for the damn military marching in and breaking stuff , the CIA might have a relatively clean batch of dominoes to set up and knock down ( clean for us TV viewers ; for the natives of the " enemy " country nothing 's __`ever good`__ ) . |
    
    
    4. _ever able_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_able`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                   |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_096.8520_x1548486_40:6-7-8`**     | Of course , they were rarely __`ever able`__ to maintain their cover , and they were often thronged by local citizens and reporters excited to set eyes on the famous former first couple .                                                                                                                                                                                                                   |
    | **`pcc_eng_05_041.5187_x0655875_54:14-16-17`**  | Despite the fact that both men gave locations for Adam 's grave , neither was __`ever able`__ to lead police to it .                                                                                                                                                                                                                                                                                          |
    | **`pcc_eng_15_070.5129_x1122862_097:63-65-66`** | Its ability to find places in which to interfere was unlimited , and it decreed that no soldier should leave Richmond , either to go home or to return direct to the army , without a brown paper passport , signed by an officer appointed for that purpose , and countersigned by certain other persons whose authority to sign or countersign anything nobody was __`ever able`__ to trace to its source . |
    | **`pcc_eng_11_083.9787_x1343003_4:27-29-30`**   | Having the opportunity to tell the many stories of Altamira , or filming the four seasons in the Picos de Europa mountain range is a privilege few are __`ever able`__ to experience .                                                                                                                                                                                                                        |
    | **`pcc_eng_27_044.7888_x0707555_10:38-40-41`**  | Looking at the chaos that 's unfolded over the last five years in retail fashion , Mark Cohen , director of retail studies at Columbia University 's Graduate School of business , observed : " Broken businesses rarely are __`ever able`__ to be fixed .                                                                                                                                                    |
    
    
    5. _ever perfect_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_perfect`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                               | `token_str`                                                                                                                                                                                           |
    |:----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_085.0742_x1361332_079:6-8-9`**  | VAN SUSTEREN : I suppose nothing 's __`ever perfect`__ .                                                                                                                                              |
    | **`apw_eng_20040317_0040_22:22-24-25`**       | Bellamy expressed confidence her agency 's supply of mostly medicine , drugs and educational material are not being diverted : `` Nothing is __`ever perfect`__ , but we feel pretty comfortable . '' |
    | **`nyt_eng_19961217_0629_34:2-4-5`**          | `` Nothing is __`ever perfect`__ .                                                                                                                                                                    |
    | **`pcc_eng_12_035.4607_x0557443_4:15-17-18`** | I have been looking for this type of wedges for a while noow but nothing is __`ever perfect`__ for me D ; I hope they have this in my local target !                                                  |
    | **`pcc_eng_06_025.9134_x0403208_054:1-3-4`**  | Nothing is __`ever perfect`__ defending Manziel given his improvisational abilities , but it was slightly surprising to see teams sit back and let the Ags dictate to them as much as they did .      |
    
    
    6. _ever wrong_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_wrong`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                   | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
    |:--------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_013.2762_x0198274_04:10-12-13`**    | For their part , his teammates acted as if nothing was __`ever wrong`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_10_024.6973_x0382886_125:32-34-35`**   | We have all had the experience of a passing symptom , something clearly not working as it should , like a car engine stuttering one day and then resuming as though nothing was __`ever wrong`__ .                                                                                                                                                                                                                                                                                                                                                                           |
    | **`pcc_eng_28_027.0292_x0420396_29:103-104-105`** | Other focal points of Burns ' discussion included China , which he described as an increasingly formidable rising power , " part of a wider phenomenon of movement of the center of gravity from West to East " ; North Korea , " the single biggest test for U.S. diplomacy in the coming years , " with the U.S. having limited options in seeking to contain North Korea 's nuclear development ; Europe , " facing the toughest set of challenges at any time since the end of the Cold War " ; and the Middle East , where " pessimists are hardly __`ever wrong`__ . " |
    | **`pcc_eng_06_075.1900_x1199996_065:28-30-31`**   | All my bloody -minded defiance at taking care of this thing on my own , and getting on with life all singing , all dancing as if nothing is __`ever wrong`__ became completely irrelevant to the point of hilarity in that dark hotel room in the middle of the night .                                                                                                                                                                                                                                                                                                      |
    | **`pcc_eng_10_079.2703_x1265091_5:30-31-32`**     | i bought my integra with 128 K miles on it , and i drive it 150 miles a day ( not by choice ) and it holds firm and nothing __`ever wrong`__ with it .                                                                                                                                                                                                                                                                                                                                                                                                                       |
    
    
    7. _ever true_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==ever_true`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                     |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_068.8872_x1097611_220:08-12-13`** | You can count on a junkie - nothing they say is __`ever true`__ .                                               |
    | **`pcc_eng_24_008.6342_x0123177_26:5-6-7`**     | What they say is hardly __`ever true`__ .                                                                       |
    | **`nyt_eng_20081030_0162_8:10-14-15`**          | `` That raises a question as to whether or not the allegations were __`ever true`__ , '' the judge said .       |
    | **`pcc_eng_05_009.3531_x0135563_06:20-21-22`**  | You 'll find that some girls enjoy reading " boy " books , but the converse of this is hardly __`ever true`__ . |
    | **`pcc_eng_06_074.6445_x1191258_20:6-7-8`**     | And even if that were n't __`ever true`__ for James , it is true for many , many others .                       |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_simple_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_easy_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_good_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_able_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_perfect_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_wrong_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_true_50ex.csv
    
    ## 8. *immediately*
    
    |                         |        `N` |      `f1` |   `adv_total` |
    |:------------------------|-----------:|----------:|--------------:|
    | **NEGATED_immediately** | 86,330,752 | 3,226,213 |       103,177 |
    | **NEGMIR_immediately**  |  2,032,082 |   293,963 |         1,442 |
    
    
    |                                   |    `f` |   `dP1` |   `LRC` |       `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:----------------------------------|-------:|--------:|--------:|-----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~immediately_clear**      | 25,276 |    0.90 |    8.32 | 153,302.22 | 27,066 |  1,011.47 |   24,264.53 |       491,108 |
    | **NEGany~immediately_possible**   |  1,027 |    0.90 |    7.68 |   6,269.26 |  1,091 |     40.77 |      986.23 |       364,265 |
    | **NEGany~immediately_available**  | 21,297 |    0.66 |    5.77 | 102,962.94 | 30,725 |  1,148.20 |   20,148.80 |       866,272 |
    | **NEGany~immediately_able**       |    639 |    0.58 |    4.87 |   2,851.84 |  1,036 |     38.72 |      600.28 |       428,268 |
    | **NEGany~immediately_obvious**    |  2,258 |    0.49 |    4.59 |   9,043.23 |  4,305 |    160.88 |    2,097.12 |       193,498 |
    | **NEGany~immediately_apparent**   |  2,031 |    0.35 |    3.80 |   6,581.69 |  5,260 |    196.57 |    1,834.43 |        64,104 |
    | **NEGany~immediately_successful** |    292 |    0.36 |    3.47 |     958.19 |    743 |     27.77 |      264.23 |       407,004 |
    | **NEGany~immediately_visible**    |    436 |    0.32 |    3.35 |   1,324.08 |  1,234 |     46.12 |      389.88 |       137,609 |
    | **NEGany~immediately_evident**    |    428 |    0.25 |    2.96 |   1,122.08 |  1,466 |     54.78 |      373.22 |        60,888 |
    | **NEGmir~immediately_available**  |    164 |    0.39 |    1.91 |     258.42 |    304 |     43.98 |      120.02 |        14,919 |
    
    
    1. _immediately clear_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_clear`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                             | `token_str`                                                                                                                                                                  |
    |:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20060428_0733_4:3-4-5`**         | it was not __`immediately clear`__ if or when the storm will hit Bangladesh 's coast _ and there was a possibility it may hit neighboring Myanmar , the statement said .     |
    | **`apw_eng_20060404_0983_18:12-13-14`**     | a spokeswoman for the U.S. attorney 's office said it was not __`immediately clear`__ who would be defending those charged .                                                 |
    | **`pcc_eng_09_040.4412_x0638161_02:3-4-5`** | It was not __`immediately clear`__ how the 30 - year- old middle linebacker , one of the leaders of the Eagles for most of the past decade , fits into Jon Gruden 's plans . |
    | **`apw_eng_19950912_0024_16:3-4-5`**        | it was not __`immediately clear`__ what the Rockefeller Group 's proposal would mean for that deal .                                                                         |
    | **`apw_eng_19970313_0172_3:3-4-5`**         | it was not __`immediately clear`__ if the explosions Wednesday night were connected to the announcement of the plot to kill Buyoya .                                         |
    
    
    2. _immediately possible_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_possible`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                             | `token_str`                                                                                                                                                                       |
    |:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20080329_0283_3:3-4-5`**         | it was not __`immediately possible`__ to independently verify whether those killed were civilians or combatants .                                                                 |
    | **`apw_eng_20010228_0437_12:5-6-7`**        | a precise count was n't __`immediately possible`__ , because most rail passengers travel without reservations .                                                                   |
    | **`apw_eng_20090520_0278_3:09-10-11`**      | independent confirmation of the arrests early Wednesday was not __`immediately possible`__ .                                                                                      |
    | **`apw_eng_19980821_0315_4:3-4-5`**         | it was not __`immediately possible`__ to confirm whether Albright also telephoned Kenyan President Daniel arap Moi or Tanzanian President Benjamin Mkapa about the U.S. actions . |
    | **`pcc_eng_17_033.9680_x0533175_16:3-4-5`** | It was not __`immediately possible`__ to reconcile these claims and the authorities could not be reached for comment .                                                            |
    
    
    3. _immediately available_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_available`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                              |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19980620_0196_4:4-5-6`**            | Prefectural officials were not __`immediately available`__ for comment Saturday .                                                                        |
    | **`pcc_eng_28_095.1036_x1522355_15:7-8-9`**    | The names of the workers were not __`immediately available`__ .                                                                                          |
    | **`nyt_eng_19970324_0577_10:09-10-11`**        | officials at the NRA and the CAGW were not __`immediately available`__ for comment .                                                                     |
    | **`pcc_eng_01_019.2094_x0294397_10:18-19-20`** | The contractor has referred all comment to the National Oceanic and Atmospheric Administration , whose spokeswoman was not __`immediately available`__ . |
    | **`apw_eng_20090426_0140_11:5-6-7`**           | the Unification Ministry was not __`immediately available`__ for comments on the report .                                                                |
    
    
    4. _immediately able_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_able`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                             | `token_str`                                                                                                                                                                                    |
    |:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_100.5163_x1607823_40:4-5-6`** | The Guardian was not __`immediately able`__ to verify the claims .                                                                                                                             |
    | **`pcc_eng_09_040.3743_x0637115_26:4-5-6`** | Since retailers are not __`immediately able`__ to change sourcing , importing productions from China will continue .                                                                           |
    | **`apw_eng_20001019_0380_3:3-4-5`**         | he was not __`immediately able`__ to identify the company that tried to send the container , which was in a terminal waiting to be loaded onto a ship when authorities found the human cargo . |
    | **`pcc_eng_14_043.4741_x0686162_15:3-4-5`** | Reuters was not __`immediately able`__ to contact the lawyer .                                                                                                                                 |
    | **`pcc_eng_08_099.3950_x1593158_21:5-6-7`** | Laurie said authorities were n't __`immediately able`__ to seize the animals because there was no place to take them .                                                                         |
    
    
    5. _immediately obvious_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_obvious`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                       |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_074.2675_x1185737_14:3-4-5`**     | This was n't __`immediately obvious`__ to us - for some reason the " Pick " pane was only a few pixels high and we could n't see what it contained - but after a little manual sizing , everything become clear . |
    | **`pcc_eng_25_061.0842_x0973251_05:32-33-34`**  | The most effective use of Energy or Effort " , although with the furious activity one sees in a Judo practice or a competition between two matched opponents , it 's not __`immediately obvious`__ .              |
    | **`pcc_eng_07_056.7422_x0900827_038:15-17-18`** | My only desire is to expose psychological manipulation and corruption ; but it is n't always __`immediately obvious`__ to ' mostpeople ' when that is happening .                                                 |
    | **`pcc_eng_01_011.8932_x0176019_47:12-13-14`**  | It will be located on Lexington , a street that is n't __`immediately obvious`__ to people passing by but should become more popular with The Place and Kuni 's already calling it home .                         |
    | **`pcc_eng_06_048.3368_x0765962_26:4-5-6`**     | Some expenses are n't __`immediately obvious`__ - such as medical costs ( which include not only doctors but also those trips to Walgreen 's and Rite - Aid for cold medicine ) .                                 |
    
    
    6. _immediately apparent_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_apparent`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                   |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_092.0298_x1471066_3:20-22-23`**   | The relevance of Julian Jaynes 's theory of the bicameral mind to the history of religion in Tibet may not be __`immediately apparent`__ to either readers of Jaynes 's work or Tibetologists .                               |
    | **`pcc_eng_10_070.2939_x1120202_34:23-25-26`**  | Hence , you will be able to use the web interface , but the import process will be proceeding and results may not be __`immediately apparent`__ .                                                                             |
    | **`pcc_eng_27_028.2341_x0439875_049:17-18-19`** | The timber structure essentially hides the cables ; and from a quick view , it is not __`immediately apparent`__ that it is even a suspension bridge .                                                                        |
    | **`pcc_eng_02_101.4150_x1623668_16:16-17-18`**  | " But when a writer does have a particular relationship to his subject that is not __`immediately apparent`__ to the reader , it is important to disclose that so that the reader can evaluate the argument intelligently . " |
    | **`pcc_eng_00_065.8934_x1048992_05:08-09-10`**  | The compatibility between CF and Yara is not __`immediately apparent`__ ; however , the two giants have complementary markets .                                                                                               |
    
    
    7. _immediately successful_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_successful`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                  |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_100.8970_x1616341_58:7-8-9`**    | Attempts to reach With Honor were not __`immediately successful`__ .                                                                                                         |
    | **`pcc_eng_06_089.0466_x1423837_15:16-17-18`** | Attempts to reach Rice through Stanford University , where she is a professor , were not __`immediately successful`__ , nor were attempts to reach Jernstedt .               |
    | **`pcc_eng_00_064.5598_x1027629_13:08-09-10`** | Efforts to reach her by telephone were not __`immediately successful`__ .                                                                                                    |
    | **`pcc_eng_20_071.2187_x1134656_24:26-27-28`** | It could not be immediately determined if he entered a plea , and attempts by the AP to reach Fowlkes or his public defender were n't __`immediately successful`__ Tuesday . |
    | **`apw_eng_20090324_0028_5:09-10-11`**         | attempts to obtain a comment from Frank were not __`immediately successful`__ Monday .                                                                                       |
    
    
    8. _immediately visible_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_visible`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_035.6120_x0560247_02:27-28-29`** | For Elves and Wizards , this " magic " was not something special or different from the natural world , just part of it that was not __`immediately visible`__ , leading to more common categorization of things as " Seen " or " Unseen " . |
    | **`pcc_eng_01_009.8537_x0143055_18:4-5-6`**    | The urns are not __`immediately visible`__ , but are located behind a wall of toughened glass .                                                                                                                                             |
    | **`pcc_eng_29_079.5984_x1269701_12:16-18-19`** | Often , soft spots are combined with warping over time , which may or may not be __`immediately visible`__ from an inspection .                                                                                                             |
    | **`pcc_eng_16_064.5934_x1029369_2:31-32-33`**  | Forum contributor Heath Koch encourages students to reflect on what service means and emphasizes the importance of the effects service has on the community , even if those changes are n't __`immediately visible`__ .                     |
    | **`nyt_eng_20060630_0291_14:6-8-9`**           | most of his changes will not be __`immediately visible`__ to the untrained eye .                                                                                                                                                            |
    
    
    9. _immediately evident_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==immediately_evident`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                       |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_089.4986_x1429351_10:4-5-6`**     | Clear rot is not __`immediately evident`__ but will show up as softening of the tissue with possible mold .       |
    | **`pcc_eng_08_022.6995_x0351479_284:3-4-5`**    | It was n't __`immediately evident`__ to me whether or not Horn has a TV gig , but he 's not currently coaching .  |
    | **`pcc_eng_13_053.3685_x0846612_19:5-6-7`**     | Proof of improvement was not __`immediately evident`__ in the results , so her attitude was not always positive . |
    | **`pcc_eng_00_053.7271_x0852189_17:07-09-10`**  | The presence of genital warts might not be __`immediately evident`__ when you first contract them .               |
    | **`pcc_eng_02_031.5925_x0495019_090:11-13-14`** | Sometimes hearing loss can occur suddenly -- and it 's not always __`immediately evident`__ why .                 |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_clear_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_possible_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_available_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_able_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_obvious_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_apparent_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_successful_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_visible_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_evident_50ex.csv
    
    ## 9. *any*
    
    |                 |        `N` |      `f1` |   `adv_total` |
    |:----------------|-----------:|----------:|--------------:|
    | **NEGATED_any** | 86,330,752 | 3,226,213 |        94,152 |
    | **NEGMIR_any**  |  2,032,082 |   293,963 |         1,514 |
    
    
    |                          |   `f` |   `dP1` |   `LRC` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:-------------------------|------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~any_happier**   |   830 |    0.53 |    4.65 | 3,488.76 |  1,472 |     55.01 |      774.99 |        19,501 |
    | **NEGmir~any_better**    |   382 |    0.61 |    3.42 |   960.25 |    503 |     72.76 |      309.24 |        16,232 |
    | **NEGany~any_clearer**   |   357 |    0.30 |    3.21 | 1,051.22 |  1,053 |     39.35 |      317.65 |        13,369 |
    | **NEGany~any_simpler**   |   228 |    0.30 |    3.09 |   671.74 |    672 |     25.11 |      202.89 |        26,094 |
    | **NEGany~any_different** |   910 |    0.24 |    2.98 | 2,270.24 |  3,313 |    123.81 |      786.19 |       909,864 |
    | **NEGany~any_worse**     | 1,693 |    0.16 |    2.47 | 3,165.88 |  8,487 |    317.16 |    1,375.84 |       214,166 |
    | **NEGany~any_younger**   |   256 |    0.19 |    2.37 |   544.17 |  1,121 |     41.89 |      214.11 |        29,805 |
    | **NEGmir~any_different** |    51 |    0.75 |    2.35 |   160.72 |     57 |      8.25 |       42.75 |        40,266 |
    | **NEGmir~any_easier**    |    67 |    0.61 |    2.29 |   166.41 |     89 |     12.87 |       54.13 |         2,640 |
    | **NEGany~any_bigger**    |   357 |    0.17 |    2.27 |   688.06 |  1,735 |     64.84 |      292.16 |       130,470 |
    | **NEGmir~any_closer**    |    57 |    0.60 |    2.09 |   138.45 |     77 |     11.14 |       45.86 |         1,168 |
    | **NEGany~any_harder**    |   227 |    0.15 |    1.98 |   395.22 |  1,221 |     45.63 |      181.37 |        99,332 |
    | **NEGany~any_easier**    | 1,607 |    0.11 |    1.95 | 2,164.75 | 10,860 |    405.84 |    1,201.16 |       237,680 |
    | **NEGany~any_better**    | 4,754 |    0.10 |    1.87 | 5,646.41 | 35,471 |  1,325.56 |    3,428.44 |       743,338 |
    | **NEGmir~any_worse**     |    88 |    0.36 |    1.45 |   127.07 |    173 |     25.03 |       62.97 |        11,295 |
    
    
    1. _any happier_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_happier`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                           |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_063.7208_x1015990_06:21-23-24`** | It 's been 2 years since we 've started RVing with our four kids full - time and we could n't be __`any happier`__ !                  |
    | **`pcc_eng_24_021.1817_x0325996_039:5-6-7`**   | The Scott administration is n't __`any happier`__ over Trump 's plans for the U.S. Environmental Protection Agency .                  |
    | **`pcc_eng_17_103.1065_x1650555_22:4-6-7`**    | and we could n't be __`any happier`__ .                                                                                               |
    | **`pcc_eng_24_029.6417_x0463220_13:4-6-7`**    | " I could not be __`any happier`__ , " said Tierney , reached in Las Vegas by telephone .                                             |
    | **`nyt_eng_19981221_0037_25:2-7-8`**           | and nobody in the stadium was __`any happier`__ about it than the guy on crutches with a brace on his surgically repaired left knee . |
    
    
    2. _any better_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_better`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_026.5739_x0413820_11:5-6-7`**    | Even outdoor phones are not __`any better`__ .                                                                                                                                             |
    | **`pcc_eng_11_058.8801_x0936493_23:5-6-7`**    | And the outlook is n't __`any better`__ this year , even as surveys suggest Atlantic City 's image is improving :                                                                          |
    | **`pcc_eng_08_037.6375_x0593215_20:16-21-22`** | There is an atrocious audio tour that we suggest you skip , although it 's not like the signage is __`any better`__ .                                                                      |
    | **`pcc_eng_12_053.9238_x0855598_19:12-13-14`** | And when he was in that NHS group he was definitely not __`any better`__ .                                                                                                                 |
    | **`pcc_eng_25_032.2465_x0505700_29:08-10-11`** | The timing of this deal also could n't be __`any better`__ for Marvel , as any comic book fan will tell you that Spider - Man plays a pretty significant role in the Civil War storyline . |
    
    
    3. _any clearer_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_clearer`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_106.9234_x1713409_22:07-10-11`** | " With me , I could n't have been __`any clearer`__ .                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_14_045.5385_x0719606_05:11-13-14`** | And now that it 's here , the answer is n't really __`any clearer`__ .                                                                                                                                                                                                                                                 |
    | **`pcc_eng_20_019.1065_x0292494_09:5-7-8`**    | I guess you ca n't be __`any clearer`__ than that .                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_08_070.7116_x1128744_39:30-33-34`** | Red Wings general manager Ken Holland did not meet with reporters at Joe Louis Arena during Monday 's locker cleanout / team photo function , but the message could n't have been __`any clearer`__ from players and coach Mike Babcock -- Detroit is going to be a major player on July 1 , when free agency starts . |
    | **`pcc_eng_25_008.2868_x0118141_11:09-10-11`** | After two rounds of consultations most people are n't __`any clearer`__ on how the next steps will unfold .                                                                                                                                                                                                            |
    
    
    4. _any simpler_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_simpler`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                               |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_003.7424_x0044612_17:09-11-12`**  | However , the point I 'm making could n't be __`any simpler`__ .                                                          |
    | **`pcc_eng_29_010.2184_x0149071_036:07-09-10`** | Applying for a cash advance could n't be __`any simpler`__ .                                                              |
    | **`pcc_eng_02_022.0995_x0341311_36:3-5-6`**     | It ca n't be __`any simpler`__ to obtain a loan with bad credit or no credit when you utilize Title Loans Bellefontaine . |
    | **`pcc_eng_25_060.2436_x0959545_24:3-5-6`**     | It could n't be __`any simpler`__ . . . or more lucrative .                                                               |
    | **`pcc_eng_23_057.7549_x0917284_47:07-09-10`**  | Win FF 's user interface could not be __`any simpler`__ .                                                                 |
    
    
    5. _any different_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_different`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                             | `token_str`                                                                                                                                                      |
    |:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_054.0207_x0857737_25:7-8-9`** | Erickson said , " It 's not __`any different`__ than it has been .                                                                                               |
    | **`nyt_eng_20021011_0055_48:5-7-8`**        | Brown and Simms should n't be __`any different`__ .                                                                                                              |
    | **`nyt_eng_19990424_0147_19:12-13-14`**     | `` As great as last season was , we 're really not __`any different`__ in points from where we were last year , except for maybe one more win , '' Gordon said . |
    | **`nyt_eng_19950501_0016_41:4-5-6`**        | `` It was n't __`any different`__ before the game _ there were n't any indications that we were n't ready to play . ''                                           |
    | **`nyt_eng_20001215_0354_37:3-5-6`**        | that wo n't be __`any different`__ -LRB- tonight -RRB- .                                                                                                         |
    
    
    6. _any worse_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_worse`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_081.9042_x1308370_09:13-15-16`**  | The argument that a replacement super regulator replacing all other regulators could not be __`any worse`__ than the regulator we currently have , is a valid one .                                                                                                                     |
    | **`pcc_eng_15_090.1110_x1440327_128:07-09-10`** | Well , I guess he ca n't be __`any worse`__ than that guy who had the job before him , right ?                                                                                                                                                                                          |
    | **`pcc_eng_00_105.4284_x1688996_47:3-5-6`**     | They ca n't be __`any worse`__ than this effort ...!                                                                                                                                                                                                                                    |
    | **`pcc_eng_00_008.9609_x0128456_11:45-47-48`**  | Longtime backup Matt Moore played well in relief ( 17 - of - 28 , 282 yards , one touchdown , zero interceptions in one half ) , and although Moore was brutal in the blowout loss to the Ravens , the offense ca n't be __`any worse`__ with him at the helm than it was with Cutler . |
    | **`pcc_eng_23_070.5600_x1123953_020:40-41-42`** | Actually , he recognizes the countess has more humanity than the rest of the party , because when she had told the others she had shot an Apache , they seemed to think killing a " savage " was n't __`any worse`__ than killing an animal .                                           |
    
    
    7. _any younger_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_younger`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                           |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_043.8152_x0692827_39:13-14-15`** | So you know , it 's a lot , and I 'm not __`any younger`__ .                                                                                                          |
    | **`nyt_eng_19981215_0268_34:4-6-7`**           | my prostate 's not getting __`any younger`__ , you know .                                                                                                             |
    | **`nyt_eng_20070826_0030_48:13-15-16`**        | he 'd promised he would at some point , and they were n't getting __`any younger`__ .                                                                                 |
    | **`nyt_eng_20060112_0160_104:5-7-8`**          | you are 25 and not getting __`any younger`__ , its either now or never .                                                                                              |
    | **`nyt_eng_19990102_0274_7:08-10-11`**         | `` The nucleus of the team is not getting __`any younger`__ , and it 's time to step up or step out , '' said Sanders , who played for the first time since Nov. 22 . |
    
    
    8. _any easier_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_easier`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                              |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_009.1377_x0131375_12:6-8-9`**     | Setting up Quick Apps could not be __`any easier`__ .                                                                                                                                                                                                                                    |
    | **`pcc_eng_09_046.9708_x0743833_02:38-40-41`**  | ( Reuters Health ) - - It 's been almost five years since the U.S. Food and Drug Administration made emergency contraception available without a prescription for all consumers , but a new study suggests it may not be __`any easier`__ for some teens to buy the drug at pharmacies . |
    | **`pcc_eng_09_108.07333_x1745470_20:13-15-16`** | The recipe requires just 5 regular pantry ingredients , and it could n't be __`any easier`__ to make !                                                                                                                                                                                   |
    | **`nyt_eng_19950624_0107_15:08-10-11`**         | this sport she insists on playing has n't become __`any easier`__ as the years have worn on and the titles , including the Grand Slam trophy she won at the French Open , her 16th , have piled up .                                                                                     |
    | **`pcc_eng_03_017.9821_x0274634_10:5-7-8`**     | Using Band Master could n't be __`any easier`__ .                                                                                                                                                                                                                                        |
    
    
    9. _any bigger_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==any_bigger`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                         |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_086.6510_x1384089_14:13-14-15`** | In contrast , a few of the latest miniature amplifier styles are not __`any bigger`__ than a deck of cards .                                                        |
    | **`pcc_eng_10_060.5741_x0963070_13:4-5-6`**    | Their world is n't __`any bigger`__ than the living room .                                                                                                          |
    | **`pcc_eng_10_054.7078_x0868620_165:3-4-5`**   | He was n't __`any bigger`__ or stronger than any of the rest of us , but he picked me up like a rag doll and ran as the jungle began erupting in flames behind us . |
    | **`pcc_eng_25_089.1968_x1427148_12:3-4-5`**    | They were n't __`any bigger`__ than she was .                                                                                                                       |
    | **`pcc_eng_01_007.6696_x0107751_02:23-25-26`** | This concept by Eduardo Guerrero is in keeping with Apple 's late design language of " bigger is better " but is n't actually __`any bigger`__ !                    |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_happier_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_better_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_clearer_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_simpler_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_different_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_worse_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_younger_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_easier_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_bigger_50ex.csv
    
    ## 10. *particularly*
    
    |                          |        `N` |      `f1` |   `adv_total` |
    |:-------------------------|-----------:|----------:|--------------:|
    | **NEGMIR_particularly**  |  2,032,082 |   293,963 |        14,954 |
    | **NEGATED_particularly** | 86,330,752 | 3,226,213 |       575,960 |
    
    
    |                                     |   `f` |   `dP1` |   `LRC` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:------------------------------------|------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGmir~particularly_new**         |   407 |    0.80 |    5.04 | 1,396.47 |    431 |     62.35 |      344.65 |        14,734 |
    | **NEGany~particularly_surprising**  | 1,076 |    0.51 |    4.58 | 4,411.15 |  1,981 |     74.03 |    1,001.97 |       150,067 |
    | **NEGany~particularly_religious**   |   488 |    0.53 |    4.54 | 2,059.88 |    860 |     32.14 |      455.86 |        37,788 |
    | **NEGmir~particularly_wrong**       |   212 |    0.82 |    4.54 |   753.64 |    220 |     31.83 |      180.17 |        24,007 |
    | **NEGany~particularly_new**         |   752 |    0.50 |    4.49 | 3,065.77 |  1,396 |     52.17 |      699.83 |       321,311 |
    | **NEGany~particularly_original**    |   363 |    0.53 |    4.44 | 1,526.99 |    643 |     24.03 |      338.97 |        45,732 |
    | **NEGmir~particularly_surprising**  |   168 |    0.78 |    4.02 |   555.35 |    182 |     26.33 |      141.67 |         3,048 |
    | **NEGany~particularly_wrong**       |   219 |    0.45 |    3.89 |   838.81 |    446 |     16.67 |      202.33 |       187,720 |
    | **NEGany~particularly_friendly**    |   269 |    0.40 |    3.69 |   953.96 |    613 |     22.91 |      246.09 |       132,897 |
    | **NEGmir~particularly_unusual**     |   173 |    0.72 |    3.69 |   522.88 |    199 |     28.79 |      144.21 |         2,679 |
    | **NEGany~particularly_fast**        |   221 |    0.39 |    3.55 |   765.43 |    521 |     19.47 |      201.53 |        87,126 |
    | **NEGany~particularly_unusual**     |   440 |    0.35 |    3.53 | 1,419.90 |  1,146 |     42.83 |      397.17 |       108,584 |
    | **NEGany~particularly_comfortable** |   291 |    0.36 |    3.51 |   968.42 |    726 |     27.13 |      263.87 |       311,139 |
    | **NEGmir~particularly_remarkable**  |   108 |    0.81 |    3.50 |   378.25 |    113 |     16.35 |       91.65 |         3,471 |
    | **NEGmir~particularly_close**       |   138 |    0.71 |    3.39 |   405.25 |    162 |     23.44 |      114.56 |        15,958 |
    | **NEGmir~particularly_special**     |   327 |    0.61 |    3.36 |   820.88 |    431 |     62.35 |      264.65 |        16,942 |
    | **NEGany~particularly_happy**       |   837 |    0.28 |    3.26 | 2,347.24 |  2,632 |     98.36 |      738.64 |       528,511 |
    | **NEGmir~particularly_good**        |   392 |    0.57 |    3.18 |   912.45 |    547 |     79.13 |      312.87 |        38,252 |
    | **NEGmir~particularly_successful**  |    80 |    0.71 |    2.86 |   234.61 |     94 |     13.60 |       66.40 |         5,669 |
    | **NEGmir~particularly_memorable**   |   132 |    0.61 |    2.86 |   331.25 |    174 |     25.17 |      106.83 |         2,079 |
    
    
    1. _particularly new_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_new`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                         |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_008.5261_x0121315_11:4-5-6`**    | Though there is nothing __`particularly new`__ in his book , Savage does a respectable job of pulling together disparate material and showing how the details fit into a larger picture .                                                                                                                                                                           |
    | **`pcc_eng_24_063.1772_x1005979_15:09-10-11`** | The link between mercury and deteriorated vision is not __`particularly new`__ .                                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_23_031.0959_x0485846_19:20-21-22`** | One of the problems with reading old scifi is that what was new and radical in the 50s is not __`particularly new`__ or radical today .                                                                                                                                                                                                                             |
    | **`pcc_eng_01_022.3249_x0344921_12:11-12-13`** | As a conversion process , in fact , there 's nothing __`particularly new`__ about it in the US : it already existed there , on a parish by parish basis , in the so-called " Anglican Use Pastoral Provision " , whereby Anglican Parishes converted , but became not , as under the ordinariate , part of a new jurisdiction but simply joined the local diocese . |
    | **`pcc_eng_07_094.3489_x1508661_07:3-7-8`**    | Probably , none of this is __`particularly new`__ to you because not only I 've made a small presentation of this set , a few weeks ago , but also because it has been spoken on many websites on the last few days .                                                                                                                                               |
    
    
    2. _particularly surprising_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_surprising`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                         |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_096.6863_x1546013_022:64-65-66`** | To be sure , there are broken promises , like the one about not raising taxes on anyone making less than $ 250,000 per year , but the most consequential initiatives of his presidency -- health care , pursuing cap and trade , drawing down Iraq , ramping up Afghanistan , wanting to roll back some of the Bush tax cuts -- are n't __`particularly surprising`__ for anyone paying a little bit of attention . |
    | **`pcc_eng_03_009.9692_x0145042_06:13-14-15`**  | As the games tend to appeal to older audiences , this is not __`particularly surprising`__ .                                                                                                                                                                                                                                                                                                                        |
    | **`pcc_eng_17_099.5125_x1592225_08:18-19-20`**  | Like most autopsies , it was n't pretty -- and , in my view , it was n't __`particularly surprising`__ .                                                                                                                                                                                                                                                                                                            |
    | **`pcc_eng_15_080.1118_x1278489_28:4-5-6`**     | This finding is not __`particularly surprising`__ , as the difficulties in prompting Muslim conversions and the restrictions on religion in Muslim-majority countries are well - documented , and one might reasonably expect small population countries to be less able to support a variety of denominations .                                                                                                    |
    | **`nyt_eng_20050724_0039_17:3-4-5`**            | that 's not __`particularly surprising`__ , McGovern said .                                                                                                                                                                                                                                                                                                                                                         |
    
    
    3. _particularly religious_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_religious`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                       |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_058.4052_x0927720_07:7-8-9`**    | Amazingly , even people who are n't __`particularly religious`__ sometimes believe in ghosts , demons , souls , magic and psychic phenomena .                                     |
    | **`pcc_eng_00_047.3740_x0749547_05:5-6-7`**    | Though his family was not __`particularly religious`__ , Hassan became interested in theological studies and eventually moved to a Shi'a seminary in Bekaa Valley near Ba'albek . |
    | **`pcc_eng_23_017.5951_x0267706_15:10-11-12`** | Although most of the Jewish people in Israel are n't __`particularly religious`__ , I do believe it was God 's will that they be restored to nationhood .                         |
    | **`pcc_eng_15_007.2147_x0100343_17:4-5-6`**    | This family was not __`particularly religious`__ -- witness their dissolute behavior in Manila , where they planned another attack .                                              |
    | **`pcc_eng_04_087.7659_x1401984_10:11-12-13`** | I was raised in a Christian Orthodox family which was not __`particularly religious`__ .                                                                                          |
    
    
    4. _particularly wrong_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_wrong`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_044.2151_x0698918_19:38-39-40`** | 1987 - In an interview with Barbara Walters , Connery states " I would n't change my opinion " about what he said to Playboy in 1965 , and stands by his statement that there is " nothing __`particularly wrong`__ with hitting a woman . "                                                                                              |
    | **`pcc_eng_18_090.5334_x1449964_43:3-4-5`**    | There 's nothing __`particularly wrong`__ about any those ideas .                                                                                                                                                                                                                                                                         |
    | **`pcc_eng_13_033.8897_x0531756_19:7-8-9`**    | The Blu-ray I suppose there 's nothing __`particularly wrong`__ with the art Twilight Time has selected for How to Steal a Million -- a picture of the two stars underneath the original title treatment -- but it 's a shame they did n't go with , for instance , the image on the reverse of the sleeve , which is much more playful . |
    | **`pcc_eng_27_023.1755_x0358508_25:3-4-5`**    | There is nothing __`particularly wrong`__ with the last point ; it 's just that we should not be fooled into thinking that this year 's budget is somehow radically different from last year 's budget .                                                                                                                                  |
    | **`pcc_eng_12_027.8603_x0434617_13:11-12-13`** | Insofar as no one is above reproach , there is nothing __`particularly wrong`__ with this .                                                                                                                                                                                                                                               |
    
    
    5. _particularly original_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_original`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_018.0743_x0275810_02:19-23-24`** | The first entry from the so-called Smartest Person on Television took a few digs at The Office , none of which were __`particularly original`__ or enlightening .                                                                                          |
    | **`pcc_eng_27_098.2996_x1573716_063:3-4-5`**   | It is not __`particularly original`__ to observe that , in the dissolution of Christendom , Europe retained the body while America inherited the spirit , but one sometimes wonders whether for " spirit " it would not be better to say " poltergeist . " |
    | **`pcc_eng_02_104.7333_x1677463_22:6-7-8`**    | The episode 's story is n't __`particularly original`__ , but it 's very well -executed .                                                                                                                                                                  |
    | **`pcc_eng_02_022.1768_x0342545_07:3-5-6`**    | Folio might n't be __`particularly original`__ or distinctive , but when placed next to Diary , it looks like a comparative feat of engineering magic at a similar price point .                                                                           |
    | **`pcc_eng_27_095.2048_x1523839_051:4-5-6`**   | The idea was not __`particularly original`__ as the Americans had already developed missiles and UAVs that mislead AA systems by overloading their radar systems .                                                                                         |
    
    
    6. _particularly friendly_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_friendly`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                          |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_011.2459_x0166067_17:43-44-45`**  | If Israel is safer than ever , and they believe this is a relatively long term condition , the idea of withdrawing Israeli forces from the West Bank and letting the territory come under the control of a new country , the not __`particularly friendly`__ or strong Arab country of Palestine , will seem a more tolerable risk . |
    | **`pcc_eng_29_104.1794_x1667364_38:4-5-6`**     | The bartenders are n't __`particularly friendly`__ -- they are n't trying to cultivate regulars and do n't seem to care .                                                                                                                                                                                                            |
    | **`pcc_eng_08_048.5192_x0769247_02:1-7-8`**     | Not that the Pepsi Center is __`particularly friendly`__ to visiting teams anyway , but there were a couple of instances when you had to wonder if the Nuggets have been taking acting lessons during their none-too-copious free time .                                                                                             |
    | **`pcc_eng_28_071.3264_x1137815_084:20-21-22`** | So what happens to a person once they go from nothing to having an abundance of a bizarre and not __`particularly friendly`__ brand of success , and all while still in their early teens ?                                                                                                                                          |
    | **`pcc_eng_13_026.8833_x0418524_109:18-19-20`** | Steve Allen said , " I just feel that I know the facts and although I 'm not __`particularly friendly`__ with George Schatter ...                                                                                                                                                                                                    |
    
    
    7. _particularly unusual_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==particularly_unusual`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                            |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_041.1184_x0649986_07:16-17-18`**  | While the Catatumbo River attracts an unusually high number of lightning strikes , there is nothing __`particularly unusual`__ about the thunderstorms themselves - they 're the same kinds of storms that rumble all over the world . |
    | **`pcc_eng_05_048.7962_x0773716_35:24-25-26`**  | The first surprise was the weather , as we walked outwards from Glenmore - warm and springlike , with clear blue skies ; not __`particularly unusual`__ for the last week in May , but much better than the forecast had suggested .   |
    | **`nyt_eng_19960419_0385_10:10-11-12`**         | that the plot becomes overly convenient and unbelievable is not __`particularly unusual`__ in an action-heavy movie like `` The Subtitute . ''                                                                                         |
    | **`pcc_eng_16_054.8490_x0871476_012:25-26-27`** | Let 's start with Kennie 's story , since it 's both amazing and heart - breaking , even if , we fear , not __`particularly unusual`__ right about now ...                                                                             |
    | **`pcc_eng_25_081.1343_x1297279_13:3-4-5`**     | There is nothing __`particularly unusual`__ about current weather and climate change - it is generally well within long-term normal patterns .                                                                                         |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_new_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_surprising_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_religious_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_wrong_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_original_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_friendly_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_unusual_50ex.csv
    
    ## 11. *terribly*
    
    |                      |        `N` |      `f1` |   `adv_total` |
    |:---------------------|-----------:|----------:|--------------:|
    | **NEGATED_terribly** | 86,330,752 | 3,226,213 |        70,174 |
    | **NEGMIR_terribly**  |  2,032,082 |   293,963 |         5,218 |
    | **POSMIR_terribly**  |  2,032,082 | 1,738,105 |         5,218 |
    
    
    |                                 |   `f` |   `dP1` |   `LRC` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:--------------------------------|------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~terribly_surprising**  |   951 |    0.86 |    7.08 | 5,585.09 |  1,054 |     39.39 |      911.61 |       150,067 |
    | **NEGany~terribly_impressed**   |   280 |    0.72 |    5.36 | 1,434.24 |    371 |     13.86 |      266.14 |       113,281 |
    | **NEGany~terribly_different**   |   370 |    0.67 |    5.19 | 1,807.02 |    525 |     19.62 |      350.38 |       909,864 |
    | **NEGany~terribly_interested**  |   496 |    0.65 |    5.18 | 2,373.72 |    725 |     27.09 |      468.91 |       364,497 |
    | **NEGany~terribly_surprised**   |   289 |    0.68 |    5.17 | 1,430.88 |    402 |     15.02 |      273.98 |       104,044 |
    | **NEGany~terribly_concerned**   |   416 |    0.53 |    4.49 | 1,756.14 |    733 |     27.39 |      388.61 |       254,407 |
    | **NEGany~terribly_interesting** |   364 |    0.49 |    4.26 | 1,466.12 |    688 |     25.71 |      338.29 |       495,662 |
    | **NEGany~terribly_useful**      |   226 |    0.52 |    4.25 |   946.46 |    403 |     15.06 |      210.94 |       254,276 |
    | **NEGany~terribly_exciting**    |   382 |    0.42 |    3.92 | 1,402.29 |    828 |     30.94 |      351.06 |       236,396 |
    | **NEGany~terribly_expensive**   |   326 |    0.41 |    3.78 | 1,164.69 |    735 |     27.47 |      298.53 |       444,946 |
    | **NEGmir~terribly_new**         |    69 |    0.79 |    2.81 |   231.78 |     74 |     10.70 |       58.30 |        14,734 |
    | **NEGmir~terribly_surprising**  |    67 |    0.81 |    2.53 |   235.25 |     70 |     10.13 |       56.87 |         3,048 |
    | **NEGmir~terribly_interesting** |    56 |    0.58 |    2.02 |   132.87 |     77 |     11.14 |       44.86 |        14,240 |
    | **NEGmir~terribly_exciting**    |    78 |    0.49 |    1.95 |   155.84 |    122 |     17.65 |       60.35 |         8,844 |
    | **POS~terribly_wrong**          | 1,878 |    0.10 |    1.09 |   223.10 |  1,960 |  1,676.45 |      201.55 |        24,007 |
    
    
    1. _terribly surprising_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_surprising`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                     |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_056.8764_x0904315_45:32-33-34`** | I should caveat this by saying that I 've been involved in social justice movements of various kinds for nearly 15 years , so becoming vegan for ethical reasons was probably not __`terribly surprising`__ to the people who know me best .                                                    |
    | **`pcc_eng_15_036.4131_x0572526_31:10-11-12`** | With so much going for it , it is n't __`terribly surprising`__ that an Avondale zip code ( 60618 ) made it onto a list of the 10 most expensive zip codes in Chicago .                                                                                                                         |
    | **`pcc_eng_00_069.4515_x1106246_31:5-6-7`**    | Thus , it 's not __`terribly surprising`__ that the system in trial at Houston airport closely follows the design I outlined .                                                                                                                                                                  |
    | **`pcc_eng_27_003.7270_x0043774_19:6-7-8`**    | Of course , it is not __`terribly surprising`__ , because as a legislative group they are nothing but bullies , disparaging and demeaning those without power in this country in order to build themselves up .                                                                                 |
    | **`pcc_eng_20_100.4975_x1607683_10:26-27-28`** | It 's a question central to the continued survival of the human species ( or human civilization , at least ) , so it 's not __`terribly surprising`__ that people have written thousands of books on the subject and continue to argue over even the most minute and trivial parenting points . |
    
    
    2. _terribly impressed_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_impressed`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                 |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_099.7932_x1596539_078:3-4-5`**   | I was not __`terribly impressed`__ with the left-handed options , although Will Ohlman , acquired from the Cubs , will almost certainly be on the team and play an important set- up role . |
    | **`pcc_eng_29_048.5862_x0768484_43:12-14-15`** | How about Coors Light Iced Tea ? ) , Joyce has n't been __`terribly impressed`__ .                                                                                                          |
    | **`pcc_eng_21_104.1091_x1666328_1:3-4-5`**     | I was n't __`terribly impressed`__ , as every one of the cups was empty ---                                                                                                                 |
    | **`nyt_eng_20060421_0250_309:3-4-5`**          | he was n't __`terribly impressed`__ , anyway , with what his roommate was doing in his journalism classes .                                                                                 |
    | **`pcc_eng_00_088.1006_x1408157_045:3-4-5`**   | I was n't __`terribly impressed`__ , but I also did n't feel like it was an hour-and - a- half of my life I could n't get back .                                                            |
    
    
    3. _terribly different_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_different`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                     |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_13_037.7827_x0594746_10:6-7-8`**    | Because really , this is not __`terribly different`__ from saying that a judge threw a case because he was thinking about his reelection .                                                                                                                                                                                                                                      |
    | **`pcc_eng_08_002.2719_x0020612_13:10-11-12`** | The repetition remains , the loops and strategies are n't __`terribly different`__ , but the tone is brighter , with more snare drums in the mix , and Lennox 's voice , sometimes just making vowel sounds up and down scales , seems pointed backwards to the Brian Wilson styles found on Person Pitch and his guest spot on Daft Punk 's " Doin It Right " from last year . |
    | **`nyt_eng_20000328_0115_60:5-6-7`**           | the hectic lifestyle is n't __`terribly different`__ from investment banking .                                                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_26_098.4519_x1575474_13:4-5-6`**    | But it 's not __`terribly different`__ in the two countries , " said Reitz .                                                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_07_029.9640_x0468415_02:5-8-9`**    | I suppose it ca n't be too __`terribly different`__ down ( and over ) there though ~                                                                                                                                                                                                                                                                                            |
    
    
    4. _terribly interested_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_interested`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                                                  |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_016.7177_x0253762_14:3-4-5`**     | I was n't __`terribly interested`__ in the complex storylines , but I was happy to have a friend .                                                                                                                                           |
    | **`pcc_eng_09_104.8526_x1680690_6:26-27-28`**   | " The entire world hoped for a John F. Kerry victory , but the rednecks , the Bible-thumpers and other riff-raff from White America were n't __`terribly interested`__ by that . "                                                           |
    | **`pcc_eng_27_017.4472_x0266154_24:27-28-29`**  | So without a source which cites documents , or at least observations by an experienced soldier who was not trying to impress anyone , I am not __`terribly interested`__ .                                                                   |
    | **`pcc_eng_18_088.2726_x1413313_198:11-12-13`** | Klein , along on the junket with Hillary , was n't __`terribly interested`__ in the secretary 's obituary of Obama 's failed outreach to Iran .                                                                                              |
    | **`pcc_eng_02_059.3520_x0943773_20:28-29-30`**  | Electronic Product Codes can be used to identify individual items -- so every single can ( more likely , every bottle of champagne , as people are n't __`terribly interested`__ in tracking by the soda can ) could have a different code . |
    
    
    5. _terribly surprised_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_surprised`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                                       |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_043.8056_x0691741_05:5-6-7`**     | 2 ) I 'm not __`terribly surprised`__ that Alexi Casilla and Matt Tolbert raced to the bottom this spring .                                                                                                       |
    | **`nyt_eng_19970715_0862_21:5-7-8`**            | the Democratic candidates did not seem __`terribly surprised`__ that they were not invited to attend .                                                                                                            |
    | **`pcc_eng_14_049.2390_x0779466_10:14-16-17`**  | Dana A. Curhan , who represents Greig , told Lawyers Weekly he was not " __`terribly surprised`__ " by the ruling , but noted that the court 's reasoning differed significantly from Woodlock 's at sentencing . |
    | **`pcc_eng_19_066.6932_x1060572_05:3-4-5`**     | I 'm not __`terribly surprised`__ either , as their registration emails hinted at it , and I tried to ask about it , but with no response .                                                                       |
    | **`pcc_eng_07_032.2368_x0505138_326:11-12-13`** | They came out of the tunnel , and Mhumhi was not __`terribly surprised`__ to find them at the bottom of a ravine , like the one they had left earlier .                                                           |
    
    
    6. _terribly concerned_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_concerned`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_026.4274_x0410591_16:54-55-56`** | " We continue to believe that our video value proposition compelling one and especially with the improvements we 're making in the guide , the size of the VOD library and the continued improvements in the TWC TV app , we feel like we 've got a very strong video offering and were not __`terribly concerned`__ about others eating into that over - the - top offerings , " he said . |
    | **`pcc_eng_11_067.1570_x1070802_16:4-5-6`**    | the doctor was not __`terribly concerned`__ .                                                                                                                                                                                                                                                                                                                                               |
    | **`nyt_eng_20000519_0072_38:3-4-5`**           | i 'm not __`terribly concerned`__ whether a cockroach is discomfited when I kill it .                                                                                                                                                                                                                                                                                                       |
    | **`pcc_eng_02_047.9212_x0759088_21:5-6-7`**    | Consequently , they 're not __`terribly concerned`__ with how efficiently the selling firm ( which they will essentially be shutting down ) has been operated .                                                                                                                                                                                                                             |
    | **`pcc_eng_16_068.5199_x1092727_07:14-15-16`** | Longtime and successful RE / MAX Results real estate broker John Sullivan was n't __`terribly concerned`__ when he went in for a scheduled surgery to repair damage to his heart from an aortic aneurysm .                                                                                                                                                                                  |
    
    
    7. _terribly interesting_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_interesting`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                                                         |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_036.0451_x0566736_10:08-09-10`** | As a tweet it was neither informative nor __`terribly interesting`__ , but as the first , sent by Jack Dorsey to colleagues at San Francisco web firm Odeo five years ago today , it launched a global phenomenon . |
    | **`pcc_eng_17_035.0079_x0549843_24:6-7-8`**    | While most of them are n't __`terribly interesting`__ , Andy Richter frequently steals the show as the office bully Herb who has a dark secret .                                                                    |
    | **`pcc_eng_08_024.2265_x0376293_66:4-5-6`**    | Mark Graison is n't __`terribly interesting`__ either but at least he looks fine in a pair of swim trunks .                                                                                                         |
    | **`pcc_eng_16_096.7004_x1549187_3:4-5-6`**     | They just are n't __`terribly interesting`__ unless you 're attracted to women .                                                                                                                                    |
    | **`pcc_eng_08_068.5313_x1093569_4:5-6-7`**     | OK , so , nothing __`terribly interesting`__ there .                                                                                                                                                                |
    
    
    8. _terribly useful_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_useful`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                 | `token_str`                                                                                                                                                                                         |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_089.8878_x1436184_10:19-20-21`**  | So a year on , while I still think ADN 's objectives are laudable ; their service is n't __`terribly useful`__ to me and for it 's faults                                                           |
    | **`pcc_eng_22_057.9033_x0919835_20:13-14-15`**  | Alibris , and Abebooks seem to be the most prominent , but not __`terribly useful`__ .                                                                                                              |
    | **`pcc_eng_11_040.7853_x0643794_062:19-21-22`** | Since heart rate takes some time ( 3 - 5 minutes ) to go up , it 's never been __`terribly useful`__ for setting the intensity of HIIT and here RPE is a better choice .                            |
    | **`pcc_eng_15_069.8612_x1112397_33:2-3-4`**     | While not __`terribly useful`__ ( as they seem to know who we are already , as they DID find us ) , it 's a conversation starter for other uses of the code .                                       |
    | **`pcc_eng_24_031.8237_x0498558_14:6-7-8`**     | Euros stuck in Cyprus are not __`terribly useful`__ for engaging in trade with the rest of Europe , or for protecting the small country against being buffeted by the waves of the global economy . |
    
    
    9. _terribly exciting_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_exciting`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                                | `token_str`                                                                                                                                                                     |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_046.6107_x0737984_30:1-2-3`**    | Not __`terribly exciting`__ , I know , but I love the variety of textures one can achieve with it .                                                                             |
    | **`pcc_eng_26_042.3981_x0669661_122:4-5-6`**   | Otherwise there was nothing __`terribly exciting`__ to report on this leopard .                                                                                                 |
    | **`pcc_eng_09_029.5029_x0461446_034:6-7-8`**   | Well I can honestly say nothing __`terribly exciting`__ has happened - not that this was ever a new phenomenon .                                                                |
    | **`pcc_eng_28_025.2135_x0390941_56:17-18-19`** | Among the extras on the DVD is a collection of TV commercials and promotional spots -- not __`terribly exciting`__ unless you like seeing the same few clips spliced together . |
    | **`pcc_eng_12_038.7931_x0611311_14:4-5-6`**    | If Dreamer is n't __`terribly exciting`__ , Gatins picks up steam in the home stretch ( when it counts ) .                                                                      |
    
    
    10. _terribly expensive_
    
    - *filtering rows...*
      - regex parsing = False
      - ✓ Applied filter: `bigram_lower==terribly_expensive`
    
    ### 50 random rows matching filter(s) from `input frame`
    
    
    |                                             | `token_str`                                                                                                                                    |
    |:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_049.7948_x0789602_03:4-5-6`** | Although boxes are n't __`terribly expensive`__ , they 've got just one pack .                                                                 |
    | **`pcc_eng_06_036.4290_x0572814_14:4-5-6`** | A subscription is n't __`terribly expensive`__ and the games are not time - consuming or arduous .                                             |
    | **`pcc_eng_17_024.6851_x0383472_13:6-7-8`** | At 12000 yen it 's not __`terribly expensive`__ - excluding the shipping charges - and you can choose either stainless steel or titanium rod . |
    | **`pcc_eng_22_052.9174_x0838751_25:7-8-9`** | They are not cheap , but not __`terribly expensive`__ .                                                                                        |
    | **`nyt_eng_20050401_0092_31:20-21-22`**     | `` I want to show good art at reasonable prices , but some people think if a painting is n't __`terribly expensive`__ , it ca n't be good . '' |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/...
    
    Samples saved as...
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_surprising_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_impressed_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_different_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_interested_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_surprised_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_concerned_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_interesting_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_useful_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_exciting_50ex.csv
    1. /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_expensive_50ex.csv

