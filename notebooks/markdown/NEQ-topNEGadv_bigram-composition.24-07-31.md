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
> `/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-07-30.csv`



```python
NEG_HITS_PATH = HIT_TABLES_DIR /'RBdirect'/'ALL-RBdirect_final.parq'
POS_HITS_PATH = HIT_TABLES_DIR /'not-RBdirect'/f'{TAG}_not-RBdirect_final.parq'
```


```python
adv_list = adv_am.index.to_list()
print_iter(adv_list, header=f'## Top {K} Most Negative Adverbs',bullet = '1.')
```


## Top 8 Most Negative Adverbs
1. necessarily
1. that
1. exactly
1. any
1. remotely
1. ever
1. yet
1. immediately
1. particularly
1. terribly
1. inherently


## Load AM table for `adv~adj` comparison (bigram composition)


```python
blind_am_iter = AM_DF_DIR.joinpath('adv_adj').rglob(f'AdvAdj_{TAG}*min{BIGRAM_F_FLOOR}x_extra.parq')
blam_dict = {blamp.parent.parent.name.strip('ANY'): blamp for blamp in blind_am_iter}
print(pd.Series(blam_dict)
       .to_frame('path to "context-blind" AM scores')
       .to_markdown(tablefmt='rounded_grid', maxcolwidths=[None, 72]))

```

    ╭────────┬──────────────────────────────────────────────────────────────────────────╮
    │        │ path to "context-blind" AM scores                                        │
    ├────────┼──────────────────────────────────────────────────────────────────────────┤
    │ mirror │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYmirror/extra/ │
    │        │ AdvAdj_NEQ_any-mirror_final-freq_min50x_extra.parq                       │
    ├────────┼──────────────────────────────────────────────────────────────────────────┤
    │ direct │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYdirect/extra/ │
    │        │ AdvAdj_NEQ_any-direct_final-freq_min50x_extra.parq                       │
    ╰────────┴──────────────────────────────────────────────────────────────────────────╯



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
    for peek_metric in blind_priority_cols:
        nb_show_table(peek_am(peek_metric, peek_df), n_dec=2)
    blamin.index = f'[_{blam_kind}_] ' + blamin.index
    blam_dfs[blam_kind] = blamin
```


### Loading `mirror` AM scores

 Path: `assoc_df/adv_adj/ANYmirror/extra/AdvAdj_NEQ_any-mirror_final-freq_min50x_extra.parq`


_Bigrams with the highest `LRC` value for each adverb_


|                             |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:----------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **any~closer**              |    6.05 |   477.62 |           0.22 |            0.14 | any          |    61 |  1,095 |    278 |
| **immediately~available**   |    5.44 | 1,232.57 |           0.32 |            0.19 | immediately  |   184 |    564 |  3,079 |
| **inherently~wrong**        |    5.09 | 9,012.22 |           0.46 |            0.32 | inherently   | 1,571 |  3,342 |  8,506 |
| **ever~perfect**            |    3.91 |   867.68 |           0.15 |            0.10 | ever         |   206 |  4,786 |  1,303 |
| **that~great**              |    3.89 | 1,216.00 |           0.13 |            0.10 | that         |   298 |  4,559 |  2,123 |
| **particularly~noteworthy** |    3.89 |   389.48 |           0.33 |            0.17 | particularly |    87 | 10,029 |    251 |
| **exactly~right**           |    3.84 |   379.55 |           0.09 |            0.06 | exactly      |    80 |    869 |  2,038 |
| **necessarily~wrong**       |    3.38 |   802.78 |           0.20 |            0.11 | necessarily  |   214 |    992 |  8,506 |
| **remotely~close**          |    3.34 |   805.38 |           0.11 |            0.08 | remotely     |   226 |  1,953 |  4,831 |
| **terribly~wrong**          |    3.31 | 1,369.70 |           0.17 |            0.11 | terribly     |   401 |  2,204 |  8,506 |


_Bigrams with the highest `G2` value for each adverb_


|                           |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:--------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **inherently~wrong**      |    5.09 | 9,012.22 |           0.46 |            0.32 | inherently   | 1,571 |  3,342 |  8,506 |
| **any~better**            |    5.50 | 2,543.31 |           0.35 |            0.23 | any          |   390 |  1,095 |  3,831 |
| **terribly~wrong**        |    3.31 | 1,369.70 |           0.17 |            0.11 | terribly     |   401 |  2,204 |  8,506 |
| **that~simple**           |    2.77 | 1,259.25 |           0.09 |            0.08 | that         |   483 |  4,559 |  7,465 |
| **immediately~available** |    5.44 | 1,232.57 |           0.32 |            0.19 | immediately  |   184 |    564 |  3,079 |
| **ever~perfect**          |    3.91 |   867.68 |           0.15 |            0.10 | ever         |   206 |  4,786 |  1,303 |
| **remotely~close**        |    3.34 |   805.38 |           0.11 |            0.08 | remotely     |   226 |  1,953 |  4,831 |
| **necessarily~wrong**     |    3.38 |   802.78 |           0.20 |            0.11 | necessarily  |   214 |    992 |  8,506 |
| **particularly~new**      |    2.17 |   753.63 |           0.08 |            0.06 | particularly |   405 | 10,029 |  4,300 |
| **exactly~sure**          |    3.43 |   580.91 |           0.16 |            0.09 | exactly      |   148 |    869 |  5,978 |


_Bigrams with the highest `deltaP_max` value for each adverb_


|                             |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:----------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **inherently~wrong**        |    5.09 | 9,012.22 |           0.46 |            0.32 | inherently   | 1,571 |  3,342 |  8,506 |
| **any~better**              |    5.50 | 2,543.31 |           0.35 |            0.23 | any          |   390 |  1,095 |  3,831 |
| **particularly~noteworthy** |    3.89 |   389.48 |           0.33 |            0.17 | particularly |    87 | 10,029 |    251 |
| **immediately~available**   |    5.44 | 1,232.57 |           0.32 |            0.19 | immediately  |   184 |    564 |  3,079 |
| **necessarily~wrong**       |    3.38 |   802.78 |           0.20 |            0.11 | necessarily  |   214 |    992 |  8,506 |
| **terribly~wrong**          |    3.31 | 1,369.70 |           0.17 |            0.11 | terribly     |   401 |  2,204 |  8,506 |
| **exactly~sure**            |    3.43 |   580.91 |           0.16 |            0.09 | exactly      |   148 |    869 |  5,978 |
| **ever~perfect**            |    3.91 |   867.68 |           0.15 |            0.10 | ever         |   206 |  4,786 |  1,303 |
| **that~great**              |    3.89 | 1,216.00 |           0.13 |            0.10 | that         |   298 |  4,559 |  2,123 |
| **remotely~close**          |    3.34 |   805.38 |           0.11 |            0.08 | remotely     |   226 |  1,953 |  4,831 |


_Bigrams with the highest `deltaP_mean` value for each adverb_


|                             |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |   `f` |   `f1` |   `f2` |
|:----------------------------|--------:|---------:|---------------:|----------------:|:-------------|------:|-------:|-------:|
| **inherently~wrong**        |    5.09 | 9,012.22 |           0.46 |            0.32 | inherently   | 1,571 |  3,342 |  8,506 |
| **any~better**              |    5.50 | 2,543.31 |           0.35 |            0.23 | any          |   390 |  1,095 |  3,831 |
| **immediately~available**   |    5.44 | 1,232.57 |           0.32 |            0.19 | immediately  |   184 |    564 |  3,079 |
| **particularly~noteworthy** |    3.89 |   389.48 |           0.33 |            0.17 | particularly |    87 | 10,029 |    251 |
| **necessarily~wrong**       |    3.38 |   802.78 |           0.20 |            0.11 | necessarily  |   214 |    992 |  8,506 |
| **terribly~wrong**          |    3.31 | 1,369.70 |           0.17 |            0.11 | terribly     |   401 |  2,204 |  8,506 |
| **that~great**              |    3.89 | 1,216.00 |           0.13 |            0.10 | that         |   298 |  4,559 |  2,123 |
| **ever~perfect**            |    3.91 |   867.68 |           0.15 |            0.10 | ever         |   206 |  4,786 |  1,303 |
| **exactly~sure**            |    3.43 |   580.91 |           0.16 |            0.09 | exactly      |   148 |    869 |  5,978 |
| **remotely~close**          |    3.34 |   805.38 |           0.11 |            0.08 | remotely     |   226 |  1,953 |  4,831 |


### Loading `direct` AM scores

 Path: `assoc_df/adv_adj/ANYdirect/extra/AdvAdj_NEQ_any-direct_final-freq_min50x_extra.parq`


_Bigrams with the highest `LRC` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |   `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|-------:|
| **any~happier**             |    7.76 |   7,282.99 |           0.41 |            0.23 | any          |    834 |  16,238 |  2,004 |
| **necessarily~indicative**  |    7.46 |  10,827.28 |           0.59 |            0.31 | necessarily  |  1,389 |  42,886 |  2,313 |
| **yet~final**               |    6.58 |   4,443.69 |           0.52 |            0.27 | yet          |    640 |  53,881 |  1,213 |
| **inherently~evil**         |    6.26 |   2,829.19 |           0.12 |            0.08 | inherently   |    392 |   8,614 |  3,171 |
| **immediately~clear**       |    5.41 | 141,124.53 |           0.41 |            0.35 | immediately  | 24,488 |  58,040 | 84,227 |
| **ever~closer**             |    5.08 |   1,611.94 |           0.07 |            0.05 | ever         |    281 |  10,870 |  3,686 |
| **remotely~comparable**     |    5.05 |     759.06 |           0.05 |            0.04 | remotely     |    125 |   6,161 |  2,401 |
| **exactly~alike**           |    4.67 |   1,293.40 |           0.20 |            0.10 | exactly      |    254 |  44,503 |  1,205 |
| **particularly~noteworthy** |    4.25 |   1,483.20 |           0.23 |            0.12 | particularly |    338 |  76,162 |  1,374 |
| **terribly~surprising**     |    3.82 |   3,589.19 |           0.05 |            0.05 | terribly     |    949 |  19,802 | 18,776 |
| **that~great**              |    3.50 |  32,588.43 |           0.22 |            0.14 | that         | 11,065 | 166,676 | 45,359 |


_Bigrams with the highest `G2` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |    `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|--------:|
| **immediately~clear**       |    5.41 | 141,124.53 |           0.41 |            0.35 | immediately  | 24,488 |  58,040 |  84,227 |
| **yet~ready**               |    5.21 |  39,487.38 |           0.25 |            0.19 | yet          |  7,505 |  53,881 |  29,583 |
| **that~great**              |    3.50 |  32,588.43 |           0.22 |            0.14 | that         | 11,065 | 166,676 |  45,359 |
| **any~better**              |    5.30 |  28,923.07 |           0.30 |            0.20 | any          |  5,004 |  16,238 |  50,827 |
| **exactly~sure**            |    3.23 |  25,681.61 |           0.18 |            0.12 | exactly      |  8,810 |  44,503 | 134,139 |
| **necessarily~true**        |    3.77 |  11,473.44 |           0.09 |            0.08 | necessarily  |  3,245 |  42,886 |  34,967 |
| **inherently~wrong**        |    5.77 |  10,797.34 |           0.19 |            0.13 | inherently   |  1,678 |   8,614 |  21,332 |
| **particularly~interested** |    2.70 |   6,106.11 |           0.07 |            0.05 | particularly |  2,783 |  76,162 |  34,543 |
| **terribly~surprising**     |    3.82 |   3,589.19 |           0.05 |            0.05 | terribly     |    949 |  19,802 |  18,776 |
| **remotely~close**          |    3.75 |   2,801.94 |           0.11 |            0.06 | remotely     |    733 |   6,161 |  46,485 |
| **ever~closer**             |    5.08 |   1,611.94 |           0.07 |            0.05 | ever         |    281 |  10,870 |   3,686 |


_Bigrams with the highest `deltaP_max` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |   `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|-------:|
| **necessarily~indicative**  |    7.46 |  10,827.28 |           0.59 |            0.31 | necessarily  |  1,389 |  42,886 |  2,313 |
| **yet~final**               |    6.58 |   4,443.69 |           0.52 |            0.27 | yet          |    640 |  53,881 |  1,213 |
| **any~happier**             |    7.76 |   7,282.99 |           0.41 |            0.23 | any          |    834 |  16,238 |  2,004 |
| **immediately~clear**       |    5.41 | 141,124.53 |           0.41 |            0.35 | immediately  | 24,488 |  58,040 | 84,227 |
| **particularly~noteworthy** |    4.25 |   1,483.20 |           0.23 |            0.12 | particularly |    338 |  76,162 |  1,374 |
| **that~uncommon**           |    3.33 |   2,384.09 |           0.23 |            0.12 | that         |    802 | 166,676 |  3,165 |
| **exactly~stellar**         |    4.57 |     873.03 |           0.21 |            0.11 | exactly      |    170 |  44,503 |    790 |
| **inherently~wrong**        |    5.77 |  10,797.34 |           0.19 |            0.13 | inherently   |  1,678 |   8,614 | 21,332 |
| **remotely~close**          |    3.75 |   2,801.94 |           0.11 |            0.06 | remotely     |    733 |   6,161 | 46,485 |
| **ever~closer**             |    5.08 |   1,611.94 |           0.07 |            0.05 | ever         |    281 |  10,870 |  3,686 |
| **terribly~surprising**     |    3.82 |   3,589.19 |           0.05 |            0.05 | terribly     |    949 |  19,802 | 18,776 |


_Bigrams with the highest `deltaP_mean` value for each adverb_


|                             |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` | `l1`         |    `f` |    `f1` |    `f2` |
|:----------------------------|--------:|-----------:|---------------:|----------------:|:-------------|-------:|--------:|--------:|
| **immediately~clear**       |    5.41 | 141,124.53 |           0.41 |            0.35 | immediately  | 24,488 |  58,040 |  84,227 |
| **necessarily~indicative**  |    7.46 |  10,827.28 |           0.59 |            0.31 | necessarily  |  1,389 |  42,886 |   2,313 |
| **yet~final**               |    6.58 |   4,443.69 |           0.52 |            0.27 | yet          |    640 |  53,881 |   1,213 |
| **any~happier**             |    7.76 |   7,282.99 |           0.41 |            0.23 | any          |    834 |  16,238 |   2,004 |
| **that~great**              |    3.50 |  32,588.43 |           0.22 |            0.14 | that         | 11,065 | 166,676 |  45,359 |
| **inherently~wrong**        |    5.77 |  10,797.34 |           0.19 |            0.13 | inherently   |  1,678 |   8,614 |  21,332 |
| **particularly~noteworthy** |    4.25 |   1,483.20 |           0.23 |            0.12 | particularly |    338 |  76,162 |   1,374 |
| **exactly~sure**            |    3.23 |  25,681.61 |           0.18 |            0.12 | exactly      |  8,810 |  44,503 | 134,139 |
| **remotely~close**          |    3.75 |   2,801.94 |           0.11 |            0.06 | remotely     |    733 |   6,161 |  46,485 |
| **ever~closer**             |    5.08 |   1,611.94 |           0.07 |            0.05 | ever         |    281 |  10,870 |   3,686 |
| **terribly~surprising**     |    3.82 |   3,589.19 |           0.05 |            0.05 | terribly     |    949 |  19,802 |  18,776 |




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


|                                       |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`        | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:--------------------------------------|------:|--------:|--------:|-------:|----------:|:------------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] any~happier**            |   834 |    0.41 |    7.76 |   0.42 |  7,282.99 | any         | happier    | 16,238 |  2,004 | 6,347,362 |      5.13 |      828.87 |        0.99 |            2.47 | 28.70 |   2.21 |    0.05 |   0.05 |           0.41 |            0.23 | direct      |
| **[_direct_] necessarily~indicative** | 1,389 |    0.59 |    7.46 |   0.60 | 10,827.28 | necessarily | indicative | 42,886 |  2,313 | 6,347,362 |     15.63 |    1,373.37 |        0.99 |            2.36 | 36.85 |   1.95 |    0.03 |   0.03 |           0.59 |            0.31 | direct      |
| **[_direct_] any~clearer**            |   371 |    0.38 |    7.39 |   0.38 |  3,147.58 | any         | clearer    | 16,238 |    972 | 6,347,362 |      2.49 |      368.51 |        0.99 |            2.39 | 19.13 |   2.17 |    0.02 |   0.02 |           0.38 |            0.20 | direct      |
| **[_direct_] yet~final**              |   640 |    0.52 |    6.58 |   0.53 |  4,443.69 | yet         | final      | 53,881 |  1,213 | 6,347,362 |     10.30 |      629.70 |        0.98 |            2.12 | 24.89 |   1.79 |    0.01 |   0.01 |           0.52 |            0.27 | direct      |
| **[_direct_] inherently~evil**        |   392 |    0.12 |    6.26 |   0.12 |  2,829.19 | inherently  | evil       |  8,614 |  3,171 | 6,347,362 |      4.30 |      387.70 |        0.99 |            2.04 | 19.58 |   1.96 |    0.05 |   0.05 |           0.12 |            0.08 | direct      |
| **[_mirror_] any~closer**             |    61 |    0.22 |    6.05 |   0.22 |    477.62 | any         | closer     |  1,095 |    278 |   583,470 |      0.52 |       60.48 |        0.99 |            2.20 |  7.74 |   2.07 |    0.06 |   0.06 |           0.22 |            0.14 | mirror      |
| **[_direct_] any~closer**             |   611 |    0.16 |    5.92 |   0.17 |  4,021.04 | any         | closer     | 16,238 |  3,686 | 6,347,362 |      9.43 |      601.57 |        0.98 |            1.91 | 24.34 |   1.81 |    0.04 |   0.04 |           0.16 |            0.10 | direct      |
| **[_direct_] any~worse**              | 1,762 |    0.14 |    5.85 |   0.15 | 11,229.25 | any         | worse      | 16,238 | 12,116 | 6,347,362 |     31.00 |    1,731.00 |        0.98 |            1.87 | 41.24 |   1.75 |    0.11 |   0.11 |           0.14 |            0.13 | direct      |
| **[_direct_] inherently~wrong**       | 1,678 |    0.08 |    5.77 |   0.08 | 10,797.34 | inherently  | wrong      |  8,614 | 21,332 | 6,347,362 |     28.95 |    1,649.05 |        0.98 |            1.89 | 40.26 |   1.76 |    0.19 |   0.19 |           0.19 |            0.13 | direct      |
| **[_direct_] yet~official**           |   352 |    0.37 |    5.63 |   0.38 |  2,141.31 | yet         | official   | 53,881 |    924 | 6,347,362 |      7.84 |      344.16 |        0.98 |            1.86 | 18.34 |   1.65 |    0.01 |   0.01 |           0.37 |            0.19 | direct      |
| **[_direct_] any~simpler**            |   229 |    0.16 |    5.61 |   0.16 |  1,479.26 | any         | simpler    | 16,238 |  1,446 | 6,347,362 |      3.70 |      225.30 |        0.98 |            1.87 | 14.89 |   1.79 |    0.01 |   0.01 |           0.16 |            0.08 | direct      |
| **[_direct_] any~easier**             | 1,625 |    0.12 |    5.61 |   0.13 |  9,854.27 | any         | easier     | 16,238 | 12,877 | 6,347,362 |     32.94 |    1,592.06 |        0.98 |            1.80 | 39.49 |   1.69 |    0.10 |   0.10 |           0.12 |            0.11 | direct      |
| **[_mirror_] any~better**             |   390 |    0.10 |    5.50 |   0.10 |  2,543.31 | any         | better     |  1,095 |  3,831 |   583,470 |      7.19 |      382.81 |        0.98 |            1.97 | 19.38 |   1.73 |    0.35 |   0.36 |           0.35 |            0.23 | mirror      |
| **[_direct_] any~younger**            |   255 |    0.14 |    5.47 |   0.14 |  1,591.82 | any         | younger    | 16,238 |  1,784 | 6,347,362 |      4.56 |      250.44 |        0.98 |            1.82 | 15.68 |   1.75 |    0.02 |   0.02 |           0.14 |            0.08 | direct      |
| **[_mirror_] immediately~available**  |   184 |    0.06 |    5.44 |   0.06 |  1,232.57 | immediately | available  |    564 |  3,079 |   583,470 |      2.98 |      181.02 |        0.98 |            1.99 | 13.35 |   1.79 |    0.32 |   0.33 |           0.32 |            0.19 | mirror      |




```python
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

|                                       |   `LRC` |   `G2` |   `deltaP_max` |   `deltaP_mean` |
|:--------------------------------------|--------:|-------:|---------------:|----------------:|
| **[_mirror_] any~easier**             |    4.67 | 377.02 |           0.09 |            0.07 |
| **[_mirror_] terribly~surprising**    |    2.87 | 236.04 |           0.05 |            0.04 |
| **[_mirror_] necessarily~bad**        |    1.43 |  99.94 |           0.04 |            0.03 |
| **[_mirror_] ever~free**              |    1.37 | 116.66 |           0.03 |            0.02 |
| **[_mirror_] particularly~difficult** |    0.00 |  24.72 |           0.01 |            0.01 |





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
| **[_direct_] necessarily~indicative**     |    7.46 | 10,827.28 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,313 |        0.99 |
| **[_direct_] necessarily~cause**          |    5.07 |    341.90 |           0.38 |            0.19 |    0.38 |    0.00 |    52 |     134 |        0.98 |
| **[_direct_] necessarily~representative** |    4.71 |  2,416.54 |           0.18 |            0.10 |    0.18 |    0.01 |   488 |   2,560 |        0.96 |
| **[_direct_] necessarily~important**      |   -1.70 |   -868.50 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   203 | 139,114 |       -3.63 |
| **[_direct_] necessarily~sure**           |   -1.71 |   -842.41 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,139 |       -3.67 |
| **[_direct_] necessarily~different**      |   -2.01 |   -638.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,643 |       -5.99 |

#### 1.2. _necessarily_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                       |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:--------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] necessarily~true**       |    3.77 | 11,473.44 |           0.09 |            0.08 |    0.09 |    0.07 | 3,245 |  34,967 |        0.93 |
| **[_direct_] necessarily~indicative** |    7.46 | 10,827.28 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,313 |        0.99 |
| **[_direct_] necessarily~better**     |    2.32 |  3,461.95 |           0.04 |            0.03 |    0.03 |    0.04 | 1,891 |  50,827 |        0.82 |
| **[_direct_] necessarily~different**  |   -2.01 |   -638.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,643 |       -5.99 |
| **[_direct_] necessarily~sure**       |   -1.71 |   -842.41 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,139 |       -3.67 |
| **[_direct_] necessarily~important**  |   -1.70 |   -868.50 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   203 | 139,114 |       -3.63 |

#### 1.3. _necessarily_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                         |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:----------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] necessarily~indicative**   |    7.46 | 10,827.28 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,313 |        0.99 |
| **[_direct_] necessarily~cause**        |    5.07 |    341.90 |           0.38 |            0.19 |    0.38 |    0.00 |    52 |     134 |        0.98 |
| **[_direct_] necessarily~incompatible** |    4.25 |    506.31 |           0.19 |            0.10 |    0.19 |    0.00 |   101 |     513 |        0.97 |
| **[_direct_] necessarily~important**    |   -1.70 |   -868.50 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   203 | 139,114 |       -3.63 |
| **[_direct_] necessarily~sure**         |   -1.71 |   -842.41 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,139 |       -3.67 |
| **[_direct_] necessarily~different**    |   -2.01 |   -638.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,643 |       -5.99 |

#### 1.4. _necessarily_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] necessarily~wrong**     |    3.38 |    802.78 |           0.20 |            0.11 |    0.02 |    0.20 |   214 |   8,506 |        0.93 |
| **[_direct_] necessarily~true**      |    3.77 | 11,473.44 |           0.09 |            0.08 |    0.09 |    0.07 | 3,245 |  34,967 |        0.93 |
| **[_mirror_] necessarily~true**      |    2.46 |    180.47 |           0.05 |            0.04 |    0.02 |    0.05 |    57 |   2,850 |        0.91 |
| **[_direct_] necessarily~different** |   -2.01 |   -638.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,643 |       -5.99 |
| **[_direct_] necessarily~important** |   -1.70 |   -868.50 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   203 | 139,114 |       -3.63 |
| **[_direct_] necessarily~sure**      |   -1.71 |   -842.41 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   194 | 134,139 |       -3.67 |


---

### 2. Sampling _that_ context-blind bigram AMs

#### 2.1. _that_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_mirror_] that~great**    |    3.89 |  1,216.00 |           0.13 |            0.10 |    0.13 |    0.06 |    298 |   2,123 |        0.94 |
| **[_direct_] that~great**    |    3.50 | 32,588.43 |           0.22 |            0.14 |    0.22 |    0.06 | 11,065 |  45,359 |        0.89 |
| **[_direct_] that~uncommon** |    3.33 |  2,384.09 |           0.23 |            0.12 |    0.23 |    0.00 |    802 |   3,165 |        0.90 |
| **[_direct_] that~better**   |   -2.72 | -1,823.15 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    134 |  50,827 |       -8.96 |
| **[_direct_] that~likely**   |   -2.90 | -1,876.49 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    111 |  49,647 |      -10.74 |
| **[_direct_] that~sure**     |   -3.16 | -5,105.66 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    301 | 134,139 |      -10.70 |

#### 2.2. _that_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:--------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] that~great** |    3.50 | 32,588.43 |           0.22 |            0.14 |    0.22 |    0.06 | 11,065 |  45,359 |        0.89 |
| **[_direct_] that~bad**   |    2.52 | 31,301.65 |           0.12 |            0.10 |    0.12 |    0.08 | 16,635 | 119,509 |        0.81 |
| **[_direct_] that~hard**  |    3.31 | 27,269.05 |           0.20 |            0.13 |    0.20 |    0.05 |  9,963 |  45,061 |        0.88 |
| **[_direct_] that~clear** |   -1.78 | -1,915.57 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    525 |  84,227 |       -3.21 |
| **[_direct_] that~many**  |   -2.47 | -3,082.65 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    361 |  97,883 |       -6.12 |
| **[_direct_] that~sure**  |   -3.16 | -5,105.66 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    301 | 134,139 |      -10.70 |

#### 2.3. _that_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] that~uncommon** |    3.33 |  2,384.09 |           0.23 |            0.12 |    0.23 |    0.00 |    802 |   3,165 |        0.90 |
| **[_direct_] that~great**    |    3.50 | 32,588.43 |           0.22 |            0.14 |    0.22 |    0.06 | 11,065 |  45,359 |        0.89 |
| **[_direct_] that~hard**     |    3.31 | 27,269.05 |           0.20 |            0.13 |    0.20 |    0.05 |  9,963 |  45,061 |        0.88 |
| **[_direct_] that~better**   |   -2.72 | -1,823.15 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    134 |  50,827 |       -8.96 |
| **[_direct_] that~likely**   |   -2.90 | -1,876.49 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    111 |  49,647 |      -10.74 |
| **[_direct_] that~sure**     |   -3.16 | -5,105.66 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    301 | 134,139 |      -10.70 |

#### 2.4. _that_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_mirror_] that~simple** |    2.77 |  1,259.25 |           0.09 |            0.08 |    0.06 |    0.09 |    483 |   7,465 |        0.88 |
| **[_mirror_] that~easy**   |    2.65 |  1,146.45 |           0.09 |            0.07 |    0.05 |    0.09 |    465 |   7,749 |        0.87 |
| **[_direct_] that~bad**    |    2.52 | 31,301.65 |           0.12 |            0.10 |    0.12 |    0.08 | 16,635 | 119,509 |        0.81 |
| **[_direct_] that~better** |   -2.72 | -1,823.15 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    134 |  50,827 |       -8.96 |
| **[_direct_] that~likely** |   -2.90 | -1,876.49 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |    111 |  49,647 |      -10.74 |
| **[_direct_] that~sure**   |   -3.16 | -5,105.66 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |    301 | 134,139 |      -10.70 |


---

### 3. Sampling _exactly_ context-blind bigram AMs

#### 3.1. _exactly_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] exactly~alike**   |    4.67 |  1,293.40 |           0.20 |            0.10 |    0.20 |    0.01 |   254 |   1,205 |        0.97 |
| **[_direct_] exactly~stellar** |    4.57 |    873.03 |           0.21 |            0.11 |    0.21 |    0.00 |   170 |     790 |        0.97 |
| **[_direct_] exactly~ideal**   |    3.93 |  1,678.75 |           0.12 |            0.06 |    0.12 |    0.01 |   418 |   3,316 |        0.94 |
| **[_direct_] exactly~simple**  |   -1.49 |   -322.89 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  46,867 |       -4.13 |
| **[_direct_] exactly~good**    |   -1.98 | -1,449.44 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   263 | 201,244 |       -4.36 |
| **[_direct_] exactly~bad**     |   -2.11 |   -966.10 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   125 | 119,509 |       -5.70 |

#### 3.2. _exactly_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] exactly~sure**   |    3.23 | 25,681.61 |           0.18 |            0.12 |    0.06 |    0.18 | 8,810 | 134,139 |        0.89 |
| **[_direct_] exactly~new**    |    3.05 |  3,718.41 |           0.06 |            0.04 |    0.06 |    0.03 | 1,372 |  21,538 |        0.89 |
| **[_direct_] exactly~true**   |    2.41 |  2,849.90 |           0.03 |            0.03 |    0.03 |    0.03 | 1,458 |  34,967 |        0.83 |
| **[_direct_] exactly~simple** |   -1.49 |   -322.89 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  46,867 |       -4.13 |
| **[_direct_] exactly~bad**    |   -2.11 |   -966.10 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   125 | 119,509 |       -5.70 |
| **[_direct_] exactly~good**   |   -1.98 | -1,449.44 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   263 | 201,244 |       -4.36 |

#### 3.3. _exactly_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] exactly~stellar** |    4.57 |    873.03 |           0.21 |            0.11 |    0.21 |    0.00 |   170 |     790 |        0.97 |
| **[_direct_] exactly~alike**   |    4.67 |  1,293.40 |           0.20 |            0.10 |    0.20 |    0.01 |   254 |   1,205 |        0.97 |
| **[_direct_] exactly~ideal**   |    3.93 |  1,678.75 |           0.12 |            0.06 |    0.12 |    0.01 |   418 |   3,316 |        0.94 |
| **[_direct_] exactly~simple**  |   -1.49 |   -322.89 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  46,867 |       -4.13 |
| **[_direct_] exactly~good**    |   -1.98 | -1,449.44 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   263 | 201,244 |       -4.36 |
| **[_direct_] exactly~bad**     |   -2.11 |   -966.10 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   125 | 119,509 |       -5.70 |

#### 3.4. _exactly_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] exactly~sure**   |    3.23 | 25,681.61 |           0.18 |            0.12 |    0.06 |    0.18 | 8,810 | 134,139 |        0.89 |
| **[_mirror_] exactly~sure**   |    3.43 |    580.91 |           0.16 |            0.09 |    0.02 |    0.16 |   148 |   5,978 |        0.94 |
| **[_mirror_] exactly~right**  |    3.84 |    379.55 |           0.09 |            0.06 |    0.04 |    0.09 |    80 |   2,038 |        0.96 |
| **[_direct_] exactly~simple** |   -1.49 |   -322.89 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    64 |  46,867 |       -4.13 |
| **[_direct_] exactly~bad**    |   -2.11 |   -966.10 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   125 | 119,509 |       -5.70 |
| **[_direct_] exactly~good**   |   -1.98 | -1,449.44 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   263 | 201,244 |       -4.36 |


---

### 4. Sampling _any_ context-blind bigram AMs

#### 4.1. _any_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                            |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] any~happier** |    7.76 | 7,282.99 |           0.41 |            0.23 |    0.41 |    0.05 |   834 |   2,004 |        0.99 |
| **[_direct_] any~clearer** |    7.39 | 3,147.58 |           0.38 |            0.20 |    0.38 |    0.02 |   371 |     972 |        0.99 |
| **[_mirror_] any~closer**  |    6.05 |   477.62 |           0.22 |            0.14 |    0.22 |    0.06 |    61 |     278 |        0.99 |
| **[_direct_] any~larger**  |    1.43 |   151.17 |           0.01 |            0.01 |    0.01 |    0.00 |    94 |   7,453 |        0.80 |
| **[_direct_] any~lower**   |    1.20 |   116.95 |           0.01 |            0.01 |    0.01 |    0.00 |    81 |   7,121 |        0.78 |
| **[_direct_] any~good**    |   -1.17 |  -363.78 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   152 | 201,244 |       -2.39 |

#### 4.2. _any_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] any~better**  |    5.30 | 28,923.07 |           0.30 |            0.20 |    0.10 |    0.30 | 5,004 |  50,827 |        0.97 |
| **[_direct_] any~worse**   |    5.85 | 11,229.25 |           0.14 |            0.13 |    0.14 |    0.11 | 1,762 |  12,116 |        0.98 |
| **[_direct_] any~easier**  |    5.61 |  9,854.27 |           0.12 |            0.11 |    0.12 |    0.10 | 1,625 |  12,877 |        0.98 |
| **[_direct_] any~smaller** |    1.47 |    126.87 |           0.01 |            0.01 |    0.01 |    0.00 |    69 |   4,749 |        0.82 |
| **[_direct_] any~lower**   |    1.20 |    116.95 |           0.01 |            0.01 |    0.01 |    0.00 |    81 |   7,121 |        0.78 |
| **[_direct_] any~good**    |   -1.17 |   -363.78 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   152 | 201,244 |       -2.39 |

#### 4.3. _any_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:---------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] any~happier** |    7.76 | 7,282.99 |           0.41 |            0.23 |    0.41 |    0.05 |   834 |   2,004 |        0.99 |
| **[_direct_] any~clearer** |    7.39 | 3,147.58 |           0.38 |            0.20 |    0.38 |    0.02 |   371 |     972 |        0.99 |
| **[_mirror_] any~closer**  |    6.05 |   477.62 |           0.22 |            0.14 |    0.22 |    0.06 |    61 |     278 |        0.99 |
| **[_direct_] any~larger**  |    1.43 |   151.17 |           0.01 |            0.01 |    0.01 |    0.00 |    94 |   7,453 |        0.80 |
| **[_direct_] any~lower**   |    1.20 |   116.95 |           0.01 |            0.01 |    0.01 |    0.00 |    81 |   7,121 |        0.78 |
| **[_direct_] any~good**    |   -1.17 |  -363.78 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   152 | 201,244 |       -2.39 |

#### 4.4. _any_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:--------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] any~better** |    5.50 |  2,543.31 |           0.35 |            0.23 |    0.10 |    0.35 |   390 |   3,831 |        0.98 |
| **[_direct_] any~better** |    5.30 | 28,923.07 |           0.30 |            0.20 |    0.10 |    0.30 | 5,004 |  50,827 |        0.97 |
| **[_direct_] any~worse**  |    5.85 | 11,229.25 |           0.14 |            0.13 |    0.14 |    0.11 | 1,762 |  12,116 |        0.98 |
| **[_direct_] any~larger** |    1.43 |    151.17 |           0.01 |            0.01 |    0.01 |    0.00 |    94 |   7,453 |        0.80 |
| **[_direct_] any~lower**  |    1.20 |    116.95 |           0.01 |            0.01 |    0.01 |    0.00 |    81 |   7,121 |        0.78 |
| **[_direct_] any~good**   |   -1.17 |   -363.78 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   152 | 201,244 |       -2.39 |


---

### 5. Sampling _remotely_ context-blind bigram AMs

#### 5.1. _remotely_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~comparable** |    5.05 |   759.06 |           0.05 |            0.04 |    0.05 |    0.02 |   125 |   2,401 |        0.98 |
| **[_direct_] remotely~close**      |    3.75 | 2,801.94 |           0.11 |            0.06 |    0.01 |    0.11 |   733 |  46,485 |        0.94 |
| **[_direct_] remotely~similar**    |    3.35 |   620.70 |           0.03 |            0.02 |    0.01 |    0.03 |   169 |  11,088 |        0.94 |
| **[_direct_] remotely~accurate**   |    0.29 |    42.81 |           0.01 |            0.00 |    0.00 |    0.01 |    54 |  19,648 |        0.65 |
| **[_direct_] remotely~ready**      |    0.00 |    23.15 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,583 |        0.50 |
| **[_direct_] remotely~good**       |   -0.92 |  -149.87 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    53 | 201,244 |       -2.69 |

#### 5.2. _remotely_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~close**      |    3.75 | 2,801.94 |           0.11 |            0.06 |    0.01 |    0.11 |   733 |  46,485 |        0.94 |
| **[_direct_] remotely~interested** |    3.03 | 1,096.50 |           0.05 |            0.03 |    0.01 |    0.05 |   364 |  34,543 |        0.91 |
| **[_mirror_] remotely~close**      |    3.34 |   805.38 |           0.11 |            0.08 |    0.04 |    0.11 |   226 |   4,831 |        0.93 |
| **[_direct_] remotely~accurate**   |    0.29 |    42.81 |           0.01 |            0.00 |    0.00 |    0.01 |    54 |  19,648 |        0.65 |
| **[_direct_] remotely~ready**      |    0.00 |    23.15 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,583 |        0.50 |
| **[_direct_] remotely~good**       |   -0.92 |  -149.87 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    53 | 201,244 |       -2.69 |

#### 5.3. _remotely_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                    |   `LRC` |    `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|--------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~comparable** |    5.05 |  759.06 |           0.05 |            0.04 |    0.05 |    0.02 |   125 |   2,401 |        0.98 |
| **[_mirror_] remotely~similar**    |    3.07 |  296.76 |           0.05 |            0.04 |    0.05 |    0.04 |    81 |   1,586 |        0.93 |
| **[_mirror_] remotely~close**      |    3.34 |  805.38 |           0.11 |            0.08 |    0.04 |    0.11 |   226 |   4,831 |        0.93 |
| **[_direct_] remotely~accurate**   |    0.29 |   42.81 |           0.01 |            0.00 |    0.00 |    0.01 |    54 |  19,648 |        0.65 |
| **[_direct_] remotely~ready**      |    0.00 |   23.15 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,583 |        0.50 |
| **[_direct_] remotely~good**       |   -0.92 | -149.87 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    53 | 201,244 |       -2.69 |

#### 5.4. _remotely_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] remotely~close**      |    3.75 | 2,801.94 |           0.11 |            0.06 |    0.01 |    0.11 |   733 |  46,485 |        0.94 |
| **[_mirror_] remotely~close**      |    3.34 |   805.38 |           0.11 |            0.08 |    0.04 |    0.11 |   226 |   4,831 |        0.93 |
| **[_direct_] remotely~interested** |    3.03 | 1,096.50 |           0.05 |            0.03 |    0.01 |    0.05 |   364 |  34,543 |        0.91 |
| **[_direct_] remotely~accurate**   |    0.29 |    42.81 |           0.01 |            0.00 |    0.00 |    0.01 |    54 |  19,648 |        0.65 |
| **[_direct_] remotely~ready**      |    0.00 |    23.15 |           0.00 |            0.00 |    0.00 |    0.00 |    58 |  29,583 |        0.50 |
| **[_direct_] remotely~good**       |   -0.92 |  -149.87 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    53 | 201,244 |       -2.69 |


---

### 6. Sampling _ever_ context-blind bigram AMs

#### 6.1. _ever_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                               |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] ever~closer**    |    5.08 | 1,611.94 |           0.07 |            0.05 |    0.07 |    0.03 |   281 |   3,686 |        0.98 |
| **[_direct_] ever~mindful**   |    4.15 |   290.04 |           0.07 |            0.04 |    0.07 |    0.00 |    53 |     784 |        0.97 |
| **[_direct_] ever~present**   |    3.95 | 1,370.21 |           0.03 |            0.03 |    0.03 |    0.03 |   326 |   9,262 |        0.95 |
| **[_direct_] ever~better**    |    0.00 |   -14.65 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    54 |  50,827 |       -0.61 |
| **[_direct_] ever~available** |   -0.02 |   -31.50 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    81 |  82,956 |       -0.75 |
| **[_direct_] ever~sure**      |   -0.60 |  -112.74 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    90 | 134,139 |       -1.55 |

#### 6.2. _ever_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                               |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] ever~closer**    |    5.08 | 1,611.94 |           0.07 |            0.05 |    0.07 |    0.03 |   281 |   3,686 |        0.98 |
| **[_direct_] ever~present**   |    3.95 | 1,370.21 |           0.03 |            0.03 |    0.03 |    0.03 |   326 |   9,262 |        0.95 |
| **[_mirror_] ever~perfect**   |    3.91 |   867.68 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,303 |        0.95 |
| **[_direct_] ever~better**    |    0.00 |   -14.65 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    54 |  50,827 |       -0.61 |
| **[_direct_] ever~available** |   -0.02 |   -31.50 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    81 |  82,956 |       -0.75 |
| **[_direct_] ever~sure**      |   -0.60 |  -112.74 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    90 | 134,139 |       -1.55 |

#### 6.3. _ever_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |    `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|--------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] ever~perfect**   |    3.91 |  867.68 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,303 |        0.95 |
| **[_mirror_] ever~certain**   |    3.23 |  500.86 |           0.10 |            0.07 |    0.10 |    0.03 |   143 |   1,276 |        0.93 |
| **[_mirror_] ever~enough**    |    3.22 |  511.83 |           0.10 |            0.07 |    0.10 |    0.03 |   147 |   1,326 |        0.93 |
| **[_mirror_] ever~wrong**     |    0.00 |   13.36 |           0.01 |            0.01 |    0.00 |    0.01 |   102 |   8,506 |        0.32 |
| **[_direct_] ever~available** |   -0.02 |  -31.50 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    81 |  82,956 |       -0.75 |
| **[_direct_] ever~sure**      |   -0.60 | -112.74 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    90 | 134,139 |       -1.55 |

#### 6.4. _ever_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |    `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:------------------------------|--------:|--------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_mirror_] ever~easy**      |    2.18 |  719.76 |           0.06 |            0.05 |    0.04 |    0.06 |   369 |   7,749 |        0.83 |
| **[_mirror_] ever~perfect**   |    3.91 |  867.68 |           0.15 |            0.10 |    0.15 |    0.04 |   206 |   1,303 |        0.95 |
| **[_mirror_] ever~good**      |    1.01 |  232.23 |           0.04 |            0.03 |    0.01 |    0.04 |   300 |  13,423 |        0.63 |
| **[_direct_] ever~happy**     |    0.00 |   -1.68 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    69 |  46,884 |       -0.16 |
| **[_direct_] ever~available** |   -0.02 |  -31.50 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    81 |  82,956 |       -0.75 |
| **[_direct_] ever~sure**      |   -0.60 | -112.74 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    90 | 134,139 |       -1.55 |


---

### 7. Sampling _yet_ context-blind bigram AMs

#### 7.1. _yet_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                             |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] yet~final**    |    6.58 |  4,443.69 |           0.52 |            0.27 |    0.52 |    0.01 |   640 |   1,213 |        0.98 |
| **[_direct_] yet~official** |    5.63 |  2,141.31 |           0.37 |            0.19 |    0.37 |    0.01 |   352 |     924 |        0.98 |
| **[_direct_] yet~ready**    |    5.21 | 39,487.38 |           0.25 |            0.19 |    0.25 |    0.14 | 7,505 |  29,583 |        0.97 |
| **[_direct_] yet~big**      |   -1.61 |   -374.81 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    66 |  42,912 |       -4.52 |
| **[_direct_] yet~popular**  |   -1.81 |   -481.26 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    69 |  51,120 |       -5.29 |
| **[_direct_] yet~good**     |   -2.63 | -2,244.36 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   193 | 201,244 |       -7.85 |

#### 7.2. _yet_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] yet~ready**     |    5.21 | 39,487.38 |           0.25 |            0.19 |    0.25 |    0.14 |  7,505 |  29,583 |        0.97 |
| **[_direct_] yet~clear**     |    3.96 | 39,438.80 |           0.18 |            0.15 |    0.12 |    0.18 | 10,409 |  84,227 |        0.93 |
| **[_direct_] yet~available** |    3.43 | 23,183.87 |           0.13 |            0.10 |    0.08 |    0.13 |  7,461 |  82,956 |        0.91 |
| **[_direct_] yet~big**       |   -1.61 |   -374.81 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     66 |  42,912 |       -4.52 |
| **[_direct_] yet~popular**   |   -1.81 |   -481.26 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     69 |  51,120 |       -5.29 |
| **[_direct_] yet~good**      |   -2.63 | -2,244.36 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |    193 | 201,244 |       -7.85 |

#### 7.3. _yet_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                             |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] yet~final**    |    6.58 |  4,443.69 |           0.52 |            0.27 |    0.52 |    0.01 |   640 |   1,213 |        0.98 |
| **[_direct_] yet~official** |    5.63 |  2,141.31 |           0.37 |            0.19 |    0.37 |    0.01 |   352 |     924 |        0.98 |
| **[_direct_] yet~over**     |    4.65 |    845.32 |           0.26 |            0.13 |    0.26 |    0.00 |   162 |     613 |        0.97 |
| **[_direct_] yet~big**      |   -1.61 |   -374.81 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    66 |  42,912 |       -4.52 |
| **[_direct_] yet~popular**  |   -1.81 |   -481.26 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    69 |  51,120 |       -5.29 |
| **[_direct_] yet~good**     |   -2.63 | -2,244.36 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   193 | 201,244 |       -7.85 |

#### 7.4. _yet_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] yet~clear**     |    3.96 | 39,438.80 |           0.18 |            0.15 |    0.12 |    0.18 | 10,409 |  84,227 |        0.93 |
| **[_direct_] yet~ready**     |    5.21 | 39,487.38 |           0.25 |            0.19 |    0.25 |    0.14 |  7,505 |  29,583 |        0.97 |
| **[_direct_] yet~available** |    3.43 | 23,183.87 |           0.13 |            0.10 |    0.08 |    0.13 |  7,461 |  82,956 |        0.91 |
| **[_direct_] yet~big**       |   -1.61 |   -374.81 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     66 |  42,912 |       -4.52 |
| **[_direct_] yet~popular**   |   -1.81 |   -481.26 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |     69 |  51,120 |       -5.29 |
| **[_direct_] yet~good**      |   -2.63 | -2,244.36 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |    193 | 201,244 |       -7.85 |


---

### 8. Sampling _immediately_ context-blind bigram AMs

#### 8.1. _immediately_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_mirror_] immediately~available** |    5.44 |   1,232.57 |           0.32 |            0.19 |    0.06 |    0.32 |    184 |   3,079 |        0.98 |
| **[_direct_] immediately~clear**     |    5.41 | 141,124.53 |           0.41 |            0.35 |    0.29 |    0.41 | 24,488 |  84,227 |        0.97 |
| **[_direct_] immediately~available** |    5.18 | 116,575.85 |           0.36 |            0.31 |    0.25 |    0.36 | 21,477 |  82,956 |        0.96 |
| **[_direct_] immediately~concerned** |   -1.29 |    -232.17 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     53 |  27,374 |       -3.72 |
| **[_direct_] immediately~ready**     |   -1.33 |    -251.83 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     57 |  29,583 |       -3.75 |
| **[_direct_] immediately~sure**      |   -2.55 |  -1,603.95 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    138 | 134,139 |       -7.89 |

#### 8.2. _immediately_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~clear**     |    5.41 | 141,124.53 |           0.41 |            0.35 |    0.29 |    0.41 | 24,488 |  84,227 |        0.97 |
| **[_direct_] immediately~available** |    5.18 | 116,575.85 |           0.36 |            0.31 |    0.25 |    0.36 | 21,477 |  82,956 |        0.96 |
| **[_direct_] immediately~apparent**  |    4.73 |  10,042.87 |           0.21 |            0.12 |    0.21 |    0.04 |  2,143 |   9,798 |        0.96 |
| **[_direct_] immediately~concerned** |   -1.29 |    -232.17 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     53 |  27,374 |       -3.72 |
| **[_direct_] immediately~ready**     |   -1.33 |    -251.83 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     57 |  29,583 |       -3.75 |
| **[_direct_] immediately~sure**      |   -2.55 |  -1,603.95 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    138 | 134,139 |       -7.89 |

#### 8.3. _immediately_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~adjacent**  |    4.69 |     591.96 |           0.31 |            0.15 |    0.31 |    0.00 |    108 |     342 |        0.97 |
| **[_direct_] immediately~reachable** |    4.67 |     593.89 |           0.30 |            0.15 |    0.30 |    0.00 |    109 |     350 |        0.97 |
| **[_direct_] immediately~clear**     |    5.41 | 141,124.53 |           0.41 |            0.35 |    0.29 |    0.41 | 24,488 |  84,227 |        0.97 |
| **[_direct_] immediately~concerned** |   -1.29 |    -232.17 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     53 |  27,374 |       -3.72 |
| **[_direct_] immediately~ready**     |   -1.33 |    -251.83 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     57 |  29,583 |       -3.75 |
| **[_direct_] immediately~sure**      |   -2.55 |  -1,603.95 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    138 | 134,139 |       -7.89 |

#### 8.4. _immediately_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |    `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|--------:|------------:|
| **[_direct_] immediately~clear**     |    5.41 | 141,124.53 |           0.41 |            0.35 |    0.29 |    0.41 | 24,488 |  84,227 |        0.97 |
| **[_direct_] immediately~available** |    5.18 | 116,575.85 |           0.36 |            0.31 |    0.25 |    0.36 | 21,477 |  82,956 |        0.96 |
| **[_mirror_] immediately~available** |    5.44 |   1,232.57 |           0.32 |            0.19 |    0.06 |    0.32 |    184 |   3,079 |        0.98 |
| **[_direct_] immediately~concerned** |   -1.29 |    -232.17 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     53 |  27,374 |       -3.72 |
| **[_direct_] immediately~ready**     |   -1.33 |    -251.83 |          -0.00 |           -0.01 |   -0.01 |   -0.00 |     57 |  29,583 |       -3.75 |
| **[_direct_] immediately~sure**      |   -2.55 |  -1,603.95 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |    138 | 134,139 |       -7.89 |


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
* Total time to write partitioned parquet ⇾  `00:00:00.480`



```python
show_sample(hits_df.filter(['all_forms_lower', 'token_str']).sample(10).sort_values('all_forms_lower'))
```

    +-----------------------+---------------------------+---------------------------------------------------------------+
    | hit_id                | all_forms_lower           | token_str                                                     |
    +=======================+===========================+===============================================================+
    | pcc_eng_26_076.5750_x | (+)_inherently_social     | We 're trends experts , conversationalists and inherently     |
    | 1221569_14:8-9        |                           | social .                                                      |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_14_022.1646_x | (+)_particularly_risky    | Reading is a particularly risky pursuit , as there 's a       |
    | 0341833_217:4-5       |                           | perpetual danger that you might learn something .             |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_03_097.8994_x | (+)_that_much             | Have our needs really changed that much in six decades ?      |
    | 1568946_15:6-7        |                           |                                                               |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | apw_eng_19970723_0518 | hardly_any_busier         | the presidential press service , which serves as Yeltsin 's   |
    | _5:14-15-16           |                           | mouthpiece , is hardly any busier when the boss is in the     |
    |                       |                           | Kremlin .                                                     |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_val_1.6512_x1 | n't_that_big              | There 's been a string of high- profile " confessions " from  |
    | 0552_06:35-36-37      |                           | people who smoked pot in their younger days and are now       |
    |                       |                           | willing to concede something along the lines of " it was n't  |
    |                       |                           | that big of a deal . "                                        |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | nyt_eng_20070503_0010 | n't_that_simple           | it was n't that simple , not with pinch-runner Ben Zobrist    |
    | _7:3-4-5              |                           | falling as he tripped going around third on what should have  |
    |                       |                           | been a winning hit by Brendan Harris .                        |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_08_007.7250_x | not_exactly_inspiring     | As long as they pitch well , it works OK , but it 's not      |
    | 0108747_12:15-16-17   |                           | exactly inspiring .                                           |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_04_105.3270_x | not_particularly_accurate | While not particularly accurate ( if only pear trees really   |
    | 1685422_10:2-3-4      |                           | grew this fast ) , this is a lovely poetic encounter in both  |
    |                       |                           | word and image .                                              |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_15_098.7166_x | not_that_strong           | The motivation to buy a motorcycle will not be that strong    |
    | 1579317_12:08-10-11   |                           | among people who do not know how to ride one .                |
    +-----------------------+---------------------------+---------------------------------------------------------------+
    | pcc_eng_14_085.0139_x | not_yet_right             | Ganger had turned in a resume last March when Brown left but  |
    | 1358009_15:26-27-28   |                           | did not follow up to get the position , saying the timing was |
    |                       |                           | not yet right .                                               |
    +-----------------------+---------------------------+---------------------------------------------------------------+



```python
# perspect_blam = (blam_df
#                  .filter(regex=r'|'.join(adv_list[:5]), axis=0)
#                  .filter(perspective_cols + adjust_am_names(FOCUS_DICT[TAG]['adv_adj']))
#                  .filter(regex=r'^[^laN]').iloc[:,:14]
#                  .sort_values(blind_priority_cols, ascending=False))
# nb_show_table(pd.concat([perspect_blam.head(20), perspect_blam.tail(10)]))
```

```py
perspect_blam = (blam_df
                 .filter(regex=r'|'.join(adv_list[:5]), axis=0)
                 .filter(perspective_cols + adjust_am_names(FOCUS_DICT[TAG]['adv_adj']))
                 .filter(regex=r'^[^laN]').iloc[:,:14]
                 .sort_values(blind_priority_cols, ascending=False))
nb_show_table(pd.concat([perspect_blam.head(20), perspect_blam.tail(10)]))
```

|                                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |   `P1` |    `f1` |   `exp_f` |   `unexp_f` |   `odds_r_disc` |
|:------------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|-------:|--------:|----------:|------------:|----------------:|
| **[_direct_] any~happier**                |    7.76 |  7,282.99 |           0.41 |            0.23 |    0.41 |    0.05 |   834 |   2,004 |        0.99 |   0.42 |  16,238 |      5.13 |      828.87 |            2.47 |
| **[_direct_] necessarily~indicative**     |    7.46 | 10,827.28 |           0.59 |            0.31 |    0.59 |    0.03 | 1,389 |   2,313 |        0.99 |   0.60 |  42,886 |     15.63 |    1,373.37 |            2.36 |
| **[_direct_] any~clearer**                |    7.39 |  3,147.58 |           0.38 |            0.20 |    0.38 |    0.02 |   371 |     972 |        0.99 |   0.38 |  16,238 |      2.49 |      368.51 |            2.39 |
| **[_mirror_] any~closer**                 |    6.05 |    477.62 |           0.22 |            0.14 |    0.22 |    0.06 |    61 |     278 |        0.99 |   0.22 |   1,095 |      0.52 |       60.48 |            2.20 |
| **[_direct_] any~closer**                 |    5.92 |  4,021.04 |           0.16 |            0.10 |    0.16 |    0.04 |   611 |   3,686 |        0.98 |   0.17 |  16,238 |      9.43 |      601.57 |            1.91 |
| **[_direct_] any~worse**                  |    5.85 | 11,229.25 |           0.14 |            0.13 |    0.14 |    0.11 | 1,762 |  12,116 |        0.98 |   0.15 |  16,238 |     31.00 |    1,731.00 |            1.87 |
| **[_direct_] any~simpler**                |    5.61 |  1,479.26 |           0.16 |            0.08 |    0.16 |    0.01 |   229 |   1,446 |        0.98 |   0.16 |  16,238 |      3.70 |      225.30 |            1.87 |
| **[_direct_] any~easier**                 |    5.61 |  9,854.27 |           0.12 |            0.11 |    0.12 |    0.10 | 1,625 |  12,877 |        0.98 |   0.13 |  16,238 |     32.94 |    1,592.06 |            1.80 |
| **[_mirror_] any~better**                 |    5.50 |  2,543.31 |           0.35 |            0.23 |    0.10 |    0.35 |   390 |   3,831 |        0.98 |   0.10 |   1,095 |      7.19 |      382.81 |            1.97 |
| **[_direct_] any~younger**                |    5.47 |  1,591.82 |           0.14 |            0.08 |    0.14 |    0.02 |   255 |   1,784 |        0.98 |   0.14 |  16,238 |      4.56 |      250.44 |            1.82 |
| **[_direct_] any~safer**                  |    5.42 |  1,575.71 |           0.14 |            0.08 |    0.14 |    0.02 |   255 |   1,838 |        0.98 |   0.14 |  16,238 |      4.70 |      250.30 |            1.81 |
| **[_direct_] any~wiser**                  |    5.34 |    480.95 |           0.18 |            0.09 |    0.18 |    0.00 |    71 |     386 |        0.99 |   0.18 |  16,238 |      0.99 |       70.01 |            1.95 |
| **[_direct_] any~better**                 |    5.30 | 28,923.07 |           0.30 |            0.20 |    0.10 |    0.30 | 5,004 |  50,827 |        0.97 |   0.10 |  16,238 |    130.03 |    4,873.97 |            1.79 |
| **[_direct_] any~nicer**                  |    5.17 |    607.57 |           0.15 |            0.08 |    0.15 |    0.01 |    96 |     642 |        0.98 |   0.15 |  16,238 |      1.64 |       94.36 |            1.84 |
| **[_direct_] necessarily~cause**          |    5.07 |    341.90 |           0.38 |            0.19 |    0.38 |    0.00 |    52 |     134 |        0.98 |   0.39 |  42,886 |      0.91 |       51.09 |            1.97 |
| **[_direct_] remotely~comparable**        |    5.05 |    759.06 |           0.05 |            0.04 |    0.05 |    0.02 |   125 |   2,401 |        0.98 |   0.05 |   6,161 |      2.33 |      122.67 |            1.76 |
| **[_direct_] any~sweeter**                |    4.87 |    366.90 |           0.15 |            0.08 |    0.15 |    0.00 |    58 |     388 |        0.98 |   0.15 |  16,238 |      0.99 |       57.01 |            1.84 |
| **[_direct_] any~smarter**                |    4.82 |    532.11 |           0.12 |            0.06 |    0.12 |    0.01 |    90 |     733 |        0.98 |   0.12 |  16,238 |      1.88 |       88.12 |            1.74 |
| **[_direct_] necessarily~representative** |    4.71 |  2,416.54 |           0.18 |            0.10 |    0.18 |    0.01 |   488 |   2,560 |        0.96 |   0.19 |  42,886 |     17.30 |      470.70 |            1.54 |
| **[_mirror_] any~easier**                 |    4.67 |    377.02 |           0.09 |            0.07 |    0.09 |    0.06 |    63 |     681 |        0.98 |   0.09 |   1,095 |      1.28 |       61.72 |            1.76 |
| **[_direct_] that~aware**                 |   -1.90 |   -800.95 |          -0.00 |           -0.01 |   -0.02 |   -0.00 |   135 |  28,973 |       -4.64 |   0.00 | 166,676 |    760.80 |     -625.80 |           -0.76 |
| **[_direct_] exactly~good**               |   -1.98 | -1,449.44 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |   263 | 201,244 |       -4.36 |   0.00 |  44,503 |  1,410.97 |   -1,147.97 |           -0.74 |
| **[_direct_] necessarily~different**      |   -2.01 |   -638.37 |          -0.01 |           -0.01 |   -0.01 |   -0.01 |    78 |  80,643 |       -5.99 |   0.00 |  42,886 |    544.87 |     -466.87 |           -0.85 |
| **[_direct_] that~wrong**                 |   -2.03 |   -657.43 |          -0.00 |           -0.01 |   -0.02 |   -0.00 |    81 |  21,332 |       -5.92 |   0.00 | 166,676 |    560.16 |     -479.16 |           -0.85 |
| **[_direct_] exactly~bad**                |   -2.11 |   -966.10 |          -0.01 |           -0.01 |   -0.01 |   -0.02 |   125 | 119,509 |       -5.70 |   0.00 |  44,503 |    837.91 |     -712.91 |           -0.83 |
| **[_direct_] that~proud**                 |   -2.15 |   -557.56 |          -0.00 |           -0.01 |   -0.02 |   -0.00 |    51 |  16,528 |       -7.51 |   0.00 | 166,676 |    434.01 |     -383.01 |           -0.94 |
| **[_direct_] that~many**                  |   -2.47 | -3,082.65 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |   361 |  97,883 |       -6.12 |   0.00 | 166,676 |  2,570.32 |   -2,209.32 |           -0.87 |
| **[_direct_] that~better**                |   -2.72 | -1,823.15 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |   134 |  50,827 |       -8.96 |   0.00 | 166,676 |  1,334.67 |   -1,200.67 |           -1.01 |
| **[_direct_] that~likely**                |   -2.90 | -1,876.49 |          -0.01 |           -0.02 |   -0.02 |   -0.01 |   111 |  49,647 |      -10.74 |   0.00 | 166,676 |  1,303.69 |   -1,192.69 |           -1.08 |
| **[_direct_] that~sure**                  |   -3.16 | -5,105.66 |          -0.02 |           -0.02 |   -0.02 |   -0.02 |   301 | 134,139 |      -10.70 |   0.00 | 166,676 |  3,522.37 |   -3,221.37 |           -1.09 |




```python
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
2024-07-31

## *necessarily*


|                                           |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`        | `l2`           |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:------------------------------------------|------:|--------:|--------:|-------:|----------:|:------------|:---------------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] necessarily~indicative**     | 1,389 |    0.59 |    7.46 |   0.60 | 10,827.28 | necessarily | indicative     | 42,886 |  2,313 | 6,347,362 |     15.63 |    1,373.37 |        0.99 |            2.36 | 36.85 |   1.95 |    0.03 |   0.03 |           0.59 |            0.31 | direct      |
| **[_direct_] necessarily~cause**          |    52 |    0.38 |    5.07 |   0.39 |    341.90 | necessarily | cause          | 42,886 |    134 | 6,347,362 |      0.91 |       51.09 |        0.98 |            1.97 |  7.09 |   1.76 |    0.00 |   0.00 |           0.38 |            0.19 | direct      |
| **[_direct_] necessarily~representative** |   488 |    0.18 |    4.71 |   0.19 |  2,416.54 | necessarily | representative | 42,886 |  2,560 | 6,347,362 |     17.30 |      470.70 |        0.96 |            1.54 | 21.31 |   1.45 |    0.01 |   0.01 |           0.18 |            0.10 | direct      |
| **[_direct_] necessarily~synonymous**     |   165 |    0.17 |    4.26 |   0.17 |    785.72 | necessarily | synonymous     | 42,886 |    943 | 6,347,362 |      6.37 |      158.63 |        0.96 |            1.50 | 12.35 |   1.41 |    0.00 |   0.00 |           0.17 |            0.09 | direct      |
| **[_direct_] necessarily~incompatible**   |   101 |    0.19 |    4.25 |   0.20 |    506.31 | necessarily | incompatible   | 42,886 |    513 | 6,347,362 |      3.47 |       97.53 |        0.97 |            1.56 |  9.70 |   1.46 |    0.00 |   0.00 |           0.19 |            0.10 | direct      |
| **[_direct_] necessarily~reflective**     |   181 |    0.14 |    4.05 |   0.15 |    806.50 | necessarily | reflective     | 42,886 |  1,197 | 6,347,362 |      8.09 |      172.91 |        0.96 |            1.42 | 12.85 |   1.35 |    0.00 |   0.00 |           0.14 |            0.07 | direct      |
| **[_direct_] necessarily~predictive**     |    57 |    0.18 |    3.85 |   0.19 |    281.73 | necessarily | predictive     | 42,886 |    299 | 6,347,362 |      2.02 |       54.98 |        0.96 |            1.54 |  7.28 |   1.45 |    0.00 |   0.00 |           0.18 |            0.09 | direct      |
| **[_direct_] necessarily~true**           | 3,245 |    0.09 |    3.77 |   0.09 | 11,473.44 | necessarily | true           | 42,886 | 34,967 | 6,347,362 |    236.25 |    3,008.75 |        0.93 |            1.21 | 52.82 |   1.14 |    0.07 |   0.08 |           0.09 |            0.08 | direct      |
| **[_mirror_] necessarily~wrong**          |   214 |    0.02 |    3.38 |   0.03 |    802.78 | necessarily | wrong          |    992 |  8,506 |   583,470 |     14.46 |      199.54 |        0.93 |            1.28 | 13.64 |   1.17 |    0.20 |   0.22 |           0.20 |            0.11 | mirror      |
| **[_direct_] necessarily~permanent**      |   151 |    0.09 |    3.34 |   0.10 |    550.69 | necessarily | permanent      | 42,886 |  1,488 | 6,347,362 |     10.05 |      140.95 |        0.93 |            1.22 | 11.47 |   1.18 |    0.00 |   0.00 |           0.09 |            0.05 | direct      |


### 1. _necessarily indicative_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_085.0184_x1357579_27:29-30-31`**  | This is a fine performance for the Republicans , to be sure , but winning in Republican states in a Republican year in a politically polarized era is not __`necessarily indicative`__ of a wave .                                                                                                                                           |
| **`pcc_eng_28_012.2281_x0181852_057:44-45-46`** | Out of the 1050 pastors we surveyed during two pastors conferences held in Pasadena , California , 825 , or 78 % ( 326 in 2005 and 499 in 2006 , This is a small local sampling to assess causes and motivations , not __`necessarily indicative`__ of a national sampling . ) said they were forced to resign from a church at least once . |
| **`pcc_eng_08_077.4050_x1237053_11:11-12-13`**  | The test results should be considered as preliminary and are not __`necessarily indicative`__ of long-term performance .                                                                                                                                                                                                                     |
| **`pcc_eng_14_018.0116_x0274841_03:7-8-9`**     | How busy a person seems is not __`necessarily indicative`__ of the quality of their results .                                                                                                                                                                                                                                                |
| **`pcc_eng_19_016.6467_x0252410_04:14-15-16`**  | References made to mineralization hosted on adjacent and / or nearby properties is not __`necessarily indicative`__ of mineralization hosted on the Company 's Douay Property .                                                                                                                                                              |
| **`pcc_eng_22_059.0403_x0938370_033:08-09-10`** | Operating results for the interim period are not __`necessarily indicative`__ of the results to be expected for the full year .                                                                                                                                                                                                              |
| **`pcc_eng_25_037.9325_x0597906_43:6-7-8`**     | A high feature rating is n't __`necessarily indicative`__ of a host that offers plenty of features but rather one which offers more or better features than similarly priced or situated web hosts .                                                                                                                                         |
| **`pcc_eng_05_035.0238_x0550987_29:17-18-19`**  | We argue that the apparent resistance of certain experiential phenomena to literal description and explanation is not __`necessarily indicative`__ of pre-theoretic linguistic imprecision .                                                                                                                                                 |


### 2. _necessarily cause_


|                                                | `token_str`                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_089.5717_x1432874_45:11-12-13`** | A test showing small amphetamine concentrations in your body is not __`necessarily cause`__ for alarm .                                        |
| **`pcc_eng_11_068.0100_x1084620_43:3-4-5`**    | This is not __`necessarily cause`__ for concern .                                                                                              |
| **`pcc_eng_07_013.9785_x0210279_048:3-4-5`**   | This is not __`necessarily cause`__ for alarm .                                                                                                |
| **`pcc_eng_00_067.7784_x1079285_18:17-18-19`** | While it appears problematic , economists with the federal government say a negative savings rate is n't __`necessarily cause`__ for concern . |
| **`pcc_eng_08_103.7341_x1663397_40:10-11-12`** | Small changes in color , smell or taste are not __`necessarily cause`__ for alarm , adds Dr. Goldstone .                                       |
| **`pcc_eng_test_2.05409_x24786_01:11-12-13`**  | The likes of botulism and anthrax in the air are n't __`necessarily cause`__ for alarm .                                                       |
| **`pcc_eng_02_098.4559_x1575696_01:4-5-6`**    | This change is not __`necessarily cause`__ for a meltdown : Wait and taste the 42 % before you freak out .                                     |
| **`pcc_eng_21_013.1878_x0196808_03:17-18-19`** | Although there are be 95 convicted sex offenders living in Island County , their presence is not __`necessarily cause`__ for public concern .  |


### 3. _necessarily representative_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                           |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_016.2604_x0246368_02:1-2-3`**     | Not __`necessarily representative`__ of the book , this is a peek at some of the mystery .                                                                                                                                                                                                                                                                                            |
| **`pcc_eng_29_093.0438_x1486867_15:6-7-8`**     | Admittedly , that company was not __`necessarily representative`__ of the treasury world as a whole .                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_26_004.5340_x0056996_064:25-26-27`** | His effectiveness as a shooter off the dribble was n't quite as good , but the sample size is low enough that this is n't __`necessarily representative`__ of his skill set , and he could see big improvement going forward as he gets more opportunity , as the form is there .                                                                                                     |
| **`pcc_eng_16_085.5685_x1368719_09:17-18-19`**  | And the pool of students who take the SAT is tilted toward college - goers and not __`necessarily representative`__ of all high school students .                                                                                                                                                                                                                                     |
| **`pcc_eng_10_019.7780_x0303476_14:18-19-20`**  | The brains studied were mostly donated by concerned families , which means they were n't random and not __`necessarily representative`__ of all men who have played football .                                                                                                                                                                                                        |
| **`pcc_eng_05_083.7342_x1338981_30:27-28-29`**  | The views and opinions expressed by the SOI Industry Consortium through officers in the SOI Industry Consortium or in this presentation or other communication vehicles are not __`necessarily representative`__ of the views and opinions of individual members .                                                                                                                    |
| **`pcc_eng_06_020.6503_x0317914_05:28-29-30`**  | Pharmaceutical Commerce reported that the revised numbers in fact ranged from 29 to 729 percent and furthermore noted that the original and even the revised numbers are not __`necessarily representative`__ of anything at all because the sample base consisted of solicitations that Premier member hospitals chose to send in rather than a true scientific sample of invoices . |
| **`pcc_eng_06_078.9827_x1261010_14:7-8-9`**     | I know that cover art is not __`necessarily representative`__ of the actual product , but in this case the cover art has little to do with reality .                                                                                                                                                                                                                                  |


### 4. _necessarily synonymous_


|                                                | `token_str`                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_072.3516_x1152499_2:4-5-6`**     | " Laughter is not __`necessarily synonymous`__ with superficiality , carelessness or a lack of seriousness , and it can even have a more beneficial effect on the mind than the grave expression which some think characteristic of sages . |
| **`pcc_eng_12_060.5320_x0962597_10:08-09-10`** | ' Quantity ' , however , is n't __`necessarily synonymous`__ to ' quality ' .                                                                                                                                                               |
| **`pcc_eng_03_005.0237_x0065009_10:15-16-17`** | Oculus is seeking the most " innovative " games and experiences , which is not __`necessarily synonymous`__ with the " best " .                                                                                                             |
| **`pcc_eng_28_074.6429_x1191131_35:19-20-21`** | All of this goes to imply that the writers desired to make a clear point : Islam is not __`necessarily synonymous`__ with terrorism .                                                                                                       |
| **`pcc_eng_28_075.3189_x1201948_43:09-10-11`** | " Vintage " and " valuable " are not __`necessarily synonymous`__ .                                                                                                                                                                         |
| **`pcc_eng_02_033.6539_x0528570_06:17-18-19`** | It 's clear that boycotts are an increasingly popular form of protest , but popularity is not __`necessarily synonymous`__ with effectiveness .                                                                                             |
| **`pcc_eng_22_001.4748_x0007738_11:19-20-21`** | Kernot said that she hoped the calendar would send the message to women that success and inspiration were not __`necessarily synonymous`__ with fame and wealth and that happiness was not just about being thin or fashionable .           |
| **`pcc_eng_19_016.8392_x0255461_12:11-12-13`** | But the charging of this criminal and his partners is n't __`necessarily synonymous`__ with justice or their repaying society as they should , a situation that often occurs in Havana as well .                                            |


### 5. _necessarily incompatible_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_035.9927_x0566392_36:70-71-72`**  | Just as Motherwell saw his work in terms of 'a dialectic between the conscious ( straight lines , designed shapes , weighted colours , abstract language ) and the unconscious ( soft lines , obscured shapes , automatism ) resolved into a synthesis which differs as a whole from either ' 6 , so Umerle 's work treads a similar path , proving that formal and spontaneous procedures are not __`necessarily incompatible`__ and that mark - making truly is both a means to an end and an end in itself . |
| **`pcc_eng_15_098.4535_x1575054_15:7-8-9`**     | But that kind of vivacity is not __`necessarily incompatible`__ with steadiness .                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_23_096.7808_x1547968_167:08-09-10`** | I have always maintained that technology is not __`necessarily incompatible`__ with the preservation of our values and freedoms .                                                                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_29_034.5737_x0541912_107:43-44-45`** | The first is a biography of Darwin and attempts to show that Darwin was a believing member of the Church of England until the ascent of Darwin to agnosticism later in his life ; hence , " Darwinism " and theism are not __`necessarily incompatible`__ .                                                                                                                                                                                                                                                     |
| **`pcc_eng_16_057.4490_x0913733_25:7-8-9`**     | More , the dual objectives are n't __`necessarily incompatible`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **`apw_eng_20090520_0695_5:14-15-16`**          | but Schiffer says the countries ' interests in the crucial region `` are not __`necessarily incompatible`__ . ''                                                                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_11_065.1912_x1038846_017:15-16-17`** | A science teacher from a Catholic high school countered that evolution and religion are n't __`necessarily incompatible`__ ; at least they are n't in her school .                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_25_008.4050_x0120105_66:11-12-13`**  | Though independent of cultures , the Gospel and evangelization are not __`necessarily incompatible`__ with them ; rather they are capable of permeating them all without becoming subject to any one of them .                                                                                                                                                                                                                                                                                                  |


### 6. _necessarily reflective_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                          |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_032.9150_x0516037_10:12-13-14`**  | The story although very similar to a biblical creation story is n't __`necessarily reflective`__ only of a christian view point , to me it 's about the author 's own creation .                                                                                                                     |
| **`pcc_eng_06_105.7066_x1693818_041:26-27-28`** | The observation that the open source community generally does n't have time for anything but the truth which is a nice ideal but perhaps is n't __`necessarily reflective`__ of the entire open source world so much as a few of the important luminaries .                                          |
| **`pcc_eng_11_019.0500_x0291825_2:12-13-14`**   | Now , it 's worth noting that these Ukraine dates are n't __`necessarily reflective`__ of availability elsewhere .                                                                                                                                                                                   |
| **`pcc_eng_02_081.4934_x1301592_09:23-24-25`**  | Ellison 's public support is impressive , and it has helped to keep potential challengers on the bench , but it 's not __`necessarily reflective`__ of actual DNC votes .                                                                                                                            |
| **`pcc_eng_13_085.5362_x1366486_114:23-24-25`** | However , because the program is voluntary , the employers represented are self-selected and unevenly distributed across the country , and thus not __`necessarily reflective`__ of the general population of national employers who would be required to screen workers under a mandatory program . |
| **`pcc_eng_02_089.0522_x1423589_262:36-37-38`** | Even before I read that article I recognized that the persona someone tries to convey in Facebook , My Space , Twitter and even professional networking sites such as Linked In and Plaxo , are not __`necessarily reflective`__ of what is really going on in that person 's life .                 |
| **`pcc_eng_17_080.3200_x1281910_05:7-8-9`**     | Falling flat in the WWE is n't __`necessarily reflective`__ of your skills as a professional wrestler .                                                                                                                                                                                              |
| **`pcc_eng_11_080.7360_x1290630_46:19-20-21`**  | This is a personal blog , and does not constitute legal advice in any form , and is not __`necessarily reflective`__ of the policies or opinions of Stafne Law Firm .                                                                                                                                |


### 7. _necessarily predictive_


|                                                 | `token_str`                                                                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_102.6723_x1643252_091:4-5-6`**    | The number is not __`necessarily predictive`__ because Democrats are typically more likely to vote early than Republicans "                                                                                                                                     |
| **`pcc_eng_18_086.5054_x1384629_026:21-22-23`** | There are varying degrees of offensive prowess sprinkled throughout the list of the hardest-hitters in baseball , so it is n't __`necessarily predictive`__ of anything other than solid-average offense - but it 's a good sign nevertheless .                 |
| **`pcc_eng_29_097.7421_x1563023_31:7-8-9`**     | That said , these results are not __`necessarily predictive`__ of any case .                                                                                                                                                                                    |
| **`pcc_eng_26_039.3441_x0619981_08:29-30-31`**  | Previous contests have seen candidates rise and fall in the weeks before the first votes are cast , and national polls at this stage of the race are not __`necessarily predictive`__ of the final outcome of the monthslong nominating battle .                |
| **`pcc_eng_08_106.2551_x1704303_70:4-5-6`**     | Historial data is not __`necessarily predictive`__ of future movement in interest rates .                                                                                                                                                                       |
| **`pcc_eng_11_087.4867_x1399981_082:34-35-36`** | Of course , this survey only looked at homeschoolers with religious mothers , not at all homeschoolers , and it looked at individuals who were adults in 2011 , meaning that it is n't __`necessarily predictive`__ of how current homechoolers will turn out . |
| **`pcc_eng_17_078.4589_x1251825_057:4-5-6`**    | But they 're not __`necessarily predictive`__ .                                                                                                                                                                                                                 |
| **`pcc_eng_13_009.6430_x0139427_29:3-4-5`**     | That 's not __`necessarily predictive`__ , either .                                                                                                                                                                                                             |


### 8. _necessarily true_


|                                                 | `token_str`                                                                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_041.6390_x0656897_026:18-19-20`** | And that 's a huge thing for a man to say to his son , and -- not __`necessarily true`__ , I might add , he 's a wonderful actor himself -- but it was so encouraging and supportive . "                                  |
| **`pcc_eng_25_031.7343_x0497429_03:32-33-34`**  | While more than half of consumers are now using Internet search engines to locate nearby restaurants , and 56 % are using them to locate nearby retailers , the same is n't __`necessarily true`__ for other businesses . |
| **`pcc_eng_02_037.9328_x0597633_32:5-6-7`**     | But , this is not __`necessarily true`__ .                                                                                                                                                                                |
| **`pcc_eng_08_004.1465_x0050914_04:5-6-7`**     | but in fact is not __`necessarily true`__ ,                                                                                                                                                                               |
| **`pcc_eng_08_078.5423_x1255656_082:19-20-21`** | You might think that proves that we value things more when we own them , but that 's not __`necessarily true`__ .                                                                                                         |
| **`pcc_eng_10_079.8713_x1274736_053:15-16-17`** | That 's all they would really need to know , even if it 's not __`necessarily true`__ .                                                                                                                                   |
| **`pcc_eng_28_077.4421_x1236483_10:19-20-21`**  | Some cat owners believe that the Selkirk Rex 's curly fur makes him hypoallergenic , but that 's not __`necessarily true`__ .                                                                                             |
| **`pcc_eng_15_047.3185_x0748840_230:17-18-19`** | It helps to hydrate you by taking in more fluid than it releases , which is not __`necessarily true`__ of highly caffeinated drinks .                                                                                     |


### 9. _necessarily wrong_


|                                                | `token_str`                                                                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_004.7926_x0061277_30:3-4-5`**    | There 's nothing __`necessarily wrong`__ with Tweedy or fun .                                                                                                                      |
| **`pcc_eng_29_002.4357_x0023086_11:3-4-5`**    | There 's nothing __`necessarily wrong`__ with that , but that type of content does have an expiration date and not much value to online visitors or search engines .               |
| **`pcc_eng_06_071.0597_x1133620_16:3-4-5`**    | This is n't __`necessarily wrong`__ if the entire area is of uniform darkness .                                                                                                    |
| **`pcc_eng_16_051.2525_x0813463_19:09-10-11`** | It 's important to note that there is nothing __`necessarily wrong`__ with going broke .                                                                                           |
| **`pcc_eng_16_088.0642_x1409368_06:3-4-5`**    | There is nothing __`necessarily wrong`__ with this ; editors make choices and the Star Observer is far more balanced and objective than the current Murdoch press , for instance . |
| **`pcc_eng_01_065.4083_x1041807_20:21-22-23`** | It may have been impolitic to lump them together in one dismissive phrase , but that which is impolitic is not __`necessarily wrong`__ .                                           |
| **`pcc_eng_03_092.9341_x1488582_44:1-2-3`**    | Not __`necessarily wrong`__ , but not the way to seize ground going forward .                                                                                                      |
| **`pcc_eng_16_022.6427_x0350405_025:3-4-5`**   | There 's nothing __`necessarily wrong`__ with your head .                                                                                                                          |


### 10. _necessarily permanent_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                          |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_087.2858_x1396726_06:10-11-12`**  | It can be cut out , but this is not __`necessarily permanent`__ , or permanent removal of the ingrown toenail .                                                                                                                                                                                                      |
| **`pcc_eng_23_030.9006_x0482759_73:4-5-6`**     | But it is n't __`necessarily permanent`__ .                                                                                                                                                                                                                                                                          |
| **`pcc_eng_26_083.9281_x1341010_23:5-6-7`**     | Domestic violence orders are not __`necessarily permanent`__ - the Queensland Courts shows more than 30 per cent of all orders made in 2018 were temporary .                                                                                                                                                         |
| **`pcc_eng_07_019.1048_x0292784_61:17-18-19`**  | Rates were volatile late last week , and are calmer this week , but that 's not __`necessarily permanent`__ .                                                                                                                                                                                                        |
| **`pcc_eng_12_039.6552_x0625230_50:27-28-29`**  | MO Tempo plays a ton of efficient creatures that excels in interacting with opposing creatures ( especially through Spiky ) as well as efficient , but not __`necessarily permanent`__ , ways to move blockers out of the way such as Pushback and Pother :                                                          |
| **`pcc_eng_08_049.4219_x0783755_7:7-8-9`**      | The Treasury said the sanctions were not __`necessarily permanent`__ and could be lifted on people " who take concrete and meaningful actions to restore democratic order , refuse to take part in human rights abuses , speak out against abuses committed by the government and combat corruption in Venezuela . " |
| **`pcc_eng_07_012.6661_x0189144_13:19-20-21`**  | The early crawler shall seem light years ahead of his or her peers , but this advantage is n't __`necessarily permanent`__ .                                                                                                                                                                                         |
| **`pcc_eng_22_002.4236_x0023136_104:09-10-11`** | Of course , making a living wage is not __`necessarily permanent`__ either .                                                                                                                                                                                                                                         |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_indicative_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_cause_80ex~10.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_representative_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_synonymous_80ex~47.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_incompatible_80ex~30.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_reflective_80ex~45.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_predictive_80ex~22.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_true_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_wrong_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/necessarily/necessarily_permanent_80ex~44.csv`

## *that*


|                              |    `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`     |    `f1` |    `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-----------------------------|-------:|--------:|--------:|-------:|----------:|:-------|:---------|--------:|--------:|----------:|----------:|------------:|------------:|----------------:|-------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_mirror_] that~great**    |    298 |    0.13 |    3.89 |   0.14 |  1,216.00 | that   | great    |   4,559 |   2,123 |   583,470 |     16.59 |      281.41 |        0.94 |            1.35 |  16.30 |   1.25 |    0.06 |   0.07 |           0.13 |            0.10 | mirror      |
| **[_direct_] that~great**    | 11,065 |    0.22 |    3.50 |   0.24 | 32,588.43 | that   | great    | 166,676 |  45,359 | 6,347,362 |  1,191.09 |    9,873.91 |        0.89 |            1.11 |  93.87 |   0.97 |    0.06 |   0.07 |           0.22 |            0.14 | direct      |
| **[_direct_] that~uncommon** |    802 |    0.23 |    3.33 |   0.25 |  2,384.09 | that   | uncommon | 166,676 |   3,165 | 6,347,362 |     83.11 |      718.89 |        0.90 |            1.10 |  25.38 |   0.98 |    0.00 |   0.00 |           0.23 |            0.12 | direct      |
| **[_direct_] that~hard**     |  9,963 |    0.20 |    3.31 |   0.22 | 27,269.05 | that   | hard     | 166,676 |  45,061 | 6,347,362 |  1,183.26 |    8,779.74 |        0.88 |            1.05 |  87.96 |   0.93 |    0.05 |   0.06 |           0.20 |            0.13 | direct      |
| **[_mirror_] that~simple**   |    483 |    0.06 |    2.77 |   0.06 |  1,259.25 | that   | simple   |   4,559 |   7,465 |   583,470 |     58.33 |      424.67 |        0.88 |            0.99 |  19.32 |   0.92 |    0.09 |   0.11 |           0.09 |            0.08 | mirror      |
| **[_mirror_] that~easy**     |    465 |    0.05 |    2.65 |   0.06 |  1,146.45 | that   | easy     |   4,559 |   7,749 |   583,470 |     60.55 |      404.45 |        0.87 |            0.95 |  18.76 |   0.89 |    0.09 |   0.10 |           0.09 |            0.07 | mirror      |
| **[_direct_] that~big**      |  6,273 |    0.12 |    2.56 |   0.15 | 12,074.72 | that   | big      | 166,676 |  42,912 | 6,347,362 |  1,126.83 |    5,146.17 |        0.82 |            0.82 |  64.98 |   0.75 |    0.03 |   0.04 |           0.12 |            0.08 | direct      |
| **[_direct_] that~bad**      | 16,635 |    0.12 |    2.52 |   0.14 | 31,301.65 | that   | bad      | 166,676 | 119,509 | 6,347,362 |  3,138.20 |   13,496.80 |        0.81 |            0.82 | 104.65 |   0.72 |    0.08 |   0.10 |           0.12 |            0.10 | direct      |
| **[_direct_] that~simple**   |  6,219 |    0.11 |    2.40 |   0.13 | 10,895.68 | that   | simple   | 166,676 |  46,867 | 6,347,362 |  1,230.69 |    4,988.31 |        0.80 |            0.77 |  63.25 |   0.70 |    0.03 |   0.04 |           0.11 |            0.07 | direct      |
| **[_direct_] that~stupid**   |    811 |    0.12 |    2.34 |   0.14 |  1,524.30 | that   | stupid   | 166,676 |   5,617 | 6,347,362 |    147.50 |      663.50 |        0.82 |            0.80 |  23.30 |   0.74 |    0.00 |   0.00 |           0.12 |            0.06 | direct      |


### 1. _that great_


|                                                | `token_str`                                                                                                                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20070522_0013_45:5-6-7`**           | `` Wow , is n't __`that great`__ ? '' Romney responded .                                                                                                                                                                 |
| **`pcc_eng_09_033.0993_x0519629_12:37-38-39`** | Musk also explained to Mashable when Solar City looked at their third - party panel manufacturers , " They were happy to make a standard efficiency 15 panel panel year - over - year that looked not __`that great`__ . |
| **`pcc_eng_01_045.9200_x0725816_49:5-6-7`**    | Overall , thing were n't __`that great`__ for the collective farm chairmen either .                                                                                                                                      |
| **`nyt_eng_19960207_0819_3:22-23-24`**         | `` If you take out the recent liquidity in the market , you are left with a macroeconomic situation that is n't __`that great`__ . ''                                                                                    |
| **`pcc_eng_06_021.1620_x0326162_23:23-25-26`** | From a pure football standpoint , however , Purifoy has tremendous athleticism and is very fluid in coverage , although he is n't all __`that great`__ in run support .                                                  |
| **`pcc_eng_03_043.0993_x0681989_3:3-4-5`**     | Restaurants are not __`that great`__ .                                                                                                                                                                                   |
| **`pcc_eng_13_009.7563_x0141284_27:7-8-9`**    | Even if the DPP proposal was not __`that great`__ , the KMT is far from considerate to the flood victims and the Aborigines .                                                                                            |
| **`pcc_eng_01_097.6537_x1562546_16:15-17-18`** | Been enjoying putting together cool packages for my downstream , even though I 've not been __`that great`__ at being cheap !                                                                                            |


### 2. _that uncommon_


|                                                 | `token_str`                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_103.3141_x1653401_22:10-11-12`**  | This type of military operations in our area is not __`that uncommon`__ .                                                                                                                                |
| **`pcc_eng_17_079.7416_x1272578_13:16-17-18`**  | As bold as it may seem , drug tunnels beneath the port of entry are n't __`that uncommon`__ .                                                                                                            |
| **`pcc_eng_19_014.5838_x0219430_16:5-6-7`**     | " It 's really not __`that uncommon`__ for me to not know him , like , I 'm not that surprised that we have n't met before , " said Arendas .                                                            |
| **`pcc_eng_26_033.6692_x0528152_06:5-6-7`**     | Churches sharing churchyards is not __`that uncommon`__ ; there are at least a dozen examples in East Anglia , and there were once more .                                                                |
| **`pcc_eng_22_085.2565_x1361818_117:22-23-24`** | The communal lifestyle of the bandhouse , reflective of the hippie days of the ' 60s and ' 70s , was not __`that uncommon`__ among rock groups , such as the Beach Boys and others , according to Jinx . |
| **`pcc_eng_23_007.2810_x0101499_38:3-4-5`**     | Firing is n't __`that uncommon`__ , especially in sales .                                                                                                                                                |
| **`pcc_eng_21_092.3071_x1475561_09:08-10-11`**  | The truth is that these tables are n't all __`that uncommon`__ .                                                                                                                                         |
| **`pcc_eng_02_005.7628_x0077021_14:08-09-10`**  | But the reality is that it 's not __`that uncommon`__ .                                                                                                                                                  |


### 3. _that hard_


|                                                | `token_str`                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_062.4800_x0994181_028:7-8-9`**   | The concept of machine learning is n't __`that hard`__ to grasp :                                                                  |
| **`pcc_eng_23_009.6496_x0139600_01:3-4-5`**    | It is not __`that hard`__ to get the council tax written off                                                                       |
| **`pcc_eng_00_011.7344_x0173314_01:4-5-6`**    | Saving money is n't __`that hard`__ .                                                                                              |
| **`pcc_eng_26_081.8756_x1307504_08:08-09-10`** | Calculating the Stamp Duty and Registration is not __`that hard`__ since you can do it manually using the stamp duty calculator .  |
| **`pcc_eng_19_013.6843_x0204868_68:3-4-5`**    | It 's not __`that hard`__ to make a plumbing diagram so long as you can visualize the pipes in your head before you install them . |
| **`pcc_eng_14_005.4285_x0071765_88:3-4-5`**    | It 's not __`that hard`__ and it 'll probably save your arse at some point in the very near future .                               |
| **`pcc_eng_25_038.8348_x0612330_120:7-8-9`**   | However , writing product review is not __`that hard`__ to define .                                                                |
| **`pcc_eng_24_073.7877_x1177460_23:08-10-11`** | It 's just writing , it ca n't be __`that hard`__ !                                                                                |


### 4. _that simple_


|                                                | `token_str`                                                                                                    |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_089.8584_x1435560_7:12-13-14`**  | Our job to explore it and share with our kids are not __`that simple`__ .                                      |
| **`pcc_eng_16_052.7466_x0837553_54:4-5-6`**    | Unfortunately it 's not __`that simple`__ though .                                                             |
| **`pcc_eng_26_009.7911_x0142116_08:09-10-11`** | Discount rates for these kinds of guidelines are n't __`that simple`__ to find .                               |
| **`pcc_eng_12_030.5044_x0477711_54:6-7-8`**    | Solomon said the cost is not __`that simple`__ .                                                               |
| **`pcc_eng_03_085.2862_x1364812_026:3-4-5`**   | It 's not __`that simple`__ with Phragmites , and we have yet to see this kind of commitment from government . |
| **`pcc_eng_09_091.2686_x1460547_18:4-6-7`**    | The process is not always __`that simple`__ - or fast .                                                        |
| **`pcc_eng_28_049.1401_x0778921_08:4-5`**      | IT COULD BE __`THAT SIMPLE`__ .                                                                                |
| **`pcc_eng_19_071.0763_x1131741_22:12-13-14`** | But when watching Internet video on a TV , it is n't __`that simple`__ .                                       |


### 5. _that easy_


|                                                | `token_str`                                                                                                                                                                                                                                  |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_104.6413_x1675406_27:38-39-40`** | It 's taken finding out she has a brother , a move to a new city , and making friends with unexpected people to help Sayer try to let go of her past , but it 's not __`that easy`__ and we get to see the internal struggle she has daily . |
| **`pcc_eng_26_040.5813_x0640017_05:3-4-5`**    | It is not __`that easy`__ to know if someone blocked you on Facebook .                                                                                                                                                                       |
| **`pcc_eng_26_031.7913_x0497547_47:15-16-17`** | Mostly not on Wall Street , as stock portfolios without Arms Bazaar stigma are not __`that easy`__ to come by , and tend to be jeered at by those judging a fund by what it returns .                                                        |
| **`pcc_eng_19_070.4512_x1121673_03:23-24-25`** | The World Badminton Championship in London but he had done his best on this match even mistake are there but it 's not __`that easy`__ to prevent as it may seen .                                                                           |
| **`pcc_eng_18_086.4968_x1384488_04:6-8-9`**    | Of course , it may not be __`that easy`__ , and there are a few things that could be happening in your home that could end up with you scheduling furnace repair or trying to figure out why your bill is so high .                          |
| **`pcc_eng_27_037.9945_x0597966_05:3-4-5`**    | It is not __`that easy`__ to make a website a money making machine .                                                                                                                                                                         |
| **`pcc_eng_20_087.1149_x1391270_09:5-6-7`**    | However , it is not __`that easy`__ to achieve .                                                                                                                                                                                             |
| **`nyt_eng_20000312_0003_20:7-8-9`**           | this year , it 's just not __`that easy`__ .                                                                                                                                                                                                 |


### 6. _that big_


|                                                | `token_str`                                                                                                                                                                                                         |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_094.1804_x1505595_13:6-7-8`**    | Of course , story is n't __`that big`__ here - it 's all about tactics and murder and reminds me of these free-to - play Adult Swim flash games from years ago where the goal is to try and kill yourself quickly . |
| **`pcc_eng_28_015.4187_x0233456_16:10-11-12`** | " When we started in 2012 , it was n't __`that big`__ , but now it 's an enabler .                                                                                                                                  |
| **`pcc_eng_07_031.6603_x0495854_25:14-15-16`** | ( Bahrain flag is red and white as well and my monitor is n't __`that big`__ ) .                                                                                                                                    |
| **`pcc_eng_08_078.2884_x1251506_39:08-09-10`** | Speaking from experience , # 2 is n't __`that big`__ of a problem .                                                                                                                                                 |
| **`pcc_eng_14_001.7455_x0012178_10:12-13-14`** | Comments like , " You 're so tough , you 're not __`that big`__ .                                                                                                                                                   |
| **`pcc_eng_16_088.6517_x1418899_20:08-09-10`** | XO - Marion PS - you are n't __`that big`__ / tall in that photo !                                                                                                                                                  |
| **`nyt_eng_20000104_0006_51:4-5-6`**           | but I 'm not __`that big`__ of a dreamer . ''                                                                                                                                                                       |
| **`pcc_eng_09_086.3260_x1380449_12:16-17-18`** | Missing the spring is in no way ideal for Key , but it also is n't __`that big`__ of a deal .                                                                                                                       |


### 7. _that bad_


|                                                 | `token_str`                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_013.2766_x0198466_48:15-16-17`**  | I would n't say it was a completely comfortable experience , but it was n't __`that bad`__ .                                                                              |
| **`pcc_eng_12_085.5057_x1365520_381:14-15-16`** | Somehow , we often have a way of convincing ourselves that it 's not __`that bad`__ to use vulgar language , especially since it 's so firmly entrenched in our culture . |
| **`pcc_eng_13_030.3923_x0475343_083:3-4-5`**    | It 's not __`that bad`__ , I 'm just maneuvering to the shredder to strike down some water , she answers .                                                                |
| **`pcc_eng_20_089.6345_x1431904_06:09-10-11`**  | From a user perspective , redirects are generally not __`that bad`__ , assuming the user ends up on the correct destination page eventually .                             |
| **`pcc_eng_22_013.3529_x0199340_280:4-5-6`**    | It really was n't __`that bad`__ , but he did n't like it .                                                                                                               |
| **`pcc_eng_28_040.5919_x0640457_03:09-10-11`**  | Symposium headed to essence her " they 're not __`that bad`__ " when she missing man to pregnant woman tf wear rank spots in the improve .                                |
| **`apw_eng_20020529_1698_16:14-15-16`**         | if they would free all of them we can say that they 're not __`that bad`__ , '' said Singson .                                                                            |
| **`pcc_eng_01_061.3552_x0976216_54:09-10-11`**  | With that perspective , maybe 60 % is n't __`that bad`__ .                                                                                                                |


### 8. _that stupid_


|                                                 | `token_str`                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19960604_0156_15:11-12`**            | it 's been a long time since we 've been __`that stupid`__ .                                           |
| **`pcc_eng_05_035.9313_x0565818_08:6-7-8`**     | I said : " Is n't __`that stupid`__ , I need to be a voice , I do n't need to silence myself " .       |
| **`nyt_eng_20070410_0111_35:13-15-16`**         | `` The worst stuff is not going to happen because we ca n't be __`that stupid`__ , ''                  |
| **`pcc_eng_26_030.0492_x0469406_054:09-11-12`** | That was n't like me -- I was n't usually __`that stupid`__ .                                          |
| **`apw_eng_20090107_0567_25:3-5-6`**            | i could n't be __`that stupid`__ surely . ''                                                           |
| **`pcc_eng_02_005.8183_x0077944_73:11-12-13`**  | Maybe we could call it stupidity , but humans are not __`that stupid`__ .                              |
| **`pcc_eng_06_001.0886_x0001412_17:08-09-10`**  | " People in Washington are stupid but not __`that stupid`__ . "                                        |
| **`nyt_eng_19961016_0341_48:16-17-18`**         | asked to put the order in writing , Amarillas allegedly responded : `` I 'm not __`that stupid`__ . '' |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/that/`...

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


|                                      |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`    | `l2`          |   `f1` |    `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-------------------------------------|------:|--------:|--------:|-------:|----------:|:--------|:--------------|-------:|--------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] exactly~alike**         |   254 |    0.20 |    4.67 |   0.21 |  1,293.40 | exactly | alike         | 44,503 |   1,205 | 6,347,362 |      8.45 |      245.55 |        0.97 |            1.58 | 15.41 |   1.48 |    0.01 |   0.01 |           0.20 |            0.10 | direct      |
| **[_direct_] exactly~stellar**       |   170 |    0.21 |    4.57 |   0.22 |    873.03 | exactly | stellar       | 44,503 |     790 | 6,347,362 |      5.54 |      164.46 |        0.97 |            1.59 | 12.61 |   1.49 |    0.00 |   0.00 |           0.21 |            0.11 | direct      |
| **[_direct_] exactly~ideal**         |   418 |    0.12 |    3.93 |   0.13 |  1,678.75 | exactly | ideal         | 44,503 |   3,316 | 6,347,362 |     23.25 |      394.75 |        0.94 |            1.31 | 19.31 |   1.25 |    0.01 |   0.01 |           0.12 |            0.06 | direct      |
| **[_mirror_] exactly~right**         |    80 |    0.04 |    3.84 |   0.04 |    379.55 | exactly | right         |    869 |   2,038 |   583,470 |      3.04 |       76.96 |        0.96 |            1.48 |  8.60 |   1.42 |    0.09 |   0.09 |           0.09 |            0.06 | mirror      |
| **[_direct_] exactly~cheap**         |   691 |    0.10 |    3.73 |   0.10 |  2,523.80 | exactly | cheap         | 44,503 |   6,591 | 6,347,362 |     46.21 |      644.79 |        0.93 |            1.23 | 24.53 |   1.17 |    0.01 |   0.02 |           0.10 |            0.06 | direct      |
| **[_direct_] exactly~conducive**     |   208 |    0.10 |    3.48 |   0.11 |    764.40 | exactly | conducive     | 44,503 |   1,952 | 6,347,362 |     13.69 |      194.31 |        0.93 |            1.23 | 13.47 |   1.18 |    0.00 |   0.00 |           0.10 |            0.05 | direct      |
| **[_mirror_] exactly~sure**          |   148 |    0.02 |    3.43 |   0.02 |    580.91 | exactly | sure          |    869 |   5,978 |   583,470 |      8.90 |      139.10 |        0.94 |            1.31 | 11.43 |   1.22 |    0.16 |   0.17 |           0.16 |            0.09 | mirror      |
| **[_direct_] exactly~sure**          | 8,810 |    0.06 |    3.23 |   0.07 | 25,681.61 | exactly | sure          | 44,503 | 134,139 | 6,347,362 |    940.48 |    7,869.52 |        0.89 |            1.09 | 83.84 |   0.97 |    0.18 |   0.20 |           0.18 |            0.12 | direct      |
| **[_direct_] exactly~revolutionary** |   120 |    0.09 |    3.16 |   0.10 |    423.78 | exactly | revolutionary | 44,503 |   1,210 | 6,347,362 |      8.48 |      111.52 |        0.93 |            1.20 | 10.18 |   1.15 |    0.00 |   0.00 |           0.09 |            0.05 | direct      |
| **[_direct_] exactly~new**           | 1,372 |    0.06 |    3.05 |   0.06 |  3,718.41 | exactly | new           | 44,503 |  21,538 | 6,347,362 |    151.01 |    1,220.99 |        0.89 |            1.00 | 32.96 |   0.96 |    0.03 |   0.03 |           0.06 |            0.04 | direct      |


### 1. _exactly alike_


|                                                | `token_str`                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_020.3221_x0312596_028:5-6`**     | No two maps are __`exactly alike`__ .                                                                                                                                                                                                                          |
| **`pcc_eng_07_050.5710_x0801344_07:8-9`**      | We realize that no two brides are __`exactly alike`__ and want to help each showcase her personality & originality .                                                                                                                                           |
| **`pcc_eng_23_028.6217_x0445794_12:5-6`**      | No two homes are __`exactly alike`__ and for that reason no two homes should be marketed alike .                                                                                                                                                               |
| **`pcc_eng_03_092.4722_x1481139_28:1-7-8`**    | Nor are any two cornfields truly __`exactly alike`__ , despite Monsanto 's best efforts .                                                                                                                                                                      |
| **`pcc_eng_20_086.2909_x1378010_02:29-31-32`** | Given that still - life portraiture allows the painter or photographer to exert maximal design control , it is also worth noting that the naturalism of flowers -- no two __`exactly alike`__ -- injects a wild note into the most controlled studio setting . |
| **`pcc_eng_00_045.4322_x0718212_23:3-4-5`**    | They were not __`exactly alike`__ .                                                                                                                                                                                                                            |
| **`pcc_eng_28_039.2911_x0619326_69:5-6`**      | No two people are __`exactly alike`__ , and a person 's genes may impact how long it takes him or her to detox from Adderall .                                                                                                                                 |
| **`pcc_eng_05_012.2151_x0181840_012:18-19`**   | But what happens when , in a wold of people knocked down and stood up to be __`exactly alike`__ , a person wants to be different ?                                                                                                                             |


### 2. _exactly stellar_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_108.02261_x1734602_18:29-30-31`** | From reports saying they are the laziest generation , to the most entitled , to the least likely to succeed , the PR for the next generation is not __`exactly stellar`__ .                                                                                                                                     |
| **`pcc_eng_12_085.4601_x1364762_38:28-29-30`**  | Even so , Facebook 's record on user privacy -- given the Cambridge Analytica data scandal and the more recent bug involving users ' photos -- is n't __`exactly stellar`__ .                                                                                                                                   |
| **`pcc_eng_03_005.0577_x0065564_50:2-3-4`**     | But not __`exactly stellar`__ given the ostentatious nature of their menu and beer .                                                                                                                                                                                                                            |
| **`pcc_eng_15_095.5724_x1528632_060:12-13-14`** | It was a long day for them and the Browns are n't __`exactly stellar`__ in the passing game .                                                                                                                                                                                                                   |
| **`pcc_eng_24_105.6568_x1693270_09:3-4-5`**     | -- was n't __`exactly stellar`__ in her Hurricane Katrina performance ; and Schwarzenegger of California , who is in the midst of a bruising reelection campaign in the deep- blue sunshine state .                                                                                                             |
| **`pcc_eng_08_103.5536_x1660407_09:6-7-8`**     | First impressions of Idris are not __`exactly stellar`__ - her early eccentric behaviour tends to grate rather than amuse , and , while it 's undoubtedly a difficult role to play , the performance of guest star Suranne Jones veers slightly too far towards cartoonish caricature in these initial scenes . |
| **`pcc_eng_12_080.2784_x1280838_25:11-12-13`**  | But the GOP 's recent record on political realism is n't __`exactly stellar`__ .                                                                                                                                                                                                                                |
| **`pcc_eng_17_052.7290_x0835763_24:21-22-23`**  | A tough sell in previews , " Spring " benefited from enthusiastic reviews , building to become a steady if not __`exactly stellar`__ performer with a growing youth following .                                                                                                                                 |


### 3. _exactly ideal_


|                                                 | `token_str`                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_073.0021_x1164689_25:14-15-16`**  | Likewise , if you are going to be in debt ( which is not __`exactly ideal`__ ) , make sure you go for the low-cost , tax - deductible , long-term , fixed - rate kind .                                         |
| **`pcc_eng_10_052.6383_x0835188_045:1-2-3`**    | Not __`exactly ideal`__ for a film crew . "                                                                                                                                                                     |
| **`pcc_eng_27_036.7016_x0576917_23:16-17-18`**  | After all , despite what Allen Iverson thinks , practicing without your best player is n't __`exactly ideal`__ .                                                                                                |
| **`pcc_eng_18_009.5257_x0138021_027:10-11-12`** | Gregg will make $ 5.8 million in 2012 , not __`exactly ideal`__ for a guy with a WHIP of 1.642 last season and an ERA of 4.37 while picking up 22 saves .                                                       |
| **`pcc_eng_28_038.1309_x0600525_16:29-30-31`**  | " We showed up three days before the 2002 Olympics , and the dressing room was green and the crapper was in the middle of the room -- not __`exactly ideal`__ for Team Canada , " Hitchcock said with a smile . |
| **`pcc_eng_27_065.1722_x1037364_16:1-2-3`**     | Not __`exactly ideal`__ for Hard Knocks .                                                                                                                                                                       |
| **`pcc_eng_18_089.4398_x1432087_126:11-12-13`** | The typical colonial construction , it turned out , were n't __`exactly ideal`__ for Hawaiian heat .                                                                                                            |
| **`pcc_eng_18_006.5801_x0090409_7:25-26-27`**   | The newly - announced Civilization Beyond Earth will be arriving on Linux , although the port is being handled Aspyr Media , which is not __`exactly ideal`__ .                                                 |


### 4. _exactly right_


|                                                | `token_str`                                                                                                                                                                         |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_088.2698_x1411301_4:4-5`**       | The length is __`exactly right`__ and the cut generous enough not to be too tight below the waist .                                                                                 |
| **`pcc_eng_23_014.5524_x0218357_31:3-4`**      | You are __`exactly right`__ in your call for negotiation .                                                                                                                          |
| **`pcc_eng_25_008.3027_x0118393_10:23-24-25`** | We 've been known to build up what appears to be the perfect solution only to tear it down because it is not __`exactly right`__ .                                                  |
| **`pcc_eng_07_021.1081_x0325130_21:4-6-7`**    | The time will never be __`exactly right`__ .                                                                                                                                        |
| **`pcc_eng_12_037.3697_x0588291_03:3-4-5`**    | That 's not __`exactly right`__ , there 's another layer involving the Federal Aviation Administration ( FAA ) here , but regardless it was quite the surprise to a lot of people . |
| **`pcc_eng_14_049.3465_x0781202_07:12-13-14`** | Well , that 's not exactly wrong , but it 's not __`exactly right`__ either .                                                                                                       |
| **`pcc_eng_21_083.9587_x1340872_222:5-6`**     | RUSH : That 's __`exactly right`__ .                                                                                                                                                |
| **`pcc_eng_04_060.5718_x0962324_49:5-6`**      | This I think is __`exactly right`__ .                                                                                                                                               |


### 5. _exactly cheap_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_101.4229_x1624707_03:21-22-23`** | " The employer community has benefitted , but at a price for the cost of the review , which is not __`exactly cheap`__ if it is just over a dispute over the declination ... of a prescription , " said Zachary Sacks , managing partner at Culver City , California , law firm Sacks & Zolonz Under California workers comp reforms passed in 2012 , injured workers can request independent medical reviews to dispute treatment that was modified or denied under utilization reviews , which employers and insurers request . |
| **`pcc_eng_24_035.5437_x0558628_58:09-10-11`** | While not a scam , the program is not __`exactly cheap`__ to use .                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_03_087.9477_x1407923_03:45-46-47`** | The objective should 've probably been reducing the evaporation and designing a solution that does so , not comparing a cheap and slightly less cheap option ( i fully understand cost reduction is important , and gaskets require additional tooling , but Wash ai n't __`exactly cheap`__ either ) .                                                                                                                                                                                                                           |
| **`nyt_eng_20061023_0208_16:5-6-7`**           | the GateHouse offering is n't __`exactly cheap`__ , either .                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **`nyt_eng_20070218_0057_35:20-21-22`**        | at $ 650 for a small car , and $ 2,500 for semi-trucks and RVs , the kits are n't __`exactly cheap`__ .                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_13_034.7417_x0545543_10:09-10-11`** | However , they must have if you are not __`exactly cheap`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_03_085.8111_x1373290_53:7-8-9`**    | This makes sense as it 's not __`exactly cheap`__ , and its almost unapologetically unhealthy .                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_09_082.0474_x1311272_18:36-37-38`** | As the mayor himself acknowledges , the homes built around the periphery of Irvine 's Great Park will be priced only 20 percent lower than the city 's median - priced homes , which are n't __`exactly cheap`__ .                                                                                                                                                                                                                                                                                                                |


### 6. _exactly conducive_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19991125_0190_34:21-22-23`**         | i 'm sure he realizes alternating three point guards and shuttling other players in and out of the lineup is n't __`exactly conducive`__ to team continuity and chemistry .                                                                                                                                                                                                                               |
| **`pcc_eng_26_036.8341_x0579250_18:10-11-12`**  | The day was trying though as the weather was not __`exactly conducive`__ for home construction due to raining season in Kota Kinabalu .                                                                                                                                                                                                                                                                   |
| **`pcc_eng_20_009.0365_x0129691_17:66-67-68`**  | granted , not a whole lot gets done between noon and late afternoon - the arabs probably have an equivalent word for " siesta " - but seriously : no wonder they are stuck in the seventh century - a four to six hour workday in a land of near constant tribal and sectarian warfare , poor infrastructure and spotty water and electrical service is not __`exactly conducive`__ to productivity ..... |
| **`pcc_eng_07_056.4749_x0896609_054:13-14-15`** | But as delicious as such comfort foods may be , they are n't __`exactly conducive`__ to eating light .                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_29_035.8826_x0562973_25:54-55-56`**  | Most companies ' finance and legal departments still do n't have fixed guidelines for freelancers , so they might ask you to register as a vendor , adhere to a 3 - month payment cycle or in the current scenario , might even expect you to have a GST number as well - not __`exactly conducive`__ to creativity .                                                                                     |
| **`pcc_eng_06_100.1997_x1604563_65:09-10-11`**  | A massive invective -filled flamewar among coworkers is not __`exactly conducive`__ to a good working environment .                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_25_005.0585_x0066209_38:18-19-20`**  | The brutal weather certainly did n't cause the looting and chaos that followed -- but it was n't __`exactly conducive`__ to staying calm , either .                                                                                                                                                                                                                                                       |
| **`pcc_eng_07_057.2082_x0908386_62:5-6-7`**     | The cold weather was not __`exactly conducive`__ to hanging out .                                                                                                                                                                                                                                                                                                                                         |


### 7. _exactly sure_


|                                                 | `token_str`                                                                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_086.7336_x1387716_08:3-4-5`**     | We are n't __`exactly sure`__ yet , but we 're having fun with it !                                                                                                                                                                                        |
| **`pcc_eng_14_081.9647_x1308840_80:3-4-5`**     | I 'm not __`exactly sure`__ how the members of Pink Floyd ( especially Roger Waters ) , then young men in their twenties , were able to so fully comprehend Life , in all it 's madness , futility , pain , and ecstasy .                                  |
| **`pcc_eng_28_019.0610_x0291935_055:3-4-5`**    | I 'm not __`exactly sure`__ what 's going on because I tuned in in the middle of it , but it does n't matter , I 'm not moving from the sofa until this is over .                                                                                          |
| **`pcc_eng_03_031.1783_x0488682_064:10-11-12`** | Of course , we have handwriting that we 're not __`exactly sure`__ who it belongs to , because they 've never provided a signature .                                                                                                                       |
| **`pcc_eng_28_048.1493_x0762845_09:4-5-6`**     | " We are n't __`exactly sure`__ why populations have exploded in recent decades .                                                                                                                                                                          |
| **`pcc_eng_09_049.4458_x0783772_30:3-4-5`**     | I 'm not __`exactly sure`__ when it happened , because the scorpions had been in their burrow for months .                                                                                                                                                 |
| **`pcc_eng_04_106.2232_x1699859_43:3-4-5`**     | We 're not __`exactly sure`__ how long it will last nor if there will be any interactive elements , but expect references to both the original series and the recent revival , Twin Peaks : The Return .                                                   |
| **`pcc_eng_02_084.8517_x1355700_11:19-20-21`**  | I 've just been induced for a similar thing , they should put you on medication I 'm not __`exactly sure`__ how they are going to handle your situation because they where going to induce me there n then if I got worse but I was further on then you :/ |


### 8. _exactly revolutionary_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_048.3621_x0766084_102:1-2-3`**   | Not __`exactly revolutionary`__ in that regard , but it was very revolutionary in one aspect .                                                                                                                                                                                                                                                                                           |
| **`nyt_eng_19991024_0096_2:33-34-35`**         | in an interview , Herman defended the Clinton administration 's work on behalf of labor rights , but also acknowledged that its main labor proposal to the World Trade Organization is `` not __`exactly revolutionary`__ '' and warned that if the world 's trade ministers do n't do a better job recognizing worker rights , the world 's economies risk `` a race to the bottom . '' |
| **`pcc_eng_20_034.0984_x0535171_12:3-4-5`**    | It 's not __`exactly revolutionary`__ , but it 's super fun , and it will make going back to previous Borderlands with regular gravity kind of a bummer .                                                                                                                                                                                                                                |
| **`pcc_eng_24_072.7950_x1161322_04:6-7-8`**    | The Streetside Photos feature is n't __`exactly revolutionary`__ now that every man and his dog has used Street View , but by using people 's uploaded Flickr photos ( geotagged , naturally ) they 'll be in a higher-res and offer more colour and life than Google 's own Street View cars can snap .                                                                                 |
| **`pcc_eng_10_026.2572_x0408097_36:7-8-9`**    | The concept for this game is n't __`exactly revolutionary`__ , but is enjoyable .                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_23_081.0523_x1293490_14:7-8-9`**    | On its own , that 's not __`exactly revolutionary`__ -- nine - panel is regularly used to denote routine -- but Heisserer and artists Raul Allen and Patricia Martin distinguish themselves by how they incorporate phones into this layout .                                                                                                                                            |
| **`pcc_eng_28_073.6117_x1174457_39:4-5-6`**    | Personal attacks are n't __`exactly revolutionary`__ in the long history of hitting someone below the figurative belt , but this was taking it too far , no ?                                                                                                                                                                                                                            |
| **`pcc_eng_19_010.7761_x0157974_05:08-09-10`** | The notion of a luxury SUV is n't __`exactly revolutionary`__ in this day and age , but when the truck launched on June 17 , 1970 , it certainly was .                                                                                                                                                                                                                                   |


### 9. _exactly new_


|                                               | `token_str`                                                                                                                                                                                                                                                                                                                                         |
|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_004.1202_x0050213_2:35-36-37`** | There 's no way the Green Bay Packers can really replace Al Harris and Aaron Kampman in their defense , but they 're going to go about filling those roles with players who are n't __`exactly new`__ to the duty being thrust upon them .                                                                                                          |
| **`pcc_eng_15_091.2548_x1458930_08:4-5-6`**   | Helium shortages are n't __`exactly new`__ .                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_09_082.3113_x1315523_01:6-7-8`**   | RYU on Emek Refaim is not __`exactly new`__ , but it was new to me when I went there a few weeks ago .                                                                                                                                                                                                                                              |
| **`apw_eng_19980120_1480_71:12-13-14`**       | look where we went with public toilets , and they 're not __`exactly new`__ .                                                                                                                                                                                                                                                                       |
| **`apw_eng_20081215_0013_26:21-22-23`**       | the show 's ultimate message -- it 's what 's inside that counts , not the outer wrapper -- while not __`exactly new`__ , is a fine one .                                                                                                                                                                                                           |
| **`pcc_eng_16_078.8454_x1259903_16:6-7-8`**   | Solar roofing technology , while not __`exactly new`__ , is being installed with greater ease and efficiency than ever before .                                                                                                                                                                                                                     |
| **`pcc_eng_16_020.7744_x0320310_01:7-8-9`**   | Burning giant piles of drugs is n't __`exactly new`__ in the history of media relations , but we ca n't think of anything else quite on this scale : the Mexican government invited national and international press from the capital to Tijuana where , after a gun battle with drug traffickers , the Mexican army seized 134 tons of marijuana . |
| **`apw_eng_20020926_0050_8:6-7-8`**           | `` Some things they are not __`exactly new`__ and need verification .                                                                                                                                                                                                                                                                               |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_alike_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_stellar_80ex~49.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_ideal_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_right_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_cheap_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_conducive_80ex~50.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_sure_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_revolutionary_80ex~36.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/exactly/exactly_new_80ex~80.csv`

## *any*


|                            |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`    |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:---------------------------|------:|--------:|--------:|-------:|----------:|:-------|:--------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] any~happier** |   834 |    0.41 |    7.76 |   0.42 |  7,282.99 | any    | happier | 16,238 |  2,004 | 6,347,362 |      5.13 |      828.87 |        0.99 |            2.47 | 28.70 |   2.21 |    0.05 |   0.05 |           0.41 |            0.23 | direct      |
| **[_direct_] any~clearer** |   371 |    0.38 |    7.39 |   0.38 |  3,147.58 | any    | clearer | 16,238 |    972 | 6,347,362 |      2.49 |      368.51 |        0.99 |            2.39 | 19.13 |   2.17 |    0.02 |   0.02 |           0.38 |            0.20 | direct      |
| **[_mirror_] any~closer**  |    61 |    0.22 |    6.05 |   0.22 |    477.62 | any    | closer  |  1,095 |    278 |   583,470 |      0.52 |       60.48 |        0.99 |            2.20 |  7.74 |   2.07 |    0.06 |   0.06 |           0.22 |            0.14 | mirror      |
| **[_direct_] any~closer**  |   611 |    0.16 |    5.92 |   0.17 |  4,021.04 | any    | closer  | 16,238 |  3,686 | 6,347,362 |      9.43 |      601.57 |        0.98 |            1.91 | 24.34 |   1.81 |    0.04 |   0.04 |           0.16 |            0.10 | direct      |
| **[_direct_] any~worse**   | 1,762 |    0.14 |    5.85 |   0.15 | 11,229.25 | any    | worse   | 16,238 | 12,116 | 6,347,362 |     31.00 |    1,731.00 |        0.98 |            1.87 | 41.24 |   1.75 |    0.11 |   0.11 |           0.14 |            0.13 | direct      |
| **[_direct_] any~simpler** |   229 |    0.16 |    5.61 |   0.16 |  1,479.26 | any    | simpler | 16,238 |  1,446 | 6,347,362 |      3.70 |      225.30 |        0.98 |            1.87 | 14.89 |   1.79 |    0.01 |   0.01 |           0.16 |            0.08 | direct      |
| **[_direct_] any~easier**  | 1,625 |    0.12 |    5.61 |   0.13 |  9,854.27 | any    | easier  | 16,238 | 12,877 | 6,347,362 |     32.94 |    1,592.06 |        0.98 |            1.80 | 39.49 |   1.69 |    0.10 |   0.10 |           0.12 |            0.11 | direct      |
| **[_mirror_] any~better**  |   390 |    0.10 |    5.50 |   0.10 |  2,543.31 | any    | better  |  1,095 |  3,831 |   583,470 |      7.19 |      382.81 |        0.98 |            1.97 | 19.38 |   1.73 |    0.35 |   0.36 |           0.35 |            0.23 | mirror      |
| **[_direct_] any~younger** |   255 |    0.14 |    5.47 |   0.14 |  1,591.82 | any    | younger | 16,238 |  1,784 | 6,347,362 |      4.56 |      250.44 |        0.98 |            1.82 | 15.68 |   1.75 |    0.02 |   0.02 |           0.14 |            0.08 | direct      |
| **[_direct_] any~safer**   |   255 |    0.14 |    5.42 |   0.14 |  1,575.71 | any    | safer   | 16,238 |  1,838 | 6,347,362 |      4.70 |      250.30 |        0.98 |            1.81 | 15.67 |   1.73 |    0.02 |   0.02 |           0.14 |            0.08 | direct      |


### 1. _any happier_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_017.6884_x0269580_51:46-47-48`** | Jackson , Serkis , Cameron and Trumbull have all thrown their considerable weight behind the idea , but Hollywood remains in a state of flux ; traditionalists once decried the switch from film to digital , and blogs around the web suggest that they 're not __`any happier`__ about this new format , either . |
| **`pcc_eng_07_010.3970_x0152343_16:16-18-19`** | Dr. Freiman performed my breast augmentation surgery back in March 2013 , and I could n't be __`any happier`__ with my results .                                                                                                                                                                                    |
| **`pcc_eng_24_021.1817_x0325996_039:5-6-7`**   | The Scott administration is n't __`any happier`__ over Trump 's plans for the U.S. Environmental Protection Agency .                                                                                                                                                                                                |
| **`pcc_eng_18_083.8590_x1341768_2:09-11-12`**  | Results blew my mind away and I could n't be __`any happier`__ .                                                                                                                                                                                                                                                    |
| **`pcc_eng_06_073.4359_x1171713_26:3-5-6`**    | I could n't be __`any happier`__ . "                                                                                                                                                                                                                                                                                |
| **`pcc_eng_04_070.1124_x1116281_45:20-22-23`** | I can tell you with certainty that if you have no love for what you do , you wo n't be __`any happier`__ when you achieve higher levels of mastery .                                                                                                                                                                |
| **`pcc_eng_00_013.4145_x0200508_12:4-6-7`**    | " We could n't be __`any happier`__ .                                                                                                                                                                                                                                                                               |
| **`pcc_eng_val_3.06113_x44415_20:11-15-16`**   | We purchased our pup in September of 2014 and could not have possibly been __`any happier`__ with her or the breeder , John .                                                                                                                                                                                       |


### 2. _any clearer_


|                                                | `token_str`                                                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_095.3153_x1524455_08:06-09-10`** | The response from Sampras could not have been __`any clearer`__ as he aimed a serve directly at Agassi 's head .                                                                                                                                                                               |
| **`pcc_eng_20_063.1658_x1004390_09:09-10`**    | Could the threat to our national sovereignty be __`any clearer`__ ? "                                                                                                                                                                                                                          |
| **`pcc_eng_24_070.1379_x1118297_09:52-53-54`** | After Baker struggled a bit with command -- hitting three batters in a row at one point in the first inning -- but overall came through his latest outing fairly well in a 10 - 6 Mariners victory over the Angels on Tuesday , the skipper said the picture really is n't __`any clearer`__ . |
| **`pcc_eng_27_064.4807_x1026202_22:10-12-13`** | The message from California to the federal government could n't be __`any clearer`__ .                                                                                                                                                                                                         |
| **`pcc_eng_16_084.4175_x1350224_020:4-6-7`**   | Our cause could not be __`any clearer`__ .                                                                                                                                                                                                                                                     |
| **`pcc_eng_09_084.7064_x1354210_22:3-4-5`**    | Life is never __`any clearer`__ than that moment you let something completely hate -filled and juvenile slip out of your mouth and all you want to do is take it back .                                                                                                                        |
| **`pcc_eng_12_085.4958_x1365342_03:19-20-21`** | A lane was blocked off , and my path to the former CEO of Godfather 's Pizza was n't __`any clearer`__ .                                                                                                                                                                                       |
| **`pcc_eng_07_007.8115_x0110303_212:8-9`**     | QUESTION : Is the weekend picture getting __`any clearer`__ yet ?                                                                                                                                                                                                                              |


### 3. _any closer_


|                                                 | `token_str`                                                                                                                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_083.2629_x1329229_686:08-09-10`** | " Maybe so , but I 'm not __`any closer`__ to fulfilling my promise to Marc and I 've probably just given us one more man to die in the service of the cause ' . "                                                                                                          |
| **`pcc_eng_15_043.3976_x0685475_09:17-18-19`**  | Sanchez needed a command performance to try to close the gap but " Loretta Sanchez is n't __`any closer`__ to the Senate than she was an hour ago , " said Claremont Mc Kenna College political scientist Jack Pitney , summing up the debate .                             |
| **`pcc_eng_17_050.9874_x0807565_07:4-6-7`**     | Immigration reform may not be __`any closer`__ to the hearts of Puerto Ricans than of any other Americans , but the idea of having " different classes of people " and " not being a full citizen " might be .                                                              |
| **`nyt_eng_20070612_0185_3:6-8-9`**             | in reality , the ships never got __`any closer`__ to the South Pacific islands than San Francisco Bay .                                                                                                                                                                     |
| **`pcc_eng_10_088.8470_x1419911_074:4-5-6`**    | And I was n't __`any closer`__ to coming out . "                                                                                                                                                                                                                            |
| **`pcc_eng_27_003.6621_x0042728_008:23-25-26`** | Some scientists have designed elaborate computer models to determine how fingerprints form , but despite understanding how they grow , we are n't really __`any closer`__ to understanding the evolutionary reason why we have individualized ID badges on our fingertips . |
| **`pcc_eng_18_108.1442_x1735733_10:6-7`**       | But is it a solution __`any closer`__ ? ( sic ) "                                                                                                                                                                                                                           |
| **`pcc_eng_13_034.5754_x0542799_31:23-25-26`**  | Although his perspective is gaining more influence than ever as the Muslim Brotherhood increases its power in Egypt , this goal may not be __`any closer`__ to fruition than it was before .                                                                                |


### 4. _any worse_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                             |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_044.4389_x0702303_076:12-13-14`** | Though she may not be better than Dandridge she is certainly not __`any worse`__ .                                                                                                                                                                                                                      |
| **`pcc_eng_00_079.9330_x1276067_030:7-8`**      | I hate to make this situation __`any worse`__ for you than it already is . "                                                                                                                                                                                                                            |
| **`pcc_eng_29_090.5379_x1446204_530:14-15`**    | Will you please go talk to her and stop this before it gets __`any worse`__ ?                                                                                                                                                                                                                           |
| **`pcc_eng_09_088.4113_x1414432_12:3-5-6`**     | It 's not really __`any worse`__ than other kinds of records like you said , but we should recognize that there is a risk that 's greater than zero .                                                                                                                                                   |
| **`pcc_eng_14_031.3547_x0490535_16:19-22-23`**  | However lengthy and convoluted and foolish sounding the laws and the commandments may need been , they could not have been __`any worse`__ than the Code of Federal Rules , which appears to cover about the identical sort of trivialities .                                                           |
| **`pcc_eng_07_018.9342_x0290066_10:3-5-6`**     | Things could n't be __`any worse`__ for black bears here if their survival depended on Congress !                                                                                                                                                                                                       |
| **`pcc_eng_21_011.2130_x0164848_39:4-5-6`**     | Maybe it 's not __`any worse`__ than usual but somehow the dreadful shooting on the beach in Tunisia yesterday seems to underline the fragility of life at the end of a week which has seen Irish hearts blown open with grief after the tragic deaths of the young students in Berkeley , California . |
| **`pcc_eng_09_002.5048_x0024348_13:36-38-39`**  | The only visible optical flaw is lateral chromatic aberration , but this is pretty well inevitable for this type of lens , and while red / cyan fringing is visible in many circumstances it 's not really __`any worse`__ in than we'd expect .                                                        |


### 5. _any simpler_


|                                                | `token_str`                                                                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_008.7486_x0125083_3:4-5`**       | This doesnt receive __`any simpler`__ than in which !                                                                                                                                                 |
| **`pcc_eng_28_013.4622_x0201899_051:2-3-4`**   | but not __`any simpler`__ .                                                                                                                                                                           |
| **`pcc_eng_10_079.9487_x1276007_40:18-20-21`** | It is easy as breeze to make , delicious to the last drop and the ingredients could n't be __`any simpler`__ .                                                                                        |
| **`pcc_eng_02_083.9536_x1341196_29:31-33-34`** | Workflow simplified Built to support the DV family of codecs , as well as the Quick Time animation codec , while using the industry standard .mov wrapper , workflow could not be __`any simpler`__ . |
| **`nyt_eng_19961128_0003_5:23-25-26`**         | uncertainty remains about how this game will affect Robinson 's future , but for the 14 USC seniors , the predicament could not be __`any simpler`__ .                                                |
| **`pcc_eng_29_012.2594_x0181896_107:3-5-6`**   | It ca n't be __`any simpler`__ .                                                                                                                                                                      |
| **`pcc_eng_29_085.2439_x1360678_25:1-4-5`**    | Nor were things __`any simpler`__ when Cap was unaware that Stark and Iron Man were actually one and the same .                                                                                       |
| **`pcc_eng_06_070.0843_x1117789_4:07-09-10`**  | Converting them into an appetizer could not be __`any simpler`__ -- for this flavorful recipe , all you need is a toaster !                                                                           |


### 6. _any easier_


|                                                | `token_str`                                                                                                                                                                                                                                                           |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_060.4558_x0960900_16:3-5-6`**    | It could n't be __`any easier`__ . "                                                                                                                                                                                                                                  |
| **`pcc_eng_06_106.5420_x1707390_07:4-5-6`**    | But it is n't __`any easier`__ to watch in 2014 than it was before my first child was born .                                                                                                                                                                          |
| **`pcc_eng_18_010.8212_x0158874_04:15-17-18`** | Made with Great Day Farms Peeled and Ready-To-Eat Hard Boiled Eggs , convenience could n't be __`any easier`__ !                                                                                                                                                      |
| **`pcc_eng_17_103.7264_x1660561_17:5-6-7`**    | Synthetic decking materials are n't __`any easier`__ to bend than regular wooden boards -- unless you heat them up .                                                                                                                                                  |
| **`apw_eng_19970512_0757_19:10-11-12`**        | Ang said capturing `` the high '70s '' was n't __`any easier`__ than the buttoned-up Edwardian England of his acclaimed `` Sense and Sensibility . ''                                                                                                                 |
| **`pcc_eng_11_087.0602_x1393019_37:09-11-12`** | Democrats and some Republicans complained that it wo n't be __`any easier`__ under the GOP bill to reach a compromise on sustainable , long - term means to pay for programs by pushing off a decision until next year when the presidential campaign is heating up . |
| **`pcc_eng_27_005.2126_x0067590_3:5-7-8`**     | And it likely wo n't be __`any easier`__ for them to wait patiently now that the premium network has announced the date for the series ' return -- Sunday , Oct. 1 , at 10 pm ET .                                                                                    |
| **`pcc_eng_09_038.3448_x0604393_172:25-26`**   | " Ya do realize forcin ' me ta continue on as though nothin ' fuckin ' happened doesn ' help me deal with this __`any easier`__ ?                                                                                                                                     |


### 7. _any better_


|                                                  | `token_str`                                                                                                                                                                                                                               |
|:-------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_019.2809_x0295322_29:5-7-8`**      | In other words , nobody is __`any better`__ or any worse than anyone else !                                                                                                                                                               |
| **`pcc_eng_11_012.6581_x0188463_04:7-8-9`**      | " I mean , oil 's not __`any better`__ .                                                                                                                                                                                                  |
| **`pcc_eng_17_071.4009_x1137586_34:6-7-8`**      | What if the hours are n't __`any better`__ , or the money is n't enough ?                                                                                                                                                                 |
| **`pcc_eng_11_033.1756_x0520751_045:37-38`**     | So whether we call those societies socialist or give them some other label , we need to answer the underlying question : what makes us think that the next attempts to build socialist societies will do __`any better`__ than they did ? |
| **`pcc_eng_14_089.9066_x1437142_2822:21-22-23`** | And many will admire to see what a good memory you are furnished with , when perhaps your memory is not __`any better`__ than mine .                                                                                                      |
| **`pcc_eng_05_038.3564_x0604836_3:28-33-34`**    | However , at the entrance ceremony , he encounters a " princess " whom he thinks has had everything given to her on a silver platter , not that her thoughts are __`any better`__ .                                                       |
| **`pcc_eng_00_060.9966_x0969949_37:1-2-3`**      | Not __`any better`__ for me .                                                                                                                                                                                                             |
| **`pcc_eng_25_068.9808_x1101305_071:09-10`**     | After all , was the old magic circle __`any better`__ than the new one ?                                                                                                                                                                  |


### 8. _any younger_


|                                                | `token_str`                                                                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20080417_0533_35:09-11-12`**        | `` Let 's face it , we 're not getting __`any younger`__ , '' said retired accountant Sheldon Rothman of Queens , New York , who like McCain is 71 .                                                       |
| **`nyt_eng_19991001_0250_4:12-14-15`**         | `` It 's a big year for him , he 's not getting __`any younger`__ .                                                                                                                                        |
| **`nyt_eng_20050402_0206_25:17-19-20`**        | then again , in the field , Darin Erstad , Garret Anderson and Steve Finley are n't getting __`any younger`__ .                                                                                            |
| **`nyt_eng_20071213_0030_29:07-09-10`**        | but at 27 , I 'm not getting __`any younger`__ .                                                                                                                                                           |
| **`pcc_eng_05_006.1379_x0083559_05:32-36-37`** | If the label says that the whisky is 20 Years Old ( or Twenty Years Old ) then , although it may contain older whiskies , you can be certain that none of components are __`any younger`__ than 20 years . |
| **`apw_eng_20090323_0044_8:4-6-7`**            | `` I 'm not getting __`any younger`__ , '' the 60-year-old told The Associated Press in a recent telephone interview .                                                                                     |
| **`nyt_eng_20060112_0160_104:5-7-8`**          | you are 25 and not getting __`any younger`__ , its either now or never .                                                                                                                                   |
| **`nyt_eng_20050103_0014_41:09-11-12`**        | he will turn 64 next summer , is n't getting __`any younger`__ , and only Manning , not the Giants , has gotten any better .                                                                               |


### 9. _any safer_


|                                                | `token_str`                                                                                                                                                                                                                                       |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19990212_0464_33:7-8-9`**           | `` You know , it 's not __`any safer`__ where I am now , in Oak Lawn , '' Mrs. Goldsmith said .                                                                                                                                                   |
| **`pcc_eng_20_008.0515_x0113701_08:37-39-40`** | The senators said that while hospitals and emergency rooms are in urgent need of blood products , " healthy blood donors are turned away every day due to an antiquated policy and our blood supply is not necessarily __`any safer`__ for it . " |
| **`pcc_eng_24_028.4231_x0443452_08:19-20-21`** | Is n't it QUITE obvious that our situation is as serious as a heart attack , we are NOT __`any safer`__ and the ONLY option you have left is to lie ?                                                                                             |
| **`pcc_eng_16_059.8196_x0952398_12:19-20`**    | He said the military mission has reached the limits of its ability to help Afghans or make Americans __`any safer`__ , and he would close down the war immediately if he could .                                                                  |
| **`pcc_eng_18_094.6872_x1517412_04:10-11`**    | There is no evidence that mobile communication makes children __`any safer`__ .                                                                                                                                                                   |
| **`pcc_eng_17_052.5586_x0833004_039:3-4-5`**   | Walking is n't __`any safer`__ ( not least for the crickets ) .                                                                                                                                                                                   |
| **`pcc_eng_05_004.5437_x0057622_38:3-4-5`**    | It 's not __`any safer`__ than your cow meat or pig flesh .                                                                                                                                                                                       |
| **`pcc_eng_18_050.5876_x0802840_024:3-4`**     | Are they __`any safer`__ than they were that day one year ago ?                                                                                                                                                                                   |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_happier_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_clearer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_closer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_worse_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_simpler_80ex~51.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_easier_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_better_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_younger_80ex~66.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/any/any_safer_80ex~80.csv`

## *remotely*


|                                    |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`     | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-----------------------------------|------:|--------:|--------:|-------:|---------:|:---------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] remotely~comparable** |   125 |    0.05 |    5.05 |   0.05 |   759.06 | remotely | comparable |  6,161 |  2,401 | 6,347,362 |      2.33 |      122.67 |        0.98 |            1.76 | 10.97 |   1.73 |    0.02 |   0.02 |           0.05 |            0.04 | direct      |
| **[_direct_] remotely~close**      |   733 |    0.01 |    3.75 |   0.02 | 2,801.94 | remotely | close      |  6,161 | 46,485 | 6,347,362 |     45.12 |      687.88 |        0.94 |            1.27 | 25.41 |   1.21 |    0.11 |   0.12 |           0.11 |            0.06 | direct      |
| **[_direct_] remotely~similar**    |   169 |    0.01 |    3.35 |   0.02 |   620.70 | remotely | similar    |  6,161 | 11,088 | 6,347,362 |     10.76 |      158.24 |        0.94 |            1.21 | 12.17 |   1.20 |    0.03 |   0.03 |           0.03 |            0.02 | direct      |
| **[_mirror_] remotely~close**      |   226 |    0.04 |    3.34 |   0.05 |   805.38 | remotely | close      |  1,953 |  4,831 |   583,470 |     16.17 |      209.83 |        0.93 |            1.22 | 13.96 |   1.15 |    0.11 |   0.12 |           0.11 |            0.08 | mirror      |
| **[_mirror_] remotely~similar**    |    81 |    0.05 |    3.07 |   0.05 |   296.76 | remotely | similar    |  1,953 |  1,586 |   583,470 |      5.31 |       75.69 |        0.93 |            1.22 |  8.41 |   1.18 |    0.04 |   0.04 |           0.05 |            0.04 | mirror      |
| **[_direct_] remotely~interested** |   364 |    0.01 |    3.03 |   0.01 | 1,096.50 | remotely | interested |  6,161 | 34,543 | 6,347,362 |     33.53 |      330.47 |        0.91 |            1.06 | 17.32 |   1.04 |    0.05 |   0.06 |           0.05 |            0.03 | direct      |
| **[_direct_] remotely~related**    |   163 |    0.01 |    2.91 |   0.01 |   510.85 | remotely | related    |  6,161 | 14,260 | 6,347,362 |     13.84 |      149.16 |        0.92 |            1.09 | 11.68 |   1.07 |    0.02 |   0.03 |           0.02 |            0.02 | direct      |
| **[_direct_] remotely~funny**      |   141 |    0.01 |    2.58 |   0.01 |   391.23 | remotely | funny      |  6,161 | 14,992 | 6,347,362 |     14.55 |      126.45 |        0.90 |            1.00 | 10.65 |   0.99 |    0.02 |   0.02 |           0.02 |            0.01 | direct      |
| **[_direct_] remotely~true**       |   251 |    0.01 |    2.37 |   0.01 |   579.45 | remotely | true       |  6,161 | 34,967 | 6,347,362 |     33.94 |      217.06 |        0.86 |            0.89 | 13.70 |   0.87 |    0.04 |   0.04 |           0.04 |            0.02 | direct      |
| **[_direct_] remotely~qualified**  |    59 |    0.01 |    2.25 |   0.01 |   171.27 | remotely | qualified  |  6,161 |  5,810 | 6,347,362 |      5.64 |       53.36 |        0.90 |            1.03 |  6.95 |   1.02 |    0.01 |   0.01 |           0.01 |            0.01 | direct      |


### 1. _remotely comparable_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_060.8241_x0967067_3:11-12-13`**   | Yes , yes , I know , the cases are not __`remotely comparable`__ .                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_28_027.4330_x0426919_18:3-5-6`**     | There is nothing even __`remotely comparable`__ in American politics today .                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_21_063.6691_x1012800_072:1-2-3`**    | Nothing __`remotely comparable`__ to the post-World War II de-nazification of Germany has occurred ; only a handful of communists have been prosecuted .                                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_05_036.4412_x0574031_03:27-28-29`**  | Comparing space colonization to Manifest Destiny is n't apt , because while we possess immensely better tools than pioneers of the past , the challenges are n't __`remotely comparable`__ .                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_24_100.1865_x1604654_138:31-32-33`** | Slavery can appear , then , to even the most anti-utopian and anti-progressivist among us as evidence that no matter what problems exist in modern life , they are surely not __`remotely comparable`__ to the destructiveness and cruelty of the slave trade -- much as , following Adorno , we might be inclined to let " Auschwitz " serve a symbolic or synecdochal function beyond its literal ones : it is the special case , the low-water mark of man 's unbridled inhumanity to man . |
| **`pcc_eng_17_061.7779_x0981746_085:32-33`**    | My daughter will , perhaps , be a pest some- day , but I herewith - forever public - ask God to rot off my hands if I ever do anything __`remotely comparable`__ .                                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_01_032.9426_x0516326_1:22-24-25`**   | What is ironic is that with all the technology and what not that we are blessed with today , Supriya is n't even __`remotely comparable`__ to Silk , when it comes to pure sensuousness .                                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_12_039.3369_x0620049_138:7-8-9`**    | My grief is my own and not __`remotely comparable`__ to anyone else 's , so please do n't tell me how it is easy for me because it is n't .                                                                                                                                                                                                                                                                                                                                                    |


### 2. _remotely close_


|                                                | `token_str`                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_040.2916_x0635554_05:41-43-44`** | But Brian Encino of Baldwin , NY , does n't have an opinion one way or the other on whether or not the abuse happened as Dylan described it , or whether Allen is telling the truth when he says nothing even __`remotely close`__ to what she describes in her letter ever happened . |
| **`pcc_eng_06_024.5759_x0381662_09:5-6-7`**    | At the time , nothing __`remotely close`__ to The Tease had taken off in the little D .                                                                                                                                                                                                |
| **`pcc_eng_16_053.8488_x0855378_26:1-2-3`**    | Not __`remotely close`__ to prior bottles .                                                                                                                                                                                                                                            |
| **`pcc_eng_19_022.5521_x0348013_10:26-27`**    | Unrivaled craftsmanship and materials make our VIVOSUN grow tent the best choice for savvy shoppers note : please be aware that all grow tents even __`remotely close`__ to this price point may emit a few tiny pinholes of light along the seams .                                   |
| **`pcc_eng_19_106.1461_x1700201_21:4-5`**      | Do you live __`remotely close`__ to East Tennessee ?                                                                                                                                                                                                                                   |
| **`pcc_eng_29_041.9360_x0661231_37:3-4-5`**    | It was never __`remotely close`__ to what Ellsbury could have gotten .                                                                                                                                                                                                                 |
| **`pcc_eng_09_041.7494_x0659265_01:3-5-6`**    | Maelstrom , not even __`remotely close`__ to the pop scene .                                                                                                                                                                                                                           |
| **`pcc_eng_03_007.3879_x0103217_087:5-7-8`**   | What makes it " not even __`remotely close`__ to Optima in regards to quality or overall design " ?                                                                                                                                                                                    |


### 3. _remotely similar_


|                                                | `token_str`                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_002.5867_x0025675_37:6-7-8`**    | ( Ed. : They 're not __`remotely similar`__ .                                                                                                                                                                                                             |
| **`pcc_eng_22_080.9888_x1292788_18:15-17-18`** | The scene with the Doctor and Erimem cracking up is surprisingly believable , though nothing even __`remotely similar`__ has been seen before with Davison .                                                                                              |
| **`pcc_eng_02_098.9743_x1584144_37:18-19`**    | No government agencies , acting on their own or in combination , are going to create anything __`remotely similar`__ .                                                                                                                                    |
| **`pcc_eng_18_004.2143_x0052147_10:12-13-14`** | While all this is activity is going on for Bush , nothing __`remotely similar`__ is taking place on Mc Cain 's behalf .                                                                                                                                   |
| **`nyt_eng_19980629_0471_6:13-14`**            | in the short history of privatization in this country the only sale __`remotely similar`__ was that of Conrail , a collection of failing Northeast railroads phe government took over and subsequently sold in a 1987 stock offering for $ 1.65 billion . |
| **`pcc_eng_22_082.1540_x1311776_20:19-21-22`** | None of that mattered when I started working in the city , however , because the job was n't even __`remotely similar`__ to anything I 'd done in the business .                                                                                          |
| **`pcc_eng_09_085.8391_x1372556_39:6-7-8`**    | The circumstances of 2008 were not __`remotely similar`__ to those of 1930 , most notably because back then America was a massive global creditor and exporter , which got                                                                                |
| **`pcc_eng_20_080.0498_x1277185_64:3-4-5`**    | It 's not __`remotely similar`__ to Brady Anderson hitting 50 ( at age 32 ) but only cracking 20 two other times ( 24 and 21 ) .                                                                                                                          |


### 4. _remotely interested_


|                                                 | `token_str`                                                                                                                                                                             |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_075.3740_x1204142_052:33-35-36`** | I would say that we 're definitely the minority in our age group , because most of the over - 30 year olds that I know do not have Myspace and are not even __`remotely interested`__ . |
| **`pcc_eng_28_035.8485_x0563596_24:10-11-12`**  | Even if you make it clear that you are not __`remotely interested`__ in someone else 's opinions they will still make sure you hear all about them .                                    |
| **`pcc_eng_29_093.6681_x1496995_34:3-4-5`**     | I 'm not __`remotely interested`__ in cashing in on someone else 's fame .                                                                                                              |
| **`pcc_eng_12_081.2332_x1296276_52:7-8`**       | Of course , if you 're __`remotely interested`__ in learning traditional polo , then this is also a great and cheap way to start .                                                      |
| **`pcc_eng_18_037.3736_x0588488_10:21-22-23`**  | Without US assistance , Israel is quite strong enough to take on any combination of Arab armies , which are n't __`remotely interested`__ in such a conflict .                          |
| **`pcc_eng_09_006.6936_x0092244_16:21-22-23`**  | Chris Nichols tweeted that Bob Mc Kenzie believes the Avs would be looking at Thomas Chabot and the Sens are n't __`remotely interested`__ if that 's the case .                        |
| **`pcc_eng_22_009.8604_x0142831_14:30-31-32`**  | " The truth is , I think one of the big reasons I went to law school is that , by the time I finished college , I was not __`remotely interested`__ in having a job .                   |
| **`pcc_eng_27_051.7123_x0819619_09:28-29-30`**  | For all of the incredible things that my body was capable of , I loathed my size so much that I told my mother that I was not __`remotely interested`__ in the idea .                   |


### 5. _remotely related_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_075.3205_x1202092_23:42-44-45`** | This all seems pretty harmless , because that is the point of using social media , letting your friends know what you are up to , but there are people on these websites who are not your friends , who are not even __`remotely related`__ to you , and if they want , as long as they have access to any internet service such as Viasat Satellite Internet , they can pretty much see what you are posting about from wherever they are located unless you make those posts private . |
| **`pcc_eng_04_048.1583_x0762088_17:16-18-19`** | The love I dwell in now is so foreign to those notions , they are n't even __`remotely related`__ ; and yet we call it the same thing , love .                                                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_29_098.9114_x1582001_25:14-15-16`** | There 's a sense of isolation and barrenness from the footage , but nothing __`remotely related`__ to the human element , and nothing that holds a candle to the actual film taken on the voyage .                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_11_015.4407_x0233709_15:15-20-21`** | And yes , there will be new names introduced , though let 's hope none of them are even __`remotely related`__ to Jar Jar Binks .                                                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_29_103.5575_x1657335_071:12-13`**   | Despite being virtually unable to secure a job in any field __`remotely related`__ to any degree I 've earned , I 've managed to squeak by on meager tips from miserable food service jobs and hobble out some semblance of a life with the additional assistance of good friends , a patient partner , and great beer .                                                                                                                                                                 |
| **`pcc_eng_01_102.3412_x1637920_27:2-7-8`**    | " Nothing about this will be __`remotely related`__ to public housing .                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_03_002.3133_x0021241_07:15-16-17`** | Over time several movies have been released that have the same title that are n't __`remotely related`__ .                                                                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_04_092.8132_x1483266_01:25-26`**    | But unlike some of his past lies intended to sow the seeds of doubt among the Republican electorate about the reliability of anything even __`remotely related`__ to the Russia investigation ( gee , I wonder why a president whose party controls all levers of the federal government would need to do such a thing ? ) , this one was exposed fairly quickly and decisively .                                                                                                        |


### 6. _remotely funny_


|                                                | `token_str`                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_055.6848_x0883912_10:22-23-24`** | They 're good for so many things , from venting and sorting feelings and seeing the humor in situations that are not __`remotely funny`__ in the moment , to tracking where you 've been and of course for assessing what worked and what didn't . |
| **`pcc_eng_13_088.9619_x1421689_20:19-20-21`** | So , as a response , the balance of this column will be exclusively about things that are n't __`remotely funny`__ , so you can read it without worrying that your body temperature will increase even one degree of Kelvin .                      |
| **`pcc_eng_07_021.7718_x0336046_36:14-15-16`** | It 's common , its happened to people you know , and its not __`remotely funny`__ .                                                                                                                                                                |
| **`pcc_eng_20_007.1232_x0098645_19:20-22-23`** | In the last two months I 've read so many topics where FSUIPC was the culprit , it 's not even __`remotely funny`__ . ]                                                                                                                            |
| **`pcc_eng_14_088.5429_x1415038_07:18-22-23`** | Some of this sounds funny in writing , but thanks to witless execution and sloppy writing , none of it is __`remotely funny`__ on-screen .                                                                                                         |
| **`pcc_eng_22_002.4181_x0023050_35:13-14-15`** | The most telling aspect of Tosh 's joke is that it is not __`remotely funny`__ .                                                                                                                                                                   |
| **`pcc_eng_25_040.3526_x0637005_48:3-5-6`**    | It 's not even __`remotely funny`__ .                                                                                                                                                                                                              |
| **`pcc_eng_20_030.2939_x0473614_15:1-2-3`**    | Not __`remotely funny`__ .                                                                                                                                                                                                                         |


### 7. _remotely true_


|                                                 | `token_str`                                                                                                                                                                                                                          |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_005.8437_x0078827_05:15-17-18`**  | After years of fish sticks , I was surprised to learn that this is not even __`remotely true`__ .                                                                                                                                    |
| **`pcc_eng_01_091.1640_x1457940_04:27-28-29`**  | But the reality is that the idea that there is a massive terror threat from " white supremacists , " dwarfing the jihad threat , is n't __`remotely true`__ .                                                                        |
| **`pcc_eng_25_005.6198_x0075235_09:09-11-12`**  | Not surprisingly , this turns out to be not even __`remotely true`__ .                                                                                                                                                               |
| **`pcc_eng_20_006.3181_x0085665_11:10-11-12`**  | This is a lovely sentiment , but it 's not __`remotely true`__ .                                                                                                                                                                     |
| **`pcc_eng_08_107.4795_x1724114_012:02-17-18`** | That none of these claims ( with the arguable exception of the second ) is even __`remotely true`__ should n't be too surprising , because the " experts " who give voice to them typically define their expertise institutionally : |
| **`pcc_eng_26_008.0465_x0113678_033:13-15-16`** | In fact , not only is that inherently contradictory , it is not even __`remotely true`__ .                                                                                                                                           |
| **`pcc_eng_26_044.7963_x0708350_17:6-7-8`**     | A lot of it 's not __`remotely true`__ , so it 's kind of funny .                                                                                                                                                                    |
| **`pcc_eng_22_054.5010_x0864392_19:7-8-9`**     | In both cases , this is not __`remotely true`__ of the ' modern ' law enforced by corrupt and incompetent police and courts .                                                                                                        |


### 8. _remotely qualified_


|                                                 | `token_str`                                                                                                                                                                                                                                                                   |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_073.7395_x1176604_25:07-09-10`**  | The truth is , you are not even __`remotely qualified`__ to determine what caused any type of erosion anywhere on the planet , unless you yourself witness the erosion .                                                                                                      |
| **`pcc_eng_15_092.7806_x1483434_28:4-6-7`**     | If you are not even __`remotely qualified`__ for a position , do n't apply .                                                                                                                                                                                                  |
| **`nyt_eng_19990502_0236_3:09-10-11`**          | BUCHANAN-CHINA -LRB- Seattle -RRB- _ China is `` not __`remotely qualified`__ ''                                                                                                                                                                                              |
| **`pcc_eng_18_086.7234_x1388165_067:29-30-31`** | I do n't know how respectable this research is , because I do n't care enough to actually read it , and even if I did I am not __`remotely qualified`__ to judge something in this field .                                                                                    |
| **`pcc_eng_12_086.2209_x1377012_072:07-10-11`** | I 'm not a doctor , nor am I __`remotely qualified`__ to draw a conclusion .                                                                                                                                                                                                  |
| **`pcc_eng_03_037.9436_x0598305_32:27-28-29`**  | In the back of your mind , you constantly worry that every single parenting choice you 've made has been wrong , and that you are n't __`remotely qualified`__ for this business of raising young people .                                                                    |
| **`pcc_eng_26_084.3059_x1347179_184:3-4-5`**    | I 'm not __`remotely qualified`__ to hold an opinion , but find this debate fascinating , drawn as I am by the history those war-pocked shells evoke .                                                                                                                        |
| **`pcc_eng_19_043.1145_x0679902_08:08-09-10`**  | Bohr 's theory - which I am not __`remotely qualified`__ to explain , though I will try-suggested that : 1 ) two particles could become interrelated or entangled and 2 ) after which , they could interact even at astronomical distances , without any visible connection . |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_comparable_80ex~42.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_close_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_similar_80ex~60.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_interested_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_related_80ex~59.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_funny_80ex~49.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_true_80ex~66.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/remotely/remotely_qualified_80ex~19.csv`

## *ever*


|                             |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`   | `l2`    |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:----------------------------|------:|--------:|--------:|-------:|---------:|:-------|:--------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] ever~closer**  |   281 |    0.07 |    5.08 |   0.08 | 1,611.94 | ever   | closer  | 10,870 |  3,686 | 6,347,362 |      6.31 |      274.69 |        0.98 |            1.69 | 16.39 |   1.65 |    0.03 |   0.03 |           0.07 |            0.05 | direct      |
| **[_direct_] ever~mindful** |    53 |    0.07 |    4.15 |   0.07 |   290.04 | ever   | mindful | 10,870 |    784 | 6,347,362 |      1.34 |       51.66 |        0.97 |            1.63 |  7.10 |   1.60 |    0.00 |   0.00 |           0.07 |            0.04 | direct      |
| **[_direct_] ever~present** |   326 |    0.03 |    3.95 |   0.04 | 1,370.21 | ever   | present | 10,870 |  9,262 | 6,347,362 |     15.86 |      310.14 |        0.95 |            1.34 | 17.18 |   1.31 |    0.03 |   0.03 |           0.03 |            0.03 | direct      |
| **[_mirror_] ever~perfect** |   206 |    0.15 |    3.91 |   0.16 |   867.68 | ever   | perfect |  4,786 |  1,303 |   583,470 |     10.69 |      195.31 |        0.95 |            1.38 | 13.61 |   1.28 |    0.04 |   0.04 |           0.15 |            0.10 | mirror      |
| **[_direct_] ever~greater** |   187 |    0.03 |    3.40 |   0.03 |   687.30 | ever   | greater | 10,870 |  6,949 | 6,347,362 |     11.90 |      175.10 |        0.94 |            1.22 | 12.80 |   1.20 |    0.02 |   0.02 |           0.03 |            0.02 | direct      |
| **[_direct_] ever~deeper**  |    62 |    0.03 |    3.27 |   0.04 |   258.76 | ever   | deeper  | 10,870 |  1,768 | 6,347,362 |      3.03 |       58.97 |        0.95 |            1.33 |  7.49 |   1.31 |    0.01 |   0.01 |           0.03 |            0.02 | direct      |
| **[_mirror_] ever~certain** |   143 |    0.10 |    3.23 |   0.11 |   500.86 | ever   | certain |  4,786 |  1,276 |   583,470 |     10.47 |      132.53 |        0.93 |            1.20 | 11.08 |   1.14 |    0.03 |   0.03 |           0.10 |            0.07 | mirror      |
| **[_mirror_] ever~enough**  |   147 |    0.10 |    3.22 |   0.11 |   511.83 | ever   | enough  |  4,786 |  1,326 |   583,470 |     10.88 |      136.12 |        0.93 |            1.19 | 11.23 |   1.13 |    0.03 |   0.03 |           0.10 |            0.07 | mirror      |
| **[_direct_] ever~perfect** |   225 |    0.02 |    2.82 |   0.02 |   647.77 | ever   | perfect | 10,870 | 12,833 | 6,347,362 |     21.98 |      203.02 |        0.90 |            1.03 | 13.53 |   1.01 |    0.02 |   0.02 |           0.02 |            0.02 | direct      |
| **[_direct_] ever~larger**  |   139 |    0.02 |    2.75 |   0.02 |   414.99 | ever   | larger  | 10,870 |  7,453 | 6,347,362 |     12.76 |      126.24 |        0.91 |            1.05 | 10.71 |   1.04 |    0.01 |   0.01 |           0.02 |            0.01 | direct      |


### 1. _ever closer_


|                                              | `token_str`                                                                                                                                                                                                                                                                                            |
|:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_069.0099_x1099021_098:20-21`** | The same questions will be repeated like an incessant drum-beat , speeding up and getting louder as we move __`ever closer`__ to the great day when the summit opens :                                                                                                                                 |
| **`pcc_eng_22_059.6472_x0948100_01:5-6`**    | As the NHL gets __`ever closer`__ to the playoffs , Capitals prospect Axel Jonsson - Fjallby is already impressing in Djurgarden 's run .                                                                                                                                                              |
| **`pcc_eng_25_008.1729_x0116322_103:16-17`** | Fortunately , they were on the last stretch and the city beckoned as it drew __`ever closer`__ .                                                                                                                                                                                                       |
| **`pcc_eng_14_056.9725_x0904556_039:19-20`** | Of course , it is impossible to know what Assad must be thinking , as the rebels inch __`ever closer`__ to his palace doors .                                                                                                                                                                          |
| **`pcc_eng_29_093.9674_x1501857_85:5-6`**    | And they 're moving __`ever closer`__ .                                                                                                                                                                                                                                                                |
| **`pcc_eng_12_049.4649_x0783371_11:8-9`**    | And as her dangerous role thrusts her __`ever closer`__ to the carnage of Bunker Hill , headstrong Elizabeth must learn to follow her Lord instead of her own willful heart .                                                                                                                          |
| **`pcc_eng_11_097.0538_x1554909_04:11-12`**  | The agreed document reaffirmed " the process of creating an __`ever closer`__ union among the peoples of Europe , " but in effect recognized that " Treaty provisions also allow for the non-participation of one or more Member States in actions intended to further the objectives of the Union ... |
| **`pcc_eng_10_040.1813_x0633772_2:20-21`**   | The lineup for the UFC's March 16 stop in Montreal is continuing to fill up as the date grows __`ever closer`__ .                                                                                                                                                                                      |


### 2. _ever mindful_


|                                            | `token_str`                                                                                                                                                                          |
|:-------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_034.0866_x0534873_05:4-5`**  | I should be __`ever mindful`__ about how lucky ( blessed , if that is how you lean ) I am .                                                                                          |
| **`pcc_eng_00_085.9257_x1373057_02:1-2`**  | Ever mindful to immerse the world in evolutionary mythology , the Smithsonian.com 's " Dinosaur Tracking " column on Thanksgiving Day zoomed in on your turkey 's genealogy .        |
| **`pcc_eng_06_086.8657_x1388653_24:8-9`**  | One who is such , calmed and __`ever mindful`__ , He has no sorrows !                                                                                                                |
| **`pcc_eng_06_077.9864_x1244937_14:1-2`**  | Ever mindful that words hold the power to crush or to bless ; I choose to bless , but confess I sometimes slip .                                                                     |
| **`nyt_eng_19970905_0634_12:11-12`**       | F. Murray Abraham is the New York district attorney , __`ever mindful`__ of his law-and-order image , who insists on trying the youths as adults .                                   |
| **`pcc_eng_13_107.09376_x1728027_02:1-2`** | Ever mindful of providing its students with a reliable passport to employment , the School is confident that it can guide each student " to the first job , at the highest level " . |
| **`pcc_eng_28_060.7761_x0967028_19:1-2`**  | Ever mindful of proper etiquette , Miss Manners has social graces down to a fine art .                                                                                               |
| **`pcc_eng_08_081.7962_x1308374_105:3-4`** | I am __`ever mindful`__ of Alma 's words :                                                                                                                                           |


### 3. _ever present_


|                                                | `token_str`                                                                                                                                                                                                                |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_033.6729_x0528887_099:4-5`**     | The needs are __`ever present`__ and with an ever increasing population , government efforts will never be sufficient .                                                                                                    |
| **`pcc_eng_24_082.3121_x1315197_17:05-09-10`** | Do you hear me not though I am __`ever present`__ ?                                                                                                                                                                        |
| **`pcc_eng_24_092.6604_x1482525_43:19-20`**    | A Proplem that most Graffiti / Street artist face is the grey area of the law and the __`ever present`__ CCTV Cameras .                                                                                                    |
| **`pcc_eng_29_080.1995_x1279442_37:11-12`**    | Then there is our big bro Henry Framhein , the __`ever present`__ Henry , always there communicating between committees , providing his transport , picking up , dropping off and forever snapping photos of every event . |
| **`pcc_eng_00_071.2506_x1135582_6:26-27`**     | I left amazed by the different journeys students take to arrive at Penn and stunned by the reality so different from our own that 's __`ever present`__ only a few streets further west into Philadelphia .                |
| **`pcc_eng_01_084.3728_x1348177_07:7-8`**      | The sustained economic growth resulted in __`ever present`__ acute labour shortages which were filled by strong inflows of foreigners .                                                                                    |
| **`pcc_eng_09_093.0856_x1489754_031:26-27`**   | Why does he appear to be haunting the background of the shared DCU as if he were no more than one of his own , __`ever present`__ shadows ?                                                                                |
| **`pcc_eng_15_090.5973_x1448211_18:42-43`**    | * Impaired operators can be found on any waterway and in any type or size of vessel -- whether it 's a cabin cruiser off the New Jersey shore or a canoe on a Missouri back water , the risk is __`ever present`__ *       |


### 4. _ever perfect_


|                                                 | `token_str`                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_035.4607_x0557443_4:15-17-18`**   | I have been looking for this type of wedges for a while noow but nothing is __`ever perfect`__ for me D ; I hope they have this in my local target !                                                     |
| **`pcc_eng_12_050.7557_x0804212_29:5-6`**       | No peace process is __`ever perfect`__ , and these recent developments could jeopardise the Good Friday Agreement .                                                                                      |
| **`pcc_eng_06_025.9134_x0403208_054:1-3-4`**    | Nothing is __`ever perfect`__ defending Manziel given his improvisational abilities , but it was slightly surprising to see teams sit back and let the Ags dictate to them as much as they did .         |
| **`pcc_eng_22_057.2517_x0909124_26:1-3-4`**     | Nothing is __`ever perfect`__ or easy .                                                                                                                                                                  |
| **`pcc_eng_25_008.1610_x0116128_097:20-21-22`** | And yeah , the soft goods do n't hang as well as they should , but soft goods are hardly __`ever perfect`__ and I just hooked it to the bottom of my figure 's legs to spread it out and it looks fine . |
| **`pcc_eng_25_099.9849_x1601968_333:09-10-11`** | It was a delicate balance that she might not __`ever perfect`__ .                                                                                                                                        |
| **`pcc_eng_02_036.0254_x0566939_101:19-21-22`** | Many reasons for this are given ; one is that it 's helpful to keep in mind that nothing is __`ever perfect`__ .                                                                                         |
| **`pcc_eng_20_002.8566_x0029741_14:08-10-11`**  | I 'm not really pursuing perfection - nothing 's __`ever perfect`__ .                                                                                                                                    |


### 5. _ever greater_


|                                             | `token_str`                                                                                                                                                                                                                                                                      |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_013.7183_x0205526_10:19-20`** | Learning and helping each other is the best way for the industry to grow and to make an __`ever greater`__ positive impact for all artisans everywhere .                                                                                                                         |
| **`pcc_eng_21_076.5138_x1220299_05:7-8`**   | The need to pay attention is __`ever greater`__ , no matter which leaders pretend otherwise , and the possibilities of making a difference have increased as well .                                                                                                              |
| **`pcc_eng_07_037.1831_x0585037_05:32-33`** | And the treasures of grace which God had granted him so lavishly and unceasingly he passed on through his ministry , serving the men and women who came to him in __`ever greater`__ numbers , and bringing to birth an immense host of spiritual sons and daughters .           |
| **`pcc_eng_09_064.1732_x1022028_10:38-39`** | While television spots and print ads were once far and away the most central components to a brand 's advertising efforts in the United States , times are changing quickly , as digital communication takes on an __`ever greater`__ role .                                     |
| **`pcc_eng_06_001.4485_x0007249_13:8-9`**   | Be inspired and develop motivation to gain __`ever greater`__ heights within your career                                                                                                                                                                                         |
| **`pcc_eng_13_046.0741_x0728792_06:41-42`** | In his book The Victory Lab : the Secret Science of Winning Campaigns ( Crown Publishing ) he describes how the hitherto unimaginable quantities of data assembled by US political parties have enabled them to " micro-target " voters with __`ever greater`__ sophistication . |
| **`pcc_eng_13_020.0719_x0308224_13:29-30`** | This is no bad description of our aspirations at the Hall , as well as fulfilling the ultimate purpose of this Jesuit foundation : to work for the __`ever greater`__ glory of God .                                                                                             |
| **`pcc_eng_21_055.8090_x0886071_56:11-12`** | With populism on the march across Europe , and with __`ever greater`__ concern about the democratic deficit , the trade - off between market access and democracy cannot be ignored .                                                                                            |


### 6. _ever deeper_


|                                             | `token_str`                                                                                                                                                                                                                                                                                              |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_029.8068_x0466362_10:19-20`** | His desperate search for his wife will cost him everything he thought he believed in as he digs __`ever deeper`__ into the ugly reality behind the facade of his world 's peace and security , and finds himself at last .                                                                               |
| **`pcc_eng_23_054.4544_x0863938_14:31-32`** | Each has found themselves caught up in the fight for power as they come into conflict with each other and so have taken up with the guilds , entrenching themselves __`ever deeper`__ into the war for Ravnica 's secrets .                                                                              |
| **`pcc_eng_04_097.5103_x1559157_17:20-21`** | People throw out words like " compromise " from their respective corners , demonizing each other while we dig __`ever deeper`__ trenches of defensive self-justification , focused entirely on what makes us different instead of what makes us the same - our human dignity and the feelings we share . |
| **`pcc_eng_04_106.4061_x1702797_27:12-13`** | The roaring waterfalls and the tearing water masses have cut themselves __`ever deeper`__ into the ravine for thousands of years and the rocks now stand so narrow and high that the sky can only be seen as a small strip .                                                                             |
| **`pcc_eng_06_041.5373_x0655549_72:25-26`** | It centres on the love that selflessly and unconditionally gives and gives again , the love that longs to draw us ever closer and __`ever deeper`__ into that relationship of divine love .                                                                                                              |
| **`pcc_eng_23_050.5838_x0800893_65:1-2`**   | Ever deeper into Rockbottum CC Philosophy .                                                                                                                                                                                                                                                              |
| **`pcc_eng_24_091.2520_x1459557_13:22-23`** | The country was illegally invaded by Ethiopian troops , backed by the US military , last December and has been descending __`ever deeper`__ into catastrophe since .                                                                                                                                     |
| **`pcc_eng_22_091.9483_x1469704_05:17-18`** | They include boat builders and representatives of the flourishing offshore drilling industry , which is going __`ever deeper`__ in the quest for oil and natural gas and increasingly requires skilled supply boats and people to staff them .                                                           |


### 7. _ever certain_


|                                                | `token_str`                                                                                                                                               |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_063.4103_x1009071_14:13-15-16`** | At first , Abigail Salmon clings on to the thought that " nothing is __`ever certain`__ " .                                                               |
| **`pcc_eng_13_008.6655_x0123750_36:2-4-5`**    | While nothing is __`ever certain`__ in the crazy world of college football , everybody else definitely has an uphill climb to get past the Crimson Tide . |
| **`pcc_eng_24_078.9703_x1261259_11:07-09-10`** | But Ferguson knows from experience that nothing is __`ever certain`__ in football .                                                                       |
| **`pcc_eng_27_058.7436_x0933359_11:1-3-4`**    | Nothing is __`ever certain`__ of course but , the more information the better if needing to profile an account reasonably quickly                         |
| **`pcc_eng_14_044.1696_x0697560_045:2-4-5`**   | But nothing is __`ever certain`__ in sports , it 's why we watch them .                                                                                   |
| **`pcc_eng_26_037.5848_x0591549_09:23-25-26`** | About a month ago , Smaldone and Ward were tipped off that a cover shot was a possibility with the caveat that nothing is __`ever certain`__ .            |
| **`nyt_eng_19981024_0272_9:2-6-7`**            | but nothing about Tyson is __`ever certain`__ .                                                                                                           |
| **`pcc_eng_28_047.0273_x0744787_44:1-3-4`**    | Nothing is __`ever certain`__ in Sitka .                                                                                                                  |


### 8. _ever enough_


|                                                | `token_str`                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_003.7190_x0043610_11:1-6-7`**    | Nothing in this world is __`ever enough`__ , nothing satisfies .                                                                                                                                                               |
| **`pcc_eng_15_010.7531_x0157460_05:3-5-6`**    | However , nothing is __`ever enough`__ when it comes to competing in a competitive industry .                                                                                                                                  |
| **`pcc_eng_29_035.0390_x0549301_33:10-11-12`** | Over - the-counter products , traps and gadgets are rarely __`ever enough`__ to guarantee the successful extermination of an established pest colony .                                                                         |
| **`pcc_eng_11_065.2271_x1039404_05:32-34-35`** | i was worried about you but you never cared about me none you took my money and i knew that you , you could kill someone i gave you everything but nothing was __`ever enough`__ you were always jealous over such crazy stuff |
| **`pcc_eng_24_106.1874_x1701892_08:4-5-6`**    | The income is hardly __`ever enough`__ to make a significant impact on her household expenses .                                                                                                                                |
| **`pcc_eng_06_103.8732_x1664194_10:08-09-10`** | Another problem is that one trial is hardly __`ever enough`__ .                                                                                                                                                                |
| **`pcc_eng_27_008.3888_x0118995_08:29-31-32`** | As the interviewer points out , Mc Donald 's has bent over backwards to accommodate the food faddists in recent years , but , for people like Banzhaf nothing is __`ever enough`__ .                                           |
| **`pcc_eng_17_009.5380_x0138096_58:3-5-6`**    | Why was n't that __`ever enough`__ ?                                                                                                                                                                                           |


### 9. _ever larger_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                   |
|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_049.4778_x0783784_14:18-19`**  | But Scott has argued that Florida cannot afford to expand a program that has been eating an __`ever larger`__ share of the state budget .                                                                                                                                                                                                                     |
| **`pcc_eng_25_009.3585_x0135341_10:39-40`**  | The driving force behind the need for rapid reporting of microbiological test results is the clinical relevance in a time of financial austerity , a time when cost and health care effectiveness to the patient and diagnostician looms __`ever larger`__ , and where after - the -fact results at high expense are coming under severe scrutiny worldwide . |
| **`pcc_eng_22_053.9827_x0855976_50:11-12`**  | With climate change and the global threat to biodiversity looming __`ever larger`__ , that hope must become reality .                                                                                                                                                                                                                                         |
| **`pcc_eng_23_068.8145_x1095512_11:7-8`**    | Since then her enemies list grows __`ever larger`__ as she learns to identify the alien plants among us .                                                                                                                                                                                                                                                     |
| **`pcc_eng_20_048.9382_x0774396_51:13-14`**  | But we can see the mountains of debt and paper money growing __`ever larger`__ , posing greater and greater risks to the system .                                                                                                                                                                                                                             |
| **`pcc_eng_25_083.5019_x1335281_002:7-8`**   | But it is being read in __`ever larger`__ numbers , partly thanks to digital tools that make it easier to grasp , and growing interest from women - who see no reason why men should have it to themselves .                                                                                                                                                  |
| **`pcc_eng_05_033.0142_x0518595_225:7-8`**   | I felt like I was growing __`ever larger`__ with collected insulation and that the rats were getting ever closer .                                                                                                                                                                                                                                            |
| **`pcc_eng_04_019.3843_x0296754_096:11-12`** | After death we expand into the infinite spaces , growing __`ever larger`__ .                                                                                                                                                                                                                                                                                  |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_closer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_mindful_80ex~52.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_present_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_perfect_80ex~65.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_greater_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_deeper_80ex~62.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_certain_80ex~45.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_enough_80ex~51.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/ever/ever_larger_80ex~80.csv`

## *yet*


|                               |    `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:------------------------------|-------:|--------:|--------:|-------:|----------:|:-------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] yet~final**      |    640 |    0.52 |    6.58 |   0.53 |  4,443.69 | yet    | final      | 53,881 |  1,213 | 6,347,362 |     10.30 |      629.70 |        0.98 |            2.12 | 24.89 |   1.79 |    0.01 |   0.01 |           0.52 |            0.27 | direct      |
| **[_direct_] yet~official**   |    352 |    0.37 |    5.63 |   0.38 |  2,141.31 | yet    | official   | 53,881 |    924 | 6,347,362 |      7.84 |      344.16 |        0.98 |            1.86 | 18.34 |   1.65 |    0.01 |   0.01 |           0.37 |            0.19 | direct      |
| **[_direct_] yet~ready**      |  7,505 |    0.25 |    5.21 |   0.25 | 39,487.38 | yet    | ready      | 53,881 | 29,583 | 6,347,362 |    251.12 |    7,253.88 |        0.97 |            1.66 | 83.73 |   1.48 |    0.14 |   0.14 |           0.25 |            0.19 | direct      |
| **[_direct_] yet~complete**   |  2,175 |    0.25 |    5.15 |   0.26 | 11,318.19 | yet    | complete   | 53,881 |  8,415 | 6,347,362 |     71.43 |    2,103.57 |        0.97 |            1.63 | 45.11 |   1.48 |    0.04 |   0.04 |           0.25 |            0.14 | direct      |
| **[_direct_] yet~ripe**       |    381 |    0.25 |    4.90 |   0.26 |  1,982.82 | yet    | ripe       | 53,881 |  1,453 | 6,347,362 |     12.33 |      368.67 |        0.97 |            1.62 | 18.89 |   1.49 |    0.01 |   0.01 |           0.25 |            0.13 | direct      |
| **[_direct_] yet~over**       |    162 |    0.26 |    4.65 |   0.26 |    845.32 | yet    | over       | 53,881 |    613 | 6,347,362 |      5.20 |      156.80 |        0.97 |            1.62 | 12.32 |   1.49 |    0.00 |   0.00 |           0.26 |            0.13 | direct      |
| **[_direct_] yet~public**     |    467 |    0.17 |    4.23 |   0.18 |  2,025.17 | yet    | public     | 53,881 |  2,656 | 6,347,362 |     22.55 |      444.45 |        0.95 |            1.40 | 20.57 |   1.32 |    0.01 |   0.01 |           0.17 |            0.09 | direct      |
| **[_direct_] yet~eligible**   |    448 |    0.16 |    4.17 |   0.17 |  1,916.40 | yet    | eligible   | 53,881 |  2,620 | 6,347,362 |     22.24 |      425.76 |        0.95 |            1.39 | 20.12 |   1.30 |    0.01 |   0.01 |           0.16 |            0.09 | direct      |
| **[_direct_] yet~clear**      | 10,409 |    0.12 |    3.96 |   0.12 | 39,438.80 | yet    | clear      | 53,881 | 84,227 | 6,347,362 |    714.98 |    9,694.02 |        0.93 |            1.30 | 95.02 |   1.16 |    0.18 |   0.19 |           0.18 |            0.15 | direct      |
| **[_direct_] yet~conclusive** |    127 |    0.15 |    3.69 |   0.16 |    528.59 | yet    | conclusive | 53,881 |    783 | 6,347,362 |      6.65 |      120.35 |        0.95 |            1.36 | 10.68 |   1.28 |    0.00 |   0.00 |           0.15 |            0.08 | direct      |


### 1. _yet final_


|                                                 | `token_str`                                                                                                                                                                                                                                                 |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19960711_0735_28:7-8-9`**            | but details of the plan are not __`yet final`__ , and Hondros added , `` we will be emphasizing the Adviser funds with additional educational support '' and the like aimed at investment counselors and planners .                                         |
| **`pcc_eng_09_038.7391_x0610772_029:20-21-22`** | A planned sale to Millersville - based Aurora Health Management , which is now operating the centers , is not __`yet final`__ .                                                                                                                             |
| **`pcc_eng_07_020.3007_x0312171_01:22-23-24`**  | According to local news outlet Portal do Bitcoin , Walltime won a preliminary injunction , meaning the court 's decision is n't __`yet final`__ but nevertheless lets the exchange use the funds on its account to keep on serving clients in the interim . |
| **`pcc_eng_14_030.8423_x0482218_05:18-19-20`**  | According to a person close to the deal who was unauthorized to speak publicly , negotiations are not __`yet final`__ .                                                                                                                                     |
| **`pcc_eng_25_001.5067_x0008307_12:12-13-14`**  | The first instance judgment of the Tribunal de Grande Instance is not __`yet final`__ and may be appealed .                                                                                                                                                 |
| **`pcc_eng_25_002.9303_x0031435_38:16-17-18`**  | A Microsoft spokesperson declined to comment , noting that the language of license agreements is not __`yet final`__ .                                                                                                                                      |
| **`pcc_eng_16_087.0098_x1392213_13:19-20-21`**  | KOMO News 4 in Seattle even noted that there were more votes to be counted and results are not __`yet final`__ .                                                                                                                                            |
| **`nyt_eng_20070311_0061_3:13-14-15`**          | he asked that he not be named , because the deal was not __`yet final`__ .                                                                                                                                                                                  |


### 2. _yet official_


|                                                | `token_str`                                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_086.7684_x1388353_08:6-7-8`**    | Although the reorganization plan is not __`yet official`__ , it involves multiple divisions , one of which is the media solutions center .                                                                                                                                                 |
| **`pcc_eng_17_105.0798_x1682483_12:4-5-6`**    | The charges are not __`yet official`__ , as many details of the case have yet to be resolved .                                                                                                                                                                                             |
| **`pcc_eng_12_080.2582_x1280531_06:16-17-18`** | Despite polishing off approximately $ 423.5 million in future salaries -- Teixeira 's deal is not __`yet official`__ because the first baseman must first pass a physical -- the Yankees have not been able to come to terms with Pettitte , their first choice to complete the rotation . |
| **`pcc_eng_08_070.0918_x1118766_3:30-31-32`**  | Liver Kick.com has spoken with Walker over the past few weeks and learned that he was having discussions with Glory about fighting for them , but that it was not __`yet official`__ .                                                                                                     |
| **`nyt_eng_19990124_0225_10:16-17-18`**        | it is a celebration of a landmark career , and though Elway 's retirement is not __`yet official`__ , it is fitting that he is being celebrated on pro football 's grandest stage , the Super Bowl , which is only proper given the lifelong stage presence of Sunday 's guest of honor .  |
| **`pcc_eng_13_088.2373_x1409889_07:25-26-27`** | Marquardt vs. Maia has been reported for Aug. 29 in Portland , Ore. , at UFC 102 , although Marquardt noted the fight is not __`yet official`__ and contracts have n't been signed .                                                                                                       |
| **`pcc_eng_26_032.6551_x0511647_09:38-39-40`** | The 2014 tyre supplier is supposed to offer up details of next year 's tyre specification to the teams by October 1 and Hembery said his company intends to stick to that even if a deal is not __`yet official`__ .                                                                       |
| **`pcc_eng_23_008.9223_x0127868_08:2-3-4`**    | Although not __`yet official`__ until January 6th when the Congress formally declares the vote in Trump 's favor , today 's milestone guarantees his seat in the Oval Office .                                                                                                             |


### 3. _yet ready_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_030.6667_x0480192_181:17-18-19`** | As Jean Pisani - Ferry wrote recently , a large part of the developing world is not __`yet ready`__ for independent floating of their currencies , because of incomplete financial liberalization and anxieties about uncontrolled adjustment .                                            |
| **`pcc_eng_03_086.4607_x1383907_5:43-44-45`**   | But , the new European Union member states have to apply these common rules and regulations in order for them to accede to EMU , which could produce both positive and negative effects , especially given that most of their economies are not __`yet ready`__ for this king of changes . |
| **`pcc_eng_08_042.9167_x0678333_055:18-19-20`** | He could see that this was not going to end for his people , but he was not __`yet ready`__ to give up .                                                                                                                                                                                   |
| **`pcc_eng_18_030.6426_x0479774_02:11-12-13`**  | Saudi arch-rival and OPEC member Iran said the country was not __`yet ready`__ for an output pact , but several OPEC sources said the atmosphere inside the group had improved and a compromise was possible .                                                                             |
| **`apw_eng_20030929_0050_3:6-7-8`**             | but he said Russia is not __`yet ready`__ to make a decision .                                                                                                                                                                                                                             |
| **`pcc_eng_15_098.4233_x1574577_04:1-2-3`**     | Not __`yet ready`__ to finish her studies she starts at the University of Rotterdam and receives her Master of History and Arts , with honours in 2000 .                                                                                                                                   |
| **`pcc_eng_15_093.6022_x1496853_07:3-4-5`**     | Radiance is not __`yet ready`__ .                                                                                                                                                                                                                                                          |
| **`nyt_eng_20071219_0139_18:20-21-22`**         | one compelling argument for keeping more troops in Germany longer than previously planned is that their new housing was not __`yet ready`__ at bases in the United States .                                                                                                                |


### 4. _yet complete_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_107.03316_x1719995_13:08-09-10`** | The restoration of Inwood Hill Park is not __`yet complete`__ but we have achieved the immediate goal of enhancing the habitat for native birds , butterflies and insects .                                                                                                                                                                                |
| **`pcc_eng_04_072.7562_x1158913_15:17-18-19`**  | It has taken another two years to finalize the technical rules , and even those are n't __`yet complete`__ ; the key specifications for the geolocation database still must be drafted , and every commissioner asked the FCC staff to do this quickly .                                                                                                   |
| **`pcc_eng_23_081.2470_x1296646_24:10-11-12`**  | CWC 's full report on the NJCAA violations is not __`yet complete`__ , but Wood predicted official findings will be " anticlimactic . "                                                                                                                                                                                                                    |
| **`pcc_eng_04_076.2347_x1215062_13:5-6-7`**     | With the bridge study not __`yet complete`__ , it is impossible to tell exactly how much the work will cost , but estimates range in the millions of dollars for a renovation , which could add up to 20 years of life to the bridge , and tens of millions for a total replacement , which would presumably last 80 to 100 years , Jones and Bodge said . |
| **`pcc_eng_27_027.7523_x0432167_06:5-6-7`**     | Although that process is not __`yet complete`__ , and will continue for up to three more weeks , IMO is in a position to confirm that the November ratifications did not trigger the convention 's entry into force .                                                                                                                                      |
| **`pcc_eng_21_079.0459_x1261209_06:08-09-10`**  | World economies were able to recover but not __`yet complete`__ .                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_18_041.2399_x0651118_03:13-14-15`**  | However , the report which was originally due some weeks ago is not __`yet complete`__ .                                                                                                                                                                                                                                                                   |
| **`pcc_eng_24_029.3857_x0459037_06:18-19-20`**  | Poof asked me to delay posting this video because some groundwork for the new financial system was not __`yet complete`__ , which is why its being released 6 weeks after the fact .                                                                                                                                                                       |


### 5. _yet ripe_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                        |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_048.9065_x0773207_21:28-29-30`**  | " You find them even having trouble giving birth because it 's like you have gone to the forest and you have plucked a fruit that is not __`yet ripe`__ , " she continued .                                                                                                                                                                                                                        |
| **`pcc_eng_14_009.4136_x0135794_44:12-13-14`**  | We are at a stage in the ministry when we are not __`yet ripe`__ to make decisions on funding , because things could be changed by the German committee . "                                                                                                                                                                                                                                        |
| **`pcc_eng_08_048.4992_x0768921_03:23-24-25`**  | It was drafted by Gopalaswami Ayyangar , Minister without portfolio in the first Union Cabinet of Nehru who felt that JK was not __`yet ripe`__ for integration .                                                                                                                                                                                                                                  |
| **`pcc_eng_13_036.7188_x0577446_34:13-14-15`**  | One might speculate that Pope Paul had decided that the time was not __`yet ripe`__ for establishing a collegial body to help the pope govern the universal Church .                                                                                                                                                                                                                               |
| **`nyt_eng_20070708_0111_34:21-22-23`**         | the Rhode Island Supreme Court ducked the issue in a lead paint case last year , saying that it was not __`yet ripe`__ to be decided but noting that it `` implicates sensitive questions regarding the separation of powers in this state and the proper role of the constitutional office of the attorney general in relation to the exclusively legislative powers of the general assembly . '' |
| **`pcc_eng_19_074.0753_x1180477_684:47-48-49`** | In vain would the baronet struggle in the unsound arguments in which Monsieur de Ramiere entangled him ; with admirable force he would argue that a greater extension of the suffrage would infallibly lead to the excesses of ' 93 , and that the nation was not __`yet ripe`__ for liberty , which is not the same as license .                                                                  |
| **`pcc_eng_15_019.4529_x0298077_50:6-7-8`**     | Evidently , the story is not __`yet ripe`__ ; the antique media believes it can wait until , say , November 7th or later to pick up the threads and examine the incident in detail .                                                                                                                                                                                                               |
| **`pcc_eng_14_030.1198_x0470573_118:18-19-20`** | To desire rulership at this time would have been a serious aveirah , as the time was not __`yet ripe`__ for Klal Yisroel to have a king or independent rulership .                                                                                                                                                                                                                                 |


### 6. _yet over_


|                                         | `token_str`                                                                                                                                                                                                                                                                                                    |
|:----------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20050218_0225_1:39-40-41`**  | WASHINGTON - More than 1,000 men and women across the nation came forward last year to say that they had been sexually abused by a Catholic priest or deacon , indicating that the clergy sexual abuse crisis is not __`yet over`__ , according to a top official of the US bishops conference .               |
| **`apw_eng_20080408_0824_1:27-28-29`**  | the National Association of Realtors says pending U.S. home sales fell to the lowest reading on record in February , signaling the housing market distress is not __`yet over`__ .                                                                                                                             |
| **`apw_eng_20020624_0436_1:27-28-29`**  | Madagascar 's rival leader , Didier Ratsiraka , has returned to the island nation , officials said Monday , signaling the country 's leadership struggle was not __`yet over`__ .                                                                                                                              |
| **`apw_eng_20020814_0321_16:40-41-42`** | in nearby Passau , on the Austrian and Czech borders at the confluence of the Inn , Danube and Ilz rivers , the level of the Danube was falling , but city spokesman Herbert Zillinger said the threat was not __`yet over`__ because another flood wave could still travel up the Inn .                       |
| **`apw_eng_20081113_0174_3:25-26-27`**  | the conflicting statements indicated that bickering over verification of the North 's nuclear disarmament -- which has already dragged on for months -- was not __`yet over`__ , despite a deal reached last month in Pyongyang between U.S. nuclear envoy Christopher Hill and his North Korean counterpart . |
| **`apw_eng_20090511_1144_15:34-35-36`** | after Fannie Mae 's warning last week that it needs an extra $ 19 billion from the government after receiving $ 15 billion in March , it 's clear the financial crisis is not __`yet over`__ .                                                                                                                 |
| **`apw_eng_19970924_0155_1:21-22-23`**  | a case of mistaken identity means American war veteran Richard Luttrell 's search for the Vietnamese soldier he shot is not __`yet over`__ .                                                                                                                                                                   |
| **`nyt_eng_19971112_0725_18:13-14-15`** | U.S. Ambassador Bill Richardson told reporters that the crisis with Iraq was not __`yet over`__ and that `` we have not ruled out any options including the military option . ''                                                                                                                               |


### 7. _yet public_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_001.6912_x0011236_4:36-37-38`**   | The navy will need begin afresh the process for buying the submarines worth $ 7.5 billion and helicopters worth $ 5 billion , they said , asking not to be identified as the information is not __`yet public`__ .                                                                                                        |
| **`pcc_eng_14_003.4436_x0039541_05:51-52-53`**  | Tom Wheeler , the chairman of the Federal Communications Commission , will circulate a proposal to his colleagues Thursday that would radically update the 30 - year- old aid program , known as Lifeline , according to FCC officials who spoke on the condition of anonymity because the plan is not __`yet public`__ . |
| **`pcc_eng_05_090.8154_x1452904_4:15-16-17`**   | BIHS is also reeling after losing its director suddenly - for reasons that are n't __`yet public`__ .                                                                                                                                                                                                                     |
| **`pcc_eng_27_106.9922_x1714469_1:36-37-38`**   | From Bloomberg : Richard Williamson , who oversaw the mapping team , was fired by Senior Vice President Eddy Cue , said the people , who asked not to be named because the information was n't __`yet public`__ .                                                                                                         |
| **`pcc_eng_17_101.7944_x1629247_09:6-7-8`**     | The proposed regulatory changes are not __`yet public`__ , but MDE will post an announcement when they have been published by the Maryland Register .                                                                                                                                                                     |
| **`apw_eng_20080228_1648_5:18-19-20`**          | another military officer , speaking on condition of anonymity because full details about the ship movements are not __`yet public`__ , said the USS Cole is headed for patrol in the eastern Mediterranean and that the USS Nassau , an amphibious warship , would be joining it shortly .                                |
| **`pcc_eng_16_088.6064_x1418146_05:25-26-27`**  | The FAA was still considering that request today , said an agency official , who asked not to be identified because the details are n't __`yet public`__ .                                                                                                                                                                |
| **`pcc_eng_09_007.5841_x0106624_194:12-13-14`** | The details of the AFL - CIO / Chamber agreement are not __`yet public`__ .                                                                                                                                                                                                                                               |


### 8. _yet eligible_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                      |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_041.5928_x0656576_25:40-41-42`**  | But between that provision and a cut in the total amount for federal money appropriated for subsidies ( or " tax credits " ) , the Congressional Budget Office numbers say some lower - income older Americans who are n't __`yet eligible`__ for Medicare could face out - of - pocket health costs several times as much as they do now .                      |
| **`pcc_eng_18_008.1104_x0115066_2:55-56-57`**   | Today , the Department of Health and Human Services announced the " first round of applicants accepted into the Early Retiree Reinsurance Program , " a $ 5 billion program established by the new health care law to help employers and states " maintain coverage for early retirees age 55 and older who are not __`yet eligible`__ for Medicare . "          |
| **`pcc_eng_27_002.8687_x0030040_126:3-4-5`**    | For residents not __`yet eligible`__ for Life Minded rewards , we increase rent on the anniversary of your move - in date .                                                                                                                                                                                                                                      |
| **`pcc_eng_26_080.7078_x1288641_54:24-25-26`**  | Early in 2013 as part of the fiscal cliff deal , roth conversions were expanded to allow participants to convert amounts that were not __`yet eligible`__ for distribution .                                                                                                                                                                                     |
| **`pcc_eng_29_039.9590_x0628961_23:17-18-19`**  | White House proposal , future workers would have lost a supplemental payment that current FERS retirees not __`yet eligible`__ for Social Security receive .                                                                                                                                                                                                     |
| **`pcc_eng_03_005.9833_x0080546_05:22-23-24`**  | The legislation would also end the annuity supplement for new FERS employees who retire before age 62 ( when they are not __`yet eligible`__ for Social Security ) and use the " chained consumer price index " to calculate future cost- of-living pension adjustments instead of the current CPI .                                                             |
| **`apw_eng_20081120_0060_26:44-45-46`**         | when Dodd asked the United Auto Workers union 's president , Ron Gettelfinger , this week whether prepackaged bankruptcy backed by federal guarantees was any more palatable , Gettelfinger cited risks to pensions and to retirees who could lose health benefits and are not __`yet eligible`__ for Medicare , the government 's health plan for the elderly . |
| **`pcc_eng_25_088.0475_x1408736_244:11-12-13`** | 1B Andy Phillips Contract status : Signed through 2006 ( not __`yet eligible`__ for arbitration ) Phillips has proven this season that he can be a productive big-league hitter with regular playing time .                                                                                                                                                      |


### 9. _yet clear_


|                                                | `token_str`                                                                                                                                                                                                                                                                             |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_071.5364_x1140931_10:3-4-5`**    | It is not __`yet clear`__ who was operating the boat .                                                                                                                                                                                                                                  |
| **`pcc_eng_02_008.6885_x0124027_09:3-4-5`**    | It is not __`yet clear`__ whether the methane presents an opportunity for a new source of energy or a potentially serious environmental threat , but for now the researchers want to map the distribution of the sites and conduct research on the composition and sources of the gas . |
| **`pcc_eng_17_041.1030_x0647939_02:34-35-36`** | The 5 - 4 decision in the case of Mark Janus versus AFSCME Council 31 may have started in Illinois , but the ruling had national implications -- though the full extent is n't __`yet clear`__ .                                                                                        |
| **`pcc_eng_02_001.0073_x0000134_55:3-4-5`**    | It is n't __`yet clear`__ whether they 'd even be able to do that if they wanted to .                                                                                                                                                                                                   |
| **`pcc_eng_15_014.0647_x0210689_08:08-09-10`** | The cause of Sunday 's explosion was not __`yet clear`__ , officials said .                                                                                                                                                                                                             |
| **`pcc_eng_22_058.9828_x0937436_40:14-15-16`** | Further study of this group of tumors is needed , as we are not __`yet clear`__ as to when metastasis takes place , although late work by Bloodgood seems to show that this is often comparatively early .                                                                              |
| **`apw_eng_20021015_0196_6:10-11-12`**         | Baja said the exact nature of the declaration was not __`yet clear`__ .                                                                                                                                                                                                                 |
| **`pcc_eng_08_046.2191_x0731947_06:12-13-14`** | If the effect were the same in humans - which is not __`yet clear`__ - that would be a greater impact than found with other dietary supplements , and similar to the effects of some prescription drugs .                                                                               |


### 10. _yet conclusive_


|                                                | `token_str`                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_011.4983_x0169416_57:38-39-40`** | 3 ) As with any ( relatively new ) invasive species , the unknowns abound and while Herborg et al . ( 2007 ) are important pieces of the puzzle , it sounds like their results are not __`yet conclusive`__ .                                                    |
| **`pcc_eng_02_091.0227_x1455453_78:5-6-7`**    | But these findings are n't __`yet conclusive`__ .                                                                                                                                                                                                                |
| **`pcc_eng_21_095.7299_x1530453_45:10-11-12`** | After all While the research on the issue is not __`yet conclusive`__ Treating eye conditions medical cannabis has been used for several years in the treatment of glaucoma .                                                                                    |
| **`pcc_eng_12_080.9182_x1291208_04:10-11-12`** | " These are intriguing results , but they are not __`yet conclusive`__ .                                                                                                                                                                                         |
| **`pcc_eng_01_061.1421_x0972772_29:12-13-14`** | The evidence on the cancer-causing potential of cell phone radiation is not __`yet conclusive`__ , but the World Health Organization 's cautionary stand is certain to fuel intensified research into electromagnetic fields and their impact on public health . |
| **`apw_eng_20020723_0185_6:7-8-9`**            | but Karleusa suggested the evidence was not __`yet conclusive`__ that the bodies exhumed from the camp were those removed from the truck .                                                                                                                       |
| **`pcc_eng_15_006.3520_x0086359_05:2-3-4`**    | Although not __`yet conclusive`__ , archaeologists argue that the only way that the objects could have arrived there is for humans to have placed them deliberately during times of drought .                                                                    |
| **`nyt_eng_20051117_0052_3:2-3-4`**            | though not __`yet conclusive`__ , a stream of reports in recent weeks indicates the nation 's long housing boom is coming off spectacular peaks and may be headed for far slower growth or even a decline .                                                      |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_final_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_official_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_ready_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_complete_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_ripe_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_over_80ex~51.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_public_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_eligible_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_clear_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/yet/yet_conclusive_80ex~29.csv`

## *immediately*


|                                             |    `f` |   `dP1` |   `LRC` |   `P1` |       `G2` | `l1`        | `l2`             |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:--------------------------------------------|-------:|--------:|--------:|-------:|-----------:|:------------|:-----------------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|-------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_mirror_] immediately~available**        |    184 |    0.06 |    5.44 |   0.06 |   1,232.57 | immediately | available        |    564 |  3,079 |   583,470 |      2.98 |      181.02 |        0.98 |            1.99 |  13.35 |   1.79 |    0.32 |   0.33 |           0.32 |            0.19 | mirror      |
| **[_direct_] immediately~clear**            | 24,488 |    0.29 |    5.41 |   0.29 | 141,124.53 | immediately | clear            | 58,040 | 84,227 | 6,347,362 |    770.17 |   23,717.83 |        0.97 |            1.88 | 151.56 |   1.50 |    0.41 |   0.42 |           0.41 |            0.35 | direct      |
| **[_direct_] immediately~available**        | 21,477 |    0.25 |    5.18 |   0.26 | 116,575.85 | immediately | available        | 58,040 | 82,956 | 6,347,362 |    758.55 |   20,718.45 |        0.96 |            1.77 | 141.37 |   1.45 |    0.36 |   0.37 |           0.36 |            0.31 | direct      |
| **[_direct_] immediately~apparent**         |  2,143 |    0.21 |    4.73 |   0.22 |  10,042.87 | immediately | apparent         | 58,040 |  9,798 | 6,347,362 |     89.59 |    2,053.41 |        0.96 |            1.50 |  44.36 |   1.38 |    0.04 |   0.04 |           0.21 |            0.12 | direct      |
| **[_direct_] immediately~adjacent**         |    108 |    0.31 |    4.69 |   0.32 |     591.96 | immediately | adjacent         | 58,040 |    342 | 6,347,362 |      3.13 |      104.87 |        0.97 |            1.70 |  10.09 |   1.54 |    0.00 |   0.00 |           0.31 |            0.15 | direct      |
| **[_direct_] immediately~reachable**        |    109 |    0.30 |    4.67 |   0.31 |     593.89 | immediately | reachable        | 58,040 |    350 | 6,347,362 |      3.20 |      105.80 |        0.97 |            1.69 |  10.13 |   1.53 |    0.00 |   0.00 |           0.30 |            0.15 | direct      |
| **[_direct_] immediately~obvious**          |  2,325 |    0.09 |    3.46 |   0.10 |   7,294.46 | immediately | obvious          | 58,040 | 22,651 | 6,347,362 |    207.12 |    2,117.88 |        0.91 |            1.11 |  43.92 |   1.05 |    0.04 |   0.04 |           0.09 |            0.07 | direct      |
| **[_direct_] immediately~recognizable**     |    249 |    0.09 |    3.10 |   0.10 |     777.98 | immediately | recognizable     | 58,040 |  2,404 | 6,347,362 |     21.98 |      227.02 |        0.91 |            1.10 |  14.39 |   1.05 |    0.00 |   0.00 |           0.09 |            0.05 | direct      |
| **[_direct_] immediately~life-threatening** |     64 |    0.12 |    2.85 |   0.13 |     227.19 | immediately | life-threatening | 58,040 |    497 | 6,347,362 |      4.54 |       59.46 |        0.93 |            1.21 |   7.43 |   1.15 |    0.00 |   0.00 |           0.12 |            0.06 | direct      |
| **[_direct_] immediately~evident**          |    470 |    0.07 |    2.78 |   0.08 |   1,202.69 | immediately | evident          | 58,040 |  6,131 | 6,347,362 |     56.06 |      413.94 |        0.88 |            0.96 |  19.09 |   0.92 |    0.01 |   0.01 |           0.07 |            0.04 | direct      |


### 1. _immediately available_


|                                                | `token_str`                                                                                                                                      |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_051.7020_x0819454_70:12-13-14`** | If you have questions or encounter difficulty when technical staff is not __`immediately available`__ , go to the conference registration desk . |
| **`apw_eng_19980722_1229_10:5-6-7`**           | Mordechai 's aide was not __`immediately available`__ for comment .                                                                              |
| **`nyt_eng_19960719_0366_18:5-6-7`**           | the after-tax figure was n't __`immediately available`__ .                                                                                       |
| **`pcc_eng_13_047.7595_x0756076_16:3-4-5`**    | Google was n't __`immediately available`__ for comment on its plans for the patent .                                                             |
| **`apw_eng_20030129_0653_7:7-8-9`**            | the length of the sentence was n't __`immediately available`__ .                                                                                 |
| **`apw_eng_19980324_0062_18:7-8-9`**           | the details of their deaths were not __`immediately available`__ .                                                                               |
| **`apw_eng_20030812_0590_3:09-10-11`**         | the man 's name and the charges were not __`immediately available`__ .                                                                           |
| **`pcc_eng_09_070.0229_x1116556_05:21-22`**    | A program spokesman said Blackmon will " continue to be evaluated , " though no timetable for a return was __`immediately available`__ .         |


### 2. _immediately clear_


|                                                | `token_str`                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_023.1584_x0358305_5:10-11-12`**  | The dogs were alive , but their welfare was n't __`immediately clear`__ , according to a member of the SPCA assisting in the removal of the dogs this morning .               |
| **`apw_eng_20080722_0684_3:3-4-5`**            | it was not __`immediately clear`__ if production had resumed , and company officials could not be reached for comment Tuesday .                                               |
| **`apw_eng_20030410_0263_10:3-4-5`**           | it was not __`immediately clear`__ how Nazarbayev would respond to Ablyazov 's request .                                                                                      |
| **`pcc_eng_22_051.6702_x0818622_18:22-23-24`** | The player is armed with a backpack and tonnes of resources they can find throughout the rainforest , though it 's never __`immediately clear`__ what they 're useful for .   |
| **`apw_eng_20090417_0728_8:3-4-5`**            | it was n't __`immediately clear`__ which groups the Vatican was referring to .                                                                                                |
| **`apw_eng_20090629_0201_10:3-4-5`**           | it was not __`immediately clear`__ who fired the mortar , but intelligence officials said it appeared to be aimed by at a nearby military outpost , presumably by militants . |
| **`nyt_eng_20050719_0243_4:3-4-5`**            | it was not __`immediately clear`__ whether his efforts would disrupt plans for the trial , which is to start in September .                                                   |
| **`pcc_eng_22_083.8057_x1338498_075:3-5-6`**   | It may not be __`immediately clear`__ what the relevance of the Prisoner 's Dilemma is to Smith 's theory of the Invisible Hand .                                             |


### 3. _immediately apparent_


|                                                 | `token_str`                                                                                                                                                      |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_085.3847_x1364701_05:5-6`**       | The main issue is __`immediately apparent`__ ; Church members do not grant interviews .                                                                          |
| **`pcc_eng_23_001.3790_x0006061_24:16-17-18`**  | I think the purpose for this NSA program is being missed , because it is not __`immediately apparent`__ .                                                        |
| **`pcc_eng_09_036.8836_x0580852_110:23-24-25`** | Why the physical landscape of the city should make you want to do pull-ups , squats , and Olympic-style weight lifting is not __`immediately apparent`__ .       |
| **`pcc_eng_06_027.2289_x0424319_125:09-10`**    | Moreover a severe shortage of Catholic priests was __`immediately apparent`__ .                                                                                  |
| **`pcc_eng_16_058.1336_x0924960_31:08-10-11`**  | The final result of your surgery may not be __`immediately apparent`__ .                                                                                         |
| **`pcc_eng_26_089.5722_x1432274_032:19-20-21`** | The crisis that had faced Timothy Henzel on the death of his father Paul in early 1898 was not __`immediately apparent`__ .                                      |
| **`pcc_eng_00_065.2288_x1038412_27:19-21-22`**  | ( This is used in some cases where the negative effects of a crime are ongoing and may not be __`immediately apparent`__ , like in medical malpractice cases ) . |
| **`pcc_eng_21_023.1885_x0358406_15:6-8-9`**     | Initially , that style may not be __`immediately apparent`__ in Dunedin .                                                                                        |


### 4. _immediately adjacent_


|                                             | `token_str`                                                                                                                                                                                                                                 |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_098.1861_x1570130_10:26-27`** | The Duke Energy Innovation Center , which is a joint project of Clemson University and the South Carolina Research Authority ( SCRA ) , is __`immediately adjacent`__ to the AMRL .                                                         |
| **`pcc_eng_08_083.6555_x1338325_30:16-17`** | The pumps for the sewer main are housed in the basement of the brick building __`immediately adjacent`__ to the bridge 's Pennsylvania abutment .                                                                                           |
| **`pcc_eng_03_055.2905_x0879298_26:39-40`** | " Unlike the majority of my colleagues , I have no ' Main Street ' in my district , but I do have a long stretch of Niagara Falls Boulevard , and the Niagara Falls International Airport is __`immediately adjacent`__ , " Lance said .    |
| **`pcc_eng_23_010.9317_x0160394_120:8-9`**  | The main worship halls for each are __`immediately adjacent`__ to one and other .                                                                                                                                                           |
| **`pcc_eng_11_016.1750_x0245558_11:5-6`**   | This wild landscape lies __`immediately adjacent`__ to the Blue Range Wolf Recovery Area , where an effort to return highly endangered Mexican wolves to the wild is currently underway .                                                   |
| **`pcc_eng_18_001.9784_x0015931_32:21-22`** | Sometimes the parking is in its own big ugly building , and sometimes it 's designed so that it 's __`immediately adjacent`__ to the apartment or townhouse of its occupant .                                                               |
| **`pcc_eng_02_088.6879_x1417760_27:7-8`**   | First , when they are located __`immediately adjacent`__ to the treatment bath , the water from the wash bath is transferred to the treatment bath .                                                                                        |
| **`pcc_eng_10_055.5000_x0881484_13:09-10`** | The western building , which will be located __`immediately adjacent`__ to Central Park , will become new home to Center for Hospice Care 's Life Transition Center ( LTC ) , its art counseling program and bereavement counseling staff . |


### 5. _immediately reachable_


|                                                | `token_str`                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_040.5565_x0639587_11:12-13-14`** | Semper Fi Management is headed by Frank Palazzolo , who was not __`immediately reachable`__ for comment .                                                                                                                                      |
| **`pcc_eng_23_088.3073_x1410953_5:4-5-6`**     | Diageo officials were not __`immediately reachable`__ .                                                                                                                                                                                        |
| **`pcc_eng_05_083.3476_x1332698_5:4-5-6`**     | The company was not __`immediately reachable`__ for comment .                                                                                                                                                                                  |
| **`pcc_eng_23_040.5596_x0639199_39:5-6-7`**    | The three multinationals were not __`immediately reachable`__ for comment .                                                                                                                                                                    |
| **`pcc_eng_21_013.5517_x0202789_17:22-23-24`** | Ateny Wek Ateny , a spokesman for Mr. Kiir , and Nyarji Roman , a spokesman for Mr. Machar , were not __`immediately reachable`__ by phone or email for comment on the report .                                                                |
| **`pcc_eng_11_083.1162_x1329074_10:17-18-19`** | Soft Bank also declined to comment , while Tiger , its other lead investor , was not __`immediately reachable`__ for comment .                                                                                                                 |
| **`pcc_eng_10_020.5099_x0315343_06:19-20-21`** | It is possible that residents headed to higher ground as soon as they felt the earthquake and were not __`immediately reachable`__ , said Chris Mc Kee , the assistant director of the Geophysical Observatory in the capital , Port Moresby . |
| **`pcc_eng_24_035.0110_x0550090_11:3-4-5`**    | Apple was not __`immediately reachable`__ for comment .                                                                                                                                                                                        |


### 6. _immediately obvious_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                             |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19960303_0205_24:18-19-20`**        | for starters , precisely what you are supposed to do in one of these virtual environments is not __`immediately obvious`__ , except perhaps to an avid video game player .                                                                                                                                                              |
| **`pcc_eng_18_101.9405_x1635217_5:4-5`**       | Pizza is an __`immediately obvious`__ pairing to drunken cooking -- it's delicious and quick , most of us keep some basic version of the components on hand , and it 's been a classic companion to drinking since time immemorial .                                                                                                    |
| **`pcc_eng_22_086.0038_x1373964_144:5-8-9`**   | 1 . It is not quite as __`immediately obvious`__ to new arrivals where to get certain needed information for interacting with a Git Hub repository .                                                                                                                                                                                    |
| **`pcc_eng_01_046.0118_x0727294_28:6-7-8`**    | For example , it is n't __`immediately obvious`__ how hoarding disorder should be treated , especially to someone who is n't a mental health professional .                                                                                                                                                                             |
| **`pcc_eng_28_074.2765_x1185123_29:11-12-13`** | In particular , we 're looking for songs that are n't __`immediately obvious`__ .                                                                                                                                                                                                                                                       |
| **`pcc_eng_05_083.3321_x1332440_166:5-6-7`**   | Now , it 's not __`immediately obvious`__ in the story that the priest and the Levite did a bad thing by passing the man on the opposite side of the road .                                                                                                                                                                             |
| **`pcc_eng_26_036.6562_x0576371_11:09-11-12`** | Their understanding of the dangers of fascism may not be __`immediately obvious`__ under all the robot dragon-dogs and hovercrafts and wacky bosses , one of which probably turns out to be a hentai octopus from another dimension -- you ca n't really escape those trappings of excessiveness in a big-budget video game like this . |
| **`pcc_eng_12_039.5919_x0624208_51:4-5-6`**    | If it 's not __`immediately obvious`__ how a bad person might become better , reserve the details on how to do this for a future write - up .                                                                                                                                                                                           |


### 7. _immediately recognizable_


|                                                 | `token_str`                                                                                                                                                                                                                                                       |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_005.4088_x0071299_081:11-12-13`** | One was surely Mr. Frodo's , but the other was not __`immediately recognizable`__ .                                                                                                                                                                               |
| **`pcc_eng_10_042.2575_x0667546_2:27-28`**      | Today , September 8th , 2017 , would have been the 85th birthday of Patsy Cline -- one of the most iconic , influential , and __`immediately recognizable`__ voices in the history of country music .                                                             |
| **`pcc_eng_14_038.6121_x0607626_08:10-11`**     | Rachel 's bringing her " playa bikes " , __`immediately recognizable`__ by those in the know as bikes embellished for Burning Man , an " annual art event and temporary community based on radical self expression and self-reliance in the Black Rock Desert . " |
| **`pcc_eng_02_043.6408_x0689951_52:12-14-15`**  | Despite being the most educated generation ever , the connection is n't always __`immediately recognizable`__ .                                                                                                                                                   |
| **`apw_eng_20010613_0785_9:6-7`**               | Frankfurt 's postcard-perfect skyline , __`immediately recognizable`__ to anyone who has flown into the city or rolled in by train , is the well-planned product of the city 's bustling commercial history and grandiose aspirations .                           |
| **`pcc_eng_21_099.1277_x1585389_16:11-12`**     | Tribeca 's tallest tower with it 's sculpted glass surfaces __`immediately recognizable`__ from miles away is a full-service condominium building .                                                                                                               |
| **`nyt_eng_19980108_0287_2:3-4`**               | he 's __`immediately recognizable`__ by his sculpted , craggy face , even if you ca n't quite place the name .                                                                                                                                                    |
| **`nyt_eng_20090911_0061_6:10-11`**             | her voice -- wry and wistful -- is almost __`immediately recognizable`__ and -LRB- though many have tried -RRB- inimitable .                                                                                                                                      |


### 8. _immediately life-threatening_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_057.6967_x0917816_06:1-6-7`**    | None of these diseases are __`immediately life-threatening`__ , but they can make life difficult to bear and place a great financial , emotional and logistical burden on health services , families and carers .                                                                                                             |
| **`pcc_eng_27_033.1664_x0519421_53:2-3-4`**    | Although not __`immediately life-threatening`__ , complications of atrial flutter can be serious if left untreated .                                                                                                                                                                                                          |
| **`pcc_eng_11_087.8466_x1405644_10:2-3-4`**    | Although not __`immediately life-threatening`__ , the impact of these abnormalities on the long term health and quality of life in these patients may be considerable .                                                                                                                                                       |
| **`pcc_eng_14_011.2443_x0165555_10:10-11`**    | Children whose symptoms or combination of symptoms suggest an __`immediately life-threatening`__ illness should be referred immediately for emergency medical care by the most appropriate means of transport ( usually 999 ambulance )                                                                                       |
| **`pcc_eng_10_048.1360_x0762453_26:3-4-5`**    | It 's not __`immediately life-threatening`__ , and in some cases , an AF episode is short-lived and goes away on its own .                                                                                                                                                                                                    |
| **`pcc_eng_10_072.7133_x1159301_18:11-12-13`** | She says she feels invisible because her chronic conditions are n't __`immediately life-threatening`__ , making her less of a priority than she should be .                                                                                                                                                                   |
| **`pcc_eng_21_066.7061_x1061833_14:26-28-29`** | But with their bone marrow destroyed , transplant recipients become vulnerable to life-threatening complications , a risk viewed as unnecessary because sickle cell disease is not typically __`immediately life-threatening`__ .                                                                                             |
| **`pcc_eng_06_107.7156_x1726233_26:2-3-4`**    | Although not __`immediately life-threatening`__ , sleep apnea significantly reduces your quality of life and will increase the potential for significant health conditions , such as high blood pressure , cardiovascular disease , type - 2 diabetes , liver problems and complications with other medications and surgery . |


### 9. _immediately evident_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                    |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000308_0481_48:4-5-6`**            | although it is not __`immediately evident`__ in the broad market indexes , most shares are currently trading at bear market levels .                                                                                                                                                                                                                                                                                           |
| **`nyt_eng_19990304_0008_26:15-16-17`**         | if the Clippers were bent on ending the suspense Tuesday night , it was n't __`immediately evident`__ .                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_23_004.7119_x0059761_15:49-50-51`**  | On the Pole Star at a week 's residency at the Gloucester Writers Center , the former home of poet Vincent Ferrini , frequented by Charles Olson , both poetically speaking trollers in the sea of creative discovery , extending the poem into an associative exploration of connections not __`immediately evident`__ to the naked eye , from August 2 - 9 , 2014 .                                                          |
| **`pcc_eng_29_006.2108_x0084403_10:10-12-13`**  | The connection between the U.S. and the Arctic might not be __`immediately evident`__ due to the distance , but the U.S. is actually one of eight countries that make up the Arctic Council .                                                                                                                                                                                                                                  |
| **`pcc_eng_25_034.8250_x0547616_18:18-19-20`**  | Gerry can be seen in the images below , checking out remains of an early verandah ( not __`immediately evident`__ in the 1972 photograph ) .                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_23_038.8161_x0610941_08:12-13-14`**  | * Identify , define and develop solutions to issues that are not __`immediately evident`__ in existing processes and systems .                                                                                                                                                                                                                                                                                                 |
| **`nyt_eng_20090727_0033_27:17-18`**            | walk through the front door , and Hipskind 's knack for mixing styles and eras is __`immediately evident`__ .                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_16_051.1876_x0812393_037:60-61-62`** | But they 're difficult to pin down as to why they say this , because this animal , like all other quasi-birds of that age , lacks many definitive features of modern birds , and it retains so many distinctly saurian features that when the last Archaeopteryx was found in the 1960s , the traces of its feathers were n't __`immediately evident`__ , and it was thus mistaken for a small dinosaur called Compsognathus . |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_available_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_clear_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_apparent_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_adjacent_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_reachable_80ex~32.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_obvious_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_recognizable_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_life-threatening_80ex~19.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/immediately/immediately_evident_80ex~80.csv`

## *particularly*


|                                        |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`         | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:---------------------------------------|------:|--------:|--------:|-------:|---------:|:-------------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] particularly~noteworthy** |   338 |    0.23 |    4.25 |   0.25 | 1,483.20 | particularly | noteworthy | 76,162 |  1,374 | 6,347,362 |     16.49 |      321.51 |        0.95 |            1.43 | 17.49 |   1.31 |    0.00 |   0.00 |           0.23 |            0.12 | direct      |
| **[_mirror_] particularly~noteworthy** |    87 |    0.33 |    3.89 |   0.35 |   389.48 | particularly | noteworthy | 10,029 |    251 |   583,470 |      4.31 |       82.69 |        0.95 |            1.49 |  8.86 |   1.30 |    0.01 |   0.01 |           0.33 |            0.17 | mirror      |
| **[_direct_] particularly~fond**       | 1,254 |    0.15 |    3.74 |   0.16 | 4,399.54 | particularly | fond       | 76,162 |  7,771 | 6,347,362 |     93.24 |    1,160.76 |        0.93 |            1.21 | 32.78 |   1.13 |    0.02 |   0.02 |           0.15 |            0.08 | direct      |
| **[_direct_] particularly~revelatory** |    60 |    0.22 |    3.38 |   0.23 |   254.72 | particularly | revelatory | 76,162 |    260 | 6,347,362 |      3.12 |       56.88 |        0.95 |            1.40 |  7.34 |   1.28 |    0.00 |   0.00 |           0.22 |            0.11 | direct      |
| **[_direct_] particularly~religious**  |   486 |    0.13 |    3.34 |   0.14 | 1,552.38 | particularly | religious  | 76,162 |  3,507 | 6,347,362 |     42.08 |      443.92 |        0.91 |            1.13 | 20.14 |   1.06 |    0.01 |   0.01 |           0.13 |            0.07 | direct      |
| **[_mirror_] particularly~novel**      |    54 |    0.28 |    3.32 |   0.30 |   224.26 | particularly | novel      | 10,029 |    179 |   583,470 |      3.08 |       50.92 |        0.94 |            1.40 |  6.93 |   1.24 |    0.01 |   0.01 |           0.28 |            0.14 | mirror      |
| **[_mirror_] particularly~unusual**    |   173 |    0.17 |    3.04 |   0.19 |   540.06 | particularly | unusual    | 10,029 |    933 |   583,470 |     16.04 |      156.96 |        0.91 |            1.12 | 11.93 |   1.03 |    0.02 |   0.02 |           0.17 |            0.09 | mirror      |
| **[_direct_] particularly~novel**      |   129 |    0.13 |    2.98 |   0.14 |   418.75 | particularly | novel      | 76,162 |    905 | 6,347,362 |     10.86 |      118.14 |        0.92 |            1.14 | 10.40 |   1.07 |    0.00 |   0.00 |           0.13 |            0.07 | direct      |
| **[_mirror_] particularly~fond**       |   117 |    0.18 |    2.98 |   0.20 |   377.50 | particularly | fond       | 10,029 |    598 |   583,470 |     10.28 |      106.72 |        0.91 |            1.15 |  9.87 |   1.06 |    0.01 |   0.01 |           0.18 |            0.09 | mirror      |
| **[_direct_] particularly~acute**      |   135 |    0.12 |    2.85 |   0.13 |   413.83 | particularly | acute      | 76,162 |  1,038 | 6,347,362 |     12.45 |      122.55 |        0.91 |            1.09 | 10.55 |   1.03 |    0.00 |   0.00 |           0.12 |            0.06 | direct      |


### 1. _particularly noteworthy_


|                                                | `token_str`                                                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_082.3005_x1314504_13:18-19`**    | The depiction of the aftermath may be on shaky ground but Clarke 's portrayal of Kennedy is __`particularly noteworthy`__ .                                                                                                                                                                    |
| **`pcc_eng_28_069.2642_x1104583_04:5-6`**      | What makes these voyages __`particularly noteworthy`__ is that Croisi Europe has further broken them down according to the time of year in which they operate , designing separate itineraries for Christmas , New Year's , and the fabled Christmas Markets that run up until Christmas Eve . |
| **`pcc_eng_26_020.3872_x0313413_27:12-13`**    | The artistry and ambiance established within the show have always been __`particularly noteworthy`__ and this volume is no exception .                                                                                                                                                         |
| **`pcc_eng_08_044.7060_x0707309_55:8-9`**      | Finally , we come to the third __`particularly noteworthy`__ point of failure , which was identified by Senators Chambliss and Burr in their " Additional Views . "                                                                                                                            |
| **`pcc_eng_08_028.6142_x0447192_27:5-6`**      | Wednesday 's study is __`particularly noteworthy`__ , Mason says , because it includes clinical data -- in - office blood pressure checks , for example , and validated diagnostic tools for depression and anxiety -- rather than depending exclusively on self-reported diagnoses .          |
| **`pcc_eng_18_008.3753_x0119415_14:10-12-13`** | Not surprisingly , Empire Resorts ' financial results have n't been __`particularly noteworthy`__ lately .                                                                                                                                                                                     |
| **`pcc_eng_25_092.1845_x1475532_009:4-5-6`**   | That alone is not __`particularly noteworthy`__ , but what he has chosen to do with his voice is .                                                                                                                                                                                             |
| **`pcc_eng_15_091.3334_x1460176_2:7-8`**       | His creation of the syllabary is __`particularly noteworthy`__ in that he could not previously read any script .                                                                                                                                                                               |


### 2. _particularly fond_


|                                                | `token_str`                                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_073.1280_x1165994_08:16-17-18`** | I am not sure why it continued to captivate me , especially as I was not __`particularly fond`__ of hamburgers .                                                                                                                                                    |
| **`pcc_eng_18_038.5869_x0608123_19:12-13-14`** | Although the resulting low latency is rather nice , I 'm not __`particularly fond`__ of this " fix . "                                                                                                                                                              |
| **`pcc_eng_14_089.2986_x1427228_32:3-4-5`**    | I was never __`particularly fond`__ of her , and admonished throughout my life to remember that " she 's family and will always love you no matter what . "                                                                                                         |
| **`pcc_eng_27_002.8693_x0030050_09:47-48-49`** | Eventually it turned out that " The Maze Runner " is one of the best books I 've ever read in my life , and I 'm really glad I did n't put this particular book back onto my daughter 's bookshelf just because she was n't __`particularly fond`__ of it herself ! |
| **`pcc_eng_00_012.9178_x0192484_5:17-18`**     | If you 're looking for a very strong , long- lasting scent -- and you 're __`particularly fond`__ of licorice -- then this moisturizing salve is a great way to keep your skin soft and itch-free throughout the year .                                             |
| **`pcc_eng_14_036.3064_x0570331_22:16-18-19`** | Until then , Nancy had survived just fine with her well , although she 'd never been __`particularly fond`__ of the water that came out of it .                                                                                                                     |
| **`pcc_eng_05_039.1207_x0617051_32:19-20-21`** | Try this easy recipe : I promise you that you will love it , even if you 're not __`particularly fond`__ of Indian food ( do n't worry , I was a non-believer , too ) .                                                                                             |
| **`pcc_eng_18_015.4229_x0233758_4:3-4`**       | She is __`particularly fond`__ of the fleece lined pockets .                                                                                                                                                                                                        |


### 3. _particularly revelatory_


|                                                 | `token_str`                                                                                                                                                                       |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_033.8881_x0532347_28:1-2-3`**     | Not __`particularly revelatory`__ , but still quite delicious .                                                                                                                   |
| **`pcc_eng_26_085.6133_x1368274_15:12-13-14`**  | THQ has teased new Darksiders II DLC with a single , not __`particularly revelatory`__ image via its Darksiders Twitter page .                                                    |
| **`pcc_eng_09_035.6066_x0560265_35:16-17-18`**  | Once again , what she 's saying is absolutely true ( even if it 's not __`particularly revelatory`__ ) , but it 's how she 's saying it that 's such a disservice .               |
| **`pcc_eng_18_033.0161_x0518279_21:17-18-19`**  | Fine also comments on the director performance , saying : " You 've Been Trumped is n't __`particularly revelatory`__ , nor is it an outstanding piece of film-making .           |
| **`pcc_eng_21_094.6388_x1512900_13:22-23-24`**  | Extensive liner notes clear up the confusion , but it feels like a lot of work for an album that 's not __`particularly revelatory`__ in either music or story .                  |
| **`pcc_eng_01_095.8512_x1533647_08:18-23-24`**  | Since the comment filing system is commercially cloud-hosted , and the system is fundamentally internet- based , neither of these descriptions is __`particularly revelatory`__ . |
| **`pcc_eng_24_077.1833_x1232345_083:19-20-21`** | Altoona is the sole location reporting any snow , and a look at the satellite and radar was n't __`particularly revelatory`__ either .                                            |
| **`pcc_eng_26_009.2294_x0132926_09:09-10-11`**  | Aside from the unusual setting , there 's nothing __`particularly revelatory`__ about Monty Python Live at the Hollywood Bowl .                                                   |


### 4. _particularly religious_


|                                                | `token_str`                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_080.0056_x1279012_46:28-29-30`** | Now that I think about it , my IL 's used the whole " reproduction " argument on me a few weeks ago and considering they 're not __`particularly religious`__ , I guess this would be outside of the bible defense .                             |
| **`pcc_eng_22_055.9010_x0887221_13:4-5-6`**    | If you 're not __`particularly religious`__ , then the idea of body respect remains the same ; your body is still a miracle !                                                                                                                    |
| **`pcc_eng_18_036.7245_x0578132_30:20-21-22`** | He tells his parents ( and his religious relatives ) that he does eat pork and that he 's not __`particularly religious`__ .                                                                                                                     |
| **`pcc_eng_11_003.1763_x0035328_61:4-5-6`**    | Although she 's not __`particularly religious`__ , Milman feels very connected to Judaism -- at least on a cultural , traditional level .                                                                                                        |
| **`pcc_eng_18_088.1212_x1410819_18:23-24-25`** | Here 's an interesting article by a St. Thomas professor and the feedback she 's getting from students who she says are n't __`particularly religious`__ .                                                                                       |
| **`pcc_eng_01_068.1971_x1086925_36:3-4-5`**    | Kato was n't __`particularly religious`__ and honestly did n't understand western religion anyhow , so attempting to name and describe these foreign things was beyond him .                                                                     |
| **`pcc_eng_25_082.7596_x1323456_91:4-5-6`**    | East asians are n't __`particularly religious`__ in the first place , and do n't have any kind of " monoreligious " concept the way westerners do .                                                                                              |
| **`pcc_eng_03_085.7256_x1371927_30:5-6-7`**    | Even though I 'm not __`particularly religious`__ , I 've found that the churches and other religious buildings in almost every city or town I 've ever been to are one of the best places to visit , and they 're usually free or almost free . |


### 5. _particularly novel_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_028.7972_x0449423_25:2-3`**       | A __`particularly novel`__ aspect is that it automatically determines the minimum number of rounds needed for a computation , ...                                                                                                                                                                                                                                                         |
| **`pcc_eng_18_084.9988_x1360098_13:30-31-32`**  | Langewiesche 's presentation of nuclear weapons as the great equalizer ( with increasing potential of becoming ' the great leveller ' ) in the international system was interesting but not __`particularly novel`__ .                                                                                                                                                                    |
| **`pcc_eng_22_007.1907_x0099856_16:55-60-61`**  | More realistic Superman clones , law enforcement agencies dedicated to superhero activity , superheroes letting their power and skewed perspective drive them bonkers , superheroes " going bad , " superheroes as they would " really " be , or a world that reacts to super-people like we react to real life celebrities ; none of these things are __`particularly novel`__ anymore . |
| **`pcc_eng_21_024.6887_x0382786_29:4-5-6`**     | Gastronomic snobbery is nothing __`particularly novel`__ .                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_23_006.9388_x0095981_05:11-13-14`**  | Setting a game in the theatre of modern war may not be __`particularly novel`__ anymore , but for EA 's long-running Medal of Honor franchise it 's a first .                                                                                                                                                                                                                             |
| **`pcc_eng_13_092.5269_x1479594_125:09-10-11`** | Although I really enjoyed it , there is nothing __`particularly novel`__ in the story .                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_21_097.8756_x1565111_16:7-8-9`**     | ALEC ROSS : There 's actually nothing __`particularly novel`__ about any of this , except that we all get to see it .                                                                                                                                                                                                                                                                     |
| **`pcc_eng_11_086.3735_x1381926_10:12-13-14`**  | First , a definition : while our definition of productivity is n't __`particularly novel`__ , it does describe its fundamental nature : based on our study , productivity is ' work that is produced on time and to specification ' .                                                                                                                                                     |


### 6. _particularly unusual_


|                                                | `token_str`                                                                                                                                                                                                                                                                                          |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_052.9195_x0838778_70:27-28-29`** | Tampa Bay and Cleveland are the only two teams in the NFL that have a turnover ratio of 0 after four games , but that is not __`particularly unusual`__ .                                                                                                                                            |
| **`pcc_eng_00_061.0830_x0971292_12:5-6-7`**    | Now , this is n't __`particularly unusual`__ for me , because I love music of several different types , and i Tunes is an easy way for me to preview something and decide if I want to just have it for background on the computer , or it I want [...]                                              |
| **`pcc_eng_21_091.9800_x1470236_19:4-5-6`**    | And this is n't __`particularly unusual`__ .                                                                                                                                                                                                                                                         |
| **`pcc_eng_06_026.3041_x0409524_17:4-5-6`**    | So there 's nothing __`particularly unusual`__ about the style of these vocals , they are just done exceptionally well , and with enough variation to keep you off your guard for the next barrage of inhuman vocal carnage .                                                                        |
| **`pcc_eng_19_007.2499_x0101246_04:2-3`**      | One __`particularly unusual`__ rack , constructed from stainless steel with room for four bikes , resembles a patch of waist - high grass .                                                                                                                                                          |
| **`pcc_eng_25_004.0739_x0050272_19:56-57-58`** | In a post on our site , Michael Santoro , a professor of business ethics at Rutgers , pointed out that the 2007 deal at the center of the case , which was called Abacus , and which Tourre , in an e-mail to his girlfriend , described as a " monstrosity , " was n't __`particularly unusual`__ . |
| **`pcc_eng_29_085.7449_x1368909_01:13-14-15`** | FOOTBALL is a sport that constantly reinvents itself , so there is nothing __`particularly unusual`__ about a prevailing orthodoxy collapsing .                                                                                                                                                      |
| **`pcc_eng_28_021.8256_x0336428_021:7-8-9`**   | These extremes are not rare , not __`particularly unusual`__ .                                                                                                                                                                                                                                       |


### 7. _particularly acute_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                                                                  |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20001113_0347_17:11-12`**        | the problem of repetitive stress injuries -LRB- RSI -RRB- is __`particularly acute`__ in Massachusetts .                                                                                                                                                                                                                                                                     |
| **`pcc_eng_28_105.6670_x1692592_05:4-5`**   | The problem was __`particularly acute`__ in San Francisco , and it was clear that a significant segment of the city 's cultural identity and economy was at risk of displacement .                                                                                                                                                                                           |
| **`pcc_eng_03_059.5531_x0948266_18:4-5`**   | The risk is __`particularly acute`__ with regard to the economic rationale to develop low-cost , high flight rate launch systems .                                                                                                                                                                                                                                           |
| **`pcc_eng_28_041.5545_x0655959_56:16-17`** | My outrage was prompted by witnessing the steady deterioration of another prisoner , resulting from __`particularly acute`__ mental torture inflicted in Oregon 's Disciplinary Segregation Units , which duplicate almost exactly conditions of torture practiced at Philadelphia 's Eastern State Penitentiary that were outlawed by the U.S. Supreme Court in the 1800s . |
| **`pcc_eng_12_040.7681_x0643163_19:18-19`** | John Richter , Vice President of Friends of the Jordan River Valley , says the problem is __`particularly acute`__ in the Jordan Valley .                                                                                                                                                                                                                                    |
| **`pcc_eng_09_017.9210_x0274138_05:7-8`**   | The feeling of almost has been __`particularly acute`__ in my life recently .                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_17_101.2254_x1620014_04:4-5`**   | The problem is __`particularly acute`__ at some hospitals .                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_27_017.2394_x0262799_23:7-8`**   | " The need for safeguards is __`particularly acute`__ because EPA is giving industry an economic incentive to push the edge of the ethical envelope , " Roose added .                                                                                                                                                                                                        |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_noteworthy_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_fond_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_revelatory_80ex~15.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_religious_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_novel_80ex~41.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_unusual_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/particularly/particularly_acute_80ex~80.csv`

## *terribly*


|                                    |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`     | `l2`       |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-----------------------------------|------:|--------:|--------:|-------:|---------:|:---------|:-----------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] terribly~surprising** |   949 |    0.05 |    3.82 |   0.05 | 3,589.19 | terribly | surprising | 19,802 | 18,776 | 6,347,362 |     58.58 |      890.42 |        0.94 |            1.25 | 28.90 |   1.21 |    0.05 |   0.05 |           0.05 |            0.05 | direct      |
| **[_mirror_] terribly~wrong**      |   401 |    0.04 |    3.31 |   0.05 | 1,369.70 | terribly | wrong      |  2,204 |  8,506 |   583,470 |     32.13 |      368.87 |        0.92 |            1.20 | 18.42 |   1.10 |    0.17 |   0.18 |           0.17 |            0.11 | mirror      |
| **[_direct_] terribly~original**   |   201 |    0.04 |    3.24 |   0.04 |   689.61 | terribly | original   | 19,802 |  4,693 | 6,347,362 |     14.64 |      186.36 |        0.93 |            1.16 | 13.14 |   1.14 |    0.01 |   0.01 |           0.04 |            0.02 | direct      |
| **[_mirror_] terribly~surprising** |    67 |    0.05 |    2.87 |   0.05 |   236.04 | terribly | surprising |  2,204 |  1,248 |   583,470 |      4.71 |       62.29 |        0.93 |            1.19 |  7.61 |   1.15 |    0.03 |   0.03 |           0.05 |            0.04 | mirror      |
| **[_direct_] terribly~surprised**  |   291 |    0.03 |    2.75 |   0.03 |   782.04 | terribly | surprised  | 19,802 | 10,157 | 6,347,362 |     31.69 |      259.31 |        0.89 |            0.98 | 15.20 |   0.96 |    0.01 |   0.01 |           0.03 |            0.02 | direct      |
| **[_direct_] terribly~uncommon**   |   103 |    0.03 |    2.57 |   0.03 |   300.00 | terribly | uncommon   | 19,802 |  3,165 | 6,347,362 |      9.87 |       93.13 |        0.90 |            1.04 |  9.18 |   1.02 |    0.00 |   0.01 |           0.03 |            0.02 | direct      |
| **[_direct_] terribly~impressed**  |   283 |    0.02 |    2.44 |   0.02 |   656.23 | terribly | impressed  | 19,802 | 12,138 | 6,347,362 |     37.87 |      245.13 |        0.87 |            0.89 | 14.57 |   0.87 |    0.01 |   0.01 |           0.02 |            0.02 | direct      |
| **[_direct_] terribly~fond**       |   192 |    0.02 |    2.41 |   0.02 |   464.21 | terribly | fond       | 19,802 |  7,771 | 6,347,362 |     24.24 |      167.76 |        0.87 |            0.91 | 12.11 |   0.90 |    0.01 |   0.01 |           0.02 |            0.02 | direct      |
| **[_direct_] terribly~exciting**   |   391 |    0.02 |    2.24 |   0.02 |   781.19 | terribly | exciting   | 19,802 | 20,233 | 6,347,362 |     63.12 |      327.88 |        0.84 |            0.81 | 16.58 |   0.79 |    0.02 |   0.02 |           0.02 |            0.02 | direct      |
| **[_direct_] terribly~wrong**      |   398 |    0.02 |    2.19 |   0.02 |   771.55 | terribly | wrong      | 19,802 | 21,332 | 6,347,362 |     66.55 |      331.45 |        0.83 |            0.79 | 16.61 |   0.78 |    0.02 |   0.02 |           0.02 |            0.02 | direct      |


### 1. _terribly surprising_


|                                                 | `token_str`                                                                                                                                                                                      |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_073.2940_x1168275_07:16-17-18`**  | " Most teens eat , sleep , and breathe the Internet , so it is not __`terribly surprising`__ that they would embrace a therapy delivered in this way , " she says .                              |
| **`pcc_eng_24_027.7324_x0432291_12:1-2-3`**     | Not __`terribly surprising`__ about the lack of a woman .                                                                                                                                        |
| **`pcc_eng_13_087.2844_x1394633_22:5-6-7`**     | No , it 's not __`terribly surprising`__ that " Raising the Bar " did n't last longer : it was a pleasant show , but unlike TNT 's other series , it did n't really have a hook that stood out . |
| **`pcc_eng_05_093.1749_x1491303_036:5-6-7`**    | This win is actually not __`terribly surprising`__ .                                                                                                                                             |
| **`pcc_eng_05_095.6152_x1530760_02:5-6-7`**     | That in itself is not __`terribly surprising`__ for the Internet search giant .                                                                                                                  |
| **`pcc_eng_19_042.5567_x0670889_034:19-21-22`** | The current government has done an awful lot of things I do n't agree with -- this should n't be __`terribly surprising`__ to you .                                                              |
| **`pcc_eng_05_080.9584_x1294155_03:3-4-5`**     | It 's not __`terribly surprising`__ , given the trio's history together , that most of Austere sounds very much like songs                                                                       |
| **`pcc_eng_00_011.8633_x0175452_17:12-13-14`**  | The $ 500 price tag on the standalone model is also not __`terribly surprising`__ .                                                                                                              |


### 2. _terribly wrong_


|                                              | `token_str`                                                                                                                                                                                             |
|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_049.4595_x0784351_056:4-5`**   | Has something gone __`terribly wrong`__ in America ?                                                                                                                                                    |
| **`pcc_eng_17_072.6490_x1157852_16:8-9`**    | When Jerry 's crush on Fiona goes __`terribly wrong`__ , his reality starts to unravel , and his life slowly begins to spiral out of control .                                                          |
| **`nyt_eng_19970213_0007_4:4-5`**            | but something went __`terribly wrong`__ , and three of them died .                                                                                                                                      |
| **`pcc_eng_20_092.0864_x1471622_92:28-29`**  | It 's creepy , haunting , dark and gritty , and shows the true horror of what happens when the love between a mother and daughter goes __`terribly wrong`__ ( or worse , is n't there to begin with ) . |
| **`pcc_eng_17_076.5687_x1221334_033:14-15`** | And by the start of the 1960s , he knew something had gone __`terribly wrong`__ .                                                                                                                       |
| **`pcc_eng_28_008.7425_x0125112_041:8-9`**   | Do we conclude that there is something __`terribly wrong`__ with American culture ?                                                                                                                     |
| **`pcc_eng_00_070.9881_x1131332_07:3-4`**    | Something was __`terribly wrong`__ in Scott 's life , but it was n't his inability - or unwillingness - to speak in tongues .                                                                           |
| **`pcc_eng_23_021.0750_x0324198_080:11-12`** | Michelle : Well , oftentimes they think that something is __`terribly wrong`__ physically .                                                                                                             |


### 3. _terribly original_


|                                                 | `token_str`                                                                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_098.1773_x1571097_03:3-4-5`**     | There 's nothing __`terribly original`__ about the premise or plot of " Welcome to Your Authentic Indian Experience ( tm ) " by Rebecca Roanhorse , but do not mistake this observation for an unfriendly critique .        |
| **`pcc_eng_24_103.1597_x1652783_09:7-8-9`**     | Ok , so the setup is n't __`terribly original`__ .                                                                                                                                                                          |
| **`pcc_eng_24_086.2673_x1379137_12:15-16-17`**  | As far as forays into contemporary masculine psychology go , Hymowitz 's essay was n't __`terribly original`__ .                                                                                                            |
| **`pcc_eng_16_088.0325_x1408847_017:13-14-15`** | In its place , a new identity would form that , while not __`terribly original`__ in the context of the times , was nonetheless a much truer vision of who he was .                                                         |
| **`pcc_eng_22_084.8728_x1355692_20:11-12-13`**  | But it 's worth pointing out that the movie is n't __`terribly original`__ .                                                                                                                                                |
| **`pcc_eng_25_096.5754_x1546741_106:5-6-7`**    | I guess that 's nothing __`terribly original`__ or useful .                                                                                                                                                                 |
| **`pcc_eng_14_030.4738_x0476280_28:6-7-8`**     | I said the plot was n't __`terribly original`__ , but I have n't seen much like this , so it was original enough for me .                                                                                                   |
| **`pcc_eng_29_003.8577_x0046227_27:4-5-6`**     | The denoument is n't __`terribly original`__ but the central conceit , mingling present and two layers of past events , works well , and there 's certainly more substance to this than to the average haunted house tale . |


### 4. _terribly surprised_


|                                                  | `token_str`                                                                                                                                                                                                                                     |
|:-------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_095.7823_x1534409_235:31-33-34`**  | Given that series was based on a challenge given to him to write something based off two " lame " ideas given by someone on the internet , I would n't be __`terribly surprised`__ if some of the place names were after-thoughts .             |
| **`pcc_eng_28_010.0621_x0146455_70:1-2-3`**      | Not __`terribly surprised`__ .                                                                                                                                                                                                                  |
| **`nyt_eng_20000720_0356_8:22-23-24`**           | Duncan admitted that he anticipated the Spearman hypothesis would be borne out by neural imaging , and that therefore he was not __`terribly surprised`__ by his results .                                                                      |
| **`nyt_eng_20000905_0351_5:5-7-8`**              | so theater fans should n't be __`terribly surprised`__ to learn that none of the above is now expected to reach a Broadway theater anytime soon , with the possible exception of `` The Visit , '' which in any case will be without Lansbury . |
| **`pcc_eng_13_094.7143_x1514541_21:4-5-6`**      | " I 'm not __`terribly surprised`__ . "                                                                                                                                                                                                         |
| **`pcc_eng_29_044.3419_x0700323_58:5-6-7`**      | Father Marek was " not __`terribly surprised`__ " at the finding , he says .                                                                                                                                                                    |
| **`pcc_eng_06_108.2215_x1734333_091:18-21-22`**  | Supposedly he dies , although if you 've seen any of the trailers , you probably wo n't be too __`terribly surprised`__ when he pops up alive about an hour later .                                                                             |
| **`pcc_eng_27_028.6385_x0446323_0398:20-21-22`** | " Mal , we 're coming up on Amnesty , " Hank said into the com , but was n't __`terribly surprised`__ when the man himself spoke at his elbow .                                                                                                 |


### 5. _terribly uncommon_


|                                                | `token_str`                                                                                                                                                                                                     |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_031.3481_x0490431_40:3-4-5`**    | It 's not __`terribly uncommon`__ for the entire party to be decimated in a seemingly - routine random encounter , especially if they 're just trying to breeze their way through an encounter .                |
| **`pcc_eng_01_069.4322_x1107026_33:3-4-5`**    | It 's not __`terribly uncommon`__ in people who ca n't let themselves go ; those people do n't like to meditate because they do n't like to relinquish control .                                                |
| **`pcc_eng_14_082.8058_x1322266_07:14-15-16`** | While Christians marrying Jews , Jews marrying Hindus and Hindus marrying Buddhists is not __`terribly uncommon`__ in the US and other first world nations , it has not always been this way .                  |
| **`pcc_eng_28_026.9821_x0419639_32:3-4-5`**    | Plums are n't __`terribly uncommon`__ , but not a lot of people are familiar with pluots .                                                                                                                      |
| **`pcc_eng_22_089.4691_x1429976_26:26-27-28`** | The second surprise that fell through was that Bill had set up a police escort from the ceremony to the reception - something that is n't __`terribly uncommon`__ for a high ranking official in a small town . |
| **`pcc_eng_11_017.2605_x0263128_03:7-8-9`**    | American Robins with abnormal plumage are not __`terribly uncommon`__ , and a number of them are shown on our introductory page on odd plumages .                                                               |
| **`pcc_eng_28_079.4186_x1268524_56:3-4-5`**    | This is n't __`terribly uncommon`__ nor does it spell complete failure .                                                                                                                                        |
| **`pcc_eng_11_064.8935_x1034009_14:5-6-7`**    | Although lunar-planetary partnerships are not __`terribly uncommon`__ , Boberg said it is the specific planet 's presence that makes this an occasion to note .                                                 |


### 6. _terribly impressed_


|                                                | `token_str`                                                                                                                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_064.7858_x1031559_4:4-5-6`**     | While investors were n't __`terribly impressed`__ with RIM 's efforts and the company 's stock took a hit , developers and users alike were intrigued by several features shown off by the struggling smartphone maker . |
| **`pcc_eng_26_007.1231_x0098713_68:6-7-8`**    | I was , unfortunately , not __`terribly impressed`__ by their descriptions .                                                                                                                                             |
| **`pcc_eng_04_074.9212_x1194017_18:18-20-21`** | If your rich heiress does n't dig the whole wolf thing , make the whole wolf thing not be __`terribly impressed`__ with her either .                                                                                     |
| **`pcc_eng_27_051.4713_x0815756_163:3-4-5`**   | I was n't __`terribly impressed`__ , but this was dessert for me after a substanial meal , so maybe it was just my appetite at the time .                                                                                |
| **`pcc_eng_10_045.5017_x0720006_03:28-30-31`** | I love Tolkien , to be sure , but I 've seen and played a lot of adaptations of Middle- earth - related things , and have n't been __`terribly impressed`__ in recent years .                                            |
| **`pcc_eng_11_018.9588_x0290360_03:11-12-13`** | I 've tried dyeing with lawn grass before and was n't __`terribly impressed`__ .                                                                                                                                         |
| **`pcc_eng_26_045.1589_x0714206_09:3-4-5`**    | I was n't __`terribly impressed`__ and did n't really get it .                                                                                                                                                           |
| **`pcc_eng_08_106.0474_x1700935_12:3-4-5`**    | Poppaea 's not __`terribly impressed`__ with Barbara , no doubt because she 's witnessed Nero 's instant attraction to her .                                                                                             |


### 7. _terribly fond_


|                                                 | `token_str`                                                                                                                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_19971231_0619_24:11-12-13`**         | -lrb- Do n't know about you folks but I am not __`terribly fond`__ of Stanley Kubrick 's 2001 : A Space Odyssey , which many hail as the precursor of all modern science fiction films , thanks to its groundbreaking special effects , etc. -RRB-        |
| **`pcc_eng_29_032.1064_x0501927_19:3-4-5`**     | I am not __`terribly fond`__ of the idea of " software as a service ; " I like to have control over where my data is stored , and I also like the convenience and speed which comes from using software which does not depend on an Internet connection . |
| **`pcc_eng_28_068.7554_x1096311_12:15-16-17`**  | Available seating consists of small and square high tables and stools ( I was n't __`terribly fond`__ of this arrangement , but given the limited space , it did seem appropriate ) , and I did n't register any music .                                  |
| **`pcc_eng_28_104.5610_x1674823_06:3-4`**       | I 'm __`terribly fond`__ of both Buffy and old-fashioned adventure games and these capture the spirit of both of these things perfectly ( and they 're also quite funny ) .                                                                               |
| **`pcc_eng_10_088.9621_x1421758_050:3-4-5`**    | I 'm not __`terribly fond`__ of doing curses , but I just love the concept of these little tablets .                                                                                                                                                      |
| **`pcc_eng_19_071.1918_x1133663_003:6-7-8`**    | For example , he was n't __`terribly fond`__ of waiting for his latest brew to ferment and mature to the point where he could sample it .                                                                                                                 |
| **`pcc_eng_13_048.4233_x0766771_324:13-14-15`** | I got the idea last time it came up that you were n't __`terribly fond`__ of it .                                                                                                                                                                         |
| **`pcc_eng_04_032.5134_x0509229_09:13-14`**     | The foundation is cracking a little here , because the Left is __`terribly fond`__ of " born that way " arguments when they can get any traction from them .                                                                                              |


### 8. _terribly exciting_


|                                                | `token_str`                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_048.7228_x0770662_36:11-12-13`** | I was born and raised in Arkansas , which is n't __`terribly exciting`__ .                                                                             |
| **`pcc_eng_10_029.2611_x0456823_46:11-12-13`** | Wonder Woman came with the right leg , which was n't __`terribly exciting`__ on its own but is obviously vital to building the figure .                |
| **`pcc_eng_14_007.4135_x0103643_11:4-5-6`**    | ( It is not __`terribly exciting`__ , but it gets the job done . )                                                                                     |
| **`pcc_eng_14_039.1564_x0616445_77:3-4-5`**    | There is nothing __`terribly exciting`__ to be found here .                                                                                            |
| **`pcc_eng_23_009.0860_x0130506_06:1-2-3`**    | Nothing __`terribly exciting`__ happening in my life at the moment - and that 's a good thing .                                                        |
| **`pcc_eng_12_038.7931_x0611311_14:4-5-6`**    | If Dreamer is n't __`terribly exciting`__ , Gatins picks up steam in the home stretch ( when it counts ) .                                             |
| **`pcc_eng_29_032.6929_x0511559_12:08-09-10`** | While that in and of itself is n't __`terribly exciting`__ , the fact it can wirelessly charge compatible smartphones is more than a little uncommon . |
| **`pcc_eng_06_079.5061_x1269433_74:6-7-8`**    | Cat Ba town itself is not __`terribly exciting`__ though it does have a few hidden gems if you look for them .                                         |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_surprising_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_wrong_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_original_80ex~63.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_surprised_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_uncommon_80ex~20.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_impressed_80ex~77.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_fond_80ex~47.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/terribly/terribly_exciting_80ex~80.csv`

## *inherently*


|                                       |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`       | `l2`        |   `f1` |   `f2` |       `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:--------------------------------------|------:|--------:|--------:|-------:|----------:|:-----------|:------------|-------:|-------:|----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] inherently~evil**        |   392 |    0.12 |    6.26 |   0.12 |  2,829.19 | inherently | evil        |  8,614 |  3,171 | 6,347,362 |      4.30 |      387.70 |        0.99 |            2.04 | 19.58 |   1.96 |    0.05 |   0.05 |           0.12 |            0.08 | direct      |
| **[_direct_] inherently~wrong**       | 1,678 |    0.08 |    5.77 |   0.08 | 10,797.34 | inherently | wrong       |  8,614 | 21,332 | 6,347,362 |     28.95 |    1,649.05 |        0.98 |            1.89 | 40.26 |   1.76 |    0.19 |   0.19 |           0.19 |            0.13 | direct      |
| **[_mirror_] inherently~wrong**       | 1,571 |    0.18 |    5.09 |   0.18 |  9,012.22 | inherently | wrong       |  3,342 |  8,506 |   583,470 |     48.72 |    1,522.28 |        0.97 |            1.87 | 38.41 |   1.51 |    0.46 |   0.47 |           0.46 |            0.32 | mirror      |
| **[_direct_] inherently~racist**      |    67 |    0.04 |    3.91 |   0.04 |    332.29 | inherently | racist      |  8,614 |  1,609 | 6,347,362 |      2.18 |       64.82 |        0.97 |            1.51 |  7.92 |   1.49 |    0.01 |   0.01 |           0.04 |            0.02 | direct      |
| **[_direct_] inherently~flawed**      |    61 |    0.04 |    3.74 |   0.04 |    293.38 | inherently | flawed      |  8,614 |  1,580 | 6,347,362 |      2.14 |       58.86 |        0.96 |            1.48 |  7.54 |   1.45 |    0.01 |   0.01 |           0.04 |            0.02 | direct      |
| **[_mirror_] inherently~evil**        |    64 |    0.13 |    3.64 |   0.13 |    290.01 | inherently | evil        |  3,342 |    479 |   583,470 |      2.74 |       61.26 |        0.96 |            1.44 |  7.66 |   1.37 |    0.02 |   0.02 |           0.13 |            0.07 | mirror      |
| **[_direct_] inherently~problematic** |    72 |    0.03 |    3.37 |   0.03 |    301.21 | inherently | problematic |  8,614 |  2,572 | 6,347,362 |      3.49 |       68.51 |        0.95 |            1.33 |  8.07 |   1.31 |    0.01 |   0.01 |           0.03 |            0.02 | direct      |
| **[_direct_] inherently~negative**    |    87 |    0.02 |    3.02 |   0.02 |    312.43 | inherently | negative    |  8,614 |  4,240 | 6,347,362 |      5.75 |       81.25 |        0.93 |            1.19 |  8.71 |   1.18 |    0.01 |   0.01 |           0.02 |            0.01 | direct      |
| **[_direct_] inherently~dangerous**   |   277 |    0.01 |    2.99 |   0.02 |    838.61 | inherently | dangerous   |  8,614 | 18,450 | 6,347,362 |     25.04 |      251.96 |        0.91 |            1.06 | 15.14 |   1.04 |    0.03 |   0.03 |           0.03 |            0.02 | direct      |
| **[_direct_] inherently~illegal**     |    60 |    0.02 |    2.50 |   0.02 |    192.56 | inherently | illegal     |  8,614 |  3,580 | 6,347,362 |      4.86 |       55.14 |        0.92 |            1.10 |  7.12 |   1.09 |    0.01 |   0.01 |           0.02 |            0.01 | direct      |


### 1. _inherently evil_


|                                                | `token_str`                                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_042.4225_x0670205_08:11-12-13`** | Thing , " I argued that the Silo Mentality is n't __`inherently evil`__ .                                                                                                                                                                                   |
| **`pcc_eng_19_012.0140_x0177948_17:42-43`**    | So , I guess the thing I found odd was Mozilla appears to be building something very similar to Adobe AIR ( which is fine and cool ) , but somehow it is inherently good when Mozilla does it , and __`inherently evil`__ when Adobe does it .              |
| **`pcc_eng_23_095.2839_x1523991_3:4-5-6`**     | Insurance companies are n't __`inherently evil`__ .                                                                                                                                                                                                         |
| **`pcc_eng_09_049.6170_x0786566_24:5-6-7`**    | Then again there 's nothing __`inherently Evil`__ about the item .                                                                                                                                                                                          |
| **`pcc_eng_27_070.5441_x1124480_17:29-30`**    | 8 . Another point that I find issue with is how she keeps on insisting that bloggers should have a sense of ethics , that advertorial masking is __`inherently evil`__ and how bloggers who engage in such methods deserve the harshest punishment of all . |
| **`pcc_eng_09_032.9374_x0517044_18:3-4-5`**    | Anger is n't __`inherently evil`__ or bad but when someone is blinded by it , there is a clear sign of disconnection from reality .                                                                                                                         |
| **`pcc_eng_29_105.3243_x1685827_069:17-18`**   | No amount of cultural relativism can ease the pain of people who have been victimized by __`inherently evil`__ cultural practices .                                                                                                                         |
| **`pcc_eng_08_052.3456_x0831327_27:09-10`**    | According to the NOI , whites were an __`inherently evil`__ race created in ancient times by a sinister black scientist named Yacub .                                                                                                                       |


### 2. _inherently wrong_


|                                                 | `token_str`                                                                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_058.2445_x0925138_11:4-5-6`**     | Secondly there is nothing __`inherently wrong`__ with men .                                                                                                                                                         |
| **`pcc_eng_23_082.6110_x1318836_08:3-4-5`**     | There 's nothing __`inherently wrong`__ with casual encounters .                                                                                                                                                    |
| **`pcc_eng_24_074.1011_x1182519_056:5-6`**      | So , is it __`inherently wrong`__ to pay artists different amounts ?                                                                                                                                                |
| **`pcc_eng_00_038.6259_x0607789_08:4-5-6`**     | There would be nothing __`inherently wrong`__ with techno-social engineering if we could be absolutely certain the Internet companies that collect and analyze our data acted only in our best interests .          |
| **`pcc_eng_25_003.3552_x0038464_072:13-14-15`** | It may not be practical on multiple levels , but there is nothing __`inherently wrong`__ with a vast age difference in marriage .                                                                                   |
| **`pcc_eng_29_018.9986_x0290372_17:11-12-13`**  | It is important to understand that conflicts of interest are not __`inherently wrong`__ .                                                                                                                           |
| **`nyt_eng_19950612_0295_286:11-12`**           | he also allows that `` -LRB- n -RRB- othing is __`inherently wrong`__ with applying a single standard to fundamentally different situations , as long as that standard takes relevant differences into account . '' |
| **`pcc_eng_06_026.0581_x0405529_21:3-4-5`**     | There is nothing __`inherently wrong`__ with the camera obscura or any other mechanical aid to drawing .                                                                                                            |


### 3. _inherently racist_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                          |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_100.3695_x1605809_28:5-6`**      | Since our system is __`inherently racist`__ , we must abolish the death penalty .                                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_25_006.5091_x0089511_91:21-22-23`** | Agreed on UKIP , they 're a bit swivel - eyed and slap dash with their policies but they 're not __`inherently racist`__ per se ( they are on the other hand quite openly homophobic which is as bad . )                                                                                                                                                                                             |
| **`pcc_eng_08_108.2605_x1735403_46:6-8-9`**    | So no , we are not all __`inherently racist`__ .                                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_07_031.5458_x0494053_41:19-20`**    | But most astonishing of all is that the liberal press , which routinely accuses the Right of being __`inherently racist`__ , also condemns the Right for opposing the aborting of black babies -- on grounds that wanting more black babies to be born , and opposing a procedure that steadily diminishes the number of blacks in comparison to whites , evidently makes conservatives " racist ! " |
| **`pcc_eng_25_006.3988_x0087770_42:3-4-5`**    | It is not __`inherently racist`__ for citizens to worry whether the language and culture of their nation will be handed on to the next generation .                                                                                                                                                                                                                                                  |
| **`pcc_eng_23_092.3764_x1476849_12:14-15`**    | In the school situation , I get the impression that the principal is __`inherently racist`__ and losing her cool allowed those private thoughts to bubble up into public words and actions .                                                                                                                                                                                                         |
| **`pcc_eng_24_103.8711_x1664396_59:27-28`**    | Ms. Patrick - Odeen , who is African -American , felt the implied link between a black musical genre and the threat of increased crime was __`inherently racist`__ .                                                                                                                                                                                                                                 |
| **`pcc_eng_27_041.5818_x0655658_14:6-7`**      | It implies the country is __`inherently racist`__ , that young Germans share guilt for the Holocaust , that without patronising rules they will inevitably repeat the awful sins of their grandfathers .                                                                                                                                                                                             |


### 4. _inherently flawed_


|                                              | `token_str`                                                                                                                                                                                                       |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_074.1670_x1182189_47:10-11`**  | Numerous state officials and regulators criticize the report as __`inherently flawed`__ .                                                                                                                         |
| **`pcc_eng_21_079.3996_x1266887_22:6-7`**    | Yet , this argument is __`inherently flawed`__ because it eliminates an entire person .                                                                                                                           |
| **`pcc_eng_26_093.1512_x1490330_08:18-19`**  | One reason for this lack of foresight was uncritical admiration of financial innovation ; another was the __`inherently flawed`__ structure of the eurozone .                                                     |
| **`pcc_eng_29_095.5815_x1528031_13:09-10`**  | " Instead of insuring more people through an __`inherently flawed`__ system , we hope to purchase private insurance for as many as 175,000 more Tennesseans , " Haslam told lawmakers on Wednesday in Nashville . |
| **`pcc_eng_02_021.9262_x0338572_019:7-8`**   | They are keenly aware of the __`inherently flawed`__ nature of human thinking when left unchecked .                                                                                                               |
| **`pcc_eng_10_094.1183_x1505404_39:15-16`**  | The biggest issue with Social Security 's COLA is that the CPI -W is __`inherently flawed`__ .                                                                                                                    |
| **`pcc_eng_29_099.7127_x1594843_06:28-29`**  | The first question is whether Yale can afford to ignore its stated , legitimate concern : namely , that its early admissions program is by no means __`inherently flawed`__ .                                     |
| **`pcc_eng_07_073.9723_x1179421_043:23-24`** | Spalding must realize that the rounder argument overwhelms the ridiculous fraud of Mr. Graves and the findings of the commission which are __`inherently flawed`__ .                                              |


### 5. _inherently problematic_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                          |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_027.3458_x0425736_054:6-7-8`**   | Engaged or impassioned scholarship is not __`inherently problematic`__ , of course ; but light is as important as heat .                                                                                                                                                                                             |
| **`pcc_eng_14_008.8168_x0126131_26:16-17`**    | Expressing concerns that Moffat might be a little bit sexist due to his creation of __`inherently problematic`__ characters and saying some rather sexist things about a woman actor in Doctor Who is apparently defamation .                                                                                        |
| **`pcc_eng_11_100.2957_x1607275_21:24-25`**    | It 's too early to assess how Blair 's replacement , General James R. Clapper , will perform in a job that is __`inherently problematic`__ , given its mismatch between responsibility and power .                                                                                                                   |
| **`pcc_eng_10_076.6512_x1222701_26:22-23`**    | As Jonah Goldberg points out , 1 in 15 Black males are in prison , and there 's something systemically and __`inherently problematic`__ about the dark statistics - inasmuch that it is no longer a Black or Brown issue , but an American concern .                                                                 |
| **`pcc_eng_06_101.9856_x1633608_22:31-32-33`** | Trying to fit new kinds of energy into infrastructures not designed for them is expensive , and creates complications -- the fact that solar resources fluctuate throughout the day is n't __`inherently problematic`__ , but it is a problem when paired with an infrastructure that ca n't deal with fluctuation . |
| **`pcc_eng_09_009.2292_x0133301_22:4-5`**      | Congress is an __`inherently problematic`__ institution , populated by flawed human beings who are primarily accountable to the short-term desires of narrow interest groups .                                                                                                                                       |
| **`pcc_eng_23_005.2832_x0069089_26:16-20-21`** | We should be open to being critical about traditional western rhetorical theories and methods , not because they are __`inherently problematic`__ , but because they do n't always work for texts outside of that mold .                                                                                             |
| **`pcc_eng_11_013.3608_x0199808_21:3-8-9`**    | It 's not that the cross-cutting is __`inherently problematic`__ .                                                                                                                                                                                                                                                   |


### 6. _inherently negative_


|                                                | `token_str`                                                                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_032.3327_x0506641_15:5-6-7`**    | This in itself is not __`inherently negative`__ , aside from the fact that people are living in poverty , but can lead to conflict when the segregation extends to minority ethnic and racial groups . |
| **`pcc_eng_24_100.9946_x1617795_010:3-4-5`**   | There 's nothing __`inherently negative`__ or unexciting about laboratory work .                                                                                                                       |
| **`pcc_eng_28_062.2968_x0991699_29:16-17-18`** | Contrary to what some were saying in 2010 , a quarterback rotation in itself is not __`inherently negative`__ for those involved .                                                                     |
| **`pcc_eng_23_006.6814_x0091752_58:7-8-9`**    | Anger , for example , is not __`inherently negative`__ .                                                                                                                                               |
| **`pcc_eng_19_057.8152_x0917063_45:16-17`**    | Weve fought off so many bad things that people have started viewing any change as __`inherently negative`__ .                                                                                          |
| **`pcc_eng_26_038.9822_x0614179_42:11-12-13`** | An individual may experience an impairment , but this is not __`inherently negative`__ .                                                                                                               |
| **`pcc_eng_17_017.6032_x0268681_07:12-13`**    | This environment creates openings for populists to peddle policies that are __`inherently negative`__ , protectionist and divisive .                                                                   |
| **`pcc_eng_10_028.9549_x0451869_10:20-21-22`** | This is because unemployment checks are a type of benefit intended for individuals who need it ; there 's nothing __`inherently negative`__ about seeking a financial cushion following job loss .     |


### 7. _inherently dangerous_


|                                              | `token_str`                                                                                                                                                    |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_002.5851_x0025649_13:7-8-9`**  | The fact that the article is not __`inherently dangerous`__ if properly made is immaterial .                                                                   |
| **`pcc_eng_02_057.2298_x0909606_03:8-9`**    | Please be aware that climbing is an __`inherently dangerous`__ sport .                                                                                         |
| **`pcc_eng_23_051.1228_x0809645_09:18-19`**  | Many owners among the 52,000 horses in Connecticut were scared by the ruling that declared horses are __`inherently dangerous`__ .                             |
| **`pcc_eng_24_007.7209_x0108251_17:10-11`**  | " The job of the Peace Corps volunteer is __`inherently dangerous`__ , " said Rep.                                                                             |
| **`pcc_eng_09_031.9380_x0500815_112:8-9`**   | The ski resort had set up and __`inherently dangerous`__ competition during which alcohol was served .                                                         |
| **`pcc_eng_11_085.9233_x1374653_011:19-20`** | As Richard Hill states in Observe and Understand the Sun : " Observing the sun is the only __`inherently dangerous`__ observing an amateur astronomer can do . |
| **`pcc_eng_10_082.3023_x1313878_450:3-4-5`** | Bicycling is not __`inherently dangerous`__ , but in the city streets a network of aid can be tremendously helpful .                                           |
| **`pcc_eng_02_101.4585_x1624398_23:17-18`**  | No municipality , city planner , or civil engineer would intentionally build a road that was __`inherently dangerous`__ .                                      |


### 8. _inherently illegal_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                     |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_030.8763_x0484001_11:4-5-6`**    | While there 's nothing __`inherently illegal`__ about an arranged marriage .                                                                                                                                                                                                                                                                    |
| **`pcc_eng_03_005.3203_x0069828_46:10-11-12`** | Taking that difference one step further , there was nothing __`inherently illegal`__ in the quest for information on Manafort and how that might link Donald Trump to Russia .                                                                                                                                                                  |
| **`pcc_eng_11_063.1843_x1006356_04:17-18-19`** | On the plus side , Obama correctly emphasized that the use of drones against terrorists is not __`inherently illegal`__ nor immoral , that drones are often more discriminating and less likely to inflict civilian casualties than other military tactics , and that US citizens can be legitimate targets when they become enemy combatants . |
| **`pcc_eng_29_098.1170_x1569081_15:7-8-9`**    | Holding offshore companies and accounts is not __`inherently illegal`__ but they can be used to hide assets from the taxman or to launder money from illicit sources .                                                                                                                                                                          |
| **`pcc_eng_14_038.6784_x0608659_17:19-20-21`** | The foundation , while accepting his resignation , quoted from the indictment which said that " Bitcoin are not __`inherently illegal`__ and have known legitimate uses . "                                                                                                                                                                     |
| **`pcc_eng_17_101.7170_x1628000_29:20-21-22`** | The distrubutor argued that vertical agreements -- those involving companies in different levels of the supply chain -- are not __`inherently illegal`__ .                                                                                                                                                                                      |
| **`nyt_eng_19980311_0164_15:5-6-7`**           | becoming a monopoly is not __`inherently illegal`__ .                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_15_097.1646_x1554298_14:5-6-7`**    | A prohibited device is not __`inherently illegal`__ in Canada but it does require an uncommon and very specific prohibited device license for its possession , use , and transport .                                                                                                                                                            |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/`...

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_evil_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_wrong_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_racist_80ex~41.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_flawed_80ex~40.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_problematic_80ex~31.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_negative_80ex~36.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_dangerous_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/NEQ/any_bigram_examples/inherently/inherently_illegal_80ex~17.csv`

