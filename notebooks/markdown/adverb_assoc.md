# Identifying Adverbs with Strongest Negative Environment Associations


```python
from pathlib import Path

import pandas as pd

from source.utils import PKL_SUFF
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.general import print_iter, snake_to_camel, timestamp_today

SET_FLOOR = 2000
MIR_FLOOR = 200
K = 5
```

    /home/arh234/anaconda3/envs/dev-sanpi/lib/python3.10/site-packages/scipy/__init__.py:146: UserWarning: A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy (detected version 1.24.3
      warnings.warn(f"A NumPy version >={np_minversion} and <{np_maxversion}"


Set columns and diplay settings


```python
FOCUS = ['f',
         'am_p1_given2', 'conservative_log_ratio',
         'am_log_likelihood',
        #  'mutual_information', 'am_odds_ratio_disc', 't_score',
         'N', 'f1', 'f2', 'E11', 'unexpected_f', 
         'l1', 'l2']
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 90)
pd.set_option("display.precision", 2)
pd.set_option("styler.format.precision", 2)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.2f}'.format)
# pd.set_option("styler.render.repr", "html")
```


```python
def force_ints(_df):
    count_cols = _df.filter(regex=r'total|^[fN]').columns
    _df[count_cols] = _df[count_cols].astype('int')
    # _df[count_cols] = _df[:, count_cols].astype('int64')
    # print(_df.dtypes.to_frame('dtypes'))
    return _df
```


```python
def nb_show_table(df, n_dec: int = 2,
                  adjust_columns: bool = True,
                   outpath:Path=None, 
                   return_df:bool=False) -> None: 
    _df = df.copy()
    if adjust_columns: 
        _df = adjust_assoc_columns(_df)
    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index ]
    table = _df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    if outpath:
        outpath.write_text(table)

    print(f'\n{table}\n')
    return (_df if return_df else None)
```

## Set paths and load adverb association tables


```python
def update_index(df, pat_name:str = None):
    neg_env_name = df.filter(like='NEG', axis=0).l1[0]
    # > will be either `NEGATED` or `NEGMIR`
    #   both are shortened to just `NEG` for the keys in their separate dataframes
    # > replace to avoid ambiguity in `key` values when combined
    #! some filtering relies on 'NEG', so have to keep that prefix
    index_update = pat_name or ('NEGmir' if neg_env_name.endswith('MIR') else 'NEGany')
    df.index = df.index.str.replace('NEG', index_update)
    return df
```


```python
POLAR_DIR = AM_DF_DIR.joinpath('polar')

polar_adv_dirs = []
# results/assoc_df/polar/RBdirect/adv/extra/polarized-adv_35f-7c_min5000x_extra.pkl.gz
adv_am_paths = {
    p.name: tuple(
        p.joinpath('adv/extra').glob(
            f'*35f-7c_min{SET_FLOOR if p.name == "RBdirect" else MIR_FLOOR}x*{PKL_SUFF}')
    )[0]
    for p in POLAR_DIR.iterdir()}

setdiff_adv = update_index(pd.read_pickle(adv_am_paths['RBdirect']))
mirror_adv = update_index(pd.read_pickle(adv_am_paths['NEGmirror']))
nb_show_table(setdiff_adv.sample(K//2).sort_values('conservative_log_ratio', ascending=False)[FOCUS])
```

    
    |                          |    `f` |   `dP1` |   `LRC` |      `G2` |        `N` |       `f1` |    `f2` |   `exp_f` |   `unexp_f` | `l1`       | `l2`          |
    |:-------------------------|-------:|--------:|--------:|----------:|-----------:|-----------:|--------:|----------:|------------:|:-----------|:--------------|
    | **COM~reasonably**       | 63,753 |    0.02 |    1.16 |  1,226.62 | 86,330,752 | 83,102,035 |  64,688 | 62,268.71 |    1,484.29 | COMPLEMENT | reasonably    |
    | **NEGany~significantly** |  3,013 |   -0.02 |   -0.67 | -1,120.96 | 86,330,752 |  3,226,213 | 139,099 |  5,198.18 |   -2,185.18 | NEGATED    | significantly |
    



```python
nb_show_table(mirror_adv.sample(K//2).sort_values('conservative_log_ratio', ascending=False)[FOCUS])
```

    
    |                      |   `f` |   `dP1` |   `LRC` |   `G2` |       `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`   | `l2`       |
    |:---------------------|------:|--------:|--------:|-------:|----------:|----------:|-------:|----------:|------------:|:-------|:-----------|
    | **POS~absolutely**   | 5,834 |    0.06 |    0.52 | 202.52 | 2,032,082 | 1,738,105 |  6,384 |  5,460.44 |      373.56 | POSMIR | absolutely |
    | **NEGmir~seriously** |   435 |   -0.05 |   -0.28 | -88.22 | 2,032,082 |   293,963 |  4,453 |    644.18 |     -209.18 | NEGMIR | seriously  |
    


## Calculate "Most Negative" Adverbs for each Polarity Approximation


```python
def get_top_vals(df: pd.DataFrame,
                 index_like: str = 'NEG',
                 metric_filter: str | list = ['am_p1_given2', 'conservative_log_ratio'],
                 k: int = 10,
                 val_col: str = None,
                 ignore_neg_adv: bool = True):
    env_df = df.copy().loc[df.conservative_log_ratio >=
                           1].filter(like=index_like, axis=0)
    if ignore_neg_adv:
        env_df = env_df.loc[~df.l2.isin(
            ("n't", 'not', 'barely', 'never', 'no', 'none')), :]
    if isinstance(metric_filter, str):
        metric_filter = [metric_filter]

    top = pd.concat([env_df.nlargest(k, m) for m in metric_filter]
                    ).drop_duplicates(keep='first')

    if val_col:
        top = top[[val_col] + metric_filter]

    return top.sort_values(metric_filter, ascending=False)


[setdiff_top15, mirror_top15] = [
    get_top_vals(adv_df, k=15)
    for adv_df in (setdiff_adv, mirror_adv)
]
nb_show_table(setdiff_top15.filter(items=FOCUS).reset_index())
```

    
    |        | `key`              |     `f` |   `dP1` |   `LRC` |       `G2` |        `N` |      `f1` |    `f2` |   `exp_f` |   `unexp_f` | `l1`    | `l2`        |
    |:-------|:-------------------|--------:|--------:|--------:|-----------:|-----------:|----------:|--------:|----------:|------------:|:--------|:------------|
    | **0**  | NEGany~necessarily |  42,708 |    0.72 |    6.23 | 219,003.46 | 86,330,752 | 3,226,213 |  56,694 |  2,118.68 |   40,589.32 | NEGATED | necessarily |
    | **1**  | NEGany~exactly     |  43,635 |    0.67 |    5.90 | 214,404.20 | 86,330,752 | 3,226,213 |  61,599 |  2,301.98 |   41,333.02 | NEGATED | exactly     |
    | **2**  | NEGany~that        | 165,411 |    0.63 |    5.62 | 781,016.11 | 86,330,752 | 3,226,213 | 250,392 |  9,357.24 |  156,053.76 | NEGATED | that        |
    | **3**  | NEGany~immediately |  57,319 |    0.52 |    4.96 | 239,462.58 | 86,330,752 | 3,226,213 | 103,177 |  3,855.76 |   53,463.24 | NEGATED | immediately |
    | **4**  | NEGany~yet         |  52,546 |    0.48 |    4.74 | 209,055.78 | 86,330,752 | 3,226,213 | 101,707 |  3,800.83 |   48,745.17 | NEGATED | yet         |
    | **5**  | NEGany~terribly    |  18,054 |    0.22 |    3.09 |  42,704.93 | 86,330,752 | 3,226,213 |  70,174 |  2,622.43 |   15,431.57 | NEGATED | terribly    |
    | **6**  | NEGany~remotely    |   5,679 |    0.22 |    3.03 |  13,354.33 | 86,330,752 | 3,226,213 |  22,194 |    829.40 |    4,849.60 | NEGATED | remotely    |
    | **7**  | NEGany~only        | 114,070 |    0.21 |    3.04 | 261,936.36 | 86,330,752 | 3,226,213 | 464,168 | 17,346.13 |   96,723.87 | NEGATED | only        |
    | **8**  | NEGany~altogether  |   4,575 |    0.18 |    2.75 |   9,468.00 | 86,330,752 | 3,226,213 |  20,636 |    771.17 |    3,803.82 | NEGATED | altogether  |
    | **9**  | NEGany~entirely    |  63,708 |    0.17 |    2.74 | 125,925.14 | 86,330,752 | 3,226,213 | 303,833 | 11,354.35 |   52,353.65 | NEGATED | entirely    |
    | **10** | NEGany~overly      |  24,707 |    0.17 |    2.66 |  46,993.58 | 86,330,752 | 3,226,213 | 122,058 |  4,561.35 |   20,145.65 | NEGATED | overly      |
    | **11** | NEGany~merely      |   5,944 |    0.13 |    2.26 |   9,223.66 | 86,330,752 | 3,226,213 |  35,608 |  1,330.68 |    4,613.32 | NEGATED | merely      |
    | **12** | NEGany~any         |  15,492 |    0.13 |    2.28 |  23,683.00 | 86,330,752 | 3,226,213 |  94,152 |  3,518.50 |   11,973.50 | NEGATED | any         |
    | **13** | NEGany~always      | 104,605 |    0.12 |    2.28 | 157,437.56 | 86,330,752 | 3,226,213 | 651,053 | 24,330.10 |   80,274.90 | NEGATED | always      |
    | **14** | NEGany~directly    |   8,317 |    0.12 |    2.13 |  11,654.57 | 86,330,752 | 3,226,213 |  54,441 |  2,034.48 |    6,282.52 | NEGATED | directly    |
    


15 Most Negatively Associated Adverbs for full dataset (_Absent Negative_ approximation) as ranked by $\Delta P(1|2)$ (`dP1`) and $LRC$

|        | `key`              |     `f` |   `dP1` |   `LRC` |       `G2` |        `N` |      `f1` |    `f2` |   `exp_f` |   `unexp_f` | `l1`    | `l2`        |
|:-------|:-------------------|--------:|--------:|--------:|-----------:|-----------:|----------:|--------:|----------:|------------:|:--------|:------------|
| **0**  | NEGany~necessarily |  42,708 |    0.72 |    6.23 | 219,003.46 | 86,330,752 | 3,226,213 |  56,694 |  2,118.68 |   40,589.32 | NEGATED | necessarily |
| **1**  | NEGany~exactly     |  43,635 |    0.67 |    5.90 | 214,404.20 | 86,330,752 | 3,226,213 |  61,599 |  2,301.98 |   41,333.02 | NEGATED | exactly     |
| **2**  | NEGany~that        | 165,411 |    0.63 |    5.62 | 781,016.11 | 86,330,752 | 3,226,213 | 250,392 |  9,357.24 |  156,053.76 | NEGATED | that        |
| **3**  | NEGany~immediately |  57,319 |    0.52 |    4.96 | 239,462.58 | 86,330,752 | 3,226,213 | 103,177 |  3,855.76 |   53,463.24 | NEGATED | immediately |
| **4**  | NEGany~yet         |  52,546 |    0.48 |    4.74 | 209,055.78 | 86,330,752 | 3,226,213 | 101,707 |  3,800.83 |   48,745.17 | NEGATED | yet         |
| **5**  | NEGany~terribly    |  18,054 |    0.22 |    3.09 |  42,704.93 | 86,330,752 | 3,226,213 |  70,174 |  2,622.43 |   15,431.57 | NEGATED | terribly    |
| **6**  | NEGany~remotely    |   5,679 |    0.22 |    3.03 |  13,354.33 | 86,330,752 | 3,226,213 |  22,194 |    829.40 |    4,849.60 | NEGATED | remotely    |
| **7**  | NEGany~only        | 114,070 |    0.21 |    3.04 | 261,936.36 | 86,330,752 | 3,226,213 | 464,168 | 17,346.13 |   96,723.87 | NEGATED | only        |
| **8**  | NEGany~altogether  |   4,575 |    0.18 |    2.75 |   9,468.00 | 86,330,752 | 3,226,213 |  20,636 |    771.17 |    3,803.82 | NEGATED | altogether  |
| **9**  | NEGany~entirely    |  63,708 |    0.17 |    2.74 | 125,925.14 | 86,330,752 | 3,226,213 | 303,833 | 11,354.35 |   52,353.65 | NEGATED | entirely    |
| **10** | NEGany~overly      |  24,707 |    0.17 |    2.66 |  46,993.58 | 86,330,752 | 3,226,213 | 122,058 |  4,561.35 |   20,145.65 | NEGATED | overly      |
| **11** | NEGany~merely      |   5,944 |    0.13 |    2.26 |   9,223.66 | 86,330,752 | 3,226,213 |  35,608 |  1,330.68 |    4,613.32 | NEGATED | merely      |
| **12** | NEGany~any         |  15,492 |    0.13 |    2.28 |  23,683.00 | 86,330,752 | 3,226,213 |  94,152 |  3,518.50 |   11,973.50 | NEGATED | any         |
| **13** | NEGany~always      | 104,605 |    0.12 |    2.28 | 157,437.56 | 86,330,752 | 3,226,213 | 651,053 | 24,330.10 |   80,274.90 | NEGATED | always      |
| **14** | NEGany~directly    |   8,317 |    0.12 |    2.13 |  11,654.57 | 86,330,752 | 3,226,213 |  54,441 |  2,034.48 |    6,282.52 | NEGATED | directly    |


```python
nb_show_table(mirror_top15.filter(items=FOCUS).reset_index())
```

    
    |        | `key`                |   `f` |   `dP1` |   `LRC` |      `G2` |       `N` |    `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`   | `l2`          |
    |:-------|:---------------------|------:|--------:|--------:|----------:|----------:|--------:|-------:|----------:|------------:|:-------|:--------------|
    | **0**  | NEGmir~before        |   290 |    0.84 |    5.11 |  1,080.52 | 2,032,082 | 293,963 |    294 |     42.53 |      247.47 | NEGMIR | before        |
    | **1**  | NEGmir~ever          | 4,718 |    0.77 |    5.57 | 15,340.34 | 2,032,082 | 293,963 |  5,179 |    749.20 |    3,968.80 | NEGMIR | ever          |
    | **2**  | NEGmir~exactly       |   813 |    0.59 |    3.51 |  1,939.47 | 2,032,082 | 293,963 |  1,114 |    161.15 |      651.85 | NEGMIR | exactly       |
    | **3**  | NEGmir~any           | 1,082 |    0.57 |    3.48 |  2,511.26 | 2,032,082 | 293,963 |  1,514 |    219.02 |      862.98 | NEGMIR | any           |
    | **4**  | NEGmir~remotely      | 1,846 |    0.54 |    3.35 |  4,009.84 | 2,032,082 | 293,963 |  2,717 |    393.04 |    1,452.96 | NEGMIR | remotely      |
    | **5**  | NEGmir~particularly  | 9,278 |    0.48 |    3.15 | 17,999.07 | 2,032,082 | 293,963 | 14,954 |  2,163.26 |    7,114.74 | NEGMIR | particularly  |
    | **6**  | NEGmir~that          | 4,338 |    0.44 |    2.86 |  7,632.21 | 2,032,082 | 293,963 |  7,472 |  1,080.91 |    3,257.09 | NEGMIR | that          |
    | **7**  | NEGmir~necessarily   |   971 |    0.43 |    2.66 |  1,688.91 | 2,032,082 | 293,963 |  1,681 |    243.18 |      727.82 | NEGMIR | necessarily   |
    | **8**  | NEGmir~inherently    | 2,872 |    0.36 |    2.42 |  4,160.38 | 2,032,082 | 293,963 |  5,649 |    817.19 |    2,054.81 | NEGMIR | inherently    |
    | **9**  | NEGmir~overtly       |   392 |    0.29 |    1.71 |    443.78 | 2,032,082 | 293,963 |    898 |    129.91 |      262.09 | NEGMIR | overtly       |
    | **10** | NEGmir~intrinsically |   432 |    0.29 |    1.73 |    487.95 | 2,032,082 | 293,963 |    991 |    143.36 |      288.64 | NEGMIR | intrinsically |
    | **11** | NEGmir~especially    | 1,573 |    0.21 |    1.49 |  1,232.03 | 2,032,082 | 293,963 |  4,400 |    636.51 |      936.49 | NEGMIR | especially    |
    | **12** | NEGmir~yet           |   320 |    0.21 |    1.18 |    242.23 | 2,032,082 | 293,963 |    909 |    131.50 |      188.50 | NEGMIR | yet           |
    | **13** | NEGmir~fully         | 1,668 |    0.18 |    1.31 |  1,086.24 | 2,032,082 | 293,963 |  5,084 |    735.46 |      932.54 | NEGMIR | fully         |
    | **14** | NEGmir~terribly      | 1,579 |    0.16 |    1.14 |    847.65 | 2,032,082 | 293,963 |  5,218 |    754.84 |      824.16 | NEGMIR | terribly      |
    


15 Most Negatively Associated Adverbs for `mirror` subset (_Present Positive_ approximation) as ranked by $\Delta P(1|2)$ (`dP1`) and $LRC$

|        | `key`                |   `f` |   `dP1` |   `LRC` |      `G2` |       `N` |    `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`   | `l2`          |
|:-------|:---------------------|------:|--------:|--------:|----------:|----------:|--------:|-------:|----------:|------------:|:-------|:--------------|
| **0**  | NEGmir~before        |   290 |    0.84 |    5.11 |  1,080.52 | 2,032,082 | 293,963 |    294 |     42.53 |      247.47 | NEGMIR | before        |
| **1**  | NEGmir~ever          | 4,718 |    0.77 |    5.57 | 15,340.34 | 2,032,082 | 293,963 |  5,179 |    749.20 |    3,968.80 | NEGMIR | ever          |
| **2**  | NEGmir~exactly       |   813 |    0.59 |    3.51 |  1,939.47 | 2,032,082 | 293,963 |  1,114 |    161.15 |      651.85 | NEGMIR | exactly       |
| **3**  | NEGmir~any           | 1,082 |    0.57 |    3.48 |  2,511.26 | 2,032,082 | 293,963 |  1,514 |    219.02 |      862.98 | NEGMIR | any           |
| **4**  | NEGmir~remotely      | 1,846 |    0.54 |    3.35 |  4,009.84 | 2,032,082 | 293,963 |  2,717 |    393.04 |    1,452.96 | NEGMIR | remotely      |
| **5**  | NEGmir~particularly  | 9,278 |    0.48 |    3.15 | 17,999.07 | 2,032,082 | 293,963 | 14,954 |  2,163.26 |    7,114.74 | NEGMIR | particularly  |
| **6**  | NEGmir~that          | 4,338 |    0.44 |    2.86 |  7,632.21 | 2,032,082 | 293,963 |  7,472 |  1,080.91 |    3,257.09 | NEGMIR | that          |
| **7**  | NEGmir~necessarily   |   971 |    0.43 |    2.66 |  1,688.91 | 2,032,082 | 293,963 |  1,681 |    243.18 |      727.82 | NEGMIR | necessarily   |
| **8**  | NEGmir~inherently    | 2,872 |    0.36 |    2.42 |  4,160.38 | 2,032,082 | 293,963 |  5,649 |    817.19 |    2,054.81 | NEGMIR | inherently    |
| **9**  | NEGmir~overtly       |   392 |    0.29 |    1.71 |    443.78 | 2,032,082 | 293,963 |    898 |    129.91 |      262.09 | NEGMIR | overtly       |
| **10** | NEGmir~intrinsically |   432 |    0.29 |    1.73 |    487.95 | 2,032,082 | 293,963 |    991 |    143.36 |      288.64 | NEGMIR | intrinsically |
| **11** | NEGmir~especially    | 1,573 |    0.21 |    1.49 |  1,232.03 | 2,032,082 | 293,963 |  4,400 |    636.51 |      936.49 | NEGMIR | especially    |
| **12** | NEGmir~yet           |   320 |    0.21 |    1.18 |    242.23 | 2,032,082 | 293,963 |    909 |    131.50 |      188.50 | NEGMIR | yet           |
| **13** | NEGmir~fully         | 1,668 |    0.18 |    1.31 |  1,086.24 | 2,032,082 | 293,963 |  5,084 |    735.46 |      932.54 | NEGMIR | fully         |
| **14** | NEGmir~terribly      | 1,579 |    0.16 |    1.14 |    847.65 | 2,032,082 | 293,963 |  5,218 |    754.84 |      824.16 | NEGMIR | terribly      |

### Or here, the least "negative"/most "non-negative"


```python
for adv_df in (setdiff_adv, mirror_adv):
    nb_show_table(
        get_top_vals(
            adv_df.filter(items=FOCUS), 
            k=10,
            index_like='O',  # should match "POS" & "COM", but neither "NEG*"
            ).sort_values('conservative_log_ratio', ascending=False)
    )
```

    
    |                      |       `f` |   `dP1` |   `LRC` |       `G2` |        `N` |       `f1` |      `f2` |      `exp_f` |   `unexp_f` | `l1`       | `l2`         |
    |:---------------------|----------:|--------:|--------:|-----------:|-----------:|-----------:|----------:|-------------:|------------:|:-----------|:-------------|
    | **COM~increasingly** |   404,356 |    0.04 |    6.00 |  29,076.69 | 86,330,752 | 83,102,035 |   404,521 |   389,392.16 |   14,963.84 | COMPLEMENT | increasingly |
    | **COM~relatively**   |   626,369 |    0.04 |    5.24 |  42,957.87 | 86,330,752 | 83,102,035 |   626,884 |   603,438.92 |   22,930.08 | COMPLEMENT | relatively   |
    | **COM~almost**       |   466,468 |    0.04 |    4.85 |  31,107.72 | 86,330,752 | 83,102,035 |   466,967 |   449,502.72 |   16,965.28 | COMPLEMENT | almost       |
    | **COM~seemingly**    |   176,135 |    0.04 |    4.77 |  11,864.41 | 86,330,752 | 83,102,035 |   176,304 |   169,710.34 |    6,424.66 | COMPLEMENT | seemingly    |
    | **COM~mostly**       |   212,255 |    0.04 |    4.71 |  14,160.67 | 86,330,752 | 83,102,035 |   212,478 |   204,531.45 |    7,723.55 | COMPLEMENT | mostly       |
    | **COM~pretty**       | 1,650,041 |    0.04 |    4.64 | 107,081.72 | 86,330,752 | 83,102,035 | 1,652,360 | 1,590,562.75 |   59,478.25 | COMPLEMENT | pretty       |
    | **COM~fairly**       |   401,326 |    0.04 |    4.50 |  25,904.34 | 86,330,752 | 83,102,035 |   401,879 |   386,848.97 |   14,477.03 | COMPLEMENT | fairly       |
    | **COM~partly**       |    80,461 |    0.04 |    4.50 |   5,418.01 | 86,330,752 | 83,102,035 |    80,538 |    77,525.93 |    2,935.07 | COMPLEMENT | partly       |
    | **COM~rather**       |   402,067 |    0.04 |    4.44 |  25,775.15 | 86,330,752 | 83,102,035 |   402,648 |   387,589.21 |   14,477.79 | COMPLEMENT | rather       |
    | **COM~largely**      |   186,382 |    0.04 |    4.36 |  12,018.96 | 86,330,752 | 83,102,035 |   186,638 |   179,657.85 |    6,724.15 | COMPLEMENT | largely      |
    | **COM~supposedly**   |    30,854 |    0.04 |    4.13 |   2,118.60 | 86,330,752 | 83,102,035 |    30,878 |    29,723.18 |    1,130.82 | COMPLEMENT | supposedly   |
    | **COM~most**         | 7,713,908 |    0.04 |    3.84 | 465,492.10 | 86,330,752 | 83,102,035 | 7,734,027 | 7,444,779.15 |  269,128.85 | COMPLEMENT | most         |
    | **COM~albeit**       |    17,169 |    0.04 |    3.53 |   1,270.78 | 86,330,752 | 83,102,035 |    17,172 |    16,529.78 |      639.22 | COMPLEMENT | albeit       |
    | **COM~presumably**   |     8,011 |    0.04 |    2.59 |     568.20 | 86,330,752 | 83,102,035 |     8,015 |     7,715.24 |      295.76 | COMPLEMENT | presumably   |
    | **COM~alternately**  |     4,148 |    0.04 |    1.11 |     294.82 | 86,330,752 | 83,102,035 |     4,150 |     3,994.79 |      153.21 | COMPLEMENT | alternately  |
    
    
    |                    |    `f` |   `dP1` |   `LRC` |     `G2` |       `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`   | `l2`       |
    |:-------------------|-------:|--------:|--------:|---------:|----------:|----------:|-------:|----------:|------------:|:-------|:-----------|
    | **POS~pretty**     | 26,788 |    0.14 |    4.48 | 7,278.87 | 2,032,082 | 1,738,105 | 26,919 | 23,024.69 |    3,763.31 | POSMIR | pretty     |
    | **POS~rather**     |  9,290 |    0.14 |    4.34 | 2,607.01 | 2,032,082 | 1,738,105 |  9,322 |  7,973.41 |    1,316.59 | POSMIR | rather     |
    | **POS~plain**      |  6,049 |    0.14 |    4.19 | 1,733.36 | 2,032,082 | 1,738,105 |  6,065 |  5,187.59 |      861.41 | POSMIR | plain      |
    | **POS~otherwise**  |  9,368 |    0.14 |    4.12 | 2,558.73 | 2,032,082 | 1,738,105 |  9,410 |  8,048.68 |    1,319.32 | POSMIR | otherwise  |
    | **POS~fairly**     |  6,184 |    0.14 |    3.97 | 1,713.96 | 2,032,082 | 1,738,105 |  6,208 |  5,309.90 |      874.10 | POSMIR | fairly     |
    | **POS~somewhat**   |  4,961 |    0.14 |    3.87 | 1,391.12 | 2,032,082 | 1,738,105 |  4,978 |  4,257.84 |      703.16 | POSMIR | somewhat   |
    | **POS~downright**  |  5,502 |    0.14 |    3.63 | 1,465.04 | 2,032,082 | 1,738,105 |  5,532 |  4,731.70 |      770.30 | POSMIR | downright  |
    | **POS~already**    |  5,035 |    0.14 |    3.56 | 1,336.93 | 2,032,082 | 1,738,105 |  5,063 |  4,330.55 |      704.45 | POSMIR | already    |
    | **POS~relatively** |  5,774 |    0.14 |    3.51 | 1,496.02 | 2,032,082 | 1,738,105 |  5,812 |  4,971.19 |      802.81 | POSMIR | relatively |
    | **POS~maybe**      |  2,998 |    0.14 |    3.43 |   857.78 | 2,032,082 | 1,738,105 |  3,006 |  2,571.13 |      426.87 | POSMIR | maybe      |
    


#### 10 Most Positively/Non-Negatively Associated Adverbs  as ranked by $\Delta P(1|2)$ (`dP1`) and $LRC$ (sorted by `LRC`)

full dataset (_Absent Negation_ approximation)

|                      |       `f` |   `dP1` |   `LRC` |       `G2` |        `N` |       `f1` |      `f2` |      `exp_f` |   `unexp_f` | `l1`       | `l2`         |
|:---------------------|----------:|--------:|--------:|-----------:|-----------:|-----------:|----------:|-------------:|------------:|:-----------|:-------------|
| **COM~increasingly** |   404,356 |    0.04 |    6.00 |  29,076.69 | 86,330,752 | 83,102,035 |   404,521 |   389,392.16 |   14,963.84 | COMPLEMENT | increasingly |
| **COM~relatively**   |   626,369 |    0.04 |    5.24 |  42,957.87 | 86,330,752 | 83,102,035 |   626,884 |   603,438.92 |   22,930.08 | COMPLEMENT | relatively   |
| **COM~almost**       |   466,468 |    0.04 |    4.85 |  31,107.72 | 86,330,752 | 83,102,035 |   466,967 |   449,502.72 |   16,965.28 | COMPLEMENT | almost       |
| **COM~seemingly**    |   176,135 |    0.04 |    4.77 |  11,864.41 | 86,330,752 | 83,102,035 |   176,304 |   169,710.34 |    6,424.66 | COMPLEMENT | seemingly    |
| **COM~mostly**       |   212,255 |    0.04 |    4.71 |  14,160.67 | 86,330,752 | 83,102,035 |   212,478 |   204,531.45 |    7,723.55 | COMPLEMENT | mostly       |
| **COM~pretty**       | 1,650,041 |    0.04 |    4.64 | 107,081.72 | 86,330,752 | 83,102,035 | 1,652,360 | 1,590,562.75 |   59,478.25 | COMPLEMENT | pretty       |
| **COM~fairly**       |   401,326 |    0.04 |    4.50 |  25,904.34 | 86,330,752 | 83,102,035 |   401,879 |   386,848.97 |   14,477.03 | COMPLEMENT | fairly       |
| **COM~partly**       |    80,461 |    0.04 |    4.50 |   5,418.01 | 86,330,752 | 83,102,035 |    80,538 |    77,525.93 |    2,935.07 | COMPLEMENT | partly       |
| **COM~rather**       |   402,067 |    0.04 |    4.44 |  25,775.15 | 86,330,752 | 83,102,035 |   402,648 |   387,589.21 |   14,477.79 | COMPLEMENT | rather       |
| **COM~largely**      |   186,382 |    0.04 |    4.36 |  12,018.96 | 86,330,752 | 83,102,035 |   186,638 |   179,657.85 |    6,724.15 | COMPLEMENT | largely      |
| **COM~supposedly**   |    30,854 |    0.04 |    4.13 |   2,118.60 | 86,330,752 | 83,102,035 |    30,878 |    29,723.18 |    1,130.82 | COMPLEMENT | supposedly   |
| **COM~most**         | 7,713,908 |    0.04 |    3.84 | 465,492.10 | 86,330,752 | 83,102,035 | 7,734,027 | 7,444,779.15 |  269,128.85 | COMPLEMENT | most         |
| **COM~albeit**       |    17,169 |    0.04 |    3.53 |   1,270.78 | 86,330,752 | 83,102,035 |    17,172 |    16,529.78 |      639.22 | COMPLEMENT | albeit       |
| **COM~presumably**   |     8,011 |    0.04 |    2.59 |     568.20 | 86,330,752 | 83,102,035 |     8,015 |     7,715.24 |      295.76 | COMPLEMENT | presumably   |
| **COM~alternately**  |     4,148 |    0.04 |    1.11 |     294.82 | 86,330,752 | 83,102,035 |     4,150 |     3,994.79 |      153.21 | COMPLEMENT | alternately  |

`mirror` subset (_Present Positive_ approximation) 

|                    |    `f` |   `dP1` |   `LRC` |     `G2` |       `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`   | `l2`       |
|:-------------------|-------:|--------:|--------:|---------:|----------:|----------:|-------:|----------:|------------:|:-------|:-----------|
| **POS~pretty**     | 26,788 |    0.14 |    4.48 | 7,278.87 | 2,032,082 | 1,738,105 | 26,919 | 23,024.69 |    3,763.31 | POSMIR | pretty     |
| **POS~rather**     |  9,290 |    0.14 |    4.34 | 2,607.01 | 2,032,082 | 1,738,105 |  9,322 |  7,973.41 |    1,316.59 | POSMIR | rather     |
| **POS~plain**      |  6,049 |    0.14 |    4.19 | 1,733.36 | 2,032,082 | 1,738,105 |  6,065 |  5,187.59 |      861.41 | POSMIR | plain      |
| **POS~otherwise**  |  9,368 |    0.14 |    4.12 | 2,558.73 | 2,032,082 | 1,738,105 |  9,410 |  8,048.68 |    1,319.32 | POSMIR | otherwise  |
| **POS~fairly**     |  6,184 |    0.14 |    3.97 | 1,713.96 | 2,032,082 | 1,738,105 |  6,208 |  5,309.90 |      874.10 | POSMIR | fairly     |
| **POS~somewhat**   |  4,961 |    0.14 |    3.87 | 1,391.12 | 2,032,082 | 1,738,105 |  4,978 |  4,257.84 |      703.16 | POSMIR | somewhat   |
| **POS~downright**  |  5,502 |    0.14 |    3.63 | 1,465.04 | 2,032,082 | 1,738,105 |  5,532 |  4,731.70 |      770.30 | POSMIR | downright  |
| **POS~already**    |  5,035 |    0.14 |    3.56 | 1,336.93 | 2,032,082 | 1,738,105 |  5,063 |  4,330.55 |      704.45 | POSMIR | already    |
| **POS~relatively** |  5,774 |    0.14 |    3.51 | 1,496.02 | 2,032,082 | 1,738,105 |  5,812 |  4,971.19 |      802.81 | POSMIR | relatively |
| **POS~maybe**      |  2,998 |    0.14 |    3.43 |   857.78 | 2,032,082 | 1,738,105 |  3,006 |  2,571.13 |      426.87 | POSMIR | maybe      |


```python
def load_backup(lower_floor: int = 100,
                loaded_path: Path = adv_am_paths['RBdirect']) -> pd.DataFrame:
    located_paths = tuple(loaded_path.parent.glob(
        f'*35f-7c_min{lower_floor}x*{PKL_SUFF}'))
    if any(located_paths):
        backup_df = pd.read_pickle(located_paths[0])

        backup_df = backup_df.filter(like='NEG', axis=0).filter(
            items=FOCUS).reset_index().set_index('l2')
        backup_df.index.name = 'adv'
        return backup_df
    else:
        return []


def uncat(df):
    cats = df.select_dtypes('category').columns
    df[cats] = df[cats].astype('string')
    # print(df.dtypes)
    return df, cats


def fill_empties(name_1, name_2, both, loaded_paths):
    for name in (name_1, name_2):
        name = name.strip('_')
        path = loaded_paths['RBdirect'] if name == 'SET' else loaded_paths['NEGmirror']
        if any(both[f'f_{name}'].isna()):

            floor = 100
            neg_backup = load_backup(floor, loaded_path=path)
            if not any(neg_backup):
                print('Error. Backup data not found. [in fill_empties()]')

            neg_backup.columns = (pd.Series(adjust_assoc_columns(neg_backup.columns)
                                            ) + f'_{name}').to_list()
            both, cats = uncat(both)
            neg_backup, __ = uncat(neg_backup)

            undefined_adv = both.loc[
                both[f'f_{name}'].isna(), :].index.to_list()

            both.loc[undefined_adv,
                     neg_backup.columns] = neg_backup.filter(items=undefined_adv, axis=0)

            both[cats] = both[cats].astype('category')

    return both


def combine_top(df_1: pd.DataFrame,
                name_1: str,
                df_2: pd.DataFrame,
                name_2: str,
                env_filter: str = 'NEG',
                filter_items: list = FOCUS,
                k: int = 10) -> pd.DataFrame:

    top_dfs = [
        (get_top_vals(adv_df,  k=k,
                      index_like=env_filter,
                      metric_filter=['am_p1_given2',
                                     'conservative_log_ratio'])
         .sort_values('conservative_log_ratio', ascending=False))
        for adv_df in [df_1, df_2]
    ]
    for i, name in enumerate([name_1, name_2]):

        print_iter(
            [f'_{w}_' for w in top_dfs[i].l2], bullet='1.',
            header=(f'`{name}`: union of top {k} adverbs ranked by '
                    r'$LRC$ & $\Delta P(\texttt{env}|\texttt{adv})$'))
    top_adv_lists = [dx.l2.to_list() for dx in top_dfs]
    top_adv = pd.Series(top_adv_lists[0] + top_adv_lists[1]).drop_duplicates()
    # top_adv = pd.concat((top_dfs[0].l2, top_dfs[1].l2)).drop_duplicates()

    print_iter(
        [f'_{w}_' for w in top_adv], bullet='1.',
        header=f'Union of top adverbs for {name_1} and {name_2}. (Novel {name_2} adverbs listed last)')

    df_1 = narrow_selection(df_1, top_adv, env_filter, filter_items)
    df_2 = narrow_selection(df_2, top_adv, env_filter, filter_items)

    name_1, name_2 = [f"_{n.strip('_')}" for n in [name_1, name_2]]
    both = df_1.join(df_2, how="outer", lsuffix=name_1, rsuffix=name_2)

    # ! Empty cells need to be filled _before_ calculating mean
    both = fill_empties(name_1, name_2, both, adv_am_paths)
    both = force_ints(both)
    both = add_means(both)
    both = add_f_ratio(both, name_2, name_1)
    return both


def add_f_ratio(df, subset_name, superset_name):
    counts = df.filter(regex=r'^[Nf][12]?').columns.str.split(
        '_').str.get(0).drop_duplicates()
    for count in counts:
        ratio_col = f'ratio_{count}{subset_name}'
        df[ratio_col] = (df[f'{count}{subset_name}']
                         / df[f'{count}{superset_name}'])
        print(df.filter(like=count))
    return df

def add_means(both):
    for metric in (both.select_dtypes(include='number').columns.to_series()
                   .str.replace(r'_(MIR|SET)$', '', regex=True).unique()):
        both[f'mean_{snake_to_camel(metric)}'] = both.filter(
            regex=f"^{metric}").agg('mean', axis='columns')
    return both


def narrow_selection(df: pd.DataFrame,
                     top_adv: list,
                     env_filter: str = 'NEG',
                     filter_items: list = FOCUS):
    df = adjust_assoc_columns(
        df.filter(items=filter_items)
        .filter(like=env_filter, axis=0)
        .reset_index().set_index('l2')
        .filter(top_adv, axis=0))
    df.index.name = 'adv'
    nb_show_table(df)

    return df
```

## Compile top NEG~adverb associations across both approximation methods


```python
C = combine_top(setdiff_adv.copy(), 'SET',
                mirror_adv.copy(), 'MIR', k=K)
```

    
    `SET`: union of top 5 adverbs ranked by $LRC$ & $\Delta P(\texttt{env}|\texttt{adv})$
    1. _necessarily_
    1. _exactly_
    1. _that_
    1. _immediately_
    1. _yet_
    
    `MIR`: union of top 5 adverbs ranked by $LRC$ & $\Delta P(\texttt{env}|\texttt{adv})$
    1. _ever_
    1. _before_
    1. _exactly_
    1. _any_
    1. _remotely_
    
    Union of top adverbs for SET and MIR. (Novel MIR adverbs listed last)
    1. _necessarily_
    1. _exactly_
    1. _that_
    1. _immediately_
    1. _yet_
    1. _ever_
    1. _before_
    1. _any_
    1. _remotely_
    
    |                 | `key`              |     `f` |   `dP1` |   `LRC` |       `G2` |        `N` |      `f1` |    `f2` |   `exp_f` |   `unexp_f` | `l1`    |
    |:----------------|:-------------------|--------:|--------:|--------:|-----------:|-----------:|----------:|--------:|----------:|------------:|:--------|
    | **necessarily** | NEGany~necessarily |  42,708 |    0.72 |    6.23 | 219,003.46 | 86,330,752 | 3,226,213 |  56,694 |  2,118.68 |   40,589.32 | NEGATED |
    | **exactly**     | NEGany~exactly     |  43,635 |    0.67 |    5.90 | 214,404.20 | 86,330,752 | 3,226,213 |  61,599 |  2,301.98 |   41,333.02 | NEGATED |
    | **that**        | NEGany~that        | 165,411 |    0.63 |    5.62 | 781,016.11 | 86,330,752 | 3,226,213 | 250,392 |  9,357.24 |  156,053.76 | NEGATED |
    | **immediately** | NEGany~immediately |  57,319 |    0.52 |    4.96 | 239,462.58 | 86,330,752 | 3,226,213 | 103,177 |  3,855.76 |   53,463.24 | NEGATED |
    | **yet**         | NEGany~yet         |  52,546 |    0.48 |    4.74 | 209,055.78 | 86,330,752 | 3,226,213 | 101,707 |  3,800.83 |   48,745.17 | NEGATED |
    | **ever**        | NEGany~ever        |   5,967 |    0.01 |    0.28 |     353.58 | 86,330,752 | 3,226,213 | 124,592 |  4,656.05 |    1,310.95 | NEGATED |
    | **any**         | NEGany~any         |  15,492 |    0.13 |    2.28 |  23,683.00 | 86,330,752 | 3,226,213 |  94,152 |  3,518.50 |   11,973.50 | NEGATED |
    | **remotely**    | NEGany~remotely    |   5,679 |    0.22 |    3.03 |  13,354.33 | 86,330,752 | 3,226,213 |  22,194 |    829.40 |    4,849.60 | NEGATED |
    
    
    |                 | `key`              |   `f` |   `dP1` |   `LRC` |      `G2` |       `N` |    `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`   |
    |:----------------|:-------------------|------:|--------:|--------:|----------:|----------:|--------:|-------:|----------:|------------:|:-------|
    | **necessarily** | NEGmir~necessarily |   971 |    0.43 |    2.66 |  1,688.91 | 2,032,082 | 293,963 |  1,681 |    243.18 |      727.82 | NEGMIR |
    | **exactly**     | NEGmir~exactly     |   813 |    0.59 |    3.51 |  1,939.47 | 2,032,082 | 293,963 |  1,114 |    161.15 |      651.85 | NEGMIR |
    | **that**        | NEGmir~that        | 4,338 |    0.44 |    2.86 |  7,632.21 | 2,032,082 | 293,963 |  7,472 |  1,080.91 |    3,257.09 | NEGMIR |
    | **immediately** | NEGmir~immediately |   407 |    0.14 |    0.79 |    181.20 | 2,032,082 | 293,963 |  1,442 |    208.60 |      198.40 | NEGMIR |
    | **yet**         | NEGmir~yet         |   320 |    0.21 |    1.18 |    242.23 | 2,032,082 | 293,963 |    909 |    131.50 |      188.50 | NEGMIR |
    | **ever**        | NEGmir~ever        | 4,718 |    0.77 |    5.57 | 15,340.34 | 2,032,082 | 293,963 |  5,179 |    749.20 |    3,968.80 | NEGMIR |
    | **before**      | NEGmir~before      |   290 |    0.84 |    5.11 |  1,080.52 | 2,032,082 | 293,963 |    294 |     42.53 |      247.47 | NEGMIR |
    | **any**         | NEGmir~any         | 1,082 |    0.57 |    3.48 |  2,511.26 | 2,032,082 | 293,963 |  1,514 |    219.02 |      862.98 | NEGMIR |
    | **remotely**    | NEGmir~remotely    | 1,846 |    0.54 |    3.35 |  4,009.84 | 2,032,082 | 293,963 |  2,717 |    393.04 |    1,452.96 | NEGMIR |
    
                  f_SET   f1_SET  f2_SET  exp_f_SET  unexp_f_SET  f_MIR  f1_MIR  f2_MIR  \
    adv                                                                                   
    any           15492  3226213   94152   3,518.50    11,973.50   1082  293963    1514   
    before          311  3226213     748      27.95       283.05    290  293963     294   
    ever           5967  3226213  124592   4,656.05     1,310.95   4718  293963    5179   
    exactly       43635  3226213   61599   2,301.98    41,333.02    813  293963    1114   
    immediately   57319  3226213  103177   3,855.76    53,463.24    407  293963    1442   
    necessarily   42708  3226213   56694   2,118.68    40,589.32    971  293963    1681   
    remotely       5679  3226213   22194     829.40     4,849.60   1846  293963    2717   
    that         165411  3226213  250392   9,357.24   156,053.76   4338  293963    7472   
    yet           52546  3226213  101707   3,800.83    48,745.17    320  293963     909   
    
                 exp_f_MIR  unexp_f_MIR     mean_f      mean_f1    mean_f2  ratio_f_MIR  
    adv                                                                                  
    any             219.02       862.98 605,402.67 1,760,088.00  47,833.00         0.07  
    before           42.53       247.47 586,969.83 1,760,088.00     521.00         0.93  
    ever            749.20     3,968.80 610,105.33 1,760,088.00  64,885.50         0.79  
    exactly         161.15       651.85 604,556.17 1,760,088.00  31,356.50         0.02  
    immediately     208.60       198.40 613,753.50 1,760,088.00  52,309.50         0.01  
    necessarily     243.18       727.82 603,705.00 1,760,088.00  29,187.50         0.02  
    remotely        393.04     1,452.96 592,102.00 1,760,088.00  12,455.50         0.33  
    that          1,080.91     3,257.09 657,964.83 1,760,088.00 128,932.00         0.03  
    yet             131.50       188.50 612,609.67 1,760,088.00  51,308.00         0.01  
                    N_SET    N_MIR        mean_N  ratio_N_MIR
    adv                                                      
    any          86330752  2032082 44,181,417.00         0.02
    before       86330752  2032082 44,181,417.00         0.02
    ever         86330752  2032082 44,181,417.00         0.02
    exactly      86330752  2032082 44,181,417.00         0.02
    immediately  86330752  2032082 44,181,417.00         0.02
    necessarily  86330752  2032082 44,181,417.00         0.02
    remotely     86330752  2032082 44,181,417.00         0.02
    that         86330752  2032082 44,181,417.00         0.02
    yet          86330752  2032082 44,181,417.00         0.02
                  f1_SET  f1_MIR      mean_f1  ratio_f1_MIR
    adv                                                    
    any          3226213  293963 1,760,088.00          0.09
    before       3226213  293963 1,760,088.00          0.09
    ever         3226213  293963 1,760,088.00          0.09
    exactly      3226213  293963 1,760,088.00          0.09
    immediately  3226213  293963 1,760,088.00          0.09
    necessarily  3226213  293963 1,760,088.00          0.09
    remotely     3226213  293963 1,760,088.00          0.09
    that         3226213  293963 1,760,088.00          0.09
    yet          3226213  293963 1,760,088.00          0.09
                 f2_SET  f2_MIR    mean_f2  ratio_f2_MIR
    adv                                                 
    any           94152    1514  47,833.00          0.02
    before          748     294     521.00          0.39
    ever         124592    5179  64,885.50          0.04
    exactly       61599    1114  31,356.50          0.02
    immediately  103177    1442  52,309.50          0.01
    necessarily   56694    1681  29,187.50          0.03
    remotely      22194    2717  12,455.50          0.12
    that         250392    7472 128,932.00          0.03
    yet          101707     909  51,308.00          0.01


### Frequency Comparisons between Polarity Approximations: All Data vs. Mirror Subset
The following values indicate the percentage of the negated frequency (`f`) and the marginal frequency (`f2`) accounted for by the `mirror` subset for each adverb. 
That is, `ratio_f_MIR` indicates the percentage of negated tokens with the specific triggers covered by `NEGmirror`, 
and `ratio_f2_MIR` the percentage of all adverb tokens which were captured by _either_ mirror pattern, `POSmirror` or `NEGmirror`. 
The third column then indicates the discrepancy between these percentages: 
For example, 

- [ ] 🚩 **finish this discussion!**

Note that _before_ and _ever_ have a much higher proportions of their negated tokens representated in the mirror subset. 
However, the discrepancy indicated by the `difference` column, which illuminates the 

#### Percentage Comparision

|                   |  joint % MIR |  adverb % MIR | % MIR $\Delta$ |
|:------------------|-------------:|--------------:|---------------:|
| **ever**          |         79.1 |           4.2 |           74.9 |
| **before**        |         93.2 |          39.3 |           53.9 |
| **inherently**    |         41.9 |          10.3 |           31.7 |
| **intrinsically** |         40.3 |           9.9 |           30.4 |
| **remotely**      |         32.5 |          12.2 |           20.3 |
| **particularly**  |         16.6 |           2.6 |           14.0 |
| **overtly**       |         18.1 |           5.9 |           12.2 |
| **any**           |          7.0 |           1.6 |            5.4 |
| **terribly**      |          8.7 |           7.4 |            1.3 |
| **exactly**       |          1.9 |           1.8 |            0.1 |
| **entirely**      |          3.8 |           3.9 |           -0.1 |
| **yet**           |          0.6 |           0.9 |           -0.3 |
| **that**          |          2.6 |           3.0 |           -0.4 |
| **necessarily**   |          2.3 |           3.0 |           -0.7 |
| **immediately**   |          0.7 |           1.4 |           -0.7 |
| **only**          |          0.2 |           1.1 |           -1.0 |
| **altogether**    |          2.4 |           8.8 |           -6.3 |


```python
nb_show_table(C.filter(regex=r'^ratio_f2?_')
              .assign(f_minus_f2=C.ratio_f_MIR - C.ratio_f2_MIR)
              .multiply(100).round(1)
              .sort_values(['f_minus_f2', 'ratio_f_MIR'], ascending=False),
              n_dec=1, adjust_columns=False)

```

    
    |                 |   `ratio_f_MIR` |   `ratio_f2_MIR` |   `f_minus_f2` |
    |:----------------|----------------:|-----------------:|---------------:|
    | **ever**        |            79.1 |              4.2 |           74.9 |
    | **before**      |            93.2 |             39.3 |           53.9 |
    | **remotely**    |            32.5 |             12.2 |           20.3 |
    | **any**         |             7.0 |              1.6 |            5.4 |
    | **exactly**     |             1.9 |              1.8 |            0.1 |
    | **yet**         |             0.6 |              0.9 |           -0.3 |
    | **that**        |             2.6 |              3.0 |           -0.4 |
    | **necessarily** |             2.3 |              3.0 |           -0.7 |
    | **immediately** |             0.7 |              1.4 |           -0.7 |
    


#### Joint (_Negated_) Frequency Comparison

|                   |   `total negations` |   `mirror subset negations` |   `negations not in mirror subset` |
|:------------------|--------------------:|----------------------------:|-----------------------------------:|
| **that**          |             165,411 |                       4,338 |                            161,073 |
| **only**          |             114,070 |                         173 |                            113,897 |
| **entirely**      |              63,708 |                       2,429 |                             61,279 |
| **immediately**   |              57,319 |                         407 |                             56,912 |
| **yet**           |              52,546 |                         320 |                             52,226 |
| **particularly**  |              55,799 |                       9,278 |                             46,521 |
| **exactly**       |              43,635 |                         813 |                             42,822 |
| **necessarily**   |              42,708 |                         971 |                             41,737 |
| **terribly**      |              18,054 |                       1,579 |                             16,475 |
| **any**           |              15,492 |                       1,082 |                             14,410 |
| **altogether**    |               4,575 |                         112 |                              4,463 |
| **inherently**    |               6,847 |                       2,872 |                              3,975 |
| **remotely**      |               5,679 |                       1,846 |                              3,833 |
| **overtly**       |               2,169 |                         392 |                              1,777 |
| **ever**          |               5,967 |                       4,718 |                              1,249 |
| **intrinsically** |               1,071 |                         432 |                                639 |
| **before**        |                 311 |                         290 |                                 21 |


```python
nb_show_table(
    C
    # .assign(f_percent_MIR=C.ratio_f_MIR * 100)
    .filter(regex=r'^f_.*[MS]').sort_index(axis=1, ascending=False)
    .assign(
        f_diff=C.f_SET-C.f_MIR).sort_values('f_diff', ascending=False)
    .rename(columns={'f_SET':'total negations', 
                     'f_MIR':'mirror subset negations', 
                     'f_diff': 'negations not in mirror subset'}), n_dec=0)
```

    
    |                 |   `total negations` |   `mirror subset negations` |   `negations not in mirror subset` |
    |:----------------|--------------------:|----------------------------:|-----------------------------------:|
    | **that**        |             165,411 |                       4,338 |                            161,073 |
    | **immediately** |              57,319 |                         407 |                             56,912 |
    | **yet**         |              52,546 |                         320 |                             52,226 |
    | **exactly**     |              43,635 |                         813 |                             42,822 |
    | **necessarily** |              42,708 |                         971 |                             41,737 |
    | **any**         |              15,492 |                       1,082 |                             14,410 |
    | **remotely**    |               5,679 |                       1,846 |                              3,833 |
    | **ever**        |               5,967 |                       4,718 |                              1,249 |
    | **before**      |                 311 |                         290 |                                 21 |
    


#### Marginal (_Adverb Total_) Frequency Comparison

|                   |   `total adverb tokens` |   `mirror subset adverb tokens` |   `adverb tokens not in mirror subset` |
|:------------------|------------------------:|--------------------------------:|---------------------------------------:|
| **particularly**  |                 575,960 |                          14,954 |                                561,006 |
| **only**          |                 464,168 |                           5,169 |                                458,999 |
| **entirely**      |                 303,833 |                          11,803 |                                292,030 |
| **that**          |                 250,392 |                           7,472 |                                242,920 |
| **ever**          |                 124,592 |                           5,179 |                                119,413 |
| **immediately**   |                 103,177 |                           1,442 |                                101,735 |
| **yet**           |                 101,707 |                             909 |                                100,798 |
| **any**           |                  94,152 |                           1,514 |                                 92,638 |
| **terribly**      |                  70,174 |                           5,218 |                                 64,956 |
| **exactly**       |                  61,599 |                           1,114 |                                 60,485 |
| **necessarily**   |                  56,694 |                           1,681 |                                 55,013 |
| **inherently**    |                  55,088 |                           5,649 |                                 49,439 |
| **remotely**      |                  22,194 |                           2,717 |                                 19,477 |
| **altogether**    |                  20,636 |                           1,808 |                                 18,828 |
| **overtly**       |                  15,219 |                             898 |                                 14,321 |
| **intrinsically** |                  10,001 |                             991 |                                  9,010 |
| **before**        |                     748 |                             294 |                                    454 |


```python
nb_show_table(
    C
    # .assign(f2_percent_MIR=C.ratio_f2_MIR * 100)
    .filter(regex=r'^f2_.*[MS]').sort_index(axis=1, ascending=False)
    .assign(
        f2_diff=C.f2_SET-C.f2_MIR).sort_values('f2_diff', ascending=False)
    .rename(columns={'f2_SET':'total adverb tokens', 
                     'f2_MIR':'mirror subset adverb tokens', 
                     'f2_diff': 'adverb tokens not in mirror subset'}), n_dec=0)
```

    
    |                 |   `total adverb tokens` |   `mirror subset adverb tokens` |   `adverb tokens not in mirror subset` |
    |:----------------|------------------------:|--------------------------------:|---------------------------------------:|
    | **that**        |                 250,392 |                           7,472 |                                242,920 |
    | **ever**        |                 124,592 |                           5,179 |                                119,413 |
    | **immediately** |                 103,177 |                           1,442 |                                101,735 |
    | **yet**         |                 101,707 |                             909 |                                100,798 |
    | **any**         |                  94,152 |                           1,514 |                                 92,638 |
    | **exactly**     |                  61,599 |                           1,114 |                                 60,485 |
    | **necessarily** |                  56,694 |                           1,681 |                                 55,013 |
    | **remotely**    |                  22,194 |                           2,717 |                                 19,477 |
    | **before**      |                     748 |                             294 |                                    454 |
    



```python
full_C = C.copy()
main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in ('LRC', 'P1', 'G2')],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2'] ]) 
                              ).to_list()
print_iter([f'`{c}`' for c in main_cols_ordered], bullet='1.', header='Main Columns')
main_C = C[[c for c in main_cols_ordered if c in C.columns]]
main_C
```

    
    Main Columns
    1. `LRC_SET`
    1. `LRC_MIR`
    1. `mean_LRC`
    1. `dP1_SET`
    1. `dP1_MIR`
    1. `mean_dP1`
    1. `G2_SET`
    1. `G2_MIR`
    1. `mean_G2`
    1. `f_SET`
    1. `f_MIR`
    1. `f1_SET`
    1. `f1_MIR`
    1. `f2_SET`
    1. `f2_MIR`





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
      <th>LRC_SET</th>
      <th>LRC_MIR</th>
      <th>mean_LRC</th>
      <th>dP1_SET</th>
      <th>dP1_MIR</th>
      <th>mean_dP1</th>
      <th>G2_SET</th>
      <th>G2_MIR</th>
      <th>mean_G2</th>
      <th>f_SET</th>
      <th>f_MIR</th>
      <th>f1_SET</th>
      <th>f1_MIR</th>
      <th>f2_SET</th>
      <th>f2_MIR</th>
    </tr>
    <tr>
      <th>adv</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>any</th>
      <td>2.28</td>
      <td>3.48</td>
      <td>2.88</td>
      <td>0.13</td>
      <td>0.57</td>
      <td>0.35</td>
      <td>23,683.00</td>
      <td>2,511.26</td>
      <td>13,097.13</td>
      <td>15492</td>
      <td>1082</td>
      <td>3226213</td>
      <td>293963</td>
      <td>94152</td>
      <td>1514</td>
    </tr>
    <tr>
      <th>before</th>
      <td>3.65</td>
      <td>5.11</td>
      <td>4.38</td>
      <td>0.38</td>
      <td>0.84</td>
      <td>0.61</td>
      <td>1,062.13</td>
      <td>1,080.52</td>
      <td>1,071.32</td>
      <td>311</td>
      <td>290</td>
      <td>3226213</td>
      <td>293963</td>
      <td>748</td>
      <td>294</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>0.28</td>
      <td>5.57</td>
      <td>2.92</td>
      <td>0.01</td>
      <td>0.77</td>
      <td>0.39</td>
      <td>353.58</td>
      <td>15,340.34</td>
      <td>7,846.96</td>
      <td>5967</td>
      <td>4718</td>
      <td>3226213</td>
      <td>293963</td>
      <td>124592</td>
      <td>5179</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>5.90</td>
      <td>3.51</td>
      <td>4.71</td>
      <td>0.67</td>
      <td>0.59</td>
      <td>0.63</td>
      <td>214,404.20</td>
      <td>1,939.47</td>
      <td>108,171.83</td>
      <td>43635</td>
      <td>813</td>
      <td>3226213</td>
      <td>293963</td>
      <td>61599</td>
      <td>1114</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>4.96</td>
      <td>0.79</td>
      <td>2.88</td>
      <td>0.52</td>
      <td>0.14</td>
      <td>0.33</td>
      <td>239,462.58</td>
      <td>181.20</td>
      <td>119,821.89</td>
      <td>57319</td>
      <td>407</td>
      <td>3226213</td>
      <td>293963</td>
      <td>103177</td>
      <td>1442</td>
    </tr>
    <tr>
      <th>necessarily</th>
      <td>6.23</td>
      <td>2.66</td>
      <td>4.44</td>
      <td>0.72</td>
      <td>0.43</td>
      <td>0.57</td>
      <td>219,003.46</td>
      <td>1,688.91</td>
      <td>110,346.18</td>
      <td>42708</td>
      <td>971</td>
      <td>3226213</td>
      <td>293963</td>
      <td>56694</td>
      <td>1681</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>3.03</td>
      <td>3.35</td>
      <td>3.19</td>
      <td>0.22</td>
      <td>0.54</td>
      <td>0.38</td>
      <td>13,354.33</td>
      <td>4,009.84</td>
      <td>8,682.08</td>
      <td>5679</td>
      <td>1846</td>
      <td>3226213</td>
      <td>293963</td>
      <td>22194</td>
      <td>2717</td>
    </tr>
    <tr>
      <th>that</th>
      <td>5.62</td>
      <td>2.86</td>
      <td>4.24</td>
      <td>0.63</td>
      <td>0.44</td>
      <td>0.53</td>
      <td>781,016.11</td>
      <td>7,632.21</td>
      <td>394,324.16</td>
      <td>165411</td>
      <td>4338</td>
      <td>3226213</td>
      <td>293963</td>
      <td>250392</td>
      <td>7472</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>4.74</td>
      <td>1.18</td>
      <td>2.96</td>
      <td>0.48</td>
      <td>0.21</td>
      <td>0.34</td>
      <td>209,055.78</td>
      <td>242.23</td>
      <td>104,649.01</td>
      <td>52546</td>
      <td>320</td>
      <td>3226213</td>
      <td>293963</td>
      <td>101707</td>
      <td>909</td>
    </tr>
  </tbody>
</table>
</div>




```python
C.index.name = 'adv'
C=force_ints(C.sort_values('mean_LRC', ascending=False))
pd.set_option('display.max_columns', 16)
nb_show_table(C)
```

    
    |                 | `key_SET`          |   `f_SET` |   `dP1_SET` |   `LRC_SET` |   `G2_SET` |    `N_SET` |   `f1_SET` |   `f2_SET` |   `exp_f_SET` |   `unexp_f_SET` | `l1_SET`   | `key_MIR`          |   `f_MIR` |   `dP1_MIR` |   `LRC_MIR` |   `G2_MIR` |   `N_MIR` |   `f1_MIR` |   `f2_MIR` |   `exp_f_MIR` |   `unexp_f_MIR` | `l1_MIR`   |   `mean_f` |   `mean_dP1` |   `mean_LRC` |   `mean_G2` |      `mean_N` |    `mean_f1` |   `mean_f2` |   `mean_expF` |   `mean_unexpF` |   `r_f_MIR` |   `r_N_MIR` |   `r_f1_MIR` |   `r_f2_MIR` |
    |:----------------|:-------------------|----------:|------------:|------------:|-----------:|-----------:|-----------:|-----------:|--------------:|----------------:|:-----------|:-------------------|----------:|------------:|------------:|-----------:|----------:|-----------:|-----------:|--------------:|----------------:|:-----------|-----------:|-------------:|-------------:|------------:|--------------:|-------------:|------------:|--------------:|----------------:|------------:|------------:|-------------:|-------------:|
    | **exactly**     | NEGany~exactly     |    43,635 |        0.67 |        5.90 | 214,404.20 | 86,330,752 |  3,226,213 |     61,599 |      2,301.98 |       41,333.02 | NEGATED    | NEGmir~exactly     |       813 |        0.59 |        3.51 |   1,939.47 | 2,032,082 |    293,963 |      1,114 |        161.15 |          651.85 | NEGMIR     | 604,556.17 |         0.63 |         4.71 |  108,171.83 | 44,181,417.00 | 1,760,088.00 |   31,356.50 |      1,231.57 |       20,992.43 |        0.02 |        0.02 |         0.09 |         0.02 |
    | **necessarily** | NEGany~necessarily |    42,708 |        0.72 |        6.23 | 219,003.46 | 86,330,752 |  3,226,213 |     56,694 |      2,118.68 |       40,589.32 | NEGATED    | NEGmir~necessarily |       971 |        0.43 |        2.66 |   1,688.91 | 2,032,082 |    293,963 |      1,681 |        243.18 |          727.82 | NEGMIR     | 603,705.00 |         0.57 |         4.44 |  110,346.18 | 44,181,417.00 | 1,760,088.00 |   29,187.50 |      1,180.93 |       20,658.57 |        0.02 |        0.02 |         0.09 |         0.03 |
    | **before**      | NEG~before         |       311 |        0.38 |        3.65 |   1,062.13 | 86,330,752 |  3,226,213 |        748 |         27.95 |          283.05 | NEGATED    | NEGmir~before      |       290 |        0.84 |        5.11 |   1,080.52 | 2,032,082 |    293,963 |        294 |         42.53 |          247.47 | NEGMIR     | 586,969.83 |         0.61 |         4.38 |    1,071.32 | 44,181,417.00 | 1,760,088.00 |      521.00 |         35.24 |          265.26 |        0.93 |        0.02 |         0.09 |         0.39 |
    | **that**        | NEGany~that        |   165,411 |        0.63 |        5.62 | 781,016.11 | 86,330,752 |  3,226,213 |    250,392 |      9,357.24 |      156,053.76 | NEGATED    | NEGmir~that        |     4,338 |        0.44 |        2.86 |   7,632.21 | 2,032,082 |    293,963 |      7,472 |      1,080.91 |        3,257.09 | NEGMIR     | 657,964.83 |         0.53 |         4.24 |  394,324.16 | 44,181,417.00 | 1,760,088.00 |  128,932.00 |      5,219.08 |       79,655.42 |        0.03 |        0.02 |         0.09 |         0.03 |
    | **remotely**    | NEGany~remotely    |     5,679 |        0.22 |        3.03 |  13,354.33 | 86,330,752 |  3,226,213 |     22,194 |        829.40 |        4,849.60 | NEGATED    | NEGmir~remotely    |     1,846 |        0.54 |        3.35 |   4,009.84 | 2,032,082 |    293,963 |      2,717 |        393.04 |        1,452.96 | NEGMIR     | 592,102.00 |         0.38 |         3.19 |    8,682.08 | 44,181,417.00 | 1,760,088.00 |   12,455.50 |        611.22 |        3,151.28 |        0.33 |        0.02 |         0.09 |         0.12 |
    | **yet**         | NEGany~yet         |    52,546 |        0.48 |        4.74 | 209,055.78 | 86,330,752 |  3,226,213 |    101,707 |      3,800.83 |       48,745.17 | NEGATED    | NEGmir~yet         |       320 |        0.21 |        1.18 |     242.23 | 2,032,082 |    293,963 |        909 |        131.50 |          188.50 | NEGMIR     | 612,609.67 |         0.34 |         2.96 |  104,649.01 | 44,181,417.00 | 1,760,088.00 |   51,308.00 |      1,966.16 |       24,466.84 |        0.01 |        0.02 |         0.09 |         0.01 |
    | **ever**        | NEGany~ever        |     5,967 |        0.01 |        0.28 |     353.58 | 86,330,752 |  3,226,213 |    124,592 |      4,656.05 |        1,310.95 | NEGATED    | NEGmir~ever        |     4,718 |        0.77 |        5.57 |  15,340.34 | 2,032,082 |    293,963 |      5,179 |        749.20 |        3,968.80 | NEGMIR     | 610,105.33 |         0.39 |         2.92 |    7,846.96 | 44,181,417.00 | 1,760,088.00 |   64,885.50 |      2,702.62 |        2,639.88 |        0.79 |        0.02 |         0.09 |         0.04 |
    | **immediately** | NEGany~immediately |    57,319 |        0.52 |        4.96 | 239,462.58 | 86,330,752 |  3,226,213 |    103,177 |      3,855.76 |       53,463.24 | NEGATED    | NEGmir~immediately |       407 |        0.14 |        0.79 |     181.20 | 2,032,082 |    293,963 |      1,442 |        208.60 |          198.40 | NEGMIR     | 613,753.50 |         0.33 |         2.88 |  119,821.89 | 44,181,417.00 | 1,760,088.00 |   52,309.50 |      2,032.18 |       26,830.82 |        0.01 |        0.02 |         0.09 |         0.01 |
    | **any**         | NEGany~any         |    15,492 |        0.13 |        2.28 |  23,683.00 | 86,330,752 |  3,226,213 |     94,152 |      3,518.50 |       11,973.50 | NEGATED    | NEGmir~any         |     1,082 |        0.57 |        3.48 |   2,511.26 | 2,032,082 |    293,963 |      1,514 |        219.02 |          862.98 | NEGMIR     | 605,402.67 |         0.35 |         2.88 |   13,097.13 | 44,181,417.00 | 1,760,088.00 |   47,833.00 |      1,868.76 |        6,418.24 |        0.07 |        0.02 |         0.09 |         0.02 |
    


Save full adverb selection as `.csv`


```python
C.to_csv(TOP_AM_DIR / f'Top{K}_NEG-ADV_combined.35f-7c_{timestamp_today()}.csv')
```

Save `all-columns`, `means`, and `MAIN` as markdown formatted tables


```python
C.to_markdown(floatfmt=',.2f', intfmt=',', buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_all-columns.35f-7c_{timestamp_today()}.md')
C.filter(like='mean_').to_markdown(floatfmt=',.2f', intfmt=',', buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_means.35f-7c_{timestamp_today()}.md')
C[main_cols_ordered].to_markdown(floatfmt=',.2f', intfmt=',', buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_MAIN.35f-7c_{timestamp_today()}.md')
```

## Collect bigrams corresponding to top adverbs


```python
# results/assoc_df/polar/RBdirect/bigram/polarized-bigram_35f-7c_min1000x.pkl.gz
bigram_floor = 200
mirror_floor = 50
bigram_dfs = {d.name:
              update_index(pd.read_pickle(
                  tuple(d.joinpath('bigram/extra')
                        .glob(f'*35f-7c*min{mirror_floor if d.name == "NEGmirror" else bigram_floor}x*.pkl.gz')
                        )[0]))
              for d in POLAR_DIR.iterdir()}
```


```python
def show_adv_bigrams(sample_size, C, 
                     bigram_dfs, 
                     selector:str='dP1',
                     column_list: list = None) -> dict:
    def _force_ints(_df):
        count_cols = _df.filter(regex=r'total$|^[fN]').columns
        _df[count_cols] = _df[count_cols].apply(
            pd.to_numeric, downcast='unsigned')
        return _df
    bigram_k = max(sample_size + 2, 10)
    print(f'## Top {bigram_k} "most negative" bigrams corresponding to top {K} adverbs\n')
    print(timestamp_today())
    patterns = list(bigram_dfs.keys())
    top_adverbs = C.index
    bigram_samples = dict.fromkeys(top_adverbs)
    bigrams = []
    adj = []
    for rank,adv in enumerate(top_adverbs, start=1):
        print(f'\n### {rank}. _{adv}_\n')
        adv_top = None
        bigram_samples[adv] = dict.fromkeys(patterns + ['both', 'adj'])
        adj_for_adv = []
        for pat, bdf in bigram_dfs.items():
            # avoid KeyError while maintaining intended order
            bdf = adjust_assoc_columns(
                bdf[[c for c in FOCUS+['adj', 'adj_total', 'adv', 'adv_total']
                     if c in bdf.columns]
                    ])
            #> Force significant & positive association according to LRC
            bdf = bdf.loc[bdf.LRC >= 1, :]

            adv_pat_bigrams = _force_ints(
                bdf.filter(like=f'~{adv}_', axis=0)
                .nlargest(bigram_k, [selector]+list({'LRC', 'dP1'} - {selector}))
                )

            if adv_pat_bigrams.empty:
                print(f'No bigrams found in loaded `{pat}` AM table.')
            else:
                print(
                    f'\n#### Top {bigram_k} `{pat}` "{adv}_*" bigrams (sorted by `{selector}`; `LRC > 1`)\n')
                column_list = column_list or bdf.columns
                nb_show_table(adv_pat_bigrams[column_list], n_dec=2)

            adj_for_adv.extend(adv_pat_bigrams.adj.drop_duplicates().to_list())

            bigram_samples[adv][pat] = adv_pat_bigrams

            adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
                [adv_top, adv_pat_bigrams])

        bigram_samples[adv]['adj'] = set(adj_for_adv)
        bigrams.extend(adv_top.l2.drop_duplicates().to_list())
        adj.extend(adj_for_adv)
        bigram_samples[adv]['both'] = adv_top
    bigram_samples['bigrams'] = set(bigrams)
    bigram_samples['adj'] = set(adj)
    return bigram_samples, bigram_k


samples_dict, bigram_k = show_adv_bigrams(
    K, C, bigram_dfs,
    column_list=[
        'adj', 'adj_total',
        *pd.Series(main_cols_ordered).str.replace(
            r'mean_|_SET|_MIR', '', regex=True)
        .drop_duplicates().to_list(),
        # 't', 'MI'
    ]
)
```

    ## Top 10 "most negative" bigrams corresponding to top 5 adverbs
    
    2024-05-21
    
    ### 1. _exactly_
    
    
    #### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                               | `adj`      |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
    |:------------------------------|:-----------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
    | **NEGany~exactly_surprising** | surprising |       150,067 |    7.34 |    0.96 |  2,863.35 |   441 | 3,226,213 |    444 |
    | **NEGany~exactly_cheap**      | cheap      |        83,765 |    8.28 |    0.95 |  4,443.27 |   693 | 3,226,213 |    704 |
    | **NEGany~exactly_subtle**     | subtle     |        56,845 |    6.92 |    0.94 |  1,671.02 |   264 | 3,226,213 |    271 |
    | **NEGany~exactly_fun**        | fun        |       224,457 |    6.67 |    0.94 |  1,423.92 |   225 | 3,226,213 |    231 |
    | **NEGany~exactly_conducive**  | conducive  |        16,405 |    6.56 |    0.93 |  1,313.09 |   208 | 3,226,213 |    214 |
    | **NEGany~exactly_easy**       | easy       |       771,307 |    8.37 |    0.93 |  6,747.64 | 1,069 | 3,226,213 |  1,100 |
    | **NEGany~exactly_new**        | new        |       321,311 |    8.54 |    0.93 |  8,697.93 | 1,378 | 3,226,213 |  1,418 |
    | **NEGany~exactly_hard**       | hard       |       430,990 |    6.53 |    0.92 |  1,267.04 |   203 | 3,226,213 |    211 |
    | **NEGany~exactly_clear**      | clear      |       491,108 |    8.30 |    0.92 | 10,937.16 | 1,759 | 3,226,213 |  1,835 |
    | **NEGany~exactly_sure**       | sure       |       844,981 |    8.63 |    0.92 | 54,750.58 | 8,860 | 3,226,213 |  9,301 |
    
    
    #### Top 10 `NEGmirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          | `adj`   |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
    |:-------------------------|:--------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
    | **NEGmir~exactly_sure**  | sure    |        11,297 |    2.09 |    0.85 | 560.65 |   148 | 293,963 |    149 |
    | **NEGmir~exactly_clear** | clear   |         8,639 |    2.13 |    0.80 | 178.73 |    52 | 293,963 |     55 |
    
    
    ### 2. _necessarily_
    
    
    #### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                       | `adj`          |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
    |:--------------------------------------|:---------------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
    | **NEGany~necessarily_sure**           | sure           |       844,981 |    5.91 |    0.95 | 1,436.68 |   222 | 3,226,213 |    224 |
    | **NEGany~necessarily_surprising**     | surprising     |       150,067 |    7.22 |    0.93 | 2,150.86 |   343 | 3,226,213 |    355 |
    | **NEGany~necessarily_indicative**     | indicative     |        12,760 |    8.37 |    0.93 | 8,811.69 | 1,406 | 3,226,213 |  1,456 |
    | **NEGany~necessarily_representative** | representative |        25,187 |    7.31 |    0.91 | 3,044.27 |   496 | 3,226,213 |    524 |
    | **NEGany~necessarily_available**      | available      |       866,272 |    6.36 |    0.89 | 1,280.24 |   213 | 3,226,213 |    230 |
    | **NEGany~necessarily_easy**           | easy           |       771,307 |    7.26 |    0.88 | 5,448.34 |   914 | 3,226,213 |    996 |
    | **NEGany~necessarily_illegal**        | illegal        |        44,028 |    6.48 |    0.87 | 1,659.90 |   280 | 3,226,213 |    307 |
    | **NEGany~necessarily_interested**     | interested     |       364,497 |    6.77 |    0.87 | 2,500.26 |   422 | 3,226,213 |    463 |
    | **NEGany~necessarily_obvious**        | obvious        |       193,498 |    6.16 |    0.87 | 1,211.19 |   206 | 3,226,213 |    228 |
    | **NEGany~necessarily_aware**          | aware          |       321,193 |    6.12 |    0.86 | 1,221.21 |   209 | 3,226,213 |    233 |
    
    
    #### Top 10 `NEGmirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                              | `adj`   |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
    |:-----------------------------|:--------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
    | **NEGmir~necessarily_wrong** | wrong   |        24,007 |    4.19 |    0.77 | 693.55 |   213 | 293,963 |    233 |
    | **NEGmir~necessarily_true**  | true    |         8,402 |    1.64 |    0.49 | 105.71 |    53 | 293,963 |     83 |
    | **NEGmir~necessarily_bad**   | bad     |        12,841 |    1.48 |    0.47 |  93.65 |    50 | 293,963 |     82 |
    
    
    ### 3. _before_
    
    No bigrams found in loaded `RBdirect` AM table.
    
    #### Top 10 `NEGmirror` "before_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                             | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
    |:----------------------------|:----------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
    | **NEGmir~before_available** | available |        14,919 |    3.99 |    0.84 | 654.92 |   177 | 293,963 |    180 |
    
    
    ### 4. _that_
    
    
    #### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                             | `adj`       |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
    |:----------------------------|:------------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
    | **NEGany~that_uncommon**    | uncommon    |        61,767 |    8.39 |    0.94 | 5,136.91 |   804 | 3,226,213 |    819 |
    | **NEGany~that_fond**        | fond        |        39,809 |    7.27 |    0.94 | 2,127.94 |   334 | 3,226,213 |    341 |
    | **NEGany~that_surprising**  | surprising  |       150,067 |    8.14 |    0.92 | 7,115.30 | 1,141 | 3,226,213 |  1,187 |
    | **NEGany~that_common**      | common      |       556,435 |    8.12 |    0.92 | 7,564.08 | 1,216 | 3,226,213 |  1,268 |
    | **NEGany~that_dissimilar**  | dissimilar  |         8,816 |    7.00 |    0.92 | 1,904.15 |   307 | 3,226,213 |    321 |
    | **NEGany~that_unusual**     | unusual     |       108,584 |    7.94 |    0.92 | 6,096.13 |   983 | 3,226,213 |  1,028 |
    | **NEGany~that_complicated** | complicated |       180,071 |    7.95 |    0.91 | 7,450.89 | 1,208 | 3,226,213 |  1,270 |
    | **NEGany~that_noticeable**  | noticeable  |        40,372 |    6.78 |    0.91 | 1,632.07 |   265 | 3,226,213 |    279 |
    | **NEGany~that_impressed**   | impressed   |       113,281 |    7.57 |    0.91 | 4,207.58 |   684 | 3,226,213 |    721 |
    | **NEGany~that_exciting**    | exciting    |       236,396 |    7.48 |    0.90 | 4,892.83 |   805 | 3,226,213 |    859 |
    
    
    #### Top 10 `NEGmirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                            | `adj`      |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
    |:---------------------------|:-----------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
    | **NEGmir~that_simple**     | simple     |        27,835 |    4.48 |    0.74 | 1,483.32 |   478 | 293,963 |    540 |
    | **NEGmir~that_close**      | close      |        15,958 |    2.53 |    0.71 |   177.72 |    60 | 293,963 |     70 |
    | **NEGmir~that_easy**       | easy       |        21,775 |    3.91 |    0.68 | 1,278.04 |   458 | 293,963 |    558 |
    | **NEGmir~that_interested** | interested |        10,913 |    2.45 |    0.67 |   171.51 |    62 | 293,963 |     76 |
    | **NEGmir~that_big**        | big        |         9,564 |    2.99 |    0.66 |   308.12 |   113 | 293,963 |    140 |
    | **NEGmir~that_hard**       | hard       |         8,168 |    2.25 |    0.63 |   152.67 |    59 | 293,963 |     76 |
    | **NEGmir~that_popular**    | popular    |         6,409 |    2.34 |    0.63 |   167.47 |    65 | 293,963 |     84 |
    | **NEGmir~that_serious**    | serious    |        10,801 |    1.93 |    0.59 |   120.37 |    50 | 293,963 |     68 |
    | **NEGmir~that_good**       | good       |        38,252 |    2.65 |    0.47 |   848.28 |   449 | 293,963 |    732 |
    | **NEGmir~that_difficult**  | difficult  |        18,107 |    1.08 |    0.36 |    74.23 |    52 | 293,963 |    103 |
    
    
    ### 5. _remotely_
    
    
    #### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                | `adj`      |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
    |:-------------------------------|:-----------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
    | **NEGany~remotely_true**       | true       |       348,994 |    4.46 |    0.56 | 1,089.49 |   250 | 3,226,213 |    420 |
    | **NEGany~remotely_close**      | close      |       480,288 |    2.92 |    0.23 | 1,722.76 |   696 | 3,226,213 |  2,558 |
    | **NEGany~remotely_interested** | interested |       364,497 |    2.72 |    0.23 |   808.74 |   333 | 3,226,213 |  1,252 |
    
    
    #### Top 10 `NEGmirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 | `adj`       |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
    |:--------------------------------|:------------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
    | **NEGmir~remotely_true**        | true        |         8,402 |    2.59 |    0.73 | 184.98 |    61 | 293,963 |     70 |
    | **NEGmir~remotely_close**       | close       |        15,958 |    3.02 |    0.59 | 524.61 |   219 | 293,963 |    299 |
    | **NEGmir~remotely_interesting** | interesting |        14,240 |    1.52 |    0.45 | 102.91 |    57 | 293,963 |     96 |
    | **NEGmir~remotely_similar**     | similar     |         7,887 |    1.62 |    0.43 | 123.23 |    71 | 293,963 |    123 |
    
    
    ### 6. _yet_
    
    
    #### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                            | `adj`       |   `adj_total` |   `LRC` |   `dP1` |      `G2` |    `f` |      `f1` |   `f2` |
    |:---------------------------|:------------|--------------:|--------:|--------:|----------:|-------:|----------:|-------:|
    | **NEGany~yet_clear**       | clear       |       491,108 |   10.26 |    0.95 | 67,924.56 | 10,553 | 3,226,213 | 10,693 |
    | **NEGany~yet_eligible**    | eligible    |        49,578 |    7.72 |    0.94 |  2,929.15 |    459 | 3,226,213 |    468 |
    | **NEGany~yet_official**    | official    |         9,778 |    7.33 |    0.94 |  2,236.98 |    353 | 3,226,213 |    362 |
    | **NEGany~yet_ready**       | ready       |       240,297 |    9.23 |    0.93 | 48,012.06 |  7,611 | 3,226,213 |  7,838 |
    | **NEGany~yet_certain**     | certain     |       104,544 |    8.12 |    0.93 |  5,491.41 |    874 | 3,226,213 |    903 |
    | **NEGany~yet_complete**    | complete    |       107,018 |    8.42 |    0.92 | 13,815.99 |  2,220 | 3,226,213 |  2,314 |
    | **NEGany~yet_sure**        | sure        |       844,981 |    8.37 |    0.92 | 12,379.79 |  1,990 | 3,226,213 |  2,075 |
    | **NEGany~yet_right**       | right       |       204,572 |    6.50 |    0.92 |  1,254.20 |    202 | 3,226,213 |    211 |
    | **NEGany~yet_operational** | operational |        17,793 |    6.56 |    0.92 |  1,312.87 |    212 | 3,226,213 |    222 |
    | **NEGany~yet_public**      | public      |        41,602 |    7.36 |    0.91 |  3,055.97 |    496 | 3,226,213 |    522 |
    
    No bigrams found in loaded `NEGmirror` AM table.
    
    ### 7. _ever_
    
    
    #### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                         | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |       `f1` |   `f2` |
    |:------------------------|:--------|--------------:|--------:|--------:|---------:|------:|-----------:|-------:|
    | **NEGany~ever_simple**  | simple  |       427,167 |    5.54 |    0.77 | 1,142.04 |   212 |  3,226,213 |    262 |
    | **NEGany~ever_easy**    | easy    |       771,307 |    5.06 |    0.63 | 2,030.58 |   430 |  3,226,213 |    641 |
    | **NEGany~ever_good**    | good    |     2,037,285 |    3.76 |    0.40 | 1,178.00 |   332 |  3,226,213 |    756 |
    | **NEGany~ever_perfect** | perfect |       164,519 |    3.48 |    0.37 |   736.05 |   217 |  3,226,213 |    527 |
    | **NEGany~ever_able**    | able    |       428,268 |    1.81 |    0.13 |   363.95 |   234 |  3,226,213 |  1,398 |
    | **COM~ever_closer**     | closer  |        70,294 |    1.52 |    0.04 |   501.08 | 6,880 | 83,102,035 |  6,882 |
    | **COM~ever_popular**    | popular |       828,951 |    1.67 |    0.04 |   283.43 | 4,485 | 83,102,035 |  4,492 |
    | **COM~ever_more**       | more    |     1,032,280 |    1.72 |    0.03 |   331.84 | 6,763 | 83,102,035 |  6,792 |
    | **COM~ever_present**    | present |       127,265 |    1.70 |    0.03 |   354.47 | 7,602 | 83,102,035 |  7,639 |
    
    
    #### Top 10 `NEGmirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                           | `adj`     |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
    |:--------------------------|:----------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
    | **NEGmir~ever_perfect**   | perfect   |         4,239 |    2.58 |    0.85 |   788.18 |   207 | 293,963 |    208 |
    | **NEGmir~ever_easy**      | easy      |        21,775 |    4.66 |    0.85 | 1,399.10 |   368 | 293,963 |    370 |
    | **NEGmir~ever_good**      | good      |        38,252 |    5.05 |    0.84 | 1,103.09 |   300 | 293,963 |    306 |
    | **NEGmir~ever_free**      | free      |         5,605 |    2.18 |    0.83 |   249.22 |    69 | 293,963 |     71 |
    | **NEGmir~ever_wrong**     | wrong     |        24,007 |    3.34 |    0.82 |   361.62 |   102 | 293,963 |    106 |
    | **NEGmir~ever_available** | available |        14,919 |    1.69 |    0.82 |   177.01 |    50 | 293,963 |     52 |
    | **NEGmir~ever_worth**     | worth     |         6,182 |    2.16 |    0.80 |   182.49 |    53 | 293,963 |     56 |
    | **NEGmir~ever_able**      | able      |         8,177 |    3.73 |    0.77 |   441.74 |   136 | 293,963 |    149 |
    | **NEGmir~ever_true**      | true      |         8,402 |    2.35 |    0.75 |   160.72 |    51 | 293,963 |     57 |
    | **NEGmir~ever_likely**    | likely    |        15,433 |    2.00 |    0.46 |   192.81 |   103 | 293,963 |    169 |
    
    
    ### 8. _immediately_
    
    
    #### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                   | `adj`      |   `adj_total` |   `LRC` |   `dP1` |       `G2` |    `f` |      `f1` |   `f2` |
    |:----------------------------------|:-----------|--------------:|--------:|--------:|-----------:|-------:|----------:|-------:|
    | **NEGany~immediately_possible**   | possible   |       364,265 |    7.68 |    0.90 |   6,269.26 |  1,027 | 3,226,213 |  1,091 |
    | **NEGany~immediately_clear**      | clear      |       491,108 |    8.32 |    0.90 | 153,302.22 | 25,276 | 3,226,213 | 27,066 |
    | **NEGany~immediately_available**  | available  |       866,272 |    5.77 |    0.66 | 102,962.94 | 21,297 | 3,226,213 | 30,725 |
    | **NEGany~immediately_able**       | able       |       428,268 |    4.87 |    0.58 |   2,851.84 |    639 | 3,226,213 |  1,036 |
    | **NEGany~immediately_obvious**    | obvious    |       193,498 |    4.59 |    0.49 |   9,043.23 |  2,258 | 3,226,213 |  4,305 |
    | **NEGany~immediately_successful** | successful |       407,004 |    3.47 |    0.36 |     958.19 |    292 | 3,226,213 |    743 |
    | **NEGany~immediately_apparent**   | apparent   |        64,104 |    3.80 |    0.35 |   6,581.69 |  2,031 | 3,226,213 |  5,260 |
    | **NEGany~immediately_visible**    | visible    |       137,609 |    3.35 |    0.32 |   1,324.08 |    436 | 3,226,213 |  1,234 |
    | **NEGany~immediately_evident**    | evident    |        60,888 |    2.96 |    0.25 |   1,122.08 |    428 | 3,226,213 |  1,466 |
    
    
    #### Top 10 `NEGmirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                  | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
    |:---------------------------------|:----------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
    | **NEGmir~immediately_available** | available |        14,919 |    1.91 |    0.39 | 258.42 |   164 | 293,963 |    304 |
    
    
    ### 9. _any_
    
    
    #### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
    |:-------------------------|:----------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
    | **NEGany~any_happier**   | happier   |        19,501 |    4.65 |    0.53 | 3,488.76 |   830 | 3,226,213 |  1,472 |
    | **NEGany~any_simpler**   | simpler   |        26,094 |    3.09 |    0.30 |   671.74 |   228 | 3,226,213 |    672 |
    | **NEGany~any_clearer**   | clearer   |        13,369 |    3.21 |    0.30 | 1,051.22 |   357 | 3,226,213 |  1,053 |
    | **NEGany~any_different** | different |       909,864 |    2.98 |    0.24 | 2,270.24 |   910 | 3,226,213 |  3,313 |
    | **NEGany~any_younger**   | younger   |        29,805 |    2.37 |    0.19 |   544.17 |   256 | 3,226,213 |  1,121 |
    | **NEGany~any_bigger**    | bigger    |       130,470 |    2.27 |    0.17 |   688.06 |   357 | 3,226,213 |  1,735 |
    | **NEGany~any_worse**     | worse     |       214,166 |    2.47 |    0.16 | 3,165.88 | 1,693 | 3,226,213 |  8,487 |
    | **NEGany~any_harder**    | harder    |        99,332 |    1.98 |    0.15 |   395.22 |   227 | 3,226,213 |  1,221 |
    | **NEGany~any_safer**     | safer     |        26,779 |    1.73 |    0.12 |   346.68 |   235 | 3,226,213 |  1,471 |
    | **NEGany~any_higher**    | higher    |       271,250 |    1.77 |    0.12 |   434.16 |   301 | 3,226,213 |  1,921 |
    
    
    #### Top 10 `NEGmirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
    |:-------------------------|:----------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
    | **NEGmir~any_different** | different |        40,266 |    2.35 |    0.75 | 160.72 |    51 | 293,963 |     57 |
    | **NEGmir~any_better**    | better    |        16,232 |    3.42 |    0.61 | 960.25 |   382 | 293,963 |    503 |
    | **NEGmir~any_easier**    | easier    |         2,640 |    2.29 |    0.61 | 166.41 |    67 | 293,963 |     89 |
    | **NEGmir~any_closer**    | closer    |         1,168 |    2.09 |    0.60 | 138.45 |    57 | 293,963 |     77 |
    | **NEGmir~any_worse**     | worse     |        11,295 |    1.45 |    0.36 | 127.07 |    88 | 293,963 |    173 |
    



```python
for key, info in samples_dict.items():
    if key in ('bigrams', 'adj'):
        key = f'ALL {key.replace("adj", "adjectives")}'
    formatted_iter = [
        f'_{a.replace("_", " ")}_' for a
        in (info['adj'] if isinstance(info, dict)
            else info)]
    print_iter(formatted_iter,
               header=f'1. _{key}_ ({len(formatted_iter)} unique)',
               bullet='1.', indent=3)
```

    
    1. _exactly_ (10 unique)
       1. _surprising_
       1. _new_
       1. _conducive_
       1. _subtle_
       1. _clear_
       1. _hard_
       1. _sure_
       1. _easy_
       1. _cheap_
       1. _fun_
    
    1. _necessarily_ (13 unique)
       1. _surprising_
       1. _interested_
       1. _aware_
       1. _illegal_
       1. _available_
       1. _obvious_
       1. _bad_
       1. _wrong_
       1. _true_
       1. _sure_
       1. _indicative_
       1. _easy_
       1. _representative_
    
    1. _before_ (1 unique)
       1. _available_
    
    1. _that_ (20 unique)
       1. _surprising_
       1. _interested_
       1. _fond_
       1. _good_
       1. _hard_
       1. _uncommon_
       1. _impressed_
       1. _simple_
       1. _popular_
       1. _serious_
       1. _noticeable_
       1. _exciting_
       1. _dissimilar_
       1. _complicated_
       1. _difficult_
       1. _big_
       1. _unusual_
       1. _close_
       1. _common_
       1. _easy_
    
    1. _remotely_ (5 unique)
       1. _interested_
       1. _interesting_
       1. _close_
       1. _true_
       1. _similar_
    
    1. _yet_ (10 unique)
       1. _eligible_
       1. _public_
       1. _clear_
       1. _complete_
       1. _right_
       1. _operational_
       1. _ready_
       1. _certain_
       1. _official_
       1. _sure_
    
    1. _ever_ (15 unique)
       1. _closer_
       1. _available_
       1. _more_
       1. _simple_
       1. _able_
       1. _good_
       1. _popular_
       1. _wrong_
       1. _present_
       1. _perfect_
       1. _free_
       1. _worth_
       1. _likely_
       1. _true_
       1. _easy_
    
    1. _immediately_ (9 unique)
       1. _possible_
       1. _available_
       1. _evident_
       1. _obvious_
       1. _able_
       1. _clear_
       1. _apparent_
       1. _successful_
       1. _visible_
    
    1. _any_ (13 unique)
       1. _simpler_
       1. _bigger_
       1. _different_
       1. _closer_
       1. _easier_
       1. _higher_
       1. _harder_
       1. _younger_
       1. _happier_
       1. _worse_
       1. _clearer_
       1. _safer_
       1. _better_
    
    1. _ALL bigrams_ (96 unique)
       1. _necessarily sure_
       1. _that noticeable_
       1. _that simple_
       1. _immediately successful_
       1. _any younger_
       1. _ever free_
       1. _necessarily obvious_
       1. _before available_
       1. _yet certain_
       1. _exactly easy_
       1. _ever able_
       1. _that fond_
       1. _remotely similar_
       1. _necessarily illegal_
       1. _that surprising_
       1. _that popular_
       1. _ever perfect_
       1. _immediately possible_
       1. _any happier_
       1. _any different_
       1. _yet sure_
       1. _any bigger_
       1. _that common_
       1. _necessarily aware_
       1. _immediately available_
       1. _exactly conducive_
       1. _necessarily available_
       1. _that easy_
       1. _remotely close_
       1. _any simpler_
       1. _yet public_
       1. _ever closer_
       1. _exactly cheap_
       1. _that dissimilar_
       1. _ever wrong_
       1. _exactly hard_
       1. _any better_
       1. _necessarily true_
       1. _immediately able_
       1. _necessarily easy_
       1. _necessarily representative_
       1. _yet eligible_
       1. _exactly clear_
       1. _that exciting_
       1. _ever available_
       1. _yet clear_
       1. _immediately visible_
       1. _that interested_
       1. _yet ready_
       1. _any closer_
       1. _ever present_
       1. _any safer_
       1. _that big_
       1. _remotely true_
       1. _that unusual_
       1. _that complicated_
       1. _immediately apparent_
       1. _ever easy_
       1. _necessarily bad_
       1. _yet official_
       1. _immediately evident_
       1. _necessarily surprising_
       1. _remotely interested_
       1. _yet operational_
       1. _that good_
       1. _ever true_
       1. _necessarily indicative_
       1. _that impressed_
       1. _remotely interesting_
       1. _ever more_
       1. _ever popular_
       1. _necessarily interested_
       1. _exactly new_
       1. _yet right_
       1. _any easier_
       1. _exactly fun_
       1. _exactly sure_
       1. _yet complete_
       1. _ever worth_
       1. _that uncommon_
       1. _that close_
       1. _immediately obvious_
       1. _exactly subtle_
       1. _any higher_
       1. _immediately clear_
       1. _that difficult_
       1. _that hard_
       1. _ever good_
       1. _that serious_
       1. _ever simple_
       1. _exactly surprising_
       1. _any harder_
       1. _necessarily wrong_
       1. _any clearer_
       1. _ever likely_
       1. _any worse_
    
    1. _ALL adjectives_ (71 unique)
       1. _surprising_
       1. _interested_
       1. _aware_
       1. _interesting_
       1. _available_
       1. _possible_
       1. _evident_
       1. _fond_
       1. _obvious_
       1. _higher_
       1. _good_
       1. _subtle_
       1. _clear_
       1. _free_
       1. _hard_
       1. _true_
       1. _indicative_
       1. _certain_
       1. _successful_
       1. _fun_
       1. _representative_
       1. _uncommon_
       1. _illegal_
       1. _impressed_
       1. _closer_
       1. _different_
       1. _simple_
       1. _able_
       1. _bad_
       1. _popular_
       1. _harder_
       1. _complete_
       1. _right_
       1. _serious_
       1. _ready_
       1. _operational_
       1. _safer_
       1. _better_
       1. _noticeable_
       1. _new_
       1. _exciting_
       1. _dissimilar_
       1. _more_
       1. _complicated_
       1. _easier_
       1. _wrong_
       1. _difficult_
       1. _happier_
       1. _younger_
       1. _worth_
       1. _apparent_
       1. _worse_
       1. _official_
       1. _big_
       1. _simpler_
       1. _eligible_
       1. _public_
       1. _unusual_
       1. _bigger_
       1. _conducive_
       1. _close_
       1. _common_
       1. _perfect_
       1. _present_
       1. _likely_
       1. _sure_
       1. _clearer_
       1. _easy_
       1. _cheap_
       1. _visible_
       1. _similar_



```python
NEG_bigrams_sample = pd.concat(
    (ad['both'] for ad in samples_dict.values() if isinstance(ad, dict))).sort_values('LRC', ascending=False)
```


```python
top_NEGbigram_df_path = TOP_AM_DIR.joinpath(
    f'Top{K}_NEG-ADV_top-{bigram_k}-bigrams.{timestamp_today()}.csv')
print(top_NEGbigram_df_path)
NEG_bigrams_sample.to_csv(top_NEGbigram_df_path)
nb_show_table(NEG_bigrams_sample.sort_values('LRC', ascending=False), outpath= top_NEGbigram_df_path.with_suffix('.md'))
```

    /share/compling/projects/sanpi/results/top_AM/Top5_NEG-ADV_top-10-bigrams.2024-05-21.csv
    
    |                                       |    `f` |   `dP1` |   `LRC` |       `G2` |        `N` |       `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`       | `l2`                       | `adj`          |   `adj_total` | `adv`       |   `adv_total` |
    |:--------------------------------------|-------:|--------:|--------:|-----------:|-----------:|-----------:|-------:|----------:|------------:|:-----------|:---------------------------|:---------------|--------------:|:------------|--------------:|
    | **NEGany~yet_clear**                  | 10,553 |    0.95 |   10.26 |  67,924.56 | 86,330,752 |  3,226,213 | 10,693 |    399.60 |   10,153.40 | NEGATED    | yet_clear                  | clear          |    491,108.00 | yet         |    101,707.00 |
    | **NEGany~yet_ready**                  |  7,611 |    0.93 |    9.23 |  48,012.06 | 86,330,752 |  3,226,213 |  7,838 |    292.91 |    7,318.09 | NEGATED    | yet_ready                  | ready          |    240,297.00 | yet         |    101,707.00 |
    | **NEGany~exactly_sure**               |  8,860 |    0.92 |    8.63 |  54,750.58 | 86,330,752 |  3,226,213 |  9,301 |    347.58 |    8,512.42 | NEGATED    | exactly_sure               | sure           |    844,981.00 | exactly     |     61,599.00 |
    | **NEGany~exactly_new**                |  1,378 |    0.93 |    8.54 |   8,697.93 | 86,330,752 |  3,226,213 |  1,418 |     52.99 |    1,325.01 | NEGATED    | exactly_new                | new            |    321,311.00 | exactly     |     61,599.00 |
    | **NEGany~yet_complete**               |  2,220 |    0.92 |    8.42 |  13,815.99 | 86,330,752 |  3,226,213 |  2,314 |     86.48 |    2,133.52 | NEGATED    | yet_complete               | complete       |    107,018.00 | yet         |    101,707.00 |
    | **NEGany~that_uncommon**              |    804 |    0.94 |    8.39 |   5,136.91 | 86,330,752 |  3,226,213 |    819 |     30.61 |      773.39 | NEGATED    | that_uncommon              | uncommon       |     61,767.00 | that        |    250,392.00 |
    | **NEGany~necessarily_indicative**     |  1,406 |    0.93 |    8.37 |   8,811.69 | 86,330,752 |  3,226,213 |  1,456 |     54.41 |    1,351.59 | NEGATED    | necessarily_indicative     | indicative     |     12,760.00 | necessarily |     56,694.00 |
    | **NEGany~yet_sure**                   |  1,990 |    0.92 |    8.37 |  12,379.79 | 86,330,752 |  3,226,213 |  2,075 |     77.54 |    1,912.46 | NEGATED    | yet_sure                   | sure           |    844,981.00 | yet         |    101,707.00 |
    | **NEGany~exactly_easy**               |  1,069 |    0.93 |    8.37 |   6,747.64 | 86,330,752 |  3,226,213 |  1,100 |     41.11 |    1,027.89 | NEGATED    | exactly_easy               | easy           |    771,307.00 | exactly     |     61,599.00 |
    | **NEGany~immediately_clear**          | 25,276 |    0.90 |    8.32 | 153,302.22 | 86,330,752 |  3,226,213 | 27,066 |  1,011.47 |   24,264.53 | NEGATED    | immediately_clear          | clear          |    491,108.00 | immediately |    103,177.00 |
    | **NEGany~exactly_clear**              |  1,759 |    0.92 |    8.30 |  10,937.16 | 86,330,752 |  3,226,213 |  1,835 |     68.57 |    1,690.43 | NEGATED    | exactly_clear              | clear          |    491,108.00 | exactly     |     61,599.00 |
    | **NEGany~exactly_cheap**              |    693 |    0.95 |    8.28 |   4,443.27 | 86,330,752 |  3,226,213 |    704 |     26.31 |      666.69 | NEGATED    | exactly_cheap              | cheap          |     83,765.00 | exactly     |     61,599.00 |
    | **NEGany~that_surprising**            |  1,141 |    0.92 |    8.14 |   7,115.30 | 86,330,752 |  3,226,213 |  1,187 |     44.36 |    1,096.64 | NEGATED    | that_surprising            | surprising     |    150,067.00 | that        |    250,392.00 |
    | **NEGany~that_common**                |  1,216 |    0.92 |    8.12 |   7,564.08 | 86,330,752 |  3,226,213 |  1,268 |     47.39 |    1,168.61 | NEGATED    | that_common                | common         |    556,435.00 | that        |    250,392.00 |
    | **NEGany~yet_certain**                |    874 |    0.93 |    8.12 |   5,491.41 | 86,330,752 |  3,226,213 |    903 |     33.75 |      840.25 | NEGATED    | yet_certain                | certain        |    104,544.00 | yet         |    101,707.00 |
    | **NEGany~that_complicated**           |  1,208 |    0.91 |    7.95 |   7,450.89 | 86,330,752 |  3,226,213 |  1,270 |     47.46 |    1,160.54 | NEGATED    | that_complicated           | complicated    |    180,071.00 | that        |    250,392.00 |
    | **NEGany~that_unusual**               |    983 |    0.92 |    7.94 |   6,096.13 | 86,330,752 |  3,226,213 |  1,028 |     38.42 |      944.58 | NEGATED    | that_unusual               | unusual        |    108,584.00 | that        |    250,392.00 |
    | **NEGany~yet_eligible**               |    459 |    0.94 |    7.72 |   2,929.15 | 86,330,752 |  3,226,213 |    468 |     17.49 |      441.51 | NEGATED    | yet_eligible               | eligible       |     49,578.00 | yet         |    101,707.00 |
    | **NEGany~immediately_possible**       |  1,027 |    0.90 |    7.68 |   6,269.26 | 86,330,752 |  3,226,213 |  1,091 |     40.77 |      986.23 | NEGATED    | immediately_possible       | possible       |    364,265.00 | immediately |    103,177.00 |
    | **NEGany~that_impressed**             |    684 |    0.91 |    7.57 |   4,207.58 | 86,330,752 |  3,226,213 |    721 |     26.94 |      657.06 | NEGATED    | that_impressed             | impressed      |    113,281.00 | that        |    250,392.00 |
    | **NEGany~that_exciting**              |    805 |    0.90 |    7.48 |   4,892.83 | 86,330,752 |  3,226,213 |    859 |     32.10 |      772.90 | NEGATED    | that_exciting              | exciting       |    236,396.00 | that        |    250,392.00 |
    | **NEGany~yet_public**                 |    496 |    0.91 |    7.36 |   3,055.97 | 86,330,752 |  3,226,213 |    522 |     19.51 |      476.49 | NEGATED    | yet_public                 | public         |     41,602.00 | yet         |    101,707.00 |
    | **NEGany~exactly_surprising**         |    441 |    0.96 |    7.34 |   2,863.35 | 86,330,752 |  3,226,213 |    444 |     16.59 |      424.41 | NEGATED    | exactly_surprising         | surprising     |    150,067.00 | exactly     |     61,599.00 |
    | **NEGany~yet_official**               |    353 |    0.94 |    7.33 |   2,236.98 | 86,330,752 |  3,226,213 |    362 |     13.53 |      339.47 | NEGATED    | yet_official               | official       |      9,778.00 | yet         |    101,707.00 |
    | **NEGany~necessarily_representative** |    496 |    0.91 |    7.31 |   3,044.27 | 86,330,752 |  3,226,213 |    524 |     19.58 |      476.42 | NEGATED    | necessarily_representative | representative |     25,187.00 | necessarily |     56,694.00 |
    | **NEGany~that_fond**                  |    334 |    0.94 |    7.27 |   2,127.94 | 86,330,752 |  3,226,213 |    341 |     12.74 |      321.26 | NEGATED    | that_fond                  | fond           |     39,809.00 | that        |    250,392.00 |
    | **NEGany~necessarily_easy**           |    914 |    0.88 |    7.26 |   5,448.34 | 86,330,752 |  3,226,213 |    996 |     37.22 |      876.78 | NEGATED    | necessarily_easy           | easy           |    771,307.00 | necessarily |     56,694.00 |
    | **NEGany~necessarily_surprising**     |    343 |    0.93 |    7.22 |   2,150.86 | 86,330,752 |  3,226,213 |    355 |     13.27 |      329.73 | NEGATED    | necessarily_surprising     | surprising     |    150,067.00 | necessarily |     56,694.00 |
    | **NEGany~that_dissimilar**            |    307 |    0.92 |    7.00 |   1,904.15 | 86,330,752 |  3,226,213 |    321 |     12.00 |      295.00 | NEGATED    | that_dissimilar            | dissimilar     |      8,816.00 | that        |    250,392.00 |
    | **NEGany~exactly_subtle**             |    264 |    0.94 |    6.92 |   1,671.02 | 86,330,752 |  3,226,213 |    271 |     10.13 |      253.87 | NEGATED    | exactly_subtle             | subtle         |     56,845.00 | exactly     |     61,599.00 |
    | **NEGany~that_noticeable**            |    265 |    0.91 |    6.78 |   1,632.07 | 86,330,752 |  3,226,213 |    279 |     10.43 |      254.57 | NEGATED    | that_noticeable            | noticeable     |     40,372.00 | that        |    250,392.00 |
    | **NEGany~necessarily_interested**     |    422 |    0.87 |    6.77 |   2,500.26 | 86,330,752 |  3,226,213 |    463 |     17.30 |      404.70 | NEGATED    | necessarily_interested     | interested     |    364,497.00 | necessarily |     56,694.00 |
    | **NEGany~exactly_fun**                |    225 |    0.94 |    6.67 |   1,423.92 | 86,330,752 |  3,226,213 |    231 |      8.63 |      216.37 | NEGATED    | exactly_fun                | fun            |    224,457.00 | exactly     |     61,599.00 |
    | **NEGany~exactly_conducive**          |    208 |    0.93 |    6.56 |   1,313.09 | 86,330,752 |  3,226,213 |    214 |      8.00 |      200.00 | NEGATED    | exactly_conducive          | conducive      |     16,405.00 | exactly     |     61,599.00 |
    | **NEGany~yet_operational**            |    212 |    0.92 |    6.56 |   1,312.87 | 86,330,752 |  3,226,213 |    222 |      8.30 |      203.70 | NEGATED    | yet_operational            | operational    |     17,793.00 | yet         |    101,707.00 |
    | **NEGany~exactly_hard**               |    203 |    0.92 |    6.53 |   1,267.04 | 86,330,752 |  3,226,213 |    211 |      7.89 |      195.11 | NEGATED    | exactly_hard               | hard           |    430,990.00 | exactly     |     61,599.00 |
    | **NEGany~yet_right**                  |    202 |    0.92 |    6.50 |   1,254.20 | 86,330,752 |  3,226,213 |    211 |      7.89 |      194.11 | NEGATED    | yet_right                  | right          |    204,572.00 | yet         |    101,707.00 |
    | **NEGany~necessarily_illegal**        |    280 |    0.87 |    6.48 |   1,659.90 | 86,330,752 |  3,226,213 |    307 |     11.47 |      268.53 | NEGATED    | necessarily_illegal        | illegal        |     44,028.00 | necessarily |     56,694.00 |
    | **NEGany~necessarily_available**      |    213 |    0.89 |    6.36 |   1,280.24 | 86,330,752 |  3,226,213 |    230 |      8.60 |      204.40 | NEGATED    | necessarily_available      | available      |    866,272.00 | necessarily |     56,694.00 |
    | **NEGany~necessarily_obvious**        |    206 |    0.87 |    6.16 |   1,211.19 | 86,330,752 |  3,226,213 |    228 |      8.52 |      197.48 | NEGATED    | necessarily_obvious        | obvious        |    193,498.00 | necessarily |     56,694.00 |
    | **NEGany~necessarily_aware**          |    209 |    0.86 |    6.12 |   1,221.21 | 86,330,752 |  3,226,213 |    233 |      8.71 |      200.29 | NEGATED    | necessarily_aware          | aware          |    321,193.00 | necessarily |     56,694.00 |
    | **NEGany~necessarily_sure**           |    222 |    0.95 |    5.91 |   1,436.68 | 86,330,752 |  3,226,213 |    224 |      8.37 |      213.63 | NEGATED    | necessarily_sure           | sure           |    844,981.00 | necessarily |     56,694.00 |
    | **NEGany~immediately_available**      | 21,297 |    0.66 |    5.77 | 102,962.94 | 86,330,752 |  3,226,213 | 30,725 |  1,148.20 |   20,148.80 | NEGATED    | immediately_available      | available      |    866,272.00 | immediately |    103,177.00 |
    | **NEGany~ever_simple**                |    212 |    0.77 |    5.54 |   1,142.04 | 86,330,752 |  3,226,213 |    262 |      9.79 |      202.21 | NEGATED    | ever_simple                | simple         |    427,167.00 | ever        |    124,592.00 |
    | **NEGany~ever_easy**                  |    430 |    0.63 |    5.06 |   2,030.58 | 86,330,752 |  3,226,213 |    641 |     23.95 |      406.05 | NEGATED    | ever_easy                  | easy           |    771,307.00 | ever        |    124,592.00 |
    | **NEGmir~ever_good**                  |    300 |    0.84 |    5.05 |   1,103.09 |  2,032,082 |    293,963 |    306 |     44.27 |      255.73 | NEGMIR     | ever_good                  | good           |     38,252.00 | ever        |      5,179.00 |
    | **NEGany~immediately_able**           |    639 |    0.58 |    4.87 |   2,851.84 | 86,330,752 |  3,226,213 |  1,036 |     38.72 |      600.28 | NEGATED    | immediately_able           | able           |    428,268.00 | immediately |    103,177.00 |
    | **NEGmir~ever_easy**                  |    368 |    0.85 |    4.66 |   1,399.10 |  2,032,082 |    293,963 |    370 |     53.52 |      314.48 | NEGMIR     | ever_easy                  | easy           |     21,775.00 | ever        |      5,179.00 |
    | **NEGany~any_happier**                |    830 |    0.53 |    4.65 |   3,488.76 | 86,330,752 |  3,226,213 |  1,472 |     55.01 |      774.99 | NEGATED    | any_happier                | happier        |     19,501.00 | any         |     94,152.00 |
    | **NEGany~immediately_obvious**        |  2,258 |    0.49 |    4.59 |   9,043.23 | 86,330,752 |  3,226,213 |  4,305 |    160.88 |    2,097.12 | NEGATED    | immediately_obvious        | obvious        |    193,498.00 | immediately |    103,177.00 |
    | **NEGmir~that_simple**                |    478 |    0.74 |    4.48 |   1,483.32 |  2,032,082 |    293,963 |    540 |     78.12 |      399.88 | NEGMIR     | that_simple                | simple         |     27,835.00 | that        |      7,472.00 |
    | **NEGany~remotely_true**              |    250 |    0.56 |    4.46 |   1,089.49 | 86,330,752 |  3,226,213 |    420 |     15.70 |      234.30 | NEGATED    | remotely_true              | true           |    348,994.00 | remotely    |     22,194.00 |
    | **NEGmir~necessarily_wrong**          |    213 |    0.77 |    4.19 |     693.55 |  2,032,082 |    293,963 |    233 |     33.71 |      179.29 | NEGMIR     | necessarily_wrong          | wrong          |     24,007.00 | necessarily |      1,681.00 |
    | **NEGmir~before_available**           |    177 |    0.84 |    3.99 |     654.92 |  2,032,082 |    293,963 |    180 |     26.04 |      150.96 | NEGMIR     | before_available           | available      |     14,919.00 | before      |        294.00 |
    | **NEGmir~that_easy**                  |    458 |    0.68 |    3.91 |   1,278.04 |  2,032,082 |    293,963 |    558 |     80.72 |      377.28 | NEGMIR     | that_easy                  | easy           |     21,775.00 | that        |      7,472.00 |
    | **NEGany~immediately_apparent**       |  2,031 |    0.35 |    3.80 |   6,581.69 | 86,330,752 |  3,226,213 |  5,260 |    196.57 |    1,834.43 | NEGATED    | immediately_apparent       | apparent       |     64,104.00 | immediately |    103,177.00 |
    | **NEGany~ever_good**                  |    332 |    0.40 |    3.76 |   1,178.00 | 86,330,752 |  3,226,213 |    756 |     28.25 |      303.75 | NEGATED    | ever_good                  | good           |  2,037,285.00 | ever        |    124,592.00 |
    | **NEGmir~ever_able**                  |    136 |    0.77 |    3.73 |     441.74 |  2,032,082 |    293,963 |    149 |     21.55 |      114.45 | NEGMIR     | ever_able                  | able           |      8,177.00 | ever        |      5,179.00 |
    | **NEGany~ever_perfect**               |    217 |    0.37 |    3.48 |     736.05 | 86,330,752 |  3,226,213 |    527 |     19.69 |      197.31 | NEGATED    | ever_perfect               | perfect        |    164,519.00 | ever        |    124,592.00 |
    | **NEGany~immediately_successful**     |    292 |    0.36 |    3.47 |     958.19 | 86,330,752 |  3,226,213 |    743 |     27.77 |      264.23 | NEGATED    | immediately_successful     | successful     |    407,004.00 | immediately |    103,177.00 |
    | **NEGmir~any_better**                 |    382 |    0.61 |    3.42 |     960.25 |  2,032,082 |    293,963 |    503 |     72.76 |      309.24 | NEGMIR     | any_better                 | better         |     16,232.00 | any         |      1,514.00 |
    | **NEGany~immediately_visible**        |    436 |    0.32 |    3.35 |   1,324.08 | 86,330,752 |  3,226,213 |  1,234 |     46.12 |      389.88 | NEGATED    | immediately_visible        | visible        |    137,609.00 | immediately |    103,177.00 |
    | **NEGmir~ever_wrong**                 |    102 |    0.82 |    3.34 |     361.62 |  2,032,082 |    293,963 |    106 |     15.33 |       86.67 | NEGMIR     | ever_wrong                 | wrong          |     24,007.00 | ever        |      5,179.00 |
    | **NEGany~any_clearer**                |    357 |    0.30 |    3.21 |   1,051.22 | 86,330,752 |  3,226,213 |  1,053 |     39.35 |      317.65 | NEGATED    | any_clearer                | clearer        |     13,369.00 | any         |     94,152.00 |
    | **NEGany~any_simpler**                |    228 |    0.30 |    3.09 |     671.74 | 86,330,752 |  3,226,213 |    672 |     25.11 |      202.89 | NEGATED    | any_simpler                | simpler        |     26,094.00 | any         |     94,152.00 |
    | **NEGmir~remotely_close**             |    219 |    0.59 |    3.02 |     524.61 |  2,032,082 |    293,963 |    299 |     43.25 |      175.75 | NEGMIR     | remotely_close             | close          |     15,958.00 | remotely    |      2,717.00 |
    | **NEGmir~that_big**                   |    113 |    0.66 |    2.99 |     308.12 |  2,032,082 |    293,963 |    140 |     20.25 |       92.75 | NEGMIR     | that_big                   | big            |      9,564.00 | that        |      7,472.00 |
    | **NEGany~any_different**              |    910 |    0.24 |    2.98 |   2,270.24 | 86,330,752 |  3,226,213 |  3,313 |    123.81 |      786.19 | NEGATED    | any_different              | different      |    909,864.00 | any         |     94,152.00 |
    | **NEGany~immediately_evident**        |    428 |    0.25 |    2.96 |   1,122.08 | 86,330,752 |  3,226,213 |  1,466 |     54.78 |      373.22 | NEGATED    | immediately_evident        | evident        |     60,888.00 | immediately |    103,177.00 |
    | **NEGany~remotely_close**             |    696 |    0.23 |    2.92 |   1,722.76 | 86,330,752 |  3,226,213 |  2,558 |     95.59 |      600.41 | NEGATED    | remotely_close             | close          |    480,288.00 | remotely    |     22,194.00 |
    | **NEGany~remotely_interested**        |    333 |    0.23 |    2.72 |     808.74 | 86,330,752 |  3,226,213 |  1,252 |     46.79 |      286.21 | NEGATED    | remotely_interested        | interested     |    364,497.00 | remotely    |     22,194.00 |
    | **NEGmir~that_good**                  |    449 |    0.47 |    2.65 |     848.28 |  2,032,082 |    293,963 |    732 |    105.89 |      343.11 | NEGMIR     | that_good                  | good           |     38,252.00 | that        |      7,472.00 |
    | **NEGmir~remotely_true**              |     61 |    0.73 |    2.59 |     184.98 |  2,032,082 |    293,963 |     70 |     10.13 |       50.87 | NEGMIR     | remotely_true              | true           |      8,402.00 | remotely    |      2,717.00 |
    | **NEGmir~ever_perfect**               |    207 |    0.85 |    2.58 |     788.18 |  2,032,082 |    293,963 |    208 |     30.09 |      176.91 | NEGMIR     | ever_perfect               | perfect        |      4,239.00 | ever        |      5,179.00 |
    | **NEGmir~that_close**                 |     60 |    0.71 |    2.53 |     177.72 |  2,032,082 |    293,963 |     70 |     10.13 |       49.87 | NEGMIR     | that_close                 | close          |     15,958.00 | that        |      7,472.00 |
    | **NEGany~any_worse**                  |  1,693 |    0.16 |    2.47 |   3,165.88 | 86,330,752 |  3,226,213 |  8,487 |    317.16 |    1,375.84 | NEGATED    | any_worse                  | worse          |    214,166.00 | any         |     94,152.00 |
    | **NEGmir~that_interested**            |     62 |    0.67 |    2.45 |     171.51 |  2,032,082 |    293,963 |     76 |     10.99 |       51.01 | NEGMIR     | that_interested            | interested     |     10,913.00 | that        |      7,472.00 |
    | **NEGany~any_younger**                |    256 |    0.19 |    2.37 |     544.17 | 86,330,752 |  3,226,213 |  1,121 |     41.89 |      214.11 | NEGATED    | any_younger                | younger        |     29,805.00 | any         |     94,152.00 |
    | **NEGmir~ever_true**                  |     51 |    0.75 |    2.35 |     160.72 |  2,032,082 |    293,963 |     57 |      8.25 |       42.75 | NEGMIR     | ever_true                  | true           |      8,402.00 | ever        |      5,179.00 |
    | **NEGmir~any_different**              |     51 |    0.75 |    2.35 |     160.72 |  2,032,082 |    293,963 |     57 |      8.25 |       42.75 | NEGMIR     | any_different              | different      |     40,266.00 | any         |      1,514.00 |
    | **NEGmir~that_popular**               |     65 |    0.63 |    2.34 |     167.47 |  2,032,082 |    293,963 |     84 |     12.15 |       52.85 | NEGMIR     | that_popular               | popular        |      6,409.00 | that        |      7,472.00 |
    | **NEGmir~any_easier**                 |     67 |    0.61 |    2.29 |     166.41 |  2,032,082 |    293,963 |     89 |     12.87 |       54.13 | NEGMIR     | any_easier                 | easier         |      2,640.00 | any         |      1,514.00 |
    | **NEGany~any_bigger**                 |    357 |    0.17 |    2.27 |     688.06 | 86,330,752 |  3,226,213 |  1,735 |     64.84 |      292.16 | NEGATED    | any_bigger                 | bigger         |    130,470.00 | any         |     94,152.00 |
    | **NEGmir~that_hard**                  |     59 |    0.63 |    2.25 |     152.67 |  2,032,082 |    293,963 |     76 |     10.99 |       48.01 | NEGMIR     | that_hard                  | hard           |      8,168.00 | that        |      7,472.00 |
    | **NEGmir~ever_free**                  |     69 |    0.83 |    2.18 |     249.22 |  2,032,082 |    293,963 |     71 |     10.27 |       58.73 | NEGMIR     | ever_free                  | free           |      5,605.00 | ever        |      5,179.00 |
    | **NEGmir~ever_worth**                 |     53 |    0.80 |    2.16 |     182.49 |  2,032,082 |    293,963 |     56 |      8.10 |       44.90 | NEGMIR     | ever_worth                 | worth          |      6,182.00 | ever        |      5,179.00 |
    | **NEGmir~exactly_clear**              |     52 |    0.80 |    2.13 |     178.73 |  2,032,082 |    293,963 |     55 |      7.96 |       44.04 | NEGMIR     | exactly_clear              | clear          |      8,639.00 | exactly     |      1,114.00 |
    | **NEGmir~exactly_sure**               |    148 |    0.85 |    2.09 |     560.65 |  2,032,082 |    293,963 |    149 |     21.55 |      126.45 | NEGMIR     | exactly_sure               | sure           |     11,297.00 | exactly     |      1,114.00 |
    | **NEGmir~any_closer**                 |     57 |    0.60 |    2.09 |     138.45 |  2,032,082 |    293,963 |     77 |     11.14 |       45.86 | NEGMIR     | any_closer                 | closer         |      1,168.00 | any         |      1,514.00 |
    | **NEGmir~ever_likely**                |    103 |    0.46 |    2.00 |     192.81 |  2,032,082 |    293,963 |    169 |     24.45 |       78.55 | NEGMIR     | ever_likely                | likely         |     15,433.00 | ever        |      5,179.00 |
    | **NEGany~any_harder**                 |    227 |    0.15 |    1.98 |     395.22 | 86,330,752 |  3,226,213 |  1,221 |     45.63 |      181.37 | NEGATED    | any_harder                 | harder         |     99,332.00 | any         |     94,152.00 |
    | **NEGmir~that_serious**               |     50 |    0.59 |    1.93 |     120.37 |  2,032,082 |    293,963 |     68 |      9.84 |       40.16 | NEGMIR     | that_serious               | serious        |     10,801.00 | that        |      7,472.00 |
    | **NEGmir~immediately_available**      |    164 |    0.39 |    1.91 |     258.42 |  2,032,082 |    293,963 |    304 |     43.98 |      120.02 | NEGMIR     | immediately_available      | available      |     14,919.00 | immediately |      1,442.00 |
    | **NEGany~ever_able**                  |    234 |    0.13 |    1.81 |     363.95 | 86,330,752 |  3,226,213 |  1,398 |     52.24 |      181.76 | NEGATED    | ever_able                  | able           |    428,268.00 | ever        |    124,592.00 |
    | **NEGany~any_higher**                 |    301 |    0.12 |    1.77 |     434.16 | 86,330,752 |  3,226,213 |  1,921 |     71.79 |      229.21 | NEGATED    | any_higher                 | higher         |    271,250.00 | any         |     94,152.00 |
    | **NEGany~any_safer**                  |    235 |    0.12 |    1.73 |     346.68 | 86,330,752 |  3,226,213 |  1,471 |     54.97 |      180.03 | NEGATED    | any_safer                  | safer          |     26,779.00 | any         |     94,152.00 |
    | **COM~ever_more**                     |  6,763 |    0.03 |    1.72 |     331.84 | 86,330,752 | 83,102,035 |  6,792 |  6,537.98 |      225.02 | COMPLEMENT | ever_more                  | more           |  1,032,280.00 | ever        |    124,592.00 |
    | **COM~ever_present**                  |  7,602 |    0.03 |    1.70 |     354.47 | 86,330,752 | 83,102,035 |  7,639 |  7,353.31 |      248.69 | COMPLEMENT | ever_present               | present        |    127,265.00 | ever        |    124,592.00 |
    | **NEGmir~ever_available**             |     50 |    0.82 |    1.69 |     177.01 |  2,032,082 |    293,963 |     52 |      7.52 |       42.48 | NEGMIR     | ever_available             | available      |     14,919.00 | ever        |      5,179.00 |
    | **COM~ever_popular**                  |  4,485 |    0.04 |    1.67 |     283.43 | 86,330,752 | 83,102,035 |  4,492 |  4,324.00 |      161.00 | COMPLEMENT | ever_popular               | popular        |    828,951.00 | ever        |    124,592.00 |
    | **NEGmir~necessarily_true**           |     53 |    0.49 |    1.64 |     105.71 |  2,032,082 |    293,963 |     83 |     12.01 |       40.99 | NEGMIR     | necessarily_true           | true           |      8,402.00 | necessarily |      1,681.00 |
    | **NEGmir~remotely_similar**           |     71 |    0.43 |    1.62 |     123.23 |  2,032,082 |    293,963 |    123 |     17.79 |       53.21 | NEGMIR     | remotely_similar           | similar        |      7,887.00 | remotely    |      2,717.00 |
    | **NEGmir~remotely_interesting**       |     57 |    0.45 |    1.52 |     102.91 |  2,032,082 |    293,963 |     96 |     13.89 |       43.11 | NEGMIR     | remotely_interesting       | interesting    |     14,240.00 | remotely    |      2,717.00 |
    | **COM~ever_closer**                   |  6,880 |    0.04 |    1.52 |     501.08 | 86,330,752 | 83,102,035 |  6,882 |  6,624.62 |      255.38 | COMPLEMENT | ever_closer                | closer         |     70,294.00 | ever        |    124,592.00 |
    | **NEGmir~necessarily_bad**            |     50 |    0.47 |    1.48 |      93.65 |  2,032,082 |    293,963 |     82 |     11.86 |       38.14 | NEGMIR     | necessarily_bad            | bad            |     12,841.00 | necessarily |      1,681.00 |
    | **NEGmir~any_worse**                  |     88 |    0.36 |    1.45 |     127.07 |  2,032,082 |    293,963 |    173 |     25.03 |       62.97 | NEGMIR     | any_worse                  | worse          |     11,295.00 | any         |      1,514.00 |
    | **NEGmir~that_difficult**             |     52 |    0.36 |    1.08 |      74.23 |  2,032,082 |    293,963 |    103 |     14.90 |       37.10 | NEGMIR     | that_difficult             | difficult      |     18,107.00 | that        |      7,472.00 |
    



```python
NEG_bigrams_sample.l1.value_counts()
```




    l1
    NEGATED       67
    NEGMIR        36
    COMPLEMENT     4
    Name: count, dtype: Int64


