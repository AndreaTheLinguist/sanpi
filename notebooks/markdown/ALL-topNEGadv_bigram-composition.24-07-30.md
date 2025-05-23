```python
from am_notebooks import *

from source.utils import HIT_TABLES_DIR
from source.utils.associate import TOP_AM_DIR

TAG='ALL'
K=8
BK = max(K+2, 10)
BIGRAM_F_FLOOR=50 if TAG == 'ALL' else 25

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
> `/share/compling/projects/sanpi/results/top_AM/ALL/ALL-Top8/ALL-Top8_NEG-ADV_combined-5000.2024-07-30.csv`



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
1. inherently
1. terribly



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
    │        │ AdvAdj_ALL_any-mirror_final-freq_min50x_extra.parq                       │
    ├────────┼──────────────────────────────────────────────────────────────────────────┤
    │ direct │ /share/compling/projects/sanpi/results/assoc_df/adv_adj/ANYdirect/extra/ │
    │        │ AdvAdj_ALL_any-direct_final-freq_min50x_extra.parq                       │
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
    print(f'\n### Loading `{blam_kind}` AM scores\n\n Path: `{blam_path.relative_to(AM_DF_DIR.parent)}`\n')
    blamin = pd.read_parquet(
        blam_path, engine='pyarrow',
        filters=[('l1', 'in', adv_list)],
        columns=FOCUS_DICT[TAG]['adv_adj'])
    blamin['dataset']=blam_kind
    blamin = catify(adjust_am_names(blamin),
                    reverse=True)
    
    for peek_metric in blind_priority_cols:
        nb_show_table(peek_am(peek_metric, blamin).filter(blind_priority_cols), n_dec=3)
    blamin.index = f'[_{blam_kind}_] ' + blamin.index
    blam_dfs[blam_kind] = blamin
```


### Loading `mirror` AM scores

 Path: `assoc_df/adv_adj/ANYmirror/extra/AdvAdj_ALL_any-mirror_final-freq_min50x_extra.parq`


_Bigrams with the highest `LRC` value for each adverb_


|                              |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:-----------------------------|--------:|----------------:|---------------:|------------:|
| **exactly~alike**            |   7.793 |           0.147 |          0.210 |       0.997 |
| **immediately~recognizable** |   5.980 |           0.069 |          0.090 |       0.992 |
| **any~closer**               |   5.679 |           0.063 |          0.069 |       0.990 |
| **terribly~wrong**           |   4.859 |           0.222 |          0.363 |       0.967 |
| **inherently~wrong**         |   4.797 |           0.215 |          0.345 |       0.966 |
| **particularly~noteworthy**  |   4.227 |           0.107 |          0.207 |       0.964 |
| **ever~certain**             |   4.147 |           0.052 |          0.077 |       0.963 |
| **that~great**               |   3.895 |           0.059 |          0.059 |       0.947 |
| **necessarily~wrong**        |   3.455 |           0.096 |          0.183 |       0.937 |
| **remotely~close**           |   3.339 |           0.062 |          0.106 |       0.929 |


_Bigrams with the highest `deltaP_mean` value for each adverb_


|                             |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:----------------------------|--------:|----------------:|---------------:|------------:|
| **terribly~wrong**          |   4.859 |           0.222 |          0.363 |       0.967 |
| **inherently~wrong**        |   4.797 |           0.215 |          0.345 |       0.966 |
| **any~better**              |   5.061 |           0.186 |          0.342 |       0.976 |
| **exactly~alike**           |   7.793 |           0.147 |          0.210 |       0.997 |
| **immediately~available**   |   4.802 |           0.125 |          0.224 |       0.974 |
| **particularly~noteworthy** |   4.227 |           0.107 |          0.207 |       0.964 |
| **necessarily~wrong**       |   3.455 |           0.096 |          0.183 |       0.937 |
| **remotely~close**          |   3.339 |           0.062 |          0.106 |       0.929 |
| **that~great**              |   3.895 |           0.059 |          0.059 |       0.947 |
| **ever~certain**            |   4.147 |           0.052 |          0.077 |       0.963 |


_Bigrams with the highest `deltaP_max` value for each adverb_


|                             |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:----------------------------|--------:|----------------:|---------------:|------------:|
| **terribly~wrong**          |   4.859 |           0.222 |          0.363 |       0.967 |
| **inherently~wrong**        |   4.797 |           0.215 |          0.345 |       0.966 |
| **any~better**              |   5.061 |           0.186 |          0.342 |       0.976 |
| **immediately~available**   |   4.802 |           0.125 |          0.224 |       0.974 |
| **exactly~alike**           |   7.793 |           0.147 |          0.210 |       0.997 |
| **particularly~noteworthy** |   4.227 |           0.107 |          0.207 |       0.964 |
| **necessarily~wrong**       |   3.455 |           0.096 |          0.183 |       0.937 |
| **remotely~close**          |   3.339 |           0.062 |          0.106 |       0.929 |
| **that~good**               |   2.295 |           0.055 |          0.094 |       0.834 |
| **ever~certain**            |   4.147 |           0.052 |          0.077 |       0.963 |


_Bigrams with the highest `unexp_r` value for each adverb_


|                              |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:-----------------------------|--------:|----------------:|---------------:|------------:|
| **exactly~alike**            |   7.793 |           0.147 |          0.210 |       0.997 |
| **immediately~recognizable** |   5.980 |           0.069 |          0.090 |       0.992 |
| **any~closer**               |   5.679 |           0.063 |          0.069 |       0.990 |
| **terribly~amiss**           |   3.986 |           0.050 |          0.089 |       0.970 |
| **inherently~wrong**         |   4.797 |           0.215 |          0.345 |       0.966 |
| **particularly~noteworthy**  |   4.227 |           0.107 |          0.207 |       0.964 |
| **ever~certain**             |   4.147 |           0.052 |          0.077 |       0.963 |
| **that~great**               |   3.895 |           0.059 |          0.059 |       0.947 |
| **necessarily~wrong**        |   3.455 |           0.096 |          0.183 |       0.937 |
| **remotely~related**         |   2.970 |           0.024 |          0.029 |       0.935 |


### Loading `direct` AM scores

 Path: `assoc_df/adv_adj/ANYdirect/extra/AdvAdj_ALL_any-direct_final-freq_min50x_extra.parq`


_Bigrams with the highest `LRC` value for each adverb_


|                             |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:----------------------------|--------:|----------------:|---------------:|------------:|
| **remotely~detonated**      |  12.691 |           0.440 |          0.876 |       1.000 |
| **yet~unborn**              |  10.135 |           0.360 |          0.715 |       0.998 |
| **inherently~governmental** |   8.919 |           0.169 |          0.332 |       0.998 |
| **immediately~accretive**   |   8.539 |           0.226 |          0.450 |       0.997 |
| **exactly~alike**           |   8.461 |           0.145 |          0.243 |       0.997 |
| **that~purported**          |   8.416 |           0.391 |          0.782 |       0.996 |
| **ever~olympic**            |   8.231 |           0.222 |          0.442 |       0.996 |
| **necessarily~indicative**  |   8.025 |           0.100 |          0.171 |       0.996 |
| **terribly~awry**           |   8.019 |           0.131 |          0.259 |       0.997 |
| **any~happier**             |   6.748 |           0.043 |          0.058 |       0.992 |
| **particularly~hard-hit**   |   5.642 |           0.194 |          0.387 |       0.982 |


_Bigrams with the highest `deltaP_mean` value for each adverb_


|                             |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:----------------------------|--------:|----------------:|---------------:|------------:|
| **remotely~detonated**      |  12.691 |           0.440 |          0.876 |       1.000 |
| **that~purported**          |   8.416 |           0.391 |          0.782 |       0.996 |
| **yet~unborn**              |  10.135 |           0.360 |          0.715 |       0.998 |
| **immediately~appealable**  |   8.409 |           0.273 |          0.545 |       0.998 |
| **ever~quarterly**          |   8.049 |           0.224 |          0.446 |       0.997 |
| **particularly~hard-hit**   |   5.642 |           0.194 |          0.387 |       0.982 |
| **any~better**              |   5.227 |           0.171 |          0.325 |       0.974 |
| **inherently~governmental** |   8.919 |           0.169 |          0.332 |       0.998 |
| **exactly~alike**           |   8.461 |           0.145 |          0.243 |       0.997 |
| **terribly~awry**           |   8.019 |           0.131 |          0.259 |       0.997 |
| **necessarily~indicative**  |   8.025 |           0.100 |          0.171 |       0.996 |


_Bigrams with the highest `deltaP_max` value for each adverb_


|                             |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:----------------------------|--------:|----------------:|---------------:|------------:|
| **remotely~detonated**      |  12.691 |           0.440 |          0.876 |       1.000 |
| **that~purported**          |   8.416 |           0.391 |          0.782 |       0.996 |
| **yet~unborn**              |  10.135 |           0.360 |          0.715 |       0.998 |
| **immediately~appealable**  |   8.409 |           0.273 |          0.545 |       0.998 |
| **ever~quarterly**          |   8.049 |           0.224 |          0.446 |       0.997 |
| **particularly~hard-hit**   |   5.642 |           0.194 |          0.387 |       0.982 |
| **inherently~governmental** |   8.919 |           0.169 |          0.332 |       0.998 |
| **any~better**              |   5.227 |           0.171 |          0.325 |       0.974 |
| **terribly~awry**           |   8.019 |           0.131 |          0.259 |       0.997 |
| **exactly~alike**           |   8.461 |           0.145 |          0.243 |       0.997 |
| **necessarily~indicative**  |   8.025 |           0.100 |          0.171 |       0.996 |


_Bigrams with the highest `unexp_r` value for each adverb_


|                             |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:----------------------------|--------:|----------------:|---------------:|------------:|
| **remotely~detonated**      |  12.691 |           0.440 |          0.876 |       1.000 |
| **yet~unborn**              |  10.135 |           0.360 |          0.715 |       0.998 |
| **inherently~governmental** |   8.919 |           0.169 |          0.332 |       0.998 |
| **immediately~appealable**  |   8.409 |           0.273 |          0.545 |       0.998 |
| **terribly~awry**           |   8.019 |           0.131 |          0.259 |       0.997 |
| **exactly~alike**           |   8.461 |           0.145 |          0.243 |       0.997 |
| **ever~quarterly**          |   8.049 |           0.224 |          0.446 |       0.997 |
| **that~purported**          |   8.416 |           0.391 |          0.782 |       0.996 |
| **necessarily~indicative**  |   8.025 |           0.100 |          0.171 |       0.996 |
| **any~happier**             |   6.748 |           0.043 |          0.058 |       0.992 |
| **particularly~hard-hit**   |   5.642 |           0.194 |          0.387 |       0.982 |




```python
blam_df = pd.concat(blam_dfs.values()).sort_values(blind_priority_cols[0], ascending=False)
print(f'### Top 15 *context-blind* `{blind_priority_cols[0]}` values across all adverbs and datasets\n')
nb_show_table(blam_df.head(15))
```

### Top 15 *context-blind* `LRC` values across all adverbs and datasets


|                                        |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`        | `l2`         |    `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:---------------------------------------|------:|--------:|--------:|-------:|----------:|:------------|:-------------|--------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] remotely~detonated**      |    78 |    0.88 |   12.69 |   0.88 |  1,243.75 | remotely    | detonated    |  16,426 |     89 | 72,839,571 |      0.02 |       77.98 |        1.00 |            4.48 |  8.83 |   3.59 |    0.00 |   0.00 |           0.88 |            0.44 | direct      |
| **[_direct_] yet~unborn**              |   372 |    0.72 |   10.14 |   0.72 |  4,319.00 | yet         | unborn       |  95,763 |    519 | 72,839,571 |      0.68 |      371.32 |        1.00 |            3.28 | 19.25 |   2.74 |    0.00 |   0.00 |           0.72 |            0.36 | direct      |
| **[_direct_] inherently~governmental** |   253 |    0.33 |    8.92 |   0.33 |  2,742.59 | inherently  | governmental |  47,803 |    761 | 72,839,571 |      0.50 |      252.50 |        1.00 |            2.88 | 15.87 |   2.70 |    0.01 |   0.01 |           0.33 |            0.17 | direct      |
| **[_direct_] remotely~exploitable**    |   145 |    0.15 |    8.79 |   0.15 |  1,613.38 | remotely    | exploitable  |  16,426 |    986 | 72,839,571 |      0.22 |      144.78 |        1.00 |            2.89 | 12.02 |   2.81 |    0.01 |   0.01 |           0.15 |            0.08 | direct      |
| **[_direct_] immediately~accretive**   |   236 |    0.45 |    8.54 |   0.45 |  2,406.67 | immediately | accretive    |  96,973 |    523 | 72,839,571 |      0.70 |      235.30 |        1.00 |            2.79 | 15.32 |   2.53 |    0.00 |   0.00 |           0.45 |            0.23 | direct      |
| **[_direct_] exactly~alike**           | 2,768 |    0.24 |    8.46 |   0.24 | 26,963.37 | exactly     | alike        |  58,643 | 11,375 | 72,839,571 |      9.16 |    2,758.84 |        1.00 |            2.62 | 52.44 |   2.48 |    0.05 |   0.05 |           0.24 |            0.14 | direct      |
| **[_direct_] that~purported**          |    73 |    0.78 |    8.42 |   0.78 |    758.47 | that        | purported    | 208,262 |     93 | 72,839,571 |      0.27 |       72.73 |        1.00 |            3.10 |  8.51 |   2.44 |    0.00 |   0.00 |           0.78 |            0.39 | direct      |
| **[_direct_] immediately~appealable**  |    76 |    0.55 |    8.41 |   0.55 |    815.23 | immediately | appealable   |  96,973 |    139 | 72,839,571 |      0.19 |       75.81 |        1.00 |            2.96 |  8.70 |   2.61 |    0.00 |   0.00 |           0.55 |            0.27 | direct      |
| **[_direct_] immediately~adjacent**    | 1,595 |    0.33 |    8.31 |   0.34 | 15,089.64 | immediately | adjacent     |  96,973 |  4,756 | 72,839,571 |      6.33 |    1,588.67 |        1.00 |            2.59 | 39.78 |   2.40 |    0.02 |   0.02 |           0.33 |            0.18 | direct      |
| **[_direct_] yet~unnamed**             |   736 |    0.35 |    8.29 |   0.35 |  7,048.15 | yet         | unnamed      |  95,763 |  2,107 | 72,839,571 |      2.77 |      733.23 |        1.00 |            2.61 | 27.03 |   2.42 |    0.01 |   0.01 |           0.35 |            0.18 | direct      |
| **[_direct_] ever~olympic**            |   218 |    0.44 |    8.23 |   0.44 |  2,141.80 | ever        | olympic      | 114,075 |    492 | 72,839,571 |      0.77 |      217.23 |        1.00 |            2.71 | 14.71 |   2.45 |    0.00 |   0.00 |           0.44 |            0.22 | direct      |
| **[_direct_] ever~quarterly**          |   137 |    0.45 |    8.05 |   0.45 |  1,349.65 | ever        | quarterly    | 114,075 |    306 | 72,839,571 |      0.48 |      136.52 |        1.00 |            2.71 | 11.66 |   2.46 |    0.00 |   0.00 |           0.45 |            0.22 | direct      |
| **[_direct_] necessarily~indicative**  | 1,400 |    0.17 |    8.03 |   0.17 | 13,028.00 | necessarily | indicative   |  48,947 |  8,148 | 72,839,571 |      5.48 |    1,394.52 |        1.00 |            2.50 | 37.27 |   2.41 |    0.03 |   0.03 |           0.17 |            0.10 | direct      |
| **[_direct_] terribly~awry**           |   180 |    0.26 |    8.02 |   0.26 |  1,770.97 | terribly    | awry         |  58,964 |    692 | 72,839,571 |      0.56 |      179.44 |        1.00 |            2.64 | 13.37 |   2.51 |    0.00 |   0.00 |           0.26 |            0.13 | direct      |
| **[_direct_] yet~unspecified**         |   204 |    0.33 |    7.86 |   0.34 |  1,933.20 | yet         | unspecified  |  95,763 |    607 | 72,839,571 |      0.80 |      203.20 |        1.00 |            2.59 | 14.23 |   2.41 |    0.00 |   0.00 |           0.33 |            0.17 | direct      |




```python
nb_show_table(blam_df
              .filter(like='mirror', axis=0)
              .sample(5)
              .filter(blind_priority_cols)
              .sort_values(blind_priority_cols[0], ascending=False))
```

```python
nb_show_table(blam_df
              .filter(like='mirror', axis=0)
              .sample(5)
              .filter(blind_priority_cols)
              .sort_values(blind_priority_cols[0], ascending=False))
```


|                                  |   `LRC` |   `deltaP_mean` |   `deltaP_max` |   `unexp_r` |
|:---------------------------------|--------:|----------------:|---------------:|------------:|
| **[_mirror_] ever~enough**       |    3.64 |            0.04 |           0.05 |        0.95 |
| **[_mirror_] remotely~possible** |    2.39 |            0.02 |           0.02 |        0.92 |
| **[_mirror_] that~interested**   |    0.29 |            0.01 |           0.01 |        0.60 |
| **[_mirror_] terribly~new**      |    0.03 |            0.01 |           0.01 |        0.51 |
| **[_mirror_] particularly~hard** |    0.00 |            0.00 |           0.00 |        0.33 |






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

|                                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] necessarily~indicative**     |    8.03 | 13,028.00 |           0.17 |            0.10 |    0.17 |    0.03 | 1,400 |     8,148 |        1.00 |
| **[_direct_] necessarily~cause**          |    5.46 |    383.88 |           0.07 |            0.04 |    0.07 |    0.00 |    52 |       743 |        0.99 |
| **[_direct_] necessarily~representative** |    4.97 |  2,685.16 |           0.03 |            0.02 |    0.03 |    0.01 |   492 |    18,355 |        0.97 |
| **[_direct_] necessarily~common**         |   -1.74 |   -396.47 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    51 |   514,723 |       -5.78 |
| **[_direct_] necessarily~more**           |   -2.03 |   -716.14 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    85 |   903,653 |       -6.14 |
| **[_direct_] necessarily~important**      |   -2.06 | -1,465.12 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   229 | 2,016,665 |       -4.92 |

#### 1.2. _necessarily_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                       |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:--------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] necessarily~true**       |    4.35 | 15,129.32 |           0.07 |            0.04 |    0.01 |    0.07 | 3,460 |   231,639 |        0.96 |
| **[_direct_] necessarily~indicative** |    8.03 | 13,028.00 |           0.17 |            0.10 |    0.17 |    0.03 | 1,400 |     8,148 |        1.00 |
| **[_direct_] necessarily~bad**        |    2.75 |  5,144.57 |           0.04 |            0.02 |    0.00 |    0.04 | 2,187 |   429,537 |        0.87 |
| **[_direct_] necessarily~popular**    |   -1.71 |   -537.88 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    92 |   770,759 |       -4.63 |
| **[_direct_] necessarily~more**       |   -2.03 |   -716.14 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    85 |   903,653 |       -6.14 |
| **[_direct_] necessarily~important**  |   -2.06 | -1,465.12 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   229 | 2,016,665 |       -4.92 |

#### 1.3. _necessarily_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] necessarily~indicative**     |    8.03 | 13,028.00 |           0.17 |            0.10 |    0.17 |    0.03 | 1,400 |     8,148 |        1.00 |
| **[_direct_] necessarily~cause**          |    5.46 |    383.88 |           0.07 |            0.04 |    0.07 |    0.00 |    52 |       743 |        0.99 |
| **[_direct_] necessarily~representative** |    4.97 |  2,685.16 |           0.03 |            0.02 |    0.03 |    0.01 |   492 |    18,355 |        0.97 |
| **[_direct_] necessarily~common**         |   -1.74 |   -396.47 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    51 |   514,723 |       -5.78 |
| **[_direct_] necessarily~more**           |   -2.03 |   -716.14 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    85 |   903,653 |       -6.14 |
| **[_direct_] necessarily~important**      |   -2.06 | -1,465.12 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   229 | 2,016,665 |       -4.92 |

#### 1.4. _necessarily_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_mirror_] necessarily~wrong**     |    3.45 |    832.35 |           0.18 |            0.10 |    0.01 |    0.18 |   216 |    20,880 |        0.94 |
| **[_direct_] necessarily~true**      |    4.35 | 15,129.32 |           0.07 |            0.04 |    0.01 |    0.07 | 3,460 |   231,639 |        0.96 |
| **[_mirror_] necessarily~true**      |    2.76 |    210.11 |           0.05 |            0.03 |    0.01 |    0.05 |    59 |     6,191 |        0.93 |
| **[_direct_] necessarily~common**    |   -1.74 |   -396.47 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    51 |   514,723 |       -5.78 |
| **[_direct_] necessarily~more**      |   -2.03 |   -716.14 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    85 |   903,653 |       -6.14 |
| **[_direct_] necessarily~important** |   -2.06 | -1,465.12 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   229 | 2,016,665 |       -4.92 |


---

### 2. Sampling _that_ context-blind bigram AMs

#### 2.1. _that_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] that~purported**  |    8.42 |    758.47 |           0.78 |            0.39 |    0.78 |    0.00 |    73 |      93 |        1.00 |
| **[_direct_] that~uncommon**   |    4.43 |  3,680.42 |           0.07 |            0.04 |    0.07 |    0.00 |   804 |  11,312 |        0.96 |
| **[_direct_] that~dissimilar** |    4.13 |  1,365.55 |           0.06 |            0.03 |    0.06 |    0.00 |   307 |   4,605 |        0.96 |
| **[_direct_] that~easier**     |   -2.18 |   -749.58 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    73 | 209,940 |       -7.22 |
| **[_direct_] that~better**     |   -2.42 | -2,161.56 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |   237 | 625,733 |       -6.55 |
| **[_direct_] that~likely**     |   -3.75 | -4,172.31 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |   117 | 890,421 |      -20.76 |

#### 2.2. _that_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] that~bad**    |    4.01 | 74,955.42 |           0.09 |            0.07 |    0.04 |    0.09 | 19,708 |   429,537 |        0.94 |
| **[_direct_] that~great**  |    3.71 | 40,195.14 |           0.05 |            0.04 |    0.04 |    0.05 | 11,781 |   309,258 |        0.92 |
| **[_direct_] that~easy**   |    2.91 | 30,976.20 |           0.05 |            0.04 |    0.02 |    0.05 | 12,825 |   579,827 |        0.87 |
| **[_direct_] that~better** |   -2.42 | -2,161.56 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    237 |   625,733 |       -6.55 |
| **[_direct_] that~likely** |   -3.75 | -4,172.31 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    117 |   890,421 |      -20.76 |
| **[_direct_] that~many**   |   -1.94 | -4,767.75 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |  1,179 | 1,848,723 |       -3.48 |

#### 2.3. _that_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |    `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|--------:|------------:|
| **[_direct_] that~purported**  |    8.42 |    758.47 |           0.78 |            0.39 |    0.78 |    0.00 |    73 |      93 |        1.00 |
| **[_direct_] that~uncommon**   |    4.43 |  3,680.42 |           0.07 |            0.04 |    0.07 |    0.00 |   804 |  11,312 |        0.96 |
| **[_direct_] that~farfetched** |    3.75 |    423.24 |           0.07 |            0.03 |    0.07 |    0.00 |    93 |   1,324 |        0.96 |
| **[_direct_] that~easier**     |   -2.18 |   -749.58 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    73 | 209,940 |       -7.22 |
| **[_direct_] that~better**     |   -2.42 | -2,161.56 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |   237 | 625,733 |       -6.55 |
| **[_direct_] that~likely**     |   -3.75 | -4,172.31 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |   117 | 890,421 |      -20.76 |

#### 2.4. _that_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] that~bad**    |    4.01 | 74,955.42 |           0.09 |            0.07 |    0.04 |    0.09 | 19,708 |   429,537 |        0.94 |
| **[_mirror_] that~good**   |    2.29 |  1,239.46 |           0.09 |            0.06 |    0.02 |    0.09 |    614 |    31,585 |        0.83 |
| **[_mirror_] that~easy**   |    2.76 |  1,322.20 |           0.08 |            0.05 |    0.02 |    0.08 |    508 |    18,610 |        0.88 |
| **[_direct_] that~better** |   -2.42 | -2,161.56 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    237 |   625,733 |       -6.55 |
| **[_direct_] that~likely** |   -3.75 | -4,172.31 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    117 |   890,421 |      -20.76 |
| **[_direct_] that~many**   |   -1.94 | -4,767.75 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |  1,179 | 1,848,723 |       -3.48 |


---

### 3. Sampling _exactly_ context-blind bigram AMs

#### 3.1. _exactly_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                 |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:--------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] exactly~alike**    |    8.46 | 26,963.37 |           0.24 |            0.14 |    0.24 |    0.05 | 2,768 |    11,375 |        1.00 |
| **[_mirror_] exactly~alike**    |    7.79 |    880.53 |           0.21 |            0.15 |    0.21 |    0.08 |    88 |       417 |        1.00 |
| **[_direct_] exactly~opposite** |    5.76 |  3,028.33 |           0.05 |            0.03 |    0.05 |    0.01 |   464 |     8,491 |        0.99 |
| **[_direct_] exactly~good**     |   -1.78 | -1,263.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   287 | 1,681,795 |       -3.72 |
| **[_direct_] exactly~much**     |   -3.37 | -1,771.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    52 | 1,349,399 |      -19.89 |
| **[_direct_] exactly~many**     |   -3.77 | -2,540.81 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    55 | 1,848,723 |      -26.06 |

#### 3.2. _exactly_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] exactly~sure**  |    5.40 | 52,863.18 |           0.15 |            0.09 |    0.03 |    0.15 | 9,157 |   262,825 |        0.98 |
| **[_direct_] exactly~right** |    5.74 | 39,191.64 |           0.11 |            0.07 |    0.04 |    0.11 | 6,323 |   143,095 |        0.98 |
| **[_direct_] exactly~alike** |    8.46 | 26,963.37 |           0.24 |            0.14 |    0.24 |    0.05 | 2,768 |    11,375 |        1.00 |
| **[_direct_] exactly~good**  |   -1.78 | -1,263.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   287 | 1,681,795 |       -3.72 |
| **[_direct_] exactly~much**  |   -3.37 | -1,771.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    52 | 1,349,399 |      -19.89 |
| **[_direct_] exactly~many**  |   -3.77 | -2,540.81 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    55 | 1,848,723 |      -26.06 |

#### 3.3. _exactly_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                 |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:--------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] exactly~alike**    |    8.46 | 26,963.37 |           0.24 |            0.14 |    0.24 |    0.05 | 2,768 |    11,375 |        1.00 |
| **[_mirror_] exactly~alike**    |    7.79 |    880.53 |           0.21 |            0.15 |    0.21 |    0.08 |    88 |       417 |        1.00 |
| **[_direct_] exactly~opposite** |    5.76 |  3,028.33 |           0.05 |            0.03 |    0.05 |    0.01 |   464 |     8,491 |        0.99 |
| **[_direct_] exactly~good**     |   -1.78 | -1,263.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   287 | 1,681,795 |       -3.72 |
| **[_direct_] exactly~much**     |   -3.37 | -1,771.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    52 | 1,349,399 |      -19.89 |
| **[_direct_] exactly~many**     |   -3.77 | -2,540.81 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    55 | 1,848,723 |      -26.06 |

#### 3.4. _exactly_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] exactly~sure**  |    5.40 | 52,863.18 |           0.15 |            0.09 |    0.03 |    0.15 | 9,157 |   262,825 |        0.98 |
| **[_mirror_] exactly~sure**  |    4.51 |    795.30 |           0.14 |            0.08 |    0.02 |    0.14 |   148 |     6,761 |        0.97 |
| **[_mirror_] exactly~right** |    4.61 |    742.90 |           0.13 |            0.07 |    0.02 |    0.13 |   134 |     5,576 |        0.97 |
| **[_direct_] exactly~good**  |   -1.78 | -1,263.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   287 | 1,681,795 |       -3.72 |
| **[_direct_] exactly~much**  |   -3.37 | -1,771.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    52 | 1,349,399 |      -19.89 |
| **[_direct_] exactly~many**  |   -3.77 | -2,540.81 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    55 | 1,848,723 |      -26.06 |


---

### 4. Sampling _any_ context-blind bigram AMs

#### 4.1. _any_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] any~happier** |    6.75 |  7,438.55 |           0.06 |            0.04 |    0.06 |    0.03 |   963 |    16,606 |        0.99 |
| **[_direct_] any~clearer** |    6.51 |  4,556.17 |           0.05 |            0.03 |    0.05 |    0.02 |   608 |    11,680 |        0.99 |
| **[_direct_] any~closer**  |    5.74 | 10,942.35 |           0.05 |            0.04 |    0.03 |    0.05 | 1,738 |    61,475 |        0.98 |
| **[_direct_] any~smaller** |    1.28 |    208.43 |           0.00 |            0.00 |    0.00 |    0.00 |   169 |    92,123 |        0.74 |
| **[_direct_] any~greater** |    1.13 |    214.21 |           0.00 |            0.00 |    0.00 |    0.00 |   215 |   138,165 |        0.70 |
| **[_direct_] any~good**    |   -0.37 |   -148.72 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |   479 | 1,681,795 |       -0.66 |

#### 4.2. _any_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                           |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:--------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] any~better** |    5.23 | 65,861.94 |           0.32 |            0.17 |    0.02 |    0.32 | 11,460 |   625,733 |        0.97 |
| **[_direct_] any~worse**  |    5.33 | 20,994.30 |           0.10 |            0.06 |    0.02 |    0.10 |  3,673 |   179,012 |        0.98 |
| **[_direct_] any~closer** |    5.74 | 10,942.35 |           0.05 |            0.04 |    0.03 |    0.05 |  1,738 |    61,475 |        0.98 |
| **[_direct_] any~warmer** |    2.60 |    202.67 |           0.01 |            0.00 |    0.01 |    0.00 |     59 |     8,895 |        0.93 |
| **[_direct_] any~darker** |    1.69 |    128.24 |           0.00 |            0.00 |    0.00 |    0.00 |     54 |    14,615 |        0.87 |
| **[_direct_] any~good**   |   -0.37 |   -148.72 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    479 | 1,681,795 |       -0.66 |

#### 4.3. _any_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:---------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_mirror_] any~closer**  |    5.68 |   506.03 |           0.07 |            0.06 |    0.07 |    0.06 |    69 |       993 |        0.99 |
| **[_direct_] any~happier** |    6.75 | 7,438.55 |           0.06 |            0.04 |    0.06 |    0.03 |   963 |    16,606 |        0.99 |
| **[_direct_] any~clearer** |    6.51 | 4,556.17 |           0.05 |            0.03 |    0.05 |    0.02 |   608 |    11,680 |        0.99 |
| **[_direct_] any~smaller** |    1.28 |   208.43 |           0.00 |            0.00 |    0.00 |    0.00 |   169 |    92,123 |        0.74 |
| **[_direct_] any~greater** |    1.13 |   214.21 |           0.00 |            0.00 |    0.00 |    0.00 |   215 |   138,165 |        0.70 |
| **[_direct_] any~good**    |   -0.37 |  -148.72 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |   479 | 1,681,795 |       -0.66 |

#### 4.4. _any_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                            |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:---------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_mirror_] any~better**  |    5.06 |  2,497.00 |           0.34 |            0.19 |    0.03 |    0.34 |    419 |    14,013 |        0.98 |
| **[_direct_] any~better**  |    5.23 | 65,861.94 |           0.32 |            0.17 |    0.02 |    0.32 | 11,460 |   625,733 |        0.97 |
| **[_direct_] any~worse**   |    5.33 | 20,994.30 |           0.10 |            0.06 |    0.02 |    0.10 |  3,673 |   179,012 |        0.98 |
| **[_direct_] any~smaller** |    1.28 |    208.43 |           0.00 |            0.00 |    0.00 |    0.00 |    169 |    92,123 |        0.74 |
| **[_direct_] any~greater** |    1.13 |    214.21 |           0.00 |            0.00 |    0.00 |    0.00 |    215 |   138,165 |        0.70 |
| **[_direct_] any~good**    |   -0.37 |   -148.72 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    479 | 1,681,795 |       -0.66 |


---

### 5. Sampling _remotely_ context-blind bigram AMs

#### 5.1. _remotely_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                     |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] remotely~detonated**   |   12.69 | 1,243.75 |           0.88 |            0.44 |    0.88 |    0.00 |    78 |        89 |        1.00 |
| **[_direct_] remotely~exploitable** |    8.79 | 1,613.38 |           0.15 |            0.08 |    0.15 |    0.01 |   145 |       986 |        1.00 |
| **[_direct_] remotely~comparable**  |    6.15 | 2,015.00 |           0.02 |            0.02 |    0.02 |    0.02 |   277 |    12,252 |        0.99 |
| **[_direct_] remotely~successful**  |    0.00 |    -8.99 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    57 |   366,516 |       -0.45 |
| **[_direct_] remotely~likely**      |   -0.71 |  -126.12 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    65 |   890,421 |       -2.09 |
| **[_direct_] remotely~good**        |   -0.71 |  -181.66 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |   151 | 1,681,795 |       -1.51 |

#### 5.2. _remotely_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] remotely~close**      |    3.90 | 6,229.80 |           0.09 |            0.05 |    0.00 |    0.09 | 1,597 |   411,329 |        0.94 |
| **[_direct_] remotely~interested** |    3.90 | 4,177.56 |           0.06 |            0.03 |    0.00 |    0.06 | 1,062 |   264,528 |        0.94 |
| **[_direct_] remotely~related**    |    4.36 | 2,857.41 |           0.04 |            0.02 |    0.01 |    0.04 |   617 |   105,375 |        0.96 |
| **[_direct_] remotely~successful** |    0.00 |    -8.99 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |    57 |   366,516 |       -0.45 |
| **[_direct_] remotely~likely**     |   -0.71 |  -126.12 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    65 |   890,421 |       -2.09 |
| **[_direct_] remotely~good**       |   -0.71 |  -181.66 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |   151 | 1,681,795 |       -1.51 |

#### 5.3. _remotely_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                     |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] remotely~detonated**   |   12.69 | 1,243.75 |           0.88 |            0.44 |    0.88 |    0.00 |    78 |        89 |        1.00 |
| **[_direct_] remotely~exploitable** |    8.79 | 1,613.38 |           0.15 |            0.08 |    0.15 |    0.01 |   145 |       986 |        1.00 |
| **[_direct_] remotely~comparable**  |    6.15 | 2,015.00 |           0.02 |            0.02 |    0.02 |    0.02 |   277 |    12,252 |        0.99 |
| **[_direct_] remotely~new**         |    0.00 |     1.01 |           0.00 |            0.00 |    0.00 |    0.00 |    65 |   253,862 |        0.12 |
| **[_direct_] remotely~good**        |   -0.71 |  -181.66 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |   151 | 1,681,795 |       -1.51 |
| **[_direct_] remotely~likely**      |   -0.71 |  -126.12 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    65 |   890,421 |       -2.09 |

#### 5.4. _remotely_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                    |   `LRC` |     `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-----------------------------------|--------:|---------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_mirror_] remotely~close**      |    3.34 |   945.05 |           0.11 |            0.06 |    0.02 |    0.11 |   267 |    13,874 |        0.93 |
| **[_direct_] remotely~close**      |    3.90 | 6,229.80 |           0.09 |            0.05 |    0.00 |    0.09 | 1,597 |   411,329 |        0.94 |
| **[_direct_] remotely~interested** |    3.90 | 4,177.56 |           0.06 |            0.03 |    0.00 |    0.06 | 1,062 |   264,528 |        0.94 |
| **[_direct_] remotely~new**        |    0.00 |     1.01 |           0.00 |            0.00 |    0.00 |    0.00 |    65 |   253,862 |        0.12 |
| **[_direct_] remotely~good**       |   -0.71 |  -181.66 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |   151 | 1,681,795 |       -1.51 |
| **[_direct_] remotely~likely**     |   -0.71 |  -126.12 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    65 |   890,421 |       -2.09 |


---

### 6. Sampling _ever_ context-blind bigram AMs

#### 6.1. _ever_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] ever~olympic**   |    8.23 |  2,141.80 |           0.44 |            0.22 |    0.44 |    0.00 |   218 |       492 |        1.00 |
| **[_direct_] ever~quarterly** |    8.05 |  1,349.65 |           0.45 |            0.22 |    0.45 |    0.00 |   137 |       306 |        1.00 |
| **[_direct_] ever~watchful**  |    7.05 |  3,399.87 |           0.22 |            0.11 |    0.22 |    0.00 |   416 |     1,866 |        0.99 |
| **[_direct_] ever~difficult** |   -3.20 | -1,790.48 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    67 |   732,106 |      -16.11 |
| **[_direct_] ever~many**      |   -3.47 | -4,528.63 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   175 | 1,848,723 |      -15.54 |
| **[_direct_] ever~much**      |   -3.67 | -3,467.83 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    98 | 1,349,399 |      -20.56 |

#### 6.2. _ever_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] ever~closer**    |    6.08 | 41,328.73 |           0.10 |            0.08 |    0.10 |    0.05 | 6,307 |    61,475 |        0.98 |
| **[_direct_] ever~present**   |    5.59 | 41,015.56 |           0.07 |            0.07 |    0.07 |    0.06 | 6,942 |    92,777 |        0.98 |
| **[_direct_] ever~greater**   |    4.07 | 15,260.42 |           0.03 |            0.03 |    0.03 |    0.03 | 3,875 |   138,165 |        0.94 |
| **[_direct_] ever~much**      |   -3.67 | -3,467.83 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    98 | 1,349,399 |      -20.56 |
| **[_direct_] ever~important** |   -2.42 | -3,696.95 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   459 | 2,016,665 |       -5.88 |
| **[_direct_] ever~many**      |   -3.47 | -4,528.63 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   175 | 1,848,723 |      -15.54 |

#### 6.3. _ever_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] ever~quarterly** |    8.05 |  1,349.65 |           0.45 |            0.22 |    0.45 |    0.00 |   137 |       306 |        1.00 |
| **[_direct_] ever~olympic**   |    8.23 |  2,141.80 |           0.44 |            0.22 |    0.44 |    0.00 |   218 |       492 |        1.00 |
| **[_direct_] ever~watchful**  |    7.05 |  3,399.87 |           0.22 |            0.11 |    0.22 |    0.00 |   416 |     1,866 |        0.99 |
| **[_direct_] ever~difficult** |   -3.20 | -1,790.48 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    67 |   732,106 |      -16.11 |
| **[_direct_] ever~many**      |   -3.47 | -4,528.63 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   175 | 1,848,723 |      -15.54 |
| **[_direct_] ever~much**      |   -3.67 | -3,467.83 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    98 | 1,349,399 |      -20.56 |

#### 6.4. _ever_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                               |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] ever~present**   |    5.59 | 41,015.56 |           0.07 |            0.07 |    0.07 |    0.06 | 6,942 |    92,777 |        0.98 |
| **[_mirror_] ever~easy**      |    2.35 |    798.48 |           0.06 |            0.04 |    0.02 |    0.06 |   369 |    18,610 |        0.85 |
| **[_direct_] ever~closer**    |    6.08 | 41,328.73 |           0.10 |            0.08 |    0.10 |    0.05 | 6,307 |    61,475 |        0.98 |
| **[_direct_] ever~important** |   -2.42 | -3,696.95 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   459 | 2,016,665 |       -5.88 |
| **[_direct_] ever~many**      |   -3.47 | -4,528.63 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   175 | 1,848,723 |      -15.54 |
| **[_direct_] ever~much**      |   -3.67 | -3,467.83 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    98 | 1,349,399 |      -20.56 |


---

### 7. Sampling _yet_ context-blind bigram AMs

#### 7.1. _yet_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] yet~unborn**      |   10.14 |  4,319.00 |           0.72 |            0.36 |    0.72 |    0.00 |   372 |       519 |        1.00 |
| **[_direct_] yet~unnamed**     |    8.29 |  7,048.15 |           0.35 |            0.18 |    0.35 |    0.01 |   736 |     2,107 |        1.00 |
| **[_direct_] yet~unspecified** |    7.86 |  1,933.20 |           0.33 |            0.17 |    0.33 |    0.00 |   204 |       607 |        1.00 |
| **[_direct_] yet~many**        |   -3.82 | -4,064.46 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   103 | 1,848,723 |      -22.60 |
| **[_direct_] yet~much**        |   -3.84 | -3,014.74 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    66 | 1,349,399 |      -25.88 |
| **[_direct_] yet~important**   |   -4.41 | -4,750.28 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |    67 | 2,016,665 |      -38.57 |

#### 7.2. _yet_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] yet~clear**     |    4.47 | 46,878.12 |           0.10 |            0.07 |    0.03 |    0.10 | 10,476 |   349,214 |        0.96 |
| **[_direct_] yet~ready**     |    5.33 | 42,533.76 |           0.08 |            0.06 |    0.05 |    0.08 |  7,599 |   141,590 |        0.98 |
| **[_direct_] yet~available** |    3.12 | 21,869.30 |           0.07 |            0.04 |    0.01 |    0.07 |  8,025 |   666,909 |        0.89 |
| **[_direct_] yet~much**      |   -3.84 | -3,014.74 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |     66 | 1,349,399 |      -25.88 |
| **[_direct_] yet~many**      |   -3.82 | -4,064.46 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    103 | 1,848,723 |      -22.60 |
| **[_direct_] yet~important** |   -4.41 | -4,750.28 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |     67 | 2,016,665 |      -38.57 |

#### 7.3. _yet_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:-------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] yet~unborn**      |   10.14 |  4,319.00 |           0.72 |            0.36 |    0.72 |    0.00 |   372 |       519 |        1.00 |
| **[_direct_] yet~unnamed**     |    8.29 |  7,048.15 |           0.35 |            0.18 |    0.35 |    0.01 |   736 |     2,107 |        1.00 |
| **[_direct_] yet~unspecified** |    7.86 |  1,933.20 |           0.33 |            0.17 |    0.33 |    0.00 |   204 |       607 |        1.00 |
| **[_direct_] yet~many**        |   -3.82 | -4,064.46 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |   103 | 1,848,723 |      -22.60 |
| **[_direct_] yet~much**        |   -3.84 | -3,014.74 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    66 | 1,349,399 |      -25.88 |
| **[_direct_] yet~important**   |   -4.41 | -4,750.28 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |    67 | 2,016,665 |      -38.57 |

#### 7.4. _yet_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                              |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:-----------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] yet~clear**     |    4.47 | 46,878.12 |           0.10 |            0.07 |    0.03 |    0.10 | 10,476 |   349,214 |        0.96 |
| **[_direct_] yet~ready**     |    5.33 | 42,533.76 |           0.08 |            0.06 |    0.05 |    0.08 |  7,599 |   141,590 |        0.98 |
| **[_direct_] yet~available** |    3.12 | 21,869.30 |           0.07 |            0.04 |    0.01 |    0.07 |  8,025 |   666,909 |        0.89 |
| **[_direct_] yet~many**      |   -3.82 | -4,064.46 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    103 | 1,848,723 |      -22.60 |
| **[_direct_] yet~much**      |   -3.84 | -3,014.74 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |     66 | 1,349,399 |      -25.88 |
| **[_direct_] yet~important** |   -4.41 | -4,750.28 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |     67 | 2,016,665 |      -38.57 |


---

### 8. Sampling _immediately_ context-blind bigram AMs

#### 8.1. _immediately_ Highest and Lowest `LRC`

(_tie-breaker: `G2`_)

|                                       |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:--------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] immediately~accretive**  |    8.54 |  2,406.67 |           0.45 |            0.23 |    0.45 |    0.00 |   236 |       523 |        1.00 |
| **[_direct_] immediately~appealable** |    8.41 |    815.23 |           0.55 |            0.27 |    0.55 |    0.00 |    76 |       139 |        1.00 |
| **[_direct_] immediately~adjacent**   |    8.31 | 15,089.64 |           0.33 |            0.18 |    0.33 |    0.02 | 1,595 |     4,756 |        1.00 |
| **[_direct_] immediately~better**     |   -2.36 | -1,070.10 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    95 |   625,733 |       -7.77 |
| **[_direct_] immediately~different**  |   -3.41 | -1,796.47 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    51 |   825,838 |      -20.56 |
| **[_direct_] immediately~important**  |   -4.14 | -4,666.41 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |    88 | 2,016,665 |      -29.51 |

#### 8.2. _immediately_ Highest and Lowest `G2`

(_tie-breaker: `deltaP_max`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] immediately~clear**     |    5.86 | 167,884.90 |           0.26 |            0.17 |    0.07 |    0.26 | 26,038 |   349,214 |        0.98 |
| **[_direct_] immediately~available** |    5.06 | 159,088.54 |           0.29 |            0.17 |    0.04 |    0.29 | 29,351 |   666,909 |        0.97 |
| **[_direct_] immediately~apparent**  |    6.12 |  32,982.98 |           0.09 |            0.07 |    0.09 |    0.05 |  4,971 |    54,246 |        0.99 |
| **[_direct_] immediately~better**    |   -2.36 |  -1,070.10 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |     95 |   625,733 |       -7.77 |
| **[_direct_] immediately~different** |   -3.41 |  -1,796.47 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |     51 |   825,838 |      -20.56 |
| **[_direct_] immediately~important** |   -4.14 |  -4,666.41 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |     88 | 2,016,665 |      -29.51 |

#### 8.3. _immediately_ Highest and Lowest `dP1`

(_tie-breaker: `LRC`_)

|                                       |   `LRC` |      `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |   `f` |      `f2` |   `unexp_r` |
|:--------------------------------------|--------:|----------:|---------------:|----------------:|--------:|--------:|------:|----------:|------------:|
| **[_direct_] immediately~appealable** |    8.41 |    815.23 |           0.55 |            0.27 |    0.55 |    0.00 |    76 |       139 |        1.00 |
| **[_direct_] immediately~accretive**  |    8.54 |  2,406.67 |           0.45 |            0.23 |    0.45 |    0.00 |   236 |       523 |        1.00 |
| **[_direct_] immediately~adjacent**   |    8.31 | 15,089.64 |           0.33 |            0.18 |    0.33 |    0.02 | 1,595 |     4,756 |        1.00 |
| **[_direct_] immediately~better**     |   -2.36 | -1,070.10 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    95 |   625,733 |       -7.77 |
| **[_direct_] immediately~different**  |   -3.41 | -1,796.47 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    51 |   825,838 |      -20.56 |
| **[_direct_] immediately~important**  |   -4.14 | -4,666.41 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |    88 | 2,016,665 |      -29.51 |

#### 8.4. _immediately_ Highest and Lowest `dP2`

(_tie-breaker: `LRC`_)

|                                      |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |
|:-------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|
| **[_direct_] immediately~available** |    5.06 | 159,088.54 |           0.29 |            0.17 |    0.04 |    0.29 | 29,351 |   666,909 |        0.97 |
| **[_direct_] immediately~clear**     |    5.86 | 167,884.90 |           0.26 |            0.17 |    0.07 |    0.26 | 26,038 |   349,214 |        0.98 |
| **[_mirror_] immediately~available** |    4.80 |   1,538.91 |           0.22 |            0.13 |    0.03 |    0.22 |    275 |    10,284 |        0.97 |
| **[_direct_] immediately~better**    |   -2.36 |  -1,070.10 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |     95 |   625,733 |       -7.77 |
| **[_direct_] immediately~different** |   -3.41 |  -1,796.47 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |     51 |   825,838 |      -20.56 |
| **[_direct_] immediately~important** |   -4.14 |  -4,666.41 |          -0.00 |           -0.01 |   -0.00 |   -0.03 |     88 | 2,016,665 |      -29.51 |


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
| particularly     | 101,341 |
| that             |  53,554 |
| yet              |  22,946 |
| immediately      |  22,486 |
| ever             |  21,513 |
| exactly          |  15,047 |
| necessarily      |  12,891 |
| terribly         |  12,762 |
| inherently       |   9,628 |
| any              |   7,948 |
| remotely         |   3,656 |

> no more than 8,600 rows per individual `group-[#].parquet`
  - max rows in writing batch = 4,301
  - min rows in writing batch = 1,434

✓ Sample of bigram tokens for `ALL-Top8[5000]`  successfully saved as  
> "/share/compling/projects/sanpi/results/top_AM/ALL/ALL-Top8/ALL-Top8adv_sample-hits_2024-07-30.parq"
* Total time to write partitioned parquet ⇾  `00:00:00.420`



```python
show_sample(hits_df.filter(['all_forms_lower', 'token_str']).sample(10).sort_values('all_forms_lower'))
```

    +-----------------------+----------------------------+----------------------------------------------------------------+
    | hit_id                | all_forms_lower            | token_str                                                      |
    +=======================+============================+================================================================+
    | pcc_eng_08_021.2371_x | (+)_ever_dissatisfied      | If you are ever dissatisfied , we will reshoot your image      |
    | 0327464_24:4-5        |                            | until you are completely satisfied or it 's Free !             |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_01_044.4626_x | (+)_ever_thankful          | Ever thankful for small miracles , at least he did n't quote   |
    | 0702153_43:1-2        |                            | Robert Jeffress or Islamophobic warmonger Franklin Graham .    |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_09_024.0578_x | (+)_particularly_enjoyable | This project with Katharine ( funded by the Britten Pears      |
    | 0373383_04:15-16      |                            | Foundation ) was a particularly enjoyable collaboration , and  |
    |                       |                            | the end result feels very personal with lots of room for       |
    |                       |                            | musical expression .                                           |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_14_059.3936_x | (+)_yet_accessible         | The design consists of useful cardboard flaps attached with    |
    | 0943953_3:23-24       |                            | rubber bands that hold the eggs firmly in place , keeping them |
    |                       |                            | protected yet accessible .                                     |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | apw_eng_20080302_0067 | n't_immediately_clear      | it was n't immediately clear how Reyes ' death would affect    |
    | _27:3-4-5             |                            | efforts to negotiate the release of rebel-held hostages ,      |
    |                       |                            | including French-Colombian presidential candidate Ingrid       |
    |                       |                            | Betancourt and three U.S. defense contractors .                |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_03_031.1217_x | not_immediately_available  | It is not possible for us to determine how long it will take   |
    | 0487773_19:39-41-42   |                            | to receive a deposit via U.S. Mail ; however , all deposits    |
    |                       |                            | will post on the same business day they are received , but may |
    |                       |                            | not be immediately available .                                 |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_07_051.7317_x | not_terribly_surprising    | Mijares has been struggling all through camp , so it 's not    |
    | 0820210_063:12-13-14  |                            | terribly surprising that he did n't make the team .            |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_17_102.1135_x | not_that_expensive         | They are not that expensive and the quality that you get makes |
    | 1634467_31:3-4-5      |                            | it a bargain .                                                 |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_08_071.1842_x | not_that_impressive        | In Germany , it 's OK , but not that impressive , " the couple |
    | 1136374_12:09-10-11   |                            | said .                                                         |
    +-----------------------+----------------------------+----------------------------------------------------------------+
    | pcc_eng_17_105.5233_x | not_that_simple            | Appropriately responding to these types of concerns can cause  |
    | 1689710_062:17-18-19  |                            | sound economic judgements , however everything is not that     |
    |                       |                            | simple .                                                       |
    +-----------------------+----------------------------+----------------------------------------------------------------+



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


|                                       |   `LRC` |       `G2` |   `deltaP_max` |   `deltaP_mean` |   `dP1` |   `dP2` |    `f` |      `f2` |   `unexp_r` |   `P1` |    `f1` |   `exp_f` |   `unexp_f` |   `odds_r_disc` |
|:--------------------------------------|--------:|-----------:|---------------:|----------------:|--------:|--------:|-------:|----------:|------------:|-------:|--------:|----------:|------------:|----------------:|
| **[_direct_] remotely~detonated**     |   12.69 |   1,243.75 |           0.88 |            0.44 |    0.88 |    0.00 |     78 |        89 |        1.00 |   0.88 |  16,426 |      0.02 |       77.98 |            4.48 |
| **[_direct_] remotely~exploitable**   |    8.79 |   1,613.38 |           0.15 |            0.08 |    0.15 |    0.01 |    145 |       986 |        1.00 |   0.15 |  16,426 |      0.22 |      144.78 |            2.89 |
| **[_direct_] exactly~alike**          |    8.46 |  26,963.37 |           0.24 |            0.14 |    0.24 |    0.05 |  2,768 |    11,375 |        1.00 |   0.24 |  58,643 |      9.16 |    2,758.84 |            2.62 |
| **[_direct_] that~purported**         |    8.42 |     758.47 |           0.78 |            0.39 |    0.78 |    0.00 |     73 |        93 |        1.00 |   0.78 | 208,262 |      0.27 |       72.73 |            3.10 |
| **[_direct_] necessarily~indicative** |    8.03 |  13,028.00 |           0.17 |            0.10 |    0.17 |    0.03 |  1,400 |     8,148 |        1.00 |   0.17 |  48,947 |      5.48 |    1,394.52 |            2.50 |
| **[_mirror_] exactly~alike**          |    7.79 |     880.53 |           0.21 |            0.15 |    0.21 |    0.08 |     88 |       417 |        1.00 |   0.21 |   1,041 |      0.26 |       87.74 |            2.68 |
| **[_direct_] any~happier**            |    6.75 |   7,438.55 |           0.06 |            0.04 |    0.06 |    0.03 |    963 |    16,606 |        0.99 |   0.06 |  34,382 |      7.84 |      955.16 |            2.13 |
| **[_direct_] any~clearer**            |    6.51 |   4,556.17 |           0.05 |            0.03 |    0.05 |    0.02 |    608 |    11,680 |        0.99 |   0.05 |  34,382 |      5.51 |      602.49 |            2.07 |
| **[_direct_] remotely~comparable**    |    6.15 |   2,015.00 |           0.02 |            0.02 |    0.02 |    0.02 |    277 |    12,252 |        0.99 |   0.02 |  16,426 |      2.76 |      274.24 |            2.02 |
| **[_direct_] exactly~opposite**       |    5.76 |   3,028.33 |           0.05 |            0.03 |    0.05 |    0.01 |    464 |     8,491 |        0.99 |   0.05 |  58,643 |      6.84 |      457.16 |            1.86 |
| **[_direct_] any~closer**             |    5.74 |  10,942.35 |           0.05 |            0.04 |    0.03 |    0.05 |  1,738 |    61,475 |        0.98 |   0.03 |  34,382 |     29.02 |    1,708.98 |            1.81 |
| **[_direct_] exactly~right**          |    5.74 |  39,191.64 |           0.11 |            0.07 |    0.04 |    0.11 |  6,323 |   143,095 |        0.98 |   0.04 |  58,643 |    115.21 |    6,207.79 |            1.81 |
| **[_mirror_] any~closer**             |    5.68 |     506.03 |           0.07 |            0.06 |    0.07 |    0.06 |     69 |       993 |        0.99 |   0.07 |   1,197 |      0.70 |       68.30 |            2.05 |
| **[_direct_] any~wiser**              |    5.66 |     971.10 |           0.04 |            0.02 |    0.04 |    0.00 |    141 |     3,630 |        0.99 |   0.04 |  34,382 |      1.71 |      139.29 |            1.94 |
| **[_direct_] any~cuter**              |    5.56 |     570.11 |           0.04 |            0.02 |    0.04 |    0.00 |     80 |     1,828 |        0.99 |   0.04 |  34,382 |      0.86 |       79.14 |            1.99 |
| **[_direct_] any~safer**              |    5.56 |   3,883.22 |           0.03 |            0.02 |    0.03 |    0.02 |    626 |    22,826 |        0.98 |   0.03 |  34,382 |     10.77 |      615.23 |            1.78 |
| **[_direct_] necessarily~cause**      |    5.46 |     383.88 |           0.07 |            0.04 |    0.07 |    0.00 |     52 |       743 |        0.99 |   0.07 |  48,947 |      0.50 |       51.50 |            2.05 |
| **[_direct_] exactly~sure**           |    5.40 |  52,863.18 |           0.15 |            0.09 |    0.03 |    0.15 |  9,157 |   262,825 |        0.98 |   0.03 |  58,643 |    211.60 |    8,945.40 |            1.72 |
| **[_direct_] any~worse**              |    5.33 |  20,994.30 |           0.10 |            0.06 |    0.02 |    0.10 |  3,673 |   179,012 |        0.98 |   0.02 |  34,382 |     84.50 |    3,588.50 |            1.70 |
| **[_direct_] any~better**             |    5.23 |  65,861.94 |           0.32 |            0.17 |    0.02 |    0.32 | 11,460 |   625,733 |        0.97 |   0.02 |  34,382 |    295.36 |   11,164.64 |            1.77 |
| **[_direct_] necessarily~important**  |   -2.06 |  -1,465.12 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    229 | 2,016,665 |       -4.92 |   0.00 |  48,947 |  1,355.17 |   -1,126.17 |           -0.78 |
| **[_direct_] that~proud**             |   -2.08 |    -712.73 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |     79 |   207,536 |       -6.51 |   0.00 | 208,262 |    593.38 |     -514.38 |           -0.88 |
| **[_direct_] that~easier**            |   -2.18 |    -749.58 |          -0.00 |           -0.00 |   -0.00 |   -0.00 |     73 |   209,940 |       -7.22 |   0.00 | 208,262 |    600.26 |     -527.26 |           -0.91 |
| **[_direct_] that~better**            |   -2.42 |  -2,161.56 |          -0.00 |           -0.00 |   -0.00 |   -0.01 |    237 |   625,733 |       -6.55 |   0.00 | 208,262 |  1,789.09 |   -1,552.09 |           -0.88 |
| **[_direct_] exactly~much**           |   -3.37 |  -1,771.99 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |     52 | 1,349,399 |      -19.89 |   0.00 |  58,643 |  1,086.40 |   -1,034.40 |           -1.32 |
| **[_direct_] ever~many**              |   -3.47 |  -4,528.63 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    175 | 1,848,723 |      -15.54 |   0.00 | 114,075 |  2,895.31 |   -2,720.31 |           -1.23 |
| **[_direct_] that~likely**            |   -3.75 |  -4,172.31 |          -0.00 |           -0.01 |   -0.00 |   -0.01 |    117 |   890,421 |      -20.76 |   0.00 | 208,262 |  2,545.88 |   -2,428.88 |           -1.34 |
| **[_direct_] exactly~many**           |   -3.77 |  -2,540.81 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |     55 | 1,848,723 |      -26.06 |   0.00 |  58,643 |  1,488.40 |   -1,433.40 |           -1.44 |
| **[_direct_] yet~many**               |   -3.82 |  -4,064.46 |          -0.00 |           -0.01 |   -0.00 |   -0.02 |    103 | 1,848,723 |      -22.60 |   0.00 |  95,763 |  2,430.54 |   -2,327.54 |           -1.38 |
| **[_direct_] particularly~many**      |   -6.54 | -25,535.99 |          -0.01 |           -0.02 |   -0.01 |   -0.03 |     79 | 1,848,723 |     -164.03 |   0.00 | 513,668 | 13,037.28 |  -12,958.28 |           -2.23 |




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

2024-07-30

## *necessarily*


|                                           |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`        | `l2`           |   `f1` |    `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:------------------------------------------|------:|--------:|--------:|-------:|----------:|:------------|:---------------|-------:|--------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] necessarily~indicative**     | 1,400 |    0.17 |    8.03 |   0.17 | 13,028.00 | necessarily | indicative     | 48,947 |   8,148 | 72,839,571 |      5.48 |    1,394.52 |        1.00 |            2.50 | 37.27 |   2.41 |    0.03 |   0.03 |           0.17 |            0.10 | direct      |
| **[_direct_] necessarily~cause**          |    52 |    0.07 |    5.46 |   0.07 |    383.88 | necessarily | cause          | 48,947 |     743 | 72,839,571 |      0.50 |       51.50 |        0.99 |            2.05 |  7.14 |   2.02 |    0.00 |   0.00 |           0.07 |            0.04 | direct      |
| **[_direct_] necessarily~representative** |   492 |    0.03 |    4.97 |   0.03 |  2,685.16 | necessarily | representative | 48,947 |  18,355 | 72,839,571 |     12.33 |      479.67 |        0.97 |            1.62 | 21.63 |   1.60 |    0.01 |   0.01 |           0.03 |            0.02 | direct      |
| **[_direct_] necessarily~predictive**     |    58 |    0.02 |    3.95 |   0.02 |    303.20 | necessarily | predictive     | 48,947 |   2,421 | 72,839,571 |      1.63 |       56.37 |        0.97 |            1.57 |  7.40 |   1.55 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_direct_] necessarily~incompatible**   |   112 |    0.02 |    4.14 |   0.02 |    556.70 | necessarily | incompatible   | 48,947 |   5,332 | 72,839,571 |      3.58 |      108.42 |        0.97 |            1.51 | 10.24 |   1.49 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_direct_] necessarily~synonymous**     |   167 |    0.02 |    4.25 |   0.02 |    818.37 | necessarily | synonymous     | 48,947 |   8,245 | 72,839,571 |      5.54 |      161.46 |        0.97 |            1.49 | 12.49 |   1.48 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_direct_] necessarily~reflective**     |   183 |    0.02 |    3.97 |   0.02 |    819.22 | necessarily | reflective     | 48,947 |  11,237 | 72,839,571 |      7.55 |      175.45 |        0.96 |            1.39 | 12.97 |   1.38 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_direct_] necessarily~incomplete**     |   124 |    0.02 |    3.81 |   0.02 |    554.34 | necessarily | incomplete     | 48,947 |   7,634 | 72,839,571 |      5.13 |      118.87 |        0.96 |            1.39 | 10.67 |   1.38 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_direct_] necessarily~true**           | 3,460 |    0.01 |    4.35 |   0.01 | 15,129.32 | necessarily | true           | 48,947 | 231,639 | 72,839,571 |    155.66 |    3,304.34 |        0.96 |            1.38 | 56.18 |   1.35 |    0.07 |   0.07 |           0.07 |            0.04 | direct      |
| **[_direct_] necessarily~wiser**          |    51 |    0.01 |    3.07 |   0.01 |    213.67 | necessarily | wiser          | 48,947 |   3,630 | 72,839,571 |      2.44 |       48.56 |        0.95 |            1.33 |  6.80 |   1.32 |    0.00 |   0.00 |           0.01 |            0.01 | direct      |


### 1. _necessarily indicative_


|                                                 | `token_str`                                                                                                                                                                                                                                  |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_033.8991_x0532910_086:4-5-6`**    | Past performance is not __`necessarily indicative`__ of future performance .                                                                                                                                                                 |
| **`pcc_eng_29_006.4138_x0087654_22:10-11-12`**  | Not to minimize South Carolina , but it is not __`necessarily indicative`__ of anything except that the Democratic voters of South Carolina have truly transcended South 's racial stereotypes .                                             |
| **`pcc_eng_24_028.0325_x0437183_23:4-5-6`**     | Past performance is not __`necessarily indicative`__ of future results and Schroders does not guarantee the future performance of the Fund , the amount or timing of any return from it , or that it will achieve its investment objective . |
| **`pcc_eng_18_080.0744_x1280427_05:4-5-6`**     | These changes are not __`necessarily indicative`__ of an underlying disease but they can be distressing to the individual .                                                                                                                  |
| **`pcc_eng_12_064.7876_x1031233_88:5-6-7`**     | My past results are not __`necessarily indicative`__ of future performance .                                                                                                                                                                 |
| **`pcc_eng_25_005.4228_x0071986_08:15-16-17`**  | Of course , that 's one producer firing off a single Tweet , and not __`necessarily indicative`__ of what we 're going to see .                                                                                                              |
| **`pcc_eng_06_078.6094_x1254991_26:17-18-19`**  | Absentee voting already is ahead of where it was in 2008 , though that figure is not __`necessarily indicative`__ of Election Day turnout .                                                                                                  |
| **`pcc_eng_29_009.2979_x0134140_064:26-27-28`** | If a spiritual teacher ca n't seem to keep their pants on , this is probably due to some lack of psychosexual development and is not __`necessarily indicative`__ of any limitation in their spiritual attainment .                          |


### 2. _necessarily cause_


|                                                | `token_str`                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_068.0100_x1084620_43:3-4-5`**    | This is not __`necessarily cause`__ for concern .                                                                                                                                                                              |
| **`pcc_eng_09_080.7578_x1290219_66:19-20-21`** | So , a mild and gradual loss of weight and body mass in an older greyhound , is not __`necessarily cause`__ for concern , particularly if the dog is vetted routinely , and there are no symptoms of distress or dysfunction . |
| **`pcc_eng_05_089.5717_x1432874_45:11-12-13`** | A test showing small amphetamine concentrations in your body is not __`necessarily cause`__ for alarm .                                                                                                                        |
| **`pcc_eng_test_2.05409_x24786_01:11-12-13`**  | The likes of botulism and anthrax in the air are n't __`necessarily cause`__ for alarm .                                                                                                                                       |
| **`pcc_eng_07_013.9785_x0210279_048:3-4-5`**   | This is not __`necessarily cause`__ for alarm .                                                                                                                                                                                |
| **`pcc_eng_14_009.3541_x0134841_12:4-5-6`**    | But this is not __`necessarily cause`__ for despair .                                                                                                                                                                          |
| **`pcc_eng_21_013.1878_x0196808_03:17-18-19`** | Although there are be 95 convicted sex offenders living in Island County , their presence is not __`necessarily cause`__ for public concern .                                                                                  |
| **`pcc_eng_00_067.7784_x1079285_18:17-18-19`** | While it appears problematic , economists with the federal government say a negative savings rate is n't __`necessarily cause`__ for concern .                                                                                 |


### 3. _necessarily representative_


|                                                 | `token_str`                                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_073.0330_x1165130_71:30-31-32`**  | I hope that everyone watching the show - women of all ages and men alike - keep in mind that these are models , and that their bodies are not __`necessarily representative`__ of the female population , nor are they realistic for most of us .                                         |
| **`pcc_eng_27_003.7550_x0044217_12:27-28-29`**  | In researching the Chinese equivalents of Reddit or 4 chan , instead of Facebook , Han is drawing conclusions on the basis of polarized internet subcultures not __`necessarily representative`__ of the Chinese internet as a whole .                                                    |
| **`pcc_eng_26_003.8053_x0045203_09:19-20-21`**  | It is important to highlight that we abide by the fact that articles selected here for analysis are not __`necessarily representative`__ of the Globe and Mail 's overall coverage of social issues nor the evidence presented in this report serve as proof of bias in media in Canada . |
| **`pcc_eng_28_017.1574_x0261382_11:7-8-9`**     | Their words and their lives are not __`necessarily representative`__ of the Italian Jewish community , but their letters are interesting for two main reasons .                                                                                                                           |
| **`pcc_eng_28_079.8739_x1275824_49:22-23-24`**  | The societal implication that staying at home means you are living a life of luxury versus solely fulfilling domestic duties is not __`necessarily representative`__ of what mothers at home are doing .                                                                                  |
| **`pcc_eng_29_037.5350_x0589619_208:15-17-18`** | He recommends using only rents , even if few rents are available and may not be __`necessarily representative`__ of the housing stock and market .                                                                                                                                        |
| **`pcc_eng_13_094.0896_x1504558_10:08-09-10`**  | Q: Your home is very traditional and not __`necessarily representative`__ of the stereotypical Florida style .                                                                                                                                                                            |
| **`pcc_eng_23_046.1591_x0729668_26:08-09-10`**  | Particularly since those vocal constituent opponents are not __`necessarily representative`__ of the public .                                                                                                                                                                             |


### 4. _necessarily predictive_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_083.8751_x1339268_06:5-6-7`**     | Animal model outcomes are not __`necessarily predictive`__ of human results and should , therefore , be interpreted cautiously with respect to potential applicability to human conditions .                                                                                                                        |
| **`pcc_eng_00_061.9269_x0984962_11:10-11-12`**  | How you perform on one of these tests is not __`necessarily predictive`__ of your future success , it merely reflects your prior history of cognitive engagement , and potentially how prepared you are at this time to enter a graduate program or a law school , as opposed to how prepared you could ever be . " |
| **`pcc_eng_26_039.3441_x0619981_08:29-30-31`**  | Previous contests have seen candidates rise and fall in the weeks before the first votes are cast , and national polls at this stage of the race are not __`necessarily predictive`__ of the final outcome of the monthslong nominating battle .                                                                    |
| **`pcc_eng_17_078.4589_x1251825_057:4-5-6`**    | But they 're not __`necessarily predictive`__ .                                                                                                                                                                                                                                                                     |
| **`pcc_eng_18_086.5054_x1384629_026:21-22-23`** | There are varying degrees of offensive prowess sprinkled throughout the list of the hardest-hitters in baseball , so it is n't __`necessarily predictive`__ of anything other than solid-average offense - but it 's a good sign nevertheless .                                                                     |
| **`pcc_eng_12_087.9172_x1404503_09:4-5-6`**     | See college is not __`necessarily predictive`__ of your future success .                                                                                                                                                                                                                                            |
| **`pcc_eng_11_087.4867_x1399981_082:34-35-36`** | Of course , this survey only looked at homeschoolers with religious mothers , not at all homeschoolers , and it looked at individuals who were adults in 2011 , meaning that it is n't __`necessarily predictive`__ of how current homechoolers will turn out .                                                     |
| **`pcc_eng_12_001.4852_x0008010_14:10-11-12`**  | The behavior of the winter sea ice maximum is not __`necessarily predictive`__ of the following melt season .                                                                                                                                                                                                       |


### 5. _necessarily incompatible_


|                                                 | `token_str`                                                                                                                                                                                                                       |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_096.7808_x1547968_167:08-09-10`** | I have always maintained that technology is not __`necessarily incompatible`__ with the preservation of our values and freedoms .                                                                                                 |
| **`pcc_eng_22_088.0023_x1406421_11:5-6-7`**     | The two views are not __`necessarily incompatible`__ .                                                                                                                                                                            |
| **`pcc_eng_25_008.4050_x0120105_66:11-12-13`**  | Though independent of cultures , the Gospel and evangelization are not __`necessarily incompatible`__ with them ; rather they are capable of permeating them all without becoming subject to any one of them .                    |
| **`pcc_eng_02_004.3943_x0054785_40:21-22-23`**  | On the question of evolution , Bowling said this : " The Christian faith and some understandings of evolution are not __`necessarily incompatible`__ .                                                                            |
| **`pcc_eng_02_040.3549_x0636753_106:09-10-11`** | The approaches may be contradictory but they are not __`necessarily incompatible`__ .                                                                                                                                             |
| **`pcc_eng_15_098.4535_x1575054_15:7-8-9`**     | But that kind of vivacity is not __`necessarily incompatible`__ with steadiness .                                                                                                                                                 |
| **`pcc_eng_17_072.1236_x1149365_21:30-31-32`**  | My response did n't try to pressure him ; I just tried to explain where I was coming from , what evolution is about , and why it 's not __`necessarily incompatible`__ with belief in some kind of god , even the Christian God . |
| **`pcc_eng_03_031.4026_x0492406_4:34-35-36`**   | Beyond funding , others have raised worries that an FPL plan for 100 - foot new towers along U.S. 1 could also imperil the idea , though FPL says the two projects are n't __`necessarily incompatible`__ .                       |


### 6. _necessarily synonymous_


|                                                | `token_str`                                                                                                                                                                                                               |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_075.3189_x1201948_43:09-10-11`** | " Vintage " and " valuable " are not __`necessarily synonymous`__ .                                                                                                                                                       |
| **`pcc_eng_14_031.7644_x0497066_32:16-17-18`** | In tonight 's case , " inefficient shots " and " mid-range jumpers " are not __`necessarily synonymous`__ , as the Knicks allow the highest shooting percentage in the league of that mid-range shot variety ( 44.5 % ) . |
| **`pcc_eng_07_052.1047_x0826170_12:18-19-20`** | It is important to prove that today , building a sustainable and energy - efficient , is not __`necessarily synonymous`__ with building in wood .                                                                         |
| **`nyt_eng_19961129_0184_11:17-18-19`**        | but as veteran lawmakers know , giving it a high priority and getting it done are not __`necessarily synonymous`__ , especially with so many conflicting political pressures and so little judicial guidance .            |
| **`nyt_eng_19960701_0502_49:15-16-17`**        | and the Kerrville festival 's eclectic audience _ tie-dye clad or not _ was n't __`necessarily synonymous`__ with Woodstock or hippies .                                                                                  |
| **`pcc_eng_05_032.5549_x0511201_04:26-27-28`** | While big data applications are often associated with fast-moving organizations that can quickly act on real-time data feeds , big data and real time are not __`necessarily synonymous`__ .                              |
| **`pcc_eng_03_089.5263_x1433673_34:14-15-16`** | * Interdenominationalism is a Christian / Jewish hybrid , similar to ( although not __`necessarily synonymous`__ with ) messianic Judaism .                                                                               |
| **`pcc_eng_02_033.6539_x0528570_06:17-18-19`** | It 's clear that boycotts are an increasingly popular form of protest , but popularity is not __`necessarily synonymous`__ with effectiveness .                                                                           |


### 7. _necessarily reflective_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                           |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_091.0646_x1457334_149:6-7-8`**   | First , your count is not __`necessarily reflective`__ of the cultures of violence in Mormonism , Christianity , and Islam .                                                                                                                                                                                          |
| **`pcc_eng_09_039.7874_x0627772_04:13-14-15`** | Please note all views in this blog are Angie 's own and not __`necessarily reflective`__ of those of Bachcare Holiday Homes .                                                                                                                                                                                         |
| **`pcc_eng_11_019.0500_x0291825_2:12-13-14`**  | Now , it 's worth noting that these Ukraine dates are n't __`necessarily reflective`__ of availability elsewhere .                                                                                                                                                                                                    |
| **`pcc_eng_26_092.1549_x1474174_14:22-23-24`** | However , I can say that the anecdotal vignettes in the commission 's report and the generalizations drawn from them are not __`necessarily reflective`__ of our policies , procedures or operations in New York .                                                                                                    |
| **`pcc_eng_18_086.9264_x1391477_46:4-5-6`**    | Narratives are therefore not __`necessarily reflective`__ of reality .                                                                                                                                                                                                                                                |
| **`apw_eng_20090714_1177_18:16-17-18`**        | with this year 's July 4 holiday falling on Saturday , the week-to-week decline is not __`necessarily reflective`__ of a significant drop in holiday gas demand this year , said Michael McNamara , vice president of SpendingPulse .                                                                                 |
| **`pcc_eng_24_108.05339_x1740555_27:4-5-6`**   | Their stories are not __`necessarily reflective`__ of the entire Indian nation but they are reflective of their own experience , and that is important -- because the more stories we can see from the ground up and on the screen , the more stories we can share amongst ourselves and bring to the global market . |
| **`pcc_eng_18_084.0257_x1344467_01:18-19-20`** | certain external compounds such as drugs , is that the artificial environments they are conducted in are not __`necessarily reflective`__ of the real-life conditions .                                                                                                                                               |


### 8. _necessarily incomplete_


|                                             | `token_str`                                                                                                                                                                                                    |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_029.0582_x0453472_19:8-9`**   | This post is based on my ( __`necessarily incomplete`__ ) understanding and experience .                                                                                                                       |
| **`pcc_eng_27_103.8854_x1664520_25:6-7`**   | The TPC 's analysis is __`necessarily incomplete`__ ; it considers only the rate reductions Romney has made public and not the tax preferences that he has said he will eliminate but has n't yet identified . |
| **`pcc_eng_02_041.6777_x0658224_36:4-5`**   | A tentative , __`necessarily incomplete`__ , analysis follows .                                                                                                                                                |
| **`pcc_eng_12_023.0991_x0357561_19:5-6`**   | Documentary evidence is always __`necessarily incomplete`__ , and no historian is capable of acquiring all of the potentially relevant evidence that does exist .                                              |
| **`pcc_eng_27_037.6042_x0591630_73:13-14`** | ... Much better to accept that our knowledge of physical reality is __`necessarily incomplete`__ . "                                                                                                           |
| **`pcc_eng_06_020.5756_x0316688_06:11-12`** | In the spirit of that , here are my ( __`necessarily incomplete`__ ) answers .                                                                                                                                 |
| **`pcc_eng_28_023.3071_x0360313_63:7-8`**   | The recognition that finite cognition is __`necessarily incomplete`__ in this regard is reflected in the lack of a proper noun for the Deity in Judaism .                                                      |
| **`pcc_eng_20_011.4844_x0169092_9:7-8`**    | And is Austrian business cycle theory __`necessarily incomplete`__ as a tool to help investors ?                                                                                                               |


### 9. _necessarily true_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                    |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19970417_0634_21:4-5-6`**            | it is patently not __`necessarily true`__ that a so-called outside counsel brings political and legal purity to his task while an attorney general does not .                                                                                                                                                                  |
| **`pcc_eng_07_051.2144_x0811769_45:31-32-33`**  | Frankly , I 'm not entirely sure why , although it probably has to do with the perception that there 's more money and fame involved even if that 's not __`necessarily true`__ locally .                                                                                                                                      |
| **`pcc_eng_21_074.5172_x1188054_11:17-18-19`**  | Some of the impetus for same sex marriage can probably be explained by the belief , not __`necessarily true`__ , that marriage must be a wonderful institution if so many people are doing it .                                                                                                                                |
| **`pcc_eng_12_089.7372_x1433826_090:6-7-8`**    | ( However , this is not __`necessarily true`__ of all products . )                                                                                                                                                                                                                                                             |
| **`pcc_eng_00_066.2210_x1054282_17:4-5-6`**     | But that 's not __`necessarily true`__ .                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_02_041.9670_x0662883_039:13-14-15`** | But what we 've seen in other countries is that that is not __`necessarily true`__ .                                                                                                                                                                                                                                           |
| **`pcc_eng_07_020.3337_x0312678_089:39-41-42`** | Of course people have to weigh the pros and cons , consider if a choice is right for them , but you still seem to want to insist that aha , it 's really expensive ... which is n't even __`necessarily true`__ and just seems to be a way to discourage others from an opportunity you do n't even seem to fully understand . |
| **`pcc_eng_16_056.8195_x0903367_100:43-44-45`** | This is something that Indian companies have been extremely successful in using , and it has given them a high status , because people believe that if you are on level five then you must build really good software -- which is not __`necessarily true`__ .                                                                 |


### 10. _necessarily wiser_


|                                                  | `token_str`                                                                                                                                                                                                                                                                                                          |
|:-------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_088.7180_x1418519_367:14-15-16`**  | Homer was not just a " pagan " Greek , and we are not __`necessarily wiser`__ because we live twenty seven hundred years later .                                                                                                                                                                                     |
| **`pcc_eng_test_1.8922_x14307_04:30-31-32`**     | This year , the 100th anniversary of Richard Nixon 's birth , it is fascinating -- riveting , really -- to watch the older , more practiced , but not __`necessarily wiser`__ Mrs. Hillary Rodham Clinton , now our secretary of state , end her public career on the other side of a hearing table .                |
| **`pcc_eng_03_007.1202_x0098909_25:17-18-19`**   | You 'd like to know that the person you 're talking to is older , if not __`necessarily wiser`__ , and has a little perspective on what looks terribly scary . "                                                                                                                                                     |
| **`pcc_eng_03_037.7223_x0594744_08:41-42-43`**   | Though it leaves little time for breathing , The Force Awakens succeeds in capturing the feel of the Star Wars universe and is a thoroughly entertaining , action-filled and adventurous romp through a world , where people are older but not __`necessarily wiser`__ and familiar faces lurk around every corner . |
| **`pcc_eng_25_081.1930_x1298308_21:7-8-9`**      | We find an older - but not __`necessarily wiser`__ - Ash strapping himself in , but not to a chainsaw / shotgun brace , rather a man size girdle .                                                                                                                                                                   |
| **`pcc_eng_02_091.6736_x1466000_126:14-15-16`**  | Kyren are taller , slimmer , more attractive , and intelligent ( though not __`necessarily wiser`__ ) than other goblins .                                                                                                                                                                                           |
| **`pcc_eng_10_087.6604_x1400537_0045:09-10-11`** | Elliott breezes through the much older , but not __`necessarily wiser`__ , Notre Dame back court .                                                                                                                                                                                                                   |
| **`pcc_eng_04_076.2278_x1214949_10:27-28-29`**   | Today the generational divide opened up to me again on this subject , this time with me sitting on the side of the elder - although not __`necessarily wiser`__ , generation .                                                                                                                                       |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/`...
* Renaming existing version of `necessarily_indicative_80ex~80.csv`
* Renaming existing version of `necessarily_representative_80ex~80.csv`
* Renaming existing version of `necessarily_true_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_indicative_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_cause_80ex~10.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_representative_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_predictive_80ex~22.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_incompatible_80ex~31.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_synonymous_80ex~48.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_reflective_80ex~45.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_incomplete_80ex~22.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_true_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/necessarily/necessarily_wiser_80ex~14.csv`

## *that*


|                                |    `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`       |    `f1` |    `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-------------------------------|-------:|--------:|--------:|-------:|----------:|:-------|:-----------|--------:|--------:|-----------:|----------:|------------:|------------:|----------------:|-------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] that~purported**  |     73 |    0.78 |    8.42 |   0.78 |    758.47 | that   | purported  | 208,262 |      93 | 72,839,571 |      0.27 |       72.73 |        1.00 |            3.10 |   8.51 |   2.44 |    0.00 |   0.00 |           0.78 |            0.39 | direct      |
| **[_direct_] that~uncommon**   |    804 |    0.07 |    4.43 |   0.07 |  3,680.42 | that   | uncommon   | 208,262 |  11,312 | 72,839,571 |     32.34 |      771.66 |        0.96 |            1.43 |  27.21 |   1.40 |    0.00 |   0.00 |           0.07 |            0.04 | direct      |
| **[_direct_] that~farfetched** |     93 |    0.07 |    3.75 |   0.07 |    423.24 | that   | farfetched | 208,262 |   1,324 | 72,839,571 |      3.79 |       89.21 |        0.96 |            1.42 |   9.25 |   1.39 |    0.00 |   0.00 |           0.07 |            0.03 | direct      |
| **[_direct_] that~dissimilar** |    307 |    0.06 |    4.13 |   0.07 |  1,365.55 | that   | dissimilar | 208,262 |   4,605 | 72,839,571 |     13.17 |      293.83 |        0.96 |            1.40 |  16.77 |   1.37 |    0.00 |   0.00 |           0.06 |            0.03 | direct      |
| **[_mirror_] that~great**      |    342 |    0.06 |    3.90 |   0.06 |  1,405.85 | that   | great      |   5,494 |   5,568 |  1,701,929 |     17.97 |      324.03 |        0.95 |            1.33 |  17.52 |   1.28 |    0.06 |   0.06 |           0.06 |            0.06 | mirror      |
| **[_direct_] that~bad**        | 19,708 |    0.04 |    4.01 |   0.05 | 74,955.42 | that   | bad        | 208,262 | 429,537 | 72,839,571 |  1,228.13 |   18,479.87 |        0.94 |            1.27 | 131.64 |   1.21 |    0.09 |   0.09 |           0.09 |            0.07 | direct      |
| **[_direct_] that~great**      | 11,781 |    0.04 |    3.71 |   0.04 | 40,195.14 | that   | great      | 208,262 | 309,258 | 72,839,571 |    884.23 |   10,896.77 |        0.92 |            1.16 | 100.39 |   1.12 |    0.05 |   0.06 |           0.05 |            0.04 | direct      |
| **[_direct_] that~hard**       | 10,380 |    0.03 |    3.34 |   0.03 | 30,573.42 | that   | hard       | 208,262 | 348,463 | 72,839,571 |    996.32 |    9,383.68 |        0.90 |            1.05 |  92.10 |   1.02 |    0.05 |   0.05 |           0.05 |            0.04 | direct      |
| **[_mirror_] that~bad**        |    299 |    0.03 |    2.75 |   0.03 |    804.14 | that   | bad        |   5,494 |  10,261 |  1,701,929 |     33.12 |      265.88 |        0.89 |            0.99 |  15.38 |   0.96 |    0.05 |   0.05 |           0.05 |            0.04 | mirror      |
| **[_direct_] that~gullible**   |     71 |    0.03 |    2.27 |   0.03 |    202.12 | that   | gullible   | 208,262 |   2,459 | 72,839,571 |      7.03 |       63.97 |        0.90 |            1.02 |   7.59 |   1.00 |    0.00 |   0.00 |           0.03 |            0.01 | direct      |


### 1. _that purported_


|                                      | `token_str`                                                                                                                                                                                                                                                                                                                     |
|:-------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20100713_0143_27:16-17`** | he was fired by The Mirror in 2004 , after the newspaper published faked photographs __`that purported`__ to show abuse of Iraqi prisoners by British soldiers , and he set his sights on a full-time television future .                                                                                                       |
| **`nyt_eng_19950818_0395_5:14-15`**  | by spending tax dollars on a number of outrageous and patently offensive projects __`that purported`__ to have cornered the market on American culture , the National Endowment for the Arts managed to make itself anathema to voters .                                                                                        |
| **`nyt_eng_20090328_0020_39:20-21`** | in another instance , Banach said that Motherwell himself had in the 1980s determined that a work on paper __`that purported`__ to be his was actually fake , but that Flam later said this work was authentic .                                                                                                                |
| **`nyt_eng_20080309_0051_2:10-11`**  | in the early 1970s in Moscow they created paintings __`that purported`__ to examine Socialist Realism , but the work 's irony was so obvious that they were branded as political dissidents .                                                                                                                                   |
| **`nyt_eng_20040920_0191_2:11-12`**  | from the rodeo , Burkett took the National Guard records __`that purported`__ to shed negative light on President Bush 's military career to a West Texas cold storage locker where , according to Burkett 's lawyer , they remained until CBS sweet-talked them out of his client .                                            |
| **`apw_eng_20050331_0083_6:14-15`**  | BAGHDAD , Iraq -LRB- AP -RRB- _ Al-Jazeera satellite channel aired a tape __`that purported`__ to show three Romanian journalists kidnapped in Iraq and a fourth unidentified person , apparently an American .                                                                                                                 |
| **`nyt_eng_20080309_0051_24:33-34`** | and `` The People 's Choice , '' a project that began in 1993 with a telephone opinion poll that surveyed popular tastes , by 2004 had resulted in 36 strange paintings __`that purported`__ to give the people what they wanted .                                                                                              |
| **`nyt_eng_20001113_0335_24:17-18`** | Benham noted that in Davis ' most recent appeals , his lawyers put into evidence affidavits __`that purported`__ to show that executions by electrocution have been plagued by `` shocking and grotesque errors '' and that there is a substantial risk they result in `` unnecessary infliction of pain and disfigurement . '' |


### 2. _that uncommon_


|                                                 | `token_str`                                                                                                                         |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_012.7769_x0190128_37:12-13-14`**  | Been a bunch of players switching agents lately , which is not __`that uncommon`__ this time of year .                              |
| **`pcc_eng_05_006.7923_x0094128_02:4-5-6`**     | Finch irruptions are not __`that uncommon`__ .                                                                                      |
| **`pcc_eng_26_034.0160_x0533685_272:23-25-26`** | If I had to say the breakdown -- it 's hard to say , but maybe 50 - 50 , which may not be __`that uncommon`__ for games .           |
| **`pcc_eng_13_003.8856_x0046453_09:13-14-15`**  | Getting kicked off a bus or streetcar for an unknown reason is not __`that uncommon`__ .                                            |
| **`pcc_eng_20_001.7986_x0012709_05:16-17-18`**  | Now , unfortunately , with the insane people out there , orders of protection are n't __`that uncommon`__ in the sports world .     |
| **`pcc_eng_28_073.0575_x1165564_113:4-5-6`**    | Apparently seizures are not __`that uncommon`__ in pregnant women .                                                                 |
| **`pcc_eng_22_087.1685_x1392875_04:7-8-9`**     | Run-ins on the high seas are not __`that uncommon`__ , but the manner in which a country 's warships react to challenge , matters . |
| **`pcc_eng_23_083.5754_x1334435_10:19-20-21`**  | Finding them as a side dish for all meals , breakfast , lunch , and dinner , is n't __`that uncommon`__ at all .                    |


### 3. _that farfetched_


|                                                 | `token_str`                                                                                                                                                                                                                  |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20060627_0061_11:29-31-32`**         | at any rate , your intrepid video-game prognosticators dared to ask `` What if ? '' and came up with this look into a future that really is n't all __`that farfetched`__ considering the industry 's track record .         |
| **`pcc_eng_15_010.3089_x0150303_021:24-26-27`** | And that 's part of what makes Hush scary : the idea that someone can be lurking right outside your bedroom window is n't all __`that farfetched`__ .                                                                        |
| **`pcc_eng_14_015.6855_x0237125_37:5-6-7`**     | And the technology is not __`that farfetched`__ . "                                                                                                                                                                          |
| **`nyt_eng_19990128_0247_64:15-16-17`**         | after the kind of year the NFL officials had in1998 , the possibility is n't __`that farfetched`__ .                                                                                                                         |
| **`pcc_eng_16_024.0073_x0372368_4:24-25-26`**   | It does sound like they 've run out of ideas , but pets are popular in other games too , so it 's not __`that farfetched`__ .                                                                                                |
| **`pcc_eng_03_081.3969_x1301997_43:29-30-31`**  | What we do know is that the strain of a global nuclear war on the ecosystem would be so severe that the blasted landscape of Fallout 4 is not __`that farfetched`__ .                                                        |
| **`pcc_eng_24_023.0920_x0357012_60:39-40-41`**  | Wish the guy all the best for all the enjoyment he 's brought us , but the whole thing reminds me a bit of Apple / Jobs ... of course taking a huge pay off and retiring is n't __`that farfetched`__ either .               |
| **`pcc_eng_07_013.5240_x0202916_24:29-30-31`**  | I am just being paranoid , but our gov't seems to have no qualms about conducting warrantless wiretaps against some people with minimal oversight , so it is n't __`that farfetched`__ to think they would n't expand this . |


### 4. _that dissimilar_


|                                                 | `token_str`                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_105.6252_x1692749_36:26-27`**     | Swirling around the bassists double stops and the drummers press rolls , he progressively accelerates the tempo , suggesting that Peterson and Taylors styles arent __`that dissimilar`__ .                     |
| **`pcc_eng_10_044.9891_x0711754_175:4-5-6`**    | Ironically it is not __`that dissimilar`__ to what I do now .                                                                                                                                                   |
| **`nyt_eng_20070324_0044_83:5-8-9`**            | but a restaurant is n't really all __`that dissimilar`__ to a football team , in the following sense : It has the moments for which it must psych itself up and the moments when it can let its posture relax . |
| **`pcc_eng_08_072.8747_x1163604_25:29-30-31`**  | Of course in a work context , giving developmental feedback needs to be more than the one liner from a reality TV show - but the principles are not __`that dissimilar`__ .                                     |
| **`pcc_eng_15_014.6660_x0220574_21:3-4-5`**     | Governments are not __`that dissimilar`__ to businesses .                                                                                                                                                       |
| **`pcc_eng_29_048.6228_x0769057_13:4-5-6`**     | The process is not __`that dissimilar`__ .                                                                                                                                                                      |
| **`pcc_eng_07_054.1593_x0859256_074:13-14-15`** | Yes - it 's abhorrent and morally unjustifiable , but it 's not __`that dissimilar`__ to robbing a bank . "                                                                                                     |
| **`pcc_eng_00_069.8341_x1112547_158:17-18-19`** | Gold and silver , its a slightly different story , but I mean , the storys not __`that dissimilar`__ .                                                                                                          |


### 5. _that great_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_061.6070_x0980817_26:30-31-32`**  | However , the German children 's hospital is amazing , if your child needs a hospital ; if you have an infant with a fever , it 's really not __`that great`__ .                                                                                                                                                                                                                                                                                                                                                                     |
| **`nyt_eng_19991228_0384_12:19-20-21`**         | i think it 's reassuring to listen to famous people make speeches because you realize that they 're not __`that great`__ . ''                                                                                                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_12_030.2230_x0473166_244:38-39-40`** | In sum : no secedeable Territorial tidewater route for Alberta ; no BC secession likely ( and not for Greater Cascadia , either ) ; no Alberta-alone secession ; Prairie Province secession best possible option -- although not __`that great`__ ; and , then , joining America ( it occurred to me that if Montana , North Dakota and Minnesota were to secede from the USA and Alberta join them , it 'd have a route to tidewater via the Great Lakes ; I can see the Americans not much missing the first two , but Minnesota ? |
| **`pcc_eng_23_039.5378_x0622718_13:09-11-12`**  | As Bill Alsup alluded to , banks are n't all __`that great`__ for a city streetscape , and it 's admirable that they planned to forego such a dependable and high- rent - paying tenant .                                                                                                                                                                                                                                                                                                                                            |
| **`pcc_eng_15_082.7755_x1321535_183:6-7`**      | 3 ) Course layout isnt __`that great`__ because the criss cross between # 6 and 7 .                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_24_022.6148_x0349229_14:4-5-6`**     | the reproduction is n't __`that great`__ unfortunately as it would n't fit on the scanner , so took photos of her and the colours and textures are n't showing up as they look on the original .                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_17_077.7617_x1240468_14:15-17-18`**  | " Although there 's a lot of ambition and potential , most bands are n't always __`that great`__ when they start out .                                                                                                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_14_035.6985_x0560554_085:4-5-6`**    | My pain was n't __`that great`__ , I was able to remain calm between contractions , and I never got the urge to push .                                                                                                                                                                                                                                                                                                                                                                                                               |


### 6. _that bad_


|                                                 | `token_str`                                                                                                                                                                                                                                           |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_106.0546_x1699477_042:16-17-18`** | Not much of a team , otherwise they would not have been 12th , but not __`that bad`__ either : Premysl Bicovsky was regular national team for some years and their biggest star , although the midfielder was not in the European champions ' squad . |
| **`pcc_eng_01_044.2084_x0698053_040:4-5-6`**    | But it was n't __`THAT bad`__ - really !                                                                                                                                                                                                              |
| **`pcc_eng_03_018.8882_x0289259_52:4-5-6`**     | IMO Hamilton was n't __`that bad`__ and was n't good ...                                                                                                                                                                                              |
| **`pcc_eng_18_097.6908_x1566197_109:6-7-8`**    | You know , they were n't __`that bad`__ .                                                                                                                                                                                                             |
| **`pcc_eng_25_039.1380_x0617313_30:33-35-36`**  | Although I suppose that Super Princess Peach is an example of Nintendo slumming for cash , it also proves that even when Nintendo is slumming , it churns out stuff that is n't really __`that bad`__ .                                               |
| **`pcc_eng_27_107.05300_x1723200_078:5-6`**     | I can still be __`that bad`__ .                                                                                                                                                                                                                       |
| **`pcc_eng_29_089.2205_x1424850_45:28-29-30`**  | This also adds a big to the calorie content - 180 calories per can , but for an every-once - in - a- while treat this is no __`that bad`__ .                                                                                                          |
| **`pcc_eng_17_076.3625_x1217983_08:26-28-29`**  | I bought this tube for my son & his friends to ride , I read the other reviews regarding getting air and thought it ca n't be __`that bad`__ .                                                                                                        |


### 7. _that hard_


|                                                 | `token_str`                                                                                                                                                                                |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_086.3258_x1381032_39:26-28-29`**  | The conservative case against rent control , granted , probably does n't lend itself well to narrative treatment -- though I 'll bet it would n't be __`that hard`__ to come up with one . |
| **`pcc_eng_24_001.4868_x0007858_073:5-6-7`**    | " It 's really not __`that hard`__ .                                                                                                                                                       |
| **`pcc_eng_03_036.6423_x0577343_11:4-5-6`**     | " It was n't __`that hard`__ of a decision , " Martin said .                                                                                                                               |
| **`pcc_eng_27_026.0507_x0404820_069:10-11-12`** | This takes a bit of practice , but is n't __`that hard`__ to do .                                                                                                                          |
| **`pcc_eng_00_037.7878_x0594244_05:6-7-8`**     | Seriously , this life is not __`that hard`__ .                                                                                                                                             |
| **`pcc_eng_25_006.8396_x0094803_3:08-09-10`**   | Anybody can do this , it 's not __`that hard`__ .                                                                                                                                          |
| **`pcc_eng_04_104.3171_x1669027_18:3-4-5`**     | It 's not __`that hard`__ to find those types of players , if you know what you are looking at and looking for in a player .                                                               |
| **`pcc_eng_26_001.4294_x0006967_61:08-09-10`**  | Selling at auction on e Bay is n't __`that hard`__ - IF you know what you 're doing .                                                                                                      |


### 8. _that gullible_


|                                                 | `token_str`                                                                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_029.4008_x0459511_76:7-8-9`**     | Customers in today 's world are n't __`that gullible`__ .                                                                                                                                                                   |
| **`pcc_eng_03_002.1584_x0018748_122:12-13-14`** | Simply put , they are n't that smart and we are n't __`that gullible`__ .                                                                                                                                                   |
| **`pcc_eng_26_041.4254_x0653720_22:09-10`**     | Jolee will wonder aloud if all Sith are __`that gullible`__ when they join the order .                                                                                                                                      |
| **`pcc_eng_05_078.9488_x1261700_216:15-16`**    | Sorry , Charlie , but 20 years ago was the last time I was __`that gullible`__ ( and then only because I thought I 'd be related to the first family ) ...                                                                  |
| **`pcc_eng_01_066.6673_x1062229_11:08-09-10`**  | Sorry Hillary , the American people are n't __`that gullible`__ .                                                                                                                                                           |
| **`pcc_eng_24_108.04161_x1738566_076:5-7-8`**   | You hope he is n't really __`that gullible`__ .                                                                                                                                                                             |
| **`pcc_eng_08_055.3331_x0879778_078:31-32`**    | I personally would like to see Mc Mahon win strictly because Blumenthal is such a bucket of scum , it boggles the mind that the people of Connecticut would be __`that gullible`__ as to send that assclown to the Senate . |
| **`pcc_eng_00_042.6498_x0673011_26:10-11`**     | unfortunately , too many of my generation are apparently __`that gullible`__ .                                                                                                                                              |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/`...
* Renaming existing version of `that_uncommon_80ex~80.csv`
* Renaming existing version of `that_dissimilar_80ex~80.csv`
* Renaming existing version of `that_great_80ex~80.csv`
* Renaming existing version of `that_bad_80ex~80.csv`
* Renaming existing version of `that_hard_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_purported_80ex~13.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_uncommon_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_farfetched_80ex~23.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_dissimilar_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_great_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_bad_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_hard_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/that/that_gullible_80ex~15.csv`

## *exactly*


|                                      |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`    | `l2`          |   `f1` |    `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-------------------------------------|------:|--------:|--------:|-------:|----------:|:--------|:--------------|-------:|--------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] exactly~alike**         | 2,768 |    0.24 |    8.46 |   0.24 | 26,963.37 | exactly | alike         | 58,643 |  11,375 | 72,839,571 |      9.16 |    2,758.84 |        1.00 |            2.62 | 52.44 |   2.48 |    0.05 |   0.05 |           0.24 |            0.14 | direct      |
| **[_mirror_] exactly~alike**         |    88 |    0.21 |    7.79 |   0.21 |    880.53 | exactly | alike         |  1,041 |     417 |  1,701,929 |      0.26 |       87.74 |        1.00 |            2.68 |  9.35 |   2.54 |    0.08 |   0.08 |           0.21 |            0.15 | mirror      |
| **[_direct_] exactly~opposite**      |   464 |    0.05 |    5.76 |   0.05 |  3,028.33 | exactly | opposite      | 58,643 |   8,491 | 72,839,571 |      6.84 |      457.16 |        0.99 |            1.86 | 21.22 |   1.83 |    0.01 |   0.01 |           0.05 |            0.03 | direct      |
| **[_direct_] exactly~right**         | 6,323 |    0.04 |    5.74 |   0.04 | 39,191.64 | exactly | right         | 58,643 | 143,095 | 72,839,571 |    115.21 |    6,207.79 |        0.98 |            1.81 | 78.07 |   1.74 |    0.11 |   0.11 |           0.11 |            0.07 | direct      |
| **[_direct_] exactly~perpendicular** |    50 |    0.04 |    4.34 |   0.04 |    295.37 | exactly | perpendicular | 58,643 |   1,240 | 72,839,571 |      1.00 |       49.00 |        0.98 |            1.72 |  6.93 |   1.70 |    0.00 |   0.00 |           0.04 |            0.02 | direct      |
| **[_direct_] exactly~sure**          | 9,157 |    0.03 |    5.40 |   0.03 | 52,863.18 | exactly | sure          | 58,643 | 262,825 | 72,839,571 |    211.60 |    8,945.40 |        0.98 |            1.72 | 93.48 |   1.64 |    0.15 |   0.16 |           0.15 |            0.09 | direct      |
| **[_direct_] exactly~analogous**     |   103 |    0.03 |    4.53 |   0.03 |    571.33 | exactly | analogous     | 58,643 |   3,062 | 72,839,571 |      2.47 |      100.53 |        0.98 |            1.64 |  9.91 |   1.62 |    0.00 |   0.00 |           0.03 |            0.02 | direct      |
| **[_direct_] exactly~zero**          |   305 |    0.03 |    4.86 |   0.03 |  1,664.57 | exactly | zero          | 58,643 |   9,500 | 72,839,571 |      7.65 |      297.35 |        0.97 |            1.62 | 17.03 |   1.60 |    0.01 |   0.01 |           0.03 |            0.02 | direct      |
| **[_direct_] exactly~stellar**       |   172 |    0.03 |    4.68 |   0.03 |    936.96 | exactly | stellar       | 58,643 |   5,379 | 72,839,571 |      4.33 |      167.67 |        0.97 |            1.62 | 12.78 |   1.60 |    0.00 |   0.00 |           0.03 |            0.02 | direct      |
| **[_direct_] exactly~parallel**      |   205 |    0.03 |    4.72 |   0.03 |  1,111.99 | exactly | parallel      | 58,643 |   6,488 | 72,839,571 |      5.22 |      199.78 |        0.97 |            1.61 | 13.95 |   1.59 |    0.00 |   0.00 |           0.03 |            0.02 | direct      |


### 1. _exactly alike_


|                                              | `token_str`                                                                                                                                                                                               |
|:---------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_040.3347_x0636717_4:18-19`**   | For example , I freaked out when I watched March of the Penguins because the penguins looked __`exactly alike`__ and were moving in the same direction at the same time .                                 |
| **`pcc_eng_10_078.5570_x1253525_17:5-6`**    | No two Drupalists are __`exactly alike`__ .                                                                                                                                                               |
| **`pcc_eng_05_080.8490_x1292363_10:18-19`**  | To a neophyte , a piece of yellow quartz and a piece of yellow topaz look almost __`exactly alike`__ .                                                                                                    |
| **`pcc_eng_00_087.8701_x1404522_45:4-5`**    | People are all __`exactly alike`__ .                                                                                                                                                                      |
| **`pcc_eng_25_086.3206_x1380827_303:17-18`** | Gleaming fingers touched the glass lightly , and drew it apart into two bubbles , both __`exactly alike`__ .                                                                                              |
| **`pcc_eng_21_011.2800_x0165938_52:5-6`**    | No two situations are __`exactly alike`__ , and there are many additional types of insurance coverage available for an additional cost .                                                                  |
| **`pcc_eng_11_039.4740_x0622676_16:11-12`**  | Why do all Janet Jackson songs after Rythm Nation sound __`exactly alike`__ ?                                                                                                                             |
| **`pcc_eng_27_100.3059_x1606479_2:12-13`**   | In Chuck 's first appearance in " No Two THings Are __`Exactly Alike`__ " , Chuck tips Drew to the person who complained about a cartoon which he put on a memo in the hopes of boosting company morale . |


### 2. _exactly opposite_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                         |
|:---------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_037.9316_x0596852_10:28-29`**  | " We know that when the governor does venture a position , it 's a safe bet that he previously took or is about to take an __`exactly opposite`__ position , " Biden said , noting that Romney had originally supported setting a time frame for pulling U.S. troops from Afghanistan only to criticize Obama 's plan to do so by the end of 2014 . |
| **`pcc_eng_23_087.1460_x1392349_054:14-15`** | The current Bailouts are the most striking example of the government having the __`exactly opposite`__ priorities .                                                                                                                                                                                                                                 |
| **`pcc_eng_20_078.6791_x1255104_23:5-6`**    | The grade could be __`exactly opposite`__ , a downward grade .                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_05_018.7183_x0287021_46:15-16`**  | Henke is even " sheep - dipped " ( tarred with a false reputation __`exactly opposite`__ to what he was being used as ) the same way as Oswald was , handing out anti-Communist leaflets on the street , exactly the same as Oswald .                                                                                                               |
| **`pcc_eng_28_044.6395_x0706126_3:6-7`**     | However , the truth is __`exactly opposite`__ .                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_08_081.0164_x1295665_28:4-5`**    | The truth is __`exactly opposite`__ ; you should have ample sleep to lose weight .                                                                                                                                                                                                                                                                  |
| **`pcc_eng_22_045.7419_x0723121_22:11-12`**  | Two scientists can examine the same data and come to __`exactly opposite`__ conclusions about causation . "                                                                                                                                                                                                                                         |
| **`pcc_eng_05_094.7311_x1516525_09:09-10`**  | Reverse mortgage as its name suggests , is __`exactly opposite`__ to a typical mortgage such as home loan .                                                                                                                                                                                                                                         |


### 3. _exactly right_


|                                                | `token_str`                                                                                                                                                                                                                          |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_047.3803_x0749030_22:11-12-13`** | " During the tomography , I realized that something was not __`exactly right`__ .                                                                                                                                                    |
| **`pcc_eng_23_069.1493_x1100899_344:11-12`**   | DAN : Well , yeah , I think you 're __`exactly right`__ .                                                                                                                                                                            |
| **`pcc_eng_28_055.1957_x0876949_073:8-9`**     | QUINN : I think that that is __`exactly right`__ .                                                                                                                                                                                   |
| **`pcc_eng_02_016.1337_x0245065_010:3-4`**     | Mayweather is __`exactly right`__ !                                                                                                                                                                                                  |
| **`pcc_eng_24_023.8033_x0368667_627:25-26`**   | Laban basically says to him , 'in our culture , it 's the custom to marry the eldest daughter first , ' which is __`exactly right`__ .                                                                                               |
| **`pcc_eng_27_025.4056_x0394327_15:08-09-10`** | But Haller well knows that that is n't __`exactly right`__ and with some careful phraseology manipulates the all-knowing Judge and prosecutor gaining more time for his client to deliver a key witness in the case -- a Mr. Green . |
| **`pcc_eng_22_049.7992_x0788588_32:30-31`**    | If you 're an online supplier and you want to win a customer 's repeat business , you need to make sure prices , products and service are all __`exactly right`__ .                                                                  |
| **`pcc_eng_26_023.3668_x0361434_200:7-8`**     | WEBER : I think that 's __`exactly right`__ .                                                                                                                                                                                        |


### 4. _exactly perpendicular_


|                                                | `token_str`                                                                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_012.5579_x0187003_2:11-12`**     | The reason for this is the plane is flying almost __`exactly perpendicular`__ to the sun , so the contrail on the near side was in shadow .                                                                |
| **`pcc_eng_25_086.4620_x1383127_11:4-5`**      | Weld the shaft __`exactly perpendicular`__ to the mounting plate ( see How to Build a Chicken Plucker 2.jpg ) .                                                                                            |
| **`pcc_eng_17_045.6612_x0721413_091:11-12`**   | The line of sight of the telescope needed to be __`exactly perpendicular`__ to the axis of rotation .                                                                                                      |
| **`pcc_eng_20_026.8413_x0417781_25:5-6`**      | The slot would be __`exactly perpendicular`__ to the lip at the back .                                                                                                                                     |
| **`pcc_eng_02_057.6308_x0916136_20:11-12`**    | These characteristics include flatness of the nozzles and nozzle array __`exactly perpendicular`__ to the axis , an optical polish , and edges of nozzles chip free and slightly rounded .                 |
| **`pcc_eng_02_047.4148_x0750907_36:32-33`**    | Ball drive 's three motors are configured as two motors in a standard tank drive ( one of the easiest drives to code ) , with an third motor which strafes __`exactly perpendicular`__ to the tank drive . |
| **`pcc_eng_06_068.5114_x1092382_26:20-21`**    | In this context , the rotation of the ground floor white volume is included in order to be located __`exactly perpendicular`__ to the south .                                                              |
| **`pcc_eng_09_090.4196_x1446791_29:12-14-15`** | But in many places on earth , the gravity vector may not be __`exactly perpendicular`__ to the reference ellipsoid .                                                                                       |


### 5. _exactly sure_


|                                                | `token_str`                                                                                                                                                                                          |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_096.3484_x1540866_164:6-7-8`**   | Explain that sometimes we are not __`exactly sure`__ what activities are appropriate on the Sabbath .                                                                                                |
| **`pcc_eng_04_076.9894_x1227363_07:4-5`**      | No one is __`exactly sure`__ what the new i Phone will feature , but rumors have been swirling about a better camera and a faster processor .                                                        |
| **`apw_eng_20080124_0945_12:26-27-28`**        | the culture , the system , political system , tradition in teaching , science , work ethic , '' she said , adding she 's not __`exactly sure`__ what has gone wrong .                                |
| **`pcc_eng_06_026.1718_x0407379_29:22-23-24`** | Remember as a kid when you were getting ready to open that birthday present from your Grandparents and you just were n't __`exactly sure`__ how this was going to turn out ?                         |
| **`pcc_eng_28_061.7249_x0982473_50:17-18-19`** | At times there seemed to be an argument happening with himself , as if he was n't __`exactly sure`__ what he believed .                                                                              |
| **`pcc_eng_25_001.0412_x0000707_14:26-27-28`** | But having worked in the Senate , having seen firsthand members who hate the gamesmanship just as much as we all do , I 'm not __`exactly sure`__ what can be done to fix it .                       |
| **`pcc_eng_17_053.7992_x0853091_33:09-10-11`** | That Czech cover is strange , I 'm not __`exactly sure`__ what they are getting at , maybe the idea of how reality is distorted by our perception of it .                                            |
| **`pcc_eng_24_072.1219_x1150371_352:4-5-6`**   | I still was n't __`exactly sure`__ what I wanted to major in , but I got matched with a mentor who was an electrical engineer , doing some robotics testing on the arm for the Phoenix Mars Lander . |


### 6. _exactly analogous_


|                                             | `token_str`                                                                                                                                                                                                                                                                                     |
|:--------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_071.1032_x1132172_35:5-6-7`** | Kanter 's situation is not __`exactly analogous`__ , but there is a similarity in terms of intent .                                                                                                                                                                                             |
| **`pcc_eng_20_006.2958_x0085283_14:6-7`**   | But to make his zone __`exactly analogous`__ to the art zone , you have to add this : every time he shoots , in order to make a basket Michael Jordan would have to confront , without flinching , the moment when his father 's chest was blown apart by the shotgun held by his kidnapper ... |
| **`pcc_eng_26_043.6272_x0689415_36:30-31`** | A much better analogy is that ' no one in their right minds ' would talk about ' agendums ' ( ' agendum ' being a gerund and therefore __`exactly analogous`__ to ' referendum ' ) .                                                                                                            |
| **`pcc_eng_16_061.5705_x0980613_14:8-9`**   | In short , the cases are almost __`exactly analogous`__ .                                                                                                                                                                                                                                       |
| **`pcc_eng_08_108.4917_x1739135_34:2-3-4`** | Though not __`exactly analogous`__ , the 1970s oil embargo helped lead the Netherlands to dramatically transform car-filled streets to pedestrian plazas and open space for biking .                                                                                                            |
| **`pcc_eng_28_082.9033_x1324875_10:09-10`** | Shakespeare has embalmed some traditions of the kind __`exactly analogous`__ to the present case :                                                                                                                                                                                              |
| **`pcc_eng_17_008.5157_x0121549_15:3-4`**   | This is __`exactly analogous`__ to rewarding XP for combat or other accomplishments , and story rewards .                                                                                                                                                                                       |
| **`pcc_eng_20_086.8625_x1387185_17:3-4-5`** | That 's not __`exactly analogous`__ to your situation , but it 's enough to make me careful about exposure to sunlight .                                                                                                                                                                        |


### 7. _exactly zero_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_041.9298_x0661548_09:41-42`**    | The author explains that when one tests for a correlation between two variables - take them to be number of nobel prize recipients of a country and chocolate consumption for example - the nil hypothesis is that the correlation is __`exactly zero`__ , while in fact a small , maybe minuscle , but nonzero correlation is bound to exist anyway . |
| **`pcc_eng_14_001.0770_x0001262_08:15-16-17`** | The reality is that the potential for a replay of 2008 on steroids is not __`exactly zero`__ , " said Bonnie Baha , portfolio manager at Double Line Capital , which oversees $ 35 billion .                                                                                                                                                           |
| **`pcc_eng_00_038.8901_x0612044_24:24-25`**    | But unless you manage to wipe out your enemy entirely , the long-term usefulness of violence in obtaining peace of any kind is __`exactly zero`__ .                                                                                                                                                                                                    |
| **`pcc_eng_00_072.8146_x1161004_286:17-18`**   | In fact , the percentage of Schuyler 's body that consists of any robotics whatsoever is __`exactly zero`__ .                                                                                                                                                                                                                                          |
| **`pcc_eng_23_068.3961_x1088730_65:15-16`**    | And the number of American teams that competed in Europe 's biggest races was __`exactly zero`__ .                                                                                                                                                                                                                                                     |
| **`pcc_eng_22_052.2937_x0828675_11:17-18`**    | But after spending $ 1.4 million investigating voter fraud , Abbott 's crack squad turned up __`exactly zero`__ cases of impersonating an eligible voter at a polling place , which is what supporters say Voter ID laws would prevent .                                                                                                               |
| **`pcc_eng_07_077.5475_x1237018_14:44-45`**    | In fact , those two elections occurred within the past three years ( the 2004 governor 's race in Washington and a 2006 auditor race in Vermont ) , so between 1980 and 2003 the number of reversed outcomes due to recounts was __`exactly zero`__ .                                                                                                  |
| **`pcc_eng_09_044.3476_x0701438_49:53-54`**    | Now just for the record , the number of " civil rights " groups and activists , the number of law professors terribly concerned about freedom of speech , and the number of Israeli Democracy Institute members who have spoken out against this arbitrary assault against freedom of speech for Jews is __`exactly zero`__ !                          |


### 8. _exactly stellar_


|                                                 | `token_str`                                                                                                                                                                                     |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_002.2565_x0020231_06:2-3-4`**     | Earnings not __`exactly stellar`__ in US , where GDP estmates of 2.3 % may be just good enough to get fed to move away from zero interest policy .                                              |
| **`pcc_eng_05_008.4424_x0120840_6:09-10-11`**   | In other words , the sound quality is n't __`exactly stellar`__ , but it should give you a good idea of the song 's vintage pop sound .                                                         |
| **`pcc_eng_18_012.3447_x0183743_43:5-6-7`**     | Of course that is n't __`exactly stellar`__ .                                                                                                                                                   |
| **`pcc_eng_09_035.6753_x0561343_078:19-20-21`** | Half of them were cheap temporary workers his boss had hired to save money ; their motivation was n't __`exactly stellar`__ .                                                                   |
| **`pcc_eng_28_077.7269_x1241109_01:12-13-14`**  | Interest in aquaponics is growing , but the success rate is not __`exactly stellar`__ .                                                                                                         |
| **`pcc_eng_15_095.5724_x1528632_060:12-13-14`** | It was a long day for them and the Browns are n't __`exactly stellar`__ in the passing game .                                                                                                   |
| **`pcc_eng_00_060.5275_x0962471_058:08-09-10`** | No , the list of wins was n't __`exactly stellar`__ ( no victory over team with a winning FBS record ) , but the losses were n't exactly duds .                                                 |
| **`pcc_eng_11_061.9414_x0986251_04:13-14-15`**  | The vehicle he has to work with in The Living Daylights is n't __`exactly stellar`__ , tagging along with a European cellist ( Maryam d'Abo ) as he unravels a KGB plot to kill MI - 6 agents . |


### 9. _exactly parallel_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_029.7851_x0466006_19:16-17`**    | It would also be best to straighten out your ship first so it is runs __`exactly parallel`__ with the walls , just in case you panic and fly off at an angle , which could lead to you accidentally hitting a wall and causing damage to your shields ( if not getting caught by an emerging Mourning Star and destroying your ship and ending the game ) . |
| **`pcc_eng_11_055.0062_x0873765_192:12-13`**   | In regard to these pedigrees , the ancient Greeks furnish an __`exactly parallel`__ example .                                                                                                                                                                                                                                                               |
| **`pcc_eng_16_099.2753_x1590802_043:8-9`**     | The current state of the environment is __`exactly parallel`__ to our inner state .                                                                                                                                                                                                                                                                         |
| **`pcc_eng_02_031.1436_x0487887_56:10-11-12`** | If your serving , make an effort to serve not __`exactly parallel`__ to your position ... serve it on an angle , so when the return comes in , you can see the shuttle .                                                                                                                                                                                    |
| **`pcc_eng_11_001.2074_x0003258_020:4-5`**     | All this is __`exactly parallel`__ to the porn industry .                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_06_061.6135_x0980824_43:8-9`**      | " Our understanding of the Anasazi is __`exactly parallel`__ to what was thought of the Maya years ago - this advanced society responsible for beautiful things , that now we realize was not a peaceful place , " said David Wilcox , curator of the Museum of Northern Arizona .                                                                          |
| **`pcc_eng_25_014.9267_x0225207_13:15-16`**    | Gray pinstripes were made to look slightly off-kilter , sporting lapels whose stripes were __`exactly parallel`__ ( not diagonal ) to those on the jacket -- a feat of fastidious production .                                                                                                                                                              |
| **`pcc_eng_14_067.6976_x1078195_081:11-12`**   | Professor Samaritan leaned over and sliced the back in two __`exactly parallel`__ lines each exactly fifty centimetres long .                                                                                                                                                                                                                               |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/`...
* Renaming existing version of `exactly_alike_80ex~80.csv`
* Renaming existing version of `exactly_opposite_80ex~80.csv`
* Renaming existing version of `exactly_right_80ex~80.csv`
* Renaming existing version of `exactly_sure_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_alike_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_opposite_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_right_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_perpendicular_80ex~9.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_sure_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_analogous_80ex~27.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_zero_80ex~61.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_stellar_80ex~49.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/exactly/exactly_parallel_80ex~39.csv`

## *any*


|                            |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`    |   `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:---------------------------|------:|--------:|--------:|-------:|----------:|:-------|:--------|-------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_mirror_] any~closer**  |    69 |    0.07 |    5.68 |   0.07 |    506.03 | any    | closer  |  1,197 |    993 |  1,701,929 |      0.70 |       68.30 |        0.99 |            2.05 |  8.22 |   1.99 |    0.06 |   0.06 |           0.07 |            0.06 | mirror      |
| **[_direct_] any~happier** |   963 |    0.06 |    6.75 |   0.06 |  7,438.55 | any    | happier | 34,382 | 16,606 | 72,839,571 |      7.84 |      955.16 |        0.99 |            2.13 | 30.78 |   2.09 |    0.03 |   0.03 |           0.06 |            0.04 | direct      |
| **[_direct_] any~clearer** |   608 |    0.05 |    6.51 |   0.05 |  4,556.17 | any    | clearer | 34,382 | 11,680 | 72,839,571 |      5.51 |      602.49 |        0.99 |            2.07 | 24.43 |   2.04 |    0.02 |   0.02 |           0.05 |            0.03 | direct      |
| **[_direct_] any~cuter**   |    80 |    0.04 |    5.56 |   0.04 |    570.11 | any    | cuter   | 34,382 |  1,828 | 72,839,571 |      0.86 |       79.14 |        0.99 |            1.99 |  8.85 |   1.97 |    0.00 |   0.00 |           0.04 |            0.02 | direct      |
| **[_direct_] any~truer**   |    56 |    0.04 |    5.16 |   0.04 |    386.71 | any    | truer   | 34,382 |  1,427 | 72,839,571 |      0.67 |       55.33 |        0.99 |            1.94 |  7.39 |   1.92 |    0.00 |   0.00 |           0.04 |            0.02 | direct      |
| **[_direct_] any~wiser**   |   141 |    0.04 |    5.66 |   0.04 |    971.10 | any    | wiser   | 34,382 |  3,630 | 72,839,571 |      1.71 |      139.29 |        0.99 |            1.94 | 11.73 |   1.92 |    0.00 |   0.00 |           0.04 |            0.02 | direct      |
| **[_direct_] any~nearer**  |    66 |    0.04 |    5.15 |   0.04 |    444.12 | any    | nearer  | 34,382 |  1,836 | 72,839,571 |      0.87 |       65.13 |        0.99 |            1.90 |  8.02 |   1.88 |    0.00 |   0.00 |           0.04 |            0.02 | direct      |
| **[_mirror_] any~better**  |   419 |    0.03 |    5.06 |   0.03 |  2,497.00 | any    | better  |  1,197 | 14,013 |  1,701,929 |      9.86 |      409.14 |        0.98 |            1.83 | 19.99 |   1.63 |    0.34 |   0.35 |           0.34 |            0.19 | mirror      |
| **[_direct_] any~closer**  | 1,738 |    0.03 |    5.74 |   0.03 | 10,942.35 | any    | closer  | 34,382 | 61,475 | 72,839,571 |     29.02 |    1,708.98 |        0.98 |            1.81 | 40.99 |   1.78 |    0.05 |   0.05 |           0.05 |            0.04 | direct      |
| **[_mirror_] any~easier**  |    66 |    0.03 |    4.28 |   0.03 |    361.34 | any    | easier  |  1,197 |  2,386 |  1,701,929 |      1.68 |       64.32 |        0.97 |            1.63 |  7.92 |   1.59 |    0.05 |   0.06 |           0.05 |            0.04 | mirror      |


### 1. _any closer_


|                                                | `token_str`                                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_074.5381_x1188384_23:32-33-34`** | " It 's happened in California , that 's what this case was about , and it helps at the federal benefits level , she said , " but we are n't __`any closer`__ to having same - sex marriage in Nevada based on this decision . "                                                           |
| **`pcc_eng_22_034.8591_x0546831_45:7-8`**      | ( On if the team is __`any closer`__ in stabilizing the right guard position ) - " Probably not .                                                                                                                                                                                          |
| **`pcc_eng_22_086.4318_x1380920_10:4-5-6`**    | " We are not __`any closer`__ than we were in September . "                                                                                                                                                                                                                                |
| **`pcc_eng_06_039.5139_x0622880_27:13-14`**    | In these moments of resilience , of self-assertion , do artists come __`any closer`__ to " the truth " ?                                                                                                                                                                                   |
| **`pcc_eng_09_073.1632_x1167046_05:24-25`**    | Farrah guessed her age at about thirteen to fifteen , but she would have to turn around and look to pinpoint her age __`any closer`__ .                                                                                                                                                    |
| **`pcc_eng_08_108.2832_x1735765_27:41-42`**    | Hozan Kenbu ( Beng Shan Jian Wu , Fallen-Mount Sword Dance ) : Tatsufusa 's signature technique , utilizes his immense strength and sword skill to rapidly swing his Zanpakuto about his body , rendering an opponent unable to get __`any closer`__ without getting injured . [ 4 ] [ 6 ] |
| **`pcc_eng_00_039.2931_x0618607_33:22-23-24`** | Voters who chose Brexit are increasingly frustrated that the ' easy ' and ' prosperous ' deal they were promised is n't __`any closer`__ than it was a year ago and actually pretty hard going .                                                                                           |
| **`nyt_eng_19950831_0069_10:22-23`**           | despite the pleas of management and the warm reception from the crowd , there was little evidence Wednesday suggesting Busch was __`any closer`__ to being accepted by teammates still bitter over his decision to play in replacement exhibition games last spring .                      |


### 2. _any happier_


|                                                | `token_str`                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_097.5104_x1559856_41:17-19-20`** | It has become my new home and family for the next 2 years and I could n't be __`any happier`__ about that .                                                                                                                                |
| **`pcc_eng_15_099.5323_x1592400_19:4-5`**      | Could I be __`any happier`__ ?                                                                                                                                                                                                             |
| **`pcc_eng_29_064.6939_x1029107_34:18-19`**    | If a time comes when the Eagles trade away Kevin Kolb , I doubt Roy will be __`any happier`__ than Sam was .                                                                                                                               |
| **`pcc_eng_22_051.7046_x0819165_17:4-6-7`**    | " I could n't be __`any happier`__ , " Kiker said Tuesday night .                                                                                                                                                                          |
| **`pcc_eng_29_036.1275_x0566863_16:3-4-5`**    | Spellcheck is n't __`any happier`__ about this than you are .                                                                                                                                                                              |
| **`pcc_eng_00_034.8747_x0547248_29:5-6`**      | " Are people really __`any happier`__ for that sort of self-indulgent spending ?                                                                                                                                                           |
| **`pcc_eng_00_078.9978_x1260908_09:08-10-11`** | Those we spoke with say they could n't be __`any happier`__ with the results .                                                                                                                                                             |
| **`pcc_eng_07_025.2221_x0391840_29:41-43-44`** | " For what it meant not just off of some big opening weekends but for the playability over the last couple of months and really for what it means in setting up the franchise for the future , everyone could n't be __`any happier`__ . " |


### 3. _any clearer_


|                                                 | `token_str`                                                                                                                                                                |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_061.1983_x0972609_085:5-6`**      | Can I make it __`any clearer`__ ?                                                                                                                                          |
| **`pcc_eng_01_063.8350_x1016325_20:10-12-13`**  | When it comes to business , the implications could n't be __`any clearer`__ .                                                                                              |
| **`pcc_eng_11_012.3742_x0183843_142:09-11-12`** | The political disintegration of this entire adventure could n't be __`any clearer`__ .                                                                                     |
| **`pcc_eng_23_046.3428_x0732681_15:7-8`**       | 6 - 11 Could it be __`any clearer`__ ?                                                                                                                                     |
| **`pcc_eng_01_044.5653_x0703783_11:7-8`**       | And no message could have been any clearer                                                                                                                                 |
| **`pcc_eng_21_010.2611_x0149495_17:31-33-34`**  | While market pundits continue to bicker over whether the oil rout has been " good " or " bad " for the economy , its effect on the market could n't be __`any clearer`__ . |
| **`pcc_eng_17_108.05201_x1739347_05:5-7-8`**    | Although one thing could not be __`any clearer`__ -- only a few of them are doing it right .                                                                               |
| **`pcc_eng_27_054.6528_x0867265_28:09-10`**     | The consequences of such patchwork legislation cannot be __`any clearer`__ or more devastating .                                                                           |


### 4. _any cuter_


|                                                 | `token_str`                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_022.6833_x0350833_03:3-4`**       | Doesnt get __`any cuter`__ than this !                                                                                                                                    |
| **`pcc_eng_27_033.0828_x0518065_37:6-7`**       | Seriously , could it get __`any cuter`__ than this ?                                                                                                                      |
| **`pcc_eng_13_009.5277_x0137537_2:12-14-15`**   | These white chocolate dipped Oreos are decorated as ornaments and could n't be __`any cuter`__ !                                                                          |
| **`pcc_eng_21_096.2884_x1539570_055:10-12-13`** | But for now , Taylor says Grande " could n't be __`any cuter`__ . "                                                                                                       |
| **`pcc_eng_06_039.9737_x0630262_15:4-5`**       | Does it get __`any cuter`__ than this ?                                                                                                                                   |
| **`pcc_eng_28_073.9748_x1180309_51:14-16-17`**  | Just when you think the kid from Room , Jacob Tremblay , could not be __`any cuter`__ , there he is , standing on his chair to cheer Globe-winning costar , Brie Larson . |
| **`pcc_eng_06_070.2572_x1120687_18:14-16-17`**  | The new baby , with its full head of brown hair , could not be __`any cuter`__ from what Serratos has showed .                                                            |
| **`pcc_eng_24_075.5254_x1205471_13:11-13-14`**  | On top of all of that , you just could n't be __`any cuter`__ or nicer !                                                                                                  |


### 5. _any truer_


|                                                 | `token_str`                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_038.3029_x0602677_28:10-11`**     | Yet there is little to suggest that it is __`any truer`__ now than it was , say , when we started Salon in 1995 .                                                                        |
| **`pcc_eng_14_049.1795_x0778506_040:10-13-14`** | In the case of Alan , this saying could not have been __`any truer`__ .                                                                                                                  |
| **`pcc_eng_28_076.5038_x1221257_07:5-7-8`**     | And this fact ca n't be __`any truer`__ , than in connection to the corporate world , where skills and requirements change every day .                                                   |
| **`pcc_eng_13_032.5970_x0510899_090:19-21-22`** | Someone said its best to hire professionals to do something that you cannot do , and this has never been __`any truer`__ than with lawn care services .                                  |
| **`pcc_eng_26_045.6389_x0721892_18:07-09-10`**  | In Highpoint 's case it could not be __`any truer`__ .                                                                                                                                   |
| **`pcc_eng_25_030.4255_x0476166_06:4-6-7`**     | And this could n't be __`any truer`__ than of spring .                                                                                                                                   |
| **`pcc_eng_15_047.3354_x0749102_31:6-8-9`**     | And such a sentiment could not be __`any truer`__ in terms of applying genetic engineering and synthetic biology to the genomes of our planet 's organisms including humans themselves . |
| **`pcc_eng_01_065.1360_x1037269_28:16-18-19`**  | You know what they say : laughter is the best medicine ; and this could n't be __`any truer`__ !                                                                                         |


### 6. _any wiser_


|                                                 | `token_str`                                                                                                                                                                                                                                 |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_013.2252_x0197841_17:7-8`**       | " Thy reasoning , is it __`any wiser`__ ?                                                                                                                                                                                                   |
| **`pcc_eng_16_039.3173_x0620188_20:09-10`**     | This , of course , made no one __`any wiser`__ and sent the rumour mill in Moscow and far beyond into overdrive .                                                                                                                           |
| **`pcc_eng_17_106.5170_x1705885_230:4-5-6`**    | But I was n't __`any wiser`__ after reading it .                                                                                                                                                                                            |
| **`pcc_eng_24_107.00037_x1715095_04:19-20-21`** | This is the seventh year this survey has been conducted , and , alas , the business is n't __`any wiser`__ to the agile way of doing things .                                                                                               |
| **`pcc_eng_29_108.3048_x1734183_006:4-5`**      | No one was __`any wiser`__ .                                                                                                                                                                                                                |
| **`pcc_eng_06_028.3691_x0442793_062:38-40-41`** | However , this time I started thinking about why the hell am I clicking on that link and watching a video of this harridan , when I know exactly what to expect , and that I will not be __`any wiser`__ or otherwise improved afterwards ? |
| **`pcc_eng_00_039.1418_x0616152_165:3-4-5`**    | I 'm not __`any wiser`__ than all the other 20,000 people in the field .                                                                                                                                                                    |
| **`pcc_eng_00_065.4053_x1041249_040:10-13-14`** | Some of these babes are fucking around on camera without hubby being __`any wiser`__ to it !                                                                                                                                                |


### 7. _any nearer_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_19990724_1009_25:6-7`**              | '' No one will come __`any nearer`__ than that . ''                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_27_061.3397_x0975269_024:07-09-10`** | One may be drunk with love without being __`any nearer`__ to finding his mate .                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_29_023.7397_x0367056_037:6-7`**      | " No one will come __`any nearer`__ than that .                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_25_100.5512_x1611089_19:4-5`**       | No one lives __`any nearer`__ than town .                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_01_062.4079_x0993254_162:14-15`**    | Whoa ! : Tucson 2004 : Ten years on , and are we __`any nearer`__ to a Science of Consciousness ? : Journal of Consciousness Studies Vol 11 ( 12 ) Dec 2004 , 68-88 .                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_21_069.5591_x1107968_10:16-17-18`**  | Some 76 days after over 200 girls were abducted from Chibok , the girls are not __`any nearer`__ home today than they were on the day they were abducted , and all the clueless and ineffective Administration of President Jonathan can do is to engage in image laundering that has caused the taxpayers US $ 1.2 million ; witch - hunt the media as well as those perceived to be opponents of the Administration and engage in a continuous and unprecedented abuse of national institutions . |
| **`pcc_eng_00_031.9647_x0500415_29:20-21-22`**  | Some statements from official sources you want to believe , and some you consider lies , but you 're not __`any nearer`__ to knowing the final result than anyone else outside those with actual knowledge of which way " the US " position is set .                                                                                                                                                                                                                                                |
| **`apw_eng_19980812_0179_14:16-18-19`**         | and despite an intensification of diplomatic efforts have been stepped up , though they do n't appear __`any nearer`__ to a solution than last month .                                                                                                                                                                                                                                                                                                                                              |


### 8. _any better_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19961029_0515_27:14-17-18`**         | Next up was Robertson , of whom Russell would later say , `` Nobody was ever __`any better`__ than Oscar Robertson _ nobody . ''                                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_26_008.7741_x0125558_107:10-12-13`** | And I think the dynamics of that relationship could n't be __`any better`__ . "                                                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_13_006.2012_x0083896_83:06-09-10`**  | Jackman & Hathaway both could not have been __`any better`__ in their roles .                                                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_21_068.6715_x1093716_42:85-86-87`**  | Elections matter and if this - literally - LIFE AND DEATH situation does n't inspire better candidates to get in the mix , I do n't know what will , so we can END these GOP LEGISLATIVE DEATH PANELS , because that 's what the Teabaggers railed about with OBama and the ACA way back in 2010 , and the ' Death Panel ' rhetoric propelled them while Dems were stunned , slack and lazy , basking in the glow of 2008 and 2014 hardly __`any better`__ . |
| **`pcc_eng_19_077.8696_x1241821_51:4-5-6`**     | The situation is hardly __`any better`__ for the people in the HIPO program who are n't likely to flourish in senior management roles .                                                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_20_081.3002_x1297333_33:3-5-6`**     | AI is n't necessarily __`any better`__ at detecting malware than traditional antivirus software , because an AI system ca n't look at a piece of code and know whether it 's good or bad , he says .                                                                                                                                                                                                                                                         |
| **`pcc_eng_08_039.3261_x0620527_421:09-10`**    | " Hey , if it makes ya feel __`any better`__ , our crime scene officers out there said it 's likely she died as soon as her neck cracked up against that thing and went kersplat ! "                                                                                                                                                                                                                                                                         |
| **`pcc_eng_26_023.5846_x0364973_35:6-7`**       | Does Constantine 's solution look __`any better`__ than before ?                                                                                                                                                                                                                                                                                                                                                                                             |


### 9. _any easier_


|                                                | `token_str`                                                                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_003.5931_x0041718_08:5-7-8`**    | Luckily , it could n't be __`any easier`__ to prepare .                                                                                                                                                                                                                       |
| **`pcc_eng_05_033.1375_x0520593_40:21-23-24`** | Beating away competition , both gas-powered and electric , while carving a thin slice of market share for itself wo n't be __`any easier`__ than it was five years ago .                                                                                                      |
| **`pcc_eng_18_036.1069_x0568229_15:17-19-20`** | It would n't have been easy turning Mc Chrystal down next July , and it wo n't be __`any easier`__ with Petraeus .                                                                                                                                                            |
| **`pcc_eng_26_019.0370_x0291427_12:08-09-10`** | The end result , though , is n't __`any easier`__ on the ears .                                                                                                                                                                                                               |
| **`pcc_eng_02_096.6978_x1547322_26:1-2-3`**    | Not __`any easier`__ than you can make real whisky or gin at home .                                                                                                                                                                                                           |
| **`nyt_eng_20070222_0026_66:4-5-6`**           | `` It 's not __`any easier`__ , '' she said .                                                                                                                                                                                                                                 |
| **`pcc_eng_06_101.9428_x1632927_16:4-5-6`**    | While it was n't __`any easier`__ for me to make my brain buckle down and start work every day , I at least had fewer alternative uses for my work time .                                                                                                                     |
| **`pcc_eng_13_009.3985_x0135478_51:14-16-17`** | After playing a total of 72 minutes last season , playing time wo n't be __`any easier`__ to find as he enters his third season in the NBA , as the Thunder acquired Domantas Sabonis with the 11th pick in the draft and acquired Ersan Ilyasova in a trade with the Magic . |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/`...
* Renaming existing version of `any_closer_80ex~80.csv`
* Renaming existing version of `any_happier_80ex~80.csv`
* Renaming existing version of `any_clearer_80ex~80.csv`
* Renaming existing version of `any_better_80ex~80.csv`
* Renaming existing version of `any_easier_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_closer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_happier_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_clearer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_cuter_80ex~20.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_truer_80ex~12.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_wiser_80ex~32.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_nearer_80ex~14.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_better_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/any/any_easier_80ex~80.csv`

## *remotely*


|                                     |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`     | `l2`        |   `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:------------------------------------|------:|--------:|--------:|-------:|---------:|:---------|:------------|-------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] remotely~detonated**   |    78 |    0.88 |   12.69 |   0.88 | 1,243.75 | remotely | detonated   | 16,426 |     89 | 72,839,571 |      0.02 |       77.98 |        1.00 |            4.48 |  8.83 |   3.59 |    0.00 |   0.00 |           0.88 |            0.44 | direct      |
| **[_direct_] remotely~exploitable** |   145 |    0.15 |    8.79 |   0.15 | 1,613.38 | remotely | exploitable | 16,426 |    986 | 72,839,571 |      0.22 |      144.78 |        1.00 |            2.89 | 12.02 |   2.81 |    0.01 |   0.01 |           0.15 |            0.08 | direct      |
| **[_direct_] remotely~comparable**  |   277 |    0.02 |    6.15 |   0.02 | 2,015.00 | remotely | comparable  | 16,426 | 12,252 | 72,839,571 |      2.76 |      274.24 |        0.99 |            2.02 | 16.48 |   2.00 |    0.02 |   0.02 |           0.02 |            0.02 | direct      |
| **[_mirror_] remotely~related**     |    73 |    0.02 |    2.97 |   0.02 |   265.65 | remotely | related     |  2,341 |  3,457 |  1,701,929 |      4.76 |       68.24 |        0.93 |            1.21 |  7.99 |   1.19 |    0.03 |   0.03 |           0.03 |            0.02 | mirror      |
| **[_mirror_] remotely~close**       |   267 |    0.02 |    3.34 |   0.02 |   945.05 | remotely | close       |  2,341 | 13,874 |  1,701,929 |     19.08 |      247.92 |        0.93 |            1.20 | 15.17 |   1.15 |    0.11 |   0.11 |           0.11 |            0.06 | mirror      |
| **[_mirror_] remotely~possible**    |    52 |    0.02 |    2.39 |   0.02 |   164.51 | remotely | possible    |  2,341 |  3,160 |  1,701,929 |      4.35 |       47.65 |        0.92 |            1.10 |  6.61 |   1.08 |    0.02 |   0.02 |           0.02 |            0.02 | mirror      |
| **[_mirror_] remotely~similar**     |   107 |    0.01 |    2.69 |   0.02 |   325.77 | remotely | similar     |  2,341 |  7,011 |  1,701,929 |      9.64 |       97.36 |        0.91 |            1.07 |  9.41 |   1.05 |    0.04 |   0.05 |           0.04 |            0.03 | mirror      |
| **[_direct_] remotely~plausible**   |   183 |    0.01 |    4.89 |   0.01 | 1,048.46 | remotely | plausible   | 16,426 | 17,571 | 72,839,571 |      3.96 |      179.04 |        0.98 |            1.67 | 13.23 |   1.66 |    0.01 |   0.01 |           0.01 |            0.01 | direct      |
| **[_mirror_] remotely~true**        |    66 |    0.01 |    1.91 |   0.01 |   157.30 | remotely | true        |  2,341 |  6,191 |  1,701,929 |      8.52 |       57.48 |        0.87 |            0.91 |  7.08 |   0.89 |    0.02 |   0.03 |           0.02 |            0.02 | mirror      |
| **[_mirror_] remotely~funny**       |    51 |    0.01 |    1.58 |   0.01 |   111.11 | remotely | funny       |  2,341 |  5,365 |  1,701,929 |      7.38 |       43.62 |        0.86 |            0.86 |  6.11 |   0.84 |    0.02 |   0.02 |           0.02 |            0.01 | mirror      |


### 1. _remotely detonated_


|                                      | `token_str`                                                                                                                                                                                                                              |
|:-------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20040223_0226_12:10-11`** | and gun battles with guerrillas have been supplanted by __`remotely detonated`__ bombs and suicide bombers .                                                                                                                             |
| **`apw_eng_20090709_0201_4:20-21`**  | authorities suspect the explosives were in the back of the truck , mingled with the timber , and were __`remotely detonated`__ , Khan said .                                                                                             |
| **`nyt_eng_20050621_0205_15:12-13`** | car bomb attacks against American forces -- both suicide attacks and __`remotely detonated`__ devices -- reached a monthly high of 70 in April and fell slightly in May , according to figures provided by the U.S. military in Iraq .   |
| **`apw_eng_20021019_0204_7:27-28`**  | although Russian forces outnumber the rebels and have heavier weapons at their disposal , the insurgents inflict daily casualties through small attacks and with booby-traps and __`remotely detonated`__ land mines .                   |
| **`apw_eng_20090804_0026_4:7-8`**    | Afghan police said the bomb was __`remotely detonated`__ , killing a woman , a 12-year-old girl , seven civilian men , including several fruit vendors , and two police officers .                                                       |
| **`apw_eng_20090709_0294_5:38-39`**  | after police arrived to clear the road , militants apparently decided to blow up the truck , Khan said , adding that authorities believe the explosives were mixed with timber in the back of the vehicle and __`remotely detonated`__ . |
| **`apw_eng_20030215_0098_4:5-6`**    | `` The charge was __`remotely detonated`__ and an anti-terrorist unit is on the scene investigating , '' Konteska said .                                                                                                                 |
| **`nyt_eng_20090319_0207_4:21-22`**  | the bomb hit the car only a few miles from its destination , officials said , and may have been __`remotely detonated`__ .                                                                                                               |


### 2. _remotely exploitable_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                            |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_017.9675_x0273891_08:26-27`** | In those early days the vulnerability assessment space was still in its infancy with much of the focus being around scanning network based services for __`remotely exploitable`__ vulnerabilities .                                                                                                                   |
| **`pcc_eng_17_049.0999_x0777120_08:21-22`** | Thirty -one of the vulnerabilities affect the Oracle Sun product suite ( Solaris ) , including 11 Oracle classified as __`remotely exploitable`__ .                                                                                                                                                                    |
| **`pcc_eng_14_032.4974_x0508950_14:20-21`** | I would 've submitted to Apple if their bug bounty included mac OS , or if the vuln was __`remotely exploitable`__ . "                                                                                                                                                                                                 |
| **`pcc_eng_03_056.9947_x0907011_12:12-13`** | Security is announcing the existence of a comprehensive security research on __`remotely exploitable`__ " Binary Planting " vulnerabilities affecting a large percentage of Windows applications and often allowing for trivial exploitation .                                                                         |
| **`pcc_eng_29_021.4478_x0329897_05:3-4`**   | " A __`remotely exploitable`__ flaw exists within Publisher 2007 that allows arbitrary code to be executed in the context of the logged in user , " the alert read .                                                                                                                                                   |
| **`pcc_eng_01_027.2683_x0424799_11:30-31`** | The Solaris product suite that Oracle acquired from its purchase of Sun Microsystems , meanwhile , accounted for 21 of the patches released today , 7 of which are __`remotely exploitable`__ .                                                                                                                        |
| **`pcc_eng_00_097.0439_x1553320_09:12-13`** | Sun Systems products get 23 fixes , seven of which are __`remotely exploitable`__ .                                                                                                                                                                                                                                    |
| **`pcc_eng_26_013.8259_x0207202_9:47-48`**  | The security patch for this vulnerability comes just about two weeks after Oracle 's regular Critical Patch Update ( CPU ) for October 2017 , which patches a total of 252 vulnerabilities in its products , including 40 in Fusion Middleware out of which 26 are __`remotely exploitable`__ without authentication . |


### 3. _remotely comparable_


|                                               | `token_str`                                                                                                                                                                                                                             |
|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000718_0109_19:19-20-21`**       | while the three-week race through France is one of the world 's most-watched sporting spectacles , there is nothing __`remotely comparable`__ to it in this country , and most mainstream media here give bicycle racing short shrift . |
| **`nyt_eng_19990212_0165_25:14-16-17`**       | the metaphor seems like a stretch -LRB- Vietnam and The Great Society are not even __`remotely comparable`__ to cruise missile launches and school uniforms -RRB- , but there are parallels that should give Gore pause .               |
| **`pcc_eng_26_030.6111_x0478494_42:6-7`**     | No other group has a __`remotely comparable`__ right and only Jews enjoy any collective rights under Israeli law . "                                                                                                                    |
| **`pcc_eng_21_063.6691_x1012800_072:1-2-3`**  | Nothing __`remotely comparable`__ to the post-World War II de-nazification of Germany has occurred ; only a handful of communists have been prosecuted .                                                                                |
| **`pcc_eng_01_032.9426_x0516326_1:22-24-25`** | What is ironic is that with all the technology and what not that we are blessed with today , Supriya is n't even __`remotely comparable`__ to Silk , when it comes to pure sensuousness .                                               |
| **`pcc_eng_26_032.9739_x0516965_15:4-6-7`**   | Jonathan Ross was not even __`remotely comparable`__ to anyone on 1Xtra - his shows , unlike those on that station , were full of the new elite and its footsoldiers .                                                                  |
| **`nyt_eng_20001127_0360_22:8-9`**            | he added that he could find no __`remotely comparable`__ situation in his own past , although , he said , `` I 've been through some strange circumstances .                                                                            |
| **`pcc_eng_00_039.2830_x0618432_21:10-11`**   | In the entire history of mankind there is no __`remotely comparable`__ example of a people in all history which experienced a renaissance after such a lengthy interlude .                                                              |


### 4. _remotely related_


|                                                | `token_str`                                                                                                                                                                                     |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_018.9393_x0289857_64:10-11`**    | Walter , ask anybody who works in any field __`remotely related`__ to health care and they will tell you that you are dead wrong in your stance on emergency room overuse / abuse .             |
| **`pcc_eng_21_011.5634_x0170498_02:13-14`**    | Every part of my body , giant shemale cock videos , even __`remotely related`__ to sex was included in response to your every touch .                                                           |
| **`pcc_eng_02_074.5104_x1188694_105:8-9`**     | Whatever your specialty , if it 's __`remotely related`__ to science or medicine , we 've got you covered .                                                                                     |
| **`pcc_eng_21_086.2274_x1377586_4:11-12`**     | The only requirement is that it must be at least __`remotely related`__ to blues music .                                                                                                        |
| **`pcc_eng_11_015.4407_x0233709_15:15-20-21`** | And yes , there will be new names introduced , though let 's hope none of them are even __`remotely related`__ to Jar Jar Binks .                                                               |
| **`pcc_eng_08_106.5234_x1708667_157:3-5-6`**   | He was not even __`remotely related`__ to the entire investigation .                                                                                                                            |
| **`pcc_eng_15_043.0438_x0679735_56:5-6-7`**    | I know this is n't __`remotely related`__ to airport security , but I 'm just saying ...                                                                                                        |
| **`pcc_eng_03_014.7759_x0222890_17:30-31`**    | I deplore the base level of cynicism , hate , and childishness that flows so frequently online to such a degree that I hesitated to participate in anything even __`remotely related`__ to it . |


### 5. _remotely close_


|                                                 | `token_str`                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_060.1050_x0956957_17:8-9`**       | The only reason the Sabres are even __`remotely close`__ to playoff contention is due to the play of their goaltender .                                                                                    |
| **`pcc_eng_05_088.3563_x1413334_115:21-27-28`** | The next night she goes through the dictionary because People have some very peculiar names sometimes ( 7 ) but none of the words are even __`remotely close`__ to the mans name                           |
| **`pcc_eng_03_008.8463_x0126923_17:17-18-19`**  | So when we consider the purchasing power of the dollar , then our stock portfolio was n't __`remotely close`__ to flat , but rather had dropped by a staggering 70 % in fourteen years , from 919 to 274 . |
| **`pcc_eng_18_010.9692_x0161302_045:1-3-4`**    | Nothing even __`remotely close`__ to that .                                                                                                                                                                |
| **`pcc_eng_17_050.4256_x0798425_12:11-12-13`**  | The number of dead in all wars since 1945 is n't __`remotely close`__ to those numbers .                                                                                                                   |
| **`pcc_eng_20_074.3670_x1185400_090:09-10`**    | No other country in Latin America gets even __`remotely close`__ to Cuba in any of these indicators .                                                                                                      |
| **`pcc_eng_01_065.0477_x1035836_060:19-20-21`** | As you would expect from an eleven-year - old title , the graphics of Xanadu Next definitely are n't __`remotely close`__ to the games of today .                                                          |
| **`pcc_eng_16_053.8488_x0855378_26:1-2-3`**     | Not __`remotely close`__ to prior bottles .                                                                                                                                                                |


### 6. _remotely possible_


|                                                | `token_str`                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20050211_0294_14:15-19-20`**        | if one-tenth of all the energy in every wave could be captured -- and nothing like that is __`remotely possible`__ -- that would amount to only about as much as the country 's current total output of hydroelectric power . |
| **`pcc_eng_00_072.5627_x1156857_19:3-4`**      | It is __`remotely possible`__ the code encounters a design flaw in the unidentified microprocessor that causes the circuitry to freeze .                                                                                      |
| **`pcc_eng_02_048.0324_x0760924_38:16-17`**    | Where are the shining examples of government efficiency that leads you to believe it is __`remotely possible`__ that government will do a better job than the private sector in any of these things ?                         |
| **`pcc_eng_00_028.7106_x0447831_5:17-18`**     | The Ars Technica article goes through great lengths to argue why using AMD CPUs is only __`remotely possible`__ under one condition and that buying AMD altogether is not an option at all !                                  |
| **`pcc_eng_10_076.2656_x1216459_05:20-25-26`** | American conservatives are freaking out about the thought of UN or Sharia law being implemented in the States , neither of which is even __`remotely possible`__ at any point in the near ( or distant ) future .             |
| **`pcc_eng_00_009.1550_x0131699_07:23-25-26`** | Without the hundreds of kilos of gear that Interplast bring over from Australia , most of the procedures the surgeons performed would not be __`remotely possible`__ .                                                        |
| **`pcc_eng_10_028.2319_x0440139_1:20-21`**     | I remember someone mentioning it can be done but from my experience I cant see how it is even __`remotely possible`__ .                                                                                                       |
| **`pcc_eng_20_035.2703_x0553962_06:19-20`**    | While I know you 're a fan of Museum Victoria 's particular shade of green , it 's __`remotely possible`__ that somebody with a less sophisticated palette may want to change the colour of the toolbars .                    |


### 7. _remotely similar_


|                                                | `token_str`                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_025.4173_x0394536_040:7-8`**     | If a Republican today used language __`remotely similar`__ to what Bush and Reagan did , they would be hooted off many a conservative stage .                                                                                                                                          |
| **`pcc_eng_24_077.7562_x1241626_26:09-10`**    | The chances that you can achieve something even __`remotely similar`__ are practically zero .                                                                                                                                                                                          |
| **`pcc_eng_11_005.8578_x0078800_18:21-23-24`** | This album definitely is n't " Enter the Wu-Tang : The 36 Chambers , " part two ; it 's not even __`remotely similar`__ to " Only Built 4 Cuban Linx . "                                                                                                                               |
| **`pcc_eng_17_010.4188_x0152383_32:6-7`**      | When he has discovered anything __`remotely similar`__ to a breach of this policy , Riley said , it was often more done more implicitly ; for example , officials worried about leaving traces of their activities may make a point of not creating any written record to begin with . |
| **`pcc_eng_03_031.6455_x0496391_57:11-12-13`** | If she is very religious or has opinions that are not __`remotely similar`__ to mine , I probably would not .                                                                                                                                                                          |
| **`pcc_eng_09_104.7135_x1678473_029:15-16`**   | Have we studied anything in the book of Daniel so far that seems even __`remotely similar`__ ?                                                                                                                                                                                         |
| **`pcc_eng_24_100.3273_x1606937_18:11-13-14`** | It is also called " cruise " but it is not even __`remotely similar`__ to big time cruises .                                                                                                                                                                                           |
| **`pcc_eng_03_088.0188_x1409076_04:18-19-20`** | There were a few bus lines in Springfield , Illinois , where I grew up , but nothing __`remotely similar`__ to the CTA .                                                                                                                                                               |


### 8. _remotely plausible_


|                                              | `token_str`                                                                                                                                                                                                                           |
|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_006.6967_x0092135_160:3-5-6`** | It is n't even __`remotely plausible`__ to suggest that inequality is simply happening by some kind of accident .                                                                                                                     |
| **`pcc_eng_10_031.6528_x0495648_25:14-15`**  | Chris may be right that they will say this , but is it __`remotely plausible`__ ?                                                                                                                                                     |
| **`pcc_eng_16_025.3532_x0394188_177:16-17`** | No , it 's " ugh " because whatever it takes to make this couple __`remotely plausible`__ , let alone palatable , neither the stars , nor screenwriter Alex Gottlieb , nor director Frank Tashlin have it .                           |
| **`pcc_eng_05_076.7632_x1226239_178:09-10`** | Which reminds me , how was it even __`remotely plausible`__ that Sally Yates was convinced that Mike Flynn was compromised because he had n't been completely forthright in disclosing his conversation with the Russian ambassador ? |
| **`pcc_eng_29_048.3466_x0764599_28:13-14`**  | To the author 's credit they figured out that to sound even __`remotely plausible`__ and still make me wet my Underoos over the advanced technology featured in the book , one had to open with a year further out than 2000 A.D .    |
| **`pcc_eng_10_033.6088_x0527367_25:15-16`**  | Yet there is something puzzling about Trump 's failure to come up with a __`remotely plausible`__ infrastructure plan .                                                                                                               |
| **`pcc_eng_26_100.6587_x1611112_70:8-9`**    | For whatever reason , that only seems __`remotely plausible`__ and even somehow adorable in the context of that franchise .                                                                                                           |
| **`pcc_eng_val_1.8183_x13288_11:19-20`**     | The bad news is that much of The Joker 's appeal -- and all of what makes him __`remotely plausible`__ -- is that nobody is sure who or what he is .                                                                                  |


### 9. _remotely true_


|                                                 | `token_str`                                                                                                                                                                                                                                                                     |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_100.2676_x1604993_53:7-8`**       | There is no suggestion of anything __`remotely true`__ in any of the statements in the scary story posted by the OP .                                                                                                                                                           |
| **`pcc_eng_00_062.2374_x0989988_14:17-27-28`**  | Moreover , three decades of independent journalism have led me to conclude not only that virtually nothing of what is presented as ' news ' is __`remotely true`__ , but that the conventional writing and presentation of history itself is as phoney as a three dollar bill . |
| **`nyt_eng_20070105_0118_23:4-5-6`**            | and it is n't __`remotely true`__ .                                                                                                                                                                                                                                             |
| **`pcc_eng_05_043.1571_x0682511_21:11-12`**     | You could use facts to prove anything that 's even __`remotely true`__ ! " - Matt Groening , The Simpsons                                                                                                                                                                       |
| **`pcc_eng_02_090.8710_x1452967_23:3-5-6`**     | That 's not even __`remotely true`__ and is a very dangerous message to spread to such a wide audience .                                                                                                                                                                        |
| **`pcc_eng_23_004.5264_x0056740_002:31-33-34`** | I know many of you think that those of us who have published books are big time millionaires , which is really fun to think about , but it 's not even __`remotely true`__ , except for Jamie Ford , who is a multi-billionaire .                                               |
| **`pcc_eng_04_004.7168_x0060249_21:7-8-9`**     | Which , of course , is not __`remotely true`__ as Trump 's father came from Germany .                                                                                                                                                                                           |
| **`pcc_eng_11_019.2848_x0295627_02:22-24-25`**  | Most people think that a restaurant is the be all and end all of a chef 's career but that is not even __`remotely true`__ .                                                                                                                                                    |


### 10. _remotely funny_


|                                                | `token_str`                                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_048.5546_x0770275_06:45-46`**    | In the 21st century -- after the horrific events of Sept. 11 , 2001 , and more recently , after the April 15 , 2013 , Boston Marathon bombings -- what once may have passed as an acceptable high-school prank is no longer even __`remotely funny`__ , if it ever was . |
| **`pcc_eng_15_093.7738_x1499594_21:16-18-19`** | JP ( John Paul Temple ) is good like that , annoying as hell and not even __`remotely funny`__ , he is an excellent PT though .                                                                                                                                          |
| **`pcc_eng_20_030.2939_x0473614_15:1-2-3`**    | Not __`remotely funny`__ .                                                                                                                                                                                                                                               |
| **`pcc_eng_08_049.8663_x0790906_25:37-39-40`** | You may also ponder the degree of nepotism involved with casting Catherine Reitman , the daughter of producer Ivan Retiman , as Ryden 's arch-rival Jessica , as she gives a flat deep-voiced performance that 's never even __`remotely funny`__ .                      |
| **`pcc_eng_09_083.0771_x1327763_75:19-21-22`** | But suddenly , now that I 'm not saying what they want to hear politically , I 'm not even __`REMOTELY funny`__ .                                                                                                                                                        |
| **`pcc_eng_15_025.8675_x0401865_07:16-17`**    | Giving me even more impetus to subject myself to a movie that may be only __`remotely funny`__ is news today that professional Mexican wrestler , Hijo del Santo ( " Son of the Saint " ) , is laying an eco-smackdown on the Pacific coastline .                        |
| **`pcc_eng_25_034.2862_x0538911_12:11-13-14`** | However , as Barnett points out , the label was n't " __`remotely funny`__ " -- if it had , she would have laughed .                                                                                                                                                     |
| **`pcc_eng_16_080.3288_x1283871_3:26-28-29`**  | because atleast to me it looks like she 's legitimately retarded and aside from a few errors with her japanese / pronounciation there 's absolutely nothing even __`remotely funny`__ , even for someone who ' gets ' what she is talking about .                        |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/`...
* Renaming existing version of `remotely_related_80ex~80.csv`
* Renaming existing version of `remotely_close_80ex~80.csv`
* Renaming existing version of `remotely_possible_80ex~80.csv`
* Renaming existing version of `remotely_similar_80ex~80.csv`
* Renaming existing version of `remotely_true_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_detonated_80ex~11.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_exploitable_80ex~24.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_comparable_80ex~67.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_related_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_close_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_possible_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_similar_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_plausible_80ex~36.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_true_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/remotely/remotely_funny_80ex~65.csv`

## *ever*


|                                 |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`   | `l2`        |    `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:--------------------------------|------:|--------:|--------:|-------:|----------:|:-------|:------------|--------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] ever~quarterly**   |   137 |    0.45 |    8.05 |   0.45 |  1,349.65 | ever   | quarterly   | 114,075 |    306 | 72,839,571 |      0.48 |      136.52 |        1.00 |            2.71 | 11.66 |   2.46 |    0.00 |   0.00 |           0.45 |            0.22 | direct      |
| **[_direct_] ever~olympic**     |   218 |    0.44 |    8.23 |   0.44 |  2,141.80 | ever   | olympic     | 114,075 |    492 | 72,839,571 |      0.77 |      217.23 |        1.00 |            2.71 | 14.71 |   2.45 |    0.00 |   0.00 |           0.44 |            0.22 | direct      |
| **[_direct_] ever~watchful**    |   416 |    0.22 |    7.05 |   0.22 |  3,399.87 | ever   | watchful    | 114,075 |  1,866 | 72,839,571 |      2.92 |      413.08 |        0.99 |            2.26 | 20.25 |   2.15 |    0.00 |   0.00 |           0.22 |            0.11 | direct      |
| **[_direct_] ever~diminishing** |    71 |    0.16 |    5.75 |   0.16 |    527.77 | ever   | diminishing | 114,075 |    445 | 72,839,571 |      0.70 |       70.30 |        0.99 |            2.09 |  8.34 |   2.01 |    0.00 |   0.00 |           0.16 |            0.08 | direct      |
| **[_direct_] ever~scarcer**     |    82 |    0.15 |    5.75 |   0.15 |    599.19 | ever   | scarcer     | 114,075 |    545 | 72,839,571 |      0.85 |       81.15 |        0.99 |            2.06 |  8.96 |   1.98 |    0.00 |   0.00 |           0.15 |            0.07 | direct      |
| **[_direct_] ever~joint**       |   195 |    0.13 |    5.95 |   0.13 |  1,375.51 | ever   | joint       | 114,075 |  1,460 | 72,839,571 |      2.29 |      192.71 |        0.99 |            1.99 | 13.80 |   1.93 |    0.00 |   0.00 |           0.13 |            0.07 | direct      |
| **[_direct_] ever~nearer**      |   223 |    0.12 |    5.84 |   0.12 |  1,528.28 | ever   | nearer      | 114,075 |  1,836 | 72,839,571 |      2.88 |      220.12 |        0.99 |            1.95 | 14.74 |   1.89 |    0.00 |   0.00 |           0.12 |            0.06 | direct      |
| **[_direct_] ever~shrinking**   |   120 |    0.12 |    5.60 |   0.12 |    822.02 | ever   | shrinking   | 114,075 |    989 | 72,839,571 |      1.55 |      118.45 |        0.99 |            1.95 | 10.81 |   1.89 |    0.00 |   0.00 |           0.12 |            0.06 | direct      |
| **[_direct_] ever~closer**      | 6,307 |    0.10 |    6.08 |   0.10 | 41,328.73 | ever   | closer      | 114,075 | 61,475 | 72,839,571 |     96.28 |    6,210.72 |        0.98 |            1.89 | 78.20 |   1.82 |    0.05 |   0.06 |           0.10 |            0.08 | direct      |
| **[_direct_] ever~vigilant**    |   923 |    0.10 |    5.80 |   0.10 |  5,892.45 | ever   | vigilant    | 114,075 |  9,541 | 72,839,571 |     14.94 |      908.06 |        0.98 |            1.84 | 29.89 |   1.79 |    0.01 |   0.01 |           0.10 |            0.05 | direct      |


### 1. _ever quarterly_


|                                             | `token_str`                                                                                                                                                                                                                 |
|:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_021.1009_x0324851_07:7-8`**   | Bajaj Auto reported its highest - __`ever quarterly`__ dispatches of 1.16 million units , an increase of 16.3 % , in the three months to 30 September .                                                                     |
| **`pcc_eng_20_026.6234_x0414310_3:19-20`**  | " We are continuing to grow in a generally weak retail sector , and we noted our highest __`ever quarterly`__ earnings .                                                                                                    |
| **`pcc_eng_08_094.1749_x1508353_14:14-15`** | Tesla shares have tripled since the year began following the company 's first- __`ever quarterly`__ profit and slightly boosted annual production forecast for the Model S to 21,000 units from 20,000 .                    |
| **`pcc_eng_12_026.6180_x0414579_4:22-23`**  | Shares in India 's fraud- hit Punjab National Bank plunged more than 12 % on Wednesday after it posted the largest __`ever quarterly`__ loss for an Indian lender , AFP reported .                                          |
| **`pcc_eng_27_053.3683_x0846418_05:11-12`** | The Swoosh has been shaken up after suffering its first __`ever quarterly`__ profit slide the previous year .                                                                                                               |
| **`apw_eng_20080829_0935_8:8-9`**           | Lukoil called the figures `` the best __`ever quarterly`__ and semiannual results , '' but analysts said the oil producer has underperformed , struggling against a production decline at older fields in western Siberia . |
| **`pcc_eng_11_048.4576_x0767850_04:4-5`**   | posted its second- __`ever quarterly`__ net loss on Tuesday , the result of a one-time charge of $ 1.6 billion for the sale of 1,600 restaurants and development licenses in Latin America and the Caribbean .              |
| **`pcc_eng_17_002.5451_x0024881_08:8-9`**   | The company has recently posted its first __`ever quarterly`__ loss for the past three months of the year , while rival Samsung - and the primary source of HTC 's pain - posted record profits .                           |


### 2. _ever olympic_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                          |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_055.2173_x0877221_22:16-17`**  | At the 2008 Olympic 100 - metre finals in Beijing , China , her first __`ever Olympic`__ finals - Frazer - Pryce clocked a personal best 10.78s to win gold and become the first Jamaican woman to claim an Olympic 100 - metre title .                                                                              |
| **`pcc_eng_15_082.6115_x1318911_14:17-18`**  | From Amanda passing herself the puck off the boards for an unassisted goal in her first __`ever Olympic`__ game to Phil 's hat trick over Slovenia in the preliminary round - the Kessels are doing exactly what they set out to do - win .                                                                          |
| **`pcc_eng_19_023.4004_x0361640_097:15-16`** | At next year 's qualifying tournament , they 'll be playing for their first __`ever Olympic`__ berth in men's basketball and lacking the international experience of the other contenders for the top three spots .                                                                                                  |
| **`pcc_eng_09_022.7403_x0351893_48:8-9`**    | I dedicated the championship to our first __`ever Olympic`__ medalist in wrestling .                                                                                                                                                                                                                                 |
| **`pcc_eng_05_085.6327_x1369546_06:8-9`**    | Players Indoor is having its ' first __`ever Olympic`__ Games !                                                                                                                                                                                                                                                      |
| **`pcc_eng_11_042.4071_x0670248_06:32-33`**  | Simone Biles became the women 's individual all- round Olympic champion Teammate Aly Raisman earned silver , making up for her disappointment four years ago in London Fiji won its first __`ever Olympic`__ medal , winning gold in rugby sevens Michael Phelps won his 22nd gold medal , crushing the opposition i |
| **`pcc_eng_11_048.6263_x0770595_04:15-16`**  | He beat his idol in the 100 - meter butterfly to deliver the first __`ever Olympic`__ gold medal for the city -state of 5.54 million .                                                                                                                                                                               |
| **`pcc_eng_01_006.5425_x0089476_25:18-19`**  | It nearly guaranteed its first women 's field hockey medal on Wednesday , but lost the first __`ever Olympic`__ shootout contest on Wednesday against the Netherlands .                                                                                                                                              |


### 3. _ever watchful_


|                                               | `token_str`                                                                                                                                                                                                                                 |
|:----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_048.9239_x0775661_180:4-5`**    | Correspondent Nano , __`ever watchful`__ .                                                                                                                                                                                                  |
| **`pcc_eng_21_047.9569_x0758961_17:1-2`**     | Ever watchful , they remove obstacles and create support systems .                                                                                                                                                                          |
| **`pcc_eng_05_078.2462_x1250452_06:11-12`**   | We believe it is important for business leaders to remain __`ever watchful`__ for indicators of declining performance and to this end , Jim Collins provides an insightful list of decline indicating markers .                             |
| **`pcc_eng_19_017.8178_x0271346_0066:11-12`** | The doe inched toward the stream , ever careful , __`ever watchful`__ .                                                                                                                                                                     |
| **`pcc_eng_21_010.4379_x0152304_09:22-23`**   | In September 2014 , Islamic State spokesman Abu Mohammed al- Adnani published a lengthy piece entitled " Indeed Your Lord Is __`Ever Watchful`__ , " consisting largely of a call for Muslims to mount jihad attacks in Western countries . |
| **`pcc_eng_29_077.4400_x1235159_061:3-4`**    | In speech __`ever watchful`__ with mind well - restrained never with body do unwholesomeness .                                                                                                                                              |
| **`pcc_eng_17_073.6419_x1173916_28:5-6`**     | We need to be __`ever watchful`__ .                                                                                                                                                                                                         |
| **`pcc_eng_01_035.4169_x0556001_07:4-5`**     | they may be __`ever watchful`__ in keeping your commands .                                                                                                                                                                                  |


### 4. _ever diminishing_


|                                              | `token_str`                                                                                                                                                                                |
|:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_060.4568_x0962512_01:13-14`**  | Fractals are shapes in which an identical motif repeats itself on an __`ever diminishing`__ scale .                                                                                        |
| **`pcc_eng_17_022.3218_x0345153_092:14-15`** | Miners create a block after a period of time that 's worth an __`ever diminishing`__ amount of money or some sort of benefit to be able to ensure the deficit .                            |
| **`pcc_eng_19_009.3719_x0135421_78:12-13`**  | However , after seventeen decades of climate inaction there is an __`ever diminishing`__ window within which we must act if we are to avoid the worst impacts of a rapidly warming world . |
| **`pcc_eng_07_060.5728_x0963028_07:15-16`**  | In America , we celebrate the reality that , to a large , yet __`ever diminishing`__ extent , we are free to pursue our own desires in whatever way we see fit .                           |
| **`pcc_eng_05_063.4604_x1010618_119:14-15`** | Miners create a block after a period of time which is worth an __`ever diminishing`__ amount of currency or some sort of benefit so that you can ensure the shortage .                     |
| **`pcc_eng_29_064.1886_x1020978_066:13-14`** | Miners create a block after a time frame which is worth an __`ever diminishing`__ amount of currency or some kind of reward in order to ensure the shortfall .                             |
| **`pcc_eng_25_051.7358_x0821287_027:15-16`** | We 're bigger than a word , capable of more than one specific , __`ever diminishing`__ thing .                                                                                             |
| **`pcc_eng_05_077.3183_x1235236_016:13-14`** | Miners create a block after a time frame that is worth an __`ever diminishing`__ amount of money or some sort of wages so that you can ensure the shortfall .                              |


### 5. _ever scarcer_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                   |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_004.4929_x0056675_25:16-17`**  | But precisely this " raw material " of life -- time -- seems to be __`ever scarcer`__ .                                                                                                                                                                                                                                       |
| **`pcc_eng_10_015.3664_x0231993_51:12-13`**  | As populations rise and good agricultural land for growing food becomes __`ever scarcer`__ , if a food - based company such as Sainsbury 's are so keen to destroy agricultural land in the name of commercial expansion then what hope do we have to preserve the precious resource of farming land for future generations ? |
| **`pcc_eng_04_019.5080_x0298824_271:21-22`** | " We are facing a long decline as the resources to maintain the life we have grown accustomed to grow __`ever scarcer`__ .                                                                                                                                                                                                    |
| **`pcc_eng_28_050.1610_x0795453_37:10-11`**  | Plaintiffs who prevail in employment discrimination cases are becoming __`ever scarcer`__ .                                                                                                                                                                                                                                   |
| **`pcc_eng_08_021.8777_x0338066_05:13-14`**  | As The City 's rents rise even higher and real estate becomes __`ever scarcer`__ with more people flocking here to take advantage of the tech -fueled economic boom , a new kind of street person is emerging : older , gay , and living with HIV or AIDS .                                                                   |
| **`pcc_eng_24_043.8301_x0692320_07:8-9`**    | As public funding for conservation efforts grows __`ever scarcer`__ and the private sector is brimming with ideas about how its role -- along with its profits -- can grow , market forces have found their way into environmental management to a degree unimaginable only a few years ago .                                 |
| **`pcc_eng_22_076.3605_x1217952_08:8-9`**    | In China 's countryside , food became __`ever scarcer`__ .                                                                                                                                                                                                                                                                    |
| **`apw_eng_20070119_0711_31:23-24`**         | with large , top-grade bluefin tuna fetching up to 40,000 euros at Tokyo wholesale markets , Mediterranean vessels still go after the __`ever scarcer`__ big fish , eliminating the specimens that lay the most eggs .                                                                                                        |


### 6. _ever joint_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                       |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_054.6538_x0868097_10:8-9`**    | Most notable was agreement on the first __`ever joint`__ naval exercise between the MSDF and the Vietnamese navy .                                                                                                                                                                                                |
| **`pcc_eng_12_044.4919_x0703116_35:09-10`**  | The Fanboy Review is back with its second __`ever joint`__ review !                                                                                                                                                                                                                                               |
| **`pcc_eng_12_034.6663_x0544651_1:10-11`**   | The US and Israel will commence the largest - __`ever joint`__ air defense drill of its kind in Israel on October 21 , an army source said on Tuesday .                                                                                                                                                           |
| **`pcc_eng_06_054.6816_x0868551_02:15-16`**  | SEOUL . - The US and South Korea on Monday kicked off their largest __`ever joint`__ air exercise , an operation North Korea has labelled an " all - out provocation " , days after Pyongyang fired its most powerful intercontinental ballistic missile .                                                        |
| **`pcc_eng_12_018.5759_x0284353_07:13-14`**  | In May , the armies of the two countries held their biggest __`ever joint`__ exercise - Balance Iroquois - in the northern Indian city of Agra .                                                                                                                                                                  |
| **`pcc_eng_11_021.5601_x0332568_141:09-10`** | NATO and Russian fighter jets held their first __`ever joint`__ exercise .                                                                                                                                                                                                                                        |
| **`pcc_eng_28_012.6400_x0188427_02:16-17`**  | US politicians ' threats of a pre-emptive war against Pyongyang and the ongoing largest - __`ever joint`__ aerial drills by Seoul and Washington have made the outbreak of war on the Korean Peninsula " an established fact , " North Korea 's Foreign Ministry said .                                           |
| **`pcc_eng_26_043.9283_x0694242_03:7-8`**    | If anyone thought that the first __`ever joint`__ counter terror exercise carried out by Indian and Chinese militaries in Kunming in China 's Yunnan province would be an out and out serious affair , then one is grossly mistaken as it had a lot to do with cultural extravaganza and friendly bonhomie also . |


### 7. _ever nearer_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_003.7251_x0043713_01:31-32`** | The escalating outbreak of disease and displacement of tens of thousands by recent fighting has inflamed one of the world 's worst humanitarian crises , pushing Yemen 's war-pummelled society __`ever nearer`__ to collapse .                                                                                                                                                                                                                                |
| **`pcc_eng_01_014.4035_x0216274_09:28-29`** | At Wednesday 's ceremony , the 2012 medals will be shown to the world for the first time , yet another reminder that the Games are drawing __`ever nearer`__ .                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_27_001.6449_x0010262_02:26-27`** | But in the months since Attorney General Jeff Sessions recused himself from the ongoing collusion investigation , and as Special Counsel Robert Mueller has drawn __`ever nearer`__ to Trump 's inner circle , the president 's attacks have taken a darker turn , devolving into public castigations of his own Justice Department and top lawyer for failing to investigate and prosecute his one - time political opponent for a myriad of rumored crimes . |
| **`pcc_eng_06_072.2729_x1153020_2:28-29`**  | Combined , all of this weakness has worked to put downward pressure on the 25 market composite index , thwarting any chances for annual appreciation and bringing __`ever nearer`__ thespecter of a new post-panic low for prices .                                                                                                                                                                                                                            |
| **`pcc_eng_29_020.1018_x0308230_05:21-22`** | People either get excited about the imminent arrival of driverless cars , or become terrified that the machines are inching __`ever nearer`__ to put us all in danger .                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_15_007.8955_x0111307_15:20-21`** | At the same time , as graphics continue to evolve and photo-realism ( or its stylized equivalent ) draws __`ever nearer`__ , focus is shifting towards aspects other than graphical : clever AI , body kinetics , convincing and consistent world design , more options , more things to do - basically a better response to the player 's actions through physics , improved AI responses and all those little things that make the world work .              |
| **`pcc_eng_04_070.1504_x1116930_05:31-32`** | Ms. Kristoffer similarly suffers the horrors of CHINESE WATER TORTURE while the bodaciously buxom Ms. Robbins ironically finds herself on THE RACK and threatened by a medieval marital aid inching __`ever nearer`__ to you know where !                                                                                                                                                                                                                      |
| **`pcc_eng_11_059.1142_x0940311_10:12-13`** | In terms of economy , Turkey has everything to benefit from __`ever nearer`__ relations .                                                                                                                                                                                                                                                                                                                                                                      |


### 8. _ever shrinking_


|                                              | `token_str`                                                                                                                                                                                                                                                            |
|:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_023.8652_x0369340_52:13-14`**  | I was 5 Ks in the jungle , alone , with an __`ever shrinking`__ path .                                                                                                                                                                                                 |
| **`pcc_eng_12_068.9190_x1097534_10:16-17`**  | But today , doctors of all types are scrambling to maintain their income with an __`ever shrinking`__ insurance pot .                                                                                                                                                  |
| **`pcc_eng_29_004.1844_x0051579_110:12-13`** | Death is the great dread ; we all live in an __`ever shrinking`__ shadow of time , and between now and then all kinds of bad things could happen .                                                                                                                     |
| **`pcc_eng_28_003.8932_x0046765_18:28-29`**  | What it means is that by 2030 , Singapore will have as many people above 75 years of age as young people below 15 , and an __`ever shrinking`__ number of young people will have to look after a growing number of elderly folk .                                      |
| **`pcc_eng_18_050.7566_x0805625_32:19-20`**  | 5 . The Mr. Sam is an absolute flavor treat and will undoubtedly find a home in the __`ever shrinking`__ capacity of my humidor .                                                                                                                                      |
| **`pcc_eng_07_050.6514_x0802641_07:7-8`**    | There 's an incredibly sweet and __`ever shrinking`__ window around here -- after the trails empty out but before they get buried .                                                                                                                                    |
| **`pcc_eng_09_045.7609_x0724255_11:23-24`**  | In the last fifty years much of this has either been transformed , or else become increasingly redundant - catering for an __`ever shrinking`__ body of old-school scholars ; while much of the effective infrastructure that underpins research has moved elsewhere . |
| **`pcc_eng_26_016.3737_x0248399_09:8-9`**    | What forces everyone to fight is the __`ever shrinking`__ map which slowly brings all players closer together and forces them to engage each other .                                                                                                                   |


### 9. _ever closer_


|                                             | `token_str`                                                                                                                                                                                                                                                                        |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_022.9584_x0355324_19:32-33`** | Indeed , if we believe in the doctrine of sanctification and the kingdom living Jesus proclaims in the Sermon on the Mount , then our aim is to move our people __`ever closer`__ to being like Jesus ( 2 Cor 3:18 ; Rom 8:29 ; Matt 5 - 7) .1                                     |
| **`pcc_eng_29_056.3904_x0894822_22:8-9`**   | While the UPA government binds India into __`ever closer`__ strategic integration with the US , the CPI ( M ) voices only piecemeal opposition from time to time .                                                                                                                 |
| **`pcc_eng_16_026.2585_x0408918_36:19-20`** | Abstract : Much analysis of the European Union ( EU ) has focused on the process of " __`ever closer`__ union " .                                                                                                                                                                  |
| **`pcc_eng_21_022.0272_x0339556_15:36-37`** | It 's a destructive act of rebellion against the society that forces them to be there and while it 's amazing to see them finally doing something so honest and impulsive , they have edged __`ever closer`__ to the void , a place of pure chaos , which ca n't be a good thing . |
| **`pcc_eng_05_106.1657_x1700862_46:12-13`** | Bringing some of these shapes into your home can take you __`ever closer`__ to that mid century house you desire .                                                                                                                                                                 |
| **`pcc_eng_11_041.9886_x0663389_04:09-10`** | Dozens of wildlife species are endangered , pushed __`ever closer`__ to extinction by habitat loss and illegal trade .                                                                                                                                                             |
| **`pcc_eng_04_071.4568_x1137860_374:4-5`**  | " To climb __`ever closer`__ to God is not to move away from our troubled and troubling neighbors , but closer to them , " that from the author and new monastic Jonathan Wilson - Hartgrove                                                                                       |
| **`pcc_eng_12_037.8869_x0596594_11:5-6`**   | Seemingly , one crept __`ever closer`__ .                                                                                                                                                                                                                                          |


### 10. _ever vigilant_


|                                              | `token_str`                                                                                                                                                                                                                               |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_028.0809_x0438402_39:20-21`**  | With a focus on promoting the craft beer community in his hometown of Dayton , Ohio , he is __`ever vigilant`__ in hunting down the next great sample , pint , or bottle of beer .                                                        |
| **`pcc_eng_24_098.8871_x1583453_13:6-7`**    | Performance associated incentives maintain them __`ever vigilant`__ about non-compliers and policy - breakers .                                                                                                                           |
| **`pcc_eng_01_013.3320_x0199023_25:2-3`**    | Be __`ever vigilant`__ that pastors fulfill their office zealously , wisely and holily .                                                                                                                                                  |
| **`pcc_eng_25_037.2194_x0586255_21:4-5`**    | Wyckoffians must be __`ever vigilant`__ .                                                                                                                                                                                                 |
| **`pcc_eng_23_088.6266_x1416113_5:8-9`**     | Realizing your relationship with God is an __`ever vigilant`__ lifetime endeavor .                                                                                                                                                        |
| **`pcc_eng_24_001.4949_x0007981_27:1-2`**    | Ever vigilant , we 've scoured the online wire to find a treasure trove of juicy non -MS stories to share .                                                                                                                               |
| **`pcc_eng_08_069.2161_x1104712_05:1-2`**    | Ever vigilant against being the victim of an indifferent custodian of her people , the Cuians , though it rarely happened these days , she keeps her wits about her ; never gives anyone an excuse to point an accusatory finger at her . |
| **`pcc_eng_01_035.8037_x0562225_031:36-37`** | You know , when you have people arrested in Buffalo and Oregon , you realize , wait a minute , this network of terrorists has expanded throughout the world , and we have to be __`ever vigilant`__ , we have to be ever aggressive .     |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/`...
* Renaming existing version of `ever_closer_80ex~80.csv`
* Renaming existing version of `ever_vigilant_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_quarterly_80ex~28.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_olympic_80ex~31.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_watchful_80ex~71.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_diminishing_80ex~13.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_scarcer_80ex~18.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_joint_80ex~38.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_nearer_80ex~45.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_shrinking_80ex~13.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_closer_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/ever/ever_vigilant_80ex~80.csv`

## *yet*


|                                 |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`   | `l2`         |   `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:--------------------------------|------:|--------:|--------:|-------:|---------:|:-------|:-------------|-------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] yet~unborn**       |   372 |    0.72 |   10.14 |   0.72 | 4,319.00 | yet    | unborn       | 95,763 |    519 | 72,839,571 |      0.68 |      371.32 |        1.00 |            3.28 | 19.25 |   2.74 |    0.00 |   0.00 |           0.72 |            0.36 | direct      |
| **[_direct_] yet~unnamed**      |   736 |    0.35 |    8.29 |   0.35 | 7,048.15 | yet    | unnamed      | 95,763 |  2,107 | 72,839,571 |      2.77 |      733.23 |        1.00 |            2.61 | 27.03 |   2.42 |    0.01 |   0.01 |           0.35 |            0.18 | direct      |
| **[_direct_] yet~unspecified**  |   204 |    0.33 |    7.86 |   0.34 | 1,933.20 | yet    | unspecified  | 95,763 |    607 | 72,839,571 |      0.80 |      203.20 |        1.00 |            2.59 | 14.23 |   2.41 |    0.00 |   0.00 |           0.33 |            0.17 | direct      |
| **[_direct_] yet~untitled**     |   121 |    0.29 |    7.37 |   0.29 | 1,107.51 | yet    | untitled     | 95,763 |    412 | 72,839,571 |      0.54 |      120.46 |        1.00 |            2.50 | 10.95 |   2.35 |    0.00 |   0.00 |           0.29 |            0.15 | direct      |
| **[_direct_] yet~undetermined** |   297 |    0.27 |    7.55 |   0.27 | 2,658.03 | yet    | undetermined | 95,763 |  1,104 | 72,839,571 |      1.45 |      295.55 |        1.00 |            2.45 | 17.15 |   2.31 |    0.00 |   0.00 |           0.27 |            0.14 | direct      |
| **[_direct_] yet~unformed**     |    53 |    0.21 |    6.28 |   0.21 |   445.94 | yet    | unformed     | 95,763 |    249 | 72,839,571 |      0.33 |       52.67 |        0.99 |            2.32 |  7.24 |   2.21 |    0.00 |   0.00 |           0.21 |            0.11 | direct      |
| **[_direct_] yet~unidentified** |   336 |    0.18 |    6.85 |   0.18 | 2,694.33 | yet    | unidentified | 95,763 |  1,890 | 72,839,571 |      2.48 |      333.52 |        0.99 |            2.22 | 18.19 |   2.13 |    0.00 |   0.00 |           0.18 |            0.09 | direct      |
| **[_direct_] yet~unscheduled**  |    52 |    0.16 |    5.81 |   0.16 |   406.30 | yet    | unscheduled  | 95,763 |    321 | 72,839,571 |      0.42 |       51.58 |        0.99 |            2.17 |  7.15 |   2.09 |    0.00 |   0.00 |           0.16 |            0.08 | direct      |
| **[_direct_] yet~unannounced**  |   129 |    0.14 |    6.19 |   0.15 |   979.33 | yet    | unannounced  | 95,763 |    883 | 72,839,571 |      1.16 |      127.84 |        0.99 |            2.12 | 11.26 |   2.05 |    0.00 |   0.00 |           0.14 |            0.07 | direct      |
| **[_direct_] yet~unwritten**    |    75 |    0.14 |    5.83 |   0.14 |   562.71 | yet    | unwritten    | 95,763 |    535 | 72,839,571 |      0.70 |       74.30 |        0.99 |            2.10 |  8.58 |   2.03 |    0.00 |   0.00 |           0.14 |            0.07 | direct      |


### 1. _yet unborn_


|                                              | `token_str`                                                                                                                                                                                                                                                                     |
|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_085.3341_x1364987_235:13-14`** | Hopefully they will be in this same place listening to a preacher __`yet unborn`__ reminding them of the Lord 's life - and - death message and their need to pay it heed .                                                                                                     |
| **`nyt_eng_19991116_0269_13:8-9`**           | the apostles of our New Economy were __`yet unborn`__ .                                                                                                                                                                                                                         |
| **`pcc_eng_25_016.0180_x0242732_04:50-51`**  | Between an expensive , cruel , and unnecessary war , and billions to the rich and well - placed in political bribe paybacks , Uncle Sam is in debt up to his eyebrows , forcing the dollar down , inflation up , and a walloping tax burden on grandchildren __`yet unborn`__ . |
| **`pcc_eng_06_006.4568_x0088426_33:15-16`**  | Let us together recommit to preserving that dream for our children and the generations __`yet unborn`__ .                                                                                                                                                                       |
| **`pcc_eng_23_038.6672_x0608591_068:11-12`** | Let us protect our children , and grandchildren and generations __`yet unborn`__ from this imminent threat to America .                                                                                                                                                         |
| **`pcc_eng_07_028.8569_x0450622_12:34-35`**  | Miss Farida Yunusa has also promised that if she wins the competition , she will do her best to always contribute positively to society for a better Nigeria for everyone and the generations __`yet unborn`__ .                                                                |
| **`nyt_eng_20001219_0178_14:54-55`**         | in his State of the Union Message in 1971 , Nixon said , `` If we act boldly _ if we seize this moment , '' we could close great gaps , and warned in 1972 that `` if we failed to seize this moment , '' we would be untrue to generations __`yet unborn`__ .                  |
| **`nyt_eng_19960919_0285_39:15-16`**         | `` Their originators may die , but the reform will live to bless millions __`yet unborn`__ . ''                                                                                                                                                                                 |


### 2. _yet unnamed_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_053.1407_x0842522_06:51-52`**  | On June 17th , Treasury Secretary Jack Lew shocked many , including former Chairman of the Federal Reserve Ben Bernanke , when he proclaimed that Alexander Hamilton ( 1755 - 1804 ) -- the first and foremost Treasury Secretary -- would be demoted and share the ten-dollar bill with a __`yet unnamed`__ woman .                                                                                                                                                                       |
| **`apw_eng_20070108_0858_13:7-8`**           | the new defense minister , as __`yet unnamed`__ , will have the task of reducing the cost of Austria 's current contract for 18 combat jets that caused severe tension between the two parties , the Austria Press Agency reported .                                                                                                                                                                                                                                                       |
| **`nyt_eng_19950919_0353_25:36-37`**         | `` I 've eaten Vietnamese food in France , and I love it , '' said Lynn Wagenknecht , an owner of Kiosk and Odeon , who expects to open a Vietnamese restaurant , as __`yet unnamed`__ , at 100 West Houston Street , in SoHo , in November .                                                                                                                                                                                                                                              |
| **`pcc_eng_25_059.2497_x0943341_4:12-13`**   | - - - In Maple Grove , Minnesota , an as __`yet unnamed`__ bank robber arranged for a floral delivery to a Wells Fargo branch there - - - then called the bank manager , and told her that the accompanying package was a bomb - - - and instructed her to put some money in a garbage bag - - - and give it over to a waiting limo - - - the driver of which had been led to believe he was picking up some laundry - - - who then met the robber a couple of blocks away - - - MORE at = |
| **`pcc_eng_22_029.9848_x0467837_345:24-25`** | You and the mysterious woman will be brought together in some place now unknown , and will present to Mr. Armadale some liquid __`yet unnamed`__ , which will turn him faint ?                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_10_091.4883_x1462967_03:10-11`**  | The two groups will be merged into an as __`yet unnamed`__ new company , which will be the world 's third - largest capital goods maker by sales , in which investors will receive 3.828 shares per CNH share , and one share per Fiat Industrial share .                                                                                                                                                                                                                                  |
| **`nyt_eng_20001228_0208_28:26-27`**         | he has some advice of his own , based on his experiences , to pass along to his successor in the Bush administration , as __`yet unnamed`__ .                                                                                                                                                                                                                                                                                                                                              |
| **`nyt_eng_19950605_0660_20:14-15`**         | was it simply to clear the way for Silas and another , as __`yet unnamed`__ assistant , who are supposed to add an element of toughness , not to mention coach a little defense ? There is all this talk about how Silas is a disciplinarian who will impart the same take-no-prisoners attitude he displayed as a player .                                                                                                                                                                |


### 3. _yet unspecified_


|                                              | `token_str`                                                                                                                                                                                                                                                                               |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_034.0651_x0533640_6:27-28`**   | The House International Relations Committee late Tuesday cleared the sanctions measure unanimously , and the full House was to take it up Wednesday at an as __`yet unspecified`__ time .                                                                                                 |
| **`pcc_eng_17_001.2305_x0003638_52:26-27`**  | The U.S. Stock Exchange registration statement said that the principal intention " is to sell enough shares to new investors to pay off an as __`yet unspecified`__ portion of United 's [ US $ 658.23M ] debts , which the Glazers loaded on to the club when they bought it in 2005 . " |
| **`pcc_eng_20_029.7506_x0464920_41:19-20`**  | That may be accurate compared to what family films like this usually make and in light an as __`yet unspecified`__ large budget but it 's still within a couple of million of this weekend 's $ 50 - 70 million live-action hit .                                                         |
| **`pcc_eng_27_107.00999_x1716216_13:09-10`** | Ben Whishaw and Helen Mc Crory have as __`yet unspecified`__ roles .                                                                                                                                                                                                                      |
| **`nyt_eng_19951011_0637_9:29-30`**          | most of the justices are troubled by outsized verdicts , and the court has ruled that the constitutional guarantee of due process of law places some , as __`yet unspecified`__ , limits on punitive damages .                                                                            |
| **`pcc_eng_10_017.3613_x0264228_18:22-23`**  | Actors Tom Conti and 11 - year old Joey King have also joined the cast , but their roles are as __`yet unspecified`__ .                                                                                                                                                                   |
| **`apw_eng_19980528_1681_31:12-13`**         | Forluxe Securities , which went under this month , has as __`yet unspecified`__ debts .                                                                                                                                                                                                   |
| **`nyt_eng_20100722_0202_62:26-27`**         | after a closed investigation of nearly two years , a bipartisan subcommittee has properly concluded that there are grounds for charging the congressman with as __`yet unspecified`__ violations .                                                                                        |


### 4. _yet untitled_


|                                              | `token_str`                                                                                                                                                                                     |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_072.8881_x1162691_139:14-15`** | " X Japan is always evolving , " says Yoshiki about the as __`yet untitled`__ album .                                                                                                           |
| **`pcc_eng_22_070.8527_x1128986_04:2-3`**    | The __`yet untitled`__ movie will star John Abraham and Asin and will be directed by Nishikant Kamath .                                                                                         |
| **`pcc_eng_15_096.5566_x1544437_03:17-18`**  | David Floyd is currently in the process of writing original music for a new and as __`yet untitled`__ album .                                                                                   |
| **`pcc_eng_29_050.6094_x0801162_04:3-4`**    | Perry 's __`yet untitled`__ project will follow his character Madea on her comedic trials and tribulations , and will teach ' children about family values , in a way that only Madea could ! ' |
| **`apw_eng_20010725_0858_12:7-8`**           | Sigler 's debut album , as __`yet untitled`__ , is scheduled for release by BAB\/Edel Records in October .                                                                                      |
| **`pcc_eng_12_100.3433_x1605349_65:17-18`**  | Here 's a little of the art I 've done so far , for our as __`yet untitled`__ project .                                                                                                         |
| **`nyt_eng_19940818_0230_20:10-11`**         | he completed a fourth volume of memoirs , as __`yet untitled`__ , that will be published by Farrar , Straus & Giroux .                                                                          |
| **`pcc_eng_20_107.09759_x1728770_08:3-4`**   | An as __`yet untitled`__ photograph bt Brother Paul Quenon                                                                                                                                      |


### 5. _yet undetermined_


|                                              | `token_str`                                                                                                                                                                                                                                                             |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_19980401_1356_5:38-39`**          | the other teams that are scheduled to compete are Asian champion Saudi Arabia , African champion Egypt , South American runner-up Bolivia , defending champion Brazil , the Oceania champion still to be determined and an as __`yet undetermined`__ team from Europe . |
| **`apw_eng_20011113_1111_14:25-26`**         | under the EU bill , companies will be restricted in how they can use cookies and can only gather user data for an as __`yet undetermined`__ limited amount of time , before having to erase it unless governments request otherwise for security reasons .              |
| **`pcc_eng_17_021.6591_x0334480_21:13-14`**  | Those in the " slow " track will get it at a __`yet undetermined`__ date " after we see how everything goes " with the first batch of testers , according to Aul .                                                                                                      |
| **`nyt_eng_19990214_0159_31:11-12`**         | the treaty would take effect after a certain , as __`yet undetermined`__ , number of nations ratify it .                                                                                                                                                                |
| **`pcc_eng_01_074.7166_x1192341_341:2-3`**   | As __`yet undetermined`__ ?                                                                                                                                                                                                                                             |
| **`pcc_eng_19_042.1511_x0664322_206:30-31`** | I was burned out from journalism and had no career prospects or plans beyond a vague notion that I might want to write a book -- subject matter as __`yet undetermined`__ .                                                                                             |
| **`pcc_eng_09_095.6291_x1531141_18:7-8`**    | The book 's final stop is __`yet undetermined`__ .                                                                                                                                                                                                                      |
| **`pcc_eng_12_020.5855_x0316944_10:23-24`**  | The customs bill is a technical piece of legislation creating the legal powers for the government to put in place an as __`yet undetermined`__ customs policy on imposing duties on goods entering the country .                                                        |


### 6. _yet unformed_


|                                              | `token_str`                                                                                                                                                                                                                                    |
|:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_012.2350_x0181829_069:5-6`**   | Whilst earth , as __`yet unformed`__ and void ,                                                                                                                                                                                                |
| **`pcc_eng_20_064.5653_x1027027_14:3-4`**    | Bruce is __`yet unformed`__ as a psychiatrist , but he also feels somewhat underdeveloped as a character .                                                                                                                                     |
| **`pcc_eng_22_026.6374_x0413384_096:5-6`**   | Whilst Earth -- as __`yet unformed`__ and void --                                                                                                                                                                                              |
| **`pcc_eng_15_083.5671_x1334345_038:10-11`** | In both disciplines , models give shape to the __`yet unformed`__ , and climate specifically is known only through modeling .                                                                                                                  |
| **`pcc_eng_03_105.0142_x1684165_01:09-10`**  | Psalm 139:16-18Your eyes saw my substance , being __`yet unformed`__ .                                                                                                                                                                         |
| **`pcc_eng_15_054.6771_x0867481_112:5-6`**   | She is a person __`yet unformed`__ , becoming at times a plaything of the " older " dancers who , driven by momentary interest , roll her among each other .                                                                                   |
| **`pcc_eng_11_034.4915_x0542022_159:17-18`** | Second , the transformation of Soviet-American relations from a Cold War character to something else as __`yet unformed`__ is promoting a healthy questioning of the strategic utility of strategic -nuclear capabilities of different kinds . |
| **`pcc_eng_02_032.9829_x0517621_45:20-21`**  | Just like the environmental movement itself , local governments ' ideas and methods for handling these incidents are as __`yet unformed`__ .                                                                                                   |


### 7. _yet unidentified_


|                                              | `token_str`                                                                                                                                                                                                                                          |
|:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_009.6833_x0140362_34:13-14`**  | This is since in many cases the sex of the child is __`yet unidentified`__ .                                                                                                                                                                         |
| **`pcc_eng_10_035.4600_x0557277_014:30-31`** | This time protests erupted in the Sherman Park neighborhood of Milwaukee , Wisconsin following the killing of 23 - year- old African American Sylville K. Smith by an as __`yet unidentified`__ African American police officer Saturday afternoon . |
| **`pcc_eng_11_090.2391_x1444554_10:16-17`**  | His death in hospital overnight triggered renewed clashes in which a second person , as __`yet unidentified`__ , was killed by a home-made grenade , Mutlu said .                                                                                    |
| **`pcc_eng_26_010.5499_x0154290_21:24-25`**  | Roddey has emerged as a key figure in helping to recruit a mystery automotive venture , first publicly mentioned in May but as __`yet unidentified`__ , that could bring 1,500 jobs to the county .                                                  |
| **`pcc_eng_27_054.8168_x0869821_06:11-12`**  | Then they found out that a 13th player , as __`yet unidentified`__ , was on the field .                                                                                                                                                              |
| **`pcc_eng_26_011.7800_x0174281_23:22-23`**  | Instead , he wants a " green revolution " leading to the establishment of a government run by spotless but as __`yet unidentified`__ technocrats .                                                                                                   |
| **`pcc_eng_26_017.3078_x0263553_03:16-17`**  | Nearly three weeks have passed since Israeli warplanes conducted a mysterious raid against an as __`yet unidentified`__ target in northeast ...                                                                                                      |
| **`pcc_eng_03_048.3507_x0767001_24:20-21`**  | It is therefore likely that flints found at Happisburgh 3 were made by either Homo antecessor or an as __`yet unidentified`__ descendent of this species .                                                                                           |


### 8. _yet unscheduled_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                              |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19940726_0228_17:22-23`**        | U.S. Fish and Wildlife officials said Texans are over-reacting to the proposed designation , which will be the subject of as __`yet unscheduled`__ public hearings later this year .                                                                                                                                                     |
| **`pcc_eng_23_044.1208_x0696759_12:14-15`** | According to Rogin , the White House has decided to hold an as __`yet unscheduled`__ meeting of top officials to decide whether or not to release the $ 125 million that Rogin asserts is " on hold . "                                                                                                                                  |
| **`nyt_eng_19951117_0426_44:33-34`**        | about 23 percent of Learning Co. stock is held by management , so that 's one block it can count on when the Broderbund-Learning Co. bid goes to a vote , as __`yet unscheduled`__ .                                                                                                                                                     |
| **`pcc_eng_22_100.7929_x1612655_12:10-11`** | The coach plans to appeal the proposal at a __`yet unscheduled`__ hearing this month .                                                                                                                                                                                                                                                   |
| **`pcc_eng_21_051.7971_x0821166_12:43-44`** | The program included , Mr. Bungle 's Retrovertigo [ performed by Patton for the first time in almost 18 years ] , Chilean musical legend Violeta Parra 's Que He Sacado With Quererte , a new composition from the upcoming [ as __`yet unscheduled`__ ] collaboration between Patton and Jean- Claude Vannier titled Chansons D'amour . |
| **`nyt_eng_19960604_0144_31:22-23`**        | giving bonus shares to those that buy shares in the first tranche and hold them through to the next , as __`yet unscheduled`__ , share sale is something the company is considering , he said .                                                                                                                                          |
| **`pcc_eng_11_071.2533_x1137411_25:5-6`**   | But elections are as __`yet unscheduled`__ and dealing with decades of grievances , as well as the question of how much former Qaddafi loyalists will be allowed to participate in public life going forward , remain explosive issues that will have to be addressed in 2012 .                                                          |
| **`nyt_eng_20040924_0268_29:22-23`**        | attorneys for All Creatures immediately appealed the state 's decision to close the shelter and it remains open until the as __`yet unscheduled`__ appeal in the case is heard .                                                                                                                                                         |


### 9. _yet unannounced_


|                                              | `token_str`                                                                                                                                                                                                                                                |
|:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_051.8392_x0822002_4:8-9`**     | The release date is still as of __`yet unannounced`__ , with the window still being Fall of this year .                                                                                                                                                    |
| **`pcc_eng_25_008.3326_x0118869_082:19-20`** | And to follow that up , most likely there will be some kind of NHL realignment , as __`yet unannounced`__ , probably into an NFL type structure that will allow the NHL to expand easily to 40 teams .                                                     |
| **`pcc_eng_28_032.3889_x0507508_42:12-13`**  | He recently left Master Image 3D and is working on a __`yet unannounced`__ project .                                                                                                                                                                       |
| **`pcc_eng_05_101.8297_x1630922_40:6-7`**    | Google has posted an as __`yet unannounced`__ Glass update with an experimental " notification glance " feature .                                                                                                                                          |
| **`apw_eng_20070115_1140_9:7-8`**            | Ahtisaari 's widely anticipated but as __`yet unannounced`__ proposal would need U.N. Security Council approval before becoming an internationally accepted solution for the troubled province , which has been an international protectorate since 1999 . |
| **`pcc_eng_29_011.4181_x0168504_12:21-22`**  | The race kicks off on August 18 , after which the Star Car will be passed on to another as __`yet unannounced`__ driver for the Pahrump Nugget 250 at the end of November .                                                                                |
| **`pcc_eng_18_080.4433_x1286293_09:14-15`**  | That 'll be on the Play Station 4 and some other platforms as __`yet unannounced`__ . "                                                                                                                                                                    |
| **`pcc_eng_17_072.3332_x1152713_01:10-11`**  | The album of the year nominees are ... as __`yet unannounced`__ .                                                                                                                                                                                          |


### 10. _yet unwritten_


|                                              | `token_str`                                                                                                                                                                                                                                     |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_058.9415_x0936465_39:5-6`**    | The ending is as __`yet unwritten`__ .                                                                                                                                                                                                          |
| **`pcc_eng_20_006.3350_x0085930_261:22-23`** | I 'm discovering many things that are grounding , things I always took for granted : a playlist for an as __`yet unwritten`__ novel , a particular series of books , consuming ridiculous amounts of Chick - Fil -A , country music from 1998 . |
| **`pcc_eng_28_010.9421_x0160807_04:37-38`**  | If this tournament 's No. 1 overall seed does reach New Orleans , there 's a good chance they will have some harrowing war stories to tell , starting with Royce White and including chapters as __`yet unwritten`__ .                          |
| **`pcc_eng_12_048.8606_x0773449_068:25-26`** | While the emergency actions taken by world central bankers has slowed the contraction of credit and cascading of defaults , the full story is __`yet unwritten`__ .                                                                             |
| **`pcc_eng_29_096.6278_x1544877_20:09-10`**  | Here 's a story whose ending is as __`yet unwritten`__ .                                                                                                                                                                                        |
| **`pcc_eng_08_055.5575_x0883476_12:15-16`**  | Q. A noun , an adjective and a verb find themselves in an as __`yet unwritten`__ line of a Rachel Zavecz poem .                                                                                                                                 |
| **`pcc_eng_09_065.7134_x1046860_31:20-21`**  | When she gets to the end of each book she sees that there are still many chapters that are __`yet unwritten`__ .                                                                                                                                |
| **`pcc_eng_17_048.4092_x0765941_72:7-8`**    | The story behind it , as __`yet unwritten`__ .                                                                                                                                                                                                  |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/`...
* Renaming existing version of `yet_unnamed_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unborn_80ex~72.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unnamed_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unspecified_80ex~28.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_untitled_80ex~19.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_undetermined_80ex~51.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unformed_80ex~9.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unidentified_80ex~53.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unscheduled_80ex~8.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unannounced_80ex~19.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/yet/yet_unwritten_80ex~12.csv`

## *immediately*


|                                         |    `f` |   `dP1` |   `LRC` |   `P1` |       `G2` | `l1`        | `l2`         |   `f1` |    `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |    `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:----------------------------------------|-------:|--------:|--------:|-------:|-----------:|:------------|:-------------|-------:|--------:|-----------:|----------:|------------:|------------:|----------------:|-------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] immediately~appealable**   |     76 |    0.55 |    8.41 |   0.55 |     815.23 | immediately | appealable   | 96,973 |     139 | 72,839,571 |      0.19 |       75.81 |        1.00 |            2.96 |   8.70 |   2.61 |    0.00 |   0.00 |           0.55 |            0.27 | direct      |
| **[_direct_] immediately~accretive**    |    236 |    0.45 |    8.54 |   0.45 |   2,406.67 | immediately | accretive    | 96,973 |     523 | 72,839,571 |      0.70 |      235.30 |        1.00 |            2.79 |  15.32 |   2.53 |    0.00 |   0.00 |           0.45 |            0.23 | direct      |
| **[_direct_] immediately~adjacent**     |  1,595 |    0.33 |    8.31 |   0.34 |  15,089.64 | immediately | adjacent     | 96,973 |   4,756 | 72,839,571 |      6.33 |    1,588.67 |        1.00 |            2.59 |  39.78 |   2.40 |    0.02 |   0.02 |           0.33 |            0.18 | direct      |
| **[_direct_] immediately~apparent**     |  4,971 |    0.09 |    6.12 |   0.09 |  32,982.98 | immediately | apparent     | 96,973 |  54,246 | 72,839,571 |     72.22 |    4,898.78 |        0.99 |            1.90 |  69.48 |   1.84 |    0.05 |   0.05 |           0.09 |            0.07 | direct      |
| **[_mirror_] immediately~recognizable** |     58 |    0.09 |    5.98 |   0.09 |     456.86 | immediately | recognizable |  1,195 |     640 |  1,701,929 |      0.45 |       57.55 |        0.99 |            2.18 |   7.56 |   2.11 |    0.05 |   0.05 |           0.09 |            0.07 | mirror      |
| **[_direct_] immediately~actionable**   |    173 |    0.09 |    5.47 |   0.09 |   1,121.82 | immediately | actionable   | 96,973 |   1,983 | 72,839,571 |      2.64 |      170.36 |        0.98 |            1.86 |  12.95 |   1.82 |    0.00 |   0.00 |           0.09 |            0.04 | direct      |
| **[_direct_] immediately~subsequent**   |     59 |    0.08 |    4.81 |   0.08 |     374.58 | immediately | subsequent   | 96,973 |     722 | 72,839,571 |      0.96 |       58.04 |        0.98 |            1.83 |   7.56 |   1.79 |    0.00 |   0.00 |           0.08 |            0.04 | direct      |
| **[_direct_] immediately~clear**        | 26,038 |    0.07 |    5.86 |   0.07 | 167,884.90 | immediately | clear        | 96,973 | 349,214 | 72,839,571 |    464.92 |   25,573.08 |        0.98 |            1.92 | 158.48 |   1.75 |    0.26 |   0.27 |           0.26 |            0.17 | direct      |
| **[_direct_] immediately~prior**        |     66 |    0.06 |    4.35 |   0.06 |     372.18 | immediately | prior        | 96,973 |   1,145 | 72,839,571 |      1.52 |       64.48 |        0.98 |            1.67 |   7.94 |   1.64 |    0.00 |   0.00 |           0.06 |            0.03 | direct      |
| **[_direct_] immediately~recognizable** |  1,736 |    0.05 |    5.15 |   0.05 |   9,447.17 | immediately | recognizable | 96,973 |  33,499 | 72,839,571 |     44.60 |    1,691.40 |        0.97 |            1.62 |  40.59 |   1.59 |    0.02 |   0.02 |           0.05 |            0.03 | direct      |


### 1. _immediately appealable_


|                                                   | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|:--------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_077.6049_x1240298_14:23-24-25`**    | Generally , the denial of a motion to dismiss under Rule 12 ( b ) ( 6 ) , SCRCP , is not __`immediately appealable`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_08_077.6049_x1240298_30:32-33-34`**    | After a careful analysis of section 14- 3- 330 and the authority cited herein , we find the denial of Appellants ' motion to dismiss based on forum non conveniens is not __`immediately appealable`__ . [ 3 ]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_12_103.5395_x1657178_19:8-9`**         | Our court concluded such an order was __`immediately appealable`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_08_077.6049_x1240298_29:114-115-116`** | See King v. Cessna Aircraft Co. , 562 F.3d 1374 , 1378-81 ( 11th Cir. 2009 ) ( finding the denial of a motion to dismiss on the basis of forum non conveniens is not a final , appealable order ) ; Rosenstein v. Merrell Dow Pharm. , Inc. , 769 F.2d 352 , 354 ( 6th Cir. 1985 ) ( holding the denial of a motion to dismiss on forum non conveniens grounds is not __`immediately appealable`__ under collateral order exception to final judgment rule ) ; Rolinski v. Lewis , 828 A.2d 739 , 742 ( D.C. 2003 ) ( holding that denials of forum non conveniens motions to dismiss are not __`immediately appealable`__ as of right ) ; Payton-Henderson v. Evans , 949 A.2d 654 , 662 ( Md. Ct. Spec. App. 2008 ) ( stating forum non conveniens issues are treated the same as change of venue and the denial of either is not __`immediately appealable`__ ) . |
| **`nyt_eng_19990603_0257_49:4-5`**                | the ruling is __`immediately appealable`__ , which the AJC is doing , so no one is being hauled in .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **`nyt_eng_19960221_0286_141:15-16-17`**          | Johnson held , simply , that determinations of evidentiary sufficiency at summary judgment are not __`immediately appealable`__ merely because they happen to arise in a qualified-immunity case ; if what is at issue in the sufficiency determination is nothing more than whether the evidence could support a finding that particular conduct occurred , the question decided is not truly `` separable '' from the plaintiff 's claim , and hence there is no `` final decision '' under Cohen and Mitchell .                                                                                                                                                                                                                                                                                                                                                   |
| **`nyt_eng_19950612_0267_21:29-30`**              | second , under Cohen v. Beneficial Industrial Loan Corp. , 337 U. S. 541 , and subsequent decisions , a so-called `` collateral order '' amounts to an __`immediately appealable`__ `` final decisio -LRB- n -RRB- '' under s1291 , even though the district court may have entered it long before the case has ended , if the order -LRB- 1 -RRB- conclusively determines the disputed question , -LRB- 2 -RRB- resolves an important issue completely separate from the merits of the action , and -LRB- 3 -RRB- will be effectively unreviewable on appeal from the final judgment .                                                                                                                                                                                                                                                                              |
| **`pcc_eng_08_077.6049_x1240298_26:31-32-33`**    | The Supreme Court held that the question of the convenience of the forum is not " completely separate from the merits of the action , " and thus , is not __`immediately appealable`__ as of right .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |


### 2. _immediately accretive_


|                                              | `token_str`                                                                                                                                                                                        |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_031.7023_x0495643_18:6-7`**    | Both of these transactions are __`immediately accretive`__ to our earnings . "                                                                                                                     |
| **`pcc_eng_25_028.2464_x0440862_09:17-18`**  | The property is being purchased with a going in capitalization rate of 6 % and is __`immediately accretive`__ to the REIT .                                                                        |
| **`pcc_eng_10_107.01606_x1716696_16:15-16`** | And a topping $ 42 a share bid funded predominantly with cash would be __`immediately accretive`__ to Priceline even before factoring in any synergies , according to data compiled by Bloomberg . |
| **`pcc_eng_13_084.9815_x1357565_17:09-10`**  | Rogers said it expects the deal to be __`immediately accretive`__ to its media division 's operating profit .                                                                                      |
| **`pcc_eng_09_023.0019_x0356120_13:7-8`**    | The acquisition is expected to be __`immediately accretive`__ to earnings .                                                                                                                        |
| **`pcc_eng_26_018.1741_x0277614_05:15-16`**  | The deal will add more than $ 1,700,000 in annual revenue and will be __`immediately accretive`__ to Silver Sun 's earnings .                                                                      |
| **`pcc_eng_20_007.9912_x0112746_15:25-26`**  | We also further enhanced our financial flexibility by paying down $ 2.5 billion in debt , which will reduce our interest expense and be __`immediately accretive`__ .                              |
| **`pcc_eng_22_011.4102_x0167994_03:16-17`**  | The acquisition enhances Endo 's attractive commercialization and development platform and is expected to be __`immediately accretive`__ to Endo 's 2014 adjusted earnings per share ( EPS ) .     |


### 3. _immediately adjacent_


|                                             | `token_str`                                                                                                                                                                                                                                          |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_015.3581_x0232186_2:7-8`**    | Situated mid-block on West Pender , __`immediately adjacent`__ to the Bentall Centre , 1050 West Pender offers ease of access to restaurants , hotels & shopping .                                                                                   |
| **`pcc_eng_07_049.6502_x0786438_11:14-15`** | The building is a remarkable place , owned and built by London Transport __`immediately adjacent`__ to the tube line and , indeed , with a secret direct access to the platform .                                                                    |
| **`pcc_eng_21_052.3451_x0830064_2:18-19`**  | The physical security ramifications for failure on this project must have been immense , considering the buildings __`immediately adjacent`__ to the hole .                                                                                          |
| **`pcc_eng_24_002.6162_x0026019_16:20-21`** | The study found that food plots were causing an increase in browse intensity on commercial tree species to areas __`immediately adjacent`__ ( 0 - 2 meters ) to the food plots .                                                                     |
| **`pcc_eng_18_028.2970_x0441526_26:5-6`**   | The find spot was __`immediately adjacent`__ to a natural pond , and the tile was installed to follow a natural swale that drained higher parts of the field into the pond .                                                                         |
| **`pcc_eng_04_098.2386_x1571025_18:16-17`** | One dealt with the creation of the Moffitt Cafe Express convenience store , which is __`immediately adjacent`__ to the Moffitt Cafe .                                                                                                                |
| **`nyt_eng_20100801_0182_17:15-16`**        | the two-and-a-half-mile-wide demilitarized zone , which divides the two Koreas , and the land __`immediately adjacent`__ to it on either side are heavily seeded with land mines to guard against infiltration by soldiers from the North or South . |
| **`pcc_eng_25_019.9364_x0305986_03:22-23`** | Releases of petroleum contaminants from a retail gasoline station in a medium-sized California Central Valley town threatened a municipal supply well __`immediately adjacent`__ and approximately 200 ft downgradient to the station .              |


### 4. _immediately apparent_


|                                                 | `token_str`                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20001207_0139_9:20-21`**             | Bullet fragments are scattered like lethal confetti throughout the X-ray of the dead man 's shoulder and chest , __`immediately apparent`__ to even a layman .                                                  |
| **`pcc_eng_01_081.9685_x1309124_26:6-7`**       | Business cost overhead savings are __`immediately apparent`__ .                                                                                                                                                 |
| **`pcc_eng_04_018.5116_x0282922_07:16-17`**     | The nineteenth - century French economist Frederic Bastiat exhorted us to look beyond what is __`immediately apparent`__ to the harder - to - see but still -real effects of policies like tariffs .            |
| **`pcc_eng_23_044.6296_x0704976_09:13-14`**     | This long hiatus in hosting amplified musical performances inside the room became __`immediately apparent`__ at the outset , though band and engineers would persevere through the host of sound difficulties . |
| **`pcc_eng_17_073.1987_x1166742_066:16-17-18`** | The premise of the show is a fairly basic revenge tale , but this is n't __`immediately apparent`__ , even through the first half of the show .                                                                 |
| **`pcc_eng_12_068.1343_x1084871_52:20-21-22`**  | Once he devises the rules for a particular movie , he 's extremely rigorous although those rules are often not __`immediately apparent`__ :                                                                     |
| **`pcc_eng_05_046.1906_x0731506_103:12-13`**    | While some of those changes were internal , one would become __`immediately apparent`__ to anyone who saw her .                                                                                                 |
| **`apw_eng_20090125_0804_18:14-15`**            | `` The character , love and true friendship of the Bahamian people became __`immediately apparent`__ during our time of crisis , '' the statement read .                                                        |


### 5. _immediately recognizable_


|                                              | `token_str`                                                                                                                                                                                   |
|:---------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_008.5262_x0122051_17:16-17`**  | Of course , however , like with all great composers Stockhausen 's personal voice is __`immediately recognizable`__ in most of his works throughout his career .                              |
| **`pcc_eng_04_099.0720_x1584389_19:4-5`**    | Their lineage is __`immediately recognizable`__ , which is pretty much the source of their charm .                                                                                            |
| **`pcc_eng_04_074.9044_x1193741_4:10-11`**   | The functional and flexible becomes couture and fashion , __`immediately recognizable`__ .                                                                                                    |
| **`pcc_eng_26_108.05137_x1739143_23:11-12`** | She has a smooth vocal quality that is ethereal and __`immediately recognizable`__ .                                                                                                          |
| **`pcc_eng_00_044.0159_x0695093_08:4-5`**    | That bassline is __`immediately recognizable`__ and was probably later sampled in plenty of hip hop tunes ( I 'd look that info up if I was actually interested in it ) .                     |
| **`pcc_eng_16_024.9000_x0386873_14:5-6`**    | Altair 's outfit is __`immediately recognizable`__ with its enclosed Assassin 's hood that covers his neck , revealing only his face in shadow .                                              |
| **`pcc_eng_12_063.0977_x1004097_57:4-5`**    | Press books are __`immediately recognizable`__ :                                                                                                                                              |
| **`pcc_eng_29_049.0992_x0776635_08:25-26`**  | " What 's real about the show is the emotions and the people , though they may be from the distant future , are __`immediately recognizable`__ and people will relate to these characters . " |


### 6. _immediately actionable_


|                                              | `token_str`                                                                                                                                                                                                                                           |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_025.4102_x0394339_011:29-30`** | The point of using a service like toodledo , for me , is to avoid having to rely on manual intervention and to show the shortest list of __`immediately actionable`__ tasks possible .                                                                |
| **`pcc_eng_16_026.1288_x0406809_11:5-6`**    | This summit will include __`immediately actionable`__ topics such as *                                                                                                                                                                                |
| **`pcc_eng_27_102.9812_x1649800_23:27-28`**  | From top to bottom , most senior to least experienced , every single person on my team walked out of the two days with practical , __`immediately actionable`__ new skills . "                                                                        |
| **`pcc_eng_21_066.3814_x1056527_133:7-8`**   | It 's all pretty cool and __`immediately actionable`__ .                                                                                                                                                                                              |
| **`pcc_eng_05_034.6773_x0545370_16:11-12`**  | We filter out the bad information and provide you with __`immediately actionable`__ information of the highest possible quality to help you reach your ultimate health goals .                                                                        |
| **`pcc_eng_06_067.7856_x1080725_14:21-22`**  | Somewhere in the process the SSG provided the CNO with a high- level blueprint as well as a roadmap with __`immediately actionable`__ steps - operational , process , and technological that our Navy can take to begin developing the capabilities . |
| **`pcc_eng_27_019.5522_x0300049_21:09-10`**  | It 's culture combined with growth techniques in __`immediately actionable`__ takeaways .                                                                                                                                                             |
| **`pcc_eng_02_050.6768_x0803732_25:22-23`**  | For labs running Thermo Fisher equipment , the new quantitative reporting platform from CLS provides faster , more accurate results with __`immediately actionable`__ guidance for informed decision-making .                                         |


### 7. _immediately subsequent_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_097.7754_x1564582_07:11-12`**  | When a notable rise in ratings failed to materialize in __`immediately subsequent`__ survey periods coupled with widespread criticism by radio industry observers of the stations ' formats and execution - further exacerbated by Michaels receiving negative publicity in the midst of all this for being arrested on DUI charges - the heat was on and Michaels began facing enormous internal and external pressure to modify the programming approach . |
| **`pcc_eng_27_100.5741_x1610802_061:11-12`** | In addition to the above-specified Directors , during the year __`immediately subsequent`__ to his retirement , the retiring SSA Chair shall be a Director - at - Large if he will not otherwise be serving as a duly elected Director .                                                                                                                                                                                                                     |
| **`pcc_eng_08_031.1414_x0488068_125:25-26`** | Unfortunately for the latter , that story of Godfrey 's offer and acceptance had been communicated to Isabella , as had of course the __`immediately subsequent`__ story of their separation .                                                                                                                                                                                                                                                               |
| **`pcc_eng_11_033.1568_x0520437_039:4-5`**   | Benjamin explains how __`immediately subsequent`__ to a strike ( invariably painted as a victory by the U.S. media ) , local terrorist groups mobilize to identify the persons who provided the information used to locate and ultimately effect the deaths of their comrades .                                                                                                                                                                              |
| **`pcc_eng_04_027.6216_x0430208_12:16-17`**  | Mostly , Boll 's reputation emerged out of a string of videogame adaptations he made __`immediately subsequent`__ to Heart of America , with House of the Dead ( 2003 ) , Alone in the Dark ( 2005 ) , Bloodrayne ( 2005 ) ,                                                                                                                                                                                                                                 |
| **`pcc_eng_18_062.0383_x0988160_03:32-33`**  | At issue , as FHQ has discussed , is the discrepancy between the longstanding New Hampshire election law that requires seven days between the primary in the Granite state and the __`immediately subsequent`__ primary or caucus and a newly -enacted Nevada Republican Party resolution tethering the party 's caucuses to the Saturday following the New Hampshire primary .                                                                              |
| **`pcc_eng_01_012.9535_x0192993_12:24-25`**  | Raven and Dani are here in place of Emily and Gar joins in later on as we discuss the undeniably predictable un-betrayal and __`immediately subsequent`__ death of Katsuragi Shinobu , Kairi and Tsukasa have a weird adopted mommy moment , and Cluster ......                                                                                                                                                                                              |
| **`pcc_eng_05_077.3101_x1235099_223:22-23`** | Secondly , they shift the active cells in the primary selector column so that each corresponds to the CAM array sections __`immediately subsequent`__ to the previous matching CAM array sections .                                                                                                                                                                                                                                                          |


### 8. _immediately clear_


|                                                | `token_str`                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20080316_0480_6:3-4-5`**            | it was not __`immediately clear`__ if he was referring to China 's overall policies in Tibet when he spoke of a genocide , or the recent crackdown .                                                                                        |
| **`apw_eng_20020925_0388_4:3-4-5`**            | it was not __`immediately clear`__ what , if any , conflicts the simultaneous presence of Bush and Espin would generate .                                                                                                                   |
| **`pcc_eng_15_019.6160_x0300737_11:3-4-5`**    | It was n't __`immediately clear`__ whether there were any injuries .                                                                                                                                                                        |
| **`pcc_eng_18_010.5264_x0154063_13:3-4-5`**    | It was n't __`immediately clear`__ if the planes had been deployed .                                                                                                                                                                        |
| **`apw_eng_20091113_0469_9:3-4-5`**            | it was not __`immediately clear`__ where commission-bound detainees like al-Nashiri might be sent , but a military brig in South Carolina has been high on the list of considered sites .                                                   |
| **`pcc_eng_25_005.3013_x0070083_12:5-6-7`**    | However , it is not __`immediately clear`__ whether Mr. Odwar is the kinds of John the Baptist who had come ahead of Jesus to prepare the way , in this case , it remains to be seen whether his boss Machar will follow him to Juba soon . |
| **`pcc_eng_23_001.7846_x0012714_07:3-4-5`**    | It 's not __`immediately clear`__ if any other executives have been shuffled amid the departure .                                                                                                                                           |
| **`pcc_eng_04_006.7547_x0093078_23:16-17-18`** | Whether these actions go far enough to stem the tide of criticism against Facebook is n't __`immediately clear`__ .                                                                                                                         |


### 9. _immediately prior_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:---------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_016.4737_x0249933_12:19-20`**  | Oddly it has much , though perhaps in the end a little too much in common with the __`immediately prior`__ Disney release , Frozen .                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_25_008.2058_x0116865_061:73-74`** | ( e) No adjustment shall be made in the Conversion Price as the result of the issuance of Additional Shares of Common Stock or otherwise , unless the consideration per share determined pursuant to subpart ( h ) of this Section 11 for an Additional Share of Common Stock issued or deemed to be issued by the Maker is less than the Conversion Price in effect on the date of , and __`immediately prior`__ to , the issuance of such Additional Shares of Common Stock .                                                                                                   |
| **`pcc_eng_15_021.0759_x0324447_23:26-27`**  | This site is optimized for use in Internet Explorer and AOL running on Windows Operating System ; we shall fully support the most current and __`immediately prior`__ version of these browsers .                                                                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_21_051.5648_x0817422_003:12-13`** | Harry 's second appearance at the Con ( his first , __`immediately prior`__ , was with Brian Aldiss on How to Write a Best Seller ) in Hall 4 was for a one-man-show in the Third Programme , called The Stainless Steel Rat Speaks Esperanto , a title doubtless given to attract Stainless Steel Rat fans to what was intended to be a fairly straight talk on Esperanto .                                                                                                                                                                                                      |
| **`pcc_eng_12_035.2527_x0554053_7:32-33`**   | ( Rates subject to change monthly based on like term interest rate swaps published by the Federal Reserve Board in its H.15 Release as of the last Friday of the month __`immediately prior`__ . )                                                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_24_097.6139_x1562795_08:17-18`**  | There are three levels of first-person limited narration , with each successive level embedded in the __`immediately prior`__ level .                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_04_072.4855_x1154648_19:13-14`**  | During the period , Pulse Asia said various issues preoccupied Filipinos " __`immediately prior`__ to and during the conduct of the field interviews , " including the filing of graft and plunder charges against three senators and other public officials for alleged misuse of pork barrel funds , the decision by the Supreme Court declaring certain actions and provisions of the Disbursement Acceleration Program ( DAP ) as unconstitutional , and the controversial decision of Aquino to reject the nomination of movie star Nora Aunor as National Artist for Film . |
| **`pcc_eng_22_101.3586_x1621751_08:14-15`**  | Here is a look back at the major historical figures of the years __`immediately prior`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/`...
* Renaming existing version of `immediately_adjacent_80ex~80.csv`
* Renaming existing version of `immediately_apparent_80ex~80.csv`
* Renaming existing version of `immediately_recognizable_80ex~80.csv`
* Renaming existing version of `immediately_clear_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_appealable_80ex~20.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_accretive_80ex~42.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_adjacent_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_apparent_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_recognizable_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_actionable_80ex~37.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_subsequent_80ex~9.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_clear_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/immediately/immediately_prior_80ex~12.csv`

## *particularly*


|                                         |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`         | `l2`        |    `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:----------------------------------------|------:|--------:|--------:|-------:|----------:|:-------------|:------------|--------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] particularly~hard-hit**    |   154 |    0.39 |    5.64 |   0.39 |  1,005.08 | particularly | hard-hit    | 513,668 |    391 | 72,839,571 |      2.76 |      151.24 |        0.98 |            1.96 | 12.19 |   1.75 |    0.00 |   0.00 |           0.39 |            0.19 | direct      |
| **[_direct_] particularly~well-suited** |    62 |    0.35 |    4.91 |   0.36 |    390.17 | particularly | well-suited | 513,668 |    173 | 72,839,571 |      1.22 |       60.78 |        0.98 |            1.90 |  7.72 |   1.71 |    0.00 |   0.00 |           0.35 |            0.18 | direct      |
| **[_direct_] particularly~galling**     |   540 |    0.24 |    5.12 |   0.25 |  2,937.15 | particularly | galling     | 513,668 |  2,174 | 72,839,571 |     15.33 |      524.67 |        0.97 |            1.67 | 22.58 |   1.55 |    0.00 |   0.00 |           0.24 |            0.12 | direct      |
| **[_direct_] particularly~nettlesome**  |    63 |    0.21 |    4.02 |   0.22 |    324.87 | particularly | nettlesome  | 513,668 |    288 | 72,839,571 |      2.03 |       60.97 |        0.97 |            1.60 |  7.68 |   1.49 |    0.00 |   0.00 |           0.21 |            0.11 | direct      |
| **[_mirror_] particularly~noteworthy**  |    99 |    0.21 |    4.23 |   0.21 |    491.30 | particularly | noteworthy  |  13,003 |    462 |  1,701,929 |      3.53 |       95.47 |        0.96 |            1.55 |  9.60 |   1.45 |    0.01 |   0.01 |           0.21 |            0.11 | mirror      |
| **[_direct_] particularly~acute**       | 2,809 |    0.17 |    4.79 |   0.18 | 13,361.56 | particularly | acute       | 513,668 | 15,489 | 72,839,571 |    109.23 |    2,699.77 |        0.96 |            1.50 | 50.94 |   1.41 |    0.01 |   0.01 |           0.17 |            0.09 | direct      |
| **[_direct_] particularly~thorny**      |   308 |    0.17 |    4.36 |   0.17 |  1,439.60 | particularly | thorny      | 513,668 |  1,762 | 72,839,571 |     12.43 |      295.57 |        0.96 |            1.48 | 16.84 |   1.39 |    0.00 |   0.00 |           0.17 |            0.08 | direct      |
| **[_mirror_] particularly~novel**       |    54 |    0.16 |    3.47 |   0.17 |    240.22 | particularly | novel       |  13,003 |    320 |  1,701,929 |      2.44 |       51.56 |        0.95 |            1.43 |  7.02 |   1.34 |    0.00 |   0.00 |           0.16 |            0.08 | mirror      |
| **[_direct_] particularly~irksome**     |   155 |    0.15 |    3.90 |   0.15 |    680.19 | particularly | irksome     | 513,668 |  1,016 | 72,839,571 |      7.16 |      147.84 |        0.95 |            1.41 | 11.87 |   1.34 |    0.00 |   0.00 |           0.15 |            0.07 | direct      |
| **[_direct_] particularly~noteworthy**  | 2,294 |    0.14 |    4.37 |   0.14 |  9,788.31 | particularly | noteworthy  | 513,668 | 15,975 | 72,839,571 |    112.66 |    2,181.34 |        0.95 |            1.38 | 45.54 |   1.31 |    0.00 |   0.00 |           0.14 |            0.07 | direct      |


### 1. _particularly hard-hit_


|                                      | `token_str`                                                                                                                                                                                                                                                               |
|:-------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20011207_1366_2:39-40`**  | the Labor Department report Friday showed just how devastating the Sept. 11 terrorist attacks were on the labor market , prompting huge layoffs across a wide swath of the U.S. economy , with airlines and other travel-related industries __`particularly hard-hit`__ . |
| **`apw_eng_20011211_0087_27:21-22`** | the figures reflect huge post-attack layoffs across a swath of the U.S. economy , with airlines and other travel industries __`particularly hard-hit`__ .                                                                                                                 |
| **`apw_eng_20050308_0202_6:5-6`**    | Britain and France were __`particularly hard-hit`__ by mad cow disease , known formally as bovine spongiform encephalopathy , after the illness was detected in 1986 .                                                                                                    |
| **`nyt_eng_19990927_0384_1:17-18`**  | stock prices rebounded a bit Monday , as investors became selective buyers of shares that were __`particularly hard-hit`__ by last week 's steep sell-off .                                                                                                               |
| **`apw_eng_19950831_1151_16:7-8`**   | Russia 's struggling farm sector is __`particularly hard-hit`__ this year because of drought , and some estimates say the grain harvest will be the lowest in three decades .                                                                                             |
| **`apw_eng_20020112_0056_4:27-28`**  | `` It 's more than eight hours away by donkey , the terrain is mountainous , it was a former front-line area and the villagers were __`particularly hard-hit`__ by the drought . ''                                                                                       |
| **`apw_eng_20070918_1273_7:33-34`**  | `` The American dream is in peril for many families in this country as foreclosures rise and dreams shatter , '' Rep. Betty Sutton , a Democrat from Ohio , a state __`particularly hard-hit`__ by the default wave , declared in House debate before the vote .          |
| **`apw_eng_20070130_1554_20:35-36`** | since Bush took office in 2001 , however , the country has seen one in five manufacturing jobs disappear , a total of 2.96 million lost jobs , with U.S. automakers and textile companies __`particularly hard-hit`__ .                                                   |


### 2. _particularly well-suited_


|                                         | `token_str`                                                                                                                                                                                                                                                                 |
|:----------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20060922_0092_20:14-15-16`** | `` I do n't think he liked being president , and he was n't __`particularly well-suited`__ to the job , '' Seligman said .                                                                                                                                                  |
| **`nyt_eng_20050407_0320_48:8-9`**      | `` One of the things theater is __`particularly well-suited`__ for is really exploring a lot of different sides to one issue , and it is a huge relief to me that this group of plays really looks deeply at subjects we just do n't see often in the mainstream media . '' |
| **`nyt_eng_20001229_0026_26:18-19`**    | `` Readers of business books are often just looking for snippets of information and that makes them __`particularly well-suited`__ for the Internet . ''                                                                                                                    |
| **`nyt_eng_19940908_0392_13:19-20`**    | but the plutonium produced by its two breeders , Monju and Joyo , is a kind that is __`particularly well-suited`__ to bombs , Greenpeace said .                                                                                                                             |
| **`nyt_eng_19950706_0144_18:5-6`**      | the travel business is __`particularly well-suited`__ to marriage with the multimedia revolution , since it is the world 's fastest-growing industry and has already created a vast market for conventional publishing through guidebooks .                                 |
| **`apw_eng_20070928_0553_6:26-27`**     | `` AstraZeneca has embarked on its own change journey including the transformational move into large-scale biologics this year , so Simon 's background makes him __`particularly well-suited`__ to this role , '' he added .                                               |
| **`apw_eng_20000126_0062_19:5-6`**      | `` New England is __`particularly well-suited`__ for him , '' Kessler told the judge .                                                                                                                                                                                      |
| **`nyt_eng_20040901_0055_7:17-18`**     | Miller , the Democratic senator of Georgia and a pariah in his own party , is __`particularly well-suited`__ to attacking John Kerry , though he once called him an `` authentic hero . ''                                                                                  |


### 3. _particularly galling_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                                                                |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_049.6298_x0785917_16:8-9`**   | For Mr Caird , the graffiti was __`particularly galling`__ .                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_29_104.8502_x1678068_147:8-9`**  | One clause in the settlement agreement was __`particularly galling`__ .                                                                                                                                                                                                                                                                                                    |
| **`apw_eng_20080913_0251_19:8-9`**          | the brazen presence in Poti has been __`particularly galling`__ for Georgia because it is hundreds of kilometers -LRB- miles -RRB- from South Ossetia , where the war broke out and where most of the fighting occurred .                                                                                                                                                  |
| **`nyt_eng_20041218_0184_15:7-8`**          | local leaders said they found it __`particularly galling`__ that the Social Security Administration failed to distinguish between the marriage documents issued for gay and straight couples , especially since the 300 or so same-sex marriage affidavits issued by West 's office read and look very different from the marriage certificates issued by the town clerk . |
| **`pcc_eng_21_041.7527_x0658956_09:11-12`** | Still , getting flagged by the maker of Budweiser sounds __`particularly galling`__ , inasmuch as beer and football are so inextricably linked , and the company has pretty much treated the Super Bowl as its own special showcase for as long as anyone can remember .                                                                                                   |
| **`nyt_eng_20060824_0176_29:1-2`**          | particularly galling to flight attendants is that Northwest 's operations were profitable during the second quarter and will probably be in the black this quarter , too .                                                                                                                                                                                                 |
| **`nyt_eng_19950622_0010_17:5-6`**          | the latest setback was __`particularly galling`__ .                                                                                                                                                                                                                                                                                                                        |
| **`nyt_eng_19960921_0242_34:5-6`**          | the mascot incident was __`particularly galling`__ .                                                                                                                                                                                                                                                                                                                       |


### 4. _particularly nettlesome_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                   |
|:--------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20041102_0116_9:4-5`**           | it is a __`particularly nettlesome`__ issue for the stars of the show 's first two seasons -- Clarkson , Studdard and Aiken -- who are releasing albums without the hype of a just-finished television victory behind them .                                                                                                  |
| **`nyt_eng_20040905_0106_13:32-33`**        | this year , union members are looking for new ways to extend their influence , by getting members elected to local offices and by trying to oust an administration it finds __`particularly nettlesome`__ .                                                                                                                   |
| **`pcc_eng_23_049.7808_x0788058_09:16-17`** | DDo S has been common in online gaming for years , and it 's become __`particularly nettlesome`__ around Minecraft , where black - hat players use low-grade DDo S as a form of cheating or bullying , and professional server operators routinely face larger versions of the attack at the hands of unethical competitors . |
| **`nyt_eng_19951113_0680_30:09-10`**        | the latter partnership may turn out to be __`particularly nettlesome`__ to Microsoft .                                                                                                                                                                                                                                        |
| **`nyt_eng_20040915_0143_33:4-5`**          | Algebra is a __`particularly nettlesome`__ subject , the stage in a math curriculum where discouragement is most likely to set in .                                                                                                                                                                                           |
| **`nyt_eng_19940804_0354_10:35-36`**        | a person close to Diller said this missed opportunity , while relatively minor compared with the profit of some $ 100 million that Diller will take away from the QVC buyout , had been __`particularly nettlesome`__ to the QVC chairman .                                                                                   |
| **`pcc_eng_00_063.8264_x1015809_30:15-16`** | What if they could apply the amazing predictive power of fuzzy logic to a __`particularly nettlesome`__ medical problem ?                                                                                                                                                                                                     |
| **`pcc_eng_06_029.9625_x0468667_27:6-7`**   | Two developments concerning Taiwan were __`particularly nettlesome`__ to U.S. policymakers in 2005-2006 .                                                                                                                                                                                                                     |


### 5. _particularly noteworthy_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_043.4086_x0685411_07:11-12`** | Over the next four weeks , we will highlight some __`particularly noteworthy`__ research : from using computing to better understand the body 's immune response to HIV and AIDS , to measuring and modeling complex ecosystems and global environment conditions , to tools that inspire and enable citizen-scientists around the world .                                                                                                                                                                                                                                  |
| **`pcc_eng_04_099.8037_x1596280_18:34-35`** | Decision Will Probably Be Appealed but Law Will Still Be Suspended Constitutional vagueness challenges to state laws are extremely difficult to win , particularly in California firearms litigation , so this success is __`particularly noteworthy`__ .                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_03_046.5895_x0738600_13:1-2`**   | Particularly noteworthy is the new ladder , whose rungs have been replaced with non-slip plastic steps .                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_17_050.0634_x0792554_31:7-8`**   | The " Vermont " episode was __`particularly noteworthy`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_29_020.1903_x0309680_26:22-23`** | Other advances in polarimetry ( as for vegetation and other surface structure signature analysis ) , in multi- band SAR ( __`particularly noteworthy`__ : A. Reigber , also from DLR , on an integrated airborne SAR system involving P , L , S , C , and X - band operation , with S and X multiple apertures for interferometry ) , in broadband pulse compression ( for high range resolution in SBR and other SAR imaging ) , were covered and provide a great resource for keeping our courses current and " connected " to the active international radar community . |
| **`pcc_eng_04_072.1011_x1148350_08:2-3`**   | A __`particularly noteworthy`__ moment of the House debate occurred when Frank Niceley ( R- District 17 ) misinvoked the authority of Albert Einstein in support of HB 368 , quoting the physicist as saying , according to the Knoxville News Sentinel ( April 8 , 2011 ) , " A little knowledge would turn your head to atheism , while a broader knowledge would turn your head to Christianity . "                                                                                                                                                                      |
| **`pcc_eng_28_036.1245_x0568067_15:1-2`**   | Particularly noteworthy is the mosaic floor of the Church of St Stephen with its representation of towns in the region .                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_28_013.6563_x0205030_064:3-4`**  | What is __`particularly noteworthy`__ is the case of Taiwan , which the report regards as a model to watch and to emulate .                                                                                                                                                                                                                                                                                                                                                                                                                                                 |


### 6. _particularly acute_


|                                             | `token_str`                                                                                                                                                                                                                                  |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20100916_0097_11:17-18`**        | here in California , backers of the initiative have seized on that anxiety -- which is __`particularly acute`__ in this state , with its 12.3 percent unemployment rate -- in search of a victory .                                          |
| **`pcc_eng_05_029.1928_x0456662_20:15-16`** | He said the two leaders discussed " the dangers of protectionism , which becomes __`particularly acute`__ in times of recession . "                                                                                                          |
| **`pcc_eng_14_024.7871_x0384237_18:4-5`**   | Problems have become __`particularly acute`__ in the West , followed by the Midwest , Northeast and South , according to the survey .                                                                                                        |
| **`pcc_eng_00_073.7346_x1175820_26:4-5`**   | The problem is __`particularly acute`__ in Toronto , which despite its wealth , is still the worst city in Canada for children , according to The Hidden Epidemic report released last week .                                                |
| **`pcc_eng_16_079.5281_x1270954_18:27-28`** | A community college in southwestern Michigan is expanding its nursing and health education building in an attempt to combat a growing shortage of nurses that seems __`particularly acute`__ in the area .                                   |
| **`pcc_eng_13_030.3646_x0474892_03:8-9`**   | Today the problem of resort areas is __`particularly acute`__ .                                                                                                                                                                              |
| **`apw_eng_19990228_1016_10:6-7`**          | `` The Y2K problem is __`particularly acute`__ for small and medium-sized enterprises , '' the paper said .                                                                                                                                  |
| **`pcc_eng_21_008.9233_x0127814_14:31-32`** | It faces the eternal conundrum that plagues all ad-driven business -- while trying to win people 's money , you may just get them angry -- but this problem becomes __`particularly acute`__ when you 're tracking people on mobile phones . |


### 7. _particularly thorny_


|                                              | `token_str`                                                                                                                                                                                                                                                                      |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20041012_0175_21:24-25`**         | as the court learned during its consideration of the Pledge of Allegiance case during the past term , the school environment presents a __`particularly thorny`__ issue .                                                                                                        |
| **`nyt_eng_19940812_0008_11:6-7`**           | this seems to be a __`particularly thorny`__ problem for the Dodgers , who paid Darryl Strawberry $ 4 million after he did not show up for work because he was on drugs .                                                                                                        |
| **`pcc_eng_27_057.9944_x0921278_08:16-17`**  | With a certain regularity they would individually come to his corporate office to discuss a __`particularly thorny`__ issue .                                                                                                                                                    |
| **`pcc_eng_08_062.9330_x1003099_031:5-6`**   | Interracial adoption is a __`particularly thorny`__ issue to challenge because few would question that adoptive parents love their children , and certainly Ng does n't -- but then again , her narrative gently suggests that perhaps that 's not the only thing that matters . |
| **`pcc_eng_06_009.1456_x0131620_080:12-13`** | A Ravenclaw could forget food if they were immersed in a __`particularly thorny`__ object of study .                                                                                                                                                                             |
| **`apw_eng_19990928_0191_5:10-11`**          | then there 's the matter of gambling , a __`particularly thorny`__ issue with the NBA .                                                                                                                                                                                          |
| **`pcc_eng_27_002.4217_x0022833_071:5-6`**   | Currency problems can be __`particularly thorny`__ .                                                                                                                                                                                                                             |
| **`nyt_eng_19960608_0225_10:5-6`**           | `` It 's a __`particularly thorny`__ issue in smaller buildings , '' Ms. Arougheti said .                                                                                                                                                                                        |


### 8. _particularly novel_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_037.2059_x0585353_46:7-8`**      | Murray has pushed the matter in __`particularly novel`__ ways .                                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_11_003.0853_x0033856_05:2-3`**      | One __`particularly novel`__ tribute is MGo View .                                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_22_007.1907_x0099856_16:55-60-61`** | More realistic Superman clones , law enforcement agencies dedicated to superhero activity , superheroes letting their power and skewed perspective drive them bonkers , superheroes " going bad , " superheroes as they would " really " be , or a world that reacts to super-people like we react to real life celebrities ; none of these things are __`particularly novel`__ anymore . |
| **`pcc_eng_03_085.6512_x1370701_05:17-18-19`** | In a city where five-star restaurants are tucked away in nondescript strip malls , there 's nothing __`particularly novel`__ about a high / low culinary mash- up .                                                                                                                                                                                                                       |
| **`pcc_eng_10_049.5724_x0785567_29:6-7-8`**    | In truth , there 's nothing __`particularly novel`__ or disquieting about the scheme Murray 's drawn up , except insofar as the procedural extremism conservatives have deployed in the Obama era is alarming in general .                                                                                                                                                                |
| **`pcc_eng_26_009.6880_x0140416_047:3-4-5`**   | This is nothing __`particularly novel`__ .                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_28_048.5566_x0769388_031:7-8-9`**   | The idea of electronic money is not __`particularly novel`__ .                                                                                                                                                                                                                                                                                                                            |
| **`nyt_eng_20000602_0053_10:3-4-5`**           | there is nothing __`particularly novel`__ about that .                                                                                                                                                                                                                                                                                                                                    |


### 9. _particularly irksome_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                     |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20020626_0299_5:1-2`**            | particularly irksome , as Segar 's question indicates , is the fact that the asylum center proposal comes fast on the heels of another indignity visited on Throckmorton : the dumping last year of tens of thousands of decomposing animal carcasses , casualties of the foot-and-mouth crisis , in a huge pit in the middle of a field here . |
| **`pcc_eng_04_042.1488_x0665003_12:3-4`**    | It is __`particularly irksome`__ for me , since I use Reader as the main service provider for my Reeder app on i OS and OS X.                                                                                                                                                                                                                   |
| **`nyt_eng_20051015_0024_62:1-2`**           | particularly irksome are calls by Alan Greenspan , the Federal Reserve chairman , to shrink Fannie Mae and Freddie Mac , the quasi-government institutions that buy huge numbers of mortgages from financial institutions , notably from Countrywide .                                                                                          |
| **`pcc_eng_19_054.3277_x0860584_322:09-10`** | She wants you to target and destroy a __`particularly irksome`__ naga warrior in her name . ''                                                                                                                                                                                                                                                  |
| **`pcc_eng_22_038.1904_x0600862_21:11-12`**  | Stereogum 's Claire Lobenfeld found " Stop Pretending , " __`particularly irksome`__ , calling it " mansplaining " ( when a man , intentionally or otherwise , uses a condescending tone to explain something to a woman that she already knows ) at its most egregious . "                                                                     |
| **`pcc_eng_26_021.4166_x0329992_01:3-4`**    | What 's __`particularly irksome`__ about this is that Obama , a student of history and a law lecturer , has surely thought through the broader ramifications of his decision .                                                                                                                                                                  |
| **`pcc_eng_06_068.6114_x1093968_01:3-4`**    | It is __`particularly irksome`__ , since I have duly informed Sprint / Nextel of this fact twice a year , every year , since 2007 .                                                                                                                                                                                                             |
| **`pcc_eng_12_038.8661_x0612568_230:5-6`**   | The informal economy is __`particularly irksome`__ because its works outside state ( and taxation ) structures .                                                                                                                                                                                                                                |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/`...
* Renaming existing version of `particularly_galling_80ex~80.csv`
* Renaming existing version of `particularly_noteworthy_80ex~80.csv`
* Renaming existing version of `particularly_acute_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_hard-hit_80ex~25.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_well-suited_80ex~14.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_galling_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_nettlesome_80ex~18.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_noteworthy_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_acute_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_thorny_80ex~58.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_novel_80ex~51.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/particularly/particularly_irksome_80ex~28.csv`

## *inherently*


|                                             |   `f` |   `dP1` |   `LRC` |   `P1` |     `G2` | `l1`       | `l2`              |   `f1` |   `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:--------------------------------------------|------:|--------:|--------:|-------:|---------:|:-----------|:------------------|-------:|-------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] inherently~governmental**      |   253 |    0.33 |    8.92 |   0.33 | 2,742.59 | inherently | governmental      | 47,803 |    761 | 72,839,571 |      0.50 |      252.50 |        1.00 |            2.88 | 15.87 |   2.70 |    0.01 |   0.01 |           0.33 |            0.17 | direct      |
| **[_mirror_] inherently~wrong**             | 1,826 |    0.09 |    4.80 |   0.09 | 9,626.26 | inherently | wrong             |  5,133 | 20,880 |  1,701,929 |     62.97 |    1,763.03 |        0.97 |            1.69 | 41.26 |   1.46 |    0.34 |   0.36 |           0.34 |            0.21 | mirror      |
| **[_mirror_] inherently~evil**              |    99 |    0.07 |    3.94 |   0.08 |   462.56 | inherently | evil              |  5,133 |  1,271 |  1,701,929 |      3.83 |       95.17 |        0.96 |            1.46 |  9.56 |   1.41 |    0.02 |   0.02 |           0.07 |            0.05 | mirror      |
| **[_direct_] inherently~coercive**          |    94 |    0.07 |    5.98 |   0.08 |   711.86 | inherently | coercive          | 47,803 |  1,253 | 72,839,571 |      0.82 |       93.18 |        0.99 |            2.09 |  9.61 |   2.06 |    0.00 |   0.00 |           0.07 |            0.04 | direct      |
| **[_direct_] inherently~unequal**           |   390 |    0.07 |    6.38 |   0.07 | 2,893.14 | inherently | unequal           | 47,803 |  5,621 | 72,839,571 |      3.69 |      386.31 |        0.99 |            2.06 | 19.56 |   2.02 |    0.01 |   0.01 |           0.07 |            0.04 | direct      |
| **[_direct_] inherently~untrustworthy**     |    69 |    0.06 |    5.39 |   0.06 |   483.61 | inherently | untrustworthy     | 47,803 |  1,211 | 72,839,571 |      0.79 |       68.21 |        0.99 |            1.97 |  8.21 |   1.94 |    0.00 |   0.00 |           0.06 |            0.03 | direct      |
| **[_direct_] inherently~indiscriminate**    |    58 |    0.05 |    5.22 |   0.06 |   402.96 | inherently | indiscriminate    | 47,803 |  1,049 | 72,839,571 |      0.69 |       57.31 |        0.99 |            1.95 |  7.53 |   1.93 |    0.00 |   0.00 |           0.05 |            0.03 | direct      |
| **[_direct_] inherently~evil**              | 1,123 |    0.05 |    6.05 |   0.05 | 7,572.62 | inherently | evil              | 47,803 | 22,706 | 72,839,571 |     14.90 |    1,108.10 |        0.99 |            1.91 | 33.07 |   1.88 |    0.02 |   0.02 |           0.05 |            0.04 | direct      |
| **[_direct_] inherently~interdisciplinary** |    94 |    0.05 |    5.35 |   0.05 |   631.33 | inherently | interdisciplinary | 47,803 |  1,906 | 72,839,571 |      1.25 |       92.75 |        0.99 |            1.90 |  9.57 |   1.88 |    0.00 |   0.00 |           0.05 |            0.03 | direct      |
| **[_direct_] inherently~sinful**            |   145 |    0.05 |    5.49 |   0.05 |   962.39 | inherently | sinful            | 47,803 |  3,059 | 72,839,571 |      2.01 |      142.99 |        0.99 |            1.88 | 11.87 |   1.86 |    0.00 |   0.00 |           0.05 |            0.02 | direct      |


### 1. _inherently governmental_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_051.7548_x0820477_05:21-22`**    | While reviewing listings for federal government contractor jobs , the Project On Government Oversight was reminded of the confusion surrounding __`inherently governmental`__ functions .                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_15_098.1891_x1570838_23:34-35-36`** | Some IRS officials said that the agency was once reluctant to conduct competitive sourcing studies , which encourages agencies to cut costs by competing with the private sector for federal jobs that are not __`inherently governmental`__ .                                                                                                                                                                                                                                                        |
| **`pcc_eng_24_010.3236_x0150513_69:22-23`**    | The lack of a policy leaves an open range of issues , including the question of whether cloud hosting is an __`inherently governmental`__ function or a closely associated function .                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_07_058.9343_x0936353_13:21-22`**    | The size of government , government regulations , and entitlement and transfer programs , should be limited to essential , __`inherently governmental`__ functions .                                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_19_039.8077_x0626127_51:12-13`**    | He strongly asserts that human intelligence ( HUMINT ) is an __`inherently governmental`__ function because it affects relationships between nations .                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_22_054.4825_x0864110_02:15-16`**    | " When it comes to security in war zones , what is considered ' __`inherently governmental`__ ? '                                                                                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_21_023.9152_x0370222_11:70-71`**    | Clanahan is somewhat vague about whether contractors in the program are performing or have performed __`inherently governmental`__ functions , stating only that " there have been situations " where contractors might have crossed the line and either commanded military forces or participated in combat operations , activities which would be in violation of the Federal Acquisition Regulation ( FAR ) and the White House 's 2011 policy letter on __`inherently governmental`__ functions . |
| **`pcc_eng_23_093.2198_x1490504_08:17-18`**    | " This is especially a problem when contractors are used to carry out activities that are __`inherently governmental`__ . "                                                                                                                                                                                                                                                                                                                                                                           |


### 2. _inherently wrong_


|                                                | `token_str`                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_101.3877_x1624153_67:4-5-6`**    | ' There is nothing __`inherently wrong`__ with a guy wanting to get some feedback on his beard with the simple intent to make himself look better .                                                |
| **`pcc_eng_07_011.9578_x0177585_09:21-22-23`** | Legendary games such as Twilight Imperium or Here I Stand are notoriously complex ( and long ) and there is nothing __`inherently wrong`__ with that ( well , maybe apart from the length ) .      |
| **`pcc_eng_21_038.3732_x0604271_418:4-5`**     | There 's something __`inherently wrong`__ with the system in this country which led to the financial crisis , is n't there ?                                                                       |
| **`pcc_eng_06_076.5613_x1222036_36:5-6-7`**    | Sure -- there 's nothing __`inherently wrong`__ with something like Martini & Rossi .                                                                                                              |
| **`nyt_eng_20000305_0169_22:3-4-5`**           | there is nothing __`inherently wrong`__ with patronage .                                                                                                                                           |
| **`pcc_eng_01_099.8104_x1597304_172:3-4-5`**   | There is nothing __`inherently wrong`__ with having a politics that is essentially a religion , providing that you recognise it for what it is , something personal between you and your friends . |
| **`pcc_eng_15_092.2704_x1475230_081:4-5`**     | There is something __`inherently wrong`__ about the direction the things mentioned in the post above are leading .                                                                                 |
| **`pcc_eng_21_097.0240_x1551391_57:17-18-19`** | Look , as a Black man , White people often frustrate me -- but there 's nothing __`inherently wrong`__ with being White .                                                                          |


### 3. _inherently evil_


|                                                 | `token_str`                                                                                                                                                                                                                    |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_034.4478_x0540478_09:09-10`**     | The first is the argument that capitalism is __`inherently evil`__ and must be strictly curbed if not completely replaced by socialism .                                                                                       |
| **`pcc_eng_22_008.1033_x0114616_192:24-25`**    | At some point a lot of us started listening to heavier and heavier bands until we came across Slayer 's extremely catchy yet __`inherently evil`__ sounding riffs which opened the door for us to the world of extreme metal . |
| **`nyt_eng_19990416_0075_8:3-4-5`**             | television is not __`inherently evil`__ , as is the implication .                                                                                                                                                              |
| **`pcc_eng_23_049.3832_x0781737_119:12-13`**    | ... and Whatshername , the mage who is worried she 's __`inherently evil`__ and has turne to the religion that says she 's evil to get solace .                                                                                |
| **`pcc_eng_19_067.2348_x1069391_6:12-13`**      | I 've come to the necessary conclusion that central banks are __`inherently evil`__ .                                                                                                                                          |
| **`pcc_eng_05_037.0167_x0583270_081:16-17-18`** | There are some who use their money for less ambitious purposes , but money is not __`inherently evil`__ .                                                                                                                      |
| **`pcc_eng_23_095.2839_x1523991_3:4-5-6`**      | Insurance companies are n't __`inherently evil`__ .                                                                                                                                                                            |
| **`pcc_eng_25_011.5414_x0170505_091:15-16`**    | But I think the question is backwards , here 's why : Man is __`inherently evil`__ , even the best of us struggle daily to " do the right thing " and can cause pain in others without even thinking about it .                |


### 4. _inherently coercive_


|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                             |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20011204_0352_11:26-27`**           | still , Donna Lieberman , the interim executive director of the New York Civil Liberties Union , said the requests for the interviews were `` __`inherently coercive`__ . ''                                                                                                                                                                                            |
| **`pcc_eng_25_016.0431_x0243129_047:7-8`**     | The moment of silence is an __`inherently coercive`__ institution .                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_27_023.1549_x0358192_31:19-20`**    | Yet to me the most compelling case against democracy is the very notion that the state , an __`inherently coercive`__ and collectivistic monopoly , be somehow associated with the best interests of the greater society .                                                                                                                                              |
| **`pcc_eng_04_004.4880_x0056540_21:26-27`**    | To keep people from obeying their cells ' and organs ' natural tendencies by just walking away from this culture , it is of necessity __`inherently coercive`__ , using hierarchy , violence , threat of imprisonment , propaganda and other means to ensure obedience and conformity of the group .                                                                    |
| **`pcc_eng_29_043.5310_x0687089_46:11-12-13`** | While direct contact is somewhat more intrusive , it is not __`inherently coercive`__ .                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_09_046.6341_x0738347_131:36-37`**   | This court has noted that , because of the conflicting interests involved , a delicate balance must be achieved between the employer 's need to prepare adequately for pending unfair labor practice cases and the __`inherently coercive`__ nature ( in violation of an employee 's Section 7 rights ) of employer interrogation of employees during a labor dispute . |
| **`pcc_eng_26_014.4632_x0217613_028:13-14`**   | Some allege physical abuse ; all allege that they were in an __`inherently coercive`__ environment .                                                                                                                                                                                                                                                                    |
| **`pcc_eng_25_028.9535_x0452371_27:6-7`**      | The international border is an __`inherently coercive`__ environment , where harried travelers must seek permission to come home from uniformed and frequently armed agents in an unfamiliar space .                                                                                                                                                                    |


### 5. _inherently unequal_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                                                                                |
|:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_039.1845_x0618021_32:5-6`**   | Separate educational facilities are __`inherently unequal`__ " ( Brown , p. 495 ) .                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_27_014.8647_x0224208_25:35-36`** | Based on the premise that charity is an inherent part of capitalism , the Communist Zizek sees that it is unable and unwilling to create real change since it is a part of an __`inherently unequal`__ system .                                                                                                                                                                            |
| **`pcc_eng_09_020.2580_x0311715_11:20-21`** | Bad enough , because a judge and law clerk enjoy a relationship that is at once uniquely intimate and __`inherently unequal`__ .                                                                                                                                                                                                                                                           |
| **`pcc_eng_28_043.3414_x0685079_36:35-36`** | He first became widely known in the South when he translated into English the work of the French count Arthur de Gobineau , who had argued that mankind was divided into three different and __`inherently unequal`__ races , the white , the black and the yellow .                                                                                                                       |
| **`pcc_eng_01_061.6758_x0981340_19:64-65`** | The veteran attorney is considered something of an icon in nearby Prince Edward County , a racially troubled spot in the ' 50s and ' 60s where local government officials fought school integration all the way to the Supreme Court in Brown v. Board of Education - the landmark case in which the Court ruled that " separate but equal " institutions are __`inherently unequal`__ .   |
| **`nyt_eng_19950701_0037_19:41-42`**        | almost from the start , Brown 's reliance on social science conclusions concerning educational effects had drawn sharp professional criticism even from the decision 's supporters , for , as one commentator recently explained , `` something that is ` __`inherently unequal`__ ' is not so because of empirical data , but because of its very nature , known through pure reason . '' |
| **`pcc_eng_26_013.1817_x0196619_20:36-37`** | This is a spiritual and ethical problem , especially for those among us who believe that humans are made in the image of the Divine and who at the same time believe we were made __`inherently unequal`__ in Divine physical and mental endowment .                                                                                                                                       |
| **`pcc_eng_07_097.1857_x1554516_32:5-6`**   | Separate educational facilities are __`inherently unequal`__ . "                                                                                                                                                                                                                                                                                                                           |


### 6. _inherently untrustworthy_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_047.8237_x0758518_18:4-5`**    | Career politicians are __`inherently untrustworthy`__ . "                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_22_015.9487_x0241061_60:3-4`**    | Got an __`inherently untrustworthy`__ character that people blindly trust ?                                                                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_05_077.1229_x1232072_1:1-2`**     | Inherently Untrustworthy                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_23_038.5812_x0607169_16:15-16`**  | The U.S. manufacturers have been trying to portray Italian olive oil as tainted and __`inherently untrustworthy`__ .                                                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_21_022.8227_x0352444_23:8-9`**    | Because mainstream journalism , therefore , was __`inherently untrustworthy`__ , Breitbart was justified in subjecting the world on which he was reporting to his ideological prism ; and if the facts happened to fail to cooperate with a worldview he knew to be correct -- a worldview denied and defamed by the established organs of so-called Big Journalism -- then his guerrilla journalism was justified in reconfiguring those facts to accord with his cause . |
| **`pcc_eng_18_042.6563_x0674065_43:17-18`**  | Any statements he makes on a wing and a prayer for a shorter prison stay is __`inherently untrustworthy`__ .                                                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_05_067.3239_x1073032_061:14-15`** | Public servants cannot be trusted to give of their best ; they are __`inherently untrustworthy`__ .                                                                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_14_059.3953_x0943982_09:21-22`**  | The general consensus from the left is that this view treats women as inherent temptresses , holds men to be __`inherently untrustworthy`__ and excludes women from networking and mentoring opportunities that are so often vital to their advancement .                                                                                                                                                                                                                  |


### 7. _inherently indiscriminate_


|                                             | `token_str`                                                                                                                                                                                                                                                                                                                                   |
|:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_024.9847_x0386814_12:11-12`** | Nuclear weapons are the most inhumane weapons ever conceived , __`inherently indiscriminate`__ in those they kill and maim , and with an impact deadly for decades .                                                                                                                                                                          |
| **`pcc_eng_06_061.9898_x0986975_09:23-24`** | " All the rockets used by Palestinian armed groups are unguided projectiles which cannot be accurately aimed at specific targets and are __`inherently indiscriminate`__ , " the report said , adding that mortars are also imprecise munitions .                                                                                             |
| **`pcc_eng_19_041.7526_x0657785_10:21-22`** | In this respect , it directly condemned the " extrajudicial executions of alleged collaborators " and " the use of __`inherently indiscriminate`__ projectiles towards Israel " that caused " immense distress and disruption " to Israelis ' lives .                                                                                         |
| **`pcc_eng_07_004.5029_x0056559_22:2-3`**   | The __`inherently indiscriminate`__ nature of powerful modern weapons is one of the central features of current U.S. war policy .                                                                                                                                                                                                             |
| **`pcc_eng_26_013.5684_x0202941_5:17-18`**  | Reading this leaves me to question the agency 's ongoing support of trapping , which is __`inherently indiscriminate`__ , inflicts prolonged suffering and results in the non targeted capture of wildlife each year .                                                                                                                        |
| **`pcc_eng_07_074.5298_x1188312_07:17-18`** | These weapons are commonly known as improvised rocket -assisted munitions ( IRAM ) and they are __`inherently indiscriminate`__ .                                                                                                                                                                                                             |
| **`pcc_eng_11_049.0314_x0777074_07:12-13`** | As for Palestinian armed groups , the panel cited the " __`inherently indiscriminate`__ nature " of rockets and mortars fired at Israeli civilians , condemned the killing of people suspected of being collaborators , and said the Palestinian authorities had " consistently failed " to bring violators of international law to justice . |
| **`pcc_eng_01_043.5287_x0687175_03:22-23`** | ... Lebanon is engaged in a deadly war against Palestinian al Qaeda - affiliates , and has resorted to massive and __`inherently indiscriminate`__ shelling of Palestinian camp hideouts in Beirut - - in a manner far more savage than the CNN - BBC monitored Israeli responses .                                                           |


### 8. _inherently interdisciplinary_


|                                             | `token_str`                                                                                                                                                                                                  |
|:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_023.4589_x0363199_3:6-7`**    | The management of innovation is __`inherently interdisciplinary`__ and multifunctional and Tidd , Bessant & Pavitt provide an integrative approach to the subject .                                          |
| **`pcc_eng_08_030.1131_x0471421_2:16-17`**  | The fully open access Journal of Cybersecurity publishes accessible articles describing original research in the __`inherently interdisciplinary`__ world of computer , systems , and information security . |
| **`pcc_eng_10_097.5626_x1561145_18:4-5`**   | The journal is __`inherently interdisciplinary`__ and publishes papers from a range of academic disciplines within the humanities , social sciences and natural sciences .                                   |
| **`pcc_eng_17_027.0423_x0421439_68:16-17`** | Thayer School is uniquely positioned to be a leader in this area because of its __`inherently interdisciplinary`__ structure .                                                                               |
| **`pcc_eng_26_036.8317_x0579210_26:3-4`**   | Filmmaking is __`inherently interdisciplinary`__ , Oliva says .                                                                                                                                              |
| **`pcc_eng_19_008.6509_x0123830_39:6-7`**   | " The polar sciences are __`inherently interdisciplinary`__ , " Virginia said , " and it 's making each science better by collaborating .                                                                    |
| **`pcc_eng_10_016.4890_x0250172_079:3-4`**  | It is __`inherently interdisciplinary`__ , requiring knowledge of the physical sciences and mathematics , although specialities may be oriented toward a group of organisms or a level of organization .     |
| **`pcc_eng_val_2.08583_x30163_13:1-2`**     | Inherently interdisciplinary , visual stylometry uses computational and statistical methods to calculate and compare these underlying image features in ways humans never could before .                     |


### 9. _inherently sinful_


|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                             |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_046.5083_x0735314_15:8-9`**       | We often think of anger as being __`inherently sinful`__ .                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_10_071.9511_x1146996_08:19-20`**     | That debate revolves around the question : " Is a homosexual orientation or attraction to the same sex __`inherently sinful`__ or is that orientation / attraction okay if that person does n't act on it and avoids all same- sex sexual activity ? "                                                                                                  |
| **`pcc_eng_19_096.2872_x1540509_24:10-11`**     | Only from our Bible onward , were women considered __`inherently sinful`__ and destined for eternal punishment .                                                                                                                                                                                                                                        |
| **`pcc_eng_21_089.8849_x1436625_029:7-8`**      | Menstruation showed that the body is __`inherently sinful`__ , women even more so .                                                                                                                                                                                                                                                                     |
| **`pcc_eng_29_011.6221_x0171758_083:11-12`**    | Whereas medieval writers would have acknowledged that men , as __`inherently sinful`__ , constantly thwart the most noble intentions and , as imperfectable , must fail to achieve their own ambitions in this life , modern confidence that rulers can do what they want and must be judged accordingly makes Stephen look inadequate for his office . |
| **`pcc_eng_01_019.7065_x0302450_4:16-17`**      | With such a weak doctrine , some of them may have regarded sexual relationships as __`inherently sinful`__ because they take place through the body ( 7:1 - 5 ) .                                                                                                                                                                                       |
| **`pcc_eng_28_073.6885_x1175706_077:37-42-43`** | The Constitution begins " We the people ... " reflecting liberal belief that human beings can come together to form a government for themselves without reference to God , a positive view of human capability , not that " man is __`inherently sinful`__ . "                                                                                          |
| **`pcc_eng_08_061.5979_x0981545_62:33-34`**     | The idea that women are too emotional to be judges , must be secluded or that women are inferior to men stems from " dirty " menstruation and women being seen as __`inherently sinful`__ .                                                                                                                                                             |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/`...
* Renaming existing version of `inherently_wrong_80ex~80.csv`
* Renaming existing version of `inherently_evil_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_governmental_80ex~60.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_wrong_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_evil_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_coercive_80ex~18.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_unequal_80ex~71.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_untrustworthy_80ex~13.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_indiscriminate_80ex~13.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_interdisciplinary_80ex~20.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/inherently/inherently_sinful_80ex~31.csv`

## *terribly*


|                                      |   `f` |   `dP1` |   `LRC` |   `P1` |      `G2` | `l1`     | `l2`         |   `f1` |    `f2` |        `N` |   `exp_f` |   `unexp_f` |   `unexp_r` |   `odds_r_disc` |   `t` |   `MI` |   `dP2` |   `P2` |   `deltaP_max` |   `deltaP_mean` | `dataset`   |
|:-------------------------------------|------:|--------:|--------:|-------:|----------:|:---------|:-------------|-------:|--------:|-----------:|----------:|------------:|------------:|----------------:|------:|-------:|--------:|-------:|---------------:|----------------:|:------------|
| **[_direct_] terribly~awry**         |   180 |    0.26 |    8.02 |   0.26 |  1,770.97 | terribly | awry         | 58,964 |     692 | 72,839,571 |      0.56 |      179.44 |        1.00 |            2.64 | 13.37 |   2.51 |    0.00 |   0.00 |           0.26 |            0.13 | direct      |
| **[_mirror_] terribly~amiss**        |    53 |    0.09 |    3.99 |   0.09 |    275.77 | terribly | amiss        |  4,610 |     578 |  1,701,929 |      1.57 |       51.43 |        0.97 |            1.58 |  7.07 |   1.53 |    0.01 |   0.01 |           0.09 |            0.05 | mirror      |
| **[_mirror_] terribly~wrong**        | 1,726 |    0.08 |    4.86 |   0.08 |  9,304.94 | terribly | wrong        |  4,610 |  20,880 |  1,701,929 |     56.56 |    1,669.44 |        0.97 |            1.72 | 40.18 |   1.48 |    0.36 |   0.37 |           0.36 |            0.22 | mirror      |
| **[_direct_] terribly~amiss**        |    64 |    0.07 |    5.37 |   0.07 |    451.25 | terribly | amiss        | 58,964 |     898 | 72,839,571 |      0.73 |       63.27 |        0.99 |            1.98 |  7.91 |   1.94 |    0.00 |   0.00 |           0.07 |            0.04 | direct      |
| **[_direct_] terribly~wrong**        | 6,349 |    0.04 |    5.67 |   0.04 | 38,814.14 | terribly | wrong        | 58,964 | 149,064 | 72,839,571 |    120.67 |    6,228.33 |        0.98 |            1.79 | 78.17 |   1.72 |    0.11 |   0.11 |           0.11 |            0.07 | direct      |
| **[_direct_] terribly~misguided**    |   101 |    0.02 |    4.09 |   0.03 |    501.57 | terribly | misguided    | 58,964 |   4,008 | 72,839,571 |      3.24 |       97.76 |        0.97 |            1.51 |  9.73 |   1.49 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_mirror_] terribly~surprising**   |    67 |    0.02 |    2.20 |   0.03 |    181.27 | terribly | surprising   |  4,610 |   2,662 |  1,701,929 |      7.21 |       59.79 |        0.89 |            0.99 |  7.30 |   0.97 |    0.01 |   0.01 |           0.02 |            0.02 | mirror      |
| **[_direct_] terribly~inefficient**  |   198 |    0.02 |    4.05 |   0.02 |    900.41 | terribly | inefficient  | 58,964 |   9,744 | 72,839,571 |      7.89 |      190.11 |        0.96 |            1.41 | 13.51 |   1.40 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |
| **[_direct_] terribly~sorry**        | 1,262 |    0.02 |    4.43 |   0.02 |  5,741.83 | terribly | sorry        | 58,964 |  62,573 | 72,839,571 |     50.65 |    1,211.35 |        0.96 |            1.41 | 34.10 |   1.40 |    0.02 |   0.02 |           0.02 |            0.02 | direct      |
| **[_direct_] terribly~inconvenient** |   129 |    0.02 |    3.59 |   0.02 |    535.38 | terribly | inconvenient | 58,964 |   7,795 | 72,839,571 |      6.31 |      122.69 |        0.95 |            1.32 | 10.80 |   1.31 |    0.00 |   0.00 |           0.02 |            0.01 | direct      |


### 1. _terribly awry_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                               |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20080810_0971_2:25-26`**          | then he recalls seeing his photo on national TV and grasping the reality that their Hollywood-style plan to rob a Nevada casino had gone __`terribly awry`__ .                                                                                                                                                                                                                            |
| **`pcc_eng_23_015.7613_x0237884_111:15-16`** | The problem is that they are misguided int heir efforts , which is go __`terribly awry`__ .                                                                                                                                                                                                                                                                                               |
| **`nyt_eng_20060905_0020_2:39-40`**          | but if Eli Manning of the Giants and Peyton Manning of the Colts are on the field at the same time at Giants Stadium , except for pregame warm-ups or a postgame hug , something will have gone __`terribly awry`__ .                                                                                                                                                                     |
| **`pcc_eng_04_070.2969_x1119272_06:09-10`**  | Of course , there are days that go __`terribly awry`__ : I start a simple task and end with 20 open tabs + a pounding headache ; I say yes to another glass of wine and learn for the millionth time that an extra hour of sleep would have probably been more beneficial ; I fall into a rabbit hole of social feeds and emerge hours later frustrated with my lack of self-regulation . |
| **`pcc_eng_26_009.1984_x0132410_04:35-36`**  | The opening scene , set in the early nineties , gives us the back-story : Matthew Scudder ( Liam Neeson ) is an alcoholic NYC cop who drunkenly stumbles into a shootout that goes __`terribly awry`__ .                                                                                                                                                                                  |
| **`nyt_eng_20000728_0352_15:4-5`**           | unless things go __`terribly awry`__ , the Bush and Gore operations will make Nixon '72 look like parvenus when it comes to convention orchestration .                                                                                                                                                                                                                                    |
| **`pcc_eng_22_100.8986_x1614355_064:4-5`**   | ( That goes __`terribly awry`__ . )                                                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_10_092.5089_x1479429_20:6-7`**    | One , there 's something __`terribly awry`__ between the public message and the actual reality , and two , coordination among Congress , Do D and VA does matter .                                                                                                                                                                                                                        |


### 2. _terribly amiss_


|                                             | `token_str`                                                                                                                                                                                                               |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_027.0264_x0420608_16:10-11`** | As a general rule , unless there is something __`terribly amiss`__ with a candidate , I generally support the right of a President - even one with whom I disagree - to choose whomever he wants for the Court .          |
| **`pcc_eng_24_066.1939_x1054666_11:3-4`**   | Something is __`terribly amiss`__ with our system of scientific communication when so many anti-science events can occur almost simultaneously .                                                                          |
| **`pcc_eng_01_026.5450_x0413153_24:8-9`**   | That was when I realized something was __`terribly amiss`__ .                                                                                                                                                             |
| **`pcc_eng_25_063.7653_x1016753_03:17-18`** | As the professional basketball and hockey seasons advance deep into the playoffs , there 's something __`terribly amiss`__ :                                                                                              |
| **`pcc_eng_25_014.7843_x0222899_11:19-20`** | " It was made blatantly obvious to the millions of people watching the post parade that something was __`terribly amiss`__ ( with Life At Ten ) , " De Bartolo 's letter said .                                           |
| **`pcc_eng_10_085.8180_x1370782_38:6-7`**   | Clearly , there is something __`terribly amiss`__ in the present " development " paradigm that the people of one of the poorest and most backward states of the country are saying no to this form of industrialisation . |
| **`pcc_eng_02_065.9740_x1050915_21:13-14`** | Starting way back in 2002 , the PETA people knew something was __`terribly amiss`__ in the Golden State .                                                                                                                 |
| **`pcc_eng_27_001.0101_x0000157_10:4-5`**   | " Something is __`terribly amiss`__ in our traffic safety culture when , in the safest year since 1949 , on average there is still one needless death every 16 minutes in motor vehicle crashes . "                       |


### 3. _terribly wrong_


|                                              | `token_str`                                                                                                                                                                                                                                                                             |
|:---------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_036.7771_x0578970_122:10-11`** | In death , Mr Morrison symbolised everything that was __`terribly wrong`__ with the health system in the late 1990s .                                                                                                                                                                   |
| **`pcc_eng_05_096.6850_x1548088_4:09-10`**   | Have you ever had a date night go __`terribly wrong`__ ?                                                                                                                                                                                                                                |
| **`pcc_eng_20_010.2754_x0149437_02:44-45`**  | Mark Wahlberg and Dwayne Johnson star in the film based on a true story and the two lead actors play a pair of Florida bodybuilders who get caught up in an extortion ring and a kidnapping scheme involving a wealthy businessman that goes __`terribly wrong`__ .                     |
| **`pcc_eng_19_016.3923_x0248306_08:7-8`**    | It was obvious there was something __`terribly wrong`__ with his body .                                                                                                                                                                                                                 |
| **`pcc_eng_16_065.4061_x1042455_012:20-21`** | ... And by the way , if you are a practicing Pagan or Wiccan , and I got something __`terribly wrong`__ , or you want to share another version or another vision of something I wrote -- PLEASE let me know which it is , and give me the info in a comment on the related blog entry ! |
| **`pcc_eng_03_027.4101_x0427656_0763:3-4`**  | Something was __`terribly wrong`__ .                                                                                                                                                                                                                                                    |
| **`pcc_eng_11_052.7812_x0837708_276:8-9`**   | Things would have to go terribly , __`terribly wrong`__ before I 'd resort to personal anecdote . "                                                                                                                                                                                     |
| **`nyt_eng_19980914_0325_54:09-10`**         | but within minutes it became clear something was __`terribly wrong`__ .                                                                                                                                                                                                                 |


### 4. _terribly misguided_


|                                              | `token_str`                                                                                                                                                                                                                                  |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_080.7835_x1289479_10:14-15`**  | We do have the brains to build guided missiles , But we are terribly misguided                                                                                                                                                               |
| **`pcc_eng_07_059.7943_x0950366_07:8-9`**    | That initial response is understandable , but __`terribly misguided`__ .                                                                                                                                                                     |
| **`pcc_eng_00_067.4039_x1073331_13:16-17`**  | And that the folks over at Stop Letting Brown People Do Services for Americans are __`terribly misguided`__ .                                                                                                                                |
| **`pcc_eng_07_019.5911_x0300679_09:27-28`**  | I disagree with almost every position that tea partiers advocate and would be horrified if anyone saw me with a flag and associated me with their __`terribly misguided`__ , outrageously hypocritical , sometimes racist political agenda . |
| **`pcc_eng_02_037.1177_x0584490_025:2-3`**   | Even __`terribly misguided`__ Bank Swallows do n't nest in man-made structures , so this seemed unusual on two levels .                                                                                                                      |
| **`pcc_eng_26_009.6211_x0139293_199:16-17`** | Some Southern " Conservatives " ( be they Republican or otherwise ) rejected integration for __`terribly misguided`__ fears about what would happen to their " civilization . "                                                              |
| **`pcc_eng_09_106.5253_x1707663_100:6-7`**   | This looks more like a __`terribly misguided`__ attempt to silence a critic with a little intimidation .                                                                                                                                     |
| **`pcc_eng_25_010.1586_x0148297_1:18-19`**   | Penelope Braxton Surname / Boys names on girls - I feel like people who do this are __`terribly misguided`__ .                                                                                                                               |


### 5. _terribly surprising_


|                                                 | `token_str`                                                                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_039.3118_x0618969_04:3-4-5`**     | That 's not __`terribly surprising`__ when you consider all of the power Amazon has crammed inside this thing .                                                                                                                                          |
| **`pcc_eng_00_062.0183_x0986441_01:3-4-5`**     | It was not __`terribly surprising`__ that Romney would , on the eve of the election , toss aside the antiabortion positions he cultivated during the Republican primaries ; lately , he has reversed himself more often than a parking - lot attendant . |
| **`nyt_eng_20000628_0352_26:3-4-5`**            | that 's not __`terribly surprising`__ .                                                                                                                                                                                                                  |
| **`nyt_eng_19981015_0074_8:12-13`**             | the success of the book , her first , was `` __`terribly surprising`__ _ I had no expectations . ''                                                                                                                                                      |
| **`pcc_eng_04_042.0070_x0662731_07:1-2-3`**     | Nothing __`terribly surprising`__ in the Starbuck plot , some nice tear-jerky bits with Apollo , and oh my the situation on the Cylon side just got real , real interesting .                                                                            |
| **`pcc_eng_13_087.8953_x1404395_071:10-11-12`** | In a move that counts as disappointing , if not __`terribly surprising`__ , Pittsburgh Steelers reserve offensive tackle Ryan Harris has announced his retirement .                                                                                      |
| **`pcc_eng_03_036.3703_x0572888_020:13-14-15`** | Overall , A Sky Painted Gold is a fairly traditional story , nothing __`terribly surprising`__ is happening here , but it 's got a modern air about it .                                                                                                 |
| **`pcc_eng_07_023.4162_x0362485_18:3-4-5`**     | Which is n't __`terribly surprising`__ :                                                                                                                                                                                                                 |


### 6. _terribly inefficient_


|                                             | `token_str`                                                                                                                                                                                                                                 |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_035.4152_x0556557_09:5-6`**   | Air cooled engine , __`terribly inefficient`__ .                                                                                                                                                                                            |
| **`pcc_eng_08_054.4689_x0865908_04:15-16`** | Simply packing enough food to last for the entirety of the trip would be __`terribly inefficient`__ and would leave space travelers in a tight spot if their return is delayed and they somehow run out of things to eat .                  |
| **`pcc_eng_28_055.6557_x0884485_71:14-15`** | You gotta have something to do with all that computing power besides write __`terribly inefficient`__ code .                                                                                                                                |
| **`apw_eng_19980331_0031_5:26-27`**         | China spends nearly half its annual revenues on salaries for more than 30 million officials `` whose work is often redundant , bureaucratic , and __`terribly inefficient`__ , '' Xinhua said .                                             |
| **`pcc_eng_29_100.8780_x1613861_07:10-11`** | It would take forever to heat and would be __`terribly inefficient`__ on a stove top .                                                                                                                                                      |
| **`pcc_eng_02_046.2746_x0732418_08:21-22`** | While discussing economies of scale , we decided that a communal village ( families in separate houses ) would be __`terribly inefficient`__ .                                                                                              |
| **`pcc_eng_29_021.4067_x0329232_08:25-26`** | When cancerous tumors form , they need a very dense collection of blood vessels supplying them with nutrients , because tumor cells are so __`terribly inefficient`__ at creating energy .                                                  |
| **`pcc_eng_19_041.6957_x0656891_323:5-6`**  | The Utes have been __`terribly inefficient`__ offensively , have struggled shooting the ball ( especially from deep ) and have even struggled on the glass , which is completely unacceptable for one of the tallest teams in the country . |


### 7. _terribly sorry_


|                                              | `token_str`                                                                                                                                                                                                                                                                                                                |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_063.2717_x1007472_08:6-7`**    | Hello everyone , I 'm __`terribly sorry`__ that I have n't sent out an email in quite a while , but I have a good excuse :                                                                                                                                                                                                 |
| **`pcc_eng_23_053.5551_x0849194_468:31-32`** | Dickens pulled out at the last minute and the sponsor who 'd set up all these gigs was left terribly embarrassed and said to the Australians , ' We 're __`terribly sorry`__ that Dickens ca n't come and there 's no other writer of his stature to take his place , so why do n't we send you a cricket team instead ? ' |
| **`pcc_eng_28_035.3647_x0555706_026:3-4`**   | I am __`terribly sorry`__ for being mean .                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_09_086.7214_x1386915_4:24-25`**   | If you have received your order and we have inadvertently sent you the incorrect format or the wrong item altogether - we 're __`terribly sorry`__ !                                                                                                                                                                       |
| **`pcc_eng_17_044.5195_x0702897_24:16-17`**  | The owner of the pet store was quite upset and said , " I 'm __`terribly sorry`__ to hear that ! "                                                                                                                                                                                                                         |
| **`pcc_eng_13_016.5170_x0250576_098:4-5`**   | I am so __`terribly sorry`__ for your loss .                                                                                                                                                                                                                                                                               |
| **`pcc_eng_17_008.0128_x0113422_167:10-11`** | She recited this phrase again : " I 'm __`terribly sorry`__ to interrupt , but I was wondering if I could ask you something . "                                                                                                                                                                                            |
| **`pcc_eng_28_049.6150_x0786648_13:8-9`**    | Hulu and Pandora are saying they are __`terribly sorry`__ but you are not in the USA and so they are just not feeling good about streaming content to you , for some reason or another .                                                                                                                                   |


### 8. _terribly inconvenient_


|                                               | `token_str`                                                                                                                                                            |
|:----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_078.6311_x1255762_21:4-5`**     | It will be __`terribly inconvenient`__ is the vehicle leaves you or runs over your foot !                                                                              |
| **`pcc_eng_03_048.4337_x0768368_46:20-21`**   | And that is very well how we might have gone on living happily ever after , except for one __`terribly inconvenient`__ interference .                                  |
| **`pcc_eng_val_3.10516_x51518_04:6-7`**       | This all strikes me as __`terribly inconvenient`__ , not to say tedious .                                                                                              |
| **`pcc_eng_25_011.1002_x0163449_13:14-15`**   | As far as politicians and the press are concerned , it would be __`terribly inconvenient`__ in a politically correct world to identify radical Islam with real Islam . |
| **`pcc_eng_21_052.7357_x0836356_0830:13-14`** | You would have to move about quickly , and guns would be __`terribly inconvenient`__ , if you had to push your way through a hedge or a close thicket .                |
| **`apw_eng_19991014_0142_17:11-12`**          | `` It 's a difficult thing and it 's a __`terribly inconvenient`__ thing , '' Robinson said .                                                                          |
| **`pcc_eng_01_064.0994_x1020577_124:3-4`**    | " How __`terribly inconvenient`__ , " Lady Li said innocently .                                                                                                        |
| **`pcc_eng_17_050.8240_x0804915_08:4-5`**     | That would be __`terribly inconvenient`__ , as my January bill was very high indeed .                                                                                  |


Saving Samples in `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/`...
* Renaming existing version of `terribly_wrong_80ex~80.csv`
* Renaming existing version of `terribly_surprising_80ex~80.csv`
* Renaming existing version of `terribly_sorry_80ex~80.csv`

Samples saved as...
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_awry_80ex~35.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_amiss_80ex~9.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_wrong_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_misguided_80ex~19.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_surprising_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_inefficient_80ex~33.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_sorry_80ex~80.csv`
+ `/share/compling/projects/sanpi/results/top_AM/ALL/any_bigram_examples/terribly/terribly_inconvenient_80ex~25.csv`

