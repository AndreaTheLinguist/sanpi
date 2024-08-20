```python
from am_notebooks import *

from source.utils import HIT_TABLES_DIR
from source.utils.associate import TOP_AM_DIR, AM_DF_DIR

TAG='NEQ'
K=8
BK = max(K+2, 10)
BIGRAM_F_FLOOR=50
# BIGRAM_F_FLOOR={'ALL':50, 'NEQ':25}[TAG]

ADV_F_FLOOR=5000

TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
TAG_TOP_STR = f'{TAG}-Top{K}'
TAG_TOP_DIR = TOP_AM_TAG_DIR / TAG_TOP_STR
DATE=timestamp_today()
FOCUS_ORIG = ['f', 'E11', 'unexpected_f',
              'am_p1_given2', 'am_p1_given2_simple', 
              'am_p2_given1', 'am_p2_given1_simple', 
              'conservative_log_ratio',
              'am_log_likelihood', 
              'N', 'f1', 'f2', 'l1', 'l2']
FOCUS = adjust_am_names(FOCUS_ORIG)
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 80)

```


```python
adv_am = seek_top_adv_am(date_str=DATE, adv_floor=ADV_F_FLOOR, 
                         tag_top_str=TAG_TOP_STR, tag_top_dir=TAG_TOP_DIR)
```

> Loaded top adv AM table from  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-08-05.csv`



```python
NEG_HITS_PATH = HIT_TABLES_DIR /'RBdirect'/'ALL-RBdirect_final.parq'
POS_HITS_PATH = HIT_TABLES_DIR /'not-RBdirect'/f'{TAG}_not-RBdirect_final.parq'
```


```python
adv_list = adv_am.index.to_list()
# print_iter(adv_list, header=f'## Top {K} Most Negative Adverbs',bullet = '1.')
```

## Top 8 Most Negative Adverbs

1. necessarily
1. that
1. exactly
1. any
1. remotely
1. yet
1. immediately
1. ever
1. longer
1. particularly
1. terribly

## Load AM table for `adv~adj` comparison (bigram composition)


```python
blind_am_iter = AM_DF_DIR.joinpath('adv_adj').rglob(f'AdvAdj_{TAG}*min{BIGRAM_F_FLOOR}x_extra.parq')
blam_dict = {blamp.parent.parent.name.strip('ANY'): blamp for blamp in blind_am_iter}
print(pd.Series(blam_dict)
       .to_frame('path to "context-blind" AM scores')
       .to_markdown(tablefmt='rounded_grid', maxcolwidths=[None, 72]))

```

```log
╭────────┬──────────────────────────────────────────────────────────────────────────╮
│        │ path to "context-blind" AM scores                                        │
├────────┼──────────────────────────────────────────────────────────────────────────┤
│ mirror │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYmirror/extra/ │
│        │ AdvAdj_NEQ_any-mirror_final-freq_min50x_extra.parq                       │
├────────┼──────────────────────────────────────────────────────────────────────────┤
│ direct │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYdirect/extra/ │
│        │ AdvAdj_NEQ_any-direct_final-freq_min50x_extra.parq                       │
╰────────┴──────────────────────────────────────────────────────────────────────────╯
```


```python
def peek_am(peek_metric, blamin):
    peek = blamin.reset_index().groupby('l1').apply(
        lambda x: x.nlargest(1, peek_metric)
        ).reset_index(drop=True).set_index('key')
    print(f'\n_Bigrams with the highest `{peek_metric}` value for each adverb_\n')
    return peek.sort_values(peek_metric, ascending=False)


blind_priority_cols = METRIC_PRIORITY_DICT[f'{TAG}_blind']
blam_dfs = {}
for blam_kind, blam_path in blam_dict.items():
    print(f'\n### Loading `{blam_kind}` AM scores\n\n Path:',
          f'`{blam_path.relative_to(AM_DF_DIR.parent)}`\n')
    blamin = pd.read_parquet(
        blam_path, engine='pyarrow',
        filters=[('l1', 'in', adv_list)],
        columns=FOCUS_DICT[TAG]['adv_adj'])
    blamin['dataset'] = blam_kind
    blamin = catify(adjust_am_names(blamin),
                    reverse=True)
    peek_df = blamin.copy().filter(blind_priority_cols + ['l1'] + FREQ_COLS)
    # for peek_metric in blind_priority_cols:
    #     nb_show_table(peek_am(peek_metric, peek_df), n_dec=2)
    blamin.index = f'[_{blam_kind}_] ' + blamin.index
    blam_dfs[blam_kind] = blamin
```


### Loading `mirror` AM scores

 Path: `assoc_df/adv_adj/ANYmirror/extra/AdvAdj_NEQ_any-mirror_final-freq_min50x_extra.parq`


_Bigrams with the highest `LRC` value for each adverb_


|                             |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:----------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **exactly~alike**           |    7.30 |   517.06 |           0.37 |            0.22 | exactly      |    54 |    862 |    144 |
| **longer~viable**           |    6.47 |   482.88 |           0.23 |            0.15 | longer       |    57 |    841 |    248 |
| **any~closer**              |    5.98 |   465.53 |           0.21 |            0.13 | any          |    60 |  1,083 |    285 |
| **immediately~available**   |    5.43 | 1,249.24 |           0.32 |            0.19 | immediately  |   187 |    578 |  3,078 |
| **ever~perfect**            |    3.95 |   876.15 |           0.15 |            0.10 | ever         |   206 |  4,776 |  1,280 |
| **that~great**              |    3.84 | 1,174.94 |           0.13 |            0.09 | that         |   292 |  4,538 |  2,147 |
| **particularly~noteworthy** |    3.82 |   386.06 |           0.32 |            0.16 | particularly |    88 | 10,020 |    264 |
| **terribly~wrong**          |    3.40 | 1,488.08 |           0.18 |            0.11 | terribly     |   422 |  2,196 |  8,526 |
| **necessarily~wrong**       |    3.35 |   783.75 |           0.20 |            0.11 | necessarily  |   211 |    993 |  8,526 |
| **remotely~close**          |    3.34 |   829.53 |           0.11 |            0.08 | remotely     |   233 |  1,963 |  4,972 |


_Bigrams with the highest `G2` value for each adverb_


|                           |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:--------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **any~better**            |    5.56 | 2,549.65 |           0.35 |            0.23 | any          |   386 |  1,083 |  3,681 |
| **terribly~wrong**        |    3.40 | 1,488.08 |           0.18 |            0.11 | terribly     |   422 |  2,196 |  8,526 |
| **that~simple**           |    2.77 | 1,267.95 |           0.10 |            0.08 | that         |   487 |  4,538 |  7,580 |
| **immediately~available** |    5.43 | 1,249.24 |           0.32 |            0.19 | immediately  |   187 |    578 |  3,078 |
| **ever~perfect**          |    3.95 |   876.15 |           0.15 |            0.10 | ever         |   206 |  4,776 |  1,280 |
| **remotely~close**        |    3.34 |   829.53 |           0.11 |            0.08 | remotely     |   233 |  1,963 |  4,972 |
| **necessarily~wrong**     |    3.35 |   783.75 |           0.20 |            0.11 | necessarily  |   211 |    993 |  8,526 |
| **particularly~new**      |    2.15 |   746.36 |           0.08 |            0.05 | particularly |   407 | 10,020 |  4,393 |
| **exactly~sure**          |    3.44 |   583.16 |           0.16 |            0.09 | exactly      |   148 |    862 |  5,983 |
| **longer~viable**         |    6.47 |   482.88 |           0.23 |            0.15 | longer       |    57 |    841 |    248 |


_Bigrams with the highest `deltaP_max` value for each adverb_


|                             |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:----------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **exactly~alike**           |    7.30 |   517.06 |           0.37 |            0.22 | exactly      |    54 |    862 |    144 |
| **any~better**              |    5.56 | 2,549.65 |           0.35 |            0.23 | any          |   386 |  1,083 |  3,681 |
| **immediately~available**   |    5.43 | 1,249.24 |           0.32 |            0.19 | immediately  |   187 |    578 |  3,078 |
| **particularly~noteworthy** |    3.82 |   386.06 |           0.32 |            0.16 | particularly |    88 | 10,020 |    264 |
| **longer~viable**           |    6.47 |   482.88 |           0.23 |            0.15 | longer       |    57 |    841 |    248 |
| **necessarily~wrong**       |    3.35 |   783.75 |           0.20 |            0.11 | necessarily  |   211 |    993 |  8,526 |
| **terribly~wrong**          |    3.40 | 1,488.08 |           0.18 |            0.11 | terribly     |   422 |  2,196 |  8,526 |
| **ever~perfect**            |    3.95 |   876.15 |           0.15 |            0.10 | ever         |   206 |  4,776 |  1,280 |
| **that~great**              |    3.84 | 1,174.94 |           0.13 |            0.09 | that         |   292 |  4,538 |  2,147 |
| **remotely~close**          |    3.34 |   829.53 |           0.11 |            0.08 | remotely     |   233 |  1,963 |  4,972 |


_Bigrams with the highest `deltaP_mean` value for each adverb_


|                             |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:----------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **any~better**              |    5.56 | 2,549.65 |           0.35 |            0.23 | any          |   386 |  1,083 |  3,681 |
| **exactly~alike**           |    7.30 |   517.06 |           0.37 |            0.22 | exactly      |    54 |    862 |    144 |
| **immediately~available**   |    5.43 | 1,249.24 |           0.32 |            0.19 | immediately  |   187 |    578 |  3,078 |
| **particularly~noteworthy** |    3.82 |   386.06 |           0.32 |            0.16 | particularly |    88 | 10,020 |    264 |
| **longer~viable**           |    6.47 |   482.88 |           0.23 |            0.15 | longer       |    57 |    841 |    248 |
| **terribly~wrong**          |    3.40 | 1,488.08 |           0.18 |            0.11 | terribly     |   422 |  2,196 |  8,526 |
| **necessarily~wrong**       |    3.35 |   783.75 |           0.20 |            0.11 | necessarily  |   211 |    993 |  8,526 |
| **ever~perfect**            |    3.95 |   876.15 |           0.15 |            0.10 | ever         |   206 |  4,776 |  1,280 |
| **that~great**              |    3.84 | 1,174.94 |           0.13 |            0.09 | that         |   292 |  4,538 |  2,147 |
| **remotely~close**          |    3.34 |   829.53 |           0.11 |            0.08 | remotely     |   233 |  1,963 |  4,972 |


### Loading `direct` AM scores

 Path: `assoc_df/adv_adj/ANYdirect/extra/AdvAdj_NEQ_any-direct_final-freq_min50x_extra.parq`


_Bigrams with the highest `LRC` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |   `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|-------:|
| **longer~lasting**          |    8.01 |   1,560.03 |           0.11 |            0.10 | longer       |    155 |   1,803 |  1,450 |
| **any~happier**             |    7.87 |   7,348.55 |           0.43 |            0.24 | any          |    830 |  16,176 |  1,909 |
| **necessarily~indicative**  |    7.45 |  10,814.41 |           0.59 |            0.31 | necessarily  |  1,389 |  42,916 |  2,319 |
| **yet~final**               |    6.59 |   4,447.60 |           0.52 |            0.27 | yet          |    640 |  53,779 |  1,212 |
| **immediately~clear**       |    5.43 | 141,537.62 |           0.41 |            0.35 | immediately  | 24,476 |  57,730 | 83,958 |
| **ever~closer**             |    5.28 |   1,788.53 |           0.08 |            0.06 | ever         |    299 |  10,849 |  3,488 |
| **remotely~comparable**     |    5.03 |     756.79 |           0.05 |            0.04 | remotely     |    125 |   6,109 |  2,443 |
| **exactly~stellar**         |    4.55 |     868.83 |           0.21 |            0.10 | exactly      |    170 |  44,378 |    801 |
| **particularly~noteworthy** |    4.37 |   1,627.29 |           0.25 |            0.13 | particularly |    360 |  76,722 |  1,370 |
| **terribly~surprising**     |    3.81 |   3,578.57 |           0.05 |            0.05 | terribly     |    949 |  19,801 | 18,886 |
| **that~great**              |    3.49 |  32,446.71 |           0.22 |            0.14 | that         | 11,055 | 166,680 | 45,537 |


_Bigrams with the highest `G2` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |    `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|--------:|
| **immediately~clear**       |    5.43 | 141,537.62 |           0.41 |            0.35 | immediately  | 24,476 |  57,730 |  83,958 |
| **yet~clear**               |    3.97 |  39,559.63 |           0.18 |            0.15 | yet          | 10,411 |  53,779 |  83,958 |
| **that~great**              |    3.49 |  32,446.71 |           0.22 |            0.14 | that         | 11,055 | 166,680 |  45,537 |
| **any~better**              |    5.34 |  29,300.27 |           0.30 |            0.20 | any          |  5,022 |  16,176 |  49,936 |
| **exactly~sure**            |    3.23 |  25,676.86 |           0.18 |            0.12 | exactly      |  8,797 |  44,378 | 134,058 |
| **necessarily~true**        |    3.76 |  11,419.84 |           0.09 |            0.08 | necessarily  |  3,242 |  42,916 |  35,146 |
| **particularly~interested** |    2.72 |   6,246.34 |           0.07 |            0.05 | particularly |  2,816 |  76,722 |  34,247 |
| **terribly~surprising**     |    3.81 |   3,578.57 |           0.05 |            0.05 | terribly     |    949 |  19,801 |  18,886 |
| **remotely~close**          |    3.75 |   2,790.99 |           0.11 |            0.06 | remotely     |    729 |   6,109 |  46,485 |
| **ever~closer**             |    5.28 |   1,788.53 |           0.08 |            0.06 | ever         |    299 |  10,849 |   3,488 |
| **longer~lasting**          |    8.01 |   1,560.03 |           0.11 |            0.10 | longer       |    155 |   1,803 |   1,450 |


_Bigrams with the highest `deltaP_max` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |   `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|-------:|
| **necessarily~indicative**  |    7.45 |  10,814.41 |           0.59 |            0.31 | necessarily  |  1,389 |  42,916 |  2,319 |
| **yet~final**               |    6.59 |   4,447.60 |           0.52 |            0.27 | yet          |    640 |  53,779 |  1,212 |
| **any~happier**             |    7.87 |   7,348.55 |           0.43 |            0.24 | any          |    830 |  16,176 |  1,909 |
| **immediately~clear**       |    5.43 | 141,537.62 |           0.41 |            0.35 | immediately  | 24,476 |  57,730 | 83,958 |
| **particularly~noteworthy** |    4.37 |   1,627.29 |           0.25 |            0.13 | particularly |    360 |  76,722 |  1,370 |
| **that~uncommon**           |    3.31 |   2,369.26 |           0.23 |            0.11 | that         |    802 | 166,680 |  3,193 |
| **exactly~stellar**         |    4.55 |     868.83 |           0.21 |            0.10 | exactly      |    170 |  44,378 |    801 |
| **remotely~close**          |    3.75 |   2,790.99 |           0.11 |            0.06 | remotely     |    729 |   6,109 | 46,485 |
| **longer~lasting**          |    8.01 |   1,560.03 |           0.11 |            0.10 | longer       |    155 |   1,803 |  1,450 |
| **ever~closer**             |    5.28 |   1,788.53 |           0.08 |            0.06 | ever         |    299 |  10,849 |  3,488 |
| **terribly~surprising**     |    3.81 |   3,578.57 |           0.05 |            0.05 | terribly     |    949 |  19,801 | 18,886 |


_Bigrams with the highest `deltaP_mean` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |    `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|--------:|
| **immediately~clear**       |    5.43 | 141,537.62 |           0.41 |            0.35 | immediately  | 24,476 |  57,730 |  83,958 |
| **necessarily~indicative**  |    7.45 |  10,814.41 |           0.59 |            0.31 | necessarily  |  1,389 |  42,916 |   2,319 |
| **yet~final**               |    6.59 |   4,447.60 |           0.52 |            0.27 | yet          |    640 |  53,779 |   1,212 |
| **any~happier**             |    7.87 |   7,348.55 |           0.43 |            0.24 | any          |    830 |  16,176 |   1,909 |
| **that~great**              |    3.49 |  32,446.71 |           0.22 |            0.14 | that         | 11,055 | 166,680 |  45,537 |
| **particularly~noteworthy** |    4.37 |   1,627.29 |           0.25 |            0.13 | particularly |    360 |  76,722 |   1,370 |
| **exactly~sure**            |    3.23 |  25,676.86 |           0.18 |            0.12 | exactly      |  8,797 |  44,378 | 134,058 |
| **longer~lasting**          |    8.01 |   1,560.03 |           0.11 |            0.10 | longer       |    155 |   1,803 |   1,450 |
| **remotely~close**          |    3.75 |   2,790.99 |           0.11 |            0.06 | remotely     |    729 |   6,109 |  46,485 |
| **ever~closer**             |    5.28 |   1,788.53 |           0.08 |            0.06 | ever         |    299 |  10,849 |   3,488 |
| **terribly~surprising**     |    3.81 |   3,578.57 |           0.05 |            0.05 | terribly     |    949 |  19,801 |  18,886 |




```python
blam_df = pd.concat(blam_dfs.values()).sort_values(blind_priority_cols[0], ascending=False)

# print(f'### Top 15 *context-blind* `{blind_priority_cols[0]}` values across all adverbs and datasets\n')
# nb_show_table(blam_df.head(15))
```

```python
print(f'### Top 15 *context-blind* `{blind_priority_cols[0]}` values across all adverbs and datasets\n')
nb_show_table(blam_df.head(15))
```
### Top 15 *context-blind* `LRC` values across all adverbs and datasets


|                                       |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`        | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:--------------------------------------|------:|--------:|--------:|-------:|----------:|:------------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] longer~lasting**         |   155 |    0.11 |    8.01 |   0.11 |  1,560.03 | longer      | lasting    |  1,803 |  1,450 | 6,347,362 |      0.41 |      154.59 |        1.00 |    0.09 |   0.09 |           0.11 |            0.10 |            2.66 | 12.42 |   2.58 | direct      |
| **[_direct_] any~happier**            |   830 |    0.43 |    7.87 |   0.43 |  7,348.55 | any         | happier    | 16,176 |  1,909 | 6,347,362 |      4.87 |      825.13 |        0.99 |    0.05 |   0.05 |           0.43 |            0.24 |            2.50 | 28.64 |   2.23 | direct      |
| **[_direct_] necessarily~indicative** | 1,389 |    0.59 |    7.45 |   0.60 | 10,814.41 | necessarily | indicative | 42,916 |  2,319 | 6,347,362 |     15.68 |    1,373.32 |        0.99 |    0.03 |   0.03 |           0.59 |            0.31 |            2.36 | 36.85 |   1.95 | direct      |
| **[_mirror_] exactly~alike**          |    54 |    0.37 |    7.30 |   0.38 |    517.06 | exactly     | alike      |    862 |    144 |   583,470 |      0.21 |       53.79 |        1.00 |    0.06 |   0.06 |           0.37 |            0.22 |            2.64 |  7.32 |   2.40 | mirror      |
| **[_direct_] any~clearer**            |   361 |    0.35 |    7.19 |   0.35 |  2,983.07 | any         | clearer    | 16,176 |  1,037 | 6,347,362 |      2.64 |      358.36 |        0.99 |    0.02 |   0.02 |           0.35 |            0.18 |            2.33 | 18.86 |   2.14 | direct      |
| **[_direct_] longer~pink**            |    51 |    0.08 |    7.04 |   0.08 |    483.99 | longer      | pink       |  1,803 |    610 | 6,347,362 |      0.17 |       50.83 |        1.00 |    0.03 |   0.03 |           0.08 |            0.06 |            2.52 |  7.12 |   2.47 | direct      |
| **[_direct_] yet~final**              |   640 |    0.52 |    6.59 |   0.53 |  4,447.60 | yet         | final      | 53,779 |  1,212 | 6,347,362 |     10.27 |      629.73 |        0.98 |    0.01 |   0.01 |           0.52 |            0.27 |            2.12 | 24.89 |   1.79 | direct      |
| **[_mirror_] longer~viable**          |    57 |    0.23 |    6.47 |   0.23 |    482.88 | longer      | viable     |    841 |    248 |   583,470 |      0.36 |       56.64 |        0.99 |    0.07 |   0.07 |           0.23 |            0.15 |            2.35 |  7.50 |   2.20 | mirror      |
| **[_direct_] any~closer**             |   600 |    0.17 |    5.99 |   0.17 |  4,000.91 | any         | closer     | 16,176 |  3,488 | 6,347,362 |      8.89 |      591.11 |        0.99 |    0.04 |   0.04 |           0.17 |            0.10 |            1.93 | 24.13 |   1.83 | direct      |
| **[_mirror_] any~closer**             |    60 |    0.21 |    5.98 |   0.21 |    465.53 | any         | closer     |  1,083 |    285 |   583,470 |      0.53 |       59.47 |        0.99 |    0.06 |   0.06 |           0.21 |            0.13 |            2.18 |  7.68 |   2.05 | mirror      |
| **[_direct_] any~worse**              | 1,797 |    0.15 |    5.92 |   0.15 | 11,618.05 | any         | worse      | 16,176 | 11,891 | 6,347,362 |     30.30 |    1,766.70 |        0.98 |    0.11 |   0.11 |           0.15 |            0.13 |            1.89 | 41.68 |   1.77 | direct      |
| **[_direct_] any~easier**             | 1,624 |    0.12 |    5.60 |   0.13 |  9,840.90 | any         | easier     | 16,176 | 12,945 | 6,347,362 |     32.99 |    1,591.01 |        0.98 |    0.10 |   0.10 |           0.12 |            0.11 |            1.79 | 39.48 |   1.69 | direct      |
| **[_direct_] any~simpler**            |   232 |    0.15 |    5.58 |   0.15 |  1,488.36 | any         | simpler    | 16,176 |  1,501 | 6,347,362 |      3.83 |      228.17 |        0.98 |    0.01 |   0.01 |           0.15 |            0.08 |            1.86 | 14.98 |   1.78 | direct      |
| **[_mirror_] any~better**             |   386 |    0.10 |    5.56 |   0.10 |  2,549.65 | any         | better     |  1,083 |  3,681 |   583,470 |      6.83 |      379.17 |        0.98 |    0.35 |   0.36 |           0.35 |            0.23 |            1.99 | 19.30 |   1.75 | mirror      |
| **[_direct_] yet~official**           |   352 |    0.36 |    5.56 |   0.37 |  2,112.24 | yet         | official   | 53,779 |    957 | 6,347,362 |      8.11 |      343.89 |        0.98 |    0.01 |   0.01 |           0.36 |            0.18 |            1.84 | 18.33 |   1.64 | direct      |




```python
# md_frame_code("""nb_show_table(blam_df
#               .filter(like='mirror', axis=0)
#               .sample(5)
#               .filter(blind_priority_cols)
#               .sort_values(blind_priority_cols[0], ascending=False))""")
# nb_show_table(blam_df
#               .filter(like='mirror', axis=0)
#               .sample(5)
#               .filter(blind_priority_cols)
#               .sort_values(blind_priority_cols[0], ascending=False))
```


```python
nb_show_table(blam_df
              .filter(like='mirror', axis=0)
              .sample(5)
              .filter(blind_priority_cols)
              .sort_values(blind_priority_cols[0], ascending=False))
```


|                                     |   `LRC` |   `G2` |   `deltaP_max` |   `deltaP_mean` |
|:------------------------------------|--------:|-------:|---------------:|----------------:|
| **[_mirror_] particularly~unusual** |    3.05 | 539.33 |           0.17 |            0.09 |
| **[_mirror_] ever~able**            |    2.60 | 380.42 |           0.07 |            0.05 |
| **[_mirror_] particularly~strong**  |    0.00 |  26.82 |           0.02 |            0.01 |
| **[_mirror_] that~difficult**       |    0.00 |   5.33 |           0.00 |            0.00 |
| **[_mirror_] ever~true**            |    0.00 |  24.48 |           0.01 |            0.01 |




```python
perspective_cols = blind_priority_cols + ['dP1', 'dP2', 'f', 'f2', 'unexp_r']
filter_blam = (blam_df.copy()
               .filter(perspective_cols)
               .round(2))
perspectives = [perspective_cols[i:i+2] for i in range(0,2)]
perspectives.extend([['dP1', 'LRC'], ['dP2', 'LRC']])

for ia, _adv in enumerate(adv_list[:8], start=1):
    print(f'### {ia}. Sampling _{_adv}_ context-blind bigram AMs\n')
    adv_blam = filter_blam.filter(like=f' {_adv}~', axis=0)
                
    for ip, col_list in enumerate(perspectives, start=1): 
        print(f'#### {ia}.{ip}. _{_adv}_ Highest and Lowest `{col_list[0]}`\n\n(_tie-breaker: `{col_list[1]}`_)')
        x_blam = adv_blam.sort_values(col_list, ascending=False)
        nb_show_table(pd.concat([x_blam.head(3),
                                 x_blam.tail(3)]))
    print('\n---\n')
```

### 1. Sampling _necessarily_ context-blind bigram AMs

#### 1.1. _necessarily_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] necessarily~indicative**     |    7.45 | 10,814.41 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,319 |        0.99 |
| **[_direct_] necessarily~cause**          |    5.20 |    349.89 |           0.41 |            0.20 |    0.41 |    0.00 |    52 |     126 |        0.98 |
| **[_direct_] necessarily~representative** |    4.71 |  2,409.17 |           0.18 |            0.10 |    0.18 |    0.01 |   487 |   2,559 |        0.96 |
| **[_direct_] necessarily~important**      |   -1.69 |   -861.49 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   204 | 138,658 |       -3.60 |
| **[_direct_] necessarily~sure**           |   -1.71 |   -842.55 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,058 |       -3.67 |
| **[_direct_] necessarily~different**      |   -2.00 |   -631.69 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,019 |       -5.94 |

#### 1.2. _necessarily_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                       |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:--------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] necessarily~true**       |    3.76 | 11,419.84 |           0.09 |            0.08 |    0.09 |    0.07 | 3,242 |  35,146 |        0.93 |
| **[_direct_] necessarily~indicative** |    7.45 | 10,814.41 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,319 |        0.99 |
| **[_direct_] necessarily~better**     |    2.34 |  3,509.08 |           0.04 |            0.03 |    0.03 |    0.04 | 1,889 |  49,936 |        0.82 |
| **[_direct_] necessarily~different**  |   -2.00 |   -631.69 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,019 |       -5.94 |
| **[_direct_] necessarily~sure**       |   -1.71 |   -842.55 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,058 |       -3.67 |
| **[_direct_] necessarily~important**  |   -1.69 |   -861.49 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   204 | 138,658 |       -3.60 |

#### 1.3. _necessarily_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] necessarily~indicative**     |    7.45 | 10,814.41 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,319 |        0.99 |
| **[_direct_] necessarily~cause**          |    5.20 |    349.89 |           0.41 |            0.20 |    0.41 |    0.00 |    52 |     126 |        0.98 |
| **[_direct_] necessarily~representative** |    4.71 |  2,409.17 |           0.18 |            0.10 |    0.18 |    0.01 |   487 |   2,559 |        0.96 |
| **[_direct_] necessarily~important**      |   -1.69 |   -861.49 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   204 | 138,658 |       -3.60 |
| **[_direct_] necessarily~sure**           |   -1.71 |   -842.55 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,058 |       -3.67 |
| **[_direct_] necessarily~different**      |   -2.00 |   -631.69 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,019 |       -5.94 |

#### 1.4. _necessarily_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] necessarily~wrong**     |    3.35 |    783.75 |           0.20 |            0.11 |    0.02 |    0.20 |   211 |   8,526 |        0.93 |
| **[_direct_] necessarily~true**      |    3.76 | 11,419.84 |           0.09 |            0.08 |    0.09 |    0.07 | 3,242 |  35,146 |        0.93 |
| **[_mirror_] necessarily~true**      |    2.30 |    159.70 |           0.05 |            0.03 |    0.02 |    0.05 |    53 |   2,870 |        0.91 |
| **[_direct_] necessarily~different** |   -2.00 |   -631.69 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,019 |       -5.94 |
| **[_direct_] necessarily~important** |   -1.69 |   -861.49 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   204 | 138,658 |       -3.60 |
| **[_direct_] necessarily~sure**      |   -1.71 |   -842.55 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,058 |       -3.67 |


---

### 2. Sampling _that_ context-blind bigram AMs

#### 2.1. _that_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_mirror_] that~great**    |    3.84 |  1,174.94 |           0.13 |            0.09 |    0.13 |    0.06 |    292 |   2,147 |        0.94 |
| **[_direct_] that~great**    |    3.49 | 32,446.71 |           0.22 |            0.14 |    0.22 |    0.06 | 11,055 |  45,537 |        0.89 |
| **[_direct_] that~uncommon** |    3.31 |  2,369.26 |           0.23 |            0.11 |    0.23 |    0.00 |    802 |   3,193 |        0.90 |
| **[_direct_] that~better**   |   -2.69 | -1,775.57 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    135 |  49,936 |       -8.71 |
| **[_direct_] that~likely**   |   -2.91 | -1,893.65 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    111 |  49,995 |      -10.83 |
| **[_direct_] that~sure**     |   -3.16 | -5,111.81 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    299 | 134,058 |      -10.77 |

#### 2.2. _that_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:--------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] that~great** |    3.49 | 32,446.71 |           0.22 |            0.14 |    0.22 |    0.06 | 11,055 |  45,537 |        0.89 |
| **[_direct_] that~bad**   |    2.51 | 31,136.23 |           0.11 |            0.10 |    0.11 |    0.08 | 16,609 | 119,777 |        0.81 |
| **[_direct_] that~hard**  |    3.29 | 27,114.66 |           0.19 |            0.12 |    0.19 |    0.05 |  9,964 |  45,416 |        0.88 |
| **[_direct_] that~clear** |   -1.77 | -1,904.56 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    525 |  83,958 |       -3.20 |
| **[_direct_] that~many**  |   -2.51 | -3,118.03 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    351 |  97,776 |       -6.32 |
| **[_direct_] that~sure**  |   -3.16 | -5,111.81 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    299 | 134,058 |      -10.77 |

#### 2.3. _that_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] that~uncommon** |    3.31 |  2,369.26 |           0.23 |            0.11 |    0.23 |    0.00 |    802 |   3,193 |        0.90 |
| **[_direct_] that~great**    |    3.49 | 32,446.71 |           0.22 |            0.14 |    0.22 |    0.06 | 11,055 |  45,537 |        0.89 |
| **[_direct_] that~hard**     |    3.29 | 27,114.66 |           0.19 |            0.12 |    0.19 |    0.05 |  9,964 |  45,416 |        0.88 |
| **[_direct_] that~better**   |   -2.69 | -1,775.57 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    135 |  49,936 |       -8.71 |
| **[_direct_] that~likely**   |   -2.91 | -1,893.65 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    111 |  49,995 |      -10.83 |
| **[_direct_] that~sure**     |   -3.16 | -5,111.81 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    299 | 134,058 |      -10.77 |

#### 2.4. _that_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_mirror_] that~simple** |    2.77 |  1,267.95 |           0.10 |            0.08 |    0.06 |    0.10 |    487 |   7,580 |        0.88 |
| **[_mirror_] that~easy**   |    2.63 |  1,130.07 |           0.09 |            0.07 |    0.05 |    0.09 |    464 |   7,897 |        0.87 |
| **[_direct_] that~bad**    |    2.51 | 31,136.23 |           0.11 |            0.10 |    0.11 |    0.08 | 16,609 | 119,777 |        0.81 |
| **[_direct_] that~better** |   -2.69 | -1,775.57 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    135 |  49,936 |       -8.71 |
| **[_direct_] that~likely** |   -2.91 | -1,893.65 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    111 |  49,995 |      -10.83 |
| **[_direct_] that~sure**   |   -3.16 | -5,111.81 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    299 | 134,058 |      -10.77 |


---

### 3. Sampling _exactly_ context-blind bigram AMs

#### 3.1. _exactly_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] exactly~alike**   |    7.30 |    517.06 |           0.37 |            0.22 |    0.37 |    0.06 |    54 |     144 |        1.00 |
| **[_direct_] exactly~stellar** |    4.55 |    868.83 |           0.21 |            0.10 |    0.21 |    0.00 |   170 |     801 |        0.97 |
| **[_direct_] exactly~alike**   |    3.93 |    704.69 |           0.14 |            0.07 |    0.14 |    0.00 |   162 |   1,092 |        0.95 |
| **[_direct_] exactly~simple**  |   -1.49 |   -324.42 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  47,134 |       -4.15 |
| **[_direct_] exactly~good**    |   -1.97 | -1,448.89 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   264 | 202,048 |       -4.35 |
| **[_direct_] exactly~bad**     |   -2.11 |   -969.14 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   124 | 119,777 |       -5.75 |

#### 3.2. _exactly_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] exactly~sure**   |    3.23 | 25,676.86 |           0.18 |            0.12 |    0.06 |    0.18 | 8,797 | 134,058 |        0.89 |
| **[_direct_] exactly~new**    |    3.05 |  3,724.27 |           0.06 |            0.04 |    0.06 |    0.03 | 1,372 |  21,548 |        0.89 |
| **[_direct_] exactly~true**   |    2.41 |  2,836.77 |           0.03 |            0.03 |    0.03 |    0.03 | 1,456 |  35,146 |        0.83 |
| **[_direct_] exactly~simple** |   -1.49 |   -324.42 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  47,134 |       -4.15 |
| **[_direct_] exactly~bad**    |   -2.11 |   -969.14 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   124 | 119,777 |       -5.75 |
| **[_direct_] exactly~good**   |   -1.97 | -1,448.89 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   264 | 202,048 |       -4.35 |

#### 3.3. _exactly_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] exactly~alike**   |    7.30 |    517.06 |           0.37 |            0.22 |    0.37 |    0.06 |    54 |     144 |        1.00 |
| **[_direct_] exactly~stellar** |    4.55 |    868.83 |           0.21 |            0.10 |    0.21 |    0.00 |   170 |     801 |        0.97 |
| **[_direct_] exactly~alike**   |    3.93 |    704.69 |           0.14 |            0.07 |    0.14 |    0.00 |   162 |   1,092 |        0.95 |
| **[_direct_] exactly~simple**  |   -1.49 |   -324.42 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  47,134 |       -4.15 |
| **[_direct_] exactly~good**    |   -1.97 | -1,448.89 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   264 | 202,048 |       -4.35 |
| **[_direct_] exactly~bad**     |   -2.11 |   -969.14 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   124 | 119,777 |       -5.75 |

#### 3.4. _exactly_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] exactly~sure**   |    3.23 | 25,676.86 |           0.18 |            0.12 |    0.06 |    0.18 | 8,797 | 134,058 |        0.89 |
| **[_mirror_] exactly~sure**   |    3.44 |    583.16 |           0.16 |            0.09 |    0.02 |    0.16 |   148 |   5,983 |        0.94 |
| **[_mirror_] exactly~right**  |    3.54 |    302.37 |           0.08 |            0.05 |    0.03 |    0.08 |    68 |   2,019 |        0.96 |
| **[_direct_] exactly~simple** |   -1.49 |   -324.42 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  47,134 |       -4.15 |
| **[_direct_] exactly~bad**    |   -2.11 |   -969.14 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   124 | 119,777 |       -5.75 |
| **[_direct_] exactly~good**   |   -1.97 | -1,448.89 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   264 | 202,048 |       -4.35 |


---

### 4. Sampling _any_ context-blind bigram AMs

#### 4.1. _any_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                            |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] any~happier** |    7.87 | 7,348.55 |           0.43 |            0.24 |    0.43 |    0.05 |   830 |   1,909 |        0.99 |
| **[_direct_] any~clearer** |    7.19 | 2,983.07 |           0.35 |            0.18 |    0.35 |    0.02 |   361 |   1,037 |        0.99 |
| **[_direct_] any~closer**  |    5.99 | 4,000.91 |           0.17 |            0.10 |    0.17 |    0.04 |   600 |   3,488 |        0.99 |
| **[_direct_] any~more**    |    1.42 |   451.35 |           0.02 |            0.01 |    0.01 |    0.02 |   410 |  45,770 |        0.72 |
| **[_direct_] any~lower**   |    1.17 |   113.92 |           0.01 |            0.01 |    0.01 |    0.00 |    80 |   7,150 |        0.77 |
| **[_direct_] any~good**    |   -1.11 |  -344.43 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   160 | 202,048 |       -2.22 |

#### 4.2. _any_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] any~better**  |    5.34 | 29,300.27 |           0.30 |            0.20 |    0.10 |    0.30 | 5,022 |  49,936 |        0.97 |
| **[_direct_] any~worse**   |    5.92 | 11,618.05 |           0.15 |            0.13 |    0.15 |    0.11 | 1,797 |  11,891 |        0.98 |
| **[_direct_] any~easier**  |    5.60 |  9,840.90 |           0.12 |            0.11 |    0.12 |    0.10 | 1,624 |  12,945 |        0.98 |
| **[_direct_] any~smaller** |    1.46 |    126.13 |           0.01 |            0.01 |    0.01 |    0.00 |    69 |   4,798 |        0.82 |
| **[_direct_] any~lower**   |    1.17 |    113.92 |           0.01 |            0.01 |    0.01 |    0.00 |    80 |   7,150 |        0.77 |
| **[_direct_] any~good**    |   -1.11 |   -344.43 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   160 | 202,048 |       -2.22 |

#### 4.3. _any_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] any~happier** |    7.87 | 7,348.55 |           0.43 |            0.24 |    0.43 |    0.05 |   830 |   1,909 |        0.99 |
| **[_direct_] any~clearer** |    7.19 | 2,983.07 |           0.35 |            0.18 |    0.35 |    0.02 |   361 |   1,037 |        0.99 |
| **[_mirror_] any~closer**  |    5.98 |   465.53 |           0.21 |            0.13 |    0.21 |    0.06 |    60 |     285 |        0.99 |
| **[_direct_] any~more**    |    1.42 |   451.35 |           0.02 |            0.01 |    0.01 |    0.02 |   410 |  45,770 |        0.72 |
| **[_direct_] any~lower**   |    1.17 |   113.92 |           0.01 |            0.01 |    0.01 |    0.00 |    80 |   7,150 |        0.77 |
| **[_direct_] any~good**    |   -1.11 |  -344.43 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   160 | 202,048 |       -2.22 |

#### 4.4. _any_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] any~better**  |    5.56 |  2,549.65 |           0.35 |            0.23 |    0.10 |    0.35 |   386 |   3,681 |        0.98 |
| **[_direct_] any~better**  |    5.34 | 29,300.27 |           0.30 |            0.20 |    0.10 |    0.30 | 5,022 |  49,936 |        0.97 |
| **[_direct_] any~worse**   |    5.92 | 11,618.05 |           0.15 |            0.13 |    0.15 |    0.11 | 1,797 |  11,891 |        0.98 |
| **[_direct_] any~smaller** |    1.46 |    126.13 |           0.01 |            0.01 |    0.01 |    0.00 |    69 |   4,798 |        0.82 |
| **[_direct_] any~lower**   |    1.17 |    113.92 |           0.01 |            0.01 |    0.01 |    0.00 |    80 |   7,150 |        0.77 |
| **[_direct_] any~good**    |   -1.11 |   -344.43 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   160 | 202,048 |       -2.22 |


---

### 5. Sampling _remotely_ context-blind bigram AMs

#### 5.1. _remotely_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~comparable** |    5.03 |   756.79 |           0.05 |            0.04 |    0.05 |    0.02 |   125 |   2,443 |        0.98 |
| **[_direct_] remotely~close**      |    3.75 | 2,790.99 |           0.11 |            0.06 |    0.01 |    0.11 |   729 |  46,485 |        0.94 |
| **[_mirror_] remotely~close**      |    3.34 |   829.53 |           0.11 |            0.08 |    0.04 |    0.11 |   233 |   4,972 |        0.93 |
| **[_direct_] remotely~accurate**   |    0.18 |    37.05 |           0.01 |            0.00 |    0.00 |    0.01 |    51 |  19,706 |        0.63 |
| **[_direct_] remotely~ready**      |    0.00 |    23.54 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,641 |        0.51 |
| **[_direct_] remotely~good**       |   -0.98 |  -156.71 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    50 | 202,048 |       -2.89 |

#### 5.2. _remotely_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~close**      |    3.75 | 2,790.99 |           0.11 |            0.06 |    0.01 |    0.11 |   729 |  46,485 |        0.94 |
| **[_direct_] remotely~interested** |    3.05 | 1,113.00 |           0.05 |            0.03 |    0.01 |    0.05 |   365 |  34,247 |        0.91 |
| **[_mirror_] remotely~close**      |    3.34 |   829.53 |           0.11 |            0.08 |    0.04 |    0.11 |   233 |   4,972 |        0.93 |
| **[_direct_] remotely~accurate**   |    0.18 |    37.05 |           0.01 |            0.00 |    0.00 |    0.01 |    51 |  19,706 |        0.63 |
| **[_direct_] remotely~ready**      |    0.00 |    23.54 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,641 |        0.51 |
| **[_direct_] remotely~good**       |   -0.98 |  -156.71 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    50 | 202,048 |       -2.89 |

#### 5.3. _remotely_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                    |   `LRC` |    `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|--------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~comparable** |    5.03 |  756.79 |           0.05 |            0.04 |    0.05 |    0.02 |   125 |   2,443 |        0.98 |
| **[_mirror_] remotely~similar**    |    3.08 |  300.50 |           0.05 |            0.04 |    0.05 |    0.04 |    82 |   1,597 |        0.93 |
| **[_mirror_] remotely~close**      |    3.34 |  829.53 |           0.11 |            0.08 |    0.04 |    0.11 |   233 |   4,972 |        0.93 |
| **[_direct_] remotely~accurate**   |    0.18 |   37.05 |           0.01 |            0.00 |    0.00 |    0.01 |    51 |  19,706 |        0.63 |
| **[_direct_] remotely~ready**      |    0.00 |   23.54 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,641 |        0.51 |
| **[_direct_] remotely~good**       |   -0.98 | -156.71 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    50 | 202,048 |       -2.89 |

#### 5.4. _remotely_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~close**      |    3.75 | 2,790.99 |           0.11 |            0.06 |    0.01 |    0.11 |   729 |  46,485 |        0.94 |
| **[_mirror_] remotely~close**      |    3.34 |   829.53 |           0.11 |            0.08 |    0.04 |    0.11 |   233 |   4,972 |        0.93 |
| **[_direct_] remotely~interested** |    3.05 | 1,113.00 |           0.05 |            0.03 |    0.01 |    0.05 |   365 |  34,247 |        0.91 |
| **[_direct_] remotely~accurate**   |    0.18 |    37.05 |           0.01 |            0.00 |    0.00 |    0.01 |    51 |  19,706 |        0.63 |
| **[_direct_] remotely~ready**      |    0.00 |    23.54 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,641 |        0.51 |
| **[_direct_] remotely~good**       |   -0.98 |  -156.71 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    50 | 202,048 |       -2.89 |


---

### 6. Sampling _yet_ context-blind bigram AMs

#### 6.1. _yet_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                             |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] yet~final**    |    6.59 |  4,447.60 |           0.52 |            0.27 |    0.52 |    0.01 |   640 |   1,212 |        0.98 |
| **[_direct_] yet~official** |    5.56 |  2,112.24 |           0.36 |            0.18 |    0.36 |    0.01 |   352 |     957 |        0.98 |
| **[_direct_] yet~ready**    |    5.21 | 39,484.24 |           0.25 |            0.19 |    0.25 |    0.14 | 7,505 |  29,641 |        0.97 |
| **[_direct_] yet~big**      |   -1.60 |   -370.58 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    66 |  42,692 |       -4.48 |
| **[_direct_] yet~popular**  |   -1.83 |   -490.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    69 |  51,847 |       -5.37 |
| **[_direct_] yet~good**     |   -2.62 | -2,242.15 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   195 | 202,048 |       -7.78 |

#### 6.2. _yet_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] yet~clear**     |    3.97 | 39,559.63 |           0.18 |            0.15 |    0.12 |    0.18 | 10,411 |  83,958 |        0.93 |
| **[_direct_] yet~ready**     |    5.21 | 39,484.24 |           0.25 |            0.19 |    0.25 |    0.14 |  7,505 |  29,641 |        0.97 |
| **[_direct_] yet~available** |    3.45 | 23,243.68 |           0.13 |            0.10 |    0.08 |    0.13 |  7,434 |  81,972 |        0.91 |
| **[_direct_] yet~big**       |   -1.60 |   -370.58 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     66 |  42,692 |       -4.48 |
| **[_direct_] yet~popular**   |   -1.83 |   -490.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     69 |  51,847 |       -5.37 |
| **[_direct_] yet~good**      |   -2.62 | -2,242.15 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |    195 | 202,048 |       -7.78 |

#### 6.3. _yet_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                             |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] yet~final**    |    6.59 |  4,447.60 |           0.52 |            0.27 |    0.52 |    0.01 |   640 |   1,212 |        0.98 |
| **[_direct_] yet~official** |    5.56 |  2,112.24 |           0.36 |            0.18 |    0.36 |    0.01 |   352 |     957 |        0.98 |
| **[_direct_] yet~complete** |    5.19 | 11,415.79 |           0.26 |            0.15 |    0.26 |    0.04 | 2,175 |   8,263 |        0.97 |
| **[_direct_] yet~big**      |   -1.60 |   -370.58 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    66 |  42,692 |       -4.48 |
| **[_direct_] yet~popular**  |   -1.83 |   -490.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    69 |  51,847 |       -5.37 |
| **[_direct_] yet~good**     |   -2.62 | -2,242.15 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   195 | 202,048 |       -7.78 |

#### 6.4. _yet_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] yet~clear**     |    3.97 | 39,559.63 |           0.18 |            0.15 |    0.12 |    0.18 | 10,411 |  83,958 |        0.93 |
| **[_direct_] yet~ready**     |    5.21 | 39,484.24 |           0.25 |            0.19 |    0.25 |    0.14 |  7,505 |  29,641 |        0.97 |
| **[_direct_] yet~available** |    3.45 | 23,243.68 |           0.13 |            0.10 |    0.08 |    0.13 |  7,434 |  81,972 |        0.91 |
| **[_direct_] yet~big**       |   -1.60 |   -370.58 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     66 |  42,692 |       -4.48 |
| **[_direct_] yet~popular**   |   -1.83 |   -490.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     69 |  51,847 |       -5.37 |
| **[_direct_] yet~good**      |   -2.62 | -2,242.15 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |    195 | 202,048 |       -7.78 |


---

### 7. Sampling _immediately_ context-blind bigram AMs

#### 7.1. _immediately_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~clear**     |    5.43 | 141,537.62 |           0.41 |            0.35 |    0.29 |    0.41 | 24,476 |  83,958 |        0.97 |
| **[_mirror_] immediately~available** |    5.43 |   1,249.24 |           0.32 |            0.19 |    0.06 |    0.32 |    187 |   3,078 |        0.98 |
| **[_direct_] immediately~available** |    5.19 | 115,831.59 |           0.36 |            0.31 |    0.25 |    0.36 | 21,281 |  81,972 |        0.96 |
| **[_direct_] immediately~necessary** |   -0.56 |     -88.22 |          -0.00 |           -0.00 |   -0.01 |   -0.00 |     56 |  17,339 |       -1.82 |
| **[_direct_] immediately~ready**     |   -1.30 |    -247.25 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     58 |  29,641 |       -3.65 |
| **[_direct_] immediately~sure**      |   -2.53 |  -1,586.33 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    139 | 134,058 |       -7.77 |

#### 7.2. _immediately_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~clear**     |    5.43 | 141,537.62 |           0.41 |            0.35 |    0.29 |    0.41 | 24,476 |  83,958 |        0.97 |
| **[_direct_] immediately~available** |    5.19 | 115,831.59 |           0.36 |            0.31 |    0.25 |    0.36 | 21,281 |  81,972 |        0.96 |
| **[_direct_] immediately~apparent**  |    4.73 |  10,005.27 |           0.21 |            0.12 |    0.21 |    0.04 |  2,134 |   9,794 |        0.96 |
| **[_direct_] immediately~useful**    |   -0.54 |     -90.32 |          -0.00 |           -0.00 |   -0.01 |   -0.00 |     68 |  19,602 |       -1.62 |
| **[_direct_] immediately~ready**     |   -1.30 |    -247.25 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     58 |  29,641 |       -3.65 |
| **[_direct_] immediately~sure**      |   -2.53 |  -1,586.33 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    139 | 134,058 |       -7.77 |

#### 7.3. _immediately_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~reachable** |    4.75 |     608.82 |           0.31 |            0.16 |    0.31 |    0.00 |    110 |     342 |        0.97 |
| **[_direct_] immediately~clear**     |    5.43 | 141,537.62 |           0.41 |            0.35 |    0.29 |    0.41 | 24,476 |  83,958 |        0.97 |
| **[_direct_] immediately~adjacent**  |    4.51 |     507.33 |           0.29 |            0.14 |    0.29 |    0.00 |     95 |     321 |        0.97 |
| **[_direct_] immediately~necessary** |   -0.56 |     -88.22 |          -0.00 |           -0.00 |   -0.01 |   -0.00 |     56 |  17,339 |       -1.82 |
| **[_direct_] immediately~ready**     |   -1.30 |    -247.25 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     58 |  29,641 |       -3.65 |
| **[_direct_] immediately~sure**      |   -2.53 |  -1,586.33 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    139 | 134,058 |       -7.77 |

#### 7.4. _immediately_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~clear**     |    5.43 | 141,537.62 |           0.41 |            0.35 |    0.29 |    0.41 | 24,476 |  83,958 |        0.97 |
| **[_direct_] immediately~available** |    5.19 | 115,831.59 |           0.36 |            0.31 |    0.25 |    0.36 | 21,281 |  81,972 |        0.96 |
| **[_mirror_] immediately~available** |    5.43 |   1,249.24 |           0.32 |            0.19 |    0.06 |    0.32 |    187 |   3,078 |        0.98 |
| **[_direct_] immediately~necessary** |   -0.56 |     -88.22 |          -0.00 |           -0.00 |   -0.01 |   -0.00 |     56 |  17,339 |       -1.82 |
| **[_direct_] immediately~ready**     |   -1.30 |    -247.25 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     58 |  29,641 |       -3.65 |
| **[_direct_] immediately~sure**      |   -2.53 |  -1,586.33 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    139 | 134,058 |       -7.77 |


---

### 8. Sampling _ever_ context-blind bigram AMs

#### 8.1. _ever_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                               |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] ever~closer**    |    5.28 | 1,788.53 |           0.08 |            0.06 |    0.08 |    0.03 |   299 |   3,488 |        0.98 |
| **[_direct_] ever~present**   |    4.13 | 1,610.82 |           0.04 |            0.03 |    0.04 |    0.03 |   366 |   9,428 |        0.96 |
| **[_mirror_] ever~perfect**   |    3.95 |   876.15 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,280 |        0.95 |
| **[_direct_] ever~happy**     |    0.00 |    -3.25 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    65 |  47,131 |       -0.24 |
| **[_direct_] ever~available** |   -0.04 |   -33.25 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    78 |  81,972 |       -0.80 |
| **[_direct_] ever~sure**      |   -0.62 |  -115.86 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    88 | 134,058 |       -1.60 |

#### 8.2. _ever_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                               |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] ever~closer**    |    5.28 | 1,788.53 |           0.08 |            0.06 |    0.08 |    0.03 |   299 |   3,488 |        0.98 |
| **[_direct_] ever~present**   |    4.13 | 1,610.82 |           0.04 |            0.03 |    0.04 |    0.03 |   366 |   9,428 |        0.96 |
| **[_mirror_] ever~perfect**   |    3.95 |   876.15 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,280 |        0.95 |
| **[_direct_] ever~happy**     |    0.00 |    -3.25 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    65 |  47,131 |       -0.24 |
| **[_direct_] ever~available** |   -0.04 |   -33.25 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    78 |  81,972 |       -0.80 |
| **[_direct_] ever~sure**      |   -0.62 |  -115.86 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    88 | 134,058 |       -1.60 |

#### 8.3. _ever_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |    `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|--------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] ever~perfect**   |    3.95 |  876.15 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,280 |        0.95 |
| **[_mirror_] ever~certain**   |    3.22 |  499.66 |           0.10 |            0.07 |    0.10 |    0.03 |   143 |   1,284 |        0.93 |
| **[_mirror_] ever~enough**    |    3.22 |  510.66 |           0.10 |            0.07 |    0.10 |    0.03 |   147 |   1,334 |        0.93 |
| **[_mirror_] ever~wrong**     |    0.00 |   13.34 |           0.01 |            0.01 |    0.00 |    0.01 |   102 |   8,526 |        0.32 |
| **[_direct_] ever~available** |   -0.04 |  -33.25 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    78 |  81,972 |       -0.80 |
| **[_direct_] ever~sure**      |   -0.62 | -115.86 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    88 | 134,058 |       -1.60 |

#### 8.4. _ever_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |    `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|--------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] ever~easy**      |    2.15 |  705.39 |           0.06 |            0.05 |    0.04 |    0.06 |   368 |   7,897 |        0.82 |
| **[_mirror_] ever~perfect**   |    3.95 |  876.15 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,280 |        0.95 |
| **[_mirror_] ever~good**      |    1.01 |  231.27 |           0.04 |            0.03 |    0.01 |    0.04 |   300 |  13,484 |        0.63 |
| **[_direct_] ever~possible**  |    0.00 |   22.33 |           0.00 |            0.00 |    0.00 |    0.00 |    89 |  30,222 |        0.42 |
| **[_direct_] ever~available** |   -0.04 |  -33.25 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    78 |  81,972 |       -0.80 |
| **[_direct_] ever~sure**      |   -0.62 | -115.86 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    88 | 134,058 |       -1.60 |


---




```python
hits_df = load_hit_table(
    adv_set=set(adv_list), 
    adv_floor=ADV_F_FLOOR, tag_top_dir=TAG_TOP_DIR, 
    pos_hits=POS_HITS_PATH, neg_hits=NEG_HITS_PATH)

```

Saving as parquet
  partitioned by `['adv_form_lower']`...

| adv_form_lower   |   count |
|:-----------------|--------:|
| that             |  47,189 |
| particularly     |  36,679 |
| yet              |  16,456 |
| immediately      |  16,325 |
| exactly          |  12,840 |
| necessarily      |  12,013 |
| terribly         |   6,725 |
| ever             |   6,616 |
| any              |   5,029 |
| remotely         |   2,070 |
| longer           |     816 |

> no more than 4,900 rows per individual `group-[#].parquet`
  - max rows in writing batch = 2,451
  - min rows in writing batch = 408

✓ Sample of bigram tokens for `NEQ-Top8[5000]`  successfully saved as  
> "/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8adv_sample-hits_2024-08-06.parq"
* Total time to write partitioned parquet ⇾  `00:00:00.574`


<!-- 
Saving as parquet
  partitioned by `['adv_form_lower']`...

| adv_form_lower   |   count |
|:-----------------|--------:|
| that             |  47,187 |
| particularly     |  35,928 |
| immediately      |  16,612 |
| yet              |  16,571 |
| exactly          |  12,953 |
| necessarily      |  11,968 |
| terribly         |   6,726 |
| ever             |   6,590 |
| any              |   5,081 |
| inherently       |   3,761 |
| remotely         |   2,130 |

> no more than 5,000 rows per individual `group-[#].parquet`
  - max rows in writing batch = 2,501
  - min rows in writing batch = 834

✓ Sample of bigram tokens for `NEQ-Top8[5000]`  successfully saved as  
> "/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8adv_sample-hits_2024-07-31.parq"
* Total time to write partitioned parquet ⇾  `00:00:00.480` -->



```python
show_sample(hits_df.filter(['all_forms_lower', 'token_str']).sample(10).sort_values('all_forms_lower'))
```

    +-----------------------+----------------------------+--------------------------------------------------------------+
    | hit_id                | all_forms_lower            | token_str                                                    |
    +=======================+============================+==============================================================+
    | pcc_eng_20_052.4196_x | (+)_immediately_suspicious | Immediately suspicious of West , it is n't until Cain        |
    | 0830750_148:1-2       |                            | stumbles upon an experiment with a dead cat that he begins   |
    |                       |                            | to believe in the serum .                                    |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | nyt_eng_20020531_0116 | (+)_particularly_awkward   | Frank LeBoeuf looked particularly awkward Friday night .     |
    | _32:4-5               |                            |                                                              |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_26_073.1630_x | (+)_terribly_distressing   | I also hear racist remarks , which is terribly distressing . |
    | 1166420_08:09-10      |                            |                                                              |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_11_093.7314_x | n't_that_stupid            | People in their position are n't THAT stupid .               |
    | 1501216_38:6-7-8      |                            |                                                              |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_26_096.7544_x | never_ever_superfluous     | Nevertheless , there are many but facts that are proving a   |
    | 1548296_096:14-15-16  |                            | condom is never ever superfluous .                           |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_05_004.2094_x | not_any_different          | Readers bemoaned the rumors of its decline not because the   |
    | 0052181_42:08-16-17   |                            | content of an e-book is any different than that of its paper |
    |                       |                            | and cloth counterpart , but because a stack of pages can be  |
    |                       |                            | measured in both time and space .                            |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | apw_eng_19981218_0387 | not_immediately_available  | wider figures on strike participation were not immediately   |
    | _6:7-8-9              |                            | available .                                                  |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_06_072.1008_x | not_necessarily_true       | While that is not necessarily true , there is no formula to  |
    | 1150224_007:4-5-6     |                            | pick that " sleeper team " for any given season .            |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_00_067.3624_x | not_that_good              | You 're not that good at doing this . ' "                    |
    | 1072650_052:3-4-5     |                            |                                                              |
    +-----------------------+----------------------------+--------------------------------------------------------------+
    | pcc_eng_14_038.2153_x | not_yet_clear              | The House Foreign Affairs Committee 's Bergdahl hearing      |
    | 0601239_14:24-25-26   |                            | quickly became polarized , with Democrats cautioning that    |
    |                       |                            | the facts of Bergdahl 's capture were not yet clear and      |
    |                       |                            | Republicans using testimony discrediting Bergdahl as a way   |
    |                       |                            | to criticize the Obama administration 's decision to trade   |
    |                       |                            | five Taliban prisoners for him .                             |
    +-----------------------+----------------------------+--------------------------------------------------------------+



```python
md_frame_code("""perspect_blam = (blam_df
                 .filter(regex=r'|'.join(adv_list[:5]), axis=0)
                 .filter(perspective_cols + adjust_am_names(FOCUS_DICT[TAG]['adv_adj']))
                 .filter(regex=r'^[^laN]').iloc[:, :14]
                 .sort_values(blind_priority_cols, ascending=False))
nb_show_table(pd.concat([perspect_blam.head(20), perspect_blam.tail(10)]))""")
perspect_blam = (blam_df
                 .filter(regex=r'|'.join(adv_list[:5]), axis=0)
                 .filter(perspective_cols + adjust_am_names(FOCUS_DICT[TAG]['adv_adj']))
                 .filter(regex=r'^[^laN]').iloc[:, :14]
                 .sort_values(blind_priority_cols, ascending=False))
nb_show_table(pd.concat([perspect_blam.head(20), perspect_blam.tail(10)]))
```


```python
perspect_blam = (blam_df
                 .filter(regex=r'|'.join(adv_list[:5]), axis=0)
                 .filter(perspective_cols + adjust_am_names(FOCUS_DICT[TAG]['adv_adj']))
                 .filter(regex=r'^[^laN]').iloc[:, :14]
                 .sort_values(blind_priority_cols, ascending=False))
nb_show_table(pd.concat([perspect_blam.head(20), perspect_blam.tail(10)]))
```


|                                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |   `P1` |    `f1` |   `exp_f` |   `unexp_f` |   `P2` |
|:------------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|-------:|--------:|----------:|------------:|-------:|
| **[_direct_] any~happier**                |    7.87 |  7,348.55 |           0.43 |            0.24 |    0.43 |    0.05 |   830 |   1,909 |        0.99 |   0.43 |  16,176 |      4.87 |      825.13 |   0.05 |
| **[_direct_] necessarily~indicative**     |    7.45 | 10,814.41 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,319 |        0.99 |   0.60 |  42,916 |     15.68 |    1,373.32 |   0.03 |
| **[_mirror_] exactly~alike**              |    7.30 |    517.06 |           0.37 |            0.22 |    0.37 |    0.06 |    54 |     144 |        1.00 |   0.38 |     862 |      0.21 |       53.79 |   0.06 |
| **[_direct_] any~clearer**                |    7.19 |  2,983.07 |           0.35 |            0.18 |    0.35 |    0.02 |   361 |   1,037 |        0.99 |   0.35 |  16,176 |      2.64 |      358.36 |   0.02 |
| **[_direct_] any~closer**                 |    5.99 |  4,000.91 |           0.17 |            0.10 |    0.17 |    0.04 |   600 |   3,488 |        0.99 |   0.17 |  16,176 |      8.89 |      591.11 |   0.04 |
| **[_mirror_] any~closer**                 |    5.98 |    465.53 |           0.21 |            0.13 |    0.21 |    0.06 |    60 |     285 |        0.99 |   0.21 |   1,083 |      0.53 |       59.47 |   0.06 |
| **[_direct_] any~worse**                  |    5.92 | 11,618.05 |           0.15 |            0.13 |    0.15 |    0.11 | 1,797 |  11,891 |        0.98 |   0.15 |  16,176 |     30.30 |    1,766.70 |   0.11 |
| **[_direct_] any~easier**                 |    5.60 |  9,840.90 |           0.12 |            0.11 |    0.12 |    0.10 | 1,624 |  12,945 |        0.98 |   0.13 |  16,176 |     32.99 |    1,591.01 |   0.10 |
| **[_direct_] any~simpler**                |    5.58 |  1,488.36 |           0.15 |            0.08 |    0.15 |    0.01 |   232 |   1,501 |        0.98 |   0.15 |  16,176 |      3.83 |      228.17 |   0.01 |
| **[_mirror_] any~better**                 |    5.56 |  2,549.65 |           0.35 |            0.23 |    0.10 |    0.35 |   386 |   3,681 |        0.98 |   0.10 |   1,083 |      6.83 |      379.17 |   0.36 |
| **[_direct_] any~younger**                |    5.50 |  1,625.85 |           0.14 |            0.08 |    0.14 |    0.02 |   259 |   1,789 |        0.98 |   0.14 |  16,176 |      4.56 |      254.44 |   0.02 |
| **[_direct_] any~safer**                  |    5.40 |  1,516.32 |           0.13 |            0.07 |    0.13 |    0.01 |   246 |   1,792 |        0.98 |   0.14 |  16,176 |      4.57 |      241.43 |   0.02 |
| **[_direct_] any~better**                 |    5.34 | 29,300.27 |           0.30 |            0.20 |    0.10 |    0.30 | 5,022 |  49,936 |        0.97 |   0.10 |  16,176 |    127.26 |    4,894.74 |   0.31 |
| **[_direct_] any~nicer**                  |    5.23 |    620.70 |           0.15 |            0.08 |    0.15 |    0.01 |    97 |     630 |        0.98 |   0.15 |  16,176 |      1.61 |       95.39 |   0.01 |
| **[_direct_] necessarily~cause**          |    5.20 |    349.89 |           0.41 |            0.20 |    0.41 |    0.00 |    52 |     126 |        0.98 |   0.41 |  42,916 |      0.85 |       51.15 |   0.00 |
| **[_direct_] any~wiser**                  |    5.11 |    414.09 |           0.16 |            0.08 |    0.16 |    0.00 |    63 |     377 |        0.98 |   0.17 |  16,176 |      0.96 |       62.04 |   0.00 |
| **[_direct_] remotely~comparable**        |    5.03 |    756.79 |           0.05 |            0.04 |    0.05 |    0.02 |   125 |   2,443 |        0.98 |   0.05 |   6,109 |      2.35 |      122.65 |   0.02 |
| **[_direct_] any~smarter**                |    4.91 |    547.98 |           0.13 |            0.07 |    0.13 |    0.01 |    91 |     706 |        0.98 |   0.13 |  16,176 |      1.80 |       89.20 |   0.01 |
| **[_mirror_] any~easier**                 |    4.72 |    370.25 |           0.09 |            0.07 |    0.09 |    0.06 |    61 |     639 |        0.98 |   0.10 |   1,083 |      1.19 |       59.81 |   0.06 |
| **[_direct_] necessarily~representative** |    4.71 |  2,409.17 |           0.18 |            0.10 |    0.18 |    0.01 |   487 |   2,559 |        0.96 |   0.19 |  42,916 |     17.30 |      469.70 |   0.01 |
| **[_direct_] that~wrong**                 |   -1.91 |   -617.59 |          -0.00 |           -0.01 |   -0.02 |   -0.00 |    90 |  21,208 |       -5.19 |   0.00 | 166,680 |    556.92 |     -466.92 |   0.00 |
| **[_direct_] that~aware**                 |   -1.92 |   -805.78 |          -0.00 |           -0.01 |   -0.02 |   -0.00 |   133 |  28,922 |       -4.71 |   0.00 | 166,680 |    759.48 |     -626.48 |   0.00 |
| **[_direct_] exactly~good**               |   -1.97 | -1,448.89 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   264 | 202,048 |       -4.35 |   0.00 |  44,378 |  1,412.63 |   -1,148.63 |   0.01 |
| **[_direct_] necessarily~different**      |   -2.00 |   -631.69 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,019 |       -5.94 |   0.00 |  42,916 |    541.03 |     -463.03 |   0.00 |
| **[_direct_] exactly~bad**                |   -2.11 |   -969.14 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   124 | 119,777 |       -5.75 |   0.00 |  44,378 |    837.43 |     -713.43 |   0.00 |
| **[_direct_] that~proud**                 |   -2.13 |   -562.05 |          -0.00 |           -0.01 |   -0.02 |   -0.00 |    53 |  16,806 |       -7.33 |   0.00 | 166,680 |    441.32 |     -388.32 |   0.00 |
| **[_direct_] that~many**                  |   -2.51 | -3,118.03 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |   351 |  97,776 |       -6.32 |   0.00 | 166,680 |  2,567.57 |   -2,216.57 |   0.00 |
| **[_direct_] that~better**                |   -2.69 | -1,775.57 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |   135 |  49,936 |       -8.71 |   0.00 | 166,680 |  1,311.31 |   -1,176.31 |   0.00 |
| **[_direct_] that~likely**                |   -2.91 | -1,893.65 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |   111 |  49,995 |      -10.83 |   0.00 | 166,680 |  1,312.86 |   -1,201.86 |   0.00 |
| **[_direct_] that~sure**                  |   -3.16 | -5,111.81 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |   299 | 134,058 |      -10.77 |   0.00 | 166,680 |  3,520.33 |   -3,221.33 |   0.00 |




```python
# md_frame_code("""print(timestamp_today())
# for adverb in adv_am.index:
#     sample_adv_bigrams(
#         adverb, data_tag=TAG, verbose=True,
#         amdf=blam_df, hits_df=hits_df,
#         n_top_bigrams=BK, bigram_floor=BIGRAM_F_FLOOR)""")
# print(timestamp_today())
# for adverb in adv_am.index:
#     sample_adv_bigrams(
#         adverb, data_tag=TAG, verbose=True,
#         amdf=blam_df, hits_df=hits_df,
#         n_top_bigrams=BK, bigram_floor=BIGRAM_F_FLOOR)
```


```python
print(timestamp_today())
for adverb in adv_am.index:
    sample_adv_bigrams(
        adverb, data_tag=TAG, verbose=True,
        amdf=blam_df, hits_df=hits_df,
        n_top_bigrams=BK, bigram_floor=BIGRAM_F_FLOOR)
```

2024-08-06

## *necessarily*


|                                           |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`        | `l2`           |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:------------------------------------------|------:|--------:|--------:|-------:|----------:|:------------|:---------------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] necessarily~indicative**     | 1,389 |    0.59 |    7.45 |   0.60 | 10,814.41 | necessarily | indicative     | 42,916 |  2,319 | 6,347,362 |     15.68 |    1,373.32 |        0.99 |    0.03 |   0.03 |           0.59 |            0.31 |            2.36 | 36.85 |   1.95 | direct      |
| **[_direct_] necessarily~cause**          |    52 |    0.41 |    5.20 |   0.41 |    349.89 | necessarily | cause          | 42,916 |    126 | 6,347,362 |      0.85 |       51.15 |        0.98 |    0.00 |   0.00 |           0.41 |            0.20 |            2.02 |  7.09 |   1.79 | direct      |
| **[_direct_] necessarily~representative** |   487 |    0.18 |    4.71 |   0.19 |  2,409.17 | necessarily | representative | 42,916 |  2,559 | 6,347,362 |     17.30 |      469.70 |        0.96 |    0.01 |   0.01 |           0.18 |            0.10 |            1.54 | 21.28 |   1.45 | direct      |
| **[_direct_] necessarily~synonymous**     |   165 |    0.16 |    4.21 |   0.17 |    776.36 | necessarily | synonymous     | 42,916 |    968 | 6,347,362 |      6.54 |      158.46 |        0.96 |    0.00 |   0.00 |           0.16 |            0.08 |            1.48 | 12.34 |   1.40 | direct      |
| **[_direct_] necessarily~incompatible**   |   101 |    0.18 |    4.16 |   0.19 |    495.03 | necessarily | incompatible   | 42,916 |    540 | 6,347,362 |      3.65 |       97.35 |        0.96 |    0.00 |   0.00 |           0.18 |            0.09 |            1.53 |  9.69 |   1.44 | direct      |
| **[_direct_] necessarily~reflective**     |   181 |    0.14 |    4.03 |   0.15 |    802.51 | necessarily | reflective     | 42,916 |  1,209 | 6,347,362 |      8.17 |      172.83 |        0.95 |    0.00 |   0.00 |           0.14 |            0.07 |            1.42 | 12.85 |   1.35 | direct      |
| **[_direct_] necessarily~true**           | 3,242 |    0.09 |    3.76 |   0.09 | 11,419.84 | necessarily | true           | 42,916 | 35,146 | 6,347,362 |    237.63 |    3,004.37 |        0.93 |    0.07 |   0.08 |           0.09 |            0.08 |            1.21 | 52.77 |   1.13 | direct      |
| **[_direct_] necessarily~predictive**     |    57 |    0.17 |    3.68 |   0.17 |    269.66 | necessarily | predictive     | 42,916 |    330 | 6,347,362 |      2.23 |       54.77 |        0.96 |    0.00 |   0.00 |           0.17 |            0.08 |            1.49 |  7.25 |   1.41 | direct      |
| **[_direct_] necessarily~permanent**      |   151 |    0.10 |    3.37 |   0.10 |    556.98 | necessarily | permanent      | 42,916 |  1,456 | 6,347,362 |      9.84 |      141.16 |        0.93 |    0.00 |   0.00 |           0.10 |            0.05 |            1.23 | 11.49 |   1.19 | direct      |
| **[_mirror_] necessarily~wrong**          |   211 |    0.02 |    3.35 |   0.02 |    783.75 | necessarily | wrong          |    993 |  8,526 |   583,470 |     14.51 |      196.49 |        0.93 |    0.20 |   0.21 |           0.20 |            0.11 |            1.27 | 13.53 |   1.16 | mirror      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/NEQ-necessarily_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _necessarily indicative_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_088.9564_x1420693_46:3-4-5`**     | This is not__``necessarily indicative``__of something bad to be afraid of but definitely needs to be checked by a doctor to get the appropriate medicines or treatments .                                                                                                                                                                    |
| **`pcc_eng_18_011.6927_x0173116_4:14-15-16`**   | Any references to performance are for illustrative purposes only ; past performance is not__``necessarily indicative``__of future results .                                                                                                                                                                                                  |
| **`pcc_eng_28_012.2281_x0181852_057:44-45-46`** | Out of the 1050 pastors we surveyed during two pastors conferences held in Pasadena , California , 825 , or 78 % ( 326 in 2005 and 499 in 2006 , This is a small local sampling to assess causes and motivations , not__``necessarily indicative``__of a national sampling . ) said they were forced to resign from a church at least once . |
| **`pcc_eng_23_037.5692_x0590867_12:21-22-23`**  | " In addition , atypical blood data , which may be within this database from 2009 - 2012 , is not__``necessarily indicative``__of doping , " he continued .                                                                                                                                                                                  |
| **`pcc_eng_19_072.3956_x1153193_219:21-22-23`** | Clearly a high Wonderlic score is not a golden ticket to future NFL success , while a low one is not__``necessarily indicative``__of future failures .                                                                                                                                                                                       |
| **`pcc_eng_28_019.2533_x0295114_20:11-12-13`**  | The past performance of any trading method or system is not__``necessarily indicative``__of future issue and result .                                                                                                                                                                                                                        |
| **`pcc_eng_14_017.6869_x0269547_50:08-09-10`**  | The past performance of any service is not__``necessarily indicative``__of future results .                                                                                                                                                                                                                                                  |
| **`pcc_eng_25_003.9807_x0048751_55:38-39-40`**  | During last week 's meeting , no matter how many times the four men in dark suits on the NRC panel referred to the controversial email as " a snapshot in time , " claiming it was not__``necessarily indicative``__of what the final report would conclude , the crowd was n't buying it .                                                  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_indicative_ex.md`


### 2. _necessarily cause_


|                                                | `token_str`                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_067.7784_x1079285_18:17-18-19`** | While it appears problematic , economists with the federal government say a negative savings rate is n't__``necessarily cause``__for concern . |
| **`pcc_eng_15_012.6241_x0187604_4:3-4-5`**     | This is not__``necessarily cause``__for alarm .                                                                                                |
| **`pcc_eng_21_013.1878_x0196808_03:17-18-19`** | Although there are be 95 convicted sex offenders living in Island County , their presence is not__``necessarily cause``__for public concern .  |
| **`pcc_eng_14_009.3541_x0134841_12:4-5-6`**    | But this is not__``necessarily cause``__for despair .                                                                                          |
| **`pcc_eng_05_089.5717_x1432874_45:11-12-13`** | A test showing small amphetamine concentrations in your body is not__``necessarily cause``__for alarm .                                        |
| **`pcc_eng_08_103.7341_x1663397_40:10-11-12`** | Small changes in color , smell or taste are not__``necessarily cause``__for alarm , adds Dr. Goldstone .                                       |
| **`pcc_eng_test_2.05409_x24786_01:11-12-13`**  | The likes of botulism and anthrax in the air are n't__``necessarily cause``__for alarm .                                                       |
| **`pcc_eng_02_098.4559_x1575696_01:4-5-6`**    | This change is not__``necessarily cause``__for a meltdown : Wait and taste the 42 % before you freak out .                                     |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_cause_ex.md`


### 3. _necessarily representative_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_059.4764_x0944589_063:09-10-11`** | The report cautions that the countries reviewed are not__``necessarily representative``__of the G-20 countries .                                                                                                                                                                                                            |
| **`pcc_eng_22_006.4374_x0087757_12:5-6-7`**     | The results , while not__``necessarily representative``__of Canada at large , were troubling : municipalities representing 25 % of the population of the responding municipalities had experienced water -quality problems that year , and municipalities accounting for more than 22 % had issued boil -water advisories . |
| **`nyt_eng_20070312_0121_37:21-22-23`**         | they also acknowledged that they did not have information on suicide attempts , and that the group they studied was not__``necessarily representative``__of the general population .                                                                                                                                        |
| **`pcc_eng_29_098.6716_x1578038_16:4-5-6`**     | These findings are not__``necessarily representative``__of the whole country .                                                                                                                                                                                                                                              |
| **`pcc_eng_05_033.2076_x0521749_274:08-09-10`** | Also , research done on powerlifters is not__``necessarily representative``__of anyone else who should deadlift .                                                                                                                                                                                                           |
| **`pcc_eng_25_081.3834_x1301369_60:16-17-18`**  | So Bob Howarth at Cornell University says the results from the 190 study sites are not__``necessarily representative``__of the industry as a whole .                                                                                                                                                                        |
| **`pcc_eng_23_037.4066_x0588215_53:18-19-20`**  | And as far as that goes , the views expressed by those commenting on the blog are not__``necessarily representative``__of our views either .                                                                                                                                                                                |
| **`nyt_eng_20000109_0144_3:25-26-27`**          | the audience reaction at the dinner at the University of New Hampshire , a fund-raising event for the state 's Republican Party , is not__``necessarily representative``__of how Bush will perform in the first primary in the nation on Feb. 1 .                                                                           |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_representative_ex.md`


### 4. _necessarily synonymous_


|                                                | `token_str`                                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_016.8392_x0255461_12:11-12-13`** | But the charging of this criminal and his partners is n't__``necessarily synonymous``__with justice or their repaying society as they should , a situation that often occurs in Havana as well .                                                                                                          |
| **`pcc_eng_02_082.8272_x1323046_30:20-21-22`** | Citing the New York Court of Appeals , Justice Jaffe , said : " ' Legal personhood ' is not__``necessarily synonymous``__with being human ...                                                                                                                                                             |
| **`pcc_eng_28_074.6429_x1191131_35:19-20-21`** | All of this goes to imply that the writers desired to make a clear point : Islam is not__``necessarily synonymous``__with terrorism .                                                                                                                                                                     |
| **`pcc_eng_12_007.4633_x0104484_41:19-20-21`** | " People 's religious beliefs and their views on the legal protections and what Constitution stands for are not__``necessarily synonymous``__, " Northup said .                                                                                                                                           |
| **`pcc_eng_09_089.7942_x1436727_08:18-19-20`** | From bassheads and trance addicts to festival bros and flag-wavers , stages were drawing crowds that were n't__``necessarily synonymous``__with any particular artist 's following .                                                                                                                      |
| **`pcc_eng_22_001.4748_x0007738_11:19-20-21`** | Kernot said that she hoped the calendar would send the message to women that success and inspiration were not__``necessarily synonymous``__with fame and wealth and that happiness was not just about being thin or fashionable .                                                                         |
| **`pcc_eng_05_032.5549_x0511201_04:26-27-28`** | While big data applications are often associated with fast-moving organizations that can quickly act on real-time data feeds , big data and real time are not__``necessarily synonymous``__.                                                                                                              |
| **`nyt_eng_20000324_0268_8:50-51-52`**         | Shopping is also a form of self-expression , a means of `` creative involvement , of picking things up and making them yours , '' said Jeff Stone , co-publisher of the Chic Simple series of books , which illustrate the premise that high style and high prices are not__``necessarily synonymous``__. |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_synonymous_ex.md`


### 5. _necessarily incompatible_


|                                                 | `token_str`                                                                                                                                                                                                                                                                      |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_038.1359_x0601099_07:17-18-19`**  | In particular , he noted that , in his view , DRIPA and similar legislation are not__``necessarily incompatible``__with EU law as such .                                                                                                                                         |
| **`pcc_eng_17_072.1236_x1149365_21:30-31-32`**  | My response did n't try to pressure him ; I just tried to explain where I was coming from , what evolution is about , and why it 's not__``necessarily incompatible``__with belief in some kind of god , even the Christian God .                                                |
| **`pcc_eng_14_035.4931_x0557166_20:25-26-27`**  | In other words , Graham and Chamberlain said , " the two views of the history of the uplift of the Sierra Nevada are not__``necessarily incompatible``__. "                                                                                                                      |
| **`pcc_eng_02_040.3549_x0636753_106:09-10-11`** | The approaches may be contradictory but they are not__``necessarily incompatible``__.                                                                                                                                                                                            |
| **`pcc_eng_22_088.0023_x1406421_11:5-6-7`**     | The two views are not__``necessarily incompatible``__.                                                                                                                                                                                                                           |
| **`pcc_eng_11_065.1912_x1038846_017:15-16-17`** | A science teacher from a Catholic high school countered that evolution and religion are n't__``necessarily incompatible``__; at least they are n't in her school .                                                                                                               |
| **`pcc_eng_25_046.0799_x0729769_59:4-5-6`**     | Teacher autonomy is not__``necessarily incompatible``__with administrative support .                                                                                                                                                                                             |
| **`nyt_eng_20061116_0189_23:45-46-47`**         | the only thing Amber wants more than to change the world is to get out of Cody , and one of the film 's quiet insights is that these two desires -- to fight the system and to win by its rules -- are not__``necessarily incompatible``__, though they may seem contradictory . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_incompatible_ex.md`


### 6. _necessarily reflective_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                          |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_101.7938_x1629025_18:22-23-24`**  | So the cities that are little bit less saturated might have employers that are willing to understand that the degree is n't__``necessarily reflective``__of the skill that they need .                                                                                                               |
| **`pcc_eng_13_085.5362_x1366486_114:23-24-25`** | However , because the program is voluntary , the employers represented are self-selected and unevenly distributed across the country , and thus not__``necessarily reflective``__of the general population of national employers who would be required to screen workers under a mandatory program . |
| **`pcc_eng_02_089.0522_x1423589_262:36-37-38`** | Even before I read that article I recognized that the persona someone tries to convey in Facebook , My Space , Twitter and even professional networking sites such as Linked In and Plaxo , are not__``necessarily reflective``__of what is really going on in that person 's life .                 |
| **`pcc_eng_14_088.5171_x1414621_38:14-15-16`**  | Prior to this , the information may be less complete , and therefore not__``necessarily reflective``__of the true rate of cancer .                                                                                                                                                                   |
| **`pcc_eng_15_013.9670_x0209077_112:22-23-24`** | Of course , even this level is n't that simple , because the evidence of our senses is , sadly , not__``necessarily reflective``__of objective reality ; all my senses could verify that it is in fact raining , but I could be mad , or in the Matrix .                                             |
| **`pcc_eng_03_034.1558_x0537071_20:14-15-16`**  | Too frequently , the plans that inform resource allocation and public policy are not__``necessarily reflective``__of the community as a whole , but rather a small subsection of those who have the time , resources and inclination to participate .                                                |
| **`pcc_eng_01_090.9465_x1454416_14:29-30-31`**  | Rav Shteinman is in the Intensive Care Unit because , Dr. Weinberg explained , the centenarian gadol can receive more comprehensive treatment there ; the ICU location is not__``necessarily reflective``__of his health status , he explained .                                                     |
| **`pcc_eng_08_043.2554_x0683868_51:13-14-15`**  | The views and opinions expressed in his column are his own and not__``necessarily reflective``__of any organizations he works for .                                                                                                                                                                  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_reflective_ex.md`


### 7. _necessarily true_


|                                                 | `token_str`                                                                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_074.5172_x1188054_11:17-18-19`**  | Some of the impetus for same sex marriage can probably be explained by the belief , not__``necessarily true``__, that marriage must be a wonderful institution if so many people are doing it .           |
| **`pcc_eng_01_091.7752_x1467757_716:21-22-23`** | Living the Will of God is the same as proclaiming the Will of God , and yet the inverse is not__``necessarily true``__, or simply put , talk can be cheap while action is work .                          |
| **`pcc_eng_02_004.4366_x0055473_11:1-2-3`**     | Not__``necessarily true``__.                                                                                                                                                                              |
| **`pcc_eng_16_025.1387_x0390730_005:12-13-14`** | However , any seasoned golfer will tell you that this is not__``necessarily true``__.                                                                                                                     |
| **`pcc_eng_17_103.1222_x1650804_3:5-6-7`**      | Even if that 's not__``necessarily true``__despite all those obligatory JDM bits , swapping a 1998 car 's old single overhead cam engine for a 2002 WRX turbo is definitely the right way to go forward . |
| **`pcc_eng_07_022.7398_x0351549_06:12-13-14`**  | You may think your injuries are minor , but that is n't__``necessarily true``__.                                                                                                                          |
| **`pcc_eng_08_075.3312_x1203475_086:4-5-6`**    | So that 's not__``necessarily true``__that because a guy is a great athlete that he 'll be a great fighter .                                                                                              |
| **`pcc_eng_15_016.9052_x0256548_054:3-4-5`**    | This is n't__``necessarily true``__, though .                                                                                                                                                             |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_true_ex.md`


### 8. _necessarily predictive_


|                                                 | `token_str`                                                                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_009.8182_x0142325_14:10-11-12`**  | The thing about technical trading is that it 's not__``necessarily predictive``__, you have to wait until a trend begins , is confirmed , and THEN you trade .                                                                                                  |
| **`pcc_eng_09_034.3646_x0540198_37:5-6-7`**     | But those conversations are not__``necessarily predictive``__of specific outcomes like elections , revolutions , or successful products , " says Marc Smith , founder of the Social Media Research Foundation .                                                 |
| **`pcc_eng_03_037.7182_x0594676_10:14-15-16`**  | One of the biggest problems with all rating systems is that they are not__``necessarily predictive``__in nature .                                                                                                                                               |
| **`pcc_eng_11_087.4867_x1399981_082:34-35-36`** | Of course , this survey only looked at homeschoolers with religious mothers , not at all homeschoolers , and it looked at individuals who were adults in 2011 , meaning that it is n't__``necessarily predictive``__of how current homechoolers will turn out . |
| **`pcc_eng_17_078.4589_x1251825_057:4-5-6`**    | But they 're not__``necessarily predictive``__.                                                                                                                                                                                                                 |
| **`pcc_eng_16_029.7005_x0464510_11:12-13-14`**  | We note that this is only one data point and is not__``necessarily predictive``__of 1Q performance .                                                                                                                                                            |
| **`pcc_eng_13_009.6430_x0139427_29:3-4-5`**     | That 's not__``necessarily predictive``__, either .                                                                                                                                                                                                             |
| **`pcc_eng_01_041.9764_x0662242_26:09-11-12`**  | The system , the article says , was not "__``necessarily predictive``__of academic trouble .                                                                                                                                                                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_predictive_ex.md`


### 9. _necessarily permanent_


|                                                | `token_str`                                                                                                                                                                                 |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_037.3058_x0586997_26:16-17-18`** | The trend is not inexorable , and the loss of any condition of power is not__``necessarily permanent``__, depending essentially on the will and actions of the society .                    |
| **`pcc_eng_02_046.4212_x0734815_24:3-4-5`**    | This is n't__``necessarily permanent``__.                                                                                                                                                   |
| **`pcc_eng_26_083.9281_x1341010_23:5-6-7`**    | Domestic violence orders are not__``necessarily permanent``__- the Queensland Courts shows more than 30 per cent of all orders made in 2018 were temporary .                                |
| **`nyt_eng_20050128_0132_20:29-30-31`**        | just as Halliburton might preserve links to KBR and its contracts in Iraq , the company also signaled on Friday that cooling off its dealings in Iran was not__``necessarily permanent``__. |
| **`pcc_eng_15_091.3134_x1459846_10:10-11-12`** | You need to remember that income tax exemption is not__``necessarily permanent``__.                                                                                                         |
| **`nyt_eng_19960706_0146_12:27-28-29`**        | but since mortgage insurance is required only when the borrower 's equity is less than 20 percent , Ms. Schweppe said , the monthly premium is not__``necessarily permanent``__.            |
| **`pcc_eng_13_030.8875_x0483336_03:10-11-12`** | However , like phone numbers , web addresses are not__``necessarily permanent``__, and do change from time to time .                                                                        |
| **`pcc_eng_18_084.4652_x1351623_09:18-19-20`** | However , I also wrote in January that the al Qaeda core 's weakness and irrelevance were not__``necessarily permanent``__.                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_permanent_ex.md`


### 10. _necessarily wrong_


|                                                 | `token_str`                                                                                                                                                                        |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_106.3424_x1704209_11:3-4-5`**     | There is nothing__``necessarily wrong``__with that .                                                                                                                               |
| **`pcc_eng_10_019.5473_x0299696_031:4-5-6`**    | First impressions are n't__``necessarily wrong``__, but -- like Ron 's initial impression of Heather -- they 're not necessarily right , either .                                  |
| **`pcc_eng_28_016.5979_x0252363_17:11-12-13`**  | With Manchester City as the reference point , they were n't__``necessarily wrong``__; but they were misguided .                                                                    |
| **`pcc_eng_21_094.5986_x1512298_06:4-5-6`**     | Their logic is n't__``necessarily wrong``__.                                                                                                                                       |
| **`pcc_eng_26_009.3989_x0135632_23:1-4-5`**     | Nor is it__``necessarily wrong``__to brag about having sex with someone .                                                                                                          |
| **`pcc_eng_24_103.6272_x1660457_030:26-27-28`** | It 's drilled into our brains that we need to write so many words because it is " good for SEO " and they 're not__``necessarily wrong``__, either .                               |
| **`pcc_eng_16_088.0642_x1409368_06:3-4-5`**     | There is nothing__``necessarily wrong``__with this ; editors make choices and the Star Observer is far more balanced and objective than the current Murdoch press , for instance . |
| **`pcc_eng_12_009.2372_x0133197_19:3-4-5`**     | It is n't__``necessarily wrong``__to be mad or think that the other side is nuts -- all of us do , at some point or another .                                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_wrong_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/`...
* Renaming existing version of `necessarily_indicative_80ex~80.csv`
* Renaming existing version of `necessarily_representative_80ex~80.csv`
* Renaming existing version of `necessarily_true_80ex~80.csv`
* Renaming existing version of `necessarily_wrong_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_indicative_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_cause_80ex~10.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_representative_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_synonymous_80ex~48.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_incompatible_80ex~28.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_reflective_80ex~49.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_true_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_predictive_80ex~20.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_permanent_80ex~42.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_wrong_80ex~80.csv`

## *that*


|                              |    `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`     |    `f1` |    `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |    `t` |   `MI` | `dataset`   |
|:-----------------------------|-------:|--------:|--------:|-------:|----------:|:-------|:---------|--------:|--------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|-------:|-------:|:------------|
| **[_mirror_] that~great**    |    292 |    0.13 |    3.84 |   0.14 |  1,174.94 | that   | great    |   4,538 |   2,147 |   583,470 |     16.70 |      275.30 |        0.94 |    0.06 |   0.06 |           0.13 |            0.09 |            1.33 |  16.11 |   1.24 | mirror      |
| **[_direct_] that~great**    | 11,055 |    0.22 |    3.49 |   0.24 | 32,446.71 | that   | great    | 166,680 |  45,537 | 6,347,362 |  1,195.79 |    9,859.21 |        0.89 |    0.06 |   0.07 |           0.22 |            0.14 |            1.10 |  93.77 |   0.97 | direct      |
| **[_direct_] that~uncommon** |    802 |    0.23 |    3.31 |   0.25 |  2,369.26 | that   | uncommon | 166,680 |   3,193 | 6,347,362 |     83.85 |      718.15 |        0.90 |    0.00 |   0.00 |           0.23 |            0.11 |            1.10 |  25.36 |   0.98 | direct      |
| **[_direct_] that~hard**     |  9,964 |    0.19 |    3.29 |   0.22 | 27,114.66 | that   | hard     | 166,680 |  45,416 | 6,347,362 |  1,192.61 |    8,771.39 |        0.88 |    0.05 |   0.06 |           0.19 |            0.12 |            1.04 |  87.87 |   0.92 | direct      |
| **[_mirror_] that~simple**   |    487 |    0.06 |    2.77 |   0.06 |  1,267.95 | that   | simple   |   4,538 |   7,580 |   583,470 |     58.95 |      428.05 |        0.88 |    0.10 |   0.11 |           0.10 |            0.08 |            0.99 |  19.40 |   0.92 | mirror      |
| **[_mirror_] that~easy**     |    464 |    0.05 |    2.63 |   0.06 |  1,130.07 | that   | easy     |   4,538 |   7,897 |   583,470 |     61.42 |      402.58 |        0.87 |    0.09 |   0.10 |           0.09 |            0.07 |            0.94 |  18.69 |   0.88 | mirror      |
| **[_direct_] that~big**      |  6,280 |    0.12 |    2.57 |   0.15 | 12,159.27 | that   | big      | 166,680 |  42,692 | 6,347,362 |  1,121.08 |    5,158.92 |        0.82 |    0.03 |   0.04 |           0.12 |            0.08 |            0.82 |  65.10 |   0.75 | direct      |
| **[_direct_] that~bad**      | 16,609 |    0.11 |    2.51 |   0.14 | 31,136.23 | that   | bad      | 166,680 | 119,777 | 6,347,362 |  3,145.31 |   13,463.69 |        0.81 |    0.08 |   0.10 |           0.11 |            0.10 |            0.81 | 104.47 |   0.72 | direct      |
| **[_direct_] that~stupid**   |    824 |    0.12 |    2.41 |   0.15 |  1,604.73 | that   | stupid   | 166,680 |   5,496 | 6,347,362 |    144.32 |      679.68 |        0.82 |    0.00 |   0.00 |           0.12 |            0.06 |            0.82 |  23.68 |   0.76 | direct      |
| **[_direct_] that~simple**   |  6,252 |    0.11 |    2.40 |   0.13 | 10,949.82 | that   | simple   | 166,680 |  47,134 | 6,347,362 |  1,237.73 |    5,014.27 |        0.80 |    0.03 |   0.04 |           0.11 |            0.07 |            0.77 |  63.42 |   0.70 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/NEQ-that_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _that great_


|                                                 | `token_str`                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_050.7125_x0804728_660:11-12-13`** | Wakefield is 45 and his best days -- which were never__``that great``__to begin with -- are over .                                                         |
| **`pcc_eng_20_038.4435_x0605182_18:4-6-7`**     | High school has n't been__``that great``__for him in the past three years , considering his mysterious past , but now , things have taken an sudden turn . |
| **`pcc_eng_23_002.7362_x0027804_2:13-14-15`**   | In a recent speech , Governor Andrew Cuomo said that America was never__``that great``__.                                                                  |
| **`pcc_eng_12_012.9838_x0193857_13:6-7-8`**     | Hence , the quality is not__``that great``__.                                                                                                              |
| **`pcc_eng_11_093.1900_x1492465_09:4-6-7`**     | " I was n't actually__``that great``__at wrestling .                                                                                                       |
| **`pcc_eng_02_098.1325_x1570404_20:12-14-15`**  | Beautiful ballpark , fun place to visit since the team is n't all__``that great``__.                                                                       |
| **`pcc_eng_05_010.7099_x0157478_43:7-8-9`**     | She 's invested , but still not__``that great``__of an actor , sadly .                                                                                     |
| **`pcc_eng_19_011.9388_x0176729_19:27-28-29`**  | If you intend to mail your jewellery , discover how a lot it can be to get it came back for you if the supply is n't__``that great``__.                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_great_ex.md`


### 2. _that uncommon_


|                                                | `token_str`                                                                                                                                                                              |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_026.0935_x0406268_07:25-26-27`** | While Facebook is working on the fix and most spam listings have been taken care of , reports of an occasional illegal listing are not__``that uncommon``__.                             |
| **`pcc_eng_23_033.2186_x0520190_25:11-12-13`** | Unfortunately , testing bodily fluids for drugs and alcohol is not__``that uncommon``__.                                                                                                 |
| **`pcc_eng_16_088.6139_x1418264_23:6-7-8`**    | These sorts of spin-outs are n't__``that uncommon``__.                                                                                                                                   |
| **`pcc_eng_18_037.2851_x0587002_39:3-4-5`**    | It is n't__``that uncommon``__for a team to dress seven defenders as it is , especially in the playoffs when an injury on the blueline can throw the entire defensive unit out of wack . |
| **`pcc_eng_03_093.2455_x1493610_04:12-13-14`** | But you will be surprised to know that your condition is not__``that uncommon``__.                                                                                                       |
| **`nyt_eng_19990323_0152_18:11-13-14`**        | but if you talk to restaurateurs , solo diners are not actually__``that uncommon``__in New York .                                                                                        |
| **`pcc_eng_21_097.7569_x1563185_21:3-4-5`**    | It was not__``that uncommon``__to drink a beer whilst sweating in the bath .                                                                                                             |
| **`pcc_eng_26_038.6901_x0609439_13:16-17-18`** | That kind of thing is n't supposed to happen , but in Rochester it 's not__``that uncommon``__.                                                                                          |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_uncommon_ex.md`


### 3. _that hard_


|                                                | `token_str`                                                                                                                       |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_030.5306_x0477595_14:3-4-5`**    | It was n't__``that hard``__to draw freehand , but I did have to be pretty precise to make it look good .                          |
| **`pcc_eng_16_077.8340_x1243453_09:13-14-15`** | The thesis of the children 's book is that communism is " not__``that hard``__, " but has not been implemented in the right way . |
| **`pcc_eng_13_013.1323_x0195783_26:4-5-6`**    | " It 's not__``that hard``__to engineer . "                                                                                       |
| **`pcc_eng_29_019.5298_x0299052_011:4-5-6`**   | It really is n't__``that hard``__to make , and the flavor will beguile even those who dislike fruitcakes .                        |
| **`pcc_eng_11_060.6019_x0964503_84:16-17-18`** | She made us realise the critical importance of having accessible content and that it was n't__``that hard``__!                    |
| **`pcc_eng_16_050.1794_x0796131_60:4-5-6`**    | They are also not__``that hard``__( hence they are not hard- mode ... ) .                                                         |
| **`pcc_eng_04_051.5635_x0816855_017:3-5-6`**   | They are not all__``that hard``__to find in our contiguous 48 states .                                                            |
| **`pcc_eng_18_096.8193_x1551964_21:5-6-7`**    | Because it 's just NOT__``THAT HARD``__, and I know you can do it !                                                               |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_hard_ex.md`


### 4. _that simple_


|                                                 | `token_str`                                                                                                                                                                                                                  |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_006.5790_x0089890_043:5-6-7`**    | Sadly , it is n't__``that simple``__.                                                                                                                                                                                        |
| **`pcc_eng_12_030.5044_x0477711_54:6-7-8`**     | Solomon said the cost is not__``that simple``__.                                                                                                                                                                             |
| **`pcc_eng_17_030.1751_x0471974_65:5-6`**       | " It might be__``that simple``__of a business plan . "                                                                                                                                                                       |
| **`pcc_eng_09_035.2300_x0554234_014:24-25-26`** | She wrote on the Daily Mail , '' I could use the excuse that women are jealous of me , but it 's not__``that simple``__.                                                                                                     |
| **`pcc_eng_28_069.7893_x1112995_27:18-19`**     | By reduce the amount of energy you 're saving money on your energy bills , it 's__``that simple``__!                                                                                                                         |
| **`pcc_eng_24_077.9308_x1244448_16:35-36-37`**  | An early attempt at operating an irrigation district in the Portales valley 100 years ago proved that good wells could be put in but getting everyone to work together where water was concerned was n't__``that simple``__. |
| **`pcc_eng_23_090.0144_x1438822_12:6-7-8`**     | in fact , it is not__``that simple``__when budget is your only hindrance .                                                                                                                                                   |
| **`pcc_eng_24_083.1759_x1329168_05:08-09-10`**  | Creating electricity in your own home is n't__``that simple``__.                                                                                                                                                             |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_simple_ex.md`


### 5. _that easy_


|                                                | `token_str`                                                                                                                                                                |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19990408_0395_25:13-14-15`**        | `` I tried , '' Franco said , `` but it 's not__``that easy``__. ''                                                                                                        |
| **`pcc_eng_26_091.0161_x1455808_089:4-6-7`**   | " It 's not really__``that easy``__for the stuff to travel vertically .                                                                                                    |
| **`pcc_eng_11_064.3395_x1025115_10:4-6-7`**    | But it may not be__``that easy``__for Uncle Sam to do the build :                                                                                                          |
| **`pcc_eng_28_029.6409_x0462769_09:07-09-10`** | Because trying to be healthy is n't always__``that easy``__.                                                                                                               |
| **`pcc_eng_22_060.2297_x0957514_27:4-5-6`**    | Key Maps were never__``that easy``__.                                                                                                                                      |
| **`pcc_eng_14_004.0240_x0049020_10:16-17-18`** | First off , Hard Candy is cruelty - free which is great -- it 's not__``that easy``__to find cruelty - free at Walmart of all places , so that 's a huge plus in my book . |
| **`pcc_eng_23_030.4147_x0474853_47:3-4-5`**    | It 's not__``that easy``__, " Steven Thompson , founder of Kentucky Artisan Distillery told Forbes .                                                                       |
| **`pcc_eng_22_003.8188_x0045717_06:5-7-8`**    | In reality this is not always__``that easy``__.                                                                                                                            |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_easy_ex.md`


### 6. _that big_


|                                                 | `token_str`                                                                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_001.7497_x0012242_27:16-17-18`**  | The steak was ostensibly 20 ounces but that includes bone , so it really was n't__``that big``__.                                                                                                                                        |
| **`pcc_eng_00_064.9477_x1033925_20:7-8-9`**     | Cheating on some science homework is n't__``that big``__of a deal , but I am glad to know that my kids are learning values at home and are willing to stand up for what they think is right .                                            |
| **`pcc_eng_10_047.3669_x0750240_21:11-12-13`**  | The drink was overly sweet , so if you 're not__``that big``__into sugary drinks , avoid this frappuccino .                                                                                                                              |
| **`pcc_eng_14_032.3741_x0506900_044:6-7-8`**    | From far away it is n't__``that big``__of a deal , but if anyone is close enough to talk to you , it 's going to be noticeable so sadly I have n't got much use for this one .                                                           |
| **`pcc_eng_15_093.6503_x1497626_11:24-25-26`**  | Guy - Uriel Charles , the interim co-dean of Minnesota 's law school , characterized the objections to Delahunty 's hiring as " not__``that big``__of a deal , " adding , " You 've probably only got three students who are unhappy . " |
| **`pcc_eng_01_097.0634_x1553141_110:18-19-20`** | But after washing it , quite a few of the front spots came out so it was n't__``that big``__of a concern anymore .                                                                                                                       |
| **`pcc_eng_17_043.8013_x0691195_31:17-18-19`**  | The most common answer was that dice are supposed to be random and that it was n't__``that big``__of a deal to them , cost was also a big factor as well .                                                                               |
| **`pcc_eng_10_049.7960_x0789116_228:6-7-8`**    | In C-Segment the domination is not__``that big``__: 6.6 % .                                                                                                                                                                              |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_big_ex.md`


### 7. _that bad_


|                                                | `token_str`                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_084.3835_x1347506_08:30-31-32`** | The current state of education mirrors the true agenda and objectives of both colonialism and apartheid which in the words of former DA Leader Helen Zille was after all not__``that bad``__. |
| **`nyt_eng_19961206_0254_40:4-6-7`**           | fuel mileage is n't all__``that bad``__, 21.21 miles per gallon clocked over a bit more than 600 miles .                                                                                      |
| **`apw_eng_20090416_0526_7:16-17-18`**         | `` Everyone talked Nokia down , so there was a general relief that things were n't__``that bad``__after all . ''                                                                              |
| **`pcc_eng_08_108.4991_x1739254_44:09-10-11`** | They say , ' This pain really is n't__``that bad``__. '                                                                                                                                       |
| **`pcc_eng_02_030.1646_x0472182_08:3-4-5`**    | This was n't__``that bad``__but we had started with the Benjamin Moore Fresh Start interior primer but it was not sticking well .                                                             |
| **`pcc_eng_07_020.3375_x0312741_08:09-11-12`** | Not in the sense of " it ca n't be__``that bad``__" as much as " what are the limits of what we can put into a film ? "                                                                       |
| **`pcc_eng_24_086.2948_x1379587_13:6-8-9`**    | I guess the insomnia is not really__``that bad``__.                                                                                                                                           |
| **`pcc_eng_24_075.8088_x1210119_058:5-6-7`**   | The ewes were actually not__``that bad``__to shear , and I managed to get into the zone quite easily .                                                                                        |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_bad_ex.md`


### 8. _that stupid_


|                                                | `token_str`                                                                                                                                                    |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_068.7237_x1096245_18:18-19`**    | Of course , this is the Big Three , so it 's possible that they could be__``that stupid``__.                                                                   |
| **`pcc_eng_04_003.2094_x0035859_64:1-4-5`**    | Nobody could be__``that stupid``__, right ?                                                                                                                    |
| **`pcc_eng_10_051.9586_x0824265_47:4-5-6`**    | " They were n't__``that stupid``__. "                                                                                                                          |
| **`pcc_eng_11_068.7251_x1096264_07:26-27-28`** | I find myself analyzing the stupidest little every day things but the more I think on them , the more I realize it 's really not__``that stupid``__after all . |
| **`pcc_eng_26_045.9991_x0727726_048:3-4-5`**   | Mexicans are not__``that stupid``__.                                                                                                                           |
| **`pcc_eng_16_081.8759_x1308918_13:5-7-8`**    | Surely , they ca n't be__``that stupid``__.                                                                                                                    |
| **`pcc_eng_00_066.4760_x1058446_102:5-6`**     | " Are you really__``that stupid``__? " she spat .                                                                                                              |
| **`pcc_eng_26_096.9618_x1551590_25:2-3-4`**    | Is n't__``that stupid``__? "                                                                                                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_stupid_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/`...
* Renaming existing version of `that_great_80ex~80.csv`
* Renaming existing version of `that_uncommon_80ex~80.csv`
* Renaming existing version of `that_hard_80ex~80.csv`
* Renaming existing version of `that_simple_80ex~80.csv`
* Renaming existing version of `that_easy_80ex~80.csv`
* Renaming existing version of `that_big_80ex~80.csv`
* Renaming existing version of `that_bad_80ex~80.csv`
* Renaming existing version of `that_stupid_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_great_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_uncommon_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_hard_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_simple_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_easy_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_big_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_bad_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/that_stupid_80ex~80.csv`

## *exactly*


|                                      |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`    | `l2`          |   `f1` |    `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:-------------------------------------|------:|--------:|--------:|-------:|----------:|:--------|:--------------|-------:|--------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_mirror_] exactly~alike**         |    54 |    0.37 |    7.30 |   0.38 |    517.06 | exactly | alike         |    862 |     144 |   583,470 |      0.21 |       53.79 |        1.00 |    0.06 |   0.06 |           0.37 |            0.22 |            2.64 |  7.32 |   2.40 | mirror      |
| **[_direct_] exactly~stellar**       |   170 |    0.21 |    4.55 |   0.21 |    868.83 | exactly | stellar       | 44,378 |     801 | 6,347,362 |      5.60 |      164.40 |        0.97 |    0.00 |   0.00 |           0.21 |            0.10 |            1.59 | 12.61 |   1.48 | direct      |
| **[_direct_] exactly~alike**         |   162 |    0.14 |    3.93 |   0.15 |    704.69 | exactly | alike         | 44,378 |   1,092 | 6,347,362 |      7.63 |      154.37 |        0.95 |    0.00 |   0.00 |           0.14 |            0.07 |            1.40 | 12.13 |   1.33 | direct      |
| **[_direct_] exactly~ideal**         |   418 |    0.12 |    3.92 |   0.12 |  1,671.10 | exactly | ideal         | 44,378 |   3,355 | 6,347,362 |     23.46 |      394.54 |        0.94 |    0.01 |   0.01 |           0.12 |            0.06 |            1.31 | 19.30 |   1.25 | direct      |
| **[_direct_] exactly~cheap**         |   692 |    0.10 |    3.74 |   0.10 |  2,532.72 | exactly | cheap         | 44,378 |   6,593 | 6,347,362 |     46.10 |      645.90 |        0.93 |    0.01 |   0.02 |           0.10 |            0.06 |            1.23 | 24.55 |   1.18 | direct      |
| **[_mirror_] exactly~right**         |    68 |    0.03 |    3.54 |   0.03 |    302.37 | exactly | right         |    862 |   2,019 |   583,470 |      2.98 |       65.02 |        0.96 |    0.08 |   0.08 |           0.08 |            0.05 |            1.41 |  7.88 |   1.36 | mirror      |
| **[_direct_] exactly~conducive**     |   208 |    0.10 |    3.49 |   0.11 |    767.20 | exactly | conducive     | 44,378 |   1,944 | 6,347,362 |     13.59 |      194.41 |        0.93 |    0.00 |   0.00 |           0.10 |            0.05 |            1.23 | 13.48 |   1.18 | direct      |
| **[_mirror_] exactly~sure**          |   148 |    0.02 |    3.44 |   0.02 |    583.16 | exactly | sure          |    862 |   5,983 |   583,470 |      8.84 |      139.16 |        0.94 |    0.16 |   0.17 |           0.16 |            0.09 |            1.31 | 11.44 |   1.22 | mirror      |
| **[_direct_] exactly~sure**          | 8,797 |    0.06 |    3.23 |   0.07 | 25,676.86 | exactly | sure          | 44,378 | 134,058 | 6,347,362 |    937.28 |    7,859.72 |        0.89 |    0.18 |   0.20 |           0.18 |            0.12 |            1.09 | 83.80 |   0.97 | direct      |
| **[_direct_] exactly~revolutionary** |   120 |    0.09 |    3.13 |   0.10 |    420.36 | exactly | revolutionary | 44,378 |   1,231 | 6,347,362 |      8.61 |      111.39 |        0.93 |    0.00 |   0.00 |           0.09 |            0.05 |            1.19 | 10.17 |   1.14 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/NEQ-exactly_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _exactly alike_


|                                                 | `token_str`                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_084.3862_x1349722_13:14-15-16`**  | Their respective receipts will circulate as competitive currencies , both redeemable , yet not__``exactly alike``__.                                      |
| **`pcc_eng_13_041.8313_x0660228_32:12-13-14`**  | Of course , driving a car and performing brain surgery are n't__``exactly alike``__.                                                                      |
| **`pcc_eng_10_019.6431_x0301270_20:24-25-26`**  | Matter of fact , after receiving education and research , as well as for government agencies or in the best economics books are not__``exactly alike``__. |
| **`pcc_eng_23_069.7066_x1110102_13:14-15`**     | There may be two homes on your street , and they could be__``exactly alike``__, but the one with the extra room / rooms is going to be worth more .       |
| **`pcc_eng_24_006.5951_x0090149_59:11-12`**     | That seems rather clear to me that they both look__``exactly alike``__.                                                                                   |
| **`pcc_eng_08_033.7935_x0530996_05:7-8`**       | We 're twins and we 're__``exactly alike``__.                                                                                                             |
| **`pcc_eng_09_009.1079_x0131344_021:08-09-10`** | There were all sorts of descriptions , none__``exactly alike``__.                                                                                         |
| **`pcc_eng_07_021.3674_x0329404_034:7-8-9`**    | Of course , all drunkards are not__``exactly alike``__; the ruin still preserves the general outline of the primitive structure .                         |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_alike_ex.md`


### 2. _exactly stellar_


|                                                 | `token_str`                                                                                                                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_095.5724_x1528632_060:12-13-14`** | It was a long day for them and the Browns are n't__``exactly stellar``__in the passing game .                                                                                                          |
| **`pcc_eng_15_106.1427_x1699691_080:09-10-11`** | Like many 1973 Topps , the photo is not__``exactly stellar``__.                                                                                                                                        |
| **`pcc_eng_06_073.6214_x1174707_09:13-14-15`**  | the weather on the trip ( and especially that day ) was n't__``exactly stellar``__.                                                                                                                    |
| **`pcc_eng_00_032.5197_x0509415_32:12-13-14`**  | This will in turn hurt their image , which already is n't__``exactly stellar``__in the eyes of most Americans .                                                                                        |
| **`pcc_eng_20_003.1658_x0034741_07:13-14-15`**  | " Grey " sites are n't exceedingly difficult , but they 're not__``exactly stellar``__about facilitating the process , either .                                                                        |
| **`pcc_eng_01_045.2200_x0714444_007:11-12-13`** | While the daily rewards you earn with the card are n't__``exactly stellar``__, its intro bonus is worth a lot more than one would think at first glance .                                              |
| **`pcc_eng_22_009.0615_x0129998_13:15-16-17`**  | This is only due to the imitations of the console 's capabilities which were not__``exactly stellar``__with a 333 MHz processor and a 166 MHz graphics processor with 2 megabytes of embedded memory . |
| **`pcc_eng_10_029.3736_x0458626_05:6-8-9`**     | This government 's record has not been__``exactly stellar``__.                                                                                                                                         |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_stellar_ex.md`


### 3. _exactly ideal_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_076.5779_x1222286_69:6-7-8`**     | However , the outcome is n't__``exactly ideal``__.                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_15_093.6183_x1497105_036:37-38-39`** | Using the current story on the island with the losties waiting / fighting for rescue , countered with the many hints in the flash forward future stories that the events leading up to the rescue were n't__``exactly ideal``__and even a bit of nightmare , you find the drama of the show turned up to eleven as the thirteen episodes play out . |
| **`pcc_eng_04_070.3731_x1120457_02:24-25-26`**  | Last year , I made a robot with a Raspberry Pi but I originally used my laptop to control it - which was n't__``exactly ideal``__.                                                                                                                                                                                                                  |
| **`pcc_eng_03_046.9153_x0743855_12:3-4-5`**     | That 's not__``exactly ideal``__from a usability standpoint .                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_18_001.0031_x0000044_086:20-21-22`** | The Brain Harvest , trying to read it at the slow points in my work day , which is n't__``exactly ideal``__or productive .                                                                                                                                                                                                                          |
| **`pcc_eng_22_006.0997_x0082340_02:5-6-7`**     | Apparently weather conditions were n't__``exactly ideal``__for an end-of-summer float - with high winds blowing and a thunderstorm warning issued - [...]                                                                                                                                                                                           |
| **`pcc_eng_18_009.5257_x0138021_027:10-11-12`** | Gregg will make $ 5.8 million in 2012 , not__``exactly ideal``__for a guy with a WHIP of 1.642 last season and an ERA of 4.37 while picking up 22 saves .                                                                                                                                                                                           |
| **`pcc_eng_19_086.5304_x1382202_015:7-8-9`**    | Which are all delicious but are n't__``exactly ideal``__when you 're trying to drop over 100lbs .                                                                                                                                                                                                                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_ideal_ex.md`


### 4. _exactly cheap_


|                                                 | `token_str`                                                                                                                                                                                                                                 |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_012.7635_x0190279_58:3-4-5`**     | Potatoes are n't__``exactly cheap``__which makes them the type of food you want to buy in bulk .                                                                                                                                            |
| **`pcc_eng_11_006.8989_x0095457_17:24-25-26`**  | I know it sounds like a terrible first world problem but as I had ordered it well in advance and as it was n't__``exactly cheap``__I expected it to be delivered as agreed .                                                                |
| **`pcc_eng_22_001.7087_x0011560_33:7-8-9`**     | quick bit , no frills , not__``exactly cheap``__but budget ok la ... i would go again , when i run out of ideas and want a quiet spot in the ever boisterous vivocity .                                                                     |
| **`pcc_eng_11_081.0721_x1296103_127:08-09-10`** | The rooms are nicely decorated and are not__``exactly cheap``__so it probably does not class as a budget hotel but it is selected primarily for its value because it delivers with enough and yet is still in a prime location .            |
| **`pcc_eng_25_085.7201_x1371149_01:5-6-7`**     | The Nest Thermostat is n't__``exactly cheap``__, but if you 've been in the market for a smart thermostat for a while now and just do n't want to pay full price for one , here 's how you can save money when buying the Nest Thermostat . |
| **`pcc_eng_20_008.1965_x0116043_12:10-11-12`**  | The latter is perhaps surprising as the LOKI is n't__``exactly cheap``__on first review , however when considering the costs of each individual configuration the cost starts to make sense .                                               |
| **`pcc_eng_09_008.2883_x0118066_40:4-5-6`**     | The prices are n't__``exactly cheap``__but it 's a little more private than most places and you can enjoy a quiet sit-down here to see an end to the perfect night .                                                                        |
| **`pcc_eng_04_052.4710_x0831407_25:12-13-14`**  | But the price -- $ 549 without a contract -- is n't__``exactly cheap``__.                                                                                                                                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_cheap_ex.md`


### 5. _exactly right_


|                                                | `token_str`                                                                                                                                                                       |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_051.8408_x0823074_15:23-24`**    | He knew the score , and with a single question reduced the whole industry to a pack of charlatans , which is__``exactly right``__.                                                |
| **`pcc_eng_12_009.1460_x0131745_07:10-11-12`** | You 're not entirely wrong , but you 're not__``exactly right``__either .                                                                                                         |
| **`pcc_eng_11_049.3295_x0781913_248:5-6`**     | JONES : That 's__``exactly right``__, which they did .                                                                                                                            |
| **`pcc_eng_28_005.8690_x0078662_04:22-23`**    | We pride ourselves in sourcing our lifts from the best manufacturers worldwide to ensure that each lift that we install is__``exactly right``__for its planned use and location . |
| **`pcc_eng_14_090.7284_x1450278_25:12-13`**    | I listened to the Mountain Talk candidate forum and you are__``exactly right``__.                                                                                                 |
| **`pcc_eng_01_042.9397_x0677694_018:5-6-7`**   | STERN : It 's not__``exactly right``__but ...                                                                                                                                     |
| **`pcc_eng_05_101.1354_x1619792_35:7-8`**      | DK : I think that 's__``exactly right``__.                                                                                                                                        |
| **`apw_eng_20020206_1608_4:1-3-4`**            | none is__``exactly right``__for everybody .                                                                                                                                       |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_right_ex.md`


### 6. _exactly conducive_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                           |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_035.8826_x0562973_25:54-55-56`** | Most companies ' finance and legal departments still do n't have fixed guidelines for freelancers , so they might ask you to register as a vendor , adhere to a 3 - month payment cycle or in the current scenario , might even expect you to have a GST number as well - not__``exactly conducive``__to creativity . |
| **`pcc_eng_09_093.1069_x1490105_36:13-14-15`** | While Altidore did not play up to expectations , the atmosphere was not__``exactly conducive``__to positive performances .                                                                                                                                                                                            |
| **`pcc_eng_21_074.5469_x1188529_13:21-22-23`** | Monday through Wednesday I 'm flying out to South Dakota to visit an operations center , and business trips are n't__``exactly conducive``__to watching your calorie intake .                                                                                                                                         |
| **`pcc_eng_12_030.1882_x0472626_31:13-14-15`** | For anyone with a weakness for alcohol , dining provided an atmosphere not__``exactly conducive``__to sobriety .                                                                                                                                                                                                      |
| **`nyt_eng_20070904_0152_14:15-16-17`**        | except the kernels were already off the cob , and cut corn kernels are not__``exactly conducive``__to grilling .                                                                                                                                                                                                      |
| **`pcc_eng_03_043.5140_x0688805_03:1-2-3`**    | Not__``exactly conducive``__to concentration , y'know .                                                                                                                                                                                                                                                               |
| **`apw_eng_19970814_1256_11:16-17-18`**        | there are some drawbacks : No main roads go there , and Warsaw winters are n't__``exactly conducive``__to riding a Ferris wheel .                                                                                                                                                                                     |
| **`pcc_eng_29_035.8399_x0562315_34:12-13-14`** | The anticipatory anxiety of competing in a tenuous job market is n't__``exactly conducive``__to cutting class in order to shout into a megaphone and possibly get arrested .                                                                                                                                          |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_conducive_ex.md`


### 7. _exactly sure_


|                                                | `token_str`                                                                                                                                                                                                                                             |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_041.8587_x0660684_13:3-4-5`**    | I 'm not__``exactly sure``__how he even lasted that long without giving up more runs .                                                                                                                                                                  |
| **`pcc_eng_08_040.7169_x0642857_4:29-30-31`**  | Have you ever been asked to assist colleagues in a project that involves requesting access to systems or data that you do n't normally use and you 're not__``exactly sure``__what information you " need " but you think this new data holds the key ? |
| **`pcc_eng_11_086.7898_x1388729_78:13-14-15`** | They have goals they 're moving toward , but often they 're not__``exactly sure``__how to get to them -- or even all that sure what those goals will look like in detail if achieved .                                                                  |
| **`pcc_eng_03_036.6708_x0577822_31:3-4-5`**    | I 'm not__``exactly sure``__what kind of bun they use for the burning man , but we did n't quite like the texture , and the overall taste was not that good , if compare to my baby huey .                                                              |
| **`pcc_eng_27_006.8409_x0093923_3:11-12-13`**  | The Fashion Garret starts their 11th cycle sometime today , not__``exactly sure``__when the magic happens .                                                                                                                                             |
| **`pcc_eng_16_086.0063_x1375882_14:3-4-5`**    | I 'm not__``exactly sure``__what kind of good luck bird poop would bring .                                                                                                                                                                              |
| **`pcc_eng_08_100.8946_x1617424_18:3-4-5`**    | I 'm not__``exactly sure``__what I would have expected from Claremont in response to a questions like this , though I do feel his tone is a bit more low key than I might have guessed .                                                                |
| **`pcc_eng_10_025.2488_x0391752_05:1-2-3`**    | Not__``exactly sure``__how to use stationery ?                                                                                                                                                                                                          |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_sure_ex.md`


### 8. _exactly revolutionary_


|                                                 | `token_str`                                                                                                                                                                                                                                   |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_010.7761_x0157974_05:08-09-10`**  | The notion of a luxury SUV is n't__``exactly revolutionary``__in this day and age , but when the truck launched on June 17 , 1970 , it certainly was .                                                                                        |
| **`pcc_eng_15_049.1225_x0778023_11:5-6-7`**     | " Takers " is n't__``exactly revolutionary``__in glorifying flashy criminals -- gangster movies have done that for years .                                                                                                                    |
| **`pcc_eng_12_015.9826_x0242400_31:09-10-11`**  | With that said , the characters here are n't__``exactly revolutionary``__.                                                                                                                                                                    |
| **`pcc_eng_10_078.9235_x1259501_01:08-09-10`**  | Okay , okay , so this is n't__``exactly revolutionary``__, but how can you resist mini ice cream sandwiches on a popsicle stick ?!                                                                                                            |
| **`pcc_eng_21_066.3814_x1056527_134:13-14-15`** | This part of the module is super in - depth , if not__``exactly revolutionary``__apart from a few specific practices .                                                                                                                        |
| **`pcc_eng_26_035.0576_x0550485_25:21-22-23`**  | The 6s and the 6s Plus , they 're better , but as the names would suggest , they 're not__``exactly revolutionary``__.                                                                                                                        |
| **`pcc_eng_10_026.2572_x0408097_36:7-8-9`**     | The concept for this game is n't__``exactly revolutionary``__, but is enjoyable .                                                                                                                                                             |
| **`pcc_eng_23_081.0523_x1293490_14:7-8-9`**     | On its own , that 's not__``exactly revolutionary``__-- nine - panel is regularly used to denote routine -- but Heisserer and artists Raul Allen and Patricia Martin distinguish themselves by how they incorporate phones into this layout . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_revolutionary_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/`...
* Renaming existing version of `exactly_ideal_80ex~80.csv`
* Renaming existing version of `exactly_cheap_80ex~80.csv`
* Renaming existing version of `exactly_right_80ex~80.csv`
* Renaming existing version of `exactly_sure_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_alike_80ex~69.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_stellar_80ex~45.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_ideal_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_cheap_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_right_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_conducive_80ex~49.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_sure_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_revolutionary_80ex~37.csv`

## *any*


|                            |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`    |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:---------------------------|------:|--------:|--------:|-------:|----------:|:-------|:--------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] any~happier** |   830 |    0.43 |    7.87 |   0.43 |  7,348.55 | any    | happier | 16,176 |  1,909 | 6,347,362 |      4.87 |      825.13 |        0.99 |    0.05 |   0.05 |           0.43 |            0.24 |            2.50 | 28.64 |   2.23 | direct      |
| **[_direct_] any~clearer** |   361 |    0.35 |    7.19 |   0.35 |  2,983.07 | any    | clearer | 16,176 |  1,037 | 6,347,362 |      2.64 |      358.36 |        0.99 |    0.02 |   0.02 |           0.35 |            0.18 |            2.33 | 18.86 |   2.14 | direct      |
| **[_direct_] any~closer**  |   600 |    0.17 |    5.99 |   0.17 |  4,000.91 | any    | closer  | 16,176 |  3,488 | 6,347,362 |      8.89 |      591.11 |        0.99 |    0.04 |   0.04 |           0.17 |            0.10 |            1.93 | 24.13 |   1.83 | direct      |
| **[_mirror_] any~closer**  |    60 |    0.21 |    5.98 |   0.21 |    465.53 | any    | closer  |  1,083 |    285 |   583,470 |      0.53 |       59.47 |        0.99 |    0.06 |   0.06 |           0.21 |            0.13 |            2.18 |  7.68 |   2.05 | mirror      |
| **[_direct_] any~worse**   | 1,797 |    0.15 |    5.92 |   0.15 | 11,618.05 | any    | worse   | 16,176 | 11,891 | 6,347,362 |     30.30 |    1,766.70 |        0.98 |    0.11 |   0.11 |           0.15 |            0.13 |            1.89 | 41.68 |   1.77 | direct      |
| **[_direct_] any~easier**  | 1,624 |    0.12 |    5.60 |   0.13 |  9,840.90 | any    | easier  | 16,176 | 12,945 | 6,347,362 |     32.99 |    1,591.01 |        0.98 |    0.10 |   0.10 |           0.12 |            0.11 |            1.79 | 39.48 |   1.69 | direct      |
| **[_direct_] any~simpler** |   232 |    0.15 |    5.58 |   0.15 |  1,488.36 | any    | simpler | 16,176 |  1,501 | 6,347,362 |      3.83 |      228.17 |        0.98 |    0.01 |   0.01 |           0.15 |            0.08 |            1.86 | 14.98 |   1.78 | direct      |
| **[_mirror_] any~better**  |   386 |    0.10 |    5.56 |   0.10 |  2,549.65 | any    | better  |  1,083 |  3,681 |   583,470 |      6.83 |      379.17 |        0.98 |    0.35 |   0.36 |           0.35 |            0.23 |            1.99 | 19.30 |   1.75 | mirror      |
| **[_direct_] any~younger** |   259 |    0.14 |    5.50 |   0.14 |  1,625.85 | any    | younger | 16,176 |  1,789 | 6,347,362 |      4.56 |      254.44 |        0.98 |    0.02 |   0.02 |           0.14 |            0.08 |            1.83 | 15.81 |   1.75 | direct      |
| **[_direct_] any~safer**   |   246 |    0.13 |    5.40 |   0.14 |  1,516.32 | any    | safer   | 16,176 |  1,792 | 6,347,362 |      4.57 |      241.43 |        0.98 |    0.01 |   0.02 |           0.13 |            0.07 |            1.80 | 15.39 |   1.73 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/NEQ-any_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _any happier_


|                                                | `token_str`                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_042.6710_x0674310_19:4-5-6`**    | The scene is n't__``any happier``__in India .                                                                                                      |
| **`pcc_eng_22_087.0707_x1391287_13:12-13-14`** | Glaber 's pregnant wife , Ilithyia ( Viva Bianca ) is n't__``any happier``__about it , especially when he insists that she accompany him .         |
| **`pcc_eng_05_003.2939_x0037260_22:3-5-6`**    | I ca n't be__``any happier``__with the final product and the level of workmanship .                                                                |
| **`pcc_eng_19_043.2745_x0682546_12:23-26-27`** | " I ca n't be disappointed with the way she is going , she galloped really well this week and I could n't really be__``any happier``__with her . " |
| **`pcc_eng_02_002.1020_x0017827_44:11-12-13`** | If these medications are such wonder drugs why are we not__``any happier``__?                                                                      |
| **`pcc_eng_07_026.8183_x0417542_19:3-5-6`**    | I could n't be__``any happier``__for Barboursville Vineyards .                                                                                     |
| **`pcc_eng_07_003.4267_x0039113_32:10-12-13`** | I did my research for this surgery and could not be__``any happier``__with how I look !!                                                           |
| **`pcc_eng_17_053.7912_x0852960_07:13-15-16`** | Kyle and I were married May 15 , 2009 and we could not be__``any happier``__!                                                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_happier_ex.md`


### 2. _any clearer_


|                                                | `token_str`                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_071.1109_x1132821_026:4-6-7`**   | Ye Xiu could n't be__``any clearer``__on the strengths of a Battle Mage .                                                                                                                      |
| **`pcc_eng_05_083.0657_x1328092_030:4-6-7`**   | This point could n't be__``any clearer``__than in a local , Metro- Detroit court where one Judge runs a sobriety court , but the other Judge wo n't allow any of his cases to transfer to it . |
| **`pcc_eng_29_049.8438_x0788751_18:07-09-10`** | The spin on this one ca n't be__``any clearer``__:                                                                                                                                             |
| **`pcc_eng_10_010.9274_x0160335_24:16-18-19`** | Throw in Tom 's engagement to his girlfriend of eight years , and it could n't be__``any clearer``__to Darcy that a relationship between the two of them would n't work .                      |
| **`pcc_eng_01_002.8201_x0029401_11:5-6`**      | He cannot possibly be__``any clearer``__as he spent endless hours for many months assuring Israel and its supporters , while condemning Palestinians without any reservation or remorse .      |
| **`pcc_eng_27_008.5336_x0121269_146:3-5-6`**   | They could n't be__``any clearer``__on that point -- the main point of each passage above .                                                                                                    |
| **`pcc_eng_28_077.0290_x1229808_05:28-31-32`** | The direction was clear ... buy a piece of cardboard ( x by y in dimension ) and paint it red ( really , the instruction could not have been__``any clearer``__, unless you are me ) .         |
| **`pcc_eng_13_008.8532_x0126790_13:20-23-24`** | When my older and only sister went through recruitment at my mom 's alma mater , the choice could n't have been__``any clearer``__.                                                            |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_clearer_ex.md`


### 3. _any closer_


|                                                | `token_str`                                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_099.5486_x1592393_24:7-8`**      | I asked him whether Kurds were__``any closer``__to their historical dream of independence .                                                                                                                                                                                    |
| **`pcc_eng_29_044.6227_x0704880_09:07-09-10`** | In this case , it could n't be__``any closer``__.                                                                                                                                                                                                                              |
| **`pcc_eng_29_003.1257_x0034344_41:31-33-34`** | And while both India and China can both justifiably claim to have made inroads towards the latter over the past 12 months , it 's more realistic to state that neither are__``any closer``__to achieving complete emergence when assessing the grander present - day picture . |
| **`pcc_eng_17_050.9874_x0807565_07:4-6-7`**    | Immigration reform may not be__``any closer``__to the hearts of Puerto Ricans than of any other Americans , but the idea of having " different classes of people " and " not being a full citizen " might be .                                                                 |
| **`pcc_eng_18_004.6571_x0059251_12:24-26-27`** | Now at 28 years old , I 've not only come to peace with my body , but seriously , my ears could n't be__``any closer``__to my head - I literally have no idea what my nine year old self was seeing .                                                                          |
| **`pcc_eng_02_019.9279_x0306384_45:7-8-9`**    | A much needed new stadium is n't__``any closer``__to becoming a reality .                                                                                                                                                                                                      |
| **`pcc_eng_28_094.2985_x1509404_4:16-17`**     | However , these opportunities are mostly missed , because three outsider perspectives prevent us getting__``any closer``__to the man .                                                                                                                                         |
| **`nyt_eng_20041209_0047_94:29-30`**           | HKN-LOCKOUT -LRB- Toronto -RRB- -- Representatives from the National Hockey League and the players union meet for the first time since Sept. 9 to see if they are__``any closer``__to resolving the lockout .                                                                  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_closer_ex.md`


### 4. _any worse_


|                                                | `token_str`                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_061.4200_x0977779_11:15-17-18`** | Warwick is preparing for a lavish dinner party , so John 's timing could n't be__``any worse``__.                                                            |
| **`pcc_eng_27_085.8144_x1371746_46:10-11`**    | After all , many argue , it cannot get__``any worse``__.                                                                                                     |
| **`pcc_eng_28_080.6418_x1288261_14:34-35`**    | I imagined the flat I might get on the road , and how I 'd be alone with my kids in the evening on the side of a Chicago highway if it got__``any worse``__. |
| **`pcc_eng_18_108.3436_x1739116_17:8-9`**      | Only Michael Cera could make this concept__``any worse``__.                                                                                                  |
| **`pcc_eng_12_069.7600_x1110874_35:3-4-5`**    | You are n't__``any worse``__off than renting , and you got a chance to do extremely well .                                                                   |
| **`pcc_eng_27_024.9881_x0387609_37:2-3-4`**    | But not__``any worse``__than many roughly structured Republics with similar problems ( like Turkey and Syria and Libya ) .                                   |
| **`pcc_eng_23_054.6843_x0867648_08:09-10`**    | I 've got to wonder if it 's__``any worse``__than other parts of the country .                                                                               |
| **`pcc_eng_07_072.1302_x1149730_6:7-8`**       | She doesnit think things can get__``any worse``__, but then sheis rescuedoby pirates led by Jean Laffite !                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_worse_ex.md`


### 5. _any easier_


|                                                 | `token_str`                                                                                                                                                                                          |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_036.6205_x0575486_062:19-21-22`** | 5 ) For socialists outside the West , the task is a much more straightforward one , if not therefore__``any easier``__and considerably more dangerous .                                              |
| **`pcc_eng_25_039.9179_x0629948_01:15-16-17`**  | Apple 's newest Mac Book Air , nearly identical to its predecessor , is not__``any easier``__to repair , i Fixit said this week after tearing apart one of the just-released ultra-light notebooks . |
| **`nyt_eng_19990119_0478_5:28-29-30`**          | but if it was difficult for the Senate to try the president in the afternoon , then try to listen to him that night , it was n't__``any easier``__for viewers .                                      |
| **`pcc_eng_27_060.4558_x0960900_16:3-5-6`**     | It could n't be__``any easier``__. "                                                                                                                                                                 |
| **`pcc_eng_12_033.0582_x0518863_02:6-8-9`**     | This crumble recipe really could n't be__``any easier``__, and it can be used for all kinds of fruit crumbles .                                                                                      |
| **`pcc_eng_08_059.1334_x0941393_5:6-8-9`**      | Making money trading Forex could n't be__``any easier``__or more convenient than this !                                                                                                              |
| **`nyt_eng_19990130_0014_13:4-6-7`**            | the sit-ups would n't be__``any easier``__, but they 'd sure seem that way .                                                                                                                         |
| **`pcc_eng_08_052.3742_x0831786_49:3-4`**       | Was Phillip__``any easier``__to deal with and stand outside of the game than in it ?                                                                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_easier_ex.md`


### 6. _any simpler_


|                                                 | `token_str`                                                                                                                                                      |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_037.4734_x0590598_05:22-24-25`**  | It 's just like they asked themselves : " Why possess a haircut ? " useful link and the response could n't be__``any simpler``__: it appears cleaner like that . |
| **`pcc_eng_23_086.5804_x1383271_006:08-10-11`** | Finding professional Annapolis , IL movers could not be__``any simpler``__!                                                                                      |
| **`pcc_eng_15_090.2995_x1443414_071:4-6-7`**    | The recipe could n't be__``any simpler``__.                                                                                                                      |
| **`pcc_eng_03_048.6493_x0771787_28:13-14-15`**  | The PTDC prides itself on being as simple as possible , but not__``any simpler``__.                                                                              |
| **`pcc_eng_03_092.7450_x1485504_10:10-12-13`**  | The basic operation of the GT - 120 could not be__``any simpler``__.                                                                                             |
| **`pcc_eng_00_044.1110_x0696598_23:12-14-15`**  | When your battery is empty , charging it up again could n't be__``any simpler``__!                                                                               |
| **`pcc_eng_20_001.3965_x0006316_16:3-5-6`**     | It can not be__``any simpler``__.                                                                                                                                |
| **`pcc_eng_06_070.0843_x1117789_4:07-09-10`**   | Converting them into an appetizer could not be__``any simpler``__-- for this flavorful recipe , all you need is a toaster !                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_simpler_ex.md`


### 7. _any better_


|                                                | `token_str`                                                                                                                                                                                                          |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_099.2135_x1588662_08:4-7-8`**    | The casting could n't have been__``any better``__.                                                                                                                                                                   |
| **`pcc_eng_24_100.3241_x1606891_10:30-31-32`** | His dad , in a discussion with a reporter shortly after Jamal 's death , must have raised some eyebrows when he told the reporter his son " was not__``any better``__or any worse than any other inner-city kids . " |
| **`pcc_eng_23_074.7880_x1192207_034:17-18`**   | Now I have to get back to my sleeve , and check if the SSSSS is__``any better``__.                                                                                                                                   |
| **`pcc_eng_26_037.4850_x0589964_57:21-22-23`** | " Because I am not working , I do n't have any money and I am saying my condition is n't__``any better``__, " he said .                                                                                              |
| **`pcc_eng_01_096.2466_x1539926_20:27-30-31`** | Such a soft and elegant whisky as we have come to expect from Japanese producers , it paired deliciously with the food and the company could n't have been__``any better``__.                                        |
| **`pcc_eng_01_074.6749_x1191678_22:6-7-8`**    | Those who received training were not__``any better``__at detecting deception than those who did not receive training .                                                                                               |
| **`pcc_eng_29_006.5464_x0089730_06:4-7-8`**    | The weather could n't have been__``any better``__, and those who live here in Colorado know late September at Red Rocks is precarious , at best .                                                                    |
| **`pcc_eng_03_014.3634_x0216234_22:10-11-12`** | Reports from those who have heard his briefings are n't__``any better``__.                                                                                                                                           |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_better_ex.md`


### 8. _any younger_


|                                         | `token_str`                                                                                                                                                                                                              |
|:----------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19960515_0026_32:24-26-27`** | so even though the Jazz lost to the Rockets in the first round last year , and even though Stockton and Malone are n't getting__``any younger``__, it did not matter if the Jazz were bounced in the first round again . |
| **`apw_eng_19981107_0088_6:13-15-16`**  | another said : `` As long as we live , we 're not getting__``any younger``__, but to be alive is wonderful _ no matter how much we suffer . ''                                                                           |
| **`apw_eng_19970215_0592_13:3-5-6`**    | i was n't getting__``any younger``__.                                                                                                                                                                                    |
| **`nyt_eng_19980328_0007_50:4-6-7`**    | `` He 's not getting__``any younger``__, '' she said .                                                                                                                                                                   |
| **`apw_eng_20080415_1153_21:19-21-22`** | although he does n't play in the field , baseball 's top home run hitter since 2004 is n't getting__``any younger``__.                                                                                                   |
| **`nyt_eng_19961114_0375_33:6-8-9`**    | `` We realized we were n't getting__``any younger``__, '' says Klein , a trim , fit woman who like many of the others has run in marathons .                                                                             |
| **`nyt_eng_20000520_0200_42:08-10-11`** | let 's face it , he 's not getting__``any younger``__, but he does have the talent and the ability to win this race , but he needs to be here and have the chance to try .                                               |
| **`nyt_eng_20071130_0032_23:3-5-6`**    | i 'm not getting__``any younger``__, and it takes longer for me to heal , but I expect to play . ''                                                                                                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_younger_ex.md`


### 9. _any safer_


|                                                  | `token_str`                                                                                                                                                                                                                                                                                                                       |
|:-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_021.3314_x0329259_3:18-19-20`**    | Many of the health effects of electronic cigarettes are still uncertain but local physicians say they are not__``any safer``__than traditional cigarettes .                                                                                                                                                                       |
| **`pcc_eng_23_039.4260_x0620930_126:27-28-29`**  | The Honolulu Star-Bulletin is running its usual letter of the day distortion that " despite the Bush Administration 's War on Terror , this country is not__``any safer``__than it was before 9/11 " -- when any historian would be amazed that there indeed , has n't been another terrorist attack in the US in all that time . |
| **`pcc_eng_25_002.1465_x0018667_051:11-13-14`**  | Even generic bottled water is a lot more expensive and not necessarily__``any safer``__than .                                                                                                                                                                                                                                     |
| **`pcc_eng_14_034.7300_x0544917_0857:26-27-28`** | The thought of what could be waiting for her at the island gave her the chills , and standing alone in this cove certainly was n't__``any safer``__.                                                                                                                                                                              |
| **`pcc_eng_26_094.5017_x1512028_19:3-4-5`**      | Motorists are n't__``any safer``__.                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_19_081.9418_x1307800_15:4-5-6`**      | And I 'm not__``any safer``__.                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_19_011.8623_x0175492_45:20-22-23`**   | " We have been spending too much money on a system that is broken , and our communities have not been__``any safer``__for it . "                                                                                                                                                                                                  |
| **`pcc_eng_29_088.6769_x1416106_12:3-4-5`**      | We are not__``any safer``__now than before Saddam was captured and probably at much greater danger than we were before the war .                                                                                                                                                                                                  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_safer_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/`...
* Renaming existing version of `any_happier_80ex~80.csv`
* Renaming existing version of `any_clearer_80ex~80.csv`
* Renaming existing version of `any_closer_80ex~80.csv`
* Renaming existing version of `any_worse_80ex~80.csv`
* Renaming existing version of `any_easier_80ex~80.csv`
* Renaming existing version of `any_better_80ex~80.csv`
* Renaming existing version of `any_safer_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_happier_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_clearer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_closer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_worse_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_easier_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_simpler_80ex~55.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_better_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_younger_80ex~70.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_safer_80ex~80.csv`

## *remotely*


|                                    |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`     | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:-----------------------------------|------:|--------:|--------:|-------:|---------:|:---------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] remotely~comparable** |   125 |    0.05 |    5.03 |   0.05 |   756.79 | remotely | comparable |  6,109 |  2,443 | 6,347,362 |      2.35 |      122.65 |        0.98 |    0.02 |   0.02 |           0.05 |            0.04 |            1.76 | 10.97 |   1.73 | direct      |
| **[_direct_] remotely~close**      |   729 |    0.01 |    3.75 |   0.02 | 2,790.99 | remotely | close      |  6,109 | 46,485 | 6,347,362 |     44.74 |      684.26 |        0.94 |    0.11 |   0.12 |           0.11 |            0.06 |            1.27 | 25.34 |   1.21 | direct      |
| **[_mirror_] remotely~close**      |   233 |    0.04 |    3.34 |   0.05 |   829.53 | remotely | close      |  1,963 |  4,972 |   583,470 |     16.73 |      216.27 |        0.93 |    0.11 |   0.12 |           0.11 |            0.08 |            1.22 | 14.17 |   1.14 | mirror      |
| **[_direct_] remotely~similar**    |   168 |    0.01 |    3.33 |   0.01 |   613.84 | remotely | similar    |  6,109 | 11,228 | 6,347,362 |     10.81 |      157.19 |        0.94 |    0.03 |   0.03 |           0.03 |            0.02 |            1.21 | 12.13 |   1.19 | direct      |
| **[_mirror_] remotely~similar**    |    82 |    0.05 |    3.08 |   0.05 |   300.50 | remotely | similar    |  1,963 |  1,597 |   583,470 |      5.37 |       76.63 |        0.93 |    0.04 |   0.04 |           0.05 |            0.04 |            1.22 |  8.46 |   1.18 | mirror      |
| **[_direct_] remotely~interested** |   365 |    0.01 |    3.05 |   0.01 | 1,113.00 | remotely | interested |  6,109 | 34,247 | 6,347,362 |     32.96 |      332.04 |        0.91 |    0.05 |   0.06 |           0.05 |            0.03 |            1.07 | 17.38 |   1.04 | direct      |
| **[_direct_] remotely~related**    |   174 |    0.01 |    3.05 |   0.01 |   569.46 | remotely | related    |  6,109 | 14,257 | 6,347,362 |     13.72 |      160.28 |        0.92 |    0.03 |   0.03 |           0.03 |            0.02 |            1.12 | 12.15 |   1.10 | direct      |
| **[_direct_] remotely~funny**      |   143 |    0.01 |    2.60 |   0.01 |   399.39 | remotely | funny      |  6,109 | 15,183 | 6,347,362 |     14.61 |      128.39 |        0.90 |    0.02 |   0.02 |           0.02 |            0.01 |            1.01 | 10.74 |   0.99 | direct      |
| **[_direct_] remotely~true**       |   253 |    0.01 |    2.39 |   0.01 |   589.19 | remotely | true       |  6,109 | 35,146 | 6,347,362 |     33.83 |      219.17 |        0.87 |    0.04 |   0.04 |           0.04 |            0.02 |            0.89 | 13.78 |   0.87 | direct      |
| **[_direct_] remotely~qualified**  |    61 |    0.01 |    2.34 |   0.01 |   182.87 | remotely | qualified  |  6,109 |  5,752 | 6,347,362 |      5.54 |       55.46 |        0.91 |    0.01 |   0.01 |           0.01 |            0.01 |            1.05 |  7.10 |   1.04 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/NEQ-remotely_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _remotely comparable_


|                                                 | `token_str`                                                                                                                                                                               |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_097.3545_x1556971_068:09-10-11`** | Pat Dorsey : The U.S. and Greece are n't__``remotely comparable``__.                                                                                                                      |
| **`pcc_eng_01_032.9426_x0516326_1:22-24-25`**   | What is ironic is that with all the technology and what not that we are blessed with today , Supriya is n't even__``remotely comparable``__to Silk , when it comes to pure sensuousness . |
| **`pcc_eng_16_097.4883_x1561897_3:15-16`**      | Can you name a musical artist of the past 20 or so years even__``remotely comparable``__to Charlie Parker , Miles Davis , Elvis , Chuck Berry , Bob Dylan or Janis Joplin ?               |
| **`pcc_eng_06_011.1493_x0164108_102:18-19`**    | The Bering Sea is far too cold and frozen over most of the year to be even__``remotely comparable``__to the English Channel ?                                                             |
| **`pcc_eng_10_019.2527_x0295016_57:5-6-7`**     | The two situations are n't__``remotely comparable``__, and in fact I think they differ in at least six key ways :                                                                         |
| **`pcc_eng_21_063.6691_x1012800_072:1-2-3`**    | Nothing__``remotely comparable``__to the post-World War II de-nazification of Germany has occurred ; only a handful of communists have been prosecuted .                                  |
| **`pcc_eng_19_016.3155_x0247072_69:5-6-7`**     | Her political challenges are n't__``remotely comparable``__to Nixon's .                                                                                                                   |
| **`pcc_eng_08_073.1834_x1168686_12:07-11-12`**  | A key problem here is that not all values are__``remotely comparable``__.                                                                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_comparable_ex.md`


### 2. _remotely close_


|                                                | `token_str`                                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_003.5078_x0040372_26:32-37-38`** | It seems highly likely that the DOH review will recommend further consideration of the health impacts - particularly in light of the specific reference to the three studies mentioned above , none of which will be__``remotely close``__to completion within a " few weeks . " |
| **`pcc_eng_21_081.5360_x1301617_47:34-35`**    | And still , I will go out and pick up guys , let them use me , make me dirty all over again because the only thing that makes me feel anything even__``remotely close``__to real in this world is the guilt .                                                                    |
| **`pcc_eng_08_107.2266_x1720081_09:10-12-13`** | ( Seriously , that never happened to me , not even__``remotely close``__to happening . )                                                                                                                                                                                         |
| **`pcc_eng_18_010.9692_x0161302_045:1-3-4`**   | Nothing even__``remotely close``__to that .                                                                                                                                                                                                                                      |
| **`pcc_eng_04_079.0567_x1260900_37:3-4-5`**    | I was never__``remotely close``__to Woody .                                                                                                                                                                                                                                      |
| **`pcc_eng_16_053.8488_x0855378_26:1-2-3`**    | Not__``remotely close``__to prior bottles .                                                                                                                                                                                                                                      |
| **`pcc_eng_18_009.7913_x0142251_28:4-6-7`**    | I have seen nothing even__``remotely close``__to that since , although reporters have asked me about it and have implied that they are comparable ever since the tea party movement .                                                                                            |
| **`pcc_eng_14_009.4118_x0135764_43:09-10-11`** | And the pleasure I take in it is not__``remotely close``__to the feeling I will have if the Jets can somehow win a Super Bowl in my lifetime .                                                                                                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_close_ex.md`


### 3. _remotely similar_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_089.8340_x1435823_27:21-22-23`** | Despite decades of exhaustive scanning no mechanisms have ever been discovered within the Guardians structure ; it appears to have nothing__``remotely similar``__to information processing systems or moving parts , nor any kind of any generation system - although it must be able to generate and control massive amounts of energy in order to do what it does . |
| **`pcc_eng_22_082.1540_x1311776_20:19-21-22`** | None of that mattered when I started working in the city , however , because the job was n't even__``remotely similar``__to anything I 'd done in the business .                                                                                                                                                                                                       |
| **`pcc_eng_02_002.5867_x0025675_37:6-7-8`**    | ( Ed. : They 're not__``remotely similar``__.                                                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_24_079.0918_x1263217_1:15-16`**     | i think you need to explain how jagr 's game is in any way__``remotely similar``__to torres ' .                                                                                                                                                                                                                                                                        |
| **`pcc_eng_12_068.8236_x1095982_23:24-25-26`** | I would quibble with his worldbuilding - it does n't make sense for his Christian - anologues to celebrate Easter when they have nothing__``remotely similar``__to the Incarnation - but that 's not a moral complaint .                                                                                                                                               |
| **`pcc_eng_17_006.1601_x0083455_34:17-18`**    | Fast - forward and their money turns into patent muscle , and anyone who used anything__``remotely similar``__to the ideas they bought and patented , gets screwed .                                                                                                                                                                                                   |
| **`pcc_eng_13_008.3112_x0118046_32:7-8-9`**    | The way we eat today is n't__``remotely similar``__to the way our ancestors did .                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_04_078.7667_x1256207_60:13-27-28`** | Being only a fictional animal herself , she is nonetheless concerned that none of the goods for which the opponents had registered their earlier CTMs are__``remotely similar``__to " live animals " for which , in her humble opinion , registration for live animals should be allowed -- though not for animals that are both pink and English .                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_similar_ex.md`


### 4. _remotely interested_


|                                                | `token_str`                                                                                                                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20090530_0040_13:09-10-11`**        | but , Palumbo added , `` He is not__``remotely interested``__in the cult of celebrity .                                                                                                                                  |
| **`pcc_eng_18_037.3736_x0588488_10:21-22-23`** | Without US assistance , Israel is quite strong enough to take on any combination of Arab armies , which are n't__``remotely interested``__in such a conflict .                                                           |
| **`pcc_eng_09_003.8255_x0045946_34:29-30-31`** | Lord Justice Leveson is obliged by his terms of reference to make recommendations that support press freedom and in any case he pledged many times that he was not__``remotely interested``__in gagging the newspapers . |
| **`pcc_eng_21_070.8257_x1128388_34:4-5-6`**    | If you are n't__``remotely interested``__in saving spiders , that is okay , just contact us instead !                                                                                                                    |
| **`pcc_eng_17_069.9134_x1113474_02:5-6`**      | If you are even__``remotely interested``__in photography , adventure or the outdoors , then you best be in attendance at the first ever PDN Outdoor Photo Expo .                                                         |
| **`pcc_eng_27_008.2734_x0117141_22:3-4-5`**    | I am not__``remotely interested``__in determining difference .                                                                                                                                                           |
| **`pcc_eng_27_060.9757_x0969337_10:32-33`**    | All of these attributes are shown in this seven- issue series that acts as a prelude to David 's 1990s run of Aquaman , the only time I 've ever been__``remotely interested``__in the character ( sorry , Bill Reed ) . |
| **`pcc_eng_08_085.5488_x1368868_11:09-10`**    | This is must-read for anyone who 's even__``remotely interested``__in working in television .                                                                                                                            |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_interested_ex.md`


### 5. _remotely related_


|                                                 | `token_str`                                                                                                                                                                                                                  |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_046.5054_x0734855_29:8-9`**       | Additionally we note that it is only__``remotely related``__to the primary tasks of maintaining price stability .                                                                                                            |
| **`pcc_eng_22_059.1721_x0940518_066:33-35-36`** | But when the same hook is used for piercing hundreds of devotees who come to fulfill their vows or to draw blood from their foreheads with one and the same razor is not even__``remotely related``__to worshiping a deity . |
| **`pcc_eng_18_092.9466_x1488961_18:5-6`**       | Elaeagnus Angustifolia is only__``remotely related``__to the olive tree .                                                                                                                                                    |
| **`pcc_eng_29_099.2757_x1587875_04:4-6-7`**     | These creatures are not even__``remotely related``__to Dinosaurs , as they are amphibians .                                                                                                                                  |
| **`pcc_eng_28_079.2036_x1264994_36:1-6-7`**     | None of her concern was__``remotely related``__to health , but that 's where fat bigotry always comes back to .                                                                                                              |
| **`pcc_eng_24_079.0658_x1262808_093:23-24-25`** | This 1819 version is very close to what the final version of the Constitution says , if awkwardly worded , and is n't__``remotely related``__to anything Pinckney ever said .                                                |
| **`pcc_eng_13_077.1139_x1230121_28:6-7`**       | Since when that is even__``remotely related``__?                                                                                                                                                                             |
| **`pcc_eng_val_2.02511_x20268_13:4-6-7`**       | Southern Kitchen - Not even__``remotely related``__to the one in Los Gatos .                                                                                                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_related_ex.md`


### 6. _remotely funny_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                        |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_049.8663_x0790906_21:30-32-33`**  | Just the fact you can have Burnett and Lynch , two of the funniest women of the last five decades , on screen together in a scene that 's not even__``remotely funny``__is the crux of the problems with Vicky Jenson 's lazy direction .                                                                                                                          |
| **`pcc_eng_25_034.2862_x0538911_12:11-13-14`**  | However , as Barnett points out , the label was n't "__``remotely funny``__" -- if it had , she would have laughed .                                                                                                                                                                                                                                               |
| **`pcc_eng_12_015.5907_x0236155_54:4-5-6`**     | But it 's not__``remotely funny``__.                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_16_029.8081_x0466292_04:3-4-5`**     | There is nothing__``remotely funny``__about this video .                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_21_069.4617_x1106415_163:48-49-50`** | In Chris Heath 's book Pet Shop Boys , Literally , he briefly quotes Neil ( on page 116 of at least some editions ) about this unreleased song : " Sometimes the inspiration behind a song is something funny , though often the song itself is n't__``remotely funny``__.                                                                                         |
| **`pcc_eng_06_079.8378_x1274832_017:09-13-14`** | I would like to thank my family , none of whom are__``remotely funny``__.                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_06_107.1522_x1717198_08:25-34-35`**  | He only wishes for Bode , currently a head trainer for the village security squad ; all sheep in wooden dog costumes , so few of the gags created by result are even__``remotely funny``__; to just find the natural energy his chosen life had been given , and just enjoy the work presented to him , even if the work is just a disappointing endeavor anyway . |
| **`pcc_eng_27_063.1531_x1004836_23:08-10-11`**  | That 's disturbing , disgusting , and not even__``remotely funny``__.                                                                                                                                                                                                                                                                                              |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_funny_ex.md`


### 7. _remotely true_


|                                                | `token_str`                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_090.8710_x1452967_23:3-5-6`**    | That 's not even__``remotely true``__and is a very dangerous message to spread to such a wide audience .                                                                               |
| **`pcc_eng_16_088.6554_x1418960_07:8-9`**      | But is this assessment fair or even__``remotely true``__when it comes to The Duchess of Cornwall 's two children from her first marriage to Andrew Parker -Bowles ?                    |
| **`pcc_eng_11_019.2848_x0295627_02:22-24-25`** | Most people think that a restaurant is the be all and end all of a chef 's career but that is not even__``remotely true``__.                                                           |
| **`pcc_eng_27_035.4660_x0556935_073:4-5-6`**   | This just is n't__``remotely true``__.                                                                                                                                                 |
| **`nyt_eng_20060414_0121_65:6-7-8`**           | but of course that was n't__``remotely true``__.                                                                                                                                       |
| **`pcc_eng_14_008.2396_x0116793_150:3-5-6`**   | That 's not even__``remotely true``__, but it 's a good way to keep people listening to just your own message and not have to change and grow and evolve like we 're supposed to .     |
| **`pcc_eng_25_008.2053_x0116855_17:2-7-8`**    | Actually none of the above is__``remotely true``__.                                                                                                                                    |
| **`pcc_eng_03_084.1890_x1347081_18:3-5-6`**    | This is not even__``remotely true``__, but we liked the spirit that made him walk the Camino in Hugo Boss trousers and a stripy shirt , pumping weights ( I kid you not ) as he went . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_true_ex.md`


### 8. _remotely qualified_


|                                                 | `token_str`                                                                                                                                                                                                                                          |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_042.9529_x0678698_60:16-17-18`**  | Sure teaching special needs takes a certain kind of person , but obviously she was n't__``remotely qualified``__to do so .                                                                                                                           |
| **`pcc_eng_26_084.3059_x1347179_184:3-4-5`**    | I 'm not__``remotely qualified``__to hold an opinion , but find this debate fascinating , drawn as I am by the history those war-pocked shells evoke .                                                                                               |
| **`pcc_eng_25_085.2826_x1364049_17:22-25-26`**  | " The Skeleton Twins " can best be described as : two dysfunctional siblings telling one another how to live when neither is even__``remotely qualified``__to give such advice .                                                                     |
| **`pcc_eng_05_060.5103_x0962870_4:20-21`**      | When a small company is in a staffing pinch some may overreact and hire the first person that is__``remotely qualified``__, rather than waiting for a more fitting candidate .                                                                       |
| **`pcc_eng_25_034.8588_x0548146_117:32-33-34`** | FDA is supposed to be the watchdog of the pharmaceutical industry but more often than not the head of the agency is a former executive of a drug company , or not__``remotely qualified``__or have received substantial amounts of money from them . |
| **`nyt_eng_19990502_0236_3:09-10-11`**          | BUCHANAN-CHINA -LRB- Seattle -RRB- _ China is `` not__``remotely qualified``__''                                                                                                                                                                     |
| **`pcc_eng_18_086.7234_x1388165_067:29-30-31`** | I do n't know how respectable this research is , because I do n't care enough to actually read it , and even if I did I am not__``remotely qualified``__to judge something in this field .                                                           |
| **`pcc_eng_15_092.7806_x1483434_28:4-6-7`**     | If you are not even__``remotely qualified``__for a position , do n't apply .                                                                                                                                                                         |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_qualified_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/`...
* Renaming existing version of `remotely_close_80ex~80.csv`
* Renaming existing version of `remotely_interested_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_comparable_80ex~40.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_close_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_similar_80ex~57.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_interested_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_related_80ex~69.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_funny_80ex~52.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_true_80ex~70.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_qualified_80ex~19.csv`

## *yet*


|                                |    `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`        |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:-------------------------------|-------:|--------:|--------:|-------:|----------:|:-------|:------------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] yet~final**       |    640 |    0.52 |    6.59 |   0.53 |  4,447.60 | yet    | final       | 53,779 |  1,212 | 6,347,362 |     10.27 |      629.73 |        0.98 |    0.01 |   0.01 |           0.52 |            0.27 |            2.12 | 24.89 |   1.79 | direct      |
| **[_direct_] yet~official**    |    352 |    0.36 |    5.56 |   0.37 |  2,112.24 | yet    | official    | 53,779 |    957 | 6,347,362 |      8.11 |      343.89 |        0.98 |    0.01 |   0.01 |           0.36 |            0.18 |            1.84 | 18.33 |   1.64 | direct      |
| **[_direct_] yet~ready**       |  7,505 |    0.25 |    5.21 |   0.25 | 39,484.24 | yet    | ready       | 53,779 | 29,641 | 6,347,362 |    251.14 |    7,253.86 |        0.97 |    0.14 |   0.14 |           0.25 |            0.19 |            1.66 | 83.73 |   1.48 | direct      |
| **[_direct_] yet~complete**    |  2,175 |    0.26 |    5.19 |   0.26 | 11,415.79 | yet    | complete    | 53,779 |  8,263 | 6,347,362 |     70.01 |    2,104.99 |        0.97 |    0.04 |   0.04 |           0.26 |            0.15 |            1.64 | 45.14 |   1.49 | direct      |
| **[_direct_] yet~ripe**        |    380 |    0.25 |    4.89 |   0.26 |  1,976.18 | yet    | ripe        | 53,779 |  1,454 | 6,347,362 |     12.32 |      367.68 |        0.97 |    0.01 |   0.01 |           0.25 |            0.13 |            1.62 | 18.86 |   1.49 | direct      |
| **[_direct_] yet~over**        |    162 |    0.25 |    4.59 |   0.26 |    834.79 | yet    | over        | 53,779 |    632 | 6,347,362 |      5.35 |      156.65 |        0.97 |    0.00 |   0.00 |           0.25 |            0.13 |            1.61 | 12.31 |   1.48 | direct      |
| **[_direct_] yet~public**      |    467 |    0.17 |    4.28 |   0.18 |  2,050.88 | yet    | public      | 53,779 |  2,592 | 6,347,362 |     21.96 |      445.04 |        0.95 |    0.01 |   0.01 |           0.17 |            0.09 |            1.41 | 20.59 |   1.33 | direct      |
| **[_direct_] yet~eligible**    |    448 |    0.17 |    4.24 |   0.18 |  1,950.56 | yet    | eligible    | 53,779 |  2,531 | 6,347,362 |     21.44 |      426.56 |        0.95 |    0.01 |   0.01 |           0.17 |            0.09 |            1.40 | 20.15 |   1.32 | direct      |
| **[_direct_] yet~clear**       | 10,411 |    0.12 |    3.97 |   0.12 | 39,559.63 | yet    | clear       | 53,779 | 83,958 | 6,347,362 |    711.35 |    9,699.65 |        0.93 |    0.18 |   0.19 |           0.18 |            0.15 |            1.31 | 95.06 |   1.17 | direct      |
| **[_direct_] yet~operational** |    209 |    0.14 |    3.69 |   0.14 |    819.23 | yet    | operational | 53,779 |  1,453 | 6,347,362 |     12.31 |      196.69 |        0.94 |    0.00 |   0.00 |           0.14 |            0.07 |            1.30 | 13.61 |   1.23 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/NEQ-yet_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _yet final_


|                                                | `token_str`                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20080724_1290_6:26-27-28`**         | Tate had apparently sought a fine of $ 8 million , according to FCC officials who asked not to be named because the deal was not__``yet final``__.                                                                                                                                        |
| **`pcc_eng_22_007.3489_x0102498_10:5-6-7`**    | Since the decision is not__``yet final``__and binding , we are not in a position to comment on it any further . "                                                                                                                                                                         |
| **`apw_eng_20020422_0614_6:13-14-15`**         | Maly said that the roster of the three-time defending world champions was not__``yet final``__, and that Augusta was likely to add few other NHL players , depending on playoff results .                                                                                                 |
| **`nyt_eng_20070320_0147_19:09-10-11`**        | the ambassador was told that the deal was not__``yet final``__, according to American and Repsol officials .                                                                                                                                                                              |
| **`pcc_eng_27_034.0899_x0534412_10:11-12-13`** | The KFA official , however , said the schedule is not__``yet final``__.                                                                                                                                                                                                                   |
| **`apw_eng_20091209_0096_2:43-44-45`**         | the World Series champions would trade pitcher Ian Kennedy to the Arizona Diamondbacks , and lefty reliever Phil Coke and outfield prospect Austin Jackson to Detroit , a Major League Baseball official said on condition of anonymity because Tuesday 's deal was not__``yet final``__. |
| **`pcc_eng_05_084.6569_x1353855_04:4-5-6`**    | The agreement is not__``yet final``__as negotiators still need to settle a dispute over controversial policy riders , but congressional leaders hope to announce something Monday evening , according to a Senate source .                                                                |
| **`pcc_eng_22_008.6764_x0123827_03:39-40-41`** | BAYOMBONG , Nueva Vizcaya , Philippines - Embattled Isabela Gov. Grace Padaca yesterday stressed that the ruling of the Commission on Elections ( Comelec ) unseating her and installing her rival , former governor Benjamin Dy , was not__``yet final``__and executory .                |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_final_ex.md`


### 2. _yet official_


|                                                 | `token_str`                                                                                                                                                                                                          |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_032.6551_x0511647_09:38-39-40`**  | The 2014 tyre supplier is supposed to offer up details of next year 's tyre specification to the teams by October 1 and Hembery said his company intends to stick to that even if a deal is not__``yet official``__. |
| **`pcc_eng_25_086.4357_x1382702_16:30-31-32`**  | The sequel to X - Men : First Class is set to start filming from the beginning of 2013 , and a sequel to Avengers Assemble is planned if not__``yet official``__.                                                    |
| **`pcc_eng_01_099.4748_x1591907_5:6-7-8`**      | However , your claim is n't__``yet official``__until you have these Women 's Wife of the Party Liner Socks to prove it !                                                                                             |
| **`apw_eng_20090212_0476_5:3-4-5`**             | results were not__``yet official``__because some lower-ranked skiers had still to race .                                                                                                                             |
| **`pcc_eng_00_061.3232_x0975183_005:08-09-10`** | The 4th hottest year on record ( not__``yet official``__but likely ) .                                                                                                                                               |
| **`pcc_eng_20_007.4763_x0104347_24:4-5-6`**     | The change is not__``yet official``__.                                                                                                                                                                               |
| **`pcc_eng_12_002.2311_x0019898_19:7-8-9`**     | While the SEC 's inquiry is n't__``yet official``__, a source close to Bloomberg spilled the beans and you can expect official word to come soon as a result .                                                       |
| **`pcc_eng_08_076.7369_x1226277_19:23-24-25`**  | He since has moderated his position and has given the military several months to bring home troops , yet the withdraw is not__``yet official``__.                                                                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_official_ex.md`


### 3. _yet ready_


|                                                 | `token_str`                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_004.1738_x0051167_108:36-37-38`** | THE CABIN ANTHRAX , MURPHY , N.C. ( CT&P ) - After analyzing the results of a new Pew Research Center poll conducted just last week , experts have concluded that the United States is not__``yet ready``__for a democratic form of government .                    |
| **`pcc_eng_28_020.3350_x0312591_18:13-14-15`**  | A few minutes later , your top salesperson shares information that was not__``yet ready``__for public consumption .                                                                                                                                                 |
| **`pcc_eng_08_046.4840_x0736265_30:23-24-25`**  | The teenager requesting nasal reshaping who cannot rearrange their sports obligations to allow 6 - 8 weeks for surgery and healing is not__``yet ready``__to commit to the surgery and is not a good candidate for surgery .                                        |
| **`pcc_eng_13_039.9235_x0629290_06:13-14-15`**  | Some have chosen to retire or remain unchanged , as they are not__``yet ready``__to be born again in the same physical body , because the processes that are required for this transformation are truly enormous and very complex .                                 |
| **`pcc_eng_05_087.9874_x1407472_14:15-16-17`**  | They are suitable for readers who still need a formatted reading scheme and are not__``yet ready``__to go onto free readers , but who still want interesting , engaging , real- life books .                                                                        |
| **`pcc_eng_02_043.2331_x0683369_045:12-13-14`** | One enduring argument against the trade is that the Royals were n't__``yet ready``__to win big .                                                                                                                                                                    |
| **`pcc_eng_04_078.9939_x1259891_11:5-6-7`**     | For those who are not__``yet ready``__for a full facelift , this is an excellent , less invasive option which can provide a very natural , often subtle result .                                                                                                    |
| **`nyt_eng_20001115_0281_27:35-36-37`**         | economy has shifted into a lower gear , the Federal Reserve voted Wednesday to hold interest rates steady , but with unemployment low and energy prices high , the central bank said it was not__``yet ready``__to proclaim that inflation was no longer a threat . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_ready_ex.md`


### 4. _yet complete_


|                                                | `token_str`                                                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20080712_0366_11:5-6-7`**           | the agreement , though not__``yet complete``__, signals the start of the final phase of years of on-again , off-again negotiations to get North Korea to abandon its nuclear weapons program .                                                                                                     |
| **`pcc_eng_03_086.0793_x1377778_05:31-32-33`** | The Cardinals said it was aware of the investigation and has " fully cooperated and will continue to do so , " but declined additional comment because the investigation is not__``yet complete``__.                                                                                               |
| **`apw_eng_20020816_0591_5:6-7-8`**            | although a final tally is not__``yet complete``__, it appears that most of the companies that had to file earnings certifications with the Securities and Exchange Commission by last Wednesday 's deadline were able to do so with minimal delays or revisions .                                  |
| **`apw_eng_20031118_0202_12:6-7-8`**           | turkish officials said identification was n't__``yet complete``__.                                                                                                                                                                                                                                 |
| **`pcc_eng_12_033.7517_x0530060_13:18-19-20`** | If you forget to do this , you will not have any reminder that the project is not__``yet complete``__.                                                                                                                                                                                             |
| **`pcc_eng_08_072.3870_x1155826_18:15-16-17`** | A representative involved in the case told Fortune that 's because the investigation is n't__``yet complete``__.                                                                                                                                                                                   |
| **`pcc_eng_02_037.0750_x0583791_14:5-6-7`**    | While the transformation is not__``yet complete``__, RWJBarnabas Health has already achieved $ 53 million in supply chain savings -- with the opportunity to save millions more while continuing to provide its clinicians and patients with the highest quality of medical supplies and devices . |
| **`pcc_eng_09_049.8035_x0789669_10:7-8-9`**    | But he says this process is not__``yet complete``__.                                                                                                                                                                                                                                               |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_complete_ex.md`


### 5. _yet ripe_


|                                                 | `token_str`                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_005.3719_x0071093_006:11-12-13`** | If the grain is chewy - soft , it 's not__``yet ripe``__.                                                                                                                                                                                                           |
| **`pcc_eng_12_043.0971_x0680687_087:09-10-11`** | Green is the color of things young and not__``yet ripe``__.                                                                                                                                                                                                         |
| **`pcc_eng_04_100.1710_x1602190_025:13-14-15`** | But like other Socialists he had to admit that the masses were not__``yet ripe``__for the struggle .                                                                                                                                                                |
| **`nyt_eng_19970523_0350_17:18-19-20`**         | Long deflected criticism of the slow pace of the negotiations by arguing that China 's economy is n't__``yet ripe``__for full liberalization .                                                                                                                      |
| **`pcc_eng_06_101.7006_x1628963_1:43-44-45`**   | When the people are too much attached to savage independence , to be tolerant of the amount of power to which it is for their good that they should be subject , the state of society ( as already observed ) is not__``yet ripe``__for representative government . |
| **`nyt_eng_19990115_0187_40:20-21-22`**         | as a graduate student in European history at Yale University in the 1970s , she found the time was not__``yet ripe``__for someone interested in clothing .                                                                                                          |
| **`pcc_eng_02_094.3027_x1508656_052:4-5-6`**    | But circumstances were not__``yet ripe``__for the erection of a church of the Greek rite .                                                                                                                                                                          |
| **`pcc_eng_06_029.1113_x0454838_06:41-42-43`**  | The D.C. Court of Appeals also said Friday that the city 's ethics board should have the opportunity to rule on Mary Oates Walker 's request to dismiss a 19 - count case against her , suggesting the matter is not__``yet ripe``__for litigation in the courts .  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_ripe_ex.md`


### 6. _yet over_


|                                         | `token_str`                                                                                                                                                                                                                                                                                                            |
|:----------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20081022_0827_8:39-40-41`**  | but while prices will likely blip upward at least briefly as a consequence of any unusually sharp cutback , there are signs that a significant upward trend may be short-lived because of widespread worries that the worst is not__``yet over``__as far as the world 's economic and financial malaise is concerned . |
| **`nyt_eng_19980413_0396_18:4-5-6`**    | the war is not__``yet over``__.                                                                                                                                                                                                                                                                                        |
| **`nyt_eng_19971112_0725_18:13-14-15`** | U.S. Ambassador Bill Richardson told reporters that the crisis with Iraq was not__``yet over``__and that `` we have not ruled out any options including the military option . ''                                                                                                                                       |
| **`apw_eng_20020611_0010_1:26-27-28`**  | the State Department welcomed a continuation in the easing of tensions between India and Pakistan but said the crisis involving the South Asian rivals is not__``yet over``__.                                                                                                                                         |
| **`nyt_eng_19961204_0152_3:38-39-40`**  | while 30 of 34 investors and analysts polled by Bloomberg Business News forecast the Bundesbank will leave rates untouched tomorrow , 19 said the cycle of German rate reductions , now in its fifth year , is not__``yet over``__.                                                                                    |
| **`nyt_eng_20001205_0355_16:32-33-34`** | but because a cleanup decision on the Hudson has been delayed so many times , some people also struck a distinct note of caution that their fight for the river was not__``yet over``__.                                                                                                                               |
| **`apw_eng_20090902_0281_1:26-27-28`**  | the euro largely held steady against the dollar on Wednesday , a day after the U.S. currency made gains on concerns the global recession is not__``yet over``__.                                                                                                                                                       |
| **`apw_eng_20090407_0877_5:18-19-20`**  | resurgent fears about the banking sector were partly to blame after analysts warned the financial crisis is not__``yet over``__.                                                                                                                                                                                       |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_over_ex.md`


### 7. _yet public_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_084.7061_x1351888_64:5-6-7`**     | Final sales figures are not__``yet public``__for two schools , but one , Longan Elementary School , sold for $ 1 million .                                                                                                                                                                                                  |
| **`pcc_eng_24_079.7267_x1273480_4:33-34-35`**   | According to Reuters the money should appear on the balance sheet of the third or fourth quarter , " the source said , who declined to be named because the information was not__``yet public``__.                                                                                                                          |
| **`pcc_eng_13_039.4772_x0622127_25:7-8-9`**     | Details about the tentative agreement are not__``yet public``__.                                                                                                                                                                                                                                                            |
| **`pcc_eng_00_010.1111_x0147031_23:4-5-6`**     | The terms are not__``yet public``__.                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_22_080.3348_x1282300_27:11-12-13`**  | Although the details of Ocasio-Cortez and Markey 's plan are n't__``yet public``__, Rep. Ilhan Omar ( D- Minn . ) -- another vocal supporter of the Green New Deal backed by climate campaigners -- told MPR News this week that the broad proposal has enough support to pass the Democratically - controlled U.S. House . |
| **`pcc_eng_05_001.5927_x0009633_06:14-15-16`**  | The sources asked not to be identified because the financial advisory roles are not__``yet public``__.                                                                                                                                                                                                                      |
| **`pcc_eng_19_071.6981_x1141924_043:17-18-19`** | At the time , it was known to us through intelligence sources -- but it was not__``yet public``__-- that there was an organization headed up by a man named A.Q. Khan .                                                                                                                                                     |
| **`pcc_eng_11_067.2683_x1072662_09:4-5-6`**     | The figures are not__``yet public``__, but he described them as " awesome . "                                                                                                                                                                                                                                               |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_public_ex.md`


### 8. _yet eligible_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                             |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_015.0280_x0227166_19:18-19-20`** | But thanks to the ACA , private exchanges can expand their market to include users who are not__``yet eligible``__for Medicare .                                                                                                                                                                                                                                        |
| **`pcc_eng_21_099.2159_x1586794_12:6-7-8`**    | We assumed that we were not__``yet eligible``__to vote in Minnesota , because we had just arrived .                                                                                                                                                                                                                                                                     |
| **`pcc_eng_01_068.2947_x1088548_04:30-31-32`** | Yahoo Sports and others have reported that agent Craig Landis and Halos general manager Jerry Dipoto are working on a deal that would be the biggest for a player not__``yet eligible``__for arbitration .                                                                                                                                                              |
| **`pcc_eng_28_068.7278_x1095853_14:28-29-30`** | Over 2,800 employers would lose access to the Early Retiree Reinsurance Program , which is currently helping them provide health benefits to 13 million retirees who are not__``yet eligible``__for Medicare .                                                                                                                                                          |
| **`pcc_eng_17_046.1997_x0730198_30:18-19-20`** | In a study published in Health Affairs , researchers reported that Americans younger than 65 ( and not__``yet eligible``__for our single - payer Medicare program ) are more likely to die because of a lack of timely access to affordable , effective care than people in the same age group in the single payer systems in France , Germany and the United Kingdom . |
| **`nyt_eng_20001018_0490_21:18-19-20`**        | Stumpel , 28 , was a restricted free agent -- a player whose contract has expired but not__``yet eligible``__for unrestricted free agency .                                                                                                                                                                                                                             |
| **`pcc_eng_05_084.9531_x1358621_11:08-09-10`** | This will impact millions of older Americans not__``yet eligible``__for Medicare ( which is available at age 65 ) .                                                                                                                                                                                                                                                     |
| **`nyt_eng_20050227_0080_32:16-17-18`**        | SIGNINGS : Assistant general manager Kim Ng , who is in charge of signing players not__``yet eligible``__for arbitration , was tightlipped about which players have signed .                                                                                                                                                                                            |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_eligible_ex.md`


### 9. _yet clear_


|                                                 | `token_str`                                                                                                                                                                                                              |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20090327_0194_6:10-11-12`**          | South Jakarta Police chief Makmur Simbolon says it is not__``yet clear``__what caused the failure of the 10-meter-high -LRB- 32-foot-high -RRB- dam .                                                                    |
| **`pcc_eng_17_041.5460_x0655059_15:3-4-5`**     | It is not__``yet clear``__who staged Monday 's assault ; some Indian officials have alleged the involvement of Lashkar-e-Taiba , the Pakistani anti-India group responsible for the 2008 terror strikes on Mumbai .      |
| **`apw_eng_20090828_0058_18:13-14-15`**         | whether that 's enough to try to fight Alinghi 's venue is not__``yet clear``__.                                                                                                                                         |
| **`pcc_eng_22_080.7171_x1288422_19:3-4-5`**     | It is n't__``yet clear``__why , but lions often rub their heads on surfaces before scent-marking them with urine , suggesting that compounds that occur on their heads are somehow involved in olfactory communication . |
| **`nyt_eng_19980815_0115_19:11-12-13`**         | exactly how the fragments will fit into the structure is not__``yet clear``__.                                                                                                                                           |
| **`pcc_eng_14_007.0040_x0097073_268:08-09-10`** | However , Simpson said that it is not__``yet clear``__what impact the brown anole will have on green anole populations .                                                                                                 |
| **`pcc_eng_05_089.8169_x1436802_15:3-4-5`**     | It is not__``yet clear``__whether the Islamist parties will form one coalition inside the parliament , or the Brotherhood will seek to ally with the liberal forces against the more radical Nour Party .                |
| **`pcc_eng_19_044.7757_x0706678_6:14-15-16`**   | Whether this has an impact on current goalkeeper coach Max de Jong is not__``yet clear``__.                                                                                                                              |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_clear_ex.md`


### 10. _yet operational_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                          |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20070117_0032_23:17-18-19`**         | that will include Kennedy Airport , where one lane opened yesterday but with its shoe scanner not__``yet operational``__.                                                                                                                                                                                                            |
| **`pcc_eng_00_008.7044_x0124354_091:25-26-27`** | Ultimately , I believe systems like these , and like the other eight similar concepts about which I 've been briefed but which are not__``yet operational``__, are going to change the world , forever .                                                                                                                             |
| **`nyt_eng_19990503_0318_36:7-8-9`**            | 8 . The Death Star is not yet operational                                                                                                                                                                                                                                                                                            |
| **`pcc_eng_25_008.5617_x0122632_04:31-32-33`**  | But with Iran 's economy dependent on crude exports that are traded in U.S. dollars , a promised European trade channel to bypass American sanctions has proved complicated , is not__``yet operational``__, and may never be able to handle oil sales .                                                                             |
| **`pcc_eng_25_081.5282_x1303701_17:14-15-16`**  | While the monitors were on order , and after they were installed but not__``yet operational``__, officers , city council members , and others wondered aloud about the wisdom of the idea .                                                                                                                                          |
| **`nyt_eng_20000911_0380_13:5-6-7`**            | `` Because it is not__``yet operational``__, and because its founders represent such a large share of the automobile market , the commission can not say that implementation of the Covisint venture will not cause competitive concerns , '' the FTC said in a statement .                                                          |
| **`pcc_eng_24_108.09436_x1747127_21:15-16-17`** | According to the head of state , the implementation mechanism for this legislation is not__``yet operational``__.                                                                                                                                                                                                                    |
| **`pcc_eng_05_082.2412_x1314888_28:14-15-16`**  | The plan , run jointly by Britain , France and Germany , is not__``yet operational``__, but the fact that the three influential nations banded together to come up with a way to frustrate US sanctions is one more sign that the alliances that helped rebuild western Europe after World War II are being tested as never before . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_operational_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/`...
* Renaming existing version of `yet_final_80ex~80.csv`
* Renaming existing version of `yet_official_80ex~80.csv`
* Renaming existing version of `yet_ready_80ex~80.csv`
* Renaming existing version of `yet_complete_80ex~80.csv`
* Renaming existing version of `yet_ripe_80ex~80.csv`
* Renaming existing version of `yet_public_80ex~80.csv`
* Renaming existing version of `yet_eligible_80ex~80.csv`
* Renaming existing version of `yet_clear_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_final_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_official_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_ready_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_complete_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_ripe_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_over_80ex~52.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_public_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_eligible_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_clear_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_operational_80ex~55.csv`

## *immediately*


|                                             |    `f` |   `dP1` |   `LRC` |   `P1` |       `G2` | `l1`        | `l2`             |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |    `t` |   `MI` | `dataset`   |
|:--------------------------------------------|-------:|--------:|--------:|-------:|-----------:|:------------|:-----------------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|-------:|-------:|:------------|
| **[_mirror_] immediately~available**        |    187 |    0.06 |    5.43 |   0.06 |   1,249.24 | immediately | available        |    578 |  3,078 |   583,470 |      3.05 |      183.95 |        0.98 |    0.32 |   0.32 |           0.32 |            0.19 |            1.98 |  13.45 |   1.79 | mirror      |
| **[_direct_] immediately~clear**            | 24,476 |    0.29 |    5.43 |   0.29 | 141,537.62 | immediately | clear            | 57,730 | 83,958 | 6,347,362 |    763.61 |   23,712.39 |        0.97 |    0.41 |   0.42 |           0.41 |            0.35 |            1.89 | 151.57 |   1.51 | direct      |
| **[_direct_] immediately~available**        | 21,281 |    0.25 |    5.19 |   0.26 | 115,831.59 | immediately | available        | 57,730 | 81,972 | 6,347,362 |    745.54 |   20,535.46 |        0.96 |    0.36 |   0.37 |           0.36 |            0.31 |            1.78 | 140.77 |   1.46 | direct      |
| **[_direct_] immediately~reachable**        |    110 |    0.31 |    4.75 |   0.32 |     608.82 | immediately | reachable        | 57,730 |    342 | 6,347,362 |      3.11 |      106.89 |        0.97 |    0.00 |   0.00 |           0.31 |            0.16 |            1.71 |  10.19 |   1.55 | direct      |
| **[_direct_] immediately~apparent**         |  2,134 |    0.21 |    4.73 |   0.22 |  10,005.27 | immediately | apparent         | 57,730 |  9,794 | 6,347,362 |     89.08 |    2,044.92 |        0.96 |    0.04 |   0.04 |           0.21 |            0.12 |            1.50 |  44.27 |   1.38 | direct      |
| **[_direct_] immediately~adjacent**         |     95 |    0.29 |    4.51 |   0.30 |     507.33 | immediately | adjacent         | 57,730 |    321 | 6,347,362 |      2.92 |       92.08 |        0.97 |    0.00 |   0.00 |           0.29 |            0.14 |            1.66 |   9.45 |   1.51 | direct      |
| **[_direct_] immediately~obvious**          |  2,310 |    0.09 |    3.47 |   0.10 |   7,286.66 | immediately | obvious          | 57,730 | 22,422 | 6,347,362 |    203.93 |    2,106.07 |        0.91 |    0.04 |   0.04 |           0.09 |            0.07 |            1.11 |  43.82 |   1.05 | direct      |
| **[_direct_] immediately~recognizable**     |    234 |    0.09 |    2.97 |   0.10 |     698.71 | immediately | recognizable     | 57,730 |  2,440 | 6,347,362 |     22.19 |      211.81 |        0.91 |    0.00 |   0.00 |           0.09 |            0.05 |            1.07 |  13.85 |   1.02 | direct      |
| **[_direct_] immediately~life-threatening** |     62 |    0.12 |    2.84 |   0.13 |     221.09 | immediately | life-threatening | 57,730 |    480 | 6,347,362 |      4.37 |       57.63 |        0.93 |    0.00 |   0.00 |           0.12 |            0.06 |            1.21 |   7.32 |   1.15 | direct      |
| **[_direct_] immediately~evident**          |    467 |    0.07 |    2.78 |   0.08 |   1,195.35 | immediately | evident          | 57,730 |  6,121 | 6,347,362 |     55.67 |      411.33 |        0.88 |    0.01 |   0.01 |           0.07 |            0.04 |            0.96 |  19.03 |   0.92 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/NEQ-immediately_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _immediately available_


|                                                | `token_str`                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_044.7949_x0708160_18:09-10-11`** | A spokesman for the committee said lawmakers were not__``immediately available``__for additional comment .                                                                                                                    |
| **`apw_eng_20021025_0760_4:4-5-6`**            | chinese officials were not__``immediately available``__for reaction and often do not comment immediately on such developments .                                                                                               |
| **`pcc_eng_03_039.9051_x0630276_11:26-27-28`** | U.S. lawmakers who have in the past expressed concerns about the prospect of the deal between AT&T and Huawei either declined to comment or were not__``immediately available``__.                                            |
| **`apw_eng_20030923_0333_17:5-6-7`**           | Governing Council officials were not__``immediately available``__for comment .                                                                                                                                                |
| **`apw_eng_19970423_1247_4:4-5-6`**            | damage estimates were not__``immediately available``__, though the Seoul Regency Hotel in the island 's resort district was evacuated after cracks were found in some walls , said Guam Civil Defense Director John Rosario . |
| **`apw_eng_20090916_1384_14:7-8-9`**           | a spokesman for General Dynamics was not__``immediately available``__to comment Wednesday evening .                                                                                                                           |
| **`pcc_eng_23_040.9886_x0646074_10:09-10-11`** | Further details about the couple 's arrest were not__``immediately available``__.                                                                                                                                             |
| **`pcc_eng_00_041.9693_x0661923_12:6-7-8`**    | Attorney information for him was not__``immediately available``__.                                                                                                                                                            |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_available_ex.md`


### 2. _immediately clear_


|                                             | `token_str`                                                                                                                                                                     |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20020112_0169_30:3-4-5`**        | it was not__``immediately clear``__who found the tape or other evidence in Afghanistan .                                                                                        |
| **`apw_eng_20020809_0349_12:3-4-5`**        | it was not__``immediately clear``__whether the two protests were linked .                                                                                                       |
| **`apw_eng_19980506_0049_4:3-4-5`**         | it was not__``immediately clear``__how many people were staying at the hotel .                                                                                                  |
| **`apw_eng_19980211_0436_8:3-4-5`**         | it was not__``immediately clear``__if the parties , which generally support Iraq , would heed the ban , which appears to be aimed at avoiding giving Jordan a pro-Iraqi image . |
| **`pcc_eng_23_009.3761_x0135164_3:3-4-5`**  | It was n't__``immediately clear``__if the roof , ceiling or balcony had collapsed during a performance .                                                                        |
| **`apw_eng_20090228_0759_3:3-4-5`**         | it is not__``immediately clear``__what intervention would involve .                                                                                                             |
| **`pcc_eng_07_100.2294_x1603522_11:3-4-5`** | It was not__``immediately clear``__if she had legal representation .                                                                                                            |
| **`apw_eng_20020610_1172_5:3-4-5`**         | it was not__``immediately clear``__where the two monks were found .                                                                                                             |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_clear_ex.md`


### 3. _immediately reachable_


|                                                | `token_str`                                                                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_046.4634_x0735883_11:4-5-6`**    | Mr. Cherney was n't__``immediately reachable``__for comment .                                                                                                                                                |
| **`pcc_eng_08_103.9720_x1667266_12:4-5-6`**    | The hotel was not__``immediately reachable``__by telephone .                                                                                                                                                 |
| **`pcc_eng_24_035.0110_x0550090_11:3-4-5`**    | Apple was not__``immediately reachable``__for comment .                                                                                                                                                      |
| **`pcc_eng_26_040.5565_x0639587_11:12-13-14`** | Semper Fi Management is headed by Frank Palazzolo , who was not__``immediately reachable``__for comment .                                                                                                    |
| **`pcc_eng_11_013.5269_x0202455_11:6-7-8`**    | The Taliban 's spokesman was not__``immediately reachable``__to comment on the latest attack .                                                                                                               |
| **`pcc_eng_19_072.1259_x1148812_07:4-5-6`**    | Algerian officials were not__``immediately reachable``__for comment .                                                                                                                                        |
| **`pcc_eng_05_083.3476_x1332698_5:4-5-6`**     | The company was not__``immediately reachable``__for comment .                                                                                                                                                |
| **`pcc_eng_20_037.8346_x0595457_13:08-09-10`** | After it became clear that Baghdad was not__``immediately reachable``__, the overall commander , General Nixon , ordered Major-General Townshend , Commanding the 6th Indian Division , to hold out at Kut . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_reachable_ex.md`


### 4. _immediately apparent_


|                                                 | `token_str`                                                                                                                                                                                                                                                       |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_064.4179_x1026058_183:14-15`**    | Since bills generates revenues , the value derived from the analytical approach was__``immediately apparent``__to managment and helped gain support for the data-driven approach to decision-making .                                                             |
| **`pcc_eng_28_077.9558_x1244916_12:15-17-18`**  | Is there some unique or useful quality or feature of your product that might not be__``immediately apparent``__?                                                                                                                                                  |
| **`pcc_eng_19_063.2453_x1004897_10:09-10`**     | " Beautifully taught is the Lord's Dhamma ,__``immediately apparent``__, timeless , of the nature of a personal invitation , progressive , to be attained by the wise , each for himself . "                                                                      |
| **`pcc_eng_11_062.4137_x0993913_11:3-5-6`**     | This might not be__``immediately apparent``__because like many pleasures , we develop our deep appreciation of it through practice and exposure .                                                                                                                 |
| **`pcc_eng_27_101.1335_x1619857_089:20-22-23`** | The heavily cropped central photograph of Corby leaves in only her wrist and central facial features ; it is not even__``immediately apparent``__that the photograph is of Corby .                                                                                |
| **`pcc_eng_17_106.0404_x1698140_34:07-09-10`**  | While problems of information delivery may not be__``immediately apparent``__, there are better ways of ensuring the process of its access .                                                                                                                      |
| **`pcc_eng_18_003.9299_x0047488_10:2-3-4`**     | Though not__``immediately apparent``__, slight variations in the opacity of the red metallic film distorts the viewer 's perception ; reflections , shadows , and objects alternately disappear and reappear as one traverses the seemingly simple installation . |
| **`pcc_eng_13_104.1519_x1666725_20:14-15`**     | Forewarned with an understanding of wave personality , however , the disconnect is__``immediately apparent``__.                                                                                                                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_apparent_ex.md`


### 5. _immediately adjacent_


|                                             | `token_str`                                                                                                                                                                                                                              |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_062.5053_x0995884_09:5-6`**   | This project is located__``immediately adjacent``__to Interstate 90 , which has long been seen by the city as an untapped opportunity for growth due to the proximity to this major transportation corridor .                            |
| **`pcc_eng_03_030.8946_x0484047_16:7-8`**   | This is an educational corridor lying__``immediately adjacent``__to elementary and middle schools , an aquatic center , and Virginia Western Community College .                                                                         |
| **`pcc_eng_22_015.7661_x0238154_12:10-11`** | The majority of the trade exhibition space will be__``immediately adjacent``__to the Conference presentations , with delegates congregating in the display area for catering breaks .                                                    |
| **`pcc_eng_02_088.6879_x1417760_27:7-8`**   | First , when they are located__``immediately adjacent``__to the treatment bath , the water from the wash bath is transferred to the treatment bath .                                                                                     |
| **`pcc_eng_17_036.0682_x0566898_03:5-6`**   | The venue has hotels__``immediately adjacent``__to the conference center as well as other reasonably priced hotels nearby .                                                                                                              |
| **`pcc_eng_25_047.0572_x0745687_064:7-8`**  | " They built public latrine buildings__``immediately adjacent``__to the baths , " Schladweiler says , and flushed the latrines by routing the used bathwater under them .                                                                |
| **`pcc_eng_24_008.6487_x0123423_22:10-11`** | This project consisted of a new structure being built__``immediately adjacent``__to the existing church .                                                                                                                                |
| **`pcc_eng_28_056.2064_x0893490_47:12-13`** | The wild , 967,000 - acre Admiralty Island National Monument ,__``immediately adjacent``__to Chichagof Island on which Puerta is believed to have perished , was known to the Native Tlingit Indians as " The Fortress of the Bears . '' |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_adjacent_ex.md`


### 6. _immediately obvious_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                           |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_069.6047_x1108436_26:3-4`**       | What was__``immediately obvious``__when discussions about these different futures began , though , was just how hard it is to step outside the present to think about the future .                                                                                                                                    |
| **`pcc_eng_24_027.4782_x0428081_25:3-4-5`**     | " While not__``immediately obvious``__, all of my art is driven by a concept .                                                                                                                                                                                                                                        |
| **`pcc_eng_04_089.6134_x1431717_11:8-9`**       | Attention to detail & careful maintenance are__``immediately obvious``__.                                                                                                                                                                                                                                             |
| **`pcc_eng_14_001.8794_x0014337_017:49-50-51`** | " We are seeing more younger people , those in their 50s instead of their 60s and 70s , camping at Starbucks , Mc Donald's , Internet and gaming cafes , libraries and other urban spaces , as these are places where people hang out and it is not__``immediately obvious``__that they are homeless , " he added . " |
| **`pcc_eng_10_014.3385_x0215526_65:4-6-7`**     | Although this may not been__``immediately obvious``__to website readers , none of the stories and commentaries I have published on since September 2008 has appeared in print .                                                                                                                                       |
| **`apw_eng_20080906_0198_5:13-14-15`**          | the woman had no visible injuries and the cause of death was not__``immediately obvious``__, he said , adding that it was n't clear how long she had been in the room or how long she had been dead .                                                                                                                 |
| **`pcc_eng_17_107.08344_x1727135_05:43-45-46`** | For each of these types of technology , the basic goal is to solve a problem that could be done by human reasoning , but either the person has incomplete knowledge of the field , or the problem involves variables that may not be__``immediately obvious``__.                                                      |
| **`pcc_eng_23_032.3335_x0505932_13:23-25-26`**  | Probably not : obviously after a round or two of stickering it 'll be clear anyway , and the idea of it not being__``immediately obvious``__to non-players is nice .                                                                                                                                                  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_obvious_ex.md`


### 7. _immediately recognizable_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_097.0815_x1554458_07:15-16`**    | Intense colors , strong lines and engaging subjects - a Meir Salomon painting is__``immediately recognizable``__.                                                                                                                                                                                                                         |
| **`pcc_eng_24_056.1218_x0891342_056:15-16`**   | In addition , many jewelers have their own particular style that makes the ring__``immediately recognizable``__as a designer ring .                                                                                                                                                                                                       |
| **`pcc_eng_11_104.6941_x1678373_08:35-36`**    | With the rectangular earpiece style I first experienced on the Harman Kardon Wireless Over - Ear Headphones ( it's also used on their NC Noise Canceling Headphones ) , the Soho Mini Headphones are__``immediately recognizable``__as Harman Kardon .                                                                                    |
| **`pcc_eng_03_038.8137_x0612548_42:28-30-31`** | The character is based partly on the exploits of Elizabeth Wood , the film 's writer and director , so art really is imitating life -- though neither is__``immediately recognizable``__as such . "                                                                                                                                       |
| **`pcc_eng_09_006.4713_x0088674_08:09-10`**    | It was important to me that he be__``immediately recognizable``__as a wolf , so rather than stylize his face into a half man / half wolf design , I went with a sexy furry concept !                                                                                                                                                      |
| **`pcc_eng_03_047.6171_x0755191_08:7-8`**      | The New Museum by SANAA is__``immediately recognizable``__.                                                                                                                                                                                                                                                                               |
| **`pcc_eng_28_066.1639_x1054318_6:22-23`**     | Books and the bookshelves that house the books will become the wall that defines the library , a symbol of knowledge__``immediately recognizable``__from both inside and out ; from the outside the library will be viewed as a monument and urban landmark , and a much more comfortable and intimate cocoon when view from the inside . |
| **`pcc_eng_09_101.0940_x1619533_13:4-5`**      | There is an__``immediately recognizable``__difference between the early tyrannosaurs and the later tyrannosaurs .                                                                                                                                                                                                                         |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_recognizable_ex.md`


### 8. _immediately life-threatening_


|                                                | `token_str`                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20080111_1136_3:24-25-26`**         | the 19 hurt in the ferry collision -- 10 men and nine women -- suffered mainly head injuries and bone fractures that were not__``immediately life-threatening``__, said Alex Che , a spokesman for the government of Macau , which is a popular gambling enclave . |
| **`pcc_eng_10_048.1360_x0762453_26:3-4-5`**    | It 's not__``immediately life-threatening``__, and in some cases , an AF episode is short-lived and goes away on its own .                                                                                                                                         |
| **`pcc_eng_02_035.8455_x0564005_16:4-5-6`**    | Although gonorrhea is not__``immediately life-threatening``__, it can lead to serious health problems such as infertility in women and infectious arthritis .                                                                                                      |
| **`nyt_eng_19990801_0123_56:4-5-6`**           | the problems are not__``immediately life-threatening``__, but life as a `` normal '' person will never be in DeJong 's future .                                                                                                                                    |
| **`pcc_eng_11_087.8466_x1405644_10:2-3-4`**    | Although not__``immediately life-threatening``__, the impact of these abnormalities on the long term health and quality of life in these patients may be considerable .                                                                                            |
| **`pcc_eng_16_057.6967_x0917816_06:1-6-7`**    | None of these diseases are__``immediately life-threatening``__, but they can make life difficult to bear and place a great financial , emotional and logistical burden on health services , families and carers .                                                  |
| **`nyt_eng_20000717_0016_26:24-25-26`**        | before Kelly began the Proleukin treatments , his T-cell counts were hovering under 170 , toward the worrisome end of the spectrum though not__``immediately life-threatening``__.                                                                                 |
| **`pcc_eng_01_094.9799_x1519652_38:12-13-14`** | Q : So most of the events were problems that were n't__``immediately life-threatening``__but could cause damage over time ?                                                                                                                                        |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_life-threatening_ex.md`


### 9. _immediately evident_


|                                                | `token_str`                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_001.1987_x0003126_17:6-7-8`**    | The blood orange addition is n't__``immediately evident``__on the nose .                                                                                                                                                                           |
| **`nyt_eng_20000308_0481_48:4-5-6`**           | although it is not__``immediately evident``__in the broad market indexes , most shares are currently trading at bear market levels .                                                                                                               |
| **`pcc_eng_07_075.7172_x1207487_02:20-21`**    | When she first laid eyes on Jayson Delaney , bathed in sunlight and appearing so ethereal , it was__``immediately evident``__that he was destined to change her life .                                                                             |
| **`pcc_eng_08_008.8106_x0126249_140:4-5`**     | Sweets it is__``immediately evident``__that this is not your average bakery .                                                                                                                                                                      |
| **`pcc_eng_02_039.4178_x0621583_28:19-20-21`** | The guy took 2 checks and both Carbons from the middle of the book -- so it was n't__``immediately evident``__.                                                                                                                                    |
| **`nyt_eng_19971211_0799_33:6-7-8`**           | `` All the implications are n't__``immediately evident``__, '' said Peter Wypkema , director of government relations for the Council of Forest Industries , a trade association that represents about 130 forestry companies in British Columbia . |
| **`pcc_eng_02_085.4298_x1364977_14:5-6`**      | But two things are__``immediately evident``__.                                                                                                                                                                                                     |
| **`pcc_eng_05_035.6076_x0560532_56:5-6-7`**    | A value that is not__``immediately evident``__in contemporary photographs , but that becomes more evident as time passes .                                                                                                                         |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_evident_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/`...
* Renaming existing version of `immediately_available_80ex~80.csv`
* Renaming existing version of `immediately_clear_80ex~80.csv`
* Renaming existing version of `immediately_apparent_80ex~80.csv`
* Renaming existing version of `immediately_obvious_80ex~80.csv`
* Renaming existing version of `immediately_recognizable_80ex~80.csv`
* Renaming existing version of `immediately_evident_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_available_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_clear_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_reachable_80ex~33.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_apparent_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_adjacent_80ex~70.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_obvious_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_recognizable_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_life-threatening_80ex~18.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_evident_80ex~80.csv`

## *ever*


|                             |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`   | `l2`    |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:----------------------------|------:|--------:|--------:|-------:|---------:|:-------|:--------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] ever~closer**  |   299 |    0.08 |    5.28 |   0.09 | 1,788.53 | ever   | closer  | 10,849 |  3,488 | 6,347,362 |      5.96 |      293.04 |        0.98 |    0.03 |   0.03 |           0.08 |            0.06 |            1.75 | 16.95 |   1.70 | direct      |
| **[_direct_] ever~present** |   366 |    0.04 |    4.13 |   0.04 | 1,610.82 | ever   | present | 10,849 |  9,428 | 6,347,362 |     16.11 |      349.89 |        0.96 |    0.03 |   0.03 |           0.04 |            0.03 |            1.39 | 18.29 |   1.36 | direct      |
| **[_mirror_] ever~perfect** |   206 |    0.15 |    3.95 |   0.16 |   876.15 | ever   | perfect |  4,776 |  1,280 |   583,470 |     10.48 |      195.52 |        0.95 |    0.04 |   0.04 |           0.15 |            0.10 |            1.39 | 13.62 |   1.29 | mirror      |
| **[_direct_] ever~deeper**  |    78 |    0.04 |    3.71 |   0.04 |   356.23 | ever   | deeper  | 10,849 |  1,823 | 6,347,362 |      3.12 |       74.88 |        0.96 |    0.01 |   0.01 |           0.04 |            0.02 |            1.42 |  8.48 |   1.40 | direct      |
| **[_direct_] ever~greater** |   170 |    0.02 |    3.28 |   0.03 |   607.29 | ever   | greater | 10,849 |  6,678 | 6,347,362 |     11.41 |      158.59 |        0.93 |    0.01 |   0.02 |           0.02 |            0.02 |            1.19 | 12.16 |   1.17 | direct      |
| **[_mirror_] ever~certain** |   143 |    0.10 |    3.22 |   0.11 |   499.66 | ever   | certain |  4,776 |  1,284 |   583,470 |     10.51 |      132.49 |        0.93 |    0.03 |   0.03 |           0.10 |            0.07 |            1.20 | 11.08 |   1.13 | mirror      |
| **[_mirror_] ever~enough**  |   147 |    0.10 |    3.22 |   0.11 |   510.66 | ever   | enough  |  4,776 |  1,334 |   583,470 |     10.92 |      136.08 |        0.93 |    0.03 |   0.03 |           0.10 |            0.07 |            1.19 | 11.22 |   1.13 | mirror      |
| **[_direct_] ever~ok**      |    71 |    0.02 |    2.80 |   0.02 |   245.00 | ever   | ok      | 10,849 |  2,962 | 6,347,362 |      5.06 |       65.94 |        0.93 |    0.01 |   0.01 |           0.02 |            0.01 |            1.16 |  7.83 |   1.15 | direct      |
| **[_direct_] ever~perfect** |   218 |    0.02 |    2.78 |   0.02 |   618.91 | ever   | perfect | 10,849 | 12,730 | 6,347,362 |     21.76 |      196.24 |        0.90 |    0.02 |   0.02 |           0.02 |            0.02 |            1.02 | 13.29 |   1.00 | direct      |
| **[_direct_] ever~alone**   |    53 |    0.02 |    2.70 |   0.03 |   188.97 | ever   | alone   | 10,849 |  2,079 | 6,347,362 |      3.55 |       49.45 |        0.93 |    0.00 |   0.00 |           0.02 |            0.01 |            1.19 |  6.79 |   1.17 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/NEQ-ever_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _ever closer_


|                                             | `token_str`                                                                                                                                                                                                                                    |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_077.1112_x1229553_05:16-17`** | He set out for her to do during those six long years , she drew__``ever closer``__to Him , and carried on perhaps the most important work of her life - Prayer .                                                                               |
| **`pcc_eng_12_050.5323_x0800633_57:34-35`** | The American 's day was also made easier when Masten Gregory fell away with an ignition problem , leaving Gurney to be hunted down by team mate Jo Bonnier as the race ran__``ever closer``__to the halfway mark . [ 4 ]                       |
| **`pcc_eng_08_071.1590_x1135969_02:34-35`** | But a three - week - old offensive by rebel fighters in the north of Latakia province , a bastion of President Bashar al- Assad 's Alawite minority , has brought the battle__``ever closer``__and shattered that sense of relative security . |
| **`pcc_eng_10_011.5994_x0171215_08:18-19`** | Summer nuptials are still claiming space on your calendar , while Fall dates are starting to loom__``ever closer``__.                                                                                                                          |
| **`pcc_eng_23_105.7505_x1693320_19:4-5`**   | She also inched__``ever closer``__to the elusive NCAA A cut time of 52.02 .                                                                                                                                                                    |
| **`pcc_eng_16_058.6115_x0932778_11:7-8`**   | The deadline for responses is drawing__``ever closer``__and we would urge you to get involved and submit your thoughts .                                                                                                                       |
| **`pcc_eng_19_089.2708_x1426789_21:17-18`** | Merry 's fast and furious pussy fingering leaves both girls ' tits jiggling as Amira climbs__``ever closer``__to one final explosion .                                                                                                         |
| **`pcc_eng_24_041.0351_x0647071_16:24-25`** | Damien Delaney penned a new contract until 2015 on Wednesday , while Millen confirmed a new contract for captain Mile Jedinak is edging__``ever closer``__.                                                                                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_closer_ex.md`


### 2. _ever present_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_066.1813_x1053201_09:11-12`**  | If you were raised in a home where music was__``ever present``__, like the home that I was raised in , you probably have an appreciation and love of music that plays an important part in your life today .                                                                                                                                                                                                                               |
| **`pcc_eng_03_094.9627_x1521332_43:21-22`**  | The other taciturn and humble , telling anyone and everyone to rein in their egotistic pride and pretense with his__``ever present``__mantra : " The Whale That Spouts Gets the Harpoon . "                                                                                                                                                                                                                                                |
| **`pcc_eng_18_055.0286_x0874795_13:1-2`**    | Ever Present : Daily Intentions for a Life of Now is a book of daily inspirational quotes and poems to uplift and invite personal reflection .                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_16_028.2912_x0441844_66:26-27`**  | " The combination of nearly a million square feet of Dominick 's space being absorbed by the market leaders ... with short-term bankruptcies and the__``ever present``__threat of Amazon 's launch into grocery has created a stall and step backwards in urban Chicago , " says Dan Tausk , a Mid-America principal and director of its urban tenant brokerage who co-authored a study on the Chicago supermarket scene with Dan Maentz . |
| **`pcc_eng_29_082.0301_x1308797_09:09-10`**  | Catherine said ' It was a moving and__``ever present``__memory ' .                                                                                                                                                                                                                                                                                                                                                                         |
| **`pcc_eng_14_023.9744_x0371119_21:19-20`**  | Crossing the creek a half dozen times was challenging with slick rocks and ice but the rewards were__``ever present``__.                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_20_002.7776_x0028438_037:22-23`** | And when we emerge again at the Glen Avenue bridge we find Northern Rough -winged Swallow on the wires with the__``ever present``__Rock Dove .                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_16_022.0321_x0340611_18:15-16`**  | " It was a living hell , the unbearable smell of burning flesh was__``ever present``__.                                                                                                                                                                                                                                                                                                                                                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_present_ex.md`


### 3. _ever perfect_


|                                                 | `token_str`                                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_002.8566_x0029741_14:08-10-11`**  | I 'm not really pursuing perfection - nothing 's__``ever perfect``__.                                                                                                                                                                                                                    |
| **`pcc_eng_25_099.9849_x1601968_333:09-10-11`** | It was a delicate balance that she might not__``ever perfect``__.                                                                                                                                                                                                                        |
| **`pcc_eng_19_074.8831_x1193534_066:2-6-7`**    | Well none of us is__``ever perfect``__, and I know I still have negative thoughts and still have a long road to travel until I can say I can do real honour to the name ' Dreamwalker , and I know like you , we may forever pull ourselves up for making the same mistakes over again . |
| **`pcc_eng_02_095.7967_x1532724_06:4-5-6`**     | A friend is hardly__``ever perfect``__.                                                                                                                                                                                                                                                  |
| **`pcc_eng_17_072.5844_x1156839_39:35-36-37`**  | Says Shawn Johnson , the 2008 Olympic gold medalist on the balance beam : " We just kind of grow up with this mentality that you are n't ever fit enough ; you are n't__``ever perfect``__.                                                                                              |
| **`pcc_eng_29_003.0224_x0032620_74:1-3-4`**     | Nothing 's__``ever perfect``__, " she said .                                                                                                                                                                                                                                             |
| **`pcc_eng_26_086.9023_x1389101_46:6-8-9`**     | All moments remind you that nothing is__``ever perfect``__in Life and Life actually demands you take imperfect scenarios and constantly make imperfect decisions & choices .                                                                                                             |
| **`pcc_eng_01_047.5874_x0752809_68:3-4-5`**     | Life is n't__``ever perfect``__.                                                                                                                                                                                                                                                         |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_perfect_ex.md`


### 4. _ever deeper_


|                                             | `token_str`                                                                                                                                                                                                                                          |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_050.2137_x0795494_09:25-26`** | Gold mine operations in South Africa have come under scrutiny over the past few months following a series of accidents as gold producers mine__``ever deeper``__to offset lower production and reap the benefits of a sharply higher bullion price . |
| **`pcc_eng_20_033.6406_x0527754_15:4-5`**   | They must drill__``ever deeper``__to tap the sinking water table .                                                                                                                                                                                   |
| **`pcc_eng_14_075.1365_x1198770_69:21-22`** | The foreign minister would boast that the Canadians kept " heads up with fixed determination " as the Russians sunk__``ever deeper``__into their chairs .                                                                                            |
| **`pcc_eng_02_106.2493_x1702082_10:11-12`** | New and fantastic technologies were developed that sent the explorers__``ever deeper``__into the blackness of space .                                                                                                                                |
| **`pcc_eng_20_052.8938_x0838360_12:15-16`** | Even worse , the people of Judah , the chosen people , were sinking__``ever deeper``__into moral weakness .                                                                                                                                          |
| **`pcc_eng_22_045.8485_x0724794_10:11-12`** | Messi meanwhile has taken on a new role , playing__``ever deeper``__than before and controlling the play from deep .                                                                                                                                 |
| **`pcc_eng_18_100.7569_x1615902_06:2-3`**   | Drawn__``ever deeper``__into the vortex around Elisa 's death , Grace gradually discovers that even she has her limits .                                                                                                                             |
| **`pcc_eng_18_065.1748_x1039050_12:16-17`** | He has also since moved to Glastonbury , and may perhaps be finding himself drawn__``ever deeper``__into its spell .                                                                                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_deeper_ex.md`


### 5. _ever greater_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                    |
|:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_032.2328_x0505008_25:62-63`**  | While there are many projections of a coming apocalypse , which may already be upon us , people need to also learn about positive alternative future scenarios in order to have hope for the future , and to be able to recognize the paths through the future that can and will , if we make the effort , lead us to__``ever greater``__approximations of paradise on Earth . |
| **`pcc_eng_12_035.3111_x0554974_05:23-24`**  | According to Jobs , Apple has almost 12,000 people in the area and has been forced to rent buildings " at an__``ever greater``__radius " form its headquarters .                                                                                                                                                                                                               |
| **`pcc_eng_24_077.6704_x1240230_09:28-29`**  | The fight for Afrin , a once stable pocket of northwest Syria , has opened a new front in Syria 's multi-sided civil war and highlighted the__``ever greater``__role of foreign powers in the seven- year - old conflict .                                                                                                                                                     |
| **`pcc_eng_25_036.6692_x0577330_05:12-13`**  | The Third Edition , while maintaining these features , reflects the__``ever greater``__breadth and depth of evolutionary science by providing expanded treatment of many topics and by emphasizing the new intellectual and molecular perspectives that have revolutionized evolutionary studies in the last decade .                                                          |
| **`pcc_eng_16_064.1391_x1022021_11:19-20`**  | We share our success by providing a platform for charities to reach a wider audience and have an__``ever greater``__impact by raising funds , awareness and profile of their organisation on the streets of Liverpool ONE .                                                                                                                                                    |
| **`pcc_eng_00_036.4889_x0573293_068:13-14`** | The problem of a society undergoing acceleration is that people crave an__``ever greater``__variety of social experiences out of the sheer sense that they must " keep up . "                                                                                                                                                                                                  |
| **`pcc_eng_29_002.0768_x0017210_61:21-22`**  | In England , as in the United States , drastic crackdowns on gun ownership by law-abiding citizens were accompanied by__``ever greater``__leniency to criminals .                                                                                                                                                                                                              |
| **`pcc_eng_21_060.9051_x0968400_07:19-20`**  | Meanwhile , massive open online courses ( MOOCs ) seem to hold out the possibility of universities reaching__``ever greater``__audiences .                                                                                                                                                                                                                                     |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_greater_ex.md`


### 6. _ever certain_


|                                                 | `token_str`                                                                                                                                                                                                                                     |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_001.6290_x0010022_14:3-5-6`**     | Sure , nothing is__``ever certain``__and the competition is tough , but when you have strong young talent at key positions and a couple of good arms , you 're ahead of the game .                                                              |
| **`pcc_eng_04_040.6433_x0640856_07:08-10-11`**  | When it comes to fortune telling , nothing is__``ever certain``__, but a handful of industry experts share their thoughts on Nevada 's economy in 2014 .                                                                                        |
| **`pcc_eng_24_078.9703_x1261259_11:07-09-10`**  | But Ferguson knows from experience that nothing is__``ever certain``__in football .                                                                                                                                                             |
| **`pcc_eng_12_002.8133_x0029317_046:21-23-24`** | It 's more important to do something the right way even if it does n't produce the correct outcome - nothing is__``ever certain``__so by focusing on the method you give yourself the best chances of producing the preferred outcome .         |
| **`pcc_eng_17_018.6885_x0286260_20:15-16`**     | The news will be about the drop in HIV / AIDS whenever and if__``ever certain``__people desist from certain behaviors .                                                                                                                         |
| **`pcc_eng_26_037.5848_x0591549_09:23-25-26`**  | About a month ago , Smaldone and Ward were tipped off that a cover shot was a possibility with the caveat that nothing is__``ever certain``__.                                                                                                  |
| **`pcc_eng_24_107.08950_x1729489_04:15-16-17`** | Being actually Northern as well as understood for limited budgeting , I am actually never__``ever certain``__whether olive oil coming from Italian inventory is actually really worth devoting a lot more on than a grocery store 's personal . |
| **`pcc_eng_00_030.4322_x0475695_70:25-27-28`**  | This means that we should do all that we can to be prepared , even if we are not certain it will happen ( nothing is__``ever certain``__) .                                                                                                     |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_certain_ex.md`


### 7. _ever enough_


|                                                | `token_str`                                                                                                                                                                                                                             |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_035.0390_x0549301_33:10-11-12`** | Over - the-counter products , traps and gadgets are rarely__``ever enough``__to guarantee the successful extermination of an established pest colony .                                                                                  |
| **`pcc_eng_25_044.3676_x0702147_21:15-18-19`** | In the area of blogging and site- building , at times it feels like nothing is definitely__``ever enough``__.                                                                                                                           |
| **`pcc_eng_09_006.0539_x0082006_15:1-7-8`**    | Nothing the writer can do is__``ever enough``__.                                                                                                                                                                                        |
| **`pcc_eng_20_041.4516_x0653550_136:1-3-4`**   | Nothing is__``ever enough``__for my heart .                                                                                                                                                                                             |
| **`pcc_eng_18_088.1978_x1412120_32:23-24-25`** | It seems that whatever we spend on communications , and however much time we spend on this effort , that it is never__``ever enough``__.                                                                                                |
| **`pcc_eng_11_094.6310_x1515752_21:14-17-18`** | In the area of writing a blog , at times it feels like nothing is usually__``ever enough``__.                                                                                                                                           |
| **`pcc_eng_24_078.6156_x1255518_18:44-45-46`** | Anyone who has ever tried and failed to get someone else 's hand-rolled , organic , locally - sourced python package to behave nicely knows what I mean : it 's nice to have the code in Git Hub , but it 's hardly__``ever enough``__. |
| **`pcc_eng_19_050.7883_x0803660_32:4-5`**      | But is it__``ever enough``__?                                                                                                                                                                                                           |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_enough_ex.md`


### 8. _ever ok_


|                                                | `token_str`                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_097.5356_x1559697_47:23-25-26`** | And ps : grouping me with someone else who seems to have a female embodiment and then calling us LADIES , is never ,__``ever ok``__! " ( September 3 , 2012 ) .                                                              |
| **`pcc_eng_29_061.9817_x0985129_11:3-4`**      | Is it__``ever OK``__to walk away ?                                                                                                                                                                                           |
| **`pcc_eng_17_096.9894_x1551559_16:4-5`**      | How is it ever okay to not tell a man that he 's a father ?!?!!?                                                                                                                                                             |
| **`pcc_eng_07_078.8638_x1258142_64:4-5`**      | Why it is__``ever OK``__to have any perceived conflict of interest , under any circumstances ?                                                                                                                               |
| **`pcc_eng_03_045.3308_x0718149_03:3-4`**      | Is it__``ever OK``__to leave a restaurant without tipping ?                                                                                                                                                                  |
| **`pcc_eng_15_072.8747_x1161099_14:3-4`**      | Is it ever okay as a writer / parent to share how incredibly cute it was the time your kid ate that grape ?                                                                                                                  |
| **`pcc_eng_20_048.5736_x0768542_20:11-12`**    | Ask anyone who 's been on strike if it is ever okay to cross a picket line , and you will likely hear a resounding " No ! "                                                                                                  |
| **`pcc_eng_26_041.9009_x0661462_09:14-15`**    | The panelists discussed everything from the importance of networking to whether it 's__``ever OK``__to work for free , and also talked about how creating a community can be a major step to success in the music business . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_ok_ex.md`


### 9. _ever alone_


|                                                 | `token_str`                                                                                                                                                                                                                       |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_094.4497_x1510283_36:3-4-5`**     | You are not__``ever alone``__.                                                                                                                                                                                                    |
| **`pcc_eng_25_008.9906_x0129507_116:08-09-10`** | We Are Alone , and We Are Not Ever Alone                                                                                                                                                                                          |
| **`pcc_eng_23_031.8473_x0498005_02:44-45-46`**  | This is a special place for pups to share their love and support for each other during difficult times ; it 's a place to light candles , give the " Power of the Paw , " and let everyfur know they are never__``ever alone``__. |
| **`pcc_eng_23_080.2001_x1279736_025:1-6-7`**    | None of these wasps are__``ever alone``__; when the colony gets too big , a group of queens and a group of workers , and rarely a small cohort of males ( the workers are all female ) fly to a new site and begin a new nest .   |
| **`pcc_eng_00_001.4452_x0007168_141:37-41-42`** | On my desk , I found a note card and wrote to a woman I had n't talked to in months , reaching out , reminded again that no matter how isolated we might feel , none of us are__``ever alone``__.                                 |
| **`pcc_eng_18_083.7518_x1340055_070:18-19-20`** | I now never leave children home alone and I also make sure my own two children are never__``ever alone``__with the 16 year old .                                                                                                  |
| **`pcc_eng_23_008.1525_x0115489_02:1-3-4`**     | Nobody is Ever Alone                                                                                                                                                                                                              |
| **`pcc_eng_03_045.5736_x0722035_06:7-8-9`**     | Because truth is , you are never__``ever alone``__.                                                                                                                                                                               |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_alone_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/`...
* Renaming existing version of `ever_closer_80ex~80.csv`
* Renaming existing version of `ever_present_80ex~80.csv`
* Renaming existing version of `ever_greater_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_closer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_present_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_perfect_80ex~57.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_deeper_80ex~78.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_greater_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_certain_80ex~48.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_enough_80ex~52.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_ok_80ex~39.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_alone_80ex~20.csv`

## *longer*


|                                 |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`   | `l2`      |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:--------------------------------|------:|--------:|--------:|-------:|---------:|:-------|:----------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] longer~lasting**   |   155 |    0.11 |    8.01 |   0.11 | 1,560.03 | longer | lasting   |  1,803 |  1,450 | 6,347,362 |      0.41 |      154.59 |        1.00 |    0.09 |   0.09 |           0.11 |            0.10 |            2.66 | 12.42 |   2.58 | direct      |
| **[_direct_] longer~pink**      |    51 |    0.08 |    7.04 |   0.08 |   483.99 | longer | pink      |  1,803 |    610 | 6,347,362 |      0.17 |       50.83 |        1.00 |    0.03 |   0.03 |           0.08 |            0.06 |            2.52 |  7.12 |   2.47 | direct      |
| **[_mirror_] longer~viable**    |    57 |    0.23 |    6.47 |   0.23 |   482.88 | longer | viable    |    841 |    248 |   583,470 |      0.36 |       56.64 |        0.99 |    0.07 |   0.07 |           0.23 |            0.15 |            2.35 |  7.50 |   2.20 | mirror      |
| **[_direct_] longer~viable**    |    61 |    0.01 |    4.53 |   0.01 |   360.74 | longer | viable    |  1,803 |  4,288 | 6,347,362 |      1.22 |       59.78 |        0.98 |    0.03 |   0.03 |           0.03 |            0.02 |            1.72 |  7.65 |   1.70 | direct      |
| **[_direct_] longer~available** |    65 |    0.00 |    0.39 |   0.00 |    51.03 | longer | available |  1,803 | 81,972 | 6,347,362 |     23.28 |       41.72 |        0.64 |    0.02 |   0.04 |           0.02 |            0.01 |            0.46 |  5.17 |   0.45 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/NEQ-longer_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _longer lasting_


|                                              | `token_str`                                                                                                                                                                                    |
|:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_009.9736_x0144892_011:10-11`** | As a tool for change , influence has a__``longer lasting``__effect than simply giving out orders on the office floor or through e-mail .                                                       |
| **`pcc_eng_08_065.4410_x1043920_18:6-7`**    | There 's a deeper ,__``longer lasting``__cooling .                                                                                                                                             |
| **`pcc_eng_10_020.1887_x0310153_58:33-34`**  | " Our recommendation is to build from what exists , so that you can take the AYA program and expand it to make it more flexible more generous and to making a__``longer lasting``__support . " |
| **`pcc_eng_20_004.4505_x0055411_59:8-9`**    | That stimulates the economy and it has__``longer lasting``__effects .                                                                                                                          |
| **`pcc_eng_06_057.7338_x0918076_042:3-4`**   | It is__``longer lasting``__and in my sons case he does not metabolise the medication four about 8 - 10 hours .                                                                                 |
| **`pcc_eng_01_039.9651_x0629582_07:7-8`**    | The next gimmick needs to be__``longer lasting``__blades , but I do n't suppose that would be very profitable for them ..                                                                      |
| **`pcc_eng_19_002.4308_x0023053_05:13-14`**  | When eaten rather than smoked , it also produces a stronger and__``longer lasting``__effect .                                                                                                  |
| **`pcc_eng_06_069.7719_x1112759_19:13-14`**  | Eversense continuous glucose monitor , which promises to be less invasive and__``longer lasting``__than traditional CGMs , still is n't FDA cleared or CE -marked .                            |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_lasting_ex.md`


### 2. _longer pink_


|                                                | `token_str`                                                                                                                                                                              |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000815_0227_55:13-14-15`**        | stir-fry for 1 to 2 minutes , or until the pork is no__``longer pink``__.                                                                                                                |
| **`nyt_eng_20050810_0048_12:21-22-23`**        | while crust bakes , in a large skillet over medium heat , cook the beef until it crumbles and is no__``longer pink``__.                                                                  |
| **`nyt_eng_19990825_0071_74:10-11-12`**        | add ground beef and cook , stirring , until no__``longer pink``__, about 5 minutes .                                                                                                     |
| **`nyt_eng_19990623_0145_82:09-10-11`**        | Simmer about 4 minutes or until chicken is no__``longer pink``__.                                                                                                                        |
| **`nyt_eng_19990214_0151_65:7-8-9`**           | Cook just until the middle is no__``longer pink``__.                                                                                                                                     |
| **`nyt_eng_19991020_0189_2:11-12-13`**         | add half the pork and stir-fry 3 minutes , until no__``longer pink``__.                                                                                                                  |
| **`nyt_eng_19990609_0159_39:14-15-16`**        | bake in 325-degree oven about 45 minutes or until chicken is tender and no__``longer pink``__.                                                                                           |
| **`pcc_eng_03_033.7772_x0530908_13:25-26-27`** | When you flip the chicken for the last time , brush with the reserved barbecue sauce mixture and continue cooking until the chicken is not__``longer pink``__and registers 160 degrees . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_pink_ex.md`


### 3. _longer viable_


|                                                | `token_str`                                                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_047.8229_x0757615_03:32-33-34`** | The CDC 's announcement echos concerns raised by the World Health Organization ( WHO ) earlier this summer , that sounded the alarm that a widespread treatment for the disease was not__``longer viable``__.                                                                                      |
| **`apw_eng_19980203_1320_20:30-31-32`**        | such a situation provides an excuse or a basis for the other party to pull out of the arrangement as the business for which the property is purchased is no__``longer viable``__or a similar property can be purchased cheaper elsewhere .                                                         |
| **`apw_eng_20090307_0165_9:14-15-16`**         | he says only that the `` situation '' means his music business was no__``longer viable``__.                                                                                                                                                                                                        |
| **`nyt_eng_20001018_0372_18:29-30-31`**        | there are no active repair enzymes in a spore , he said , and radioactivity alone would eventually break the DNA into pieces that would make a spore no__``longer viable``__.                                                                                                                      |
| **`apw_eng_19970424_1005_11:23-24-25`**        | with regard to shipbuilders in Spain , Wijers said , `` at the end of next year , if the shipyards are no__``longer viable``__they will cease . ''                                                                                                                                                 |
| **`nyt_eng_20001230_0097_5:38-39-40`**         | his current one , Aetna U.S. Healthcare , will drop all 52,330 Medicare HMO beneficiaries in Ohio on Jan. 1 , having concluded that `` inadequate government reimbursements have made operating a number of our Medicare HMOs no__``longer viable``__. ''                                          |
| **`nyt_eng_19990120_0551_7:08-09-10`**         | the 4 percent target for 1999 was no__``longer viable``__, they argued .                                                                                                                                                                                                                           |
| **`nyt_eng_20051221_0312_40:41-42-43`**        | and one thing Boras correctly pointed out in the massive negotiating manifesto he was schlepping around the baseball world the past month or so was that Damon 's value to a team will not automatically cease the minute he is no__``longer viable``__as either a center fielder or leadoff man . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_viable_ex.md`


### 4. _longer available_


|                                                | `token_str`                                                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_022.8271_x0352686_12:23-24-25`** | Secondly , this list only consists of cycling jerseys that are currently available - three jersey were not included because they are not__``longer available``__.                                                                                                           |
| **`pcc_eng_01_048.8381_x0773080_01:17-18-19`** | It is often said that it is human nature to only appreciate something when it is not__``longer available``__.                                                                                                                                                               |
| **`pcc_eng_14_018.3214_x0279754_43:09-10-11`** | Update 1 : The Download Assistant Extension is not__``longer available``__on the Chrome Store .                                                                                                                                                                             |
| **`pcc_eng_25_099.4125_x1592606_06:4-5-6`**    | The headlights are not__``longer available``__.                                                                                                                                                                                                                             |
| **`pcc_eng_24_083.6680_x1337178_1:4-5-6`**     | This pattern is not__``longer available``__!                                                                                                                                                                                                                                |
| **`pcc_eng_10_025.1543_x0390217_1:09-10-11`**  | The Middle Schools Leadership Program has expired and not__``longer available``__.                                                                                                                                                                                          |
| **`nyt_eng_19960515_0653_7:12-13-14`**         | `` You are potentially going to have a lot of product no__``longer available``__or have great price inflation because of scarcity , '' said Carol Sanger , a spokeswoman for Federated Department Stores Inc. , which operates Bloomingdale 's , Macy 's and other chains . |
| **`pcc_eng_23_081.3808_x1298814_10:13-14-15`** | So just after the statement an Amazon spokesman mentioned that items are not__``longer available``__for sale on that website .                                                                                                                                              |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_available_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/`...
* Renaming existing version of `longer_lasting_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_lasting_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_pink_80ex~9.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_viable_80ex~13.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/longer/longer_available_80ex~23.csv`

## *particularly*


|                                        |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`         | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:---------------------------------------|------:|--------:|--------:|-------:|---------:|:-------------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] particularly~noteworthy** |   360 |    0.25 |    4.37 |   0.26 | 1,627.29 | particularly | noteworthy | 76,722 |  1,370 | 6,347,362 |     16.56 |      343.44 |        0.95 |    0.00 |   0.00 |           0.25 |            0.13 |            1.47 | 18.10 |   1.34 | direct      |
| **[_mirror_] particularly~noteworthy** |    88 |    0.32 |    3.82 |   0.33 |   386.06 | particularly | noteworthy | 10,020 |    264 |   583,470 |      4.53 |       83.47 |        0.95 |    0.01 |   0.01 |           0.32 |            0.16 |            1.46 |  8.90 |   1.29 | mirror      |
| **[_direct_] particularly~fond**       | 1,309 |    0.16 |    3.80 |   0.17 | 4,667.88 | particularly | fond       | 76,722 |  7,835 | 6,347,362 |     94.70 |    1,214.30 |        0.93 |    0.02 |   0.02 |           0.16 |            0.09 |            1.22 | 33.56 |   1.14 | direct      |
| **[_mirror_] particularly~novel**      |    54 |    0.31 |    3.45 |   0.32 |   232.93 | particularly | novel      | 10,020 |    167 |   583,470 |      2.87 |       51.13 |        0.95 |    0.01 |   0.01 |           0.31 |            0.16 |            1.44 |  6.96 |   1.27 | mirror      |
| **[_direct_] particularly~revelatory** |    61 |    0.21 |    3.31 |   0.22 |   253.37 | particularly | revelatory | 76,722 |    274 | 6,347,362 |      3.31 |       57.69 |        0.95 |    0.00 |   0.00 |           0.21 |            0.11 |            1.37 |  7.39 |   1.27 | direct      |
| **[_direct_] particularly~religious**  |   489 |    0.12 |    3.30 |   0.14 | 1,541.37 | particularly | religious  | 76,722 |  3,580 | 6,347,362 |     43.27 |      445.73 |        0.91 |    0.01 |   0.01 |           0.12 |            0.07 |            1.11 | 20.16 |   1.05 | direct      |
| **[_mirror_] particularly~unusual**    |   172 |    0.17 |    3.05 |   0.19 |   539.33 | particularly | unusual    | 10,020 |    922 |   583,470 |     15.83 |      156.17 |        0.91 |    0.02 |   0.02 |           0.17 |            0.09 |            1.13 | 11.91 |   1.04 | mirror      |
| **[_mirror_] particularly~fond**       |   117 |    0.18 |    2.97 |   0.19 |   375.30 | particularly | fond       | 10,020 |    604 |   583,470 |     10.37 |      106.63 |        0.91 |    0.01 |   0.01 |           0.18 |            0.09 |            1.14 |  9.86 |   1.05 | mirror      |
| **[_direct_] particularly~novel**      |   129 |    0.13 |    2.97 |   0.14 |   416.15 | particularly | novel      | 76,722 |    908 | 6,347,362 |     10.98 |      118.02 |        0.91 |    0.00 |   0.00 |           0.13 |            0.07 |            1.13 | 10.39 |   1.07 | direct      |
| **[_direct_] particularly~likeable**   |   108 |    0.13 |    2.83 |   0.14 |   340.97 | particularly | likeable   | 76,722 |    787 | 6,347,362 |      9.51 |       98.49 |        0.91 |    0.00 |   0.00 |           0.13 |            0.06 |            1.12 |  9.48 |   1.06 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/NEQ-particularly_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _particularly noteworthy_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_041.9905_x0663237_013:1-6-7`**   | None of them have been__``particularly noteworthy``__, either , but the one thing each had in common is that they brought something interesting to the table and managed to foul it up spectacularly .                                                                                                                                                                                                       |
| **`pcc_eng_08_107.5881_x1725828_09:09-10-11`** | ( While the current Beetle Bailey strip is n't__``particularly noteworthy``__, I still have fond memories of older strips I 've read in paperback collections . )                                                                                                                                                                                                                                            |
| **`nyt_eng_19990412_0080_7:3-4`**              | this is__``particularly noteworthy``__now as some end-of-the-century retrospectives refer to Churchill as the greatest person of these past 100 years .                                                                                                                                                                                                                                                      |
| **`nyt_eng_20000926_0134_25:46-47-48`**        | but does a Guernica exist ? Or is it just a name symbolic of a tragedy , remaining only on canvas in a museum ? Inland , away from the main coastal highway , it does indeed appear in a pine-rimmed valley , rebuilt , not__``particularly noteworthy``__in structure _ except that the revered oaks , so dear to Basque hearts , are in place , and the elder , a sapling in 1860 , survived the bombing . |
| **`pcc_eng_04_026.4863_x0411993_21:24-25`**    | Okay : so we know that we 've discussed buckled booties for ages and swoon over many a pair , but these are__``particularly noteworthy``__, we swear !                                                                                                                                                                                                                                                       |
| **`pcc_eng_17_050.1513_x0793979_36:07-09-10`** | " In and of themselves , neither is__``particularly noteworthy``__, " he said .                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_07_024.2114_x0375296_20:15-16-17`** | On the face of it , it may appear to be something common and not__``particularly noteworthy``__.                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_21_107.05269_x1721577_16:23-24`**   | The architecture is unique and much of the decorative features are inspired by Achilles - the statue of the dying Achilles is__``particularly noteworthy``__.                                                                                                                                                                                                                                                |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_noteworthy_ex.md`


### 2. _particularly fond_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_031.8396_x0499543_01:23-24-25`** | If you 're in a position where you practically need a Facebook account because of work or school culture but you 're not__``particularly fond``__of leaving your virtual self unattended , the " super-logoff " technique gives you radically more control over your Facebook account .                                                               |
| **`pcc_eng_21_035.9437_x0565103_10:3-4`**      | I am__``particularly fond``__of the fact that he never lowers himself to provide any proof or documentation of his statements .                                                                                                                                                                                                                       |
| **`pcc_eng_21_061.9270_x0984829_03:4-5-6`**    | The paper was never__``particularly fond``__of Cruz to begin with , having supported his impeachment - happy opponent David Dewhurst in the Republican primary , but ultimately concluded that he was a " thoughtful , energetic and dynamic " guy who would " spend his energies standing up for Texans of every background and economic station . " |
| **`pcc_eng_21_011.4695_x0169030_04:7-8-9`**    | Many prominent media figures who are n't__``particularly fond``__of Carlson 's TV work are expressing their support for the Fox Newser and his family .                                                                                                                                                                                               |
| **`pcc_eng_20_048.8480_x0772925_12:1-2-3`**    | Not__``particularly fond``__of your cheeseburger today ?                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_16_072.2127_x1152293_06:10-11`**    | This week , I received two that I was__``particularly fond``__of ..                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_22_007.1284_x0098848_11:28-29-30`** | I 'm not having the most conventional wedding , and can already anticipate some snide comments from a few of my friends ' spouses that I 'm not__``particularly fond``__of and would rather not invite . "                                                                                                                                            |
| **`pcc_eng_13_049.6405_x0786432_274:3-4-5`**   | I 'm not__``particularly fond``__of either .                                                                                                                                                                                                                                                                                                          |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_fond_ex.md`


### 3. _particularly novel_


|                                                | `token_str`                                                                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_084.9897_x1359228_49:35-36-37`** | " Heart on Fire , " the title track to his latest EP , is enthusiastically sung and tightly played in the style of Willie Nile or Southside Johnny ; even if there 's nothing__``particularly novel``__about it , it 's certainly fun .                                                     |
| **`pcc_eng_23_006.9388_x0095981_05:11-13-14`** | Setting a game in the theatre of modern war may not be__``particularly novel``__anymore , but for EA 's long-running Medal of Honor franchise it 's a first .                                                                                                                               |
| **`pcc_eng_00_064.3182_x1023716_003:1-2-3`**   | Nothing__``particularly novel``__about this porno scene -- it 's a standard - issue boy-girl vignette .                                                                                                                                                                                     |
| **`pcc_eng_21_024.6887_x0382786_29:4-5-6`**    | Gastronomic snobbery is nothing__``particularly novel``__.                                                                                                                                                                                                                                  |
| **`pcc_eng_03_038.0558_x0600129_068:4-5`**     | MIRROR provides a__``particularly novel``__take on Poe's " The Tell - Tale Heart . "                                                                                                                                                                                                        |
| **`pcc_eng_13_053.5796_x0849951_44:5-6`**      | The serving method is__``particularly novel``__: the cooked lamb breast is heaped to one side of a tray used for tea ceremonies , surrounded by petite steamed breads ( called mantou ) and a spicy , savory dipping sauce .                                                                |
| **`pcc_eng_25_033.1210_x0519960_021:3-4-5`**   | There 's nothing__``particularly novel``__about utilizing targeted and sometimes conflicting messages to different audiences , but it would be nice if GOPers stopped squealing like little piggies every time they get called on it , and projecting their dishonesty onto everyone else . |
| **`pcc_eng_27_106.1698_x1701274_23:24-25-26`** | For a sense of what awaits , our seven courses began with a raw slice of hamachi and asparagus tips in ponzu - not__``particularly novel``__, but a refreshing start .                                                                                                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_novel_ex.md`


### 4. _particularly revelatory_


|                                                 | `token_str`                                                                                                                                                                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_102.3695_x1639142_7:4-5`**        | IRON MONKEY is__``particularly revelatory``__due to the amazing action sequences directed by Woo -Ping , who went on to                                                                                                                                |
| **`apw_eng_20090205_1554_13:4-5-6`**            | the facts are not__``particularly revelatory``__, none that a reader of daily newspapers -LRB- and there must be few left -RRB- wo n't know .                                                                                                          |
| **`pcc_eng_09_035.6066_x0560265_35:16-17-18`**  | Once again , what she 's saying is absolutely true ( even if it 's not__``particularly revelatory``__) , but it 's how she 's saying it that 's such a disservice .                                                                                    |
| **`pcc_eng_02_097.5983_x1561707_05:23-24-25`**  | Continuously attempting to up itself , or explain itself , After The Wedding is far too self-involved to realise it really is n't__``particularly revelatory``__.                                                                                      |
| **`pcc_eng_07_050.9080_x0806811_21:41-42-43`**  | In fact , the scares are so diminished that the only links between this and previous games in the series are the names of the characters and the story arc which , having finished the game , is neither rewarding nor__``particularly revelatory``__. |
| **`pcc_eng_07_026.6030_x0414177_04:4-8-9`**     | Of course , none of this is__``particularly revelatory``__:                                                                                                                                                                                            |
| **`pcc_eng_21_094.6388_x1512900_13:22-23-24`**  | Extensive liner notes clear up the confusion , but it feels like a lot of work for an album that 's not__``particularly revelatory``__in either music or story .                                                                                       |
| **`pcc_eng_24_077.1833_x1232345_083:19-20-21`** | Altoona is the sole location reporting any snow , and a look at the satellite and radar was n't__``particularly revelatory``__either .                                                                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_revelatory_ex.md`


### 5. _particularly religious_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_061.7029_x0981134_32:08-09-10`**  | It has been reported that she was not__``particularly religious``__and was said to be outgoing .                                                                                                                                                                                                                                                         |
| **`pcc_eng_27_005.2794_x0068673_13:1-5-6`**     | Neither of them were__``particularly religious``__.                                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_13_032.1982_x0504458_13:16-17-18`**  | " I think it 's important that a church sponsors it even if it is n't__``particularly religious``__, " Mc Intosh says .                                                                                                                                                                                                                                  |
| **`nyt_eng_20000828_0205_23:2-3-4`**            | although not__``particularly religious``__, Greenberg never denied his Jewish heritage _ and his decision not to play on Yom Kippur , the most sacred Jewish holiday , during a 1934 pennant race made national headlines , with gentile fans respecting his move .                                                                                      |
| **`pcc_eng_29_010.9994_x0161687_02:4-5-6`**     | Whilst I 'm not__``particularly religious``__, I do have a fascination of religious cultures across the world .                                                                                                                                                                                                                                          |
| **`pcc_eng_04_077.4349_x1234613_27:23-24-25`**  | " There is a large part of the population that considers themselves smart , educated , conscientious , connected people who are not__``particularly religious``__and have not regularly read the Bible , " said Larry Norton , a former publishing executive and president of Illuminated World , the company that is publishing " Bible Illuminated . " |
| **`pcc_eng_06_106.3287_x1703973_51:15-16-17`**  | Shira is a Hebrew name that means " song " ; my parents were n't__``particularly religious``__but liked the way it sounded despite the unforeseen implications of a whole slew of substitute teachers who completely butchered the pronunciation during my formative years .                                                                             |
| **`pcc_eng_21_015.2604_x0230298_082:10-11-12`** | In The Dead-Tossed Waves , the larger village has nothing__``particularly religious``__about it , but has rigid rules intended to protect the village .                                                                                                                                                                                                  |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_religious_ex.md`


### 6. _particularly unusual_


|                                                 | `token_str`                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_073.5930_x1173259_04:19-20-21`**  | For UFC heavyweight Travis Browne , the circumstances surrounding his 12th booking in the promotion 's octagon were n't__``particularly unusual``__.                                                                                                                     |
| **`pcc_eng_20_080.8573_x1290231_081:18-19-20`** | This may seem modern staging , but even as a structural device in lyric poetry this is n't__``particularly unusual``__, in a tradition extending through three centuries , from George Herbert 's " The Collar , " say , to Eliot 's Prufrock poem and Wallace Steven 's |
| **`pcc_eng_25_083.3031_x1332047_34:3-4-5`**     | It 's not__``particularly unusual``__for a couple of Spanish guys to take advantage of the shade to enjoy a cool , refreshing beer , so this encounter between David Sky and Josh Milk does n't come as too much of a surprise .                                         |
| **`pcc_eng_25_083.9881_x1343139_02:3-4-5`**     | There 's nothing__``particularly unusual``__about that -- these things happen , a lot of books get published on military history and they ca n't all be good .                                                                                                           |
| **`pcc_eng_09_017.6118_x0269114_19:5-6`**       | Crane 's candidacy was__``particularly unusual``__in that , unlike Delaney , he still ran for reelection to his congressional seat even though he announced his run for the White House before the intervening midterm .                                                 |
| **`pcc_eng_26_008.9897_x0129026_24:3-4-5`**     | It is not__``particularly unusual``__for a child to experience confusion as they take stock of the world and their place in it .                                                                                                                                         |
| **`pcc_eng_00_034.7195_x0544786_08:3-4-5`**     | This is n't__``particularly unusual``__considering most of their new games focuses on different characters from Assassin's Creed IV Black Flag with Edward Kenway to Assassin's Creed Unity 's Arno Dorian .                                                             |
| **`pcc_eng_24_071.5170_x1140616_40:30-31-32`**  | Also notice in Figure 6 that still , even after accounting for the onset and recovery from volcanic eruptions , the low trend values in recent years are still not__``particularly unusual``__.                                                                          |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_unusual_ex.md`


### 7. _particularly likeable_


|                                                | `token_str`                                                                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_025.4152_x0394502_31:6-7-8`**    | Most of the characters are n't__``particularly likeable``__, but they are n't ones you despise either .                                                                                                    |
| **`pcc_eng_11_060.2436_x0958672_28:1-6-7`**    | Neither of these men was__``particularly likeable``__.                                                                                                                                                     |
| **`pcc_eng_07_103.2411_x1652558_133:3-4-5`**   | She 's not__``particularly likeable``__, but the show would not be the same without her .                                                                                                                  |
| **`pcc_eng_20_003.1812_x0034994_13:5-6-7`**    | Unfortunatrly , Murphy is n't__``particularly likeable``__.                                                                                                                                                |
| **`pcc_eng_17_042.4874_x0670147_32:7-8-9`**    | Teri Garr's Frannie is attractive but not__``particularly likeable``__- the poorly -written domestic squabbles keep us from caring about the lovers , and their dreams are far too shallow to involve us . |
| **`pcc_eng_14_082.3593_x1315203_21:11-12-13`** | However , that said as their partners and friends were not__``particularly likeable``__either it was at times hard to really care .                                                                        |
| **`pcc_eng_04_101.2489_x1619564_146:2-3-4`**   | Characters not__``particularly likeable``__or sympathetic , plot non-existent , too many and not very interesting or clever jewish jokes .                                                                 |
| **`pcc_eng_05_084.9030_x1357825_17:15-20-21`** | His choice made for a refreshing change as did the fact that pretty much none of the characters were__``particularly likeable``__or sympathetic .                                                          |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_likeable_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/`...
* Renaming existing version of `particularly_noteworthy_80ex~80.csv`
* Renaming existing version of `particularly_fond_80ex~80.csv`
* Renaming existing version of `particularly_religious_80ex~80.csv`
* Renaming existing version of `particularly_unusual_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_noteworthy_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_fond_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_novel_80ex~40.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_revelatory_80ex~17.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_religious_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_unusual_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_likeable_80ex~33.csv`

## *terribly*


|                                    |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`     | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` |   `odds_r_disc` |   `t` |   `MI` | `dataset`   |
|:-----------------------------------|------:|--------:|--------:|-------:|---------:|:---------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|--------:|-------:|---------------:|----------------:|----------------:|------:|-------:|:------------|
| **[_direct_] terribly~surprising** |   949 |    0.05 |    3.81 |   0.05 | 3,578.57 | terribly | surprising | 19,801 | 18,886 | 6,347,362 |     58.92 |      890.08 |        0.94 |    0.05 |   0.05 |           0.05 |            0.05 |            1.25 | 28.89 |   1.21 | direct      |
| **[_mirror_] terribly~wrong**      |   422 |    0.05 |    3.40 |   0.05 | 1,488.08 | terribly | wrong      |  2,196 |  8,526 |   583,470 |     32.09 |      389.91 |        0.92 |    0.18 |   0.19 |           0.18 |            0.11 |            1.23 | 18.98 |   1.12 | mirror      |
| **[_direct_] terribly~original**   |   199 |    0.04 |    3.22 |   0.04 |   678.00 | terribly | original   | 19,801 |  4,705 | 6,347,362 |     14.68 |      184.32 |        0.93 |    0.01 |   0.01 |           0.04 |            0.02 |            1.15 | 13.07 |   1.13 | direct      |
| **[_mirror_] terribly~surprising** |    67 |    0.05 |    2.85 |   0.05 |   234.26 | terribly | surprising |  2,196 |  1,270 |   583,470 |      4.78 |       62.22 |        0.93 |    0.03 |   0.03 |           0.05 |            0.04 |            1.18 |  7.60 |   1.15 | mirror      |
| **[_direct_] terribly~surprised**  |   290 |    0.03 |    2.75 |   0.03 |   779.11 | terribly | surprised  | 19,801 | 10,127 | 6,347,362 |     31.59 |      258.41 |        0.89 |    0.01 |   0.01 |           0.03 |            0.02 |            0.98 | 15.17 |   0.96 | direct      |
| **[_direct_] terribly~uncommon**   |   103 |    0.03 |    2.56 |   0.03 |   298.34 | terribly | uncommon   | 19,801 |  3,193 | 6,347,362 |      9.96 |       93.04 |        0.90 |    0.00 |   0.01 |           0.03 |            0.02 |            1.03 |  9.17 |   1.01 | direct      |
| **[_direct_] terribly~impressed**  |   283 |    0.02 |    2.42 |   0.02 |   650.91 | terribly | impressed  | 19,801 | 12,269 | 6,347,362 |     38.27 |      244.73 |        0.86 |    0.01 |   0.01 |           0.02 |            0.02 |            0.88 | 14.55 |   0.87 | direct      |
| **[_direct_] terribly~fond**       |   190 |    0.02 |    2.38 |   0.02 |   453.09 | terribly | fond       | 19,801 |  7,835 | 6,347,362 |     24.44 |      165.56 |        0.87 |    0.01 |   0.01 |           0.02 |            0.01 |            0.90 | 12.01 |   0.89 | direct      |
| **[_direct_] terribly~exciting**   |   393 |    0.02 |    2.27 |   0.02 |   797.90 | terribly | exciting   | 19,801 | 19,956 | 6,347,362 |     62.25 |      330.75 |        0.84 |    0.02 |   0.02 |           0.02 |            0.02 |            0.82 | 16.68 |   0.80 | direct      |
| **[_direct_] terribly~wrong**      |   398 |    0.02 |    2.20 |   0.02 |   775.51 | terribly | wrong      | 19,801 | 21,208 | 6,347,362 |     66.16 |      331.84 |        0.83 |    0.02 |   0.02 |           0.02 |            0.02 |            0.79 | 16.63 |   0.78 | direct      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/NEQ-terribly_top10-bigrams-50_AMscores_2024-08-06.md`


### 1. _terribly surprising_


|                                                | `token_str`                                                                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_033.6374_x0528288_18:31-33-34`** | Seeing how Tinker , Tailor , Soldier , Spy is also a remake , and that Oldman 's character was played in the original by Sir Alec , it would n't be__``terribly surprising``__.                                                        |
| **`pcc_eng_00_068.6230_x1092868_40:15-20-21`** | Given that this is a Lindsay Lohan movie that went straight to video , none of this should be__``terribly surprising``__.                                                                                                              |
| **`pcc_eng_07_028.2856_x0441312_086:7-8-9`**   | So on the whole it 's not__``terribly surprising``__that it caused some damage en route .                                                                                                                                              |
| **`pcc_eng_14_086.6814_x1384902_13:20-21-22`** | And he meets Adriana , Pablo Picasso 's girlfriend , who Gil quickly becomes infatuated with , a task not__``terribly surprising``__since she is played by slinky , stunning Marion Cotillard .                                        |
| **`pcc_eng_24_102.6094_x1643968_04:3-4-5`**    | That is not__``terribly surprising``__: since the start of last year , Lackey has logged 306 2/3 innings of 3.64 ERA ball with 7.8 K/9 and 1.8 BB /9 .                                                                                 |
| **`pcc_eng_15_013.7322_x0205354_10:11-12-13`** | The demise of Gawkerhas been sad to watch but also not__``terribly surprising``__.                                                                                                                                                     |
| **`pcc_eng_15_093.4870_x1495009_11:5-6-7`**    | However , that 's not__``terribly surprising``__since it was our third most trendy puppy name last year , which we suspect has something to do withthe popularity of the Luna Lovegood character in the Harry Potterbooks and movies . |
| **`pcc_eng_06_100.7479_x1613488_04:7-8-9`**    | Most of what Morse said is n't__``terribly surprising``__, especially his noting that U.S. News has much different goals than the President 's goals .                                                                                 |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_surprising_ex.md`


### 2. _terribly wrong_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                               |
|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_068.2918_x1088605_16:6-7`**    | However , something has gone__``terribly wrong``__, and players are the only ones who can help .                                                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_06_032.2047_x0504837_07:17-18`**  | When they insist he give them the Belt of Deltora , Lief realizes that something is__``terribly wrong``__.                                                                                                                                                                                                                                                                                                                |
| **`nyt_eng_19990606_0066_7:37-38`**          | last month , Vanity Fair , which is published by the Conde Nast Publications unit of Advance Publications , ran Bryan Burroughs ' `` Death at Sea : Behind the Scenes at an Ocean-Sailing Race Gone__``Terribly Wrong``__, '' while Dennis Publishing 's Stuff magazine carried a feature by a hiker titled `` Reality Bites : I Saw My Wife Get Killed By a Bear '' in its second issue , which came out two weeks ago . |
| **`nyt_eng_19960403_0132_3:3-4-5`**          | there 's nothing__``terribly wrong``__with Mike Nichols ' scene-by-scene                                                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_04_094.4613_x1509994_37:12-13`**  | But even a simple Google search would have decisively revealed how__``terribly wrong``__it would be to paint everyone on the government 's watch list a " terrorist . "                                                                                                                                                                                                                                                   |
| **`pcc_eng_26_065.8733_x1048859_25:14-15`**  | He was publicly shamed and made to feel that his personal beliefs were__``terribly wrong``__. "                                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_07_104.4893_x1672910_017:11-12`** | Also , after one of Scott 's early shifts goes__``terribly wrong``__, he never really experiences any further consequences from his new-found shifting ability .                                                                                                                                                                                                                                                          |
| **`pcc_eng_17_005.3719_x0070688_295:26-27`** | She gave me a testy look as we neared Wind Song 's underbelly , giving me the distinct feeling that if something were to go__``terribly wrong``__she would wholeheartedly blame me .                                                                                                                                                                                                                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_wrong_ex.md`


### 3. _terribly original_


|                                                | `token_str`                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_015.6410_x0236262_16:1-2-3`**    | Nothing__``terribly original``__there .                                                                                                                                                        |
| **`pcc_eng_18_094.8344_x1519783_16:3-4-5`**    | It was n't__``terribly original``__, but it was fun for the kids .                                                                                                                             |
| **`pcc_eng_22_005.5730_x0073865_07:14-15-16`** | It 's an entertaining read , if a trifle predictable -- Starchasr 's not__``terribly original``__, you see , and his arguments are approximately identical to other such street- preachers ' . |
| **`pcc_eng_00_068.6102_x1092658_02:20-21-22`** | Alice Blanchard drags the readers into the pit with A Breath After Drowning , a thriller that -- while not__``terribly original``__-- is as close to perfect as it can get in this genre .     |
| **`pcc_eng_16_040.8456_x0644974_04:5-6-7`**    | Colour Revolt , while not__``terribly original``__, had a much - appreciated post-hardcore tinge to their solid guitar lines as well as some good stage energy .                               |
| **`nyt_eng_20000109_0032_38:27-29-30`**        | to Stein , the fact that he reveals intimate , seemingly eccentric but actually quite normal aspects of his personality to the readers of Time does not seem__``terribly original``__.         |
| **`pcc_eng_03_035.5226_x0559142_18:7-8-9`**    | Mc Anuff concedes the notion is n't__``terribly original``__, but he notes , " The history of mankind underwent a seismic shift with the detonation of those two bombs .                       |
| **`pcc_eng_25_096.5754_x1546741_106:5-6-7`**   | I guess that 's nothing__``terribly original``__or useful .                                                                                                                                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_original_ex.md`


### 4. _terribly surprised_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                     |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_val_3.10906_x52155_23:38-39-40`**   | " We are emerging as a player in the world , with serious interests - economic , political , commercial in places - and this is what big boys and girls do , and so I 'm not__``terribly surprised``__, but I do n't know the extent of this - nobody does . "                                                                  |
| **`nyt_eng_20000712_0450_2:3-5-6`**            | we would n't be__``terribly surprised``__if all of those involved in the race to anoint Marion Jones the breakout performer of the 2000 Olympics are called back because of a false start .                                                                                                                                     |
| **`pcc_eng_05_009.6783_x0140846_15:3-5-6`**    | I would n't be__``terribly surprised``__if the sell - off was a byproduct of comparatively modest guidance .                                                                                                                                                                                                                    |
| **`pcc_eng_15_042.3589_x0668721_11:3-4-5`**    | I was not__``terribly surprised``__when we received no answer to our long letter .                                                                                                                                                                                                                                              |
| **`pcc_eng_24_102.3059_x1639002_04:13-14-15`** | Now that I have , I 'm a bit disappointed , but not__``terribly surprised``__.                                                                                                                                                                                                                                                  |
| **`pcc_eng_27_028.3615_x0441891_16:20-21-22`** | When I saw that all of the boards combined had over $ 600 million in holdings , I was n't__``terribly surprised``__.                                                                                                                                                                                                            |
| **`pcc_eng_17_102.2962_x1637391_20:12-14-15`** | " Repeal " is a teabagger fantasy , but we would not be__``terribly surprised``__to see the Supreme Court take on the individual mandate at some point in 2016 or so , and if John Roberts is still in charge than we expect they 'll rule 5 - 4 to abolish the Necessary and Proper Clause and shutter the Fed .               |
| **`pcc_eng_06_103.6756_x1661049_40:20-22-23`** | But this online snafu makes me very nervous about what I might find at Gen Con -- I would not be__``terribly surprised``__to find the con bumped from the convention center and arena and out onto the streets of Milwaukee , with cardboard boxes for tables ( if we 're lucky ) and vendors hacking their wares out of vans . |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_surprised_ex.md`


### 5. _terribly uncommon_


|                                                 | `token_str`                                                                                                                                                                                      |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_026.9821_x0419639_32:3-4-5`**     | Plums are n't__``terribly uncommon``__, but not a lot of people are familiar with pluots .                                                                                                       |
| **`pcc_eng_02_017.7265_x0270696_03:08-09-10`**  | Brawls between fans at sporting events are not__``terribly uncommon``__.                                                                                                                         |
| **`nyt_eng_20050330_0011_21:6-7-8`**            | these days , it is not__``terribly uncommon``__for a women 's team to become the competitive face of a major university .                                                                        |
| **`pcc_eng_09_099.1577_x1588269_059:13-14-15`** | In the Andes , for instance , temperatures in the 20s are not__``terribly uncommon``__.                                                                                                          |
| **`pcc_eng_14_031.3481_x0490431_40:3-4-5`**     | It 's not__``terribly uncommon``__for the entire party to be decimated in a seemingly - routine random encounter , especially if they 're just trying to breeze their way through an encounter . |
| **`pcc_eng_20_081.8641_x1306459_03:3-4-5`**     | This is n't__``terribly uncommon``__, but this also was a school nightmare .                                                                                                                     |
| **`pcc_eng_07_107.03206_x1718362_13:4-5-6`**    | And it is not__``terribly uncommon``__for associative arrays to be sparse ( not every index value defined between first and last ) .                                                             |
| **`pcc_eng_16_058.4557_x0930243_23:5-6-7`**     | Apparently , it 's not__``terribly uncommon``__to bleed regularly during the first trimester .                                                                                                   |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_uncommon_ex.md`


### 6. _terribly impressed_


|                                                 | `token_str`                                                                                                                                                                                          |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_047.1462_x0746088_069:6-7-8`**    | Either way , I was not__``terribly impressed``__with the manner in which the character was written -- she could probably be described as half - dimensional : one-quarter fire and one-quarter woe . |
| **`pcc_eng_11_018.9588_x0290360_03:11-12-13`**  | I 've tried dyeing with lawn grass before and was n't__``terribly impressed``__.                                                                                                                     |
| **`pcc_eng_14_094.0526_x1504453_046:08-09-10`** | On a negative note , I was n't__``terribly impressed``__with James Earl Jones 's performance .                                                                                                       |
| **`pcc_eng_13_004.1018_x0049996_15:10-11-12`**  | But here 's the rub : Investors still are n't__``terribly impressed``__.                                                                                                                             |
| **`nyt_eng_20000119_0168_44:19-23-24`**         | i managed to oh-so-casually mention this to all the doctors I spoke to for this column , but none of them were__``terribly impressed``__and none had a miracle cure .                                |
| **`pcc_eng_22_082.5682_x1318482_19:3-4-5`**     | Voters are n't__``terribly impressed``__with that , either .                                                                                                                                         |
| **`pcc_eng_08_073.4096_x1172317_065:13-14-15`** | We also had gumbo at a few places , but I was n't__``terribly impressed``__with the gumbo at those restaurants ...                                                                                   |
| **`pcc_eng_29_059.4714_x0944666_10:15-16`**     | I was underwhelmed if I 'm honest , but I do admit to being__``terribly impressed``__with the fact that I conquered the mythical cheese souffle .                                                    |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_impressed_ex.md`


### 7. _terribly fond_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                             |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_002.8881_x0030727_020:3-4-5`**    | I 'm not__``terribly fond``__of fairy tales for some reason but I did enjoy this book -- the world the author created is written so beautifully and the story and characters are interesting .                                                                                                          |
| **`pcc_eng_04_100.5294_x1607944_09:3-4-5`**     | If youre not__``terribly fond``__of women , you probably shouldnt see Volver , a movie wherein mere mortality doesnt stop mothers from loudly smooching their daughters cheeks , a breezy comedy in which a seemingly typical male gets stabbed , stuffed into a fridge and buried at swamps edge .     |
| **`pcc_eng_27_006.6590_x0090971_08:1-2-3`**     | Not__``terribly fond``__of the greatful dead though .                                                                                                                                                                                                                                                   |
| **`pcc_eng_02_082.0392_x1310260_13:1-5-6`**     | Not that I 'm__``terribly fond``__of any of the Republican muppets , mind you -- the only declared candidate from either side of the aisle that would n't make me retch while I pull the lever is Ron Paul - - but let 's at least give the job to someone who has some experience running something .  |
| **`pcc_eng_06_079.5061_x1269433_47:3-4-5`**     | I 'm not__``terribly fond``__of monkeys after a somewhat unfortunate and terrifying incident at a temple in Malaysia , but Davis was pretty excited to see them up close for the first time - that is until they started chasing & hissing at some kids - note to all - Monkey 's are not your friend ! |
| **`pcc_eng_10_088.9621_x1421758_050:3-4-5`**    | I 'm not__``terribly fond``__of doing curses , but I just love the concept of these little tablets .                                                                                                                                                                                                    |
| **`pcc_eng_12_063.0881_x1003933_03:09-10-11`**  | I 've mentioned before that my husband is not__``terribly fond``__of sandwiches for dinner , mostly because he eats two sandwiches every day of his life for lunch .                                                                                                                                    |
| **`pcc_eng_00_063.9521_x1017787_054:14-15-16`** | I was forced into a rehab program by my probation officer who was not__``terribly fond``__of you .                                                                                                                                                                                                      |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_fond_ex.md`


### 8. _terribly exciting_


|                                               | `token_str`                                                                                                                                                                         |
|:----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_090.9270_x1453467_16:4-5-6`**   | It 's just not__``terribly exciting``__.                                                                                                                                            |
| **`pcc_eng_11_061.7760_x0983564_34:3-4-5`**   | It was n't__``terribly exciting``__, which is what I always want it to be , but it was just really , really lovely , which is what I was n't entirely expecting .                   |
| **`pcc_eng_01_038.5467_x0606822_6:09-10-11`** | Of course , many of the options are n't__``terribly exciting``__, that is , unless you 're particularly fond of microfiber screen cleaning cloths , pillow cases , or beach balls . |
| **`pcc_eng_29_007.7541_x0109199_15:5-6-7`**   | While the oscillators are n't__``terribly exciting``__when taken on their own , the sound of the instrument springs to life when it hits the filter section .                       |
| **`pcc_eng_09_008.1753_x0116227_49:3-5-6`**   | It has n't been__``terribly exciting``__lately , but there 's been the usual offseason type of things - trade rumors , draft prospects , free agency ideas , etc .                  |
| **`pcc_eng_14_094.0309_x1504122_6:14-15-16`** | I read the initial results of the test with Speakerpower 's owner were n't__``terribly exciting``__.                                                                                |
| **`pcc_eng_25_099.7887_x1598711_12:17-18`**   | And , late in the week another long-sought demolition wrapped up , as seen in this__``terribly exciting``__before- and - after :                                                    |
| **`pcc_eng_08_029.3541_x0459000_006:09-10`**  | It can mean all sorts of different and__``terribly exciting``__things .                                                                                                             |


> saved as:  
> `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_exciting_ex.md`


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/`...
* Renaming existing version of `terribly_surprising_80ex~80.csv`
* Renaming existing version of `terribly_wrong_80ex~80.csv`
* Renaming existing version of `terribly_surprised_80ex~80.csv`
* Renaming existing version of `terribly_exciting_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_surprising_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_wrong_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_original_80ex~58.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_surprised_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_uncommon_80ex~21.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_impressed_80ex~76.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_fond_80ex~48.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_exciting_80ex~80.csv`

