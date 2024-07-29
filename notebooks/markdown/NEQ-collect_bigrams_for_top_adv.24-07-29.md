# `NEQ`: Collect bigrams corresponding to top adverbs


```python
from pathlib import Path
from pprint import pprint

import pandas as pd

from source.utils.associate import TOP_AM_DIR, adjust_assoc_columns
# from source.utils.dataframes import update_assoc_index as update_index
from source.utils.general import (confirm_dir, print_iter, #snake_to_camel,
                                  timestamp_today)
from am_notebooks import *

ADV_FLOOR = 5000
K = 8

DATA_DATE = timestamp_today()
TAG = 'NEQ'
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
confirm_dir(TOP_AM_TAG_DIR)

data_top = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / data_top
confirm_dir(OUT_DIR)

# for loading `polar/*/bigram/*` tables
bigram_floor = 25
mirror_floor = 5
```

## Set columns and diplay settings


```python
# FOCUS = ['f',
#          'am_p1_given2', 'am_p1_given2_simple', 
#          'conservative_log_ratio',
#          'am_log_likelihood',
#           'mutual_information',
#          'am_odds_ratio_disc', 't_score',
#          'N', 'f1', 'f2', 'E11', 'unexpected_f',
#          'l1', 'l2', 
#          'adv', 'adv_total', 'adj', 'adj_total']

if TAG == 'NEQ': 
    FOCUS.extend(['am_p2_given1_simple', 'am_p2_given1'])
pd.set_option('display.max_colwidth', 30)
pd.set_option('display.max_columns', 9)
pd.set_option('display.width', 120)
pd.set_option("display.precision", 2)
pd.set_option("styler.format.precision", 2)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.2f}'.format)
FOCUS
```




    ['f',
     'am_p1_given2',
     'am_p1_given2_simple',
     'conservative_log_ratio',
     'am_log_likelihood',
     'mutual_information',
     'am_odds_ratio_disc',
     't_score',
     'N',
     'f1',
     'f2',
     'E11',
     'unexpected_f',
     'l1',
     'l2',
     'adv',
     'adv_total',
     'adj',
     'adj_total',
     'am_p2_given1_simple',
     'am_p2_given1']



(MOVED the following to `./am_notebooks.py`)

## Load data


```python
bigram_dfs = load_bigram_dfs(
    locate_bigram_am_paths(TAG, mirror_floor, bigram_floor))
# combined_am_csv = None
# try:
#     combined_am_csv = tuple(OUT_DIR.glob(
#                    f'{TAG}-Top{K}_NEG-ADV_combined-{ADV_FLOOR}*.{DATA_DATE or timestamp_today()}.csv'))[0]
# except IndexError:
#     combined_am_csv = tuple(TOP_AM_TAG_DIR.rglob(
#         f'{TAG}-Top{K}_NEG-ADV_combined*.csv'))[0]
top_adv_am = None
while top_adv_am is None:
    try:
        combined_am_csv = OUT_DIR / \
            f'{data_top}_NEG-ADV_combined-{ADV_FLOOR}.{DATA_DATE}.csv'
        top_adv_am = pd.read_csv(combined_am_csv, index_col='adv')
    except FileNotFoundError:
        DATA_DATE = DATA_DATE[:-1]+str(int(DATA_DATE[-1])-1)

top_adv_am = adjust_assoc_columns(
    pd.read_csv(combined_am_csv, index_col='adv'))
print(f'Loaded from: "{combined_am_csv}"')

main_cols_ordered = pd.concat((*[top_adv_am.filter(like=m).columns.to_series() for m in ('LRC', 'P1', 'P2', 'G2')],
                               *[top_adv_am.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2']])
                              ).to_list()
top_adv_am
```

    {'RBdirect': PosixPath('/share/compling/projects/sanpi/results/assoc_df/polar/RBdirect/bigram/extra/polarized-bigram_NEQ-direct_min25x_extra.parq'),
     'mirror': PosixPath('/share/compling/projects/sanpi/results/assoc_df/polar/mirror/bigram/extra/polarized-bigram_NEQ-mirror_min5x_extra.parq')}
    Loaded from: "/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-07-29.csv"





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
      <th>key_SET</th>
      <th>f_SET</th>
      <th>dP1_SET</th>
      <th>P1_SET</th>
      <th>...</th>
      <th>r_f_MIR</th>
      <th>r_N_MIR</th>
      <th>r_f1_MIR</th>
      <th>r_f2_MIR</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>necessarily</th>
      <td>NEGany~necessarily</td>
      <td>42595</td>
      <td>0.50</td>
      <td>0.99</td>
      <td>...</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>that</th>
      <td>NEGany~that</td>
      <td>164768</td>
      <td>0.50</td>
      <td>0.99</td>
      <td>...</td>
      <td>0.03</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>NEGany~exactly</td>
      <td>43813</td>
      <td>0.49</td>
      <td>0.98</td>
      <td>...</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>any</th>
      <td>NEGany~any</td>
      <td>15384</td>
      <td>0.45</td>
      <td>0.95</td>
      <td>...</td>
      <td>0.07</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.07</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>NEGany~remotely</td>
      <td>5661</td>
      <td>0.42</td>
      <td>0.92</td>
      <td>...</td>
      <td>0.33</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.32</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>NEGany~yet</td>
      <td>51867</td>
      <td>0.47</td>
      <td>0.96</td>
      <td>...</td>
      <td>0.01</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>NEGany~immediately</td>
      <td>56099</td>
      <td>0.47</td>
      <td>0.97</td>
      <td>...</td>
      <td>0.01</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>NEGany~particularly</td>
      <td>55527</td>
      <td>0.23</td>
      <td>0.73</td>
      <td>...</td>
      <td>0.17</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.13</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>NEGany~inherently</td>
      <td>6743</td>
      <td>0.28</td>
      <td>0.78</td>
      <td>...</td>
      <td>0.42</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.39</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>NEGany~terribly</td>
      <td>17949</td>
      <td>0.41</td>
      <td>0.91</td>
      <td>...</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.11</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>NEGany~ever</td>
      <td>5932</td>
      <td>0.05</td>
      <td>0.55</td>
      <td>...</td>
      <td>0.79</td>
      <td>0.09</td>
      <td>0.09</td>
      <td>0.44</td>
    </tr>
  </tbody>
</table>
<p>11 rows × 53 columns</p>
</div>




```python
[
        *pd.Series(main_cols_ordered).str.replace(
            r'mean_|_SET|_MIR', '', regex=True)
        .drop_duplicates().to_list(),
        'adv_total', 'adj_total'
        # 't', 'MI'
    ]
```




    ['LRC',
     'dP1',
     'P1',
     'P2',
     'dP2',
     'G2',
     'f',
     'f1',
     'f2',
     'adv_total',
     'adj_total']




```python
samples_dict, bigram_k = show_adv_bigrams(
    K, top_adv_am, bigram_dfs,
    column_list=[
        *pd.Series(main_cols_ordered).str.replace(
            r'mean_|_SET|_MIR', '', regex=True)
        .drop_duplicates().to_list(),
        'adv_total', 'adj_total'
        # 't', 'MI'
    ], focus_cols=FOCUS
)
```

    ## Top 10 "most negative" bigrams corresponding to top 8 adverbs
    
    2024-07-29
    
    ### 1. _necessarily_
    
    
    #### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                   |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~necessarily_indicative** |    6.29 |    0.50 |   1.00 |   0.00 |    0.00 | 1,925.89 | 1,389 | 3,173,660 |  1,389 |        42,886 |         2,313 |
    | **NEGany~necessarily_easy**       |    5.67 |    0.50 |   1.00 |   0.00 |    0.00 | 1,260.28 |   909 | 3,173,660 |    909 |        42,886 |       108,923 |
    | **NEGany~necessarily_new**        |    4.74 |    0.50 |   1.00 |   0.00 |    0.00 |   668.24 |   482 | 3,173,660 |    482 |        42,886 |        21,538 |
    | **NEGany~necessarily_surprising** |    4.23 |    0.50 |   1.00 |   0.00 |    0.00 |   471.36 |   340 | 3,173,660 |    340 |        42,886 |        18,776 |
    | **NEGany~necessarily_enough**     |    3.93 |    0.50 |   1.00 |   0.00 |    0.00 |   386.79 |   279 | 3,173,660 |    279 |        42,886 |        27,603 |
    | **NEGany~necessarily_bad**        |    6.31 |    0.50 |   1.00 |   0.00 |    0.00 | 2,814.04 | 2,059 | 3,173,660 |  2,062 |        42,886 |       119,509 |
    | **NEGany~necessarily_true**       |    6.16 |    0.50 |   1.00 |   0.00 |    0.00 | 4,330.74 | 3,232 | 3,173,660 |  3,245 |        42,886 |        34,967 |
    | **NEGany~necessarily_better**     |    6.07 |    0.50 |   1.00 |   0.00 |    0.00 | 2,564.81 | 1,887 | 3,173,660 |  1,891 |        42,886 |        50,827 |
    | **NEGany~necessarily_aware**      |    3.48 |    0.50 |   1.00 |   0.00 |    0.00 |   285.59 |   206 | 3,173,660 |    206 |        42,886 |        28,973 |
    | **NEGany~necessarily_related**    |    5.14 |    0.50 |   1.00 |   0.00 |    0.00 | 1,013.51 |   741 | 3,173,660 |    742 |        42,886 |        14,260 |
    
    
    #### Top 2 `mirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                              |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~necessarily_bad**   |    1.37 |    0.50 |   1.00 |   0.00 |    0.00 |  69.32 |    50 | 291,732 |     50 |           992 |         4,790 |
    | **NEGmir~necessarily_wrong** |    3.05 |    0.49 |   0.99 |   0.00 |    0.00 | 265.18 |   211 | 291,732 |    214 |           992 |         8,506 |
    
    
    ### 2. _that_
    
    
    #### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                            |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------|--------:|--------:|-------:|-------:|--------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~that_surprising** |    5.99 |    0.50 |   1.00 |   0.00 |    0.00 |  1,570.89 |  1,133 | 3,173,660 |  1,133 |       166,676 |        18,776 |
    | **NEGany~that_unusual**    |    5.77 |    0.50 |   1.00 |   0.00 |    0.00 |  1,354.57 |    977 | 3,173,660 |    977 |       166,676 |         7,412 |
    | **NEGany~that_exciting**   |    5.49 |    0.50 |   1.00 |   0.00 |    0.00 |  1,116.08 |    805 | 3,173,660 |    805 |       166,676 |        20,233 |
    | **NEGany~that_uncommon**   |    5.49 |    0.50 |   1.00 |   0.00 |    0.00 |  1,111.92 |    802 | 3,173,660 |    802 |       166,676 |         3,165 |
    | **NEGany~that_impressed**  |    5.25 |    0.50 |   1.00 |   0.00 |    0.00 |    944.15 |    681 | 3,173,660 |    681 |       166,676 |        12,138 |
    | **NEGany~that_hard**       |    7.68 |    0.50 |   1.00 |   0.00 |    0.00 | 13,602.42 |  9,948 | 3,173,660 |  9,963 |       166,676 |        45,061 |
    | **NEGany~that_different**  |    7.18 |    0.50 |   1.00 |   0.00 |    0.00 |  8,895.12 |  6,534 | 3,173,660 |  6,547 |       166,676 |        80,643 |
    | **NEGany~that_great**      |    7.18 |    0.50 |   1.00 |   0.00 |    0.00 | 14,908.90 | 11,032 | 3,173,660 | 11,065 |       166,676 |        45,359 |
    | **NEGany~that_difficult**  |    7.06 |    0.50 |   1.00 |   0.00 |    0.00 |  7,569.00 |  5,560 | 3,173,660 |  5,571 |       166,676 |        61,490 |
    | **NEGany~that_big**        |    6.47 |    0.50 |   1.00 |   0.00 |    0.00 |  8,332.69 |  6,244 | 3,173,660 |  6,273 |       166,676 |        42,912 |
    
    
    #### Top 10 `mirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                            |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~that_close**      |    1.67 |    0.50 |   1.00 |   0.00 |    0.00 |  83.19 |    60 | 291,732 |     60 |         4,559 |         4,831 |
    | **NEGmir~that_happy**      |    1.03 |    0.50 |   1.00 |   0.00 |    0.00 |  56.84 |    41 | 291,732 |     41 |         4,559 |         5,463 |
    | **NEGmir~that_popular**    |    1.54 |    0.48 |   0.98 |   0.00 |    0.00 |  81.14 |    65 | 291,732 |     66 |         4,559 |         2,841 |
    | **NEGmir~that_simple**     |    3.67 |    0.48 |   0.98 |   0.00 |    0.00 | 580.44 |   474 | 291,732 |    483 |         4,559 |         7,465 |
    | **NEGmir~that_difficult**  |    1.16 |    0.48 |   0.98 |   0.00 |    0.00 |  63.56 |    52 | 291,732 |     53 |         4,559 |         4,854 |
    | **NEGmir~that_easy**       |    3.23 |    0.47 |   0.97 |   0.00 |    0.00 | 512.43 |   450 | 291,732 |    465 |         4,559 |         7,749 |
    | **NEGmir~that_great**      |    2.71 |    0.46 |   0.96 |   0.00 |    0.00 | 312.65 |   286 | 291,732 |    298 |         4,559 |         2,123 |
    | **NEGmir~that_good**       |    2.65 |    0.44 |   0.94 |   0.00 |    0.00 | 441.70 |   447 | 291,732 |    476 |         4,559 |        13,423 |
    | **NEGmir~that_big**        |    2.08 |    0.47 |   0.97 |   0.00 |    0.00 | 132.98 |   113 | 291,732 |    116 |         4,559 |         3,134 |
    | **NEGmir~that_interested** |    1.26 |    0.47 |   0.97 |   0.00 |    0.00 |  70.93 |    62 | 291,732 |     64 |         4,559 |         2,877 |
    
    
    ### 3. _exactly_
    
    
    #### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                               |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------|--------:|--------:|-------:|-------:|--------:|----------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~exactly_cheap**      |    5.27 |    0.50 |   1.00 |   0.00 |    0.00 |    958.01 |   691 | 3,173,660 |    691 |        44,503 |         6,591 |
    | **NEGany~exactly_surprising** |    4.61 |    0.50 |   1.00 |   0.00 |    0.00 |    610.01 |   440 | 3,173,660 |    440 |        44,503 |        18,776 |
    | **NEGany~exactly_subtle**     |    3.84 |    0.50 |   1.00 |   0.00 |    0.00 |    364.61 |   263 | 3,173,660 |    263 |        44,503 |         5,299 |
    | **NEGany~exactly_fair**       |    3.83 |    0.50 |   1.00 |   0.00 |    0.00 |    360.45 |   260 | 3,173,660 |    260 |        44,503 |         6,964 |
    | **NEGany~exactly_fun**        |    3.60 |    0.50 |   1.00 |   0.00 |    0.00 |    310.54 |   224 | 3,173,660 |    224 |        44,503 |        19,661 |
    | **NEGany~exactly_sure**       |    7.46 |    0.50 |   1.00 |   0.00 |    0.00 | 11,991.61 | 8,794 | 3,173,660 |  8,810 |        44,503 |       134,139 |
    | **NEGany~exactly_clear**      |    6.38 |    0.50 |   1.00 |   0.00 |    0.00 |  2,405.43 | 1,746 | 3,173,660 |  1,747 |        44,503 |        84,227 |
    | **NEGany~exactly_new**        |    6.03 |    0.50 |   1.00 |   0.00 |    0.00 |  1,885.86 | 1,371 | 3,173,660 |  1,372 |        44,503 |        21,538 |
    | **NEGany~exactly_easy**       |    5.67 |    0.50 |   1.00 |   0.00 |    0.00 |  1,463.43 | 1,066 | 3,173,660 |  1,067 |        44,503 |       108,923 |
    | **NEGany~exactly_hard**       |    3.46 |    0.50 |   1.00 |   0.00 |    0.00 |    281.43 |   203 | 3,173,660 |    203 |        44,503 |        45,061 |
    
    
    #### Top 2 `mirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~exactly_sure**  |    3.10 |    0.50 |   1.00 |   0.00 |    0.00 | 205.21 |   148 | 291,732 |    148 |           869 |         5,978 |
    | **NEGmir~exactly_clear** |    1.16 |    0.48 |   0.98 |   0.00 |    0.00 |  63.56 |    52 | 291,732 |     53 |           869 |         3,321 |
    
    
    ### 4. _any_
    
    
    #### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~any_younger**   |    3.80 |    0.50 |   1.00 |   0.00 |    0.00 |   353.52 |   255 | 3,173,660 |    255 |        16,238 |         1,784 |
    | **NEGany~any_nicer**     |    2.30 |    0.50 |   1.00 |   0.00 |    0.00 |   133.09 |    96 | 3,173,660 |     96 |        16,238 |           642 |
    | **NEGany~any_sweeter**   |    1.49 |    0.50 |   1.00 |   0.00 |    0.00 |    80.41 |    58 | 3,173,660 |     58 |        16,238 |           388 |
    | **NEGany~any_happier**   |    4.66 |    0.49 |   0.99 |   0.00 |    0.00 | 1,085.12 |   828 | 3,173,660 |    834 |        16,238 |         2,004 |
    | **NEGany~any_smarter**   |    1.94 |    0.49 |   0.99 |   0.00 |    0.00 |   113.78 |    89 | 3,173,660 |     90 |        16,238 |           733 |
    | **NEGany~any_easier**    |    4.42 |    0.48 |   0.98 |   0.00 |    0.00 | 1,946.26 | 1,594 | 3,173,660 |  1,625 |        16,238 |        12,877 |
    | **NEGany~any_worse**     |    3.62 |    0.46 |   0.96 |   0.00 |    0.00 | 1,816.60 | 1,686 | 3,173,660 |  1,762 |        16,238 |        12,116 |
    | **NEGany~any_better**    |    3.59 |    0.44 |   0.94 |   0.00 |    0.00 | 4,753.39 | 4,719 | 3,173,660 |  5,004 |        16,238 |        50,827 |
    | **NEGany~any_brighter**  |    1.37 |    0.48 |   0.98 |   0.00 |    0.00 |    78.42 |    63 | 3,173,660 |     64 |        16,238 |           640 |
    | **NEGany~any_different** |    3.03 |    0.44 |   0.94 |   0.00 |    0.00 |   905.82 |   902 | 3,173,660 |    957 |        16,238 |        80,643 |
    
    
    #### Top 4 `mirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~any_different** |    1.30 |    0.50 |   1.00 |   0.00 |    0.00 |  66.55 |    48 | 291,732 |     48 |         1,095 |         8,644 |
    | **NEGmir~any_better**    |    3.27 |    0.47 |   0.97 |   0.00 |    0.00 | 447.88 |   380 | 291,732 |    390 |         1,095 |         3,831 |
    | **NEGmir~any_easier**    |    1.23 |    0.47 |   0.97 |   0.00 |    0.00 |  69.61 |    61 | 291,732 |     63 |         1,095 |           681 |
    | **NEGmir~any_worse**     |    1.66 |    0.47 |   0.97 |   0.00 |    0.00 |  98.47 |    87 | 291,732 |     90 |         1,095 |         2,007 |
    
    
    ### 5. _remotely_
    
    
    #### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~remotely_ready**      |    1.49 |    0.50 |   1.00 |   0.00 |    0.00 |  80.41 |    58 | 3,173,660 |     58 |         6,161 |        29,583 |
    | **NEGany~remotely_enough**     |    1.13 |    0.50 |   1.00 |   0.00 |    0.00 |  65.16 |    47 | 3,173,660 |     47 |         6,161 |        27,603 |
    | **NEGany~remotely_true**       |    3.53 |    0.50 |   1.00 |   0.00 |    0.00 | 334.93 |   250 | 3,173,660 |    251 |         6,161 |        34,967 |
    | **NEGany~remotely_surprising** |    1.66 |    0.49 |   0.99 |   0.00 |    0.00 |  94.71 |    75 | 3,173,660 |     76 |         6,161 |        18,776 |
    | **NEGany~remotely_funny**      |    2.16 |    0.47 |   0.97 |   0.00 |    0.00 | 159.09 |   137 | 3,173,660 |    141 |         6,161 |        14,992 |
    | **NEGany~remotely_close**      |    2.98 |    0.45 |   0.95 |   0.00 |    0.00 | 711.52 |   694 | 3,173,660 |    733 |         6,161 |        46,485 |
    | **NEGany~remotely_interested** |    1.99 |    0.41 |   0.91 |   0.00 |    0.00 | 278.69 |   330 | 3,173,660 |    364 |         6,161 |        34,543 |
    | **NEGany~remotely_comparable** |    1.62 |    0.44 |   0.94 |   0.00 |    0.00 | 119.34 |   118 | 3,173,660 |    125 |         6,161 |         2,401 |
    | **NEGany~remotely_similar**    |    1.39 |    0.40 |   0.90 |   0.00 |    0.00 | 123.97 |   152 | 3,173,660 |    169 |         6,161 |        11,088 |
    | **NEGany~remotely_related**    |    1.33 |    0.40 |   0.90 |   0.00 |    0.00 | 116.95 |   146 | 3,173,660 |    163 |         6,161 |        14,260 |
    
    
    #### Top 3 `mirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~remotely_comparable** |    1.15 |    0.50 |   1.00 |   0.00 |    0.00 |  61.00 |    44 | 291,732 |     44 |         1,953 |           158 |
    | **NEGmir~remotely_true**       |    1.43 |    0.48 |   0.98 |   0.00 |    0.00 |  75.72 |    61 | 291,732 |     62 |         1,953 |         2,850 |
    | **NEGmir~remotely_close**      |    2.58 |    0.46 |   0.96 |   0.00 |    0.00 | 244.21 |   218 | 291,732 |    226 |         1,953 |         4,831 |
    
    
    ### 6. _yet_
    
    
    #### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|--------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~yet_clear**     |    8.66 |    0.50 |   1.00 |   0.00 |    0.00 | 14,392.25 | 10,406 | 3,173,660 | 10,409 |        53,881 |        84,227 |
    | **NEGany~yet_certain**   |    5.60 |    0.50 |   1.00 |   0.00 |    0.00 |  1,200.66 |    866 | 3,173,660 |    866 |        53,881 |        11,334 |
    | **NEGany~yet_ready**     |    8.06 |    0.50 |   1.00 |   0.00 |    0.00 | 10,344.81 |  7,501 | 3,173,660 |  7,505 |        53,881 |        29,583 |
    | **NEGany~yet_final**     |    5.16 |    0.50 |   1.00 |   0.00 |    0.00 |    887.30 |    640 | 3,173,660 |    640 |        53,881 |         1,213 |
    | **NEGany~yet_public**    |    4.69 |    0.50 |   1.00 |   0.00 |    0.00 |    647.44 |    467 | 3,173,660 |    467 |        53,881 |         2,656 |
    | **NEGany~yet_complete**  |    6.70 |    0.50 |   1.00 |   0.00 |    0.00 |  2,998.60 |  2,174 | 3,173,660 |  2,175 |        53,881 |         8,415 |
    | **NEGany~yet_available** |    6.66 |    0.50 |   1.00 |   0.00 |    0.00 |  9,950.03 |  7,430 | 3,173,660 |  7,461 |        53,881 |        82,956 |
    | **NEGany~yet_sure**      |    6.13 |    0.50 |   1.00 |   0.00 |    0.00 |  2,689.26 |  1,977 | 3,173,660 |  1,981 |        53,881 |       134,139 |
    | **NEGany~yet_dead**      |    4.47 |    0.50 |   1.00 |   0.00 |    0.00 |    555.93 |    401 | 3,173,660 |    401 |        53,881 |         6,348 |
    | **NEGany~yet_able**      |    5.44 |    0.50 |   1.00 |   0.00 |    0.00 |  1,764.46 |  1,315 | 3,173,660 |  1,320 |        53,881 |        23,355 |
    
    No bigrams found in loaded `mirror` AM table.
    
    ### 7. _immediately_
    
    
    #### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                   |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------------|--------:|--------:|-------:|-------:|--------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~immediately_sure**       |    2.87 |    0.50 |   1.00 |   0.00 |    0.00 |    191.31 |    138 | 3,173,660 |    138 |        58,040 |       134,139 |
    | **NEGany~immediately_reachable**  |    2.50 |    0.50 |   1.00 |   0.00 |    0.00 |    151.11 |    109 | 3,173,660 |    109 |        58,040 |           350 |
    | **NEGany~immediately_certain**    |    1.80 |    0.50 |   1.00 |   0.00 |    0.00 |     97.04 |     70 | 3,173,660 |     70 |        58,040 |        11,334 |
    | **NEGany~immediately_clear**      |    7.55 |    0.50 |   1.00 |   0.01 |    0.01 | 33,058.44 | 24,416 | 3,173,660 | 24,488 |        58,040 |        84,227 |
    | **NEGany~immediately_possible**   |    5.40 |    0.50 |   1.00 |   0.00 |    0.00 |  1,360.38 |  1,000 | 3,173,660 |  1,002 |        58,040 |        30,446 |
    | **NEGany~immediately_available**  |    5.34 |    0.48 |   0.98 |   0.01 |    0.01 | 25,870.14 | 21,078 | 3,173,660 | 21,477 |        58,040 |        82,956 |
    | **NEGany~immediately_obvious**    |    3.88 |    0.46 |   0.96 |   0.00 |    0.00 |  2,481.50 |  2,238 | 3,173,660 |  2,325 |        58,040 |        22,651 |
    | **NEGany~immediately_able**       |    3.66 |    0.48 |   0.98 |   0.00 |    0.00 |    746.39 |    626 | 3,173,660 |    641 |        58,040 |        23,355 |
    | **NEGany~immediately_successful** |    2.87 |    0.47 |   0.97 |   0.00 |    0.00 |    333.73 |    290 | 3,173,660 |    299 |        58,040 |        31,460 |
    | **NEGany~immediately_apparent**   |    3.30 |    0.44 |   0.94 |   0.00 |    0.00 |  2,001.83 |  2,015 | 3,173,660 |  2,143 |        58,040 |         9,798 |
    
    
    #### Top 1 `mirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                  |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~immediately_available** |    1.34 |    0.38 |   0.88 |   0.00 |    0.00 | 120.41 |   162 | 291,732 |    184 |           564 |         3,079 |
    
    
    ### 8. _particularly_
    
    
    #### Top 10 `RBdirect` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                    |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **COM~particularly_acute**         |    2.84 |    0.50 |   1.00 |   0.00 |    0.00 |   187.16 |   135 | 3,173,552 |    135 |        76,162 |         1,038 |
    | **NEGany~particularly_wrong**      |    3.56 |    0.50 |   1.00 |   0.00 |    0.00 |   302.22 |   218 | 3,173,660 |    218 |        76,162 |        21,332 |
    | **NEGany~particularly_athletic**   |    2.49 |    0.50 |   1.00 |   0.00 |    0.00 |   149.72 |   108 | 3,173,660 |    108 |        76,162 |         1,772 |
    | **NEGany~particularly_likeable**   |    2.46 |    0.50 |   1.00 |   0.00 |    0.00 |   146.95 |   106 | 3,173,660 |    106 |        76,162 |           861 |
    | **NEGany~particularly_radical**    |    1.99 |    0.50 |   1.00 |   0.00 |    0.00 |   109.52 |    79 | 3,173,660 |     79 |        76,162 |         2,637 |
    | **NEGany~particularly_new**        |    4.61 |    0.49 |   0.99 |   0.00 |    0.00 |   982.49 |   747 | 3,173,660 |    752 |        76,162 |        21,538 |
    | **NEGany~particularly_religious**  |    4.52 |    0.50 |   1.00 |   0.00 |    0.00 |   659.41 |   485 | 3,173,660 |    486 |        76,162 |         3,507 |
    | **NEGany~particularly_surprising** |    3.93 |    0.47 |   0.97 |   0.00 |    0.00 | 1,260.26 | 1,069 | 3,173,660 |  1,097 |        76,162 |        18,776 |
    | **NEGany~particularly_original**   |    3.64 |    0.49 |   0.99 |   0.00 |    0.00 |   460.59 |   360 | 3,173,660 |    364 |        76,162 |         4,693 |
    | **NEGany~particularly_flashy**     |    1.46 |    0.50 |   1.00 |   0.00 |    0.00 |    79.02 |    57 | 3,173,660 |     57 |        76,162 |         1,732 |
    
    
    #### Top 10 `mirror` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                     |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~particularly_surprising**  |    3.27 |    0.50 |   1.00 |   0.00 |    0.00 | 230.18 |   166 | 291,732 |    166 |        10,029 |         1,248 |
    | **NEGmir~particularly_original**    |    2.33 |    0.50 |   1.00 |   0.00 |    0.00 | 124.78 |    90 | 291,732 |     90 |        10,029 |           715 |
    | **NEGmir~particularly_novel**       |    1.50 |    0.50 |   1.00 |   0.00 |    0.00 |  74.87 |    54 | 291,732 |     54 |        10,029 |           179 |
    | **NEGmir~particularly_religious**   |    1.47 |    0.50 |   1.00 |   0.00 |    0.00 |  73.48 |    53 | 291,732 |     53 |        10,029 |           337 |
    | **NEGmir~particularly_innovative**  |    1.26 |    0.50 |   1.00 |   0.00 |    0.00 |  65.16 |    47 | 291,732 |     47 |        10,029 |           675 |
    | **NEGmir~particularly_new**         |    4.35 |    0.50 |   1.00 |   0.00 |    0.00 | 547.73 |   404 | 291,732 |    405 |        10,029 |         4,300 |
    | **NEGmir~particularly_wrong**       |    3.39 |    0.50 |   1.00 |   0.00 |    0.00 | 282.64 |   212 | 291,732 |    213 |        10,029 |         8,506 |
    | **NEGmir~particularly_good**        |    3.24 |    0.47 |   0.97 |   0.00 |    0.00 | 455.35 |   390 | 291,732 |    401 |        10,029 |        13,423 |
    | **NEGmir~particularly_unusual**     |    2.72 |    0.48 |   0.98 |   0.00 |    0.00 | 209.60 |   170 | 291,732 |    173 |        10,029 |           933 |
    | **NEGmir~particularly_comfortable** |    1.15 |    0.50 |   1.00 |   0.00 |    0.00 |  61.00 |    44 | 291,732 |     44 |        10,029 |         1,888 |
    
    
    ### 9. _inherently_
    
    
    #### Top 6 `RBdirect` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                               |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~inherently_illegal** |    1.26 |    0.48 |   0.98 |   0.00 |    0.00 |    73.01 |    59 | 3,173,660 |     60 |         8,614 |         3,580 |
    | **NEGany~inherently_bad**     |    3.87 |    0.48 |   0.98 |   0.00 |    0.00 |   953.05 |   794 | 3,173,660 |    812 |         8,614 |       119,509 |
    | **NEGany~inherently_wrong**   |    4.25 |    0.48 |   0.98 |   0.00 |    0.00 | 1,956.12 | 1,639 | 3,173,660 |  1,678 |         8,614 |        21,332 |
    | **NEGany~inherently_evil**    |    2.12 |    0.41 |   0.91 |   0.00 |    0.00 |   312.23 |   358 | 3,173,660 |    392 |         8,614 |         3,171 |
    | **NEGany~inherently_better**  |    1.46 |    0.41 |   0.91 |   0.00 |    0.00 |   124.46 |   144 | 3,173,660 |    158 |         8,614 |        50,827 |
    | **NEGany~inherently_good**    |    1.46 |    0.36 |   0.86 |   0.00 |    0.00 |   189.85 |   283 | 3,173,660 |    329 |         8,614 |       201,244 |
    
    
    #### Top 2 `mirror` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                             |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~inherently_wrong** |    3.78 |    0.46 |   0.96 |   0.01 |    0.00 | 1,685.02 | 1,513 | 291,732 |  1,571 |         3,342 |         8,506 |
    | **NEGmir~inherently_bad**   |    1.83 |    0.44 |   0.94 |   0.00 |    0.00 |   144.52 |   148 | 291,732 |    158 |         3,342 |         4,790 |
    
    
    ### 10. _terribly_
    
    
    #### Top 10 `RBdirect` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~terribly_surprising**  |    5.73 |    0.50 |   1.00 |   0.00 |    0.00 | 1,315.75 |   949 | 3,173,660 |    949 |        19,802 |        18,776 |
    | **NEGany~terribly_popular**     |    2.99 |    0.50 |   1.00 |   0.00 |    0.00 |   206.56 |   149 | 3,173,660 |    149 |        19,802 |        51,120 |
    | **NEGany~terribly_unusual**     |    2.96 |    0.50 |   1.00 |   0.00 |    0.00 |   202.40 |   146 | 3,173,660 |    146 |        19,802 |         7,412 |
    | **NEGany~terribly_comfortable** |    2.77 |    0.50 |   1.00 |   0.00 |    0.00 |   178.84 |   129 | 3,173,660 |    129 |        19,802 |        23,908 |
    | **NEGany~terribly_bright**      |    2.61 |    0.50 |   1.00 |   0.00 |    0.00 |   162.20 |   117 | 3,173,660 |    117 |        19,802 |         8,623 |
    | **NEGany~terribly_interested**  |    3.98 |    0.49 |   0.99 |   0.00 |    0.00 |   624.89 |   486 | 3,173,660 |    491 |        19,802 |        34,543 |
    | **NEGany~terribly_different**   |    3.93 |    0.49 |   0.99 |   0.00 |    0.00 |   485.33 |   366 | 3,173,660 |    368 |        19,802 |        80,643 |
    | **NEGany~terribly_surprised**   |    3.30 |    0.49 |   0.99 |   0.00 |    0.00 |   361.19 |   287 | 3,173,660 |    291 |        19,802 |        10,157 |
    | **NEGany~terribly_exciting**    |    3.28 |    0.48 |   0.98 |   0.00 |    0.00 |   456.39 |   382 | 3,173,660 |    391 |        19,802 |        20,233 |
    | **NEGany~terribly_common**      |    2.45 |    0.50 |   1.00 |   0.00 |    0.00 |   145.56 |   105 | 3,173,660 |    105 |        19,802 |        34,450 |
    
    
    #### Top 5 `mirror` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~terribly_surprising**  |    1.85 |    0.50 |   1.00 |   0.00 |    0.00 |  92.89 |    67 | 291,732 |     67 |         2,204 |         1,248 |
    | **NEGmir~terribly_original**    |    1.19 |    0.50 |   1.00 |   0.00 |    0.00 |  62.39 |    45 | 291,732 |     45 |         2,204 |           715 |
    | **NEGmir~terribly_new**         |    1.64 |    0.49 |   0.99 |   0.00 |    0.00 |  86.57 |    69 | 291,732 |     70 |         2,204 |         4,300 |
    | **NEGmir~terribly_interesting** |    1.29 |    0.48 |   0.98 |   0.00 |    0.00 |  68.96 |    56 | 291,732 |     57 |         2,204 |         3,863 |
    | **POS~terribly_wrong**          |    1.06 |    0.30 |   0.80 |   0.00 |    0.00 | 149.75 |   319 | 291,729 |    401 |         2,204 |         8,506 |
    
    
    ### 11. _ever_
    
    
    #### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                        |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|----------:|-------:|--------------:|--------------:|
    | **COM~ever_larger**    |    2.88 |    0.50 |   1.00 |   0.00 |    0.00 | 192.71 |   139 | 3,173,552 |    139 |        10,870 |         7,453 |
    | **NEGany~ever_boring** |    1.84 |    0.50 |   1.00 |   0.00 |    0.00 |  99.82 |    72 | 3,173,660 |     72 |        10,870 |         3,840 |
    | **NEGany~ever_simple** |    3.28 |    0.50 |   1.00 |   0.00 |    0.00 | 281.20 |   211 | 3,173,660 |    212 |        10,870 |        46,867 |
    | **COM~ever_greater**   |    3.09 |    0.49 |   0.99 |   0.00 |    0.00 | 246.80 |   186 | 3,173,552 |    187 |        10,870 |         6,949 |
    | **COM~ever_closer**    |    3.52 |    0.49 |   0.99 |   0.00 |    0.00 | 365.82 |   279 | 3,173,552 |    281 |        10,870 |         3,686 |
    | **NEGany~ever_easy**   |    3.53 |    0.48 |   0.98 |   0.00 |    0.00 | 525.98 |   429 | 3,173,660 |    437 |        10,870 |       108,923 |
    | **COM~ever_deeper**    |    1.31 |    0.48 |   0.98 |   0.00 |    0.00 |  75.72 |    61 | 3,173,552 |     62 |        10,870 |         1,768 |
    | **COM~ever_higher**    |    2.52 |    0.49 |   0.99 |   0.00 |    0.00 | 168.50 |   129 | 3,173,552 |    130 |        10,870 |        12,992 |
    | **NEGany~ever_good**   |    2.52 |    0.45 |   0.95 |   0.00 |    0.00 | 337.56 |   331 | 3,173,660 |    350 |        10,870 |       201,244 |
    | **COM~ever_mindful**   |    1.04 |    0.48 |   0.98 |   0.00 |    0.00 |  63.56 |    52 | 3,173,552 |     53 |        10,870 |           784 |
    
    
    #### Top 10 `mirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                         |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~ever_perfect** |    3.60 |    0.50 |   1.00 |   0.00 |    0.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         1,303 |
    | **NEGmir~ever_simple**  |    3.60 |    0.50 |   1.00 |   0.00 |    0.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         7,465 |
    | **NEGmir~ever_enough**  |    3.09 |    0.50 |   1.00 |   0.00 |    0.00 | 203.83 |   147 | 291,732 |    147 |         4,786 |         1,326 |
    | **NEGmir~ever_certain** |    3.04 |    0.50 |   1.00 |   0.00 |    0.00 | 198.28 |   143 | 291,732 |    143 |         4,786 |         1,276 |
    | **NEGmir~ever_wrong**   |    2.52 |    0.50 |   1.00 |   0.00 |    0.00 | 141.42 |   102 | 291,732 |    102 |         4,786 |         8,506 |
    | **NEGmir~ever_easy**    |    4.21 |    0.50 |   1.00 |   0.00 |    0.00 | 497.96 |   368 | 291,732 |    369 |         4,786 |         7,749 |
    | **NEGmir~ever_good**    |    3.90 |    0.50 |   1.00 |   0.00 |    0.00 | 402.64 |   299 | 291,732 |    300 |         4,786 |        13,423 |
    | **NEGmir~ever_black**   |    1.56 |    0.50 |   1.00 |   0.00 |    0.00 |  77.64 |    56 | 291,732 |     56 |         4,786 |           646 |
    | **NEGmir~ever_able**    |    2.71 |    0.49 |   0.99 |   0.00 |    0.00 | 178.12 |   136 | 291,732 |    137 |         4,786 |         1,891 |
    | **NEGmir~ever_right**   |    1.33 |    0.50 |   1.00 |   0.00 |    0.00 |  67.93 |    49 | 291,732 |     49 |         4,786 |         2,038 |
    


## Top 10 "most negative" bigrams corresponding to top 8 adverbs

2024-07-29

### 1. _necessarily_


#### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                   |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~necessarily_indicative** |    6.29 |    0.50 |   1.00 |   0.00 |    0.00 | 1,925.89 | 1,389 | 3,173,660 |  1,389 |        42,886 |         2,313 |
| **NEGany~necessarily_easy**       |    5.67 |    0.50 |   1.00 |   0.00 |    0.00 | 1,260.28 |   909 | 3,173,660 |    909 |        42,886 |       108,923 |
| **NEGany~necessarily_new**        |    4.74 |    0.50 |   1.00 |   0.00 |    0.00 |   668.24 |   482 | 3,173,660 |    482 |        42,886 |        21,538 |
| **NEGany~necessarily_surprising** |    4.23 |    0.50 |   1.00 |   0.00 |    0.00 |   471.36 |   340 | 3,173,660 |    340 |        42,886 |        18,776 |
| **NEGany~necessarily_enough**     |    3.93 |    0.50 |   1.00 |   0.00 |    0.00 |   386.79 |   279 | 3,173,660 |    279 |        42,886 |        27,603 |
| **NEGany~necessarily_bad**        |    6.31 |    0.50 |   1.00 |   0.00 |    0.00 | 2,814.04 | 2,059 | 3,173,660 |  2,062 |        42,886 |       119,509 |
| **NEGany~necessarily_true**       |    6.16 |    0.50 |   1.00 |   0.00 |    0.00 | 4,330.74 | 3,232 | 3,173,660 |  3,245 |        42,886 |        34,967 |
| **NEGany~necessarily_better**     |    6.07 |    0.50 |   1.00 |   0.00 |    0.00 | 2,564.81 | 1,887 | 3,173,660 |  1,891 |        42,886 |        50,827 |
| **NEGany~necessarily_aware**      |    3.48 |    0.50 |   1.00 |   0.00 |    0.00 |   285.59 |   206 | 3,173,660 |    206 |        42,886 |        28,973 |
| **NEGany~necessarily_related**    |    5.14 |    0.50 |   1.00 |   0.00 |    0.00 | 1,013.51 |   741 | 3,173,660 |    742 |        42,886 |        14,260 |


#### Top 2 `mirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                              |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~necessarily_bad**   |    1.37 |    0.50 |   1.00 |   0.00 |    0.00 |  69.32 |    50 | 291,732 |     50 |           992 |         4,790 |
| **NEGmir~necessarily_wrong** |    3.05 |    0.49 |   0.99 |   0.00 |    0.00 | 265.18 |   211 | 291,732 |    214 |           992 |         8,506 |


### 2. _that_


#### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                            |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------|--------:|--------:|-------:|-------:|--------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~that_surprising** |    5.99 |    0.50 |   1.00 |   0.00 |    0.00 |  1,570.89 |  1,133 | 3,173,660 |  1,133 |       166,676 |        18,776 |
| **NEGany~that_unusual**    |    5.77 |    0.50 |   1.00 |   0.00 |    0.00 |  1,354.57 |    977 | 3,173,660 |    977 |       166,676 |         7,412 |
| **NEGany~that_exciting**   |    5.49 |    0.50 |   1.00 |   0.00 |    0.00 |  1,116.08 |    805 | 3,173,660 |    805 |       166,676 |        20,233 |
| **NEGany~that_uncommon**   |    5.49 |    0.50 |   1.00 |   0.00 |    0.00 |  1,111.92 |    802 | 3,173,660 |    802 |       166,676 |         3,165 |
| **NEGany~that_impressed**  |    5.25 |    0.50 |   1.00 |   0.00 |    0.00 |    944.15 |    681 | 3,173,660 |    681 |       166,676 |        12,138 |
| **NEGany~that_hard**       |    7.68 |    0.50 |   1.00 |   0.00 |    0.00 | 13,602.42 |  9,948 | 3,173,660 |  9,963 |       166,676 |        45,061 |
| **NEGany~that_different**  |    7.18 |    0.50 |   1.00 |   0.00 |    0.00 |  8,895.12 |  6,534 | 3,173,660 |  6,547 |       166,676 |        80,643 |
| **NEGany~that_great**      |    7.18 |    0.50 |   1.00 |   0.00 |    0.00 | 14,908.90 | 11,032 | 3,173,660 | 11,065 |       166,676 |        45,359 |
| **NEGany~that_difficult**  |    7.06 |    0.50 |   1.00 |   0.00 |    0.00 |  7,569.00 |  5,560 | 3,173,660 |  5,571 |       166,676 |        61,490 |
| **NEGany~that_big**        |    6.47 |    0.50 |   1.00 |   0.00 |    0.00 |  8,332.69 |  6,244 | 3,173,660 |  6,273 |       166,676 |        42,912 |


#### Top 10 `mirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                            |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~that_close**      |    1.67 |    0.50 |   1.00 |   0.00 |    0.00 |  83.19 |    60 | 291,732 |     60 |         4,559 |         4,831 |
| **NEGmir~that_happy**      |    1.03 |    0.50 |   1.00 |   0.00 |    0.00 |  56.84 |    41 | 291,732 |     41 |         4,559 |         5,463 |
| **NEGmir~that_popular**    |    1.54 |    0.48 |   0.98 |   0.00 |    0.00 |  81.14 |    65 | 291,732 |     66 |         4,559 |         2,841 |
| **NEGmir~that_simple**     |    3.67 |    0.48 |   0.98 |   0.00 |    0.00 | 580.44 |   474 | 291,732 |    483 |         4,559 |         7,465 |
| **NEGmir~that_difficult**  |    1.16 |    0.48 |   0.98 |   0.00 |    0.00 |  63.56 |    52 | 291,732 |     53 |         4,559 |         4,854 |
| **NEGmir~that_easy**       |    3.23 |    0.47 |   0.97 |   0.00 |    0.00 | 512.43 |   450 | 291,732 |    465 |         4,559 |         7,749 |
| **NEGmir~that_great**      |    2.71 |    0.46 |   0.96 |   0.00 |    0.00 | 312.65 |   286 | 291,732 |    298 |         4,559 |         2,123 |
| **NEGmir~that_good**       |    2.65 |    0.44 |   0.94 |   0.00 |    0.00 | 441.70 |   447 | 291,732 |    476 |         4,559 |        13,423 |
| **NEGmir~that_big**        |    2.08 |    0.47 |   0.97 |   0.00 |    0.00 | 132.98 |   113 | 291,732 |    116 |         4,559 |         3,134 |
| **NEGmir~that_interested** |    1.26 |    0.47 |   0.97 |   0.00 |    0.00 |  70.93 |    62 | 291,732 |     64 |         4,559 |         2,877 |


### 3. _exactly_


#### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                               |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------|--------:|--------:|-------:|-------:|--------:|----------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~exactly_cheap**      |    5.27 |    0.50 |   1.00 |   0.00 |    0.00 |    958.01 |   691 | 3,173,660 |    691 |        44,503 |         6,591 |
| **NEGany~exactly_surprising** |    4.61 |    0.50 |   1.00 |   0.00 |    0.00 |    610.01 |   440 | 3,173,660 |    440 |        44,503 |        18,776 |
| **NEGany~exactly_subtle**     |    3.84 |    0.50 |   1.00 |   0.00 |    0.00 |    364.61 |   263 | 3,173,660 |    263 |        44,503 |         5,299 |
| **NEGany~exactly_fair**       |    3.83 |    0.50 |   1.00 |   0.00 |    0.00 |    360.45 |   260 | 3,173,660 |    260 |        44,503 |         6,964 |
| **NEGany~exactly_fun**        |    3.60 |    0.50 |   1.00 |   0.00 |    0.00 |    310.54 |   224 | 3,173,660 |    224 |        44,503 |        19,661 |
| **NEGany~exactly_sure**       |    7.46 |    0.50 |   1.00 |   0.00 |    0.00 | 11,991.61 | 8,794 | 3,173,660 |  8,810 |        44,503 |       134,139 |
| **NEGany~exactly_clear**      |    6.38 |    0.50 |   1.00 |   0.00 |    0.00 |  2,405.43 | 1,746 | 3,173,660 |  1,747 |        44,503 |        84,227 |
| **NEGany~exactly_new**        |    6.03 |    0.50 |   1.00 |   0.00 |    0.00 |  1,885.86 | 1,371 | 3,173,660 |  1,372 |        44,503 |        21,538 |
| **NEGany~exactly_easy**       |    5.67 |    0.50 |   1.00 |   0.00 |    0.00 |  1,463.43 | 1,066 | 3,173,660 |  1,067 |        44,503 |       108,923 |
| **NEGany~exactly_hard**       |    3.46 |    0.50 |   1.00 |   0.00 |    0.00 |    281.43 |   203 | 3,173,660 |    203 |        44,503 |        45,061 |


#### Top 2 `mirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~exactly_sure**  |    3.10 |    0.50 |   1.00 |   0.00 |    0.00 | 205.21 |   148 | 291,732 |    148 |           869 |         5,978 |
| **NEGmir~exactly_clear** |    1.16 |    0.48 |   0.98 |   0.00 |    0.00 |  63.56 |    52 | 291,732 |     53 |           869 |         3,321 |


### 4. _any_


#### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~any_younger**   |    3.80 |    0.50 |   1.00 |   0.00 |    0.00 |   353.52 |   255 | 3,173,660 |    255 |        16,238 |         1,784 |
| **NEGany~any_nicer**     |    2.30 |    0.50 |   1.00 |   0.00 |    0.00 |   133.09 |    96 | 3,173,660 |     96 |        16,238 |           642 |
| **NEGany~any_sweeter**   |    1.49 |    0.50 |   1.00 |   0.00 |    0.00 |    80.41 |    58 | 3,173,660 |     58 |        16,238 |           388 |
| **NEGany~any_happier**   |    4.66 |    0.49 |   0.99 |   0.00 |    0.00 | 1,085.12 |   828 | 3,173,660 |    834 |        16,238 |         2,004 |
| **NEGany~any_smarter**   |    1.94 |    0.49 |   0.99 |   0.00 |    0.00 |   113.78 |    89 | 3,173,660 |     90 |        16,238 |           733 |
| **NEGany~any_easier**    |    4.42 |    0.48 |   0.98 |   0.00 |    0.00 | 1,946.26 | 1,594 | 3,173,660 |  1,625 |        16,238 |        12,877 |
| **NEGany~any_worse**     |    3.62 |    0.46 |   0.96 |   0.00 |    0.00 | 1,816.60 | 1,686 | 3,173,660 |  1,762 |        16,238 |        12,116 |
| **NEGany~any_better**    |    3.59 |    0.44 |   0.94 |   0.00 |    0.00 | 4,753.39 | 4,719 | 3,173,660 |  5,004 |        16,238 |        50,827 |
| **NEGany~any_brighter**  |    1.37 |    0.48 |   0.98 |   0.00 |    0.00 |    78.42 |    63 | 3,173,660 |     64 |        16,238 |           640 |
| **NEGany~any_different** |    3.03 |    0.44 |   0.94 |   0.00 |    0.00 |   905.82 |   902 | 3,173,660 |    957 |        16,238 |        80,643 |


#### Top 4 `mirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~any_different** |    1.30 |    0.50 |   1.00 |   0.00 |    0.00 |  66.55 |    48 | 291,732 |     48 |         1,095 |         8,644 |
| **NEGmir~any_better**    |    3.27 |    0.47 |   0.97 |   0.00 |    0.00 | 447.88 |   380 | 291,732 |    390 |         1,095 |         3,831 |
| **NEGmir~any_easier**    |    1.23 |    0.47 |   0.97 |   0.00 |    0.00 |  69.61 |    61 | 291,732 |     63 |         1,095 |           681 |
| **NEGmir~any_worse**     |    1.66 |    0.47 |   0.97 |   0.00 |    0.00 |  98.47 |    87 | 291,732 |     90 |         1,095 |         2,007 |


### 5. _remotely_


#### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~remotely_ready**      |    1.49 |    0.50 |   1.00 |   0.00 |    0.00 |  80.41 |    58 | 3,173,660 |     58 |         6,161 |        29,583 |
| **NEGany~remotely_enough**     |    1.13 |    0.50 |   1.00 |   0.00 |    0.00 |  65.16 |    47 | 3,173,660 |     47 |         6,161 |        27,603 |
| **NEGany~remotely_true**       |    3.53 |    0.50 |   1.00 |   0.00 |    0.00 | 334.93 |   250 | 3,173,660 |    251 |         6,161 |        34,967 |
| **NEGany~remotely_surprising** |    1.66 |    0.49 |   0.99 |   0.00 |    0.00 |  94.71 |    75 | 3,173,660 |     76 |         6,161 |        18,776 |
| **NEGany~remotely_funny**      |    2.16 |    0.47 |   0.97 |   0.00 |    0.00 | 159.09 |   137 | 3,173,660 |    141 |         6,161 |        14,992 |
| **NEGany~remotely_close**      |    2.98 |    0.45 |   0.95 |   0.00 |    0.00 | 711.52 |   694 | 3,173,660 |    733 |         6,161 |        46,485 |
| **NEGany~remotely_interested** |    1.99 |    0.41 |   0.91 |   0.00 |    0.00 | 278.69 |   330 | 3,173,660 |    364 |         6,161 |        34,543 |
| **NEGany~remotely_comparable** |    1.62 |    0.44 |   0.94 |   0.00 |    0.00 | 119.34 |   118 | 3,173,660 |    125 |         6,161 |         2,401 |
| **NEGany~remotely_similar**    |    1.39 |    0.40 |   0.90 |   0.00 |    0.00 | 123.97 |   152 | 3,173,660 |    169 |         6,161 |        11,088 |
| **NEGany~remotely_related**    |    1.33 |    0.40 |   0.90 |   0.00 |    0.00 | 116.95 |   146 | 3,173,660 |    163 |         6,161 |        14,260 |


#### Top 3 `mirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~remotely_comparable** |    1.15 |    0.50 |   1.00 |   0.00 |    0.00 |  61.00 |    44 | 291,732 |     44 |         1,953 |           158 |
| **NEGmir~remotely_true**       |    1.43 |    0.48 |   0.98 |   0.00 |    0.00 |  75.72 |    61 | 291,732 |     62 |         1,953 |         2,850 |
| **NEGmir~remotely_close**      |    2.58 |    0.46 |   0.96 |   0.00 |    0.00 | 244.21 |   218 | 291,732 |    226 |         1,953 |         4,831 |


### 6. _yet_


#### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|--------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~yet_clear**     |    8.66 |    0.50 |   1.00 |   0.00 |    0.00 | 14,392.25 | 10,406 | 3,173,660 | 10,409 |        53,881 |        84,227 |
| **NEGany~yet_certain**   |    5.60 |    0.50 |   1.00 |   0.00 |    0.00 |  1,200.66 |    866 | 3,173,660 |    866 |        53,881 |        11,334 |
| **NEGany~yet_ready**     |    8.06 |    0.50 |   1.00 |   0.00 |    0.00 | 10,344.81 |  7,501 | 3,173,660 |  7,505 |        53,881 |        29,583 |
| **NEGany~yet_final**     |    5.16 |    0.50 |   1.00 |   0.00 |    0.00 |    887.30 |    640 | 3,173,660 |    640 |        53,881 |         1,213 |
| **NEGany~yet_public**    |    4.69 |    0.50 |   1.00 |   0.00 |    0.00 |    647.44 |    467 | 3,173,660 |    467 |        53,881 |         2,656 |
| **NEGany~yet_complete**  |    6.70 |    0.50 |   1.00 |   0.00 |    0.00 |  2,998.60 |  2,174 | 3,173,660 |  2,175 |        53,881 |         8,415 |
| **NEGany~yet_available** |    6.66 |    0.50 |   1.00 |   0.00 |    0.00 |  9,950.03 |  7,430 | 3,173,660 |  7,461 |        53,881 |        82,956 |
| **NEGany~yet_sure**      |    6.13 |    0.50 |   1.00 |   0.00 |    0.00 |  2,689.26 |  1,977 | 3,173,660 |  1,981 |        53,881 |       134,139 |
| **NEGany~yet_dead**      |    4.47 |    0.50 |   1.00 |   0.00 |    0.00 |    555.93 |    401 | 3,173,660 |    401 |        53,881 |         6,348 |
| **NEGany~yet_able**      |    5.44 |    0.50 |   1.00 |   0.00 |    0.00 |  1,764.46 |  1,315 | 3,173,660 |  1,320 |        53,881 |        23,355 |

No bigrams found in loaded `mirror` AM table.

### 7. _immediately_


#### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                   |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------------|--------:|--------:|-------:|-------:|--------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~immediately_sure**       |    2.87 |    0.50 |   1.00 |   0.00 |    0.00 |    191.31 |    138 | 3,173,660 |    138 |        58,040 |       134,139 |
| **NEGany~immediately_reachable**  |    2.50 |    0.50 |   1.00 |   0.00 |    0.00 |    151.11 |    109 | 3,173,660 |    109 |        58,040 |           350 |
| **NEGany~immediately_certain**    |    1.80 |    0.50 |   1.00 |   0.00 |    0.00 |     97.04 |     70 | 3,173,660 |     70 |        58,040 |        11,334 |
| **NEGany~immediately_clear**      |    7.55 |    0.50 |   1.00 |   0.01 |    0.01 | 33,058.44 | 24,416 | 3,173,660 | 24,488 |        58,040 |        84,227 |
| **NEGany~immediately_possible**   |    5.40 |    0.50 |   1.00 |   0.00 |    0.00 |  1,360.38 |  1,000 | 3,173,660 |  1,002 |        58,040 |        30,446 |
| **NEGany~immediately_available**  |    5.34 |    0.48 |   0.98 |   0.01 |    0.01 | 25,870.14 | 21,078 | 3,173,660 | 21,477 |        58,040 |        82,956 |
| **NEGany~immediately_obvious**    |    3.88 |    0.46 |   0.96 |   0.00 |    0.00 |  2,481.50 |  2,238 | 3,173,660 |  2,325 |        58,040 |        22,651 |
| **NEGany~immediately_able**       |    3.66 |    0.48 |   0.98 |   0.00 |    0.00 |    746.39 |    626 | 3,173,660 |    641 |        58,040 |        23,355 |
| **NEGany~immediately_successful** |    2.87 |    0.47 |   0.97 |   0.00 |    0.00 |    333.73 |    290 | 3,173,660 |    299 |        58,040 |        31,460 |
| **NEGany~immediately_apparent**   |    3.30 |    0.44 |   0.94 |   0.00 |    0.00 |  2,001.83 |  2,015 | 3,173,660 |  2,143 |        58,040 |         9,798 |


#### Top 1 `mirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                  |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~immediately_available** |    1.34 |    0.38 |   0.88 |   0.00 |    0.00 | 120.41 |   162 | 291,732 |    184 |           564 |         3,079 |


### 8. _particularly_


#### Top 10 `RBdirect` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                    |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **COM~particularly_acute**         |    2.84 |    0.50 |   1.00 |   0.00 |    0.00 |   187.16 |   135 | 3,173,552 |    135 |        76,162 |         1,038 |
| **NEGany~particularly_wrong**      |    3.56 |    0.50 |   1.00 |   0.00 |    0.00 |   302.22 |   218 | 3,173,660 |    218 |        76,162 |        21,332 |
| **NEGany~particularly_athletic**   |    2.49 |    0.50 |   1.00 |   0.00 |    0.00 |   149.72 |   108 | 3,173,660 |    108 |        76,162 |         1,772 |
| **NEGany~particularly_likeable**   |    2.46 |    0.50 |   1.00 |   0.00 |    0.00 |   146.95 |   106 | 3,173,660 |    106 |        76,162 |           861 |
| **NEGany~particularly_radical**    |    1.99 |    0.50 |   1.00 |   0.00 |    0.00 |   109.52 |    79 | 3,173,660 |     79 |        76,162 |         2,637 |
| **NEGany~particularly_new**        |    4.61 |    0.49 |   0.99 |   0.00 |    0.00 |   982.49 |   747 | 3,173,660 |    752 |        76,162 |        21,538 |
| **NEGany~particularly_religious**  |    4.52 |    0.50 |   1.00 |   0.00 |    0.00 |   659.41 |   485 | 3,173,660 |    486 |        76,162 |         3,507 |
| **NEGany~particularly_surprising** |    3.93 |    0.47 |   0.97 |   0.00 |    0.00 | 1,260.26 | 1,069 | 3,173,660 |  1,097 |        76,162 |        18,776 |
| **NEGany~particularly_original**   |    3.64 |    0.49 |   0.99 |   0.00 |    0.00 |   460.59 |   360 | 3,173,660 |    364 |        76,162 |         4,693 |
| **NEGany~particularly_flashy**     |    1.46 |    0.50 |   1.00 |   0.00 |    0.00 |    79.02 |    57 | 3,173,660 |     57 |        76,162 |         1,732 |


#### Top 10 `mirror` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                     |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~particularly_surprising**  |    3.27 |    0.50 |   1.00 |   0.00 |    0.00 | 230.18 |   166 | 291,732 |    166 |        10,029 |         1,248 |
| **NEGmir~particularly_original**    |    2.33 |    0.50 |   1.00 |   0.00 |    0.00 | 124.78 |    90 | 291,732 |     90 |        10,029 |           715 |
| **NEGmir~particularly_novel**       |    1.50 |    0.50 |   1.00 |   0.00 |    0.00 |  74.87 |    54 | 291,732 |     54 |        10,029 |           179 |
| **NEGmir~particularly_religious**   |    1.47 |    0.50 |   1.00 |   0.00 |    0.00 |  73.48 |    53 | 291,732 |     53 |        10,029 |           337 |
| **NEGmir~particularly_innovative**  |    1.26 |    0.50 |   1.00 |   0.00 |    0.00 |  65.16 |    47 | 291,732 |     47 |        10,029 |           675 |
| **NEGmir~particularly_new**         |    4.35 |    0.50 |   1.00 |   0.00 |    0.00 | 547.73 |   404 | 291,732 |    405 |        10,029 |         4,300 |
| **NEGmir~particularly_wrong**       |    3.39 |    0.50 |   1.00 |   0.00 |    0.00 | 282.64 |   212 | 291,732 |    213 |        10,029 |         8,506 |
| **NEGmir~particularly_good**        |    3.24 |    0.47 |   0.97 |   0.00 |    0.00 | 455.35 |   390 | 291,732 |    401 |        10,029 |        13,423 |
| **NEGmir~particularly_unusual**     |    2.72 |    0.48 |   0.98 |   0.00 |    0.00 | 209.60 |   170 | 291,732 |    173 |        10,029 |           933 |
| **NEGmir~particularly_comfortable** |    1.15 |    0.50 |   1.00 |   0.00 |    0.00 |  61.00 |    44 | 291,732 |     44 |        10,029 |         1,888 |


### 9. _inherently_


#### Top 6 `RBdirect` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                               |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~inherently_illegal** |    1.26 |    0.48 |   0.98 |   0.00 |    0.00 |    73.01 |    59 | 3,173,660 |     60 |         8,614 |         3,580 |
| **NEGany~inherently_bad**     |    3.87 |    0.48 |   0.98 |   0.00 |    0.00 |   953.05 |   794 | 3,173,660 |    812 |         8,614 |       119,509 |
| **NEGany~inherently_wrong**   |    4.25 |    0.48 |   0.98 |   0.00 |    0.00 | 1,956.12 | 1,639 | 3,173,660 |  1,678 |         8,614 |        21,332 |
| **NEGany~inherently_evil**    |    2.12 |    0.41 |   0.91 |   0.00 |    0.00 |   312.23 |   358 | 3,173,660 |    392 |         8,614 |         3,171 |
| **NEGany~inherently_better**  |    1.46 |    0.41 |   0.91 |   0.00 |    0.00 |   124.46 |   144 | 3,173,660 |    158 |         8,614 |        50,827 |
| **NEGany~inherently_good**    |    1.46 |    0.36 |   0.86 |   0.00 |    0.00 |   189.85 |   283 | 3,173,660 |    329 |         8,614 |       201,244 |


#### Top 2 `mirror` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                             |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~inherently_wrong** |    3.78 |    0.46 |   0.96 |   0.01 |    0.00 | 1,685.02 | 1,513 | 291,732 |  1,571 |         3,342 |         8,506 |
| **NEGmir~inherently_bad**   |    1.83 |    0.44 |   0.94 |   0.00 |    0.00 |   144.52 |   148 | 291,732 |    158 |         3,342 |         4,790 |


### 10. _terribly_


#### Top 10 `RBdirect` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                 |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------|--------:|--------:|-------:|-------:|--------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~terribly_surprising**  |    5.73 |    0.50 |   1.00 |   0.00 |    0.00 | 1,315.75 |   949 | 3,173,660 |    949 |        19,802 |        18,776 |
| **NEGany~terribly_popular**     |    2.99 |    0.50 |   1.00 |   0.00 |    0.00 |   206.56 |   149 | 3,173,660 |    149 |        19,802 |        51,120 |
| **NEGany~terribly_unusual**     |    2.96 |    0.50 |   1.00 |   0.00 |    0.00 |   202.40 |   146 | 3,173,660 |    146 |        19,802 |         7,412 |
| **NEGany~terribly_comfortable** |    2.77 |    0.50 |   1.00 |   0.00 |    0.00 |   178.84 |   129 | 3,173,660 |    129 |        19,802 |        23,908 |
| **NEGany~terribly_bright**      |    2.61 |    0.50 |   1.00 |   0.00 |    0.00 |   162.20 |   117 | 3,173,660 |    117 |        19,802 |         8,623 |
| **NEGany~terribly_interested**  |    3.98 |    0.49 |   0.99 |   0.00 |    0.00 |   624.89 |   486 | 3,173,660 |    491 |        19,802 |        34,543 |
| **NEGany~terribly_different**   |    3.93 |    0.49 |   0.99 |   0.00 |    0.00 |   485.33 |   366 | 3,173,660 |    368 |        19,802 |        80,643 |
| **NEGany~terribly_surprised**   |    3.30 |    0.49 |   0.99 |   0.00 |    0.00 |   361.19 |   287 | 3,173,660 |    291 |        19,802 |        10,157 |
| **NEGany~terribly_exciting**    |    3.28 |    0.48 |   0.98 |   0.00 |    0.00 |   456.39 |   382 | 3,173,660 |    391 |        19,802 |        20,233 |
| **NEGany~terribly_common**      |    2.45 |    0.50 |   1.00 |   0.00 |    0.00 |   145.56 |   105 | 3,173,660 |    105 |        19,802 |        34,450 |


#### Top 5 `mirror` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                 |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~terribly_surprising**  |    1.85 |    0.50 |   1.00 |   0.00 |    0.00 |  92.89 |    67 | 291,732 |     67 |         2,204 |         1,248 |
| **NEGmir~terribly_original**    |    1.19 |    0.50 |   1.00 |   0.00 |    0.00 |  62.39 |    45 | 291,732 |     45 |         2,204 |           715 |
| **NEGmir~terribly_new**         |    1.64 |    0.49 |   0.99 |   0.00 |    0.00 |  86.57 |    69 | 291,732 |     70 |         2,204 |         4,300 |
| **NEGmir~terribly_interesting** |    1.29 |    0.48 |   0.98 |   0.00 |    0.00 |  68.96 |    56 | 291,732 |     57 |         2,204 |         3,863 |
| **POS~terribly_wrong**          |    1.06 |    0.30 |   0.80 |   0.00 |    0.00 | 149.75 |   319 | 291,729 |    401 |         2,204 |         8,506 |


### 11. _ever_


#### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                        |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|----------:|-------:|--------------:|--------------:|
| **COM~ever_larger**    |    2.88 |    0.50 |   1.00 |   0.00 |    0.00 | 192.71 |   139 | 3,173,552 |    139 |        10,870 |         7,453 |
| **NEGany~ever_boring** |    1.84 |    0.50 |   1.00 |   0.00 |    0.00 |  99.82 |    72 | 3,173,660 |     72 |        10,870 |         3,840 |
| **NEGany~ever_simple** |    3.28 |    0.50 |   1.00 |   0.00 |    0.00 | 281.20 |   211 | 3,173,660 |    212 |        10,870 |        46,867 |
| **COM~ever_greater**   |    3.09 |    0.49 |   0.99 |   0.00 |    0.00 | 246.80 |   186 | 3,173,552 |    187 |        10,870 |         6,949 |
| **COM~ever_closer**    |    3.52 |    0.49 |   0.99 |   0.00 |    0.00 | 365.82 |   279 | 3,173,552 |    281 |        10,870 |         3,686 |
| **NEGany~ever_easy**   |    3.53 |    0.48 |   0.98 |   0.00 |    0.00 | 525.98 |   429 | 3,173,660 |    437 |        10,870 |       108,923 |
| **COM~ever_deeper**    |    1.31 |    0.48 |   0.98 |   0.00 |    0.00 |  75.72 |    61 | 3,173,552 |     62 |        10,870 |         1,768 |
| **COM~ever_higher**    |    2.52 |    0.49 |   0.99 |   0.00 |    0.00 | 168.50 |   129 | 3,173,552 |    130 |        10,870 |        12,992 |
| **NEGany~ever_good**   |    2.52 |    0.45 |   0.95 |   0.00 |    0.00 | 337.56 |   331 | 3,173,660 |    350 |        10,870 |       201,244 |
| **COM~ever_mindful**   |    1.04 |    0.48 |   0.98 |   0.00 |    0.00 |  63.56 |    52 | 3,173,552 |     53 |        10,870 |           784 |


#### Top 10 `mirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                         |   `LRC` |   `dP1` |   `P1` |   `P2` |   `dP2` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------|--------:|--------:|-------:|-------:|--------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~ever_perfect** |    3.60 |    0.50 |   1.00 |   0.00 |    0.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         1,303 |
| **NEGmir~ever_simple**  |    3.60 |    0.50 |   1.00 |   0.00 |    0.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         7,465 |
| **NEGmir~ever_enough**  |    3.09 |    0.50 |   1.00 |   0.00 |    0.00 | 203.83 |   147 | 291,732 |    147 |         4,786 |         1,326 |
| **NEGmir~ever_certain** |    3.04 |    0.50 |   1.00 |   0.00 |    0.00 | 198.28 |   143 | 291,732 |    143 |         4,786 |         1,276 |
| **NEGmir~ever_wrong**   |    2.52 |    0.50 |   1.00 |   0.00 |    0.00 | 141.42 |   102 | 291,732 |    102 |         4,786 |         8,506 |
| **NEGmir~ever_easy**    |    4.21 |    0.50 |   1.00 |   0.00 |    0.00 | 497.96 |   368 | 291,732 |    369 |         4,786 |         7,749 |
| **NEGmir~ever_good**    |    3.90 |    0.50 |   1.00 |   0.00 |    0.00 | 402.64 |   299 | 291,732 |    300 |         4,786 |        13,423 |
| **NEGmir~ever_black**   |    1.56 |    0.50 |   1.00 |   0.00 |    0.00 |  77.64 |    56 | 291,732 |     56 |         4,786 |           646 |
| **NEGmir~ever_able**    |    2.71 |    0.49 |   0.99 |   0.00 |    0.00 | 178.12 |   136 | 291,732 |    137 |         4,786 |         1,891 |
| **NEGmir~ever_right**   |    1.33 |    0.50 |   1.00 |   0.00 |    0.00 |  67.93 |    49 | 291,732 |     49 |         4,786 |         2,038 |



 ### `2024-05-23` Top 10 "most negative" bigrams corresponding to top 5 adverbs



#### 1. _necessarily_


Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                                       | `adj`          |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
 |:--------------------------------------|:---------------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
 | **NEGany~necessarily_sure**           | sure           |    844,981.00 |    5.91 |    0.95 |  1,436.68 |   222 | 3,226,213 |    224 |
 | **NEGany~necessarily_surprising**     | surprising     |    150,067.00 |    7.22 |    0.93 |  2,150.86 |   343 | 3,226,213 |    355 |
 | **NEGany~necessarily_indicative**     | indicative     |     12,760.00 |    8.37 |    0.93 |  8,811.69 | 1,406 | 3,226,213 |  1,456 |
 | **NEGany~necessarily_representative** | representative |     25,187.00 |    7.31 |    0.91 |  3,044.27 |   496 | 3,226,213 |    524 |
 | **NEGany~necessarily_available**      | available      |    866,272.00 |    6.36 |    0.89 |  1,280.24 |   213 | 3,226,213 |    230 |
 | **NEGany~necessarily_easy**           | easy           |    771,307.00 |    7.26 |    0.88 |  5,448.34 |   914 | 3,226,213 |    996 |
 | **NEGany~necessarily_true**           | true           |    348,994.00 |    6.89 |    0.82 | 18,199.76 | 3,238 | 3,226,213 |  3,786 |
 | **NEGany~necessarily_illegal**        | illegal        |     44,028.00 |    6.48 |    0.87 |  1,659.90 |   280 | 3,226,213 |    307 |
 | **NEGany~necessarily_related**        | related        |    137,661.00 |    6.74 |    0.84 |  4,271.76 |   742 | 3,226,213 |    842 |
 | **NEGany~necessarily_interested**     | interested     |    364,497.00 |    6.77 |    0.87 |  2,500.26 |   422 | 3,226,213 |    463 |


Top 3 `NEGmirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                              | `adj`   |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
 |:-----------------------------|:--------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
 | **NEGmir~necessarily_wrong** | wrong   |     20,866.00 |    4.27 |    0.81 | 708.98 |   209 | 289,770 |    214 |
 | **NEGmir~necessarily_bad**   | bad     |     10,783.00 |    2.02 |    0.76 | 153.43 |    50 | 289,770 |     54 |
 | **NEGmir~necessarily_true**  | true    |      7,402.00 |    2.18 |    0.75 | 159.07 |    53 | 289,770 |     58 |


#### 2. _exactly_


Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                               | `adj`      |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
 |:------------------------------|:-----------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
 | **NEGany~exactly_surprising** | surprising |    150,067.00 |    7.34 |    0.96 |  2,863.35 |   441 | 3,226,213 |    444 |
 | **NEGany~exactly_cheap**      | cheap      |     83,765.00 |    8.28 |    0.95 |  4,443.27 |   693 | 3,226,213 |    704 |
 | **NEGany~exactly_subtle**     | subtle     |     56,845.00 |    6.92 |    0.94 |  1,671.02 |   264 | 3,226,213 |    271 |
 | **NEGany~exactly_fun**        | fun        |    224,457.00 |    6.67 |    0.94 |  1,423.92 |   225 | 3,226,213 |    231 |
 | **NEGany~exactly_conducive**  | conducive  |     16,405.00 |    6.56 |    0.93 |  1,313.09 |   208 | 3,226,213 |    214 |
 | **NEGany~exactly_sure**       | sure       |    844,981.00 |    8.63 |    0.92 | 54,750.58 | 8,860 | 3,226,213 |  9,301 |
 | **NEGany~exactly_new**        | new        |    321,311.00 |    8.54 |    0.93 |  8,697.93 | 1,378 | 3,226,213 |  1,418 |
 | **NEGany~exactly_easy**       | easy       |    771,307.00 |    8.37 |    0.93 |  6,747.64 | 1,069 | 3,226,213 |  1,100 |
 | **NEGany~exactly_clear**      | clear      |    491,108.00 |    8.30 |    0.92 | 10,937.16 | 1,759 | 3,226,213 |  1,835 |
 | **NEGany~exactly_happy**      | happy      |    528,511.00 |    7.16 |    0.90 |  2,694.69 |   441 | 3,226,213 |    468 |

 No bigrams found in loaded `NEGmirror` AM table.

#### 3. _that_


Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                             | `adj`       |   `adj_total` |   `LRC` |   `dP1` |      `G2` |   `f` |      `f1` |   `f2` |
 |:----------------------------|:------------|--------------:|--------:|--------:|----------:|------:|----------:|-------:|
 | **NEGany~that_uncommon**    | uncommon    |     61,767.00 |    8.39 |    0.94 |  5,136.91 |   804 | 3,226,213 |    819 |
 | **NEGany~that_fond**        | fond        |     39,809.00 |    7.27 |    0.94 |  2,127.94 |   334 | 3,226,213 |    341 |
 | **NEGany~that_surprising**  | surprising  |    150,067.00 |    8.14 |    0.92 |  7,115.30 | 1,141 | 3,226,213 |  1,187 |
 | **NEGany~that_common**      | common      |    556,435.00 |    8.12 |    0.92 |  7,564.08 | 1,216 | 3,226,213 |  1,268 |
 | **NEGany~that_dissimilar**  | dissimilar  |      8,816.00 |    7.00 |    0.92 |  1,904.15 |   307 | 3,226,213 |    321 |
 | **NEGany~that_hard**        | hard        |    430,990.00 |    7.96 |    0.88 | 59,642.82 | 9,966 | 3,226,213 | 10,818 |
 | **NEGany~that_complicated** | complicated |    180,071.00 |    7.95 |    0.91 |  7,450.89 | 1,208 | 3,226,213 |  1,270 |
 | **NEGany~that_impressed**   | impressed   |    113,281.00 |    7.57 |    0.91 |  4,207.58 |   684 | 3,226,213 |    721 |
 | **NEGany~that_noticeable**  | noticeable  |     40,372.00 |    6.78 |    0.91 |  1,632.07 |   265 | 3,226,213 |    279 |
 | **NEGany~that_exciting**    | exciting    |    236,396.00 |    7.48 |    0.90 |  4,892.83 |   805 | 3,226,213 |    859 |


Top 10 `NEGmirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                            | `adj`      |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
 |:---------------------------|:-----------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
 | **NEGmir~that_popular**    | popular    |      5,787.00 |    2.50 |    0.76 |   200.44 |    65 | 289,770 |     70 |
 | **NEGmir~that_interested** | interested |      9,258.00 |    2.42 |    0.76 |   190.06 |    62 | 289,770 |     67 |
 | **NEGmir~that_difficult**  | difficult  |     16,043.00 |    2.15 |    0.75 |   155.64 |    52 | 289,770 |     57 |
 | **NEGmir~that_hard**       | hard       |      7,311.00 |    2.31 |    0.74 |   168.31 |    57 | 289,770 |     63 |
 | **NEGmir~that_close**      | close      |     13,962.00 |    2.39 |    0.73 |   174.26 |    60 | 289,770 |     67 |
 | **NEGmir~that_simple**     | simple     |     25,382.00 |    4.34 |    0.73 | 1,370.94 |   473 | 289,770 |    529 |
 | **NEGmir~that_easy**       | easy       |     20,050.00 |    4.21 |    0.72 | 1,258.15 |   442 | 289,770 |    500 |
 | **NEGmir~that_great**      | great      |      5,819.00 |    3.52 |    0.67 |   728.46 |   282 | 289,770 |    340 |
 | **NEGmir~that_good**       | good       |     33,540.00 |    3.07 |    0.56 |   953.31 |   447 | 289,770 |    615 |
 | **NEGmir~that_big**        | big        |      7,859.00 |    3.06 |    0.70 |   309.58 |   113 | 289,770 |    131 |


#### 4. _before_

 No bigrams found in loaded `RBdirect` AM table.
 No bigrams found in loaded `NEGmirror` AM table.

#### 5. _any_


Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
 |:-------------------------|:----------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
 | **NEGany~any_happier**   | happier   |     19,501.00 |    4.65 |    0.53 | 3,488.76 |   830 | 3,226,213 |  1,472 |
 | **NEGany~any_simpler**   | simpler   |     26,094.00 |    3.09 |    0.30 |   671.74 |   228 | 3,226,213 |    672 |
 | **NEGany~any_clearer**   | clearer   |     13,369.00 |    3.21 |    0.30 | 1,051.22 |   357 | 3,226,213 |  1,053 |
 | **NEGany~any_different** | different |    909,864.00 |    2.98 |    0.24 | 2,270.24 |   910 | 3,226,213 |  3,313 |
 | **NEGany~any_younger**   | younger   |     29,805.00 |    2.37 |    0.19 |   544.17 |   256 | 3,226,213 |  1,121 |
 | **NEGany~any_worse**     | worse     |    214,166.00 |    2.47 |    0.16 | 3,165.88 | 1,693 | 3,226,213 |  8,487 |
 | **NEGany~any_bigger**    | bigger    |    130,470.00 |    2.27 |    0.17 |   688.06 |   357 | 3,226,213 |  1,735 |
 | **NEGany~any_harder**    | harder    |     99,332.00 |    1.98 |    0.15 |   395.22 |   227 | 3,226,213 |  1,221 |
 | **NEGany~any_safer**     | safer     |     26,779.00 |    1.73 |    0.12 |   346.68 |   235 | 3,226,213 |  1,471 |
 | **NEGany~any_easier**    | easier    |    237,680.00 |    1.95 |    0.11 | 2,164.75 | 1,607 | 3,226,213 | 10,860 |


Top 4 `NEGmirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                       | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
 |:----------------------|:--------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
 | **NEGmir~any_better** | better  |     14,076.00 |    4.44 |    0.75 | 1,148.18 |   381 | 289,770 |    416 |
 | **NEGmir~any_easier** | easier  |      2,409.00 |    2.42 |    0.75 |   181.98 |    61 | 289,770 |     67 |
 | **NEGmir~any_worse**  | worse   |      8,490.00 |    2.87 |    0.72 |   248.63 |    88 | 289,770 |    100 |
 | **NEGmir~any_closer** | closer  |        986.00 |    2.21 |    0.68 |   149.62 |    56 | 289,770 |     66 |


#### 6. _ever_


Top 5 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                         | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |      `f1` |   `f2` |
 |:------------------------|:--------|--------------:|--------:|--------:|---------:|------:|----------:|-------:|
 | **NEGany~ever_simple**  | simple  |    427,167.00 |    5.54 |    0.77 | 1,142.04 |   212 | 3,226,213 |    262 |
 | **NEGany~ever_easy**    | easy    |    771,307.00 |    5.06 |    0.63 | 2,030.58 |   430 | 3,226,213 |    641 |
 | **NEGany~ever_good**    | good    |  2,037,285.00 |    3.76 |    0.40 | 1,178.00 |   332 | 3,226,213 |    756 |
 | **NEGany~ever_perfect** | perfect |    164,519.00 |    3.48 |    0.37 |   736.05 |   217 | 3,226,213 |    527 |
 | **NEGany~ever_able**    | able    |    428,268.00 |    1.81 |    0.13 |   363.95 |   234 | 3,226,213 |  1,398 |


Top 6 `NEGmirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                         | `adj`   |   `adj_total` |   `LRC` |   `dP1` |     `G2` |   `f` |    `f1` |   `f2` |
 |:------------------------|:--------|--------------:|--------:|--------:|---------:|------:|--------:|-------:|
 | **NEGmir~ever_easy**    | easy    |     20,050.00 |    3.21 |    0.83 | 1,311.83 |   367 | 289,770 |    368 |
 | **NEGmir~ever_perfect** | perfect |      3,708.00 |    2.38 |    0.83 |   735.10 |   207 | 289,770 |    208 |
 | **NEGmir~ever_good**    | good    |     33,540.00 |    4.72 |    0.82 | 1,034.95 |   298 | 289,770 |    302 |
 | **NEGmir~ever_wrong**   | wrong   |     20,866.00 |    2.56 |    0.82 |   349.21 |   102 | 289,770 |    104 |
 | **NEGmir~ever_free**    | free    |      5,043.00 |    1.97 |    0.81 |   231.61 |    69 | 289,770 |     71 |
 | **NEGmir~ever_able**    | able    |      6,448.00 |    3.66 |    0.79 |   437.65 |   136 | 289,770 |    143 |


#### 7. _yet_


Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |      `G2` |    `f` |      `f1` |   `f2` |
 |:-------------------------|:----------|--------------:|--------:|--------:|----------:|-------:|----------:|-------:|
 | **NEGany~yet_clear**     | clear     |    491,108.00 |   10.26 |    0.95 | 67,924.56 | 10,553 | 3,226,213 | 10,693 |
 | **NEGany~yet_eligible**  | eligible  |     49,578.00 |    7.72 |    0.94 |  2,929.15 |    459 | 3,226,213 |    468 |
 | **NEGany~yet_official**  | official  |      9,778.00 |    7.33 |    0.94 |  2,236.98 |    353 | 3,226,213 |    362 |
 | **NEGany~yet_ready**     | ready     |    240,297.00 |    9.23 |    0.93 | 48,012.06 |  7,611 | 3,226,213 |  7,838 |
 | **NEGany~yet_certain**   | certain   |    104,544.00 |    8.12 |    0.93 |  5,491.41 |    874 | 3,226,213 |    903 |
 | **NEGany~yet_complete**  | complete  |    107,018.00 |    8.42 |    0.92 | 13,815.99 |  2,220 | 3,226,213 |  2,314 |
 | **NEGany~yet_sure**      | sure      |    844,981.00 |    8.37 |    0.92 | 12,379.79 |  1,990 | 3,226,213 |  2,075 |
 | **NEGany~yet_available** | available |    866,272.00 |    7.69 |    0.87 | 44,196.15 |  7,481 | 3,226,213 |  8,238 |
 | **NEGany~yet_right**     | right     |    204,572.00 |    6.50 |    0.92 |  1,254.20 |    202 | 3,226,213 |    211 |
 | **NEGany~yet_final**     | final     |      9,657.00 |    7.45 |    0.91 |  4,028.75 |    659 | 3,226,213 |    699 |

 No bigrams found in loaded `NEGmirror` AM table.

#### 8. _longer_


Top 5 `RBdirect` "longer_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                          | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |    `f` |       `f1` |   `f2` |
 |:-------------------------|:----------|--------------:|--------:|--------:|-------:|-------:|-----------:|-------:|
 | **COM~longer_lasting**   | lasting   |     24,344.00 |    1.44 |    0.04 | 244.09 |  3,860 | 83,102,035 |  3,866 |
 | **COM~longer_enough**    | enough    |    453,790.00 |    1.41 |    0.03 | 216.98 |  3,952 | 83,102,035 |  3,964 |
 | **COM~longer_able**      | able      |    428,268.00 |    2.28 |    0.03 | 623.67 | 11,677 | 83,102,035 | 11,716 |
 | **COM~longer_available** | available |    866,272.00 |    2.45 |    0.03 | 974.55 | 18,865 | 83,102,035 | 18,935 |
 | **COM~longer_necessary** | necessary |    187,396.00 |    1.27 |    0.03 | 220.07 |  5,365 | 83,102,035 |  5,399 |

 No bigrams found in loaded `NEGmirror` AM table.

#### 9. _immediately_


Top 5 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                                  | `adj`     |   `adj_total` |   `LRC` |   `dP1` |       `G2` |    `f` |      `f1` |   `f2` |
 |:---------------------------------|:----------|--------------:|--------:|--------:|-----------:|-------:|----------:|-------:|
 | **NEGany~immediately_possible**  | possible  |    364,265.00 |    7.68 |    0.90 |   6,269.26 |  1,027 | 3,226,213 |  1,091 |
 | **NEGany~immediately_clear**     | clear     |    491,108.00 |    8.32 |    0.90 | 153,302.22 | 25,276 | 3,226,213 | 27,066 |
 | **NEGany~immediately_available** | available |    866,272.00 |    5.77 |    0.66 | 102,962.94 | 21,297 | 3,226,213 | 30,725 |
 | **NEGany~immediately_able**      | able      |    428,268.00 |    4.87 |    0.58 |   2,851.84 |    639 | 3,226,213 |  1,036 |
 | **NEGany~immediately_obvious**   | obvious   |    193,498.00 |    4.59 |    0.49 |   9,043.23 |  2,258 | 3,226,213 |  4,305 |


Top 1 `NEGmirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


 |                                  | `adj`     |   `adj_total` |   `LRC` |   `dP1` |   `G2` |   `f` |    `f1` |   `f2` |
 |:---------------------------------|:----------|--------------:|--------:|--------:|-------:|------:|--------:|-------:|
 | **NEGmir~immediately_available** | available |     12,636.00 |    1.94 |    0.43 | 254.47 |   162 | 289,770 |    274 |




```python
bigram_dfs['RBdirect'].filter(like='~before_', axis=0)
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
      <th>l2</th>
      <th>f</th>
      <th>E11</th>
      <th>am_log_likelihood</th>
      <th>...</th>
      <th>adj</th>
      <th>adv_total</th>
      <th>adj_total</th>
      <th>l1</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>NEGany~before_available</th>
      <td>before_available</td>
      <td>177</td>
      <td>88.50</td>
      <td>245.38</td>
      <td>...</td>
      <td>available</td>
      <td>323</td>
      <td>82956</td>
      <td>NEGATED</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 46 columns</p>
</div>




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

    
    1. _necessarily_ (11 unique)
       1. _easy_
       1. _related_
       1. _wrong_
       1. _enough_
       1. _surprising_
       1. _aware_
       1. _new_
       1. _indicative_
       1. _bad_
       1. _true_
       1. _better_
    
    1. _that_ (17 unique)
       1. _different_
       1. _easy_
       1. _difficult_
       1. _simple_
       1. _surprising_
       1. _exciting_
       1. _impressed_
       1. _popular_
       1. _happy_
       1. _hard_
       1. _big_
       1. _great_
       1. _unusual_
       1. _interested_
       1. _good_
       1. _uncommon_
       1. _close_
    
    1. _exactly_ (10 unique)
       1. _fair_
       1. _easy_
       1. _subtle_
       1. _clear_
       1. _surprising_
       1. _new_
       1. _hard_
       1. _sure_
       1. _fun_
       1. _cheap_
    
    1. _any_ (10 unique)
       1. _different_
       1. _nicer_
       1. _younger_
       1. _better_
       1. _brighter_
       1. _happier_
       1. _sweeter_
       1. _smarter_
       1. _worse_
       1. _easier_
    
    1. _remotely_ (10 unique)
       1. _ready_
       1. _related_
       1. _enough_
       1. _funny_
       1. _surprising_
       1. _comparable_
       1. _similar_
       1. _interested_
       1. _true_
       1. _close_
    
    1. _yet_ (10 unique)
       1. _ready_
       1. _clear_
       1. _complete_
       1. _final_
       1. _available_
       1. _sure_
       1. _certain_
       1. _dead_
       1. _public_
       1. _able_
    
    1. _immediately_ (10 unique)
       1. _clear_
       1. _obvious_
       1. _reachable_
       1. _sure_
       1. _available_
       1. _certain_
       1. _apparent_
       1. _possible_
       1. _successful_
       1. _able_
    
    1. _particularly_ (15 unique)
       1. _wrong_
       1. _athletic_
       1. _likeable_
       1. _surprising_
       1. _radical_
       1. _new_
       1. _innovative_
       1. _original_
       1. _novel_
       1. _comfortable_
       1. _flashy_
       1. _unusual_
       1. _good_
       1. _religious_
       1. _acute_
    
    1. _inherently_ (6 unique)
       1. _wrong_
       1. _evil_
       1. _illegal_
       1. _bad_
       1. _good_
       1. _better_
    
    1. _terribly_ (14 unique)
       1. _different_
       1. _wrong_
       1. _bright_
       1. _surprising_
       1. _exciting_
       1. _popular_
       1. _new_
       1. _original_
       1. _surprised_
       1. _comfortable_
       1. _unusual_
       1. _interested_
       1. _interesting_
       1. _common_
    
    1. _ever_ (17 unique)
       1. _easy_
       1. _deeper_
       1. _larger_
       1. _simple_
       1. _good_
       1. _perfect_
       1. _enough_
       1. _wrong_
       1. _able_
       1. _black_
       1. _right_
       1. _greater_
       1. _boring_
       1. _mindful_
       1. _certain_
       1. _closer_
       1. _higher_
    
    1. _ALL bigrams_ (130 unique)
       1. _particularly novel_
       1. _necessarily indicative_
       1. _inherently better_
       1. _particularly flashy_
       1. _that big_
       1. _remotely enough_
       1. _necessarily surprising_
       1. _inherently illegal_
       1. _ever wrong_
       1. _exactly clear_
       1. _that difficult_
       1. _terribly popular_
       1. _yet certain_
       1. _yet able_
       1. _ever black_
       1. _exactly hard_
       1. _immediately certain_
       1. _ever larger_
       1. _necessarily enough_
       1. _exactly easy_
       1. _particularly likeable_
       1. _inherently wrong_
       1. _remotely ready_
       1. _particularly new_
       1. _remotely funny_
       1. _yet public_
       1. _particularly innovative_
       1. _particularly religious_
       1. _yet complete_
       1. _particularly acute_
       1. _particularly original_
       1. _ever mindful_
       1. _exactly fair_
       1. _ever good_
       1. _immediately possible_
       1. _any worse_
       1. _ever simple_
       1. _particularly athletic_
       1. _ever higher_
       1. _any easier_
       1. _particularly surprising_
       1. _exactly sure_
       1. _terribly surprised_
       1. _any brighter_
       1. _remotely similar_
       1. _ever easy_
       1. _terribly bright_
       1. _that surprising_
       1. _any happier_
       1. _terribly different_
       1. _exactly surprising_
       1. _terribly exciting_
       1. _any smarter_
       1. _necessarily new_
       1. _terribly wrong_
       1. _any different_
       1. _inherently evil_
       1. _ever perfect_
       1. _that different_
       1. _that exciting_
       1. _particularly good_
       1. _terribly common_
       1. _yet final_
       1. _that uncommon_
       1. _necessarily aware_
       1. _necessarily better_
       1. _terribly unusual_
       1. _terribly comfortable_
       1. _terribly surprising_
       1. _that happy_
       1. _that good_
       1. _exactly new_
       1. _that close_
       1. _exactly fun_
       1. _necessarily true_
       1. _that unusual_
       1. _necessarily wrong_
       1. _any younger_
       1. _remotely comparable_
       1. _yet sure_
       1. _terribly new_
       1. _that great_
       1. _immediately reachable_
       1. _yet ready_
       1. _immediately apparent_
       1. _inherently good_
       1. _immediately successful_
       1. _necessarily easy_
       1. _that hard_
       1. _any better_
       1. _immediately clear_
       1. _particularly radical_
       1. _ever right_
       1. _that interested_
       1. _that popular_
       1. _ever enough_
       1. _remotely interested_
       1. _remotely related_
       1. _immediately able_
       1. _any sweeter_
       1. _ever able_
       1. _inherently bad_
       1. _that simple_
       1. _immediately obvious_
       1. _that easy_
       1. _ever deeper_
       1. _immediately available_
       1. _immediately sure_
       1. _necessarily bad_
       1. _any nicer_
       1. _ever boring_
       1. _remotely surprising_
       1. _that impressed_
       1. _remotely close_
       1. _yet clear_
       1. _particularly unusual_
       1. _particularly wrong_
       1. _remotely true_
       1. _yet available_
       1. _yet dead_
       1. _exactly cheap_
       1. _terribly original_
       1. _exactly subtle_
       1. _ever greater_
       1. _ever closer_
       1. _particularly comfortable_
       1. _terribly interested_
       1. _necessarily related_
       1. _terribly interesting_
       1. _ever certain_
    
    1. _ALL adjectives_ (82 unique)
       1. _original_
       1. _bad_
       1. _available_
       1. _unusual_
       1. _dead_
       1. _enough_
       1. _boring_
       1. _mindful_
       1. _reachable_
       1. _different_
       1. _ready_
       1. _difficult_
       1. _simple_
       1. _clear_
       1. _indicative_
       1. _cheap_
       1. _closer_
       1. _black_
       1. _exciting_
       1. _fair_
       1. _nicer_
       1. _funny_
       1. _happier_
       1. _hard_
       1. _possible_
       1. _close_
       1. _higher_
       1. _wrong_
       1. _athletic_
       1. _uncommon_
       1. _final_
       1. _easier_
       1. _interested_
       1. _bright_
       1. _impressed_
       1. _popular_
       1. _happy_
       1. _illegal_
       1. _certain_
       1. _public_
       1. _innovative_
       1. _big_
       1. _surprised_
       1. _similar_
       1. _better_
       1. _subtle_
       1. _radical_
       1. _sweeter_
       1. _obvious_
       1. _worse_
       1. _easy_
       1. _likeable_
       1. _new_
       1. _novel_
       1. _sure_
       1. _fun_
       1. _true_
       1. _able_
       1. _deeper_
       1. _related_
       1. _right_
       1. _flashy_
       1. _interesting_
       1. _common_
       1. _surprising_
       1. _great_
       1. _good_
       1. _successful_
       1. _evil_
       1. _comparable_
       1. _greater_
       1. _apparent_
       1. _larger_
       1. _younger_
       1. _aware_
       1. _brighter_
       1. _comfortable_
       1. _acute_
       1. _perfect_
       1. _complete_
       1. _smarter_
       1. _religious_



1. _necessarily_ (11 unique)
   1. _surprising_
   1. _easy_
   1. _enough_
   1. _aware_
   1. _wrong_
   1. _indicative_
   1. _better_
   1. _related_
   1. _true_
   1. _bad_
   1. _new_

1. _that_ (17 unique)
   1. _surprising_
   1. _great_
   1. _big_
   1. _easy_
   1. _exciting_
   1. _unusual_
   1. _uncommon_
   1. _hard_
   1. _difficult_
   1. _popular_
   1. _interested_
   1. _happy_
   1. _simple_
   1. _good_
   1. _different_
   1. _close_
   1. _impressed_

1. _exactly_ (10 unique)
   1. _surprising_
   1. _subtle_
   1. _fun_
   1. _clear_
   1. _easy_
   1. _hard_
   1. _cheap_
   1. _fair_
   1. _sure_
   1. _new_

1. _any_ (10 unique)
   1. _easier_
   1. _sweeter_
   1. _happier_
   1. _brighter_
   1. _better_
   1. _nicer_
   1. _different_
   1. _smarter_
   1. _younger_
   1. _worse_

1. _remotely_ (10 unique)
   1. _surprising_
   1. _comparable_
   1. _similar_
   1. _enough_
   1. _interested_
   1. _ready_
   1. _funny_
   1. _close_
   1. _true_
   1. _related_

1. _yet_ (10 unique)
   1. _dead_
   1. _clear_
   1. _able_
   1. _final_
   1. _complete_
   1. _ready_
   1. _available_
   1. _sure_
   1. _certain_
   1. _public_

1. _immediately_ (10 unique)
   1. _clear_
   1. _possible_
   1. _able_
   1. _obvious_
   1. _available_
   1. _sure_
   1. _certain_
   1. _apparent_
   1. _successful_
   1. _reachable_

1. _particularly_ (15 unique)
   1. _surprising_
   1. _original_
   1. _innovative_
   1. _unusual_
   1. _radical_
   1. _athletic_
   1. _religious_
   1. _novel_
   1. _wrong_
   1. _flashy_
   1. _good_
   1. _comfortable_
   1. _likeable_
   1. _acute_
   1. _new_

1. _inherently_ (6 unique)
   1. _wrong_
   1. _better_
   1. _good_
   1. _illegal_
   1. _evil_
   1. _bad_

1. _terribly_ (14 unique)
   1. _surprising_
   1. _original_
   1. _interesting_
   1. _unusual_
   1. _popular_
   1. _exciting_
   1. _interested_
   1. _common_
   1. _bright_
   1. _wrong_
   1. _surprised_
   1. _different_
   1. _comfortable_
   1. _new_

1. _ever_ (17 unique)
   1. _greater_
   1. _closer_
   1. _easy_
   1. _higher_
   1. _enough_
   1. _black_
   1. _wrong_
   1. _able_
   1. _mindful_
   1. _perfect_
   1. _simple_
   1. _good_
   1. _deeper_
   1. _certain_
   1. _right_
   1. _boring_
   1. _larger_

1. _ALL bigrams_ (130 unique)
   1. _immediately clear_
   1. _ever good_
   1. _yet clear_
   1. _inherently wrong_
   1. _any brighter_
   1. _necessarily indicative_
   1. _that big_
   1. _necessarily easy_
   1. _immediately able_
   1. _that good_
   1. _exactly sure_
   1. _particularly good_
   1. _terribly popular_
   1. _ever deeper_
   1. _any younger_
   1. _particularly acute_
   1. _necessarily aware_
   1. _ever able_
   1. _remotely enough_
   1. _immediately sure_
   1. _particularly flashy_
   1. _yet certain_
   1. _necessarily new_
   1. _yet final_
   1. _that interested_
   1. _terribly different_
   1. _particularly comfortable_
   1. _exactly clear_
   1. _exactly hard_
   1. _ever greater_
   1. _remotely surprising_
   1. _any different_
   1. _exactly new_
   1. _immediately successful_
   1. _necessarily enough_
   1. _remotely funny_
   1. _yet complete_
   1. _ever wrong_
   1. _that unusual_
   1. _that hard_
   1. _yet sure_
   1. _yet able_
   1. _particularly religious_
   1. _remotely true_
   1. _necessarily better_
   1. _exactly subtle_
   1. _ever easy_
   1. _that easy_
   1. _ever right_
   1. _remotely ready_
   1. _immediately possible_
   1. _terribly original_
   1. _that great_
   1. _terribly exciting_
   1. _that popular_
   1. _terribly surprised_
   1. _ever perfect_
   1. _terribly interesting_
   1. _remotely related_
   1. _inherently good_
   1. _immediately reachable_
   1. _immediately certain_
   1. _that exciting_
   1. _exactly fair_
   1. _that happy_
   1. _any smarter_
   1. _particularly wrong_
   1. _terribly surprising_
   1. _any easier_
   1. _terribly new_
   1. _immediately obvious_
   1. _particularly radical_
   1. _that impressed_
   1. _inherently illegal_
   1. _any nicer_
   1. _terribly unusual_
   1. _any happier_
   1. _ever larger_
   1. _terribly wrong_
   1. _any sweeter_
   1. _necessarily surprising_
   1. _remotely comparable_
   1. _ever mindful_
   1. _necessarily wrong_
   1. _exactly fun_
   1. _particularly athletic_
   1. _ever closer_
   1. _terribly comfortable_
   1. _particularly innovative_
   1. _that uncommon_
   1. _particularly novel_
   1. _particularly surprising_
   1. _immediately available_
   1. _particularly new_
   1. _ever higher_
   1. _ever black_
   1. _inherently bad_
   1. _necessarily bad_
   1. _particularly unusual_
   1. _that simple_
   1. _any worse_
   1. _ever certain_
   1. _inherently evil_
   1. _that surprising_
   1. _necessarily true_
   1. _immediately apparent_
   1. _ever boring_
   1. _ever simple_
   1. _terribly interested_
   1. _necessarily related_
   1. _remotely close_
   1. _that different_
   1. _any better_
   1. _particularly likeable_
   1. _that close_
   1. _exactly cheap_
   1. _remotely similar_
   1. _yet dead_
   1. _yet ready_
   1. _particularly original_
   1. _that difficult_
   1. _ever enough_
   1. _inherently better_
   1. _remotely interested_
   1. _yet public_
   1. _terribly bright_
   1. _terribly common_
   1. _yet available_
   1. _exactly surprising_
   1. _exactly easy_

1. _ALL adjectives_ (82 unique)
   1. _great_
   1. _higher_
   1. _brighter_
   1. _cheap_
   1. _comparable_
   1. _interested_
   1. _bright_
   1. _available_
   1. _related_
   1. _larger_
   1. _enough_
   1. _black_
   1. _perfect_
   1. _reachable_
   1. _greater_
   1. _final_
   1. _simple_
   1. _fair_
   1. _comfortable_
   1. _worse_
   1. _big_
   1. _clear_
   1. _easy_
   1. _exciting_
   1. _able_
   1. _better_
   1. _nicer_
   1. _apparent_
   1. _true_
   1. _indicative_
   1. _closer_
   1. _unusual_
   1. _popular_
   1. _novel_
   1. _obvious_
   1. _uncommon_
   1. _sweeter_
   1. _mindful_
   1. _deeper_
   1. _impressed_
   1. _younger_
   1. _acute_
   1. _happier_
   1. _complete_
   1. _surprised_
   1. _certain_
   1. _smarter_
   1. _easier_
   1. _possible_
   1. _happy_
   1. _boring_
   1. _surprising_
   1. _close_
   1. _new_
   1. _public_
   1. _subtle_
   1. _similar_
   1. _common_
   1. _athletic_
   1. _wrong_
   1. _original_
   1. _bad_
   1. _dead_
   1. _hard_
   1. _ready_
   1. _sure_
   1. _different_
   1. _successful_
   1. _evil_
   1. _fun_
   1. _religious_
   1. _flashy_
   1. _likeable_
   1. _illegal_
   1. _difficult_
   1. _innovative_
   1. _interesting_
   1. _radical_
   1. _aware_
   1. _right_
   1. _good_
   1. _funny_



```python
NEG_bigrams_sample = pd.concat(
    (ad['both'] for ad in samples_dict.values() if isinstance(ad, dict))
    ).sort_values('LRC', ascending=False)
```


```python
NEG_bigrams_sample
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
      <th>dP1</th>
      <th>P1</th>
      <th>LRC</th>
      <th>...</th>
      <th>adj</th>
      <th>adj_total</th>
      <th>P2</th>
      <th>dP2</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>NEGany~yet_clear</th>
      <td>10406</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>8.66</td>
      <td>...</td>
      <td>clear</td>
      <td>84227</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>NEGany~yet_ready</th>
      <td>7501</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>8.06</td>
      <td>...</td>
      <td>ready</td>
      <td>29583</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>NEGany~that_hard</th>
      <td>9948</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>7.68</td>
      <td>...</td>
      <td>hard</td>
      <td>45061</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>NEGany~immediately_clear</th>
      <td>24416</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>7.55</td>
      <td>...</td>
      <td>clear</td>
      <td>84227</td>
      <td>0.01</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>NEGany~exactly_sure</th>
      <td>8794</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>7.46</td>
      <td>...</td>
      <td>sure</td>
      <td>134139</td>
      <td>0.00</td>
      <td>0.00</td>
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
    </tr>
    <tr>
      <th>NEGmir~remotely_comparable</th>
      <td>44</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>1.15</td>
      <td>...</td>
      <td>comparable</td>
      <td>158</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>NEGany~remotely_enough</th>
      <td>47</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>1.13</td>
      <td>...</td>
      <td>enough</td>
      <td>27603</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>POS~terribly_wrong</th>
      <td>319</td>
      <td>0.30</td>
      <td>0.80</td>
      <td>1.06</td>
      <td>...</td>
      <td>wrong</td>
      <td>8506</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>COM~ever_mindful</th>
      <td>52</td>
      <td>0.48</td>
      <td>0.98</td>
      <td>1.04</td>
      <td>...</td>
      <td>mindful</td>
      <td>784</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>NEGmir~that_happy</th>
      <td>41</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>1.03</td>
      <td>...</td>
      <td>happy</td>
      <td>5463</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
  </tbody>
</table>
<p>155 rows × 21 columns</p>
</div>




```python
top_NEGbigram_df_path =  OUT_DIR.joinpath(
    f'{TAG}-Top{K}_NEG-ADV-{ADV_FLOOR}_top-{bigram_k}-bigrams-{bigram_floor}.{timestamp_today()}.csv')
print(top_NEGbigram_df_path)

```

    /share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV-5000_top-10-bigrams-25.2024-07-29.csv



```python
NEG_bigrams_sample.to_csv(top_NEGbigram_df_path)
nb_show_table(NEG_bigrams_sample.filter(adjust_assoc_columns(FOCUS)
                                        ).sort_values('LRC', ascending=False),
              outpath=top_NEGbigram_df_path.with_suffix('.md'))
```

    
    |                                     |    `f` |   `dP1` |   `P1` |   `LRC` |      `G2` |   `MI` |   `odds_r_disc` |   `t` |       `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`       | `l2`                     | `adv`        |   `adv_total` | `adj`       |   `adj_total` |   `P2` |   `dP2` |
    |:------------------------------------|-------:|--------:|-------:|--------:|----------:|-------:|----------------:|------:|----------:|----------:|-------:|----------:|------------:|:-----------|:-------------------------|:-------------|--------------:|:------------|--------------:|-------:|--------:|
    | **NEGany~yet_clear**                | 10,406 |    0.50 |   1.00 |    8.66 | 14,392.25 |   0.30 |            3.47 | 50.99 | 6,347,364 | 3,173,660 | 10,409 |  5,204.46 |    5,201.54 | NEGATED    | yet_clear                | yet          |        53,881 | clear       |        84,227 |   0.00 |    0.00 |
    | **NEGany~yet_ready**                |  7,501 |    0.50 |   1.00 |    8.06 | 10,344.81 |   0.30 |            3.22 | 43.28 | 6,347,364 | 3,173,660 |  7,505 |  3,752.47 |    3,748.53 | NEGATED    | yet_ready                | yet          |        53,881 | ready       |        29,583 |   0.00 |    0.00 |
    | **NEGany~that_hard**                |  9,948 |    0.50 |   1.00 |    7.68 | 13,602.42 |   0.30 |            2.81 | 49.79 | 6,347,364 | 3,173,660 |  9,963 |  4,981.47 |    4,966.53 | NEGATED    | that_hard                | that         |       166,676 | hard        |        45,061 |   0.00 |    0.00 |
    | **NEGany~immediately_clear**        | 24,416 |    0.50 |   1.00 |    7.55 | 33,058.44 |   0.30 |            2.53 | 77.90 | 6,347,364 | 3,173,660 | 24,488 | 12,243.92 |   12,172.08 | NEGATED    | immediately_clear        | immediately  |        58,040 | clear       |        84,227 |   0.01 |    0.01 |
    | **NEGany~exactly_sure**             |  8,794 |    0.50 |   1.00 |    7.46 | 11,991.61 |   0.30 |            2.73 | 46.80 | 6,347,364 | 3,173,660 |  8,810 |  4,404.97 |    4,389.03 | NEGATED    | exactly_sure             | exactly      |        44,503 | sure        |       134,139 |   0.00 |    0.00 |
    | **NEGany~that_different**           |  6,534 |    0.50 |   1.00 |    7.18 |  8,895.12 |   0.30 |            2.69 | 40.34 | 6,347,364 | 3,173,660 |  6,547 |  3,273.48 |    3,260.52 | NEGATED    | that_different           | that         |       166,676 | different   |        80,643 |   0.00 |    0.00 |
    | **NEGany~that_great**               | 11,032 |    0.50 |   1.00 |    7.18 | 14,908.90 |   0.30 |            2.52 | 52.36 | 6,347,364 | 3,173,660 | 11,065 |  5,532.46 |    5,499.54 | NEGATED    | that_great               | that         |       166,676 | great       |        45,359 |   0.00 |    0.00 |
    | **NEGany~that_difficult**           |  5,560 |    0.50 |   1.00 |    7.06 |  7,569.00 |   0.30 |            2.69 | 37.21 | 6,347,364 | 3,173,660 |  5,571 |  2,785.48 |    2,774.52 | NEGATED    | that_difficult           | that         |       166,676 | difficult   |        61,490 |   0.00 |    0.00 |
    | **NEGany~yet_complete**             |  2,174 |    0.50 |   1.00 |    6.70 |  2,998.60 |   0.30 |            3.16 | 23.30 | 6,347,364 | 3,173,660 |  2,175 |  1,087.49 |    1,086.51 | NEGATED    | yet_complete             | yet          |        53,881 | complete    |         8,415 |   0.00 |    0.00 |
    | **NEGany~yet_available**            |  7,430 |    0.50 |   1.00 |    6.66 |  9,950.03 |   0.30 |            2.37 | 42.92 | 6,347,364 | 3,173,660 |  7,461 |  3,730.47 |    3,699.53 | NEGATED    | yet_available            | yet          |        53,881 | available   |        82,956 |   0.00 |    0.00 |
    | **NEGany~that_big**                 |  6,244 |    0.50 |   1.00 |    6.47 |  8,332.69 |   0.30 |            2.33 | 39.33 | 6,347,364 | 3,173,660 |  6,273 |  3,136.48 |    3,107.52 | NEGATED    | that_big                 | that         |       166,676 | big         |        42,912 |   0.00 |    0.00 |
    | **NEGany~exactly_clear**            |  1,746 |    0.50 |   1.00 |    6.38 |  2,405.43 |   0.30 |            3.07 | 20.88 | 6,347,364 | 3,173,660 |  1,747 |    873.49 |      872.51 | NEGATED    | exactly_clear            | exactly      |        44,503 | clear       |        84,227 |   0.00 |    0.00 |
    | **NEGany~necessarily_bad**          |  2,059 |    0.50 |   1.00 |    6.31 |  2,814.04 |   0.30 |            2.77 | 22.66 | 6,347,364 | 3,173,660 |  2,062 |  1,030.99 |    1,028.01 | NEGATED    | necessarily_bad          | necessarily  |        42,886 | bad         |       119,509 |   0.00 |    0.00 |
    | **NEGany~necessarily_indicative**   |  1,389 |    0.50 |   1.00 |    6.29 |  1,925.89 |   0.30 |            3.44 | 18.63 | 6,347,364 | 3,173,660 |  1,389 |    694.50 |      694.50 | NEGATED    | necessarily_indicative   | necessarily  |        42,886 | indicative  |         2,313 |   0.00 |    0.00 |
    | **NEGany~necessarily_true**         |  3,232 |    0.50 |   1.00 |    6.16 |  4,330.74 |   0.30 |            2.38 | 28.31 | 6,347,364 | 3,173,660 |  3,245 |  1,622.49 |    1,609.51 | NEGATED    | necessarily_true         | necessarily  |        42,886 | true        |        34,967 |   0.00 |    0.00 |
    | **NEGany~yet_sure**                 |  1,977 |    0.50 |   1.00 |    6.13 |  2,689.26 |   0.30 |            2.64 | 22.19 | 6,347,364 | 3,173,660 |  1,981 |    990.49 |      986.51 | NEGATED    | yet_sure                 | yet          |        53,881 | sure        |       134,139 |   0.00 |    0.00 |
    | **NEGany~necessarily_better**       |  1,887 |    0.50 |   1.00 |    6.07 |  2,564.81 |   0.30 |            2.62 | 21.67 | 6,347,364 | 3,173,660 |  1,891 |    945.49 |      941.51 | NEGATED    | necessarily_better       | necessarily  |        42,886 | better      |        50,827 |   0.00 |    0.00 |
    | **NEGany~exactly_new**              |  1,371 |    0.50 |   1.00 |    6.03 |  1,885.86 |   0.30 |            2.96 | 18.50 | 6,347,364 | 3,173,660 |  1,372 |    686.00 |      685.00 | NEGATED    | exactly_new              | exactly      |        44,503 | new         |        21,538 |   0.00 |    0.00 |
    | **NEGany~that_surprising**          |  1,133 |    0.50 |   1.00 |    5.99 |  1,570.89 |   0.30 |            3.36 | 16.83 | 6,347,364 | 3,173,660 |  1,133 |    566.50 |      566.50 | NEGATED    | that_surprising          | that         |       166,676 | surprising  |        18,776 |   0.00 |    0.00 |
    | **NEGany~that_unusual**             |    977 |    0.50 |   1.00 |    5.77 |  1,354.57 |   0.30 |            3.29 | 15.63 | 6,347,364 | 3,173,660 |    977 |    488.50 |      488.50 | NEGATED    | that_unusual             | that         |       166,676 | unusual     |         7,412 |   0.00 |    0.00 |
    | **NEGany~terribly_surprising**      |    949 |    0.50 |   1.00 |    5.73 |  1,315.75 |   0.30 |            3.28 | 15.40 | 6,347,364 | 3,173,660 |    949 |    474.50 |      474.50 | NEGATED    | terribly_surprising      | terribly     |        19,802 | surprising  |        18,776 |   0.00 |    0.00 |
    | **NEGany~necessarily_easy**         |    909 |    0.50 |   1.00 |    5.67 |  1,260.28 |   0.30 |            3.26 | 15.07 | 6,347,364 | 3,173,660 |    909 |    454.50 |      454.50 | NEGATED    | necessarily_easy         | necessarily  |        42,886 | easy        |       108,923 |   0.00 |    0.00 |
    | **NEGany~exactly_easy**             |  1,066 |    0.50 |   1.00 |    5.67 |  1,463.43 |   0.30 |            2.85 | 16.31 | 6,347,364 | 3,173,660 |  1,067 |    533.50 |      532.50 | NEGATED    | exactly_easy             | exactly      |        44,503 | easy        |       108,923 |   0.00 |    0.00 |
    | **NEGany~yet_certain**              |    866 |    0.50 |   1.00 |    5.60 |  1,200.66 |   0.30 |            3.24 | 14.71 | 6,347,364 | 3,173,660 |    866 |    433.00 |      433.00 | NEGATED    | yet_certain              | yet          |        53,881 | certain     |        11,334 |   0.00 |    0.00 |
    | **NEGany~that_exciting**            |    805 |    0.50 |   1.00 |    5.49 |  1,116.08 |   0.30 |            3.21 | 14.19 | 6,347,364 | 3,173,660 |    805 |    402.50 |      402.50 | NEGATED    | that_exciting            | that         |       166,676 | exciting    |        20,233 |   0.00 |    0.00 |
    | **NEGany~that_uncommon**            |    802 |    0.50 |   1.00 |    5.49 |  1,111.92 |   0.30 |            3.21 | 14.16 | 6,347,364 | 3,173,660 |    802 |    401.00 |      401.00 | NEGATED    | that_uncommon            | that         |       166,676 | uncommon    |         3,165 |   0.00 |    0.00 |
    | **NEGany~yet_able**                 |  1,315 |    0.50 |   1.00 |    5.44 |  1,764.46 |   0.30 |            2.38 | 18.06 | 6,347,364 | 3,173,660 |  1,320 |    660.00 |      655.00 | NEGATED    | yet_able                 | yet          |        53,881 | able        |        23,355 |   0.00 |    0.00 |
    | **NEGany~immediately_possible**     |  1,000 |    0.50 |   1.00 |    5.40 |  1,360.38 |   0.30 |            2.60 | 15.78 | 6,347,364 | 3,173,660 |  1,002 |    501.00 |      499.00 | NEGATED    | immediately_possible     | immediately  |        58,040 | possible    |        30,446 |   0.00 |    0.00 |
    | **NEGany~immediately_available**    | 21,078 |    0.48 |   0.98 |    5.34 | 25,870.14 |   0.29 |            1.73 | 71.22 | 6,347,364 | 3,173,660 | 21,477 | 10,738.43 |   10,339.57 | NEGATED    | immediately_available    | immediately  |        58,040 | available   |        82,956 |   0.01 |    0.01 |
    | **NEGany~exactly_cheap**            |    691 |    0.50 |   1.00 |    5.27 |    958.01 |   0.30 |            3.14 | 13.14 | 6,347,364 | 3,173,660 |    691 |    345.50 |      345.50 | NEGATED    | exactly_cheap            | exactly      |        44,503 | cheap       |         6,591 |   0.00 |    0.00 |
    | **NEGany~that_impressed**           |    681 |    0.50 |   1.00 |    5.25 |    944.15 |   0.30 |            3.13 | 13.05 | 6,347,364 | 3,173,660 |    681 |    340.50 |      340.50 | NEGATED    | that_impressed           | that         |       166,676 | impressed   |        12,138 |   0.00 |    0.00 |
    | **NEGany~yet_final**                |    640 |    0.50 |   1.00 |    5.16 |    887.30 |   0.30 |            3.11 | 12.65 | 6,347,364 | 3,173,660 |    640 |    320.00 |      320.00 | NEGATED    | yet_final                | yet          |        53,881 | final       |         1,213 |   0.00 |    0.00 |
    | **NEGany~necessarily_related**      |    741 |    0.50 |   1.00 |    5.14 |  1,013.51 |   0.30 |            2.69 | 13.59 | 6,347,364 | 3,173,660 |    742 |    371.00 |      370.00 | NEGATED    | necessarily_related      | necessarily  |        42,886 | related     |        14,260 |   0.00 |    0.00 |
    | **NEGany~necessarily_new**          |    482 |    0.50 |   1.00 |    4.74 |    668.24 |   0.30 |            2.98 | 10.98 | 6,347,364 | 3,173,660 |    482 |    241.00 |      241.00 | NEGATED    | necessarily_new          | necessarily  |        42,886 | new         |        21,538 |   0.00 |    0.00 |
    | **NEGany~yet_public**               |    467 |    0.50 |   1.00 |    4.69 |    647.44 |   0.30 |            2.97 | 10.81 | 6,347,364 | 3,173,660 |    467 |    233.50 |      233.50 | NEGATED    | yet_public               | yet          |        53,881 | public      |         2,656 |   0.00 |    0.00 |
    | **NEGany~any_happier**              |    828 |    0.49 |   0.99 |    4.66 |  1,085.12 |   0.30 |            2.11 | 14.28 | 6,347,364 | 3,173,660 |    834 |    417.00 |      411.00 | NEGATED    | any_happier              | any          |        16,238 | happier     |         2,004 |   0.00 |    0.00 |
    | **NEGany~particularly_new**         |    747 |    0.49 |   0.99 |    4.61 |    982.49 |   0.30 |            2.13 | 13.57 | 6,347,364 | 3,173,660 |    752 |    376.00 |      371.00 | NEGATED    | particularly_new         | particularly |        76,162 | new         |        21,538 |   0.00 |    0.00 |
    | **NEGany~exactly_surprising**       |    440 |    0.50 |   1.00 |    4.61 |    610.01 |   0.30 |            2.95 | 10.49 | 6,347,364 | 3,173,660 |    440 |    220.00 |      220.00 | NEGATED    | exactly_surprising       | exactly      |        44,503 | surprising  |        18,776 |   0.00 |    0.00 |
    | **NEGany~particularly_religious**   |    485 |    0.50 |   1.00 |    4.52 |    659.41 |   0.30 |            2.51 | 10.99 | 6,347,364 | 3,173,660 |    486 |    243.00 |      242.00 | NEGATED    | particularly_religious   | particularly |        76,162 | religious   |         3,507 |   0.00 |    0.00 |
    | **NEGany~yet_dead**                 |    401 |    0.50 |   1.00 |    4.47 |    555.93 |   0.30 |            2.90 | 10.01 | 6,347,364 | 3,173,660 |    401 |    200.50 |      200.50 | NEGATED    | yet_dead                 | yet          |        53,881 | dead        |         6,348 |   0.00 |    0.00 |
    | **NEGany~any_easier**               |  1,594 |    0.48 |   0.98 |    4.42 |  1,946.26 |   0.29 |            1.70 | 19.57 | 6,347,364 | 3,173,660 |  1,625 |    812.49 |      781.51 | NEGATED    | any_easier               | any          |        16,238 | easier      |        12,877 |   0.00 |    0.00 |
    | **NEGmir~particularly_new**         |    404 |    0.50 |   1.00 |    4.35 |    547.73 |   0.30 |            2.43 | 10.03 |   583,470 |   291,732 |    405 |    202.50 |      201.50 | NEGMIR     | particularly_new         | particularly |        10,029 | new         |         4,300 |   0.00 |    0.00 |
    | **NEGany~inherently_wrong**         |  1,639 |    0.48 |   0.98 |    4.25 |  1,956.12 |   0.29 |            1.62 | 19.76 | 6,347,364 | 3,173,660 |  1,678 |    838.99 |      800.01 | NEGATED    | inherently_wrong         | inherently   |         8,614 | wrong       |        21,332 |   0.00 |    0.00 |
    | **NEGany~necessarily_surprising**   |    340 |    0.50 |   1.00 |    4.23 |    471.36 |   0.30 |            2.83 |  9.22 | 6,347,364 | 3,173,660 |    340 |    170.00 |      170.00 | NEGATED    | necessarily_surprising   | necessarily  |        42,886 | surprising  |        18,776 |   0.00 |    0.00 |
    | **NEGmir~ever_easy**                |    368 |    0.50 |   1.00 |    4.21 |    497.96 |   0.30 |            2.39 |  9.57 |   583,470 |   291,732 |    369 |    184.50 |      183.50 | NEGMIR     | ever_easy                | ever         |         4,786 | easy        |         7,749 |   0.00 |    0.00 |
    | **NEGany~terribly_interested**      |    486 |    0.49 |   0.99 |    3.98 |    624.89 |   0.30 |            1.95 | 10.91 | 6,347,364 | 3,173,660 |    491 |    245.50 |      240.50 | NEGATED    | terribly_interested      | terribly     |        19,802 | interested  |        34,543 |   0.00 |    0.00 |
    | **NEGany~necessarily_enough**       |    279 |    0.50 |   1.00 |    3.93 |    386.79 |   0.30 |            2.75 |  8.35 | 6,347,364 | 3,173,660 |    279 |    139.50 |      139.50 | NEGATED    | necessarily_enough       | necessarily  |        42,886 | enough      |        27,603 |   0.00 |    0.00 |
    | **NEGany~particularly_surprising**  |  1,069 |    0.47 |   0.97 |    3.93 |  1,260.26 |   0.29 |            1.57 | 15.92 | 6,347,364 | 3,173,660 |  1,097 |    548.50 |      520.50 | NEGATED    | particularly_surprising  | particularly |        76,162 | surprising  |        18,776 |   0.00 |    0.00 |
    | **NEGany~terribly_different**       |    366 |    0.49 |   0.99 |    3.93 |    485.33 |   0.30 |            2.17 |  9.51 | 6,347,364 | 3,173,660 |    368 |    184.00 |      182.00 | NEGATED    | terribly_different       | terribly     |        19,802 | different   |        80,643 |   0.00 |    0.00 |
    | **NEGmir~ever_good**                |    299 |    0.50 |   1.00 |    3.90 |    402.64 |   0.30 |            2.30 |  8.62 |   583,470 |   291,732 |    300 |    150.00 |      149.00 | NEGMIR     | ever_good                | ever         |         4,786 | good        |        13,423 |   0.00 |    0.00 |
    | **NEGany~immediately_obvious**      |  2,238 |    0.46 |   0.96 |    3.88 |  2,481.50 |   0.28 |            1.41 | 22.73 | 6,347,364 | 3,173,660 |  2,325 |  1,162.49 |    1,075.51 | NEGATED    | immediately_obvious      | immediately  |        58,040 | obvious     |        22,651 |   0.00 |    0.00 |
    | **NEGany~inherently_bad**           |    794 |    0.48 |   0.98 |    3.87 |    953.05 |   0.29 |            1.63 | 13.77 | 6,347,364 | 3,173,660 |    812 |    406.00 |      388.00 | NEGATED    | inherently_bad           | inherently   |         8,614 | bad         |       119,509 |   0.00 |    0.00 |
    | **NEGany~exactly_subtle**           |    263 |    0.50 |   1.00 |    3.84 |    364.61 |   0.30 |            2.72 |  8.11 | 6,347,364 | 3,173,660 |    263 |    131.50 |      131.50 | NEGATED    | exactly_subtle           | exactly      |        44,503 | subtle      |         5,299 |   0.00 |    0.00 |
    | **NEGany~exactly_fair**             |    260 |    0.50 |   1.00 |    3.83 |    360.45 |   0.30 |            2.72 |  8.06 | 6,347,364 | 3,173,660 |    260 |    130.00 |      130.00 | NEGATED    | exactly_fair             | exactly      |        44,503 | fair        |         6,964 |   0.00 |    0.00 |
    | **NEGany~any_younger**              |    255 |    0.50 |   1.00 |    3.80 |    353.52 |   0.30 |            2.71 |  7.98 | 6,347,364 | 3,173,660 |    255 |    127.50 |      127.50 | NEGATED    | any_younger              | any          |        16,238 | younger     |         1,784 |   0.00 |    0.00 |
    | **NEGmir~inherently_wrong**         |  1,513 |    0.46 |   0.96 |    3.78 |  1,685.02 |   0.28 |            1.42 | 18.70 |   583,470 |   291,732 |  1,571 |    785.49 |      727.51 | NEGMIR     | inherently_wrong         | inherently   |         3,342 | wrong       |         8,506 |   0.01 |    0.00 |
    | **NEGmir~that_simple**              |    474 |    0.48 |   0.98 |    3.67 |    580.44 |   0.29 |            1.70 | 10.68 |   583,470 |   291,732 |    483 |    241.50 |      232.50 | NEGMIR     | that_simple              | that         |         4,559 | simple      |         7,465 |   0.00 |    0.00 |
    | **NEGany~immediately_able**         |    626 |    0.48 |   0.98 |    3.66 |    746.39 |   0.29 |            1.61 | 12.21 | 6,347,364 | 3,173,660 |    641 |    320.50 |      305.50 | NEGATED    | immediately_able         | immediately  |        58,040 | able        |        23,355 |   0.00 |    0.00 |
    | **NEGany~particularly_original**    |    360 |    0.49 |   0.99 |    3.64 |    460.59 |   0.30 |            1.90 |  9.38 | 6,347,364 | 3,173,660 |    364 |    182.00 |      178.00 | NEGATED    | particularly_original    | particularly |        76,162 | original    |         4,693 |   0.00 |    0.00 |
    | **NEGany~any_worse**                |  1,686 |    0.46 |   0.96 |    3.62 |  1,816.60 |   0.28 |            1.34 | 19.61 | 6,347,364 | 3,173,660 |  1,762 |    880.99 |      805.01 | NEGATED    | any_worse                | any          |        16,238 | worse       |        12,116 |   0.00 |    0.00 |
    | **NEGany~exactly_fun**              |    224 |    0.50 |   1.00 |    3.60 |    310.54 |   0.30 |            2.65 |  7.48 | 6,347,364 | 3,173,660 |    224 |    112.00 |      112.00 | NEGATED    | exactly_fun              | exactly      |        44,503 | fun         |        19,661 |   0.00 |    0.00 |
    | **NEGmir~ever_perfect**             |    206 |    0.50 |   1.00 |    3.60 |    285.65 |   0.30 |            2.62 |  7.18 |   583,470 |   291,732 |    206 |    103.00 |      103.00 | NEGMIR     | ever_perfect             | ever         |         4,786 | perfect     |         1,303 |   0.00 |    0.00 |
    | **NEGmir~ever_simple**              |    206 |    0.50 |   1.00 |    3.60 |    285.65 |   0.30 |            2.62 |  7.18 |   583,470 |   291,732 |    206 |    103.00 |      103.00 | NEGMIR     | ever_simple              | ever         |         4,786 | simple      |         7,465 |   0.00 |    0.00 |
    | **NEGany~any_better**               |  4,719 |    0.44 |   0.94 |    3.59 |  4,753.39 |   0.28 |            1.22 | 32.27 | 6,347,364 | 3,173,660 |  5,004 |  2,501.98 |    2,217.02 | NEGATED    | any_better               | any          |        16,238 | better      |        50,827 |   0.00 |    0.00 |
    | **NEGany~particularly_wrong**       |    218 |    0.50 |   1.00 |    3.56 |    302.22 |   0.30 |            2.64 |  7.38 | 6,347,364 | 3,173,660 |    218 |    109.00 |      109.00 | NEGATED    | particularly_wrong       | particularly |        76,162 | wrong       |        21,332 |   0.00 |    0.00 |
    | **NEGany~remotely_true**            |    250 |    0.50 |   1.00 |    3.53 |    334.93 |   0.30 |            2.22 |  7.87 | 6,347,364 | 3,173,660 |    251 |    125.50 |      124.50 | NEGATED    | remotely_true            | remotely     |         6,161 | true        |        34,967 |   0.00 |    0.00 |
    | **NEGany~ever_easy**                |    429 |    0.48 |   0.98 |    3.53 |    525.98 |   0.29 |            1.70 | 10.16 | 6,347,364 | 3,173,660 |    437 |    218.50 |      210.50 | NEGATED    | ever_easy                | ever         |        10,870 | easy        |       108,923 |   0.00 |    0.00 |
    | **COM~ever_closer**                 |    279 |    0.49 |   0.99 |    3.52 |    365.82 |   0.30 |            2.05 |  8.29 | 6,347,364 | 3,173,552 |    281 |    140.49 |      138.51 | COMPLEMENT | ever_closer              | ever         |        10,870 | closer      |         3,686 |   0.00 |    0.00 |
    | **NEGany~necessarily_aware**        |    206 |    0.50 |   1.00 |    3.48 |    285.59 |   0.30 |            2.62 |  7.18 | 6,347,364 | 3,173,660 |    206 |    103.00 |      103.00 | NEGATED    | necessarily_aware        | necessarily  |        42,886 | aware       |        28,973 |   0.00 |    0.00 |
    | **NEGany~exactly_hard**             |    203 |    0.50 |   1.00 |    3.46 |    281.43 |   0.30 |            2.61 |  7.12 | 6,347,364 | 3,173,660 |    203 |    101.50 |      101.50 | NEGATED    | exactly_hard             | exactly      |        44,503 | hard        |        45,061 |   0.00 |    0.00 |
    | **NEGmir~particularly_wrong**       |    212 |    0.50 |   1.00 |    3.39 |    282.64 |   0.30 |            2.15 |  7.25 |   583,470 |   291,732 |    213 |    106.50 |      105.50 | NEGMIR     | particularly_wrong       | particularly |        10,029 | wrong       |         8,506 |   0.00 |    0.00 |
    | **NEGany~immediately_apparent**     |  2,015 |    0.44 |   0.94 |    3.30 |  2,001.83 |   0.27 |            1.20 | 21.02 | 6,347,364 | 3,173,660 |  2,143 |  1,071.49 |      943.51 | NEGATED    | immediately_apparent     | immediately  |        58,040 | apparent    |         9,798 |   0.00 |    0.00 |
    | **NEGany~terribly_surprised**       |    287 |    0.49 |   0.99 |    3.30 |    361.19 |   0.30 |            1.81 |  8.35 | 6,347,364 | 3,173,660 |    291 |    145.50 |      141.50 | NEGATED    | terribly_surprised       | terribly     |        19,802 | surprised   |        10,157 |   0.00 |    0.00 |
    | **NEGany~terribly_exciting**        |    382 |    0.48 |   0.98 |    3.28 |    456.39 |   0.29 |            1.60 |  9.54 | 6,347,364 | 3,173,660 |    391 |    195.50 |      186.50 | NEGATED    | terribly_exciting        | terribly     |        19,802 | exciting    |        20,233 |   0.00 |    0.00 |
    | **NEGany~ever_simple**              |    211 |    0.50 |   1.00 |    3.28 |    281.20 |   0.30 |            2.15 |  7.23 | 6,347,364 | 3,173,660 |    212 |    106.00 |      105.00 | NEGATED    | ever_simple              | ever         |        10,870 | simple      |        46,867 |   0.00 |    0.00 |
    | **NEGmir~any_better**               |    380 |    0.47 |   0.97 |    3.27 |    447.88 |   0.29 |            1.56 |  9.49 |   583,470 |   291,732 |    390 |    195.00 |      185.00 | NEGMIR     | any_better               | any          |         1,095 | better      |         3,831 |   0.00 |    0.00 |
    | **NEGmir~particularly_surprising**  |    166 |    0.50 |   1.00 |    3.27 |    230.18 |   0.30 |            2.52 |  6.44 |   583,470 |   291,732 |    166 |     83.00 |       83.00 | NEGMIR     | particularly_surprising  | particularly |        10,029 | surprising  |         1,248 |   0.00 |    0.00 |
    | **NEGmir~particularly_good**        |    390 |    0.47 |   0.97 |    3.24 |    455.35 |   0.29 |            1.53 |  9.60 |   583,470 |   291,732 |    401 |    200.50 |      189.50 | NEGMIR     | particularly_good        | particularly |        10,029 | good        |        13,423 |   0.00 |    0.00 |
    | **NEGmir~that_easy**                |    450 |    0.47 |   0.97 |    3.23 |    512.43 |   0.29 |            1.46 | 10.25 |   583,470 |   291,732 |    465 |    232.50 |      217.50 | NEGMIR     | that_easy                | that         |         4,559 | easy        |         7,749 |   0.00 |    0.00 |
    | **NEGmir~exactly_sure**             |    148 |    0.50 |   1.00 |    3.10 |    205.21 |   0.30 |            2.47 |  6.08 |   583,470 |   291,732 |    148 |     74.00 |       74.00 | NEGMIR     | exactly_sure             | exactly      |           869 | sure        |         5,978 |   0.00 |    0.00 |
    | **NEGmir~ever_enough**              |    147 |    0.50 |   1.00 |    3.09 |    203.83 |   0.30 |            2.47 |  6.06 |   583,470 |   291,732 |    147 |     73.50 |       73.50 | NEGMIR     | ever_enough              | ever         |         4,786 | enough      |         1,326 |   0.00 |    0.00 |
    | **COM~ever_greater**                |    186 |    0.49 |   0.99 |    3.09 |    246.80 |   0.30 |            2.09 |  6.78 | 6,347,364 | 3,173,552 |    187 |     93.50 |       92.50 | COMPLEMENT | ever_greater             | ever         |        10,870 | greater     |         6,949 |   0.00 |    0.00 |
    | **NEGmir~necessarily_wrong**        |    211 |    0.49 |   0.99 |    3.05 |    265.18 |   0.29 |            1.78 |  7.16 |   583,470 |   291,732 |    214 |    107.00 |      104.00 | NEGMIR     | necessarily_wrong        | necessarily  |           992 | wrong       |         8,506 |   0.00 |    0.00 |
    | **NEGmir~ever_certain**             |    143 |    0.50 |   1.00 |    3.04 |    198.28 |   0.30 |            2.46 |  5.98 |   583,470 |   291,732 |    143 |     71.50 |       71.50 | NEGMIR     | ever_certain             | ever         |         4,786 | certain     |         1,276 |   0.00 |    0.00 |
    | **NEGany~any_different**            |    902 |    0.44 |   0.94 |    3.03 |    905.82 |   0.28 |            1.21 | 14.10 | 6,347,364 | 3,173,660 |    957 |    478.50 |      423.50 | NEGATED    | any_different            | any          |        16,238 | different   |        80,643 |   0.00 |    0.00 |
    | **NEGany~terribly_popular**         |    149 |    0.50 |   1.00 |    2.99 |    206.56 |   0.30 |            2.48 |  6.10 | 6,347,364 | 3,173,660 |    149 |     74.50 |       74.50 | NEGATED    | terribly_popular         | terribly     |        19,802 | popular     |        51,120 |   0.00 |    0.00 |
    | **NEGany~remotely_close**           |    694 |    0.45 |   0.95 |    2.98 |    711.52 |   0.28 |            1.25 | 12.43 | 6,347,364 | 3,173,660 |    733 |    366.50 |      327.50 | NEGATED    | remotely_close           | remotely     |         6,161 | close       |        46,485 |   0.00 |    0.00 |
    | **NEGany~terribly_unusual**         |    146 |    0.50 |   1.00 |    2.96 |    202.40 |   0.30 |            2.47 |  6.04 | 6,347,364 | 3,173,660 |    146 |     73.00 |       73.00 | NEGATED    | terribly_unusual         | terribly     |        19,802 | unusual     |         7,412 |   0.00 |    0.00 |
    | **COM~ever_larger**                 |    139 |    0.50 |   1.00 |    2.88 |    192.71 |   0.30 |            2.45 |  5.90 | 6,347,364 | 3,173,552 |    139 |     69.50 |       69.50 | COMPLEMENT | ever_larger              | ever         |        10,870 | larger      |         7,453 |   0.00 |    0.00 |
    | **NEGany~immediately_sure**         |    138 |    0.50 |   1.00 |    2.87 |    191.31 |   0.30 |            2.44 |  5.87 | 6,347,364 | 3,173,660 |    138 |     69.00 |       69.00 | NEGATED    | immediately_sure         | immediately  |        58,040 | sure        |       134,139 |   0.00 |    0.00 |
    | **NEGany~immediately_successful**   |    290 |    0.47 |   0.97 |    2.87 |    333.73 |   0.29 |            1.49 |  8.25 | 6,347,364 | 3,173,660 |    299 |    149.50 |      140.50 | NEGATED    | immediately_successful   | immediately  |        58,040 | successful  |        31,460 |   0.00 |    0.00 |
    | **COM~particularly_acute**          |    135 |    0.50 |   1.00 |    2.84 |    187.16 |   0.30 |            2.43 |  5.81 | 6,347,364 | 3,173,552 |    135 |     67.50 |       67.50 | COMPLEMENT | particularly_acute       | particularly |        76,162 | acute       |         1,038 |   0.00 |    0.00 |
    | **NEGany~terribly_comfortable**     |    129 |    0.50 |   1.00 |    2.77 |    178.84 |   0.30 |            2.41 |  5.68 | 6,347,364 | 3,173,660 |    129 |     64.50 |       64.50 | NEGATED    | terribly_comfortable     | terribly     |        19,802 | comfortable |        23,908 |   0.00 |    0.00 |
    | **NEGmir~particularly_unusual**     |    170 |    0.48 |   0.98 |    2.72 |    209.60 |   0.29 |            1.69 |  6.40 |   583,470 |   291,732 |    173 |     86.50 |       83.50 | NEGMIR     | particularly_unusual     | particularly |        10,029 | unusual     |           933 |   0.00 |    0.00 |
    | **NEGmir~that_great**               |    286 |    0.46 |   0.96 |    2.71 |    312.65 |   0.28 |            1.36 |  8.10 |   583,470 |   291,732 |    298 |    149.00 |      137.00 | NEGMIR     | that_great               | that         |         4,559 | great       |         2,123 |   0.00 |    0.00 |
    | **NEGmir~ever_able**                |    136 |    0.49 |   0.99 |    2.71 |    178.12 |   0.30 |            1.96 |  5.79 |   583,470 |   291,732 |    137 |     68.50 |       67.50 | NEGMIR     | ever_able                | ever         |         4,786 | able        |         1,891 |   0.00 |    0.00 |
    | **NEGmir~that_good**                |    447 |    0.44 |   0.94 |    2.65 |    441.70 |   0.27 |            1.18 |  9.89 |   583,470 |   291,732 |    476 |    238.00 |      209.00 | NEGMIR     | that_good                | that         |         4,559 | good        |        13,423 |   0.00 |    0.00 |
    | **NEGany~terribly_bright**          |    117 |    0.50 |   1.00 |    2.61 |    162.20 |   0.30 |            2.37 |  5.41 | 6,347,364 | 3,173,660 |    117 |     58.50 |       58.50 | NEGATED    | terribly_bright          | terribly     |        19,802 | bright      |         8,623 |   0.00 |    0.00 |
    | **NEGmir~remotely_close**           |    218 |    0.46 |   0.96 |    2.58 |    244.21 |   0.29 |            1.41 |  7.11 |   583,470 |   291,732 |    226 |    113.00 |      105.00 | NEGMIR     | remotely_close           | remotely     |         1,953 | close       |         4,831 |   0.00 |    0.00 |
    | **COM~ever_higher**                 |    129 |    0.49 |   0.99 |    2.52 |    168.50 |   0.30 |            1.94 |  5.64 | 6,347,364 | 3,173,552 |    130 |     65.00 |       64.00 | COMPLEMENT | ever_higher              | ever         |        10,870 | higher      |        12,992 |   0.00 |    0.00 |
    | **NEGmir~ever_wrong**               |    102 |    0.50 |   1.00 |    2.52 |    141.42 |   0.30 |            2.31 |  5.05 |   583,470 |   291,732 |    102 |     51.00 |       51.00 | NEGMIR     | ever_wrong               | ever         |         4,786 | wrong       |         8,506 |   0.00 |    0.00 |
    | **NEGany~ever_good**                |    331 |    0.45 |   0.95 |    2.52 |    337.56 |   0.28 |            1.23 |  8.57 | 6,347,364 | 3,173,660 |    350 |    175.00 |      156.00 | NEGATED    | ever_good                | ever         |        10,870 | good        |       201,244 |   0.00 |    0.00 |
    | **NEGany~immediately_reachable**    |    109 |    0.50 |   1.00 |    2.50 |    151.11 |   0.30 |            2.34 |  5.22 | 6,347,364 | 3,173,660 |    109 |     54.50 |       54.50 | NEGATED    | immediately_reachable    | immediately  |        58,040 | reachable   |           350 |   0.00 |    0.00 |
    | **NEGany~particularly_athletic**    |    108 |    0.50 |   1.00 |    2.49 |    149.72 |   0.30 |            2.34 |  5.20 | 6,347,364 | 3,173,660 |    108 |     54.00 |       54.00 | NEGATED    | particularly_athletic    | particularly |        76,162 | athletic    |         1,772 |   0.00 |    0.00 |
    | **NEGany~particularly_likeable**    |    106 |    0.50 |   1.00 |    2.46 |    146.95 |   0.30 |            2.33 |  5.15 | 6,347,364 | 3,173,660 |    106 |     53.00 |       53.00 | NEGATED    | particularly_likeable    | particularly |        76,162 | likeable    |           861 |   0.00 |    0.00 |
    | **NEGany~terribly_common**          |    105 |    0.50 |   1.00 |    2.45 |    145.56 |   0.30 |            2.32 |  5.12 | 6,347,364 | 3,173,660 |    105 |     52.50 |       52.50 | NEGATED    | terribly_common          | terribly     |        19,802 | common      |        34,450 |   0.00 |    0.00 |
    | **NEGmir~particularly_original**    |     90 |    0.50 |   1.00 |    2.33 |    124.78 |   0.30 |            2.26 |  4.74 |   583,470 |   291,732 |     90 |     45.00 |       45.00 | NEGMIR     | particularly_original    | particularly |        10,029 | original    |           715 |   0.00 |    0.00 |
    | **NEGany~any_nicer**                |     96 |    0.50 |   1.00 |    2.30 |    133.09 |   0.30 |            2.29 |  4.90 | 6,347,364 | 3,173,660 |     96 |     48.00 |       48.00 | NEGATED    | any_nicer                | any          |        16,238 | nicer       |           642 |   0.00 |    0.00 |
    | **NEGany~remotely_funny**           |    137 |    0.47 |   0.97 |    2.16 |    159.09 |   0.29 |            1.49 |  5.68 | 6,347,364 | 3,173,660 |    141 |     70.50 |       66.50 | NEGATED    | remotely_funny           | remotely     |         6,161 | funny       |        14,992 |   0.00 |    0.00 |
    | **NEGany~inherently_evil**          |    358 |    0.41 |   0.91 |    2.12 |    312.23 |   0.26 |            1.02 |  8.56 | 6,347,364 | 3,173,660 |    392 |    196.00 |      162.00 | NEGATED    | inherently_evil          | inherently   |         8,614 | evil        |         3,171 |   0.00 |    0.00 |
    | **NEGmir~that_big**                 |    113 |    0.47 |   0.97 |    2.08 |    132.98 |   0.29 |            1.51 |  5.17 |   583,470 |   291,732 |    116 |     58.00 |       55.00 | NEGMIR     | that_big                 | that         |         4,559 | big         |         3,134 |   0.00 |    0.00 |
    | **NEGany~particularly_radical**     |     79 |    0.50 |   1.00 |    1.99 |    109.52 |   0.30 |            2.20 |  4.44 | 6,347,364 | 3,173,660 |     79 |     39.50 |       39.50 | NEGATED    | particularly_radical     | particularly |        76,162 | radical     |         2,637 |   0.00 |    0.00 |
    | **NEGany~remotely_interested**      |    330 |    0.41 |   0.91 |    1.99 |    278.69 |   0.26 |            0.98 |  8.15 | 6,347,364 | 3,173,660 |    364 |    182.00 |      148.00 | NEGATED    | remotely_interested      | remotely     |         6,161 | interested  |        34,543 |   0.00 |    0.00 |
    | **NEGany~any_smarter**              |     89 |    0.49 |   0.99 |    1.94 |    113.78 |   0.30 |            1.78 |  4.66 | 6,347,364 | 3,173,660 |     90 |     45.00 |       44.00 | NEGATED    | any_smarter              | any          |        16,238 | smarter     |           733 |   0.00 |    0.00 |
    | **NEGmir~terribly_surprising**      |     67 |    0.50 |   1.00 |    1.85 |     92.89 |   0.30 |            2.13 |  4.09 |   583,470 |   291,732 |     67 |     33.50 |       33.50 | NEGMIR     | terribly_surprising      | terribly     |         2,204 | surprising  |         1,248 |   0.00 |    0.00 |
    | **NEGany~ever_boring**              |     72 |    0.50 |   1.00 |    1.84 |     99.82 |   0.30 |            2.16 |  4.24 | 6,347,364 | 3,173,660 |     72 |     36.00 |       36.00 | NEGATED    | ever_boring              | ever         |        10,870 | boring      |         3,840 |   0.00 |    0.00 |
    | **NEGmir~inherently_bad**           |    148 |    0.44 |   0.94 |    1.83 |    144.52 |   0.27 |            1.15 |  5.67 |   583,470 |   291,732 |    158 |     79.00 |       69.00 | NEGMIR     | inherently_bad           | inherently   |         3,342 | bad         |         4,790 |   0.00 |    0.00 |
    | **NEGany~immediately_certain**      |     70 |    0.50 |   1.00 |    1.80 |     97.04 |   0.30 |            2.15 |  4.18 | 6,347,364 | 3,173,660 |     70 |     35.00 |       35.00 | NEGATED    | immediately_certain      | immediately  |        58,040 | certain     |        11,334 |   0.00 |    0.00 |
    | **NEGmir~that_close**               |     60 |    0.50 |   1.00 |    1.67 |     83.19 |   0.30 |            2.08 |  3.87 |   583,470 |   291,732 |     60 |     30.00 |       30.00 | NEGMIR     | that_close               | that         |         4,559 | close       |         4,831 |   0.00 |    0.00 |
    | **NEGmir~any_worse**                |     87 |    0.47 |   0.97 |    1.66 |     98.47 |   0.29 |            1.40 |  4.50 |   583,470 |   291,732 |     90 |     45.00 |       42.00 | NEGMIR     | any_worse                | any          |         1,095 | worse       |         2,007 |   0.00 |    0.00 |
    | **NEGany~remotely_surprising**      |     75 |    0.49 |   0.99 |    1.66 |     94.71 |   0.30 |            1.70 |  4.27 | 6,347,364 | 3,173,660 |     76 |     38.00 |       37.00 | NEGATED    | remotely_surprising      | remotely     |         6,161 | surprising  |        18,776 |   0.00 |    0.00 |
    | **NEGmir~terribly_new**             |     69 |    0.49 |   0.99 |    1.64 |     86.57 |   0.29 |            1.67 |  4.09 |   583,470 |   291,732 |     70 |     35.00 |       34.00 | NEGMIR     | terribly_new             | terribly     |         2,204 | new         |         4,300 |   0.00 |    0.00 |
    | **NEGany~remotely_comparable**      |    118 |    0.44 |   0.94 |    1.62 |    119.34 |   0.28 |            1.20 |  5.11 | 6,347,364 | 3,173,660 |    125 |     62.50 |       55.50 | NEGATED    | remotely_comparable      | remotely     |         6,161 | comparable  |         2,401 |   0.00 |    0.00 |
    | **NEGmir~ever_black**               |     56 |    0.50 |   1.00 |    1.56 |     77.64 |   0.30 |            2.05 |  3.74 |   583,470 |   291,732 |     56 |     28.00 |       28.00 | NEGMIR     | ever_black               | ever         |         4,786 | black       |           646 |   0.00 |    0.00 |
    | **NEGmir~that_popular**             |     65 |    0.48 |   0.98 |    1.54 |     81.14 |   0.29 |            1.64 |  3.97 |   583,470 |   291,732 |     66 |     33.00 |       32.00 | NEGMIR     | that_popular             | that         |         4,559 | popular     |         2,841 |   0.00 |    0.00 |
    | **NEGmir~particularly_novel**       |     54 |    0.50 |   1.00 |    1.50 |     74.87 |   0.30 |            2.04 |  3.67 |   583,470 |   291,732 |     54 |     27.00 |       27.00 | NEGMIR     | particularly_novel       | particularly |        10,029 | novel       |           179 |   0.00 |    0.00 |
    | **NEGany~remotely_ready**           |     58 |    0.50 |   1.00 |    1.49 |     80.41 |   0.30 |            2.07 |  3.81 | 6,347,364 | 3,173,660 |     58 |     29.00 |       29.00 | NEGATED    | remotely_ready           | remotely     |         6,161 | ready       |        29,583 |   0.00 |    0.00 |
    | **NEGany~any_sweeter**              |     58 |    0.50 |   1.00 |    1.49 |     80.41 |   0.30 |            2.07 |  3.81 | 6,347,364 | 3,173,660 |     58 |     29.00 |       29.00 | NEGATED    | any_sweeter              | any          |        16,238 | sweeter     |           388 |   0.00 |    0.00 |
    | **NEGmir~particularly_religious**   |     53 |    0.50 |   1.00 |    1.47 |     73.48 |   0.30 |            2.03 |  3.64 |   583,470 |   291,732 |     53 |     26.50 |       26.50 | NEGMIR     | particularly_religious   | particularly |        10,029 | religious   |           337 |   0.00 |    0.00 |
    | **NEGany~inherently_better**        |    144 |    0.41 |   0.91 |    1.46 |    124.46 |   0.26 |            1.00 |  5.42 | 6,347,364 | 3,173,660 |    158 |     79.00 |       65.00 | NEGATED    | inherently_better        | inherently   |         8,614 | better      |        50,827 |   0.00 |    0.00 |
    | **NEGany~particularly_flashy**      |     57 |    0.50 |   1.00 |    1.46 |     79.02 |   0.30 |            2.06 |  3.77 | 6,347,364 | 3,173,660 |     57 |     28.50 |       28.50 | NEGATED    | particularly_flashy      | particularly |        76,162 | flashy      |         1,732 |   0.00 |    0.00 |
    | **NEGany~inherently_good**          |    283 |    0.36 |   0.86 |    1.46 |    189.85 |   0.24 |            0.79 |  7.04 | 6,347,364 | 3,173,660 |    329 |    164.50 |      118.50 | NEGATED    | inherently_good          | inherently   |         8,614 | good        |       201,244 |   0.00 |    0.00 |
    | **NEGmir~remotely_true**            |     61 |    0.48 |   0.98 |    1.43 |     75.72 |   0.29 |            1.61 |  3.84 |   583,470 |   291,732 |     62 |     31.00 |       30.00 | NEGMIR     | remotely_true            | remotely     |         1,953 | true        |         2,850 |   0.00 |    0.00 |
    | **NEGany~remotely_similar**         |    152 |    0.40 |   0.90 |    1.39 |    123.97 |   0.25 |            0.94 |  5.48 | 6,347,364 | 3,173,660 |    169 |     84.50 |       67.50 | NEGATED    | remotely_similar         | remotely     |         6,161 | similar     |        11,088 |   0.00 |    0.00 |
    | **NEGany~any_brighter**             |     63 |    0.48 |   0.98 |    1.37 |     78.42 |   0.29 |            1.63 |  3.91 | 6,347,364 | 3,173,660 |     64 |     32.00 |       31.00 | NEGATED    | any_brighter             | any          |        16,238 | brighter    |           640 |   0.00 |    0.00 |
    | **NEGmir~necessarily_bad**          |     50 |    0.50 |   1.00 |    1.37 |     69.32 |   0.30 |            2.00 |  3.54 |   583,470 |   291,732 |     50 |     25.00 |       25.00 | NEGMIR     | necessarily_bad          | necessarily  |           992 | bad         |         4,790 |   0.00 |    0.00 |
    | **NEGmir~immediately_available**    |    162 |    0.38 |   0.88 |    1.34 |    120.41 |   0.25 |            0.86 |  5.50 |   583,470 |   291,732 |    184 |     92.00 |       70.00 | NEGMIR     | immediately_available    | immediately  |           564 | available   |         3,079 |   0.00 |    0.00 |
    | **NEGmir~ever_right**               |     49 |    0.50 |   1.00 |    1.33 |     67.93 |   0.30 |            2.00 |  3.50 |   583,470 |   291,732 |     49 |     24.50 |       24.50 | NEGMIR     | ever_right               | ever         |         4,786 | right       |         2,038 |   0.00 |    0.00 |
    | **NEGany~remotely_related**         |    146 |    0.40 |   0.90 |    1.33 |    116.95 |   0.25 |            0.92 |  5.34 | 6,347,364 | 3,173,660 |    163 |     81.50 |       64.50 | NEGATED    | remotely_related         | remotely     |         6,161 | related     |        14,260 |   0.00 |    0.00 |
    | **COM~ever_deeper**                 |     61 |    0.48 |   0.98 |    1.31 |     75.72 |   0.29 |            1.61 |  3.84 | 6,347,364 | 3,173,552 |     62 |     31.00 |       30.00 | COMPLEMENT | ever_deeper              | ever         |        10,870 | deeper      |         1,768 |   0.00 |    0.00 |
    | **NEGmir~any_different**            |     48 |    0.50 |   1.00 |    1.30 |     66.55 |   0.30 |            1.99 |  3.46 |   583,470 |   291,732 |     48 |     24.00 |       24.00 | NEGMIR     | any_different            | any          |         1,095 | different   |         8,644 |   0.00 |    0.00 |
    | **NEGmir~terribly_interesting**     |     56 |    0.48 |   0.98 |    1.29 |     68.96 |   0.29 |            1.58 |  3.67 |   583,470 |   291,732 |     57 |     28.50 |       27.50 | NEGMIR     | terribly_interesting     | terribly     |         2,204 | interesting |         3,863 |   0.00 |    0.00 |
    | **NEGmir~particularly_innovative**  |     47 |    0.50 |   1.00 |    1.26 |     65.16 |   0.30 |            1.98 |  3.43 |   583,470 |   291,732 |     47 |     23.50 |       23.50 | NEGMIR     | particularly_innovative  | particularly |        10,029 | innovative  |           675 |   0.00 |    0.00 |
    | **NEGmir~that_interested**          |     62 |    0.47 |   0.97 |    1.26 |     70.93 |   0.29 |            1.40 |  3.81 |   583,470 |   291,732 |     64 |     32.00 |       30.00 | NEGMIR     | that_interested          | that         |         4,559 | interested  |         2,877 |   0.00 |    0.00 |
    | **NEGany~inherently_illegal**       |     59 |    0.48 |   0.98 |    1.26 |     73.01 |   0.29 |            1.60 |  3.78 | 6,347,364 | 3,173,660 |     60 |     30.00 |       29.00 | NEGATED    | inherently_illegal       | inherently   |         8,614 | illegal     |         3,580 |   0.00 |    0.00 |
    | **NEGmir~any_easier**               |     61 |    0.47 |   0.97 |    1.23 |     69.61 |   0.29 |            1.39 |  3.78 |   583,470 |   291,732 |     63 |     31.50 |       29.50 | NEGMIR     | any_easier               | any          |         1,095 | easier      |           681 |   0.00 |    0.00 |
    | **NEGmir~terribly_original**        |     45 |    0.50 |   1.00 |    1.19 |     62.39 |   0.30 |            1.96 |  3.35 |   583,470 |   291,732 |     45 |     22.50 |       22.50 | NEGMIR     | terribly_original        | terribly     |         2,204 | original    |           715 |   0.00 |    0.00 |
    | **NEGmir~that_difficult**           |     52 |    0.48 |   0.98 |    1.16 |     63.56 |   0.29 |            1.54 |  3.54 |   583,470 |   291,732 |     53 |     26.50 |       25.50 | NEGMIR     | that_difficult           | that         |         4,559 | difficult   |         4,854 |   0.00 |    0.00 |
    | **NEGmir~exactly_clear**            |     52 |    0.48 |   0.98 |    1.16 |     63.56 |   0.29 |            1.54 |  3.54 |   583,470 |   291,732 |     53 |     26.50 |       25.50 | NEGMIR     | exactly_clear            | exactly      |           869 | clear       |         3,321 |   0.00 |    0.00 |
    | **NEGmir~particularly_comfortable** |     44 |    0.50 |   1.00 |    1.15 |     61.00 |   0.30 |            1.95 |  3.32 |   583,470 |   291,732 |     44 |     22.00 |       22.00 | NEGMIR     | particularly_comfortable | particularly |        10,029 | comfortable |         1,888 |   0.00 |    0.00 |
    | **NEGmir~remotely_comparable**      |     44 |    0.50 |   1.00 |    1.15 |     61.00 |   0.30 |            1.95 |  3.32 |   583,470 |   291,732 |     44 |     22.00 |       22.00 | NEGMIR     | remotely_comparable      | remotely     |         1,953 | comparable  |           158 |   0.00 |    0.00 |
    | **NEGany~remotely_enough**          |     47 |    0.50 |   1.00 |    1.13 |     65.16 |   0.30 |            1.98 |  3.43 | 6,347,364 | 3,173,660 |     47 |     23.50 |       23.50 | NEGATED    | remotely_enough          | remotely     |         6,161 | enough      |        27,603 |   0.00 |    0.00 |
    | **POS~terribly_wrong**              |    319 |    0.30 |   0.80 |    1.06 |    149.75 |   0.20 |            0.59 |  6.63 |   583,470 |   291,729 |    401 |    200.50 |      118.50 | POSMIR     | terribly_wrong           | terribly     |         2,204 | wrong       |         8,506 |   0.00 |    0.00 |
    | **COM~ever_mindful**                |     52 |    0.48 |   0.98 |    1.04 |     63.56 |   0.29 |            1.54 |  3.54 | 6,347,364 | 3,173,552 |     53 |     26.50 |       25.50 | COMPLEMENT | ever_mindful             | ever         |        10,870 | mindful     |           784 |   0.00 |    0.00 |
    | **NEGmir~that_happy**               |     41 |    0.50 |   1.00 |    1.03 |     56.84 |   0.30 |            1.92 |  3.20 |   583,470 |   291,732 |     41 |     20.50 |       20.50 | NEGMIR     | that_happy               | that         |         4,559 | happy       |         5,463 |   0.00 |    0.00 |
    



|                                     |    `f` |   `dP1` |   `P1` |   `LRC` |      `G2` |   `MI` |   `odds_r_disc` |   `t` |       `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` | `l1`       | `l2`                     | `adv`        |   `adv_total` | `adj`       |   `adj_total` |
|:------------------------------------|-------:|--------:|-------:|--------:|----------:|-------:|----------------:|------:|----------:|----------:|-------:|----------:|------------:|:-----------|:-------------------------|:-------------|--------------:|:------------|--------------:|
| **NEGany~yet_clear**                | 10,406 |    0.50 |   1.00 |    8.66 | 14,392.25 |   0.30 |            3.47 | 50.99 | 6,347,364 | 3,173,660 | 10,409 |  5,204.46 |    5,201.54 | NEGATED    | yet_clear                | yet          |        53,881 | clear       |        84,227 |
| **NEGany~yet_ready**                |  7,501 |    0.50 |   1.00 |    8.06 | 10,344.81 |   0.30 |            3.22 | 43.28 | 6,347,364 | 3,173,660 |  7,505 |  3,752.47 |    3,748.53 | NEGATED    | yet_ready                | yet          |        53,881 | ready       |        29,583 |
| **NEGany~that_hard**                |  9,948 |    0.50 |   1.00 |    7.68 | 13,602.42 |   0.30 |            2.81 | 49.79 | 6,347,364 | 3,173,660 |  9,963 |  4,981.47 |    4,966.53 | NEGATED    | that_hard                | that         |       166,676 | hard        |        45,061 |
| **NEGany~immediately_clear**        | 24,416 |    0.50 |   1.00 |    7.55 | 33,058.44 |   0.30 |            2.53 | 77.90 | 6,347,364 | 3,173,660 | 24,488 | 12,243.92 |   12,172.08 | NEGATED    | immediately_clear        | immediately  |        58,040 | clear       |        84,227 |
| **NEGany~exactly_sure**             |  8,794 |    0.50 |   1.00 |    7.46 | 11,991.61 |   0.30 |            2.73 | 46.80 | 6,347,364 | 3,173,660 |  8,810 |  4,404.97 |    4,389.03 | NEGATED    | exactly_sure             | exactly      |        44,503 | sure        |       134,139 |
| **NEGany~that_different**           |  6,534 |    0.50 |   1.00 |    7.18 |  8,895.12 |   0.30 |            2.69 | 40.34 | 6,347,364 | 3,173,660 |  6,547 |  3,273.48 |    3,260.52 | NEGATED    | that_different           | that         |       166,676 | different   |        80,643 |
| **NEGany~that_great**               | 11,032 |    0.50 |   1.00 |    7.18 | 14,908.90 |   0.30 |            2.52 | 52.36 | 6,347,364 | 3,173,660 | 11,065 |  5,532.46 |    5,499.54 | NEGATED    | that_great               | that         |       166,676 | great       |        45,359 |
| **NEGany~that_difficult**           |  5,560 |    0.50 |   1.00 |    7.06 |  7,569.00 |   0.30 |            2.69 | 37.21 | 6,347,364 | 3,173,660 |  5,571 |  2,785.48 |    2,774.52 | NEGATED    | that_difficult           | that         |       166,676 | difficult   |        61,490 |
| **NEGany~yet_complete**             |  2,174 |    0.50 |   1.00 |    6.70 |  2,998.60 |   0.30 |            3.16 | 23.30 | 6,347,364 | 3,173,660 |  2,175 |  1,087.49 |    1,086.51 | NEGATED    | yet_complete             | yet          |        53,881 | complete    |         8,415 |
| **NEGany~yet_available**            |  7,430 |    0.50 |   1.00 |    6.66 |  9,950.03 |   0.30 |            2.37 | 42.92 | 6,347,364 | 3,173,660 |  7,461 |  3,730.47 |    3,699.53 | NEGATED    | yet_available            | yet          |        53,881 | available   |        82,956 |
| **NEGany~that_big**                 |  6,244 |    0.50 |   1.00 |    6.47 |  8,332.69 |   0.30 |            2.33 | 39.33 | 6,347,364 | 3,173,660 |  6,273 |  3,136.48 |    3,107.52 | NEGATED    | that_big                 | that         |       166,676 | big         |        42,912 |
| **NEGany~exactly_clear**            |  1,746 |    0.50 |   1.00 |    6.38 |  2,405.43 |   0.30 |            3.07 | 20.88 | 6,347,364 | 3,173,660 |  1,747 |    873.49 |      872.51 | NEGATED    | exactly_clear            | exactly      |        44,503 | clear       |        84,227 |
| **NEGany~necessarily_bad**          |  2,059 |    0.50 |   1.00 |    6.31 |  2,814.04 |   0.30 |            2.77 | 22.66 | 6,347,364 | 3,173,660 |  2,062 |  1,030.99 |    1,028.01 | NEGATED    | necessarily_bad          | necessarily  |        42,886 | bad         |       119,509 |
| **NEGany~necessarily_indicative**   |  1,389 |    0.50 |   1.00 |    6.29 |  1,925.89 |   0.30 |            3.44 | 18.63 | 6,347,364 | 3,173,660 |  1,389 |    694.50 |      694.50 | NEGATED    | necessarily_indicative   | necessarily  |        42,886 | indicative  |         2,313 |
| **NEGany~necessarily_true**         |  3,232 |    0.50 |   1.00 |    6.16 |  4,330.74 |   0.30 |            2.38 | 28.31 | 6,347,364 | 3,173,660 |  3,245 |  1,622.49 |    1,609.51 | NEGATED    | necessarily_true         | necessarily  |        42,886 | true        |        34,967 |
| **NEGany~yet_sure**                 |  1,977 |    0.50 |   1.00 |    6.13 |  2,689.26 |   0.30 |            2.64 | 22.19 | 6,347,364 | 3,173,660 |  1,981 |    990.49 |      986.51 | NEGATED    | yet_sure                 | yet          |        53,881 | sure        |       134,139 |
| **NEGany~necessarily_better**       |  1,887 |    0.50 |   1.00 |    6.07 |  2,564.81 |   0.30 |            2.62 | 21.67 | 6,347,364 | 3,173,660 |  1,891 |    945.49 |      941.51 | NEGATED    | necessarily_better       | necessarily  |        42,886 | better      |        50,827 |
| **NEGany~exactly_new**              |  1,371 |    0.50 |   1.00 |    6.03 |  1,885.86 |   0.30 |            2.96 | 18.50 | 6,347,364 | 3,173,660 |  1,372 |    686.00 |      685.00 | NEGATED    | exactly_new              | exactly      |        44,503 | new         |        21,538 |
| **NEGany~that_surprising**          |  1,133 |    0.50 |   1.00 |    5.99 |  1,570.89 |   0.30 |            3.36 | 16.83 | 6,347,364 | 3,173,660 |  1,133 |    566.50 |      566.50 | NEGATED    | that_surprising          | that         |       166,676 | surprising  |        18,776 |
| **NEGany~that_unusual**             |    977 |    0.50 |   1.00 |    5.77 |  1,354.57 |   0.30 |            3.29 | 15.63 | 6,347,364 | 3,173,660 |    977 |    488.50 |      488.50 | NEGATED    | that_unusual             | that         |       166,676 | unusual     |         7,412 |
| **NEGany~terribly_surprising**      |    949 |    0.50 |   1.00 |    5.73 |  1,315.75 |   0.30 |            3.28 | 15.40 | 6,347,364 | 3,173,660 |    949 |    474.50 |      474.50 | NEGATED    | terribly_surprising      | terribly     |        19,802 | surprising  |        18,776 |
| **NEGany~necessarily_easy**         |    909 |    0.50 |   1.00 |    5.67 |  1,260.28 |   0.30 |            3.26 | 15.07 | 6,347,364 | 3,173,660 |    909 |    454.50 |      454.50 | NEGATED    | necessarily_easy         | necessarily  |        42,886 | easy        |       108,923 |
| **NEGany~exactly_easy**             |  1,066 |    0.50 |   1.00 |    5.67 |  1,463.43 |   0.30 |            2.85 | 16.31 | 6,347,364 | 3,173,660 |  1,067 |    533.50 |      532.50 | NEGATED    | exactly_easy             | exactly      |        44,503 | easy        |       108,923 |
| **NEGany~yet_certain**              |    866 |    0.50 |   1.00 |    5.60 |  1,200.66 |   0.30 |            3.24 | 14.71 | 6,347,364 | 3,173,660 |    866 |    433.00 |      433.00 | NEGATED    | yet_certain              | yet          |        53,881 | certain     |        11,334 |
| **NEGany~that_exciting**            |    805 |    0.50 |   1.00 |    5.49 |  1,116.08 |   0.30 |            3.21 | 14.19 | 6,347,364 | 3,173,660 |    805 |    402.50 |      402.50 | NEGATED    | that_exciting            | that         |       166,676 | exciting    |        20,233 |
| **NEGany~that_uncommon**            |    802 |    0.50 |   1.00 |    5.49 |  1,111.92 |   0.30 |            3.21 | 14.16 | 6,347,364 | 3,173,660 |    802 |    401.00 |      401.00 | NEGATED    | that_uncommon            | that         |       166,676 | uncommon    |         3,165 |
| **NEGany~yet_able**                 |  1,315 |    0.50 |   1.00 |    5.44 |  1,764.46 |   0.30 |            2.38 | 18.06 | 6,347,364 | 3,173,660 |  1,320 |    660.00 |      655.00 | NEGATED    | yet_able                 | yet          |        53,881 | able        |        23,355 |
| **NEGany~immediately_possible**     |  1,000 |    0.50 |   1.00 |    5.40 |  1,360.38 |   0.30 |            2.60 | 15.78 | 6,347,364 | 3,173,660 |  1,002 |    501.00 |      499.00 | NEGATED    | immediately_possible     | immediately  |        58,040 | possible    |        30,446 |
| **NEGany~immediately_available**    | 21,078 |    0.48 |   0.98 |    5.34 | 25,870.14 |   0.29 |            1.73 | 71.22 | 6,347,364 | 3,173,660 | 21,477 | 10,738.43 |   10,339.57 | NEGATED    | immediately_available    | immediately  |        58,040 | available   |        82,956 |
| **NEGany~exactly_cheap**            |    691 |    0.50 |   1.00 |    5.27 |    958.01 |   0.30 |            3.14 | 13.14 | 6,347,364 | 3,173,660 |    691 |    345.50 |      345.50 | NEGATED    | exactly_cheap            | exactly      |        44,503 | cheap       |         6,591 |
| **NEGany~that_impressed**           |    681 |    0.50 |   1.00 |    5.25 |    944.15 |   0.30 |            3.13 | 13.05 | 6,347,364 | 3,173,660 |    681 |    340.50 |      340.50 | NEGATED    | that_impressed           | that         |       166,676 | impressed   |        12,138 |
| **NEGany~yet_final**                |    640 |    0.50 |   1.00 |    5.16 |    887.30 |   0.30 |            3.11 | 12.65 | 6,347,364 | 3,173,660 |    640 |    320.00 |      320.00 | NEGATED    | yet_final                | yet          |        53,881 | final       |         1,213 |
| **NEGany~necessarily_related**      |    741 |    0.50 |   1.00 |    5.14 |  1,013.51 |   0.30 |            2.69 | 13.59 | 6,347,364 | 3,173,660 |    742 |    371.00 |      370.00 | NEGATED    | necessarily_related      | necessarily  |        42,886 | related     |        14,260 |
| **NEGany~necessarily_new**          |    482 |    0.50 |   1.00 |    4.74 |    668.24 |   0.30 |            2.98 | 10.98 | 6,347,364 | 3,173,660 |    482 |    241.00 |      241.00 | NEGATED    | necessarily_new          | necessarily  |        42,886 | new         |        21,538 |
| **NEGany~yet_public**               |    467 |    0.50 |   1.00 |    4.69 |    647.44 |   0.30 |            2.97 | 10.81 | 6,347,364 | 3,173,660 |    467 |    233.50 |      233.50 | NEGATED    | yet_public               | yet          |        53,881 | public      |         2,656 |
| **NEGany~any_happier**              |    828 |    0.49 |   0.99 |    4.66 |  1,085.12 |   0.30 |            2.11 | 14.28 | 6,347,364 | 3,173,660 |    834 |    417.00 |      411.00 | NEGATED    | any_happier              | any          |        16,238 | happier     |         2,004 |
| **NEGany~particularly_new**         |    747 |    0.49 |   0.99 |    4.61 |    982.49 |   0.30 |            2.13 | 13.57 | 6,347,364 | 3,173,660 |    752 |    376.00 |      371.00 | NEGATED    | particularly_new         | particularly |        76,162 | new         |        21,538 |
| **NEGany~exactly_surprising**       |    440 |    0.50 |   1.00 |    4.61 |    610.01 |   0.30 |            2.95 | 10.49 | 6,347,364 | 3,173,660 |    440 |    220.00 |      220.00 | NEGATED    | exactly_surprising       | exactly      |        44,503 | surprising  |        18,776 |
| **NEGany~particularly_religious**   |    485 |    0.50 |   1.00 |    4.52 |    659.41 |   0.30 |            2.51 | 10.99 | 6,347,364 | 3,173,660 |    486 |    243.00 |      242.00 | NEGATED    | particularly_religious   | particularly |        76,162 | religious   |         3,507 |
| **NEGany~yet_dead**                 |    401 |    0.50 |   1.00 |    4.47 |    555.93 |   0.30 |            2.90 | 10.01 | 6,347,364 | 3,173,660 |    401 |    200.50 |      200.50 | NEGATED    | yet_dead                 | yet          |        53,881 | dead        |         6,348 |
| **NEGany~any_easier**               |  1,594 |    0.48 |   0.98 |    4.42 |  1,946.26 |   0.29 |            1.70 | 19.57 | 6,347,364 | 3,173,660 |  1,625 |    812.49 |      781.51 | NEGATED    | any_easier               | any          |        16,238 | easier      |        12,877 |
| **NEGmir~particularly_new**         |    404 |    0.50 |   1.00 |    4.35 |    547.73 |   0.30 |            2.43 | 10.03 |   583,470 |   291,732 |    405 |    202.50 |      201.50 | NEGMIR     | particularly_new         | particularly |        10,029 | new         |         4,300 |
| **NEGany~inherently_wrong**         |  1,639 |    0.48 |   0.98 |    4.25 |  1,956.12 |   0.29 |            1.62 | 19.76 | 6,347,364 | 3,173,660 |  1,678 |    838.99 |      800.01 | NEGATED    | inherently_wrong         | inherently   |         8,614 | wrong       |        21,332 |
| **NEGany~necessarily_surprising**   |    340 |    0.50 |   1.00 |    4.23 |    471.36 |   0.30 |            2.83 |  9.22 | 6,347,364 | 3,173,660 |    340 |    170.00 |      170.00 | NEGATED    | necessarily_surprising   | necessarily  |        42,886 | surprising  |        18,776 |
| **NEGmir~ever_easy**                |    368 |    0.50 |   1.00 |    4.21 |    497.96 |   0.30 |            2.39 |  9.57 |   583,470 |   291,732 |    369 |    184.50 |      183.50 | NEGMIR     | ever_easy                | ever         |         4,786 | easy        |         7,749 |
| **NEGany~terribly_interested**      |    486 |    0.49 |   0.99 |    3.98 |    624.89 |   0.30 |            1.95 | 10.91 | 6,347,364 | 3,173,660 |    491 |    245.50 |      240.50 | NEGATED    | terribly_interested      | terribly     |        19,802 | interested  |        34,543 |
| **NEGany~necessarily_enough**       |    279 |    0.50 |   1.00 |    3.93 |    386.79 |   0.30 |            2.75 |  8.35 | 6,347,364 | 3,173,660 |    279 |    139.50 |      139.50 | NEGATED    | necessarily_enough       | necessarily  |        42,886 | enough      |        27,603 |
| **NEGany~particularly_surprising**  |  1,069 |    0.47 |   0.97 |    3.93 |  1,260.26 |   0.29 |            1.57 | 15.92 | 6,347,364 | 3,173,660 |  1,097 |    548.50 |      520.50 | NEGATED    | particularly_surprising  | particularly |        76,162 | surprising  |        18,776 |
| **NEGany~terribly_different**       |    366 |    0.49 |   0.99 |    3.93 |    485.33 |   0.30 |            2.17 |  9.51 | 6,347,364 | 3,173,660 |    368 |    184.00 |      182.00 | NEGATED    | terribly_different       | terribly     |        19,802 | different   |        80,643 |
| **NEGmir~ever_good**                |    299 |    0.50 |   1.00 |    3.90 |    402.64 |   0.30 |            2.30 |  8.62 |   583,470 |   291,732 |    300 |    150.00 |      149.00 | NEGMIR     | ever_good                | ever         |         4,786 | good        |        13,423 |
| **NEGany~immediately_obvious**      |  2,238 |    0.46 |   0.96 |    3.88 |  2,481.50 |   0.28 |            1.41 | 22.73 | 6,347,364 | 3,173,660 |  2,325 |  1,162.49 |    1,075.51 | NEGATED    | immediately_obvious      | immediately  |        58,040 | obvious     |        22,651 |
| **NEGany~inherently_bad**           |    794 |    0.48 |   0.98 |    3.87 |    953.05 |   0.29 |            1.63 | 13.77 | 6,347,364 | 3,173,660 |    812 |    406.00 |      388.00 | NEGATED    | inherently_bad           | inherently   |         8,614 | bad         |       119,509 |
| **NEGany~exactly_subtle**           |    263 |    0.50 |   1.00 |    3.84 |    364.61 |   0.30 |            2.72 |  8.11 | 6,347,364 | 3,173,660 |    263 |    131.50 |      131.50 | NEGATED    | exactly_subtle           | exactly      |        44,503 | subtle      |         5,299 |
| **NEGany~exactly_fair**             |    260 |    0.50 |   1.00 |    3.83 |    360.45 |   0.30 |            2.72 |  8.06 | 6,347,364 | 3,173,660 |    260 |    130.00 |      130.00 | NEGATED    | exactly_fair             | exactly      |        44,503 | fair        |         6,964 |
| **NEGany~any_younger**              |    255 |    0.50 |   1.00 |    3.80 |    353.52 |   0.30 |            2.71 |  7.98 | 6,347,364 | 3,173,660 |    255 |    127.50 |      127.50 | NEGATED    | any_younger              | any          |        16,238 | younger     |         1,784 |
| **NEGmir~inherently_wrong**         |  1,513 |    0.46 |   0.96 |    3.78 |  1,685.02 |   0.28 |            1.42 | 18.70 |   583,470 |   291,732 |  1,571 |    785.49 |      727.51 | NEGMIR     | inherently_wrong         | inherently   |         3,342 | wrong       |         8,506 |
| **NEGmir~that_simple**              |    474 |    0.48 |   0.98 |    3.67 |    580.44 |   0.29 |            1.70 | 10.68 |   583,470 |   291,732 |    483 |    241.50 |      232.50 | NEGMIR     | that_simple              | that         |         4,559 | simple      |         7,465 |
| **NEGany~immediately_able**         |    626 |    0.48 |   0.98 |    3.66 |    746.39 |   0.29 |            1.61 | 12.21 | 6,347,364 | 3,173,660 |    641 |    320.50 |      305.50 | NEGATED    | immediately_able         | immediately  |        58,040 | able        |        23,355 |
| **NEGany~particularly_original**    |    360 |    0.49 |   0.99 |    3.64 |    460.59 |   0.30 |            1.90 |  9.38 | 6,347,364 | 3,173,660 |    364 |    182.00 |      178.00 | NEGATED    | particularly_original    | particularly |        76,162 | original    |         4,693 |
| **NEGany~any_worse**                |  1,686 |    0.46 |   0.96 |    3.62 |  1,816.60 |   0.28 |            1.34 | 19.61 | 6,347,364 | 3,173,660 |  1,762 |    880.99 |      805.01 | NEGATED    | any_worse                | any          |        16,238 | worse       |        12,116 |
| **NEGany~exactly_fun**              |    224 |    0.50 |   1.00 |    3.60 |    310.54 |   0.30 |            2.65 |  7.48 | 6,347,364 | 3,173,660 |    224 |    112.00 |      112.00 | NEGATED    | exactly_fun              | exactly      |        44,503 | fun         |        19,661 |
| **NEGmir~ever_perfect**             |    206 |    0.50 |   1.00 |    3.60 |    285.65 |   0.30 |            2.62 |  7.18 |   583,470 |   291,732 |    206 |    103.00 |      103.00 | NEGMIR     | ever_perfect             | ever         |         4,786 | perfect     |         1,303 |
| **NEGmir~ever_simple**              |    206 |    0.50 |   1.00 |    3.60 |    285.65 |   0.30 |            2.62 |  7.18 |   583,470 |   291,732 |    206 |    103.00 |      103.00 | NEGMIR     | ever_simple              | ever         |         4,786 | simple      |         7,465 |
| **NEGany~any_better**               |  4,719 |    0.44 |   0.94 |    3.59 |  4,753.39 |   0.28 |            1.22 | 32.27 | 6,347,364 | 3,173,660 |  5,004 |  2,501.98 |    2,217.02 | NEGATED    | any_better               | any          |        16,238 | better      |        50,827 |
| **NEGany~particularly_wrong**       |    218 |    0.50 |   1.00 |    3.56 |    302.22 |   0.30 |            2.64 |  7.38 | 6,347,364 | 3,173,660 |    218 |    109.00 |      109.00 | NEGATED    | particularly_wrong       | particularly |        76,162 | wrong       |        21,332 |
| **NEGany~remotely_true**            |    250 |    0.50 |   1.00 |    3.53 |    334.93 |   0.30 |            2.22 |  7.87 | 6,347,364 | 3,173,660 |    251 |    125.50 |      124.50 | NEGATED    | remotely_true            | remotely     |         6,161 | true        |        34,967 |
| **NEGany~ever_easy**                |    429 |    0.48 |   0.98 |    3.53 |    525.98 |   0.29 |            1.70 | 10.16 | 6,347,364 | 3,173,660 |    437 |    218.50 |      210.50 | NEGATED    | ever_easy                | ever         |        10,870 | easy        |       108,923 |
| **COM~ever_closer**                 |    279 |    0.49 |   0.99 |    3.52 |    365.82 |   0.30 |            2.05 |  8.29 | 6,347,364 | 3,173,552 |    281 |    140.49 |      138.51 | COMPLEMENT | ever_closer              | ever         |        10,870 | closer      |         3,686 |
| **NEGany~necessarily_aware**        |    206 |    0.50 |   1.00 |    3.48 |    285.59 |   0.30 |            2.62 |  7.18 | 6,347,364 | 3,173,660 |    206 |    103.00 |      103.00 | NEGATED    | necessarily_aware        | necessarily  |        42,886 | aware       |        28,973 |
| **NEGany~exactly_hard**             |    203 |    0.50 |   1.00 |    3.46 |    281.43 |   0.30 |            2.61 |  7.12 | 6,347,364 | 3,173,660 |    203 |    101.50 |      101.50 | NEGATED    | exactly_hard             | exactly      |        44,503 | hard        |        45,061 |
| **NEGmir~particularly_wrong**       |    212 |    0.50 |   1.00 |    3.39 |    282.64 |   0.30 |            2.15 |  7.25 |   583,470 |   291,732 |    213 |    106.50 |      105.50 | NEGMIR     | particularly_wrong       | particularly |        10,029 | wrong       |         8,506 |
| **NEGany~immediately_apparent**     |  2,015 |    0.44 |   0.94 |    3.30 |  2,001.83 |   0.27 |            1.20 | 21.02 | 6,347,364 | 3,173,660 |  2,143 |  1,071.49 |      943.51 | NEGATED    | immediately_apparent     | immediately  |        58,040 | apparent    |         9,798 |
| **NEGany~terribly_surprised**       |    287 |    0.49 |   0.99 |    3.30 |    361.19 |   0.30 |            1.81 |  8.35 | 6,347,364 | 3,173,660 |    291 |    145.50 |      141.50 | NEGATED    | terribly_surprised       | terribly     |        19,802 | surprised   |        10,157 |
| **NEGany~terribly_exciting**        |    382 |    0.48 |   0.98 |    3.28 |    456.39 |   0.29 |            1.60 |  9.54 | 6,347,364 | 3,173,660 |    391 |    195.50 |      186.50 | NEGATED    | terribly_exciting        | terribly     |        19,802 | exciting    |        20,233 |
| **NEGany~ever_simple**              |    211 |    0.50 |   1.00 |    3.28 |    281.20 |   0.30 |            2.15 |  7.23 | 6,347,364 | 3,173,660 |    212 |    106.00 |      105.00 | NEGATED    | ever_simple              | ever         |        10,870 | simple      |        46,867 |
| **NEGmir~any_better**               |    380 |    0.47 |   0.97 |    3.27 |    447.88 |   0.29 |            1.56 |  9.49 |   583,470 |   291,732 |    390 |    195.00 |      185.00 | NEGMIR     | any_better               | any          |         1,095 | better      |         3,831 |
| **NEGmir~particularly_surprising**  |    166 |    0.50 |   1.00 |    3.27 |    230.18 |   0.30 |            2.52 |  6.44 |   583,470 |   291,732 |    166 |     83.00 |       83.00 | NEGMIR     | particularly_surprising  | particularly |        10,029 | surprising  |         1,248 |
| **NEGmir~particularly_good**        |    390 |    0.47 |   0.97 |    3.24 |    455.35 |   0.29 |            1.53 |  9.60 |   583,470 |   291,732 |    401 |    200.50 |      189.50 | NEGMIR     | particularly_good        | particularly |        10,029 | good        |        13,423 |
| **NEGmir~that_easy**                |    450 |    0.47 |   0.97 |    3.23 |    512.43 |   0.29 |            1.46 | 10.25 |   583,470 |   291,732 |    465 |    232.50 |      217.50 | NEGMIR     | that_easy                | that         |         4,559 | easy        |         7,749 |
| **NEGmir~exactly_sure**             |    148 |    0.50 |   1.00 |    3.10 |    205.21 |   0.30 |            2.47 |  6.08 |   583,470 |   291,732 |    148 |     74.00 |       74.00 | NEGMIR     | exactly_sure             | exactly      |           869 | sure        |         5,978 |
| **NEGmir~ever_enough**              |    147 |    0.50 |   1.00 |    3.09 |    203.83 |   0.30 |            2.47 |  6.06 |   583,470 |   291,732 |    147 |     73.50 |       73.50 | NEGMIR     | ever_enough              | ever         |         4,786 | enough      |         1,326 |
| **COM~ever_greater**                |    186 |    0.49 |   0.99 |    3.09 |    246.80 |   0.30 |            2.09 |  6.78 | 6,347,364 | 3,173,552 |    187 |     93.50 |       92.50 | COMPLEMENT | ever_greater             | ever         |        10,870 | greater     |         6,949 |
| **NEGmir~necessarily_wrong**        |    211 |    0.49 |   0.99 |    3.05 |    265.18 |   0.29 |            1.78 |  7.16 |   583,470 |   291,732 |    214 |    107.00 |      104.00 | NEGMIR     | necessarily_wrong        | necessarily  |           992 | wrong       |         8,506 |
| **NEGmir~ever_certain**             |    143 |    0.50 |   1.00 |    3.04 |    198.28 |   0.30 |            2.46 |  5.98 |   583,470 |   291,732 |    143 |     71.50 |       71.50 | NEGMIR     | ever_certain             | ever         |         4,786 | certain     |         1,276 |
| **NEGany~any_different**            |    902 |    0.44 |   0.94 |    3.03 |    905.82 |   0.28 |            1.21 | 14.10 | 6,347,364 | 3,173,660 |    957 |    478.50 |      423.50 | NEGATED    | any_different            | any          |        16,238 | different   |        80,643 |
| **NEGany~terribly_popular**         |    149 |    0.50 |   1.00 |    2.99 |    206.56 |   0.30 |            2.48 |  6.10 | 6,347,364 | 3,173,660 |    149 |     74.50 |       74.50 | NEGATED    | terribly_popular         | terribly     |        19,802 | popular     |        51,120 |
| **NEGany~remotely_close**           |    694 |    0.45 |   0.95 |    2.98 |    711.52 |   0.28 |            1.25 | 12.43 | 6,347,364 | 3,173,660 |    733 |    366.50 |      327.50 | NEGATED    | remotely_close           | remotely     |         6,161 | close       |        46,485 |
| **NEGany~terribly_unusual**         |    146 |    0.50 |   1.00 |    2.96 |    202.40 |   0.30 |            2.47 |  6.04 | 6,347,364 | 3,173,660 |    146 |     73.00 |       73.00 | NEGATED    | terribly_unusual         | terribly     |        19,802 | unusual     |         7,412 |
| **COM~ever_larger**                 |    139 |    0.50 |   1.00 |    2.88 |    192.71 |   0.30 |            2.45 |  5.90 | 6,347,364 | 3,173,552 |    139 |     69.50 |       69.50 | COMPLEMENT | ever_larger              | ever         |        10,870 | larger      |         7,453 |
| **NEGany~immediately_sure**         |    138 |    0.50 |   1.00 |    2.87 |    191.31 |   0.30 |            2.44 |  5.87 | 6,347,364 | 3,173,660 |    138 |     69.00 |       69.00 | NEGATED    | immediately_sure         | immediately  |        58,040 | sure        |       134,139 |
| **NEGany~immediately_successful**   |    290 |    0.47 |   0.97 |    2.87 |    333.73 |   0.29 |            1.49 |  8.25 | 6,347,364 | 3,173,660 |    299 |    149.50 |      140.50 | NEGATED    | immediately_successful   | immediately  |        58,040 | successful  |        31,460 |
| **COM~particularly_acute**          |    135 |    0.50 |   1.00 |    2.84 |    187.16 |   0.30 |            2.43 |  5.81 | 6,347,364 | 3,173,552 |    135 |     67.50 |       67.50 | COMPLEMENT | particularly_acute       | particularly |        76,162 | acute       |         1,038 |
| **NEGany~terribly_comfortable**     |    129 |    0.50 |   1.00 |    2.77 |    178.84 |   0.30 |            2.41 |  5.68 | 6,347,364 | 3,173,660 |    129 |     64.50 |       64.50 | NEGATED    | terribly_comfortable     | terribly     |        19,802 | comfortable |        23,908 |
| **NEGmir~particularly_unusual**     |    170 |    0.48 |   0.98 |    2.72 |    209.60 |   0.29 |            1.69 |  6.40 |   583,470 |   291,732 |    173 |     86.50 |       83.50 | NEGMIR     | particularly_unusual     | particularly |        10,029 | unusual     |           933 |
| **NEGmir~that_great**               |    286 |    0.46 |   0.96 |    2.71 |    312.65 |   0.28 |            1.36 |  8.10 |   583,470 |   291,732 |    298 |    149.00 |      137.00 | NEGMIR     | that_great               | that         |         4,559 | great       |         2,123 |
| **NEGmir~ever_able**                |    136 |    0.49 |   0.99 |    2.71 |    178.12 |   0.30 |            1.96 |  5.79 |   583,470 |   291,732 |    137 |     68.50 |       67.50 | NEGMIR     | ever_able                | ever         |         4,786 | able        |         1,891 |
| **NEGmir~that_good**                |    447 |    0.44 |   0.94 |    2.65 |    441.70 |   0.27 |            1.18 |  9.89 |   583,470 |   291,732 |    476 |    238.00 |      209.00 | NEGMIR     | that_good                | that         |         4,559 | good        |        13,423 |
| **NEGany~terribly_bright**          |    117 |    0.50 |   1.00 |    2.61 |    162.20 |   0.30 |            2.37 |  5.41 | 6,347,364 | 3,173,660 |    117 |     58.50 |       58.50 | NEGATED    | terribly_bright          | terribly     |        19,802 | bright      |         8,623 |
| **NEGmir~remotely_close**           |    218 |    0.46 |   0.96 |    2.58 |    244.21 |   0.29 |            1.41 |  7.11 |   583,470 |   291,732 |    226 |    113.00 |      105.00 | NEGMIR     | remotely_close           | remotely     |         1,953 | close       |         4,831 |
| **COM~ever_higher**                 |    129 |    0.49 |   0.99 |    2.52 |    168.50 |   0.30 |            1.94 |  5.64 | 6,347,364 | 3,173,552 |    130 |     65.00 |       64.00 | COMPLEMENT | ever_higher              | ever         |        10,870 | higher      |        12,992 |
| **NEGmir~ever_wrong**               |    102 |    0.50 |   1.00 |    2.52 |    141.42 |   0.30 |            2.31 |  5.05 |   583,470 |   291,732 |    102 |     51.00 |       51.00 | NEGMIR     | ever_wrong               | ever         |         4,786 | wrong       |         8,506 |
| **NEGany~ever_good**                |    331 |    0.45 |   0.95 |    2.52 |    337.56 |   0.28 |            1.23 |  8.57 | 6,347,364 | 3,173,660 |    350 |    175.00 |      156.00 | NEGATED    | ever_good                | ever         |        10,870 | good        |       201,244 |
| **NEGany~immediately_reachable**    |    109 |    0.50 |   1.00 |    2.50 |    151.11 |   0.30 |            2.34 |  5.22 | 6,347,364 | 3,173,660 |    109 |     54.50 |       54.50 | NEGATED    | immediately_reachable    | immediately  |        58,040 | reachable   |           350 |
| **NEGany~particularly_athletic**    |    108 |    0.50 |   1.00 |    2.49 |    149.72 |   0.30 |            2.34 |  5.20 | 6,347,364 | 3,173,660 |    108 |     54.00 |       54.00 | NEGATED    | particularly_athletic    | particularly |        76,162 | athletic    |         1,772 |
| **NEGany~particularly_likeable**    |    106 |    0.50 |   1.00 |    2.46 |    146.95 |   0.30 |            2.33 |  5.15 | 6,347,364 | 3,173,660 |    106 |     53.00 |       53.00 | NEGATED    | particularly_likeable    | particularly |        76,162 | likeable    |           861 |
| **NEGany~terribly_common**          |    105 |    0.50 |   1.00 |    2.45 |    145.56 |   0.30 |            2.32 |  5.12 | 6,347,364 | 3,173,660 |    105 |     52.50 |       52.50 | NEGATED    | terribly_common          | terribly     |        19,802 | common      |        34,450 |
| **NEGmir~particularly_original**    |     90 |    0.50 |   1.00 |    2.33 |    124.78 |   0.30 |            2.26 |  4.74 |   583,470 |   291,732 |     90 |     45.00 |       45.00 | NEGMIR     | particularly_original    | particularly |        10,029 | original    |           715 |
| **NEGany~any_nicer**                |     96 |    0.50 |   1.00 |    2.30 |    133.09 |   0.30 |            2.29 |  4.90 | 6,347,364 | 3,173,660 |     96 |     48.00 |       48.00 | NEGATED    | any_nicer                | any          |        16,238 | nicer       |           642 |
| **NEGany~remotely_funny**           |    137 |    0.47 |   0.97 |    2.16 |    159.09 |   0.29 |            1.49 |  5.68 | 6,347,364 | 3,173,660 |    141 |     70.50 |       66.50 | NEGATED    | remotely_funny           | remotely     |         6,161 | funny       |        14,992 |
| **NEGany~inherently_evil**          |    358 |    0.41 |   0.91 |    2.12 |    312.23 |   0.26 |            1.02 |  8.56 | 6,347,364 | 3,173,660 |    392 |    196.00 |      162.00 | NEGATED    | inherently_evil          | inherently   |         8,614 | evil        |         3,171 |
| **NEGmir~that_big**                 |    113 |    0.47 |   0.97 |    2.08 |    132.98 |   0.29 |            1.51 |  5.17 |   583,470 |   291,732 |    116 |     58.00 |       55.00 | NEGMIR     | that_big                 | that         |         4,559 | big         |         3,134 |
| **NEGany~particularly_radical**     |     79 |    0.50 |   1.00 |    1.99 |    109.52 |   0.30 |            2.20 |  4.44 | 6,347,364 | 3,173,660 |     79 |     39.50 |       39.50 | NEGATED    | particularly_radical     | particularly |        76,162 | radical     |         2,637 |
| **NEGany~remotely_interested**      |    330 |    0.41 |   0.91 |    1.99 |    278.69 |   0.26 |            0.98 |  8.15 | 6,347,364 | 3,173,660 |    364 |    182.00 |      148.00 | NEGATED    | remotely_interested      | remotely     |         6,161 | interested  |        34,543 |
| **NEGany~any_smarter**              |     89 |    0.49 |   0.99 |    1.94 |    113.78 |   0.30 |            1.78 |  4.66 | 6,347,364 | 3,173,660 |     90 |     45.00 |       44.00 | NEGATED    | any_smarter              | any          |        16,238 | smarter     |           733 |
| **NEGmir~terribly_surprising**      |     67 |    0.50 |   1.00 |    1.85 |     92.89 |   0.30 |            2.13 |  4.09 |   583,470 |   291,732 |     67 |     33.50 |       33.50 | NEGMIR     | terribly_surprising      | terribly     |         2,204 | surprising  |         1,248 |
| **NEGany~ever_boring**              |     72 |    0.50 |   1.00 |    1.84 |     99.82 |   0.30 |            2.16 |  4.24 | 6,347,364 | 3,173,660 |     72 |     36.00 |       36.00 | NEGATED    | ever_boring              | ever         |        10,870 | boring      |         3,840 |
| **NEGmir~inherently_bad**           |    148 |    0.44 |   0.94 |    1.83 |    144.52 |   0.27 |            1.15 |  5.67 |   583,470 |   291,732 |    158 |     79.00 |       69.00 | NEGMIR     | inherently_bad           | inherently   |         3,342 | bad         |         4,790 |
| **NEGany~immediately_certain**      |     70 |    0.50 |   1.00 |    1.80 |     97.04 |   0.30 |            2.15 |  4.18 | 6,347,364 | 3,173,660 |     70 |     35.00 |       35.00 | NEGATED    | immediately_certain      | immediately  |        58,040 | certain     |        11,334 |
| **NEGmir~that_close**               |     60 |    0.50 |   1.00 |    1.67 |     83.19 |   0.30 |            2.08 |  3.87 |   583,470 |   291,732 |     60 |     30.00 |       30.00 | NEGMIR     | that_close               | that         |         4,559 | close       |         4,831 |
| **NEGmir~any_worse**                |     87 |    0.47 |   0.97 |    1.66 |     98.47 |   0.29 |            1.40 |  4.50 |   583,470 |   291,732 |     90 |     45.00 |       42.00 | NEGMIR     | any_worse                | any          |         1,095 | worse       |         2,007 |
| **NEGany~remotely_surprising**      |     75 |    0.49 |   0.99 |    1.66 |     94.71 |   0.30 |            1.70 |  4.27 | 6,347,364 | 3,173,660 |     76 |     38.00 |       37.00 | NEGATED    | remotely_surprising      | remotely     |         6,161 | surprising  |        18,776 |
| **NEGmir~terribly_new**             |     69 |    0.49 |   0.99 |    1.64 |     86.57 |   0.29 |            1.67 |  4.09 |   583,470 |   291,732 |     70 |     35.00 |       34.00 | NEGMIR     | terribly_new             | terribly     |         2,204 | new         |         4,300 |
| **NEGany~remotely_comparable**      |    118 |    0.44 |   0.94 |    1.62 |    119.34 |   0.28 |            1.20 |  5.11 | 6,347,364 | 3,173,660 |    125 |     62.50 |       55.50 | NEGATED    | remotely_comparable      | remotely     |         6,161 | comparable  |         2,401 |
| **NEGmir~ever_black**               |     56 |    0.50 |   1.00 |    1.56 |     77.64 |   0.30 |            2.05 |  3.74 |   583,470 |   291,732 |     56 |     28.00 |       28.00 | NEGMIR     | ever_black               | ever         |         4,786 | black       |           646 |
| **NEGmir~that_popular**             |     65 |    0.48 |   0.98 |    1.54 |     81.14 |   0.29 |            1.64 |  3.97 |   583,470 |   291,732 |     66 |     33.00 |       32.00 | NEGMIR     | that_popular             | that         |         4,559 | popular     |         2,841 |
| **NEGmir~particularly_novel**       |     54 |    0.50 |   1.00 |    1.50 |     74.87 |   0.30 |            2.04 |  3.67 |   583,470 |   291,732 |     54 |     27.00 |       27.00 | NEGMIR     | particularly_novel       | particularly |        10,029 | novel       |           179 |
| **NEGany~remotely_ready**           |     58 |    0.50 |   1.00 |    1.49 |     80.41 |   0.30 |            2.07 |  3.81 | 6,347,364 | 3,173,660 |     58 |     29.00 |       29.00 | NEGATED    | remotely_ready           | remotely     |         6,161 | ready       |        29,583 |
| **NEGany~any_sweeter**              |     58 |    0.50 |   1.00 |    1.49 |     80.41 |   0.30 |            2.07 |  3.81 | 6,347,364 | 3,173,660 |     58 |     29.00 |       29.00 | NEGATED    | any_sweeter              | any          |        16,238 | sweeter     |           388 |
| **NEGmir~particularly_religious**   |     53 |    0.50 |   1.00 |    1.47 |     73.48 |   0.30 |            2.03 |  3.64 |   583,470 |   291,732 |     53 |     26.50 |       26.50 | NEGMIR     | particularly_religious   | particularly |        10,029 | religious   |           337 |
| **NEGany~inherently_better**        |    144 |    0.41 |   0.91 |    1.46 |    124.46 |   0.26 |            1.00 |  5.42 | 6,347,364 | 3,173,660 |    158 |     79.00 |       65.00 | NEGATED    | inherently_better        | inherently   |         8,614 | better      |        50,827 |
| **NEGany~particularly_flashy**      |     57 |    0.50 |   1.00 |    1.46 |     79.02 |   0.30 |            2.06 |  3.77 | 6,347,364 | 3,173,660 |     57 |     28.50 |       28.50 | NEGATED    | particularly_flashy      | particularly |        76,162 | flashy      |         1,732 |
| **NEGany~inherently_good**          |    283 |    0.36 |   0.86 |    1.46 |    189.85 |   0.24 |            0.79 |  7.04 | 6,347,364 | 3,173,660 |    329 |    164.50 |      118.50 | NEGATED    | inherently_good          | inherently   |         8,614 | good        |       201,244 |
| **NEGmir~remotely_true**            |     61 |    0.48 |   0.98 |    1.43 |     75.72 |   0.29 |            1.61 |  3.84 |   583,470 |   291,732 |     62 |     31.00 |       30.00 | NEGMIR     | remotely_true            | remotely     |         1,953 | true        |         2,850 |
| **NEGany~remotely_similar**         |    152 |    0.40 |   0.90 |    1.39 |    123.97 |   0.25 |            0.94 |  5.48 | 6,347,364 | 3,173,660 |    169 |     84.50 |       67.50 | NEGATED    | remotely_similar         | remotely     |         6,161 | similar     |        11,088 |
| **NEGany~any_brighter**             |     63 |    0.48 |   0.98 |    1.37 |     78.42 |   0.29 |            1.63 |  3.91 | 6,347,364 | 3,173,660 |     64 |     32.00 |       31.00 | NEGATED    | any_brighter             | any          |        16,238 | brighter    |           640 |
| **NEGmir~necessarily_bad**          |     50 |    0.50 |   1.00 |    1.37 |     69.32 |   0.30 |            2.00 |  3.54 |   583,470 |   291,732 |     50 |     25.00 |       25.00 | NEGMIR     | necessarily_bad          | necessarily  |           992 | bad         |         4,790 |
| **NEGmir~immediately_available**    |    162 |    0.38 |   0.88 |    1.34 |    120.41 |   0.25 |            0.86 |  5.50 |   583,470 |   291,732 |    184 |     92.00 |       70.00 | NEGMIR     | immediately_available    | immediately  |           564 | available   |         3,079 |
| **NEGmir~ever_right**               |     49 |    0.50 |   1.00 |    1.33 |     67.93 |   0.30 |            2.00 |  3.50 |   583,470 |   291,732 |     49 |     24.50 |       24.50 | NEGMIR     | ever_right               | ever         |         4,786 | right       |         2,038 |
| **NEGany~remotely_related**         |    146 |    0.40 |   0.90 |    1.33 |    116.95 |   0.25 |            0.92 |  5.34 | 6,347,364 | 3,173,660 |    163 |     81.50 |       64.50 | NEGATED    | remotely_related         | remotely     |         6,161 | related     |        14,260 |
| **COM~ever_deeper**                 |     61 |    0.48 |   0.98 |    1.31 |     75.72 |   0.29 |            1.61 |  3.84 | 6,347,364 | 3,173,552 |     62 |     31.00 |       30.00 | COMPLEMENT | ever_deeper              | ever         |        10,870 | deeper      |         1,768 |
| **NEGmir~any_different**            |     48 |    0.50 |   1.00 |    1.30 |     66.55 |   0.30 |            1.99 |  3.46 |   583,470 |   291,732 |     48 |     24.00 |       24.00 | NEGMIR     | any_different            | any          |         1,095 | different   |         8,644 |
| **NEGmir~terribly_interesting**     |     56 |    0.48 |   0.98 |    1.29 |     68.96 |   0.29 |            1.58 |  3.67 |   583,470 |   291,732 |     57 |     28.50 |       27.50 | NEGMIR     | terribly_interesting     | terribly     |         2,204 | interesting |         3,863 |
| **NEGmir~particularly_innovative**  |     47 |    0.50 |   1.00 |    1.26 |     65.16 |   0.30 |            1.98 |  3.43 |   583,470 |   291,732 |     47 |     23.50 |       23.50 | NEGMIR     | particularly_innovative  | particularly |        10,029 | innovative  |           675 |
| **NEGmir~that_interested**          |     62 |    0.47 |   0.97 |    1.26 |     70.93 |   0.29 |            1.40 |  3.81 |   583,470 |   291,732 |     64 |     32.00 |       30.00 | NEGMIR     | that_interested          | that         |         4,559 | interested  |         2,877 |
| **NEGany~inherently_illegal**       |     59 |    0.48 |   0.98 |    1.26 |     73.01 |   0.29 |            1.60 |  3.78 | 6,347,364 | 3,173,660 |     60 |     30.00 |       29.00 | NEGATED    | inherently_illegal       | inherently   |         8,614 | illegal     |         3,580 |
| **NEGmir~any_easier**               |     61 |    0.47 |   0.97 |    1.23 |     69.61 |   0.29 |            1.39 |  3.78 |   583,470 |   291,732 |     63 |     31.50 |       29.50 | NEGMIR     | any_easier               | any          |         1,095 | easier      |           681 |
| **NEGmir~terribly_original**        |     45 |    0.50 |   1.00 |    1.19 |     62.39 |   0.30 |            1.96 |  3.35 |   583,470 |   291,732 |     45 |     22.50 |       22.50 | NEGMIR     | terribly_original        | terribly     |         2,204 | original    |           715 |
| **NEGmir~that_difficult**           |     52 |    0.48 |   0.98 |    1.16 |     63.56 |   0.29 |            1.54 |  3.54 |   583,470 |   291,732 |     53 |     26.50 |       25.50 | NEGMIR     | that_difficult           | that         |         4,559 | difficult   |         4,854 |
| **NEGmir~exactly_clear**            |     52 |    0.48 |   0.98 |    1.16 |     63.56 |   0.29 |            1.54 |  3.54 |   583,470 |   291,732 |     53 |     26.50 |       25.50 | NEGMIR     | exactly_clear            | exactly      |           869 | clear       |         3,321 |
| **NEGmir~particularly_comfortable** |     44 |    0.50 |   1.00 |    1.15 |     61.00 |   0.30 |            1.95 |  3.32 |   583,470 |   291,732 |     44 |     22.00 |       22.00 | NEGMIR     | particularly_comfortable | particularly |        10,029 | comfortable |         1,888 |
| **NEGmir~remotely_comparable**      |     44 |    0.50 |   1.00 |    1.15 |     61.00 |   0.30 |            1.95 |  3.32 |   583,470 |   291,732 |     44 |     22.00 |       22.00 | NEGMIR     | remotely_comparable      | remotely     |         1,953 | comparable  |           158 |
| **NEGany~remotely_enough**          |     47 |    0.50 |   1.00 |    1.13 |     65.16 |   0.30 |            1.98 |  3.43 | 6,347,364 | 3,173,660 |     47 |     23.50 |       23.50 | NEGATED    | remotely_enough          | remotely     |         6,161 | enough      |        27,603 |
| **POS~terribly_wrong**              |    319 |    0.30 |   0.80 |    1.06 |    149.75 |   0.20 |            0.59 |  6.63 |   583,470 |   291,729 |    401 |    200.50 |      118.50 | POSMIR     | terribly_wrong           | terribly     |         2,204 | wrong       |         8,506 |
| **COM~ever_mindful**                |     52 |    0.48 |   0.98 |    1.04 |     63.56 |   0.29 |            1.54 |  3.54 | 6,347,364 | 3,173,552 |     53 |     26.50 |       25.50 | COMPLEMENT | ever_mindful             | ever         |        10,870 | mindful     |           784 |
| **NEGmir~that_happy**               |     41 |    0.50 |   1.00 |    1.03 |     56.84 |   0.30 |            1.92 |  3.20 |   583,470 |   291,732 |     41 |     20.50 |       20.50 | NEGMIR     | that_happy               | that         |         4,559 | happy       |         5,463 |




```python
nb_show_table(NEG_bigrams_sample.l1.value_counts().to_frame('subtotal in selected bigrams'))
```

    
    |                |   `subtotal in selected bigrams` |
    |:---------------|---------------------------------:|
    | **NEGATED**    |                               99 |
    | **NEGMIR**     |                               48 |
    | **COMPLEMENT** |                                7 |
    | **POSMIR**     |                                1 |
    


|                |   `subtotal in selected bigrams` |
|:---------------|---------------------------------:|
| **NEGATED**    |                               99 |
| **NEGMIR**     |                               48 |
| **COMPLEMENT** |                                7 |
| **POSMIR**     |                                1 |


```python
nb_show_table(NEG_bigrams_sample.filter(like='O', axis=0).filter(FOCUS))
```

    
    |                            |   `f` |       `N` |      `f1` |   `f2` | `l1`       | `l2`               | `adv`        |   `adv_total` | `adj`   |   `adj_total` |
    |:---------------------------|------:|----------:|----------:|-------:|:-----------|:-------------------|:-------------|--------------:|:--------|--------------:|
    | **COM~ever_closer**        |   279 | 6,347,364 | 3,173,552 |    281 | COMPLEMENT | ever_closer        | ever         |        10,870 | closer  |         3,686 |
    | **COM~ever_greater**       |   186 | 6,347,364 | 3,173,552 |    187 | COMPLEMENT | ever_greater       | ever         |        10,870 | greater |         6,949 |
    | **COM~ever_larger**        |   139 | 6,347,364 | 3,173,552 |    139 | COMPLEMENT | ever_larger        | ever         |        10,870 | larger  |         7,453 |
    | **COM~particularly_acute** |   135 | 6,347,364 | 3,173,552 |    135 | COMPLEMENT | particularly_acute | particularly |        76,162 | acute   |         1,038 |
    | **COM~ever_higher**        |   129 | 6,347,364 | 3,173,552 |    130 | COMPLEMENT | ever_higher        | ever         |        10,870 | higher  |        12,992 |
    | **COM~ever_deeper**        |    61 | 6,347,364 | 3,173,552 |     62 | COMPLEMENT | ever_deeper        | ever         |        10,870 | deeper  |         1,768 |
    | **POS~terribly_wrong**     |   319 |   583,470 |   291,729 |    401 | POSMIR     | terribly_wrong     | terribly     |         2,204 | wrong   |         8,506 |
    | **COM~ever_mindful**       |    52 | 6,347,364 | 3,173,552 |     53 | COMPLEMENT | ever_mindful       | ever         |        10,870 | mindful |           784 |
    


COM associations of selected bigrams

|                            |   `f` |       `N` |      `f1` |   `f2` | `l1`       | `l2`               | `adv`        |   `adv_total` | `adj`   |   `adj_total` |
|:---------------------------|------:|----------:|----------:|-------:|:-----------|:-------------------|:-------------|--------------:|:--------|--------------:|
| **COM~ever_closer**        |   279 | 6,347,364 | 3,173,552 |    281 | COMPLEMENT | ever_closer        | ever         |        10,870 | closer  |         3,686 |
| **COM~ever_greater**       |   186 | 6,347,364 | 3,173,552 |    187 | COMPLEMENT | ever_greater       | ever         |        10,870 | greater |         6,949 |
| **COM~ever_larger**        |   139 | 6,347,364 | 3,173,552 |    139 | COMPLEMENT | ever_larger        | ever         |        10,870 | larger  |         7,453 |
| **COM~particularly_acute** |   135 | 6,347,364 | 3,173,552 |    135 | COMPLEMENT | particularly_acute | particularly |        76,162 | acute   |         1,038 |
| **COM~ever_higher**        |   129 | 6,347,364 | 3,173,552 |    130 | COMPLEMENT | ever_higher        | ever         |        10,870 | higher  |        12,992 |
| **COM~ever_deeper**        |    61 | 6,347,364 | 3,173,552 |     62 | COMPLEMENT | ever_deeper        | ever         |        10,870 | deeper  |         1,768 |
| **POS~terribly_wrong**     |   319 |   583,470 |   291,729 |    401 | POSMIR     | terribly_wrong     | terribly     |         2,204 | wrong   |         8,506 |
| **COM~ever_mindful**       |    52 | 6,347,364 | 3,173,552 |     53 | COMPLEMENT | ever_mindful       | ever         |        10,870 | mindful |           784 |


