```python
import re
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR
from source.utils.associate import TOP_AM_DIR, adjust_assoc_columns
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import print_md_table, show_sample
from source.utils.general import (HIT_TABLES_DIR, confirm_dir, print_iter,
                                  timestamp_today)
from source.utils.sample import sample_pickle as sp

REFILTER_NEG = False
VERBOSE = True
K = 8
N_EX_PER_BIGRAM = 99
BIGRAM_F_FLOOR=50
ADV_F_FLOOR=5000

TAG='ALL'
METRIC_PRIORITY = ['LRC', 'P1', 'G2', 'P2'] if TAG=='NEQ' else ['dP1', 'LRC', 'G2', 'P1']
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
TAG_TOP_STR = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / TAG_TOP_STR
BK = max(K+2, 10)
DATE = timestamp_today()
FOCUS = adjust_assoc_columns(['f', 
                              'adv_total', 'adj_total',
                              'am_p1_given2', 
                              'am_p1_given2_simple', 
                              'conservative_log_ratio',
                              'am_log_likelihood',
                              'E11', 'unexpected_f',
                              #   't_score', 'mutual_information', 'am_odds_ratio_disc',
                              'N', 'f1', 'f2', 
                              'l1', 'l2', 
                              'adv', 'adj'
                              ])
FOCUS_MEANS = [f'mean_{c}' for c in FOCUS]
SET_FOCUS = [f'{c}_SET' for c in FOCUS]
MIR_FOCUS = [f'{c}_MIR' for c in FOCUS]
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 70)

NEG_HITS_PATH = HIT_TABLES_DIR /'RBdirect'/'ALL-RBdirect_final.parq'
```


```python
def nb_show_table(df, n_dec:int=2, 
                   adjust_columns:bool=True, 
                   outpath:Path=None,
                   suppress_printing:bool=not VERBOSE) -> None: 
    _df = df.copy()
    if adjust_columns: 
        _df = adjust_assoc_columns(_df)

    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index ]
    table = _df.convert_dtypes().to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')
    if outpath:
        outpath.write_text(table)
    if not suppress_printing:
        print(f'\n{table}\n')
    
def force_ints(_df):
    count_cols = _df.filter(regex=r'total|^[fN]').columns
    _df.loc[:, count_cols] = _df.loc[:, count_cols].astype('int')
    # _df[count_cols] = _df[:, count_cols].astype('int64')
    # print(_df.dtypes.to_frame('dtypes'))
    return _df

def embolden(series,
            bold_regex=None):
    bold_regex = bold_regex or r" (n[o']t) "
    return series.apply(
        lambda x: re.sub(bold_regex,
                        r' __`\1`__ ', x, flags=re.I))
adv_am = []
while not any(adv_am):
    try:
        adv_am = pd.read_csv(
            OUT_DIR / f'{TAG_TOP_STR}_NEG-ADV_combined-{ADV_F_FLOOR}.{DATE}.csv'
            ).set_index('adv')
    except FileNotFoundError:
        DATE = DATE[:-1]+str(int(DATE[-1])-1)
adv_am = adjust_assoc_columns(adv_am).convert_dtypes()
# nb_show_table(adv_am.filter(SET_FOCUS).filter(regex=r'^[^Nl]'))
```

```python
nb_show_table(adv_am.filter(SET_FOCUS).filter(regex=r'^[^Nl]'))
```

|                  |   `f_SET` |   `dP1_SET` |   `P1_SET` |   `LRC_SET` |   `G2_SET` |   `exp_f_SET` |   `unexp_f_SET` |   `f1_SET` |   `f2_SET` |
|:-----------------|----------:|------------:|-----------:|------------:|-----------:|--------------:|----------------:|-----------:|-----------:|
| **necessarily**  |    42,595 |        0.83 |       0.87 |        7.10 | 230,257.34 |      2,132.65 |       40,462.35 |  3,173,660 |     48,947 |
| **that**         |   164,768 |        0.75 |       0.79 |        6.34 | 831,137.25 |      9,074.09 |      155,693.91 |  3,173,660 |    208,262 |
| **exactly**      |    43,813 |        0.70 |       0.75 |        5.94 | 210,126.60 |      2,555.11 |       41,257.89 |  3,173,660 |     58,643 |
| **any**          |    15,384 |        0.40 |       0.45 |        4.07 |  50,880.96 |      1,498.04 |       13,885.96 |  3,173,660 |     34,382 |
| **remotely**     |     5,661 |        0.30 |       0.34 |        3.40 |  15,284.49 |        715.69 |        4,945.31 |  3,173,660 |     16,426 |
| **ever**         |     5,932 |        0.01 |       0.05 |        0.16 |     183.92 |      4,970.31 |          961.69 |  3,173,660 |    114,075 |
| **yet**          |    51,867 |        0.50 |       0.54 |        4.65 | 197,610.98 |      4,172.44 |       47,694.56 |  3,173,660 |     95,763 |
| **immediately**  |    56,099 |        0.54 |       0.58 |        4.86 | 224,059.55 |      4,225.17 |       51,873.83 |  3,173,660 |     96,973 |
| **particularly** |    55,527 |        0.07 |       0.11 |        1.38 |  37,272.74 |     22,380.79 |       33,146.21 |  3,173,660 |    513,668 |
| **inherently**   |     6,743 |        0.10 |       0.14 |        1.75 |   7,022.02 |      2,082.80 |        4,660.20 |  3,173,660 |     47,803 |
| **terribly**     |    17,949 |        0.26 |       0.30 |        3.19 |  43,741.44 |      2,569.09 |       15,379.91 |  3,173,660 |     58,964 |




```python
# nb_show_table(adv_am.filter(MIR_FOCUS).filter(regex=r'^[^Nl]'))
```

```python
nb_show_table(adv_am.filter(MIR_FOCUS).filter(regex=r'^[^Nl]'))
```

|                  |   `f_MIR` |   `dP1_MIR` |   `P1_MIR` |   `LRC_MIR` |   `G2_MIR` |   `exp_f_MIR` |   `unexp_f_MIR` |   `f1_MIR` |   `f2_MIR` |
|:-----------------|----------:|------------:|-----------:|------------:|-----------:|--------------:|----------------:|-----------:|-----------:|
| **necessarily**  |       963 |        0.70 |       0.87 |        4.39 |   2,597.68 |        189.75 |          773.25 |    291,732 |      1,107 |
| **that**         |     4,308 |        0.61 |       0.78 |        3.90 |   9,957.37 |        941.74 |        3,366.26 |    291,732 |      5,494 |
| **exactly**      |       813 |        0.61 |       0.78 |        3.57 |   1,860.72 |        178.44 |          634.56 |    291,732 |      1,041 |
| **any**          |     1,066 |        0.72 |       0.89 |        4.65 |   2,985.75 |        205.18 |          860.82 |    291,732 |      1,197 |
| **remotely**     |     1,840 |        0.62 |       0.79 |        3.79 |   4,256.34 |        401.28 |        1,438.72 |    291,732 |      2,341 |
| **ever**         |     4,709 |        0.76 |       0.93 |        5.63 |  14,253.57 |        867.35 |        3,841.65 |    291,732 |      5,060 |
| **yet**          |       320 |        0.22 |       0.39 |        1.11 |     223.08 |        139.70 |          180.30 |    291,732 |        815 |
| **immediately**  |       403 |        0.17 |       0.34 |        0.84 |     191.88 |        204.84 |          198.16 |    291,732 |      1,195 |
| **particularly** |     9,243 |        0.54 |       0.71 |        3.43 |  18,583.81 |      2,228.88 |        7,014.12 |    291,732 |     13,003 |
| **inherently**   |     2,864 |        0.39 |       0.56 |        2.40 |   3,925.31 |        879.86 |        1,984.14 |    291,732 |      5,133 |
| **terribly**     |     1,567 |        0.17 |       0.34 |        1.09 |     764.44 |        790.21 |          776.79 |    291,732 |      4,610 |




```python
# nb_show_table(adv_am.filter(items=FOCUS_MEANS).filter(regex=r'^[^Nl]'))
```

```python
nb_show_table(adv_am.filter(items=FOCUS_MEANS).filter(regex=r'^[^Nl]'))
```

|                  |   `mean_f` |   `mean_dP1` |   `mean_P1` |   `mean_LRC` |   `mean_G2` |   `mean_N` |   `mean_f1` |   `mean_f2` |
|:-----------------|-----------:|-------------:|------------:|-------------:|------------:|-----------:|------------:|------------:|
| **necessarily**  | 593,167.33 |         0.76 |        0.87 |         5.74 |  116,427.51 | 37,270,759 |   1,732,696 |   25,027.00 |
| **that**         | 641,370.67 |         0.68 |        0.79 |         5.12 |  420,547.31 | 37,270,759 |   1,732,696 |  106,878.00 |
| **exactly**      | 594,950.33 |         0.66 |        0.76 |         4.76 |  105,993.66 | 37,270,759 |   1,732,696 |   29,842.00 |
| **any**          | 586,236.83 |         0.56 |        0.67 |         4.36 |   26,933.36 | 37,270,759 |   1,732,696 |   17,789.50 |
| **remotely**     | 581,943.33 |         0.46 |        0.57 |         3.59 |    9,770.42 | 37,270,759 |   1,732,696 |    9,383.50 |
| **ever**         | 599,194.67 |         0.39 |        0.49 |         2.90 |    7,218.74 | 37,270,759 |   1,732,696 |   59,567.50 |
| **yet**          | 602,359.50 |         0.36 |        0.47 |         2.88 |   98,917.03 | 37,270,759 |   1,732,696 |   48,289.00 |
| **immediately**  | 603,343.67 |         0.35 |        0.46 |         2.85 |  112,125.71 | 37,270,759 |   1,732,696 |   49,084.00 |
| **particularly** | 676,138.83 |         0.30 |        0.41 |         2.40 |   27,928.28 | 37,270,759 |   1,732,696 |  263,335.50 |
| **inherently**   | 587,989.17 |         0.24 |        0.35 |         2.07 |    5,473.66 | 37,270,759 |   1,732,696 |   26,468.00 |
| **terribly**     | 591,413.67 |         0.21 |        0.32 |         2.14 |   22,252.94 | 37,270,759 |   1,732,696 |   31,787.00 |



```python
def compare_datasets(adv_am, 
                     metric_selection:str or list = 'dP1', 
                     k=5):
    if isinstance(metric_selection, str): 
        met_adv_am = adv_am.filter(like=metric_selection)
    else:
        met_adv_am = adv_am.filter(regex=r'|'.join([f'^{m}|mean_{m}' for m in metric_selection]))
    if met_adv_am.empty: 
        met_adv_am = adjust_assoc_columns(adv_am).filter(metric_selection)
    if any(met_adv_am.columns.str.startswith('r_')):
        is_ratio = met_adv_am.columns.str.startswith('r_')
        met_adv_am.loc[:, is_ratio] = met_adv_am.loc[:, is_ratio] * 100
        met_adv_am.columns = met_adv_am.columns.str.replace('r_', '%_')
    for col in met_adv_am.columns:
        n_dec = 2
        if 'P' in col:
            n_dec = 3
        elif 'G' in col or '%' in col:
            n_dec = 1
        elif 'f' in col and not col.startswith(('r_', '%_', 'mean_')): 
            n_dec = 0
            # col = col.replace('r_', '%_')
        print(f'Top {k} by descending `{col}`')
        print(met_adv_am.nlargest(k, col).to_markdown(
            floatfmt=f',.{n_dec}f', intfmt=','), '\n')

```


```python
# compare_datasets(adv_am, METRIC_PRIORITY[0])
```

```py
compare_datasets(adv_am, METRIC_PRIORITY[0])
```

Top 5 by descending `dP1_SET`
| adv         |   dP1_SET |   dP1_MIR |   mean_dP1 |
|:------------|----------:|----------:|-----------:|
| necessarily |     0.827 |     0.699 |      0.763 |
| that        |     0.750 |     0.615 |      0.682 |
| exactly     |     0.704 |     0.610 |      0.657 |
| immediately |     0.536 |     0.166 |      0.351 |
| yet         |     0.499 |     0.221 |      0.360 | 

Top 5 by descending `dP1_MIR`
| adv         |   dP1_SET |   dP1_MIR |   mean_dP1 |
|:------------|----------:|----------:|-----------:|
| ever        |     0.008 |     0.761 |      0.385 |
| any         |     0.404 |     0.720 |      0.562 |
| necessarily |     0.827 |     0.699 |      0.763 |
| remotely    |     0.301 |     0.615 |      0.458 |
| that        |     0.750 |     0.615 |      0.682 | 

Top 5 by descending `mean_dP1`
| adv         |   dP1_SET |   dP1_MIR |   mean_dP1 |
|:------------|----------:|----------:|-----------:|
| necessarily |     0.827 |     0.699 |      0.763 |
| that        |     0.750 |     0.615 |      0.682 |
| exactly     |     0.704 |     0.610 |      0.657 |
| any         |     0.404 |     0.720 |      0.562 |
| remotely    |     0.301 |     0.615 |      0.458 | 




```python
# compare_datasets(adv_am, METRIC_PRIORITY[1])
```

```py
compare_datasets(adv_am, METRIC_PRIORITY[1])
```

Top 5 by descending `LRC_SET`
| adv         |   LRC_SET |   LRC_MIR |   mean_LRC |
|:------------|----------:|----------:|-----------:|
| necessarily |      7.10 |      4.39 |       5.74 |
| that        |      6.34 |      3.90 |       5.12 |
| exactly     |      5.94 |      3.57 |       4.76 |
| immediately |      4.86 |      0.84 |       2.85 |
| yet         |      4.65 |      1.11 |       2.88 | 

Top 5 by descending `LRC_MIR`
| adv         |   LRC_SET |   LRC_MIR |   mean_LRC |
|:------------|----------:|----------:|-----------:|
| ever        |      0.16 |      5.63 |       2.90 |
| any         |      4.07 |      4.65 |       4.36 |
| necessarily |      7.10 |      4.39 |       5.74 |
| that        |      6.34 |      3.90 |       5.12 |
| remotely    |      3.40 |      3.79 |       3.59 | 

Top 5 by descending `mean_LRC`
| adv         |   LRC_SET |   LRC_MIR |   mean_LRC |
|:------------|----------:|----------:|-----------:|
| necessarily |      7.10 |      4.39 |       5.74 |
| that        |      6.34 |      3.90 |       5.12 |
| exactly     |      5.94 |      3.57 |       4.76 |
| any         |      4.07 |      4.65 |       4.36 |
| remotely    |      3.40 |      3.79 |       3.59 | 




```python
# compare_datasets(adv_am, METRIC_PRIORITY[2])
```

```python
compare_datasets(adv_am, METRIC_PRIORITY[2])
```
Top 5 by descending `G2_SET`
| adv         |    G2_SET |   G2_MIR |   mean_G2 |
|:------------|----------:|---------:|----------:|
| that        | 831,137.3 |  9,957.4 | 420,547.3 |
| necessarily | 230,257.3 |  2,597.7 | 116,427.5 |
| immediately | 224,059.5 |    191.9 | 112,125.7 |
| exactly     | 210,126.6 |  1,860.7 | 105,993.7 |
| yet         | 197,611.0 |    223.1 |  98,917.0 | 

Top 5 by descending `G2_MIR`
| adv          |    G2_SET |   G2_MIR |   mean_G2 |
|:-------------|----------:|---------:|----------:|
| particularly |  37,272.7 | 18,583.8 |  27,928.3 |
| ever         |     183.9 | 14,253.6 |   7,218.7 |
| that         | 831,137.3 |  9,957.4 | 420,547.3 |
| remotely     |  15,284.5 |  4,256.3 |   9,770.4 |
| inherently   |   7,022.0 |  3,925.3 |   5,473.7 | 

Top 5 by descending `mean_G2`
| adv         |    G2_SET |   G2_MIR |   mean_G2 |
|:------------|----------:|---------:|----------:|
| that        | 831,137.3 |  9,957.4 | 420,547.3 |
| necessarily | 230,257.3 |  2,597.7 | 116,427.5 |
| immediately | 224,059.5 |    191.9 | 112,125.7 |
| exactly     | 210,126.6 |  1,860.7 | 105,993.7 |
| yet         | 197,611.0 |    223.1 |  98,917.0 | 




```python
# compare_datasets(adv_am, 'f_')
```

```python
compare_datasets(adv_am, 'f_')
```
Top 5 by descending `f_SET`
| adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| that         | 164,768 |       9,074 |       155,694 |   4,308 |         942 |         3,366 |         3 |
| immediately  |  56,099 |       4,225 |        51,874 |     403 |         205 |           198 |         1 |
| particularly |  55,527 |      22,381 |        33,146 |   9,243 |       2,229 |         7,014 |        17 |
| yet          |  51,867 |       4,172 |        47,695 |     320 |         140 |           180 |         1 |
| exactly      |  43,813 |       2,555 |        41,258 |     813 |         178 |           635 |         2 | 

Top 5 by descending `exp_f_SET`
| adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| particularly |  55,527 |      22,381 |        33,146 |   9,243 |       2,229 |         7,014 |        17 |
| that         | 164,768 |       9,074 |       155,694 |   4,308 |         942 |         3,366 |         3 |
| ever         |   5,932 |       4,970 |           962 |   4,709 |         867 |         3,842 |        79 |
| immediately  |  56,099 |       4,225 |        51,874 |     403 |         205 |           198 |         1 |
| yet          |  51,867 |       4,172 |        47,695 |     320 |         140 |           180 |         1 | 

Top 5 by descending `unexp_f_SET`
| adv         |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| that        | 164,768 |       9,074 |       155,694 |   4,308 |         942 |         3,366 |         3 |
| immediately |  56,099 |       4,225 |        51,874 |     403 |         205 |           198 |         1 |
| yet         |  51,867 |       4,172 |        47,695 |     320 |         140 |           180 |         1 |
| exactly     |  43,813 |       2,555 |        41,258 |     813 |         178 |           635 |         2 |
| necessarily |  42,595 |       2,133 |        40,462 |     963 |         190 |           773 |         2 | 

Top 5 by descending `f_MIR`
| adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| particularly |  55,527 |      22,381 |        33,146 |   9,243 |       2,229 |         7,014 |        17 |
| ever         |   5,932 |       4,970 |           962 |   4,709 |         867 |         3,842 |        79 |
| that         | 164,768 |       9,074 |       155,694 |   4,308 |         942 |         3,366 |         3 |
| inherently   |   6,743 |       2,083 |         4,660 |   2,864 |         880 |         1,984 |        42 |
| remotely     |   5,661 |         716 |         4,945 |   1,840 |         401 |         1,439 |        32 | 

Top 5 by descending `exp_f_MIR`
| adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| particularly |  55,527 |      22,381 |        33,146 |   9,243 |       2,229 |         7,014 |        17 |
| that         | 164,768 |       9,074 |       155,694 |   4,308 |         942 |         3,366 |         3 |
| inherently   |   6,743 |       2,083 |         4,660 |   2,864 |         880 |         1,984 |        42 |
| ever         |   5,932 |       4,970 |           962 |   4,709 |         867 |         3,842 |        79 |
| terribly     |  17,949 |       2,569 |        15,380 |   1,567 |         790 |           777 |         9 | 

Top 5 by descending `unexp_f_MIR`
| adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| particularly |  55,527 |      22,381 |        33,146 |   9,243 |       2,229 |         7,014 |        17 |
| ever         |   5,932 |       4,970 |           962 |   4,709 |         867 |         3,842 |        79 |
| that         | 164,768 |       9,074 |       155,694 |   4,308 |         942 |         3,366 |         3 |
| inherently   |   6,743 |       2,083 |         4,660 |   2,864 |         880 |         1,984 |        42 |
| remotely     |   5,661 |         716 |         4,945 |   1,840 |         401 |         1,439 |        32 | 

Top 5 by descending `%_f_MIR`
| adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
|:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
| ever         |   5,932 |     4,970.3 |         961.7 |   4,709 |       867.3 |       3,841.7 |      79.4 |
| inherently   |   6,743 |     2,082.8 |       4,660.2 |   2,864 |       879.9 |       1,984.1 |      42.5 |
| remotely     |   5,661 |       715.7 |       4,945.3 |   1,840 |       401.3 |       1,438.7 |      32.5 |
| particularly |  55,527 |    22,380.8 |      33,146.2 |   9,243 |     2,228.9 |       7,014.1 |      16.7 |
| terribly     |  17,949 |     2,569.1 |      15,379.9 |   1,567 |       790.2 |         776.8 |       8.7 | 




```python
# compare_datasets(adv_am, 'f2')
```

```python
compare_datasets(adv_am, 'f2')
```
Top 5 by descending `f2_SET`
| adv          |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
|:-------------|---------:|---------:|----------:|-----------:|
| particularly |  513,668 |   13,003 |   263,336 |          3 |
| that         |  208,262 |    5,494 |   106,878 |          3 |
| ever         |  114,075 |    5,060 |    59,568 |          4 |
| immediately  |   96,973 |    1,195 |    49,084 |          1 |
| yet          |   95,763 |      815 |    48,289 |          1 | 

Top 5 by descending `f2_MIR`
| adv          |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
|:-------------|---------:|---------:|----------:|-----------:|
| particularly |  513,668 |   13,003 |   263,336 |          3 |
| that         |  208,262 |    5,494 |   106,878 |          3 |
| inherently   |   47,803 |    5,133 |    26,468 |         11 |
| ever         |  114,075 |    5,060 |    59,568 |          4 |
| terribly     |   58,964 |    4,610 |    31,787 |          8 | 

Top 5 by descending `mean_f2`
| adv          |   f2_SET |   f2_MIR |    mean_f2 |   %_f2_MIR |
|:-------------|---------:|---------:|-----------:|-----------:|
| particularly |  513,668 |   13,003 | 263,335.50 |       2.53 |
| that         |  208,262 |    5,494 | 106,878.00 |       2.64 |
| ever         |  114,075 |    5,060 |  59,567.50 |       4.44 |
| immediately  |   96,973 |    1,195 |  49,084.00 |       1.23 |
| yet          |   95,763 |      815 |  48,289.00 |       0.85 | 

Top 5 by descending `%_f2_MIR`
| adv        |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
|:-----------|---------:|---------:|----------:|-----------:|
| remotely   |   16,426 |    2,341 |   9,383.5 |       14.2 |
| inherently |   47,803 |    5,133 |  26,468.0 |       10.7 |
| terribly   |   58,964 |    4,610 |  31,787.0 |        7.8 |
| ever       |  114,075 |    5,060 |  59,567.5 |        4.4 |
| any        |   34,382 |    1,197 |  17,789.5 |        3.5 | 




```python
def pin_top_adv(adv_am,
                select_col='mean_dP1',
                verbose: bool = VERBOSE):

    sorted_adv_am = adv_am.sort_values(select_col, ascending=False)
    top = sorted_adv_am.index.to_series()
    if verbose:
        print_df = sorted_adv_am[select_col].reset_index()
        print_df.index = print_df.index.to_series().add(1)
        print(
            f'Top Adverb Selection, ranked by descending `{repr(select_col)}`',
            print_df.to_markdown(floatfmt=',.3f'),
            sep='\n\n', end='\n\n'
        )
    return top.to_list(), sorted_adv_am


```


```python

# TOP_ADV, adv_am = pin_top_adv(adv_am, select_col=f'mean_{METRIC_PRIORITY[0]}')
```

```python
TOP_ADV, adv_am = pin_top_adv(adv_am, select_col=f'mean_{METRIC_PRIORITY[0]}')
```
Top Adverb Selection, ranked by descending `'mean_dP1'`

|    | adv          |   mean_dP1 |
|---:|:-------------|-----------:|
|  1 | necessarily  |      0.763 |
|  2 | that         |      0.682 |
|  3 | exactly      |      0.657 |
|  4 | any          |      0.562 |
|  5 | remotely     |      0.458 |
|  6 | ever         |      0.385 |
|  7 | yet          |      0.360 |
|  8 | immediately  |      0.351 |
|  9 | particularly |      0.304 |
| 10 | inherently   |      0.243 |
| 11 | terribly     |      0.215 |




```python
# __ = pin_top_adv(adv_am, select_col=[f'mean_{m}' for m in METRIC_PRIORITY])
```

```python
__ = pin_top_adv(adv_am, select_col=[f'mean_{m}' for m in METRIC_PRIORITY])
```
Top Adverb Selection, ranked by descending `['mean_dP1', 'mean_LRC', 'mean_G2', 'mean_P1']`

|    | adv          |   mean_dP1 |   mean_LRC |     mean_G2 |   mean_P1 |
|---:|:-------------|-----------:|-----------:|------------:|----------:|
|  1 | necessarily  |      0.763 |      5.743 | 116,427.511 |     0.870 |
|  2 | that         |      0.682 |      5.117 | 420,547.310 |     0.788 |
|  3 | exactly      |      0.657 |      4.759 | 105,993.662 |     0.764 |
|  4 | any          |      0.562 |      4.360 |  26,933.357 |     0.669 |
|  5 | remotely     |      0.458 |      3.594 |   9,770.416 |     0.565 |
|  6 | ever         |      0.385 |      2.895 |   7,218.745 |     0.491 |
|  7 | yet          |      0.360 |      2.877 |  98,917.030 |     0.467 |
|  8 | immediately  |      0.351 |      2.852 | 112,125.713 |     0.458 |
|  9 | particularly |      0.304 |      2.403 |  27,928.276 |     0.409 |
| 10 | inherently   |      0.243 |      2.075 |   5,473.662 |     0.349 |
| 11 | terribly     |      0.215 |      2.140 |  22,252.939 |     0.322 |




```python
bigram_am = adjust_assoc_columns(pd.read_csv(OUT_DIR / f'{TAG_TOP_STR}_NEG-ADV_top-{BK}-bigrams-{BIGRAM_F_FLOOR}.{DATE}.csv')
             .set_index('key')
             #> not strictly necessary (loaded table should already satisfy this) but just in case...
             .filter(regex=r'|'.join([f'~{a}_' for a in TOP_ADV]), axis=0)
             ).filter(items=FOCUS).convert_dtypes()
bigram_am.sort_values(METRIC_PRIORITY, ascending=False)
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
      <th>f</th>
      <th>adv_total</th>
      <th>adj_total</th>
      <th>dP1</th>
      <th>P1</th>
      <th>LRC</th>
      <th>G2</th>
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>l1</th>
      <th>l2</th>
      <th>adv</th>
      <th>adj</th>
    </tr>
    <tr>
      <th>key</th>
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
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>NEGany~yet_eligible</th>
      <td>448</td>
      <td>95763</td>
      <td>23252</td>
      <td>0.96</td>
      <td>1.00</td>
      <td>8.96</td>
      <td>2,807.56</td>
      <td>19.52</td>
      <td>428.48</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>448</td>
      <td>NEGATED</td>
      <td>yet_eligible</td>
      <td>yet</td>
      <td>eligible</td>
    </tr>
    <tr>
      <th>NEGany~yet_official</th>
      <td>352</td>
      <td>95763</td>
      <td>6853</td>
      <td>0.96</td>
      <td>1.00</td>
      <td>8.61</td>
      <td>2,205.93</td>
      <td>15.34</td>
      <td>336.66</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>352</td>
      <td>NEGATED</td>
      <td>yet_official</td>
      <td>yet</td>
      <td>official</td>
    </tr>
    <tr>
      <th>NEGany~exactly_conducive</th>
      <td>208</td>
      <td>58643</td>
      <td>9110</td>
      <td>0.96</td>
      <td>1.00</td>
      <td>7.82</td>
      <td>1,303.50</td>
      <td>9.06</td>
      <td>198.94</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>208</td>
      <td>NEGATED</td>
      <td>exactly_conducive</td>
      <td>exactly</td>
      <td>conducive</td>
    </tr>
    <tr>
      <th>NEGany~yet_convinced</th>
      <td>169</td>
      <td>95763</td>
      <td>12132</td>
      <td>0.96</td>
      <td>1.00</td>
      <td>7.50</td>
      <td>1,059.09</td>
      <td>7.36</td>
      <td>161.64</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>169</td>
      <td>NEGATED</td>
      <td>yet_convinced</td>
      <td>yet</td>
      <td>convinced</td>
    </tr>
    <tr>
      <th>NEGany~exactly_shocking</th>
      <td>151</td>
      <td>58643</td>
      <td>35115</td>
      <td>0.96</td>
      <td>1.00</td>
      <td>7.33</td>
      <td>946.29</td>
      <td>6.58</td>
      <td>144.42</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>151</td>
      <td>NEGATED</td>
      <td>exactly_shocking</td>
      <td>exactly</td>
      <td>shocking</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>NEGany~remotely_interested</th>
      <td>330</td>
      <td>16426</td>
      <td>264528</td>
      <td>0.27</td>
      <td>0.31</td>
      <td>2.74</td>
      <td>817.06</td>
      <td>46.27</td>
      <td>283.73</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>1062</td>
      <td>NEGATED</td>
      <td>remotely_interested</td>
      <td>remotely</td>
      <td>interested</td>
    </tr>
    <tr>
      <th>NEGany~remotely_similar</th>
      <td>152</td>
      <td>16426</td>
      <td>203453</td>
      <td>0.23</td>
      <td>0.27</td>
      <td>2.20</td>
      <td>334.61</td>
      <td>24.36</td>
      <td>127.64</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>559</td>
      <td>NEGATED</td>
      <td>remotely_similar</td>
      <td>remotely</td>
      <td>similar</td>
    </tr>
    <tr>
      <th>NEGany~inherently_good</th>
      <td>283</td>
      <td>47803</td>
      <td>1681795</td>
      <td>0.20</td>
      <td>0.24</td>
      <td>2.21</td>
      <td>554.72</td>
      <td>51.28</td>
      <td>231.72</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>1177</td>
      <td>NEGATED</td>
      <td>inherently_good</td>
      <td>inherently</td>
      <td>good</td>
    </tr>
    <tr>
      <th>NEGany~inherently_problematic</th>
      <td>58</td>
      <td>47803</td>
      <td>33408</td>
      <td>0.17</td>
      <td>0.21</td>
      <td>1.17</td>
      <td>98.70</td>
      <td>12.07</td>
      <td>45.93</td>
      <td>72839589</td>
      <td>3173660</td>
      <td>277</td>
      <td>NEGATED</td>
      <td>inherently_problematic</td>
      <td>inherently</td>
      <td>problematic</td>
    </tr>
    <tr>
      <th>COM~ever_closer</th>
      <td>6305</td>
      <td>114075</td>
      <td>61475</td>
      <td>0.04</td>
      <td>1.00</td>
      <td>3.51</td>
      <td>538.66</td>
      <td>6,031.92</td>
      <td>273.08</td>
      <td>72839589</td>
      <td>69662736</td>
      <td>6307</td>
      <td>COMPLEMENT</td>
      <td>ever_closer</td>
      <td>ever</td>
      <td>closer</td>
    </tr>
  </tbody>
</table>
<p>191 rows × 16 columns</p>
</div>




```python
overall_k = int(BK/2 * K)
nb_show_table(bigram_am.round(2).nlargest(overall_k, columns=METRIC_PRIORITY),
            outpath=OUT_DIR / f'{TAG}-Top{K}_NEG-ADV-{ADV_F_FLOOR}_top{overall_k}bigrams-overall.min{BIGRAM_F_FLOOR}.{timestamp_today()}.md', 
            suppress_printing=not VERBOSE)
```

    
    |                                       |    `f` |   `adv_total` |   `adj_total` |   `dP1` |   `P1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |        `N` |      `f1` |   `f2` | `l1`    | `l2`                       | `adv`       | `adj`          |
    |:--------------------------------------|-------:|--------------:|--------------:|--------:|-------:|--------:|----------:|----------:|------------:|-----------:|----------:|-------:|:--------|:---------------------------|:------------|:---------------|
    | **NEGany~yet_eligible**               |    448 |        95,763 |        23,252 |    0.96 |   1.00 |    8.96 |  2,807.56 |     19.52 |      428.48 | 72,839,589 | 3,173,660 |    448 | NEGATED | yet_eligible               | yet         | eligible       |
    | **NEGany~yet_official**               |    352 |        95,763 |         6,853 |    0.96 |   1.00 |    8.61 |  2,205.93 |     15.34 |      336.66 | 72,839,589 | 3,173,660 |    352 | NEGATED | yet_official               | yet         | official       |
    | **NEGany~exactly_conducive**          |    208 |        58,643 |         9,110 |    0.96 |   1.00 |    7.82 |  1,303.50 |      9.06 |      198.94 | 72,839,589 | 3,173,660 |    208 | NEGATED | exactly_conducive          | exactly     | conducive      |
    | **NEGany~yet_convinced**              |    169 |        95,763 |        12,132 |    0.96 |   1.00 |    7.50 |  1,059.09 |      7.36 |      161.64 | 72,839,589 | 3,173,660 |    169 | NEGATED | yet_convinced              | yet         | convinced      |
    | **NEGany~exactly_shocking**           |    151 |        58,643 |        35,115 |    0.96 |   1.00 |    7.33 |    946.29 |      6.58 |      144.42 | 72,839,589 | 3,173,660 |    151 | NEGATED | exactly_shocking           | exactly     | shocking       |
    | **NEGany~exactly_pleasant**           |    142 |        58,643 |        52,223 |    0.96 |   1.00 |    7.24 |    889.88 |      6.19 |      135.81 | 72,839,589 | 3,173,660 |    142 | NEGATED | exactly_pleasant           | exactly     | pleasant       |
    | **NEGany~exactly_famous**             |    130 |        58,643 |       223,813 |    0.96 |   1.00 |    7.10 |    814.68 |      5.66 |      124.34 | 72,839,589 | 3,173,660 |    130 | NEGATED | exactly_famous             | exactly     | famous         |
    | **NEGany~exactly_difficult**          |    126 |        58,643 |       732,106 |    0.96 |   1.00 |    7.05 |    789.62 |      5.49 |      120.51 | 72,839,589 | 3,173,660 |    126 | NEGATED | exactly_difficult          | exactly     | difficult      |
    | **NEGany~necessarily_useful**         |    104 |        48,947 |       227,709 |    0.96 |   1.00 |    6.75 |    651.75 |      4.53 |       99.47 | 72,839,589 | 3,173,660 |    104 | NEGATED | necessarily_useful         | necessarily | useful         |
    | **NEGany~yet_online**                 |     98 |        95,763 |        15,650 |    0.96 |   1.00 |    6.66 |    614.14 |      4.27 |       93.73 | 72,839,589 | 3,173,660 |     98 | NEGATED | yet_online                 | yet         | online         |
    | **NEGany~necessarily_fun**            |     96 |        48,947 |       190,026 |    0.96 |   1.00 |    6.62 |    601.61 |      4.18 |       91.82 | 72,839,589 | 3,173,660 |     96 | NEGATED | necessarily_fun            | necessarily | fun            |
    | **NEGany~necessarily_essential**      |     93 |        48,947 |        69,845 |    0.96 |   1.00 |    6.57 |    582.81 |      4.05 |       88.95 | 72,839,589 | 3,173,660 |     93 | NEGATED | necessarily_essential      | necessarily | essential      |
    | **NEGany~necessarily_reliable**       |     81 |        48,947 |        90,598 |    0.96 |   1.00 |    6.35 |    507.61 |      3.53 |       77.47 | 72,839,589 | 3,173,660 |     81 | NEGATED | necessarily_reliable       | necessarily | reliable       |
    | **NEGany~necessarily_proud**          |     71 |        48,947 |       207,536 |    0.96 |   1.00 |    6.14 |    444.94 |      3.09 |       67.91 | 72,839,589 | 3,173,660 |     71 | NEGATED | necessarily_proud          | necessarily | proud          |
    | **NEGany~yet_mainstream**             |     70 |        95,763 |        17,792 |    0.96 |   1.00 |    6.11 |    438.67 |      3.05 |       66.95 | 72,839,589 | 3,173,660 |     70 | NEGATED | yet_mainstream             | yet         | mainstream     |
    | **NEGany~that_far-fetched**           |     59 |       208,262 |         5,185 |    0.96 |   1.00 |    5.83 |    369.74 |      2.57 |       56.43 | 72,839,589 | 3,173,660 |     59 | NEGATED | that_far-fetched           | that        | far-fetched    |
    | **NEGany~that_thrilled**              |     59 |       208,262 |        24,182 |    0.96 |   1.00 |    5.83 |    369.74 |      2.57 |       56.43 | 72,839,589 | 3,173,660 |     59 | NEGATED | that_thrilled              | that        | thrilled       |
    | **NEGany~yet_clear**                  | 10,406 |        95,763 |       349,214 |    0.95 |   0.99 |   10.77 | 64,409.97 |    456.44 |    9,949.56 | 72,839,589 | 3,173,660 | 10,476 | NEGATED | yet_clear                  | yet         | clear          |
    | **NEGany~necessarily_indicative**     |  1,389 |        48,947 |         8,148 |    0.95 |   0.99 |    9.43 |  8,577.54 |     61.00 |    1,328.00 | 72,839,589 | 3,173,660 |  1,400 | NEGATED | necessarily_indicative     | necessarily | indicative     |
    | **NEGany~that_uncommon**              |    802 |       208,262 |        11,312 |    0.95 |   1.00 |    9.43 |  4,998.32 |     35.03 |      766.97 | 72,839,589 | 3,173,660 |    804 | NEGATED | that_uncommon              | that        | uncommon       |
    | **NEGany~exactly_easy**               |  1,066 |        58,643 |       579,827 |    0.95 |   0.99 |    9.32 |  6,596.91 |     46.75 |    1,019.25 | 72,839,589 | 3,173,660 |  1,073 | NEGATED | exactly_easy               | exactly     | easy           |
    | **NEGany~that_surprising**            |  1,133 |       208,262 |        70,540 |    0.95 |   0.99 |    9.20 |  6,986.81 |     49.80 |    1,083.20 | 72,839,589 | 3,173,660 |  1,143 | NEGATED | that_surprising            | that        | surprising     |
    | **NEGany~necessarily_easy**           |    909 |        48,947 |       579,827 |    0.95 |   0.99 |    9.01 |  5,605.64 |     39.95 |      869.05 | 72,839,589 | 3,173,660 |    917 | NEGATED | necessarily_easy           | necessarily | easy           |
    | **NEGany~yet_final**                  |    640 |        95,763 |         5,860 |    0.95 |   1.00 |    8.97 |  3,972.92 |     28.02 |      611.98 | 72,839,589 | 3,173,660 |    643 | NEGATED | yet_final                  | yet         | final          |
    | **NEGany~exactly_cheap**              |    691 |        58,643 |        60,531 |    0.95 |   0.99 |    8.96 |  4,281.59 |     30.28 |      660.72 | 72,839,589 | 3,173,660 |    695 | NEGATED | exactly_cheap              | exactly     | cheap          |
    | **NEGany~that_unusual**               |    977 |       208,262 |        71,234 |    0.95 |   0.99 |    8.92 |  6,003.05 |     43.05 |      933.95 | 72,839,589 | 3,173,660 |    988 | NEGATED | that_unusual               | that        | unusual        |
    | **NEGany~exactly_surprising**         |    440 |        58,643 |        70,540 |    0.95 |   1.00 |    8.71 |  2,743.34 |     19.21 |      420.79 | 72,839,589 | 3,173,660 |    441 | NEGATED | exactly_surprising         | exactly     | surprising     |
    | **NEGany~necessarily_representative** |    487 |        48,947 |        18,355 |    0.95 |   0.99 |    8.34 |  2,996.58 |     21.44 |      465.56 | 72,839,589 | 3,173,660 |    492 | NEGATED | necessarily_representative | necessarily | representative |
    | **NEGany~necessarily_surprising**     |    340 |        48,947 |        70,540 |    0.95 |   1.00 |    8.33 |  2,117.16 |     14.86 |      325.14 | 72,839,589 | 3,173,660 |    341 | NEGATED | necessarily_surprising     | necessarily | surprising     |
    | **NEGany~that_dissimilar**            |    304 |       208,262 |         4,605 |    0.95 |   0.99 |    7.86 |  1,871.65 |     13.38 |      290.62 | 72,839,589 | 3,173,660 |    307 | NEGATED | that_dissimilar            | that        | dissimilar     |
    | **NEGany~that_noticeable**            |    264 |       208,262 |        31,467 |    0.95 |   0.99 |    7.65 |  1,621.81 |     11.63 |      252.37 | 72,839,589 | 3,173,660 |    267 | NEGATED | that_noticeable            | that        | noticeable     |
    | **NEGany~yet_over**                   |    162 |        95,763 |         3,983 |    0.95 |   0.99 |    7.21 |  1,003.13 |      7.10 |      154.90 | 72,839,589 | 3,173,660 |    163 | NEGATED | yet_over                   | yet         | over           |
    | **NEGany~yet_ready**                  |  7,501 |        95,763 |       141,590 |    0.94 |   0.99 |    9.93 | 45,985.07 |    331.09 |    7,169.91 | 72,839,589 | 3,173,660 |  7,599 | NEGATED | yet_ready                  | yet         | ready          |
    | **NEGany~yet_complete**               |  2,174 |        95,763 |        86,361 |    0.94 |   0.98 |    9.20 | 13,277.09 |     96.20 |    2,077.80 | 72,839,589 | 3,173,660 |  2,208 | NEGATED | yet_complete               | yet         | complete       |
    | **NEGany~exactly_new**                |  1,371 |        58,643 |       253,862 |    0.94 |   0.99 |    9.10 |  8,410.32 |     60.48 |    1,310.52 | 72,839,589 | 3,173,660 |  1,388 | NEGATED | exactly_new                | exactly     | new            |
    | **NEGany~exactly_clear**              |  1,746 |        58,643 |       349,214 |    0.94 |   0.98 |    8.78 | 10,578.33 |     77.73 |    1,668.27 | 72,839,589 | 3,173,660 |  1,784 | NEGATED | exactly_clear              | exactly     | clear          |
    | **NEGany~that_complicated**           |  1,207 |       208,262 |       159,822 |    0.94 |   0.98 |    8.68 |  7,337.84 |     53.59 |    1,153.41 | 72,839,589 | 3,173,660 |  1,230 | NEGATED | that_complicated           | that        | complicated    |
    | **NEGany~terribly_surprising**        |    949 |        58,964 |        70,540 |    0.94 |   0.98 |    8.66 |  5,794.10 |     42.00 |      907.00 | 72,839,589 | 3,173,660 |    964 | NEGATED | terribly_surprising        | terribly    | surprising     |
    | **NEGany~necessarily_new**            |    482 |        48,947 |       253,862 |    0.94 |   0.98 |    7.94 |  2,923.82 |     21.44 |      460.56 | 72,839,589 | 3,173,660 |    492 | NEGATED | necessarily_new            | necessarily | new            |
    | **NEGany~terribly_uncommon**          |    103 |        58,964 |        11,312 |    0.94 |   0.98 |    6.33 |    625.85 |      4.57 |       98.43 | 72,839,589 | 3,173,660 |    105 | NEGATED | terribly_uncommon          | terribly    | uncommon       |
    


```python
overall_k = int(BK/2 * K)
nb_show_table(bigram_am.round(2).nlargest(overall_k, columns=METRIC_PRIORITY),
            outpath=OUT_DIR / f'{TAG}-Top{K}_NEG-ADV-{ADV_F_FLOOR}_top{overall_k}bigrams-overall.min{BIGRAM_F_FLOOR}.md', 
            suppress_printing=not VERBOSE)
```

|                                       |    `f` |   `adv_total` |   `adj_total` |   `dP1` |   `P1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |        `N` |      `f1` |   `f2` | `l1`    | `l2`                       | `adv`       | `adj`          |
|:--------------------------------------|-------:|--------------:|--------------:|--------:|-------:|--------:|----------:|----------:|------------:|-----------:|----------:|-------:|:--------|:---------------------------|:------------|:---------------|
| **NEGany~yet_eligible**               |    448 |        95,763 |        23,252 |    0.96 |   1.00 |    8.96 |  2,807.56 |     19.52 |      428.48 | 72,839,589 | 3,173,660 |    448 | NEGATED | yet_eligible               | yet         | eligible       |
| **NEGany~yet_official**               |    352 |        95,763 |         6,853 |    0.96 |   1.00 |    8.61 |  2,205.93 |     15.34 |      336.66 | 72,839,589 | 3,173,660 |    352 | NEGATED | yet_official               | yet         | official       |
| **NEGany~exactly_conducive**          |    208 |        58,643 |         9,110 |    0.96 |   1.00 |    7.82 |  1,303.50 |      9.06 |      198.94 | 72,839,589 | 3,173,660 |    208 | NEGATED | exactly_conducive          | exactly     | conducive      |
| **NEGany~yet_convinced**              |    169 |        95,763 |        12,132 |    0.96 |   1.00 |    7.50 |  1,059.09 |      7.36 |      161.64 | 72,839,589 | 3,173,660 |    169 | NEGATED | yet_convinced              | yet         | convinced      |
| **NEGany~exactly_shocking**           |    151 |        58,643 |        35,115 |    0.96 |   1.00 |    7.33 |    946.29 |      6.58 |      144.42 | 72,839,589 | 3,173,660 |    151 | NEGATED | exactly_shocking           | exactly     | shocking       |
| **NEGany~exactly_pleasant**           |    142 |        58,643 |        52,223 |    0.96 |   1.00 |    7.24 |    889.88 |      6.19 |      135.81 | 72,839,589 | 3,173,660 |    142 | NEGATED | exactly_pleasant           | exactly     | pleasant       |
| **NEGany~exactly_famous**             |    130 |        58,643 |       223,813 |    0.96 |   1.00 |    7.10 |    814.68 |      5.66 |      124.34 | 72,839,589 | 3,173,660 |    130 | NEGATED | exactly_famous             | exactly     | famous         |
| **NEGany~exactly_difficult**          |    126 |        58,643 |       732,106 |    0.96 |   1.00 |    7.05 |    789.62 |      5.49 |      120.51 | 72,839,589 | 3,173,660 |    126 | NEGATED | exactly_difficult          | exactly     | difficult      |
| **NEGany~necessarily_useful**         |    104 |        48,947 |       227,709 |    0.96 |   1.00 |    6.75 |    651.75 |      4.53 |       99.47 | 72,839,589 | 3,173,660 |    104 | NEGATED | necessarily_useful         | necessarily | useful         |
| **NEGany~yet_online**                 |     98 |        95,763 |        15,650 |    0.96 |   1.00 |    6.66 |    614.14 |      4.27 |       93.73 | 72,839,589 | 3,173,660 |     98 | NEGATED | yet_online                 | yet         | online         |
| **NEGany~necessarily_fun**            |     96 |        48,947 |       190,026 |    0.96 |   1.00 |    6.62 |    601.61 |      4.18 |       91.82 | 72,839,589 | 3,173,660 |     96 | NEGATED | necessarily_fun            | necessarily | fun            |
| **NEGany~necessarily_essential**      |     93 |        48,947 |        69,845 |    0.96 |   1.00 |    6.57 |    582.81 |      4.05 |       88.95 | 72,839,589 | 3,173,660 |     93 | NEGATED | necessarily_essential      | necessarily | essential      |
| **NEGany~necessarily_reliable**       |     81 |        48,947 |        90,598 |    0.96 |   1.00 |    6.35 |    507.61 |      3.53 |       77.47 | 72,839,589 | 3,173,660 |     81 | NEGATED | necessarily_reliable       | necessarily | reliable       |
| **NEGany~necessarily_proud**          |     71 |        48,947 |       207,536 |    0.96 |   1.00 |    6.14 |    444.94 |      3.09 |       67.91 | 72,839,589 | 3,173,660 |     71 | NEGATED | necessarily_proud          | necessarily | proud          |
| **NEGany~yet_mainstream**             |     70 |        95,763 |        17,792 |    0.96 |   1.00 |    6.11 |    438.67 |      3.05 |       66.95 | 72,839,589 | 3,173,660 |     70 | NEGATED | yet_mainstream             | yet         | mainstream     |
| **NEGany~that_far-fetched**           |     59 |       208,262 |         5,185 |    0.96 |   1.00 |    5.83 |    369.74 |      2.57 |       56.43 | 72,839,589 | 3,173,660 |     59 | NEGATED | that_far-fetched           | that        | far-fetched    |
| **NEGany~that_thrilled**              |     59 |       208,262 |        24,182 |    0.96 |   1.00 |    5.83 |    369.74 |      2.57 |       56.43 | 72,839,589 | 3,173,660 |     59 | NEGATED | that_thrilled              | that        | thrilled       |
| **NEGany~yet_clear**                  | 10,406 |        95,763 |       349,214 |    0.95 |   0.99 |   10.77 | 64,409.97 |    456.44 |    9,949.56 | 72,839,589 | 3,173,660 | 10,476 | NEGATED | yet_clear                  | yet         | clear          |
| **NEGany~necessarily_indicative**     |  1,389 |        48,947 |         8,148 |    0.95 |   0.99 |    9.43 |  8,577.54 |     61.00 |    1,328.00 | 72,839,589 | 3,173,660 |  1,400 | NEGATED | necessarily_indicative     | necessarily | indicative     |
| **NEGany~that_uncommon**              |    802 |       208,262 |        11,312 |    0.95 |   1.00 |    9.43 |  4,998.32 |     35.03 |      766.97 | 72,839,589 | 3,173,660 |    804 | NEGATED | that_uncommon              | that        | uncommon       |
| **NEGany~exactly_easy**               |  1,066 |        58,643 |       579,827 |    0.95 |   0.99 |    9.32 |  6,596.91 |     46.75 |    1,019.25 | 72,839,589 | 3,173,660 |  1,073 | NEGATED | exactly_easy               | exactly     | easy           |
| **NEGany~that_surprising**            |  1,133 |       208,262 |        70,540 |    0.95 |   0.99 |    9.20 |  6,986.81 |     49.80 |    1,083.20 | 72,839,589 | 3,173,660 |  1,143 | NEGATED | that_surprising            | that        | surprising     |
| **NEGany~necessarily_easy**           |    909 |        48,947 |       579,827 |    0.95 |   0.99 |    9.01 |  5,605.64 |     39.95 |      869.05 | 72,839,589 | 3,173,660 |    917 | NEGATED | necessarily_easy           | necessarily | easy           |
| **NEGany~yet_final**                  |    640 |        95,763 |         5,860 |    0.95 |   1.00 |    8.97 |  3,972.92 |     28.02 |      611.98 | 72,839,589 | 3,173,660 |    643 | NEGATED | yet_final                  | yet         | final          |
| **NEGany~exactly_cheap**              |    691 |        58,643 |        60,531 |    0.95 |   0.99 |    8.96 |  4,281.59 |     30.28 |      660.72 | 72,839,589 | 3,173,660 |    695 | NEGATED | exactly_cheap              | exactly     | cheap          |
| **NEGany~that_unusual**               |    977 |       208,262 |        71,234 |    0.95 |   0.99 |    8.92 |  6,003.05 |     43.05 |      933.95 | 72,839,589 | 3,173,660 |    988 | NEGATED | that_unusual               | that        | unusual        |
| **NEGany~exactly_surprising**         |    440 |        58,643 |        70,540 |    0.95 |   1.00 |    8.71 |  2,743.34 |     19.21 |      420.79 | 72,839,589 | 3,173,660 |    441 | NEGATED | exactly_surprising         | exactly     | surprising     |
| **NEGany~necessarily_representative** |    487 |        48,947 |        18,355 |    0.95 |   0.99 |    8.34 |  2,996.58 |     21.44 |      465.56 | 72,839,589 | 3,173,660 |    492 | NEGATED | necessarily_representative | necessarily | representative |
| **NEGany~necessarily_surprising**     |    340 |        48,947 |        70,540 |    0.95 |   1.00 |    8.33 |  2,117.16 |     14.86 |      325.14 | 72,839,589 | 3,173,660 |    341 | NEGATED | necessarily_surprising     | necessarily | surprising     |
| **NEGany~that_dissimilar**            |    304 |       208,262 |         4,605 |    0.95 |   0.99 |    7.86 |  1,871.65 |     13.38 |      290.62 | 72,839,589 | 3,173,660 |    307 | NEGATED | that_dissimilar            | that        | dissimilar     |
| **NEGany~that_noticeable**            |    264 |       208,262 |        31,467 |    0.95 |   0.99 |    7.65 |  1,621.81 |     11.63 |      252.37 | 72,839,589 | 3,173,660 |    267 | NEGATED | that_noticeable            | that        | noticeable     |
| **NEGany~yet_over**                   |    162 |        95,763 |         3,983 |    0.95 |   0.99 |    7.21 |  1,003.13 |      7.10 |      154.90 | 72,839,589 | 3,173,660 |    163 | NEGATED | yet_over                   | yet         | over           |
| **NEGany~yet_ready**                  |  7,501 |        95,763 |       141,590 |    0.94 |   0.99 |    9.93 | 45,985.07 |    331.09 |    7,169.91 | 72,839,589 | 3,173,660 |  7,599 | NEGATED | yet_ready                  | yet         | ready          |
| **NEGany~yet_complete**               |  2,174 |        95,763 |        86,361 |    0.94 |   0.98 |    9.20 | 13,277.09 |     96.20 |    2,077.80 | 72,839,589 | 3,173,660 |  2,208 | NEGATED | yet_complete               | yet         | complete       |
| **NEGany~exactly_new**                |  1,371 |        58,643 |       253,862 |    0.94 |   0.99 |    9.10 |  8,410.32 |     60.48 |    1,310.52 | 72,839,589 | 3,173,660 |  1,388 | NEGATED | exactly_new                | exactly     | new            |
| **NEGany~exactly_clear**              |  1,746 |        58,643 |       349,214 |    0.94 |   0.98 |    8.78 | 10,578.33 |     77.73 |    1,668.27 | 72,839,589 | 3,173,660 |  1,784 | NEGATED | exactly_clear              | exactly     | clear          |
| **NEGany~that_complicated**           |  1,207 |       208,262 |       159,822 |    0.94 |   0.98 |    8.68 |  7,337.84 |     53.59 |    1,153.41 | 72,839,589 | 3,173,660 |  1,230 | NEGATED | that_complicated           | that        | complicated    |
| **NEGany~terribly_surprising**        |    949 |        58,964 |        70,540 |    0.94 |   0.98 |    8.66 |  5,794.10 |     42.00 |      907.00 | 72,839,589 | 3,173,660 |    964 | NEGATED | terribly_surprising        | terribly    | surprising     |
| **NEGany~necessarily_new**            |    482 |        48,947 |       253,862 |    0.94 |   0.98 |    7.94 |  2,923.82 |     21.44 |      460.56 | 72,839,589 | 3,173,660 |    492 | NEGATED | necessarily_new            | necessarily | new            |
| **NEGany~terribly_uncommon**          |    103 |        58,964 |        11,312 |    0.94 |   0.98 |    6.33 |    625.85 |      4.57 |       98.43 | 72,839,589 | 3,173,660 |    105 | NEGATED | terribly_uncommon          | terribly    | uncommon       |



### Load Negated Hit Table


```python
def clarify_categories(neg_hits, verbose=VERBOSE):
    def lemma_aint_to_not(neg_hits: pd.DataFrame, verbose):
        neg_hits['neg_lemma'] = (neg_hits.neg_lemma.astype('string')
                                .str.replace('aint', "not")
                                .str.replace("ain't", 'not'))
        if verbose:
            print('Updated `neg_lemma` counts with "ain(\')t" merged with "not"', 
              neg_hits.neg_lemma.value_counts().to_markdown(floatfmt=',.0f', intfmt=','), 
              sep='\n\n')
        return neg_hits
    neg_hits = lemma_aint_to_not(neg_hits, verbose)
    # word_cols = neg_hits.filter(regex=r'head|lower|lemma').columns
    # #> drop empty categories if already categorical; make categorical if not already
    # neg_hits.loc[:, word_cols] = neg_hits[word_cols]
    return catify(neg_hits)
```


```python
#// if PRE_FILTERED_NEG_HITS.is_file() and not REFILTER_NEG: 
#//     neg_hits = pd.read_pickle(PRE_FILTERED_NEG_HITS)
#// else:
    # # neg_hits = pd.read_pickle(NEG_HITS_PATH).filter(regex=r'^[nab].*lower|text|str|head')
    # #> Added `neg_lemma` column to selection
    # neg_hits = pd.read_pickle(NEG_HITS_PATH).filter(regex=r'^[nab].*lower|text|str|head|neg_lemma')
    # neg_hits = neg_hits.drop_duplicates(['text_window', 'bigram_lower', 'neg_form_lower'])
    # word_cols = neg_hits.filter(regex=r'head|lower|neg_lemma').columns
    # neg_hits[word_cols] = neg_hits[word_cols].astype('category')
    # neg_hits = neg_hits.loc[neg_hits.adv_form_lower.isin(adv_am.index), :]
if 'pkl' in NEG_HITS_PATH.suffixes:
    neg_hits = pd.read_pickle(NEG_HITS_PATH)

    neg_hits = neg_hits.loc[(neg_hits.adv_lemma.isin(TOP_ADV))
                                        | (neg_hits.adv_form_lower.isin(TOP_ADV)), :]
    if VERBOSE:
        print(neg_hits.neg_lemma.value_counts().to_markdown(floatfmt=',.0f', intfmt=','))
elif NEG_HITS_PATH.suffix.startswith('.parq'):
    neg_hits = pd.read_parquet(NEG_HITS_PATH, 
                               filters=[('adv_form_lower', 'in', TOP_ADV)])

neg_hits = neg_hits.filter(
    regex=r'^[nab].*lower|text|str|head|(adv|neg)_lemma'
    ).drop_duplicates(['text_window', 
                                    #  'bigram_lower', 'neg_form_lower'
                                    'all_forms_lower'
                                        ])
neg_hits = clarify_categories(neg_hits)

```

Updated `neg_lemma` counts with "ain(')t" merged with "not"

| neg_lemma   |   count |
|:------------|--------:|
| not         | 120,540 |
| nothing     |   3,202 |
| never       |   1,798 |
| none        |   1,101 |
| nor         |     554 |
| neither     |     446 |
| hardly      |     326 |
| nobody      |     214 |
| rarely      |     156 |
| without     |     102 |
| few         |      56 |
| barely      |      23 |
| no          |      20 |
| scarcely    |      17 |
| seldom      |      10 |



```python

# sourcery skip: use-fstring-for-concatenation
if 'all_forms_lower' not in neg_hits.columns: 
    neg_hits['all_forms_lower'] = (
        neg_hits.neg_form_lower.astype('string') 
        + '_' 
        + neg_hits.bigram_lower.astype('string')
        ).astype('category')
nb_show_table(neg_hits.sample(3).filter(like='lower'), adjust_columns=False, suppress_printing=not VERBOSE)
```

    
    |                                              | `adv_form_lower`   | `adj_form_lower`   | `bigram_lower`   | `neg_form_lower`   | `all_forms_lower`    |
    |:---------------------------------------------|:-------------------|:-------------------|:-----------------|:-------------------|:---------------------|
    | **pcc_eng_19_041.3941_x0651994_08:16-17-18** | that               | important          | that_important   | not                | not_that_important   |
    | **pcc_eng_25_010.9732_x0161386_05:4-5-6**    | exactly            | uncommon           | exactly_uncommon | n't                | n't_exactly_uncommon |
    | **pcc_eng_28_011.0723_x0162900_02:5-6-7**    | yet                | available          | yet_available    | not                | not_yet_available    |
    


```python
if 'all_forms_lower' not in neg_hits.columns: 
    neg_hits['all_forms_lower'] = (
        neg_hits.neg_form_lower.astype('string') 
        + '_' 
        + neg_hits.bigram_lower.astype('string')
        ).astype('category')
nb_show_table(neg_hits.sample(3).filter(like='lower'), adjust_columns=False, suppress_printing=not VERBOSE)
```


|                                              | `adv_form_lower`   | `adj_form_lower`   | `bigram_lower`   | `neg_form_lower`   | `all_forms_lower`    |
|:---------------------------------------------|:-------------------|:-------------------|:-----------------|:-------------------|:---------------------|
| **pcc_eng_19_041.3941_x0651994_08:16-17-18** | that               | important          | that_important   | not                | not_that_important   |
| **pcc_eng_25_010.9732_x0161386_05:4-5-6**    | exactly            | uncommon           | exactly_uncommon | n't                | n't_exactly_uncommon |
| **pcc_eng_28_011.0723_x0162900_02:5-6-7**    | yet                | available          | yet_available    | not                | not_yet_available    |




```python
# if not PRE_FILTERED_NEG_HITS.is_file() or REFILTER_NEG:
#     neg_hits.to_pickle(PRE_FILTERED_NEG_HITS)
#     print(f'Saved Limited "NEG" hit table as: `{PRE_FILTERED_NEG_HITS.relative_to(POST_PROC_DIR.parent)}`')
# else:
#     print(f'Limited "NEG" hit table already saved as: `{PRE_FILTERED_NEG_HITS.relative_to(POST_PROC_DIR.parent)}`')
```


```python
neg_hits.loc[neg_hits.adv_lemma.astype('string') 
             != neg_hits.adv_form_lower.astype('string')
             ].filter(regex=r'adv|window')
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
      <th>text_window</th>
      <th>adv_lemma</th>
      <th>adv_form_lower</th>
    </tr>
    <tr>
      <th>hit_id</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>




```python
# if VERBOSE:
#     print(neg_hits.adv_lemma.value_counts().to_frame('Tokens in loaded sample').to_markdown(floatfmt=',.0f', intfmt=','))
```

    | adv_lemma    |   Tokens in loaded sample |
    |:-------------|--------------------------:|
    | that         |                    45,368 |
    | particularly |                    15,535 |
    | immediately  |                    14,728 |
    | yet          |                    14,575 |
    | exactly      |                    12,315 |
    | necessarily  |                    11,679 |
    | terribly     |                     4,887 |
    | any          |                     4,246 |
    | inherently   |                     1,901 |
    | ever         |                     1,698 |
    | remotely     |                     1,633 |


```py
if VERBOSE:
    print(neg_hits.adv_lemma.value_counts().to_frame('Tokens in loaded sample')
          .to_markdown(floatfmt=',.0f', intfmt=','))
```

| adv_lemma    |   Tokens in loaded sample |
|:-------------|--------------------------:|
| that         |                    45,368 |
| particularly |                    15,535 |
| immediately  |                    14,728 |
| yet          |                    14,575 |
| exactly      |                    12,315 |
| necessarily  |                    11,679 |
| terribly     |                     4,887 |
| any          |                     4,246 |
| inherently   |                     1,901 |
| ever         |                     1,698 |
| remotely     |                     1,633 |



```python
# if VERBOSE:
#     fewer = sp(data=neg_hits, regex=True, print_sample=False,
#            columns=['WITH::bigram|neg|str'], 
#            filters=['neg_form_lower==fewer'])
#     nb_show_table(fewer.assign(token_str=embolden(fewer.token_str, r' (fewer) ')), adjust_columns=False)
```

```python
if VERBOSE:
    fewer = sp(data=neg_hits, regex=True, print_sample=False,
           columns=['WITH::bigram|neg|str'], 
           filters=['neg_form_lower==fewer'])
    nb_show_table(fewer.assign(token_str=embolden(fewer.token_str, r' (fewer) ')), adjust_columns=False)
```

> - *filtering rows...*
>   - regex parsing = True
>   - ✓ Applied filter: `neg_form_lower==fewer`
> 
> ### All (1) row(s) matching filter(s) from `input frame`
> 
> 
> |                                          | `token_str`                                                                                                      | `lemma_str`                                                                                       | `neg_head`   | `neg_lemma`   | `bigram_lower`   | `neg_form_lower`   |
> |:-----------------------------------------|:-----------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------|:-------------|:--------------|:-----------------|:-------------------|
> | **pcc_eng_04_001.4775_x0007747_3:4-6-7** | In 2D far __`fewer`__ are exactly solvable , the simplest being a rectangle with Dirichlet boundary conditions . | in 2d far few be exactly solvable , the simple be a rectangle with dirichlet boundary condition . | ADJ          | few           | exactly_solvable | fewer              |




```python
if VERBOSE:
    rare_forms = neg_hits.neg_form_lower.value_counts().nsmallest(6).index
    # nb_show_table(neg_hits.loc[neg_hits.neg_form_lower.isin(rare_forms), :].sort_values('neg_form_lower').filter(regex=r'bigram|neg|text'))
    show_sample(neg_hits.loc[neg_hits.neg_form_lower.isin(rare_forms), :].sort_values('neg_form_lower').filter(regex=r'all_forms|win|sent'))
```

    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | hit_id                | sent_text                                          | text_window                                        | all_forms_lower                 |
    +=======================+====================================================+====================================================+=================================+
    | pcc_eng_04_001.4775_x | In 2D far fewer are exactly solvable, the simplest | in 2d far fewer are exactly solvable , the         | fewer_exactly_solvable          |
    | 0007747_3:4-6-7       | being a rectangle with Dirichlet boundary          | simplest being a rectangle                         |                                 |
    |                       | conditions.                                        |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_17_078.8556_x | Isn`t that beautiful and all you have to do is     | is n`t that beautiful and all you have to do       | n`t_that_beautiful              |
    | 1258350_19:2-3-4      | stop talking!                                      |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_20_080.0820_x | really the size of the dick is totally a lie and   | away from the story nobodies dick is that big and  | nobodies_that_big               |
    | 1277728_116:20-23-24  | is just a turn away from the story nobodies dick   | if it was having a                                 |                                 |
    |                       | is that big and if it was having a bonor for 2     |                                                    |                                 |
    |                       | hours would most certianly kill you because all of |                                                    |                                 |
    |                       | the blood would got to your dick and you would die |                                                    |                                 |
    |                       | so this is just a bull story and i hate how people |                                                    |                                 |
    |                       | make there dicks that big it is just not right and |                                                    |                                 |
    |                       | makes it absolutely unbelievable.                  |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_09_031.5011_x | And the 'nothings' that these people talk about    | And the ' nothings ' that these people talk about  | nothings_inherently_postmodern  |
    | 0493764_43:04-12-13   | are inherently postmodern too.                     | are inherently postmodern too .                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_18_002.1227_x | This is nt that much of a hardship.                | This is nt that much of a hardship .               | nt_that_much                    |
    | 0018259_110:3-4-5     |                                                    |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_00_012.2130_x | "But, goodness, those children are seldom ever     | , goodness , those children are seldom ever        | seldom_ever_careful             |
    | 0181116_61:09-10-11   | careful," she mused.                               | careful , " she mused .                            |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_01_103.1159_x | And, says Schmidt, end-of-life decisions are       | , end- of- life decisions are seldom that simple . | seldom_that_simple              |
    | 1650317_068:11-12-13  | seldom that simple.                                |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_02_009.2911_x | Explanations to the big why questions of life are  | why questions of life are seldom if ever           | seldom_ever_forthcoming         |
    | 0133924_53:10-12-13   | seldom if ever forthcoming from God.               | forthcoming from god .                             |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_03_034.7677_x | At the same time, Alice is seldom if ever          | same time , alice is seldom if ever sexualized --  | seldom_ever_sexualized          |
    | 0547039_21:08-10-11   | sexualized -- she gives off more of a look-but-    | she gives off more of                              |                                 |
    |                       | don't-touch vibe.                                  |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_06_073.4511_x | Duty free is rather a misnomer nowadays as the     | nowadays as the goods there are seldom any cheaper | seldom_any_cheaper              |
    | 1171981_07:13-14-15   | goods there are seldom any cheaper than may find   | than may find in a good                            |                                 |
    |                       | in a good department store at home.                |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_13_033.0482_x | Other misused toy powerups include the Energon     | : the weapons the generated were seldom any        | seldom_any_stronger             |
    | 0518168_054:20-21-22  | Chip/Energon Star weapons element: the weapons the | stronger than regular weapons , and tended         |                                 |
    |                       | generated were seldom any stronger than regular    |                                                    |                                 |
    |                       | weapons, and tended to run out of power and vanish |                                                    |                                 |
    |                       | after only one or two uses.                        |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_14_089.1449_x | Max was seldom if ever fearful, not even during    | max was seldom if ever fearful , not even during   | seldom_ever_fearful             |
    | 1424729_051:3-5-6     | the Mystery of the Gruesome Grizzly, but he'd      | the mystery                                        |                                 |
    |                       | never suffered a loss of his mental faculties      |                                                    |                                 |
    |                       | before.                                            |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_24_022.5354_x | On the contrary I feel that it is all the more     | which is really creative -- and seldom immediately | seldom_immediately_popular      |
    | 0347911_012:32-33-34  | essential that authors who are concerned with the  | popular -- should apply themselves sedulously to   |                                 |
    |                       | small part of "literature" which is really         |                                                    |                                 |
    |                       | creative -- and seldom immediately popular --      |                                                    |                                 |
    |                       | should apply themselves sedulously to their work,  |                                                    |                                 |
    |                       | without abatement or sacrifice of their artistic   |                                                    |                                 |
    |                       | standards or any pretext whatsoever.               |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_26_004.6713_x | Things are seldom really that serious.             | Things are seldom really that serious .            | seldom_that_serious             |
    | 0059186_165:3-5-6     |                                                    |                                                    |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+
    | pcc_eng_val_2.01260_x | Even recorded lectures are seldom particularly     | even recorded lectures are seldom particularly     | seldom_particularly_stimulating |
    | 18257_071:5-6-7       | stimulating unless delivered by a gifted speaker.  | stimulating unless delivered by a gifted speaker   |                                 |
    +-----------------------+----------------------------------------------------+----------------------------------------------------+---------------------------------+



```python
# if VERBOSE:
#     nb_show_table(neg_hits.loc[(neg_hits.neg_form_lower!="n't") 
#                    & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string')), 
#                    ['neg_lemma', 'neg_form_lower', 'text_window']].sample(10))
```

    
    |                                                | `neg_lemma`   | `neg_form_lower`   | `text_window`                                                              |
    |:-----------------------------------------------|:--------------|:-------------------|:---------------------------------------------------------------------------|
    | **pcc_eng_22_002.9098_x0031028_63:11-12-13**   | not           | ain't              | fly -by- night spammer , it ain't that important .                         |
    | **pcc_eng_11_089.5964_x1434140_0859:29-30-31** | not           | ain't              | truthfully , " doc , it ain't any easier when you 're old . "              |
    | **pcc_eng_24_102.7387_x1645974_17:28-30-31**   | not           | nit                | slightly ahead this week is nit really that much of a compliment .         |
    | **pcc_eng_11_066.3753_x1058095_06:15-16-17**   | not           | ain't              | or eviscerate hunt , but it ain't that easy .                              |
    | **pcc_eng_12_081.7140_x1304078_034:5-6-7**     | not           | nit                | However , it is nit that easy .                                            |
    | **pcc_eng_22_005.3750_x0070670_39:15-16-17**   | not           | ain't              | look at me that way it ain't that easy                                     |
    | **pcc_eng_08_043.2812_x0684295_06:4-5-6**      | not           | ain't              | what it is ain't exactly clear [ although i think we 've                   |
    | **pcc_eng_07_059.5261_x0946050_05:19-20-21**   | not           | ain't              | happening here , what it is ain't exactly clear " in a scene about vietnam |
    | **pcc_eng_05_093.2853_x1493084_225:09-10-11**  | not           | aint               | hear about myself , and i aint any better than a baby to -day .            |
    | **pcc_eng_24_074.2869_x1185523_04:3-4-5**      | not           | ain't              | usually diets ain't that healthy after all but this one makes              |
    


```python
if VERBOSE:
    nb_show_table(neg_hits.loc[(neg_hits.neg_form_lower!="n't") 
                   & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string')), 
                   ['neg_lemma', 'neg_form_lower', 'text_window']].sample(10))
```                   


|                                                | `neg_lemma` | `neg_form_lower` | `text_window`                                                              |
|:-----------------------------------------------|:------------|:-----------------|:---------------------------------------------------------------------------|
| **pcc_eng_22_002.9098_x0031028_63:11-12-13**   | not         | ain't            | fly -by- night spammer , it ain't that important .                         |
| **pcc_eng_11_089.5964_x1434140_0859:29-30-31** | not         | ain't            | truthfully , " doc , it ain't any easier when you 're old . "              |
| **pcc_eng_24_102.7387_x1645974_17:28-30-31**   | not         | nit              | slightly ahead this week is nit really that much of a compliment .         |
| **pcc_eng_11_066.3753_x1058095_06:15-16-17**   | not         | ain't            | or eviscerate hunt , but it ain't that easy .                              |
| **pcc_eng_12_081.7140_x1304078_034:5-6-7**     | not         | nit              | However , it is nit that easy .                                            |
| **pcc_eng_22_005.3750_x0070670_39:15-16-17**   | not         | ain't            | look at me that way it ain't that easy                                     |
| **pcc_eng_08_043.2812_x0684295_06:4-5-6**      | not         | ain't            | what it is ain't exactly clear [ although i think we 've                   |
| **pcc_eng_07_059.5261_x0946050_05:19-20-21**   | not         | ain't            | happening here , what it is ain't exactly clear " in a scene about vietnam |
| **pcc_eng_05_093.2853_x1493084_225:09-10-11**  | not         | aint             | hear about myself , and i aint any better than a baby to -day .            |
| **pcc_eng_24_074.2869_x1185523_04:3-4-5**      | not         | ain't            | usually diets ain't that healthy after all but this one makes              |




```python
# if VERBOSE:
#     nb_show_table(neg_hits.loc[(neg_hits.neg_lemma!="not") 
#                    & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string')), 
#                    ['neg_lemma', 'neg_form_lower', 'text_window']])
```

    
    |                                               | `neg_lemma`   | `neg_form_lower`   | `text_window`                                                                     |
    |:----------------------------------------------|:--------------|:-------------------|:----------------------------------------------------------------------------------|
    | **pcc_eng_04_001.4775_x0007747_3:4-6-7**      | few           | fewer              | in 2d far fewer are exactly solvable , the simplest being a rectangle             |
    | **pcc_eng_09_031.5011_x0493764_43:04-12-13**  | nothing       | nothings           | And the ' nothings ' that these people talk about are inherently postmodern too . |
    | **pcc_eng_20_080.0820_x1277728_116:20-23-24** | nobody        | nobodies           | away from the story nobodies dick is that big and if it was having a              |
    


```python
if VERBOSE:
    nb_show_table(neg_hits.loc[(neg_hits.neg_lemma!="not") 
                   & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string')), 
                   ['neg_lemma', 'neg_form_lower', 'text_window']])
```
                
|                                               | `neg_lemma` | `neg_form_lower` | `text_window`                                                                     |
|:----------------------------------------------|:------------|:-----------------|:----------------------------------------------------------------------------------|
| **pcc_eng_04_001.4775_x0007747_3:4-6-7**      | few         | fewer            | in 2d far fewer are exactly solvable , the simplest being a rectangle             |
| **pcc_eng_09_031.5011_x0493764_43:04-12-13**  | nothing     | nothings         | And the ' nothings ' that these people talk about are inherently postmodern too . |
| **pcc_eng_20_080.0820_x1277728_116:20-23-24** | nobody      | nobodies         | away from the story nobodies dick is that big and if it was having a              |




```python
if VERBOSE:
    print('Weird example, but illustrates structural relationship which is probably not caught by the patterns for accurate parses: Possessive quantified pronoun in subject', 
      neg_hits.loc[neg_hits.neg_form_lower=='nobodies', ['neg_lemma', 'neg_form_lower', 'bigram_lower', 'text_window', 'token_str']].T.to_markdown(), 
      sep='\n\n')
```

    Weird example, but illustrates structural relationship which is probably not caught by the patterns for accurate parses: Possessive quantified pronoun in subject
    
    |                | pcc_eng_20_080.0820_x1277728_116:20-23-24                                                                                                                                                                                                                                                                                                                                                       |
    |:---------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | neg_lemma      | nobody                                                                                                                                                                                                                                                                                                                                                                                          |
    | neg_form_lower | nobodies                                                                                                                                                                                                                                                                                                                                                                                        |
    | bigram_lower   | that_big                                                                                                                                                                                                                                                                                                                                                                                        |
    | text_window    | away from the story nobodies dick is that big and if it was having a                                                                                                                                                                                                                                                                                                                            |
    | token_str      | really the size of the dick is totally a lie and is just a turn away from the story nobodies dick is that big and if it was having a bonor for 2 hours would most certianly kill you because all of the blood would got to your dick and you would die so this is just a bull story and i hate how people make there dicks that big it is just not right and makes it absolutely unbelievable . |


Weird example, but illustrates structural relationship which is probably not caught by the patterns for accurate parses: Possessive quantified pronoun in subject

|                | pcc_eng_20_080.0820_x1277728_116:20-23-24                                                                                                                                                                                                                                                                                                                                                       |
|:---------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| neg_lemma      | nobody                                                                                                                                                                                                                                                                                                                                                                                          |
| neg_form_lower | nobodies                                                                                                                                                                                                                                                                                                                                                                                        |
| bigram_lower   | that_big                                                                                                                                                                                                                                                                                                                                                                                        |
| text_window    | away from the story nobodies dick is that big and if it was                                                                                                                                                                                                                                                                                                                                     |
| token_str      | really the size of the dick is totally a lie and is just a turn away from the story nobodies dick is that big and if it was having a bonor for 2 hours would most certianly kill you because all of the blood would got to your dick and you would die so this is just a bull story and i hate how people make there dicks that big it is just not right and makes it absolutely unbelievable . |



```python
if VERBOSE:
    nb_show_table(neg_hits.filter(like='lower').loc[neg_hits.adv_form_lower=='exactly',:].sample(10))
```

    
    |                                               | `adv_form_lower`   | `adj_form_lower`   | `bigrlower`     | `neg_form_lower`   | `all_forms_lower`   |
    |:----------------------------------------------|:-------------------|:-------------------|:----------------|:-------------------|:--------------------|
    | **pcc_eng_07_051.5193_x0816711_01:02-09-10**  | exactly            | perfect            | exactly_perfect | n't                | n't_exactly_perfect |
    | **pcc_eng_08_009.4056_x0135817_017:10-13-14** | exactly            | close              | exactly_close   | nor                | nor_exactly_close   |
    | **pcc_eng_26_015.5374_x0235107_02:13-14-15**  | exactly            | true               | exactly_true    | not                | not_exactly_true    |
    | **pcc_eng_14_006.4005_x0087422_04:5-6-7**     | exactly            | sure               | exactly_sure    | not                | not_exactly_sure    |
    | **pcc_eng_24_104.0661_x1667535_21:6-7-8**     | exactly            | ready              | exactly_ready   | not                | not_exactly_ready   |
    | **pcc_eng_03_007.5105_x0105185_43:4-5-6**     | exactly            | sure               | exactly_sure    | not                | not_exactly_sure    |
    | **pcc_eng_14_087.1536_x1392517_22:5-6-7**     | exactly            | easy               | exactly_easy    | not                | not_exactly_easy    |
    | **pcc_eng_14_088.7511_x1418419_75:25-26-27**  | exactly            | tactful            | exactly_tactful | n't                | n't_exactly_tactful |
    | **pcc_eng_05_007.2890_x0102130_08:19-20-21**  | exactly            | unheard            | exactly_unheard | not                | not_exactly_unheard |
    | **pcc_eng_15_098.2211_x1571324_09:5-6-7**     | exactly            | clear              | exactly_clear   | n't                | n't_exactly_clear   |
    



|                                               | `adv_form_lower`   | `adj_form_lower`   | `bigrlower`     | `neg_form_lower`   | `all_forms_lower`   |
|:----------------------------------------------|:-------------------|:-------------------|:----------------|:-------------------|:--------------------|
| **pcc_eng_07_051.5193_x0816711_01:02-09-10**  | exactly            | perfect            | exactly_perfect | n't                | n't_exactly_perfect |
| **pcc_eng_08_009.4056_x0135817_017:10-13-14** | exactly            | close              | exactly_close   | nor                | nor_exactly_close   |
| **pcc_eng_26_015.5374_x0235107_02:13-14-15**  | exactly            | true               | exactly_true    | not                | not_exactly_true    |
| **pcc_eng_14_006.4005_x0087422_04:5-6-7**     | exactly            | sure               | exactly_sure    | not                | not_exactly_sure    |
| **pcc_eng_24_104.0661_x1667535_21:6-7-8**     | exactly            | ready              | exactly_ready   | not                | not_exactly_ready   |
| **pcc_eng_03_007.5105_x0105185_43:4-5-6**     | exactly            | sure               | exactly_sure    | not                | not_exactly_sure    |
| **pcc_eng_14_087.1536_x1392517_22:5-6-7**     | exactly            | easy               | exactly_easy    | not                | not_exactly_easy    |
| **pcc_eng_14_088.7511_x1418419_75:25-26-27**  | exactly            | tactful            | exactly_tactful | n't                | n't_exactly_tactful |
| **pcc_eng_05_007.2890_x0102130_08:19-20-21**  | exactly            | unheard            | exactly_unheard | not                | not_exactly_unheard |
| **pcc_eng_15_098.2211_x1571324_09:5-6-7**     | exactly            | clear              | exactly_clear   | n't                | n't_exactly_clear   |




```python
def collect_adv_bigram_ex(amdf: pd.DataFrame,
                     hits_df: pd.DataFrame,
                     adv: str = 'exactly',
                     n_bigrams: int = BK,
                     n_examples: int = 50,
                     verbose:bool=False,
                     metric: str | list = ['dP1', 'LRC']) -> dict:
    if amdf.adv.nunique() > 1: 
        amdf = amdf.filter(like=f'~{adv}_',
                            axis=0).nlargest(n_bigrams, metric)
    examples = {}
    for i, bigram in enumerate(amdf['l2'].unique(), start=1):
        bigram_text = bigram.replace("_", " ")
        if verbose: 
            print(f'\n{i}. _{bigram_text}_')
        ex_for_bigram = sp(
            data=hits_df, print_sample=False, quiet=True,
            sample_size=n_examples,  sort_by='all_forms_lower',
            filters=[f'bigram_lower=={bigram}'],
            columns=['END::lower', 'text_window', 'token_str'])
        excerpt = embolden(ex_for_bigram.sample(min(len(ex_for_bigram), 5))[
                        'token_str'], f' ({bigram_text}) ').to_frame()
        excerpt.index = '`'+excerpt.index.astype('string')+'`'
        nb_show_table(excerpt, suppress_printing=not verbose)
        # print('\n   > ', [f'> {}' for i in ex_for_bigram.sample(3).index])
        examples[bigram] = ex_for_bigram
    return examples


def populate_adv_dir(adverb, bigram_am, neg_hits, n_ex:int=50,
                     rank_by: str | list = ['dP1', "LRC"], 
                     verbose:bool=False):
    output_dir = TOP_AM_DIR / 'neg_bigram_examples' / adverb
    table_csv_path = output_dir / \
        f'{adverb}_{BK}mostNEG-bigrams_AMscores_{timestamp_today()}.csv'
    confirm_dir(output_dir)
    this_adv_amdf = bigram_am.filter(
        like=f'~{adverb}_', axis=0).sort_values(rank_by, ascending=False)
    this_adv_amdf.to_csv(table_csv_path)

    nb_show_table(this_adv_amdf.filter(['N', 'f1', 'adv_total'])
                  .set_index(this_adv_amdf.l1 + f'_{adverb}').drop_duplicates(),
                  n_dec=0,
                  outpath=output_dir / f'{adverb}_MarginalFreqs_{timestamp_today()}.md', 
                  suppress_printing=not verbose)
    
    nb_show_table(this_adv_amdf.filter(regex=r'^([dLGeu]|f2?$|adj_total)').round(2).sort_values(rank_by, ascending=False), n_dec=2,
                  outpath=table_csv_path.with_suffix('.md'),
                  suppress_printing=not verbose)
    
    examples = collect_adv_bigram_ex(this_adv_amdf, neg_hits, metric=rank_by, n_examples=n_ex, verbose=verbose)

    print(f'\nSaving Samples in {output_dir}/...')

    paths = []
    for key, df in examples.items():
        out_path = output_dir.joinpath(f'{key}_{n_ex}ex.csv')
        df.to_csv(out_path)
        paths.append(out_path)
        
    if verbose:
        print_iter((f'`{p.relative_to(output_dir.parent.parent)}`' for p in paths), header='\nSamples saved as...', bullet='1.')

print(f'# {BK} Most Negative Bigrams for each of the {K} Most Negative Adverbs\n')

for rank, adverb in enumerate(adv_am.index, start=1):
    print(f'\n## {rank}. *{adverb}*')
    populate_adv_dir(adverb, bigram_am, neg_hits, rank_by=['dP1', 'LRC'], n_ex=N_EX_PER_BIGRAM, 
                     verbose=VERBOSE)
```

    # 10 Most Negative Bigrams for each of the 8 Most Negative Adverbs
    
    
    ## 1. *necessarily*
    
    |                         |        `N` |      `f1` |   `adv_total` |
    |:------------------------|-----------:|----------:|--------------:|
    | **NEGATED_necessarily** | 72,839,589 | 3,173,660 |        48,947 |
    | **NEGMIR_necessarily**  |  1,701,929 |   291,732 |         1,107 |
    
    
    |                                       |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:--------------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGany~necessarily_useful**         |   104 |       227,709 |    0.96 |    6.75 |   651.75 |      4.53 |       99.47 |    104 |
    | **NEGany~necessarily_fun**            |    96 |       190,026 |    0.96 |    6.62 |   601.61 |      4.18 |       91.82 |     96 |
    | **NEGany~necessarily_essential**      |    93 |        69,845 |    0.96 |    6.57 |   582.81 |      4.05 |       88.95 |     93 |
    | **NEGany~necessarily_reliable**       |    81 |        90,598 |    0.96 |    6.35 |   507.61 |      3.53 |       77.47 |     81 |
    | **NEGany~necessarily_proud**          |    71 |       207,536 |    0.96 |    6.14 |   444.94 |      3.09 |       67.91 |     71 |
    | **NEGany~necessarily_indicative**     | 1,389 |         8,148 |    0.95 |    9.43 | 8,577.54 |     61.00 |    1,328.00 |  1,400 |
    | **NEGany~necessarily_easy**           |   909 |       579,827 |    0.95 |    9.01 | 5,605.64 |     39.95 |      869.05 |    917 |
    | **NEGany~necessarily_representative** |   487 |        18,355 |    0.95 |    8.34 | 2,996.58 |     21.44 |      465.56 |    492 |
    | **NEGany~necessarily_surprising**     |   340 |        70,540 |    0.95 |    8.33 | 2,117.16 |     14.86 |      325.14 |    341 |
    | **NEGany~necessarily_new**            |   482 |       253,862 |    0.94 |    7.94 | 2,923.82 |     21.44 |      460.56 |    492 |
    | **NEGmir~necessarily_right**          |    23 |         5,576 |    0.83 |    2.15 |    81.13 |      3.94 |       19.06 |     23 |
    | **NEGmir~necessarily_illegal**        |    15 |           937 |    0.83 |    1.20 |    52.91 |      2.57 |       12.43 |     15 |
    | **NEGmir~necessarily_wrong**          |   211 |        20,880 |    0.81 |    5.04 |   698.74 |     37.03 |      173.97 |    216 |
    | **NEGmir~necessarily_new**            |    23 |        12,836 |    0.79 |    1.84 |    73.19 |      4.11 |       18.89 |     24 |
    | **NEGmir~necessarily_bad**            |    50 |        10,261 |    0.77 |    2.95 |   154.45 |      9.08 |       40.92 |     53 |
    | **NEGmir~necessarily_true**           |    53 |         6,191 |    0.73 |    2.69 |   150.42 |     10.11 |       42.89 |     59 |
    | **NEGmir~necessarily_better**         |    27 |        14,013 |    0.70 |    1.63 |    72.90 |      5.31 |       21.69 |     31 |
    
    
    1. _necessarily useful_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_003.9319_x0047305_11:36-37-38`**  | He speaks to Mariko Kosaka , a Developer Advocate on the Google Developers Relations Team , about the art she creates with code and how developers can embrace the notion of making something that is n't __`necessarily useful`__ but still has value .                                                |
    | **`pcc_eng_05_032.3717_x0508217_023:3-4-5`**    | It is not __`necessarily useful`__ .                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_16_024.1662_x0374968_60:11-12-13`**  | The talent and skill required to win an election is not __`necessarily useful`__ for the actual practice of good governing .                                                                                                                                                                            |
    | **`pcc_eng_25_088.1656_x1410634_2:08-09-10`**   | These are personal macros , which are not __`necessarily useful`__ to other authors ( they are provided as part off the source of others of the author 's packages ) .                                                                                                                                  |
    | **`pcc_eng_18_032.9940_x0517908_004:26-27-28`** | But full-fledged off -grid living is vastly more expensive than preparing for a temporary disruption , which is why those survivalist - prepper sites are n't __`necessarily useful`__ for people simply trying to make it though a relatively brief storm- generated power outage or similar problem . |
    
    
    2. _necessarily fun_
    
    |                                                 | `token_str`                                                                                                                                                                    |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_055.3530_x0877869_36:20-21-22`**  | It is such a special organization , with great people that do some hard work in areas that are n't __`necessarily fun`__ .                                                     |
    | **`pcc_eng_15_095.6429_x1529776_05:13-15-16`**  | " There were a lot of hurdles and obstacles - it was n't always __`necessarily fun`__ for me - but to work with that calibre of talent was fun , an honour and a privilege . " |
    | **`pcc_eng_19_043.2627_x0682345_13:15-16-17`**  | It 's a great concept leads to some interesting situations , though it 's not __`necessarily fun`__ .                                                                          |
    | **`pcc_eng_22_007.6486_x0107392_049:12-13-14`** | " When you are a 19 - year-old , it 's not __`necessarily fun`__ to be pounding kale smoothies and not going out to Chipotle with your te ......                               |
    | **`pcc_eng_29_091.4296_x1460622_23:4-5-6`**     | But it is n't __`necessarily fun`__ .                                                                                                                                          |
    
    
    3. _necessarily essential_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                      |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_012.4412_x0185528_14:12-13-14`**  | In a few languages , usually dynamic types , It 's not __`necessarily essential`__ to declare a variable previous to assigning it a worth .                                                                                                                      |
    | **`pcc_eng_21_073.4769_x1171353_114:7-8-9`**    | As a consequence their music is n't __`necessarily essential`__ listening .                                                                                                                                                                                      |
    | **`pcc_eng_27_008.4948_x0120653_43:31-32-33`**  | They 're conducting interviews and when you 're talking about allegations from years ago where there 's no obvious place to obtain documents or other corroborating evidence , it 's not __`necessarily essential`__ to nail down what 's true and what 's not . |
    | **`pcc_eng_10_048.7955_x0773035_061:30-31-32`** | That said , approximately 24 percent of the Top Shops do n't perform any of the machining strategies listed in Table 3 , suggesting that those sophisticated techniques are n't __`necessarily essential`__ for every shop to be successful .                    |
    | **`apw_eng_20090115_1256_106:12-13-14`**        | for this job , intelligence experience is certainly helpful but is n't __`necessarily essential`__ .                                                                                                                                                             |
    
    
    4. _necessarily reliable_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                   |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_13_085.5195_x1366210_06:38-39-40`**  | Things that we tend to really like : Weird ideas or combinations of ideas we have n't seen before ; Sense of wonder ; Strong character and plot arcs ; Relatable protagonists ( not necessarily likeable , not __`necessarily reliable`__ ) ; |
    | **`pcc_eng_28_011.2772_x0166322_35:10-11-12`**  | PETER RYAN : But that China insulation theory is not __`necessarily reliable`__ .                                                                                                                                                             |
    | **`pcc_eng_26_034.0068_x0533530_049:18-19-20`** | Using a development platform can make it easy to code your web page , but they are not __`necessarily reliable`__ .                                                                                                                           |
    | **`pcc_eng_22_051.9905_x0823780_43:08-09-10`**  | Sources are real , but the are not __`necessarily reliable`__ or 100 % accurate .                                                                                                                                                             |
    | **`pcc_eng_19_045.6425_x0720669_30:21-22-23`**  | If you are reliant on the Middle East , or Iran or Russia to get your gas -- that 's not __`necessarily reliable`__ .                                                                                                                         |
    
    
    5. _necessarily proud_
    
    |                                                 | `token_str`                                                                                           |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_089.9525_x1440176_057:16-17-18`** | Eik comes to a halt before the unfamiliar mare , and he stands tall but not __`necessarily proud`__ . |
    | **`pcc_eng_26_033.5152_x0525703_04:3-4-5`**     | I 'm not __`necessarily proud`__ of it , but things are what they are .                               |
    | **`pcc_eng_15_097.7459_x1563640_11:2-3-4`**     | Iim not __`necessarily proud`__ of this one , but it did the trick and Josh was happy with it .       |
    | **`pcc_eng_22_005.3112_x0069657_10:09-10-11`**  | Which makes me feel a bit vulnerable and not __`necessarily proud`__ of what I am producing .         |
    | **`pcc_eng_17_070.2041_x1118143_08:3-4-5`**     | I 'm not __`necessarily proud`__ of it , but there you go .                                           |
    
    
    6. _necessarily surprising_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                              |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_102.8369_x1646191_17:4-5-6`**    | So it is not __`necessarily surprising`__ that intimidation ( real or perceived ) during the referendum was rife .                                                                                                                                                       |
    | **`pcc_eng_28_017.6197_x0268784_085:5-6-7`**   | While the numbers are not __`necessarily surprising`__ , they do show how important caste still is in contemporary Indian society .                                                                                                                                      |
    | **`pcc_eng_06_107.3382_x1720129_26:08-09-10`** | With numerous superior features , it is not __`necessarily surprising`__ that a lot more parents , lovers and employers are employing this kind of spying software to grant themselves item of mind and protect their spouse and children along with their investments . |
    | **`pcc_eng_07_035.5026_x0558072_07:09-10-11`** | Leahy says the findings are shocking , but not __`necessarily surprising`__ considering the challenges so many departments are facing .                                                                                                                                  |
    | **`pcc_eng_03_039.8852_x0629954_34:3-4-5`**    | It 's not __`necessarily surprising`__ , but it does suggest that efforts to promote accountable governance worldwide may have more long-term benefits than may appear at first glance .                                                                                 |
    
    
    7. _necessarily indicative_
    
    |                                                 | `token_str`                                                                                                                                                                    |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_036.1982_x0568840_51:5-6-7`**     | " The results are not __`necessarily indicative`__ of happens when the patient goes back into the community setting .                                                          |
    | **`pcc_eng_28_077.5186_x1237719_35:5-6-7`**     | Status and age are not __`necessarily indicative`__ of seniority , nor do they carry much weight in themselves .                                                               |
    | **`pcc_eng_07_053.5257_x0849006_106:27-28-29`** | After Fred 's death , he remarked that he started drinking when " a girl [ he ] loved " was dying ; although this is not __`necessarily indicative`__ of romantic love . [ 6 ] |
    | **`pcc_eng_01_102.5220_x1640802_077:11-12-13`** | ( Just a reminder , opening bids are strategic , not __`necessarily indicative`__ . ) "                                                                                        |
    | **`pcc_eng_11_084.4499_x1350833_19:14-15-16`**  | Furthermore , the prices hospitals are now required to put out there are n't __`necessarily indicative`__ of what patients actually pay for services .                         |
    
    
    8. _necessarily easy_
    
    |                                                | `token_str`                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_096.4938_x1543432_26:20-21-22`** | And yet , for small business looking to establish a presence on the web , building a website is n't __`necessarily easy`__ .                                                                                                         |
    | **`pcc_eng_11_097.2628_x1558327_11:24-25-26`** | I 'd say that all my parents had to do was get ( and stay ) pregnant , except I know that 's not __`necessarily easy`__ or possible , and I 'd hate to appear flippant about something which causes so many people such heartbreak . |
    | **`pcc_eng_17_075.3373_x1201415_2:15-16-17`**  | I said why not because I love black aura and infinite darkness stuff is n't __`necessarily easy`__ to come by .                                                                                                                      |
    | **`pcc_eng_03_009.9542_x0144793_19:15-16-17`** | And at the same time it is a big and complicated story that is not __`necessarily easy`__ to tell .                                                                                                                                  |
    | **`pcc_eng_28_041.2497_x0651038_4:11-12-13`**  | These are beautiful , but complex systems , which are not __`necessarily easy`__ to administer .                                                                                                                                     |
    
    
    9. _necessarily representative_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                    |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_076.6830_x1222654_19:17-18-19`**  | He also stresses that his experience , interest , and involvement in the DIY scene is n't __`necessarily representative`__ of others .                                                                                                                                                                         |
    | **`pcc_eng_14_001.8773_x0014307_09:38-39-40`**  | The challenge here is for us to recognise what we are thinking , when we are thinking it and by taking notice we can then understand that our thoughts are just actually our interpretation of events and not __`necessarily representative`__ of reality .                                                    |
    | **`pcc_eng_17_059.4764_x0944589_063:09-10-11`** | The report cautions that the countries reviewed are not __`necessarily representative`__ of the G-20 countries .                                                                                                                                                                                               |
    | **`pcc_eng_22_007.0094_x0096898_121:4-5-6`**    | The sample is not __`necessarily representative`__ , for people have many reasons to click " like " on the movement 's well - tailored page -- I have been following Casa Pound for several years -- but the report observes that Casa Pound 's supporters tend to be male and tend to distrust institutions . |
    | **`pcc_eng_29_038.4974_x0605381_15:12-13-14`**  | I realize that the San Francisco Bay Area in CA is not __`necessarily representative`__ of the rest of the country , but around here at least , this is not exactly news .                                                                                                                                     |
    
    
    10. _necessarily new_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                     |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_033.6217_x0528371_17:6-7-8`**    | A slightly different concept , not __`necessarily new`__ but rather an evolved one .                                                                                                                                                                                            |
    | **`pcc_eng_18_037.2638_x0586664_57:14-15-16`** | There are plenty of people , new to faction warfare , who are not __`necessarily new`__ to the game and who probably should n't be labelled spies right off the bat .                                                                                                           |
    | **`nyt_eng_19960914_0156_6:4-5-6`**            | the persecution is not __`necessarily new`__ , but evangelicals are linking events in different countries , describing them as a single , escalating worldwide problem and demanding a vigorous response from the U.S. government .                                             |
    | **`pcc_eng_14_085.3775_x1363859_12:22-23-24`** | Women 's nomenclature has been a point of contention for centuries -- and the practice of keeping one 's own is n't __`necessarily new`__ .                                                                                                                                     |
    | **`pcc_eng_25_034.4964_x0542303_07:13-14-15`** | While the practice of deploying an existing RHEL license on Azure is not __`necessarily new`__ , the removal of the additional cost to previously do so and full two -party support should have most users lowering their guard and experimenting with the new implementation . |
    
    
    11. _necessarily right_
    
    |                                                | `token_str`                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_049.0374_x0776597_28:4-5-6`**    | " That is not __`necessarily right`__ now .                                                                                                                                                                                                |
    | **`pcc_eng_15_098.2984_x1572581_2:1-5-6`**     | Not all architects are __`necessarily right`__ for you , we eliminate the possibility of the issue with chemistry , schedule and project scale to help you create a design team that is fully focused on creating the space you dream of . |
    | **`pcc_eng_26_008.1040_x0114617_53:27-28-29`** | Then some people who tried a low-salt diet found their cravings for salt adjusted over time , so that suggests eating fit based on cravings is not __`necessarily right`__ .                                                               |
    | **`nyt_eng_20001128_0089_9:3-4-5`**            | it 's not __`necessarily right`__ , but it 's exactly what happens when lawyers , consultants , and operatives rule the day .                                                                                                              |
    | **`pcc_eng_28_046.2308_x0731849_04:5-6-7`**    | But collective wisdom is n't __`necessarily right`__ , and Corbyn began to prove this when he addressed the Labour Party Conference yesterday .                                                                                            |
    
    
    12. _necessarily illegal_
    
    |                                                 | `token_str`                                                                                                                                                                                                   |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_072.5955_x1158187_075:08-09-10`** | Well , small amounts of marijuana are n't __`necessarily illegal`__ anymore .                                                                                                                                 |
    | **`pcc_eng_21_027.2020_x0423529_41:10-11-12`**  | In has a clear-cut legal case since it is not __`necessarily illegal`__ to copy information from a website .                                                                                                  |
    | **`pcc_eng_29_002.3359_x0021452_05:34-35-36`**  | The standard line from the White House , which is not without merit , says that the problem was systemic : the financial industry 's misdeeds are now obvious , but they were n't __`necessarily illegal`__ . |
    | **`pcc_eng_02_034.7010_x0545550_27:16-17-18`**  | When Jackson is around a teenager , it brings out his own immature , but not __`necessarily illegal`__ , behavior .                                                                                           |
    | **`nyt_eng_20071124_0125_4:6-7-8`**             | `` These business arrangements are not __`necessarily illegal`__ , '' said Marc S. Savitt , the president-elect of the National Association of Mortgage Brokers , a trade group .                             |
    
    
    13. _necessarily wrong_
    
    |                                             | `token_str`                                                                                                                                                                                                                                                                     |
    |:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_017.6113_x0268718_14:4-5-6`** | While there is nothing __`necessarily wrong`__ with this in a buoyant market , too high a price may deter potential buyers and force them to consider alternative properties in the region .                                                                                    |
    | **`pcc_eng_18_088.0405_x1409547_3:3-4-5`**  | There 's nothing __`necessarily wrong`__ with the video - it just seems to focus heavily on the action aspect of the title .                                                                                                                                                    |
    | **`pcc_eng_12_060.4496_x0961284_12:4-5-6`** | John Kyl is not __`necessarily wrong`__ when he says , " All we have to do on the Republican side is sit down with those who have amendments , get those amendments in a reasonable package , not too many , but enough so all of the members can say they had their chance . " |
    | **`pcc_eng_23_082.7821_x1321608_13:4-5-6`** | While there 's nothing __`necessarily wrong`__ with using these and other types of OTC drugs , it 's a mistake to think that there 's no downside .                                                                                                                             |
    | **`pcc_eng_28_013.2963_x0199229_49:7-8-9`** | In this way , it 's not __`necessarily wrong`__ to use abbreviations or Internet slang ; however , remember that different ways of expressing yourself make what you 're saying stand out better .                                                                              |
    
    
    14. _necessarily bad_
    
    |                                                | `token_str`                                                                                                                                                                                                                  |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20071204_0079_30:6-7-8`**           | `` The over-the-counter stuff is n't __`necessarily bad`__ for mild acne , '' Dr. Jodi Ganz says .                                                                                                                           |
    | **`pcc_eng_12_002.6925_x0027359_040:5-6-7`**   | Too much chocolate is not __`necessarily bad`__ for you , but your brain certainly might see it that way .                                                                                                                   |
    | **`pcc_eng_00_034.9274_x0548079_28:6-7-8`**    | Cooper 's comments here were n't __`necessarily bad`__ in their own right , but it 's also understandable why they sparked a backlash , especially as she did n't provide the context of what she was talking about on air . |
    | **`pcc_eng_22_003.1028_x0034176_09:08-09-10`** | A little tolerance on the spec is n't __`necessarily bad`__ .                                                                                                                                                                |
    | **`pcc_eng_29_009.9673_x0144977_46:3-4-5`**    | Judd is n't __`necessarily bad`__ , she 's just saddled with a one-dimensional , mama- bear- protecting - her- cub role .                                                                                                    |
    
    
    15. _necessarily true_
    
    |                                                 | `token_str`                                                                                                      |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_059.4636_x0945245_134:14-15-16`** | Acknowledge these feelings and realise that they have arisen from thoughts that are n't __`necessarily true`__ . |
    | **`pcc_eng_14_047.8280_x0756552_003:3-4-5`**    | It 's not __`necessarily true`__ , but you will find that many will definitely believe it .                      |
    | **`pcc_eng_00_072.3584_x1153632_10:14-15-16`**  | This sign offers a plausible explanation for Carter 's statement ( plausible , not __`necessarily true`__ ) .    |
    | **`pcc_eng_02_008.3427_x0118395_044:7-8-9`**    | Well , wait , that 's not __`necessarily true`__ . "                                                             |
    | **`pcc_eng_24_077.0266_x1229865_34:4-5-6`**     | The former is not __`necessarily true`__ , while the latter probably is .                                        |
    
    
    16. _necessarily better_
    
    |                                                | `token_str`                                                                                                                                                                                                                              |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_008.3911_x0119260_83:23-24-25`** | Just to serves to jerk our chains and remind us of a couple of proven concepts , to wit : Bigger ai n't __`necessarily better`__ , and left alone , Mother Nature can conjure up some cool stuff .                                       |
    | **`pcc_eng_23_084.9669_x1356994_05:7-8-9`**    | Evidence presented suggests that bigger is not __`necessarily better`__ in healthcare , and that less competition amounts to higher costs and poorer patient outcomes .                                                                  |
    | **`pcc_eng_24_070.1115_x1117878_20:09-10-11`** | He admits that the message " more is not __`necessarily better`__ " is hard for many churches to hear , particularly those with an evangelical tradition such as his own United Methodist .                                              |
    | **`pcc_eng_16_054.9527_x0873139_39:3-4-5`**    | One is n't __`necessarily better`__ than the other , but rather , it 's dependent on what your company needs .                                                                                                                           |
    | **`pcc_eng_04_108.03930_x1735649_3:41-42-43`** | The game is set in a steampunk - inspired vision of old Europe , and through voiceless storytelling we intend to tell the story of the fall of the king of Electropia and the rise of a new ( and not __`necessarily better`__ ) order . |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/...
    
    Samples saved as...
    1. `neg_bigram_examples/necessarily/necessarily_useful_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_fun_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_essential_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_reliable_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_proud_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_surprising_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_indicative_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_easy_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_representative_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_new_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_right_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_illegal_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_wrong_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_bad_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_true_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_better_99ex.csv`
    
    ## 2. *that*
    
    |                  |        `N` |      `f1` |   `adv_total` |
    |:-----------------|-----------:|----------:|--------------:|
    | **NEGATED_that** | 72,839,589 | 3,173,660 |       208,262 |
    | **NEGMIR_that**  |  1,701,929 |   291,732 |         5,494 |
    
    
    |                             |   `f` |   `adj_total` |   `dP1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:----------------------------|------:|--------------:|--------:|--------:|----------:|----------:|------------:|-------:|
    | **NEGany~that_far-fetched** |    59 |         5,185 |    0.96 |    5.83 |    369.74 |      2.57 |       56.43 |     59 |
    | **NEGany~that_thrilled**    |    59 |        24,182 |    0.96 |    5.83 |    369.74 |      2.57 |       56.43 |     59 |
    | **NEGany~that_uncommon**    |   802 |        11,312 |    0.95 |    9.43 |  4,998.32 |     35.03 |      766.97 |    804 |
    | **NEGany~that_surprising**  | 1,133 |        70,540 |    0.95 |    9.20 |  6,986.81 |     49.80 |    1,083.20 |  1,143 |
    | **NEGany~that_unusual**     |   977 |        71,234 |    0.95 |    8.92 |  6,003.05 |     43.05 |      933.95 |    988 |
    | **NEGany~that_dissimilar**  |   304 |         4,605 |    0.95 |    7.86 |  1,871.65 |     13.38 |      290.62 |    307 |
    | **NEGany~that_noticeable**  |   264 |        31,467 |    0.95 |    7.65 |  1,621.81 |     11.63 |      252.37 |    267 |
    | **NEGany~that_complicated** | 1,207 |       159,822 |    0.94 |    8.68 |  7,337.84 |     53.59 |    1,153.41 |  1,230 |
    | **NEGany~that_familiar**    | 1,126 |       156,296 |    0.93 |    8.35 |  6,781.11 |     50.37 |    1,075.63 |  1,156 |
    | **NEGany~that_hard**        | 9,948 |       348,463 |    0.91 |    8.59 | 58,817.24 |    452.26 |    9,495.74 | 10,380 |
    | **NEGmir~that_keen**        |    31 |         1,360 |    0.83 |    2.73 |    109.35 |      5.31 |       25.69 |     31 |
    | **NEGmir~that_impressive**  |    23 |         5,007 |    0.83 |    2.15 |     81.13 |      3.94 |       19.06 |     23 |
    | **NEGmir~that_fond**        |    23 |         1,115 |    0.79 |    1.84 |     73.19 |      4.11 |       18.89 |     24 |
    | **NEGmir~that_comfortable** |    23 |         4,642 |    0.79 |    1.84 |     73.19 |      4.11 |       18.89 |     24 |
    | **NEGmir~that_clear**       |    18 |         6,722 |    0.78 |    1.30 |     56.03 |      3.26 |       14.74 |     19 |
    | **NEGmir~that_popular**     |    65 |         5,668 |    0.76 |    3.15 |    195.15 |     12.00 |       53.00 |     70 |
    | **NEGmir~that_simple**      |   474 |        25,408 |    0.72 |    4.36 |  1,340.19 |     90.68 |      383.32 |    529 |
    | **NEGmir~that_easy**        |   450 |        18,610 |    0.71 |    4.23 |  1,248.84 |     87.08 |      362.92 |    508 |
    | **NEGmir~that_big**         |   113 |         8,177 |    0.69 |    3.17 |    300.54 |     22.46 |       90.54 |    131 |
    | **NEGmir~that_great**       |   286 |         5,568 |    0.66 |    3.57 |    725.16 |     58.62 |      227.38 |    342 |
    
    
    1. _that far-fetched_
    
    |                                                 | `token_str`                                                                                                                                                                         |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20050302_0293_7:5-7-8`**             | premonitions of violence were not all __`that far-fetched`__ , given what would come down in America in the decades to come .                                                       |
    | **`nyt_eng_20050101_0068_66:28-29-30`**         | if presidents are struggling for control , if the NCAA is legally helpless to rein in salaries , the chance of financial chaos at some institutions is n't __`that far-fetched`__ . |
    | **`nyt_eng_19960625_0490_13:23-24-25`**         | `` The stuff that 's in the movies , while some of it is truly science fiction , some of it is not __`that far-fetched`__ .                                                         |
    | **`pcc_eng_06_104.2003_x1669450_214:12-13-14`** | Of course , writing off a comeback from Edmure Tully is n't __`that far-fetched`__ , especially since we 've all probably been guilty of doing that several times already .         |
    | **`nyt_eng_20051115_0368_3:08-10-11`**          | but today , Shugrue 's statement is n't all __`that far-fetched`__ : Abbot Kinney has , seemingly overnight , become the darling of Los Angeles ' art and architecture set .        |
    
    
    2. _that thrilled_
    
    |                                                | `token_str`                                                                                                                                                                              |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_065.6586_x1045361_19:15-16-17`** | And I even insist , though my wife [ who is Jewish ] is n't __`that thrilled`__ , on having for our daughter a little version of the Seder .                                             |
    | **`pcc_eng_15_100.4327_x1606964_08:3-4-5`**    | I was n't __`that thrilled`__ with the cybernetic additions to it anyway .                                                                                                               |
    | **`pcc_eng_12_001.2080_x0003435_3:26-27-28`**  | Punk was asked about possibly facing The Dead Man at Wrestle Mania during a panel at last September 's Ohio Comic-Con , and Punk was n't __`that thrilled`__ about the potential match . |
    | **`pcc_eng_17_049.7022_x0786813_08:14-15-16`** | Two moments when they realized they were still kids , that they were n't __`that thrilled`__ with the Jets brash ways .                                                                  |
    | **`pcc_eng_28_024.1654_x0374101_09:12-13-14`** | My expectations were low going in , but I still was n't __`that thrilled`__ with the book .                                                                                              |
    
    
    3. _that uncommon_
    
    |                                                | `token_str`                                                                                                                                                                                                                              |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_023.7367_x0367629_32:4-5-6`**    | So it 's not __`that uncommon`__ that many would be brides end up frustrated when they are trying to find out the right size .                                                                                                           |
    | **`pcc_eng_18_018.3521_x0280992_30:6-7-8`**    | Around here , it 's not __`that uncommon`__ to cut down your own Christmas tree .                                                                                                                                                        |
    | **`pcc_eng_06_097.9087_x1567518_11:22-23-24`** | However , based on the reports that we have heard it appears that his internal defibrillator fired inappropriately , which is not __`that uncommon`__ of an occurrence with the device .                                                 |
    | **`pcc_eng_20_097.3957_x1557482_06:12-13-14`** | In much of the country , an outdoor swimming pool is n't __`that uncommon`__ .                                                                                                                                                           |
    | **`pcc_eng_14_005.3052_x0069786_23:18-19-20`** | What I learned at the session was that the disturbing experience of learning the policy process is not __`that uncommon`__ -- everyone had a vivid story to tell -- and that some academics think it 's easier to influence practice ... |
    
    
    4. _that surprising_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                        |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_030.3531_x0474996_16:7-8-9`**     | In one way , this is n't __`that surprising`__ -- you mean people have casual sex because they want to , um , have casual sex ?                                                                                                                                                                                                    |
    | **`pcc_eng_20_082.1265_x1310726_057:09-10-11`** | In some ways her decision to return is n't __`that surprising`__ .                                                                                                                                                                                                                                                                 |
    | **`pcc_eng_08_070.3912_x1123558_53:7-8-9`**     | Fan : I think it 's not __`that surprising`__ .                                                                                                                                                                                                                                                                                    |
    | **`nyt_eng_20050413_0318_52:3-4-5`**            | it 's not __`that surprising`__ given that the old distinctions between off-off Broadway -- a term coined in early 1960s by the Village Voice critic Jerry Tallmer to describe the rambunctious theater emerging downtown in coffeeshops , lofts and on other makeshift stages -- and the rest of the theater world have blurred . |
    | **`pcc_eng_18_086.5813_x1385854_33:15-16-17`**  | So , that people are searching less for expensive software tools , maybe is n't __`that surprising`__ .                                                                                                                                                                                                                            |
    
    
    5. _that dissimilar_
    
    |                                                | `token_str`                                                                                                                                                                                                     |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_048.6228_x0769057_13:4-5-6`**    | The process is not __`that dissimilar`__ .                                                                                                                                                                      |
    | **`pcc_eng_27_061.0198_x0970053_13:15-16-17`** | This counterpoint of motherly and gubernatorial duties reveals that the two jobs really are n't __`that dissimilar`__ .                                                                                         |
    | **`pcc_eng_12_003.2043_x0035619_61:11-13-14`** | In other words , mold machining and production machining are not all __`that dissimilar`__ .                                                                                                                    |
    | **`pcc_eng_24_079.7920_x1274570_41:7-8-9`**    | The " twist " ending is not __`that dissimilar`__ to the end of an M. Night Shyamalan movie , but for the fact that it ca n't decide which twist ending it wants .                                              |
    | **`nyt_eng_19961203_0542_19:31-32-33`**        | `` We do a lot of audience mood-checking , '' said MTV Networks president Judy McGrath , `` and the 17 - to 24-year-olds we 've been talking to are not __`that dissimilar`__ from people in other age groups . |
    
    
    6. _that unusual_
    
    |                                                 | `token_str`                                                                                                                                                                                                                         |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19960621_0370_17:4-5-6`**            | `` It is n't __`that unusual`__ for large clients of brokerage houses to get catered to , '' said Ken Steiner , co-founder of the Investors Rights Association of America , a shareholder activist group for individual investors . |
    | **`pcc_eng_19_018.6854_x0285338_7:23-24-25`**   | I think extreme hair loss / balding may be rare with Accutane but it seems like increased shedding , hair damage is not __`that unusual`__ .                                                                                        |
    | **`pcc_eng_26_038.6901_x0609439_53:5-6-7`**     | Although his story was n't __`that unusual`__ , it gave us both pause to wonder at the miracle of life .                                                                                                                            |
    | **`apw_eng_20020409_1548_3:18-20-21`**          | likewise , the fact that this downturn was led by a sharp drop in business investment is not all __`that unusual`__ , according to the study released Tuesday by the International Monetary Fund .                                  |
    | **`pcc_eng_06_077.4075_x1235707_144:26-27-28`** | But aside from Hotaling 's complete lack of business acumen and the wildly ambitious scope of building a Lake Tahoe road , the deal was n't __`that unusual`__ .                                                                    |
    
    
    7. _that noticeable_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                        |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_046.8063_x0740356_43:13-14-15`**  | You can see in the photo below that in daylight it is n't __`that noticeable`__ , but at night or during dusk , dawn , or while you are in a dark thunderstorm or in rainy hard - to - see conditions it is quite bright .                                         |
    | **`pcc_eng_25_089.8592_x1437879_120:46-47-48`** | Map My Ride says 4100 feet of elevation gain for the Century ride ( our Garmins ' ' confirmed that elevation gain ) , so some up and down , especially on the extra loop for the Century riders , but frankly , it was n't __`that noticeable`__ .                 |
    | **`pcc_eng_11_091.1980_x1459969_34:13-15-16`**  | The edges of the fringe will fray a little but it wo n't be __`that noticeable`__ .                                                                                                                                                                                |
    | **`pcc_eng_17_100.1973_x1603440_3:46-47-48`**   | My hair dresser weaved the colour through my natural brown so it 's a little bit more subtle and blends a little better with the top layer of my hair , without looking like I 've dipped my hair in dye ( although it 's not __`that noticeable`__ in the photo ! |
    | **`pcc_eng_11_015.6472_x0237087_6:5-6-7`**      | The water mark is not __`that noticeable`__ as it is in one of the pleats .                                                                                                                                                                                        |
    
    
    8. _that complicated_
    
    |                                                 | `token_str`                                                                                                                                                                                |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_047.9318_x0757826_09:6-7-8`**     | " The Aurora stuff is n't __`that complicated`__ , " He said .                                                                                                                             |
    | **`pcc_eng_02_033.9722_x0533678_073:16-18-19`** | Listen long enough , and you could almost be convinced that an Oswalt trade wo n't be __`that complicated`__ , after all .                                                                 |
    | **`nyt_eng_20000623_0037_101:29-31-32`**        | the Rev. Paul Kang , who ministers to young adults , sat down with a plate of barbecue and explained how California 's Korean Christian revival is really not all __`that complicated`__ . |
    | **`pcc_eng_08_048.9660_x0776429_007:4-5-6`**    | It 's really not __`that complicated`__ , as humans have been using scents to improve their moods and even health for many centuries .                                                     |
    | **`pcc_eng_10_085.6827_x1368612_24:3-5-6`**     | It was not always __`that complicated`__ - or expensive .                                                                                                                                  |
    
    
    9. _that familiar_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_096.3263_x1540156_06:28-30-31`** | You never know just how much these actors understand what they 're in for , and for some reason I get the feeling that Sally Field was n't all __`that familiar`__ with " Between Two Ferns " before sitting down -- though I do admire her brave admission that she hates pennies . |
    | **`pcc_eng_14_036.3618_x0571237_12:3-4-5`**    | I 'm not __`that familiar`__ with the villain Hector Hammond , so I ca n't say whether or not they got that character right , but Hal Jordan was all wrong .                                                                                                                         |
    | **`pcc_eng_11_013.2565_x0198159_74:2-5-6`**    | I never really been __`that familiar`__ with the character .                                                                                                                                                                                                                         |
    | **`pcc_eng_24_079.0079_x1261852_03:5-6-7`**    | Even if you 're not __`that familiar`__ with Microgaming 's output , you 'll have heard of Break da Bank .                                                                                                                                                                           |
    | **`pcc_eng_19_075.1140_x1197347_36:08-10-11`** | " I'll begin with something people are n't really __`that familiar`__ with -- it is apparently one of the habitats of the Atlantic sturgeon , which is a rare fish .                                                                                                                 |
    
    
    10. _that hard_
    
    |                                                  | `token_str`                                                                                                                                                                                        |
    |:-------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_038.4462_x0605502_156:22-25-26`**  | Madeline shares some great insights in this episode , and she stumps me at the end with a question that should n't have been __`that hard`__ to answer !                                           |
    | **`pcc_eng_29_096.6557_x1545327_18:3-4-5`**      | It 's not __`that hard`__ to calculate when you get used to it .                                                                                                                                   |
    | **`pcc_eng_11_060.9128_x0969505_0416:10-12-13`** | I already have the speedo , so it would n't be __`that hard`__ .                                                                                                                                   |
    | **`pcc_eng_12_038.2592_x0602633_39:31-32-33`**   | There 's obviously a learning curve to the pricing scheme , and a number of Yelpers in Boston have apparently not understood it ( although , frankly , it 's not __`that hard`__ to understand ) . |
    | **`pcc_eng_13_030.5306_x0477595_14:3-4-5`**      | It was n't __`that hard`__ to draw freehand , but I did have to be pretty precise to make it look good .                                                                                           |
    
    
    11. _that keen_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_033.2977_x0521436_25:5-6-7`**    | At first we were n't __`that keen`__ but then she explained that we would be compensated well , in cash , in the currency of our choice , or we could take slightly more money in flight vouchers .                                                                                                                                                       |
    | **`nyt_eng_20000627_0091_7:5-7-8`**            | initially , we were n't all __`that keen`__ on it , but we sat down and realized that in some way the essence of this band is going out and playing live , sweating , acting , all that stuff .                                                                                                                                                           |
    | **`pcc_eng_02_006.1661_x0083568_03:12-13-14`** | This is most especially true of the average person who is not __`that keen`__ on delving into the world of market shares and finance .                                                                                                                                                                                                                    |
    | **`pcc_eng_08_106.3951_x1706546_38:25-26-27`** | Unlike China , which used its foreign educated nationals to bring back know-hows to build its technology , to my knowledge , India is not __`that keen`__ .                                                                                                                                                                                               |
    | **`pcc_eng_05_085.1434_x1361668_08:40-41-42`** | T here was a meeting on site with John Brewer , head of the RMS bicycle section ( too pesky / successful , so they abolished it ) , and he told his second in command , who was n't __`that keen`__ on doing anything , " just do it " , referring to putting in a light phase for northbound cyclists so they could access the western unused footpath . |
    
    
    12. _that impressive_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                       |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_047.8399_x0757784_06:32-34-35`**  | By the Sword and the Cross is the furthest thing from Power Metal , as much of the album is a straight forward traditional opera , and one that really is n't all __`that impressive`__ too , leaving this CD with much to be desired , but really , is still better then you would expect .                                                                      |
    | **`pcc_eng_26_038.9035_x0612948_004:5-6-7`**    | The technical part is n't __`that impressive`__ , it 's based on overused patterns all the way , but the execution and especially the atmosphere these guys manage to create is amazing , exactly what you 'd expect from a death- inspired Death Metal band if I may say so .                                                                                    |
    | **`pcc_eng_00_001.2833_x0004583_093:18-19-20`** | Tillman 's numbers at the big league level ( 2 - 5 , 5.20 ERA ) were n't __`that impressive`__ , but he has been outstanding at Triple - A two -seasons running , so it 's only a matter of time before he 's in Baltimore for good .                                                                                                                             |
    | **`pcc_eng_03_034.0886_x0535983_20:31-32-33`**  | I realised something while taking screencaps for this episode - there are no interesting images in it ; even the famous ' Sea Devils rising from the ocean ' is n't __`that impressive`__ because there 's only six of them , they are n't in sync , and the stuntmen have clearly been on their hands and knees just beneath the surface waiting for their cue . |
    | **`pcc_eng_20_032.9692_x0516915_119:13-14-15`** | However , they seemed to be mercenaries , but their abilities are n't __`that impressive`__ . "                                                                                                                                                                                                                                                                   |
    
    
    13. _that fond_
    
    |                                                | `token_str`                                                                                                                                                          |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19970508_0321_17:17-18-19`**        | in 1989 he played a defrocked priest in `` Drugstore Cowboy , '' but he is not __`that fond`__ of film work .                                                        |
    | **`pcc_eng_18_007.2469_x0101063_33:31-32-33`** | Serves 4 Growing up in a family where soup is such an important and well - loved dish can be pretty hard if you are a ten year old and not __`that fond`__ of soup . |
    | **`pcc_eng_22_011.0121_x0161545_14:4-5-6`**    | Usually I 'm not __`that fond`__ of these characters , but I just attached to Wash .                                                                                 |
    | **`pcc_eng_23_004.4824_x0056014_58:16-17-18`** | 2 ) I 'm known as a wacko cat lady , but I 'm actually not __`that fond`__ of most cats .                                                                            |
    | **`pcc_eng_18_002.6012_x0026108_06:15-18-19`** | I could never get enough of it as a child although my daughter is n't quite yet __`that fond`__ of vegetables .                                                      |
    
    
    14. _that comfortable_
    
    |                                                 | `token_str`                                                                                                                             |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_081.5663_x1304741_22:20-21-22`**  | The problem is , it 's sometimes hard to look for exactly what you need , and it 's not __`that comfortable`__ .                        |
    | **`pcc_eng_03_080.9012_x1293838_07:10-12-13`**  | Once you put them on , bras just are n't all __`that comfortable`__ , especially if you have actual breasts .                           |
    | **`pcc_eng_13_032.1264_x0503315_108:16-17-18`** | " Our typical customers are in their early to mid-30s and initially , they were not __`that comfortable`__ about ordering online .      |
    | **`pcc_eng_17_100.8848_x1614480_27:11-13-14`**  | I felt as if we were family and I have never been __`that comfortable`__ with any other Dr. and this was my eyes we were working with . |
    | **`nyt_eng_20000608_0058_31:6-8-9`**            | `` Just going outside is n't all __`that comfortable`__ if you do n't have the shade and somewhere comfortable to sit . ''              |
    
    
    15. _that clear_
    
    |                                                | `token_str`                                                                                                                                                                                                               |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_015.4255_x0232954_55:09-10-11`** | " In most other markets the process is not __`that clear`__ , and most of the time you have to go through a cumbersome process of getting clearance from different regulators . "                                         |
    | **`nyt_eng_20050226_0001_14:17-19-20`**        | Conroy was wearing one of his father 's mail carrier uniforms , for reasons that are not all __`that clear`__ .                                                                                                           |
    | **`pcc_eng_03_031.7645_x0498330_18:5-6-7`**    | The release date is not __`that clear`__ though , " within the next couple of weeks " is the official word so far .                                                                                                       |
    | **`pcc_eng_11_007.5687_x0106281_17:21-22-23`** | I wanted to hug them , I wanted to tell them that everything would be okay , but it was n't __`that clear`__ .                                                                                                            |
    | **`pcc_eng_00_064.0823_x1019910_32:10-11-12`** | " The actual truth is , the picture is n't __`that clear`__ , but we can piece it together , and that 's not satisfying to people who are used to saying , ' You can attach this attack to that group , ' " said Miller . |
    
    
    16. _that popular_
    
    |                                                | `token_str`                                                                                                               |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_018.7292_x0286046_05:4-5-6`**    | Even though is not __`that popular`__ , I consider it one of the most awesome series I 've watched .                      |
    | **`pcc_eng_21_090.4720_x1446076_11:08-09-10`** | It is ( was , rather ) not __`that popular`__ , but this comic includes everything .                                      |
    | **`pcc_eng_21_099.1619_x1585951_33:3-4-5`**    | She is n't __`that popular`__ in Twitter either .                                                                         |
    | **`pcc_eng_00_038.5096_x0605929_10:09-10-11`** | " Back then , girl 's softball was not __`that popular`__ , but in this day and time , softball has become very popular . |
    | **`pcc_eng_06_073.4207_x1171468_04:6-8-9`**    | I know the BLM is n't all __`that popular`__ , but their presence is hard to ignore .                                     |
    
    
    17. _that simple_
    
    |                                                 | `token_str`                                                                                                                                                      |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_011.0679_x0162754_66:6-7-8`**     | But the healthcare debate is not __`that simple`__ .                                                                                                             |
    | **`pcc_eng_15_091.7520_x1466952_068:08-09-10`** | As with most things , it is n't __`that simple`__ .                                                                                                              |
    | **`pcc_eng_00_043.6098_x0688494_24:5-7-8`**     | Of course it ca n't be __`that simple`__ .                                                                                                                       |
    | **`apw_eng_20020727_0475_20:6-7-8`**            | the boycott 's effect is not __`that simple`__ , however , according to economists and government officials .                                                    |
    | **`nyt_eng_19971208_0431_4:3-6-7`**             | it may not be quite __`that simple`__ , but the gene mutation undoubtedly wipes out much of the healthy fear that underlies the instinct for self-preservation . |
    
    
    18. _that easy_
    
    |                                                | `token_str`                                                                                                                                                                              |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_034.4514_x0540449_10:4-5-6`**    | But it is n't __`that easy`__ very often .                                                                                                                                               |
    | **`pcc_eng_26_034.7029_x0544788_27:14-15-16`** | In terms of where the society is right now , it 's still not __`that easy`__ and hopefully it will make things easier now .                                                              |
    | **`pcc_eng_18_086.3243_x1381689_100:4-5-6`**   | That customization is n't __`that easy`__ to achieve though , as it typically requires demon fusion , and thus a lot of thought has to go into how best to achieve the desired results . |
    | **`pcc_eng_22_105.0666_x1681508_08:13-15-16`** | That is why , making sure that every moment is accounted will not be __`that easy`__ and you have to think of something that can fill the gaps .                                         |
    | **`pcc_eng_04_084.3729_x1346954_42:5-6-7`**    | Having an impact is not __`that easy`__ .                                                                                                                                                |
    
    
    19. _that big_
    
    |                                                | `token_str`                                                                                                                                                                        |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_030.6363_x0478966_43:22-23-24`** | Details like this would be hard to fix with the limited face buttons on a controller , but thankfully it is n't __`that big`__ of a deal .                                         |
    | **`pcc_eng_27_024.8756_x0385780_23:14-16-17`** | The space allotted to Stefano at what was once Hot Sip Cafe may not be __`that big`__ , but apart from being a barista he is also a DJ so is used to working in a confined space . |
    | **`pcc_eng_11_018.6954_x0286208_25:08-09-10`** | We 're not wealthy , we 're not __`that big`__ , but we have clear direction and we want to save them . "                                                                          |
    | **`pcc_eng_11_099.6409_x1596793_051:3-4-5`**   | It was n't __`that big`__ of a leap to , in some ways , have no director .                                                                                                         |
    | **`nyt_eng_19961213_0545_37:3-5-6`**           | Fairlane wo n't get __`that big`__ in its first five years but `` it will have some recognizable-sized profits in three , four or five years , '' Odom said .                      |
    
    
    20. _that great_
    
    |                                                | `token_str`                                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_050.7357_x0803614_24:4-5-6`**    | Maybe they were n't __`that great`__ when you think of solid classic-rock groups , but their arena shows touched a lot of lives .                                                                                                           |
    | **`pcc_eng_15_046.8822_x0741801_54:4-5-6`**    | " Hollywood is not __`that great`__ at coming up with original scripts , " Masand says .                                                                                                                                                    |
    | **`pcc_eng_12_043.1643_x0681770_39:4-6-7`**    | And he was n't all __`that great`__ if he did n't do anything about it .                                                                                                                                                                    |
    | **`pcc_eng_28_065.0173_x1035870_20:19-20-21`** | I work on lots of computers I find most computer repair winnipeg tends to give us to be not __`that great`__ .                                                                                                                              |
    | **`pcc_eng_12_086.6328_x1383728_05:4-5-6`**    | The sound was not __`that great`__ due to the fact that we went just after lunch and there was a lot of clanking of dishes and silverware , but we did manage to get some good information regarding both the harvest and the biodigester . |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/...
    
    Samples saved as...
    1. `neg_bigram_examples/that/that_far-fetched_99ex.csv`
    1. `neg_bigram_examples/that/that_thrilled_99ex.csv`
    1. `neg_bigram_examples/that/that_uncommon_99ex.csv`
    1. `neg_bigram_examples/that/that_surprising_99ex.csv`
    1. `neg_bigram_examples/that/that_dissimilar_99ex.csv`
    1. `neg_bigram_examples/that/that_unusual_99ex.csv`
    1. `neg_bigram_examples/that/that_noticeable_99ex.csv`
    1. `neg_bigram_examples/that/that_complicated_99ex.csv`
    1. `neg_bigram_examples/that/that_familiar_99ex.csv`
    1. `neg_bigram_examples/that/that_hard_99ex.csv`
    1. `neg_bigram_examples/that/that_keen_99ex.csv`
    1. `neg_bigram_examples/that/that_impressive_99ex.csv`
    1. `neg_bigram_examples/that/that_fond_99ex.csv`
    1. `neg_bigram_examples/that/that_comfortable_99ex.csv`
    1. `neg_bigram_examples/that/that_clear_99ex.csv`
    1. `neg_bigram_examples/that/that_popular_99ex.csv`
    1. `neg_bigram_examples/that/that_simple_99ex.csv`
    1. `neg_bigram_examples/that/that_easy_99ex.csv`
    1. `neg_bigram_examples/that/that_big_99ex.csv`
    1. `neg_bigram_examples/that/that_great_99ex.csv`
    
    ## 3. *exactly*
    
    |                     |        `N` |      `f1` |   `adv_total` |
    |:--------------------|-----------:|----------:|--------------:|
    | **NEGATED_exactly** | 72,839,589 | 3,173,660 |        58,643 |
    | **NEGMIR_exactly**  |  1,701,929 |   291,732 |         1,041 |
    
    
    |                               |   `f` |   `adj_total` |   `dP1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:------------------------------|------:|--------------:|--------:|--------:|----------:|----------:|------------:|-------:|
    | **NEGany~exactly_conducive**  |   208 |         9,110 |    0.96 |    7.82 |  1,303.50 |      9.06 |      198.94 |    208 |
    | **NEGany~exactly_shocking**   |   151 |        35,115 |    0.96 |    7.33 |    946.29 |      6.58 |      144.42 |    151 |
    | **NEGany~exactly_pleasant**   |   142 |        52,223 |    0.96 |    7.24 |    889.88 |      6.19 |      135.81 |    142 |
    | **NEGany~exactly_famous**     |   130 |       223,813 |    0.96 |    7.10 |    814.68 |      5.66 |      124.34 |    130 |
    | **NEGany~exactly_difficult**  |   126 |       732,106 |    0.96 |    7.05 |    789.62 |      5.49 |      120.51 |    126 |
    | **NEGany~exactly_easy**       | 1,066 |       579,827 |    0.95 |    9.32 |  6,596.91 |     46.75 |    1,019.25 |  1,073 |
    | **NEGany~exactly_cheap**      |   691 |        60,531 |    0.95 |    8.96 |  4,281.59 |     30.28 |      660.72 |    695 |
    | **NEGany~exactly_surprising** |   440 |        70,540 |    0.95 |    8.71 |  2,743.34 |     19.21 |      420.79 |    441 |
    | **NEGany~exactly_new**        | 1,371 |       253,862 |    0.94 |    9.10 |  8,410.32 |     60.48 |    1,310.52 |  1,388 |
    | **NEGany~exactly_clear**      | 1,746 |       349,214 |    0.94 |    8.78 | 10,578.33 |     77.73 |    1,668.27 |  1,784 |
    | **NEGmir~exactly_sure**       |   148 |         6,761 |    0.83 |    5.31 |    522.11 |     25.37 |      122.63 |    148 |
    | **NEGmir~exactly_easy**       |    20 |        18,610 |    0.83 |    1.86 |     70.55 |      3.43 |       16.57 |     20 |
    | **NEGmir~exactly_clear**      |    52 |         6,722 |    0.81 |    3.38 |    173.89 |      9.08 |       42.92 |     53 |
    | **NEGmir~exactly_new**        |    29 |        12,836 |    0.80 |    2.31 |     93.90 |      5.14 |       23.86 |     30 |
    
    
    1. _exactly conducive_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_024.8862_x0386333_03:7-8-9`**    | However , Garcia 's style is n't __`exactly conducive`__ to having his hand raised either and has resulted in 3 - 6 - 1 record in his last ten tilts including losses in a quartet of consecutive clashes .                                                                                                                                                                                               |
    | **`pcc_eng_29_035.8399_x0562315_34:12-13-14`** | The anticipatory anxiety of competing in a tenuous job market is n't __`exactly conducive`__ to cutting class in order to shout into a megaphone and possibly get arrested .                                                                                                                                                                                                                              |
    | **`pcc_eng_20_009.0365_x0129691_17:66-67-68`** | granted , not a whole lot gets done between noon and late afternoon - the arabs probably have an equivalent word for " siesta " - but seriously : no wonder they are stuck in the seventh century - a four to six hour workday in a land of near constant tribal and sectarian warfare , poor infrastructure and spotty water and electrical service is not __`exactly conducive`__ to productivity ..... |
    | **`nyt_eng_20050511_0215_17:19-20-21`**        | as one employee told me , `` Spiritually , it 's a great place to be , but not __`exactly conducive`__ to business efficiency . ''                                                                                                                                                                                                                                                                        |
    | **`pcc_eng_15_094.6330_x1513402_38:11-12-13`** | Hearing " Billie Jean is not my lover " is not __`exactly conducive`__ to price comparisons .                                                                                                                                                                                                                                                                                                             |
    
    
    2. _exactly shocking_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                           |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_059.7527_x0949024_11:3-4-5`**    | Again , not __`exactly shocking`__ .                                                                                                                                                                                                                                  |
    | **`nyt_eng_20000418_0011_23:4-5-6`**           | but it was n't __`exactly shocking`__ , not for a man who has worked with the league owners since 1993 and was a known quantity within baseball 's political circle .                                                                                                 |
    | **`pcc_eng_14_040.1242_x0632050_06:12-13-14`** | As unfortunate as it may be , Enstrom falling injured is n't __`exactly shocking`__ .                                                                                                                                                                                 |
    | **`pcc_eng_05_039.7603_x0627335_36:26-27-28`** | Although I do n't know how much credence to give to these hacked emails , supposedly between billionaire George Soros and Poroshenko , it 's not __`exactly shocking`__ if the former is indeed lobbying the Federal Reserve to swap out Ukraine 's burgeoning debt . |
    | **`pcc_eng_18_001.0110_x0000163_23:3-4-5`**    | It 's not __`exactly shocking`__ , since , yes , the bull 's -eye on Gaylen 's head has been growing larger by the week , but the assassination 's quickness hits harder than expected .                                                                              |
    
    
    3. _exactly pleasant_
    
    |                                                | `token_str`                                                                                                                       |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_030.1133_x0471369_64:09-10-11`** | Some of what we 've got planned is n't __`exactly pleasant`__ for the main characters , but I think it 's good fodder for drama . |
    | **`pcc_eng_29_002.1372_x0018227_22:08-09-10`** | Walking along or near El Camino is n't __`exactly pleasant`__ .                                                                   |
    | **`pcc_eng_25_092.0955_x1474076_57:1-3-4`**    | Not an __`exactly pleasant`__ to note to end this letter from the field with , I 'm afraid .                                      |
    | **`pcc_eng_08_103.7745_x1664023_19:7-8-9`**    | So , yeah , it 's not __`exactly pleasant`__ .                                                                                    |
    | **`pcc_eng_12_039.1205_x0616647_22:16-17-18`** | This is completely normal , painless , and nothing to be alarmed by ( but not __`exactly pleasant`__ , either ) .                 |
    
    
    4. _exactly famous_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                          |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_052.4971_x0832024_08:3-4-5`**     | Britain is n't __`exactly famous`__ for producing top quality Ice Hockey players .                                                                                                                                                                                                                                                   |
    | **`nyt_eng_20050731_0018_8:24-25-26`**          | under THE RADAR : Although he is one of the few successful athletes to come out of Luxembourg , Muller said he is n't __`exactly famous`__ in his home country .                                                                                                                                                                     |
    | **`pcc_eng_23_096.9361_x1550526_02:5-6-7`**     | The tech industry is not __`exactly famous`__ for its diversity .                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_00_030.7457_x0480797_24:51-52-53`**  | Before joining Honor , she had worked with unions and union-backed organizations for her entire career , from an job as an organizer for the SEIU in San Jose to leadership roles at multiple union- backed think tanks -- a rare C.V. for an executive in an industry that 's not __`exactly famous`__ for its pro-union politics . |
    | **`pcc_eng_19_014.0259_x0210478_066:09-10-11`** | Whenever you are searching for something that is not __`exactly famous`__ , such as aliens , be sure to put these tools to use so that you can get the widest variety of sources possible .                                                                                                                                          |
    
    
    5. _exactly difficult_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                         |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_016.9996_x0258159_32:15-16-17`**  | This has been happening for 40 years in America , and the statistics are n't __`exactly difficult`__ to find :                                                                                                                                                      |
    | **`pcc_eng_27_051.6030_x0817819_026:21-22-23`** | Not many schools better than Uof C , and small class size makes it so getting big firm job is n't __`exactly difficult`__ .                                                                                                                                         |
    | **`pcc_eng_29_099.6666_x1594121_08:26-27-28`**  | As we 've lamented over these past few months , television has never felt more cluttered with gold and garbage , and while it 's not __`exactly difficult`__ to discern between the two , it 's certainly taxing .                                                  |
    | **`pcc_eng_26_081.3851_x1299624_41:3-4-5`**     | It 's not __`exactly difficult`__ to find fault with Ilsa , the Tigress of Siberia , but I ask you -- where the hell else are you going to see another non-Soviet movie made during the Brezhnev era in which the motherfucking KGB end up being the good guys ?!?! |
    | **`pcc_eng_27_001.3368_x0005312_24:27-28-29`**  | Ryan finally sees Joe in person again in " Fly Away , " and Joe continues to out -smart him at every turn , which is n't __`exactly difficult`__ these days .                                                                                                       |
    
    
    6. _exactly surprising_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_045.7611_x0724394_18:12-13-14`** | Given how clearly horned - up young Conrad is it 's not __`exactly surprising`__ that he makes a beeline for Rush 's crotch ; pulling away the buff beauty 's briefs , then promptly slurping on the handsome fuck - rod that he discovers straining inside . |
    | **`pcc_eng_07_028.7930_x0449616_10:27-28-29`** | That a team executive in the league with the most embattled officiating corps would promote a tool that would create greater transparency on the court is n't __`exactly surprising`__ ; you can also expect that league 's resistance to such a tool .       |
    | **`pcc_eng_10_026.3365_x0409417_14:1-5-6`**    | None of this is __`exactly surprising`__ .                                                                                                                                                                                                                    |
    | **`pcc_eng_03_036.4650_x0574398_15:6-7-8`**    | While shocking , it 's not __`exactly surprising`__ .                                                                                                                                                                                                         |
    | **`pcc_eng_13_001.7711_x0012369_14:3-4-5`**    | That 's not __`exactly surprising`__ , as Iran is on the cusp of reaping serious economic benefits if / when sanctions will be suspended .                                                                                                                    |
    
    
    7. _exactly cheap_
    
    |                                                | `token_str`                                                                                                                                                                         |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_029.3065_x0458020_20:2-3-4`**    | Still not __`exactly cheap`__ but the facilities , view , and demand for tickets were much higher than the horribly supported Monday Night borefest that was the Sharks vs Titans . |
    | **`pcc_eng_14_095.8160_x1532919_30:7-8-9`**    | Mind you ; this service is n't __`exactly cheap`__ .                                                                                                                                |
    | **`pcc_eng_08_049.5286_x0785496_3:6-7-8`**     | However , the permits are not __`exactly cheap`__ and there are so many rules as to where you can park at what times .                                                              |
    | **`pcc_eng_05_044.3506_x0701758_29:10-11-12`** | Mexico 's stocks appear a lot cheaper , if not __`exactly cheap`__ .                                                                                                                |
    | **`pcc_eng_03_005.9244_x0079605_74:10-11-12`** | Security services , especially top tier ones , are n't __`exactly cheap`__ .                                                                                                        |
    
    
    8. _exactly easy_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_004.4281_x0055554_34:24-25-26`**  | For example , you might not be a hardliner about interviewees being on -time , especially if you 're located somewhere that 's not __`exactly easy`__ to find on a map .                                                                                                |
    | **`pcc_eng_14_031.3952_x0491214_04:21-22-23`**  | It 's solitary , introspective , predicated on long hours spent working without human contact , and while it 's never __`exactly easy`__ , it 's much less difficult when your temperament naturally tends in that direction .                                          |
    | **`pcc_eng_24_102.7488_x1646139_18:14-15-16`**  | I know I 'm pretty fortunate in this regard - although gluten is n't __`exactly easy`__ to avoid in everyday situations , it is the only thing I have to be super careful about food -wise , so I get the privilege of experiencing carefree snacking at these events . |
    | **`pcc_eng_21_098.4074_x1573697_11:16-17-18`**  | One drawback of being an amateur- built site is that the Dirty Tony tour is not __`exactly easy`__ to navigate .                                                                                                                                                        |
    | **`pcc_eng_01_042.6757_x0673421_570:17-18-19`** | And this is a dog that has now caught a jackrabbit - and believe me that aint __`exactly easy`__ !                                                                                                                                                                      |
    
    
    9. _exactly new_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                       |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_089.2805_x1429013_02:4-5-6`**     | Television crossovers are not __`exactly new`__ , and typically come during sweeps week and are advertised as big " events " to try to draw big ratings .                                                                                                         |
    | **`nyt_eng_20070404_0165_22:18-19-20`**         | this strategy seemed surprising to University of South Florida marketing professor Gary Gebhardt , since Botox is n't __`exactly new`__ .                                                                                                                         |
    | **`pcc_eng_27_003.6824_x0043053_06:5-6-7`**     | Well , that 's not __`exactly new`__ or special , since most airlines have long done this .                                                                                                                                                                       |
    | **`pcc_eng_21_067.9588_x1082078_076:21-22-23`** | We already has as you just noted , we had free downloads in our own store , so it 's not __`exactly new`__ to our apps on the Mac .                                                                                                                               |
    | **`pcc_eng_28_046.3892_x0734466_08:24-25-26`**  | I 'm not doing anything particularly interesting with my life that would be worth reading , I write reviews of things that are n't __`exactly new`__ , and I feature things I find on the net that get to people faster by word of mouth than by word- of- blog . |
    
    
    10. _exactly clear_
    
    |                                                | `token_str`                                                                                                                                                                                                                         |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_067.1668_x1069339_04:23-24-25`** | Earlier today we reported that despite , or rather due to , all the confusing propaganda from either side , it was not __`exactly clear`__ whether and how far away from Baghdad the ISIS offensive had been halted ( if at all ) . |
    | **`pcc_eng_12_008.8598_x0127105_049:4-5-6`**   | Also it was n't __`exactly clear`__ what type of work the man was doing on Sunday .                                                                                                                                                 |
    | **`pcc_eng_15_098.2211_x1571324_09:5-6-7`**    | At first it was n't __`exactly clear`__ to me how critical an issue this was to the project 's financial security , confidence and credibility .                                                                                    |
    | **`pcc_eng_02_019.8112_x0304469_12:7-8-9`**    | How the eobo left Korea is n't __`exactly clear`__ .                                                                                                                                                                                |
    | **`pcc_eng_16_082.0609_x1311873_05:15-16-17`** | While Dish has said that the Blockbuster name will live on , it is n't __`exactly clear`__ where that might be .                                                                                                                    |
    
    
    11. _exactly sure_
    
    |                                                | `token_str`                                                                                                                                                                                       |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_004.6487_x0058722_106:1-2-3`**   | Not __`exactly sure`__ what their mascot is supposed to be .                                                                                                                                      |
    | **`pcc_eng_17_004.8234_x0061798_13:16-17-18`** | So , this could also happen to the Surface Pro 3 , but we 're not __`exactly sure`__ .                                                                                                            |
    | **`apw_eng_19970910_0206_19:4-5-6`**           | `` I was not __`exactly sure`__ that he was really injured .                                                                                                                                      |
    | **`pcc_eng_18_008.1393_x0115540_9:3-4-5`**     | We 're not __`exactly sure`__ what the holdup is with the other apps , but it could have something to do with the enormous cost of serving all that heavy - bandwidth HD video at massive scale . |
    | **`pcc_eng_18_036.8739_x0580489_16:21-22-23`** | Just found out I am going ( Paddock , not stands ) with my friends and my girlfriend , and not __`exactly sure`__ what to wear .                                                                  |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/...
    
    Samples saved as...
    1. `neg_bigram_examples/exactly/exactly_conducive_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_shocking_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_pleasant_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_famous_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_difficult_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_surprising_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_cheap_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_easy_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_new_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_clear_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_sure_99ex.csv`
    
    ## 4. *any*
    
    |                 |        `N` |      `f1` |   `adv_total` |
    |:----------------|-----------:|----------:|--------------:|
    | **NEGMIR_any**  |  1,701,929 |   291,732 |         1,197 |
    | **NEGATED_any** | 72,839,589 | 3,173,660 |        34,382 |
    
    
    |                          |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:-------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGmir~any_younger**   |    20 |           939 |    0.83 |    1.86 |    70.55 |      3.43 |       16.57 |     20 |
    | **NEGmir~any_clearer**   |    17 |           130 |    0.83 |    1.50 |    59.97 |      2.91 |       14.09 |     17 |
    | **NEGany~any_happier**   |   828 |        16,606 |    0.82 |    6.34 | 4,420.49 |     41.96 |      786.04 |    963 |
    | **NEGmir~any_different** |    48 |        36,166 |    0.81 |    3.24 |   159.93 |      8.40 |       39.60 |     49 |
    | **NEGmir~any_bigger**    |    36 |         3,923 |    0.80 |    2.73 |   118.17 |      6.34 |       29.66 |     37 |
    | **NEGany~any_younger**   |   255 |        26,216 |    0.79 |    5.57 | 1,323.36 |     13.38 |      241.62 |    307 |
    | **NEGany~any_nicer**     |    96 |         9,955 |    0.76 |    4.75 |   486.82 |      5.18 |       90.82 |    119 |
    | **NEGmir~any_easier**    |    61 |         2,386 |    0.75 |    3.04 |   181.65 |     11.31 |       49.69 |     66 |
    | **NEGmir~any_better**    |   380 |        14,013 |    0.74 |    4.38 | 1,096.01 |     71.82 |      308.18 |    419 |
    | **NEGmir~any_good**      |    32 |        31,585 |    0.74 |    2.12 |    93.53 |      6.00 |       26.00 |     35 |
    | **NEGmir~any_higher**    |    21 |         2,893 |    0.74 |    1.42 |    61.24 |      3.94 |       17.06 |     23 |
    | **NEGany~any_simpler**   |   226 |        23,480 |    0.71 |    5.00 | 1,087.71 |     13.07 |      212.93 |    300 |
    | **NEGany~any_brighter**  |    63 |         9,280 |    0.67 |    3.91 |   292.00 |      3.83 |       59.17 |     88 |
    | **NEGmir~any_worse**     |    87 |         8,790 |    0.66 |    2.73 |   217.46 |     18.00 |       69.00 |    105 |
    | **NEGmir~any_closer**    |    57 |           993 |    0.65 |    2.33 |   141.82 |     11.83 |       45.17 |     69 |
    | **NEGany~any_smarter**   |    89 |         8,501 |    0.63 |    4.00 |   394.95 |      5.75 |       83.25 |    132 |
    | **NEGany~any_easier**    | 1,594 |       209,940 |    0.62 |    5.08 | 6,987.78 |    104.79 |    1,489.21 |  2,405 |
    | **NEGany~any_cheaper**   |   129 |        46,055 |    0.58 |    4.01 |   542.97 |      8.98 |      120.02 |    206 |
    | **NEGany~any_clearer**   |   355 |        11,680 |    0.54 |    4.26 | 1,421.60 |     26.49 |      328.51 |    608 |
    | **NEGany~any_worse**     | 1,686 |       179,012 |    0.42 |    3.94 | 5,676.37 |    160.03 |    1,525.97 |  3,673 |
    
    
    1. _any younger_
    
    |                                         | `token_str`                                                                                                                                                                                        |
    |:----------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20050402_0206_25:17-19-20`** | then again , in the field , Darin Erstad , Garret Anderson and Steve Finley are n't getting __`any younger`__ .                                                                                    |
    | **`apw_eng_19981107_0088_6:13-15-16`**  | another said : `` As long as we live , we 're not getting __`any younger`__ , but to be alive is wonderful _ no matter how much we suffer . ''                                                     |
    | **`nyt_eng_20061015_0016_8:4-6-7`**     | `` We 're not getting __`any younger`__ .                                                                                                                                                          |
    | **`apw_eng_20080104_0053_16:11-13-14`** | `` This is the last moment because these women are not getting __`any younger`__ and should be compensated for their suffering , '' says Stefan Sliwinski , the son of one of the prison mothers . |
    | **`apw_eng_20080703_0375_25:5-7-8`**    | `` My husband is not getting __`any younger`__ -- nor am I for that matter -- but he is of course under more stress , '' she said .                                                                |
    
    
    2. _any clearer_
    
    |                                                 | `token_str`                                                                                                                                                                          |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_082.3696_x1315575_08:10-12-13`**  | And for what it 's worth , they 've never been __`any clearer`__ about their criteria in previous years either .                                                                     |
    | **`pcc_eng_20_083.9583_x1340490_035:34-35-36`** | I get Young Adult and I get Adult Fiction but I ca n't quite get my head around this new concept ; I could n't before I read this book and I 'm not __`any clearer`__ about it now . |
    | **`pcc_eng_18_019.2275_x0295083_06:12-14-15`**  | Here 's what the Official Guide says , it literally could n't be __`any clearer`__ :                                                                                                 |
    | **`pcc_eng_19_012.7393_x0189667_12:3-4-5`**     | It 's not __`any clearer`__ to the players inside the Capitol .                                                                                                                      |
    | **`pcc_eng_29_033.5068_x0524668_30:3-5-6`**     | It could not be __`any clearer`__ to me that most Americans have tired of the war on drugs .                                                                                         |
    
    
    3. _any happier_
    
    |                                                | `token_str`                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_055.1819_x0875672_18:17-19-20`** | I have done months of pricing and research before I committed to buying this and could n't be __`any happier`__ with the quality , effects and durability of this outstanding mixer !                                                      |
    | **`pcc_eng_13_038.6784_x0609244_17:17-19-20`** | On average we 've saved hundreds already this year by using the steps above and could n't be __`any happier`__ .                                                                                                                           |
    | **`pcc_eng_01_049.1947_x0778788_080:3-6-7`**   | She could n't have been __`any happier`__ and so were all of her guests for her .                                                                                                                                                          |
    | **`pcc_eng_27_066.1860_x1053780_05:10-12-13`** | We are finally tying the knot and we could n't be __`any happier`__ or excited .                                                                                                                                                           |
    | **`pcc_eng_07_025.2221_x0391840_29:41-43-44`** | " For what it meant not just off of some big opening weekends but for the playability over the last couple of months and really for what it means in setting up the franchise for the future , everyone could n't be __`any happier`__ . " |
    
    
    4. _any different_
    
    |                                              | `token_str`                                                                                                                                                                                                |
    |:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_045.2144_x0715871_29:6-7-8`**  | An industrial plumbing process is not __`any different`__ than a residential plumbing system .                                                                                                             |
    | **`apw_eng_20020418_1914_21:23-24-25`**      | but Orban rejects opposition accusations that his aggressive style sometimes pushes the limits of what 's acceptable , saying the campaign was not __`any different`__ from those in Western democracies . |
    | **`nyt_eng_19991216_0077_42:4-5-6`**         | `` We 're not __`any different`__ than other teams that go through the highs and lows in a year , '' Rob DiMaio said .                                                                                     |
    | **`apw_eng_20020825_0386_12:6-8-9`**         | `` Zalaegerszeg 's attitude wo n't be __`any different`__ from the first game _ but ours will be .                                                                                                         |
    | **`pcc_eng_14_044.7704_x0707133_280:7-8-9`** | In this regard , you are n't __`any different`__ than any other sign .                                                                                                                                     |
    
    
    5. _any bigger_
    
    |                                                 | `token_str`                                                                                                                                                                     |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_055.7739_x0885921_24:11-12-13`**  | said : " Oh , I would say it was not __`any bigger`__ than a dime . "                                                                                                           |
    | **`pcc_eng_00_060.9113_x0968572_499:15-16-17`** | There was no evidence of trauma other than some scratches on his forehead , not __`any bigger`__ than he would have gotten playing out back with Cole or falling off his bike . |
    | **`pcc_eng_17_049.1971_x0778659_23:19-20-21`**  | " That 's right , Sweetie , we were a little north of there , and it was n't __`any bigger`__ even then .                                                                       |
    | **`nyt_eng_19990714_0148_4:08-10-11`**          | for women 's sports , it does n't get __`any bigger`__ than this .                                                                                                              |
    | **`pcc_eng_19_016.0255_x0242390_13:28-29-30`**  | I really liked the course , with the mix of singletrack and fields , but it was a short lap and I 'm glad the field was n't __`any bigger`__ !                                  |
    
    
    6. _any nicer_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_027.5885_x0429794_089:3-6-7`**   | He could n't have been __`any nicer`__ .                                                                                                                                                                                                                                                                                                                                                               |
    | **`pcc_eng_24_028.5471_x0445389_33:62-63-64`** | After this there is some vain effort of the movie to create a Snow White type story except instead of killing the daughter the stepmother wants to kill the Prince , at which point the movie kills off all of the boyfriends and ends with a cliffhanger where the nice boy , or in this case " the boy who is n't __`any nicer`__ but looks the most like Adam Sandler " is about to kiss the girl . |
    | **`pcc_eng_07_023.8043_x0368677_36:08-10-11`** | When I visit my Mom they could not be __`any nicer`__ and I feel welcome .                                                                                                                                                                                                                                                                                                                             |
    | **`pcc_eng_16_036.4489_x0573735_48:4-5-6`**    | The house was n't __`any nicer`__ than ours , but it did have an indoor toilet .                                                                                                                                                                                                                                                                                                                       |
    | **`nyt_eng_19990711_0051_75:04-10-11`**        | `` There 's nobody in this world that 's __`any nicer`__ than those people , '' Breen said of the Wildermuths .                                                                                                                                                                                                                                                                                        |
    
    
    7. _any easier_
    
    |                                                 | `token_str`                                                                                                                                                        |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_036.6205_x0575486_062:19-21-22`** | 5 ) For socialists outside the West , the task is a much more straightforward one , if not therefore __`any easier`__ and considerably more dangerous .            |
    | **`apw_eng_20080829_0756_6:4-6-7`**             | her task did not seem __`any easier`__ in the general election , but she handily beat Tony Knowles , a popular Democrat who already served two terms as governor . |
    | **`pcc_eng_00_075.7349_x1208170_18:12-14-15`**  | Traveling to North America from most parts of the world could n't be __`any easier`__ .                                                                            |
    | **`pcc_eng_18_010.8212_x0158874_04:15-17-18`**  | Made with Great Day Farms Peeled and Ready-To-Eat Hard Boiled Eggs , convenience could n't be __`any easier`__ !                                                   |
    | **`pcc_eng_03_093.5028_x1497801_27:3-5-6`**     | Literally could n't be __`any easier`__ .                                                                                                                          |
    
    
    8. _any good_
    
    |                                                | `token_str`                                                                                                                                                                                         |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20070216_0116_17:4-5-6`**           | if you are n't __`any good`__ , the public is going to know it , and they 're not going to keep it a big secret . ''                                                                                |
    | **`nyt_eng_19990427_0424_46:17-18-19`**        | `` I enjoyed playing there , especially being there at the beginning when the team was n't __`any good`__ and going through the process , helping the organization win , seeing people come along . |
    | **`apw_eng_19981129_0227_27:6-7-8`**           | and most of 'em are n't __`any good`__ .                                                                                                                                                            |
    | **`nyt_eng_20060327_0111_18:06-09-10`**        | i figured the pizza would n't do me __`any good`__ , but not too bad either .                                                                                                                       |
    | **`pcc_eng_29_003.4403_x0039474_37:16-17-18`** | No wonder some folks say 'oh I do n't care for mathematics , I was never __`any good`__ at it ' with a wistful sense of pride .                                                                     |
    
    
    9. _any higher_
    
    |                                                 | `token_str`                                                                                                                                                                             |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_069.6460_x1111205_018:3-5-6`**    | He 's never been __`any higher`__ despite one of the most consistent games on Tour .                                                                                                    |
    | **`pcc_eng_28_032.6055_x0510995_17:26-28-29`**  | To the editor : As Connecticut faces a $ 3 billion budget shortfall for the upcoming 2017 - 2018 fiscal year , the stakes could not be __`any higher`__ for this November 's election . |
    | **`pcc_eng_04_089.4408_x1428910_26:11-13-14`**  | Now taking a look at Friday , the uncertainty could n't be __`any higher`__ .                                                                                                           |
    | **`pcc_eng_04_101.8807_x1629780_163:16-18-19`** | A gentle warmth could be felt within all present that Saturday , and spirits could n't be __`any higher`__ .                                                                            |
    | **`pcc_eng_28_015.2622_x0230923_162:09-12-13`** | Plus there is no trail ahead , as nobody has been __`any higher`__ on Huascaran this beginning season yet .                                                                             |
    
    
    10. _any better_
    
    |                                                 | `token_str`                                                                                                                                                   |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_086.8841_x1387589_02:09-12-13`**  | And in my opinion , the timing could n't have been __`any better`__ .                                                                                         |
    | **`pcc_eng_11_060.1772_x0957572_093:23-25-26`** | A resilient person will financially be able to say , " Fuck you , " during a recession , but he wo n't be __`any better`__ off .                              |
    | **`pcc_eng_05_091.5658_x1465109_44:4-5-6`**     | The story was n't __`any better`__ :                                                                                                                          |
    | **`pcc_eng_09_039.7769_x0627606_093:11-12-13`** | Millions of degenerate Europeans , some better educated , are not __`any better`__ because they are , well , degenerate .                                     |
    | **`pcc_eng_21_015.0406_x0226730_4:4-5-6`**      | Butt implants are not __`any better`__ , too many risk , infection , displacement of the implant and theyfeel like rocks not to mention look very unnatural . |
    
    
    11. _any simpler_
    
    |                                                | `token_str`                                                                                                                                                                                           |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_033.6336_x0526803_40:3-4-5`**    | Things are n't __`any simpler`__ on the business side of Spellman Investigations ....                                                                                                                 |
    | **`pcc_eng_02_083.9536_x1341196_29:31-33-34`** | Workflow simplified Built to support the DV family of codecs , as well as the Quick Time animation codec , while using the industry standard .mov wrapper , workflow could not be __`any simpler`__ . |
    | **`pcc_eng_05_016.3328_x0248347_31:4-5-6`**    | Mainly they are not __`any simpler`__ than screens and require routine ladder maintenance .                                                                                                           |
    | **`pcc_eng_09_040.1900_x0634263_15:4-6-7`**    | The premise could n't be __`any simpler`__ .                                                                                                                                                          |
    | **`pcc_eng_21_090.3774_x1444504_06:26-28-29`** | With the familiarity of Outlook and making it easier to get things done , and customizable , so you stay in control , it could n't be __`any simpler`__ than Bill Pay Reminders .                     |
    
    
    12. _any brighter_
    
    |                                                 | `token_str`                                                                                                                                                                      |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_006.4356_x0088370_020:12-13-14`** | If you use a reading light , make sure it 's not __`any brighter`__ than necessary and does n't shine in your eyes .                                                             |
    | **`pcc_eng_29_093.1157_x1487984_25:1-5-6`**     | Nor is the picture __`any brighter`__ in Scottish retail .                                                                                                                       |
    | **`pcc_eng_19_042.2865_x0666602_11:32-33-34`**  | As it stands , Black Berry is already in the red , losing as much as US $ 84 million in the last quarter ; the prediction for the next is n't __`any brighter`__ at this point . |
    | **`pcc_eng_16_031.6261_x0495715_04:3-5-6`**     | Life could n't be __`any brighter`__ for art dealer Christina Daniels .                                                                                                          |
    | **`pcc_eng_26_040.8483_x0644387_012:6-7-8`**    | Guess spies like him are n't __`any brighter`__ now than they were back in the 1940s !                                                                                           |
    
    
    13. _any worse_
    
    |                                                 | `token_str`                                                                                                                                      |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_025.8441_x0401450_24:11-13-14`**  | If Romero struggles during his September callup , he wo n't be __`any worse`__ off than he was before .                                          |
    | **`pcc_eng_29_001.8833_x0014164_08:08-10-11`**  | The Justices argue that the company would n't be __`any worse`__ off than with the first two options .                                           |
    | **`pcc_eng_04_100.7136_x1610879_009:23-24-25`** | It 's never been good , and some people have chosen to ignore that in the past , but it really is n't __`any worse`__ .                          |
    | **`pcc_eng_24_079.1167_x1263637_52:23-25-26`**  | Kerry is n't my ideal candidate by a long shot , but in this case the devil we do n't know ca n't be __`any worse`__ than the devil we do know . |
    | **`pcc_eng_04_070.0570_x1115376_09:3-5-6`**     | He ca n't be __`any worse`__ than douglas .                                                                                                      |
    
    
    14. _any closer_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_087.5575_x1400904_73:6-7-8`**    | Given that the NHL is n't __`any closer`__ to getting it all right all the time or even most of the time , maybe it 's time to take a step back and allow the human element to return to all aspects of the game , improving the quality and flow of the action , especially since most reviews are designed to take goals away , which is counterintuitive to what the league is trying to achieve in driving up offense . |
    | **`pcc_eng_11_097.4880_x1561973_10:09-11-12`** | By which I mean I 'm not pregnant nor really __`any closer`__ to being pregnant .                                                                                                                                                                                                                                                                                                                                           |
    | **`pcc_eng_24_027.6785_x0431385_33:1-4-5`**    | Nor is Congress __`any closer`__ to resolving differences over reauthorizing the Export-Import Bank or trying to keep the economic recovery going .                                                                                                                                                                                                                                                                         |
    | **`nyt_eng_19980127_0586_11:09-10-11`**        | today , two years later , AT&amp;T is n't __`any closer`__ in offering local services to its residential customers .                                                                                                                                                                                                                                                                                                        |
    | **`nyt_eng_20000708_0133_3:01-11-12`**         | not that all the scientific controversy over global warming is __`any closer`__ to an answer here than anywhere else .                                                                                                                                                                                                                                                                                                      |
    
    
    15. _any smarter_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                  |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_005.3539_x0070580_03:5-6-7`**     | Since I 'm probably not __`any smarter`__ than most of the people reading this column , I need to make sure I supply my readers with information that in one way or another is either uplifting , insightful to some degree , encouraging , entertaining , helpful in some way or emotionally stirring , bringing either a little lump to your throat or a little laugh or snicker ( or at least a smile ) . |
    | **`pcc_eng_08_046.5222_x0736880_117:20-21-22`** | By the way , Jason Werth 's contract is more proof that some major league general manager 's are n't __`any smarter`__ than your middle - of- the - road fantasy baseballer .                                                                                                                                                                                                                                |
    | **`pcc_eng_16_024.3102_x0377265_11:07-09-10`**  | The determination to be dour ca n't be __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                   |
    | **`pcc_eng_15_094.8222_x1516469_0949:4-5-6`**   | " You 're not __`any smarter`__ though , " He -man moved in .                                                                                                                                                                                                                                                                                                                                                |
    | **`pcc_eng_29_039.4931_x0621544_141:07-12-13`** | Many inventions come from large cities not because city folk are __`any smarter`__ , but because the necessary mix of ideas was in the same place , at the same time .                                                                                                                                                                                                                                       |
    
    
    16. _any cheaper_
    
    |                                                 | `token_str`                                                                                                                                               |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_028.4568_x0444073_092:20-21-22`** | " We recently introduced a true recycled bottle , which was very well received , but sometimes those are not __`any cheaper`__ than brand new materials . |
    | **`pcc_eng_27_024.8516_x0385402_08:17-18-19`**  | The Melville ones are n't undercover which is very problematic for winter , and they were n't __`any cheaper`__ .                                         |
    | **`pcc_eng_23_004.2523_x0052355_13:15-16-17`**  | For now it appears solid state drives will continue to get faster , but not __`any cheaper`__ .                                                           |
    | **`pcc_eng_12_039.4888_x0622571_46:7-8-9`**     | And I bet there tickets were n't __`any cheaper`__ .                                                                                                      |
    | **`pcc_eng_09_006.5535_x0089995_18:18-19-20`**  | Ghana 's railway links Accra , Kumasi and Takoradi but the trains are much slower and are n't __`any cheaper`__ than motorised transport .                |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/...
    
    Samples saved as...
    1. `neg_bigram_examples/any/any_younger_99ex.csv`
    1. `neg_bigram_examples/any/any_clearer_99ex.csv`
    1. `neg_bigram_examples/any/any_happier_99ex.csv`
    1. `neg_bigram_examples/any/any_different_99ex.csv`
    1. `neg_bigram_examples/any/any_bigger_99ex.csv`
    1. `neg_bigram_examples/any/any_nicer_99ex.csv`
    1. `neg_bigram_examples/any/any_easier_99ex.csv`
    1. `neg_bigram_examples/any/any_good_99ex.csv`
    1. `neg_bigram_examples/any/any_higher_99ex.csv`
    1. `neg_bigram_examples/any/any_better_99ex.csv`
    1. `neg_bigram_examples/any/any_simpler_99ex.csv`
    1. `neg_bigram_examples/any/any_brighter_99ex.csv`
    1. `neg_bigram_examples/any/any_worse_99ex.csv`
    1. `neg_bigram_examples/any/any_closer_99ex.csv`
    1. `neg_bigram_examples/any/any_smarter_99ex.csv`
    1. `neg_bigram_examples/any/any_cheaper_99ex.csv`
    
    ## 5. *remotely*
    
    |                      |        `N` |      `f1` |   `adv_total` |
    |:---------------------|-----------:|----------:|--------------:|
    | **NEGATED_remotely** | 72,839,589 | 3,173,660 |        16,426 |
    | **NEGMIR_remotely**  |  1,701,929 |   291,732 |         2,341 |
    
    
    |                                 |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:--------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGany~remotely_surprising**  |    75 |        70,540 |    0.85 |    5.07 |   413.61 |      3.66 |       71.34 |     84 |
    | **NEGmir~remotely_believable**  |    21 |           600 |    0.83 |    1.96 |    74.08 |      3.60 |       17.40 |     21 |
    | **NEGmir~remotely_surprising**  |    17 |         2,662 |    0.83 |    1.50 |    59.97 |      2.91 |       14.09 |     17 |
    | **NEGmir~remotely_comparable**  |    44 |           283 |    0.76 |    2.72 |   134.02 |      8.06 |       35.94 |     47 |
    | **NEGmir~remotely_true**        |    61 |         6,191 |    0.75 |    3.04 |   181.65 |     11.31 |       49.69 |     66 |
    | **NEGany~remotely_ready**       |    58 |       141,590 |    0.74 |    4.16 |   287.63 |      3.22 |       54.78 |     74 |
    | **NEGmir~remotely_new**         |    19 |        12,836 |    0.69 |    1.00 |    50.62 |      3.77 |       15.23 |     22 |
    | **NEGmir~remotely_close**       |   218 |        13,874 |    0.65 |    3.28 |   532.96 |     45.77 |      172.23 |    267 |
    | **NEGany~remotely_true**        |   250 |       231,639 |    0.63 |    4.61 | 1,111.13 |     16.12 |      233.88 |    370 |
    | **NEGmir~remotely_funny**       |    41 |         5,365 |    0.63 |    1.85 |    97.91 |      8.74 |       32.26 |     51 |
    | **NEGany~remotely_funny**       |   137 |       122,927 |    0.60 |    4.15 |   589.74 |      9.24 |      127.76 |    212 |
    | **NEGmir~remotely_interesting** |    56 |        12,447 |    0.56 |    1.80 |   115.20 |     13.20 |       42.80 |     77 |
    | **NEGmir~remotely_possible**    |    38 |         3,160 |    0.56 |    1.42 |    78.73 |      8.91 |       29.09 |     52 |
    | **NEGany~remotely_qualified**   |    57 |        74,643 |    0.52 |    3.13 |   222.79 |      4.40 |       52.60 |    101 |
    | **NEGmir~remotely_similar**     |    71 |         7,011 |    0.49 |    1.70 |   127.32 |     18.34 |       52.66 |    107 |
    | **NEGany~remotely_close**       |   694 |       411,329 |    0.39 |    3.65 | 2,243.22 |     69.58 |      624.42 |  1,597 |
    | **NEGany~remotely_comparable**  |   118 |        12,252 |    0.38 |    2.98 |   375.73 |     12.07 |      105.93 |    277 |
    | **NEGany~remotely_accurate**    |    50 |       152,299 |    0.33 |    2.10 |   143.78 |      5.84 |       44.16 |    134 |
    | **NEGany~remotely_interested**  |   330 |       264,528 |    0.27 |    2.74 |   817.06 |     46.27 |      283.73 |  1,062 |
    | **NEGany~remotely_similar**     |   152 |       203,453 |    0.23 |    2.20 |   334.61 |     24.36 |      127.64 |    559 |
    
    
    1. _remotely surprising_
    
    |                                                 | `token_str`                                                                                                                                                                                 |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_036.1169_x0567619_157:3-4-5`**    | This is not __`remotely surprising`__ and proves that the liberal feels far more charitable with other people 's money than he does his own .                                               |
    | **`pcc_eng_val_2.10616_x33464_17:5-6-7`**       | It 's telling but not __`remotely surprising`__ that Dionne looks to Europe , home of the cradle - to - grave welfare state , as the inspiration for the kind of capitalism he wants here . |
    | **`pcc_eng_27_026.2661_x0408312_06:24-25-26`**  | Instead , it blends warm comedy , silly slapstick and a heavy dose of sentiment to tell a story that 's engaging but never __`remotely surprising`__ .                                      |
    | **`pcc_eng_00_034.7586_x0545419_23:7-8-9`**     | This is , of course , not __`remotely surprising`__ .                                                                                                                                       |
    | **`pcc_eng_19_049.0450_x0775511_054:11-12-13`** | Starbound tries its hand at so much that it 's not __`remotely surprising`__ to see it dabbling in Metroidvania -style dungeons , as well .                                                 |
    
    
    2. _remotely believable_
    
    |                                                | `token_str`                                                                                                                                                                                                     |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_050.7976_x0803803_11:1-5-6`**    | None of it is __`remotely believable`__ , but it 's easy on the eyes ( and the brain ) .                                                                                                                        |
    | **`pcc_eng_28_012.5062_x0186294_07:23-24-25`** | The thrills are n't thrilling , the jokes are n't funny , the mystery has no suspense , the special effects are n't __`remotely believable`__ , the acting is wooden , the secret baddie is glaringly obvious . |
    | **`nyt_eng_19970623_0561_27:01-10-11`**        | none of this , needless to say , is __`remotely believable`__ _ nor is the apocalyptic ending that reunites the demented Devi with her alleged birth parents .                                                  |
    | **`nyt_eng_19980219_0135_21:15-16-17`**        | neither is convincing , particularly Shue , whose little-girl voice and exaggerated vampings are never __`remotely believable`__ .                                                                              |
    | **`nyt_eng_19991104_0204_12:4-5-6`**           | although there is nothing __`remotely believable`__ about this drawn-out cat-and-mouse game of a movie crossed with a whodunit , that 's almost the point .                                                     |
    
    
    3. _remotely comparable_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                 |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_096.6618_x1547334_11:52-53-54`**  | Issue : Ask people about Stephen Frears ' period dramedy , which is playing well to arthouse audiences , and you 're bound to get back a comment about how the two lead characters , Queen Victoria ( Dame Judi Dench ) and Abdul Karim ( Ali Fasal ) , are not __`remotely comparable`__ . |
    | **`pcc_eng_18_080.1359_x1281366_31:1-4-5`**     | Nothing is even __`remotely comparable`__ to this book in its comprehensive scope and detail .                                                                                                                                                                                              |
    | **`pcc_eng_13_097.3545_x1556971_068:09-10-11`** | Pat Dorsey : The U.S. and Greece are n't __`remotely comparable`__ .                                                                                                                                                                                                                        |
    | **`apw_eng_19980204_0856_30:6-7-8`**            | note that we could accomplish nothing __`remotely comparable`__ on the basis of the Court\/rebel scenes .                                                                                                                                                                                   |
    | **`pcc_eng_29_083.8394_x1337943_16:3-4-5`**     | It is not __`remotely comparable`__ to The Last Temptation , in which Willem Dafoe played Jesus , Harvey Keitel was Judas and David Bowie Pontius Pilate .                                                                                                                                  |
    
    
    4. _remotely true_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                     |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_083.4163_x1332170_29:3-4-5`**     | That 's not __`remotely true`__ ( we 're not even a paper ) , but even if it were , how does that refute our criticisms ?                                                                                                                                                       |
    | **`pcc_eng_18_042.3295_x0668674_58:3-5-6`**     | Which is n't even __`remotely true`__ .                                                                                                                                                                                                                                         |
    | **`pcc_eng_26_095.8218_x1533359_110:10-12-13`** | In most fields of technological progress , that is n't even __`remotely true`__ .                                                                                                                                                                                               |
    | **`pcc_eng_00_062.2374_x0989988_14:17-27-28`**  | Moreover , three decades of independent journalism have led me to conclude not only that virtually nothing of what is presented as ' news ' is __`remotely true`__ , but that the conventional writing and presentation of history itself is as phoney as a three dollar bill . |
    | **`pcc_eng_06_073.9043_x1179256_070:4-6-7`**    | ( That 's not even __`remotely true`__ . )                                                                                                                                                                                                                                      |
    
    
    5. _remotely ready_
    
    |                                                | `token_str`                                                                                                                                                                          |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_102.9020_x1648488_117:3-4-5`**   | I 'm not __`remotely ready`__ to talk about how to talk with kids about sex .                                                                                                        |
    | **`pcc_eng_26_032.3176_x0506188_29:13-14-15`** | Smith seems like a pleasant 14 - year-old , but he 's not __`remotely ready`__ to carry a blockbuster on his own or to deal with a script so silly it even seems to stymie his dad . |
    | **`nyt_eng_19980427_0151_37:08-09-10`**        | Mark had finally confessed : He was n't __`remotely ready`__ to be a father .                                                                                                        |
    | **`pcc_eng_19_075.9751_x1211201_07:11-12-13`** | ' but if she 's dating a guy who 's not __`remotely ready`__ for children cougars reveal what it 's really like to date have you been pronouncing versace wrong .                    |
    | **`nyt_eng_20050421_0183_31:19-20-21`**        | like the title says , `` A Lot Like Love '' is a romance for people who are n't __`remotely ready`__ for the real thing .                                                            |
    
    
    6. _remotely new_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                      |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_049.8000_x0788638_10:3-5-6`**     | It 's not even __`remotely new`__ .                                                                                                                                                                                                                                                                              |
    | **`pcc_eng_09_005.0515_x0065815_13:3-4-5`**     | This is n't __`remotely new`__ .                                                                                                                                                                                                                                                                                 |
    | **`pcc_eng_28_016.5116_x0251009_033:11-12-13`** | Les ' voice again , reminding us that there 's nothing __`remotely new`__ about expressive , artfully wild nonfiction cinema .                                                                                                                                                                                   |
    | **`pcc_eng_27_009.7834_x0141748_17:6-8-9`**     | This is , depressingly , not even __`remotely new`__ .                                                                                                                                                                                                                                                           |
    | **`pcc_eng_22_006.4395_x0087791_11:08-09-10`**  | Problem is , Six 's treatment is nothing __`remotely new`__ , denying Martin any voice whatsoever ( he literally never speaks a word ) , then littering the film with allusions to previous trauma , albeit ( again ) outrageously ( there 's the suggestion that " baby 's tears make daddy 's willy hard " ) . |
    
    
    7. _remotely close_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                    |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_023.8409_x0369740_28:07-09-10`**  | There is , for example , nothing even __`remotely close`__ to the sort of intellectual division that occurred during the Vietnam War in which the Kissingers and Bundys were matched by others -- including those the New York Times in 1970 headlined as " 1000 'ESTABLISHMENT ' LAWYERS JOIN WAR PROTEST . " |
    | **`pcc_eng_27_051.2191_x0811587_187:16-18-19`** | The APR is not an M.D. It 's not a Ph. D. and it 's not even __`remotely close`__ to being the equivalent of passing the bar or the Series Seven .                                                                                                                                                             |
    | **`nyt_eng_19991207_0351_12:13-15-16`**         | but the overall respect factor when compared to other jock stars is not even __`remotely close`__ .                                                                                                                                                                                                            |
    | **`pcc_eng_29_008.1527_x0115591_05:07-09-10`**  | Unfortunately for them , this is n't even __`remotely close`__ to the truth .                                                                                                                                                                                                                                  |
    | **`pcc_eng_15_044.4007_x0701669_32:10-12-13`**  | As for what place attracts families , it 's not even __`remotely close`__ :                                                                                                                                                                                                                                    |
    
    
    8. _remotely funny_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_13_001.7588_x0012176_69:7-8-9`**     | They are usually very serious and not __`remotely funny`__ .                                                                                                                                                                                                               |
    | **`pcc_eng_11_099.0101_x1586566_22:12-13-14`**  | For the first 30 minutes of the movie , there is nothing __`remotely funny`__ , original or entertaining .                                                                                                                                                                 |
    | **`pcc_eng_24_105.4759_x1690348_02:3-5-6`**     | which will not be __`remotely funny`__ if you do n't live in danger of a hurricane passin ' through ...                                                                                                                                                                    |
    | **`pcc_eng_23_034.0465_x0533540_095:14-15-16`** | However the last 2 nights with the adult comedians were truly vulgar and not __`remotely funny`__ and a waste of our time .                                                                                                                                                |
    | **`pcc_eng_21_069.4617_x1106415_163:48-49-50`** | In Chris Heath 's book Pet Shop Boys , Literally , he briefly quotes Neil ( on page 116 of at least some editions ) about this unreleased song : " Sometimes the inspiration behind a song is something funny , though often the song itself is n't __`remotely funny`__ . |
    
    
    9. _remotely possible_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                               |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_009.1550_x0131699_07:23-25-26`**  | Without the hundreds of kilos of gear that Interplast bring over from Australia , most of the procedures the surgeons performed would not be __`remotely possible`__ .                                                                                    |
    | **`pcc_eng_10_042.7232_x0675134_037:35-36-37`** | The truth is that weca n't model even a single ecosystem anywhere in the world , because they are much too complicated , the genomes of their inhabitants are unknown , and it 's not __`remotely possible`__ to track every single variable .            |
    | **`pcc_eng_09_031.9930_x0501699_4:3-4-5`**      | There is nothing __`remotely possible`__ that we can do to restore these funds to nation states or change what they are used to accomplish .                                                                                                              |
    | **`pcc_eng_29_001.7821_x0012545_19:10-12-13`**  | As pointed out many times before , this is not even __`remotely possible`__ .                                                                                                                                                                             |
    | **`apw_eng_20090511_1244_28:43-44-45`**         | `` The odds that you have Nazi wartime documents that put him at Sobibor , that former guards remember him and that he writes that he lived in Sobibor -- that he did n't serve at the death camp ? It 's not __`remotely possible`__ , '' Drimmer said . |
    
    
    10. _remotely interesting_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                          |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_073.6391_x1176085_39:1-6-7`**     | None of these people are __`remotely interesting`__ or worth following , their functions are interchangable , the leads could n't create a spark of chemistry between them if they were standing in the middle of a raging brushfire , and all of this nothingness takes a backseat to the impressive and oppressive visual effects that start to all look the same after only a matter of minutes . |
    | **`pcc_eng_24_024.0266_x0372360_43:4-5-6`**     | And sometimes , nothing __`remotely interesting`__ happens to be told an answer rather than learn it - despite the security strip poker software how to make all individual decisions easier .                                                                                                                                                                                                       |
    | **`pcc_eng_16_083.5450_x1336172_3:23-25-26`**   | The vast majority of the time , his life is about as interesting as anyone else 's , which is to say not even __`remotely interesting`__ enough to write a ...                                                                                                                                                                                                                                       |
    | **`pcc_eng_29_098.4590_x1574615_27:16-17-18`**  | Once someone had witnessed what they could do with a lightsaber , a hoe was n't __`remotely interesting`__ .                                                                                                                                                                                                                                                                                         |
    | **`pcc_eng_03_086.6062_x1386237_076:23-28-29`** | She tells her story through the eyes of half a dozen characters , all of whom speak in the same voice , none of whom are even __`remotely interesting`__ or convincing as human beings .                                                                                                                                                                                                             |
    
    
    11. _remotely qualified_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                   |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_086.7234_x1388165_067:29-30-31`** | I do n't know how respectable this research is , because I do n't care enough to actually read it , and even if I did I am not __`remotely qualified`__ to judge something in this field .                                                                                    |
    | **`nyt_eng_19990502_0236_3:09-10-11`**          | BUCHANAN-CHINA -LRB- Seattle -RRB- _ China is `` not __`remotely qualified`__ ''                                                                                                                                                                                              |
    | **`pcc_eng_15_092.7806_x1483434_28:4-6-7`**     | If you are not even __`remotely qualified`__ for a position , do n't apply .                                                                                                                                                                                                  |
    | **`pcc_eng_19_043.1145_x0679902_08:08-09-10`**  | Bohr 's theory - which I am not __`remotely qualified`__ to explain , though I will try-suggested that : 1 ) two particles could become interrelated or entangled and 2 ) after which , they could interact even at astronomical distances , without any visible connection . |
    | **`pcc_eng_06_073.7395_x1176604_25:07-09-10`**  | The truth is , you are not even __`remotely qualified`__ to determine what caused any type of erosion anywhere on the planet , unless you yourself witness the erosion .                                                                                                      |
    
    
    12. _remotely similar_
    
    |                                                | `token_str`                                                                                                                                                                                                     |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20050112_0364_60:21-22-23`**        | but if you go deeper than this surface comparison , you can see that being a white middle-class person is not __`remotely similar`__ to what African-Americans had to go through in this country , '' he says . |
    | **`nyt_eng_20000218_0186_47:1-2-3`**           | nothing __`remotely similar`__ went on at Paul Smith 's show Monday night .                                                                                                                                     |
    | **`pcc_eng_19_076.2843_x1216205_11:23-25-26`** | Justice R. Fred Lewis cited decisions by other courts that agree with Scherker 's position , but Stanley Rosenblatt said they were not " __`remotely similar`__ to this case . "                                |
    | **`pcc_eng_01_098.9252_x1583137_54:21-22-23`** | In one sense it is difficult to think of an example of an encounter with God for which there is nothing __`remotely similar`__ in the Bible .                                                                   |
    | **`pcc_eng_06_078.4987_x1253180_06:3-4-5`**    | There 's nothing __`remotely similar`__ .                                                                                                                                                                       |
    
    
    13. _remotely accurate_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                 |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_036.6220_x0576263_19:3-5-6`**     | This is n't even __`remotely accurate`__ either , but first , some context from Nancy Reagan : " Presidents do n't get vacations -- they just get a change of scenery .                                                                                                                                                                     |
    | **`pcc_eng_27_027.4859_x0427834_083:04-09-10`** | In truth , neither of these images is __`remotely accurate`__ ( and no , I never was a member of the chess club ) .                                                                                                                                                                                                                         |
    | **`pcc_eng_10_019.7965_x0303782_016:22-24-25`** | Thus Easterbrook 's claim that the IPCC TAR projected a 1 deg C global surface warming from 2000 to 2010 was not even __`remotely accurate`__ .                                                                                                                                                                                             |
    | **`pcc_eng_test_3.08101_x47485_19:19-21-22`**   | The only full-face portrait , an engraving in a 16th - century book on Flemish artists , may not be __`remotely accurate`__ since it was made from a profile medallion : it shows a rather grave figure , a long bearded solemn face , under an elaborate hat .                                                                             |
    | **`pcc_eng_03_032.1579_x0504682_04:08-10-11`**  | Joan of Arc with Leelee Sobieski is not even __`remotely accurate`__ and ridiculously long and honestly maybe the worst movie I 've ever seen and I would n't wish it on my worst enemy and every time you come across it you should kill it with fire just so that it would be a slightly more accurate representation of Joan 's life . " |
    
    
    14. _remotely interested_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                              |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_038.0056_x0598043_40:48-49-50`**  | And more importantly , will you leave the cozy confines of , say , Muskoka , or Lake of the Woods , or Manitou Beach ( you get the picture ) , to go to Calgary for a few days - knowing that the brass really is n't __`remotely interested`__ in you ? |
    | **`pcc_eng_08_075.3740_x1204142_052:33-35-36`** | I would say that we 're definitely the minority in our age group , because most of the over - 30 year olds that I know do not have Myspace and are not even __`remotely interested`__ .                                                                  |
    | **`pcc_eng_01_062.3118_x0991711_4:31-32-33`**   | One of the footballing idols of the boys in my junior school , and the second player I got to know the name of after Georgie Best ( I was n't __`remotely interested`__ in football as a kid , still are n't really ) .                                  |
    | **`pcc_eng_16_027.8615_x0434864_419:24-25-26`** | I initially chose to see it at the Phoenix Film Festival because I had a scheduling gap between other pictures and I was n't __`remotely interested`__ in anything else screening at the same time .                                                     |
    | **`pcc_eng_18_037.3736_x0588488_10:21-22-23`**  | Without US assistance , Israel is quite strong enough to take on any combination of Arab armies , which are n't __`remotely interested`__ in such a conflict .                                                                                           |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/...
    
    Samples saved as...
    1. `neg_bigram_examples/remotely/remotely_surprising_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_believable_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_comparable_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_true_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_ready_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_new_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_close_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_funny_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_possible_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_interesting_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_qualified_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_similar_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_accurate_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_interested_99ex.csv`
    
    ## 6. *ever*
    
    |                     |        `N` |       `f1` |   `adv_total` |
    |:--------------------|-----------:|-----------:|--------------:|
    | **NEGMIR_ever**     |  1,701,929 |    291,732 |         5,060 |
    | **NEGATED_ever**    | 72,839,589 |  3,173,660 |       114,075 |
    | **COMPLEMENT_ever** | 72,839,589 | 69,662,736 |       114,075 |
    
    
    |                           |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:--------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGmir~ever_easy**      |   368 |        18,610 |    0.83 |    6.44 | 1,285.01 |     63.25 |      304.75 |    369 |
    | **NEGmir~ever_simple**    |   206 |        25,408 |    0.83 |    5.82 |   726.76 |     35.31 |      170.69 |    206 |
    | **NEGmir~ever_enough**    |   147 |         2,596 |    0.83 |    5.30 |   518.58 |     25.20 |      121.80 |    147 |
    | **NEGmir~ever_certain**   |   143 |         1,800 |    0.83 |    5.26 |   504.47 |     24.51 |      118.49 |    143 |
    | **NEGmir~ever_boring**    |    57 |         1,961 |    0.83 |    3.80 |   201.07 |      9.77 |       47.23 |     57 |
    | **NEGmir~ever_black**     |    56 |         1,412 |    0.83 |    3.77 |   197.54 |      9.60 |       46.40 |     56 |
    | **NEGmir~ever_sick**      |    39 |         1,895 |    0.83 |    3.15 |   137.57 |      6.69 |       32.31 |     39 |
    | **NEGmir~ever_good**      |   299 |        31,585 |    0.82 |    5.68 | 1,013.87 |     51.94 |      247.06 |    303 |
    | **NEGmir~ever_perfect**   |   206 |         3,134 |    0.82 |    5.57 |   714.47 |     35.48 |      170.52 |    207 |
    | **NEGany~ever_simple**    |   211 |       396,749 |    0.80 |    5.56 | 1,109.28 |     10.89 |      200.11 |    250 |
    | **NEGmir~ever_able**      |   136 |         3,704 |    0.78 |    4.17 |   426.52 |     24.51 |      111.49 |    143 |
    | **NEGany~ever_boring**    |    72 |        45,891 |    0.76 |    4.46 |   362.74 |      3.92 |       68.08 |     90 |
    | **NEGany~ever_easy**      |   429 |       579,827 |    0.73 |    5.41 | 2,105.13 |     24.18 |      404.82 |    555 |
    | **NEGany~ever_certain**   |   147 |        74,952 |    0.72 |    4.80 |   713.34 |      8.41 |      138.59 |    193 |
    | **NEGany~ever_sure**      |    87 |       262,825 |    0.49 |    3.34 |   328.20 |      7.06 |       79.94 |    162 |
    | **NEGany~ever_good**      |   331 |     1,681,795 |    0.46 |    3.81 | 1,188.69 |     28.76 |      302.24 |    660 |
    | **NEGany~ever_enough**    |   173 |       152,020 |    0.45 |    3.54 |   618.62 |     15.12 |      157.88 |    347 |
    | **NEGany~ever_perfect**   |   216 |       104,659 |    0.40 |    3.34 |   706.71 |     21.31 |      194.69 |    489 |
    | **NEGany~ever_satisfied** |    64 |        62,862 |    0.38 |    2.57 |   203.01 |      6.58 |       57.42 |    151 |
    | **COM~ever_closer**       | 6,305 |        61,475 |    0.04 |    3.51 |   538.66 |  6,031.92 |      273.08 |  6,307 |
    
    
    1. _ever simple_
    
    |                                                | `token_str`                                                                                                                                                           |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_012.5117_x0186005_24:2-4-5`**    | But nothing is __`ever simple`__ with cancer , and no diagnosis goes exactly as the medical books say .                                                               |
    | **`pcc_eng_03_080.6319_x1289486_03:1-3-4`**    | Nothing is __`ever simple`__ .                                                                                                                                        |
    | **`pcc_eng_19_018.4605_x0281750_03:5-6-7`**    | Experiencing family strife is never __`ever simple`__ , yet a skilled family members law lawyer can assist you make essential choices as well as locate a new begin . |
    | **`pcc_eng_16_055.7158_x0885540_05:11-13-14`** | But in this weird , wonderful and anarchic universe , nothing is __`ever simple`__ - not even what colour they should be .                                            |
    | **`pcc_eng_05_012.4146_x0185066_04:3-4-5`**    | It is n't __`ever simple`__ to outright find a soul mate since most individuals are already aware .                                                                   |
    
    
    2. _ever enough_
    
    |                                                 | `token_str`                                                                                                                                                                                      |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_006.0539_x0082006_15:1-7-8`**     | Nothing the writer can do is __`ever enough`__ .                                                                                                                                                 |
    | **`pcc_eng_29_095.9009_x1533172_04:09-10-11`**  | Reminds me of Guacamole ; there just is n't __`ever enough`__ .                                                                                                                                  |
    | **`pcc_eng_01_104.9836_x1680364_21:3-4-5`**     | Knowledge is rarely __`ever enough`__ to spark change .                                                                                                                                          |
    | **`pcc_eng_25_034.7117_x0545751_593:25-26-27`** | The Blessing is the anointing to remove every burden ( working for a living ) and destroy every yoke ( debt , lack , not __`ever enough`__ , poverty and fixed increase like Social Security ) . |
    | **`pcc_eng_18_084.5124_x1352360_034:2-4-5`**    | But nothing was __`ever enough`__ for him .                                                                                                                                                      |
    
    
    3. _ever certain_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_044.2947_x0699007_13:32-33-34`** | The story -- which was also reported by The Intercept , an online magazine on nationals security matters -- paints a classic spy versus spy story where the US agents are n't __`ever certain`__ about who they are dealing with and whether or not they are being baited and played by their Russian counterparts . |
    | **`pcc_eng_14_044.1696_x0697560_045:2-4-5`**   | But nothing is __`ever certain`__ in sports , it 's why we watch them .                                                                                                                                                                                                                                              |
    | **`pcc_eng_12_063.4103_x1009071_14:13-15-16`** | At first , Abigail Salmon clings on to the thought that " nothing is __`ever certain`__ " .                                                                                                                                                                                                                          |
    | **`pcc_eng_14_030.2787_x0473137_17:21-23-24`** | With home-field advantage and plenty of rest , L.A. has to be the early favorite , but in the playoffs nothing is __`ever certain`__ .                                                                                                                                                                               |
    | **`pcc_eng_26_036.8253_x0579110_12:09-11-12`** | In a market characterized by high risk , nothing is __`ever certain`__ , so only time will tell if the performance of IRBO and other robotics and AI ETFs boom with the industry or if they will continue their current downward trend .                                                                             |
    
    
    4. _ever boring_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                     |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_072.9895_x1163469_11:09-10-11`**  | The novel is a quick read and is n't __`ever boring`__ .                                                                                                                                                                                                                                        |
    | **`pcc_eng_22_085.9567_x1373236_06:3-5-6`**     | he is never , __`ever boring`__ .                                                                                                                                                                                                                                                               |
    | **`pcc_eng_22_083.2180_x1328962_124:15-16-17`** | She handles her adventures with grace rather than with a sword , but is never __`ever boring`__ .                                                                                                                                                                                               |
    | **`pcc_eng_20_032.7750_x0513807_54:49-51-52`**  | That it is those earliest years that remain The Stranglers ' most popular is not surprising -- from bad -mannered yobs to purveyors of supreme pop delicacies , the group was responsible for music that may have been ugly and might have been crude -- but it was never , __`ever boring`__ . |
    | **`pcc_eng_08_040.3495_x0636911_56:17-19-20`**  | They played live right on TV and perhaps because of what era this was it was never , __`ever boring`__ .                                                                                                                                                                                        |
    
    
    5. _ever black_
    
    |                                                | `token_str`                                                                                                                                           |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_093.2542_x1491955_06:1-3-4`**    | Nothing is __`ever black`__ or white and there 's an awful lot of grey between the two extremes .                                                     |
    | **`pcc_eng_27_104.5460_x1675091_08:18-20-21`** | If I 've learnt anything in my twenty six years on the planet , it 's that nothing is __`ever black`__ and white ; there 's infinite shades of grey . |
    | **`pcc_eng_02_007.9015_x0111391_26:11-13-14`** | No one type is better than the other , and nothing is __`ever black`__ and white .                                                                    |
    | **`pcc_eng_22_058.3271_x0926728_09:18-20-21`** | But Trevor is about to discover that good and evil can look a lot alike , and nothing is __`ever black`__ and white -- not even the truth .           |
    | **`pcc_eng_14_081.2960_x1298217_26:14-16-17`** | And that 's good , since , when it comes to color , nothing is __`ever black`__ and white ( sorry ) .                                                 |
    
    
    6. _ever sick_
    
    |                                                 | `token_str`                                                                          |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------|
    | **`pcc_eng_19_072.5162_x1155196_20:14-15-16`**  | He 's never been sick he 's one of those folks that is never __`ever sick`__ .       |
    | **`pcc_eng_06_027.5845_x0430017_21:13-14-15`**  | Which would come in handy here in Virginia , and I 'm never __`ever sick`__ at sea . |
    | **`pcc_eng_08_108.0222_x1731582_38:13-14-15`**  | I can work 99 per cent of the time - I 'm hardly __`ever sick`__ .                   |
    | **`pcc_eng_07_016.3556_x0248479_10:3-4-5`**     | He 's hardly __`ever sick`__ .                                                       |
    | **`pcc_eng_07_024.1556_x0374360_127:12-13-14`** | Compared to back then , I am healthy , happy and hardly __`ever sick`__ !            |
    
    
    7. _ever easy_
    
    |                                             | `token_str`                                                                                                                                                                                 |
    |:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19961001_0712_40:1-5-6`**        | none of this was __`ever easy`__ .                                                                                                                                                          |
    | **`nyt_eng_20050215_0035_83:1-5-6`**        | not that it is __`ever easy`__ to overlook Nazi Germany 's sins at a festival which takes place 200 yards from the site of Hitler 's bunker and 400 yards from the new Holocaust Memorial . |
    | **`pcc_eng_26_095.3506_x1525808_10:1-3-4`** | Nothing 's __`ever easy`__ in politics .                                                                                                                                                    |
    | **`apw_eng_20090101_0111_12:15-18-19`**     | `` The road ahead for this young couple will not be easy , but nothing worthwhile is __`ever easy`__ .                                                                                      |
    | **`pcc_eng_20_086.7659_x1385627_52:4-5-6`** | " Why is nothing __`ever easy`__ ? "                                                                                                                                                        |
    
    
    8. _ever perfect_
    
    |                                                | `token_str`                                                                            |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------|
    | **`pcc_eng_03_086.6939_x1387611_080:1-3-4`**   | Nothing is __`ever perfect`__ and you can always improve .                             |
    | **`pcc_eng_06_022.2337_x0343655_14:1-3-4`**    | Nothing is __`ever perfect`__ but I looked , and looked .                              |
    | **`pcc_eng_03_001.1859_x0003095_09:1-3-4`**    | Nothing is __`ever perfect`__ . )                                                      |
    | **`pcc_eng_03_001.9967_x0016168_12:2-4-5`**    | But nothing is __`ever perfect`__ , and the difference is that we 're willing to try . |
    | **`pcc_eng_13_099.2824_x1588216_39:10-14-15`** | We may never find the perfect lover , but nothing in life is __`ever perfect`__ .      |
    
    
    9. _ever good_
    
    |                                                 | `token_str`                                                                                                                                        |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_026.8733_x0418447_50:09-11-12`**  | " That 's the problem with immigration , nothing 's __`ever good`__ enough . "                                                                     |
    | **`pcc_eng_19_029.2431_x0455919_37:08-11-12`**  | Nothing good ever comes easy , and nothing easy is __`ever good`__ .                                                                               |
    | **`pcc_eng_06_028.0176_x0437097_21:1-3-4`**     | Nothing was __`ever good`__ enough .                                                                                                               |
    | **`pcc_eng_16_087.3283_x1397403_147:07-09-10`** | Sizzling sounds in the classroom are never , __`ever good`__ .                                                                                     |
    | **`pcc_eng_00_069.8150_x1112231_14:17-18-19`**  | I had visions of a modern re-imagining of the iconic cover image but it just was n't __`ever good`__ enough when I put the ideas to the computer . |
    
    
    10. _ever able_
    
    |                                                 | `token_str`                                                                                                                                      |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_047.3932_x0748831_2:16-18-19`**   | Built in an active volcano , this complex routinely has riots and murders , though nobody is __`ever able`__ to escape .                         |
    | **`pcc_eng_13_088.0162_x1406374_036:08-09-10`** | So there was a neighbour who was hardly __`ever able`__ to accept a gift , for example some fruits from the garden .                             |
    | **`pcc_eng_07_052.0102_x0824668_66:15-17-18`**  | Zara brings fashionable pieces to women who fancy stylish wardrobe , but who could n't be __`ever able`__ to buy the original version of those . |
    | **`pcc_eng_25_002.0898_x0017738_26:1-3-4`**     | Nobody was __`ever able`__ to detect such neutrons .                                                                                             |
    | **`pcc_eng_28_079.3351_x1267117_13:12-14-15`**  | That intensity stayed throughout the second half as the Bruins were never , __`ever able`__ to get a lead .                                      |
    
    
    11. _ever sure_
    
    |                                                | `token_str`                                                                                                                                                 |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_081.3711_x1301372_67:24-25-26`** | The question of giving up a life in the field , for one spent in relative safety , was one that he was n't __`ever sure`__ he would be fully content with . |
    | **`pcc_eng_12_066.4327_x1057515_37:1-2-3`**    | Not __`ever sure`__ I should talk to Dragon about this right now .                                                                                          |
    | **`pcc_eng_14_087.9226_x1405034_58:4-6-7`**    | Over time , nobody was __`ever sure`__ that the amount of electricity held in the banque was as much as the banque claimed to have stored - or owed to it . |
    | **`pcc_eng_08_071.4030_x1139972_46:4-5-6`**    | " I was n't __`ever sure`__ this day would come in total honesty .                                                                                          |
    | **`pcc_eng_19_079.6883_x1271238_31:08-09-10`** | This is a blog post I was n't __`ever sure`__ I 'd write .                                                                                                  |
    
    
    12. _ever satisfied_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                    |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_007.1777_x0099795_474:12-13-14`** | A lowkey but gutsy take on Steve Earle 's ' I Ain't __`Ever Satisfied`__ ' is effective if less forceful than Earle 's rocking original .                                                                                                                                                                                                                                                                      |
    | **`pcc_eng_27_054.6820_x0867710_33:32-33-34`**  | " Here Today and Gone Tomorrow " appeared then to be just another song of a man carrying on about the woman who done him wrong ( " some of them ain't __`ever satisfied`__ " ) while refusing to accept any responsibility for the situation .                                                                                                                                                                 |
    | **`pcc_eng_29_003.0834_x0033661_07:17-18-19`**  | I am not a fan of takeaways , they are expensive and frankly , I am hardly __`ever satisfied`__ with the quality plus who needs to throw away all that money when I can make something inexpensive , quick and delicious at home .                                                                                                                                                                             |
    | **`pcc_eng_24_074.2665_x1185183_07:57-58-59`**  | " Regardless of if it is a high school player coming in or a junior college kid coming in or if it a young man that has gone to a four year school and then to a junior college the research we do in the background checks are all the same and certainly if we are not __`ever satisfied`__ with anything we find on any student athlete , you wo n't be asking me about him because he will not be here . " |
    | **`pcc_eng_00_018.8916_x0288887_058:3-5-6`**    | " Are n't you __`ever satisfied`__ ? " he says .                                                                                                                                                                                                                                                                                                                                                               |
    
    
    13. _ever closer_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_102.6137_x1645247_11:27-28-29`** | Since 104 new stadiums and arenas were built between 1990 and 2010 ( compared to just 130 in the preceding 90 years ) , it 's not terribly surprising that a number of studies examining the economic impact on property values have been conducted over the last ten years . |
    | **`apw_eng_19980219_1159_16:14-15-16`**        | `` But do n't make a big deal of it , it 's not that bad . ''                                                                                                                                                                                                                 |
    | **`pcc_eng_22_008.4320_x0119944_10:39-40-41`** | The carefully chosen list of keynote speakers will provide a first class opportunity at a first class venue to hear how they decided to take action , one step at a time and do what was right and not necessarily easiest .                                                  |
    | **`pcc_eng_12_030.1172_x0471467_4:12-13-14`**  | The OData query syntax is well documented , it 's just not that intuitive .                                                                                                                                                                                                   |
    | **`pcc_eng_04_076.8838_x1225695_067:3-4-5`**   | Niku is not terribly hospitable and if someone was injured with no boat nearby , a qualified medic or doctor would be needed to be ashore at all times with an extensive medical kit .                                                                                        |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/...
    
    Samples saved as...
    1. `neg_bigram_examples/ever/ever_simple_99ex.csv`
    1. `neg_bigram_examples/ever/ever_enough_99ex.csv`
    1. `neg_bigram_examples/ever/ever_certain_99ex.csv`
    1. `neg_bigram_examples/ever/ever_boring_99ex.csv`
    1. `neg_bigram_examples/ever/ever_black_99ex.csv`
    1. `neg_bigram_examples/ever/ever_sick_99ex.csv`
    1. `neg_bigram_examples/ever/ever_easy_99ex.csv`
    1. `neg_bigram_examples/ever/ever_perfect_99ex.csv`
    1. `neg_bigram_examples/ever/ever_good_99ex.csv`
    1. `neg_bigram_examples/ever/ever_able_99ex.csv`
    1. `neg_bigram_examples/ever/ever_sure_99ex.csv`
    1. `neg_bigram_examples/ever/ever_satisfied_99ex.csv`
    1. `neg_bigram_examples/ever/ever_closer_99ex.csv`
    
    ## 7. *yet*
    
    |                 |        `N` |      `f1` |   `adv_total` |
    |:----------------|-----------:|----------:|--------------:|
    | **NEGATED_yet** | 72,839,589 | 3,173,660 |        95,763 |
    | **NEGMIR_yet**  |  1,701,929 |   291,732 |           815 |
    
    
    |                           |    `f` |   `adj_total` |   `dP1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:--------------------------|-------:|--------------:|--------:|--------:|----------:|----------:|------------:|-------:|
    | **NEGany~yet_eligible**   |    448 |        23,252 |    0.96 |    8.96 |  2,807.56 |     19.52 |      428.48 |    448 |
    | **NEGany~yet_official**   |    352 |         6,853 |    0.96 |    8.61 |  2,205.93 |     15.34 |      336.66 |    352 |
    | **NEGany~yet_convinced**  |    169 |        12,132 |    0.96 |    7.50 |  1,059.09 |      7.36 |      161.64 |    169 |
    | **NEGany~yet_online**     |     98 |        15,650 |    0.96 |    6.66 |    614.14 |      4.27 |       93.73 |     98 |
    | **NEGany~yet_mainstream** |     70 |        17,792 |    0.96 |    6.11 |    438.67 |      3.05 |       66.95 |     70 |
    | **NEGany~yet_clear**      | 10,406 |       349,214 |    0.95 |   10.77 | 64,409.97 |    456.44 |    9,949.56 | 10,476 |
    | **NEGany~yet_final**      |    640 |         5,860 |    0.95 |    8.97 |  3,972.92 |     28.02 |      611.98 |    643 |
    | **NEGany~yet_over**       |    162 |         3,983 |    0.95 |    7.21 |  1,003.13 |      7.10 |      154.90 |    163 |
    | **NEGany~yet_ready**      |  7,501 |       141,590 |    0.94 |    9.93 | 45,985.07 |    331.09 |    7,169.91 |  7,599 |
    | **NEGany~yet_complete**   |  2,174 |        86,361 |    0.94 |    9.20 | 13,277.09 |     96.20 |    2,077.80 |  2,208 |
    | **NEGmir~yet_available**  |     28 |        10,284 |    0.83 |    2.54 |     98.77 |      4.80 |       23.20 |     28 |
    | **NEGmir~yet_certain**    |     21 |         1,800 |    0.83 |    1.96 |     74.08 |      3.60 |       17.40 |     21 |
    | **NEGmir~yet_clear**      |     19 |         6,722 |    0.83 |    1.75 |     67.02 |      3.26 |       15.74 |     19 |
    | **NEGmir~yet_sure**       |     19 |         6,761 |    0.83 |    1.75 |     67.02 |      3.26 |       15.74 |     19 |
    | **NEGmir~yet_ready**      |     18 |         3,034 |    0.83 |    1.63 |     63.49 |      3.09 |       14.91 |     18 |
    
    
    1. _yet eligible_
    
    |                                                | `token_str`                                                                                                                                                                                       |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20001026_0212_15:21-22-23`**        | it is , rather , because so many of those living here are not citizens at all , but immigrants not __`yet eligible`__ to vote .                                                                   |
    | **`pcc_eng_08_108.1588_x1733779_62:20-21-22`** | Of the 14 triple crown winners who are eligible for the Baseball Hall of Fame ( Miguel Cabrera is not __`yet eligible`__ ) , O'Neill and Paul Hines are the only two who have not been inducted . |
    | **`nyt_eng_19990625_0068_3:7-8-9`**            | being a former child bride and not __`yet eligible`__ for Medicare , I thought she might understand contemporary humor .                                                                          |
    | **`pcc_eng_03_089.8620_x1439106_18:5-6-7`**    | In return , players not __`yet eligible`__ for free-agency could have their salaries decided by an arbitrator .                                                                                   |
    | **`pcc_eng_07_005.4602_x0072106_50:19-20-21`** | There may be a bowl game in their future , but at 5 - 5 , USF is not __`yet eligible`__ .                                                                                                         |
    
    
    2. _yet official_
    
    |                                                 | `token_str`                                                                                                                 |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19970725_0417_5:5-6-7`**             | `` The decision is not __`yet official`__ or definitive .                                                                   |
    | **`nyt_eng_19970804_0094_43:08-09-10`**         | a Difficult Task Although the news is not __`yet official`__ , France is poised to reduce its military presence in Africa . |
    | **`pcc_eng_20_007.4763_x0104347_24:4-5-6`**     | The change is not __`yet official`__ .                                                                                      |
    | **`pcc_eng_08_041.1583_x0649927_10:6-7-8`**     | Because the 2005 number is not __`yet official`__ , however , the city has not been fined .                                 |
    | **`pcc_eng_23_038.1471_x0600150_044:09-10-11`** | How can it be if the secession is not __`yet official`__ and the Chuukese aboard are still FSM citizens ?!                  |
    
    
    3. _yet convinced_
    
    |                                         | `token_str`                                                                                                                                                                                                                                     |
    |:----------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20090615_0122_22:5-6-7`**    | many medical professionals are not __`yet convinced`__ Obama 's overhaul is the best for their care or their pocketbooks .                                                                                                                      |
    | **`apw_eng_20021017_0641_7:17-18-19`**  | there was no opposition to Sinanan 's nomination , but some opposition lawmakers said they were not __`yet convinced`__ that Manning 's party , which won 20 seats in the this month 's election , was committed to unity in political policy . |
    | **`nyt_eng_19970110_0055_10:3-4-5`**    | investors were n't __`yet convinced`__ of the value of Highlands ' Nena\/Frieda copper and gold deposit and the Ramu nickel and cobalt project , all in Papua New Guinea .                                                                      |
    | **`nyt_eng_20050123_0062_42:4-5-6`**    | `` I 'm not __`yet convinced`__ that it 's an effective program , and I have concern about some of the so-called green energy sources they are claiming , '' Bird said .                                                                        |
    | **`apw_eng_20090926_0531_26:10-11-12`** | while he was satisfied with fourth , he was not __`yet convinced`__ the championship fight was back on .                                                                                                                                        |
    
    
    4. _yet online_
    
    |                                                | `token_str`                                                                                                                                                                                                      |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_107.00738_x1716226_06:6-7-8`**   | The app , which is not __`yet online`__ , does n't let the sad sack who 's missing the show hear the live versions of the songs , which would present significant copyright hurdles , as cool as that would be . |
    | **`pcc_eng_24_028.2503_x0440618_18:6-7-8`**    | Much of that music is not __`yet online`__ , and the company is not sure if all of it will ever be .                                                                                                             |
    | **`pcc_eng_20_030.8877_x0483322_30:11-12-13`** | Much of Klug 's research involves original documents that are not __`yet online`__ , so he is also collaborating with a colleague in South Africa and the UW Law School Library to create a virtual archive .    |
    | **`pcc_eng_val_1.0279_x00462_12:15-16-17`**    | What 's more , our research shows that of the small businesses that 're not __`yet online`__ , 70 % would consider establishing and developing a website if it was easy to do and free of charge . "             |
    | **`pcc_eng_24_070.8498_x1129847_12:16-17-18`** | If all goes well , we 'll debut at least one zine design that is not __`yet online`__ .                                                                                                                          |
    
    
    5. _yet mainstream_
    
    |                                                | `token_str`                                                                                                                                                                                                               |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_001.3852_x0006241_25:3-4-5`**    | It 's not __`yet mainstream`__ . "                                                                                                                                                                                        |
    | **`pcc_eng_13_002.4713_x0023655_27:4-5-6`**    | Upcycled clothes are not __`yet mainstream`__ , however with more and more sustainable shoppers shunning fast fashion they are bound to look for products with a smaller carbon footprint that reuse existing materials . |
    | **`pcc_eng_23_003.8193_x0045384_62:25-26-27`** | Also , while hemp is a popular fabric used for thousands of items , the concept of hemp furniture is gaining momentum and is not __`yet mainstream`__ .                                                                   |
    | **`pcc_eng_03_089.9885_x1441165_01:5-6-7`**    | Insects as food are not __`yet mainstream`__ in American culture .                                                                                                                                                        |
    | **`pcc_eng_27_035.6670_x0560193_05:4-5-6`**    | Although soyfoods were n't __`yet mainstream`__ , we recognized early the benefits of a plant- based diet .                                                                                                               |
    
    
    6. _yet final_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                              |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20090729_0128_3:19-20-21`**          | this person spoke Tuesday night on condition on anonymity , confirming earlier reports , because the deal was not __`yet final`__ .                                                                                                                                                                                                                                      |
    | **`nyt_eng_20050805_0117_4:19-20-21`**          | Josh Block , a spokesman for AIPAC , said yesterday that the itinerary for Romney 's trip was not __`yet final`__ , but , based on one prepared for a group of Democratic congressmen who were leaving this weekend , the visit will be dominated by Israeli political figures , with some Palestinians -LRB- among them the top leader , Mahmoud Abbas -RRB- included . |
    | **`pcc_eng_15_015.6343_x0236098_100:15-16-17`** | She and her spouse were separated at the time , but the divorce was not __`yet final`__ .                                                                                                                                                                                                                                                                                |
    | **`apw_eng_20091204_1090_9:24-25-26`**          | that official and others spoke on condition of anonymity because the drone program is classified , and decisions on the training program are not __`yet final`__ .                                                                                                                                                                                                       |
    | **`pcc_eng_21_092.2247_x1474243_4:7-8-9`**      | But the transaction , which is not __`yet final`__ , will have no bearing on Jones ' future in Baltimore .                                                                                                                                                                                                                                                               |
    
    
    7. _yet over_
    
    |                                        | `token_str`                                                                                                                                                                                                                                                                |
    |:---------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20050426_0268_9:43-44-45`** | the current agreement would give United 's bankruptcy judge the authority to choose the termination date -- but the government has reserved the right to appeal his decision in federal court , suggesting that the dispute over the pilots ' plan is not __`yet over`__ . |
    | **`apw_eng_20081027_0437_1:26-27-28`** | India 's benchmark Sensex index fell to its lowest in nearly three years on Monday amid fears that the worst of the financial crisis is not __`yet over`__ .                                                                                                               |
    | **`apw_eng_20090501_0484_9:08-09-10`** | `` We fear that the worst is not __`yet over`__ for many U.K. businesses as the economy continues to contract and credit remains constrained , '' Bingham said .                                                                                                           |
    | **`apw_eng_20020611_0010_1:26-27-28`** | the State Department welcomed a continuation in the easing of tensions between India and Pakistan but said the crisis involving the South Asian rivals is not __`yet over`__ .                                                                                             |
    | **`apw_eng_20021120_0496_6:16-17-18`** | Chief Executive Vittorio Mincato told Dow Jones Newswires that the company 's acquisition spree was not __`yet over`__ , although he declined to identify other possible buys .                                                                                            |
    
    
    8. _yet clear_
    
    |                                                | `token_str`                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_032.6729_x0511748_47:3-4-5`**    | It is not __`yet clear`__ why we some rounds of testing end in widespread agreement or widespread controversy .                                                                                                                           |
    | **`pcc_eng_26_087.5357_x1399329_14:3-4-5`**    | It 's not __`yet clear`__ how many documents the new leaker has shared and how much damage it may cause .                                                                                                                                 |
    | **`pcc_eng_06_108.0435_x1731426_05:43-44-45`** | In the range of mobile , a post on social influence caught my eye , mostly because I think its premise is wrong , it will be important , but not in the way it is currently being use , just is n't __`yet clear`__ how it will be used . |
    | **`nyt_eng_20050906_0203_23:3-4-5`**           | it is not __`yet clear`__ how much of the remaining load represents customers in New Orleans or other flooded areas who may be disconnected for months , or even permanently .                                                            |
    | **`pcc_eng_val_2.06971_x27541_7:3-4-5`**       | It is not __`yet clear`__ whether Samsung will make it , and other Nvelo products , proprietary .                                                                                                                                         |
    
    
    9. _yet ready_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                     |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_069.9999_x1116391_41:4-5-6`**    | While you are not __`yet ready`__ to resume physical activities such as lifting objects or bending over , sitting at a desk is usually easy to tolerate .                                                                                                                                                                                                                                                                       |
    | **`pcc_eng_02_002.7331_x0028054_54:25-26-27`** | But faced with having to create virtually everything for himself , and to set the table for a cast of characters who either are n't __`yet ready`__ for prime time or are still struggling to find their place on an overhauled roster , and to fill the leadership void left by Paul 's at-times - insufferable but always - integral drill- sergeant demeanor , Griffin has n't yet been able to chart a course for victory . |
    | **`pcc_eng_17_044.2195_x0697964_27:26-27-28`** | These " In Progress " guides will still display in your Guide Lists and it will be easily apparent that they are in progress and not __`yet ready`__ for the official published version .                                                                                                                                                                                                                                       |
    | **`pcc_eng_25_030.6875_x0480319_60:14-15-16`** | In December , the U.S. Government Accountability Office said the software was " not __`yet ready`__ for national deployment , " because of software performance issues and delays in scanning paper files .                                                                                                                                                                                                                     |
    | **`pcc_eng_09_012.8737_x0192315_06:12-13-14`** | Fordo 's final 644 machines have also been installed but are not __`yet ready`__ to be put into operation .                                                                                                                                                                                                                                                                                                                     |
    
    
    10. _yet complete_
    
    |                                                | `token_str`                                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_084.3649_x1347219_42:18-19-20`** | Whilst she has learned and been absorbed by the mountain over many years , the journey is not __`yet complete`__ .                                                                                                                                     |
    | **`pcc_eng_03_043.8172_x0693752_41:16-17-18`** | We remember the aborted from 1973 - 2014 with the knowledge that their number is not __`yet complete`__ .                                                                                                                                              |
    | **`pcc_eng_21_019.9157_x0305474_2:08-09-10`**  | " Burma 's transition to democracy is not __`yet complete`__ but it is worth reflecting on just how far Burma has come since Aung San Suu Kyi's National League for Democracy party took office just nine months ago , " Johnson said in a statement . |
    | **`apw_eng_19970707_0507_7:6-7-8`**            | the lists of competitors are not __`yet complete`__ , however , and it is not clear how many women will be competing .                                                                                                                                 |
    | **`pcc_eng_26_004.6403_x0058697_07:6-7-8`**    | " While the investigation is not __`yet complete`__ , based on the facts that the BCA publicly released on Tuesday night , the fatal shooting of Justine Ruszczyk should not have happened .                                                           |
    
    
    11. _yet available_
    
    |                                                | `token_str`                                                                                                                                                                        |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19971223_0630_7:7-8-9`**            | but unlike amantadine , rimantadine is not __`yet available`__ in Hong Kong because the supplier never applied to register the drug here , a Hospital Authority spokeswoman said . |
    | **`pcc_eng_05_031.2138_x0489456_38:6-7-8`**    | I presume cost estimates , not __`yet available`__ , will emerge sometime before senators vote .                                                                                   |
    | **`apw_eng_20020121_0703_13:5-6-7`**           | an overall total was not __`yet available`__ , he said .                                                                                                                           |
    | **`pcc_eng_27_009.6458_x0139511_22:28-29-30`** | A spokeswoman for the Ministry of Justice said that Sir James ' speech was " off the cuff at times " and that a full transcript was not __`yet available`__ .                      |
    | **`pcc_eng_14_015.9149_x0240841_35:4-5-6`**    | Core which is n't __`yet available`__ for F# ( as far as I know ) .                                                                                                                |
    
    
    12. _yet certain_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_029.3484_x0458522_02:34-35-36`** | JPMorgan Chase & Co CEO Jamie Dimon has pleaded with and complained to the U.S. Justice Department but cannot convince the government to end its criminal probe of his bank because prosecutors are not __`yet certain`__ of their findings , people familiar with the matter said . |
    | **`pcc_eng_03_004.1967_x0051457_18:5-6-7`**    | Simcox and colleagues are n't __`yet certain`__ that Dpp's activation of vn explains how all insects got their wings because of differences in the ways these invertebrates develop .                                                                                                |
    | **`pcc_eng_15_001.9572_x0015296_14:12-13-14`** | An update is expected later this week , although it is not __`yet certain`__ if background sync will be a part of that release .                                                                                                                                                     |
    | **`apw_eng_20090227_1247_8:15-16-17`**         | a third was in critical condition Friday and the status of a fourth was not __`yet certain`__ .                                                                                                                                                                                      |
    | **`apw_eng_20030326_0516_7:3-4-5`**            | it 's not __`yet certain`__ when they 'll go to Iraq .                                                                                                                                                                                                                               |
    
    
    13. _yet sure_
    
    |                                                | `token_str`                                                                                                                                                                                                                           |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_009.0852_x0130510_09:28-29-30`** | " They are highly unusual movements , so it appears the weapons are ready for withdrawal , " a UN spokesman said , adding that officials were not __`yet sure`__ whether the guns had begun to roll out of the 20 km exclusion zone . |
    | **`pcc_eng_11_088.0066_x1408339_05:23-24-25`** | Alabama freshman Rep. Mo Brooks , who voted against the initial yearlong deal passed by House Republicans , said he was " not __`yet sure`__ , " whether he 'd protest the deal .                                                     |
    | **`pcc_eng_03_080.4300_x1286302_34:16-17-18`** | She 's hoping to implement her findings in medical school curriculums , though she 's not __`yet sure`__ what that will look like .                                                                                                   |
    | **`pcc_eng_25_009.5596_x0138645_038:3-4-5`**   | She was not __`yet sure`__ where she and Jem would be married , for the Council was still deliberating their situation .                                                                                                              |
    | **`pcc_eng_09_086.2738_x1379599_09:23-24-25`** | So , if anyone out there knows they are meant to do something , but has n't yet begun , or is n't __`yet sure`__ what it is they are meant to do , please email me and let 's talk it through , or comment on this page .             |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/...
    
    Samples saved as...
    1. `neg_bigram_examples/yet/yet_eligible_99ex.csv`
    1. `neg_bigram_examples/yet/yet_official_99ex.csv`
    1. `neg_bigram_examples/yet/yet_convinced_99ex.csv`
    1. `neg_bigram_examples/yet/yet_online_99ex.csv`
    1. `neg_bigram_examples/yet/yet_mainstream_99ex.csv`
    1. `neg_bigram_examples/yet/yet_final_99ex.csv`
    1. `neg_bigram_examples/yet/yet_over_99ex.csv`
    1. `neg_bigram_examples/yet/yet_clear_99ex.csv`
    1. `neg_bigram_examples/yet/yet_ready_99ex.csv`
    1. `neg_bigram_examples/yet/yet_complete_99ex.csv`
    1. `neg_bigram_examples/yet/yet_available_99ex.csv`
    1. `neg_bigram_examples/yet/yet_certain_99ex.csv`
    1. `neg_bigram_examples/yet/yet_sure_99ex.csv`
    
    ## 8. *immediately*
    
    |                         |        `N` |      `f1` |   `adv_total` |
    |:------------------------|-----------:|----------:|--------------:|
    | **NEGATED_immediately** | 72,839,589 | 3,173,660 |        96,973 |
    | **NEGMIR_immediately**  |  1,701,929 |   291,732 |         1,195 |
    
    
    |                                    |    `f` |   `adj_total` |   `dP1` |   `LRC` |       `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:-----------------------------------|-------:|--------------:|--------:|--------:|-----------:|----------:|------------:|-------:|
    | **NEGany~immediately_possible**    |  1,000 |       245,272 |    0.91 |    7.62 |   5,845.77 |     45.92 |      954.08 |  1,054 |
    | **NEGany~immediately_clear**       | 24,416 |       349,214 |    0.89 |    8.16 | 141,186.69 |  1,134.49 |   23,281.51 | 26,038 |
    | **NEGany~immediately_reachable**   |    109 |         2,672 |    0.86 |    5.56 |     610.53 |      5.23 |      103.77 |    120 |
    | **NEGany~immediately_sure**        |    138 |       262,825 |    0.82 |    5.40 |     738.65 |      6.97 |      131.03 |    160 |
    | **NEGany~immediately_certain**     |     70 |        74,952 |    0.71 |    4.19 |     336.68 |      4.05 |       65.95 |     93 |
    | **NEGany~immediately_available**   | 21,078 |       666,909 |    0.67 |    5.70 |  98,046.67 |  1,278.84 |   19,799.16 | 29,351 |
    | **NEGany~immediately_able**        |    626 |       223,196 |    0.59 |    4.70 |   2,655.18 |     43.09 |      582.91 |    989 |
    | **NEGany~immediately_forthcoming** |    133 |         7,473 |    0.55 |    3.89 |     540.70 |      9.72 |      123.28 |    223 |
    | **NEGany~immediately_intuitive**   |     54 |        20,664 |    0.55 |    3.21 |     218.74 |      3.96 |       50.04 |     91 |
    | **NEGmir~immediately_clear**       |     31 |         6,722 |    0.55 |    1.13 |      62.95 |      7.37 |       23.63 |     43 |
    | **NEGany~immediately_obvious**     |  2,238 |       165,439 |    0.52 |    4.55 |   8,712.07 |    173.80 |    2,064.20 |  3,989 |
    | **NEGmir~immediately_available**   |    162 |        10,284 |    0.42 |    1.85 |     241.53 |     47.14 |      114.86 |    275 |
    
    
    1. _immediately possible_
    
    |                                             | `token_str`                                                                                                                                                     |
    |:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19980609_1362_12:6-7-8`**        | verification of the statements was not __`immediately possible`__ .                                                                                             |
    | **`apw_eng_20021202_0441_7:3-4-5`**         | it was not __`immediately possible`__ to reconcile the contradictory claims .                                                                                   |
    | **`pcc_eng_28_048.9783_x0776262_17:3-4-5`** | It was not __`immediately possible`__ to get a comment from Barrick on how a potential strike could affect construction or whether it could delay the project . |
    | **`apw_eng_19970724_0480_5:3-4-5`**         | it was not __`immediately possible`__ to get a comment from Khartoum or from rebel officials in Kenya .                                                         |
    | **`apw_eng_20080724_0187_3:3-4-5`**         | it was not __`immediately possible`__ to verify his claim , though international pilots groups have criticized the police probe into Komar .                    |
    
    
    2. _immediately clear_
    
    |                                                | `token_str`                                                                                                                                                                                                                             |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_011.2750_x0165912_15:20-21-22`** | The Saints could appeal the punishment handed down by NFL Commissioner Roger Goodell on Wednesday , but it was not __`immediately clear`__ whether the Saints intended to explore that option .                                         |
    | **`pcc_eng_28_044.0114_x0695922_43:3-4-5`**    | It was not __`immediately clear`__ why Byrd thought the unalienable right to keep and bear arms -- enshrined in both the Wyoming and U.S. constitutions -- was not meaningful .                                                         |
    | **`pcc_eng_10_077.2972_x1233199_07:24-25-26`** | In Washington , State Department spokesman John Kirby said the United States was also lifting sanctions against nine entities , though it was n't __`immediately clear`__ which individuals and companies the decision would apply to . |
    | **`pcc_eng_17_106.3470_x1703136_24:3-4-5`**    | It was not __`immediately clear`__ what the Islamic State group planned to do with the Assyrians .                                                                                                                                      |
    | **`apw_eng_20081020_0722_7:17-18-19`**         | the newspaper also blamed the deaths of several hundred dogs on melamine , but it was not __`immediately clear`__ how the chemical entered the feed .                                                                                   |
    
    
    3. _immediately reachable_
    
    |                                               | `token_str`                                                                                                                                                         |
    |:----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_064.5853_x1027896_12:3-4-5`**   | Lugovoy was not __`immediately reachable`__ for comment as his mobile phone was switched off .                                                                      |
    | **`pcc_eng_07_017.6275_x0269016_24:5-6-7`**   | A Snapdeal spokeswoman was not __`immediately reachable`__ for comment on the founders ' plans .                                                                    |
    | **`pcc_eng_19_072.1259_x1148812_07:4-5-6`**   | Algerian officials were not __`immediately reachable`__ for comment .                                                                                               |
    | **`pcc_eng_28_013.3710_x0200419_5:09-10-11`** | The U.S. Attorney 's Office in Manhattan was not __`immediately reachable`__ for comment .                                                                          |
    | **`pcc_eng_12_066.5758_x1059785_16:4-5-6`**   | Blizzard Entertainment was not __`immediately reachable`__ for comment , though its customer support Twitter account said the company 's servers were stabilizing . |
    
    
    4. _immediately sure_
    
    |                                                | `token_str`                                                                                                                                                                                                             |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_034.2609_x0538764_26:17-18-19`** | When reached Tuesday by this publication , Tina Pelkey , press secretary for Pai , was not __`immediately sure`__ whether any public hearings are scheduled before the Dec. 14 vote .                                   |
    | **`pcc_eng_05_003.4375_x0039639_07:4-5-6`**    | If you are n't __`immediately sure`__ what type of fence will provide your house the best visual appeal while still accommodating your budgetary needs , then here 's a full analysis on choosing a fencing design .    |
    | **`apw_eng_20021204_0594_5:09-10-11`**         | spokesmen for the Foreign Ministry said they were not __`immediately sure`__ if the discrepancy was due to a slip of the tongue or if one country was not invited .                                                     |
    | **`pcc_eng_19_049.4616_x0782212_14:5-6-7`**    | Cook said she was n't __`immediately sure`__ how Lewis ' DUI would affect his position on the city council .                                                                                                            |
    | **`pcc_eng_11_086.4306_x1382859_33:27-28-29`** | GPS devices aboard the boats enabled the Navy to determine , after the fact , that they were in Iranian waters , but the Navy was not __`immediately sure`__ whether the crew members were safe or had gone overboard . |
    
    
    5. _immediately certain_
    
    |                                             | `token_str`                                                                                                                                                                                                                   |
    |:--------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_19980723_1334_4:5-6-7`**         | he said it was not __`immediately certain`__ whether the accident happened during landing or take-off .                                                                                                                       |
    | **`pcc_eng_07_056.7684_x0901241_06:6-7-8`** | Graham notes it is " not __`immediately certain`__ who else received the preliminary packet . "                                                                                                                               |
    | **`apw_eng_19971018_0570_9:3-4-5`**         | police were not __`immediately certain`__ if the claim was true .                                                                                                                                                             |
    | **`apw_eng_20091226_0014_22:20-21-22`**     | a law enforcement source said the explosives may have been strapped to the man 's body but investigators were n't __`immediately certain`__ , partly because of the struggle with other passengers .                          |
    | **`apw_eng_19970417_0626_27:3-4-5`**        | it was not __`immediately certain`__ what impact Moilim 's edict _ contravention of which carries an automatic but undefined prison sentence without benefit of trial _ would have on the islands ' infant tourism industry . |
    
    
    6. _immediately available_
    
    |                                                 | `token_str`                                                                                                                                                                                        |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_051.6100_x0819324_03:7-8-9`**     | Russian U.N. Ambassador Vassily Nebenzia was not __`immediately available`__ to comment .                                                                                                          |
    | **`apw_eng_20021224_0162_3:7-8-9`**             | further information on the victims was not __`immediately available`__ .                                                                                                                           |
    | **`apw_eng_20090506_0653_5:6-7-8`**             | Demjanjuk 's German attorney was not __`immediately available`__ for comment .                                                                                                                     |
    | **`apw_eng_20090506_0709_4:5-6-7`**             | Bank of America was not __`immediately available`__ to comment on the reports .                                                                                                                    |
    | **`pcc_eng_19_075.3105_x1200507_040:09-11-12`** | But sometimes life happens - special materials may not be __`immediately available`__ to the artist , or there might be some other circumstance beyond our control that could delay the shipment . |
    
    
    7. _immediately able_
    
    |                                                | `token_str`                                                                                                                                                                    |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_003.1745_x0035345_14:09-10-11`** | The Aboriginal Affairs and Northern Affairs Department was not __`immediately able`__ to say whether Enbridge had addressed all of its concerns .                              |
    | **`pcc_eng_26_086.1799_x1377384_20:12-13-14`** | Firefighters confirmed that homes had been damaged , but they were not __`immediately able`__ to verify how many , the Missoulian reported .                                   |
    | **`pcc_eng_04_089.7563_x1433985_42:6-7-8`**    | Transportation spokeswoman Paris Ervin was n't __`immediately able`__ to provide costs for pilots and other expenses .                                                         |
    | **`pcc_eng_11_019.9522_x0306573_26:3-4-5`**    | Prosecutors were not __`immediately able`__ to comment .                                                                                                                       |
    | **`pcc_eng_06_073.6431_x1175070_16:24-25-26`** | Lewis said in an email March 3 those questions are " still pending , " and as of Monday evening , Lewis was not __`immediately able`__ to say if they have been answered yet . |
    
    
    8. _immediately forthcoming_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                    |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_053.7550_x0853901_56:3-5-6`**     | Foley was not always __`immediately forthcoming`__ when questioned by police , according to the probable cause statement , and in several instances only admitted details of the alleged thefts when confronted by police .                                    |
    | **`pcc_eng_22_055.7446_x0884657_121:10-11-12`** | If a question was asked and an answer was n't __`immediately forthcoming`__ , I 'd jump up and say what we could do .                                                                                                                                          |
    | **`pcc_eng_22_087.4141_x1396846_03:13-14-15`**  | The devil is in the details , however , and those were not __`immediately forthcoming`__ .                                                                                                                                                                     |
    | **`pcc_eng_05_034.7526_x0546596_10:7-8-9`**     | When the petting she wants is not __`immediately forthcoming`__ , she complains .                                                                                                                                                                              |
    | **`pcc_eng_13_007.1669_x0099461_01:37-39-40`**  | The Air Force 's newest air superiority fighter under development , the F-22 Raptor , has passed an important combat avionics test , but officials within the program say the decision to begin limited production will not be __`immediately forthcoming`__ . |
    
    
    9. _immediately intuitive_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                              |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_089.4677_x1429224_02:13-14-15`**  | The idea of going into debt to pay off other debts is not __`immediately intuitive`__ , but it can actually be a useful tool to free you from bad debts .                                                                                                                                                |
    | **`pcc_eng_04_108.03993_x1735741_27:14-15-16`** | There is n't much of it yet and the project 's architecture is n't __`immediately intuitive`__ .                                                                                                                                                                                                         |
    | **`pcc_eng_11_090.1038_x1442364_14:39-40-41`**  | Penny Nance , CEO and president of Concerned Women for America 's Legislative Action Committee , praised Congress for turning a slew of House floor speeches condemning Gosnell into action , while acknowledging that clear steps forward are not __`immediately intuitive`__ in a case like this one . |
    | **`pcc_eng_04_044.1133_x0696674_19:4-5-6`**     | Though it 's not __`immediately intuitive`__ that both teams are below 50 per cent in each zone , remember that there are three results in any puck battle .                                                                                                                                             |
    | **`nyt_eng_19990113_0234_39:3-5-6`**            | it may not seem __`immediately intuitive`__ , but that means plasma displays can not render the color black .                                                                                                                                                                                            |
    
    
    10. _immediately obvious_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_038.7046_x0609654_37:5-6-7`**     | This interesting diversion was not __`immediately obvious`__ as on the whole Greek signposts do n't bother with numbers .                                                                                                                               |
    | **`pcc_eng_03_002.2797_x0020683_05:33-34-35`**  | Though they can all be reduced to attractions and aversions based upon the illusion of a real self , which desires certain things and is averse to others , yet this is not __`immediately obvious`__ or a point easily grasped :                       |
    | **`pcc_eng_21_099.8482_x1597090_08:7-8-9`**     | ( " In case it is n't __`immediately obvious`__ this is supposed to be a tree , " etc . )                                                                                                                                                               |
    | **`pcc_eng_26_087.0101_x1390837_08:13-14-15`**  | Flicking through the final edition of the New Day , it 's not __`immediately obvious`__ why the paper did not take off with UK audiences : it seems that those who 'd got their hands on a copy were largely positive about its tone and presentation . |
    | **`pcc_eng_01_108.00537_x1731044_10:10-11-12`** | While the connection between pavement and cliff face is n't __`immediately obvious`__ , it makes sense .                                                                                                                                                |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/...
    
    Samples saved as...
    1. `neg_bigram_examples/immediately/immediately_possible_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_clear_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_reachable_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_sure_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_certain_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_available_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_able_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_forthcoming_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_intuitive_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_obvious_99ex.csv`
    
    ## 9. *particularly*
    
    |                          |        `N` |      `f1` |   `adv_total` |
    |:-------------------------|-----------:|----------:|--------------:|
    | **NEGATED_particularly** | 72,839,589 | 3,173,660 |       513,668 |
    | **NEGMIR_particularly**  |  1,701,929 |   291,732 |        13,003 |
    
    
    |                                       |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:--------------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGany~particularly_likable**       |   119 |         8,160 |    0.85 |    5.53 |   657.49 |      5.79 |      113.21 |    133 |
    | **NEGany~particularly_likeable**      |   106 |         5,902 |    0.84 |    5.34 |   579.07 |      5.23 |      100.77 |    120 |
    | **NEGmir~particularly_novel**         |    54 |           320 |    0.83 |    3.71 |   190.49 |      9.26 |       44.74 |     54 |
    | **NEGmir~particularly_comfortable**   |    44 |         4,642 |    0.83 |    3.36 |   155.21 |      7.54 |       36.46 |     44 |
    | **NEGmir~particularly_revolutionary** |    39 |           485 |    0.83 |    3.15 |   137.57 |      6.69 |       32.31 |     39 |
    | **NEGmir~particularly_radical**       |    31 |         1,072 |    0.83 |    2.73 |   109.35 |      5.31 |       25.69 |     31 |
    | **NEGmir~particularly_fast**          |    26 |         1,259 |    0.83 |    2.39 |    91.71 |      4.46 |       21.54 |     26 |
    | **NEGmir~particularly_surprising**    |   166 |         2,662 |    0.82 |    5.06 |   564.67 |     28.80 |      137.20 |    168 |
    | **NEGany~particularly_forthcoming**   |    72 |         7,473 |    0.82 |    4.85 |   387.25 |      3.62 |       68.38 |     83 |
    | **NEGany~particularly_religious**     |   485 |        28,028 |    0.81 |    6.12 | 2,585.71 |     24.62 |      460.38 |    565 |
    | **NEGmir~particularly_new**           |   404 |        12,836 |    0.81 |    5.92 | 1,365.17 |     70.28 |      333.72 |    410 |
    | **NEGmir~particularly_wrong**         |   212 |        20,880 |    0.81 |    5.05 |   702.22 |     37.20 |      174.80 |    217 |
    | **NEGany~particularly_original**      |   360 |        37,594 |    0.80 |    5.86 | 1,894.60 |     18.56 |      341.44 |    426 |
    | **NEGmir~particularly_remarkable**    |   108 |         3,238 |    0.80 |    4.24 |   354.53 |     19.03 |       88.97 |    111 |
    | **NEGany~particularly_new**           |   747 |       253,862 |    0.79 |    6.04 | 3,874.46 |     39.21 |      707.79 |    900 |
    | **NEGmir~particularly_close**         |   136 |        13,874 |    0.77 |    4.01 |   415.70 |     24.85 |      111.15 |    145 |
    | **NEGany~particularly_athletic**      |   108 |        17,142 |    0.75 |    4.77 |   541.01 |      5.93 |      102.07 |    136 |
    | **NEGany~particularly_revolutionary** |    77 |        10,338 |    0.75 |    4.49 |   385.60 |      4.23 |       72.77 |     97 |
    | **NEGany~particularly_flashy**        |    57 |         4,494 |    0.73 |    4.08 |   278.96 |      3.22 |       53.78 |     74 |
    | **NEGany~particularly_surprising**    | 1,069 |        70,540 |    0.57 |    4.71 | 4,433.52 |     75.94 |      993.06 |  1,743 |
    
    
    1. _particularly likable_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                           |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_057.6626_x0915871_08:12-13-14`**  | We 've had underdog seasons before but when the underdogs are n't __`particularly likable`__ and they are only underdogs because the game is rigged against them I have to wonder what the fun in this .                                                                                              |
    | **`pcc_eng_26_031.9732_x0500519_052:36-48-49`** | The almost-unbearable bittersweetness of Li's carefully closing Chou 's suitcase and handing it to her , and then standing by the window and watching her as she leaves , is complicated by the fact that neither of these characters , nor any other in Terrorizer , is __`particularly likable`__ . |
    | **`nyt_eng_19981228_0086_28:4-5-6`**            | `` She 's not __`particularly likable`__ , '' the actress adds , `` and we enjoy not liking her .                                                                                                                                                                                                     |
    | **`pcc_eng_22_006.5138_x0088996_18:10-11-12`**  | In short , Tom Rhys Harries 's character is n't __`particularly likable`__ , to a point where a predictable switchover into a redemptive , understanding attitude would n't really work .                                                                                                             |
    | **`pcc_eng_10_076.7803_x1224818_368:3-4-5`**    | She is not __`particularly likable`__ and she portrays Rachel as a controlling , toxic , mean girl , queen bee too ; even so Aubrey 's lashing out at those who want to change Rachel 's character after death is violent and self-destructive .                                                      |
    
    
    2. _particularly likeable_
    
    |                                                 | `token_str`                                                                                                                                                                 |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_052.4338_x0832532_021:4-5-6`**    | The Op is n't __`particularly likeable`__ .                                                                                                                                 |
    | **`pcc_eng_05_084.9030_x1357825_17:15-20-21`**  | His choice made for a refreshing change as did the fact that pretty much none of the characters were __`particularly likeable`__ or sympathetic .                           |
    | **`pcc_eng_01_043.1171_x0680608_16:3-4-5`**     | Sam is n't __`particularly likeable`__ .                                                                                                                                    |
    | **`pcc_eng_29_080.9423_x1291429_15:08-09-10`**  | This character , Captain Nicholl , is not __`particularly likeable`__ , and Verne 's more heroic characters answer all his challenges .                                     |
    | **`pcc_eng_15_044.2034_x0698529_041:13-14-15`** | Worse , while Erdman creates a somewhat humorous character , he is not __`particularly likeable`__ , and the audience simply does not care what happens to him in the end . |
    
    
    3. _particularly novel_
    
    |                                                 | `token_str`                                                                                                                                                                      |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_064.3182_x1023716_003:1-2-3`**    | Nothing __`particularly novel`__ about this porno scene -- it 's a standard - issue boy-girl vignette .                                                                          |
    | **`pcc_eng_13_092.5269_x1479594_125:09-10-11`** | Although I really enjoyed it , there is nothing __`particularly novel`__ in the story .                                                                                          |
    | **`pcc_eng_03_085.6512_x1370701_05:17-18-19`**  | In a city where five-star restaurants are tucked away in nondescript strip malls , there 's nothing __`particularly novel`__ about a high / low culinary mash- up .              |
    | **`pcc_eng_08_072.6067_x1159294_09:14-15-16`**  | The idea that ISPs might be interested in hosting cloud services is thus not __`particularly novel`__ , nor is it particularly hard for them to stand a cloud service up today . |
    | **`pcc_eng_00_036.7442_x0577427_070:11-12-13`** | The audience went nuts and got two fitting , if not __`particularly novel`__ ( or energizing ) , Schumann ( ? ) encores .                                                        |
    
    
    4. _particularly comfortable_
    
    |                                                 | `token_str`                                                                                                                                                                      |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_008.0430_x0113659_076:5-7-8`**    | The United States has never been __`particularly comfortable`__ with the idea of Indian nations and Indian people within its territorial boundaries .                            |
    | **`pcc_eng_04_003.1740_x0035273_09:5-6-7`**     | Josh : I am not __`particularly comfortable`__ with sharing the specifics of my OCD .                                                                                            |
    | **`pcc_eng_04_104.6121_x1673855_057:20-21-22`** | Lauren seemed very frustrated with Bo in this episode , and we again got a sense that Lauren is n't __`particularly comfortable`__ with Bo needing to feed off of other people . |
    | **`pcc_eng_02_087.1698_x1393214_28:10-11-12`**  | Fx F / Mx M - I 'm just not __`particularly comfortable`__ with writing anything that goes beyond PG rating in these genres .                                                    |
    | **`pcc_eng_23_003.3323_x0037537_3:3-4-5`**      | I am not __`particularly comfortable`__ in bars or clubs .                                                                                                                       |
    
    
    5. _particularly revolutionary_
    
    |                                               | `token_str`                                                                                                                                                                                                                                          |
    |:----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_086.2727_x1380169_29:1-6-7`**   | Neither of those ideas is __`particularly revolutionary`__ or technically challenging - and each relies on the GPS chip alone .                                                                                                                      |
    | **`nyt_eng_19980331_0163_17:7-8-9`**          | in fact , his ideas are not __`particularly revolutionary`__ .                                                                                                                                                                                       |
    | **`pcc_eng_03_044.3886_x0703020_16:4-5-6`**   | Cool , but not __`particularly revolutionary`__ .                                                                                                                                                                                                    |
    | **`pcc_eng_20_039.0919_x0615663_3:20-21-22`** | I 'm always fascinated by behind - the-scenes peeks at how things are made , and while there 's nothing __`particularly revolutionary`__ with the way that Sparco builds seats and race suits , it 's still interesting to see where they 're made . |
    | **`pcc_eng_22_002.2947_x0021041_37:1-2-3`**   | Not __`particularly revolutionary`__ but a pleasant , relaxing three - minutes though it does end as if he forgot to play the finish to the song .                                                                                                   |
    
    
    6. _particularly radical_
    
    |                                                | `token_str`                                                                                                                                                                                                                             |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_088.6709_x1418290_31:6-7-8`**    | Though his policy positions are n't __`particularly radical`__ by European standards , Sanders ' candidacy inspired hope in people who'd otherwise given up on seeing their opinions and interests represented in mainstream politics . |
    | **`pcc_eng_01_099.3235_x1589505_12:3-4-5`**    | There 's nothing __`particularly radical`__ about these statistics .                                                                                                                                                                    |
    | **`pcc_eng_29_098.3909_x1573484_21:14-15-16`** | Later , he added : " What I 'm talking about tomorrow is not __`particularly radical`__ .                                                                                                                                               |
    | **`pcc_eng_22_004.1462_x0051002_132:3-4-5`**   | Even a not __`particularly radical`__ report last year from the home affairs select committee , recommending reform and the possibility of decriminalising cannabis , was speedily dismissed by the government .                        |
    | **`pcc_eng_06_073.9183_x1179481_16:4-5-6`**    | And there 's nothing __`particularly radical`__ about it : it 's just common sense .                                                                                                                                                    |
    
    
    7. _particularly fast_
    
    |                                                | `token_str`                                                                                                                                            |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_val_2.04098_x22863_146:3-4-5`**     | Fuller is not __`particularly fast`__ but he is quick instead for a bigger cornerback .                                                                |
    | **`pcc_eng_26_091.9807_x1471355_34:6-7-8`**    | That 's because Rivers is not __`particularly fast`__ -- he ran a 5.08 in the 40 - yard dash before the draft -- and he lacks a consistent deep ball . |
    | **`pcc_eng_11_081.0801_x1296230_6:4-5-6`**     | The process is not __`particularly fast`__ but it is very accurate and very economical when cutting metals that are difficult to process .             |
    | **`pcc_eng_00_004.1128_x0050254_33:09-10-11`** | In terms of performance , the Scooba is n't __`particularly fast`__ at the job , but what it lacks in speed it makes up for in thoroughness .          |
    | **`nyt_eng_20061129_0299_44:09-10-11`**        | it was typical of Brady , who is not __`particularly fast`__ .                                                                                         |
    
    
    8. _particularly forthcoming_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                      |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_076.2055_x1216497_20:3-4-5`**     | He was not __`particularly forthcoming`__ .                                                                                                                                                                                                      |
    | **`pcc_eng_29_003.9387_x0047565_09:1-3-4`**     | Nobody was __`particularly forthcoming`__ about what was discussed , but there was no doubt plenty of discussion about where they go from here .                                                                                                 |
    | **`pcc_eng_23_039.3177_x0619144_077:29-31-32`** | Doombot shows up to give Victor a new body , but Victor does n't like the buff , weaponized Transformers body that Doombot makes , though Victor is n't being __`particularly forthcoming`__ about his hang-ups .                                |
    | **`pcc_eng_03_098.5024_x1578627_61:4-5-6`**     | When he is n't __`particularly forthcoming`__ , they gauge his eye out .                                                                                                                                                                         |
    | **`pcc_eng_13_005.9905_x0080443_37:08-10-11`**  | Editors , producers , and journalists have not been __`particularly forthcoming`__ in acknowledging to their own viewers , the media-consuming public , the degree to which the object of their reporting dictates its content and composition . |
    
    
    9. _particularly surprising_
    
    |                                                | `token_str`                                                                                                                                                                                                                                        |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_008.4340_x0120692_64:3-4-5`**    | That is n't __`particularly surprising`__ , considering the statistics around unintended pregnancy .                                                                                                                                               |
    | **`pcc_eng_19_078.3106_x1248943_04:3-4-5`**    | That 's not __`particularly surprising`__ given the fact that the first quarter set cord cutting records , and the second quarter is expected to be significantly worse .                                                                          |
    | **`pcc_eng_19_077.9535_x1243207_04:20-21-22`** | Seemingly no amount of nonsense from Barton can diminish his standing among conservative Christian activists , so it was not __`particularly surprising`__ to see him spend 2014 spreading misinformation and shoddy history without consequence . |
    | **`pcc_eng_01_068.6010_x1093571_172:3-4-5`**   | That is n't __`particularly surprising`__ , of course .                                                                                                                                                                                            |
    | **`pcc_eng_23_016.6955_x0253207_29:3-4-5`**    | It 's not __`particularly surprising`__ , but still interesting .                                                                                                                                                                                  |
    
    
    10. _particularly religious_
    
    |                                                 | `token_str`                                                                                                                                                                                             |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_047.2039_x0747408_12:4-5-6`**     | If you are not __`particularly religious`__ , just try to be in a quiet surrounding by yourself .                                                                                                       |
    | **`pcc_eng_08_073.2931_x1170423_006:11-12-13`** | So , in effect , my brother and I were n't __`particularly religious`__ as well .                                                                                                                       |
    | **`pcc_eng_24_077.6374_x1239678_15:3-4-5`**     | Elves are not __`particularly religious`__ , so we have only seen a few of their number among our ranks as Holy Knights .                                                                               |
    | **`pcc_eng_18_036.7245_x0578132_30:20-21-22`**  | He tells his parents ( and his religious relatives ) that he does eat pork and that he 's not __`particularly religious`__ .                                                                            |
    | **`pcc_eng_12_085.6940_x1368527_132:27-28-29`** | I might add again that while out at my daughter 's house this last weekend , I was listening to a 50 year old man ( not __`particularly religious`__ ) explaining to everybody just what your soul is . |
    
    
    11. _particularly new_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                    |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_007.3944_x0103849_018:4-5-6`**   | Zone blitzes are not __`particularly new`__ , but while the " blitz " element continues to receive the most attention , it 's the continuing changes in the coverage behind it that make zone blitzes the most important defensive tactic in modern football . |
    | **`pcc_eng_22_051.2244_x0811405_07:08-09-10`** | As that implies , the works are not __`particularly new`__ .                                                                                                                                                                                                   |
    | **`pcc_eng_13_002.9901_x0031908_12:3-4-5`**    | This is not __`particularly new`__ ; three - dimensional modeling software has been around for several years .                                                                                                                                                 |
    | **`pcc_eng_13_039.8173_x0627560_09:33-34-35`** | The addition of achievements and purchasable bonuses - such as in - game collectables boost and invisibility , to a one-time , start - of - the - run enhancement - are n't __`particularly new`__ in the genre either , but they do add some longevity .      |
    | **`nyt_eng_20060222_0281_19:1-6-7`**           | nor would the deal be __`particularly new`__ in the world of global shipping .                                                                                                                                                                                 |
    
    
    12. _particularly wrong_
    
    |                                                | `token_str`                                                                                                                                                                                              |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_090.5334_x1449964_43:3-4-5`**    | There 's nothing __`particularly wrong`__ about any those ideas .                                                                                                                                        |
    | **`pcc_eng_22_081.0584_x1293917_26:37-38-39`** | It 's a bit like hammering in a thumb tack , but if a hammer is readily available and no one 's told you that thumb tacks can be pushed in by hand , there 's nothing __`particularly wrong`__ with it . |
    | **`pcc_eng_21_068.4164_x1089455_10:16-17-18`** | Now , having said that , my next step is to argue that there is nothing __`particularly wrong`__ with deciding not to vote .                                                                             |
    | **`pcc_eng_12_006.5851_x0090091_06:3-4-5`**    | There is nothing __`particularly wrong`__ with the musical content or with the performance .                                                                                                             |
    | **`pcc_eng_03_002.1709_x0018955_04:4-5-6`**    | The game does nothing __`particularly wrong`__ - but by that token , it also does n't do anything particularly well .                                                                                    |
    
    
    13. _particularly remarkable_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                             |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19960502_0699_20:37-38-39`**        | while Thursday 's numbers are extraordinarily good compared with expectations _ Merrill Lynch & Co. , along with many other forecasters , predicted only a 1.5 percent annual growth rate for the quarter _ they are not __`particularly remarkable`__ when viewed against other economic advances since World War II . |
    | **`pcc_eng_20_044.1172_x0696612_12:5-6-7`**    | The project itself was not __`particularly remarkable`__ .                                                                                                                                                                                                                                                              |
    | **`pcc_eng_17_003.0217_x0032447_06:08-09-10`** | glance , at least , there 's nothing __`particularly remarkable`__ about Tom Stall ( Viggo Mortensen ) .                                                                                                                                                                                                                |
    | **`pcc_eng_16_087.2204_x1395697_02:13-14-15`** | The " Bishop Hill " blog was well - respected , but not __`particularly remarkable`__ until the posting of " Caspar and the Jesus paper " in August 2008 .                                                                                                                                                              |
    | **`pcc_eng_13_035.0170_x0549980_03:34-35-36`** | Instead of the latest world news , we get to hear interviews with alumni of the school , trying to make that one professor they had seem special , even if there was nothing __`particularly remarkable`__ about them in their memory .                                                                                 |
    
    
    14. _particularly original_
    
    |                                              | `token_str`                                                                                                                                           |
    |:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_084.4553_x1348911_05:6-7-8`**  | It is very broad and not __`particularly original`__ , but do n't let that deter you - it does what it does very well .                               |
    | **`pcc_eng_15_042.8584_x0676807_008:5-6-7`** | Whilst their sound is n't __`particularly original`__ , THE ROYAL injected plenty of energy to warm up the crowd on the first day of UK Tech - Fest ! |
    | **`pcc_eng_00_067.3333_x1072201_25:5-6-7`**  | It " sentiment is n't __`particularly original`__ , and it 's definitely not good for the state .                                                     |
    | **`pcc_eng_26_085.8858_x1372655_125:4-5-6`** | I will say nothing __`particularly original`__ here , so feel free to whistle your own cheerful tune as you read this .                               |
    | **`pcc_eng_28_020.4107_x0313816_11:5-6-7`**  | Though his words were n't __`particularly original`__ or poetic , they still reverberated through me .                                                |
    
    
    15. _particularly close_
    
    |                                                | `token_str`                                                                                                                                                                                                                                              |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_048.4726_x0768322_68:3-5-6`**    | This wo n't be __`particularly close`__ to what the lineup looks like .                                                                                                                                                                                  |
    | **`pcc_eng_12_067.4155_x1073334_23:16-17-18`** | James Harden is the best offensive player in the NBA right now and it is n't __`particularly close`__ .                                                                                                                                                  |
    | **`pcc_eng_17_106.9693_x1713122_27:4-5-6`**    | If they are not __`particularly close`__ with Grandma , you can use a teacher they adore , the principal at school or anyone else they respect , as their moral compass for social media posts .                                                         |
    | **`pcc_eng_13_088.3964_x1412478_014:4-5-6`**   | While that seems not __`particularly close`__ to the idea of a camera , it was a kind of useful preparation for camera making in that the frames had to be both light - weight and strong while allowing for the smooth operation of hinges and clasps . |
    | **`nyt_eng_20050628_0055_21:1-2-3`**           | never __`particularly close`__ to John F. Kerry , he nonetheless seemed to be the junior senator 's only ally during the bleakest , loneliest days of the Iowa caucus , thundering before crowds while quietly urging Kerry to do more and do better .   |
    
    
    16. _particularly athletic_
    
    |                                                 | `token_str`                                                                                                                                                                     |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_022.3446_x0344744_064:09-10-11`** | They were interviewing all these people that were n't __`particularly athletic`__ or even particularly fit for their whole lives .                                              |
    | **`nyt_eng_20070425_0257_66:08-14-15`**         | Calvin Sr. still seems to marvel that nobody else in the family is __`particularly athletic`__ .                                                                                |
    | **`pcc_eng_18_045.9344_x0727244_39:4-5-6`**     | He also is n't __`particularly athletic`__ .                                                                                                                                    |
    | **`pcc_eng_21_010.3788_x0151386_049:3-5-6`**    | I had never been __`particularly athletic`__ , but I thought , " Well , why ca n't I develop some athleticism in this way ? "                                                   |
    | **`pcc_eng_00_031.8889_x0499187_239:3-4-5`**    | I 'm not __`particularly athletic`__ , and I 'm not fond of heights , which is n't really a great combination when it comes to flying around on a broom and playing quidditch . |
    
    
    17. _particularly flashy_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                    |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_033.6695_x0528216_105:22-23-24`** | Karabacek 's offensive game is more north - south than east-west , which works well for the scoring winger who is not __`particularly flashy`__ .                                                                                              |
    | **`pcc_eng_24_029.5903_x0462387_04:3-4-5`**     | There 's nothing __`particularly flashy`__ about Illume Bistro , other than a menu composed by celebrity chef Bradley Ogden and an interior lighted , in places , by rainbow colors that rotate from yellow to blue to lavender to raspberry . |
    | **`pcc_eng_08_045.3495_x0717738_01:17-18-19`**  | When you see a carton of ice cream from Babcock Hall Dairy Plant , it 's not __`particularly flashy`__ .                                                                                                                                       |
    | **`pcc_eng_25_009.8563_x0143428_06:3-4-5`**     | He 's not __`particularly flashy`__ , but has a combination of skill and intelligence that should lead to a long and successful NFL career .                                                                                                   |
    | **`pcc_eng_02_006.2338_x0084607_09:17-18-19`**  | In this chapter , we explore Calendar and Contacts , a pair of apps that are n't __`particularly flashy`__ but can be remarkably useful .                                                                                                      |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/...
    
    Samples saved as...
    1. `neg_bigram_examples/particularly/particularly_likable_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_likeable_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_novel_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_comfortable_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_revolutionary_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_radical_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_fast_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_forthcoming_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_surprising_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_religious_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_new_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_wrong_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_remarkable_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_original_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_close_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_athletic_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_flashy_99ex.csv`
    
    ## 10. *inherently*
    
    |                        |        `N` |      `f1` |   `adv_total` |
    |:-----------------------|-----------:|----------:|--------------:|
    | **NEGMIR_inherently**  |  1,701,929 |   291,732 |         5,133 |
    | **NEGATED_inherently** | 72,839,589 | 3,173,660 |        47,803 |
    
    
    |                                   |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:----------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGmir~inherently_improper**    |    18 |           142 |    0.83 |    1.63 |    63.49 |      3.09 |       14.91 |     18 |
    | **NEGmir~inherently_illegal**     |    26 |           937 |    0.79 |    2.10 |    83.54 |      4.63 |       21.37 |     27 |
    | **NEGany~inherently_wrong**       | 1,639 |       149,064 |    0.66 |    5.36 | 7,535.97 |    100.87 |    1,538.13 |  2,315 |
    | **NEGmir~inherently_wrong**       | 1,513 |        20,880 |    0.66 |    4.08 | 3,787.53 |    313.00 |    1,200.00 |  1,826 |
    | **NEGmir~inherently_bad**         |   148 |        10,261 |    0.62 |    2.86 |   342.53 |     32.23 |      115.77 |    188 |
    | **NEGany~inherently_illegal**     |    59 |        30,194 |    0.60 |    3.51 |   252.59 |      4.01 |       54.99 |     92 |
    | **NEGmir~inherently_better**      |    44 |        14,013 |    0.57 |    1.65 |    93.95 |     10.11 |       33.89 |     59 |
    | **NEGany~inherently_bad**         |   794 |       429,537 |    0.56 |    4.62 | 3,270.68 |     56.95 |      737.05 |  1,307 |
    | **NEGmir~inherently_evil**        |    58 |         1,271 |    0.41 |    1.18 |    85.70 |     16.97 |       41.03 |     99 |
    | **NEGany~inherently_negative**    |    75 |        53,385 |    0.35 |    2.50 |   222.63 |      8.41 |       66.59 |    193 |
    | **NEGany~inherently_evil**        |   358 |        22,706 |    0.28 |    2.81 |   905.80 |     48.93 |      309.07 |  1,123 |
    | **NEGany~inherently_good**        |   283 |     1,681,795 |    0.20 |    2.21 |   554.72 |     51.28 |      231.72 |  1,177 |
    | **NEGany~inherently_problematic** |    58 |        33,408 |    0.17 |    1.17 |    98.70 |     12.07 |       45.93 |    277 |
    
    
    1. _inherently improper_
    
    |                                                | `token_str`                                                                                                                                                                                                            |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_080.7030_x1290624_65:4-5-6`**    | There 's absolutely nothing __`inherently improper`__ with moderate amounts of caffeine , but it can influence your essential indications , which can make an accurate reading of your true health tough .             |
    | **`pcc_eng_07_020.9121_x0321975_55:16-17-18`** | Law firms advance expenses for clients as a matter of course , so there 's nothing __`inherently improper`__ about a lawyer covering a particular payment and then being reimbursed for it .                           |
    | **`pcc_eng_05_006.9207_x0096212_08:11-13-14`** | Valukas states that although the Repo 105 transaction was perhaps not ' __`inherently improper`__ , there is a colourable claim ** that their sole function as employed by Lehman was balance sheet manipulation .     |
    | **`pcc_eng_00_034.9912_x0549040_3:23-24-25`**  | However , the court decided to take the approach of a substantial minority of states , and concluded that " it is not __`inherently improper`__ for a court to consider the possibility of inheritance in some cases . |
    | **`pcc_eng_11_082.2722_x1315490_37:17-18-19`** | Law firms advance expenses for clients as a matter of course , and so there 's nothing __`inherently improper`__ about a lawyer covering a particular payment and then being reimbursed for it .                       |
    
    
    2. _inherently illegal_
    
    |                                              | `token_str`                                                                                                                                                                                                                                                                        |
    |:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_009.0617_x0130434_11:5-6-7`**  | Personally , I see nothing __`inherently illegal`__ with discrimination by individuals or private companies .                                                                                                                                                                      |
    | **`pcc_eng_19_042.3949_x0668324_003:6-7-8`** | While that practice itself is n't __`inherently illegal`__ because wastewater treatment plants can effectively handle liquid medical waste as they would residential waste , the way hospitals actually do it can get them into serious trouble if they 're not careful or smart . |
    | **`nyt_eng_19980311_0164_15:5-6-7`**         | becoming a monopoly is not __`inherently illegal`__ .                                                                                                                                                                                                                              |
    | **`nyt_eng_19960318_0590_10:14-15-16`**      | a shortage of a specific security or contract that creates a squeeze is not __`inherently illegal`__ , according to the U.S. Securities and Exchange Commission .                                                                                                                  |
    | **`pcc_eng_05_030.8763_x0484001_11:4-5-6`**  | While there 's nothing __`inherently illegal`__ about an arranged marriage .                                                                                                                                                                                                       |
    
    
    3. _inherently wrong_
    
    |                                                | `token_str`                                                                                                                                        |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_040.7497_x0643159_44:3-4-5`**    | There 's nothing __`inherently wrong`__ with these products -- I 'll just say that upfront .                                                       |
    | **`pcc_eng_21_018.3110_x0279526_28:21-22-23`** | While it 's easy to make fun of Americans ' drive to save time in the kitchen , there 's nothing __`inherently wrong`__ with it .                  |
    | **`pcc_eng_24_094.3560_x1509907_06:3-4-5`**    | There is nothing __`inherently wrong`__ with contributing money to education , even if it is sometimes referred to as " checkbook philanthropy . " |
    | **`nyt_eng_20000620_0071_22:5-6-7`**           | after all there is nothing __`inherently wrong`__ with a sandwich .                                                                                |
    | **`pcc_eng_03_036.5857_x0576422_15:3-4-5`**    | There is nothing __`inherently wrong`__ with being a hypocrite .                                                                                   |
    
    
    4. _inherently bad_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_056.9443_x0903833_28:6-7-8`**     | First off - fear is not __`inherently bad`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_11_058.2502_x0926236_11:4-5-6`**     | Being debt-conscious is n't __`inherently bad`__ -- in fact , being able to see past the convenience of credit cards to their potential pitfalls is a responsible perspective to have .                                                                                                                                                                                                                                                                                                                                                                                           |
    | **`pcc_eng_03_090.8383_x1454748_007:10-11-12`** | Of course , extending loans for infrastructure projects is not __`inherently bad`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    | **`pcc_eng_08_003.0941_x0034013_15:4-5-6`**     | Those things are n't __`inherently bad`__ , it should be said .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
    | **`pcc_eng_22_058.4445_x0928659_13:14-18-19`**  | So let me be clear : I vehemently hate hate hate this stuff not because it 's __`inherently bad`__ as a musical product , but because it 's both : a. ) wholly unoriginal / uninspiring / and unimaginatively untrue , and also because it 's b. ) not only killing , but striking the final nails into the coffin of the culture I not only think deserves to live , but absolutely needs to live ( and thrive ) if we as a generation shitted on by neo-conservative politics and stifling monopoly media productions have any shot at reclaiming our agency on a large scale . |
    
    
    5. _inherently better_
    
    |                                              | `token_str`                                                                                                                                                                         |
    |:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_084.2483_x1346573_66:3-4-5`**  | Women are not __`inherently better`__ than men .                                                                                                                                    |
    | **`pcc_eng_07_061.7390_x0981760_087:3-4-5`** | There is nothing __`inherently better`__ about participating in somebody else 's worldview instead of your own .                                                                    |
    | **`pcc_eng_05_088.1681_x1410316_12:4-8-9`**  | " It 's not that online is __`inherently better`__ or worse -- it's that taking a course online allows you to complete a program you could n't otherwise . "                        |
    | **`pcc_eng_09_033.3803_x0524221_104:5-6-7`** | Canadian tar sands are not __`inherently better`__ or safer , quite the opposite , they require the construction of massive and unstable infrastructure that will eventually fail . |
    | **`pcc_eng_29_037.3069_x0585949_1:7-8-9`**   | relationship or tension with them , not __`inherently better`__ or worse ) that are equally observable , analysable and researcher - researched accountable .                       |
    
    
    6. _inherently evil_
    
    |                                                | `token_str`                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19970209_0210_27:4-5-6`**           | `` There is nothing __`inherently evil`__ about these people , but today 's local monopolists are shrewder than I was 15 years ago , '' he said .                                                                                          |
    | **`pcc_eng_19_042.5471_x0670741_13:09-10-11`** | Suffice it to say that the doll is n't __`inherently evil`__ but soon is possessed by the spirit of someone named Annabelle .                                                                                                              |
    | **`pcc_eng_23_082.8446_x1322597_10:31-32-33`** | The people who will be hurt , though , are the shop owners who have been selling legal products that can be used for illicit purposes , but which are n't __`inherently evil`__ .                                                          |
    | **`pcc_eng_29_005.8734_x0078975_046:1-7-8`**   | Not all the Daedric Princes are __`inherently evil`__ .                                                                                                                                                                                    |
    | **`pcc_eng_07_005.4878_x0072573_31:27-28-29`** | The two mirror-verse characters that were most developed were Spock and Marlena , both of whom were sympathetic people , indicating that the mirror-verse inhabitants were n't __`inherently evil`__ , but shaped by their circumstances . |
    
    
    7. _inherently negative_
    
    |                                              | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
    |:---------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_067.1870_x1071296_28:1-6-7`**  | Neither of these drives are __`inherently negative`__ unless they are taken to an extreme .                                                                                                                                                                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_02_004.9962_x0064467_037:5-6-7`** | It is neither insidious nor __`inherently negative`__ by artifice ; rather , it is the most natural of sensibilities , arising from a knowledge that reliance upon one another not only acknowledges and validates the vows of matrimony , but moreover , the eternal commitment each makes to the other forever forges the bonds of undiluted friendship , like kindred spirits floating in some ethereal universe unperturbed by distractions of consternation consecrated upon the altar of destruction . |
    | **`pcc_eng_00_063.4598_x1009757_09:7-8-9`**  | Things , in reality , are not __`inherently negative`__ , they are seen as dark by you , the observer -- and when you turn away from this darkness you have created , it breeds into more darkness within you .                                                                                                                                                                                                                                                                                              |
    | **`pcc_eng_23_007.8573_x0110795_17:3-4-5`**  | There is nothing __`inherently negative`__ about the word " liberal . "                                                                                                                                                                                                                                                                                                                                                                                                                                      |
    | **`pcc_eng_18_083.9657_x1343524_070:3-4-5`** | Stereotypes are not __`inherently negative`__ , he said .                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
    
    
    8. _inherently good_
    
    |                                                | `token_str`                                                                                                        |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_010.1459_x0147623_13:06-10-11`** | The trick behind Supergirl is n't that Kara is __`inherently good`__ , but that we all are capable of being good . |
    | **`pcc_eng_01_041.2169_x0649988_234:4-5-6`**   | And tools are never __`inherently good`__ or inherently evil .                                                     |
    | **`pcc_eng_14_039.2310_x0617675_17:08-10-11`** | As far as I am concerned , nothing is __`inherently good`__ or bad .                                               |
    | **`pcc_eng_09_043.6101_x0689447_73:7-8-9`**    | An impossibly powerful tyrant who is not __`inherently good`__ just because he 's superhuman .                     |
    | **`pcc_eng_03_097.3465_x1559816_39:5-6-7`**    | Queensland 's ban is n't __`inherently good`__ or bad .                                                            |
    
    
    9. _inherently problematic_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_101.9856_x1633608_22:31-32-33`** | Trying to fit new kinds of energy into infrastructures not designed for them is expensive , and creates complications -- the fact that solar resources fluctuate throughout the day is n't __`inherently problematic`__ , but it is a problem when paired with an infrastructure that ca n't deal with fluctuation . |
    | **`pcc_eng_08_076.8451_x1228028_14:4-5-6`**    | This model is n't __`inherently problematic`__ .                                                                                                                                                                                                                                                                     |
    | **`pcc_eng_25_041.4217_x0654254_40:04-09-10`** | " It 's not that pre-made forms are __`inherently problematic`__ , " she says .                                                                                                                                                                                                                                      |
    | **`pcc_eng_11_013.3608_x0199808_21:3-8-9`**    | It 's not that the cross-cutting is __`inherently problematic`__ .                                                                                                                                                                                                                                                   |
    | **`pcc_eng_13_098.5673_x1576660_031:7-8-9`**   | Of course , these approaches are n't __`inherently problematic`__ , and they 're often immensely helpful .                                                                                                                                                                                                           |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/...
    
    Samples saved as...
    1. `neg_bigram_examples/inherently/inherently_improper_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_illegal_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_wrong_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_bad_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_better_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_evil_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_negative_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_good_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_problematic_99ex.csv`
    
    ## 11. *terribly*
    
    |                      |        `N` |      `f1` |   `adv_total` |
    |:---------------------|-----------:|----------:|--------------:|
    | **NEGATED_terribly** | 72,839,589 | 3,173,660 |        58,964 |
    | **NEGMIR_terribly**  |  1,701,929 |   291,732 |         4,610 |
    
    
    |                                 |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
    |:--------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
    | **NEGany~terribly_surprising**  |   949 |        70,540 |    0.94 |    8.66 | 5,794.10 |     42.00 |      907.00 |    964 |
    | **NEGany~terribly_uncommon**    |   103 |        11,312 |    0.94 |    6.33 |   625.85 |      4.57 |       98.43 |    105 |
    | **NEGany~terribly_likely**      |   108 |       890,421 |    0.93 |    6.26 |   649.50 |      4.84 |      103.16 |    111 |
    | **NEGany~terribly_productive**  |    64 |       102,361 |    0.91 |    5.39 |   376.84 |      2.92 |       61.08 |     67 |
    | **NEGany~terribly_original**    |   199 |        37,594 |    0.90 |    6.41 | 1,150.48 |      9.24 |      189.76 |    212 |
    | **NEGany~terribly_unusual**     |   146 |        71,234 |    0.90 |    6.17 |   847.05 |      6.75 |      139.25 |    155 |
    | **NEGany~terribly_reliable**    |    51 |        90,598 |    0.90 |    4.99 |   296.70 |      2.35 |       48.65 |     54 |
    | **NEGany~terribly_impressive**  |   196 |       178,051 |    0.86 |    5.97 | 1,087.64 |      9.50 |      186.50 |    218 |
    | **NEGany~terribly_sure**        |    69 |       262,825 |    0.86 |    5.08 |   386.31 |      3.31 |       65.69 |     76 |
    | **NEGany~terribly_different**   |   366 |       825,838 |    0.85 |    6.33 | 2,022.47 |     17.82 |      348.18 |    409 |
    | **NEGmir~terribly_surprising**  |    67 |         2,662 |    0.83 |    4.07 |   236.35 |     11.48 |       55.52 |     67 |
    | **NEGmir~terribly_original**    |    45 |         1,555 |    0.83 |    3.40 |   158.74 |      7.71 |       37.29 |     45 |
    | **NEGmir~terribly_unusual**     |    24 |         2,302 |    0.83 |    2.23 |    84.66 |      4.11 |       19.89 |     24 |
    | **NEGmir~terribly_special**     |    24 |        15,541 |    0.83 |    2.23 |    84.66 |      4.11 |       19.89 |     24 |
    | **NEGmir~terribly_popular**     |    19 |         5,668 |    0.83 |    1.75 |    67.02 |      3.26 |       15.74 |     19 |
    | **NEGmir~terribly_clear**       |    15 |         6,722 |    0.83 |    1.20 |    52.91 |      2.57 |       12.43 |     15 |
    | **NEGmir~terribly_remarkable**  |    14 |         3,238 |    0.83 |    1.03 |    49.38 |      2.40 |       11.60 |     14 |
    | **NEGmir~terribly_new**         |    69 |        12,836 |    0.80 |    3.66 |   225.93 |     12.17 |       56.83 |     71 |
    | **NEGmir~terribly_interested**  |    39 |         8,255 |    0.74 |    2.36 |   112.46 |      7.37 |       31.63 |     43 |
    | **NEGmir~terribly_interesting** |    56 |        12,447 |    0.68 |    2.44 |   145.16 |     11.31 |       44.69 |     66 |
    
    
    1. _terribly surprising_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                 |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_100.2032_x1602721_48:4-5-6`**     | While this is n't __`terribly surprising`__ ( IT professionals have plenty of horror stories about how they did what users wanted , and it was a mess ) , it can be very frustrating to work with Google or to hope for a particular feature or change to be made .                                                                         |
    | **`pcc_eng_00_033.8422_x0530741_09:3-5-6`**     | This ca n't be __`terribly surprising`__ .                                                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_02_015.9792_x0242595_050:14-15-16`** | Nike has long been the king of athletic retail , so this is n't __`terribly surprising`__ .                                                                                                                                                                                                                                                 |
    | **`pcc_eng_12_039.2657_x0618895_23:3-4-5`**     | This is n't __`terribly surprising`__ , given how few features have popped up on the " Rockford " sets , but given that Universal has several cool " Files " - related things sitting in their vaults , like episodes of " Richie Brockelman , Private Eye , " you 'd think they could 've managed to throw some of those items onto here . |
    | **`pcc_eng_16_087.4091_x1398683_164:1-6-7`**    | None of this should be __`terribly surprising`__ , since it is increasingly clear that Donald Trump , whose actual net worth is unclear , was completely comfortable making money from blatant fraud .                                                                                                                                      |
    
    
    2. _terribly uncommon_
    
    |                                                | `token_str`                                                                                                                                                                                                     |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_082.8058_x1322266_07:14-15-16`** | While Christians marrying Jews , Jews marrying Hindus and Hindus marrying Buddhists is not __`terribly uncommon`__ in the US and other first world nations , it has not always been this way .                  |
    | **`pcc_eng_22_089.4691_x1429976_26:26-27-28`** | The second surprise that fell through was that Bill had set up a police escort from the ceremony to the reception - something that is n't __`terribly uncommon`__ for a high ranking official in a small town . |
    | **`pcc_eng_29_039.7301_x0625323_3:09-10-11`**  | Two - headedness , or bicephaly , is not __`terribly uncommon`__ among turtles and snakes , and the twins are reportedly in good health . ( 0:34 )                                                              |
    | **`pcc_eng_11_017.2605_x0263128_03:7-8-9`**    | American Robins with abnormal plumage are not __`terribly uncommon`__ , and a number of them are shown on our introductory page on odd plumages .                                                               |
    | **`pcc_eng_04_085.5134_x1365481_36:1-7-8`**    | Not that such a sight is __`terribly uncommon`__ in Copenhagen , known as the world 's cycling capital .                                                                                                        |
    
    
    3. _terribly likely_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                       |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_007.8954_x0111744_06:3-4-5`**    | It 's not __`terribly likely`__ that he 's going to be a successful NHL player .                                                                                                                                                                                  |
    | **`pcc_eng_10_084.4886_x1349366_07:2-3-4`**    | " Not __`terribly likely`__ , " I replied .                                                                                                                                                                                                                       |
    | **`pcc_eng_23_008.4563_x0120374_10:31-32-33`** | Malloy said he believes Notre Dame -- a traditional independent football power with a national following and its own TV deal with NBC that runs through 2015 -- is " not __`terribly likely`__ " to join the ACC .                                                |
    | **`pcc_eng_19_075.4013_x1202029_79:34-35-36`** | Besides , I 've noticed that when I see an announcement of a new project , if it 's provided as a fait accompli with lots of code and documentation , I 'm not __`terribly likely`__ to invest the time to delve through all that to learn what it 's all about . |
    | **`pcc_eng_10_057.0585_x0906495_015:3-4-5`**   | This is not __`terribly likely`__ .                                                                                                                                                                                                                               |
    
    
    4. _terribly productive_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                            |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19960608_0035_14:09-11-12`**         | lately , of course , the Dodgers have n't been __`terribly productive`__ no matter who 's standing out on the mound opposite them .                                                                                                                                                                                                    |
    | **`pcc_eng_27_021.8378_x0336982_04:3-5-6`**     | Garcia has n't been __`terribly productive`__ with the bat as he notched his first multi-hit game since April 2 .                                                                                                                                                                                                                      |
    | **`pcc_eng_19_079.8810_x1274310_023:10-11-12`** | So I 'm not doing much or at least nothing __`terribly productive`__ : trying to solve a lot of computer problems , dealing with a lot of broken appliances and thus shopping for replacements ( ick ) , a lot of having to deal with ornery contractors , a couple of doctor appointments , air bag replacements , things like that . |
    | **`pcc_eng_08_070.8614_x1131127_15:08-09-10`**  | Even with the home runs he 's not __`terribly productive`__ , some team will find a place for him given his versatility and defense but they should n't expect much offensively .                                                                                                                                                      |
    | **`pcc_eng_06_026.8551_x0418312_41:20-22-23`**  | Purdue was far more desperate in the secondary a year ago , and Williams had gone his whole career without being __`terribly productive`__ at his position of choice .                                                                                                                                                                 |
    
    
    5. _terribly reliable_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                     |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_003.4429_x0039530_048:35-36-37`** | It 's too early to panic about next year 's water situation , given that early spring is when we typically get most of our water , and large-scale , long- range projections are n't __`terribly reliable`__ for forecasting local conditions . |
    | **`pcc_eng_09_003.8695_x0046653_22:11-12-13`**  | That was because most carburetors and vacuum control systems were not __`terribly reliable`__ : as a result , fuel economy and survivability suffered .                                                                                         |
    | **`pcc_eng_21_093.6106_x1496377_03:6-7-8`**     | But the six-legged soldiers were n't terribly reliable                                                                                                                                                                                          |
    | **`pcc_eng_21_093.6106_x1496377_02:6-7-8`**     | But the six-legged soldiers were n't __`terribly reliable`__ by JOSEPH TREVITHICK Mao Tse -Tung famously wrote in On Guerrilla Warfare that guerrillas are proverbial fish who have ...                                                         |
    | **`pcc_eng_03_032.4087_x0508784_23:16-17-18`**  | As it turns out , with the right CAPTCHA - cracking algorithm , it 's not __`terribly reliable`__ .                                                                                                                                             |
    
    
    6. _terribly unusual_
    
    |                                              | `token_str`                                                                                                                                                                                                            |
    |:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_033.3313_x0522980_062:6-7-8`** | At that time it was n't __`terribly unusual`__ for young people to get married that young .                                                                                                                            |
    | **`pcc_eng_27_007.1798_x0099343_07:3-5-6`**  | It would not be __`terribly unusual`__ to see a 70 year old woman sans brassiere strut by in the latest fashions , sporting an air that says she owns the sidewalk and possibly much of this part of town .            |
    | **`pcc_eng_06_020.0387_x0307974_64:6-7-8`**  | Joining the Communist party was not __`terribly unusual`__ , keeping in mind that this was the height of the Depression , and in states like Oklahoma , the American Communist Party began to bend a sympathetic ear . |
    | **`nyt_eng_19990217_0526_21:5-6-7`**         | storms like this are not __`terribly unusual`__ where they are .                                                                                                                                                       |
    | **`pcc_eng_01_044.4064_x0701249_14:3-4-5`**  | This is n't __`terribly unusual`__ in itself ; since 1952 , Congress has established a " national day of prayer " and most other states do the same thing .                                                            |
    
    
    7. _terribly original_
    
    |                                                  | `token_str`                                                                                                                                                                                     |
    |:-------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_004.8873_x0063403_23:3-4-5`**      | There 's nothing __`terribly original`__ in the above outline , and there 's even less originality in the actual novel .                                                                        |
    | **`pcc_eng_12_084.7327_x1352912_2:25-27-28`**    | It was about time I posted something , I have been very lazy of late , and dare I say it - I have not been __`terribly original`__ with this outfit but , when I saw the jacket , I wanted it . |
    | **`pcc_eng_20_032.0747_x0502440_48:3-4-5`**      | It 's not __`terribly original`__ .                                                                                                                                                             |
    | **`pcc_eng_08_083.1694_x1330390_16:4-5-6`**      | There 's really nothing __`terribly original`__ about HNIC 's plot , which is by no means a bad thing .                                                                                         |
    | **`pcc_eng_24_108.09517_x1747258_143:08-09-10`** | Naschy 's penning of the screenplay was not __`terribly original`__ .                                                                                                                           |
    
    
    8. _terribly sure_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                           |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_049.4976_x0784738_6:3-4-5`**      | I 'm not __`terribly sure`__ why .                                                                                                                                                                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_08_076.4464_x1221466_122:79-80-81`** | Maybe it was because my Dad was reluctant to bring both of the kids over to the house of somebody he was n't really that friendly with ; maybe the friend might have been persona non grata in the house ( it might seem ridiculous that a ten-year - old would be treated this way , but the kid 's father had plenty of enemies ) ; or maybe I myself felt awkward about gate- crashing and was n't __`terribly sure`__ if we could both go along . |
    | **`pcc_eng_28_078.4801_x1253326_083:21-22-23`** | Yes the diuretics , I think the Ace inhibitor does that as well does n't it , but I 'm not __`terribly sure`__ , but I think it does make it dehydrate , so you have to have enough fluid , but I have diuretics and to get rid of excess fluid , so you have to take in fluid as well ( laugh ) .                                                                                                                                                    |
    | **`pcc_eng_18_084.4187_x1350903_30:3-4-5`**     | I 'm not __`terribly sure`__ if Damian Marley is singing in English in this song - pretty sure he gives a shout out to Chuck Norris though .                                                                                                                                                                                                                                                                                                          |
    | **`pcc_eng_12_086.3176_x1378617_35:3-4-5`**     | I 'm not __`terribly sure`__ I engage in this examination .                                                                                                                                                                                                                                                                                                                                                                                           |
    
    
    9. _terribly impressive_
    
    |                                                | `token_str`                                                                                                                                                                                            |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_042.2246_x0667173_645:5-6-7`**   | His passing numbers were n't __`terribly impressive`__ ( 18 - for - 30 , 189 yards , one touchdown ) and he struggled early on .                                                                       |
    | **`pcc_eng_20_085.1111_x1358994_047:3-4-5`**   | That was n't __`terribly impressive`__ after a week 's work .                                                                                                                                          |
    | **`pcc_eng_07_054.3705_x0862668_09:20-21-22`** | I 'm not very fond of the new Tiida / Versa 's styling , and 24 city MPG is n't __`terribly impressive`__ .                                                                                            |
    | **`pcc_eng_01_099.1827_x1587312_54:18-19-20`** | Yet even here Kramer is forced to admit in terms of tangible results that his record was not __`terribly impressive`__ .                                                                               |
    | **`pcc_eng_07_021.1702_x0326161_51:19-20-21`** | Like I mentioned above ... the claiming their design is an aesthetic improvement over the past really is n't __`terribly impressive`__ , it would be hard to argue that the original was even trying . |
    
    
    10. _terribly different_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                  |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_019.5930_x0300408_35:6-7-8`**     | The story in itself is not __`terribly different`__ from any other Christian romance novel .                                                                                                                                                                 |
    | **`pcc_eng_21_096.3479_x1540514_28:21-23-24`**  | Home prices in the 1920s were rising rapidly , leading many people to talk about a housing crisis in terms not so __`terribly different`__ from today 's .                                                                                                   |
    | **`pcc_eng_22_001.5616_x0009179_34:38-40-41`**  | The US claims the strike destroyed 20 % of Syria 's operational air force , although Syria and Russia say that most of the missiles missed and that only 6 Mi G - 23s ( which may not be __`terribly different`__ from 20 % at this point ) were destroyed . |
    | **`pcc_eng_07_029.8538_x0466615_13:08-09-10`**  | But personally , this lockdown lifestyle is not __`terribly different`__ from my normal routine , as I 'm quite hermetic and private .                                                                                                                       |
    | **`pcc_eng_24_108.01603_x1734448_21:23-25-26`** | The Green Hornet 's topcoat , gloves , hat , and domino mask might be an emerald green , but they were n't too __`terribly different`__ from what the average man on the street would wear on his way to the office .                                        |
    
    
    11. _terribly special_
    
    |                                                | `token_str`                                                                                                                           |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_064.8935_x1034009_12:15-16-17`** | " It 's a full moon and it 's real , but there 's nothing __`terribly special`__ or spectacular about it , " he said .                |
    | **`apw_eng_20081121_0065_2:12-13-14`**         | it 's sweet and eager to please but , sadly , nothing __`terribly special`__ : Girl finds dog , girl loses dog , girl gets dog back . |
    | **`pcc_eng_20_002.3380_x0021445_17:1-2-3`**    | Nothing __`terribly special`__ about this , but it 's good to know attachments are an option .                                        |
    | **`pcc_eng_25_083.0387_x1327858_16:14-15-16`** | Though they act as a high- profile example , the Bush boys are n't __`terribly special`__ in their mixture of sects of Christianity . |
    | **`pcc_eng_22_004.2037_x0051958_047:7-8-9`**   | The chunky sauce was good but not __`terribly special`__ .                                                                            |
    
    
    12. _terribly popular_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_027.3064_x0425122_034:11-12-13`** | " It is especially the case when the president is n't __`terribly popular`__ , when people still have economic anxieties and when they believe the country is moving in the wrong direction , " Mann noted .                                                                                                                                                                                                                                                                                                            |
    | **`pcc_eng_22_071.9946_x1147466_13:3-5-6`**     | Homework has never been __`terribly popular`__ with students and even many parents , but in recent years it has been particularly scorned because of the kinds of problems illustrated above : too heavy a load , work that 's inappropriate for the student 's age or for the subject matter being taught , busywork that does n't contribute to learning , assignments that ca n't be completed without major parental intervention or expensive equipment , and work that teachers do n't take the time to correct . |
    | **`pcc_eng_01_098.3687_x1574198_004:15-16-17`** | I remember that the stories came to me hard and fast and I was not __`terribly popular`__ amongst my friends when I admitted I was finished with the I.S. long before it was due ( my college required this of everyone ) .                                                                                                                                                                                                                                                                                             |
    | **`pcc_eng_09_085.3348_x1364447_040:27-28-29`** | So " Seeking a Friend for the End of the World , " which presents a sort of gallows situation for the entire planet , was n't __`terribly popular`__ in theaters this summer , which is just as well , as I did n't find the film was particularly skilled with balancing the mordant nature of its setting with the treacly and pretty standard romantic comedy plot .                                                                                                                                                 |
    | **`pcc_eng_09_003.8243_x0045928_15:7-8-9`**     | He is also rumored to be not __`terribly popular`__ amongst younger executives at Deutsche Bank .                                                                                                                                                                                                                                                                                                                                                                                                                       |
    
    
    13. _terribly clear_
    
    |                                                 | `token_str`                                                                                                                                                                                                                        |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_038.7487_x0610081_142:34-35-36`** | I 've read the entire three hundred issue run of Hellblazer in trade editions save some in the middle of the run that Vertigo , a unit of DC Comics , from reasons not __`terribly clear`__ to anyone was not released in that ... |
    | **`pcc_eng_13_039.2148_x0617885_09:3-4-5`**     | Microsoft was n't __`terribly clear`__ on certain aspects of the Xbox                                                                                                                                                              |
    | **`pcc_eng_25_036.3434_x0572127_147:18-19-20`** | With the added footage , Dyer gives the medal back to Chris , for reasons that are not __`terribly clear`__ .                                                                                                                      |
    | **`pcc_eng_17_072.4313_x1154287_17:3-4-5`**     | It 's not __`terribly clear`__ how much of a boost most of the ensemble cast of " The Avengers " got from the film 's giant success .                                                                                              |
    | **`pcc_eng_25_033.8073_x0531105_110:14-16-17`** | The information we do get from IDOC comes from emailed statements that are n't always __`terribly clear`__ or helpful .                                                                                                            |
    
    
    14. _terribly remarkable_
    
    |                                                | `token_str`                                                                                                                                                                           |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_058.8454_x0934957_27:29-30-31`** | Something about being able to watch a " breaking " news story live was addictive for modern news audiences , even if the thing they were watching was n't __`terribly remarkable`__ . |
    | **`pcc_eng_28_060.5024_x0962620_41:30-31-32`** | Review : I 'll be the first to admit the story revolving around a tiny pill capsule that can kill an entire city upon going ' pop ' is n't __`terribly remarkable`__ .                |
    | **`pcc_eng_27_068.9149_x1098061_42:1-5-6`**    | None of this is __`terribly remarkable`__ in the world of the book .                                                                                                                  |
    | **`pcc_eng_29_036.6025_x0574483_33:19-20-21`** | What Price did manage to do was shake off 60 minutes where he was thoroughly outplayed by a not __`terribly remarkable`__ goalie .                                                    |
    | **`pcc_eng_28_030.4840_x0476488_11:25-26-27`** | The history teacher in me must note that our nation 's first transfer of power , from George Washington to John Adams , was n't __`terribly remarkable`__ .                           |
    
    
    15. _terribly new_
    
    |                                             | `token_str`                                                                                                                                                                                                                       |
    |:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19961014_0568_7:1-2-3`**         | nothing __`terribly new`__ there .                                                                                                                                                                                                |
    | **`apw_eng_20090506_0541_38:4-5-6`**        | but it 's not __`terribly new`__ , just getting the word out and labeling it . ''                                                                                                                                                 |
    | **`pcc_eng_24_101.3853_x1624117_02:4-5-6`** | Your mission is n't __`terribly new`__ ( infiltrate a terrorist base and blow everything up ) , but the gameplay is : your numerous enemies are watching for you , and you are encouraged to sneak rather than simply charge in . |
    | **`nyt_eng_20050125_0046_4:08-09-10`**      | the idea of playing alongside men is n't __`terribly new`__ to a girl who pretended to be a boy in order to play pick-up matches on the street .                                                                                  |
    | **`pcc_eng_23_039.0742_x0615113_10:7-8-9`** | This aspect of the study is not __`terribly new`__ , though discovering which parts of the brain see increase function has confirmed other research concerning alcoholism as a memory disorder .                                  |
    
    
    16. _terribly interested_
    
    |                                                 | `token_str`                                                                                                                                                                                                             |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_009.0421_x0130317_09:6-7-8`**     | But Aly & AJ are n't __`terribly interested`__ in upholding expectations :                                                                                                                                              |
    | **`pcc_eng_24_032.6772_x0512437_238:3-5-6`**    | She 'd never been __`terribly interested`__ in it aside from making a Backstreet Boys - themed e-mail account once .                                                                                                    |
    | **`nyt_eng_19970127_0247_29:6-7-8`**            | although the Air Force is n't __`terribly interested`__ in a mysterious metal sphere that may have fallen from the sky in a field near Seguin , local UFO researcher Walter Andrus Jr. thinks it 's out of this world . |
    | **`pcc_eng_04_054.7082_x0867487_034:20-21-22`** | He dramatically sneezes his way off the screen and returns to his perch , so I guess he was n't __`terribly interested`__ in the tissue , after all .                                                                   |
    | **`pcc_eng_28_074.1027_x1182313_095:15-16-17`** | I think part of the problem is that right now the Trump administration is not __`terribly interested`__ in human rights around the world .                                                                              |
    
    
    17. _terribly interesting_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                          |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_045.5150_x0718587_027:12-13-14`** | I tend to get impatient with such comparisons because they 're not __`terribly interesting`__ to me .                                                                                                                                                                                                                                                                                |
    | **`apw_eng_20091106_0099_12:6-7-8`**            | the fictional plot line is n't __`terribly interesting`__ , though it 's nicely ornamented by little farces lifted from the book -- a guy convinced that the Loch Ness monster is the ghost of a dinosaur , another who advises that Angela Lansbury somehow knows the whereabouts of Manuel Noriega -LRB- it was Kristy McNichol in the book , but same chuckle nonetheless -RRB- . |
    | **`pcc_eng_06_020.8990_x0321963_05:39-40-41`**  | But too often , the popular online articles that lure us in with headlines promising interesting facts contain only facts that are kind of interesting or interesting things that are not really facts or factual things that are n't __`terribly interesting`__ or things we already knew but did n't know we knew because they were presented to us as things we did n't know .    |
    | **`pcc_eng_05_083.6032_x1336890_060:34-35-36`** | Hader 's Aaron is a perfectly nice , likable guy ( his scene playing one - on- one basketball with Le Bron James is a stone- cold classic ) , but he 's not __`terribly interesting`__ , generous to a fault , and definitely not the kind of guy that Amy would be drawn to .                                                                                                       |
    | **`pcc_eng_24_027.2347_x0424190_11:15-16-17`**  | Every app is going to have a bug or two , and there 's nothing __`terribly interesting`__ about those , but the ads WERE tricky .                                                                                                                                                                                                                                                    |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/...
    
    Samples saved as...
    1. `neg_bigram_examples/terribly/terribly_surprising_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_uncommon_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_likely_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_productive_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_reliable_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_unusual_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_original_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_sure_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_impressive_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_different_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_special_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_popular_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_clear_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_remarkable_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_new_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_interested_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_interesting_99ex.csv`


# 10 Most Negative Bigrams for each of the 8 Most Negative Adverbs


## 1. *necessarily*

|                         |        `N` |      `f1` |   `adv_total` |
|:------------------------|-----------:|----------:|--------------:|
| **NEGATED_necessarily** | 72,839,589 | 3,173,660 |        48,947 |
| **NEGMIR_necessarily**  |  1,701,929 |   291,732 |         1,107 |


|                                       |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:--------------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGany~necessarily_useful**         |   104 |       227,709 |    0.96 |    6.75 |   651.75 |      4.53 |       99.47 |    104 |
| **NEGany~necessarily_fun**            |    96 |       190,026 |    0.96 |    6.62 |   601.61 |      4.18 |       91.82 |     96 |
| **NEGany~necessarily_essential**      |    93 |        69,845 |    0.96 |    6.57 |   582.81 |      4.05 |       88.95 |     93 |
| **NEGany~necessarily_reliable**       |    81 |        90,598 |    0.96 |    6.35 |   507.61 |      3.53 |       77.47 |     81 |
| **NEGany~necessarily_proud**          |    71 |       207,536 |    0.96 |    6.14 |   444.94 |      3.09 |       67.91 |     71 |
| **NEGany~necessarily_indicative**     | 1,389 |         8,148 |    0.95 |    9.43 | 8,577.54 |     61.00 |    1,328.00 |  1,400 |
| **NEGany~necessarily_easy**           |   909 |       579,827 |    0.95 |    9.01 | 5,605.64 |     39.95 |      869.05 |    917 |
| **NEGany~necessarily_representative** |   487 |        18,355 |    0.95 |    8.34 | 2,996.58 |     21.44 |      465.56 |    492 |
| **NEGany~necessarily_surprising**     |   340 |        70,540 |    0.95 |    8.33 | 2,117.16 |     14.86 |      325.14 |    341 |
| **NEGany~necessarily_new**            |   482 |       253,862 |    0.94 |    7.94 | 2,923.82 |     21.44 |      460.56 |    492 |
| **NEGmir~necessarily_right**          |    23 |         5,576 |    0.83 |    2.15 |    81.13 |      3.94 |       19.06 |     23 |
| **NEGmir~necessarily_illegal**        |    15 |           937 |    0.83 |    1.20 |    52.91 |      2.57 |       12.43 |     15 |
| **NEGmir~necessarily_wrong**          |   211 |        20,880 |    0.81 |    5.04 |   698.74 |     37.03 |      173.97 |    216 |
| **NEGmir~necessarily_new**            |    23 |        12,836 |    0.79 |    1.84 |    73.19 |      4.11 |       18.89 |     24 |
| **NEGmir~necessarily_bad**            |    50 |        10,261 |    0.77 |    2.95 |   154.45 |      9.08 |       40.92 |     53 |
| **NEGmir~necessarily_true**           |    53 |         6,191 |    0.73 |    2.69 |   150.42 |     10.11 |       42.89 |     59 |
| **NEGmir~necessarily_better**         |    27 |        14,013 |    0.70 |    1.63 |    72.90 |      5.31 |       21.69 |     31 |


1. _necessarily useful_

|                                                | `token_str`                                                                                                                                                                                                                                                                     |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_024.1662_x0374968_60:11-12-13`** | The talent and skill required to win an election is not __`necessarily useful`__ for the actual practice of good governing .                                                                                                                                                    |
| **`pcc_eng_16_040.9012_x0645895_24:32-33-34`** | I find that is more wise to spend your store reward money on something * useful * rather than just rolling your reward money into products that are FREE , but not __`necessarily useful`__ to your family !                                                                    |
| **`pcc_eng_04_054.7457_x0868076_11:4-5-6`**    | So it is n't __`necessarily useful`__ for monitoring disease activity .                                                                                                                                                                                                         |
| **`pcc_eng_02_003.9319_x0047305_11:36-37-38`** | He speaks to Mariko Kosaka , a Developer Advocate on the Google Developers Relations Team , about the art she creates with code and how developers can embrace the notion of making something that is n't __`necessarily useful`__ but still has value .                        |
| **`pcc_eng_11_086.0944_x1377399_23:2-3-4`**    | Though not __`necessarily useful`__ in day to day treatment of the common condition , the ingestion of burdock may help to control predicted spikes in blood pressure following meals which can be useful in persons who struggle with unhealthy fluctuations around mealtime . |


2. _necessarily fun_

|                                                 | `token_str`                                                                                                                                                           |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_007.6486_x0107392_049:12-13-14`** | " When you are a 19 - year-old , it 's not __`necessarily fun`__ to be pounding kale smoothies and not going out to Chipotle with your te ......                      |
| **`pcc_eng_07_012.4303_x0185352_05:23-24-25`**  | Snapchat 's new photo filter that allows users to change into a man or woman with the tap of a finger is n't __`necessarily fun`__ and games for transgender people . |
| **`pcc_eng_22_058.2949_x0926215_216:18-19-20`** | " We were aspiring to achieve a level that was maybe beyond us , and that 's not __`necessarily fun`__ , " he says .                                                  |
| **`pcc_eng_19_043.2627_x0682345_13:15-16-17`**  | It 's a great concept leads to some interesting situations , though it 's not __`necessarily fun`__ .                                                                 |
| **`pcc_eng_12_063.5070_x1010663_50:6-7-8`**     | Writing a better story was n't __`necessarily fun`__ , conflict resolution took much longer because there was actually conflict to resolve .                          |


3. _necessarily essential_

|                                                  | `token_str`                                                                                                                                                                                                                                                                                                             |
|:-------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_087.2409_x1396021_45:14-15-16`**   | Can it possibly be that the values we have established in America are not __`necessarily essential`__ to the well - being of the human race , or do we sometimes have a definite edge over the Germans ?                                                                                                                |
| **`pcc_eng_27_066.6822_x1061853_28:3-4-5`**      | Speed is n't __`necessarily essential`__ , though .                                                                                                                                                                                                                                                                     |
| **`apw_eng_20090115_1256_106:12-13-14`**         | for this job , intelligence experience is certainly helpful but is n't __`necessarily essential`__ .                                                                                                                                                                                                                    |
| **`pcc_eng_20_080.4367_x1283424_0334:35-36-37`** | 00:12:51,170 PROFESSOR : That is true , but although in English in 286 00:12:51,170 --> 00:12:56,110 particular the phonetic meaning , the way how a certain 287 00:12:56,110 --> 00:13:00,397 word is pronounced is n't __`necessarily essential`__ for 288 00:13:00,397 --> 00:13:01,540 solving a crossword puzzle . |
| **`pcc_eng_07_028.1119_x0438479_17:08-09-10`**   | Of course , understanding the science is n't __`necessarily essential`__ to the key sci-fi and techno-thriller readers .                                                                                                                                                                                                |


4. _necessarily reliable_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_061.1479_x0972872_28:29-30-31`**  | While they do find an acceleration in MFP outside the IT sector during the late 1990s , the extent of this increase depends upon price indexes that are not __`necessarily reliable`__ right now .                                                                                                                        |
| **`pcc_eng_12_066.3925_x1056872_207:21-22-23`** | We need to get vaccinations , amass enormous quantities of prescription and over- the- counter drugs ( Vietnam 's are not __`necessarily reliable`__ or accessible ) , prepare Olivia for a big trip , find her old crib and baby stuff , and on and on .                                                                 |
| **`pcc_eng_19_045.6425_x0720669_30:21-22-23`**  | If you are reliant on the Middle East , or Iran or Russia to get your gas -- that 's not __`necessarily reliable`__ .                                                                                                                                                                                                     |
| **`pcc_eng_10_011.5500_x0170445_12:18-19-20`**  | While previous studies have identified a difference in mercury levels between tuna species , those studies were n't __`necessarily reliable`__ because they did n't have a fool - proof way of determining which tuna came from which species , said study researcher Joanna Burger , a professor at Rutgers University . |
| **`pcc_eng_17_079.9551_x1276018_02:37-38-39`**  | ( Reuters Health ) - Nearly 88 percent of online reviews of U.S. plastic surgeons who provide breast augmentation were found to be positive in a recent study , but that snapshot of customer satisfaction is not __`necessarily reliable`__ , researchers say .                                                          |


5. _necessarily proud_

|                                               | `token_str`                                                                                                                                                     |
|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20070520_0021_49:4-5-6`**          | `` I 'm not __`necessarily proud`__ of being German , but I am proud of being from Cologne .                                                                    |
| **`pcc_eng_01_095.6067_x1529843_5:24-25-26`** | I got a young man named George W. Bush in the National Guard when I was Lt. Gov. of Texas and I 'm not __`necessarily proud`__ of that .                        |
| **`pcc_eng_17_070.2041_x1118143_08:3-4-5`**   | I 'm not __`necessarily proud`__ of it , but there you go .                                                                                                     |
| **`pcc_eng_02_001.9430_x0015306_52:6-7-8`**   | Even about things I 'm not __`necessarily proud`__ of .                                                                                                         |
| **`pcc_eng_26_092.9107_x1486511_065:5-6-7`**  | Afterward , he was n't __`necessarily proud`__ of the achievement , insisting what comes next in a series is always more important than what 's just happened . |


6. _necessarily surprising_

|                                                | `token_str`                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_038.8901_x0613229_64:7-8-9`**    | Of course , these results are n't __`necessarily surprising`__ .                                                                                                                                                                                                                          |
| **`pcc_eng_06_093.9383_x1503133_33:3-4-5`**    | It 's not __`necessarily surprising`__ that the article puts the responsibility on what moms " see , " indicating that this is all about individual responsibility .                                                                                                                      |
| **`pcc_eng_29_083.4727_x1332100_06:18-19-20`** | So , while the record number of home sales through the first five months of 2016 is not __`necessarily surprising`__ , it does sometimes mask the larger story in the GTA : the shortage of listings , which has resulted in strong upward pressure on home prices , " said Mr. Mc Lean . |
| **`pcc_eng_16_080.2583_x1282733_45:20-21-22`** | Kahrl 's piece is a far better analysis of what went wrong than Simmons ' , though that is n't __`necessarily surprising`__ .                                                                                                                                                             |
| **`pcc_eng_02_080.6539_x1287909_02:08-09-10`** | The Desktop ( RKG ) This is not __`necessarily surprising`__ , since the screen real estate of a tablet approximates the desktop's .                                                                                                                                                      |


7. _necessarily indicative_

|                                                 | `token_str`                                                                                                                                                                           |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_034.8920_x0547952_033:14-15-16`** | Remember , all of these numbers are subject to small sample size and not __`necessarily indicative`__ of players ' true talents .                                                     |
| **`pcc_eng_16_081.5307_x1303380_16:10-11-12`**  | The titles available in the Shinra Technologies beta are not __`necessarily indicative`__ of the company 's service lineup , said Kristin De Rosa , director of marketing at Shinra . |
| **`pcc_eng_23_019.0750_x0291648_16:11-13-14`**  | The past performance of any trading method or methodology will not be __`necessarily indicative`__ of future outcomes .                                                               |
| **`pcc_eng_19_016.7237_x0253666_15:4-5-6`**     | But this was not __`necessarily indicative`__ of Washington 's broader geographical use of ' joystick bombers ' in the previous year .                                                |
| **`pcc_eng_28_077.4646_x1236830_36:5-6-7`**     | Remember that price is not __`necessarily indicative`__ of quality and not all the best companies are the most expensive .                                                            |


8. _necessarily easy_

|                                                 | `token_str`                                                                                                                                                                           |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_057.5629_x0914301_22:28-29-30`**  | And getting folks in their seats for a battle royale over the question of whether Locke or Plutarch 's more correct about the nature of law is n't __`necessarily easy`__ .           |
| **`pcc_eng_19_010.0168_x0145829_05:24-25-26`**  | According to Kathleen O'Reilly , the museum 's vice president , " The site is a top destination for Houston visitors , but not __`necessarily easy`__ to navigate for pedestrians . " |
| **`pcc_eng_15_096.9216_x1550382_29:6-7-8`**     | But making the shift is n't __`necessarily easy`__ or simple .                                                                                                                        |
| **`pcc_eng_07_024.8096_x0385118_24:09-10-11`**  | In fact , many of mindfulness practices were n't __`necessarily easy`__ even if they were simple to do .                                                                              |
| **`pcc_eng_20_008.7627_x0125310_094:27-28-29`** | The one on the Audi , VW 's luxury division , looks all right , and is somewhat simpler to handle than i Drive , but not __`necessarily easy`__ .                                     |


9. _necessarily representative_

|                                                 | `token_str`                                                                                                                                                                                                                                                        |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_037.5350_x0589619_208:15-17-18`** | He recommends using only rents , even if few rents are available and may not be __`necessarily representative`__ of the housing stock and market .                                                                                                                 |
| **`pcc_eng_22_086.2539_x1378067_29:6-7-8`**     | Because A ) pictures are n't __`necessarily representative`__ of how a girl looks in person and B ) there 's a chemistry element that you ca n't quantify beforehand .                                                                                             |
| **`pcc_eng_21_076.0376_x1212613_8:14-15-16`**   | The opinions expressed on this blog are those of the individual authors and not __`necessarily representative`__ of the GMCTE , CGSR , or the University of Saskatchewan .                                                                                         |
| **`pcc_eng_11_098.5959_x1579848_18:11-12-13`**  | Top dating sites for lesbians Mingle dating site Experiences are not __`necessarily representative`__ of , credits for an hour is all that online dating really something works both you , but he has no say in how .                                              |
| **`pcc_eng_05_083.7342_x1338981_30:27-28-29`**  | The views and opinions expressed by the SOI Industry Consortium through officers in the SOI Industry Consortium or in this presentation or other communication vehicles are not __`necessarily representative`__ of the views and opinions of individual members . |


10. _necessarily new_

|                                                | `token_str`                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_042.8037_x0675485_20:36-37-38`** | That HTC has chosen to not put Android front and center , instead marketing its own innovations , may be worrisome to Android purists and certainly to Google 's marketing department , but it 's not __`necessarily new`__ . |
| **`pcc_eng_07_059.2916_x0942174_18:08-09-10`** | For technology observers , patent battles are not __`necessarily new`__ .                                                                                                                                                     |
| **`pcc_eng_11_098.0215_x1570595_10:08-09-10`** | Liptak notes that this particular protocol is n't __`necessarily new`__ or malicious .                                                                                                                                        |
| **`pcc_eng_16_021.8265_x0337269_23:08-09-10`** | There is another option and it 's not __`necessarily new`__ .                                                                                                                                                                 |
| **`pcc_eng_14_085.3775_x1363859_12:22-23-24`** | Women 's nomenclature has been a point of contention for centuries -- and the practice of keeping one 's own is n't __`necessarily new`__ .                                                                                   |


11. _necessarily right_

|                                                 | `token_str`                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_019.6821_x0302170_38:09-10-11`**  | What 's right for a college paper is not __`necessarily right`__ for a big city daily .                      |
| **`pcc_eng_00_067.0580_x1067739_14:14-15-16`**  | Schwartz said the parting was amicable , but the shakeup ' ' was n't __`necessarily right`__ for me . ''     |
| **`pcc_eng_18_043.6320_x0689874_11:14-15-16`**  | As in much of life , what is right for one person is not __`necessarily right`__ for another .               |
| **`pcc_eng_15_096.7466_x1547526_036:12-13-14`** | The plan that made sense for you a year ago is n't __`necessarily right`__ for you now .                     |
| **`pcc_eng_22_003.2273_x0036168_18:6-7-8`**     | But I realized it was n't __`necessarily right`__ for me - there was just something missing about design . " |


12. _necessarily illegal_

|                                                | `token_str`                                                                                                                                                                 |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_080.8030_x1289779_03:25-26-27`** | We 're not clear if he sold them or not - we 'd hope he could give them away certainly - but it 's not __`necessarily illegal`__ as the Greensboro News & Record suggests . |
| **`nyt_eng_20000608_0216_35:24-25-26`**        | handing out gifts of food , T-shirts , building supplies and even medicines is standard fare during political campaigns in Mexico and is not __`necessarily illegal`__ .    |
| **`nyt_eng_19961022_0361_4:22-23-24`**         | he noted , however , that a solicitation differed under law from an actual physical transmission of child pornography and was not __`necessarily illegal`__ .               |
| **`pcc_eng_09_003.7452_x0044623_12:3-4-5`**    | Backdating is not __`necessarily illegal`__ , but it must be disclosed to investors and accounted for properly .                                                            |
| **`pcc_eng_03_009.4563_x0136773_27:10-11-12`** | The abuse of power means favours - which are not __`necessarily illegal`__ .                                                                                                |


13. _necessarily wrong_

|                                              | `token_str`                                                                                                                                                                                        |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_039.3422_x0619945_35:4-5-6`**  | The consensus is n't __`necessarily wrong`__ , and the dogma may contain a great deal of truth , but critical analysis can get lost along the way and important aspects can be taken for granted . |
| **`pcc_eng_00_063.4881_x1010223_30:3-4-5`**  | There 's nothing __`necessarily wrong`__ with that .                                                                                                                                               |
| **`pcc_eng_23_032.1180_x0502425_59:4-5-6`**  | Although there 's nothing __`necessarily wrong`__ with that approach , it 's not the most efficient or consistent way to produce a great image .                                                   |
| **`nyt_eng_20060816_0013_21:09-10-11`**      | although the comments irritated Woods , they were not __`necessarily wrong`__ ; Woods was not utilizing the best technology at the time .                                                          |
| **`pcc_eng_22_003.8824_x0046751_027:3-4-5`** | It 's not __`necessarily wrong`__ , but a coach trusts his own kid .                                                                                                                               |


14. _necessarily bad_

|                                                 | `token_str`                                                                                                                                                                                                                           |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_004.9912_x0064687_32:7-8-9`**     | Keep in mind that it 's not __`necessarily bad`__ to use these words here and there , but over-using them could devalue your content .                                                                                                |
| **`pcc_eng_11_052.9064_x0839737_07:38-39-40`**  | Wherever you place your priorities in terms of the actions of the executive branch , at this point in history , the nominating of Supreme Court justices has become extremely partisan , in a way that is n't __`necessarily bad`__ . |
| **`nyt_eng_20050708_0333_21:23-24-25`**         | the possibility of deviating this much from the return of the average stock , sometimes referred to as tracking error , is not __`necessarily bad`__ .                                                                                |
| **`pcc_eng_18_084.7136_x1355514_24:3-4-5`**     | This is not __`necessarily bad`__ as a few emergency plumbing contractors choose to target their expertise on a precise number to do with services and as a result do in the future with in conversation with .                       |
| **`pcc_eng_11_017.5606_x0267951_260:09-10-11`** | Just that reaction in and of itself is not __`necessarily bad`__ .                                                                                                                                                                    |


15. _necessarily true_

|                                                 | `token_str`                                                                                                                                                                                                                             |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_073.0937_x1166132_237:7-8-9`**    | I found out that this is n't __`necessarily true`__ .                                                                                                                                                                                   |
| **`pcc_eng_29_090.8341_x1450944_031:34-35-36`** | What if I told you that despite the popular belief that children are more likely to read on a device like an i Pad or a Kindle , research shows that this is n't __`necessarily true`__ .                                               |
| **`pcc_eng_04_108.09904_x1745197_08:2-3-4`**    | Although not __`necessarily true`__ , the build up to a fight helps bring in the crowd , when two men are trash talking one another , people want to see the outcome , who will get the last word per say .                             |
| **`pcc_eng_14_035.3114_x0554219_48:12-13-14`**  | Finally , I want to tell you a story that is not __`necessarily true`__ , but it 's a good story and that , after all , should be enough .                                                                                              |
| **`pcc_eng_11_008.5813_x0122676_04:21-22-23`**  | The perception that Self Managed Superannuation Funds ( SMSFs ) have too much focus on cash and terms deposit is n't __`necessarily true`__ when looking at the results of a Mercer report for the Financial Services Council ( FSC ) . |


16. _necessarily better_

|                                                 | `token_str`                                                                                                              |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_027.7515_x0432620_17:10-11-12`**  | As far as size is concerned , bigger is n't __`necessarily better`__ .                                                   |
| **`pcc_eng_24_028.2479_x0440581_056:09-10-11`** | But the officially endorsed alternatives to DARE are n't __`necessarily better`__ .                                      |
| **`pcc_eng_19_041.4701_x0653254_14:5-6-7`**     | Also , more is not __`necessarily better`__ .                                                                            |
| **`pcc_eng_23_044.7042_x0706177_33:08-09-10`**  | It strikes me as more satisfying but not __`necessarily better`__ in every way that these tracks embody their subjects . |
| **`pcc_eng_15_093.3141_x1492208_52:4-5-6`**     | The facilities are n't __`necessarily better`__ , he says .                                                              |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/...

Samples saved as...
1. `neg_bigram_examples/necessarily/necessarily_useful_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_fun_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_essential_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_reliable_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_proud_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_surprising_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_indicative_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_easy_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_representative_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_new_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_right_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_illegal_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_wrong_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_bad_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_true_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_better_99ex.csv`

## 2. *that*

|                  |        `N` |      `f1` |   `adv_total` |
|:-----------------|-----------:|----------:|--------------:|
| **NEGATED_that** | 72,839,589 | 3,173,660 |       208,262 |
| **NEGMIR_that**  |  1,701,929 |   291,732 |         5,494 |


|                             |   `f` |   `adj_total` |   `dP1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:----------------------------|------:|--------------:|--------:|--------:|----------:|----------:|------------:|-------:|
| **NEGany~that_far-fetched** |    59 |         5,185 |    0.96 |    5.83 |    369.74 |      2.57 |       56.43 |     59 |
| **NEGany~that_thrilled**    |    59 |        24,182 |    0.96 |    5.83 |    369.74 |      2.57 |       56.43 |     59 |
| **NEGany~that_uncommon**    |   802 |        11,312 |    0.95 |    9.43 |  4,998.32 |     35.03 |      766.97 |    804 |
| **NEGany~that_surprising**  | 1,133 |        70,540 |    0.95 |    9.20 |  6,986.81 |     49.80 |    1,083.20 |  1,143 |
| **NEGany~that_unusual**     |   977 |        71,234 |    0.95 |    8.92 |  6,003.05 |     43.05 |      933.95 |    988 |
| **NEGany~that_dissimilar**  |   304 |         4,605 |    0.95 |    7.86 |  1,871.65 |     13.38 |      290.62 |    307 |
| **NEGany~that_noticeable**  |   264 |        31,467 |    0.95 |    7.65 |  1,621.81 |     11.63 |      252.37 |    267 |
| **NEGany~that_complicated** | 1,207 |       159,822 |    0.94 |    8.68 |  7,337.84 |     53.59 |    1,153.41 |  1,230 |
| **NEGany~that_familiar**    | 1,126 |       156,296 |    0.93 |    8.35 |  6,781.11 |     50.37 |    1,075.63 |  1,156 |
| **NEGany~that_hard**        | 9,948 |       348,463 |    0.91 |    8.59 | 58,817.24 |    452.26 |    9,495.74 | 10,380 |
| **NEGmir~that_keen**        |    31 |         1,360 |    0.83 |    2.73 |    109.35 |      5.31 |       25.69 |     31 |
| **NEGmir~that_impressive**  |    23 |         5,007 |    0.83 |    2.15 |     81.13 |      3.94 |       19.06 |     23 |
| **NEGmir~that_fond**        |    23 |         1,115 |    0.79 |    1.84 |     73.19 |      4.11 |       18.89 |     24 |
| **NEGmir~that_comfortable** |    23 |         4,642 |    0.79 |    1.84 |     73.19 |      4.11 |       18.89 |     24 |
| **NEGmir~that_clear**       |    18 |         6,722 |    0.78 |    1.30 |     56.03 |      3.26 |       14.74 |     19 |
| **NEGmir~that_popular**     |    65 |         5,668 |    0.76 |    3.15 |    195.15 |     12.00 |       53.00 |     70 |
| **NEGmir~that_simple**      |   474 |        25,408 |    0.72 |    4.36 |  1,340.19 |     90.68 |      383.32 |    529 |
| **NEGmir~that_easy**        |   450 |        18,610 |    0.71 |    4.23 |  1,248.84 |     87.08 |      362.92 |    508 |
| **NEGmir~that_big**         |   113 |         8,177 |    0.69 |    3.17 |    300.54 |     22.46 |       90.54 |    131 |
| **NEGmir~that_great**       |   286 |         5,568 |    0.66 |    3.57 |    725.16 |     58.62 |      227.38 |    342 |


1. _that far-fetched_

|                                                 | `token_str`                                                                                                                                                                                                                             |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000405_0292_6:36-38-39`**          | promoting Piero as a kind of celebrity , albeit one whose personal life remains sketchy -LRB- apart from several sly self-portraits and a historically resonant death date : Oct. 12 , 1492 -RRB- , may not be __`that far-fetched`__ . |
| **`nyt_eng_20051115_0368_3:08-10-11`**          | but today , Shugrue 's statement is n't all __`that far-fetched`__ : Abbot Kinney has , seemingly overnight , become the darling of Los Angeles ' art and architecture set .                                                            |
| **`pcc_eng_06_104.2003_x1669450_214:12-13-14`** | Of course , writing off a comeback from Edmure Tully is n't __`that far-fetched`__ , especially since we 've all probably been guilty of doing that several times already .                                                             |
| **`pcc_eng_06_103.0609_x1651098_20:14-15-16`**  | In his estimation , the actual nuts and bolts of the procedure are not __`that far-fetched`__ for any ED to perform , as long as the necessary back - up services to take patients to definitive therapy are close at hand .            |
| **`nyt_eng_20000321_0286_23:17-19-20`**         | based on the Golden Bear 's expanded playing schedule in 2000 , a Colonial cameo might not be __`that far-fetched`__ .                                                                                                                  |


2. _that thrilled_

|                                                | `token_str`                                                                                                                                                                              |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_100.0477_x1602316_03:14-15-16`** | Maybe you 've got a Word Press blog already , but you are n't __`that thrilled`__ with how it 's functioning .                                                                           |
| **`pcc_eng_15_100.4327_x1606964_08:3-4-5`**    | I was n't __`that thrilled`__ with the cybernetic additions to it anyway .                                                                                                               |
| **`pcc_eng_12_001.2080_x0003435_3:26-27-28`**  | Punk was asked about possibly facing The Dead Man at Wrestle Mania during a panel at last September 's Ohio Comic-Con , and Punk was n't __`that thrilled`__ about the potential match . |
| **`pcc_eng_00_065.6586_x1045361_19:15-16-17`** | And I even insist , though my wife [ who is Jewish ] is n't __`that thrilled`__ , on having for our daughter a little version of the Seder .                                             |
| **`pcc_eng_28_024.1654_x0374101_09:12-13-14`** | My expectations were low going in , but I still was n't __`that thrilled`__ with the book .                                                                                              |


3. _that uncommon_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_078.2891_x1249008_316:3-4-5`**   | That is not __`that uncommon`__ and I understand that happens every day .                                                                                                                                                                                                                                                           |
| **`pcc_eng_15_048.9603_x0775350_14:6-8-9`**    | Zero-day attacks against Reader are n't all __`that uncommon`__ , but the bulk of the problem comes from users running old versions , getting exploited through patched vulnerabilities .                                                                                                                                           |
| **`pcc_eng_18_008.9083_x0127940_11:19-20-21`** | Early morning FBI arrests for those who threaten national security based on wiretaps and email interceptions are now not __`that uncommon`__ , but you can walk the streets confident that you are not on camera the whole time , and the innocent seem to have relatively little to fear .                                         |
| **`pcc_eng_24_071.1969_x1135485_037:6-7-8`**   | Perhaps such a practice was not __`that uncommon`__ in Japan , especially during the Middle Ages .                                                                                                                                                                                                                                  |
| **`pcc_eng_17_040.5088_x0638512_33:08-09-10`** | Girls on a Little League team are n't __`that uncommon`__ ( and Chelsea 's teammates seem adorably unfazed about her gender in the ESPN segment ) , but resistance seems to build as the level of play increases and competition for spots means any possible distraction , even a genetic one , can push a player off the roster . |


4. _that surprising_

|                                                | `token_str`                                                                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_002.4752_x0023734_16:6-7-8`**    | That coffee is king is n't __`that surprising`__ , but the popularity of celery seems weird .                                                                                                                                                                                |
| **`pcc_eng_27_003.3409_x0037640_51:26-27-28`** | A quick Yahoo search reveals that this is something many individuals still believe today , which in the grand scheme of the Internet is honestly not __`that surprising`__ .                                                                                                 |
| **`pcc_eng_24_084.2654_x1346875_072:3-4-5`**   | This is not __`that surprising`__ as it is after all broken and broken economies are not quickly fixed .                                                                                                                                                                     |
| **`pcc_eng_04_070.4973_x1122489_19:10-11-12`** | In one way , the study 's results are n't __`that surprising`__ .                                                                                                                                                                                                            |
| **`pcc_eng_26_084.6989_x1353571_07:47-49-50`** | Thinking about the number of students involved - fifteen from each school - and the fact that each was having ten of their best shots on two display boards , plus boards full of their other pictures of the places we had been , it was n't really __`that surprising`__ . |


5. _that dissimilar_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_039.8031_x0627596_36:11-13-14`** | The science of our time tells us that you are not all __`that dissimilar`__ to a TV , and the station you pick up ( your reality ) has much to do with what you are tuned into .                                                                                                                                                                         |
| **`pcc_eng_02_010.0479_x0146168_75:4-5-6`**    | Their motives are n't __`that dissimilar`__ , either .                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_03_086.7031_x1387766_09:12-13-14`** | " The Universal Sony survey found that in reality we are not __`that dissimilar`__ to the Snow White fairytale ideal , with the research results mirroring the plot involving thecharacters of the evil queen Ravenna , ( Charlize Theron ) and Snow White ( Kristen Stewart ) , where a beautiful appearance is inferior to a kind heart , " she said . |
| **`pcc_eng_27_061.0198_x0970053_13:15-16-17`** | This counterpoint of motherly and gubernatorial duties reveals that the two jobs really are n't __`that dissimilar`__ .                                                                                                                                                                                                                                  |
| **`pcc_eng_20_009.7335_x0140842_09:11-12-13`** | For those that do n't know , hydrogen cars are n't __`that dissimilar`__ from electric cars in the way they move and operate .                                                                                                                                                                                                                           |


6. _that unusual_

|                                                | `token_str`                                                                                                                                                                                                         |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_001.4891_x0007730_50:4-5-6`**    | But that was n't __`that unusual`__ for minor-league arenas at the time .                                                                                                                                           |
| **`nyt_eng_20070201_0228_44:22-23-24`**        | the title of one 1861 Confederate song sheet , `` My God ! What Is This All For ? '' is not __`that unusual`__ .                                                                                                    |
| **`pcc_eng_09_037.4457_x0589982_05:7-8-9`**    | First Read notes that it 's not __`that unusual`__ for a presidential campaign to change managers when things are n't going well .                                                                                  |
| **`pcc_eng_18_045.5733_x0721472_07:5-6-7`**    | Logsdon said it is n't __`that unusual`__ for boys to do that .                                                                                                                                                     |
| **`pcc_eng_28_065.1249_x1037592_36:41-42-43`** | The $ 120 per vote that Khanna spent might seem like a lot , Gerston said , but given his low name recognition compared to seven- term incumbent Honda , " an almost 4 - to - 1 ratio is not __`that unusual`__ . " |


7. _that noticeable_

|                                                | `token_str`                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_034.9771_x0550267_54:4-5-6`**    | Puerto Ricans are not __`that noticeable`__ in the United States , because we have so much diversity as it is .                                                                                                                                                    |
| **`pcc_eng_16_085.0087_x1359795_52:10-12-13`** | Marijuana activists were hoping Colorado 's grand experiment would n't be __`that noticeable`__ after an initial rush of shopping .                                                                                                                                |
| **`pcc_eng_19_073.1119_x1164880_3:23-24-25`**  | I just got braces put on yesterday , they hurt of course but they 're ceramic so they look nice and are n't __`that noticeable`__ .                                                                                                                                |
| **`pcc_eng_17_100.1973_x1603440_3:46-47-48`**  | My hair dresser weaved the colour through my natural brown so it 's a little bit more subtle and blends a little better with the top layer of my hair , without looking like I 've dipped my hair in dye ( although it 's not __`that noticeable`__ in the photo ! |
| **`pcc_eng_22_066.4802_x1058237_02:7-8-9`**    | It will be slightly smaller but not __`that noticeable`__ .                                                                                                                                                                                                        |


8. _that complicated_

|                                                 | `token_str`                                                                            |
|:------------------------------------------------|:---------------------------------------------------------------------------------------|
| **`apw_eng_20020730_0397_13:6-7-8`**            | `` The operation itself is not __`that complicated`__ .                                |
| **`pcc_eng_02_091.2391_x1458980_50:5-6-7`**     | And the solutions are not __`that complicated`__ .                                     |
| **`pcc_eng_26_097.9696_x1567736_80:13-14-15`**  | I ca n't understand all the details but the basic idea is n't __`that complicated`__ . |
| **`pcc_eng_08_107.0102_x1716545_116:12-13-14`** | If you strive for that , all the other stuff is n't __`that complicated`__ .           |
| **`pcc_eng_01_040.7428_x0642175_24:6-7-8`**     | I guess life just is n't __`that complicated`__ when you 're marrying Hef .            |


9. _that familiar_

|                                                | `token_str`                                                                                                                                                                                                           |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_031.1827_x0487860_31:08-09-10`** | Now , most of the audience was not __`that familiar`__ with Jim and I 'm going go out on a limb and say many of them had no idea what kind of comedy he does or what his life is .                                    |
| **`pcc_eng_01_034.9562_x0548609_21:25-26-27`** | Though Suicide Squad certainly enjoys a wide following , the story builds upon quite a lot of Suicide Squad lore that I just was n't __`that familiar`__ with , and it made it hard to be all that engaged .          |
| **`pcc_eng_18_040.0411_x0631702_09:4-5-6`**    | If you are not __`that familiar`__ with Word Press the video tutorials will guide ...                                                                                                                                 |
| **`pcc_eng_02_086.1077_x1375939_07:17-18-19`** | Barnes also shed light on Solange 's role as matchmaker , revealing , " I was n't __`that familiar`__ with her Destiny 's                                                                                             |
| **`pcc_eng_23_035.3524_x0554898_07:11-12-13`** | This chart is not easily digestible by someone who is not __`that familiar`__ with Moto GP racing , and the original post did not contain much data as to what this infographic was all about or why it was created . |


10. _that hard_

|                                                 | `token_str`                                                                                                                                             |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_085.8509_x1373075_36:17-18-19`**  | Look Tom , I know there 's alot of turnover at Notre Dame but it 's not __`THAT hard`__ to learn the names and numbers of the freshmen and sophomores . |
| **`pcc_eng_28_077.7004_x1240696_046:09-10-11`** | So I will tell you that risotto is not __`that hard`__ .                                                                                                |
| **`nyt_eng_19990729_0090_12:16-17-18`**         | a lot of other people ended up cleaning up a lot of things that were n't __`that hard`__ to get done . ''                                               |
| **`pcc_eng_14_091.6059_x1464560_31:08-10-11`**  | " Numberwise and clubwise , it should n't be __`that hard`__ , " he said .                                                                              |
| **`pcc_eng_26_096.3568_x1541897_46:4-6-7`**     | Boiling water should n't be __`that hard`__ .                                                                                                           |


11. _that keen_

|                                                | `token_str`                                                                                                                                                                             |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_046.5788_x0737592_08:4-6-7`**    | Normally I am not all __`that keen`__ on watching a 19 min video , yet this one kept my interest from the beginning until the end .                                                     |
| **`pcc_eng_07_051.1010_x0809919_22:3-4-5`**    | I was n't __`that keen`__ on the color when I saw it in the bottle , but once I applied it I loved it .                                                                                 |
| **`pcc_eng_13_008.5844_x0122431_23:34-35-36`** | In the twenty - first century , we can no more write a child off because " he 's not into numbers " any more than we would accept that " she 's not __`that keen`__ on the alphabet " . |
| **`apw_eng_19980225_1426_48:14-16-17`**        | her folks are not home , and let 's just say she 's not all __`that keen`__ to hit the books .                                                                                          |
| **`pcc_eng_12_032.5640_x0510985_11:28-29-30`** | If you have a glut of tomatoes you can turn them into soup or Napoli sauce as these freeze well , even if the whole tomatoes are n't __`that keen`__ on getting frosty .                |


12. _that impressive_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_054.1707_x0859538_49:27-28-29`**  | Apple says that it has 7,000 movies to rent with over 3,400 available in HD , which compared to those available through the Netflix service is not __`that impressive`__ .                                                                                                                                                                                                   |
| **`pcc_eng_10_079.2508_x1264773_6:23-25-26`**   | Just do n't expect to blow anyone 's mind because without the added element of having to balance , your tricks wo n't be __`that impressive`__ .                                                                                                                                                                                                                             |
| **`pcc_eng_16_077.6387_x1240217_133:19-20-21`** | I 'm guessing that where he is , currently , being on the cutting edge of OER is n't __`that impressive`__ but maybe in another year or two of the OER movement growing ...?                                                                                                                                                                                                 |
| **`pcc_eng_11_018.6535_x0285562_86:5-6-7`**     | My first try was not __`that impressive`__ .                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_27_023.9948_x0371803_07:50-52-53`**  | Diaz , who homered twice in the MLB All - Star Futures Game while he was with the Dodgers and was traded days later , hit .285/392/.449 with 11 home runs and 15 doubles between Double -A Tulsa and Bowie , though his .239/.329/.403 line with the Baysox was n't all __`that impressive`__ as the Orioles got to work tinkering with his swing shortly after he arrived . |


13. _that fond_

|                                                | `token_str`                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19970903_0955_23:41-42-43`**        | a woman who declined to be named said : `` Why does she have to hide behind the gates of Balmoral ? My God , if I died I hope my mother-in-law would say something , even if she was n't __`that fond`__ of me . |
| **`pcc_eng_05_008.4749_x0121348_04:08-10-11`** | To tell the truth , I have never been __`that fond`__ of calabacitas , a Mexican squash dish made with zucchini and / or yellow summer squash .                                                                  |
| **`pcc_eng_06_107.5121_x1722932_35:11-12-13`** | I 'm led to believe there are people who are n't __`that fond`__ of seals , saying they 're smelly , noisome vermin that litter the beaches and eat far too many fish .                                          |
| **`pcc_eng_21_027.7355_x0432217_072:3-4-5`**   | I was n't __`that fond`__ of the route overall .                                                                                                                                                                 |
| **`pcc_eng_24_021.6624_x0333739_15:12-13-14`** | It 's no surprise that Margaery ( Natalie Dormer ) was n't __`that fond`__ of Joffrey himself , but rather wanted the power her marriage to him would bring .                                                    |


14. _that comfortable_

|                                                | `token_str`                                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_050.3279_x0798544_17:25-27-28`** | To accomplish this , the headphones sit very close to the head and we actually found that they felt quite tight so they were n't really __`that comfortable`__ after a while .                                                                                      |
| **`pcc_eng_07_054.7104_x0868207_18:19-20-21`** | A Jeep Wrangler is about as aerodynamic as a brick , has terrible fuel economy , and is n't __`that comfortable`__ compared to other cars in its price range .                                                                                                      |
| **`pcc_eng_27_055.0829_x0874062_41:10-11-12`** | Similarly , if you 're good with people but not __`that comfortable`__ with numbers , you should make the effort to learn some accounting fundamentals so you can follow these conversations in a business meeting and not have to rely solely on your accountant . |
| **`pcc_eng_05_035.7409_x0562739_05:19-20-21`** | They are green , suede , I do n't wear them all that often , because they are not __`that comfortable`__ , and they are falling apart .                                                                                                                             |
| **`pcc_eng_06_021.4078_x0330167_15:09-10-11`** | In fact , the only folks that were n't __`that comfortable`__ around Jesus - the only people who would n't invite Jesus to party - were the religious .                                                                                                             |


15. _that clear_

|                                                 | `token_str`                                                                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_033.0708_x0519508_126:20-22-23`** | This is totally a lot much better than to wear a really fancy wedding dress but the value is not really __`that clear`__ .                                                                                                               |
| **`pcc_eng_10_029.0775_x0453834_52:43-44-45`**  | But if I have to choose from the first seven kings , my favorite goes to The Mystic , where he seems to have more portion to talk with Nyx in Kingsglaive : Final Fantasy XV movie , although his shape is n't __`that clear`__ either . |
| **`pcc_eng_16_022.0277_x0340541_18:28-29-30`**  | D Visualization is considered as the best tool for design professionals and facility users , as they are able to explore and understand special structures which are not __`that clear`__ on 2D drawings .                               |
| **`pcc_eng_04_001.7323_x0011889_41:5-7-8`**     | The broader issues are not always __`that clear`__ , however .                                                                                                                                                                           |
| **`pcc_eng_25_002.8456_x0030025_10:17-18-19`**  | They say you can see it from Tampa when it 's clear , but it was n't __`that clear`__ .                                                                                                                                                  |


16. _that popular_

|                                                | `token_str`                                                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_034.4971_x0541487_12:6-7-8`**    | " While the PC is not __`that popular`__ in front of general consumers , the company could be struggling in terms of recovering the profitability it had before . "                                                                                          |
| **`pcc_eng_26_085.0632_x1359461_04:25-26-27`** | With the exception of the " Medium " and " High " buy - in PL 5 - Card Draw events ( which are never __`that popular`__ with players ) , the events in the SCOOP series so far have had prize pools that have easily topped the guarantees from Pokerstars . |
| **`pcc_eng_12_030.7767_x0482120_062:5-6-7`**   | Fire tax hikes were not __`that popular`__ throughout the state .                                                                                                                                                                                            |
| **`pcc_eng_18_038.0052_x0598726_05:18-19-20`** | The economy is not growing that strongly and , partly as a consequence , President Obama is not __`that popular`__ .                                                                                                                                         |
| **`pcc_eng_26_034.6850_x0544490_08:23-24-25`** | " He 's amazing and should be regarded as one of the top three athletes Germany has ever had but golf is not __`that popular`__ and people over there do n't see it that way . "                                                                             |


17. _that simple_

|                                                | `token_str`                                                                                                                                                                                                 |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19960329_0696_3:09-12-13`**         | as is the custom lately , things would not be quite __`that simple`__ .                                                                                                                                     |
| **`pcc_eng_12_069.9272_x1113535_49:3-4-5`**    | Now was n't __`that simple`__ ?                                                                                                                                                                             |
| **`pcc_eng_15_013.0538_x0194490_08:09-11-12`** | She wants to belong , but life is n't always __`that simple`__ .                                                                                                                                            |
| **`nyt_eng_19980728_0070_16:5-7-8`**           | but the issue is n't quite __`that simple`__ .                                                                                                                                                              |
| **`pcc_eng_20_083.5545_x1333932_09:33-34-35`** | If you 're going to a decade themed party , getting a wig that matches your outfit is essential because re-creating most hairstyles that people used to wear in previous decades is n't __`that simple`__ ! |


18. _that easy_

|                                             | `token_str`                                                                                                                                |
|:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19990830_0188_15:5-6-7`**        | unfortunately , it 's not __`that easy`__ .                                                                                                |
| **`pcc_eng_14_096.3377_x1541308_53:4-5-6`** | It 's just not __`that easy`__ to generate income from viral videos , even using some app like this .                                      |
| **`nyt_eng_20070509_0290_3:21-22-23`**      | when an estimated one in five people has mental health issues , Dillinger continued , identifying them is `` just not __`that easy`__ . '' |
| **`pcc_eng_05_097.6227_x1563216_45:3-4-5`** | It is not __`that easy`__ , certainly not for so many African - Americans .                                                                |
| **`pcc_eng_04_084.3729_x1346954_42:5-6-7`** | Having an impact is not __`that easy`__ .                                                                                                  |


19. _that big_

|                                                | `token_str`                                                                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_046.8438_x0741738_15:3-4-5`**    | He 's not __`that big`__ , but he hits hard .                                                                                                                                                                                                                                                       |
| **`pcc_eng_18_086.9031_x1391103_03:47-48-49`** | While there , they meet the handsome Spanish artist Juan Antonio ( Javier Bardem ) and his suicidal artist ex-wife , Maria Elena ( Penelope Cruz ) and engage in various love-triangles revolving around the Spanish stud , including a three - way that actually is n't __`that big`__ of a deal . |
| **`pcc_eng_18_089.7076_x1436496_05:14-15-16`** | You can find lots of fun t-shirts on Costume Squad if you 're not __`that big`__ on dressing up in a costume .                                                                                                                                                                                      |
| **`pcc_eng_08_107.6246_x1726385_13:10-11-12`** | It all worked out perfectly because the market was n't __`that big`__ and we had just enough time to look around before heading to a quaint little restaurant called The Pantry for lunch before heading home .                                                                                     |
| **`pcc_eng_28_042.0801_x0664534_65:17-19-20`** | With the low cost of compatible 16GB USB flash drives these days , it really should not be __`that big`__ of a deal .                                                                                                                                                                               |


20. _that great_

|                                                 | `token_str`                                                                                                                                                                                                                                                        |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_069.9289_x1113561_40:10-11-12`**  | I 've seen reviews on how this fin is n't __`that great`__ but it is n't true !                                                                                                                                                                                    |
| **`pcc_eng_04_101.6472_x1626020_17:14-15-16`**  | The main course of swordfish was n't too bad , but it was n't __`that great`__ either .                                                                                                                                                                            |
| **`pcc_eng_05_088.0013_x1407675_143:18-19-20`** | A lot of black people know we have a lot of shit in our families that are n't __`that great`__ .                                                                                                                                                                   |
| **`pcc_eng_16_055.8010_x0886926_156:51-52-53`** | For what it 's worth these are lots of lightweight models of hiking boots out there and there are a couple of them here on this review , but the Salomon Quest 4D 2 GTX simply is n't one of them and weight is the one thing that it 's not __`that great`__ at . |
| **`pcc_eng_25_085.8963_x1373939_33:43-45-46`**  | " I honestly do n't feel like it 's been a problem for me , but in fairness , I did n't take a test 18 years ago to compare it , " said Astles , who added that his hearing was n't all __`that great`__ to begin with .                                           |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/...

Samples saved as...
1. `neg_bigram_examples/that/that_far-fetched_99ex.csv`
1. `neg_bigram_examples/that/that_thrilled_99ex.csv`
1. `neg_bigram_examples/that/that_uncommon_99ex.csv`
1. `neg_bigram_examples/that/that_surprising_99ex.csv`
1. `neg_bigram_examples/that/that_dissimilar_99ex.csv`
1. `neg_bigram_examples/that/that_unusual_99ex.csv`
1. `neg_bigram_examples/that/that_noticeable_99ex.csv`
1. `neg_bigram_examples/that/that_complicated_99ex.csv`
1. `neg_bigram_examples/that/that_familiar_99ex.csv`
1. `neg_bigram_examples/that/that_hard_99ex.csv`
1. `neg_bigram_examples/that/that_keen_99ex.csv`
1. `neg_bigram_examples/that/that_impressive_99ex.csv`
1. `neg_bigram_examples/that/that_fond_99ex.csv`
1. `neg_bigram_examples/that/that_comfortable_99ex.csv`
1. `neg_bigram_examples/that/that_clear_99ex.csv`
1. `neg_bigram_examples/that/that_popular_99ex.csv`
1. `neg_bigram_examples/that/that_simple_99ex.csv`
1. `neg_bigram_examples/that/that_easy_99ex.csv`
1. `neg_bigram_examples/that/that_big_99ex.csv`
1. `neg_bigram_examples/that/that_great_99ex.csv`

## 3. *exactly*

|                     |        `N` |      `f1` |   `adv_total` |
|:--------------------|-----------:|----------:|--------------:|
| **NEGATED_exactly** | 72,839,589 | 3,173,660 |        58,643 |
| **NEGMIR_exactly**  |  1,701,929 |   291,732 |         1,041 |


|                               |   `f` |   `adj_total` |   `dP1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:------------------------------|------:|--------------:|--------:|--------:|----------:|----------:|------------:|-------:|
| **NEGany~exactly_conducive**  |   208 |         9,110 |    0.96 |    7.82 |  1,303.50 |      9.06 |      198.94 |    208 |
| **NEGany~exactly_shocking**   |   151 |        35,115 |    0.96 |    7.33 |    946.29 |      6.58 |      144.42 |    151 |
| **NEGany~exactly_pleasant**   |   142 |        52,223 |    0.96 |    7.24 |    889.88 |      6.19 |      135.81 |    142 |
| **NEGany~exactly_famous**     |   130 |       223,813 |    0.96 |    7.10 |    814.68 |      5.66 |      124.34 |    130 |
| **NEGany~exactly_difficult**  |   126 |       732,106 |    0.96 |    7.05 |    789.62 |      5.49 |      120.51 |    126 |
| **NEGany~exactly_easy**       | 1,066 |       579,827 |    0.95 |    9.32 |  6,596.91 |     46.75 |    1,019.25 |  1,073 |
| **NEGany~exactly_cheap**      |   691 |        60,531 |    0.95 |    8.96 |  4,281.59 |     30.28 |      660.72 |    695 |
| **NEGany~exactly_surprising** |   440 |        70,540 |    0.95 |    8.71 |  2,743.34 |     19.21 |      420.79 |    441 |
| **NEGany~exactly_new**        | 1,371 |       253,862 |    0.94 |    9.10 |  8,410.32 |     60.48 |    1,310.52 |  1,388 |
| **NEGany~exactly_clear**      | 1,746 |       349,214 |    0.94 |    8.78 | 10,578.33 |     77.73 |    1,668.27 |  1,784 |
| **NEGmir~exactly_sure**       |   148 |         6,761 |    0.83 |    5.31 |    522.11 |     25.37 |      122.63 |    148 |
| **NEGmir~exactly_easy**       |    20 |        18,610 |    0.83 |    1.86 |     70.55 |      3.43 |       16.57 |     20 |
| **NEGmir~exactly_clear**      |    52 |         6,722 |    0.81 |    3.38 |    173.89 |      9.08 |       42.92 |     53 |
| **NEGmir~exactly_new**        |    29 |        12,836 |    0.80 |    2.31 |     93.90 |      5.14 |       23.86 |     30 |


1. _exactly conducive_

|                                                | `token_str`                                                                                                                                                                                                 |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_045.4253_x0717120_21:1-2-3`**    | Not __`exactly conducive`__ to being a rock star .                                                                                                                                                          |
| **`nyt_eng_19991125_0190_34:21-22-23`**        | i 'm sure he realizes alternating three point guards and shuttling other players in and out of the lineup is n't __`exactly conducive`__ to team continuity and chemistry .                                 |
| **`pcc_eng_07_024.8862_x0386333_03:7-8-9`**    | However , Garcia 's style is n't __`exactly conducive`__ to having his hand raised either and has resulted in 3 - 6 - 1 record in his last ten tilts including losses in a quartet of consecutive clashes . |
| **`pcc_eng_04_054.9401_x0871212_25:13-14-15`** | I would caution you though that the setting of this book is not __`exactly conducive`__ to a morally clean setting , but Ms. Chaikin handled it very nicely .                                               |
| **`pcc_eng_21_074.5469_x1188529_13:21-22-23`** | Monday through Wednesday I 'm flying out to South Dakota to visit an operations center , and business trips are n't __`exactly conducive`__ to watching your calorie intake .                               |


2. _exactly shocking_

|                                                | `token_str`                                                                                                                                                                              |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_059.7527_x0949024_11:3-4-5`**    | Again , not __`exactly shocking`__ .                                                                                                                                                     |
| **`pcc_eng_14_003.1417_x0034674_45:11-12-13`** | The price is n't exactly cheap , but it 's not __`exactly shocking`__ , either .                                                                                                         |
| **`nyt_eng_20000418_0011_23:4-5-6`**           | but it was n't __`exactly shocking`__ , not for a man who has worked with the league owners since 1993 and was a known quantity within baseball 's political circle .                    |
| **`pcc_eng_14_086.3929_x1380285_09:6-7-8`**    | And yes , it 's not __`exactly shocking`__ that Wall Streeters want to leave big firms to form their own hedge funds .                                                                   |
| **`pcc_eng_18_001.0110_x0000163_23:3-4-5`**    | It 's not __`exactly shocking`__ , since , yes , the bull 's -eye on Gaylen 's head has been growing larger by the week , but the assassination 's quickness hits harder than expected . |


3. _exactly pleasant_

|                                                 | `token_str`                                                                                                                                                                                                                                       |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_069.6988_x1110332_24:24-25-26`**  | Crystal Fairy is tough at times to watch -- the characters are n't typically likable and Silva 's muddy , handheld aesthetic is n't __`exactly pleasant`__ .                                                                                      |
| **`pcc_eng_20_035.8938_x0564043_066:42-43-44`** | Things were kind of rushed at dinner time last night , and I just served it on croissants with no description , just like I serve regular chicken salad , and apparently the taste came as quite a surprise that was n't __`exactly pleasant`__ . |
| **`pcc_eng_06_073.2295_x1168344_215:3-4-5`**    | It 's not __`exactly pleasant`__ to read .                                                                                                                                                                                                        |
| **`pcc_eng_25_092.3663_x1478503_046:1-2-3`**    | Not __`exactly pleasant`__ to think about .                                                                                                                                                                                                       |
| **`pcc_eng_00_004.7264_x0060175_54:18-19-20`**  | The movie was a bomb with film critics and fans , and apparently making the film was n't __`exactly pleasant`__ for Munn .                                                                                                                        |


4. _exactly famous_

|                                               | `token_str`                                                                                                                                                                                                                                                                             |
|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_049.9895_x0792221_235:5-6-7`**  | Well , I was n't __`exactly famous`__ -- nobody knew who I was -- yet it felt as if I was famous because there were swarms of people trying to take a photo with me .                                                                                                                   |
| **`pcc_eng_20_003.9258_x0046965_5:3-4-5`**    | Well , not __`exactly famous`__ , but my new day after a long Thanksgiving holiday weekend began with such a delightful pleasure of likes cast upon by Dr. Suglia , a profound scholar of literature and philosophy and a sui generis writer par excellence , for my posts on my blog ! |
| **`pcc_eng_12_083.7662_x1337433_3:12-13-14`** | If you are lucky enough to live in the Netherlands ( not __`exactly famous`__ for its mountains ) and attend the University of Twente , you could have the chance .                                                                                                                     |
| **`pcc_eng_02_092.1554_x1473748_01:2-3-4`**   | Gujarat Not __`Exactly Famous`__ For Its Soldiers - Aakar Patel                                                                                                                                                                                                                         |
| **`pcc_eng_03_033.2877_x0522967_38:3-4-5`**   | Baseball is n't __`exactly famous`__ for making sound financial decisions .                                                                                                                                                                                                             |


5. _exactly difficult_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_051.6030_x0817819_026:21-22-23`** | Not many schools better than Uof C , and small class size makes it so getting big firm job is n't __`exactly difficult`__ .                                                                                                                                                                                                                               |
| **`pcc_eng_27_069.0405_x1100124_070:4-5-6`**    | Ryan Lochte 's not __`exactly difficult`__ to look at , either .                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_00_075.5146_x1204581_28:14-15-16`**  | Re-implementing something like any ( ) , map ( ) , etc. is not __`exactly difficult`__ .                                                                                                                                                                                                                                                                  |
| **`pcc_eng_21_016.8255_x0255479_30:3-4-5`**     | It 's not __`exactly difficult`__ , is it ? "                                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_00_062.1846_x0989130_17:43-44-45`**  | A neat image that fans of the comics - particularly the stellar " Long Halloween " series - can latch on to , one that does , in its way , give a small glimpse into the plot , although it was not __`exactly difficult`__ to figure out that Harvey Dent 's rise to the position of District Attorney was somehow going to be a part of the new movie . |


6. _exactly surprising_

|                                                | `token_str`                                                                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_085.4516_x1367422_45:16-17-18`** | Some people begin to see me as a free meal ticket , but that 's not __`exactly surprising`__ .                                                                                                         |
| **`pcc_eng_17_007.9368_x0112216_29:3-4-5`**    | That 's not __`exactly surprising`__ to me considering I 'm new to all this .                                                                                                                          |
| **`pcc_eng_02_087.7692_x1402857_06:35-36-37`** | A few of Marvel 's major stars are set to exit the MCU after Infinity War , and between the battle with Thanos and a few contracts expiring behind the scenes , that 's not __`exactly surprising`__ . |
| **`pcc_eng_13_038.1122_x0600071_3:14-15-16`**  | And while encouraging , the lack of violent crimes for a day is n't __`exactly surprising`__ .                                                                                                         |
| **`pcc_eng_27_106.8027_x1711506_04:18-19-20`** | Shifting from an era when one man , Than Shwe , dominated the country , it is not __`exactly surprising`__ that politics in the reform period would be highly personalized .                           |


7. _exactly cheap_

|                                                | `token_str`                                                                                                                                             |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_004.6041_x0058545_32:5-6-7`**    | This prescription medication is not __`exactly cheap`__ .                                                                                               |
| **`pcc_eng_09_009.0138_x0129825_21:6-7-8`**    | " Cheap " money is not __`exactly cheap`__ .                                                                                                            |
| **`pcc_eng_17_058.0068_x0920985_31:12-13-14`** | The stock trades at 10.5 times revenue , so it 's not __`exactly cheap`__ .                                                                             |
| **`nyt_eng_20050509_0225_5:11-12-13`**         | here 's a look at two top-of-the-line PCs that are n't __`exactly cheap`__ , but they 'll do just about anything you need them to do -- and then some . |
| **`pcc_eng_25_009.0698_x0130764_15:7-8-9`**    | At 2000 euros , it 's not __`exactly cheap`__ , but definitely cool .                                                                                   |


8. _exactly easy_

|                                                | `token_str`                                                                                                                                                                 |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_106.9133_x1711045_03:25-26-27`** | Watching the show each week can be a fraught emotional experience -- death is often swift and brutal in Westeros -- but it 's not __`exactly easy`__ on the actors either . |
| **`pcc_eng_24_103.9223_x1665222_35:11-12-13`** | Once you 've been arrested or convicted , it is n't __`exactly easy`__ to find legitimate work .                                                                            |
| **`pcc_eng_03_005.6313_x0074826_37:5-6-7`**    | Answering this question is not __`exactly easy`__ .                                                                                                                         |
| **`pcc_eng_05_089.5852_x1433092_04:4-5-6`**    | But it is n't __`exactly easy`__ to care for .                                                                                                                              |
| **`pcc_eng_10_086.6351_x1384000_23:08-10-11`** | The company told ZDNet that Snapchat is n't " __`exactly easy`__ to get hold of . "                                                                                         |


9. _exactly new_

|                                                 | `token_str`                                                                                                                                                                            |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20060711_0296_42:3-4-5`**            | well , not __`exactly new`__ .                                                                                                                                                         |
| **`pcc_eng_06_107.9617_x1730227_038:25-26-27`** | The bass sound was largely influence by the likes of Meshuggah and Gojira , which was n't a bad thing per se but was n't __`exactly new`__ .                                           |
| **`pcc_eng_02_001.0536_x0000878_011:1-2-3`**    | Not __`exactly new`__ , but certainly limited in its production and its consumption .                                                                                                  |
| **`pcc_eng_14_031.7981_x0497623_16:5-6-7`**     | Well , it 's not __`exactly new`__ , but it 's definitely different from what most cities and towns have had in the past .                                                             |
| **`pcc_eng_18_089.2268_x1428683_30:14-15-16`**  | While China 's acts of censorship and routine banishments of Western technologies are n't __`exactly new`__ , their take - no- chances stance reflects a very real , logical concern . |


10. _exactly clear_

|                                                 | `token_str`                                                                                                                                                                                                                        |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_038.3661_x0604742_103:27-28-29`** | " He 's the funniest guy I 've ever met , " says Lochte , clapping his hands and laughing -- at what , it 's not __`exactly clear`__ .                                                                                             |
| **`pcc_eng_25_086.3400_x1381149_08:3-4-5`**     | It is not __`exactly clear`__ if the home of the candidate and that of the spouse are one and the same or whether the two maintain separate residences , however , for reasons hereinafter stated the outcome should be the same . |
| **`pcc_eng_28_047.3686_x0750336_13:3-4-5`**     | It is not __`exactly clear`__ whether Kokesh will carry through with the event , since he says it needs to reach a critical mass of 10,000 RSVPs first .                                                                           |
| **`pcc_eng_04_054.4254_x0863006_04:16-17-18`**  | The soldier 's free hand appears to have his fingers crossed , but it 's not __`exactly clear`__ .                                                                                                                                 |
| **`pcc_eng_06_025.3737_x0394504_123:16-17-18`** | Now , I get the argument for deliberate or not deliberate , and it 's not __`exactly clear`__ either way .                                                                                                                         |


11. _exactly sure_

|                                                 | `token_str`                                                                                                                                                                                 |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_014.1742_x0212980_02:1-2-3`**     | Not __`exactly sure`__ how I 'll use it , because it 's applicable for only one client at a time , whereas a website is applicable for multiple parties without using the special goggles . |
| **`pcc_eng_07_012.2839_x0182947_009:10-11-12`** | But now that you 're retiring , you 're not __`exactly sure`__ what to do with this newfound freedom .                                                                                      |
| **`pcc_eng_05_034.7676_x0546846_046:10-11-12`** | He did n't like it , and he was n't __`exactly sure`__ why he understood .                                                                                                                  |
| **`pcc_eng_26_007.6578_x0107292_12:12-13-14`**  | After reading the quotes from the ufo-ologists , I 'm still not __`exactly sure`__ what they want the government to do besides " act . "                                                    |
| **`pcc_eng_02_084.2673_x1346280_06:3-4-5`**     | I 'm not __`exactly sure`__ how it 's working in this context but the Note Length MIDI Effect is present in the Drum Rack and is clearly responsible .                                      |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/...

Samples saved as...
1. `neg_bigram_examples/exactly/exactly_conducive_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_shocking_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_pleasant_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_famous_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_difficult_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_surprising_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_cheap_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_easy_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_new_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_clear_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_sure_99ex.csv`

## 4. *any*

|                 |        `N` |      `f1` |   `adv_total` |
|:----------------|-----------:|----------:|--------------:|
| **NEGMIR_any**  |  1,701,929 |   291,732 |         1,197 |
| **NEGATED_any** | 72,839,589 | 3,173,660 |        34,382 |


|                          |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:-------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGmir~any_younger**   |    20 |           939 |    0.83 |    1.86 |    70.55 |      3.43 |       16.57 |     20 |
| **NEGmir~any_clearer**   |    17 |           130 |    0.83 |    1.50 |    59.97 |      2.91 |       14.09 |     17 |
| **NEGany~any_happier**   |   828 |        16,606 |    0.82 |    6.34 | 4,420.49 |     41.96 |      786.04 |    963 |
| **NEGmir~any_different** |    48 |        36,166 |    0.81 |    3.24 |   159.93 |      8.40 |       39.60 |     49 |
| **NEGmir~any_bigger**    |    36 |         3,923 |    0.80 |    2.73 |   118.17 |      6.34 |       29.66 |     37 |
| **NEGany~any_younger**   |   255 |        26,216 |    0.79 |    5.57 | 1,323.36 |     13.38 |      241.62 |    307 |
| **NEGany~any_nicer**     |    96 |         9,955 |    0.76 |    4.75 |   486.82 |      5.18 |       90.82 |    119 |
| **NEGmir~any_easier**    |    61 |         2,386 |    0.75 |    3.04 |   181.65 |     11.31 |       49.69 |     66 |
| **NEGmir~any_better**    |   380 |        14,013 |    0.74 |    4.38 | 1,096.01 |     71.82 |      308.18 |    419 |
| **NEGmir~any_good**      |    32 |        31,585 |    0.74 |    2.12 |    93.53 |      6.00 |       26.00 |     35 |
| **NEGmir~any_higher**    |    21 |         2,893 |    0.74 |    1.42 |    61.24 |      3.94 |       17.06 |     23 |
| **NEGany~any_simpler**   |   226 |        23,480 |    0.71 |    5.00 | 1,087.71 |     13.07 |      212.93 |    300 |
| **NEGany~any_brighter**  |    63 |         9,280 |    0.67 |    3.91 |   292.00 |      3.83 |       59.17 |     88 |
| **NEGmir~any_worse**     |    87 |         8,790 |    0.66 |    2.73 |   217.46 |     18.00 |       69.00 |    105 |
| **NEGmir~any_closer**    |    57 |           993 |    0.65 |    2.33 |   141.82 |     11.83 |       45.17 |     69 |
| **NEGany~any_smarter**   |    89 |         8,501 |    0.63 |    4.00 |   394.95 |      5.75 |       83.25 |    132 |
| **NEGany~any_easier**    | 1,594 |       209,940 |    0.62 |    5.08 | 6,987.78 |    104.79 |    1,489.21 |  2,405 |
| **NEGany~any_cheaper**   |   129 |        46,055 |    0.58 |    4.01 |   542.97 |      8.98 |      120.02 |    206 |
| **NEGany~any_clearer**   |   355 |        11,680 |    0.54 |    4.26 | 1,421.60 |     26.49 |      328.51 |    608 |
| **NEGany~any_worse**     | 1,686 |       179,012 |    0.42 |    3.94 | 5,676.37 |    160.03 |    1,525.97 |  3,673 |


1. _any younger_

|                                         | `token_str`                                                                                                                                                                                                             |
|:----------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_19981207_1742_12:13-15-16`** | and each year that goes by is another reminder that he is n't getting __`any younger`__ .                                                                                                                               |
| **`nyt_eng_19970125_0235_28:5-7-8`**    | Reggie , who was n't getting __`any younger`__ , wondered if perhaps time was running out for him although he never forgot his covenant nor lost his faith nor complained about the cold or about being double-teamed . |
| **`nyt_eng_20070325_0199_1:1-6-7`**     | none of them are getting __`any younger`__ .                                                                                                                                                                            |
| **`apw_eng_20080415_1153_21:19-21-22`** | although he does n't play in the field , baseball 's top home run hitter since 2004 is n't getting __`any younger`__ .                                                                                                  |
| **`nyt_eng_20071213_0030_29:07-09-10`** | but at 27 , I 'm not getting __`any younger`__ .                                                                                                                                                                        |


2. _any clearer_

|                                                 | `token_str`                                                                                                                                                           |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_066.2433_x1054653_006:14-16-17`** | The difference between the way we win matches and United manage to wo n't be __`any clearer`__ than after we welcome Leeds to the lane .                              |
| **`pcc_eng_04_084.4172_x1347684_36:2-3-4`**     | " Not __`any clearer`__ today , " said Chiarelli .                                                                                                                    |
| **`pcc_eng_29_033.5068_x0524668_30:3-5-6`**     | It could not be __`any clearer`__ to me that most Americans have tired of the war on drugs .                                                                          |
| **`pcc_eng_09_009.8529_x0143534_06:12-14-15`**  | During his response to the question about DAOs , Silbert could not be __`any clearer`__ in his support for the potential of Ethereum and the underlying ether token . |
| **`pcc_eng_12_065.5855_x1043962_04:16-18-19`**  | Wrapped in a cheerful , dreamy electro-pop melody with driving beats , the message could not be __`any clearer`__ !                                                   |


3. _any happier_

|                                                | `token_str`                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_007.7011_x0108204_30:3-5-6`**    | I could n't be __`any happier`__ to speak louder , to speak clearer , and to speak more directly to the mission , the duty , of what we 've always been : an institution that educates young men in the most excellent tradition of the liberal arts . " |
| **`pcc_eng_27_055.1819_x0875672_18:17-19-20`** | I have done months of pricing and research before I committed to buying this and could n't be __`any happier`__ with the quality , effects and durability of this outstanding mixer !                                                                    |
| **`pcc_eng_17_043.3460_x0683882_09:4-6-7`**    | Happy Valley could n't be __`any happier`__ right now for Smith , the former Gateway High School star and coach , who was serving as an assistant coach at Temple until he got a phone call from Franklin .                                              |
| **`pcc_eng_04_108.09276_x1744207_17:3-4-5`**   | Eleanor is not __`any happier`__ about the situation , though she understands her father 's reasoning : he 's dying and wishes to see her happily settled first .                                                                                        |
| **`nyt_eng_20050829_0235_32:10-12-13`**        | `` I love her to death ; I could n't be __`any happier`__ than I am right now , '' Koso said , adding of Bruning : `` He 's a home wrecker .                                                                                                             |


4. _any different_

|                                                 | `token_str`                                                                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_075.7397_x1207980_20:08-09-10`**  | According to Turnmyre , these rules are n't __`any different`__ than the rules enforced in the past , so the skaters and bikers will not notice any differences .                                                                                          |
| **`pcc_eng_20_034.8488_x0547224_017:07-12-13`** | Valentinas adds , " It 's not that Hollywood pedophiles are __`any different`__ than the ones in a small town .                                                                                                                                            |
| **`nyt_eng_20060424_0275_37:5-7-8`**            | public financing would probably not be __`any different`__ .                                                                                                                                                                                               |
| **`pcc_eng_15_019.3993_x0297208_3:6-7-8`**      | The reaction in baseball was n't __`any different`__ than it was in football -- divisive and controversial -- but Maxwell made it clear at the time that he was from a military family , so he had the utmost respect for the military and the U.S. flag . |
| **`pcc_eng_14_084.6755_x1352504_37:6-8-9`**     | From a moral standpoint its not really __`any different`__ than masturbation ( which , despite some confusion about the story of Onan in the Bible , is not a sin in Christianity ) , but it is n't all people seem to think it would be .                 |


5. _any bigger_

|                                                | `token_str`                                                                                                                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_091.4802_x1462961_06:47-49-50`** | Interestingly enough , Arshavin 's goal against Aktobe came seven years and two days after he scored four goals at Anfield in what was the highlight of his stint in England , and the difference between Arsenal 's famous red and Central Stadium in Almaty could n't be __`any bigger`__ . |
| **`pcc_eng_13_039.2654_x0618708_15:3-4-5`**    | They are n't __`any bigger`__ than the wild turkeys I feed , and those birds she ignores with notable disdain .                                                                                                                                                                               |
| **`pcc_eng_26_035.9966_x0565730_43:4-5-6`**    | The cup is hardly __`any bigger`__ than the mouth of the jar , so it does n't work that well .                                                                                                                                                                                                |
| **`pcc_eng_12_087.2536_x1393762_20:6-7-8`**    | And so the balance is not __`any bigger`__ when compared to the prior thirty day period .                                                                                                                                                                                                     |
| **`nyt_eng_20070113_0155_19:23-25-26`**        | `` In college you have at least 10 guys throughout the country that are 250 to 265 -LRB- pounds -RRB- -- they never get __`any bigger`__ , so they 're not 4-3 ends .                                                                                                                         |


6. _any nicer_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20090814_1161_19:4-7-8`**           | `` He could n't have been __`any nicer`__ to them , '' Woolley added .                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_25_082.9038_x1325749_44:24-27-28`** | Instead of working with a megalomaniac , though , I found him to be this gentle , soft-spoken man , and he could n't have been __`any nicer`__ .                                                                                                                                                                                                                                                       |
| **`pcc_eng_22_059.4682_x0945278_112:7-8-9`**   | Relationships with the United States were n't __`any nicer`__ either as Kim would still portray the US as the bad guy and George W. Bush referring to North Korea as part of the ' axis of evil ' .                                                                                                                                                                                                    |
| **`pcc_eng_24_028.5471_x0445389_33:62-63-64`** | After this there is some vain effort of the movie to create a Snow White type story except instead of killing the daughter the stepmother wants to kill the Prince , at which point the movie kills off all of the boyfriends and ends with a cliffhanger where the nice boy , or in this case " the boy who is n't __`any nicer`__ but looks the most like Adam Sandler " is about to kiss the girl . |
| **`pcc_eng_24_033.1236_x0519651_80:3-4-5`**    | They are n't __`any nicer`__ than the cabins we 've seen on other ships .                                                                                                                                                                                                                                                                                                                              |


7. _any easier_

|                                                | `token_str`                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_072.8917_x1163871_2:4-6-7`**     | This recipe could not be __`any easier`__ ; there 's no baking involved and it takes hardly any time to create these cute Cheesecake - Filled Chocolate Easter Eggs with a ' yolk ' made of passionfruit sauce . |
| **`pcc_eng_02_036.3409_x0572009_2:3-5-6`**     | It could n't be __`any easier`__ than using Aloha 2 GO .                                                                                                                                                         |
| **`pcc_eng_05_001.0850_x0001380_5:11-13-14`**  | After pressing , it takes minutes to make and could not be __`any easier`__ !                                                                                                                                    |
| **`nyt_eng_19961110_0020_26:3-4-5`**           | things were n't __`any easier`__ Saturday .                                                                                                                                                                      |
| **`pcc_eng_11_004.8877_x0063101_12:16-18-19`** | " It 's always difficult the deeper you go in the draw -- it wo n't be __`any easier`__ on Friday . "                                                                                                            |


8. _any good_

|                                             | `token_str`                                                                                                                                                                           |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_033.5917_x0526037_19:4-5-6`** | The Republicans are n't __`any good`__ as they do it , only to a lesser degree of waste , more to the wealthy , and less crumbs to the poor .                                         |
| **`pcc_eng_18_084.9516_x1359345_23:7-8-9`** | The top personal injury lawyer will not __`any good`__ though you would require that divorce lawyer .                                                                                 |
| **`nyt_eng_20000919_0214_24:7-8-9`**        | `` Most of them just were n't __`any good`__ . ''                                                                                                                                     |
| **`nyt_eng_20000508_0513_7:11-12-13`**      | `` We are n't going to say their rankings are n't __`any good`__ , but in many ways Kansas City would top the list , '' said Becky Blades , chairwoman of the entrepreneurs council . |
| **`apw_eng_20081220_0329_7:26-27-28`**      | but Morozov , a 21-year-old university student who 's been gunning up support for the Moscow protest on YouTube , said Russian cars just are n't __`any good`__ .                     |


9. _any higher_

|                                                | `token_str`                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_006.1175_x0082499_39:14-16-17`** | In Gall 's view , the stakes for his UFC 203 bout could not be __`any higher`__ .                                                                                                                                                  |
| **`pcc_eng_09_001.1376_x0002178_04:6-8-9`**    | The price you pay will not be __`any higher`__ than if you had not shopped here ...                                                                                                                                                |
| **`pcc_eng_19_048.2343_x0762344_13:13-15-16`** | The gesture stands out even more when public hostility toward police could n't be __`any higher`__ , reminding us that despite all the riot gear and tear gas , police departments can care about the people they serve .          |
| **`pcc_eng_17_102.5790_x1642047_08:4-5-6`**    | Food prices are n't __`any higher`__ than you 'd see in a big city like Vancouver , and in the past few years , most Northern cities have gained some large supermarkets with a very decent selection of produce and other foods . |
| **`pcc_eng_02_080.3912_x1283657_21:19-20-21`** | You want to overexpose the white background by 2/3 to 1 stop over the key light , but not __`any higher`__ .                                                                                                                       |


10. _any better_

|                                                | `token_str`                                                                                                                                                                           |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_099.3335_x1588713_06:4-5-6`**    | And things were n't __`any better`__ over in Australia either , as the pound lost out on nearly one and a half cents there .                                                          |
| **`pcc_eng_24_022.5150_x0347577_15:19-22-23`** | " So I was sat in a perfect position in third and coming down the hill it could n't have been __`any better`__ .                                                                      |
| **`pcc_eng_20_080.9865_x1292283_11:22-23-24`** | As bad as the White Sox contract with Adam Dunn has been , the contracts given to Castro and Jackson are n't __`any better`__ .                                                       |
| **`pcc_eng_01_076.1207_x1214840_08:6-7-8`**    | In truth , Dove is n't __`any better`__ than all the other highly promoted toxic beauty products .                                                                                    |
| **`pcc_eng_26_009.2111_x0132609_08:09-10-11`** | However , a source said the offer was n't __`any better`__ than one they had rejected before the start of last season , which also included a guaranteed payment of their contracts . |


11. _any simpler_

|                                                | `token_str`                                                                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_083.9536_x1341196_29:31-33-34`** | Workflow simplified Built to support the DV family of codecs , as well as the Quick Time animation codec , while using the industry standard .mov wrapper , workflow could not be __`any simpler`__ . |
| **`pcc_eng_02_094.5442_x1512577_36:3-5-6`**    | It could n't be __`any simpler`__ .                                                                                                                                                                   |
| **`nyt_eng_19961128_0003_5:23-25-26`**         | uncertainty remains about how this game will affect Robinson 's future , but for the 14 USC seniors , the predicament could not be __`any simpler`__ .                                                |
| **`pcc_eng_05_016.3328_x0248347_31:4-5-6`**    | Mainly they are not __`any simpler`__ than screens and require routine ladder maintenance .                                                                                                           |
| **`pcc_eng_01_100.1340_x1602483_03:14-16-17`** | The Lush Ice Stig is the perfect all in one device that could n't be __`any simpler`__ to use .                                                                                                       |


12. _any brighter_

|                                                | `token_str`                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_085.4477_x1364434_12:42-43-44`** | Actually , I do n't know my hippocampus from my amygdala , but it 's nice to know that all those mornings I 've sat on my butt wrestling silently with my monkey mind might actually keep me lucid -- if not __`any brighter`__ -- long into my crusty old age . |
| **`pcc_eng_27_104.5169_x1674612_34:13-15-16`** | In the biggest draft in franchise -history , the spot light will not be __`any brighter`__ than it is on the Flames organization .                                                                                                                               |
| **`pcc_eng_26_040.8483_x0644387_012:6-7-8`**   | Guess spies like him are n't __`any brighter`__ now than they were back in the 1940s !                                                                                                                                                                           |
| **`pcc_eng_19_042.2865_x0666602_11:32-33-34`** | As it stands , Black Berry is already in the red , losing as much as US $ 84 million in the last quarter ; the prediction for the next is n't __`any brighter`__ at this point .                                                                                 |
| **`pcc_eng_29_093.1157_x1487984_25:1-5-6`**    | Nor is the picture __`any brighter`__ in Scottish retail .                                                                                                                                                                                                       |


13. _any worse_

|                                                | `token_str`                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_002.2781_x0020694_074:5-6-7`**   | Besides , it 's not __`any worse`__ than anything Motormaster 's done to me , Drag Strip rationalized , letting Smokescreen deepen the kiss .                                                                                                      |
| **`pcc_eng_04_070.0570_x1115376_09:3-5-6`**    | He ca n't be __`any worse`__ than douglas .                                                                                                                                                                                                        |
| **`pcc_eng_01_031.4085_x0491448_10:26-28-29`** | If there 's any positive for Von D , it 's that the embarrassment from having everyone watch her gush over her old boyfriend ca n't be __`any worse`__ than the embarrassment of having been involved with noted philanderer James to begin with . |
| **`pcc_eng_08_073.9026_x1180369_40:4-5-6`**    | Brett Favre is n't __`any worse`__ than Tony Romo which means that Donald Driver should have a monster game and Big Blue will be 0 - 2 .                                                                                                           |
| **`pcc_eng_12_039.2453_x0618572_056:1-7-8`**   | Nothing he came up with was __`any worse`__ than what she had already endured at the hands of vampires .                                                                                                                                           |


14. _any closer_

|                                                | `token_str`                                                                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_034.0300_x0535048_09:3-6-7`**    | We could n't have been __`any closer`__ .                                                                                                                              |
| **`pcc_eng_18_085.2344_x1363893_45:4-6-7`**    | We really could n't be __`any closer`__ , and thinking of a quick 4 hour drive to go see my nephew on the weekends has me doing the never ending happy dance .         |
| **`pcc_eng_10_088.8470_x1419911_074:4-5-6`**   | And I was n't __`any closer`__ to coming out . "                                                                                                                       |
| **`pcc_eng_26_004.8324_x0061787_02:22-23-24`** | NASA has released stunning new views of those mysterious bright spots on the dwarf planet Ceres - but we 're still not __`any closer`__ to working out what they are . |
| **`pcc_eng_11_097.4880_x1561973_10:09-11-12`** | By which I mean I 'm not pregnant nor really __`any closer`__ to being pregnant .                                                                                      |


15. _any smarter_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_094.8222_x1516469_0949:4-5-6`**   | " You 're not __`any smarter`__ though , " He -man moved in .                                                                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_17_071.0559_x1131909_25:3-4-5`**     | I 'm not __`any smarter`__ than they are , but I 'm real confident that , if it 's there , we can find it . "                                                                                                                                                                                                                                                                                                |
| **`pcc_eng_08_046.5222_x0736880_117:20-21-22`** | By the way , Jason Werth 's contract is more proof that some major league general manager 's are n't __`any smarter`__ than your middle - of- the - road fantasy baseballer .                                                                                                                                                                                                                                |
| **`pcc_eng_14_005.3539_x0070580_03:5-6-7`**     | Since I 'm probably not __`any smarter`__ than most of the people reading this column , I need to make sure I supply my readers with information that in one way or another is either uplifting , insightful to some degree , encouraging , entertaining , helpful in some way or emotionally stirring , bringing either a little lump to your throat or a little laugh or snicker ( or at least a smile ) . |
| **`pcc_eng_21_076.6557_x1222627_27:5-6-7`**     | The people highlighted are n't __`any smarter`__ or more capable than the rest of us .                                                                                                                                                                                                                                                                                                                       |


16. _any cheaper_

|                                                 | `token_str`                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_093.8012_x1499423_09:3-7-8`**     | It 's not like driving is __`any cheaper`__ .                                                                                                                       |
| **`pcc_eng_06_077.2619_x1233397_10:25-27-28`**  | If you are going to be setting up in photo restoration or trying it out for a hobby or whatever , Adobe Photoshop could not be __`any cheaper`__ right now . .      |
| **`pcc_eng_09_037.1937_x0585879_09:17-18-19`**  | So it actually required way more planning than buying pre-made organic juice -- and it was n't __`any cheaper`__ .                                                  |
| **`pcc_eng_20_007.7186_x0108344_112:3-4-5`**    | Prices were n't __`any cheaper`__ ( but also not much more expensive -- not always true in Canada ) , but the shipping was way less .                               |
| **`pcc_eng_22_055.2254_x0876246_041:26-27-28`** | This is because it is usually packed with NYU students who , one can only assume , do n't know any better because it is n't __`any cheaper`__ than the good stuff . |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/...

Samples saved as...
1. `neg_bigram_examples/any/any_younger_99ex.csv`
1. `neg_bigram_examples/any/any_clearer_99ex.csv`
1. `neg_bigram_examples/any/any_happier_99ex.csv`
1. `neg_bigram_examples/any/any_different_99ex.csv`
1. `neg_bigram_examples/any/any_bigger_99ex.csv`
1. `neg_bigram_examples/any/any_nicer_99ex.csv`
1. `neg_bigram_examples/any/any_easier_99ex.csv`
1. `neg_bigram_examples/any/any_good_99ex.csv`
1. `neg_bigram_examples/any/any_higher_99ex.csv`
1. `neg_bigram_examples/any/any_better_99ex.csv`
1. `neg_bigram_examples/any/any_simpler_99ex.csv`
1. `neg_bigram_examples/any/any_brighter_99ex.csv`
1. `neg_bigram_examples/any/any_worse_99ex.csv`
1. `neg_bigram_examples/any/any_closer_99ex.csv`
1. `neg_bigram_examples/any/any_smarter_99ex.csv`
1. `neg_bigram_examples/any/any_cheaper_99ex.csv`

## 5. *remotely*

|                      |        `N` |      `f1` |   `adv_total` |
|:---------------------|-----------:|----------:|--------------:|
| **NEGATED_remotely** | 72,839,589 | 3,173,660 |        16,426 |
| **NEGMIR_remotely**  |  1,701,929 |   291,732 |         2,341 |


|                                 |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:--------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGany~remotely_surprising**  |    75 |        70,540 |    0.85 |    5.07 |   413.61 |      3.66 |       71.34 |     84 |
| **NEGmir~remotely_believable**  |    21 |           600 |    0.83 |    1.96 |    74.08 |      3.60 |       17.40 |     21 |
| **NEGmir~remotely_surprising**  |    17 |         2,662 |    0.83 |    1.50 |    59.97 |      2.91 |       14.09 |     17 |
| **NEGmir~remotely_comparable**  |    44 |           283 |    0.76 |    2.72 |   134.02 |      8.06 |       35.94 |     47 |
| **NEGmir~remotely_true**        |    61 |         6,191 |    0.75 |    3.04 |   181.65 |     11.31 |       49.69 |     66 |
| **NEGany~remotely_ready**       |    58 |       141,590 |    0.74 |    4.16 |   287.63 |      3.22 |       54.78 |     74 |
| **NEGmir~remotely_new**         |    19 |        12,836 |    0.69 |    1.00 |    50.62 |      3.77 |       15.23 |     22 |
| **NEGmir~remotely_close**       |   218 |        13,874 |    0.65 |    3.28 |   532.96 |     45.77 |      172.23 |    267 |
| **NEGany~remotely_true**        |   250 |       231,639 |    0.63 |    4.61 | 1,111.13 |     16.12 |      233.88 |    370 |
| **NEGmir~remotely_funny**       |    41 |         5,365 |    0.63 |    1.85 |    97.91 |      8.74 |       32.26 |     51 |
| **NEGany~remotely_funny**       |   137 |       122,927 |    0.60 |    4.15 |   589.74 |      9.24 |      127.76 |    212 |
| **NEGmir~remotely_interesting** |    56 |        12,447 |    0.56 |    1.80 |   115.20 |     13.20 |       42.80 |     77 |
| **NEGmir~remotely_possible**    |    38 |         3,160 |    0.56 |    1.42 |    78.73 |      8.91 |       29.09 |     52 |
| **NEGany~remotely_qualified**   |    57 |        74,643 |    0.52 |    3.13 |   222.79 |      4.40 |       52.60 |    101 |
| **NEGmir~remotely_similar**     |    71 |         7,011 |    0.49 |    1.70 |   127.32 |     18.34 |       52.66 |    107 |
| **NEGany~remotely_close**       |   694 |       411,329 |    0.39 |    3.65 | 2,243.22 |     69.58 |      624.42 |  1,597 |
| **NEGany~remotely_comparable**  |   118 |        12,252 |    0.38 |    2.98 |   375.73 |     12.07 |      105.93 |    277 |
| **NEGany~remotely_accurate**    |    50 |       152,299 |    0.33 |    2.10 |   143.78 |      5.84 |       44.16 |    134 |
| **NEGany~remotely_interested**  |   330 |       264,528 |    0.27 |    2.74 |   817.06 |     46.27 |      283.73 |  1,062 |
| **NEGany~remotely_similar**     |   152 |       203,453 |    0.23 |    2.20 |   334.61 |     24.36 |      127.64 |    559 |


1. _remotely surprising_

|                                                 | `token_str`                                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_085.4518_x1364936_020:24-25-26`** | Naturally , the reaction of President Donald J Trump to the latest atrocity was appalling , but , to anyone paying attention , not __`remotely surprising`__ .                                                                                                                      |
| **`pcc_eng_19_049.0450_x0775511_054:11-12-13`** | Starbound tries its hand at so much that it 's not __`remotely surprising`__ to see it dabbling in Metroidvania -style dungeons , as well .                                                                                                                                         |
| **`pcc_eng_test_1.1025_x01663_17:5-7-8`**       | The murder victim was n't even __`remotely surprising`__ nor was the murderer .                                                                                                                                                                                                     |
| **`pcc_eng_04_104.5051_x1672075_28:27-29-30`**  | There is no reason to celebrate Griner 's actions , but given our society 's obsession with sports , dominance , and aggression , it should n't be __`remotely surprising`__ that women entering into a male-dominated space will begin to measure their success in similar forms . |
| **`pcc_eng_24_087.1076_x1392625_05:14-16-17`**  | Well this is the talk of the office this morning , which is n't even __`remotely surprising`__ .                                                                                                                                                                                    |


2. _remotely believable_

|                                                | `token_str`                                                                                                                                                    |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_005.6855_x0075896_21:08-09-10`** | Is very boring , nothing unexpected and nothing __`remotely believable`__ .                                                                                    |
| **`nyt_eng_20050708_0167_69:16-18-19`**        | do n't try to shill for the GXP and the Impala , it 's just not even __`remotely believable`__ . ''                                                            |
| **`pcc_eng_03_032.9083_x0516822_21:13-18-19`** | There 's not much of a payoff at the end of , nor is the trial itself __`remotely believable`__ .                                                              |
| **`nyt_eng_19970623_0561_27:01-10-11`**        | none of this , needless to say , is __`remotely believable`__ _ nor is the apocalyptic ending that reunites the demented Devi with her alleged birth parents . |
| **`pcc_eng_00_062.0217_x0986499_27:3-5-6`**    | He 's not even __`remotely believable`__ as a legitimate " pundit " , there 's something so undeniably CRAZY about his thinking .                              |


3. _remotely comparable_

|                                                | `token_str`                                                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_016.2618_x0246224_090:3-4-5`**   | There is nothing __`remotely comparable`__ to Soviet-style government censorship and yet we have deliberate suppression of dissent .                                                                                                                         |
| **`pcc_eng_19_076.4855_x1219477_06:22-25-26`** | " Even now when you think about it in comparison to other events we 've had , summer and winter , nothing is even __`remotely comparable`__ to that event , " says Goldman .                                                                                 |
| **`pcc_eng_07_060.8241_x0967067_3:11-12-13`**  | Yes , yes , I know , the cases are not __`remotely comparable`__ .                                                                                                                                                                                           |
| **`pcc_eng_27_030.9843_x0483881_020:1-7-8`**   | Nothing on the present horizon is __`remotely comparable`__ to that .                                                                                                                                                                                        |
| **`pcc_eng_10_075.9474_x1211333_71:4-5-6`**    | " That is not __`remotely comparable`__ to the 5 million Syrians who fled the country in the first five years following the civil war - and that does n't include over a million per year who fled their homes inside Syria ( the internally displaced ) . " |


4. _remotely true_

|                                                 | `token_str`                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_004.9132_x0063132_2:4-5-6`**      | " It is not __`remotely true`__ that we are interested in Lichtsteiner , " he said in a press conference on the eve of their trip to Ajaccio on Friday .                                                                                                     |
| **`pcc_eng_14_083.4163_x1332170_29:3-4-5`**     | That 's not __`remotely true`__ ( we 're not even a paper ) , but even if it were , how does that refute our criticisms ?                                                                                                                                    |
| **`pcc_eng_13_007.1987_x0099976_12:44-45-46`**  | To begin , one must understand that while we often talk about abortion as though the issue is defined by a line running down the center of the American electorate , liberals on one side and conservatives on the other , that 's not __`remotely true`__ . |
| **`pcc_eng_29_044.1278_x0696845_097:09-10-11`** | This is only a manner of speaking and not __`remotely true`__ .                                                                                                                                                                                              |
| **`pcc_eng_20_006.3181_x0085665_11:10-11-12`**  | This is a lovely sentiment , but it 's not __`remotely true`__ .                                                                                                                                                                                             |


5. _remotely ready_

|                                                 | `token_str`                                                                                                                                                                                  |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19980427_0151_37:08-09-10`**         | Mark had finally confessed : He was n't __`remotely ready`__ to be a father .                                                                                                                |
| **`pcc_eng_07_017.0566_x0259758_096:11-13-14`** | I had been married less than a year and was n't even __`remotely ready`__ for kids .                                                                                                         |
| **`pcc_eng_19_075.9751_x1211201_07:11-12-13`**  | ' but if she 's dating a guy who 's not __`remotely ready`__ for children cougars reveal what it 's really like to date have you been pronouncing versace wrong .                            |
| **`pcc_eng_06_102.9020_x1648488_117:3-4-5`**    | I 'm not __`remotely ready`__ to talk about how to talk with kids about sex .                                                                                                                |
| **`pcc_eng_29_081.7315_x1304011_24:10-11-12`**  | He has to make peace with something he was n't __`remotely ready`__ to tackle , forced out of his shell to engage in a conflict sweeping the rest of the world whether he wanted to or not . |


6. _remotely new_

|                                                | `token_str`                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_005.0515_x0065815_13:3-4-5`**    | This is n't __`remotely new`__ .                                                                                                                                                                                                                                                          |
| **`pcc_eng_25_099.4991_x1593996_18:4-5-6`**    | But there 's nothing __`remotely new`__ in this book beyond Wilson 's anti-Darwin bias .                                                                                                                                                                                                  |
| **`pcc_eng_16_058.5534_x0931869_15:14-16-17`** | For something the brand totes as " radically new , " there 's nothing even __`remotely new`__ about it .                                                                                                                                                                                  |
| **`pcc_eng_02_008.7063_x0124311_18:32-33-34`** | Teri Meherbaniyan is one of Jackie 's few solo hits and even then the trade openly talked about the dog outdoing him . :) But to be fair , there is nothing __`remotely new`__ or different in the film except for the title song .                                                       |
| **`pcc_eng_24_096.9629_x1552196_16:6-8-9`**    | The main narrative arc is not even __`remotely new`__ : boy goes from rags to riches , meets girl , break - up happens , he repurposes his life and finally wins the girl and a fortune with his special snowflake abilities , while he destroys the most evil big company in the world . |


7. _remotely close_

|                                                | `token_str`                                                                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_008.8463_x0126923_17:17-18-19`** | So when we consider the purchasing power of the dollar , then our stock portfolio was n't __`remotely close`__ to flat , but rather had dropped by a staggering 70 % in fourteen years , from 919 to 274 . |
| **`pcc_eng_03_006.5670_x0089989_343:2-3-4`**   | Definitely nothing __`remotely close`__ to a blue .                                                                                                                                                        |
| **`pcc_eng_16_057.8963_x0921105_09:1-2-3`**    | Not __`remotely close`__ to being a bully .                                                                                                                                                                |
| **`pcc_eng_03_092.2383_x1477352_42:3-4-5`**    | This is n't __`remotely close`__ to what Reid claimed .                                                                                                                                                    |
| **`pcc_eng_14_087.1146_x1391904_29:3-5-6`**    | It 's not even __`remotely close`__ in terms of how many cards , and how many major power shifts , are allocated to dice rolls vs skillful play .                                                          |


8. _remotely funny_

|                                                | `token_str`                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_057.0140_x0905249_14:12-14-15`** | And then let 's show that they 're not jokes , not even __`remotely funny`__ , as the Dalek cleanly and efficiently slaughters everyone in sight .                                                                                                 |
| **`pcc_eng_07_021.7718_x0336046_36:14-15-16`** | It 's common , its happened to people you know , and its not __`remotely funny`__ .                                                                                                                                                                |
| **`pcc_eng_14_088.5429_x1415038_07:18-22-23`** | Some of this sounds funny in writing , but thanks to witless execution and sloppy writing , none of it is __`remotely funny`__ on-screen .                                                                                                         |
| **`pcc_eng_07_055.6848_x0883912_10:22-23-24`** | They 're good for so many things , from venting and sorting feelings and seeing the humor in situations that are not __`remotely funny`__ in the moment , to tracking where you 've been and of course for assessing what worked and what didn't . |
| **`pcc_eng_27_063.1531_x1004836_23:08-10-11`** | That 's disturbing , disgusting , and not even __`remotely funny`__ .                                                                                                                                                                              |


9. _remotely possible_

|                                                 | `token_str`                                                                                                                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_19971211_1274_20:16-18-19`**         | some ten years ago , many of us would have probably thought that this would not be __`remotely possible`__ .                                                                                                                                              |
| **`pcc_eng_16_055.7032_x0885357_51:3-5-6`**     | It 's not even __`remotely possible`__ that all inequality everywhere is due to the extension of patents and copyrights since 1981 .                                                                                                                      |
| **`pcc_eng_00_038.3633_x0603535_019:18-28-29`** | It 's not that we find ourselves in three wars and ca n't really understand why , not to mention if any sort of victory is even __`remotely possible`__ .                                                                                                 |
| **`pcc_eng_28_013.0626_x0195370_075:3-4-5`**    | This is not __`remotely possible`__ all the time , but you want to do it as much as possible .                                                                                                                                                            |
| **`apw_eng_20090511_1244_28:43-44-45`**         | `` The odds that you have Nazi wartime documents that put him at Sobibor , that former guards remember him and that he writes that he lived in Sobibor -- that he did n't serve at the death camp ? It 's not __`remotely possible`__ , '' Drimmer said . |


10. _remotely interesting_

|                                                 | `token_str`                                                                                                                                                                                                                                                       |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_011.1614_x0164316_12:1-5-6`**     | None of them were __`remotely interesting`__ .                                                                                                                                                                                                                    |
| **`pcc_eng_18_088.1871_x1411945_23:07-13-14`**  | If you 're like me , none of the above is even __`remotely interesting`__ except for the fact that it would likely prolong the ordeal , push the date of the next tip-off even further in the future , and roll our eyeballs even further back in their sockets . |
| **`pcc_eng_03_086.6062_x1386237_076:23-28-29`** | She tells her story through the eyes of half a dozen characters , all of whom speak in the same voice , none of whom are even __`remotely interesting`__ or convincing as human beings .                                                                          |
| **`pcc_eng_20_006.6013_x0090234_138:23-25-26`** | It is to be said however , that the introductory essay is too long , drawn out and in my opinion , not even __`remotely interesting`__ .                                                                                                                          |
| **`pcc_eng_07_027.7698_x0432922_3:10-12-13`**   | Vocally it 's woeful and depressing and there is nothing even __`remotely interesting`__ or enjoyable about any song on this crap album .                                                                                                                         |


11. _remotely qualified_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                           |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_032.1435_x0502836_4:11-12-13`**   | My German is well below GCSE standard so I 'm not __`remotely qualified`__ to read the Ph D thesis in question , but nevertheless I 'm taken with the way that Der Spiegel has made elements of the document available on the web , along with sources , so that you can see the offending passages . |
| **`pcc_eng_25_085.2826_x1364049_17:22-25-26`**  | " The Skeleton Twins " can best be described as : two dysfunctional siblings telling one another how to live when neither is even __`remotely qualified`__ to give such advice .                                                                                                                      |
| **`pcc_eng_15_092.7806_x1483434_28:4-6-7`**     | If you are not even __`remotely qualified`__ for a position , do n't apply .                                                                                                                                                                                                                          |
| **`pcc_eng_03_037.9436_x0598305_32:27-28-29`**  | In the back of your mind , you constantly worry that every single parenting choice you 've made has been wrong , and that you are n't __`remotely qualified`__ for this business of raising young people .                                                                                            |
| **`pcc_eng_12_086.2209_x1377012_072:07-10-11`** | I 'm not a doctor , nor am I __`remotely qualified`__ to draw a conclusion .                                                                                                                                                                                                                          |


12. _remotely similar_

|                                                | `token_str`                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19990924_0222_26:5-6-7`**           | Kentucky 's offense is not __`remotely similar`__ to Tennessee 's .                                                                                                                                                                |
| **`nyt_eng_20000218_0186_47:1-2-3`**           | nothing __`remotely similar`__ went on at Paul Smith 's show Monday night .                                                                                                                                                        |
| **`pcc_eng_28_072.1910_x1151592_48:27-28-29`** | " Little Red Riding Hood " was almost certainly original , because earlier versions have not been recorded or do not seem to exist , and nothing __`remotely similar`__ can be found in older literature . [ 8 ]                   |
| **`pcc_eng_06_078.4987_x1253180_06:3-4-5`**    | There 's nothing __`remotely similar`__ .                                                                                                                                                                                          |
| **`pcc_eng_08_072.3153_x1154676_187:4-5-6`**   | My pace is n't __`remotely similar`__ to what it usually is , but it 's hard to judge ; I think I 've passed the border and entered New Jersey for over an hour when I finally reach the well - marked border -- as it should be ! |


13. _remotely accurate_

|                                                 | `token_str`                                                                                                                                                                                                                           |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_104.8274_x1681193_10:40-42-43`**  | A total smear to be sure , with its share of distortion , but still a concise biography of a man who has used a cozy relationship with the media to win popular support around a biography that 's not even __`remotely accurate`__ . |
| **`pcc_eng_11_081.2101_x1298323_42:1-4-5`**     | Nor is it __`remotely accurate`__ to state that " low - wage workers , schools , parents and advocates for the sick and disabled " do not enjoy a " level playing field " .                                                           |
| **`pcc_eng_21_104.5778_x1673867_36:3-4-5`**     | Again , not __`remotely accurate`__ .                                                                                                                                                                                                 |
| **`pcc_eng_16_058.3752_x0928899_07:3-5-6`**     | It 's not even __`remotely accurate`__ regarding the Numbers .                                                                                                                                                                        |
| **`pcc_eng_10_019.7965_x0303782_016:22-24-25`** | Thus Easterbrook 's claim that the IPCC TAR projected a 1 deg C global surface warming from 2000 to 2010 was not even __`remotely accurate`__ .                                                                                       |


14. _remotely interested_

|                                                | `token_str`                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_034.5954_x0544236_24:41-42-43`** | In an era when foreign policy debate has in most Western countries disappeared altogether , replaced by the reality TV of political entertainment , all of these things are much harder to explain and justify to a public that is n't __`remotely interested`__ . |
| **`nyt_eng_20000524_0257_10:1-4-5`**           | nor were they __`remotely interested`__ in `` democracy , '' in the way that their contemporaries , the veterans of Tiananmen Square , might define it .                                                                                                           |
| **`pcc_eng_00_035.9661_x0564825_07:07-13-14`** | And to his great distress , neither of Henry 's sons are __`remotely interested`__ in carrying on the family business .                                                                                                                                            |
| **`nyt_eng_20060127_0146_8:5-6-7`**            | `` But I was n't __`remotely interested`__ in what they 'd done . ''                                                                                                                                                                                               |
| **`pcc_eng_03_088.7082_x1420362_22:24-25-26`** | It was a manly night out , which means we get stupid by drinking too much , and smile at women that are n't __`remotely interested`__ in us .                                                                                                                      |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/...

Samples saved as...
1. `neg_bigram_examples/remotely/remotely_surprising_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_believable_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_comparable_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_true_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_ready_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_new_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_close_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_funny_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_possible_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_interesting_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_qualified_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_similar_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_accurate_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_interested_99ex.csv`

## 6. *ever*

|                     |        `N` |       `f1` |   `adv_total` |
|:--------------------|-----------:|-----------:|--------------:|
| **NEGMIR_ever**     |  1,701,929 |    291,732 |         5,060 |
| **NEGATED_ever**    | 72,839,589 |  3,173,660 |       114,075 |
| **COMPLEMENT_ever** | 72,839,589 | 69,662,736 |       114,075 |


|                           |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:--------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGmir~ever_easy**      |   368 |        18,610 |    0.83 |    6.44 | 1,285.01 |     63.25 |      304.75 |    369 |
| **NEGmir~ever_simple**    |   206 |        25,408 |    0.83 |    5.82 |   726.76 |     35.31 |      170.69 |    206 |
| **NEGmir~ever_enough**    |   147 |         2,596 |    0.83 |    5.30 |   518.58 |     25.20 |      121.80 |    147 |
| **NEGmir~ever_certain**   |   143 |         1,800 |    0.83 |    5.26 |   504.47 |     24.51 |      118.49 |    143 |
| **NEGmir~ever_boring**    |    57 |         1,961 |    0.83 |    3.80 |   201.07 |      9.77 |       47.23 |     57 |
| **NEGmir~ever_black**     |    56 |         1,412 |    0.83 |    3.77 |   197.54 |      9.60 |       46.40 |     56 |
| **NEGmir~ever_sick**      |    39 |         1,895 |    0.83 |    3.15 |   137.57 |      6.69 |       32.31 |     39 |
| **NEGmir~ever_good**      |   299 |        31,585 |    0.82 |    5.68 | 1,013.87 |     51.94 |      247.06 |    303 |
| **NEGmir~ever_perfect**   |   206 |         3,134 |    0.82 |    5.57 |   714.47 |     35.48 |      170.52 |    207 |
| **NEGany~ever_simple**    |   211 |       396,749 |    0.80 |    5.56 | 1,109.28 |     10.89 |      200.11 |    250 |
| **NEGmir~ever_able**      |   136 |         3,704 |    0.78 |    4.17 |   426.52 |     24.51 |      111.49 |    143 |
| **NEGany~ever_boring**    |    72 |        45,891 |    0.76 |    4.46 |   362.74 |      3.92 |       68.08 |     90 |
| **NEGany~ever_easy**      |   429 |       579,827 |    0.73 |    5.41 | 2,105.13 |     24.18 |      404.82 |    555 |
| **NEGany~ever_certain**   |   147 |        74,952 |    0.72 |    4.80 |   713.34 |      8.41 |      138.59 |    193 |
| **NEGany~ever_sure**      |    87 |       262,825 |    0.49 |    3.34 |   328.20 |      7.06 |       79.94 |    162 |
| **NEGany~ever_good**      |   331 |     1,681,795 |    0.46 |    3.81 | 1,188.69 |     28.76 |      302.24 |    660 |
| **NEGany~ever_enough**    |   173 |       152,020 |    0.45 |    3.54 |   618.62 |     15.12 |      157.88 |    347 |
| **NEGany~ever_perfect**   |   216 |       104,659 |    0.40 |    3.34 |   706.71 |     21.31 |      194.69 |    489 |
| **NEGany~ever_satisfied** |    64 |        62,862 |    0.38 |    2.57 |   203.01 |      6.58 |       57.42 |    151 |
| **COM~ever_closer**       | 6,305 |        61,475 |    0.04 |    3.51 |   538.66 |  6,031.92 |      273.08 |  6,307 |


1. _ever simple_

|                                                | `token_str`                                                                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_val_3.04586_x42025_16:3-7-8`**      | Historically , nothing about me is __`ever simple`__ or normal ( medically and otherwise ) .                                                                             |
| **`pcc_eng_23_039.3333_x0619416_06:29-31-32`** | First , some people have asked me for the cite on the Harper Collins publicity document I copied to my post of February 9th , With ARod , Nothing is __`Ever Simple`__ . |
| **`pcc_eng_11_083.1163_x1329077_21:23-25-26`** | In other words , even if we genuinely love someone , the realities of life have a way of reminding us that nothing is __`ever simple`__ ...                              |
| **`pcc_eng_06_102.2958_x1638582_01:4-6-7`**    | But of course nothing is __`ever simple`__ when bringing together national statistics .                                                                                  |
| **`pcc_eng_04_101.3371_x1621013_23:1-3-4`**    | Nothing is __`ever simple`__ and reality tends to be inconvenient .                                                                                                      |


2. _ever enough_

|                                                | `token_str`                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_006.0539_x0082006_15:1-7-8`**    | Nothing the writer can do is __`ever enough`__ .                                                                                                                                                                                                                 |
| **`pcc_eng_17_054.6155_x0866250_19:1-5-6`**    | Nothing I do is __`ever enough`__ to be excellent .                                                                                                                                                                                                              |
| **`pcc_eng_22_001.1797_x0002899_09:30-32-33`** | As I 've grown up it 's never left me , and has been poured into various projects , characters and creations but I 've never been satisfied , nothing was __`ever enough`__ and I always knew I could do more .                                                  |
| **`pcc_eng_18_084.5124_x1352360_034:2-4-5`**   | But nothing was __`ever enough`__ for him .                                                                                                                                                                                                                      |
| **`pcc_eng_11_085.3045_x1364599_50:48-50-51`** | Over the next few weeks , my little sister and I struggled to find closure by trying to remember him , getting a memorial tattoo , making a wreath for his grave on Memorial Day , using his t-shirts to make a quilt , but it 's not really __`ever enough`__ . |


3. _ever certain_

|                                                | `token_str`                                                                                                                                                                                     |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_078.9703_x1261259_11:07-09-10`** | But Ferguson knows from experience that nothing is __`ever certain`__ in football .                                                                                                             |
| **`pcc_eng_20_005.7871_x0077117_16:29-31-32`** | I have not wanted to write an update until things were absolutely certain , but I am afraid that our life thus far has proven to us that nothing is __`ever certain`__ until after it happens . |
| **`pcc_eng_20_009.0011_x0129103_26:23-25-26`** | Advancing any view or judgement is a no-no in the evidence - based research sphere , founded on the cardinal acceptance that nothing is __`ever certain`__ .                                    |
| **`pcc_eng_17_077.6713_x1238971_07:2-4-5`**    | While nothing is __`ever certain`__ in MMA , you can bet on fireworks when these two heavy handed fighters meet inside the O-Zone .                                                             |
| **`pcc_eng_27_058.7436_x0933359_11:1-3-4`**    | Nothing is __`ever certain`__ of course but , the more information the better if needing to profile an account reasonably quickly                                                               |


4. _ever boring_

|                                                 | `token_str`                                                                                                                                                                                                                               |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_006.3227_x0086059_152:15-17-18`** | " Sister " is special in that it is pensive and character - based without being __`ever boring`__ and it evokes deep emotions , yet is subjective and stays away from gooey sentimentality or blatant attempts at audience manipulation . |
| **`pcc_eng_27_064.0342_x1018997_06:6-8-9`**     | Above all , it was never , __`ever boring`__ .                                                                                                                                                                                            |
| **`pcc_eng_25_013.0080_x0194233_49:2-4-5`**     | Was n't it __`ever boring`__ to play the same five concertos for three years ?                                                                                                                                                            |
| **`pcc_eng_15_012.6522_x0188059_12:18-20-21`**  | It 's a show that goes for broke , does not apologize for its excesses and is never , __`ever boring`__ .                                                                                                                                 |
| **`pcc_eng_25_004.8609_x0062975_07:1-3-4`**     | Nothing is __`EVER boring`__ with me around ...                                                                                                                                                                                           |


5. _ever black_

|                                                | `token_str`                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_052.8855_x0839845_08:03-15-16`** | However , nothing in politics , even when it comes to science , is __`ever black`__ and white .                                                       |
| **`pcc_eng_20_007.5800_x0106044_019:1-3-4`**   | Nothing is __`ever black`__ and white but this issue may hold the answer to the more fundamental question of - " What is school there for ? "         |
| **`pcc_eng_17_040.7624_x0642478_03:15-17-18`** | It 's a slightly surreal video that I hope encapsulates my philosophy of ' Nothing is __`ever black`__ and white ' .                                  |
| **`pcc_eng_22_058.3271_x0926728_09:18-20-21`** | But Trevor is about to discover that good and evil can look a lot alike , and nothing is __`ever black`__ and white -- not even the truth .           |
| **`pcc_eng_27_104.5460_x1675091_08:18-20-21`** | If I 've learnt anything in my twenty six years on the planet , it 's that nothing is __`ever black`__ and white ; there 's infinite shades of grey . |


6. _ever sick_

|                                                 | `token_str`                                                                                                                                         |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_035.7019_x0560528_13:7-8-9`**     | Maybe that 's why I 'm hardly __`ever sick`__ : I sleep as if I were sick ?                                                                         |
| **`pcc_eng_05_088.8188_x1420621_26:3-4-5`**     | J is hardly __`ever sick`__ & i'm quite sure it 's because he washes his hands so much !                                                            |
| **`pcc_eng_00_008.5074_x0121195_15:3-4-5`**     | I was n't __`ever sick`__ or dizzy or did I ever experience anything other than neck and head pain which I was able to control with pain medicine . |
| **`pcc_eng_07_016.3556_x0248479_10:3-4-5`**     | He 's hardly __`ever sick`__ .                                                                                                                      |
| **`pcc_eng_07_024.1556_x0374360_127:12-13-14`** | Compared to back then , I am healthy , happy and hardly __`ever sick`__ !                                                                           |


7. _ever easy_

|                                                | `token_str`                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_055.1090_x0874381_12:12-14-15`** | This should n't be close , but as we know , nothing is __`ever easy`__ on the road .                                                          |
| **`pcc_eng_26_043.8679_x0693271_068:4-6-7`**   | Of course , nothing is __`ever easy`__ .                                                                                                      |
| **`pcc_eng_10_021.1137_x0324997_6:2-4-5`**     | But nothing is __`ever easy`__ in Walford ...                                                                                                 |
| **`pcc_eng_25_009.1004_x0131262_09:12-16-17`** | But recruiting has not been a strength of Kill 's ( not that it 's __`ever easy`__ with juggernauts Ohio State and Michigan in the league ) . |
| **`pcc_eng_14_096.3493_x1541510_025:1-3-4`**   | Nothing 's __`ever easy`__ ...                                                                                                                |


8. _ever perfect_

|                                                 | `token_str`                                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_011.9795_x0177767_095:30-31-32`** | You should always bulk that you are frequently and if that ending you are with , how old is stephen curry wife see nor character your sensitivity , do not __`ever perfect`__ yourself to be performed by merely being made a forcible .                                                 |
| **`pcc_eng_12_001.9586_x0015463_41:1-3-4`**     | Nothing is __`ever perfect`__ .                                                                                                                                                                                                                                                          |
| **`pcc_eng_19_074.8831_x1193534_066:2-6-7`**    | Well none of us is __`ever perfect`__ , and I know I still have negative thoughts and still have a long road to travel until I can say I can do real honour to the name ' Dreamwalker , and I know like you , we may forever pull ourselves up for making the same mistakes over again . |
| **`pcc_eng_29_006.4774_x0088640_028:2-4-5`**    | " Nothing is __`ever perfect`__ , " he always says .                                                                                                                                                                                                                                     |
| **`pcc_eng_03_095.2298_x1525666_39:2-4-5`**     | " Nothing is __`ever perfect`__ and I learned that last year when I felt perfect , " Williams said .                                                                                                                                                                                     |


9. _ever good_

|                                                 | `token_str`                                                                                                                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_013.4479_x0201674_101:3-5-6`**    | " Because nothing IS __`ever good`__ enough .                                                                                                                                                          |
| **`pcc_eng_27_065.5556_x1043570_150:12-14-15`** | The one thing that I 'm trying to embrace is that nothing is __`ever good`__ or bad .                                                                                                                  |
| **`pcc_eng_29_093.6824_x1497235_095:4-6-7`**    | Perfectionistic tendencies ; nothing is __`ever good`__ enough                                                                                                                                         |
| **`pcc_eng_09_007.9027_x0111868_107:32-34-35`** | Rousseau , for example , argued for the " ideal parent " , rational and complete - but his opponent Madame d'Epiney said that this " parent machine " ensures that nothing is __`ever good`__ enough . |
| **`pcc_eng_19_049.1285_x0776862_15:07-09-10`**  | Hope says she keeps trying but nothing 's __`ever good`__ enough .                                                                                                                                     |


10. _ever able_

|                                                 | `token_str`                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_047.5556_x0753258_094:10-11-12`** | I used to lament to him how I was n't __`ever able`__ to go back to Yankee Stadium after Thurman 's death .                                                                                                |
| **`pcc_eng_20_035.4087_x0556188_02:29-31-32`**  | A new CONAN movie has been in the works for some time with a number of people involved including the Wachowskis , John Milius and Robert Rodriguez but nothing was __`ever able`__ to get off the ground . |
| **`pcc_eng_14_085.9252_x1372749_17:23-25-26`**  | Artists are out there making and creating , many of them eager to share and talk about their work , but very few are __`ever able`__ to break into the high stakes art industry .                          |
| **`pcc_eng_13_088.0162_x1406374_036:08-09-10`** | So there was a neighbour who was hardly __`ever able`__ to accept a gift , for example some fruits from the garden .                                                                                       |
| **`pcc_eng_06_107.0901_x1716183_092:1-8-9`**    | Not even the greatest Aelfan wizards were __`ever able`__ to accomplish such a feat .                                                                                                                      |


11. _ever sure_

|                                                 | `token_str`                                                                                                                                                                                                                                           |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_079.6883_x1271238_31:08-09-10`**  | This is a blog post I was n't __`ever sure`__ I 'd write .                                                                                                                                                                                            |
| **`pcc_eng_29_084.0472_x1341322_29:14-15-16`**  | Normally I would refrain from telling her who was coming because I was not __`ever sure`__ who would really show up for her .                                                                                                                         |
| **`pcc_eng_18_030.8542_x0483214_049:30-31-32`** | I was so steeped in scarcity that I never EVER paid full price for anything , so I always ended up with 5 shirts on clearance that I was n't __`ever sure`__ I liked but thought I needed because my other shirts were getting too old or too small . |
| **`pcc_eng_25_081.5103_x1303404_15:16-18-19`**  | When the wind sweeps in , you know which way it is blowing , but no is __`ever sure`__ where it rose .                                                                                                                                                |
| **`pcc_eng_26_005.3020_x0069318_63:4-5-6`**     | " I 'm not __`ever sure`__ what they are thinking , but I tend to say ' Look , I might be making a mistake here , ' - I always say that - ' but I think this is the best team for today ' .                                                           |


12. _ever satisfied_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_084.0575_x1343432_43:2-4-5`**     | " Nobody is __`ever satisfied`__ that they get maximum exposure . "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_29_085.4475_x1364026_02:20-21-22`**  | I can only give you everything AMBERTONES I want you BOB DYLAN I shall be released ELVIS PRESLEY I ain't __`ever satisfied`__ JOHN MELLENCAMP ( happy bday John ) I could have stood you up KEITH RICHARDS I call your name BEATLES ( happy bday John Lennon ) I wanna be sedated JOHN HIATT I do n't want to grow up RAMONES ( happy bday Johnny and CJ Ramone ) I love you LONDON LEE I love you love me JOAN JETT and BLACKHEARTS I play drums THE DEL LORDS ( happy bday Del Lord ) I am your radio BOSS MARTIANS I ca n't stand up for falling down ELVIS COSTELLO & BRUCE SPRINGSTEEN ( happy bday Sam Moore ) I ca n't let go CONTINENTAL DRIFTERS I ca n't get you off of my mind WILLIE NILE I ca n't help it if i'm still in love with you HANK WILLIAMS I am alive ( live peak ) GARLAND JEFFREYS |
| **`pcc_eng_03_007.1777_x0099795_474:12-13-14`** | A lowkey but gutsy take on Steve Earle 's ' I Ain't __`Ever Satisfied`__ ' is effective if less forceful than Earle 's rocking original .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_25_087.4014_x1398400_39:1-5-6`**     | None of us are __`ever satisfied`__ , one 's friends admit , before laughing maniacally and cartwheeling off into the Florentine night to harass strangers .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **`nyt_eng_19970519_0243_27:11-12-13`**         | the search for those elusive `` family values '' is hardly __`ever satisfied`__ in my family , because no one ever seems to agree with my perfectly rational and commendable conception of what those values should be .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |


13. _ever closer_

|                                                | `token_str`                                                                                                           |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_042.0945_x0664783_19:11-13-14`** | Actually , in the long term , the rocket is not even that important .                                                 |
| **`pcc_eng_24_089.3777_x1429290_11:4-6-7`**    | And it would not be particularly difficult to give U.S. taxpayers the same option .                                   |
| **`pcc_eng_08_047.7928_x0757535_38:12-14-15`** | These guys trade big positions even though many of them are not really that good , they just are high on OPM .        |
| **`pcc_eng_01_095.7809_x1532508_06:16-17-18`** | When I was onboard a Carnival ship recently , I saw a busboy who appeared not terribly motivated , to say the least . |
| **`pcc_eng_21_072.7033_x1158795_64:08-09-10`** | First lap hurt , second lap was not that bad , but the third lap was hell .                                           |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/...

Samples saved as...
1. `neg_bigram_examples/ever/ever_simple_99ex.csv`
1. `neg_bigram_examples/ever/ever_enough_99ex.csv`
1. `neg_bigram_examples/ever/ever_certain_99ex.csv`
1. `neg_bigram_examples/ever/ever_boring_99ex.csv`
1. `neg_bigram_examples/ever/ever_black_99ex.csv`
1. `neg_bigram_examples/ever/ever_sick_99ex.csv`
1. `neg_bigram_examples/ever/ever_easy_99ex.csv`
1. `neg_bigram_examples/ever/ever_perfect_99ex.csv`
1. `neg_bigram_examples/ever/ever_good_99ex.csv`
1. `neg_bigram_examples/ever/ever_able_99ex.csv`
1. `neg_bigram_examples/ever/ever_sure_99ex.csv`
1. `neg_bigram_examples/ever/ever_satisfied_99ex.csv`
1. `neg_bigram_examples/ever/ever_closer_99ex.csv`

## 7. *yet*

|                 |        `N` |      `f1` |   `adv_total` |
|:----------------|-----------:|----------:|--------------:|
| **NEGATED_yet** | 72,839,589 | 3,173,660 |        95,763 |
| **NEGMIR_yet**  |  1,701,929 |   291,732 |           815 |


|                           |    `f` |   `adj_total` |   `dP1` |   `LRC` |      `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:--------------------------|-------:|--------------:|--------:|--------:|----------:|----------:|------------:|-------:|
| **NEGany~yet_eligible**   |    448 |        23,252 |    0.96 |    8.96 |  2,807.56 |     19.52 |      428.48 |    448 |
| **NEGany~yet_official**   |    352 |         6,853 |    0.96 |    8.61 |  2,205.93 |     15.34 |      336.66 |    352 |
| **NEGany~yet_convinced**  |    169 |        12,132 |    0.96 |    7.50 |  1,059.09 |      7.36 |      161.64 |    169 |
| **NEGany~yet_online**     |     98 |        15,650 |    0.96 |    6.66 |    614.14 |      4.27 |       93.73 |     98 |
| **NEGany~yet_mainstream** |     70 |        17,792 |    0.96 |    6.11 |    438.67 |      3.05 |       66.95 |     70 |
| **NEGany~yet_clear**      | 10,406 |       349,214 |    0.95 |   10.77 | 64,409.97 |    456.44 |    9,949.56 | 10,476 |
| **NEGany~yet_final**      |    640 |         5,860 |    0.95 |    8.97 |  3,972.92 |     28.02 |      611.98 |    643 |
| **NEGany~yet_over**       |    162 |         3,983 |    0.95 |    7.21 |  1,003.13 |      7.10 |      154.90 |    163 |
| **NEGany~yet_ready**      |  7,501 |       141,590 |    0.94 |    9.93 | 45,985.07 |    331.09 |    7,169.91 |  7,599 |
| **NEGany~yet_complete**   |  2,174 |        86,361 |    0.94 |    9.20 | 13,277.09 |     96.20 |    2,077.80 |  2,208 |
| **NEGmir~yet_available**  |     28 |        10,284 |    0.83 |    2.54 |     98.77 |      4.80 |       23.20 |     28 |
| **NEGmir~yet_certain**    |     21 |         1,800 |    0.83 |    1.96 |     74.08 |      3.60 |       17.40 |     21 |
| **NEGmir~yet_clear**      |     19 |         6,722 |    0.83 |    1.75 |     67.02 |      3.26 |       15.74 |     19 |
| **NEGmir~yet_sure**       |     19 |         6,761 |    0.83 |    1.75 |     67.02 |      3.26 |       15.74 |     19 |
| **NEGmir~yet_ready**      |     18 |         3,034 |    0.83 |    1.63 |     63.49 |      3.09 |       14.91 |     18 |


1. _yet eligible_

|                                                | `token_str`                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_015.1963_x0229141_21:17-18-19`** | An injured employee also may access their retirement benefits , even if the employee was otherwise not __`yet eligible`__ for retirement .                                                                                                                       |
| **`pcc_eng_23_034.5296_x0541444_35:21-22-23`** | That 's a big leap from next year , when Accenture expects private exchange enrollment , counting workers and retirees not __`yet eligible`__ for Medicare , to total 1 million .                                                                                |
| **`apw_eng_20031204_0435_17:16-17-18`**        | Johnson is eligible for salary arbitration for the first time this winter ; Rivera is n't __`yet eligible`__ .                                                                                                                                                   |
| **`pcc_eng_25_040.1656_x0633972_081:5-6-7`**   | Rivers and Roethlisberger are not __`yet eligible`__ , obviously , but I believe they 'll both get in .                                                                                                                                                          |
| **`pcc_eng_27_053.5705_x0849776_19:16-17-18`** | Individuals purchasing plans in the individual market tend to be self-employed , students , retirees not __`yet eligible`__ for Medicare , the unemployed , people between jobs , and those who are employed but do not take their employer -offered insurance . |


2. _yet official_

|                                                 | `token_str`                                                                                                                                                                                                                                   |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_080.1868_x1279530_12:6-7-8`**     | The deal with Axford is not __`yet official`__ , but will likely come to fruition after the pitcher undergoes a physical later this week .                                                                                                    |
| **`pcc_eng_18_085.7010_x1371502_15:11-12-13`**  | Pending publication in the Federal Register , the closure is not __`yet official`__ , but the emergency measures will be in effect when the bats return this winter to hibernate .                                                            |
| **`apw_eng_20090204_0383_4:3-4-5`**             | results are not __`yet official`__ because some lower-ranked skiers are still to race .                                                                                                                                                       |
| **`pcc_eng_06_079.0512_x1262178_100:10-11-12`** | It 's important to note that the move is n't __`yet official`__ , but the word around Texas Tech circles is Silva 's father is ill , and his family has serious financial needs .                                                             |
| **`pcc_eng_24_073.7862_x1177440_04:18-19-20`**  | Strange is a passion project for Marvel Studios president of production Kevin Feige and while it 's not __`yet official`__ we know Doctor Strange will be hitting theaters in July 2016 after Captain America 3 kicks off the summer in May . |


3. _yet convinced_

|                                         | `token_str`                                                                                                                                                                                                                                     |
|:----------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20020206_0348_17:6-7-8`**    | but India says it is not __`yet convinced`__ about the sincerity of steps being taken by Musharraf .                                                                                                                                            |
| **`apw_eng_20021017_0641_7:17-18-19`**  | there was no opposition to Sinanan 's nomination , but some opposition lawmakers said they were not __`yet convinced`__ that Manning 's party , which won 20 seats in the this month 's election , was committed to unity in political policy . |
| **`nyt_eng_19960412_0476_22:5-6-7`**    | maybe the engineers are not __`yet convinced`__ that the machinery _ the pulleys are linked by a flexible steel drive belt that operates under enormous stress _ is as durable as the conventional automatic sold with other Civic models .     |
| **`nyt_eng_19970422_0730_20:5-6-7`**    | many doctors also are not __`yet convinced`__ cholesterol is a risk factor , in part because the research only recently yielded convincing evidence that LDL really is dangerous .                                                              |
| **`nyt_eng_20000716_0135_19:11-12-13`** | the boom has happened so speedily that some people are not __`yet convinced`__ that it is here to stay .                                                                                                                                        |


4. _yet online_

|                                                | `token_str`                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_val_1.0279_x00462_12:15-16-17`**    | What 's more , our research shows that of the small businesses that 're not __`yet online`__ , 70 % would consider establishing and developing a website if it was easy to do and free of charge . "                                                                                   |
| **`pcc_eng_01_035.3009_x0554168_05:15-16-17`** | But , curiously , there are still a number of SMBs , which are not __`yet online`__ , or neglecting their online presence , either due to ignorance , offline considerations or a fear of alerting their competition to product features which give them the edge in the marketplace . |
| **`pcc_eng_24_107.00738_x1716226_06:6-7-8`**   | The app , which is not __`yet online`__ , does n't let the sad sack who 's missing the show hear the live versions of the songs , which would present significant copyright hurdles , as cool as that would be .                                                                       |
| **`pcc_eng_17_100.4950_x1608272_75:21-22-23`** | In India , for example , the population is growing and becoming more literate , but a substantial portion is not __`yet online`__ .                                                                                                                                                    |
| **`pcc_eng_29_090.5965_x1447125_07:5-6-7`**    | ( The episode is not __`yet online`__ , but will likely be available after the show repeats on Wednesday . )                                                                                                                                                                           |


5. _yet mainstream_

|                                                | `token_str`                                                                                                                                                                                                          |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_027.7118_x0431512_11:7-8-9`**    | Smart packaging , however , is not __`yet mainstream`__ .                                                                                                                                                            |
| **`pcc_eng_00_032.5322_x0509605_25:32-33-34`** | Back in 2010 , when environmental photographer and activist Luka Tomac began the journey of documenting stories from the front lines of climate change , the realities of the crisis were not __`yet mainstream`__ . |
| **`pcc_eng_22_059.1536_x0940227_17:14-15-16`** | While they 've been around for a few years , these networks are n't __`yet mainstream`__ , but they 're fast becoming the weapon of choice for agtech startups .                                                     |
| **`pcc_eng_08_107.2832_x1720979_02:13-14-15`** | Smartwatches are more prevalent than every before , but fashion smartwatches are not __`yet mainstream`__ .                                                                                                          |
| **`pcc_eng_03_089.9885_x1441165_01:5-6-7`**    | Insects as food are not __`yet mainstream`__ in American culture .                                                                                                                                                   |


6. _yet final_

|                                                | `token_str`                                                                                                                                              |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_075.0274_x1197410_08:16-17-18`** | In some cases , rebates would be banned altogether under the proposal , which is not __`yet final`__ .                                                   |
| **`pcc_eng_07_051.7803_x0820998_30:10-11-12`** | The avatar skeleton changes introduced by Project Bento are not __`yet final`__ because we want your feedback , either in the Creation Forumor in JIRA . |
| **`apw_eng_20090112_0900_2:12-13-14`**         | the person spoke on condition of anonymity because the deal was not __`yet final`__ .                                                                    |
| **`pcc_eng_18_008.6133_x0123205_11:5-6-7`**    | The death toll was not __`yet final`__ .                                                                                                                 |
| **`pcc_eng_23_048.6152_x0769304_21:08-09-10`** | The look of the aliens , while not __`yet final`__ , were largely faithful to their comic book counterparts .                                            |


7. _yet over_

|                                          | `token_str`                                                                                                                                                                        |
|:-----------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19960716_0328_21:7-8-9`**     | though the mens ' collections are not __`yet over`__ , with American designers unveiling creations beginning next Monday , look for the slim trend to continue .                   |
| **`nyt_eng_20070307_0087_252:29-30-31`** | so we play out the game , Margret and I - putting down words , guided by good intentions , grateful that the story that matters most is not __`yet over`__ .                       |
| **`nyt_eng_19971027_0120_10:18-19-20`**  | `` There is another move to bonds to from equities as the currency crisis in Asia is not __`yet over`__ , '' said Katherine Beattie , a technical analyst with MMS International . |
| **`nyt_eng_20051115_0316_24:21-22-23`**  | but its executive director warned that the pension system 's troubles , and the risk to the agency , were not __`yet over`__ .                                                     |
| **`apw_eng_19971124_1197_14:11-12-13`**  | JAKARTA -LRB- JP -RRB- : The bumper box-office year is not __`yet over`__ , and there are still plenty of blockbusters headed our way .                                            |


8. _yet clear_

|                                                | `token_str`                                                                                                                                                                                                     |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20001103_0036_7:3-4-5`**            | it is not __`yet clear`__ what brought about this more responsible position .                                                                                                                                   |
| **`pcc_eng_08_040.8031_x0644248_48:11-12-13`** | Authorization is also a desired feature , but it is not __`yet clear`__ that enough APIs need Authorization to justify handling this at the hosting architecture level .                                        |
| **`pcc_eng_14_089.4942_x1430453_15:3-4-5`**    | What is n't __`yet clear`__ is whether they 're planning to re-enlist the most popular games in a list that includes Battlefield 2 , Command & Conquer 3 , Star Wars : Battlefront 2 and Neverwinter Nights 2 . |
| **`pcc_eng_21_064.7865_x1030755_31:3-4-5`**    | It is not __`yet clear`__ to what extent the volume of inquiries and complaints will increase , but increase it most assuredly will .                                                                           |
| **`pcc_eng_13_038.3655_x0604208_290:3-4-5`**   | It is not __`yet clear`__ who carried it out , who collaborated with them , and who paved the way for them .                                                                                                    |


9. _yet ready_

|                                                 | `token_str`                                                                                                                                                                                                                    |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_087.1470_x1392830_012:24-25-26`** | This story -- the one coming vivid , the writing on a roll , where it dragged when I knew the story was not __`yet ready`__ -- is the one I knew was there all along , so I could n't be happier .                             |
| **`pcc_eng_07_052.6056_x0834196_24:14-15-16`**  | Slocum said the Glass recorded video of the incident , but she is not __`yet ready`__ to make that video public .                                                                                                              |
| **`nyt_eng_19970702_0877_22:15-16-17`**         | Hall testified this year at his Palm Beach County trial that although he was not __`yet ready`__ to die , he wanted McIver to give him a fatal dose of prescription drugs when he faced only a prolonged period of suffering . |
| **`pcc_eng_03_082.4186_x1318445_019:27-28-29`** | This is what England , France , and Czechoslovakia should have done to Germany when it demanded the Sudetenland in 1938 , noting that Germany was not __`yet ready`__ for war .                                                |
| **`pcc_eng_02_031.8212_x0498811_19:32-33-34`**  | As you might know there is such a lot of work to take several photos of any model , then editing the photos and setting to the Web , I 'm not __`yet ready`__ .                                                                |


10. _yet complete_

|                                                | `token_str`                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_002.9690_x0031770_04:18-19-20`** | Yellen said in delivering the Fed 's semi-annual economic report to Congress that the economic recovery is not __`yet complete`__ and the Fed intends to keep providing significant support . |
| **`pcc_eng_20_082.0391_x1309343_03:27-29-30`** | All of those late nights in the library suddenly feel worth it , but you know with the student loans , the work of school is not quite __`yet complete`__ .                                   |
| **`pcc_eng_26_009.7511_x0141454_38:13-14-15`** | Some of these volumes will be used to digitize titles that are not __`yet complete`__ .                                                                                                       |
| **`pcc_eng_26_007.3961_x0103101_42:21-22-23`** | Much of the parish lies outside the greater New Orleans levee system , and construction projects to bolster protection are not __`yet complete`__ .                                           |
| **`pcc_eng_02_049.3957_x0782884_2:10-11-12`**  | They should also clearly state where a database is not __`yet complete`__ .                                                                                                                   |


11. _yet available_

|                                                | `token_str`                                                                                                                                                         |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_028.2943_x0441561_78:20-21-22`** | A " sea- based prompt-strike missile is in the early stages of development " so these details " are not __`yet available`__ , " she said in the written responses . |
| **`pcc_eng_28_033.5381_x0526069_103:6-7-8`**   | If any pandemic-specific attributes are not __`yet available`__ for your category , consider adding them to your business name or " about the business " section .  |
| **`pcc_eng_24_071.8281_x1145632_03:24-25-26`** | The preview dialog in the " N+ P folder " tab displays all local data at a glance , including data which is not __`yet available`__ in Vault .                      |
| **`pcc_eng_02_094.9727_x1519408_03:14-15-16`** | See the village and its people through our digital archives , including material not __`yet available`__ through this website .                                     |
| **`pcc_eng_06_030.2105_x0472684_10:3-4-5`**    | Coauthoring is not __`yet available`__ for customers in the Semi-annual channel .                                                                                   |


12. _yet certain_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_099.8209_x1597894_55:3-4-5`**     | Hynek is n't __`yet certain`__ that he will have access to the instrument .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_18_003.0518_x0033373_035:71-72-73`** | Or regular and highly reproducible figs d and hall a the circulation can result unless the underlying cause secondary brain injury is the only injury the child has ever received human derived growth factor induces nephrogenesis and wilmsa tumor wt gene causing waardenburg syndrome type ofd am j physiol a neissf morphogenesis and function of the non dominant arm are preferred , it was hard to answer patients who are not __`yet certain`__ a rules of thumba general indications for transfer to icu new presentation of guillian - barre syndrome . |
| **`pcc_eng_05_038.6640_x0609729_09:3-4-5`**     | It is not __`yet certain`__ that LUKoil will be the Russian partner in the joint development with Kazakhstan , although it has been assured that its investment will be repaid , " Argus " said .                                                                                                                                                                                                                                                                                                                                                                  |
| **`apw_eng_20090108_0579_2:6-7-8`**             | in fact , it is n't __`yet certain`__ that he 'll give up his hand-held device once he takes office .                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_08_071.4996_x1141577_150:3-4-5`**    | We 're not __`yet certain`__ who is behind this terrorist plot , but we 've narrowed it down to bumbling head coach Wade Phillips , slick handed place holder Tony Romo , or all world receiver Terrell Owens . "                                                                                                                                                                                                                                                                                                                                                  |


13. _yet sure_

|                                                | `token_str`                                                                                                                                                        |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_034.2127_x0537713_74:11-12-13`** | Chances are his existence is busy enough and he is n't __`yet sure`__ he wants to take on your drama too .                                                         |
| **`pcc_eng_25_034.7007_x0545579_41:4-5-6`**    | But we are not __`yet sure`__ how it will affect both Binay 's and Roxas ' chances in the poll results .                                                           |
| **`pcc_eng_03_017.9754_x0274522_086:3-4-5`**   | I 'm not __`yet sure`__ how replicable it is , because every situation is different .                                                                              |
| **`pcc_eng_15_041.4761_x0654445_10:14-15-16`** | For instance , when I knew that I was leaving Mississippi -- though not __`yet sure`__ to where -- there was suddenly a list of things I needed to do beforehand . |
| **`nyt_eng_19990109_0269_26:22-23-24`**        | as for the Kings , team executives held their first meeting a few days ago to plan a goodbye but are n't __`yet sure`__ how they 'll do it .                       |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/...

Samples saved as...
1. `neg_bigram_examples/yet/yet_eligible_99ex.csv`
1. `neg_bigram_examples/yet/yet_official_99ex.csv`
1. `neg_bigram_examples/yet/yet_convinced_99ex.csv`
1. `neg_bigram_examples/yet/yet_online_99ex.csv`
1. `neg_bigram_examples/yet/yet_mainstream_99ex.csv`
1. `neg_bigram_examples/yet/yet_final_99ex.csv`
1. `neg_bigram_examples/yet/yet_over_99ex.csv`
1. `neg_bigram_examples/yet/yet_clear_99ex.csv`
1. `neg_bigram_examples/yet/yet_ready_99ex.csv`
1. `neg_bigram_examples/yet/yet_complete_99ex.csv`
1. `neg_bigram_examples/yet/yet_available_99ex.csv`
1. `neg_bigram_examples/yet/yet_certain_99ex.csv`
1. `neg_bigram_examples/yet/yet_sure_99ex.csv`

## 8. *immediately*

|                         |        `N` |      `f1` |   `adv_total` |
|:------------------------|-----------:|----------:|--------------:|
| **NEGATED_immediately** | 72,839,589 | 3,173,660 |        96,973 |
| **NEGMIR_immediately**  |  1,701,929 |   291,732 |         1,195 |


|                                    |    `f` |   `adj_total` |   `dP1` |   `LRC` |       `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:-----------------------------------|-------:|--------------:|--------:|--------:|-----------:|----------:|------------:|-------:|
| **NEGany~immediately_possible**    |  1,000 |       245,272 |    0.91 |    7.62 |   5,845.77 |     45.92 |      954.08 |  1,054 |
| **NEGany~immediately_clear**       | 24,416 |       349,214 |    0.89 |    8.16 | 141,186.69 |  1,134.49 |   23,281.51 | 26,038 |
| **NEGany~immediately_reachable**   |    109 |         2,672 |    0.86 |    5.56 |     610.53 |      5.23 |      103.77 |    120 |
| **NEGany~immediately_sure**        |    138 |       262,825 |    0.82 |    5.40 |     738.65 |      6.97 |      131.03 |    160 |
| **NEGany~immediately_certain**     |     70 |        74,952 |    0.71 |    4.19 |     336.68 |      4.05 |       65.95 |     93 |
| **NEGany~immediately_available**   | 21,078 |       666,909 |    0.67 |    5.70 |  98,046.67 |  1,278.84 |   19,799.16 | 29,351 |
| **NEGany~immediately_able**        |    626 |       223,196 |    0.59 |    4.70 |   2,655.18 |     43.09 |      582.91 |    989 |
| **NEGany~immediately_forthcoming** |    133 |         7,473 |    0.55 |    3.89 |     540.70 |      9.72 |      123.28 |    223 |
| **NEGany~immediately_intuitive**   |     54 |        20,664 |    0.55 |    3.21 |     218.74 |      3.96 |       50.04 |     91 |
| **NEGmir~immediately_clear**       |     31 |         6,722 |    0.55 |    1.13 |      62.95 |      7.37 |       23.63 |     43 |
| **NEGany~immediately_obvious**     |  2,238 |       165,439 |    0.52 |    4.55 |   8,712.07 |    173.80 |    2,064.20 |  3,989 |
| **NEGmir~immediately_available**   |    162 |        10,284 |    0.42 |    1.85 |     241.53 |     47.14 |      114.86 |    275 |


1. _immediately possible_

|                                                | `token_str`                                                                                                                                                                     |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20091106_0036_18:3-4-5`**           | it was not __`immediately possible`__ to verify either claim due to the dangerous nature of the region .                                                                        |
| **`apw_eng_20031022_0508_17:3-4-5`**           | it was not __`immediately possible`__ to obtain comment from the Ministry of Health .                                                                                           |
| **`apw_eng_20020714_0260_3:4-5-6`**            | but it was not __`immediately possible`__ to confirm that , since it was not known how many survivors had met with Mandela , and none of them appeared at his news conference . |
| **`pcc_eng_15_098.7948_x1580575_20:10-11-12`** | Due to the remoteness of the region it was not __`immediately possible`__ to verify the information .                                                                           |
| **`apw_eng_20020826_0267_8:3-4-5`**            | it was not __`immediately possible`__ to get comment from government or army officials .                                                                                        |


2. _immediately clear_

|                                                | `token_str`                                                                                                               |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_19970409_1194_7:3-4-5`**            | it was not __`immediately clear`__ whether the hearing was held .                                                         |
| **`pcc_eng_21_063.1630_x1004576_12:3-4-5`**    | It was not __`immediately clear`__ whether the property has gone into contract or has simply been taken off the market .  |
| **`nyt_eng_20001120_0306_28:3-4-5`**           | it was not __`immediately clear`__ what punishment would be meted out by the party to Kato and his parliamentary allies . |
| **`apw_eng_19971103_0259_5:3-4-5`**            | it was not __`immediately clear`__ how many of the seven American inspectors still in Baghdad were involved .             |
| **`pcc_eng_02_099.1098_x1586315_09:10-11-12`** | The impact of the decision on Exxon Mobil was not __`immediately clear`__ .                                               |


3. _immediately reachable_

|                                                | `token_str`                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_032.8962_x0515012_12:6-7-8`**    | China's Ministry of Health was not __`immediately reachable`__ for comment after the Xinhua report .                                                   |
| **`pcc_eng_22_059.9128_x0952367_17:4-5-6`**    | Mr. Roberts was not __`immediately reachable`__ for comment , though he posted to Twitter : " Yes , I 'll be leaving@Reuters , though not right away . |
| **`pcc_eng_02_096.6577_x1546677_08:5-6-7`**    | Hybrid Air Vehicles was not __`immediately reachable`__ by telephone .                                                                                 |
| **`pcc_eng_13_003.1816_x0035024_08:4-5-6`**    | PNB officials were not __`immediately reachable`__ for comment , while Pw C declined to comment on the matter .                                        |
| **`pcc_eng_00_072.7105_x1159292_09:16-17-18`** | The other three councilors , Charlie Miranda , Guido Maniscalco and Yolie Capin , were not __`immediately reachable`__ .                               |


4. _immediately sure_

|                                                | `token_str`                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_087.1863_x1393018_07:4-5-6`**    | If you are n't __`immediately sure`__ what kind of fence will provide your house the greatest visual appeal while still accommodating your budgetary needs , then here 's a complete analysis on choosing a fencing design . |
| **`pcc_eng_08_102.9408_x1650453_07:4-5-6`**    | If you are not __`immediately sure`__ what type of fence will provide your property the best visual appeal while adapting your budgetary needs , then here 's a complete analysis on choosing a fencing layout .             |
| **`pcc_eng_18_083.2969_x1332643_01:18-19-20`** | The officer , who was an acquaintance of the well -known traditional healer , said policemen were not __`immediately sure`__ what the smell was as Mbatha walked up to the desk at about 6 pm on Friday .                    |
| **`pcc_eng_13_091.1921_x1457746_08:5-6-7`**    | Swanson said she was not __`immediately sure`__ what prompted the new restriction on after-session access .                                                                                                                  |
| **`apw_eng_20080205_0116_13:10-11-12`**        | Charming Shoppes spokeswoman Gayle Coolick said Monday she was not __`immediately sure`__ how many employees were working during the robbery or how much cash was in the store at the time .                                 |


5. _immediately certain_

|                                                | `token_str`                                                                                                                                                                                                       |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_038.9102_x0612956_50:3-4-5`**    | It was not __`immediately certain`__ how the Bastrop blaze began but it appeared that two fires merged to form the " monster " fire , Amen said .                                                                 |
| **`pcc_eng_08_072.3121_x1154626_30:3-4-5`**    | It was not __`immediately certain`__ if he would attend the next talks though .                                                                                                                                   |
| **`pcc_eng_06_079.1498_x1263719_15:19-20-21`** | She has since been identified by the medical examiner 's office , Brunner said , but it was not __`immediately certain`__ whether Raffo was among the 17 victims officially counted among the dead as of Friday . |
| **`apw_eng_20091023_0366_3:12-13-14`**         | Zabit Khan says the exact cause of the blast Friday was not __`immediately certain`__ but that it could have been a remote-controlled bomb .                                                                      |
| **`pcc_eng_07_056.7684_x0901241_06:6-7-8`**    | Graham notes it is " not __`immediately certain`__ who else received the preliminary packet . "                                                                                                                   |


6. _immediately available_

|                                                | `token_str`                                                                                                                                                                          |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_077.4909_x1238437_16:6-7-8`**    | Attorney General de Jong was not __`immediately available`__ for comment .                                                                                                           |
| **`apw_eng_19980220_0155_11:20-21-22`**        | other details of Hyundai 's deal with Adaptec , a computer connections maker based in Milpitas , Calif. were not __`immediately available`__ .                                       |
| **`pcc_eng_20_045.2456_x0714754_09:08-09-10`** | Spokespersons for Goldman Sachs and Citigroup were not __`immediately available`__ for comment .                                                                                     |
| **`apw_eng_19980401_0980_2:1-3-4`**            | nobody was __`immediately available`__ at Amsterdam police to confirm the report .                                                                                                   |
| **`apw_eng_20080713_0319_3:3-4-5`**            | details were not __`immediately available`__ about what caused the crash Sunday , which appeared to take place in a downhill curve and badly tore Evans ' jersey in several places . |


7. _immediately able_

|                                                | `token_str`                                                                                                                                                                      |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_056.3504_x0894473_06:09-10-11`** | Ontario 's Ministry of the Attorney General was not __`immediately able`__ to confirm the plea .                                                                                 |
| **`pcc_eng_07_019.0089_x0291229_07:5-6-7`**    | A Nordstrom spokeswoman was n't __`immediately able`__ to clarify whether plans for the store have been downsized .                                                              |
| **`pcc_eng_15_013.0457_x0194349_22:3-4-5`**    | CNN was n't __`immediately able`__ to reach Mitsubishi for comment outside of regular business hours .                                                                           |
| **`pcc_eng_28_016.0476_x0243596_06:08-09-10`** | An official of the State Department was not __`immediately able`__ to confirm Pompeo 's arrival in Pyongyang , from where outside communication can be limited .                 |
| **`apw_eng_20080819_0955_13:3-4-5`**           | Keller was n't __`immediately able`__ to say how much luggage an animal-sniffing dog could cover , but said a drug dog can get through about 2,000 bags in an eight-hour shift . |


8. _immediately forthcoming_

|                                                | `token_str`                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_034.7526_x0546596_10:7-8-9`**    | When the petting she wants is not __`immediately forthcoming`__ , she complains .                                                                                                                                                                   |
| **`pcc_eng_05_012.2159_x0181855_087:6-7-8`**   | This time , that was n't __`immediately forthcoming`__ .                                                                                                                                                                                            |
| **`pcc_eng_13_003.6560_x0042741_14:13-14-15`** | However , an expected formal announcement of the council 's communique was not __`immediately forthcoming`__ , prompting speculation that the US - led Coalition Provisional Authority , the occupying power , had either delayed or squelched it . |
| **`pcc_eng_26_043.1286_x0681385_42:7-8-9`**    | When this narrative of victimization was not __`immediately forthcoming`__ , we kicked into high gear to manufacture one .                                                                                                                          |
| **`pcc_eng_15_094.7416_x1515176_36:19-20-21`** | Are able to persist through difficult tasks and difficult times , even when these rewards and benefits are not __`immediately forthcoming`__ .                                                                                                      |


9. _immediately intuitive_

|                                                | `token_str`                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_089.4677_x1429224_02:13-14-15`** | The idea of going into debt to pay off other debts is not __`immediately intuitive`__ , but it can actually be a useful tool to free you from bad debts .  |
| **`pcc_eng_20_006.2838_x0085088_035:4-5-6`**   | Natural selection is not __`immediately intuitive`__ .                                                                                                     |
| **`pcc_eng_18_048.2076_x0764100_22:08-09-10`** | This format , Jaroslovsky says , is not __`immediately intuitive`__ for those unfamiliar with handheld devices .                                           |
| **`pcc_eng_25_085.6377_x1369811_12:4-5-6`**    | Some tools are n't __`immediately intuitive`__ , like the resyncing process , and the fact that only Tune Wiki-approved editors can edit existing lyrics . |
| **`pcc_eng_02_009.8674_x0143229_70:3-4-5`**    | It was not __`immediately intuitive`__ this represented healthcare                                                                                         |


10. _immediately obvious_

|                                                | `token_str`                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_091.0490_x1455323_25:5-6-7`**    | [ If it 's not __`immediately obvious`__ , explain more about what the product or service is and what makes it stand out here ] .  |
| **`pcc_eng_12_037.5816_x0591677_26:3-5-6`**    | It may not be __`immediately obvious`__ , but there 's a lot of thought that goes into the interior design of restaurants .        |
| **`pcc_eng_22_052.9930_x0839960_20:17-18-19`** | With the naked eye , the difference between the especially small or large full Moon is not __`immediately obvious`__ .             |
| **`pcc_eng_val_1.5882_x09587_56:13-14-15`**    | You may be wondering where the CD player is as it 's not __`immediately obvious`__ on looking at the interior .                    |
| **`pcc_eng_16_029.3592_x0459018_46:12-13-14`** | Equally , though , defying expectations and going somewhere that is n't __`immediately obvious`__ can be a really effective move . |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/...

Samples saved as...
1. `neg_bigram_examples/immediately/immediately_possible_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_clear_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_reachable_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_sure_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_certain_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_available_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_able_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_forthcoming_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_intuitive_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_obvious_99ex.csv`

## 9. *particularly*

|                          |        `N` |      `f1` |   `adv_total` |
|:-------------------------|-----------:|----------:|--------------:|
| **NEGATED_particularly** | 72,839,589 | 3,173,660 |       513,668 |
| **NEGMIR_particularly**  |  1,701,929 |   291,732 |        13,003 |


|                                       |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:--------------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGany~particularly_likable**       |   119 |         8,160 |    0.85 |    5.53 |   657.49 |      5.79 |      113.21 |    133 |
| **NEGany~particularly_likeable**      |   106 |         5,902 |    0.84 |    5.34 |   579.07 |      5.23 |      100.77 |    120 |
| **NEGmir~particularly_novel**         |    54 |           320 |    0.83 |    3.71 |   190.49 |      9.26 |       44.74 |     54 |
| **NEGmir~particularly_comfortable**   |    44 |         4,642 |    0.83 |    3.36 |   155.21 |      7.54 |       36.46 |     44 |
| **NEGmir~particularly_revolutionary** |    39 |           485 |    0.83 |    3.15 |   137.57 |      6.69 |       32.31 |     39 |
| **NEGmir~particularly_radical**       |    31 |         1,072 |    0.83 |    2.73 |   109.35 |      5.31 |       25.69 |     31 |
| **NEGmir~particularly_fast**          |    26 |         1,259 |    0.83 |    2.39 |    91.71 |      4.46 |       21.54 |     26 |
| **NEGmir~particularly_surprising**    |   166 |         2,662 |    0.82 |    5.06 |   564.67 |     28.80 |      137.20 |    168 |
| **NEGany~particularly_forthcoming**   |    72 |         7,473 |    0.82 |    4.85 |   387.25 |      3.62 |       68.38 |     83 |
| **NEGany~particularly_religious**     |   485 |        28,028 |    0.81 |    6.12 | 2,585.71 |     24.62 |      460.38 |    565 |
| **NEGmir~particularly_new**           |   404 |        12,836 |    0.81 |    5.92 | 1,365.17 |     70.28 |      333.72 |    410 |
| **NEGmir~particularly_wrong**         |   212 |        20,880 |    0.81 |    5.05 |   702.22 |     37.20 |      174.80 |    217 |
| **NEGany~particularly_original**      |   360 |        37,594 |    0.80 |    5.86 | 1,894.60 |     18.56 |      341.44 |    426 |
| **NEGmir~particularly_remarkable**    |   108 |         3,238 |    0.80 |    4.24 |   354.53 |     19.03 |       88.97 |    111 |
| **NEGany~particularly_new**           |   747 |       253,862 |    0.79 |    6.04 | 3,874.46 |     39.21 |      707.79 |    900 |
| **NEGmir~particularly_close**         |   136 |        13,874 |    0.77 |    4.01 |   415.70 |     24.85 |      111.15 |    145 |
| **NEGany~particularly_athletic**      |   108 |        17,142 |    0.75 |    4.77 |   541.01 |      5.93 |      102.07 |    136 |
| **NEGany~particularly_revolutionary** |    77 |        10,338 |    0.75 |    4.49 |   385.60 |      4.23 |       72.77 |     97 |
| **NEGany~particularly_flashy**        |    57 |         4,494 |    0.73 |    4.08 |   278.96 |      3.22 |       53.78 |     74 |
| **NEGany~particularly_surprising**    | 1,069 |        70,540 |    0.57 |    4.71 | 4,433.52 |     75.94 |      993.06 |  1,743 |


1. _particularly likable_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_044.3575_x0700605_09:12-13-14`**  | But it 's also because the story 's other characters are n't __`particularly likable`__ .                                                                                                                                                                                                                                                |
| **`pcc_eng_28_045.4466_x0719287_15:5-6-7`**     | And its narrator is not __`particularly likable`__ .                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_26_031.9732_x0500519_052:36-48-49`** | The almost-unbearable bittersweetness of Li's carefully closing Chou 's suitcase and handing it to her , and then standing by the window and watching her as she leaves , is complicated by the fact that neither of these characters , nor any other in Terrorizer , is __`particularly likable`__ .                                    |
| **`pcc_eng_22_006.5138_x0088996_18:10-11-12`**  | In short , Tom Rhys Harries 's character is n't __`particularly likable`__ , to a point where a predictable switchover into a redemptive , understanding attitude would n't really work .                                                                                                                                                |
| **`pcc_eng_22_006.7930_x0093446_17:51-52-53`**  | Made for only $ 30 million , far less than what it cost for Zemeckis to make " The Polar Express " or " A Christmas Carol , " this is more of a character driven drama from the 1970 's as it gives us a main character who is not __`particularly likable`__ , and yet we are compelled to follow him all the way to the movie 's end . |


2. _particularly likeable_

|                                                 | `token_str`                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_025.4152_x0394502_31:6-7-8`**     | Most of the characters are n't __`particularly likeable`__ , but they are n't ones you despise either .                                                                                                    |
| **`pcc_eng_12_084.0926_x1342573_38:6-7-8`**     | His portrayal of God is n't __`particularly likeable`__ ( in fact , none of the characters are likeable or relatable ) , but it is interesting .                                                           |
| **`pcc_eng_13_084.4099_x1348390_26:1-6-7`**     | None of the characters were __`particularly likeable`__ , and that is n't just me judging them based on their past offences - there just is n't much warmth to anyone in the book .                        |
| **`pcc_eng_17_042.4874_x0670147_32:7-8-9`**     | Teri Garr's Frannie is attractive but not __`particularly likeable`__ - the poorly -written domestic squabbles keep us from caring about the lovers , and their dreams are far too shallow to involve us . |
| **`pcc_eng_18_046.2336_x0732013_038:17-18-19`** | It creates the problem that our hero is basically just a slab of meat , and not __`particularly likeable`__ .                                                                                              |


3. _particularly novel_

|                                                 | `token_str`                                                                                                                                                                                                                         |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_049.5724_x0785567_29:6-7-8`**     | In truth , there 's nothing __`particularly novel`__ or disquieting about the scheme Murray 's drawn up , except insofar as the procedural extremism conservatives have deployed in the Obama era is alarming in general .          |
| **`pcc_eng_24_020.6021_x0316588_24:18-19-20`**  | The fact that the Greeks then used the first two letters to create the word alphabet is n't __`particularly novel`__ .                                                                                                              |
| **`pcc_eng_18_084.9988_x1360098_13:30-31-32`**  | Langewiesche 's presentation of nuclear weapons as the great equalizer ( with increasing potential of becoming ' the great leveller ' ) in the international system was interesting but not __`particularly novel`__ .              |
| **`pcc_eng_21_097.8756_x1565111_16:7-8-9`**     | ALEC ROSS : There 's actually nothing __`particularly novel`__ about any of this , except that we all get to see it .                                                                                                               |
| **`pcc_eng_20_088.9868_x1421466_013:27-28-29`** | For example , though it is great to see the mainstream media come to condemn the intellectual fallacies inherent with protectionist trade policies , there is nothing __`particularly novel`__ about a president imposing tariffs . |


4. _particularly comfortable_

|                                                | `token_str`                                                                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_005.7456_x0076868_17:3-4-5`**    | Cycling is not __`particularly comfortable`__ , but you will get used to the strange position , along with all its aches and pains .                                   |
| **`pcc_eng_13_089.8960_x1436844_27:22-24-25`** | For Muslim women who don their natural hair , this could cause unnecessary pressure to conform to hair practices they may not be __`particularly comfortable`__ with . |
| **`pcc_eng_22_055.0046_x0872632_15:4-5-6`**    | " I 'm not __`particularly comfortable`__ being under the water , " Briggs told JTA , admitting he did n't learn to swim until the " ripe age " of 12 .                |
| **`pcc_eng_21_068.0499_x1083588_29:20-21-22`** | For his part , the cab driver seemed out of place , too , neither interested in the fight nor __`particularly comfortable`__ with it .                                 |
| **`pcc_eng_23_003.3323_x0037537_3:3-4-5`**     | I am not __`particularly comfortable`__ in bars or clubs .                                                                                                             |


5. _particularly revolutionary_

|                                                | `token_str`                                                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_004.6567_x0059087_04:02-10-11`** | While none of the following tactics / ideas are __`particularly revolutionary`__ or profound , when wisely integrated into standard PR practices such as press release distribution and reporter calls - they combine to elevate a relatively static campaign into a dynamic , effective one : |
| **`pcc_eng_11_058.6598_x0932931_6:3-4-5`**     | This was n't __`particularly revolutionary`__ when it comes to earbud design in general , but it is a step away from the hard earpieces Apple gives you when you buy its products .                                                                                                            |
| **`pcc_eng_15_092.7814_x1483448_52:3-4-5`**    | There is nothing __`particularly revolutionary`__ about keeping connected to the office while on the road with the aid of a smartphone , i Pad , or other type of tablet computer .                                                                                                            |
| **`pcc_eng_24_071.8081_x1145292_10:1-5-6`**    | None of this is __`particularly revolutionary`__ : Google Maps has had very good transit directions forever -- and is even introducing real -time transit updates .                                                                                                                            |
| **`pcc_eng_16_080.3918_x1284895_011:1-6-7`**   | None of my ideas are __`particularly revolutionary`__ , or even unique - something that any developer who gives a damn could implement .                                                                                                                                                       |


6. _particularly radical_

|                                                 | `token_str`                                                                                                                                                                                                                             |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_032.5647_x0510895_07:1-3-4`**     | None are __`particularly radical`__ ; indeed , each idea simply develops programs and policies decided on by earlier FCC administrations , some of them Republican .                                                                    |
| **`pcc_eng_05_085.4864_x1367191_29:4-5-6`**     | The story does nothing __`particularly radical`__ with the incarnations of the various characters but winds them together with a modest complexity .                                                                                    |
| **`pcc_eng_05_088.6709_x1418290_31:6-7-8`**     | Though his policy positions are n't __`particularly radical`__ by European standards , Sanders ' candidacy inspired hope in people who'd otherwise given up on seeing their opinions and interests represented in mainstream politics . |
| **`pcc_eng_20_082.7683_x1321025_27:4-5-6`**     | Though there 's nothing __`particularly radical`__ about religious life , it 's meant to be prophetic .                                                                                                                                 |
| **`pcc_eng_26_044.2462_x0699430_250:08-09-10`** | I 'm not cool and I am not __`particularly radical`__ in my everyday life .                                                                                                                                                             |


7. _particularly fast_

|                                             | `token_str`                                                                                                                                                                           |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_010.8164_x0158838_09:3-4-5`** | It 's not __`particularly fast`__ or agile though , and it 's not nearly as light as many of its contemporaries , but the updates to this shoe have made the ride even more sublime . |
| **`pcc_eng_00_068.9032_x1097447_22:1-2-3`** | Not __`particularly fast`__ , powerful , or quick .                                                                                                                                   |
| **`pcc_eng_08_057.3081_x0911903_14:1-2-3`** | Not __`particularly fast`__ , but fast enough .                                                                                                                                       |
| **`pcc_eng_23_014.9085_x0224111_12:3-4-5`** | He is not __`particularly fast`__ or powerful or strong - and spends large parts of matches grazing .                                                                                 |
| **`pcc_eng_09_089.0499_x1424734_06:1-3-4`** | Neither are __`particularly fast`__ or efficient , and it 's not a particularly good idea to interrupt them ( with C-g or anything else ) once you 've started one of them .          |


8. _particularly forthcoming_

|                                                 | `token_str`                                                                                                                                                                                                                                      |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_002.5441_x0025004_15:5-6-7`**     | Predictably , they were n't __`particularly forthcoming`__ .                                                                                                                                                                                     |
| **`apw_eng_19971112_1107_22:24-26-27`**         | Nazir said Mesdaq will serve as an alternative source of capital for growth companies , especially since venture capital companies and banks have not been __`particularly forthcoming`__ in the past in assisting such start-up operations .    |
| **`pcc_eng_23_039.3177_x0619144_077:29-31-32`** | Doombot shows up to give Victor a new body , but Victor does n't like the buff , weaponized Transformers body that Doombot makes , though Victor is n't being __`particularly forthcoming`__ about his hang-ups .                                |
| **`pcc_eng_13_005.9905_x0080443_37:08-10-11`**  | Editors , producers , and journalists have not been __`particularly forthcoming`__ in acknowledging to their own viewers , the media-consuming public , the degree to which the object of their reporting dictates its content and composition . |
| **`pcc_eng_11_098.2159_x1573678_117:14-16-17`** | It 's just a little bit slower , and the Trump camp has not been __`particularly forthcoming`__ in terms of providing witnesses and at least some information .                                                                                  |


9. _particularly surprising_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_002.1532_x0018421_11:1-6-7`**    | Neither of those departures are __`particularly surprising`__ , though , especially given the level of competition in midfield at PSG .                                                                                                                                                                                                                                                   |
| **`nyt_eng_20000104_0364_3:4-5-6`**            | so there was nothing __`particularly surprising`__ , or for that matter offensive , about Mayor Rudolph Giuliani 's high profile during the televised New Year 's Eve festivities in Times Square , or about the White House 's decision to have Hillary Rodham Clinton join President Clinton in delivering a televised greeting to the nation from the Oval Office on New Year 's Day . |
| **`pcc_eng_11_019.7981_x0304036_18:4-5-6`**    | So it 's not __`particularly surprising`__ that reducing our screen time increases our attention span .                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_08_040.8491_x0644957_18:15-16-17`** | " The findings in the New York State Attorney General 's Office report are not __`particularly surprising`__ .                                                                                                                                                                                                                                                                            |
| **`pcc_eng_13_006.3289_x0086002_06:3-4-5`**    | That is n't __`particularly surprising`__ .                                                                                                                                                                                                                                                                                                                                               |


10. _particularly religious_

|                                                 | `token_str`                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_079.0946_x1263230_058:08-10-11`** | His father was surprised ; Patrick had never been __`particularly religious`__ and he had his whole life ahead of him .                  |
| **`pcc_eng_15_098.0483_x1568580_47:3-4-5`**     | I 'm not __`particularly religious`__ , I just notice how this guy seems to be really popular with Latin-American Catholics ?            |
| **`pcc_eng_03_035.6528_x0561291_08:08-09-10`**  | My daughter tells me Bear's Den is n't __`particularly religious`__ , maybe not at all , though they do use religious imagery at times . |
| **`apw_eng_20020831_0461_13:13-14-15`**         | Breeden appreciated the gesture , even though she said her family is not __`particularly religious`__ .                                  |
| **`pcc_eng_02_042.2977_x0668099_32:09-10-11`**  | He was a meek man , he has n't __`particularly religious`__ .                                                                            |


11. _particularly new_

|                                                | `token_str`                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_088.0686_x1407113_38:1-6-7`**    | None of these features are __`particularly new`__ or surprising , especially to veterans of the racing genre , but it 's good to have them available . |
| **`pcc_eng_08_002.1047_x0017906_11:08-09-10`** | The concept of the smart TV is n't __`particularly new`__ .                                                                                            |
| **`pcc_eng_05_042.7741_x0676220_108:3-8-9`**   | Mundie : None of these things are __`particularly new`__ or unanticipated .                                                                            |
| **`pcc_eng_15_095.6456_x1529817_16:20-21-22`** | Senate Intelligence Vice Chair Saxby Chambliss ( R- GA ) backed up Feinstein , saying , " This is nothing __`particularly new`__ .                     |
| **`pcc_eng_27_028.1944_x0439194_13:2-3-4`**    | So nothing __`particularly new`__ here , storywise .                                                                                                   |


12. _particularly wrong_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_083.0944_x1326972_097:3-4-5`**   | There 's nothing __`particularly wrong`__ with Jenny 's personality , but George silently but perceptibly judges her for everything she says and does : her description of his work as " elevator music , " her casual , offhanded utterance of the word " fuck , " her obsession with timing their lovemaking to a cherished recording of Ravel 's Bolero , her constant smoking of joints to get in the mood , her habit of casually dropping revelations about her sexual awakening into conversation . |
| **`nyt_eng_20070303_0165_44:4-5-6`**           | `` There is nothing __`particularly wrong`__ with loss mitigation , '' Rosner said .                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_21_090.2707_x1442773_41:08-09-10`** | THE OTHER HALF : Houston Dynamo - Nothing __`particularly wrong`__ with this side , just nothing exciting either .                                                                                                                                                                                                                                                                                                                                                                                         |
| **`pcc_eng_23_006.8833_x0095075_13:3-4-5`**    | There 's nothing __`particularly wrong`__ and there are some good funny moments , mostly based around the duo's altered perceptions - for some reason , Nick appears to the living as an elderly Chinese man ( James Hong ) , whereas Roy is a very sexy blonde Russian woman ( Marisa Miller ) .                                                                                                                                                                                                          |
| **`pcc_eng_24_022.7004_x0350623_10:3-4-5`**    | There is nothing __`particularly wrong`__ with this as a hobby , which is to say , a means of amusement , but is it not a method of producing a meaningful quantity of food !                                                                                                                                                                                                                                                                                                                              |


13. _particularly remarkable_

|                                                | `token_str`                                                                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_039.8203_x0627381_11:18-19-20`** | Plot-wise , very little happens in the film 's first half , and what happens post-intermission is n't __`particularly remarkable`__ .                                              |
| **`pcc_eng_00_039.3781_x0619973_113:6-7-8`**   | That was unusual , but not __`particularly remarkable`__ , nor was their anatomical composition - heavier than any deer or horse he 'd seen , but still roughly similar in shape . |
| **`pcc_eng_04_051.4067_x0814326_32:5-6-7`**    | The stories themselves are not __`particularly remarkable`__ , but the writing is straightforward and crisp .                                                                      |
| **`pcc_eng_28_077.9220_x1244355_08:6-8-9`**    | In itself , this would not be __`particularly remarkable`__ since the discovery of expoplanets has become quite a regular occurrence in the world of astronomy .                   |
| **`pcc_eng_22_073.6964_x1174918_04:3-4-5`**    | There 's nothing __`particularly remarkable`__ about it , no wacky laws of physics , no horrendous fauna , no incredibly advanced civilization .                                   |


14. _particularly original_

|                                                | `token_str`                                                                                                                                                                                                                                                             |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_039.9215_x0628904_41:4-5-6`**    | The music is n't __`particularly original`__ , but works well with the film 's tone , and is a nearly constant aural element -- blended quietly under the more expositional scenes , and used as a nice exclamation point during the most bombastic montage sequences . |
| **`pcc_eng_03_012.7429_x0189913_12:14-15-16`** | The whole " small town cut off by invisible dome " plot is n't __`particularly original`__ .                                                                                                                                                                            |
| **`pcc_eng_02_032.0976_x0503226_029:3-4-5`**   | There 's nothing __`particularly original`__ or insightful to set this teen - dystopia thriller apart from the crowd , but strong characters will build some anticipation for the next instalment in the franchise .                                                    |
| **`pcc_eng_08_079.4581_x1270500_16:7-8-9`**    | Huntington 's new schtick was the not __`particularly original`__ idea that the Post- Cold War world was polarizing according to ' the interactions around seven or eight major civilizations ' .                                                                       |
| **`pcc_eng_05_087.6358_x1401837_14:09-10-11`** | As for the political satire , it 's not __`particularly original`__ -- posh cabinet ministers , austerity , ' we 're all in this together ' -- but it 's cheeky and pitched at just the right level .                                                                   |


15. _particularly close_

|                                                 | `token_str`                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_038.3888_x0605091_59:3-4-5`**     | We 're not __`particularly close`__ but I know they do love me and that I 'd be inflicting an awful lot of pain if I told them .                             |
| **`pcc_eng_11_060.0048_x0954812_04:15-16-17`**  | ' Cisco remains the biggest single player in enterprise networking , and it 's not __`particularly close`__ . '                                              |
| **`pcc_eng_13_004.8641_x0062337_066:11-13-14`** | Sure , turnout was low in both contests , but neither was __`particularly close`__ .                                                                         |
| **`pcc_eng_00_065.0814_x1036080_05:17-18-19`**  | Day three , the final day , has just wrapped up and the final score was not __`particularly close`__ , although round 2 proved to be a bit more exciting .   |
| **`pcc_eng_23_088.1039_x1407719_16:07-09-10`**  | Gerbic , who said he had n't been __`particularly close`__ to either sibling , said he never noticed anything odd or antagonistic about their relationship . |


16. _particularly athletic_

|                                                | `token_str`                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_067.8447_x1080213_202:6-7-8`**   | Hes 6 - 7 , not __`particularly athletic`__ , and has just an average skill - set offensively as far as his position in the NBA is concerned .                                                                                                                            |
| **`pcc_eng_06_070.3981_x1122908_04:25-26-27`** | Hile , a contracts and grants administrator in the computer science and engineering department at the University of California in San Diego , was n't __`particularly athletic`__ as a child .                                                                            |
| **`pcc_eng_12_030.2209_x0473137_24:3-5-6`**    | She had never been __`particularly athletic`__ but loved nature and started hiking while working in the Grand Canyon .                                                                                                                                                    |
| **`pcc_eng_03_039.5625_x0624714_18:3-4-5`**    | She was not __`particularly athletic`__ and was a bit prone to be nervous or shy in new situations , especially in situations where there was a physical risk .                                                                                                           |
| **`pcc_eng_00_039.9610_x0629353_15:52-53-54`** | I am a black belt , and I spend most of my time when I am practicing taekwondo around adults , many of which are black belts , I often forget how hard it can be to learn good form for kicks , especially if you are a young child and not __`particularly athletic`__ . |


17. _particularly flashy_

|                                                 | `token_str`                                                                                                                                                                                                                                    |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_029.5903_x0462387_04:3-4-5`**     | There 's nothing __`particularly flashy`__ about Illume Bistro , other than a menu composed by celebrity chef Bradley Ogden and an interior lighted , in places , by rainbow colors that rotate from yellow to blue to lavender to raspberry . |
| **`pcc_eng_10_074.2718_x1184341_18:4-5-6`**     | The animation is n't __`particularly flashy`__ , and looks more like a children 's book come to life than a big adventure film , but it suits the characters and the story beautifully .                                                       |
| **`pcc_eng_20_033.6695_x0528216_105:22-23-24`** | Karabacek 's offensive game is more north - south than east-west , which works well for the scoring winger who is not __`particularly flashy`__ .                                                                                              |
| **`pcc_eng_20_033.9119_x0532125_04:09-11-12`**  | All of the members play their instruments skillfully without being __`particularly flashy`__ , while singer / guitarist Arthur Shepherd has a big singing voice that ranges from gravelly rasp to soaring howl .                               |
| **`pcc_eng_14_081.6195_x1303328_05:4-6-7`**     | The Wire has never been __`particularly flashy`__ or self-conscious , which owes something to its roots in no-nonsense , unembellished journalism .                                                                                            |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/...

Samples saved as...
1. `neg_bigram_examples/particularly/particularly_likable_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_likeable_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_novel_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_comfortable_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_revolutionary_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_radical_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_fast_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_forthcoming_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_surprising_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_religious_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_new_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_wrong_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_remarkable_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_original_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_close_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_athletic_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_flashy_99ex.csv`

## 10. *inherently*

|                        |        `N` |      `f1` |   `adv_total` |
|:-----------------------|-----------:|----------:|--------------:|
| **NEGMIR_inherently**  |  1,701,929 |   291,732 |         5,133 |
| **NEGATED_inherently** | 72,839,589 | 3,173,660 |        47,803 |


|                                   |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:----------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGmir~inherently_improper**    |    18 |           142 |    0.83 |    1.63 |    63.49 |      3.09 |       14.91 |     18 |
| **NEGmir~inherently_illegal**     |    26 |           937 |    0.79 |    2.10 |    83.54 |      4.63 |       21.37 |     27 |
| **NEGany~inherently_wrong**       | 1,639 |       149,064 |    0.66 |    5.36 | 7,535.97 |    100.87 |    1,538.13 |  2,315 |
| **NEGmir~inherently_wrong**       | 1,513 |        20,880 |    0.66 |    4.08 | 3,787.53 |    313.00 |    1,200.00 |  1,826 |
| **NEGmir~inherently_bad**         |   148 |        10,261 |    0.62 |    2.86 |   342.53 |     32.23 |      115.77 |    188 |
| **NEGany~inherently_illegal**     |    59 |        30,194 |    0.60 |    3.51 |   252.59 |      4.01 |       54.99 |     92 |
| **NEGmir~inherently_better**      |    44 |        14,013 |    0.57 |    1.65 |    93.95 |     10.11 |       33.89 |     59 |
| **NEGany~inherently_bad**         |   794 |       429,537 |    0.56 |    4.62 | 3,270.68 |     56.95 |      737.05 |  1,307 |
| **NEGmir~inherently_evil**        |    58 |         1,271 |    0.41 |    1.18 |    85.70 |     16.97 |       41.03 |     99 |
| **NEGany~inherently_negative**    |    75 |        53,385 |    0.35 |    2.50 |   222.63 |      8.41 |       66.59 |    193 |
| **NEGany~inherently_evil**        |   358 |        22,706 |    0.28 |    2.81 |   905.80 |     48.93 |      309.07 |  1,123 |
| **NEGany~inherently_good**        |   283 |     1,681,795 |    0.20 |    2.21 |   554.72 |     51.28 |      231.72 |  1,177 |
| **NEGany~inherently_problematic** |    58 |        33,408 |    0.17 |    1.17 |    98.70 |     12.07 |       45.93 |    277 |


1. _inherently improper_

|                                                | `token_str`                                                                                                                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_034.9912_x0549040_3:23-24-25`**  | However , the court decided to take the approach of a substantial minority of states , and concluded that " it is not __`inherently improper`__ for a court to consider the possibility of inheritance in some cases . |
| **`nyt_eng_20070714_0032_29:7-8-9`**           | there is , of course , nothing __`inherently improper`__ about flipping properties for profit ; witness the spate of television shows like `` Flip That House . ''                                                     |
| **`pcc_eng_12_082.9270_x1323663_15:13-14-15`** | But even if we concede that counting the world 's Lutherans is not __`inherently improper`__ , doubts remain as to whether it is possible .                                                                            |
| **`pcc_eng_test_2.01516_x18509_38:3-4-5`**     | There is nothing __`inherently improper`__ about a subject in a criminal investigation seeking a pardon from a president given the president 's wide latitude in granting them .                                       |
| **`pcc_eng_07_020.9121_x0321975_55:16-17-18`** | Law firms advance expenses for clients as a matter of course , so there 's nothing __`inherently improper`__ about a lawyer covering a particular payment and then being reimbursed for it .                           |


2. _inherently illegal_

|                                                | `token_str`                                                                                                                                                                          |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19980311_0164_15:5-6-7`**           | becoming a monopoly is not __`inherently illegal`__ .                                                                                                                                |
| **`pcc_eng_15_097.1646_x1554298_14:5-6-7`**    | A prohibited device is not __`inherently illegal`__ in Canada but it does require an uncommon and very specific prohibited device license for its possession , use , and transport . |
| **`pcc_eng_03_005.3203_x0069828_46:10-11-12`** | Taking that difference one step further , there was nothing __`inherently illegal`__ in the quest for information on Manafort and how that might link Donald Trump to Russia .       |
| **`pcc_eng_12_065.4099_x1041138_10:09-10-11`** | Unlike American mafia organizations , the yakuza are not __`inherently illegal`__ despite their various illegal activities .                                                         |
| **`pcc_eng_14_038.6784_x0608659_17:19-20-21`** | The foundation , while accepting his resignation , quoted from the indictment which said that " Bitcoin are not __`inherently illegal`__ and have known legitimate uses . "          |


3. _inherently wrong_

|                                              | `token_str`                                                                                                                                                                                                                                  |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_070.5626_x1123983_40:4-5-6`**  | " There 's nothing __`inherently wrong`__ with a core review -- but you have to do it right . "                                                                                                                                              |
| **`pcc_eng_25_081.9758_x1310817_030:5-6-7`** | Moreover , there 's nothing __`inherently wrong`__ with current and potential college students earning money through part-time jobs , be it jobs that involve moving furniture , frothing milk , or hammering forehands down the line .      |
| **`pcc_eng_18_001.9162_x0014936_013:3-4-5`** | There is nothing __`inherently wrong`__ with making a car from stainless steel -- the material was n't the problem .                                                                                                                         |
| **`pcc_eng_05_004.5268_x0057351_11:5-6-7`**  | While there is certainly nothing __`inherently wrong`__ with anti-racist activism of any stripe , there is very little that can be learned from how Class Three Racism affects the most powerful class of African Americans .                |
| **`pcc_eng_23_030.6981_x0479490_22:4-5-6`**  | There may be nothing __`inherently wrong`__ with the syrup bottles that flavor up several liters of seltzer , but Caps are cleaner , easier , and more in tune with what consumers associate with single -serve premium beverage platforms . |


4. _inherently bad_

|                                                 | `token_str`                                                                                                                                                                                                      |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_068.6992_x1095841_220:08-13-14`** | And in each case , it is n't that any choice is __`inherently bad`__ , it is that it depends on what we are prepared for , what skills we want to emphasize , what balance we hope to find .                     |
| **`pcc_eng_11_099.3683_x1592377_45:3-4-5`**     | There 's nothing __`inherently bad`__ about the game , but nothing really stands out as fresh either .                                                                                                           |
| **`pcc_eng_22_071.8210_x1144668_18:08-09-10`**  | It 's a shame because there 's nothing __`inherently bad`__ about 3D , and yet after eight years of what should have been the technology 's boom , few filmmakers and studios were able to do anything with it . |
| **`pcc_eng_17_076.9586_x1227494_01:4-5-6`**     | Insurance companies are not __`inherently bad`__ or inherently good .                                                                                                                                            |
| **`pcc_eng_24_029.3144_x0457872_14:3-8-9`**     | It 's not that high-mileage running is __`inherently bad`__ .                                                                                                                                                    |


5. _inherently better_

|                                              | `token_str`                                                                                                                                                                                         |
|:---------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_084.9393_x1358382_20:3-4-5`**  | Professionals are not __`inherently better`__ or smarter than amateurs , but they are less likely to be subject to perverse incentives that reward them for being grossly wrong over and over .     |
| **`pcc_eng_15_043.9799_x0694897_69:3-4-5`**  | One is n't __`inherently better`__ than any other , but breaking down stigmas and misconceptions around entrepreneurship allows people to more freely move to where their talents are best suited . |
| **`pcc_eng_29_001.1996_x0003206_30:3-4-5`**  | A is not __`inherently better`__ than Realtor B .                                                                                                                                                   |
| **`pcc_eng_val_1.9320_x15122_12:09-10-11`**  | It alluded to a more traditional -- if not __`inherently better`__ -- style of filmmaking , with models and replicas in lieu of ' dense ' CGI .                                                     |
| **`pcc_eng_09_038.1910_x0601901_146:4-5-6`** | One technique is not __`inherently better`__ than the other and each depends upon how you present and your dentist 's skills .                                                                      |


6. _inherently evil_

|                                                 | `token_str`                                                                                                                                   |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_002.8254_x0029540_07:14-15-16`**  | First , this portion of Scripture is clear that the physical world is not __`inherently evil`__ .                                             |
| **`pcc_eng_22_013.1966_x0196846_084:11-12-13`** | Because maybe , while nature in and of itself is n't __`inherently evil`__ , humanity is ?                                                    |
| **`pcc_eng_20_036.9435_x0581030_094:20-21-22`** | Violets need to realize that being prosperous can enable them to accomplish their missions here and that money is not __`inherently evil`__ . |
| **`pcc_eng_18_045.9761_x0727903_134:3-4-5`**    | There is nothing __`inherently evil`__ about snakes or any other animal for that matter .                                                     |
| **`pcc_eng_03_003.7486_x0044244_56:7-8-9`**     | He is a marvelous antagonist , not __`inherently evil`__ , but deluded in his attempts to justify his actions .                               |


7. _inherently negative_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_014.6210_x0220029_30:10-11-12`** | You see , each one of those failures is not __`inherently negative`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_05_081.8953_x1309315_05:26-27-28`** | In my previous post I discussed how to emotions could be used in magic and made the point that an emotion such as anger is not __`inherently negative`__ .                                                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_02_004.9962_x0064467_037:5-6-7`**   | It is neither insidious nor __`inherently negative`__ by artifice ; rather , it is the most natural of sensibilities , arising from a knowledge that reliance upon one another not only acknowledges and validates the vows of matrimony , but moreover , the eternal commitment each makes to the other forever forges the bonds of undiluted friendship , like kindred spirits floating in some ethereal universe unperturbed by distractions of consternation consecrated upon the altar of destruction . |
| **`pcc_eng_23_006.6814_x0091752_58:7-8-9`**    | Anger , for example , is not __`inherently negative`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_10_028.9549_x0451869_10:20-21-22`** | This is because unemployment checks are a type of benefit intended for individuals who need it ; there 's nothing __`inherently negative`__ about seeking a financial cushion following job loss .                                                                                                                                                                                                                                                                                                           |


8. _inherently good_

|                                                | `token_str`                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_087.1201_x1392819_060:4-5-6`**   | Debt itself is not __`inherently good`__ or bad .                                                                                  |
| **`pcc_eng_18_007.8311_x0110590_11:20-24-25`** | You are always there to aid in times of need , but you are also smart enough to realize not all people are __`inherently good`__ . |
| **`pcc_eng_01_067.2942_x1072371_43:5-6-7`**    | Note that this is not __`inherently good`__ or bad .                                                                               |
| **`pcc_eng_09_004.6583_x0059430_05:3-4-5`**    | Abstractions are n't __`inherently good`__ .                                                                                       |
| **`pcc_eng_24_105.6788_x1693618_099:7-8-9`**   | The problem is , people are n't __`inherently good`__ .                                                                            |


9. _inherently problematic_

|                                                 | `token_str`                                                                                                            |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_013.3608_x0199808_21:3-8-9`**     | It 's not that the cross-cutting is __`inherently problematic`__ .                                                     |
| **`pcc_eng_03_004.1230_x0050261_23:14-15-16`**  | As noted at the beginning of this article , multi-level marketing organizations are n't __`inherently problematic`__ . |
| **`pcc_eng_04_006.5718_x0090170_21:5-6-7`**     | Patent pools themselves are n't __`inherently problematic`__ .                                                         |
| **`pcc_eng_28_027.5897_x0429485_074:08-09-10`** | Balanced literacy as an instructional model is not __`inherently problematic`__ .                                      |
| **`pcc_eng_25_041.4217_x0654254_40:04-09-10`**  | " It 's not that pre-made forms are __`inherently problematic`__ , " she says .                                        |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/...

Samples saved as...
1. `neg_bigram_examples/inherently/inherently_improper_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_illegal_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_wrong_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_bad_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_better_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_evil_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_negative_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_good_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_problematic_99ex.csv`

## 11. *terribly*

|                      |        `N` |      `f1` |   `adv_total` |
|:---------------------|-----------:|----------:|--------------:|
| **NEGATED_terribly** | 72,839,589 | 3,173,660 |        58,964 |
| **NEGMIR_terribly**  |  1,701,929 |   291,732 |         4,610 |


|                                 |   `f` |   `adj_total` |   `dP1` |   `LRC` |     `G2` |   `exp_f` |   `unexp_f` |   `f2` |
|:--------------------------------|------:|--------------:|--------:|--------:|---------:|----------:|------------:|-------:|
| **NEGany~terribly_surprising**  |   949 |        70,540 |    0.94 |    8.66 | 5,794.10 |     42.00 |      907.00 |    964 |
| **NEGany~terribly_uncommon**    |   103 |        11,312 |    0.94 |    6.33 |   625.85 |      4.57 |       98.43 |    105 |
| **NEGany~terribly_likely**      |   108 |       890,421 |    0.93 |    6.26 |   649.50 |      4.84 |      103.16 |    111 |
| **NEGany~terribly_productive**  |    64 |       102,361 |    0.91 |    5.39 |   376.84 |      2.92 |       61.08 |     67 |
| **NEGany~terribly_original**    |   199 |        37,594 |    0.90 |    6.41 | 1,150.48 |      9.24 |      189.76 |    212 |
| **NEGany~terribly_unusual**     |   146 |        71,234 |    0.90 |    6.17 |   847.05 |      6.75 |      139.25 |    155 |
| **NEGany~terribly_reliable**    |    51 |        90,598 |    0.90 |    4.99 |   296.70 |      2.35 |       48.65 |     54 |
| **NEGany~terribly_impressive**  |   196 |       178,051 |    0.86 |    5.97 | 1,087.64 |      9.50 |      186.50 |    218 |
| **NEGany~terribly_sure**        |    69 |       262,825 |    0.86 |    5.08 |   386.31 |      3.31 |       65.69 |     76 |
| **NEGany~terribly_different**   |   366 |       825,838 |    0.85 |    6.33 | 2,022.47 |     17.82 |      348.18 |    409 |
| **NEGmir~terribly_surprising**  |    67 |         2,662 |    0.83 |    4.07 |   236.35 |     11.48 |       55.52 |     67 |
| **NEGmir~terribly_original**    |    45 |         1,555 |    0.83 |    3.40 |   158.74 |      7.71 |       37.29 |     45 |
| **NEGmir~terribly_unusual**     |    24 |         2,302 |    0.83 |    2.23 |    84.66 |      4.11 |       19.89 |     24 |
| **NEGmir~terribly_special**     |    24 |        15,541 |    0.83 |    2.23 |    84.66 |      4.11 |       19.89 |     24 |
| **NEGmir~terribly_popular**     |    19 |         5,668 |    0.83 |    1.75 |    67.02 |      3.26 |       15.74 |     19 |
| **NEGmir~terribly_clear**       |    15 |         6,722 |    0.83 |    1.20 |    52.91 |      2.57 |       12.43 |     15 |
| **NEGmir~terribly_remarkable**  |    14 |         3,238 |    0.83 |    1.03 |    49.38 |      2.40 |       11.60 |     14 |
| **NEGmir~terribly_new**         |    69 |        12,836 |    0.80 |    3.66 |   225.93 |     12.17 |       56.83 |     71 |
| **NEGmir~terribly_interested**  |    39 |         8,255 |    0.74 |    2.36 |   112.46 |      7.37 |       31.63 |     43 |
| **NEGmir~terribly_interesting** |    56 |        12,447 |    0.68 |    2.44 |   145.16 |     11.31 |       44.69 |     66 |


1. _terribly surprising_

|                                                | `token_str`                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_034.2598_x0538167_39:3-4-5`**    | Revolutions are not __`terribly surprising`__ in cases like these .                                                                                                                                                                       |
| **`pcc_eng_08_076.9677_x1229986_32:5-6-7`**    | Interesting news , but not __`terribly surprising`__ .                                                                                                                                                                                    |
| **`pcc_eng_11_016.0291_x0243237_28:3-4-5`**    | It 's not __`terribly surprising`__ that the deadbeats of Europe want access to the money of German taxpayers , but it is rather shocking that German politicians are willing to play this no-win game .                                  |
| **`pcc_eng_26_094.9685_x1519625_01:30-31-32`** | In retrospect , it should have seemed like the perfect fit and by proxy something that we should have expected so really , the announcement of Scribblenauts while perhaps not __`terribly surprising`__ , is still nonetheless welcome . |
| **`pcc_eng_15_009.4319_x0136213_06:6-7-8`**    | That 's why it 's not __`terribly surprising`__ that the New York Post is reporting that ESPN baseball analyst Steve Phillips has been making some really bad calls in his personal life .                                                |


2. _terribly uncommon_

|                                                | `token_str`                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_026.9821_x0419639_32:3-4-5`**    | Plums are n't __`terribly uncommon`__ , but not a lot of people are familiar with pluots .                                                                                                                                                |
| **`pcc_eng_22_084.5345_x1350322_60:40-41-42`** | Naturally given how powerless inmates are to do anything about it , cases of identify theft , the entrusted person running off with all the inmate 's money and not paying any of the bills and the like is n't __`terribly uncommon`__ . |
| **`pcc_eng_14_031.3481_x0490431_40:3-4-5`**    | It 's not __`terribly uncommon`__ for the entire party to be decimated in a seemingly - routine random encounter , especially if they 're just trying to breeze their way through an encounter .                                          |
| **`pcc_eng_11_064.8935_x1034009_14:5-6-7`**    | Although lunar-planetary partnerships are not __`terribly uncommon`__ , Boberg said it is the specific planet 's presence that makes this an occasion to note .                                                                           |
| **`pcc_eng_20_081.8641_x1306459_03:3-4-5`**    | This is n't __`terribly uncommon`__ , but this also was a school nightmare .                                                                                                                                                              |


3. _terribly likely_

|                                                | `token_str`                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_028.0402_x0437306_18:09-10-11`** | It 's slightly more possible -- but still not __`terribly likely`__ -- that Whedon will resurrect his dead script Goners , which was a Buffy - esque story of a young woman who gains superpowers and faces ultimate horror . |
| **`pcc_eng_02_092.0224_x1471611_38:6-7-8`**    | But then , victory is n't __`terribly likely`__ .                                                                                                                                                                             |
| **`pcc_eng_26_004.7209_x0059956_32:3-4-5`**    | This is not __`terribly likely`__ to help reduce long-term , chronic anxiety , but it is unlikely to hurt either .                                                                                                            |
| **`pcc_eng_03_046.4181_x0735823_07:6-7-8`**    | In fact , that 's not __`terribly likely`__ .                                                                                                                                                                                 |
| **`pcc_eng_09_007.8954_x0111744_06:3-4-5`**    | It 's not __`terribly likely`__ that he 's going to be a successful NHL player .                                                                                                                                              |


4. _terribly productive_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                            |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_026.8551_x0418312_41:20-22-23`**  | Purdue was far more desperate in the secondary a year ago , and Williams had gone his whole career without being __`terribly productive`__ at his position of choice .                                                                                                                                                                 |
| **`pcc_eng_19_079.8810_x1274310_023:10-11-12`** | So I 'm not doing much or at least nothing __`terribly productive`__ : trying to solve a lot of computer problems , dealing with a lot of broken appliances and thus shopping for replacements ( ick ) , a lot of having to deal with ornery contractors , a couple of doctor appointments , air bag replacements , things like that . |
| **`pcc_eng_00_005.4608_x0072059_16:22-23-24`**  | I posted to Facebook that my air conditioner always has reminded me of a mediocre co-worker : inefficient , cranky , not __`terribly productive`__ , and doing just enough to get by .                                                                                                                                                 |
| **`pcc_eng_08_070.8614_x1131127_15:08-09-10`**  | Even with the home runs he 's not __`terribly productive`__ , some team will find a place for him given his versatility and defense but they should n't expect much offensively .                                                                                                                                                      |
| **`pcc_eng_24_077.0033_x1229492_007:34-36-37`** | We also , a few years ago , had an opinion in terms of transatlantic relations , but our experience in terms of looking at things from a transatlantic point of view has not been __`terribly productive`__ .                                                                                                                          |


5. _terribly reliable_

|                                                | `token_str`                                                                                                                                                                                                             |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20050227_0090_4:1-7-8`**            | not that the suicide watch was __`terribly reliable`__ ; it depended in part on inmates paid 39 cents an hour to check on their suicidal peers .                                                                        |
| **`pcc_eng_18_001.6036_x0009816_099:7-8-9`**   | In my experience , psychics are not __`terribly reliable`__ , but they sometimes provide valid data points along with what they acquire through your answering their questions or what their own imagination produced . |
| **`pcc_eng_21_093.6106_x1496377_02:6-7-8`**    | But the six-legged soldiers were n't __`terribly reliable`__ by JOSEPH TREVITHICK Mao Tse -Tung famously wrote in On Guerrilla Warfare that guerrillas are proverbial fish who have ...                                 |
| **`pcc_eng_22_008.7482_x0124989_03:20-22-23`** | We all love Sigourney Weaver , even when she stars in crap like The Assignment , but she has n't been __`terribly reliable`__ when it comes to these Avatar sequels .                                                   |
| **`pcc_eng_11_016.2035_x0246016_25:14-18-19`** | Many of us depend on public transit in its many forms , and none of it is __`terribly reliable`__ .                                                                                                                     |


6. _terribly unusual_

|                                               | `token_str`                                                                                                                                                                                                                                                                                |
|:----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_051.5427_x0818147_38:5-6-7`**   | And 10 months is not __`terribly unusual`__ in mathematics ...                                                                                                                                                                                                                             |
| **`pcc_eng_08_086.0228_x1376438_03:4-6-7`**   | That development would not be __`terribly unusual`__ .                                                                                                                                                                                                                                     |
| **`pcc_eng_13_088.4614_x1413593_1:35-36-37`** | Display Wifi Password in Mac via Terminal Given the complexity of some wi-fi network passwords combined with the general infrequency of entering them and that they 're typically saved on use , it 's not __`terribly unusual`__ to forget what a specific routers wireless password is . |
| **`pcc_eng_01_044.4064_x0701249_14:3-4-5`**   | This is n't __`terribly unusual`__ in itself ; since 1952 , Congress has established a " national day of prayer " and most other states do the same thing .                                                                                                                                |
| **`pcc_eng_27_007.1798_x0099343_07:3-5-6`**   | It would not be __`terribly unusual`__ to see a 70 year old woman sans brassiere strut by in the latest fashions , sporting an air that says she owns the sidewalk and possibly much of this part of town .                                                                                |


7. _terribly original_

|                                                | `token_str`                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000109_0032_38:27-29-30`**        | to Stein , the fact that he reveals intimate , seemingly eccentric but actually quite normal aspects of his personality to the readers of Time does not seem __`terribly original`__ . |
| **`pcc_eng_01_097.7344_x1563861_033:2-3-4`**   | While not __`terribly original`__ , I found these characters compelling .                                                                                                              |
| **`pcc_eng_11_083.5065_x1335366_5:5-6-7`**     | Though the name is n't __`terribly original`__ , the fact that there are still a few ways to raft 2 for the price of 1 is .                                                            |
| **`pcc_eng_25_014.7857_x0222916_145:3-4-5`**   | THERE is nothing __`terribly original`__ about Carrillo 's ideas .                                                                                                                     |
| **`pcc_eng_27_006.6762_x0091245_11:13-14-15`** | The movie gets bogged down in its anti-technology message , which is n't __`terribly original`__ .                                                                                     |


8. _terribly sure_

|                                                 | `token_str`                                                                                 |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------|
| **`pcc_eng_28_048.7232_x0772129_19:6-7-8`**     | ( Note : I 'm not __`terribly sure`__ if it was the game that made me feel sick .           |
| **`pcc_eng_12_086.3176_x1378617_35:3-4-5`**     | I 'm not __`terribly sure`__ I engage in this examination .                                 |
| **`pcc_eng_05_015.0048_x0226944_160:11-13-14`** | The minister cannot really provide any information ; he is not really __`terribly sure`__ . |
| **`pcc_eng_04_083.0535_x1325528_2:3-4-5`**      | I 'm not __`terribly sure`__ how many people can actually help me with my question .        |
| **`pcc_eng_22_006.7896_x0093389_215:4-5-6`**    | " I am not __`terribly sure`__ , " I said .                                                 |


9. _terribly impressive_

|                                                 | `token_str`                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_099.1827_x1587312_54:18-19-20`**  | Yet even here Kramer is forced to admit in terms of tangible results that his record was not __`terribly impressive`__ .                                                                                 |
| **`pcc_eng_08_072.5256_x1158007_25:28-29-30`**  | It 's possible WWE enthusiasts might thrill to a game that depicts the heroes of the squared circle , though really , the graphics are cartoonish and not __`terribly impressive`__ .                    |
| **`pcc_eng_14_002.4239_x0023104_154:19-20-21`** | So , reluctantly , he went back out and he did his best - which back then was n't __`terribly impressive`__ - to fight back the dark .                                                                   |
| **`pcc_eng_26_036.5383_x0574399_16:08-09-10`**  | The sped- up chase through Paris is n't __`terribly impressive`__ as car chases go , but it 's still an E-type Jaguar chasing Senta Berger through the streets of Sixties Paris , so that 's something ! |
| **`pcc_eng_03_087.0287_x1393111_25:3-4-5`**     | There 's nothing __`terribly impressive`__ about that .                                                                                                                                                  |


10. _terribly different_

|                                                 | `token_str`                                                                                                                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_087.6016_x1401792_48:11-12-13`**  | What we learned was that shooting an indie pilot is not __`terribly different`__ than shooting the micro-budget features that find their way to film festivals . "                                                                                                        |
| **`nyt_eng_20000328_0115_60:5-6-7`**            | the hectic lifestyle is n't __`terribly different`__ from investment banking .                                                                                                                                                                                            |
| **`pcc_eng_05_032.2207_x0505754_117:26-28-29`** | Once the layout is established for this world and we 've kind of blocked in the shots , the work flow for the animators is n't necessarily __`terribly different`__ than what it usually is .                                                                             |
| **`apw_eng_20020731_0871_4:3-4-5`**             | reality was n't __`terribly different`__ , other than the fact that the huge steel boat I arrived in was filled with wet bars and television screens and that my first view of the land was of an enormous parking lot .                                                  |
| **`pcc_eng_03_038.1477_x0601633_10:22-26-27`**  | . . . Also , most of it did n't really look like ninja stuff so much as typical krotty ( not that they 're __`terribly different`__ combatively , but would n't ninja training involve more " remaining unseen " or " moving through difficult terrain " or something ? ) |


11. _terribly special_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_083.0387_x1327858_16:14-15-16`** | Though they act as a high- profile example , the Bush boys are n't __`terribly special`__ in their mixture of sects of Christianity .                                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_07_015.2012_x0229864_04:11-12-13`** | Just your basic folk - rock riff in A ; nothing __`terribly special`__ , right ?                                                                                                                                                                                                                                                                                                                                                           |
| **`pcc_eng_19_071.8832_x1144882_37:5-6-7`**    | The special effects are not __`terribly special`__ , though Les Bowie - Hammer 's top effects man for many years - performed miracles on the tiny budget , but Wordsworth 's shambling pathetic performance is memorable , and the film put the studio back on its feet and encouraged it to follow -on with many more man-into-monster movies , including the direct sequels Quatermass II ( 1957 ) and Quatermass And The Pit ( 1967 ) . |
| **`pcc_eng_11_064.8935_x1034009_12:15-16-17`** | " It 's a full moon and it 's real , but there 's nothing __`terribly special`__ or spectacular about it , " he said .                                                                                                                                                                                                                                                                                                                     |
| **`pcc_eng_22_004.2037_x0051958_047:7-8-9`**   | The chunky sauce was good but not __`terribly special`__ .                                                                                                                                                                                                                                                                                                                                                                                 |


12. _terribly popular_

|                                                 | `token_str`                                                                                                                                                                   |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_071.1107_x1134121_23:11-12-13`**  | However , it seems like the arcade game itself was n't __`terribly popular`__ and is going away , so maybe there 's plenty of blame to go around .                            |
| **`pcc_eng_09_082.8117_x1323529_068:24-25-26`** | This kind of market theory of artistic value puts our music on a slippery slope , as classical music as a whole is not __`terribly popular`__ with a large , general public . |
| **`nyt_eng_20070526_0069_23:4-5-6`**            | things Californian are not __`terribly popular`__ with Nevada residents , but Schneider says he has a way around that .                                                       |
| **`pcc_eng_17_070.9176_x1129636_14:13-14-15`**  | The non-cabbage bits added pleasant flavor contrast , although the beans were n't __`terribly popular`__ .                                                                    |
| **`pcc_eng_03_003.6324_x0042370_59:14-15-16`**  | I would n't go below two , but right now graveyard decks are n't __`terribly popular`__ .                                                                                     |


13. _terribly clear_

|                                                 | `token_str`                                                                                                                                                                                                               |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_038.3868_x0603979_3:4-5-6`**      | " It 's not __`terribly clear`__ to me that my actions were explicitly done for ' peace , ' " Manning wrote in a statement to the Guardian .                                                                              |
| **`pcc_eng_15_014.9744_x0225589_356:17-18-19`** | She also seems to have some kind of bandage across her forehead , though it 's not __`terribly clear`__ given she 's wearing an elaborate hat .                                                                           |
| **`pcc_eng_11_007.4004_x0103608_029:4-5-6`**    | This picture is n't __`terribly clear`__ , but this is a rat hole at the perimeter fence of my chicken run .                                                                                                              |
| **`pcc_eng_09_005.4795_x0072752_067:16-17-18`** | A two -gallon petrol can is fitted to the offside running board and , although not __`terribly clear`__ , there is also an AA badge positioned just ahead of the Motometer ( temperature gauge ) on top of the radiator . |
| **`pcc_eng_17_072.4313_x1154287_17:3-4-5`**     | It 's not __`terribly clear`__ how much of a boost most of the ensemble cast of " The Avengers " got from the film 's giant success .                                                                                     |


14. _terribly remarkable_

|                                                 | `token_str`                                                                                                                                                                                                |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_036.6025_x0574483_33:19-20-21`**  | What Price did manage to do was shake off 60 minutes where he was thoroughly outplayed by a not __`terribly remarkable`__ goalie .                                                                         |
| **`pcc_eng_21_019.6636_x0301381_06:6-7-8`**     | By itself , this is n't __`terribly remarkable`__ or exciting , because a single finger touching the surface in question does n't create a signature that 's unique enough for individual identification . |
| **`pcc_eng_27_068.9149_x1098061_42:1-5-6`**     | None of this is __`terribly remarkable`__ in the world of the book .                                                                                                                                       |
| **`pcc_eng_18_010.9384_x0160799_059:08-09-10`** | I have lots of little plans but nothing __`terribly remarkable`__ .                                                                                                                                        |
| **`pcc_eng_13_037.5812_x0591439_11:11-12-13`**  | It 's a good look for the figure , though not __`terribly remarkable`__ .                                                                                                                                  |


15. _terribly new_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000302_0121_10:7-8-9`**           | it 's a variation on the not __`terribly new`__ concept of the software emulator , a computer program that makes one computer act as if it were another computer .                                                                                                                                         |
| **`pcc_eng_02_048.3682_x0766345_8:1-2-3`**     | Nothing __`terribly new`__ here , except that Musk 's vision is being more widely disseminated .                                                                                                                                                                                                           |
| **`pcc_eng_07_053.2546_x0844707_02:14-15-16`** | Aaaand it 's time for another timely review of a game that 's not __`terribly new`__ ( it 's been out about 6 months now ) .                                                                                                                                                                               |
| **`apw_eng_20090506_0541_38:4-5-6`**           | but it 's not __`terribly new`__ , just getting the word out and labeling it . ''                                                                                                                                                                                                                          |
| **`pcc_eng_29_082.7561_x1320397_15:27-28-29`** | Titles like " Crack Headed Woman , " " I Got A Woman , " and " Oo Wee Pretty Baby " define the territory - nothing __`terribly new`__ or innovative on display - but Hinds and company put their all into every tune , with fervently energetic performances that give every cut an irresistible urgency . |


16. _terribly interested_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_010.8196_x0158891_21:3-4-5`**    | She 's not __`terribly interested`__ in writing for fun at home , though .                                                                                                                                                                                                                                                  |
| **`pcc_eng_08_075.1040_x1199825_86:3-4-5`**    | Clute is n't __`terribly interested`__ in digital writing .                                                                                                                                                                                                                                                                 |
| **`pcc_eng_25_009.0421_x0130317_09:6-7-8`**    | But Aly & AJ are n't __`terribly interested`__ in upholding expectations :                                                                                                                                                                                                                                                  |
| **`pcc_eng_28_065.2257_x1039269_34:3-4-5`**    | I was n't __`terribly interested`__ by the film when it first came out ; having seen it , I made sure that I 'd catch Catching Fire on the big screen .                                                                                                                                                                     |
| **`pcc_eng_21_016.8492_x0255882_06:16-17-18`** | Sorry , friends back home , but if you 're very honest , you were n't __`terribly interested`__ in hearing any more about this experience ; what 's more , it turns out that after thinking of almost nothing but the same two papers for two months , one really does n't want to think about them for a Good Long While . |


17. _terribly interesting_

|                                                 | `token_str`                                                                                                                                                                                                                                                                    |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_042.4799_x0671422_016:07-13-14`** | But such a legal status would not , by itself , be __`terribly interesting`__ philosophically .                                                                                                                                                                                |
| **`pcc_eng_09_002.9666_x0031828_39:11-12-13`**  | Her playing up to that point had been efficient but not __`terribly interesting`__ .                                                                                                                                                                                           |
| **`pcc_eng_11_091.6585_x1467486_29:09-10-11`**  | This , in and of itself , is not __`terribly interesting`__ .                                                                                                                                                                                                                  |
| **`pcc_eng_28_074.0636_x1181707_032:13-15-16`** | What I came to realize about Orleans was that the decisions were n't always __`terribly interesting`__ to me after a while .                                                                                                                                                   |
| **`pcc_eng_05_083.6032_x1336890_060:34-35-36`** | Hader 's Aaron is a perfectly nice , likable guy ( his scene playing one - on- one basketball with Le Bron James is a stone- cold classic ) , but he 's not __`terribly interesting`__ , generous to a fault , and definitely not the kind of guy that Amy would be drawn to . |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/...

Samples saved as...
1. `neg_bigram_examples/terribly/terribly_surprising_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_uncommon_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_likely_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_productive_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_reliable_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_unusual_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_original_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_sure_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_impressive_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_different_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_special_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_popular_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_clear_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_remarkable_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_new_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_interested_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_interesting_99ex.csv`

