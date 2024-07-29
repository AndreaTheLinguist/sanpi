```python
from pathlib import Path

import pandas as pd
from am_notebooks import *

from source.utils import (HIT_TABLES_DIR, confirm_dir, print_iter,
                          timestamp_today)
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.dataframes import write_part_parquet as parq_it, catify_hit_table as catify
from source.utils.sample import sample_pickle as sp

TAG='ALL'
K=8
BK = max(K+2, 10)
BIGRAM_F_FLOOR=50 if TAG == 'ALL' else 25

ADV_F_FLOOR=5000

# METRIC_PRIORITY = ['LRC', 'P1', 'G2', 'P2'] if TAG=='NEQ' else ['dP1', 'LRC', 'G2', 'P1']
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
TAG_TOP_STR = f'{TAG}-Top{K}'
TAG_TOP_DIR = TOP_AM_TAG_DIR / TAG_TOP_STR
DATE=timestamp_today()
FOCUS_ORIG = ['f', 'E11', 'unexpected_f',
              'am_p1_given2', 'am_p1_given2_simple', 
              'am_p2_given1', 'am_p2_given1_simple', 
              'conservative_log_ratio',
              'am_log_likelihood', 
            #   't_score',
            #   'mutual_information', 'am_odds_ratio_disc',
              'N', 'f1', 'f2', 'l1', 'l2']
FOCUS = adjust_assoc_columns(FOCUS_ORIG)
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 80)
adv_am = seek_top_adv_am(DATE, ADV_F_FLOOR, TAG_TOP_STR, TAG_TOP_DIR)
adv_am
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
      <th>key_SET</th>
      <th>f_SET</th>
      <th>dP1_SET</th>
      <th>P1_SET</th>
      <th>LRC_SET</th>
      <th>G2_SET</th>
      <th>MI_SET</th>
      <th>odds_r_disc_SET</th>
      <th>t_SET</th>
      <th>N_SET</th>
      <th>...</th>
      <th>mean_t</th>
      <th>mean_N</th>
      <th>mean_f1</th>
      <th>mean_f2</th>
      <th>mean_expF</th>
      <th>mean_unexpF</th>
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
      <th>necessarily</th>
      <td>NEGany~necessarily</td>
      <td>42595</td>
      <td>0.83</td>
      <td>0.87</td>
      <td>7.10</td>
      <td>230,257.34</td>
      <td>1.30</td>
      <td>2.17</td>
      <td>196.05</td>
      <td>72839589</td>
      <td>...</td>
      <td>110.48</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>25,027.00</td>
      <td>1,161.20</td>
      <td>20,617.80</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>that</th>
      <td>NEGany~that</td>
      <td>164768</td>
      <td>0.75</td>
      <td>0.79</td>
      <td>6.34</td>
      <td>831,137.25</td>
      <td>1.26</td>
      <td>1.94</td>
      <td>383.56</td>
      <td>72839589</td>
      <td>...</td>
      <td>217.42</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>106,878.00</td>
      <td>5,007.91</td>
      <td>79,530.09</td>
      <td>0.03</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>NEGany~exactly</td>
      <td>43813</td>
      <td>0.70</td>
      <td>0.75</td>
      <td>5.94</td>
      <td>210,126.60</td>
      <td>1.23</td>
      <td>1.82</td>
      <td>197.11</td>
      <td>72839589</td>
      <td>...</td>
      <td>109.68</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>29,842.00</td>
      <td>1,366.77</td>
      <td>20,946.23</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>any</th>
      <td>NEGany~any</td>
      <td>15384</td>
      <td>0.40</td>
      <td>0.45</td>
      <td>4.07</td>
      <td>50,880.96</td>
      <td>1.01</td>
      <td>1.25</td>
      <td>111.95</td>
      <td>72839589</td>
      <td>...</td>
      <td>69.16</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>17,789.50</td>
      <td>851.61</td>
      <td>7,373.39</td>
      <td>0.07</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>NEGany~remotely</td>
      <td>5661</td>
      <td>0.30</td>
      <td>0.34</td>
      <td>3.40</td>
      <td>15,284.49</td>
      <td>0.90</td>
      <td>1.06</td>
      <td>65.73</td>
      <td>72839589</td>
      <td>...</td>
      <td>49.63</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>9,383.50</td>
      <td>558.48</td>
      <td>3,192.02</td>
      <td>0.33</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>NEGany~ever</td>
      <td>5932</td>
      <td>0.01</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>183.92</td>
      <td>0.08</td>
      <td>0.08</td>
      <td>12.49</td>
      <td>72839589</td>
      <td>...</td>
      <td>34.23</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>59,567.50</td>
      <td>2,918.83</td>
      <td>2,401.67</td>
      <td>0.79</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.04</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>NEGany~yet</td>
      <td>51867</td>
      <td>0.50</td>
      <td>0.54</td>
      <td>4.65</td>
      <td>197,610.98</td>
      <td>1.09</td>
      <td>1.42</td>
      <td>209.42</td>
      <td>72839589</td>
      <td>...</td>
      <td>109.75</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>48,289.00</td>
      <td>2,156.07</td>
      <td>23,937.43</td>
      <td>0.01</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>NEGany~immediately</td>
      <td>56099</td>
      <td>0.54</td>
      <td>0.58</td>
      <td>4.86</td>
      <td>224,059.55</td>
      <td>1.12</td>
      <td>1.49</td>
      <td>219.01</td>
      <td>72839589</td>
      <td>...</td>
      <td>114.44</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>49,084.00</td>
      <td>2,215.00</td>
      <td>26,036.00</td>
      <td>0.01</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>NEGany~particularly</td>
      <td>55527</td>
      <td>0.07</td>
      <td>0.11</td>
      <td>1.38</td>
      <td>37,272.74</td>
      <td>0.39</td>
      <td>0.43</td>
      <td>140.66</td>
      <td>72839589</td>
      <td>...</td>
      <td>106.81</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>263,335.50</td>
      <td>12,304.83</td>
      <td>20,080.17</td>
      <td>0.17</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>NEGany~inherently</td>
      <td>6743</td>
      <td>0.10</td>
      <td>0.14</td>
      <td>1.75</td>
      <td>7,022.02</td>
      <td>0.51</td>
      <td>0.56</td>
      <td>56.75</td>
      <td>72839589</td>
      <td>...</td>
      <td>46.91</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>26,468.00</td>
      <td>1,481.33</td>
      <td>3,322.17</td>
      <td>0.42</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.11</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>NEGany~terribly</td>
      <td>17949</td>
      <td>0.26</td>
      <td>0.30</td>
      <td>3.19</td>
      <td>43,741.44</td>
      <td>0.84</td>
      <td>0.98</td>
      <td>114.80</td>
      <td>72839589</td>
      <td>...</td>
      <td>67.21</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>31,787.00</td>
      <td>1,679.65</td>
      <td>8,078.35</td>
      <td>0.09</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.08</td>
    </tr>
  </tbody>
</table>
<p>11 rows × 47 columns</p>
</div>




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
adv_adj_am = adjust_assoc_columns(
    pd.read_parquet(tuple(AM_DF_DIR
                          .joinpath('adv_adj/ANYdirect/extra')
                          .glob(f'*{TAG}*min{BIGRAM_F_FLOOR}x_extra.parq'))[0], 
                    filters=[('l1', 'in', adv_list)], engine='pyarrow')
    ).filter(items=FOCUS).sort_values('LRC', ascending = False)
adv_adj_am = adv_adj_am.loc[adv_adj_am.l1.isin(adv_list), :]
nb_show_table(adv_adj_am.head(20))
```

    
    |                             |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |    `f1` |   `f2` | `l1`        | `l2`         |
    |:----------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|--------:|-------:|:------------|:-------------|
    | **remotely~detonated**      |    78 |      0.02 |       77.98 |    0.88 |   0.88 |    0.00 |   0.00 |   12.69 |  1,243.75 | 72,839,589 |  16,426 |     89 | remotely    | detonated    |
    | **yet~unborn**              |   372 |      0.68 |      371.32 |    0.72 |   0.72 |    0.00 |   0.00 |   10.14 |  4,319.00 | 72,839,589 |  95,763 |    519 | yet         | unborn       |
    | **inherently~governmental** |   253 |      0.50 |      252.50 |    0.33 |   0.33 |    0.01 |   0.01 |    8.92 |  2,742.59 | 72,839,589 |  47,803 |    761 | inherently  | governmental |
    | **remotely~exploitable**    |   145 |      0.22 |      144.78 |    0.15 |   0.15 |    0.01 |   0.01 |    8.79 |  1,613.38 | 72,839,589 |  16,426 |    986 | remotely    | exploitable  |
    | **immediately~accretive**   |   236 |      0.70 |      235.30 |    0.45 |   0.45 |    0.00 |   0.00 |    8.54 |  2,406.67 | 72,839,589 |  96,973 |    523 | immediately | accretive    |
    | **exactly~alike**           | 2,768 |      9.16 |    2,758.84 |    0.24 |   0.24 |    0.05 |   0.05 |    8.46 | 26,963.38 | 72,839,589 |  58,643 | 11,375 | exactly     | alike        |
    | **that~purported**          |    73 |      0.27 |       72.73 |    0.78 |   0.78 |    0.00 |   0.00 |    8.42 |    758.47 | 72,839,589 | 208,262 |     93 | that        | purported    |
    | **immediately~appealable**  |    76 |      0.19 |       75.81 |    0.55 |   0.55 |    0.00 |   0.00 |    8.41 |    815.23 | 72,839,589 |  96,973 |    139 | immediately | appealable   |
    | **immediately~adjacent**    | 1,595 |      6.33 |    1,588.67 |    0.33 |   0.34 |    0.02 |   0.02 |    8.31 | 15,089.64 | 72,839,589 |  96,973 |  4,756 | immediately | adjacent     |
    | **yet~unnamed**             |   736 |      2.77 |      733.23 |    0.35 |   0.35 |    0.01 |   0.01 |    8.29 |  7,048.15 | 72,839,589 |  95,763 |  2,107 | yet         | unnamed      |
    | **ever~olympic**            |   218 |      0.77 |      217.23 |    0.44 |   0.44 |    0.00 |   0.00 |    8.23 |  2,141.80 | 72,839,589 | 114,075 |    492 | ever        | olympic      |
    | **ever~quarterly**          |   137 |      0.48 |      136.52 |    0.45 |   0.45 |    0.00 |   0.00 |    8.05 |  1,349.65 | 72,839,589 | 114,075 |    306 | ever        | quarterly    |
    | **necessarily~indicative**  | 1,400 |      5.48 |    1,394.52 |    0.17 |   0.17 |    0.03 |   0.03 |    8.03 | 13,028.00 | 72,839,589 |  48,947 |  8,148 | necessarily | indicative   |
    | **terribly~awry**           |   180 |      0.56 |      179.44 |    0.26 |   0.26 |    0.00 |   0.00 |    8.02 |  1,770.97 | 72,839,589 |  58,964 |    692 | terribly    | awry         |
    | **yet~unspecified**         |   204 |      0.80 |      203.20 |    0.33 |   0.34 |    0.00 |   0.00 |    7.86 |  1,933.20 | 72,839,589 |  95,763 |    607 | yet         | unspecified  |
    | **yet~undetermined**        |   297 |      1.45 |      295.55 |    0.27 |   0.27 |    0.00 |   0.00 |    7.55 |  2,658.03 | 72,839,589 |  95,763 |  1,104 | yet         | undetermined |
    | **yet~untitled**            |   121 |      0.54 |      120.46 |    0.29 |   0.29 |    0.00 |   0.00 |    7.37 |  1,107.51 | 72,839,589 |  95,763 |    412 | yet         | untitled     |
    | **ever~watchful**           |   416 |      2.92 |      413.08 |    0.22 |   0.22 |    0.00 |   0.00 |    7.05 |  3,399.87 | 72,839,589 | 114,075 |  1,866 | ever        | watchful     |
    | **yet~unidentified**        |   336 |      2.48 |      333.52 |    0.18 |   0.18 |    0.00 |   0.00 |    6.85 |  2,694.33 | 72,839,589 |  95,763 |  1,890 | yet         | unidentified |
    | **any~happier**             |   963 |      7.84 |      955.16 |    0.06 |   0.06 |    0.03 |   0.03 |    6.75 |  7,438.55 | 72,839,589 |  34,382 | 16,606 | any         | happier      |
    



|                             |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |    `f1` |   `f2` | `l1`        | `l2`         |
|:----------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|--------:|-------:|:------------|:-------------|
| **remotely~detonated**      |    78 |      0.02 |       77.98 |    0.88 |   0.88 |    0.00 |   0.00 |   12.69 |  1,243.75 | 72,839,589 |  16,426 |     89 | remotely    | detonated    |
| **yet~unborn**              |   372 |      0.68 |      371.32 |    0.72 |   0.72 |    0.00 |   0.00 |   10.14 |  4,319.00 | 72,839,589 |  95,763 |    519 | yet         | unborn       |
| **inherently~governmental** |   253 |      0.50 |      252.50 |    0.33 |   0.33 |    0.01 |   0.01 |    8.92 |  2,742.59 | 72,839,589 |  47,803 |    761 | inherently  | governmental |
| **remotely~exploitable**    |   145 |      0.22 |      144.78 |    0.15 |   0.15 |    0.01 |   0.01 |    8.79 |  1,613.38 | 72,839,589 |  16,426 |    986 | remotely    | exploitable  |
| **immediately~accretive**   |   236 |      0.70 |      235.30 |    0.45 |   0.45 |    0.00 |   0.00 |    8.54 |  2,406.67 | 72,839,589 |  96,973 |    523 | immediately | accretive    |
| **exactly~alike**           | 2,768 |      9.16 |    2,758.84 |    0.24 |   0.24 |    0.05 |   0.05 |    8.46 | 26,963.38 | 72,839,589 |  58,643 | 11,375 | exactly     | alike        |
| **that~purported**          |    73 |      0.27 |       72.73 |    0.78 |   0.78 |    0.00 |   0.00 |    8.42 |    758.47 | 72,839,589 | 208,262 |     93 | that        | purported    |
| **immediately~appealable**  |    76 |      0.19 |       75.81 |    0.55 |   0.55 |    0.00 |   0.00 |    8.41 |    815.23 | 72,839,589 |  96,973 |    139 | immediately | appealable   |
| **immediately~adjacent**    | 1,595 |      6.33 |    1,588.67 |    0.33 |   0.34 |    0.02 |   0.02 |    8.31 | 15,089.64 | 72,839,589 |  96,973 |  4,756 | immediately | adjacent     |
| **yet~unnamed**             |   736 |      2.77 |      733.23 |    0.35 |   0.35 |    0.01 |   0.01 |    8.29 |  7,048.15 | 72,839,589 |  95,763 |  2,107 | yet         | unnamed      |
| **ever~olympic**            |   218 |      0.77 |      217.23 |    0.44 |   0.44 |    0.00 |   0.00 |    8.23 |  2,141.80 | 72,839,589 | 114,075 |    492 | ever        | olympic      |
| **ever~quarterly**          |   137 |      0.48 |      136.52 |    0.45 |   0.45 |    0.00 |   0.00 |    8.05 |  1,349.65 | 72,839,589 | 114,075 |    306 | ever        | quarterly    |
| **necessarily~indicative**  | 1,400 |      5.48 |    1,394.52 |    0.17 |   0.17 |    0.03 |   0.03 |    8.03 | 13,028.00 | 72,839,589 |  48,947 |  8,148 | necessarily | indicative   |
| **terribly~awry**           |   180 |      0.56 |      179.44 |    0.26 |   0.26 |    0.00 |   0.00 |    8.02 |  1,770.97 | 72,839,589 |  58,964 |    692 | terribly    | awry         |
| **yet~unspecified**         |   204 |      0.80 |      203.20 |    0.33 |   0.34 |    0.00 |   0.00 |    7.86 |  1,933.20 | 72,839,589 |  95,763 |    607 | yet         | unspecified  |
| **yet~undetermined**        |   297 |      1.45 |      295.55 |    0.27 |   0.27 |    0.00 |   0.00 |    7.55 |  2,658.03 | 72,839,589 |  95,763 |  1,104 | yet         | undetermined |
| **yet~untitled**            |   121 |      0.54 |      120.46 |    0.29 |   0.29 |    0.00 |   0.00 |    7.37 |  1,107.51 | 72,839,589 |  95,763 |    412 | yet         | untitled     |
| **ever~watchful**           |   416 |      2.92 |      413.08 |    0.22 |   0.22 |    0.00 |   0.00 |    7.05 |  3,399.87 | 72,839,589 | 114,075 |  1,866 | ever        | watchful     |
| **yet~unidentified**        |   336 |      2.48 |      333.52 |    0.18 |   0.18 |    0.00 |   0.00 |    6.85 |  2,694.33 | 72,839,589 |  95,763 |  1,890 | yet         | unidentified |
| **any~happier**             |   963 |      7.84 |      955.16 |    0.06 |   0.06 |    0.03 |   0.03 |    6.75 |  7,438.55 | 72,839,589 |  34,382 | 16,606 | any         | happier      |




```python
adv_adj_am
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
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>dP1</th>
      <th>P1</th>
      <th>dP2</th>
      <th>P2</th>
      <th>LRC</th>
      <th>G2</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>l1</th>
      <th>l2</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>remotely~detonated</th>
      <td>78</td>
      <td>0.02</td>
      <td>77.98</td>
      <td>0.88</td>
      <td>0.88</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>12.69</td>
      <td>1,243.75</td>
      <td>72839589</td>
      <td>16426</td>
      <td>89</td>
      <td>remotely</td>
      <td>detonated</td>
    </tr>
    <tr>
      <th>yet~unborn</th>
      <td>372</td>
      <td>0.68</td>
      <td>371.32</td>
      <td>0.72</td>
      <td>0.72</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>10.14</td>
      <td>4,319.00</td>
      <td>72839589</td>
      <td>95763</td>
      <td>519</td>
      <td>yet</td>
      <td>unborn</td>
    </tr>
    <tr>
      <th>inherently~governmental</th>
      <td>253</td>
      <td>0.50</td>
      <td>252.50</td>
      <td>0.33</td>
      <td>0.33</td>
      <td>0.01</td>
      <td>0.01</td>
      <td>8.92</td>
      <td>2,742.59</td>
      <td>72839589</td>
      <td>47803</td>
      <td>761</td>
      <td>inherently</td>
      <td>governmental</td>
    </tr>
    <tr>
      <th>remotely~exploitable</th>
      <td>145</td>
      <td>0.22</td>
      <td>144.78</td>
      <td>0.15</td>
      <td>0.15</td>
      <td>0.01</td>
      <td>0.01</td>
      <td>8.79</td>
      <td>1,613.38</td>
      <td>72839589</td>
      <td>16426</td>
      <td>986</td>
      <td>remotely</td>
      <td>exploitable</td>
    </tr>
    <tr>
      <th>immediately~accretive</th>
      <td>236</td>
      <td>0.70</td>
      <td>235.30</td>
      <td>0.45</td>
      <td>0.45</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>8.54</td>
      <td>2,406.67</td>
      <td>72839589</td>
      <td>96973</td>
      <td>523</td>
      <td>immediately</td>
      <td>accretive</td>
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
    </tr>
    <tr>
      <th>yet~important</th>
      <td>67</td>
      <td>2,651.33</td>
      <td>-2,584.33</td>
      <td>-0.00</td>
      <td>0.00</td>
      <td>-0.03</td>
      <td>0.00</td>
      <td>-4.41</td>
      <td>-4,750.28</td>
      <td>72839589</td>
      <td>95763</td>
      <td>2016665</td>
      <td>yet</td>
      <td>important</td>
    </tr>
    <tr>
      <th>particularly~little</th>
      <td>50</td>
      <td>2,992.44</td>
      <td>-2,942.44</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-4.88</td>
      <td>-5,513.23</td>
      <td>72839589</td>
      <td>513668</td>
      <td>424336</td>
      <td>particularly</td>
      <td>little</td>
    </tr>
    <tr>
      <th>particularly~better</th>
      <td>56</td>
      <td>4,412.70</td>
      <td>-4,356.70</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-5.33</td>
      <td>-8,292.21</td>
      <td>72839589</td>
      <td>513668</td>
      <td>625733</td>
      <td>particularly</td>
      <td>better</td>
    </tr>
    <tr>
      <th>particularly~more</th>
      <td>54</td>
      <td>6,372.60</td>
      <td>-6,318.60</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-5.90</td>
      <td>-12,245.28</td>
      <td>72839589</td>
      <td>513668</td>
      <td>903653</td>
      <td>particularly</td>
      <td>more</td>
    </tr>
    <tr>
      <th>particularly~many</th>
      <td>79</td>
      <td>13,037.28</td>
      <td>-12,958.28</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.03</td>
      <td>0.00</td>
      <td>-6.54</td>
      <td>-25,535.98</td>
      <td>72839589</td>
      <td>513668</td>
      <td>1848723</td>
      <td>particularly</td>
      <td>many</td>
    </tr>
  </tbody>
</table>
<p>2531 rows × 14 columns</p>
</div>




```python
def load_hit_table(adv_set, pos_hits, neg_hits):

    out_path = TAG_TOP_DIR.joinpath(
        f'{TAG_TOP_STR}adv_sample-hits_{timestamp_today()}.parq')
    if not out_path.exists():

        dfs = []
        for p in (pos_hits, neg_hits):
            _df = pd.read_parquet(p, engine='pyarrow', filters=[
                                  ('adv_form_lower', 'in', adv_set)])
            _df = _df.drop_duplicates('text_window').filter(
                regex=r'token_str|text_window|bigram_lower|adv_form_lower|adj_form_lower')
            dfs.append(_df)
        hit_df = catify(pd.concat(dfs).drop_duplicates('text_window'))
        parq_it(hit_df,
                data_label='Sample of bigram tokens',
                part=f'{TAG_TOP_STR}[{ADV_F_FLOOR}]',
                out_path=out_path,
                partition_by=['adv_form_lower'])
    else:
        hit_df = pd.read_parquet(
            out_path, engine='pyarrow',
            filters=[('adv_form_lower', 'in', adv_set)])
        hit_df = catify(
            hit_df
            .drop_duplicates('text_window').filter(
                regex=r'token_str|text_window|bigram_lower|adv_form_lower|adj_form_lower'))

    return hit_df


hits_df = load_hit_table(
    adv_list, pos_hits=POS_HITS_PATH, neg_hits=NEG_HITS_PATH)
hits_df
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
      <th>token_str</th>
      <th>adj_form_lower</th>
      <th>bigram_lower</th>
      <th>adv_form_lower</th>
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
      <th>pcc_eng_25_015.3669_x0232284_401:22-23</th>
      <td>no words that would make her angst any easier to handle .</td>
      <td>All I could do was hold her in my arms , for there were no words that would ...</td>
      <td>easier</td>
      <td>any_easier</td>
      <td>any</td>
    </tr>
    <tr>
      <th>pcc_eng_25_016.2726_x0246852_05:38-39</th>
      <td>of scientific evidence that robotic surgery is any better than conventional ...</td>
      <td>An estimated four in 10 hospital websites in the United States publicize the...</td>
      <td>better</td>
      <td>any_better</td>
      <td>any</td>
    </tr>
    <tr>
      <th>pcc_eng_25_010.0104_x0145927_55:32-33</th>
      <td>and how what he is doing is any better .</td>
      <td>I would ask your brother why he want 's to make women feel the same way your...</td>
      <td>better</td>
      <td>any_better</td>
      <td>any</td>
    </tr>
    <tr>
      <th>pcc_eng_25_010.5850_x0155172_2:31-32</th>
      <td>rangoli on west 11th ( is vij`s any better ? ) to name a few</td>
      <td>Crowded restaurants seem more trouble than their worth for me : Congee Noodl...</td>
      <td>better</td>
      <td>any_better</td>
      <td>any</td>
    </tr>
    <tr>
      <th>pcc_eng_25_011.0262_x0162244_42:32-33</th>
      <td>going to help him do it correctly any better than him reminding himself ?</td>
      <td>You can be nice about this , but be clear that if he 's the one doing the ta...</td>
      <td>better</td>
      <td>any_better</td>
      <td>any</td>
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
      <th>pcc_eng_25_014.8310_x0223676_03:51-52</th>
      <td>the models for the are we x yet snowclone ( the children 's question "</td>
      <td>On Language Log , we 've had " Am I empathetic yet ? " on 1/20/07 ; " Are we...</td>
      <td>snowclone</td>
      <td>yet_snowclone</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_25_014.8775_x0224415_25:09-10</th>
      <td>envoy from a european country , as yet undecided on how it will vote ,</td>
      <td>One envoy from a European country , as yet undecided on how it will vote , s...</td>
      <td>undecided</td>
      <td>yet_undecided</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_25_015.0160_x0226639_013:12-13</th>
      <td>is that , although he is as yet unslated to perform at the fest ,</td>
      <td>But the better news is that , although he is as yet unslated to perform at t...</td>
      <td>unslated</td>
      <td>yet_unslated</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_25_015.0963_x0227920_20:16-17</th>
      <td>thousands of successful , contented former homosexuals yet unable or unwilli...</td>
      <td>With ex-gay advocates like Exodus and NARTH boasting thousands of successful...</td>
      <td>unable</td>
      <td>yet_unable</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_25_015.2248_x0229979_07:15-16</th>
      <td>smith 's escape , but it was yet unknown whether it would include special pa...</td>
      <td>A ministerial inquiry was launched to probe Smith 's escape , but it was yet...</td>
      <td>unknown</td>
      <td>yet_unknown</td>
      <td>yet</td>
    </tr>
  </tbody>
</table>
<p>283772 rows × 5 columns</p>
</div>



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
> "/share/compling/projects/sanpi/results/top_AM/ALL/ALL-Top8/ALL-Top8adv_sample-hits_2024-07-29.parq"
* Total time to write partitioned parquet ⇾  `00:00:00.113`



```python
# nb_show_table(hits_df.sort_index(axis=1).sample(13).iloc[:, :4])
```

```python
nb_show_table(hits_df.sort_index(axis=1).sample(13).iloc[:, :4])
```

|                                               | `adj_form_lower` | `adv_form_lower` | `bigrlower`             | `text_window`                                                                                     |
|:----------------------------------------------|:-----------------|:-----------------|:------------------------|:--------------------------------------------------------------------------------------------------|
| **pcc_eng_26_068.6567_x1093885_3:5-6**        | popular          | ever             | ever_popular            | spacious mid terrace in ever popular location                                                     |
| **pcc_eng_28_027.3336_x0425352_21:4-5-6**     | hea              | necessarily      | necessarily_hea         | the end is not necessarily hea , but it 's a solid                                                |
| **nyt_eng_19950702_0006_49:8-9**              | ugly             | particularly     | particularly_ugly       | he 'll make a face after a particularly ugly swing .                                              |
| **pcc_eng_24_010.6893_x0156421_04:12-13**     | effective        | particularly     | particularly_effective  | analog to album pre-sales , and are particularly effective for streaming fans who may have        |
| **nyt_eng_19960708_0547_13:26-27-28**         | addictive        | necessarily      | necessarily_addictive   | and -rrb- `` says cigarettes are n't necessarily addictive ; some say milk is bad                 |
| **nyt_eng_20040127_0066_8:25-26**             | disturbing       | particularly     | particularly_disturbing | police department employees , but it is particularly disturbing when it involves a scientist who  |
| **pcc_eng_25_007.0915_x0098850_12:14-15-16**  | useful           | particularly     | particularly_useful     | value and blog traffic but are not particularly useful for true leaders , who invent              |
| **pcc_eng_14_041.1082_x0648041_080:08-09-10** | unique           | exactly          | exactly_unique          | award - winning development project is not exactly unique .                                       |
| **pcc_eng_00_050.2537_x0795891_224:10-11**    | concerned        | particularly     | particularly_concerned  | light of climate change , i am particularly concerned about the power that corporations have      |
| **pcc_eng_22_077.2483_x1232367_62:4-5**       | true             | particularly     | particularly_true       | that could prove particularly true for " black ops . "                                            |
| **nyt_eng_20060308_0284_27:4-5-6**            | different        | that             | that_different          | `` it 's not that different from playing shortstop . ''                                           |
| **nyt_eng_20070425_0212_10:1-2-3**            | wrong            | necessarily      | necessarily_wrong       | nothing necessarily wrong with that .                                                             |
| **pcc_eng_07_027.5704_x0429654_14:27-28**     | vulnerable       | particularly     | particularly_vulnerable | to construct sewers and reduce flooding in particularly vulnerable areas in the borough of queens |



## Set adverb and collect specific values


```python
def collect_examples(amdf, 
                     hits_df, 
                     adv: str = 'exactly', 
                     n_bigrams: int = BK, 
                     n_examples: int = 50, 
                     metric: str = 'LRC') -> dict:
    df = amdf.copy().filter(like=adv, axis=0).nlargest(n_bigrams, metric)
    examples = {}
    for i, adj in enumerate(df['l2'].unique(), start=1):
        bigram = f'{adv}_{adj}'
        print(f'\n{i}. {bigram}')
        examples[bigram] = sp(
            data=hits_df, print_sample=False, 
            sample_size=n_examples, quiet=True,
            filters=[f'bigram_lower=={bigram}'],
            columns=['bigram_lower', 'text_window', 'token_str'])
        print('   > ', examples[bigram].sample(1).token_str.squeeze())
    return examples
```


```python
def sample_adv_bigrams(adverb, am_df, hits_df):
    print(f'\n## *{adverb}*\n')
    output_dir = TOP_AM_DIR / 'any_bigram_examples' / adverb
    confirm_dir(output_dir)
    
    this_adv_am = am_df.filter(like=adverb, axis=0).nlargest(BK, 'LRC')
    table_csv_path = output_dir / f'{TAG}-{adverb}_top{BK}-bigrams_AMscores_{timestamp_today()}.csv'
    this_adv_am.to_csv(table_csv_path)
    nb_show_table(this_adv_am, n_dec=2, outpath=table_csv_path.with_suffix('.md'))
    
    examples = collect_examples(this_adv_am, hits_df, adv=adverb, metric='LRC')
    

    print(f'\nSaving Samples in {output_dir}/...')
    paths = []
    for key, df in examples.items(): 
        out_path = output_dir.joinpath(f'{key}_50ex.csv')
        df.to_csv(out_path)
        paths.append(out_path)
    print_iter(paths, header='\nSamples saved as...', bullet='+')
    

```


```python
adv_am
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
      <th>key_SET</th>
      <th>f_SET</th>
      <th>dP1_SET</th>
      <th>P1_SET</th>
      <th>LRC_SET</th>
      <th>G2_SET</th>
      <th>MI_SET</th>
      <th>odds_r_disc_SET</th>
      <th>t_SET</th>
      <th>N_SET</th>
      <th>...</th>
      <th>mean_t</th>
      <th>mean_N</th>
      <th>mean_f1</th>
      <th>mean_f2</th>
      <th>mean_expF</th>
      <th>mean_unexpF</th>
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
      <th>necessarily</th>
      <td>NEGany~necessarily</td>
      <td>42595</td>
      <td>0.83</td>
      <td>0.87</td>
      <td>7.10</td>
      <td>230,257.34</td>
      <td>1.30</td>
      <td>2.17</td>
      <td>196.05</td>
      <td>72839589</td>
      <td>...</td>
      <td>110.48</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>25,027.00</td>
      <td>1,161.20</td>
      <td>20,617.80</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>that</th>
      <td>NEGany~that</td>
      <td>164768</td>
      <td>0.75</td>
      <td>0.79</td>
      <td>6.34</td>
      <td>831,137.25</td>
      <td>1.26</td>
      <td>1.94</td>
      <td>383.56</td>
      <td>72839589</td>
      <td>...</td>
      <td>217.42</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>106,878.00</td>
      <td>5,007.91</td>
      <td>79,530.09</td>
      <td>0.03</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>NEGany~exactly</td>
      <td>43813</td>
      <td>0.70</td>
      <td>0.75</td>
      <td>5.94</td>
      <td>210,126.60</td>
      <td>1.23</td>
      <td>1.82</td>
      <td>197.11</td>
      <td>72839589</td>
      <td>...</td>
      <td>109.68</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>29,842.00</td>
      <td>1,366.77</td>
      <td>20,946.23</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.02</td>
    </tr>
    <tr>
      <th>any</th>
      <td>NEGany~any</td>
      <td>15384</td>
      <td>0.40</td>
      <td>0.45</td>
      <td>4.07</td>
      <td>50,880.96</td>
      <td>1.01</td>
      <td>1.25</td>
      <td>111.95</td>
      <td>72839589</td>
      <td>...</td>
      <td>69.16</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>17,789.50</td>
      <td>851.61</td>
      <td>7,373.39</td>
      <td>0.07</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>NEGany~remotely</td>
      <td>5661</td>
      <td>0.30</td>
      <td>0.34</td>
      <td>3.40</td>
      <td>15,284.49</td>
      <td>0.90</td>
      <td>1.06</td>
      <td>65.73</td>
      <td>72839589</td>
      <td>...</td>
      <td>49.63</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>9,383.50</td>
      <td>558.48</td>
      <td>3,192.02</td>
      <td>0.33</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.14</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>NEGany~ever</td>
      <td>5932</td>
      <td>0.01</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>183.92</td>
      <td>0.08</td>
      <td>0.08</td>
      <td>12.49</td>
      <td>72839589</td>
      <td>...</td>
      <td>34.23</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>59,567.50</td>
      <td>2,918.83</td>
      <td>2,401.67</td>
      <td>0.79</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.04</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>NEGany~yet</td>
      <td>51867</td>
      <td>0.50</td>
      <td>0.54</td>
      <td>4.65</td>
      <td>197,610.98</td>
      <td>1.09</td>
      <td>1.42</td>
      <td>209.42</td>
      <td>72839589</td>
      <td>...</td>
      <td>109.75</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>48,289.00</td>
      <td>2,156.07</td>
      <td>23,937.43</td>
      <td>0.01</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>NEGany~immediately</td>
      <td>56099</td>
      <td>0.54</td>
      <td>0.58</td>
      <td>4.86</td>
      <td>224,059.55</td>
      <td>1.12</td>
      <td>1.49</td>
      <td>219.01</td>
      <td>72839589</td>
      <td>...</td>
      <td>114.44</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>49,084.00</td>
      <td>2,215.00</td>
      <td>26,036.00</td>
      <td>0.01</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.01</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>NEGany~particularly</td>
      <td>55527</td>
      <td>0.07</td>
      <td>0.11</td>
      <td>1.38</td>
      <td>37,272.74</td>
      <td>0.39</td>
      <td>0.43</td>
      <td>140.66</td>
      <td>72839589</td>
      <td>...</td>
      <td>106.81</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>263,335.50</td>
      <td>12,304.83</td>
      <td>20,080.17</td>
      <td>0.17</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.03</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>NEGany~inherently</td>
      <td>6743</td>
      <td>0.10</td>
      <td>0.14</td>
      <td>1.75</td>
      <td>7,022.02</td>
      <td>0.51</td>
      <td>0.56</td>
      <td>56.75</td>
      <td>72839589</td>
      <td>...</td>
      <td>46.91</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>26,468.00</td>
      <td>1,481.33</td>
      <td>3,322.17</td>
      <td>0.42</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.11</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>NEGany~terribly</td>
      <td>17949</td>
      <td>0.26</td>
      <td>0.30</td>
      <td>3.19</td>
      <td>43,741.44</td>
      <td>0.84</td>
      <td>0.98</td>
      <td>114.80</td>
      <td>72839589</td>
      <td>...</td>
      <td>67.21</td>
      <td>37270759</td>
      <td>1732696</td>
      <td>31,787.00</td>
      <td>1,679.65</td>
      <td>8,078.35</td>
      <td>0.09</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.08</td>
    </tr>
  </tbody>
</table>
<p>11 rows × 47 columns</p>
</div>




```python
adv_adj_am
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
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>dP1</th>
      <th>P1</th>
      <th>dP2</th>
      <th>P2</th>
      <th>LRC</th>
      <th>G2</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>l1</th>
      <th>l2</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>remotely~detonated</th>
      <td>78</td>
      <td>0.02</td>
      <td>77.98</td>
      <td>0.88</td>
      <td>0.88</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>12.69</td>
      <td>1,243.75</td>
      <td>72839589</td>
      <td>16426</td>
      <td>89</td>
      <td>remotely</td>
      <td>detonated</td>
    </tr>
    <tr>
      <th>yet~unborn</th>
      <td>372</td>
      <td>0.68</td>
      <td>371.32</td>
      <td>0.72</td>
      <td>0.72</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>10.14</td>
      <td>4,319.00</td>
      <td>72839589</td>
      <td>95763</td>
      <td>519</td>
      <td>yet</td>
      <td>unborn</td>
    </tr>
    <tr>
      <th>inherently~governmental</th>
      <td>253</td>
      <td>0.50</td>
      <td>252.50</td>
      <td>0.33</td>
      <td>0.33</td>
      <td>0.01</td>
      <td>0.01</td>
      <td>8.92</td>
      <td>2,742.59</td>
      <td>72839589</td>
      <td>47803</td>
      <td>761</td>
      <td>inherently</td>
      <td>governmental</td>
    </tr>
    <tr>
      <th>remotely~exploitable</th>
      <td>145</td>
      <td>0.22</td>
      <td>144.78</td>
      <td>0.15</td>
      <td>0.15</td>
      <td>0.01</td>
      <td>0.01</td>
      <td>8.79</td>
      <td>1,613.38</td>
      <td>72839589</td>
      <td>16426</td>
      <td>986</td>
      <td>remotely</td>
      <td>exploitable</td>
    </tr>
    <tr>
      <th>immediately~accretive</th>
      <td>236</td>
      <td>0.70</td>
      <td>235.30</td>
      <td>0.45</td>
      <td>0.45</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>8.54</td>
      <td>2,406.67</td>
      <td>72839589</td>
      <td>96973</td>
      <td>523</td>
      <td>immediately</td>
      <td>accretive</td>
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
    </tr>
    <tr>
      <th>yet~important</th>
      <td>67</td>
      <td>2,651.33</td>
      <td>-2,584.33</td>
      <td>-0.00</td>
      <td>0.00</td>
      <td>-0.03</td>
      <td>0.00</td>
      <td>-4.41</td>
      <td>-4,750.28</td>
      <td>72839589</td>
      <td>95763</td>
      <td>2016665</td>
      <td>yet</td>
      <td>important</td>
    </tr>
    <tr>
      <th>particularly~little</th>
      <td>50</td>
      <td>2,992.44</td>
      <td>-2,942.44</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-4.88</td>
      <td>-5,513.23</td>
      <td>72839589</td>
      <td>513668</td>
      <td>424336</td>
      <td>particularly</td>
      <td>little</td>
    </tr>
    <tr>
      <th>particularly~better</th>
      <td>56</td>
      <td>4,412.70</td>
      <td>-4,356.70</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-5.33</td>
      <td>-8,292.21</td>
      <td>72839589</td>
      <td>513668</td>
      <td>625733</td>
      <td>particularly</td>
      <td>better</td>
    </tr>
    <tr>
      <th>particularly~more</th>
      <td>54</td>
      <td>6,372.60</td>
      <td>-6,318.60</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-5.90</td>
      <td>-12,245.28</td>
      <td>72839589</td>
      <td>513668</td>
      <td>903653</td>
      <td>particularly</td>
      <td>more</td>
    </tr>
    <tr>
      <th>particularly~many</th>
      <td>79</td>
      <td>13,037.28</td>
      <td>-12,958.28</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.03</td>
      <td>0.00</td>
      <td>-6.54</td>
      <td>-25,535.98</td>
      <td>72839589</td>
      <td>513668</td>
      <td>1848723</td>
      <td>particularly</td>
      <td>many</td>
    </tr>
  </tbody>
</table>
<p>2531 rows × 14 columns</p>
</div>




```python
# for adverb in adv_am.index: 
#     sample_adv_bigrams(adverb, adv_adj_am, hits_df)
```

```python
for adverb in adv_am.index: 
    sample_adv_bigrams(adverb, adv_adj_am, hits_df)
```

## *necessarily*


|                                |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`        | `l2`           |
|:-------------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|-------:|--------:|:------------|:---------------|
| **necessarily~indicative**     | 1,400 |      5.48 |    1,394.52 |    0.17 |   0.17 |    0.03 |   0.03 |    8.03 | 13,028.00 | 72,839,589 | 48,947 |   8,148 | necessarily | indicative     |
| **necessarily~cause**          |    52 |      0.50 |       51.50 |    0.07 |   0.07 |    0.00 |   0.00 |    5.46 |    383.88 | 72,839,589 | 48,947 |     743 | necessarily | cause          |
| **necessarily~representative** |   492 |     12.33 |      479.67 |    0.03 |   0.03 |    0.01 |   0.01 |    4.97 |  2,685.16 | 72,839,589 | 48,947 |  18,355 | necessarily | representative |
| **necessarily~true**           | 3,460 |    155.66 |    3,304.34 |    0.01 |   0.01 |    0.07 |   0.07 |    4.35 | 15,129.32 | 72,839,589 | 48,947 | 231,639 | necessarily | true           |
| **necessarily~synonymous**     |   167 |      5.54 |      161.46 |    0.02 |   0.02 |    0.00 |   0.00 |    4.25 |    818.37 | 72,839,589 | 48,947 |   8,245 | necessarily | synonymous     |
| **necessarily~incompatible**   |   112 |      3.58 |      108.42 |    0.02 |   0.02 |    0.00 |   0.00 |    4.14 |    556.70 | 72,839,589 | 48,947 |   5,332 | necessarily | incompatible   |
| **necessarily~reflective**     |   183 |      7.55 |      175.45 |    0.02 |   0.02 |    0.00 |   0.00 |    3.97 |    819.22 | 72,839,589 | 48,947 |  11,237 | necessarily | reflective     |
| **necessarily~predictive**     |    58 |      1.63 |       56.37 |    0.02 |   0.02 |    0.00 |   0.00 |    3.95 |    303.20 | 72,839,589 | 48,947 |   2,421 | necessarily | predictive     |
| **necessarily~incomplete**     |   124 |      5.13 |      118.87 |    0.02 |   0.02 |    0.00 |   0.00 |    3.81 |    554.34 | 72,839,589 | 48,947 |   7,634 | necessarily | incomplete     |
| **necessarily~evil**           |   224 |     15.26 |      208.74 |    0.01 |   0.01 |    0.00 |   0.00 |    3.30 |    788.90 | 72,839,589 | 48,947 |  22,706 | necessarily | evil           |


1. necessarily_indicative
   >  While these lows do n't occur like clockwork every four years , and past performance is not necessarily indicative of future results , the historical record is rather impressive .

2. necessarily_cause
   >  This is not necessarily cause for alarm .

3. necessarily_representative
   >  Let 's just be clear : what some " Mormon Apologists " write is not necessarily representative of what most " Mormons " think or believe .

4. necessarily_true
   >  " I must finally conclude that this proposition , I am , I exist , is necessarily true whenever it is put forward by me or conceived in my mind . " -

5. necessarily_synonymous
   >  And this discussion always seems to come back to what we find attractive and appealing , instead of what we know to be healthy ( which research shows is not necessarily synonymous with thin ) .

6. necessarily_incompatible
   >  The philosophies of habits and intensity are n't necessarily incompatible .

7. necessarily_reflective
   >  After reading a novel by Adichie , I feel more educated and more aware of the fact that my way of viewing the world is incomplete and not necessarily reflective of everyone 's experiences .

8. necessarily_predictive
   >  There are varying degrees of offensive prowess sprinkled throughout the list of the hardest-hitters in baseball , so it is n't necessarily predictive of anything other than solid-average offense - but it 's a good sign nevertheless .

9. necessarily_incomplete
   >  The TPC 's analysis is necessarily incomplete ; it considers only the rate reductions Romney has made public and not the tax preferences that he has said he will eliminate but has n't yet identified .

10. necessarily_evil
   >  Vampires are n't necessarily evil .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_indicative_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_cause_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_representative_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_true_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_synonymous_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_incompatible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_reflective_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_predictive_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_incomplete_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_evil_50ex.csv

## *that*


|                     |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |    `f1` |    `f2` | `l1`   | `l2`       |
|:--------------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|--------:|--------:|:-------|:-----------|
| **that~purported**  |     73 |      0.27 |       72.73 |    0.78 |   0.78 |    0.00 |   0.00 |    8.42 |    758.47 | 72,839,589 | 208,262 |      93 | that   | purported  |
| **that~uncommon**   |    804 |     32.34 |      771.66 |    0.07 |   0.07 |    0.00 |   0.00 |    4.43 |  3,680.42 | 72,839,589 | 208,262 |  11,312 | that   | uncommon   |
| **that~dissimilar** |    307 |     13.17 |      293.83 |    0.06 |   0.07 |    0.00 |   0.00 |    4.13 |  1,365.56 | 72,839,589 | 208,262 |   4,605 | that   | dissimilar |
| **that~bad**        | 19,708 |  1,228.13 |   18,479.87 |    0.04 |   0.05 |    0.09 |   0.09 |    4.01 | 74,955.43 | 72,839,589 | 208,262 | 429,537 | that   | bad        |
| **that~farfetched** |     93 |      3.79 |       89.21 |    0.07 |   0.07 |    0.00 |   0.00 |    3.75 |    423.24 | 72,839,589 | 208,262 |   1,324 | that   | farfetched |
| **that~great**      | 11,781 |    884.23 |   10,896.77 |    0.04 |   0.04 |    0.05 |   0.06 |    3.71 | 40,195.15 | 72,839,589 | 208,262 | 309,258 | that   | great      |
| **that~hard**       | 10,380 |    996.32 |    9,383.68 |    0.03 |   0.03 |    0.05 |   0.05 |    3.34 | 30,573.43 | 72,839,589 | 208,262 | 348,463 | that   | hard       |
| **that~stupid**     |  1,437 |    145.02 |    1,291.98 |    0.03 |   0.03 |    0.01 |   0.01 |    3.12 |  4,048.67 | 72,839,589 | 208,262 |  50,722 | that   | stupid     |
| **that~big**        |  7,073 |    865.10 |    6,207.90 |    0.02 |   0.02 |    0.03 |   0.03 |    2.96 | 17,624.62 | 72,839,589 | 208,262 | 302,567 | that   | big        |
| **that~easy**       | 12,825 |  1,657.83 |   11,167.17 |    0.02 |   0.02 |    0.05 |   0.06 |    2.91 | 30,976.21 | 72,839,589 | 208,262 | 579,827 | that   | easy       |


1. that_purported
   >  Benham noted that in Davis ' most recent appeals , his lawyers put into evidence affidavits that purported to show that executions by electrocution have been plagued by `` shocking and grotesque errors '' and that there is a substantial risk they result in `` unnecessary infliction of pain and disfigurement . ''

2. that_uncommon
   >  Perhaps such a practice was not that uncommon in Japan , especially during the Middle Ages .

3. that_dissimilar
   >  Many of the prisoners she met were " not that dissimilar from entrepreneurs , " she tells Chu .

4. that_bad
   >  The preview I watched was n't that bad although I was left a bit confused by the end with the development of the characters .

5. that_farfetched
   >  However , it makes me wonder how much of this ' farfetched ' film is really that farfetched .

6. that_great
   >  Is hard to believe that the support was not that great , but we did not give up , and we raised enough money to BUY and ultrasound .

7. that_hard
   >  I mean really , it 's not that hard to soak a pound of dry beans , and I love beans .

8. that_stupid
   >  I 'm not that stupid , seeing as obviously he has a thing for you ... " she said , smirking as a slight flush went over Kasumi 's cheeks .

9. that_big
   >  Kemp's Ridley turtles get up to 100 feet and 2 feet long which is not that big for a turtle .

10. that_easy
   >  However , it is not that easy to find the suitable terms to characterize a wine .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_purported_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_uncommon_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_dissimilar_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_bad_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_farfetched_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_great_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_hard_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_stupid_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_big_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_easy_50ex.csv

## *exactly*


|                           |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`    | `l2`          |
|:--------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|-------:|--------:|:--------|:--------------|
| **exactly~alike**         | 2,768 |      9.16 |    2,758.84 |    0.24 |   0.24 |    0.05 |   0.05 |    8.46 | 26,963.38 | 72,839,589 | 58,643 |  11,375 | exactly | alike         |
| **exactly~opposite**      |   464 |      6.84 |      457.16 |    0.05 |   0.05 |    0.01 |   0.01 |    5.76 |  3,028.33 | 72,839,589 | 58,643 |   8,491 | exactly | opposite      |
| **exactly~right**         | 6,323 |    115.21 |    6,207.79 |    0.04 |   0.04 |    0.11 |   0.11 |    5.74 | 39,191.65 | 72,839,589 | 58,643 | 143,095 | exactly | right         |
| **exactly~sure**          | 9,157 |    211.60 |    8,945.40 |    0.03 |   0.03 |    0.15 |   0.16 |    5.40 | 52,863.19 | 72,839,589 | 58,643 | 262,825 | exactly | sure          |
| **exactly~zero**          |   305 |      7.65 |      297.35 |    0.03 |   0.03 |    0.01 |   0.01 |    4.86 |  1,664.57 | 72,839,589 | 58,643 |   9,500 | exactly | zero          |
| **exactly~parallel**      |   205 |      5.22 |      199.78 |    0.03 |   0.03 |    0.00 |   0.00 |    4.72 |  1,111.99 | 72,839,589 | 58,643 |   6,488 | exactly | parallel      |
| **exactly~stellar**       |   172 |      4.33 |      167.67 |    0.03 |   0.03 |    0.00 |   0.00 |    4.68 |    936.96 | 72,839,589 | 58,643 |   5,379 | exactly | stellar       |
| **exactly~analogous**     |   103 |      2.47 |      100.53 |    0.03 |   0.03 |    0.00 |   0.00 |    4.53 |    571.33 | 72,839,589 | 58,643 |   3,062 | exactly | analogous     |
| **exactly~perpendicular** |    50 |      1.00 |       49.00 |    0.04 |   0.04 |    0.00 |   0.00 |    4.34 |    295.37 | 72,839,589 | 58,643 |   1,240 | exactly | perpendicular |
| **exactly~conducive**     |   208 |      7.33 |      200.67 |    0.02 |   0.02 |    0.00 |   0.00 |    4.25 |    995.32 | 72,839,589 | 58,643 |   9,110 | exactly | conducive     |


1. exactly_alike
   >  No two of your characters will be exactly alike .

2. exactly_opposite
   >  Similar laws are in place for the quark and antiquark that make up a meson : their respective colors must be exactly opposite .

3. exactly_right
   >  All that is exactly right , because deciding on a university is often the first really major decision of a young adult 's life .

4. exactly_sure
   >  Not exactly sure what a Prof is ?

5. exactly_zero
   >  I did sign up for a trip to Pai Canyon to watch the sunset , and was able to chat with a group of girls from the UK on the way up and the way back , so my social interaction was n't exactly zero for Day 1 solo on the roads .

6. exactly_parallel
   >  The most common obstacle is binding which can result when mounting surfaces are n't exactly parallel .

7. exactly_stellar
   >  It was a long day for them and the Browns are n't exactly stellar in the passing game .

8. exactly_analogous
   >  In short , the cases are almost exactly analogous .

9. exactly_perpendicular
   >  In this context , the rotation of the ground floor white volume is included in order to be located exactly perpendicular to the south .

10. exactly_conducive
   >  Not exactly conducive to being a rock star .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_alike_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_opposite_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_right_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_sure_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_zero_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_parallel_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_stellar_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_analogous_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_perpendicular_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_conducive_50ex.csv

## *any*


|                 |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`   | `l2`    |
|:----------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|-------:|--------:|:-------|:--------|
| **any~happier** |    963 |      7.84 |      955.16 |    0.06 |   0.06 |    0.03 |   0.03 |    6.75 |  7,438.55 | 72,839,589 | 34,382 |  16,606 | any    | happier |
| **any~clearer** |    608 |      5.51 |      602.49 |    0.05 |   0.05 |    0.02 |   0.02 |    6.51 |  4,556.17 | 72,839,589 | 34,382 |  11,680 | any    | clearer |
| **any~closer**  |  1,738 |     29.02 |    1,708.98 |    0.03 |   0.03 |    0.05 |   0.05 |    5.74 | 10,942.35 | 72,839,589 | 34,382 |  61,475 | any    | closer  |
| **any~wiser**   |    141 |      1.71 |      139.29 |    0.04 |   0.04 |    0.00 |   0.00 |    5.66 |    971.10 | 72,839,589 | 34,382 |   3,630 | any    | wiser   |
| **any~cuter**   |     80 |      0.86 |       79.14 |    0.04 |   0.04 |    0.00 |   0.00 |    5.56 |    570.11 | 72,839,589 | 34,382 |   1,828 | any    | cuter   |
| **any~safer**   |    626 |     10.77 |      615.23 |    0.03 |   0.03 |    0.02 |   0.02 |    5.56 |  3,883.22 | 72,839,589 | 34,382 |  22,826 | any    | safer   |
| **any~worse**   |  3,673 |     84.50 |    3,588.50 |    0.02 |   0.02 |    0.10 |   0.11 |    5.33 | 20,994.30 | 72,839,589 | 34,382 | 179,012 | any    | worse   |
| **any~better**  | 11,460 |    295.36 |   11,164.64 |    0.02 |   0.02 |    0.32 |   0.33 |    5.23 | 65,861.94 | 72,839,589 | 34,382 | 625,733 | any    | better  |
| **any~truer**   |     56 |      0.67 |       55.33 |    0.04 |   0.04 |    0.00 |   0.00 |    5.16 |    386.71 | 72,839,589 | 34,382 |   1,427 | any    | truer   |
| **any~nearer**  |     66 |      0.87 |       65.13 |    0.04 |   0.04 |    0.00 |   0.00 |    5.15 |    444.12 | 72,839,589 | 34,382 |   1,836 | any    | nearer  |


1. any_happier
   >  Even though he arrived a week before my due date Frankie weighed 7lb 8oz , was in perfect health and we could n't have been any happier !

2. any_clearer
   >  The dramaturgy cannot be any clearer in trying to highlight where our focus should be .

3. any_closer
   >  Asked if she was any closer to giving an endorsement , Palin told the Fox News host that she could only tell him what she 'd do if she were a South Carolinian .

4. any_wiser
   >  Is burning binary bits of information any wiser ?

5. any_cuter
   >  It could n't be any cuter .

6. any_safer
   >  In Kate Thompson 's Creature of the Night Bobby 's mum is running away , taking her family with her , but is the country any safer than the city ? *

7. any_worse
   >  " Can this day get any worse ? "

8. any_better
   >  Do you think his odds would have been any better if he 'd been publishing his work today ?

9. any_truer
   >  In the case of Alan , this saying could not have been any truer .

10. any_nearer
   >  No one lives any nearer than town .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_happier_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_clearer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_closer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_wiser_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_cuter_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_safer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_worse_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_better_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_truer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_nearer_50ex.csv

## *remotely*


|                          |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |        `N` |   `f1` |    `f2` | `l1`     | `l2`        |
|:-------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|-----------:|-------:|--------:|:---------|:------------|
| **remotely~detonated**   |    78 |      0.02 |       77.98 |    0.88 |   0.88 |    0.00 |   0.00 |   12.69 | 1,243.75 | 72,839,589 | 16,426 |      89 | remotely | detonated   |
| **remotely~exploitable** |   145 |      0.22 |      144.78 |    0.15 |   0.15 |    0.01 |   0.01 |    8.79 | 1,613.38 | 72,839,589 | 16,426 |     986 | remotely | exploitable |
| **remotely~comparable**  |   277 |      2.76 |      274.24 |    0.02 |   0.02 |    0.02 |   0.02 |    6.15 | 2,015.00 | 72,839,589 | 16,426 |  12,252 | remotely | comparable  |
| **remotely~plausible**   |   183 |      3.96 |      179.04 |    0.01 |   0.01 |    0.01 |   0.01 |    4.89 | 1,048.46 | 72,839,589 | 16,426 |  17,571 | remotely | plausible   |
| **remotely~related**     |   617 |     23.76 |      593.24 |    0.01 |   0.01 |    0.04 |   0.04 |    4.36 | 2,857.41 | 72,839,589 | 16,426 | 105,375 | remotely | related     |
| **remotely~close**       | 1,597 |     92.76 |    1,504.24 |    0.00 |   0.00 |    0.09 |   0.10 |    3.90 | 6,229.80 | 72,839,589 | 16,426 | 411,329 | remotely | close       |
| **remotely~interested**  | 1,062 |     59.65 |    1,002.35 |    0.00 |   0.00 |    0.06 |   0.06 |    3.90 | 4,177.56 | 72,839,589 | 16,426 | 264,528 | remotely | interested  |
| **remotely~credible**    |   100 |      3.68 |       96.32 |    0.01 |   0.01 |    0.01 |   0.01 |    3.87 |   468.95 | 72,839,589 | 16,426 |  16,318 | remotely | credible    |
| **remotely~possible**    |   727 |     55.31 |      671.69 |    0.00 |   0.00 |    0.04 |   0.04 |    3.41 | 2,431.85 | 72,839,589 | 16,426 | 245,272 | remotely | possible    |
| **remotely~believable**  |    68 |      3.12 |       64.88 |    0.00 |   0.00 |    0.00 |   0.00 |    3.33 |   290.03 | 72,839,589 | 16,426 |  13,823 | remotely | believable  |


1. remotely_detonated
   >  the bomb hit the car only a few miles from its destination , officials said , and may have been remotely detonated .

2. remotely_exploitable
   >  Sun Systems products get 23 fixes , seven of which are remotely exploitable .

3. remotely_comparable
   >  Yes , yes , I know , the cases are not remotely comparable .

4. remotely_plausible
   >  Which reminds me , how was it even remotely plausible that Sally Yates was convinced that Mike Flynn was compromised because he had n't been completely forthright in disclosing his conversation with the Russian ambassador ?

5. remotely_related
   >  If you like Treme and restaurants , or restaurants only , or Bourdain or , well , any other things even remotely related to the whole thing , read it .

6. remotely_close
   >  " In only one case did I find anything even remotely close where an officer wrote that the victim did not resist to the best of her ability . "

7. remotely_interested
   >  Since the game is free-to - play , anybody who 's even remotely interested in tank warfare or shooting down birds out of the sky , would be missing out should they choose not give it a go .

8. remotely_credible
   >  Michiko Kakutani , writing in The New York Times , bridled at the book 's `` grotesque , voyeuristic scenes '' and found the female characters not `` remotely credible . ''

9. remotely_possible
   >  The guy getting credit for revealing the fraud actually did a lot of work that is not remotely possible for the average retail investor , or even the extraordinary retail investor , including going to China to meet the company .

10. remotely_believable
   >  although there is nothing remotely believable about this drawn-out cat-and-mouse game of a movie crossed with a whodunit , that 's almost the point .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_detonated_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_exploitable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_comparable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_plausible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_related_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_close_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_interested_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_credible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_possible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_believable_50ex.csv

## *ever*


|                      |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |    `f1` |   `f2` | `l1`   | `l2`        |
|:---------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|--------:|-------:|:-------|:------------|
| **ever~olympic**     |   218 |      0.77 |      217.23 |    0.44 |   0.44 |    0.00 |   0.00 |    8.23 |  2,141.80 | 72,839,589 | 114,075 |    492 | ever   | olympic     |
| **ever~quarterly**   |   137 |      0.48 |      136.52 |    0.45 |   0.45 |    0.00 |   0.00 |    8.05 |  1,349.65 | 72,839,589 | 114,075 |    306 | ever   | quarterly   |
| **ever~watchful**    |   416 |      2.92 |      413.08 |    0.22 |   0.22 |    0.00 |   0.00 |    7.05 |  3,399.87 | 72,839,589 | 114,075 |  1,866 | ever   | watchful    |
| **ever~closer**      | 6,307 |     96.28 |    6,210.72 |    0.10 |   0.10 |    0.05 |   0.06 |    6.08 | 41,328.73 | 72,839,589 | 114,075 | 61,475 | ever   | closer      |
| **ever~joint**       |   195 |      2.29 |      192.71 |    0.13 |   0.13 |    0.00 |   0.00 |    5.95 |  1,375.51 | 72,839,589 | 114,075 |  1,460 | ever   | joint       |
| **ever~nearer**      |   223 |      2.88 |      220.12 |    0.12 |   0.12 |    0.00 |   0.00 |    5.84 |  1,528.28 | 72,839,589 | 114,075 |  1,836 | ever   | nearer      |
| **ever~vigilant**    |   923 |     14.94 |      908.06 |    0.10 |   0.10 |    0.01 |   0.01 |    5.80 |  5,892.45 | 72,839,589 | 114,075 |  9,541 | ever   | vigilant    |
| **ever~diminishing** |    71 |      0.70 |       70.30 |    0.16 |   0.16 |    0.00 |   0.00 |    5.75 |    527.77 | 72,839,589 | 114,075 |    445 | ever   | diminishing |
| **ever~scarcer**     |    82 |      0.85 |       81.15 |    0.15 |   0.15 |    0.00 |   0.00 |    5.75 |    599.19 | 72,839,589 | 114,075 |    545 | ever   | scarcer     |
| **ever~shrinking**   |   120 |      1.55 |      118.45 |    0.12 |   0.12 |    0.00 |   0.00 |    5.60 |    822.02 | 72,839,589 | 114,075 |    989 | ever   | shrinking   |


1. ever_olympic
   >  Naidan Tuvshinbayar won Mongolia 's first ever Olympic gold medal when claiming the men's 100 kg title .

2. ever_quarterly
   >  Losses of Tw $ 9.8 billion in the last three months of 2017 represented its worst ever quarterly results .

3. ever_watchful
   >  Owls are a rowdy bunch with fantasy colored feathers in bright oranges , greens , reds , yellows , blues and purples , with feathers that stick out in all directions and their signature yellow eyes ever watchful for an opportunity to clown around .

4. ever_closer
   >  CW : Since the US / EU stance on the two above-territories since the collapse of the USSR has effectively achieved the precise opposite of what that stance was designed to achieve ( by pushing the regions into ever closer ties with Russia ) , how can there be any logical defence of continuing that policy ?

5. ever_joint
   >  The Nepal Army has said that Kathmandu and Beijing will conduct their first ever joint military exercise from April 16 .

6. ever_nearer
   >  At Wednesday 's ceremony , the 2012 medals will be shown to the world for the first time , yet another reminder that the Games are drawing ever nearer .

7. ever_vigilant
   >  " One after the other , each of us must be ever vigilant , to relentlessly overcome each challenge , to reach higher , set more innovative goals , and bring joy to our customers .

8. ever_diminishing
   >  Miners create a block after a time frame which is worth an ever diminishing amount of currency or some kind of reward in order to ensure the shortfall .

9. ever_scarcer
   >  As The City 's rents rise even higher and real estate becomes ever scarcer with more people flocking here to take advantage of the tech -fueled economic boom , a new kind of street person is emerging : older , gay , and living with HIV or AIDS .

10. ever_shrinking
   >  In our complicated and ever shrinking world , the power of different bodies to make or administer law is often unclear .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_olympic_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_quarterly_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_watchful_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_closer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_joint_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_nearer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_vigilant_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_diminishing_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_scarcer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_shrinking_50ex.csv

## *yet*


|                      |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |        `N` |   `f1` |   `f2` | `l1`   | `l2`         |
|:---------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|-----------:|-------:|-------:|:-------|:-------------|
| **yet~unborn**       |   372 |      0.68 |      371.32 |    0.72 |   0.72 |    0.00 |   0.00 |   10.14 | 4,319.00 | 72,839,589 | 95,763 |    519 | yet    | unborn       |
| **yet~unnamed**      |   736 |      2.77 |      733.23 |    0.35 |   0.35 |    0.01 |   0.01 |    8.29 | 7,048.15 | 72,839,589 | 95,763 |  2,107 | yet    | unnamed      |
| **yet~unspecified**  |   204 |      0.80 |      203.20 |    0.33 |   0.34 |    0.00 |   0.00 |    7.86 | 1,933.20 | 72,839,589 | 95,763 |    607 | yet    | unspecified  |
| **yet~undetermined** |   297 |      1.45 |      295.55 |    0.27 |   0.27 |    0.00 |   0.00 |    7.55 | 2,658.03 | 72,839,589 | 95,763 |  1,104 | yet    | undetermined |
| **yet~untitled**     |   121 |      0.54 |      120.46 |    0.29 |   0.29 |    0.00 |   0.00 |    7.37 | 1,107.51 | 72,839,589 | 95,763 |    412 | yet    | untitled     |
| **yet~unidentified** |   336 |      2.48 |      333.52 |    0.18 |   0.18 |    0.00 |   0.00 |    6.85 | 2,694.33 | 72,839,589 | 95,763 |  1,890 | yet    | unidentified |
| **yet~unformed**     |    53 |      0.33 |       52.67 |    0.21 |   0.21 |    0.00 |   0.00 |    6.28 |   445.94 | 72,839,589 | 95,763 |    249 | yet    | unformed     |
| **yet~final**        |   643 |      7.70 |      635.30 |    0.11 |   0.11 |    0.01 |   0.01 |    6.20 | 4,494.99 | 72,839,589 | 95,763 |  5,860 | yet    | final        |
| **yet~unannounced**  |   129 |      1.16 |      127.84 |    0.14 |   0.15 |    0.00 |   0.00 |    6.19 |   979.33 | 72,839,589 | 95,763 |    883 | yet    | unannounced  |
| **yet~undiscovered** |   278 |      2.99 |      275.01 |    0.12 |   0.12 |    0.00 |   0.00 |    6.18 | 2,006.07 | 72,839,589 | 95,763 |  2,272 | yet    | undiscovered |


1. yet_unborn
   >  You may spill your blood as a purely symbolic gesture , in service to those humans yet unborn .

2. yet_unnamed
   >  That will be powered by a yet unnamed 1.6 Ghz octa-core processor , supported by 2GB RAM .

3. yet_unspecified
   >  most of the justices are troubled by outsized verdicts , and the court has ruled that the constitutional guarantee of due process of law places some , as yet unspecified , limits on punitive damages .

4. yet_undetermined
   >  Clashes had five wounded Saturday night in circumstances yet undetermined .

5. yet_untitled
   >  Actor-filmmaker Kamal Haasan will reportedly join hands with his erstwhile assistant Rajesh M Selva , director of his last Tamil outing " Thoongaavanam " , for a yet untitled Tamil actioner .

6. yet_unidentified
   >  They are focusing genetic testing on families , like Crissy 's , where breast cancer is hereditary and develops from a yet unidentified gene mutation .

7. yet_unformed
   >  Whilst earth , as yet unformed and void ,

8. yet_final
   >  The duties are not yet final , so we will continue to use all the means available to us to ensure a fair outcome to these investigations , " the sources explained .

9. yet_unannounced
   >  3 . A yet unannounced candidate takes the White House

10. yet_undiscovered
   >  `` Countless seabirds , dolphins , fishes , corals and tiny things as yet undiscovered could survive as a result , free of the threats that are eliminating them elsewhere . ''

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unborn_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unnamed_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unspecified_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_undetermined_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_untitled_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unidentified_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unformed_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_final_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unannounced_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_undiscovered_50ex.csv

## *immediately*


|                              |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |       `G2` |        `N` |   `f1` |    `f2` | `l1`        | `l2`         |
|:-----------------------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|-----------:|-----------:|-------:|--------:|:------------|:-------------|
| **immediately~accretive**    |    236 |      0.70 |      235.30 |    0.45 |   0.45 |    0.00 |   0.00 |    8.54 |   2,406.67 | 72,839,589 | 96,973 |     523 | immediately | accretive    |
| **immediately~appealable**   |     76 |      0.19 |       75.81 |    0.55 |   0.55 |    0.00 |   0.00 |    8.41 |     815.23 | 72,839,589 | 96,973 |     139 | immediately | appealable   |
| **immediately~adjacent**     |  1,595 |      6.33 |    1,588.67 |    0.33 |   0.34 |    0.02 |   0.02 |    8.31 |  15,089.64 | 72,839,589 | 96,973 |   4,756 | immediately | adjacent     |
| **immediately~apparent**     |  4,971 |     72.22 |    4,898.78 |    0.09 |   0.09 |    0.05 |   0.05 |    6.12 |  32,982.98 | 72,839,589 | 96,973 |  54,246 | immediately | apparent     |
| **immediately~clear**        | 26,038 |    464.92 |   25,573.08 |    0.07 |   0.07 |    0.26 |   0.27 |    5.86 | 167,884.92 | 72,839,589 | 96,973 | 349,214 | immediately | clear        |
| **immediately~actionable**   |    173 |      2.64 |      170.36 |    0.09 |   0.09 |    0.00 |   0.00 |    5.47 |   1,121.82 | 72,839,589 | 96,973 |   1,983 | immediately | actionable   |
| **immediately~recognizable** |  1,736 |     44.60 |    1,691.40 |    0.05 |   0.05 |    0.02 |   0.02 |    5.15 |   9,447.17 | 72,839,589 | 96,973 |  33,499 | immediately | recognizable |
| **immediately~available**    | 29,351 |    887.87 |   28,463.13 |    0.04 |   0.04 |    0.29 |   0.30 |    5.06 | 159,088.56 | 72,839,589 | 96,973 | 666,909 | immediately | available    |
| **immediately~subsequent**   |     59 |      0.96 |       58.04 |    0.08 |   0.08 |    0.00 |   0.00 |    4.81 |     374.58 | 72,839,589 | 96,973 |     722 | immediately | subsequent   |
| **immediately~recognisable** |    349 |     10.92 |      338.08 |    0.04 |   0.04 |    0.00 |   0.00 |    4.59 |   1,757.24 | 72,839,589 | 96,973 |   8,204 | immediately | recognisable |


1. immediately_accretive
   >  " Further , we expect to leverage our purchasing , sales , distribution and administrative capabilities to improve the profitability of this business , and we expect this acquisition to be immediately accretive to Drew 's earnings . "

2. immediately_appealable
   >  Generally , the denial of a motion to dismiss under Rule 12 ( b ) ( 6 ) , SCRCP , is not immediately appealable .

3. immediately_adjacent
   >  Sometimes the parking is in its own big ugly building , and sometimes it 's designed so that it 's immediately adjacent to the apartment or townhouse of its occupant .

4. immediately_apparent
   >  " Research can be hard , and its benefits are n't always immediately apparent , " she shares .

5. immediately_clear
   >  the cause of the fire was not immediately clear but investigators say they believe it was an accident .

6. immediately_actionable
   >  I facilitate teacher workshops and online courses that deliver practical and immediately actionable advice on teachers from early childhood to Primary can develop student ICT capability in their lessons .

7. immediately_recognizable
   >  It 's an appropriate motto for the hitmaker savant , who has managed to fit a number of wildly disparate elements under that pop umbrella , crafting an immediately recognizable sound out of a multitude of genres .

8. immediately_available
   >  Financial details of the agreement were not immediately available , but Simon was more than satisfied .

9. immediately_subsequent
   >  At issue , as FHQ has discussed , is the discrepancy between the longstanding New Hampshire election law that requires seven days between the primary in the Granite state and the immediately subsequent primary or caucus and a newly -enacted Nevada Republican Party resolution tethering the party 's caucuses to the Saturday following the New Hampshire primary .

10. immediately_recognisable
   >  Its vastness and power have supplied immediately recognisable symbols for moral and religious works of art .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_accretive_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_appealable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_adjacent_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_apparent_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_clear_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_actionable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognizable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_available_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_subsequent_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognisable_50ex.csv

## *particularly*


|                              |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |    `f1` |   `f2` | `l1`         | `l2`        |
|:-----------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|--------:|-------:|:-------------|:------------|
| **particularly~hard-hit**    |   154 |      2.76 |      151.24 |    0.39 |   0.39 |    0.00 |   0.00 |    5.64 |  1,005.08 | 72,839,589 | 513,668 |    391 | particularly | hard-hit    |
| **particularly~galling**     |   540 |     15.33 |      524.67 |    0.24 |   0.25 |    0.00 |   0.00 |    5.12 |  2,937.15 | 72,839,589 | 513,668 |  2,174 | particularly | galling     |
| **particularly~well-suited** |    62 |      1.22 |       60.78 |    0.35 |   0.36 |    0.00 |   0.00 |    4.91 |    390.17 | 72,839,589 | 513,668 |    173 | particularly | well-suited |
| **particularly~acute**       | 2,809 |    109.23 |    2,699.77 |    0.17 |   0.18 |    0.01 |   0.01 |    4.79 | 13,361.56 | 72,839,589 | 513,668 | 15,489 | particularly | acute       |
| **particularly~noteworthy**  | 2,294 |    112.66 |    2,181.34 |    0.14 |   0.14 |    0.00 |   0.00 |    4.37 |  9,788.31 | 72,839,589 | 513,668 | 15,975 | particularly | noteworthy  |
| **particularly~thorny**      |   308 |     12.43 |      295.57 |    0.17 |   0.17 |    0.00 |   0.00 |    4.36 |  1,439.60 | 72,839,589 | 513,668 |  1,762 | particularly | thorny      |
| **particularly~fond**        | 4,179 |    229.28 |    3,949.72 |    0.12 |   0.13 |    0.01 |   0.01 |    4.24 | 16,897.66 | 72,839,589 | 513,668 | 32,513 | particularly | fond        |
| **particularly~nettlesome**  |    63 |      2.03 |       60.97 |    0.21 |   0.22 |    0.00 |   0.00 |    4.02 |    324.87 | 72,839,589 | 513,668 |    288 | particularly | nettlesome  |
| **particularly~nasty**       | 2,143 |    135.27 |    2,007.73 |    0.10 |   0.11 |    0.00 |   0.00 |    3.96 |  8,052.99 | 72,839,589 | 513,668 | 19,181 | particularly | nasty       |
| **particularly~egregious**   | 1,705 |    107.12 |    1,597.88 |    0.11 |   0.11 |    0.00 |   0.00 |    3.94 |  6,421.57 | 72,839,589 | 513,668 | 15,190 | particularly | egregious   |


1. particularly_hard-hit
   >  shares of financial stocks were particularly hard-hit .

2. particularly_galling
   >  the brazen presence in Poti has been particularly galling for Georgia because it is hundreds of kilometers -LRB- miles -RRB- from South Ossetia , where the war broke out and where most of the fighting occurred .

3. particularly_well-suited
   >  but the plutonium produced by its two breeders , Monju and Joyo , is a kind that is particularly well-suited to bombs , Greenpeace said .

4. particularly_acute
   >  The risks were particularly acute for correspondents in the north and east and those covering political events .

5. particularly_noteworthy
   >  Bushey recalled how , shortly after learning of what he called `` a particularly noteworthy crime , '' he directed one of his subordinates to inform Simpson `` just as soon as was humanly possible . ''

6. particularly_thorny
   >  With $ 15,000 payouts for first place and particularly thorny fields , the Championships have traditionally been considered among pool 's domestic majors .

7. particularly_fond
   >  For example , I love mixing the herbal Honeybush Vanilla [ 19 ] with a black English Breakfast [ 20 ] tea. Adagio [ 21 ] allows users to upload their favourite blends so that other tea drinkers can purchase them ( I am particularly fond of the Captain America [ 22 ] and TARDIS [ 23 ] blends ) .

8. particularly_nettlesome
   >  The court in East Bridge Lofts described that issue as " particularly nettlesome , " but it also found that South Carolina ( whose law governed this issue ) applies what is known as the " automatic waiver " rule :

9. particularly_nasty
   >  Hunter , known for his in-your-face style , gave a particularly nasty time to Red Wings captain Steve Yzerman .

10. particularly_egregious
   >  Veldhuis ' case is particularly egregious , because he was fired while his classes were still in session .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_hard-hit_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_galling_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_well-suited_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_acute_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_noteworthy_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_thorny_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_fond_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_nettlesome_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_nasty_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_egregious_50ex.csv

## *inherently*


|                                  |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |        `N` |   `f1` |   `f2` | `l1`       | `l2`              |
|:---------------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|-----------:|-------:|-------:|:-----------|:------------------|
| **inherently~governmental**      |   253 |      0.50 |      252.50 |    0.33 |   0.33 |    0.01 |   0.01 |    8.92 | 2,742.59 | 72,839,589 | 47,803 |    761 | inherently | governmental      |
| **inherently~unequal**           |   390 |      3.69 |      386.31 |    0.07 |   0.07 |    0.01 |   0.01 |    6.38 | 2,893.14 | 72,839,589 | 47,803 |  5,621 | inherently | unequal           |
| **inherently~evil**              | 1,123 |     14.90 |    1,108.10 |    0.05 |   0.05 |    0.02 |   0.02 |    6.05 | 7,572.62 | 72,839,589 | 47,803 | 22,706 | inherently | evil              |
| **inherently~coercive**          |    94 |      0.82 |       93.18 |    0.07 |   0.08 |    0.00 |   0.00 |    5.98 |   711.86 | 72,839,589 | 47,803 |  1,253 | inherently | coercive          |
| **inherently~unstable**          |   806 |     14.80 |      791.20 |    0.04 |   0.04 |    0.02 |   0.02 |    5.52 | 4,903.18 | 72,839,589 | 47,803 | 22,546 | inherently | unstable          |
| **inherently~sinful**            |   145 |      2.01 |      142.99 |    0.05 |   0.05 |    0.00 |   0.00 |    5.49 |   962.39 | 72,839,589 | 47,803 |  3,059 | inherently | sinful            |
| **inherently~flawed**            |   899 |     18.13 |      880.87 |    0.03 |   0.03 |    0.02 |   0.02 |    5.39 | 5,301.74 | 72,839,589 | 47,803 | 27,628 | inherently | flawed            |
| **inherently~untrustworthy**     |    69 |      0.79 |       68.21 |    0.06 |   0.06 |    0.00 |   0.00 |    5.39 |   483.61 | 72,839,589 | 47,803 |  1,211 | inherently | untrustworthy     |
| **inherently~interdisciplinary** |    94 |      1.25 |       92.75 |    0.05 |   0.05 |    0.00 |   0.00 |    5.35 |   631.33 | 72,839,589 | 47,803 |  1,906 | inherently | interdisciplinary |
| **inherently~discriminatory**    |   175 |      2.94 |      172.06 |    0.04 |   0.04 |    0.00 |   0.00 |    5.27 | 1,093.34 | 72,839,589 | 47,803 |  4,481 | inherently | discriminatory    |


1. inherently_governmental
   >  " When it comes to security in war zones , what is considered ' inherently governmental ? '

2. inherently_unequal
   >  And this is when the Supreme Court of the U.S. ruled that the " separate but equal " policy was inherently unequal .

3. inherently_evil
   >  The layperson 's affirmation of this proposition as necessarily true is linked essentially to some pretty basic " inside " feelings that rape is inherently evil .

4. inherently_coercive
   >  While direct contact is somewhat more intrusive , it is not inherently coercive .

5. inherently_unstable
   >  " Vitamin C is inherently unstable and easily oxidizes in air , which makes it ineffective .

6. inherently_sinful
   >  The position taken by most Anglican churches in Africa , which see homosexuality as inherently sinful ( at best ) is in the end irreconcilable with the liberal views which predominate in North America and increasingly ( though far from uniformly ) in the Church of England itself .

7. inherently_flawed
   >  A man's means may become his end as a result of conscious and reasoned choice , and there is nothing inherently flawed in this approach .

8. inherently_untrustworthy
   >  As such , UN agencies like the WTO , Human Rights Council , and World Bank are inevitably unethical and inherently untrustworthy .

9. inherently_interdisciplinary
   >  The problems are inherently interdisciplinary .

10. inherently_discriminatory
   >  some analysts said whites , often the chief architect of standardized tests and the products of better schools , tend to perform better than minorities _ making reliance on the test inherently discriminatory .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_governmental_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unequal_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_evil_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_coercive_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unstable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_sinful_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_flawed_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_untrustworthy_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_interdisciplinary_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_discriminatory_50ex.csv

## *terribly*


|                          |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`     | `l2`        |
|:-------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|-----------:|-------:|--------:|:---------|:------------|
| **terribly~awry**        |   180 |      0.56 |      179.44 |    0.26 |   0.26 |    0.00 |   0.00 |    8.02 |  1,770.97 | 72,839,589 | 58,964 |     692 | terribly | awry        |
| **terribly~wrong**       | 6,349 |    120.67 |    6,228.33 |    0.04 |   0.04 |    0.11 |   0.11 |    5.67 | 38,814.14 | 72,839,589 | 58,964 | 149,064 | terribly | wrong       |
| **terribly~amiss**       |    64 |      0.73 |       63.27 |    0.07 |   0.07 |    0.00 |   0.00 |    5.37 |    451.25 | 72,839,589 | 58,964 |     898 | terribly | amiss       |
| **terribly~sorry**       | 1,262 |     50.65 |    1,211.35 |    0.02 |   0.02 |    0.02 |   0.02 |    4.43 |  5,741.83 | 72,839,589 | 58,964 |  62,573 | terribly | sorry       |
| **terribly~misguided**   |   101 |      3.24 |       97.76 |    0.02 |   0.03 |    0.00 |   0.00 |    4.09 |    501.57 | 72,839,589 | 58,964 |   4,008 | terribly | misguided   |
| **terribly~inefficient** |   198 |      7.89 |      190.11 |    0.02 |   0.02 |    0.00 |   0.00 |    4.05 |    900.41 | 72,839,589 | 58,964 |   9,744 | terribly | inefficient |
| **terribly~surprising**  |   964 |     57.10 |      906.90 |    0.01 |   0.01 |    0.02 |   0.02 |    3.82 |  3,660.97 | 72,839,589 | 58,964 |  70,540 | terribly | surprising  |
| **terribly~sad**         | 1,241 |     80.21 |    1,160.79 |    0.01 |   0.01 |    0.02 |   0.02 |    3.73 |  4,513.50 | 72,839,589 | 58,964 |  99,081 | terribly | sad         |
| **terribly~unfair**      |   367 |     20.86 |      346.14 |    0.01 |   0.01 |    0.01 |   0.01 |    3.71 |  1,419.19 | 72,839,589 | 58,964 |  25,769 | terribly | unfair      |
| **terribly~frightened**  |   137 |      6.77 |      130.23 |    0.02 |   0.02 |    0.00 |   0.00 |    3.60 |    565.89 | 72,839,589 | 58,964 |   8,364 | terribly | frightened  |


1. terribly_awry
   >  As tends to happen , the experiment goes terribly awry .

2. terribly_wrong
   >  But he spoke with the confidence of someone who thinks his country has got things right , while others have got them terribly wrong .

3. terribly_amiss
   >  " It was made blatantly obvious to the millions of people watching the post parade that something was terribly amiss ( with Life At Ten ) , " De Bartolo 's letter said .

4. terribly_sorry
   >  I am terribly sorry to have to leave you after knowing you for such a short time .

5. terribly_misguided
   >  well , he 's a genius again , though I fear a terribly misguided one .

6. terribly_inefficient
   >  Well , I did write , but it was terribly inefficient to pile up the letters telling you I was drinking and studying and talking with folks in all sorts of interesting tongues .

7. terribly_surprising
   >  This story is a few days old ( and probably not terribly surprising ) , but I just wanted to mention Indiana University professor Julia R. Fox 's study that concludes that The Daily Show is just as substantive as nightly network news .

8. terribly_sad
   >  " Although I am terribly sad that we just lost her , I think that I am privileged to have known her , " Suen said .

9. terribly_unfair
   >  It ca n't be terribly unfair to the United States if there is zero consequence for the United States not meeting its targets .

10. terribly_frightened
   >  We are now terribly angry at your Patient ; now that we are no longer so terribly frightened about him !

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_awry_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_wrong_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_amiss_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_sorry_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_misguided_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_inefficient_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_surprising_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_sad_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_unfair_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_frightened_50ex.csv

