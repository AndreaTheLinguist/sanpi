# `NEQ`: Collect bigrams corresponding to top adverbs


```python
from pathlib import Path
from pprint import pprint

import pandas as pd

from source.utils.associate import POLAR_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.dataframes import update_assoc_index as update_index
from source.utils.general import (confirm_dir, print_iter, snake_to_camel,
                                  timestamp_today)
from am_notebooks import *

ADV_FLOOR = 5000
K = 8

DATA_DATE = '2024-07-28'
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
pd.set_option('display.max_colwidth', 30)
pd.set_option('display.max_columns', 9)
pd.set_option('display.width', 120)
pd.set_option("display.precision", 2)
pd.set_option("styler.format.precision", 2)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.2f}'.format)
```

(MOVED the following to `./am_notebooks.py`)

## Load data


```python
bigram_dfs = load_bigram_dfs(locate_bigram_am_paths(TAG, mirror_floor, bigram_floor))

try:
    combined_am_csv = tuple(OUT_DIR.glob(
                   f'{TAG}-Top{K}_NEG-ADV_combined-{ADV_FLOOR}*.{DATA_DATE or timestamp_today()}.csv'))[0]
except IndexError:
    combined_am_csv = tuple(TOP_AM_TAG_DIR.rglob(
        f'{TAG}-Top{K}_NEG-ADV_combined*.csv'))[0]
print(f'Loaded from: "{combined_am_csv}"')

C = adjust_assoc_columns(pd.read_csv(combined_am_csv, index_col='adv'))

main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in ('LRC', 'P1', 'G2')],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2']])
                              ).to_list()
C
```

    {'RBdirect': PosixPath('/share/compling/projects/sanpi/results/assoc_df/polar/RBdirect/bigram/extra/polarized-bigram_NEQ-direct_min25x_extra.parq'),
     'mirror': PosixPath('/share/compling/projects/sanpi/results/assoc_df/polar/mirror/bigram/extra/polarized-bigram_NEQ-mirror_min5x_extra.parq')}
    Loaded from: "/share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_combined-5000.2024-07-28.csv"





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
<p>11 rows × 47 columns</p>
</div>




```python
samples_dict, bigram_k = show_adv_bigrams(
    K, C, bigram_dfs,
    column_list=[
        *pd.Series(main_cols_ordered).str.replace(
            r'mean_|_SET|_MIR', '', regex=True)
        .drop_duplicates().to_list(),
        'adv_total', 'adj_total'
        # 't', 'MI'
    ]
)
```

    ## Top 10 "most negative" bigrams corresponding to top 8 adverbs
    
    2024-07-28
    
    ### 1. _necessarily_
    
    
    #### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                   |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~necessarily_indicative** |    6.29 |    0.50 |   1.00 | 1,925.89 | 1,389 | 3,173,660 |  1,389 |        42,886 |         2,313 |
    | **NEGany~necessarily_easy**       |    5.67 |    0.50 |   1.00 | 1,260.28 |   909 | 3,173,660 |    909 |        42,886 |       108,923 |
    | **NEGany~necessarily_new**        |    4.74 |    0.50 |   1.00 |   668.24 |   482 | 3,173,660 |    482 |        42,886 |        21,538 |
    | **NEGany~necessarily_surprising** |    4.23 |    0.50 |   1.00 |   471.36 |   340 | 3,173,660 |    340 |        42,886 |        18,776 |
    | **NEGany~necessarily_enough**     |    3.93 |    0.50 |   1.00 |   386.79 |   279 | 3,173,660 |    279 |        42,886 |        27,603 |
    | **NEGany~necessarily_bad**        |    6.31 |    0.50 |   1.00 | 2,814.04 | 2,059 | 3,173,660 |  2,062 |        42,886 |       119,509 |
    | **NEGany~necessarily_true**       |    6.16 |    0.50 |   1.00 | 4,330.74 | 3,232 | 3,173,660 |  3,245 |        42,886 |        34,967 |
    | **NEGany~necessarily_better**     |    6.07 |    0.50 |   1.00 | 2,564.81 | 1,887 | 3,173,660 |  1,891 |        42,886 |        50,827 |
    | **NEGany~necessarily_aware**      |    3.48 |    0.50 |   1.00 |   285.59 |   206 | 3,173,660 |    206 |        42,886 |        28,973 |
    | **NEGany~necessarily_related**    |    5.14 |    0.50 |   1.00 | 1,013.51 |   741 | 3,173,660 |    742 |        42,886 |        14,260 |
    
    
    #### Top 2 `mirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                              |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~necessarily_bad**   |    1.37 |    0.50 |   1.00 |  69.32 |    50 | 291,732 |     50 |           992 |         4,790 |
    | **NEGmir~necessarily_wrong** |    3.05 |    0.49 |   0.99 | 265.18 |   211 | 291,732 |    214 |           992 |         8,506 |
    
    
    ### 2. _that_
    
    
    #### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                            |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~that_surprising** |    5.99 |    0.50 |   1.00 |  1,570.89 |  1,133 | 3,173,660 |  1,133 |       166,676 |        18,776 |
    | **NEGany~that_unusual**    |    5.77 |    0.50 |   1.00 |  1,354.57 |    977 | 3,173,660 |    977 |       166,676 |         7,412 |
    | **NEGany~that_exciting**   |    5.49 |    0.50 |   1.00 |  1,116.08 |    805 | 3,173,660 |    805 |       166,676 |        20,233 |
    | **NEGany~that_uncommon**   |    5.49 |    0.50 |   1.00 |  1,111.92 |    802 | 3,173,660 |    802 |       166,676 |         3,165 |
    | **NEGany~that_impressed**  |    5.25 |    0.50 |   1.00 |    944.15 |    681 | 3,173,660 |    681 |       166,676 |        12,138 |
    | **NEGany~that_hard**       |    7.68 |    0.50 |   1.00 | 13,602.42 |  9,948 | 3,173,660 |  9,963 |       166,676 |        45,061 |
    | **NEGany~that_different**  |    7.18 |    0.50 |   1.00 |  8,895.12 |  6,534 | 3,173,660 |  6,547 |       166,676 |        80,643 |
    | **NEGany~that_great**      |    7.18 |    0.50 |   1.00 | 14,908.90 | 11,032 | 3,173,660 | 11,065 |       166,676 |        45,359 |
    | **NEGany~that_difficult**  |    7.06 |    0.50 |   1.00 |  7,569.00 |  5,560 | 3,173,660 |  5,571 |       166,676 |        61,490 |
    | **NEGany~that_big**        |    6.47 |    0.50 |   1.00 |  8,332.69 |  6,244 | 3,173,660 |  6,273 |       166,676 |        42,912 |
    
    
    #### Top 10 `mirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                            |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~that_close**      |    1.67 |    0.50 |   1.00 |  83.19 |    60 | 291,732 |     60 |         4,559 |         4,831 |
    | **NEGmir~that_happy**      |    1.03 |    0.50 |   1.00 |  56.84 |    41 | 291,732 |     41 |         4,559 |         5,463 |
    | **NEGmir~that_popular**    |    1.54 |    0.48 |   0.98 |  81.14 |    65 | 291,732 |     66 |         4,559 |         2,841 |
    | **NEGmir~that_simple**     |    3.67 |    0.48 |   0.98 | 580.44 |   474 | 291,732 |    483 |         4,559 |         7,465 |
    | **NEGmir~that_difficult**  |    1.16 |    0.48 |   0.98 |  63.56 |    52 | 291,732 |     53 |         4,559 |         4,854 |
    | **NEGmir~that_easy**       |    3.23 |    0.47 |   0.97 | 512.43 |   450 | 291,732 |    465 |         4,559 |         7,749 |
    | **NEGmir~that_great**      |    2.71 |    0.46 |   0.96 | 312.65 |   286 | 291,732 |    298 |         4,559 |         2,123 |
    | **NEGmir~that_good**       |    2.65 |    0.44 |   0.94 | 441.70 |   447 | 291,732 |    476 |         4,559 |        13,423 |
    | **NEGmir~that_big**        |    2.08 |    0.47 |   0.97 | 132.98 |   113 | 291,732 |    116 |         4,559 |         3,134 |
    | **NEGmir~that_interested** |    1.26 |    0.47 |   0.97 |  70.93 |    62 | 291,732 |     64 |         4,559 |         2,877 |
    
    
    ### 3. _exactly_
    
    
    #### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                               |   `LRC` |   `dP1` |   `P1` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------|--------:|--------:|-------:|----------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~exactly_cheap**      |    5.27 |    0.50 |   1.00 |    958.01 |   691 | 3,173,660 |    691 |        44,503 |         6,591 |
    | **NEGany~exactly_surprising** |    4.61 |    0.50 |   1.00 |    610.01 |   440 | 3,173,660 |    440 |        44,503 |        18,776 |
    | **NEGany~exactly_subtle**     |    3.84 |    0.50 |   1.00 |    364.61 |   263 | 3,173,660 |    263 |        44,503 |         5,299 |
    | **NEGany~exactly_fair**       |    3.83 |    0.50 |   1.00 |    360.45 |   260 | 3,173,660 |    260 |        44,503 |         6,964 |
    | **NEGany~exactly_fun**        |    3.60 |    0.50 |   1.00 |    310.54 |   224 | 3,173,660 |    224 |        44,503 |        19,661 |
    | **NEGany~exactly_sure**       |    7.46 |    0.50 |   1.00 | 11,991.61 | 8,794 | 3,173,660 |  8,810 |        44,503 |       134,139 |
    | **NEGany~exactly_clear**      |    6.38 |    0.50 |   1.00 |  2,405.43 | 1,746 | 3,173,660 |  1,747 |        44,503 |        84,227 |
    | **NEGany~exactly_new**        |    6.03 |    0.50 |   1.00 |  1,885.86 | 1,371 | 3,173,660 |  1,372 |        44,503 |        21,538 |
    | **NEGany~exactly_easy**       |    5.67 |    0.50 |   1.00 |  1,463.43 | 1,066 | 3,173,660 |  1,067 |        44,503 |       108,923 |
    | **NEGany~exactly_hard**       |    3.46 |    0.50 |   1.00 |    281.43 |   203 | 3,173,660 |    203 |        44,503 |        45,061 |
    
    
    #### Top 2 `mirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~exactly_sure**  |    3.10 |    0.50 |   1.00 | 205.21 |   148 | 291,732 |    148 |           869 |         5,978 |
    | **NEGmir~exactly_clear** |    1.16 |    0.48 |   0.98 |  63.56 |    52 | 291,732 |     53 |           869 |         3,321 |
    
    
    ### 4. _any_
    
    
    #### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~any_younger**   |    3.80 |    0.50 |   1.00 |   353.52 |   255 | 3,173,660 |    255 |        16,238 |         1,784 |
    | **NEGany~any_nicer**     |    2.30 |    0.50 |   1.00 |   133.09 |    96 | 3,173,660 |     96 |        16,238 |           642 |
    | **NEGany~any_sweeter**   |    1.49 |    0.50 |   1.00 |    80.41 |    58 | 3,173,660 |     58 |        16,238 |           388 |
    | **NEGany~any_happier**   |    4.66 |    0.49 |   0.99 | 1,085.12 |   828 | 3,173,660 |    834 |        16,238 |         2,004 |
    | **NEGany~any_smarter**   |    1.94 |    0.49 |   0.99 |   113.78 |    89 | 3,173,660 |     90 |        16,238 |           733 |
    | **NEGany~any_easier**    |    4.42 |    0.48 |   0.98 | 1,946.26 | 1,594 | 3,173,660 |  1,625 |        16,238 |        12,877 |
    | **NEGany~any_worse**     |    3.62 |    0.46 |   0.96 | 1,816.60 | 1,686 | 3,173,660 |  1,762 |        16,238 |        12,116 |
    | **NEGany~any_better**    |    3.59 |    0.44 |   0.94 | 4,753.39 | 4,719 | 3,173,660 |  5,004 |        16,238 |        50,827 |
    | **NEGany~any_brighter**  |    1.37 |    0.48 |   0.98 |    78.42 |    63 | 3,173,660 |     64 |        16,238 |           640 |
    | **NEGany~any_different** |    3.03 |    0.44 |   0.94 |   905.82 |   902 | 3,173,660 |    957 |        16,238 |        80,643 |
    
    
    #### Top 4 `mirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~any_different** |    1.30 |    0.50 |   1.00 |  66.55 |    48 | 291,732 |     48 |         1,095 |         8,644 |
    | **NEGmir~any_better**    |    3.27 |    0.47 |   0.97 | 447.88 |   380 | 291,732 |    390 |         1,095 |         3,831 |
    | **NEGmir~any_easier**    |    1.23 |    0.47 |   0.97 |  69.61 |    61 | 291,732 |     63 |         1,095 |           681 |
    | **NEGmir~any_worse**     |    1.66 |    0.47 |   0.97 |  98.47 |    87 | 291,732 |     90 |         1,095 |         2,007 |
    
    
    ### 5. _remotely_
    
    
    #### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|-------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~remotely_ready**      |    1.49 |    0.50 |   1.00 |  80.41 |    58 | 3,173,660 |     58 |         6,161 |        29,583 |
    | **NEGany~remotely_enough**     |    1.13 |    0.50 |   1.00 |  65.16 |    47 | 3,173,660 |     47 |         6,161 |        27,603 |
    | **NEGany~remotely_true**       |    3.53 |    0.50 |   1.00 | 334.93 |   250 | 3,173,660 |    251 |         6,161 |        34,967 |
    | **NEGany~remotely_surprising** |    1.66 |    0.49 |   0.99 |  94.71 |    75 | 3,173,660 |     76 |         6,161 |        18,776 |
    | **NEGany~remotely_funny**      |    2.16 |    0.47 |   0.97 | 159.09 |   137 | 3,173,660 |    141 |         6,161 |        14,992 |
    | **NEGany~remotely_close**      |    2.98 |    0.45 |   0.95 | 711.52 |   694 | 3,173,660 |    733 |         6,161 |        46,485 |
    | **NEGany~remotely_interested** |    1.99 |    0.41 |   0.91 | 278.69 |   330 | 3,173,660 |    364 |         6,161 |        34,543 |
    | **NEGany~remotely_comparable** |    1.62 |    0.44 |   0.94 | 119.34 |   118 | 3,173,660 |    125 |         6,161 |         2,401 |
    | **NEGany~remotely_similar**    |    1.39 |    0.40 |   0.90 | 123.97 |   152 | 3,173,660 |    169 |         6,161 |        11,088 |
    | **NEGany~remotely_related**    |    1.33 |    0.40 |   0.90 | 116.95 |   146 | 3,173,660 |    163 |         6,161 |        14,260 |
    
    
    #### Top 3 `mirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~remotely_comparable** |    1.15 |    0.50 |   1.00 |  61.00 |    44 | 291,732 |     44 |         1,953 |           158 |
    | **NEGmir~remotely_true**       |    1.43 |    0.48 |   0.98 |  75.72 |    61 | 291,732 |     62 |         1,953 |         2,850 |
    | **NEGmir~remotely_close**      |    2.58 |    0.46 |   0.96 | 244.21 |   218 | 291,732 |    226 |         1,953 |         4,831 |
    
    
    ### 6. _yet_
    
    
    #### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                          |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~yet_clear**     |    8.66 |    0.50 |   1.00 | 14,392.25 | 10,406 | 3,173,660 | 10,409 |        53,881 |        84,227 |
    | **NEGany~yet_certain**   |    5.60 |    0.50 |   1.00 |  1,200.66 |    866 | 3,173,660 |    866 |        53,881 |        11,334 |
    | **NEGany~yet_ready**     |    8.06 |    0.50 |   1.00 | 10,344.81 |  7,501 | 3,173,660 |  7,505 |        53,881 |        29,583 |
    | **NEGany~yet_final**     |    5.16 |    0.50 |   1.00 |    887.30 |    640 | 3,173,660 |    640 |        53,881 |         1,213 |
    | **NEGany~yet_public**    |    4.69 |    0.50 |   1.00 |    647.44 |    467 | 3,173,660 |    467 |        53,881 |         2,656 |
    | **NEGany~yet_complete**  |    6.70 |    0.50 |   1.00 |  2,998.60 |  2,174 | 3,173,660 |  2,175 |        53,881 |         8,415 |
    | **NEGany~yet_available** |    6.66 |    0.50 |   1.00 |  9,950.03 |  7,430 | 3,173,660 |  7,461 |        53,881 |        82,956 |
    | **NEGany~yet_sure**      |    6.13 |    0.50 |   1.00 |  2,689.26 |  1,977 | 3,173,660 |  1,981 |        53,881 |       134,139 |
    | **NEGany~yet_dead**      |    4.47 |    0.50 |   1.00 |    555.93 |    401 | 3,173,660 |    401 |        53,881 |         6,348 |
    | **NEGany~yet_able**      |    5.44 |    0.50 |   1.00 |  1,764.46 |  1,315 | 3,173,660 |  1,320 |        53,881 |        23,355 |
    
    No bigrams found in loaded `mirror` AM table.
    
    ### 7. _immediately_
    
    
    #### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                   |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~immediately_sure**       |    2.87 |    0.50 |   1.00 |    191.31 |    138 | 3,173,660 |    138 |        58,040 |       134,139 |
    | **NEGany~immediately_reachable**  |    2.50 |    0.50 |   1.00 |    151.11 |    109 | 3,173,660 |    109 |        58,040 |           350 |
    | **NEGany~immediately_certain**    |    1.80 |    0.50 |   1.00 |     97.04 |     70 | 3,173,660 |     70 |        58,040 |        11,334 |
    | **NEGany~immediately_clear**      |    7.55 |    0.50 |   1.00 | 33,058.44 | 24,416 | 3,173,660 | 24,488 |        58,040 |        84,227 |
    | **NEGany~immediately_possible**   |    5.40 |    0.50 |   1.00 |  1,360.38 |  1,000 | 3,173,660 |  1,002 |        58,040 |        30,446 |
    | **NEGany~immediately_available**  |    5.34 |    0.48 |   0.98 | 25,870.14 | 21,078 | 3,173,660 | 21,477 |        58,040 |        82,956 |
    | **NEGany~immediately_obvious**    |    3.88 |    0.46 |   0.96 |  2,481.50 |  2,238 | 3,173,660 |  2,325 |        58,040 |        22,651 |
    | **NEGany~immediately_able**       |    3.66 |    0.48 |   0.98 |    746.39 |    626 | 3,173,660 |    641 |        58,040 |        23,355 |
    | **NEGany~immediately_successful** |    2.87 |    0.47 |   0.97 |    333.73 |    290 | 3,173,660 |    299 |        58,040 |        31,460 |
    | **NEGany~immediately_apparent**   |    3.30 |    0.44 |   0.94 |  2,001.83 |  2,015 | 3,173,660 |  2,143 |        58,040 |         9,798 |
    
    
    #### Top 1 `mirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                  |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:---------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~immediately_available** |    1.34 |    0.38 |   0.88 | 120.41 |   162 | 291,732 |    184 |           564 |         3,079 |
    
    
    ### 8. _particularly_
    
    
    #### Top 10 `RBdirect` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                    |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **COM~particularly_acute**         |    2.84 |    0.50 |   1.00 |   187.16 |   135 | 3,173,552 |    135 |        76,162 |         1,038 |
    | **NEGany~particularly_wrong**      |    3.56 |    0.50 |   1.00 |   302.22 |   218 | 3,173,660 |    218 |        76,162 |        21,332 |
    | **NEGany~particularly_athletic**   |    2.49 |    0.50 |   1.00 |   149.72 |   108 | 3,173,660 |    108 |        76,162 |         1,772 |
    | **NEGany~particularly_likeable**   |    2.46 |    0.50 |   1.00 |   146.95 |   106 | 3,173,660 |    106 |        76,162 |           861 |
    | **NEGany~particularly_radical**    |    1.99 |    0.50 |   1.00 |   109.52 |    79 | 3,173,660 |     79 |        76,162 |         2,637 |
    | **NEGany~particularly_new**        |    4.61 |    0.49 |   0.99 |   982.49 |   747 | 3,173,660 |    752 |        76,162 |        21,538 |
    | **NEGany~particularly_religious**  |    4.52 |    0.50 |   1.00 |   659.41 |   485 | 3,173,660 |    486 |        76,162 |         3,507 |
    | **NEGany~particularly_surprising** |    3.93 |    0.47 |   0.97 | 1,260.26 | 1,069 | 3,173,660 |  1,097 |        76,162 |        18,776 |
    | **NEGany~particularly_original**   |    3.64 |    0.49 |   0.99 |   460.59 |   360 | 3,173,660 |    364 |        76,162 |         4,693 |
    | **NEGany~particularly_flashy**     |    1.46 |    0.50 |   1.00 |    79.02 |    57 | 3,173,660 |     57 |        76,162 |         1,732 |
    
    
    #### Top 10 `mirror` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                     |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~particularly_surprising**  |    3.27 |    0.50 |   1.00 | 230.18 |   166 | 291,732 |    166 |        10,029 |         1,248 |
    | **NEGmir~particularly_original**    |    2.33 |    0.50 |   1.00 | 124.78 |    90 | 291,732 |     90 |        10,029 |           715 |
    | **NEGmir~particularly_novel**       |    1.50 |    0.50 |   1.00 |  74.87 |    54 | 291,732 |     54 |        10,029 |           179 |
    | **NEGmir~particularly_religious**   |    1.47 |    0.50 |   1.00 |  73.48 |    53 | 291,732 |     53 |        10,029 |           337 |
    | **NEGmir~particularly_innovative**  |    1.26 |    0.50 |   1.00 |  65.16 |    47 | 291,732 |     47 |        10,029 |           675 |
    | **NEGmir~particularly_new**         |    4.35 |    0.50 |   1.00 | 547.73 |   404 | 291,732 |    405 |        10,029 |         4,300 |
    | **NEGmir~particularly_wrong**       |    3.39 |    0.50 |   1.00 | 282.64 |   212 | 291,732 |    213 |        10,029 |         8,506 |
    | **NEGmir~particularly_good**        |    3.24 |    0.47 |   0.97 | 455.35 |   390 | 291,732 |    401 |        10,029 |        13,423 |
    | **NEGmir~particularly_unusual**     |    2.72 |    0.48 |   0.98 | 209.60 |   170 | 291,732 |    173 |        10,029 |           933 |
    | **NEGmir~particularly_comfortable** |    1.15 |    0.50 |   1.00 |  61.00 |    44 | 291,732 |     44 |        10,029 |         1,888 |
    
    
    ### 9. _inherently_
    
    
    #### Top 6 `RBdirect` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                               |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~inherently_illegal** |    1.26 |    0.48 |   0.98 |    73.01 |    59 | 3,173,660 |     60 |         8,614 |         3,580 |
    | **NEGany~inherently_bad**     |    3.87 |    0.48 |   0.98 |   953.05 |   794 | 3,173,660 |    812 |         8,614 |       119,509 |
    | **NEGany~inherently_wrong**   |    4.25 |    0.48 |   0.98 | 1,956.12 | 1,639 | 3,173,660 |  1,678 |         8,614 |        21,332 |
    | **NEGany~inherently_evil**    |    2.12 |    0.41 |   0.91 |   312.23 |   358 | 3,173,660 |    392 |         8,614 |         3,171 |
    | **NEGany~inherently_better**  |    1.46 |    0.41 |   0.91 |   124.46 |   144 | 3,173,660 |    158 |         8,614 |        50,827 |
    | **NEGany~inherently_good**    |    1.46 |    0.36 |   0.86 |   189.85 |   283 | 3,173,660 |    329 |         8,614 |       201,244 |
    
    
    #### Top 2 `mirror` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                             |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:----------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~inherently_wrong** |    3.78 |    0.46 |   0.96 | 1,685.02 | 1,513 | 291,732 |  1,571 |         3,342 |         8,506 |
    | **NEGmir~inherently_bad**   |    1.83 |    0.44 |   0.94 |   144.52 |   148 | 291,732 |    158 |         3,342 |         4,790 |
    
    
    ### 10. _terribly_
    
    
    #### Top 10 `RBdirect` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
    | **NEGany~terribly_surprising**  |    5.73 |    0.50 |   1.00 | 1,315.75 |   949 | 3,173,660 |    949 |        19,802 |        18,776 |
    | **NEGany~terribly_popular**     |    2.99 |    0.50 |   1.00 |   206.56 |   149 | 3,173,660 |    149 |        19,802 |        51,120 |
    | **NEGany~terribly_unusual**     |    2.96 |    0.50 |   1.00 |   202.40 |   146 | 3,173,660 |    146 |        19,802 |         7,412 |
    | **NEGany~terribly_comfortable** |    2.77 |    0.50 |   1.00 |   178.84 |   129 | 3,173,660 |    129 |        19,802 |        23,908 |
    | **NEGany~terribly_bright**      |    2.61 |    0.50 |   1.00 |   162.20 |   117 | 3,173,660 |    117 |        19,802 |         8,623 |
    | **NEGany~terribly_interested**  |    3.98 |    0.49 |   0.99 |   624.89 |   486 | 3,173,660 |    491 |        19,802 |        34,543 |
    | **NEGany~terribly_different**   |    3.93 |    0.49 |   0.99 |   485.33 |   366 | 3,173,660 |    368 |        19,802 |        80,643 |
    | **NEGany~terribly_surprised**   |    3.30 |    0.49 |   0.99 |   361.19 |   287 | 3,173,660 |    291 |        19,802 |        10,157 |
    | **NEGany~terribly_exciting**    |    3.28 |    0.48 |   0.98 |   456.39 |   382 | 3,173,660 |    391 |        19,802 |        20,233 |
    | **NEGany~terribly_common**      |    2.45 |    0.50 |   1.00 |   145.56 |   105 | 3,173,660 |    105 |        19,802 |        34,450 |
    
    
    #### Top 5 `mirror` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                                 |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:--------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~terribly_surprising**  |    1.85 |    0.50 |   1.00 |  92.89 |    67 | 291,732 |     67 |         2,204 |         1,248 |
    | **NEGmir~terribly_original**    |    1.19 |    0.50 |   1.00 |  62.39 |    45 | 291,732 |     45 |         2,204 |           715 |
    | **NEGmir~terribly_new**         |    1.64 |    0.49 |   0.99 |  86.57 |    69 | 291,732 |     70 |         2,204 |         4,300 |
    | **NEGmir~terribly_interesting** |    1.29 |    0.48 |   0.98 |  68.96 |    56 | 291,732 |     57 |         2,204 |         3,863 |
    | **POS~terribly_wrong**          |    1.06 |    0.30 |   0.80 | 149.75 |   319 | 291,729 |    401 |         2,204 |         8,506 |
    
    
    ### 11. _ever_
    
    
    #### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                        |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:-----------------------|--------:|--------:|-------:|-------:|------:|----------:|-------:|--------------:|--------------:|
    | **COM~ever_larger**    |    2.88 |    0.50 |   1.00 | 192.71 |   139 | 3,173,552 |    139 |        10,870 |         7,453 |
    | **NEGany~ever_boring** |    1.84 |    0.50 |   1.00 |  99.82 |    72 | 3,173,660 |     72 |        10,870 |         3,840 |
    | **NEGany~ever_simple** |    3.28 |    0.50 |   1.00 | 281.20 |   211 | 3,173,660 |    212 |        10,870 |        46,867 |
    | **COM~ever_greater**   |    3.09 |    0.49 |   0.99 | 246.80 |   186 | 3,173,552 |    187 |        10,870 |         6,949 |
    | **COM~ever_closer**    |    3.52 |    0.49 |   0.99 | 365.82 |   279 | 3,173,552 |    281 |        10,870 |         3,686 |
    | **NEGany~ever_easy**   |    3.53 |    0.48 |   0.98 | 525.98 |   429 | 3,173,660 |    437 |        10,870 |       108,923 |
    | **COM~ever_deeper**    |    1.31 |    0.48 |   0.98 |  75.72 |    61 | 3,173,552 |     62 |        10,870 |         1,768 |
    | **COM~ever_higher**    |    2.52 |    0.49 |   0.99 | 168.50 |   129 | 3,173,552 |    130 |        10,870 |        12,992 |
    | **NEGany~ever_good**   |    2.52 |    0.45 |   0.95 | 337.56 |   331 | 3,173,660 |    350 |        10,870 |       201,244 |
    | **COM~ever_mindful**   |    1.04 |    0.48 |   0.98 |  63.56 |    52 | 3,173,552 |     53 |        10,870 |           784 |
    
    
    #### Top 10 `mirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)
    
    
    |                         |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
    |:------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
    | **NEGmir~ever_perfect** |    3.60 |    0.50 |   1.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         1,303 |
    | **NEGmir~ever_simple**  |    3.60 |    0.50 |   1.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         7,465 |
    | **NEGmir~ever_enough**  |    3.09 |    0.50 |   1.00 | 203.83 |   147 | 291,732 |    147 |         4,786 |         1,326 |
    | **NEGmir~ever_certain** |    3.04 |    0.50 |   1.00 | 198.28 |   143 | 291,732 |    143 |         4,786 |         1,276 |
    | **NEGmir~ever_wrong**   |    2.52 |    0.50 |   1.00 | 141.42 |   102 | 291,732 |    102 |         4,786 |         8,506 |
    | **NEGmir~ever_easy**    |    4.21 |    0.50 |   1.00 | 497.96 |   368 | 291,732 |    369 |         4,786 |         7,749 |
    | **NEGmir~ever_good**    |    3.90 |    0.50 |   1.00 | 402.64 |   299 | 291,732 |    300 |         4,786 |        13,423 |
    | **NEGmir~ever_black**   |    1.56 |    0.50 |   1.00 |  77.64 |    56 | 291,732 |     56 |         4,786 |           646 |
    | **NEGmir~ever_able**    |    2.71 |    0.49 |   0.99 | 178.12 |   136 | 291,732 |    137 |         4,786 |         1,891 |
    | **NEGmir~ever_right**   |    1.33 |    0.50 |   1.00 |  67.93 |    49 | 291,732 |     49 |         4,786 |         2,038 |
    


## Top 10 "most negative" bigrams corresponding to top 8 adverbs

2024-07-28

### 1. _necessarily_


#### Top 10 `RBdirect` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                   |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~necessarily_indicative** |    6.29 |    0.50 |   1.00 | 1,925.89 | 1,389 | 3,173,660 |  1,389 |        42,886 |         2,313 |
| **NEGany~necessarily_easy**       |    5.67 |    0.50 |   1.00 | 1,260.28 |   909 | 3,173,660 |    909 |        42,886 |       108,923 |
| **NEGany~necessarily_new**        |    4.74 |    0.50 |   1.00 |   668.24 |   482 | 3,173,660 |    482 |        42,886 |        21,538 |
| **NEGany~necessarily_surprising** |    4.23 |    0.50 |   1.00 |   471.36 |   340 | 3,173,660 |    340 |        42,886 |        18,776 |
| **NEGany~necessarily_enough**     |    3.93 |    0.50 |   1.00 |   386.79 |   279 | 3,173,660 |    279 |        42,886 |        27,603 |
| **NEGany~necessarily_bad**        |    6.31 |    0.50 |   1.00 | 2,814.04 | 2,059 | 3,173,660 |  2,062 |        42,886 |       119,509 |
| **NEGany~necessarily_true**       |    6.16 |    0.50 |   1.00 | 4,330.74 | 3,232 | 3,173,660 |  3,245 |        42,886 |        34,967 |
| **NEGany~necessarily_better**     |    6.07 |    0.50 |   1.00 | 2,564.81 | 1,887 | 3,173,660 |  1,891 |        42,886 |        50,827 |
| **NEGany~necessarily_aware**      |    3.48 |    0.50 |   1.00 |   285.59 |   206 | 3,173,660 |    206 |        42,886 |        28,973 |
| **NEGany~necessarily_related**    |    5.14 |    0.50 |   1.00 | 1,013.51 |   741 | 3,173,660 |    742 |        42,886 |        14,260 |


#### Top 2 `mirror` "necessarily_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                              |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~necessarily_bad**   |    1.37 |    0.50 |   1.00 |  69.32 |    50 | 291,732 |     50 |           992 |         4,790 |
| **NEGmir~necessarily_wrong** |    3.05 |    0.49 |   0.99 | 265.18 |   211 | 291,732 |    214 |           992 |         8,506 |


### 2. _that_


#### Top 10 `RBdirect` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                            |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~that_surprising** |    5.99 |    0.50 |   1.00 |  1,570.89 |  1,133 | 3,173,660 |  1,133 |       166,676 |        18,776 |
| **NEGany~that_unusual**    |    5.77 |    0.50 |   1.00 |  1,354.57 |    977 | 3,173,660 |    977 |       166,676 |         7,412 |
| **NEGany~that_exciting**   |    5.49 |    0.50 |   1.00 |  1,116.08 |    805 | 3,173,660 |    805 |       166,676 |        20,233 |
| **NEGany~that_uncommon**   |    5.49 |    0.50 |   1.00 |  1,111.92 |    802 | 3,173,660 |    802 |       166,676 |         3,165 |
| **NEGany~that_impressed**  |    5.25 |    0.50 |   1.00 |    944.15 |    681 | 3,173,660 |    681 |       166,676 |        12,138 |
| **NEGany~that_hard**       |    7.68 |    0.50 |   1.00 | 13,602.42 |  9,948 | 3,173,660 |  9,963 |       166,676 |        45,061 |
| **NEGany~that_different**  |    7.18 |    0.50 |   1.00 |  8,895.12 |  6,534 | 3,173,660 |  6,547 |       166,676 |        80,643 |
| **NEGany~that_great**      |    7.18 |    0.50 |   1.00 | 14,908.90 | 11,032 | 3,173,660 | 11,065 |       166,676 |        45,359 |
| **NEGany~that_difficult**  |    7.06 |    0.50 |   1.00 |  7,569.00 |  5,560 | 3,173,660 |  5,571 |       166,676 |        61,490 |
| **NEGany~that_big**        |    6.47 |    0.50 |   1.00 |  8,332.69 |  6,244 | 3,173,660 |  6,273 |       166,676 |        42,912 |


#### Top 10 `mirror` "that_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                            |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~that_close**      |    1.67 |    0.50 |   1.00 |  83.19 |    60 | 291,732 |     60 |         4,559 |         4,831 |
| **NEGmir~that_happy**      |    1.03 |    0.50 |   1.00 |  56.84 |    41 | 291,732 |     41 |         4,559 |         5,463 |
| **NEGmir~that_popular**    |    1.54 |    0.48 |   0.98 |  81.14 |    65 | 291,732 |     66 |         4,559 |         2,841 |
| **NEGmir~that_simple**     |    3.67 |    0.48 |   0.98 | 580.44 |   474 | 291,732 |    483 |         4,559 |         7,465 |
| **NEGmir~that_difficult**  |    1.16 |    0.48 |   0.98 |  63.56 |    52 | 291,732 |     53 |         4,559 |         4,854 |
| **NEGmir~that_easy**       |    3.23 |    0.47 |   0.97 | 512.43 |   450 | 291,732 |    465 |         4,559 |         7,749 |
| **NEGmir~that_great**      |    2.71 |    0.46 |   0.96 | 312.65 |   286 | 291,732 |    298 |         4,559 |         2,123 |
| **NEGmir~that_good**       |    2.65 |    0.44 |   0.94 | 441.70 |   447 | 291,732 |    476 |         4,559 |        13,423 |
| **NEGmir~that_big**        |    2.08 |    0.47 |   0.97 | 132.98 |   113 | 291,732 |    116 |         4,559 |         3,134 |
| **NEGmir~that_interested** |    1.26 |    0.47 |   0.97 |  70.93 |    62 | 291,732 |     64 |         4,559 |         2,877 |


### 3. _exactly_


#### Top 10 `RBdirect` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                               |   `LRC` |   `dP1` |   `P1` |      `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------|--------:|--------:|-------:|----------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~exactly_cheap**      |    5.27 |    0.50 |   1.00 |    958.01 |   691 | 3,173,660 |    691 |        44,503 |         6,591 |
| **NEGany~exactly_surprising** |    4.61 |    0.50 |   1.00 |    610.01 |   440 | 3,173,660 |    440 |        44,503 |        18,776 |
| **NEGany~exactly_subtle**     |    3.84 |    0.50 |   1.00 |    364.61 |   263 | 3,173,660 |    263 |        44,503 |         5,299 |
| **NEGany~exactly_fair**       |    3.83 |    0.50 |   1.00 |    360.45 |   260 | 3,173,660 |    260 |        44,503 |         6,964 |
| **NEGany~exactly_fun**        |    3.60 |    0.50 |   1.00 |    310.54 |   224 | 3,173,660 |    224 |        44,503 |        19,661 |
| **NEGany~exactly_sure**       |    7.46 |    0.50 |   1.00 | 11,991.61 | 8,794 | 3,173,660 |  8,810 |        44,503 |       134,139 |
| **NEGany~exactly_clear**      |    6.38 |    0.50 |   1.00 |  2,405.43 | 1,746 | 3,173,660 |  1,747 |        44,503 |        84,227 |
| **NEGany~exactly_new**        |    6.03 |    0.50 |   1.00 |  1,885.86 | 1,371 | 3,173,660 |  1,372 |        44,503 |        21,538 |
| **NEGany~exactly_easy**       |    5.67 |    0.50 |   1.00 |  1,463.43 | 1,066 | 3,173,660 |  1,067 |        44,503 |       108,923 |
| **NEGany~exactly_hard**       |    3.46 |    0.50 |   1.00 |    281.43 |   203 | 3,173,660 |    203 |        44,503 |        45,061 |


#### Top 2 `mirror` "exactly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~exactly_sure**  |    3.10 |    0.50 |   1.00 | 205.21 |   148 | 291,732 |    148 |           869 |         5,978 |
| **NEGmir~exactly_clear** |    1.16 |    0.48 |   0.98 |  63.56 |    52 | 291,732 |     53 |           869 |         3,321 |


### 4. _any_


#### Top 10 `RBdirect` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~any_younger**   |    3.80 |    0.50 |   1.00 |   353.52 |   255 | 3,173,660 |    255 |        16,238 |         1,784 |
| **NEGany~any_nicer**     |    2.30 |    0.50 |   1.00 |   133.09 |    96 | 3,173,660 |     96 |        16,238 |           642 |
| **NEGany~any_sweeter**   |    1.49 |    0.50 |   1.00 |    80.41 |    58 | 3,173,660 |     58 |        16,238 |           388 |
| **NEGany~any_happier**   |    4.66 |    0.49 |   0.99 | 1,085.12 |   828 | 3,173,660 |    834 |        16,238 |         2,004 |
| **NEGany~any_smarter**   |    1.94 |    0.49 |   0.99 |   113.78 |    89 | 3,173,660 |     90 |        16,238 |           733 |
| **NEGany~any_easier**    |    4.42 |    0.48 |   0.98 | 1,946.26 | 1,594 | 3,173,660 |  1,625 |        16,238 |        12,877 |
| **NEGany~any_worse**     |    3.62 |    0.46 |   0.96 | 1,816.60 | 1,686 | 3,173,660 |  1,762 |        16,238 |        12,116 |
| **NEGany~any_better**    |    3.59 |    0.44 |   0.94 | 4,753.39 | 4,719 | 3,173,660 |  5,004 |        16,238 |        50,827 |
| **NEGany~any_brighter**  |    1.37 |    0.48 |   0.98 |    78.42 |    63 | 3,173,660 |     64 |        16,238 |           640 |
| **NEGany~any_different** |    3.03 |    0.44 |   0.94 |   905.82 |   902 | 3,173,660 |    957 |        16,238 |        80,643 |


#### Top 4 `mirror` "any_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~any_different** |    1.30 |    0.50 |   1.00 |  66.55 |    48 | 291,732 |     48 |         1,095 |         8,644 |
| **NEGmir~any_better**    |    3.27 |    0.47 |   0.97 | 447.88 |   380 | 291,732 |    390 |         1,095 |         3,831 |
| **NEGmir~any_easier**    |    1.23 |    0.47 |   0.97 |  69.61 |    61 | 291,732 |     63 |         1,095 |           681 |
| **NEGmir~any_worse**     |    1.66 |    0.47 |   0.97 |  98.47 |    87 | 291,732 |     90 |         1,095 |         2,007 |


### 5. _remotely_


#### Top 10 `RBdirect` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|-------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~remotely_ready**      |    1.49 |    0.50 |   1.00 |  80.41 |    58 | 3,173,660 |     58 |         6,161 |        29,583 |
| **NEGany~remotely_enough**     |    1.13 |    0.50 |   1.00 |  65.16 |    47 | 3,173,660 |     47 |         6,161 |        27,603 |
| **NEGany~remotely_true**       |    3.53 |    0.50 |   1.00 | 334.93 |   250 | 3,173,660 |    251 |         6,161 |        34,967 |
| **NEGany~remotely_surprising** |    1.66 |    0.49 |   0.99 |  94.71 |    75 | 3,173,660 |     76 |         6,161 |        18,776 |
| **NEGany~remotely_funny**      |    2.16 |    0.47 |   0.97 | 159.09 |   137 | 3,173,660 |    141 |         6,161 |        14,992 |
| **NEGany~remotely_close**      |    2.98 |    0.45 |   0.95 | 711.52 |   694 | 3,173,660 |    733 |         6,161 |        46,485 |
| **NEGany~remotely_interested** |    1.99 |    0.41 |   0.91 | 278.69 |   330 | 3,173,660 |    364 |         6,161 |        34,543 |
| **NEGany~remotely_comparable** |    1.62 |    0.44 |   0.94 | 119.34 |   118 | 3,173,660 |    125 |         6,161 |         2,401 |
| **NEGany~remotely_similar**    |    1.39 |    0.40 |   0.90 | 123.97 |   152 | 3,173,660 |    169 |         6,161 |        11,088 |
| **NEGany~remotely_related**    |    1.33 |    0.40 |   0.90 | 116.95 |   146 | 3,173,660 |    163 |         6,161 |        14,260 |


#### Top 3 `mirror` "remotely_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~remotely_comparable** |    1.15 |    0.50 |   1.00 |  61.00 |    44 | 291,732 |     44 |         1,953 |           158 |
| **NEGmir~remotely_true**       |    1.43 |    0.48 |   0.98 |  75.72 |    61 | 291,732 |     62 |         1,953 |         2,850 |
| **NEGmir~remotely_close**      |    2.58 |    0.46 |   0.96 | 244.21 |   218 | 291,732 |    226 |         1,953 |         4,831 |


### 6. _yet_


#### Top 10 `RBdirect` "yet_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                          |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~yet_clear**     |    8.66 |    0.50 |   1.00 | 14,392.25 | 10,406 | 3,173,660 | 10,409 |        53,881 |        84,227 |
| **NEGany~yet_certain**   |    5.60 |    0.50 |   1.00 |  1,200.66 |    866 | 3,173,660 |    866 |        53,881 |        11,334 |
| **NEGany~yet_ready**     |    8.06 |    0.50 |   1.00 | 10,344.81 |  7,501 | 3,173,660 |  7,505 |        53,881 |        29,583 |
| **NEGany~yet_final**     |    5.16 |    0.50 |   1.00 |    887.30 |    640 | 3,173,660 |    640 |        53,881 |         1,213 |
| **NEGany~yet_public**    |    4.69 |    0.50 |   1.00 |    647.44 |    467 | 3,173,660 |    467 |        53,881 |         2,656 |
| **NEGany~yet_complete**  |    6.70 |    0.50 |   1.00 |  2,998.60 |  2,174 | 3,173,660 |  2,175 |        53,881 |         8,415 |
| **NEGany~yet_available** |    6.66 |    0.50 |   1.00 |  9,950.03 |  7,430 | 3,173,660 |  7,461 |        53,881 |        82,956 |
| **NEGany~yet_sure**      |    6.13 |    0.50 |   1.00 |  2,689.26 |  1,977 | 3,173,660 |  1,981 |        53,881 |       134,139 |
| **NEGany~yet_dead**      |    4.47 |    0.50 |   1.00 |    555.93 |    401 | 3,173,660 |    401 |        53,881 |         6,348 |
| **NEGany~yet_able**      |    5.44 |    0.50 |   1.00 |  1,764.46 |  1,315 | 3,173,660 |  1,320 |        53,881 |        23,355 |

No bigrams found in loaded `mirror` AM table.

### 7. _immediately_


#### Top 10 `RBdirect` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                   |   `LRC` |   `dP1` |   `P1` |      `G2` |    `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------------|--------:|--------:|-------:|----------:|-------:|----------:|-------:|--------------:|--------------:|
| **NEGany~immediately_sure**       |    2.87 |    0.50 |   1.00 |    191.31 |    138 | 3,173,660 |    138 |        58,040 |       134,139 |
| **NEGany~immediately_reachable**  |    2.50 |    0.50 |   1.00 |    151.11 |    109 | 3,173,660 |    109 |        58,040 |           350 |
| **NEGany~immediately_certain**    |    1.80 |    0.50 |   1.00 |     97.04 |     70 | 3,173,660 |     70 |        58,040 |        11,334 |
| **NEGany~immediately_clear**      |    7.55 |    0.50 |   1.00 | 33,058.44 | 24,416 | 3,173,660 | 24,488 |        58,040 |        84,227 |
| **NEGany~immediately_possible**   |    5.40 |    0.50 |   1.00 |  1,360.38 |  1,000 | 3,173,660 |  1,002 |        58,040 |        30,446 |
| **NEGany~immediately_available**  |    5.34 |    0.48 |   0.98 | 25,870.14 | 21,078 | 3,173,660 | 21,477 |        58,040 |        82,956 |
| **NEGany~immediately_obvious**    |    3.88 |    0.46 |   0.96 |  2,481.50 |  2,238 | 3,173,660 |  2,325 |        58,040 |        22,651 |
| **NEGany~immediately_able**       |    3.66 |    0.48 |   0.98 |    746.39 |    626 | 3,173,660 |    641 |        58,040 |        23,355 |
| **NEGany~immediately_successful** |    2.87 |    0.47 |   0.97 |    333.73 |    290 | 3,173,660 |    299 |        58,040 |        31,460 |
| **NEGany~immediately_apparent**   |    3.30 |    0.44 |   0.94 |  2,001.83 |  2,015 | 3,173,660 |  2,143 |        58,040 |         9,798 |


#### Top 1 `mirror` "immediately_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                  |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:---------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~immediately_available** |    1.34 |    0.38 |   0.88 | 120.41 |   162 | 291,732 |    184 |           564 |         3,079 |


### 8. _particularly_


#### Top 10 `RBdirect` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                    |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **COM~particularly_acute**         |    2.84 |    0.50 |   1.00 |   187.16 |   135 | 3,173,552 |    135 |        76,162 |         1,038 |
| **NEGany~particularly_wrong**      |    3.56 |    0.50 |   1.00 |   302.22 |   218 | 3,173,660 |    218 |        76,162 |        21,332 |
| **NEGany~particularly_athletic**   |    2.49 |    0.50 |   1.00 |   149.72 |   108 | 3,173,660 |    108 |        76,162 |         1,772 |
| **NEGany~particularly_likeable**   |    2.46 |    0.50 |   1.00 |   146.95 |   106 | 3,173,660 |    106 |        76,162 |           861 |
| **NEGany~particularly_radical**    |    1.99 |    0.50 |   1.00 |   109.52 |    79 | 3,173,660 |     79 |        76,162 |         2,637 |
| **NEGany~particularly_new**        |    4.61 |    0.49 |   0.99 |   982.49 |   747 | 3,173,660 |    752 |        76,162 |        21,538 |
| **NEGany~particularly_religious**  |    4.52 |    0.50 |   1.00 |   659.41 |   485 | 3,173,660 |    486 |        76,162 |         3,507 |
| **NEGany~particularly_surprising** |    3.93 |    0.47 |   0.97 | 1,260.26 | 1,069 | 3,173,660 |  1,097 |        76,162 |        18,776 |
| **NEGany~particularly_original**   |    3.64 |    0.49 |   0.99 |   460.59 |   360 | 3,173,660 |    364 |        76,162 |         4,693 |
| **NEGany~particularly_flashy**     |    1.46 |    0.50 |   1.00 |    79.02 |    57 | 3,173,660 |     57 |        76,162 |         1,732 |


#### Top 10 `mirror` "particularly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                     |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~particularly_surprising**  |    3.27 |    0.50 |   1.00 | 230.18 |   166 | 291,732 |    166 |        10,029 |         1,248 |
| **NEGmir~particularly_original**    |    2.33 |    0.50 |   1.00 | 124.78 |    90 | 291,732 |     90 |        10,029 |           715 |
| **NEGmir~particularly_novel**       |    1.50 |    0.50 |   1.00 |  74.87 |    54 | 291,732 |     54 |        10,029 |           179 |
| **NEGmir~particularly_religious**   |    1.47 |    0.50 |   1.00 |  73.48 |    53 | 291,732 |     53 |        10,029 |           337 |
| **NEGmir~particularly_innovative**  |    1.26 |    0.50 |   1.00 |  65.16 |    47 | 291,732 |     47 |        10,029 |           675 |
| **NEGmir~particularly_new**         |    4.35 |    0.50 |   1.00 | 547.73 |   404 | 291,732 |    405 |        10,029 |         4,300 |
| **NEGmir~particularly_wrong**       |    3.39 |    0.50 |   1.00 | 282.64 |   212 | 291,732 |    213 |        10,029 |         8,506 |
| **NEGmir~particularly_good**        |    3.24 |    0.47 |   0.97 | 455.35 |   390 | 291,732 |    401 |        10,029 |        13,423 |
| **NEGmir~particularly_unusual**     |    2.72 |    0.48 |   0.98 | 209.60 |   170 | 291,732 |    173 |        10,029 |           933 |
| **NEGmir~particularly_comfortable** |    1.15 |    0.50 |   1.00 |  61.00 |    44 | 291,732 |     44 |        10,029 |         1,888 |


### 9. _inherently_


#### Top 6 `RBdirect` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                               |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~inherently_illegal** |    1.26 |    0.48 |   0.98 |    73.01 |    59 | 3,173,660 |     60 |         8,614 |         3,580 |
| **NEGany~inherently_bad**     |    3.87 |    0.48 |   0.98 |   953.05 |   794 | 3,173,660 |    812 |         8,614 |       119,509 |
| **NEGany~inherently_wrong**   |    4.25 |    0.48 |   0.98 | 1,956.12 | 1,639 | 3,173,660 |  1,678 |         8,614 |        21,332 |
| **NEGany~inherently_evil**    |    2.12 |    0.41 |   0.91 |   312.23 |   358 | 3,173,660 |    392 |         8,614 |         3,171 |
| **NEGany~inherently_better**  |    1.46 |    0.41 |   0.91 |   124.46 |   144 | 3,173,660 |    158 |         8,614 |        50,827 |
| **NEGany~inherently_good**    |    1.46 |    0.36 |   0.86 |   189.85 |   283 | 3,173,660 |    329 |         8,614 |       201,244 |


#### Top 2 `mirror` "inherently_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                             |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:----------------------------|--------:|--------:|-------:|---------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~inherently_wrong** |    3.78 |    0.46 |   0.96 | 1,685.02 | 1,513 | 291,732 |  1,571 |         3,342 |         8,506 |
| **NEGmir~inherently_bad**   |    1.83 |    0.44 |   0.94 |   144.52 |   148 | 291,732 |    158 |         3,342 |         4,790 |


### 10. _terribly_


#### Top 10 `RBdirect` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                 |   `LRC` |   `dP1` |   `P1` |     `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------|--------:|--------:|-------:|---------:|------:|----------:|-------:|--------------:|--------------:|
| **NEGany~terribly_surprising**  |    5.73 |    0.50 |   1.00 | 1,315.75 |   949 | 3,173,660 |    949 |        19,802 |        18,776 |
| **NEGany~terribly_popular**     |    2.99 |    0.50 |   1.00 |   206.56 |   149 | 3,173,660 |    149 |        19,802 |        51,120 |
| **NEGany~terribly_unusual**     |    2.96 |    0.50 |   1.00 |   202.40 |   146 | 3,173,660 |    146 |        19,802 |         7,412 |
| **NEGany~terribly_comfortable** |    2.77 |    0.50 |   1.00 |   178.84 |   129 | 3,173,660 |    129 |        19,802 |        23,908 |
| **NEGany~terribly_bright**      |    2.61 |    0.50 |   1.00 |   162.20 |   117 | 3,173,660 |    117 |        19,802 |         8,623 |
| **NEGany~terribly_interested**  |    3.98 |    0.49 |   0.99 |   624.89 |   486 | 3,173,660 |    491 |        19,802 |        34,543 |
| **NEGany~terribly_different**   |    3.93 |    0.49 |   0.99 |   485.33 |   366 | 3,173,660 |    368 |        19,802 |        80,643 |
| **NEGany~terribly_surprised**   |    3.30 |    0.49 |   0.99 |   361.19 |   287 | 3,173,660 |    291 |        19,802 |        10,157 |
| **NEGany~terribly_exciting**    |    3.28 |    0.48 |   0.98 |   456.39 |   382 | 3,173,660 |    391 |        19,802 |        20,233 |
| **NEGany~terribly_common**      |    2.45 |    0.50 |   1.00 |   145.56 |   105 | 3,173,660 |    105 |        19,802 |        34,450 |


#### Top 5 `mirror` "terribly_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                                 |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:--------------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~terribly_surprising**  |    1.85 |    0.50 |   1.00 |  92.89 |    67 | 291,732 |     67 |         2,204 |         1,248 |
| **NEGmir~terribly_original**    |    1.19 |    0.50 |   1.00 |  62.39 |    45 | 291,732 |     45 |         2,204 |           715 |
| **NEGmir~terribly_new**         |    1.64 |    0.49 |   0.99 |  86.57 |    69 | 291,732 |     70 |         2,204 |         4,300 |
| **NEGmir~terribly_interesting** |    1.29 |    0.48 |   0.98 |  68.96 |    56 | 291,732 |     57 |         2,204 |         3,863 |
| **POS~terribly_wrong**          |    1.06 |    0.30 |   0.80 | 149.75 |   319 | 291,729 |    401 |         2,204 |         8,506 |


### 11. _ever_


#### Top 10 `RBdirect` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                        |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |      `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:-----------------------|--------:|--------:|-------:|-------:|------:|----------:|-------:|--------------:|--------------:|
| **COM~ever_larger**    |    2.88 |    0.50 |   1.00 | 192.71 |   139 | 3,173,552 |    139 |        10,870 |         7,453 |
| **NEGany~ever_boring** |    1.84 |    0.50 |   1.00 |  99.82 |    72 | 3,173,660 |     72 |        10,870 |         3,840 |
| **NEGany~ever_simple** |    3.28 |    0.50 |   1.00 | 281.20 |   211 | 3,173,660 |    212 |        10,870 |        46,867 |
| **COM~ever_greater**   |    3.09 |    0.49 |   0.99 | 246.80 |   186 | 3,173,552 |    187 |        10,870 |         6,949 |
| **COM~ever_closer**    |    3.52 |    0.49 |   0.99 | 365.82 |   279 | 3,173,552 |    281 |        10,870 |         3,686 |
| **NEGany~ever_easy**   |    3.53 |    0.48 |   0.98 | 525.98 |   429 | 3,173,660 |    437 |        10,870 |       108,923 |
| **COM~ever_deeper**    |    1.31 |    0.48 |   0.98 |  75.72 |    61 | 3,173,552 |     62 |        10,870 |         1,768 |
| **COM~ever_higher**    |    2.52 |    0.49 |   0.99 | 168.50 |   129 | 3,173,552 |    130 |        10,870 |        12,992 |
| **NEGany~ever_good**   |    2.52 |    0.45 |   0.95 | 337.56 |   331 | 3,173,660 |    350 |        10,870 |       201,244 |
| **COM~ever_mindful**   |    1.04 |    0.48 |   0.98 |  63.56 |    52 | 3,173,552 |     53 |        10,870 |           784 |


#### Top 10 `mirror` "ever_*" bigrams (sorted by `dP1`; `LRC > 1`)


|                         |   `LRC` |   `dP1` |   `P1` |   `G2` |   `f` |    `f1` |   `f2` |   `adv_total` |   `adj_total` |
|:------------------------|--------:|--------:|-------:|-------:|------:|--------:|-------:|--------------:|--------------:|
| **NEGmir~ever_perfect** |    3.60 |    0.50 |   1.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         1,303 |
| **NEGmir~ever_simple**  |    3.60 |    0.50 |   1.00 | 285.65 |   206 | 291,732 |    206 |         4,786 |         7,465 |
| **NEGmir~ever_enough**  |    3.09 |    0.50 |   1.00 | 203.83 |   147 | 291,732 |    147 |         4,786 |         1,326 |
| **NEGmir~ever_certain** |    3.04 |    0.50 |   1.00 | 198.28 |   143 | 291,732 |    143 |         4,786 |         1,276 |
| **NEGmir~ever_wrong**   |    2.52 |    0.50 |   1.00 | 141.42 |   102 | 291,732 |    102 |         4,786 |         8,506 |
| **NEGmir~ever_easy**    |    4.21 |    0.50 |   1.00 | 497.96 |   368 | 291,732 |    369 |         4,786 |         7,749 |
| **NEGmir~ever_good**    |    3.90 |    0.50 |   1.00 | 402.64 |   299 | 291,732 |    300 |         4,786 |        13,423 |
| **NEGmir~ever_black**   |    1.56 |    0.50 |   1.00 |  77.64 |    56 | 291,732 |     56 |         4,786 |           646 |
| **NEGmir~ever_able**    |    2.71 |    0.49 |   0.99 | 178.12 |   136 | 291,732 |    137 |         4,786 |         1,891 |
| **NEGmir~ever_right**   |    1.33 |    0.50 |   1.00 |  67.93 |    49 | 291,732 |     49 |         4,786 |         2,038 |



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
       1. _bad_
       1. _easy_
       1. _aware_
       1. _surprising_
       1. _new_
       1. _wrong_
       1. _indicative_
       1. _true_
       1. _better_
       1. _related_
       1. _enough_
    
    1. _that_ (17 unique)
       1. _easy_
       1. _exciting_
       1. _surprising_
       1. _great_
       1. _good_
       1. _uncommon_
       1. _close_
       1. _different_
       1. _happy_
       1. _popular_
       1. _difficult_
       1. _simple_
       1. _big_
       1. _interested_
       1. _impressed_
       1. _hard_
       1. _unusual_
    
    1. _exactly_ (10 unique)
       1. _subtle_
       1. _easy_
       1. _sure_
       1. _clear_
       1. _surprising_
       1. _new_
       1. _cheap_
       1. _fair_
       1. _fun_
       1. _hard_
    
    1. _any_ (10 unique)
       1. _worse_
       1. _smarter_
       1. _easier_
       1. _younger_
       1. _different_
       1. _nicer_
       1. _happier_
       1. _better_
       1. _brighter_
       1. _sweeter_
    
    1. _remotely_ (10 unique)
       1. _surprising_
       1. _comparable_
       1. _related_
       1. _ready_
       1. _close_
       1. _similar_
       1. _true_
       1. _interested_
       1. _enough_
       1. _funny_
    
    1. _yet_ (10 unique)
       1. _dead_
       1. _final_
       1. _clear_
       1. _sure_
       1. _complete_
       1. _available_
       1. _certain_
       1. _ready_
       1. _able_
       1. _public_
    
    1. _immediately_ (10 unique)
       1. _sure_
       1. _clear_
       1. _obvious_
       1. _successful_
       1. _reachable_
       1. _available_
       1. _certain_
       1. _able_
       1. _apparent_
       1. _possible_
    
    1. _particularly_ (15 unique)
       1. _comfortable_
       1. _likeable_
       1. _religious_
       1. _surprising_
       1. _new_
       1. _flashy_
       1. _novel_
       1. _athletic_
       1. _innovative_
       1. _good_
       1. _acute_
       1. _original_
       1. _radical_
       1. _wrong_
       1. _unusual_
    
    1. _inherently_ (6 unique)
       1. _bad_
       1. _illegal_
       1. _good_
       1. _evil_
       1. _better_
       1. _wrong_
    
    1. _terribly_ (14 unique)
       1. _comfortable_
       1. _exciting_
       1. _interesting_
       1. _surprised_
       1. _surprising_
       1. _new_
       1. _wrong_
       1. _common_
       1. _popular_
       1. _different_
       1. _bright_
       1. _original_
       1. _interested_
       1. _unusual_
    
    1. _ever_ (17 unique)
       1. _easy_
       1. _black_
       1. _larger_
       1. _mindful_
       1. _wrong_
       1. _closer_
       1. _higher_
       1. _good_
       1. _certain_
       1. _able_
       1. _right_
       1. _boring_
       1. _perfect_
       1. _deeper_
       1. _simple_
       1. _greater_
       1. _enough_
    
    1. _ALL bigrams_ (130 unique)
       1. _particularly comfortable_
       1. _particularly surprising_
       1. _terribly unusual_
       1. _that great_
       1. _terribly surprising_
       1. _that impressed_
       1. _that happy_
       1. _particularly original_
       1. _inherently wrong_
       1. _inherently evil_
       1. _that simple_
       1. _yet dead_
       1. _terribly exciting_
       1. _ever higher_
       1. _any sweeter_
       1. _any happier_
       1. _terribly interested_
       1. _remotely similar_
       1. _ever perfect_
       1. _particularly radical_
       1. _necessarily easy_
       1. _particularly flashy_
       1. _necessarily aware_
       1. _particularly new_
       1. _immediately clear_
       1. _ever deeper_
       1. _ever enough_
       1. _that uncommon_
       1. _exactly surprising_
       1. _immediately successful_
       1. _particularly acute_
       1. _remotely comparable_
       1. _that different_
       1. _exactly new_
       1. _ever greater_
       1. _particularly athletic_
       1. _necessarily bad_
       1. _particularly novel_
       1. _inherently good_
       1. _remotely enough_
       1. _any different_
       1. _exactly subtle_
       1. _remotely funny_
       1. _necessarily new_
       1. _necessarily indicative_
       1. _exactly fair_
       1. _exactly cheap_
       1. _yet public_
       1. _terribly original_
       1. _inherently illegal_
       1. _immediately able_
       1. _immediately possible_
       1. _that close_
       1. _yet final_
       1. _ever good_
       1. _immediately reachable_
       1. _particularly good_
       1. _remotely close_
       1. _that good_
       1. _that popular_
       1. _that interested_
       1. _necessarily true_
       1. _terribly bright_
       1. _terribly comfortable_
       1. _yet certain_
       1. _ever easy_
       1. _yet complete_
       1. _terribly different_
       1. _yet clear_
       1. _particularly religious_
       1. _necessarily better_
       1. _particularly innovative_
       1. _exactly easy_
       1. _that big_
       1. _any worse_
       1. _any brighter_
       1. _that difficult_
       1. _remotely true_
       1. _remotely ready_
       1. _necessarily related_
       1. _ever certain_
       1. _exactly sure_
       1. _terribly new_
       1. _terribly common_
       1. _necessarily enough_
       1. _terribly wrong_
       1. _yet ready_
       1. _particularly likeable_
       1. _ever closer_
       1. _yet able_
       1. _exactly fun_
       1. _any better_
       1. _yet available_
       1. _particularly wrong_
       1. _necessarily surprising_
       1. _remotely interested_
       1. _terribly popular_
       1. _exactly hard_
       1. _immediately obvious_
       1. _remotely related_
       1. _remotely surprising_
       1. _inherently bad_
       1. _ever larger_
       1. _any nicer_
       1. _ever mindful_
       1. _exactly clear_
       1. _that easy_
       1. _any younger_
       1. _immediately apparent_
       1. _that unusual_
       1. _immediately sure_
       1. _particularly unusual_
       1. _ever black_
       1. _any smarter_
       1. _ever simple_
       1. _immediately available_
       1. _necessarily wrong_
       1. _that exciting_
       1. _terribly surprised_
       1. _terribly interesting_
       1. _ever wrong_
       1. _yet sure_
       1. _that hard_
       1. _any easier_
       1. _ever boring_
       1. _ever able_
       1. _ever right_
       1. _inherently better_
       1. _immediately certain_
       1. _that surprising_
    
    1. _ALL adjectives_ (82 unique)
       1. _bad_
       1. _sure_
       1. _complete_
       1. _simple_
       1. _enough_
       1. _likeable_
       1. _surprising_
       1. _cheap_
       1. _nicer_
       1. _fun_
       1. _acute_
       1. _perfect_
       1. _interested_
       1. _closer_
       1. _right_
       1. _radical_
       1. _big_
       1. _related_
       1. _funny_
       1. _novel_
       1. _different_
       1. _difficult_
       1. _impressed_
       1. _subtle_
       1. _younger_
       1. _ready_
       1. _similar_
       1. _able_
       1. _public_
       1. _easier_
       1. _common_
       1. _popular_
       1. _wrong_
       1. _comfortable_
       1. _clear_
       1. _comparable_
       1. _new_
       1. _certain_
       1. _better_
       1. _aware_
       1. _worse_
       1. _black_
       1. _smarter_
       1. _great_
       1. _illegal_
       1. _good_
       1. _happy_
       1. _original_
       1. _hard_
       1. _mindful_
       1. _apparent_
       1. _bright_
       1. _greater_
       1. _successful_
       1. _obvious_
       1. _uncommon_
       1. _close_
       1. _deeper_
       1. _sweeter_
       1. _final_
       1. _flashy_
       1. _reachable_
       1. _larger_
       1. _athletic_
       1. _available_
       1. _higher_
       1. _indicative_
       1. _boring_
       1. _surprised_
       1. _dead_
       1. _possible_
       1. _fair_
       1. _true_
       1. _brighter_
       1. _easy_
       1. _interesting_
       1. _exciting_
       1. _religious_
       1. _innovative_
       1. _evil_
       1. _happier_
       1. _unusual_



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
NEG_bigrams_sample = adjust_assoc_columns(pd.concat(
    (ad['both'] for ad in samples_dict.values() if isinstance(ad, dict))).sort_values('LRC', ascending=False))
```


```python
top_NEGbigram_df_path =  OUT_DIR.joinpath(
    f'{TAG}-Top{K}_NEG-ADV_top-{bigram_k}-bigrams-{bigram_floor}.{timestamp_today()}.csv')
print(top_NEGbigram_df_path)

```

    /share/compling/projects/sanpi/results/top_AM/NEQ/NEQ-Top8/NEQ-Top8_NEG-ADV_top-10-bigrams-25.2024-07-28.csv



```python
NEG_bigrams_sample.to_csv(top_NEGbigram_df_path)
nb_show_table(NEG_bigrams_sample.filter(FOCUS).sort_values('LRC', ascending=False),
              outpath=top_NEGbigram_df_path.with_suffix('.md'))
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    /tmp/ipykernel_20172/2217350191.py in ?()
          1 NEG_bigrams_sample.to_csv(top_NEGbigram_df_path)
    ----> 2 nb_show_table(NEG_bigrams_sample.filter(FOCUS).sort_values('LRC', ascending=False),
          3               outpath=top_NEGbigram_df_path.with_suffix('.md'))


    ~/anaconda3/envs/dev-sanpi/lib/python3.10/site-packages/pandas/core/frame.py in ?(self, by, axis, ascending, inplace, kind, na_position, ignore_index, key)
       6940             )
       6941         elif len(by):
       6942             # len(by) == 1
       6943 
    -> 6944             k = self._get_label_or_level_values(by[0], axis=axis)
       6945 
       6946             # need to rewrap column in Series to apply key function
       6947             if key is not None:


    ~/anaconda3/envs/dev-sanpi/lib/python3.10/site-packages/pandas/core/generic.py in ?(self, key, axis)
       1840             values = self.xs(key, axis=other_axes[0])._values
       1841         elif self._is_level_reference(key, axis=axis):
       1842             values = self.axes[axis].get_level_values(key)._values
       1843         else:
    -> 1844             raise KeyError(key)
       1845 
       1846         # Check for duplicates
       1847         if values.ndim > 1:


    KeyError: 'LRC'



|                                     | `adj`       |   `f2` |   `adv_total` |   `t` |    `f` |      `f1` |      `G2` |       `N` |   `P1` | `l2`                     |   `exp_f` |   `dP1` | `l1`       |   `odds_r_disc` |   `LRC` | `adv`        |   `MI` |   `unexp_f` |   `adj_total` |
|:------------------------------------|:------------|-------:|--------------:|------:|-------:|----------:|----------:|----------:|-------:|:-------------------------|----------:|--------:|:-----------|----------------:|--------:|:-------------|-------:|------------:|--------------:|
| **NEGany~yet_clear**                | clear       | 10,409 |        53,881 | 50.99 | 10,406 | 3,173,660 | 14,392.25 | 6,347,364 |   1.00 | yet_clear                |  5,204.46 |    0.50 | NEGATED    |            3.47 |    8.66 | yet          |   0.30 |    5,201.54 |        84,227 |
| **NEGany~yet_ready**                | ready       |  7,505 |        53,881 | 43.28 |  7,501 | 3,173,660 | 10,344.81 | 6,347,364 |   1.00 | yet_ready                |  3,752.47 |    0.50 | NEGATED    |            3.22 |    8.06 | yet          |   0.30 |    3,748.53 |        29,583 |
| **NEGany~that_hard**                | hard        |  9,963 |       166,676 | 49.79 |  9,948 | 3,173,660 | 13,602.42 | 6,347,364 |   1.00 | that_hard                |  4,981.47 |    0.50 | NEGATED    |            2.81 |    7.68 | that         |   0.30 |    4,966.53 |        45,061 |
| **NEGany~immediately_clear**        | clear       | 24,488 |        58,040 | 77.90 | 24,416 | 3,173,660 | 33,058.44 | 6,347,364 |   1.00 | immediately_clear        | 12,243.92 |    0.50 | NEGATED    |            2.53 |    7.55 | immediately  |   0.30 |   12,172.08 |        84,227 |
| **NEGany~exactly_sure**             | sure        |  8,810 |        44,503 | 46.80 |  8,794 | 3,173,660 | 11,991.61 | 6,347,364 |   1.00 | exactly_sure             |  4,404.97 |    0.50 | NEGATED    |            2.73 |    7.46 | exactly      |   0.30 |    4,389.03 |       134,139 |
| **NEGany~that_different**           | different   |  6,547 |       166,676 | 40.34 |  6,534 | 3,173,660 |  8,895.12 | 6,347,364 |   1.00 | that_different           |  3,273.48 |    0.50 | NEGATED    |            2.69 |    7.18 | that         |   0.30 |    3,260.52 |        80,643 |
| **NEGany~that_great**               | great       | 11,065 |       166,676 | 52.36 | 11,032 | 3,173,660 | 14,908.90 | 6,347,364 |   1.00 | that_great               |  5,532.46 |    0.50 | NEGATED    |            2.52 |    7.18 | that         |   0.30 |    5,499.54 |        45,359 |
| **NEGany~that_difficult**           | difficult   |  5,571 |       166,676 | 37.21 |  5,560 | 3,173,660 |  7,569.00 | 6,347,364 |   1.00 | that_difficult           |  2,785.48 |    0.50 | NEGATED    |            2.69 |    7.06 | that         |   0.30 |    2,774.52 |        61,490 |
| **NEGany~yet_complete**             | complete    |  2,175 |        53,881 | 23.30 |  2,174 | 3,173,660 |  2,998.60 | 6,347,364 |   1.00 | yet_complete             |  1,087.49 |    0.50 | NEGATED    |            3.16 |    6.70 | yet          |   0.30 |    1,086.51 |         8,415 |
| **NEGany~yet_available**            | available   |  7,461 |        53,881 | 42.92 |  7,430 | 3,173,660 |  9,950.03 | 6,347,364 |   1.00 | yet_available            |  3,730.47 |    0.50 | NEGATED    |            2.37 |    6.66 | yet          |   0.30 |    3,699.53 |        82,956 |
| **NEGany~that_big**                 | big         |  6,273 |       166,676 | 39.33 |  6,244 | 3,173,660 |  8,332.69 | 6,347,364 |   1.00 | that_big                 |  3,136.48 |    0.50 | NEGATED    |            2.33 |    6.47 | that         |   0.30 |    3,107.52 |        42,912 |
| **NEGany~exactly_clear**            | clear       |  1,747 |        44,503 | 20.88 |  1,746 | 3,173,660 |  2,405.43 | 6,347,364 |   1.00 | exactly_clear            |    873.49 |    0.50 | NEGATED    |            3.07 |    6.38 | exactly      |   0.30 |      872.51 |        84,227 |
| **NEGany~necessarily_bad**          | bad         |  2,062 |        42,886 | 22.66 |  2,059 | 3,173,660 |  2,814.04 | 6,347,364 |   1.00 | necessarily_bad          |  1,030.99 |    0.50 | NEGATED    |            2.77 |    6.31 | necessarily  |   0.30 |    1,028.01 |       119,509 |
| **NEGany~necessarily_indicative**   | indicative  |  1,389 |        42,886 | 18.63 |  1,389 | 3,173,660 |  1,925.89 | 6,347,364 |   1.00 | necessarily_indicative   |    694.50 |    0.50 | NEGATED    |            3.44 |    6.29 | necessarily  |   0.30 |      694.50 |         2,313 |
| **NEGany~necessarily_true**         | true        |  3,245 |        42,886 | 28.31 |  3,232 | 3,173,660 |  4,330.74 | 6,347,364 |   1.00 | necessarily_true         |  1,622.49 |    0.50 | NEGATED    |            2.38 |    6.16 | necessarily  |   0.30 |    1,609.51 |        34,967 |
| **NEGany~yet_sure**                 | sure        |  1,981 |        53,881 | 22.19 |  1,977 | 3,173,660 |  2,689.26 | 6,347,364 |   1.00 | yet_sure                 |    990.49 |    0.50 | NEGATED    |            2.64 |    6.13 | yet          |   0.30 |      986.51 |       134,139 |
| **NEGany~necessarily_better**       | better      |  1,891 |        42,886 | 21.67 |  1,887 | 3,173,660 |  2,564.81 | 6,347,364 |   1.00 | necessarily_better       |    945.49 |    0.50 | NEGATED    |            2.62 |    6.07 | necessarily  |   0.30 |      941.51 |        50,827 |
| **NEGany~exactly_new**              | new         |  1,372 |        44,503 | 18.50 |  1,371 | 3,173,660 |  1,885.86 | 6,347,364 |   1.00 | exactly_new              |    686.00 |    0.50 | NEGATED    |            2.96 |    6.03 | exactly      |   0.30 |      685.00 |        21,538 |
| **NEGany~that_surprising**          | surprising  |  1,133 |       166,676 | 16.83 |  1,133 | 3,173,660 |  1,570.89 | 6,347,364 |   1.00 | that_surprising          |    566.50 |    0.50 | NEGATED    |            3.36 |    5.99 | that         |   0.30 |      566.50 |        18,776 |
| **NEGany~that_unusual**             | unusual     |    977 |       166,676 | 15.63 |    977 | 3,173,660 |  1,354.57 | 6,347,364 |   1.00 | that_unusual             |    488.50 |    0.50 | NEGATED    |            3.29 |    5.77 | that         |   0.30 |      488.50 |         7,412 |
| **NEGany~terribly_surprising**      | surprising  |    949 |        19,802 | 15.40 |    949 | 3,173,660 |  1,315.75 | 6,347,364 |   1.00 | terribly_surprising      |    474.50 |    0.50 | NEGATED    |            3.28 |    5.73 | terribly     |   0.30 |      474.50 |        18,776 |
| **NEGany~necessarily_easy**         | easy        |    909 |        42,886 | 15.07 |    909 | 3,173,660 |  1,260.28 | 6,347,364 |   1.00 | necessarily_easy         |    454.50 |    0.50 | NEGATED    |            3.26 |    5.67 | necessarily  |   0.30 |      454.50 |       108,923 |
| **NEGany~exactly_easy**             | easy        |  1,067 |        44,503 | 16.31 |  1,066 | 3,173,660 |  1,463.43 | 6,347,364 |   1.00 | exactly_easy             |    533.50 |    0.50 | NEGATED    |            2.85 |    5.67 | exactly      |   0.30 |      532.50 |       108,923 |
| **NEGany~yet_certain**              | certain     |    866 |        53,881 | 14.71 |    866 | 3,173,660 |  1,200.66 | 6,347,364 |   1.00 | yet_certain              |    433.00 |    0.50 | NEGATED    |            3.24 |    5.60 | yet          |   0.30 |      433.00 |        11,334 |
| **NEGany~that_exciting**            | exciting    |    805 |       166,676 | 14.19 |    805 | 3,173,660 |  1,116.08 | 6,347,364 |   1.00 | that_exciting            |    402.50 |    0.50 | NEGATED    |            3.21 |    5.49 | that         |   0.30 |      402.50 |        20,233 |
| **NEGany~that_uncommon**            | uncommon    |    802 |       166,676 | 14.16 |    802 | 3,173,660 |  1,111.92 | 6,347,364 |   1.00 | that_uncommon            |    401.00 |    0.50 | NEGATED    |            3.21 |    5.49 | that         |   0.30 |      401.00 |         3,165 |
| **NEGany~yet_able**                 | able        |  1,320 |        53,881 | 18.06 |  1,315 | 3,173,660 |  1,764.46 | 6,347,364 |   1.00 | yet_able                 |    660.00 |    0.50 | NEGATED    |            2.38 |    5.44 | yet          |   0.30 |      655.00 |        23,355 |
| **NEGany~immediately_possible**     | possible    |  1,002 |        58,040 | 15.78 |  1,000 | 3,173,660 |  1,360.38 | 6,347,364 |   1.00 | immediately_possible     |    501.00 |    0.50 | NEGATED    |            2.60 |    5.40 | immediately  |   0.30 |      499.00 |        30,446 |
| **NEGany~immediately_available**    | available   | 21,477 |        58,040 | 71.22 | 21,078 | 3,173,660 | 25,870.14 | 6,347,364 |   0.98 | immediately_available    | 10,738.43 |    0.48 | NEGATED    |            1.73 |    5.34 | immediately  |   0.29 |   10,339.57 |        82,956 |
| **NEGany~exactly_cheap**            | cheap       |    691 |        44,503 | 13.14 |    691 | 3,173,660 |    958.01 | 6,347,364 |   1.00 | exactly_cheap            |    345.50 |    0.50 | NEGATED    |            3.14 |    5.27 | exactly      |   0.30 |      345.50 |         6,591 |
| **NEGany~that_impressed**           | impressed   |    681 |       166,676 | 13.05 |    681 | 3,173,660 |    944.15 | 6,347,364 |   1.00 | that_impressed           |    340.50 |    0.50 | NEGATED    |            3.13 |    5.25 | that         |   0.30 |      340.50 |        12,138 |
| **NEGany~yet_final**                | final       |    640 |        53,881 | 12.65 |    640 | 3,173,660 |    887.30 | 6,347,364 |   1.00 | yet_final                |    320.00 |    0.50 | NEGATED    |            3.11 |    5.16 | yet          |   0.30 |      320.00 |         1,213 |
| **NEGany~necessarily_related**      | related     |    742 |        42,886 | 13.59 |    741 | 3,173,660 |  1,013.51 | 6,347,364 |   1.00 | necessarily_related      |    371.00 |    0.50 | NEGATED    |            2.69 |    5.14 | necessarily  |   0.30 |      370.00 |        14,260 |
| **NEGany~necessarily_new**          | new         |    482 |        42,886 | 10.98 |    482 | 3,173,660 |    668.24 | 6,347,364 |   1.00 | necessarily_new          |    241.00 |    0.50 | NEGATED    |            2.98 |    4.74 | necessarily  |   0.30 |      241.00 |        21,538 |
| **NEGany~yet_public**               | public      |    467 |        53,881 | 10.81 |    467 | 3,173,660 |    647.44 | 6,347,364 |   1.00 | yet_public               |    233.50 |    0.50 | NEGATED    |            2.97 |    4.69 | yet          |   0.30 |      233.50 |         2,656 |
| **NEGany~any_happier**              | happier     |    834 |        16,238 | 14.28 |    828 | 3,173,660 |  1,085.12 | 6,347,364 |   0.99 | any_happier              |    417.00 |    0.49 | NEGATED    |            2.11 |    4.66 | any          |   0.30 |      411.00 |         2,004 |
| **NEGany~particularly_new**         | new         |    752 |        76,162 | 13.57 |    747 | 3,173,660 |    982.49 | 6,347,364 |   0.99 | particularly_new         |    376.00 |    0.49 | NEGATED    |            2.13 |    4.61 | particularly |   0.30 |      371.00 |        21,538 |
| **NEGany~exactly_surprising**       | surprising  |    440 |        44,503 | 10.49 |    440 | 3,173,660 |    610.01 | 6,347,364 |   1.00 | exactly_surprising       |    220.00 |    0.50 | NEGATED    |            2.95 |    4.61 | exactly      |   0.30 |      220.00 |        18,776 |
| **NEGany~particularly_religious**   | religious   |    486 |        76,162 | 10.99 |    485 | 3,173,660 |    659.41 | 6,347,364 |   1.00 | particularly_religious   |    243.00 |    0.50 | NEGATED    |            2.51 |    4.52 | particularly |   0.30 |      242.00 |         3,507 |
| **NEGany~yet_dead**                 | dead        |    401 |        53,881 | 10.01 |    401 | 3,173,660 |    555.93 | 6,347,364 |   1.00 | yet_dead                 |    200.50 |    0.50 | NEGATED    |            2.90 |    4.47 | yet          |   0.30 |      200.50 |         6,348 |
| **NEGany~any_easier**               | easier      |  1,625 |        16,238 | 19.57 |  1,594 | 3,173,660 |  1,946.26 | 6,347,364 |   0.98 | any_easier               |    812.49 |    0.48 | NEGATED    |            1.70 |    4.42 | any          |   0.29 |      781.51 |        12,877 |
| **NEGmir~particularly_new**         | new         |    405 |        10,029 | 10.03 |    404 |   291,732 |    547.73 |   583,470 |   1.00 | particularly_new         |    202.50 |    0.50 | NEGMIR     |            2.43 |    4.35 | particularly |   0.30 |      201.50 |         4,300 |
| **NEGany~inherently_wrong**         | wrong       |  1,678 |         8,614 | 19.76 |  1,639 | 3,173,660 |  1,956.12 | 6,347,364 |   0.98 | inherently_wrong         |    838.99 |    0.48 | NEGATED    |            1.62 |    4.25 | inherently   |   0.29 |      800.01 |        21,332 |
| **NEGany~necessarily_surprising**   | surprising  |    340 |        42,886 |  9.22 |    340 | 3,173,660 |    471.36 | 6,347,364 |   1.00 | necessarily_surprising   |    170.00 |    0.50 | NEGATED    |            2.83 |    4.23 | necessarily  |   0.30 |      170.00 |        18,776 |
| **NEGmir~ever_easy**                | easy        |    369 |         4,786 |  9.57 |    368 |   291,732 |    497.96 |   583,470 |   1.00 | ever_easy                |    184.50 |    0.50 | NEGMIR     |            2.39 |    4.21 | ever         |   0.30 |      183.50 |         7,749 |
| **NEGany~terribly_interested**      | interested  |    491 |        19,802 | 10.91 |    486 | 3,173,660 |    624.89 | 6,347,364 |   0.99 | terribly_interested      |    245.50 |    0.49 | NEGATED    |            1.95 |    3.98 | terribly     |   0.30 |      240.50 |        34,543 |
| **NEGany~necessarily_enough**       | enough      |    279 |        42,886 |  8.35 |    279 | 3,173,660 |    386.79 | 6,347,364 |   1.00 | necessarily_enough       |    139.50 |    0.50 | NEGATED    |            2.75 |    3.93 | necessarily  |   0.30 |      139.50 |        27,603 |
| **NEGany~particularly_surprising**  | surprising  |  1,097 |        76,162 | 15.92 |  1,069 | 3,173,660 |  1,260.26 | 6,347,364 |   0.97 | particularly_surprising  |    548.50 |    0.47 | NEGATED    |            1.57 |    3.93 | particularly |   0.29 |      520.50 |        18,776 |
| **NEGany~terribly_different**       | different   |    368 |        19,802 |  9.51 |    366 | 3,173,660 |    485.33 | 6,347,364 |   0.99 | terribly_different       |    184.00 |    0.49 | NEGATED    |            2.17 |    3.93 | terribly     |   0.30 |      182.00 |        80,643 |
| **NEGmir~ever_good**                | good        |    300 |         4,786 |  8.62 |    299 |   291,732 |    402.64 |   583,470 |   1.00 | ever_good                |    150.00 |    0.50 | NEGMIR     |            2.30 |    3.90 | ever         |   0.30 |      149.00 |        13,423 |
| **NEGany~immediately_obvious**      | obvious     |  2,325 |        58,040 | 22.73 |  2,238 | 3,173,660 |  2,481.50 | 6,347,364 |   0.96 | immediately_obvious      |  1,162.49 |    0.46 | NEGATED    |            1.41 |    3.88 | immediately  |   0.28 |    1,075.51 |        22,651 |
| **NEGany~inherently_bad**           | bad         |    812 |         8,614 | 13.77 |    794 | 3,173,660 |    953.05 | 6,347,364 |   0.98 | inherently_bad           |    406.00 |    0.48 | NEGATED    |            1.63 |    3.87 | inherently   |   0.29 |      388.00 |       119,509 |
| **NEGany~exactly_subtle**           | subtle      |    263 |        44,503 |  8.11 |    263 | 3,173,660 |    364.61 | 6,347,364 |   1.00 | exactly_subtle           |    131.50 |    0.50 | NEGATED    |            2.72 |    3.84 | exactly      |   0.30 |      131.50 |         5,299 |
| **NEGany~exactly_fair**             | fair        |    260 |        44,503 |  8.06 |    260 | 3,173,660 |    360.45 | 6,347,364 |   1.00 | exactly_fair             |    130.00 |    0.50 | NEGATED    |            2.72 |    3.83 | exactly      |   0.30 |      130.00 |         6,964 |
| **NEGany~any_younger**              | younger     |    255 |        16,238 |  7.98 |    255 | 3,173,660 |    353.52 | 6,347,364 |   1.00 | any_younger              |    127.50 |    0.50 | NEGATED    |            2.71 |    3.80 | any          |   0.30 |      127.50 |         1,784 |
| **NEGmir~inherently_wrong**         | wrong       |  1,571 |         3,342 | 18.70 |  1,513 |   291,732 |  1,685.02 |   583,470 |   0.96 | inherently_wrong         |    785.49 |    0.46 | NEGMIR     |            1.42 |    3.78 | inherently   |   0.28 |      727.51 |         8,506 |
| **NEGmir~that_simple**              | simple      |    483 |         4,559 | 10.68 |    474 |   291,732 |    580.44 |   583,470 |   0.98 | that_simple              |    241.50 |    0.48 | NEGMIR     |            1.70 |    3.67 | that         |   0.29 |      232.50 |         7,465 |
| **NEGany~immediately_able**         | able        |    641 |        58,040 | 12.21 |    626 | 3,173,660 |    746.39 | 6,347,364 |   0.98 | immediately_able         |    320.50 |    0.48 | NEGATED    |            1.61 |    3.66 | immediately  |   0.29 |      305.50 |        23,355 |
| **NEGany~particularly_original**    | original    |    364 |        76,162 |  9.38 |    360 | 3,173,660 |    460.59 | 6,347,364 |   0.99 | particularly_original    |    182.00 |    0.49 | NEGATED    |            1.90 |    3.64 | particularly |   0.30 |      178.00 |         4,693 |
| **NEGany~any_worse**                | worse       |  1,762 |        16,238 | 19.61 |  1,686 | 3,173,660 |  1,816.60 | 6,347,364 |   0.96 | any_worse                |    880.99 |    0.46 | NEGATED    |            1.34 |    3.62 | any          |   0.28 |      805.01 |        12,116 |
| **NEGany~exactly_fun**              | fun         |    224 |        44,503 |  7.48 |    224 | 3,173,660 |    310.54 | 6,347,364 |   1.00 | exactly_fun              |    112.00 |    0.50 | NEGATED    |            2.65 |    3.60 | exactly      |   0.30 |      112.00 |        19,661 |
| **NEGmir~ever_perfect**             | perfect     |    206 |         4,786 |  7.18 |    206 |   291,732 |    285.65 |   583,470 |   1.00 | ever_perfect             |    103.00 |    0.50 | NEGMIR     |            2.62 |    3.60 | ever         |   0.30 |      103.00 |         1,303 |
| **NEGmir~ever_simple**              | simple      |    206 |         4,786 |  7.18 |    206 |   291,732 |    285.65 |   583,470 |   1.00 | ever_simple              |    103.00 |    0.50 | NEGMIR     |            2.62 |    3.60 | ever         |   0.30 |      103.00 |         7,465 |
| **NEGany~any_better**               | better      |  5,004 |        16,238 | 32.27 |  4,719 | 3,173,660 |  4,753.39 | 6,347,364 |   0.94 | any_better               |  2,501.98 |    0.44 | NEGATED    |            1.22 |    3.59 | any          |   0.28 |    2,217.02 |        50,827 |
| **NEGany~particularly_wrong**       | wrong       |    218 |        76,162 |  7.38 |    218 | 3,173,660 |    302.22 | 6,347,364 |   1.00 | particularly_wrong       |    109.00 |    0.50 | NEGATED    |            2.64 |    3.56 | particularly |   0.30 |      109.00 |        21,332 |
| **NEGany~remotely_true**            | true        |    251 |         6,161 |  7.87 |    250 | 3,173,660 |    334.93 | 6,347,364 |   1.00 | remotely_true            |    125.50 |    0.50 | NEGATED    |            2.22 |    3.53 | remotely     |   0.30 |      124.50 |        34,967 |
| **NEGany~ever_easy**                | easy        |    437 |        10,870 | 10.16 |    429 | 3,173,660 |    525.98 | 6,347,364 |   0.98 | ever_easy                |    218.50 |    0.48 | NEGATED    |            1.70 |    3.53 | ever         |   0.29 |      210.50 |       108,923 |
| **COM~ever_closer**                 | closer      |    281 |        10,870 |  8.29 |    279 | 3,173,552 |    365.82 | 6,347,364 |   0.99 | ever_closer              |    140.49 |    0.49 | COMPLEMENT |            2.05 |    3.52 | ever         |   0.30 |      138.51 |         3,686 |
| **NEGany~necessarily_aware**        | aware       |    206 |        42,886 |  7.18 |    206 | 3,173,660 |    285.59 | 6,347,364 |   1.00 | necessarily_aware        |    103.00 |    0.50 | NEGATED    |            2.62 |    3.48 | necessarily  |   0.30 |      103.00 |        28,973 |
| **NEGany~exactly_hard**             | hard        |    203 |        44,503 |  7.12 |    203 | 3,173,660 |    281.43 | 6,347,364 |   1.00 | exactly_hard             |    101.50 |    0.50 | NEGATED    |            2.61 |    3.46 | exactly      |   0.30 |      101.50 |        45,061 |
| **NEGmir~particularly_wrong**       | wrong       |    213 |        10,029 |  7.25 |    212 |   291,732 |    282.64 |   583,470 |   1.00 | particularly_wrong       |    106.50 |    0.50 | NEGMIR     |            2.15 |    3.39 | particularly |   0.30 |      105.50 |         8,506 |
| **NEGany~immediately_apparent**     | apparent    |  2,143 |        58,040 | 21.02 |  2,015 | 3,173,660 |  2,001.83 | 6,347,364 |   0.94 | immediately_apparent     |  1,071.49 |    0.44 | NEGATED    |            1.20 |    3.30 | immediately  |   0.27 |      943.51 |         9,798 |
| **NEGany~terribly_surprised**       | surprised   |    291 |        19,802 |  8.35 |    287 | 3,173,660 |    361.19 | 6,347,364 |   0.99 | terribly_surprised       |    145.50 |    0.49 | NEGATED    |            1.81 |    3.30 | terribly     |   0.30 |      141.50 |        10,157 |
| **NEGany~terribly_exciting**        | exciting    |    391 |        19,802 |  9.54 |    382 | 3,173,660 |    456.39 | 6,347,364 |   0.98 | terribly_exciting        |    195.50 |    0.48 | NEGATED    |            1.60 |    3.28 | terribly     |   0.29 |      186.50 |        20,233 |
| **NEGany~ever_simple**              | simple      |    212 |        10,870 |  7.23 |    211 | 3,173,660 |    281.20 | 6,347,364 |   1.00 | ever_simple              |    106.00 |    0.50 | NEGATED    |            2.15 |    3.28 | ever         |   0.30 |      105.00 |        46,867 |
| **NEGmir~any_better**               | better      |    390 |         1,095 |  9.49 |    380 |   291,732 |    447.88 |   583,470 |   0.97 | any_better               |    195.00 |    0.47 | NEGMIR     |            1.56 |    3.27 | any          |   0.29 |      185.00 |         3,831 |
| **NEGmir~particularly_surprising**  | surprising  |    166 |        10,029 |  6.44 |    166 |   291,732 |    230.18 |   583,470 |   1.00 | particularly_surprising  |     83.00 |    0.50 | NEGMIR     |            2.52 |    3.27 | particularly |   0.30 |       83.00 |         1,248 |
| **NEGmir~particularly_good**        | good        |    401 |        10,029 |  9.60 |    390 |   291,732 |    455.35 |   583,470 |   0.97 | particularly_good        |    200.50 |    0.47 | NEGMIR     |            1.53 |    3.24 | particularly |   0.29 |      189.50 |        13,423 |
| **NEGmir~that_easy**                | easy        |    465 |         4,559 | 10.25 |    450 |   291,732 |    512.43 |   583,470 |   0.97 | that_easy                |    232.50 |    0.47 | NEGMIR     |            1.46 |    3.23 | that         |   0.29 |      217.50 |         7,749 |
| **NEGmir~exactly_sure**             | sure        |    148 |           869 |  6.08 |    148 |   291,732 |    205.21 |   583,470 |   1.00 | exactly_sure             |     74.00 |    0.50 | NEGMIR     |            2.47 |    3.10 | exactly      |   0.30 |       74.00 |         5,978 |
| **NEGmir~ever_enough**              | enough      |    147 |         4,786 |  6.06 |    147 |   291,732 |    203.83 |   583,470 |   1.00 | ever_enough              |     73.50 |    0.50 | NEGMIR     |            2.47 |    3.09 | ever         |   0.30 |       73.50 |         1,326 |
| **COM~ever_greater**                | greater     |    187 |        10,870 |  6.78 |    186 | 3,173,552 |    246.80 | 6,347,364 |   0.99 | ever_greater             |     93.50 |    0.49 | COMPLEMENT |            2.09 |    3.09 | ever         |   0.30 |       92.50 |         6,949 |
| **NEGmir~necessarily_wrong**        | wrong       |    214 |           992 |  7.16 |    211 |   291,732 |    265.18 |   583,470 |   0.99 | necessarily_wrong        |    107.00 |    0.49 | NEGMIR     |            1.78 |    3.05 | necessarily  |   0.29 |      104.00 |         8,506 |
| **NEGmir~ever_certain**             | certain     |    143 |         4,786 |  5.98 |    143 |   291,732 |    198.28 |   583,470 |   1.00 | ever_certain             |     71.50 |    0.50 | NEGMIR     |            2.46 |    3.04 | ever         |   0.30 |       71.50 |         1,276 |
| **NEGany~any_different**            | different   |    957 |        16,238 | 14.10 |    902 | 3,173,660 |    905.82 | 6,347,364 |   0.94 | any_different            |    478.50 |    0.44 | NEGATED    |            1.21 |    3.03 | any          |   0.28 |      423.50 |        80,643 |
| **NEGany~terribly_popular**         | popular     |    149 |        19,802 |  6.10 |    149 | 3,173,660 |    206.56 | 6,347,364 |   1.00 | terribly_popular         |     74.50 |    0.50 | NEGATED    |            2.48 |    2.99 | terribly     |   0.30 |       74.50 |        51,120 |
| **NEGany~remotely_close**           | close       |    733 |         6,161 | 12.43 |    694 | 3,173,660 |    711.52 | 6,347,364 |   0.95 | remotely_close           |    366.50 |    0.45 | NEGATED    |            1.25 |    2.98 | remotely     |   0.28 |      327.50 |        46,485 |
| **NEGany~terribly_unusual**         | unusual     |    146 |        19,802 |  6.04 |    146 | 3,173,660 |    202.40 | 6,347,364 |   1.00 | terribly_unusual         |     73.00 |    0.50 | NEGATED    |            2.47 |    2.96 | terribly     |   0.30 |       73.00 |         7,412 |
| **COM~ever_larger**                 | larger      |    139 |        10,870 |  5.90 |    139 | 3,173,552 |    192.71 | 6,347,364 |   1.00 | ever_larger              |     69.50 |    0.50 | COMPLEMENT |            2.45 |    2.88 | ever         |   0.30 |       69.50 |         7,453 |
| **NEGany~immediately_sure**         | sure        |    138 |        58,040 |  5.87 |    138 | 3,173,660 |    191.31 | 6,347,364 |   1.00 | immediately_sure         |     69.00 |    0.50 | NEGATED    |            2.44 |    2.87 | immediately  |   0.30 |       69.00 |       134,139 |
| **NEGany~immediately_successful**   | successful  |    299 |        58,040 |  8.25 |    290 | 3,173,660 |    333.73 | 6,347,364 |   0.97 | immediately_successful   |    149.50 |    0.47 | NEGATED    |            1.49 |    2.87 | immediately  |   0.29 |      140.50 |        31,460 |
| **COM~particularly_acute**          | acute       |    135 |        76,162 |  5.81 |    135 | 3,173,552 |    187.16 | 6,347,364 |   1.00 | particularly_acute       |     67.50 |    0.50 | COMPLEMENT |            2.43 |    2.84 | particularly |   0.30 |       67.50 |         1,038 |
| **NEGany~terribly_comfortable**     | comfortable |    129 |        19,802 |  5.68 |    129 | 3,173,660 |    178.84 | 6,347,364 |   1.00 | terribly_comfortable     |     64.50 |    0.50 | NEGATED    |            2.41 |    2.77 | terribly     |   0.30 |       64.50 |        23,908 |
| **NEGmir~particularly_unusual**     | unusual     |    173 |        10,029 |  6.40 |    170 |   291,732 |    209.60 |   583,470 |   0.98 | particularly_unusual     |     86.50 |    0.48 | NEGMIR     |            1.69 |    2.72 | particularly |   0.29 |       83.50 |           933 |
| **NEGmir~that_great**               | great       |    298 |         4,559 |  8.10 |    286 |   291,732 |    312.65 |   583,470 |   0.96 | that_great               |    149.00 |    0.46 | NEGMIR     |            1.36 |    2.71 | that         |   0.28 |      137.00 |         2,123 |
| **NEGmir~ever_able**                | able        |    137 |         4,786 |  5.79 |    136 |   291,732 |    178.12 |   583,470 |   0.99 | ever_able                |     68.50 |    0.49 | NEGMIR     |            1.96 |    2.71 | ever         |   0.30 |       67.50 |         1,891 |
| **NEGmir~that_good**                | good        |    476 |         4,559 |  9.89 |    447 |   291,732 |    441.70 |   583,470 |   0.94 | that_good                |    238.00 |    0.44 | NEGMIR     |            1.18 |    2.65 | that         |   0.27 |      209.00 |        13,423 |
| **NEGany~terribly_bright**          | bright      |    117 |        19,802 |  5.41 |    117 | 3,173,660 |    162.20 | 6,347,364 |   1.00 | terribly_bright          |     58.50 |    0.50 | NEGATED    |            2.37 |    2.61 | terribly     |   0.30 |       58.50 |         8,623 |
| **NEGmir~remotely_close**           | close       |    226 |         1,953 |  7.11 |    218 |   291,732 |    244.21 |   583,470 |   0.96 | remotely_close           |    113.00 |    0.46 | NEGMIR     |            1.41 |    2.58 | remotely     |   0.29 |      105.00 |         4,831 |
| **COM~ever_higher**                 | higher      |    130 |        10,870 |  5.64 |    129 | 3,173,552 |    168.50 | 6,347,364 |   0.99 | ever_higher              |     65.00 |    0.49 | COMPLEMENT |            1.94 |    2.52 | ever         |   0.30 |       64.00 |        12,992 |
| **NEGmir~ever_wrong**               | wrong       |    102 |         4,786 |  5.05 |    102 |   291,732 |    141.42 |   583,470 |   1.00 | ever_wrong               |     51.00 |    0.50 | NEGMIR     |            2.31 |    2.52 | ever         |   0.30 |       51.00 |         8,506 |
| **NEGany~ever_good**                | good        |    350 |        10,870 |  8.57 |    331 | 3,173,660 |    337.56 | 6,347,364 |   0.95 | ever_good                |    175.00 |    0.45 | NEGATED    |            1.23 |    2.52 | ever         |   0.28 |      156.00 |       201,244 |
| **NEGany~immediately_reachable**    | reachable   |    109 |        58,040 |  5.22 |    109 | 3,173,660 |    151.11 | 6,347,364 |   1.00 | immediately_reachable    |     54.50 |    0.50 | NEGATED    |            2.34 |    2.50 | immediately  |   0.30 |       54.50 |           350 |
| **NEGany~particularly_athletic**    | athletic    |    108 |        76,162 |  5.20 |    108 | 3,173,660 |    149.72 | 6,347,364 |   1.00 | particularly_athletic    |     54.00 |    0.50 | NEGATED    |            2.34 |    2.49 | particularly |   0.30 |       54.00 |         1,772 |
| **NEGany~particularly_likeable**    | likeable    |    106 |        76,162 |  5.15 |    106 | 3,173,660 |    146.95 | 6,347,364 |   1.00 | particularly_likeable    |     53.00 |    0.50 | NEGATED    |            2.33 |    2.46 | particularly |   0.30 |       53.00 |           861 |
| **NEGany~terribly_common**          | common      |    105 |        19,802 |  5.12 |    105 | 3,173,660 |    145.56 | 6,347,364 |   1.00 | terribly_common          |     52.50 |    0.50 | NEGATED    |            2.32 |    2.45 | terribly     |   0.30 |       52.50 |        34,450 |
| **NEGmir~particularly_original**    | original    |     90 |        10,029 |  4.74 |     90 |   291,732 |    124.78 |   583,470 |   1.00 | particularly_original    |     45.00 |    0.50 | NEGMIR     |            2.26 |    2.33 | particularly |   0.30 |       45.00 |           715 |
| **NEGany~any_nicer**                | nicer       |     96 |        16,238 |  4.90 |     96 | 3,173,660 |    133.09 | 6,347,364 |   1.00 | any_nicer                |     48.00 |    0.50 | NEGATED    |            2.29 |    2.30 | any          |   0.30 |       48.00 |           642 |
| **NEGany~remotely_funny**           | funny       |    141 |         6,161 |  5.68 |    137 | 3,173,660 |    159.09 | 6,347,364 |   0.97 | remotely_funny           |     70.50 |    0.47 | NEGATED    |            1.49 |    2.16 | remotely     |   0.29 |       66.50 |        14,992 |
| **NEGany~inherently_evil**          | evil        |    392 |         8,614 |  8.56 |    358 | 3,173,660 |    312.23 | 6,347,364 |   0.91 | inherently_evil          |    196.00 |    0.41 | NEGATED    |            1.02 |    2.12 | inherently   |   0.26 |      162.00 |         3,171 |
| **NEGmir~that_big**                 | big         |    116 |         4,559 |  5.17 |    113 |   291,732 |    132.98 |   583,470 |   0.97 | that_big                 |     58.00 |    0.47 | NEGMIR     |            1.51 |    2.08 | that         |   0.29 |       55.00 |         3,134 |
| **NEGany~particularly_radical**     | radical     |     79 |        76,162 |  4.44 |     79 | 3,173,660 |    109.52 | 6,347,364 |   1.00 | particularly_radical     |     39.50 |    0.50 | NEGATED    |            2.20 |    1.99 | particularly |   0.30 |       39.50 |         2,637 |
| **NEGany~remotely_interested**      | interested  |    364 |         6,161 |  8.15 |    330 | 3,173,660 |    278.69 | 6,347,364 |   0.91 | remotely_interested      |    182.00 |    0.41 | NEGATED    |            0.98 |    1.99 | remotely     |   0.26 |      148.00 |        34,543 |
| **NEGany~any_smarter**              | smarter     |     90 |        16,238 |  4.66 |     89 | 3,173,660 |    113.78 | 6,347,364 |   0.99 | any_smarter              |     45.00 |    0.49 | NEGATED    |            1.78 |    1.94 | any          |   0.30 |       44.00 |           733 |
| **NEGmir~terribly_surprising**      | surprising  |     67 |         2,204 |  4.09 |     67 |   291,732 |     92.89 |   583,470 |   1.00 | terribly_surprising      |     33.50 |    0.50 | NEGMIR     |            2.13 |    1.85 | terribly     |   0.30 |       33.50 |         1,248 |
| **NEGany~ever_boring**              | boring      |     72 |        10,870 |  4.24 |     72 | 3,173,660 |     99.82 | 6,347,364 |   1.00 | ever_boring              |     36.00 |    0.50 | NEGATED    |            2.16 |    1.84 | ever         |   0.30 |       36.00 |         3,840 |
| **NEGmir~inherently_bad**           | bad         |    158 |         3,342 |  5.67 |    148 |   291,732 |    144.52 |   583,470 |   0.94 | inherently_bad           |     79.00 |    0.44 | NEGMIR     |            1.15 |    1.83 | inherently   |   0.27 |       69.00 |         4,790 |
| **NEGany~immediately_certain**      | certain     |     70 |        58,040 |  4.18 |     70 | 3,173,660 |     97.04 | 6,347,364 |   1.00 | immediately_certain      |     35.00 |    0.50 | NEGATED    |            2.15 |    1.80 | immediately  |   0.30 |       35.00 |        11,334 |
| **NEGmir~that_close**               | close       |     60 |         4,559 |  3.87 |     60 |   291,732 |     83.19 |   583,470 |   1.00 | that_close               |     30.00 |    0.50 | NEGMIR     |            2.08 |    1.67 | that         |   0.30 |       30.00 |         4,831 |
| **NEGmir~any_worse**                | worse       |     90 |         1,095 |  4.50 |     87 |   291,732 |     98.47 |   583,470 |   0.97 | any_worse                |     45.00 |    0.47 | NEGMIR     |            1.40 |    1.66 | any          |   0.29 |       42.00 |         2,007 |
| **NEGany~remotely_surprising**      | surprising  |     76 |         6,161 |  4.27 |     75 | 3,173,660 |     94.71 | 6,347,364 |   0.99 | remotely_surprising      |     38.00 |    0.49 | NEGATED    |            1.70 |    1.66 | remotely     |   0.30 |       37.00 |        18,776 |
| **NEGmir~terribly_new**             | new         |     70 |         2,204 |  4.09 |     69 |   291,732 |     86.57 |   583,470 |   0.99 | terribly_new             |     35.00 |    0.49 | NEGMIR     |            1.67 |    1.64 | terribly     |   0.29 |       34.00 |         4,300 |
| **NEGany~remotely_comparable**      | comparable  |    125 |         6,161 |  5.11 |    118 | 3,173,660 |    119.34 | 6,347,364 |   0.94 | remotely_comparable      |     62.50 |    0.44 | NEGATED    |            1.20 |    1.62 | remotely     |   0.28 |       55.50 |         2,401 |
| **NEGmir~ever_black**               | black       |     56 |         4,786 |  3.74 |     56 |   291,732 |     77.64 |   583,470 |   1.00 | ever_black               |     28.00 |    0.50 | NEGMIR     |            2.05 |    1.56 | ever         |   0.30 |       28.00 |           646 |
| **NEGmir~that_popular**             | popular     |     66 |         4,559 |  3.97 |     65 |   291,732 |     81.14 |   583,470 |   0.98 | that_popular             |     33.00 |    0.48 | NEGMIR     |            1.64 |    1.54 | that         |   0.29 |       32.00 |         2,841 |
| **NEGmir~particularly_novel**       | novel       |     54 |        10,029 |  3.67 |     54 |   291,732 |     74.87 |   583,470 |   1.00 | particularly_novel       |     27.00 |    0.50 | NEGMIR     |            2.04 |    1.50 | particularly |   0.30 |       27.00 |           179 |
| **NEGany~remotely_ready**           | ready       |     58 |         6,161 |  3.81 |     58 | 3,173,660 |     80.41 | 6,347,364 |   1.00 | remotely_ready           |     29.00 |    0.50 | NEGATED    |            2.07 |    1.49 | remotely     |   0.30 |       29.00 |        29,583 |
| **NEGany~any_sweeter**              | sweeter     |     58 |        16,238 |  3.81 |     58 | 3,173,660 |     80.41 | 6,347,364 |   1.00 | any_sweeter              |     29.00 |    0.50 | NEGATED    |            2.07 |    1.49 | any          |   0.30 |       29.00 |           388 |
| **NEGmir~particularly_religious**   | religious   |     53 |        10,029 |  3.64 |     53 |   291,732 |     73.48 |   583,470 |   1.00 | particularly_religious   |     26.50 |    0.50 | NEGMIR     |            2.03 |    1.47 | particularly |   0.30 |       26.50 |           337 |
| **NEGany~inherently_better**        | better      |    158 |         8,614 |  5.42 |    144 | 3,173,660 |    124.46 | 6,347,364 |   0.91 | inherently_better        |     79.00 |    0.41 | NEGATED    |            1.00 |    1.46 | inherently   |   0.26 |       65.00 |        50,827 |
| **NEGany~particularly_flashy**      | flashy      |     57 |        76,162 |  3.77 |     57 | 3,173,660 |     79.02 | 6,347,364 |   1.00 | particularly_flashy      |     28.50 |    0.50 | NEGATED    |            2.06 |    1.46 | particularly |   0.30 |       28.50 |         1,732 |
| **NEGany~inherently_good**          | good        |    329 |         8,614 |  7.04 |    283 | 3,173,660 |    189.85 | 6,347,364 |   0.86 | inherently_good          |    164.50 |    0.36 | NEGATED    |            0.79 |    1.46 | inherently   |   0.24 |      118.50 |       201,244 |
| **NEGmir~remotely_true**            | true        |     62 |         1,953 |  3.84 |     61 |   291,732 |     75.72 |   583,470 |   0.98 | remotely_true            |     31.00 |    0.48 | NEGMIR     |            1.61 |    1.43 | remotely     |   0.29 |       30.00 |         2,850 |
| **NEGany~remotely_similar**         | similar     |    169 |         6,161 |  5.48 |    152 | 3,173,660 |    123.97 | 6,347,364 |   0.90 | remotely_similar         |     84.50 |    0.40 | NEGATED    |            0.94 |    1.39 | remotely     |   0.25 |       67.50 |        11,088 |
| **NEGany~any_brighter**             | brighter    |     64 |        16,238 |  3.91 |     63 | 3,173,660 |     78.42 | 6,347,364 |   0.98 | any_brighter             |     32.00 |    0.48 | NEGATED    |            1.63 |    1.37 | any          |   0.29 |       31.00 |           640 |
| **NEGmir~necessarily_bad**          | bad         |     50 |           992 |  3.54 |     50 |   291,732 |     69.32 |   583,470 |   1.00 | necessarily_bad          |     25.00 |    0.50 | NEGMIR     |            2.00 |    1.37 | necessarily  |   0.30 |       25.00 |         4,790 |
| **NEGmir~immediately_available**    | available   |    184 |           564 |  5.50 |    162 |   291,732 |    120.41 |   583,470 |   0.88 | immediately_available    |     92.00 |    0.38 | NEGMIR     |            0.86 |    1.34 | immediately  |   0.25 |       70.00 |         3,079 |
| **NEGmir~ever_right**               | right       |     49 |         4,786 |  3.50 |     49 |   291,732 |     67.93 |   583,470 |   1.00 | ever_right               |     24.50 |    0.50 | NEGMIR     |            2.00 |    1.33 | ever         |   0.30 |       24.50 |         2,038 |
| **NEGany~remotely_related**         | related     |    163 |         6,161 |  5.34 |    146 | 3,173,660 |    116.95 | 6,347,364 |   0.90 | remotely_related         |     81.50 |    0.40 | NEGATED    |            0.92 |    1.33 | remotely     |   0.25 |       64.50 |        14,260 |
| **COM~ever_deeper**                 | deeper      |     62 |        10,870 |  3.84 |     61 | 3,173,552 |     75.72 | 6,347,364 |   0.98 | ever_deeper              |     31.00 |    0.48 | COMPLEMENT |            1.61 |    1.31 | ever         |   0.29 |       30.00 |         1,768 |
| **NEGmir~any_different**            | different   |     48 |         1,095 |  3.46 |     48 |   291,732 |     66.55 |   583,470 |   1.00 | any_different            |     24.00 |    0.50 | NEGMIR     |            1.99 |    1.30 | any          |   0.30 |       24.00 |         8,644 |
| **NEGmir~terribly_interesting**     | interesting |     57 |         2,204 |  3.67 |     56 |   291,732 |     68.96 |   583,470 |   0.98 | terribly_interesting     |     28.50 |    0.48 | NEGMIR     |            1.58 |    1.29 | terribly     |   0.29 |       27.50 |         3,863 |
| **NEGmir~particularly_innovative**  | innovative  |     47 |        10,029 |  3.43 |     47 |   291,732 |     65.16 |   583,470 |   1.00 | particularly_innovative  |     23.50 |    0.50 | NEGMIR     |            1.98 |    1.26 | particularly |   0.30 |       23.50 |           675 |
| **NEGmir~that_interested**          | interested  |     64 |         4,559 |  3.81 |     62 |   291,732 |     70.93 |   583,470 |   0.97 | that_interested          |     32.00 |    0.47 | NEGMIR     |            1.40 |    1.26 | that         |   0.29 |       30.00 |         2,877 |
| **NEGany~inherently_illegal**       | illegal     |     60 |         8,614 |  3.78 |     59 | 3,173,660 |     73.01 | 6,347,364 |   0.98 | inherently_illegal       |     30.00 |    0.48 | NEGATED    |            1.60 |    1.26 | inherently   |   0.29 |       29.00 |         3,580 |
| **NEGmir~any_easier**               | easier      |     63 |         1,095 |  3.78 |     61 |   291,732 |     69.61 |   583,470 |   0.97 | any_easier               |     31.50 |    0.47 | NEGMIR     |            1.39 |    1.23 | any          |   0.29 |       29.50 |           681 |
| **NEGmir~terribly_original**        | original    |     45 |         2,204 |  3.35 |     45 |   291,732 |     62.39 |   583,470 |   1.00 | terribly_original        |     22.50 |    0.50 | NEGMIR     |            1.96 |    1.19 | terribly     |   0.30 |       22.50 |           715 |
| **NEGmir~that_difficult**           | difficult   |     53 |         4,559 |  3.54 |     52 |   291,732 |     63.56 |   583,470 |   0.98 | that_difficult           |     26.50 |    0.48 | NEGMIR     |            1.54 |    1.16 | that         |   0.29 |       25.50 |         4,854 |
| **NEGmir~exactly_clear**            | clear       |     53 |           869 |  3.54 |     52 |   291,732 |     63.56 |   583,470 |   0.98 | exactly_clear            |     26.50 |    0.48 | NEGMIR     |            1.54 |    1.16 | exactly      |   0.29 |       25.50 |         3,321 |
| **NEGmir~particularly_comfortable** | comfortable |     44 |        10,029 |  3.32 |     44 |   291,732 |     61.00 |   583,470 |   1.00 | particularly_comfortable |     22.00 |    0.50 | NEGMIR     |            1.95 |    1.15 | particularly |   0.30 |       22.00 |         1,888 |
| **NEGmir~remotely_comparable**      | comparable  |     44 |         1,953 |  3.32 |     44 |   291,732 |     61.00 |   583,470 |   1.00 | remotely_comparable      |     22.00 |    0.50 | NEGMIR     |            1.95 |    1.15 | remotely     |   0.30 |       22.00 |           158 |
| **NEGany~remotely_enough**          | enough      |     47 |         6,161 |  3.43 |     47 | 3,173,660 |     65.16 | 6,347,364 |   1.00 | remotely_enough          |     23.50 |    0.50 | NEGATED    |            1.98 |    1.13 | remotely     |   0.30 |       23.50 |        27,603 |
| **POS~terribly_wrong**              | wrong       |    401 |         2,204 |  6.63 |    319 |   291,729 |    149.75 |   583,470 |   0.80 | terribly_wrong           |    200.50 |    0.30 | POSMIR     |            0.59 |    1.06 | terribly     |   0.20 |      118.50 |         8,506 |
| **COM~ever_mindful**                | mindful     |     53 |        10,870 |  3.54 |     52 | 3,173,552 |     63.56 | 6,347,364 |   0.98 | ever_mindful             |     26.50 |    0.48 | COMPLEMENT |            1.54 |    1.04 | ever         |   0.29 |       25.50 |           784 |
| **NEGmir~that_happy**               | happy       |     41 |         4,559 |  3.20 |     41 |   291,732 |     56.84 |   583,470 |   1.00 | that_happy               |     20.50 |    0.50 | NEGMIR     |            1.92 |    1.03 | that         |   0.30 |       20.50 |         5,463 |




```python
nb_show_table(NEG_bigrams_sample.l1.value_counts().to_frame('subtotal in selected bigrams'))
```

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


