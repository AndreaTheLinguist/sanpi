```python
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, corners, timestamp_today, confirm_dir, print_md_table, print_iter
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.sample import sample_pickle as sp

K=9
BK = max(K+2, 10)
DATE=timestamp_today()
FOCUS_ORIG = ['f', 'E11', 'unexpected_f',
              'am_p1_given2', 'conservative_log_ratio',
              'am_log_likelihood', 
            #   't_score',
            #   'mutual_information', 'am_odds_ratio_disc',
              'N', 'f1', 'f2', 'l1', 'l2']
FOCUS = adjust_assoc_columns(FOCUS_ORIG)
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 80)
try:
    adv_am = pd.read_csv(
    TOP_AM_DIR / f'Top{K}_NEG-ADV_combined.35f-7c_{DATE}.csv').set_index('adv')
except FileNotFoundError: 
    DATE=DATE[:-1]+str(int(DATE[-1])-1)
    adv_am = pd.read_csv(
    TOP_AM_DIR / f'Top{K}_NEG-ADV_combined.35f-7c_{DATE}.csv').set_index('adv')
# loaded_cols = adv_am.columns.to_list()
HITS_SAMPLE_PATH = TOP_AM_DIR.joinpath(f'top{K}adv_sample-{K}-hit-tables_{DATE}.pkl.gz')
if not HITS_SAMPLE_PATH.is_file(): 
    yesterday=DATE[:-1]+str(int(DATE[-1])-1)
    HITS_SAMPLE_PATH = TOP_AM_DIR.joinpath(f'top{K}adv_sample-{K}-hit-tables_{yesterday}.pkl.gz')

```


```python
def nb_print_table(df, n_dec:int=2, 
                   adjust_columns:bool=True) -> None: 
    _df = df.copy()
    if adjust_columns: 
        _df = adjust_assoc_columns(_df)
    _df.columns = [f'`{c}`' for c in _df.columns]
    _df.index = [f'**{r}**' for r in _df.index ]
    print('\n'+_df.to_markdown(floatfmt=f',.{n_dec}f', intfmt=',')+'\n')
```


```python
nb_print_table(adv_am)
```

    
    |                  |   `G2_MIR` |   `G2_SET` |   `LRC_MIR` |   `LRC_SET` |      `N_MIR` |       `N_SET` |   `dP1_MIR` |   `dP1_SET` |   `exp_f_MIR` |   `exp_f_SET` |   `f1_MIR` |     `f1_SET` |   `f2_MIR` |   `f2_SET` |   `f_MIR` |    `f_SET` | `key_MIR`           | `key_SET`           | `l1_MIR`   | `l1_SET`   |   `unexp_f_MIR` |   `unexp_f_SET` |   `mean_G2` |   `mean_LRC` |      `mean_N` |   `mean_dP1` |   `mean_expF` |    `mean_f1` |   `mean_f2` |   `mean_f` |   `mean_unexpF` |
    |:-----------------|-----------:|-----------:|------------:|------------:|-------------:|--------------:|------------:|------------:|--------------:|--------------:|-----------:|-------------:|-----------:|-----------:|----------:|-----------:|:--------------------|:--------------------|:-----------|:-----------|----------------:|----------------:|------------:|-------------:|--------------:|-------------:|--------------:|-------------:|------------:|-----------:|----------------:|
    | **exactly**      |   1,939.47 | 214,404.20 |        3.51 |        5.90 | 2,032,082.00 | 86,330,752.00 |        0.59 |        0.67 |        161.15 |      2,301.98 | 293,963.00 | 3,226,213.00 |   1,114.00 |  61,599.00 |    813.00 |  43,635.00 | NEGmir~exactly      | NEGany~exactly      | NEGMIR     | NEGATED    |          651.85 |       41,333.02 |  108,171.83 |         4.71 | 44,181,417.00 |         0.63 |      1,231.57 | 1,760,088.00 |   31,356.50 | 604,556.17 |       20,992.43 |
    | **necessarily**  |   1,688.91 | 219,003.46 |        2.66 |        6.23 | 2,032,082.00 | 86,330,752.00 |        0.43 |        0.72 |        243.18 |      2,118.68 | 293,963.00 | 3,226,213.00 |   1,681.00 |  56,694.00 |    971.00 |  42,708.00 | NEGmir~necessarily  | NEGany~necessarily  | NEGMIR     | NEGATED    |          727.82 |       40,589.32 |  110,346.18 |         4.44 | 44,181,417.00 |         0.57 |      1,180.93 | 1,760,088.00 |   29,187.50 | 603,705.00 |       20,658.57 |
    | **before**       |   1,080.52 |   1,062.13 |        5.11 |        3.65 | 2,032,082.00 | 86,330,752.00 |        0.84 |        0.38 |         42.53 |         27.95 | 293,963.00 | 3,226,213.00 |     294.00 |     748.00 |    290.00 |     311.00 | NEGmir~before       | NEG~before          | NEGMIR     | NEGATED    |          247.47 |          283.05 |    1,071.32 |         4.38 | 44,181,417.00 |         0.61 |         35.24 | 1,760,088.00 |      521.00 | 586,969.83 |          265.26 |
    | **that**         |   7,632.21 | 781,016.11 |        2.86 |        5.62 | 2,032,082.00 | 86,330,752.00 |        0.44 |        0.63 |      1,080.91 |      9,357.24 | 293,963.00 | 3,226,213.00 |   7,472.00 | 250,392.00 |  4,338.00 | 165,411.00 | NEGmir~that         | NEGany~that         | NEGMIR     | NEGATED    |        3,257.09 |      156,053.76 |  394,324.16 |         4.24 | 44,181,417.00 |         0.53 |      5,219.08 | 1,760,088.00 |  128,932.00 | 657,964.83 |       79,655.42 |
    | **remotely**     |   4,009.84 |  13,354.33 |        3.35 |        3.03 | 2,032,082.00 | 86,330,752.00 |        0.54 |        0.22 |        393.04 |        829.40 | 293,963.00 | 3,226,213.00 |   2,717.00 |  22,194.00 |  1,846.00 |   5,679.00 | NEGmir~remotely     | NEGany~remotely     | NEGMIR     | NEGATED    |        1,452.96 |        4,849.60 |    8,682.08 |         3.19 | 44,181,417.00 |         0.38 |        611.22 | 1,760,088.00 |   12,455.50 | 592,102.00 |        3,151.28 |
    | **yet**          |     242.23 | 209,055.78 |        1.18 |        4.74 | 2,032,082.00 | 86,330,752.00 |        0.21 |        0.48 |        131.50 |      3,800.83 | 293,963.00 | 3,226,213.00 |     909.00 | 101,707.00 |    320.00 |  52,546.00 | NEGmir~yet          | NEGany~yet          | NEGMIR     | NEGATED    |          188.50 |       48,745.17 |  104,649.01 |         2.96 | 44,181,417.00 |         0.34 |      1,966.16 | 1,760,088.00 |   51,308.00 | 612,609.67 |       24,466.84 |
    | **ever**         |  15,340.34 |     353.58 |        5.57 |        0.28 | 2,032,082.00 | 86,330,752.00 |        0.77 |        0.01 |        749.20 |      4,656.05 | 293,963.00 | 3,226,213.00 |   5,179.00 | 124,592.00 |  4,718.00 |   5,967.00 | NEGmir~ever         | NEGany~ever         | NEGMIR     | NEGATED    |        3,968.80 |        1,310.95 |    7,846.96 |         2.92 | 44,181,417.00 |         0.39 |      2,702.62 | 1,760,088.00 |   64,885.50 | 610,105.33 |        2,639.88 |
    | **immediately**  |     181.20 | 239,462.58 |        0.79 |        4.96 | 2,032,082.00 | 86,330,752.00 |        0.14 |        0.52 |        208.60 |      3,855.76 | 293,963.00 | 3,226,213.00 |   1,442.00 | 103,177.00 |    407.00 |  57,319.00 | NEGmir~immediately  | NEGany~immediately  | NEGMIR     | NEGATED    |          198.40 |       53,463.24 |  119,821.89 |         2.88 | 44,181,417.00 |         0.33 |      2,032.18 | 1,760,088.00 |   52,309.50 | 613,753.50 |       26,830.82 |
    | **any**          |   2,511.26 |  23,683.00 |        3.48 |        2.28 | 2,032,082.00 | 86,330,752.00 |        0.57 |        0.13 |        219.02 |      3,518.50 | 293,963.00 | 3,226,213.00 |   1,514.00 |  94,152.00 |  1,082.00 |  15,492.00 | NEGmir~any          | NEGany~any          | NEGMIR     | NEGATED    |          862.98 |       11,973.50 |   13,097.13 |         2.88 | 44,181,417.00 |         0.35 |      1,868.76 | 1,760,088.00 |   47,833.00 | 605,402.67 |        6,418.24 |
    | **particularly** |  17,999.07 |  40,303.42 |        3.15 |        1.43 | 2,032,082.00 | 86,330,752.00 |        0.48 |        0.06 |      2,163.26 |     21,523.84 | 293,963.00 | 3,226,213.00 |  14,954.00 | 575,960.00 |  9,278.00 |  55,799.00 | NEGmir~particularly | NEGany~particularly | NEGMIR     | NEGATED    |        7,114.74 |       34,275.16 |   29,151.24 |         2.29 | 44,181,417.00 |         0.27 |     11,843.55 | 1,760,088.00 |  295,457.00 | 696,027.83 |       20,694.95 |
    | **terribly**     |     847.65 |  42,704.93 |        1.14 |        3.09 | 2,032,082.00 | 86,330,752.00 |        0.16 |        0.22 |        754.84 |      2,622.43 | 293,963.00 | 3,226,213.00 |   5,218.00 |  70,174.00 |  1,579.00 |  18,054.00 | NEGmir~terribly     | NEGany~terribly     | NEGMIR     | NEGATED    |          824.16 |       15,431.57 |   21,776.29 |         2.12 | 44,181,417.00 |         0.19 |      1,688.64 | 1,760,088.00 |   37,696.00 | 602,533.50 |        8,127.86 |
    | **inherently**   |   4,160.38 |   7,333.55 |        2.42 |        1.78 | 2,032,082.00 | 86,330,752.00 |        0.36 |        0.09 |        817.19 |      2,058.66 | 293,963.00 | 3,226,213.00 |   5,649.00 |  55,088.00 |  2,872.00 |   6,847.00 | NEGmir~inherently   | NEGany~inherently   | NEGMIR     | NEGATED    |        2,054.81 |        4,788.34 |    5,746.97 |         2.10 | 44,181,417.00 |         0.23 |      1,437.92 | 1,760,088.00 |   30,368.50 | 598,438.67 |        3,421.58 |
    | **altogether**   |    -123.22 |   9,468.00 |       -0.65 |        2.75 | 2,032,082.00 | 86,330,752.00 |       -0.08 |        0.18 |        261.55 |        771.17 | 293,963.00 | 3,226,213.00 |   1,808.00 |  20,636.00 |    112.00 |   4,575.00 | NEG~altogether      | NEGany~altogether   | NEGMIR     | NEGATED    |         -149.55 |        3,803.82 |    4,672.39 |         1.05 | 44,181,417.00 |         0.05 |        516.36 | 1,760,088.00 |   11,222.00 | 591,217.83 |        1,827.14 |
    | **only**         |    -716.03 | 261,936.36 |       -1.73 |        3.04 | 2,032,082.00 | 86,330,752.00 |       -0.11 |        0.21 |        747.75 |     17,346.13 | 293,963.00 | 3,226,213.00 |   5,169.00 | 464,168.00 |    173.00 | 114,070.00 | NEG~only            | NEGany~only         | NEGMIR     | NEGATED    |         -574.75 |       96,723.87 |  130,610.17 |         0.66 | 44,181,417.00 |         0.05 |      9,046.94 | 1,760,088.00 |  234,668.50 | 683,959.33 |       48,074.56 |
    



```python
adv_list = adv_am.index.to_list()
print_iter(adv_list, header=f'Top {K} Most Negative Adverbs',bullet = '1.')
```

    
    Top 9 Most Negative Adverbs
    1. exactly
    1. necessarily
    1. before
    1. that
    1. remotely
    1. yet
    1. ever
    1. immediately
    1. any
    1. particularly
    1. terribly
    1. inherently
    1. altogether
    1. only


## Load AM table for `adv~adj` comparison (bigram composition)


```python
adv_adj_am = adjust_assoc_columns(
    pd.read_pickle(AM_DF_DIR.joinpath('adv_adj/RBXadj/extra/AdvAdj_frq-thrMIN-7.35f_min200x_extra.pkl.gz'))
                                  ).filter(items=FOCUS).sort_values('LRC', ascending = False)
adv_adj_am = adv_adj_am.loc[adv_adj_am.l1.isin(adv_list), :]
nb_print_table(adv_adj_am.head(20))
adv_adj_am
```

    
    |                             |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |    `f1` |   `f2` | `l1`        | `l2`         |
    |:----------------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|--------:|-------:|:------------|:-------------|
    | **yet~unborn**              |   463 |      0.75 |      462.25 |    0.73 |   10.47 |  5,505.48 | 86,330,753 | 101,707 |    635 | yet         | unborn       |
    | **only~half-joking**        |   209 |      1.17 |      207.83 |    0.96 |    9.48 |  2,116.01 | 86,330,753 | 464,174 |    217 | only        | half-joking  |
    | **inherently~governmental** |   295 |      0.60 |      294.40 |    0.32 |    8.96 |  3,178.72 | 86,330,753 |  55,088 |    933 | inherently  | governmental |
    | **immediately~accretive**   |   243 |      0.68 |      242.32 |    0.43 |    8.65 |  2,499.70 | 86,330,753 | 103,177 |    565 | immediately | accretive    |
    | **exactly~alike**           | 3,040 |      9.46 |    3,030.54 |    0.23 |    8.55 | 29,939.32 | 86,330,753 |  61,599 | 13,261 | exactly     | alike        |
    | **yet~unnamed**             |   771 |      2.62 |      768.38 |    0.35 |    8.47 |  7,535.14 | 86,330,753 | 101,707 |  2,227 | yet         | unnamed      |
    | **ever~olympic**            |   229 |      0.76 |      228.24 |    0.43 |    8.37 |  2,273.22 | 86,330,753 | 124,592 |    529 | ever        | olympic      |
    | **immediately~adjacent**    | 1,714 |      6.49 |    1,707.51 |    0.31 |    8.37 | 16,336.57 | 86,330,753 | 103,177 |  5,427 | immediately | adjacent     |
    | **yet~unspecified**         |   219 |      0.79 |      218.21 |    0.33 |    8.06 |  2,109.33 | 86,330,753 | 101,707 |    669 | yet         | unspecified  |
    | **yet~undetermined**        |   317 |      1.39 |      315.61 |    0.27 |    7.79 |  2,907.19 | 86,330,753 | 101,707 |  1,177 | yet         | undetermined |
    | **necessarily~indicative**  | 1,456 |      8.38 |    1,447.62 |    0.11 |    7.40 | 12,331.98 | 86,330,753 |  56,696 | 12,760 | necessarily | indicative   |
    | **ever~watchful**           |   457 |      3.15 |      453.85 |    0.21 |    7.11 |  3,744.88 | 86,330,753 | 124,592 |  2,183 | ever        | watchful     |
    | **yet~unidentified**        |   362 |      2.37 |      359.63 |    0.18 |    7.10 |  2,991.31 | 86,330,753 | 101,707 |  2,012 | yet         | unidentified |
    | **only~temporary**          | 5,980 |     81.82 |    5,898.18 |    0.39 |    6.78 | 42,280.75 | 86,330,753 | 464,174 | 15,218 | only        | temporary    |
    | **yet~undiscovered**        |   319 |      3.02 |      315.98 |    0.12 |    6.46 |  2,383.41 | 86,330,753 | 101,707 |  2,561 | yet         | undiscovered |
    | **inherently~unequal**      |   423 |      4.02 |      418.98 |    0.07 |    6.43 |  3,132.80 | 86,330,753 |  55,088 |  6,300 | inherently  | unequal      |
    | **only~so-so**              |   274 |      3.95 |      270.05 |    0.37 |    6.20 |  1,897.98 | 86,330,753 | 464,174 |    735 | only        | so-so        |
    | **only~momentary**          |   207 |      2.89 |      204.11 |    0.38 |    6.18 |  1,450.10 | 86,330,753 | 464,174 |    538 | only        | momentary    |
    | **remotely~comparable**     |   391 |      4.29 |      386.71 |    0.02 |    6.16 |  2,771.17 | 86,330,753 |  22,194 | 16,686 | remotely    | comparable   |
    | **ever~closer**             | 6,882 |    101.45 |    6,780.55 |    0.10 |    6.14 | 45,537.24 | 86,330,753 | 124,592 | 70,294 | ever        | closer       |
    





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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>yet~unborn</th>
      <td>463</td>
      <td>0.75</td>
      <td>462.25</td>
      <td>0.73</td>
      <td>10.47</td>
      <td>5,505.48</td>
      <td>86330753</td>
      <td>101707</td>
      <td>635</td>
      <td>yet</td>
      <td>unborn</td>
    </tr>
    <tr>
      <th>only~half-joking</th>
      <td>209</td>
      <td>1.17</td>
      <td>207.83</td>
      <td>0.96</td>
      <td>9.48</td>
      <td>2,116.01</td>
      <td>86330753</td>
      <td>464174</td>
      <td>217</td>
      <td>only</td>
      <td>half-joking</td>
    </tr>
    <tr>
      <th>inherently~governmental</th>
      <td>295</td>
      <td>0.60</td>
      <td>294.40</td>
      <td>0.32</td>
      <td>8.96</td>
      <td>3,178.72</td>
      <td>86330753</td>
      <td>55088</td>
      <td>933</td>
      <td>inherently</td>
      <td>governmental</td>
    </tr>
    <tr>
      <th>immediately~accretive</th>
      <td>243</td>
      <td>0.68</td>
      <td>242.32</td>
      <td>0.43</td>
      <td>8.65</td>
      <td>2,499.70</td>
      <td>86330753</td>
      <td>103177</td>
      <td>565</td>
      <td>immediately</td>
      <td>accretive</td>
    </tr>
    <tr>
      <th>exactly~alike</th>
      <td>3040</td>
      <td>9.46</td>
      <td>3,030.54</td>
      <td>0.23</td>
      <td>8.55</td>
      <td>29,939.32</td>
      <td>86330753</td>
      <td>61599</td>
      <td>13261</td>
      <td>exactly</td>
      <td>alike</td>
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
    </tr>
    <tr>
      <th>only~high</th>
      <td>327</td>
      <td>3,177.51</td>
      <td>-2,850.51</td>
      <td>-0.00</td>
      <td>-2.86</td>
      <td>-4,245.38</td>
      <td>86330753</td>
      <td>464174</td>
      <td>590978</td>
      <td>only</td>
      <td>high</td>
    </tr>
    <tr>
      <th>only~sure</th>
      <td>339</td>
      <td>4,543.20</td>
      <td>-4,204.20</td>
      <td>-0.01</td>
      <td>-3.34</td>
      <td>-6,708.28</td>
      <td>86330753</td>
      <td>464174</td>
      <td>844981</td>
      <td>only</td>
      <td>sure</td>
    </tr>
    <tr>
      <th>ever~many</th>
      <td>206</td>
      <td>3,193.77</td>
      <td>-2,987.77</td>
      <td>-0.00</td>
      <td>-3.42</td>
      <td>-4,923.30</td>
      <td>86330753</td>
      <td>124592</td>
      <td>2212989</td>
      <td>ever</td>
      <td>many</td>
    </tr>
    <tr>
      <th>particularly~different</th>
      <td>349</td>
      <td>6,070.21</td>
      <td>-5,721.21</td>
      <td>-0.01</td>
      <td>-3.72</td>
      <td>-9,542.66</td>
      <td>86330753</td>
      <td>575961</td>
      <td>909864</td>
      <td>particularly</td>
      <td>different</td>
    </tr>
    <tr>
      <th>only~many</th>
      <td>480</td>
      <td>11,898.56</td>
      <td>-11,418.56</td>
      <td>-0.01</td>
      <td>-4.29</td>
      <td>-20,101.74</td>
      <td>86330753</td>
      <td>464174</td>
      <td>2212989</td>
      <td>only</td>
      <td>many</td>
    </tr>
  </tbody>
</table>
<p>1197 rows × 11 columns</p>
</div>




```python
def load_hit_table(adv_set): 
    
    # hit_df = pd.read_pickle(HITS_PATH).filter(regex=r'^[nab].*lower|text|str|head')
    # hit_df = pd.read_pickle(HITS_PATH)
    if HITS_SAMPLE_PATH.is_file(): 
        hit_df = pd.read_pickle(HITS_SAMPLE_PATH)
    else: 
        dfs = [ ]
        for i,p in enumerate(Path('/share/compling/data/sanpi/2_hit_tables/RBXadj/simple').iterdir()):
            if i  > K: 
                break
            _df = pd.read_pickle(p).filter(regex=r'^[nab].*lower|text|str|head')

            _df = _df.loc[_df.adv_form_lower.isin(adv_set), :]
            _df = _df.drop_duplicates()
            word_cols = _df.filter(regex=r'head|lower').columns
            _df[word_cols] = _df[word_cols].astype('category')
            dfs.append(_df)
        hit_df = pd.concat(dfs)
        hit_df.to_pickle(TOP_AM_DIR.joinpath(f'top{K}adv_sample-{K}-hit-tables_{DATE}.pkl.gz'))
    return  hit_df
hits_df = load_hit_table(adv_list)
nb_print_table(hits_df.sort_index(axis=1).sample(13).iloc[:, :4])
```

    
    |                                            | `adj_form_lower`   | `adv_form_lower`   | `bigrlower`                  | `text_window`                                                  |
    |:-------------------------------------------|:-------------------|:-------------------|:-----------------------------|:---------------------------------------------------------------|
    | **pcc_eng_12_098.2799_x1572119_06:09-10**  | entertaining       | particularly       | particularly_entertaining    | Richard Vincent is particularly entertaining as Doody with     |
    | **apw_eng_20051018_0069_17:4-5**           | clear              | yet                | yet_clear                    | it 's not yet clear how that will                              |
    | **pcc_eng_06_016.0675_x0243655_21:13-14**  | christian          | only               | only_christian               | the first and only Christian in the community                  |
    | **apw_eng_20090103_0433_13:3-4**           | strong             | that               | that_strong                  | it was that strong . ''                                        |
    | **pcc_eng_18_061.1285_x0973304_08:4-5**    | depressed          | terribly           | terribly_depressed           | With you so terribly depressed Could I still                   |
    | **pcc_eng_19_055.9451_x0886821_23:28-29**  | worse              | only               | only_worse                   | be it 's only worse .                                          |
    | **nyt_eng_19970512_0570_15:4-5**           | well-positioned    | particularly       | particularly_well-positioned | `` They 're particularly well-positioned overseas because they |
    | **pcc_eng_08_104.3954_x1674148_049:32-33** | greater            | ever               | ever_greater                 | the way towards ever greater output and payload                |
    | **apw_eng_20070831_0188_3:8-9**            | clear              | immediately        | immediately_clear            | spill was not immediately clear , although Velez               |
    | **apw_eng_20060624_0121_29:6-7**           | conservative       | inherently         | inherently_conservative      | Asian nations are inherently conservative .                    |
    | **nyt_eng_19991028_0276_6:19-20**          | able               | only               | only_able                    | yet and was only able to release a                             |
    | **pcc_eng_08_068.4743_x1092604_19:3-4**    | informative        | particularly       | particularly_informative     | These proved particularly informative because , as             |
    | **pcc_eng_19_034.8848_x0546940_52:5-6**    | strange            | particularly       | particularly_strange         | scene is n't particularly strange on its own                   |
    


## Set adverb and collect specific values


```python
def collect_examples(amdf, 
                     hits_df, 
                     adv: str = 'exactly', 
                     n_bigrams: int = K, 
                     n_examples: int = 50, 
                     metric: str = 'LRC') -> dict:
    df = amdf.copy().filter(like=adv, axis=0).nlargest(n_bigrams, metric)
    examples = {}
    for i, adj in enumerate(df['l2'].unique(), start=1):
        bigram = f'{adv}_{adj}'
        print(f'\n({i}) {bigram}')
        examples[bigram] = sp(
            data=hits_df, print_sample=False, 
            sample_size=n_examples, quiet=True,
            filters=[f'bigram_lower=={bigram}'],
            columns=['bigram_lower', 'text_window', 'token_str'])
        print('    > ', examples[bigram].sample(1).token_str.squeeze())
    return examples
```


```python
for adverb in adv_am.index: 
    print(f'\n## *{adverb}*\n')
    nb_print_table(adv_adj_am.filter(like=adverb, axis=0).nlargest(BK, 'LRC'), n_dec=2)
    examples = collect_examples(adv_adj_am, hits_df, adv=adverb, metric='LRC')
    
    output_dir = TOP_AM_DIR / 'any_bigram_examples' / adverb
    confirm_dir(output_dir)
    print(f'\nSaving Samples in {output_dir}/...')

    paths = []
    for key, df in examples.items(): 
        out_path = output_dir.joinpath(f'{key}_50ex.csv')
        df.to_csv(out_path)
        paths.append(out_path)
    print_iter(paths, header='\nSamples saved as...', bullet='+')
```

    
    ## *exactly*
    
    
    |                       |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`    | `l2`      |
    |:----------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|-------:|--------:|:--------|:----------|
    | **exactly~alike**     | 3,040 |      9.46 |    3,030.54 |    0.23 |    8.55 | 29,939.32 | 86,330,753 | 61,599 |  13,261 | exactly | alike     |
    | **exactly~opposite**  |   498 |      6.71 |      491.29 |    0.05 |    5.94 |  3,337.27 | 86,330,753 | 61,599 |   9,404 | exactly | opposite  |
    | **exactly~right**     | 6,948 |    145.97 |    6,802.03 |    0.03 |    5.53 | 41,085.55 | 86,330,753 | 61,599 | 204,572 | exactly | right     |
    | **exactly~zero**      |   344 |      8.19 |      335.81 |    0.03 |    5.02 |  1,912.07 | 86,330,753 | 61,599 |  11,472 | exactly | zero      |
    | **exactly~parallel**  |   224 |      5.41 |      218.59 |    0.03 |    4.90 |  1,238.35 | 86,330,753 | 61,599 |   7,577 | exactly | parallel  |
    | **exactly~sure**      | 9,301 |    602.91 |    8,698.09 |    0.01 |    3.89 | 34,895.53 | 86,330,753 | 61,599 | 844,981 | exactly | sure      |
    | **exactly~equal**     |   560 |     33.61 |      526.39 |    0.01 |    3.75 |  2,108.45 | 86,330,753 | 61,599 |  47,099 | exactly | equal     |
    | **exactly~conducive** |   214 |     11.71 |      202.29 |    0.01 |    3.68 |    842.32 | 86,330,753 | 61,599 |  16,405 | exactly | conducive |
    | **exactly~correct**   |   788 |     55.83 |      732.17 |    0.01 |    3.56 |  2,723.36 | 86,330,753 | 61,599 |  78,240 | exactly | correct   |
    | **exactly~ideal**     |   445 |     30.47 |      414.53 |    0.01 |    3.52 |  1,564.21 | 86,330,753 | 61,599 |  42,701 | exactly | ideal     |
    | **exactly~same**      |   493 |     40.09 |      452.91 |    0.01 |    3.29 |  1,575.37 | 86,330,753 | 61,599 |  56,190 | exactly | same      |
    
    
    (1) exactly_alike
        >  Can you imagine if we all looked exactly alike ?
    
    (2) exactly_opposite
        >  Clearly , this represents a major problem , as such behavior is exactly opposite of the formula for investing success .
    
    (3) exactly_right
        >  However , Matthews was exactly right .
    
    (4) exactly_zero
        >  For a team that has exactly zero trophies , putting one on display would be pretty nice .
    
    (5) exactly_parallel
        >  Their circumstances are not exactly parallel , but they are both women at very different points in their lives whose stories involve dilemmas with life-changing outcomes .
    
    (6) exactly_sure
        >  I am not exactly sure what the next phase of life will entail , but I am confident that all of the lessons I learned during my NFL journey will provide a solid foundation for success . "
    
    (7) exactly_equal
        >  Just as was the case last year , I have the Yankees and Red Sox almost exactly equal on paper .
    
    (8) exactly_conducive
        >  A 2 - 8 start to the season is n't exactly conducive to keeping one 's job in the NFL .
    
    (9) exactly_correct
        >  And yes , ' self - assembly ' is exactly correct .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_alike_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_opposite_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_right_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_zero_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_parallel_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_sure_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_equal_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_conducive_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_correct_50ex.csv
    
    ## *necessarily*
    
    
    |                                |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`        | `l2`           |
    |:-------------------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|-------:|--------:|:------------|:---------------|
    | **necessarily~indicative**     | 1,456 |      8.38 |    1,447.62 |    0.11 |    7.40 | 12,331.98 | 86,330,753 | 56,696 |  12,760 | necessarily | indicative     |
    | **necessarily~representative** |   524 |     16.54 |      507.46 |    0.02 |    4.68 |  2,621.46 | 86,330,753 | 56,696 |  25,187 | necessarily | representative |
    | **necessarily~true**           | 3,786 |    229.19 |    3,556.81 |    0.01 |    3.94 | 14,387.45 | 86,330,753 | 56,696 | 348,994 | necessarily | true           |
    | **necessarily~evil**           |   273 |     20.19 |      252.81 |    0.01 |    3.30 |    919.56 | 86,330,753 | 56,696 |  30,742 | necessarily | evil           |
    | **necessarily~illegal**        |   307 |     28.91 |      278.09 |    0.01 |    2.98 |    897.54 | 86,330,753 | 56,696 |  44,028 | necessarily | illegal        |
    | **necessarily~related**        |   842 |     90.41 |      751.59 |    0.01 |    2.96 |  2,268.75 | 86,330,753 | 56,696 | 137,661 | necessarily | related        |
    | **necessarily~wrong**          | 1,110 |    123.28 |      986.72 |    0.01 |    2.95 |  2,927.86 | 86,330,753 | 56,696 | 187,720 | necessarily | wrong          |
    | **necessarily~bad**            | 2,646 |    366.15 |    2,279.85 |    0.00 |    2.71 |  6,009.62 | 86,330,753 | 56,696 | 557,528 | necessarily | bad            |
    | **necessarily~better**         | 2,373 |    488.17 |    1,884.83 |    0.00 |    2.13 |  3,803.67 | 86,330,753 | 56,696 | 743,338 | necessarily | better         |
    | **necessarily~negative**       |   247 |     40.45 |      206.55 |    0.00 |    2.13 |    482.11 | 86,330,753 | 56,696 |  61,599 | necessarily | negative       |
    | **necessarily~harmful**        |   200 |     32.65 |      167.35 |    0.00 |    2.08 |    391.30 | 86,330,753 | 56,696 |  49,723 | necessarily | harmful        |
    
    
    (1) necessarily_indicative
        >  Past results are not necessarily indicative of future performance .
    
    (2) necessarily_representative
        >  This research is n't necessarily representative of the general population since participants were selected on a volunteer basis , but it does support the argument for removing BDSM from the Diagnostic and Statistical Manual of Mental Disorders ( DSM ) .
    
    (3) necessarily_true
        >  Note that neither is insisting - though they probably believe that it is - that what the religious leader preaches is necessarily true .
    
    (4) necessarily_evil
        >  I do n't think Redcoats were necessarily evil and also the weaponry of the time does n't suit shooters , so I think you need to have a different genre of game to tackle them .
    
    (5) necessarily_illegal
        >  Bloomberg 's other anti-gun group , Mayors Against Illegal Guns , started to lose support when some felt that the goal was more about all guns and not necessarily illegal guns .
    
    (6) necessarily_related
        >  The same report also outlined a response from New York City mayor Bill de Blasio , who confirmed that prisoners were burying people there , but maintained that it was not necessarily related to the state 's deadly COVID -19 emergency .
    
    (7) necessarily_wrong
        >  I do n't think it is necessarily wrong to use the any of these techniques .
    
    (8) necessarily_bad
        >  Do Nothing Congresses are not necessarily bad as they are not passing more laws that end up harming Americans , reaching into our wallets , and restricting our rights .
    
    (9) necessarily_better
        >  Not necessarily better , not necessarily worse , but different .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_indicative_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_representative_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_true_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_evil_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_illegal_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_related_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_wrong_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_bad_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_better_50ex.csv
    
    ## *before*
    
    
    |                      |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |     `G2` |        `N` |   `f1` |    `f2` | `l1`   | `l2`      |
    |:---------------------|------:|----------:|------------:|--------:|--------:|---------:|-----------:|-------:|--------:|:-------|:----------|
    | **before~available** |   211 |      7.51 |      203.49 |    0.00 |    4.37 | 1,062.83 | 86,330,753 |    748 | 866,272 | before | available |
    
    
    (1) before_available
        >  Hulu exclusively offers fans seven popular TV shows never before available to U.S. audiences with the premieres of " Rev. , " " The Yard , " " Pramface , " " Derren Brown : Inside Your Mind , " " The Promise " and " Little Mosque , " along with the second season of the sci-fi thriller , " The Booth at the End . "
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/before/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/before/before_available_50ex.csv
    
    ## *that*
    
    
    |                     |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |    `f1` |    `f2` | `l1`   | `l2`       |
    |:--------------------|-------:|----------:|------------:|--------:|--------:|----------:|-----------:|--------:|--------:|:-------|:-----------|
    | **that~bad**        | 23,977 |  1,617.04 |   22,359.96 |    0.04 |    3.90 | 87,578.15 | 86,330,753 | 250,392 | 557,528 | that   | bad        |
    | **that~great**      | 14,577 |  1,104.72 |   13,472.28 |    0.04 |    3.71 | 49,495.75 | 86,330,753 | 250,392 | 380,889 | that   | great      |
    | **that~dissimilar** |    321 |     25.57 |      295.43 |    0.03 |    3.26 |  1,043.81 | 86,330,753 | 250,392 |   8,816 | that   | dissimilar |
    | **that~hard**       | 10,818 |  1,250.03 |    9,567.97 |    0.02 |    3.07 | 28,143.36 | 86,330,753 | 250,392 | 430,990 | that   | hard       |
    | **that~big**        |  8,864 |  1,037.48 |    7,826.52 |    0.02 |    3.05 | 22,799.11 | 86,330,753 | 250,392 | 357,705 | that   | big        |
    | **that~stupid**     |  1,669 |    194.48 |    1,474.52 |    0.02 |    2.94 |  4,268.04 | 86,330,753 | 250,392 |  67,052 | that   | stupid     |
    | **that~simple**     |  9,227 |  1,238.95 |    7,988.05 |    0.02 |    2.84 | 21,487.56 | 86,330,753 | 250,392 | 427,167 | that   | simple     |
    | **that~dumb**       |    501 |     63.40 |      437.60 |    0.02 |    2.67 |  1,205.74 | 86,330,753 | 250,392 |  21,858 | that   | dumb       |
    | **that~easy**       | 13,969 |  2,237.08 |   11,731.92 |    0.02 |    2.60 | 28,454.39 | 86,330,753 | 250,392 | 771,307 | that   | easy       |
    | **that~naive**      |    369 |     70.89 |      298.11 |    0.01 |    2.00 |    625.22 | 86,330,753 | 250,392 |  24,443 | that   | naive      |
    | **that~uncommon**   |    819 |    179.15 |      639.85 |    0.01 |    1.94 |  1,218.16 | 86,330,753 | 250,392 |  61,767 | that   | uncommon   |
    
    
    (1) that_bad
        >  What i'm trying to say is it is n't that bad when it comes to comparing the fast food to Americas fast food , it 's still bad for you but we are lucky none of that stuff like ammonium hydroxide and carbon monoxide is in our fast food .
    
    (2) that_great
        >  Even that , however , is not that great .
    
    (3) that_dissimilar
        >  Online A/B testing is n't that dissimilar to experiments that you most likely conducted in science class as a kid .
    
    (4) that_hard
        >  If what I have said so far makes sense , the math is n't that hard to do .
    
    (5) that_big
        >  I do n't imagine thawing it from frozen could be that big of a deal .
    
    (6) that_stupid
        >  maybe the kids , and the voters , are n't quite that stupid .
    
    (7) that_simple
        >  Life is n't that simple , so I try to make sure it is n't obvious who Colin 's soulmate is actually supposed to be .
    
    (8) that_dumb
        >  How could they be that dumb ?
    
    (9) that_easy
        >  Many new pickups have a step indent in their bumpers , but it 's not that easy to use .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_bad_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_great_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_dissimilar_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_hard_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_big_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_stupid_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_simple_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_dumb_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_easy_50ex.csv
    
    ## *remotely*
    
    
    |                          |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`     | `l2`        |
    |:-------------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|-------:|--------:|:---------|:------------|
    | **remotely~comparable**  |   391 |      4.29 |      386.71 |    0.02 |    6.16 |  2,771.17 | 86,330,753 | 22,194 |  16,686 | remotely | comparable  |
    | **remotely~plausible**   |   267 |      5.32 |      261.68 |    0.01 |    5.20 |  1,573.65 | 86,330,753 | 22,194 |  20,711 | remotely | plausible   |
    | **remotely~close**       | 2,558 |    123.47 |    2,434.53 |    0.01 |    4.24 | 10,928.77 | 86,330,753 | 22,194 | 480,288 | remotely | close       |
    | **remotely~related**     |   778 |     35.39 |      742.61 |    0.01 |    4.20 |  3,352.47 | 86,330,753 | 22,194 | 137,661 | remotely | related     |
    | **remotely~similar**     |   900 |     56.92 |      843.08 |    0.00 |    3.74 |  3,318.92 | 86,330,753 | 22,194 | 221,410 | remotely | similar     |
    | **remotely~interested**  | 1,252 |     93.71 |    1,158.29 |    0.00 |    3.53 |  4,240.14 | 86,330,753 | 22,194 | 364,497 | remotely | interested  |
    | **remotely~possible**    |   904 |     93.65 |      810.35 |    0.00 |    3.02 |  2,510.49 | 86,330,753 | 22,194 | 364,265 | remotely | possible    |
    | **remotely~funny**       |   265 |     37.96 |      227.04 |    0.00 |    2.34 |    578.50 | 86,330,753 | 22,194 | 147,658 | remotely | funny       |
    | **remotely~interesting** |   596 |    127.43 |      468.57 |    0.00 |    1.92 |    912.23 | 86,330,753 | 22,194 | 495,662 | remotely | interesting |
    | **remotely~familiar**    |   277 |     54.44 |      222.56 |    0.00 |    1.89 |    458.70 | 86,330,753 | 22,194 | 211,750 | remotely | familiar    |
    | **remotely~true**        |   420 |     89.72 |      330.28 |    0.00 |    1.86 |    641.31 | 86,330,753 | 22,194 | 348,994 | remotely | true        |
    
    
    (1) remotely_comparable
        >  Because anything even remotely comparable will cost you a whole lot more .
    
    (2) remotely_plausible
        >  ( A goodhearted hustler toting around the Great American Novel in his backpack , doling out just the wisdom Arthur needs to hear -- it's a testament to Shambry 's skill that the character seems even remotely plausible . )
    
    (3) remotely_close
        >  At least until TNA Impact demonstrates that it can at least maintain the 1.2- ish ratings it drew pre-January 4 . Nobody , including the brain trust at TNA , could have possibly believed TNA would have scored anything even remotely close to Raw 's numbers .
    
    (4) remotely_related
        >  We threw in so many things together , no matter how remotely related they are with each other , and hurled them to the enemy .
    
    (5) remotely_similar
        >  In a remotely similar but far more lethal vein , the 1,400 - year Sunni- Shiite rivalry is playing out in the streets of Baghdad , raising the specter of a breakup of Iraq into antagonistic states , one backed by Shiite Iran and the other by Saudi Arabia and other Sunni states .
    
    (6) remotely_interested
        >  Anyone who 's remotely interested in Spring has had their eye on Spring 5 for a while now .
    
    (7) remotely_possible
        >  It is n't remotely possible that mass prosperity can be achieved in an economic structure where just 500 corporations , managed solely for profit , control 40 % of global revenues .
    
    (8) remotely_funny
        >  The Anti-Defamation League ( ADL ) on Monday blasted an Oscars sketch in which potty -mouthed film star bear Ted joked about Jews in Hollywood , calling it " offensive and not remotely funny " .
    
    (9) remotely_interesting
        >  What 's in the president 's heart of hearts is unknowable and not remotely interesting .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_comparable_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_plausible_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_close_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_related_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_similar_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_interested_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_possible_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_funny_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_interesting_50ex.csv
    
    ## *yet*
    
    
    |                      |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |    `f1` |    `f2` | `l1`   | `l2`         |
    |:---------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|--------:|--------:|:-------|:-------------|
    | **yet~unborn**       |   463 |      0.75 |      462.25 |    0.73 |   10.47 |  5,505.48 | 86,330,753 | 101,707 |     635 | yet    | unborn       |
    | **yet~unnamed**      |   771 |      2.62 |      768.38 |    0.35 |    8.47 |  7,535.14 | 86,330,753 | 101,707 |   2,227 | yet    | unnamed      |
    | **yet~unspecified**  |   219 |      0.79 |      218.21 |    0.33 |    8.06 |  2,109.33 | 86,330,753 | 101,707 |     669 | yet    | unspecified  |
    | **yet~undetermined** |   317 |      1.39 |      315.61 |    0.27 |    7.79 |  2,907.19 | 86,330,753 | 101,707 |   1,177 | yet    | undetermined |
    | **yet~unidentified** |   362 |      2.37 |      359.63 |    0.18 |    7.10 |  2,991.31 | 86,330,753 | 101,707 |   2,012 | yet    | unidentified |
    | **yet~undiscovered** |   319 |      3.02 |      315.98 |    0.12 |    6.46 |  2,383.41 | 86,330,753 | 101,707 |   2,561 | yet    | undiscovered |
    | **yet~final**        |   699 |     11.38 |      687.62 |    0.07 |    5.75 |  4,436.69 | 86,330,753 | 101,707 |   9,657 | yet    | final        |
    | **yet~unpublished**  |   253 |      3.75 |      249.25 |    0.08 |    5.69 |  1,653.12 | 86,330,753 | 101,707 |   3,184 | yet    | unpublished  |
    | **yet~ready**        | 7,838 |    283.10 |    7,554.90 |    0.03 |    4.75 | 37,767.73 | 86,330,753 | 101,707 | 240,297 | yet    | ready        |
    | **yet~unseen**       |   295 |      8.71 |      286.29 |    0.04 |    4.68 |  1,517.77 | 86,330,753 | 101,707 |   7,393 | yet    | unseen       |
    | **yet~unknown**      | 2,334 |     84.50 |    2,249.50 |    0.03 |    4.67 | 11,113.66 | 86,330,753 | 101,707 |  71,727 | yet    | unknown      |
    
    
    (1) yet_unborn
        >  CUMMINGS : It is about generations yet unborn .
    
    (2) yet_unnamed
        >  based in connecticut , usa , scott falciglia shares his thoughts on the yet unnamed global revolution challenging western civilization .
    
    (3) yet_unspecified
        >  should the deal work out to less than $ 15 a share in cash , the shareholders would get an as yet unspecified number of shares in the company .
    
    (4) yet_undetermined
        >  a summit on the Congo due to take place in Lusaka Thursday was postponed to an as yet undetermined date .
    
    (5) yet_unidentified
        >  Unfortunately , many of the wonderfully weird animals included were as of yet unidentified .
    
    (6) yet_undiscovered
        >  The mutant forms of the virus , the paper 's authors from Brown University and University of TA 1/4 bingen hypothesize , might provide a grand diversion to help the main virus evade the immune system , or they could be attacking different cells than the main virus does in an as yet undiscovered way .
    
    (7) yet_final
        >  The agreement is subject to a physical , the person said yesterday , speaking on condition of anonymity to the Associated Press because the deal was not yet final .
    
    (8) yet_unpublished
        >  but today , Aetna said new , as yet unpublished studies show ThinPrep increases the detection of abnormal or precancerous cells .
    
    (9) yet_ready
        >  Nobody 's efforts ever came close to fulfilling the war-winning potential ascribed to strategic bombing by its ' air- minded ' European proponents , but then nobody thought the technology was yet ready for the job and in any case no European authority was willing or able to advocate the slaughter of countless civilians during an epoch that still considered warfare a civilised activity .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unborn_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unnamed_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unspecified_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_undetermined_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unidentified_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_undiscovered_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_final_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unpublished_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_ready_50ex.csv
    
    ## *ever*
    
    
    |                   |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |    `f1` |    `f2` | `l1`   | `l2`     |
    |:------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|--------:|--------:|:-------|:---------|
    | **ever~olympic**  |   229 |      0.76 |      228.24 |    0.43 |    8.37 |  2,273.22 | 86,330,753 | 124,592 |     529 | ever   | olympic  |
    | **ever~watchful** |   457 |      3.15 |      453.85 |    0.21 |    7.11 |  3,744.88 | 86,330,753 | 124,592 |   2,183 | ever   | watchful |
    | **ever~closer**   | 6,882 |    101.45 |    6,780.55 |    0.10 |    6.14 | 45,537.24 | 86,330,753 | 124,592 |  70,294 | ever   | closer   |
    | **ever~joint**    |   205 |      2.31 |      202.69 |    0.13 |    6.10 |  1,461.42 | 86,330,753 | 124,592 |   1,599 | ever   | joint    |
    | **ever~nearer**   |   245 |      3.18 |      241.82 |    0.11 |    5.92 |  1,673.29 | 86,330,753 | 124,592 |   2,203 | ever   | nearer   |
    | **ever~vigilant** | 1,017 |     15.67 |    1,001.33 |    0.09 |    5.91 |  6,588.66 | 86,330,753 | 124,592 |  10,857 | ever   | vigilant |
    | **ever~mindful**  |   935 |     19.85 |      915.15 |    0.07 |    5.40 |  5,442.33 | 86,330,753 | 124,592 |  13,757 | ever   | mindful  |
    | **ever~present**  | 7,639 |    183.67 |    7,455.33 |    0.06 |    5.38 | 42,946.87 | 86,330,753 | 124,592 | 127,265 | ever   | present  |
    | **ever~tighter**  |   437 |     11.33 |      425.67 |    0.05 |    4.97 |  2,365.89 | 86,330,753 | 124,592 |   7,851 | ever   | tighter  |
    | **ever~deeper**   | 1,940 |     61.07 |    1,878.93 |    0.04 |    4.88 |  9,774.43 | 86,330,753 | 124,592 |  42,313 | ever   | deeper   |
    | **ever~elusive**  |   594 |     21.72 |      572.28 |    0.04 |    4.51 |  2,811.05 | 86,330,753 | 124,592 |  15,047 | ever   | elusive  |
    
    
    (1) ever_olympic
        >  Officials from The International Amateur Boxing Association ( AIBA ) nearly incited fisticuffs when they implied that the first ever Olympic female boxers will be required to enter the ring in skirts .
    
    (2) ever_watchful
        >  Voucher legislation is n't going away anytime soon , which is why the ever watchful eye of Americans United will remain alert as we try to stop these bad bills well before they become law .
    
    (3) ever_closer
        >  Under-secured nuclear weapons and materials as well as other WMD materials are also being actively pursued by terrorists around the globe , edging the world ever closer to Armageddon .
    
    (4) ever_joint
        >  U.S. Air Force F-35A Joint Strike Fighter jets land at Kunsan Air Base , South Korea for participation in exercise Vigilant Ace 2018 , the largest ever joint aerial combat exercise between America and the Republic of Korea .
    
    (5) ever_nearer
        >  Lang never forgot the excitement he felt when he was given his Advent calendar at the beginning of each December , and how it reminded him every day that the greatest celebration of the whole year was approaching ever nearer .
    
    (6) ever_vigilant
        >  No one app is going to make an Android device immediately safe from any and all threats , but some can make it easier to remain ever vigilant .
    
    (7) ever_mindful
        >  We must remain ever mindful of the narrow scope represented in our own cultures , and always open to taking the perspective of others we hope to serve .
    
    (8) ever_present
        >  Mrs. Eddy speaks of it as " Immanuel , or ' God with us , ' - a divine influence ever present in human consciousness and repeating itself , coming now as was promised aforetime ,
    
    (9) ever_tighter
        >  `` Industrialized countries should be asking themselves whether by imposing ever tighter restrictions on asylum seekers they are not closing their doors to men , women and children fleeing persecution , '' Guterres said in a statement .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_olympic_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_watchful_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_closer_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_joint_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_nearer_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_vigilant_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_mindful_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_present_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_tighter_50ex.csv
    
    ## *immediately*
    
    
    |                              |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |       `G2` |        `N` |    `f1` |    `f2` | `l1`        | `l2`         |
    |:-----------------------------|-------:|----------:|------------:|--------:|--------:|-----------:|-----------:|--------:|--------:|:------------|:-------------|
    | **immediately~accretive**    |    243 |      0.68 |      242.32 |    0.43 |    8.65 |   2,499.70 | 86,330,753 | 103,177 |     565 | immediately | accretive    |
    | **immediately~adjacent**     |  1,714 |      6.49 |    1,707.51 |    0.31 |    8.37 |  16,336.57 | 86,330,753 | 103,177 |   5,427 | immediately | adjacent     |
    | **immediately~apparent**     |  5,260 |     76.61 |    5,183.39 |    0.08 |    6.12 |  34,820.38 | 86,330,753 | 103,177 |  64,104 | immediately | apparent     |
    | **immediately~clear**        | 27,066 |    586.94 |   26,479.06 |    0.05 |    5.57 | 163,404.00 | 86,330,753 | 103,177 | 491,108 | immediately | clear        |
    | **immediately~recognizable** |  1,891 |     46.08 |    1,844.92 |    0.05 |    5.25 |  10,481.04 | 86,330,753 | 103,177 |  38,560 | immediately | recognizable |
    | **immediately~available**    | 30,725 |  1,035.31 |   29,689.69 |    0.03 |    4.90 | 159,614.02 | 86,330,753 | 103,177 | 866,272 | immediately | available    |
    | **immediately~recognisable** |    381 |     11.11 |      369.89 |    0.04 |    4.76 |   1,970.36 | 86,330,753 | 103,177 |   9,293 | immediately | recognisable |
    | **immediately~evident**      |  1,466 |     72.77 |    1,393.23 |    0.02 |    4.16 |   6,069.42 | 86,330,753 | 103,177 |  60,888 | immediately | evident      |
    | **immediately~obvious**      |  4,305 |    231.26 |    4,073.74 |    0.02 |    4.13 |  17,278.24 | 86,330,753 | 103,177 | 193,498 | immediately | obvious      |
    | **immediately~noticeable**   |    953 |     48.25 |      904.75 |    0.02 |    4.09 |   3,904.94 | 86,330,753 | 103,177 |  40,372 | immediately | noticeable   |
    | **immediately~identifiable** |    552 |     30.23 |      521.77 |    0.02 |    3.89 |   2,176.81 | 86,330,753 | 103,177 |  25,293 | immediately | identifiable |
    
    
    (1) immediately_accretive
        >  " This tuck - in acquisition is immediately accretive to earnings and generates meaningful cash flow as well as a healthy rate of return .
    
    (2) immediately_adjacent
        >  The proposed project site is immediately adjacent to and south of the existing SBPP in the City of Chula Vista adjacent to the San Diego Bay .
    
    (3) immediately_apparent
        >  anger is a part of his persona , too , but in more layered , less immediately apparent ways .
    
    (4) immediately_clear
        >  it was n't immediately clear whether the problem originated there , or was linked to tensions between the rival Palestinian governments in the West Bank and Gaza Strip .
    
    (5) immediately_recognizable
        >  The plunger-muted cornet of Taylor Ho Bynum is immediately recognizable to fans who 've heard him playing around Boston for the past several years with the Fully Celebrated Orchestra , Aardvark , and other ensembles , as well as with his former Wesleyan instructor Anthony Braxton .
    
    (6) immediately_available
        >  We have a new 2017 Dufour 350 GL Adventure version for sale , in stock and immediately available at a very significant savings on RRP - further details available here .
    
    (7) immediately_recognisable
        >  You can see how designers have realised the importance of clarity and simplicity each in terms of producing the logo more immediately recognisable and as they have had to meet the demands of new technologies .
    
    (8) immediately_evident
        >  Although the performance enhancements of Jelly Bean are immediately evident and most welcome , there is little here to recommend it as an OS that works better on tablets of any size , especially if it comes to screens 10 ' ' or larger .
    
    (9) immediately_obvious
        >  At first glance , several immediately obvious comparisons can be made regarding simply Life Is Strange 's two main characters and their vampy counterparts .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_accretive_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_adjacent_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_apparent_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_clear_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognizable_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_available_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognisable_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_evident_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_obvious_50ex.csv
    
    ## *any*
    
    
    |                 |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |       `G2` |        `N` |   `f1` |    `f2` | `l1`   | `l2`    |
    |:----------------|-------:|----------:|------------:|--------:|--------:|-----------:|-----------:|-------:|--------:|:-------|:--------|
    | **any~clearer** |  1,053 |     14.58 |    1,038.42 |    0.08 |    6.05 |   7,030.69 | 86,330,753 | 94,153 |  13,369 | any    | clearer |
    | **any~happier** |  1,472 |     21.27 |    1,450.73 |    0.07 |    6.02 |   9,706.11 | 86,330,753 | 94,153 |  19,501 | any    | happier |
    | **any~closer**  |  3,911 |     76.66 |    3,834.34 |    0.05 |    5.63 |  23,460.34 | 86,330,753 | 94,153 |  70,294 | any    | closer  |
    | **any~safer**   |  1,471 |     29.21 |    1,441.79 |    0.05 |    5.53 |   8,748.49 | 86,330,753 | 94,153 |  26,779 | any    | safer   |
    | **any~weirder** |    218 |      3.52 |      214.48 |    0.07 |    5.52 |   1,385.02 | 86,330,753 | 94,153 |   3,228 | any    | weirder |
    | **any~better**  | 35,471 |    810.69 |   34,660.31 |    0.05 |    5.49 | 215,244.70 | 86,330,753 | 94,153 | 743,338 | any    | better  |
    | **any~easier**  | 10,860 |    259.22 |   10,600.78 |    0.04 |    5.38 |  61,653.02 | 86,330,753 | 94,153 | 237,680 | any    | easier  |
    | **any~wiser**   |    245 |      4.70 |      240.30 |    0.06 |    5.28 |   1,471.06 | 86,330,753 | 94,153 |   4,309 | any    | wiser   |
    | **any~worse**   |  8,487 |    233.57 |    8,253.43 |    0.04 |    5.16 |  45,548.31 | 86,330,753 | 94,153 | 214,166 | any    | worse   |
    | **any~younger** |  1,121 |     32.51 |    1,088.49 |    0.04 |    4.93 |   5,813.90 | 86,330,753 | 94,153 |  29,805 | any    | younger |
    | **any~hotter**  |    291 |      8.22 |      282.78 |    0.04 |    4.74 |   1,521.90 | 86,330,753 | 94,153 |   7,537 | any    | hotter  |
    
    
    (1) any_clearer
        >  While this would reduce the timing of assessment , it might not make the novel food rules any clearer .
    
    (2) any_happier
        >  The Scots being dispossessed were not any happier about it than the Native Americans in the New World and they fought back , pretty briskly too .
    
    (3) any_closer
        >  the difference is that at the store you 're paying for somebody else 's interpretation of `` We Can Work It Out , '' and it may not be any closer to the original than Wright 's version .
    
    (4) any_safer
        >  is a grassroots coalition of groups and individuals united in our belief that a border wall will not stop illegal immigration or smuggling and will not make the United States any safer .
    
    (5) any_weirder
        >  But for the horses , it 's not any weirder than moving forward in response to bilateral leg pressure .
    
    (6) any_better
        >  Just because a girl now has a cell phone and a stylish haircut does n't mean that she is any better than her ancestors .
    
    (7) any_easier
        >  Keeping the faith of a mustard seed was not any easier .
    
    (8) any_wiser
        >  Giving birth one time did not really make me any wiser about it .
    
    (9) any_worse
        >  How could it get any worse ?
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_clearer_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_happier_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_closer_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_safer_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_weirder_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_better_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_easier_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_wiser_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_worse_50ex.csv
    
    ## *particularly*
    
    
    |                              |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |    `f1` |   `f2` | `l1`         | `l2`        |
    |:-----------------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|--------:|-------:|:-------------|:------------|
    | **particularly~galling**     |   573 |     15.55 |      557.45 |    0.24 |    5.23 |  3,165.46 | 86,330,753 | 575,961 |  2,331 | particularly | galling     |
    | **particularly~acute**       | 2,918 |    113.00 |    2,805.00 |    0.17 |    4.80 | 13,874.42 | 86,330,753 | 575,961 | 16,937 | particularly | acute       |
    | **particularly~noteworthy**  | 2,501 |    115.78 |    2,385.22 |    0.14 |    4.48 | 10,955.62 | 86,330,753 | 575,961 | 17,355 | particularly | noteworthy  |
    | **particularly~thorny**      |   328 |     12.96 |      315.04 |    0.16 |    4.46 |  1,544.42 | 86,330,753 | 575,961 |  1,942 | particularly | thorny      |
    | **particularly~fond**        | 4,445 |    265.59 |    4,179.41 |    0.11 |    4.10 | 17,178.32 | 86,330,753 | 575,961 | 39,809 | particularly | fond        |
    | **particularly~egregious**   | 1,896 |    114.43 |    1,781.57 |    0.10 |    4.02 |  7,281.73 | 86,330,753 | 575,961 | 17,152 | particularly | egregious   |
    | **particularly~nasty**       | 2,373 |    146.35 |    2,226.65 |    0.10 |    4.01 |  9,012.88 | 86,330,753 | 575,961 | 21,937 | particularly | nasty       |
    | **particularly~virulent**    |   527 |     32.58 |      494.42 |    0.10 |    3.82 |  1,997.47 | 86,330,753 | 575,961 |  4,884 | particularly | virulent    |
    | **particularly~worrisome**   | 1,096 |     76.54 |    1,019.46 |    0.09 |    3.73 |  3,891.11 | 86,330,753 | 575,961 | 11,473 | particularly | worrisome   |
    | **particularly~poignant**    | 1,700 |    122.86 |    1,577.14 |    0.09 |    3.73 |  5,922.99 | 86,330,753 | 575,961 | 18,416 | particularly | poignant    |
    | **particularly~troublesome** | 1,191 |     85.24 |    1,105.76 |    0.09 |    3.70 |  4,171.34 | 86,330,753 | 575,961 | 12,777 | particularly | troublesome |
    
    
    (1) particularly_galling
        >  This has been particularly galling for the NSO for the following reasons :
    
    (2) particularly_acute
        >  the dispute is particularly acute in Russia , which has thwarted John Paul 's hopes of visiting that country .
    
    (3) particularly_noteworthy
        >  The steep sides of the land around the fjord and the stillness of the water were particularly noteworthy .
    
    (4) particularly_thorny
        >  Design thinking turns up insights galore , and there is real value and skill to be had from synthesizing the messy , chaotic , confusing and often contradictory intellect of experts gathered from different fields to tackle a particularly thorny problem .
    
    (5) particularly_fond
        >  He 's particularly fond of the granola , which Nobrega tops with citrus zest and pinenuts .
    
    (6) particularly_egregious
        >  This is regarded as a particularly egregious affront to the voice of the majority and to fair representation in our country .
    
    (7) particularly_nasty
        >  Outside the Box : June 's work with some particularly nasty wounds has left her with the skill of spontaneous improvisation .
    
    (8) particularly_virulent
        >  but the prejudice was particularly virulent in Peru , where many Japanese arrived in the late 1800s mostly to farm and by the 1940s ran thriving businesses .
    
    (9) particularly_worrisome
        >  Magdych added that XPs large base of home users , who are generally inexperienced with security matters , makes this vulnerability particularly worrisome .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_galling_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_acute_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_noteworthy_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_thorny_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_fond_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_egregious_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_nasty_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_virulent_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_worrisome_50ex.csv
    
    ## *terribly*
    
    
    |                           |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`     | `l2`         |
    |:--------------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|-------:|--------:|:---------|:-------------|
    | **terribly~wrong**        | 7,248 |    152.59 |    7,095.41 |    0.04 |    5.54 | 42,791.46 | 86,330,753 | 70,174 | 187,720 | terribly | wrong        |
    | **terribly~sorry**        | 1,358 |     59.18 |    1,298.82 |    0.02 |    4.34 |  5,959.56 | 86,330,753 | 70,174 |  72,808 | terribly | sorry        |
    | **terribly~inefficient**  |   219 |      8.92 |      210.08 |    0.02 |    4.12 |    986.37 | 86,330,753 | 70,174 |  10,976 | terribly | inefficient  |
    | **terribly~sad**          | 1,354 |     89.78 |    1,264.22 |    0.01 |    3.72 |  4,857.19 | 86,330,753 | 70,174 | 110,447 | terribly | sad          |
    | **terribly~unfair**       |   411 |     24.28 |      386.72 |    0.01 |    3.72 |  1,559.12 | 86,330,753 | 70,174 |  29,870 | terribly | unfair       |
    | **terribly~lonely**       |   201 |     15.62 |      185.38 |    0.01 |    3.16 |    658.45 | 86,330,753 | 70,174 |  19,221 | terribly | lonely       |
    | **terribly~disappointed** |   721 |     69.42 |      651.58 |    0.01 |    3.10 |  2,082.92 | 86,330,753 | 70,174 |  85,399 | terribly | disappointed |
    | **terribly~flawed**       |   269 |     25.44 |      243.56 |    0.01 |    2.95 |    784.49 | 86,330,753 | 70,174 |  31,294 | terribly | flawed       |
    | **terribly~upset**        |   517 |     54.09 |      462.91 |    0.01 |    2.93 |  1,414.59 | 86,330,753 | 70,174 |  66,546 | terribly | upset        |
    | **terribly~surprising**   | 1,054 |    121.98 |      932.02 |    0.01 |    2.89 |  2,700.08 | 86,330,753 | 70,174 | 150,067 | terribly | surprising   |
    | **terribly~original**     |   293 |     37.17 |      255.83 |    0.01 |    2.54 |    700.56 | 86,330,753 | 70,174 |  45,732 | terribly | original     |
    
    
    (1) terribly_wrong
        >  She deleted it in no time but it went terribly wrong .
    
    (2) terribly_sorry
        >  `` I 'm terribly sorry to disturb you so early this morning with a loud noise , '' said Kanoko Komura , her dainty voice booming incongruously through the neighborhood .
    
    (3) terribly_inefficient
        >  The PA is deeply corrupt , terribly inefficient in its governance , and unwilling to divorce itself from the violence often done in the name of the Palestinian people it represents .
    
    (4) terribly_sad
        >  This one is n't offensive , just terribly sad .
    
    (5) terribly_unfair
        >  " I think [ clemency ] is an absolute moral and legal necessity in this case , " says Georgia State University College of Law professor Anne Emanuel , " if for no other reason than it is so terribly unfair to the jurors themselves , to allow this death penalty to proceed when the evidence on which they relied has now been disproved , and some of it withdrawn by the State itself . "
    
    (6) terribly_lonely
        >  Have been terribly lonely since my Paulie went fishing .
    
    (7) terribly_disappointed
        >  " I 'm terribly disappointed . "
    
    (8) terribly_flawed
        >  `` For the FBI , Ruby Ridge was a series of terribly flawed law enforcement operations with tragic consequences .
    
    (9) terribly_upset
        >  Saint - Exupery tells the story of a very thoughtful chap , who as a child learned only to draw boa constrictors from the inside and outside , and was terribly upset to find no one else fully appreciates his artwork .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_wrong_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_sorry_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_inefficient_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_sad_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_unfair_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_lonely_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_disappointed_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_flawed_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_upset_50ex.csv
    
    ## *inherently*
    
    
    |                             |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |     `G2` |        `N` |   `f1` |   `f2` | `l1`       | `l2`         |
    |:----------------------------|------:|----------:|------------:|--------:|--------:|---------:|-----------:|-------:|-------:|:-----------|:-------------|
    | **inherently~governmental** |   295 |      0.60 |      294.40 |    0.32 |    8.96 | 3,178.72 | 86,330,753 | 55,088 |    933 | inherently | governmental |
    | **inherently~unequal**      |   423 |      4.02 |      418.98 |    0.07 |    6.43 | 3,132.80 | 86,330,753 | 55,088 |  6,300 | inherently | unequal      |
    | **inherently~evil**         | 1,422 |     19.62 |    1,402.38 |    0.05 |    6.04 | 9,478.40 | 86,330,753 | 55,088 | 30,742 | inherently | evil         |
    | **inherently~unstable**     |   894 |     16.11 |      877.89 |    0.03 |    5.59 | 5,470.41 | 86,330,753 | 55,088 | 25,245 | inherently | unstable     |
    | **inherently~flawed**       | 1,028 |     19.97 |    1,008.03 |    0.03 |    5.49 | 6,138.46 | 86,330,753 | 55,088 | 31,294 | inherently | flawed       |
    | **inherently~unsafe**       |   297 |      6.19 |      290.81 |    0.03 |    5.18 | 1,728.45 | 86,330,753 | 55,088 |  9,693 | inherently | unsafe       |
    | **inherently~racist**       |   541 |     14.97 |      526.03 |    0.02 |    4.88 | 2,846.10 | 86,330,753 | 55,088 | 23,467 | inherently | racist       |
    | **inherently~unfair**       |   588 |     19.06 |      568.94 |    0.02 |    4.66 | 2,911.59 | 86,330,753 | 55,088 | 29,870 | inherently | unfair       |
    | **inherently~inferior**     |   275 |      8.18 |      266.82 |    0.02 |    4.64 | 1,406.64 | 86,330,753 | 55,088 | 12,817 | inherently | inferior     |
    | **inherently~unreliable**   |   206 |      5.98 |      200.02 |    0.02 |    4.60 | 1,063.31 | 86,330,753 | 55,088 |  9,370 | inherently | unreliable   |
    | **inherently~insecure**     |   229 |      7.03 |      221.97 |    0.02 |    4.55 | 1,157.21 | 86,330,753 | 55,088 | 11,010 | inherently | insecure     |
    
    
    (1) inherently_governmental
        >  But a coalition of 14 Defense unions is arguing that all employees working on the waterways perform inherently governmental work .
    
    (2) inherently_unequal
        >  In a unanimous ruling , the court found that " separate educational facilities are inherently unequal . "
    
    (3) inherently_evil
        >  Nothing inanimate is inherently evil , it 's all down to how it 's used .
    
    (4) inherently_unstable
        >  forging a rightist coalition would mean the inclusion of the novice legislators from Pim Fortuyn 's List , seen as an inherently unstable group with no natural leader after Fortuyn 's death and lacking a cohesive ideology .
    
    (5) inherently_flawed
        >  People and media that carry heteronormative perspectives see those who do not fit this perspective as inherently flawed or inferior .
    
    (6) inherently_unsafe
        >  the board said it supports launching the next shuttle at `` the earliest date '' consistent with safety , '' and said the shuttle is `` not inherently unsafe . ''
    
    (7) inherently_racist
        >  Which would suggest that we are all inherently racist to a degree .
    
    (8) inherently_unfair
        >  NOt GuiLTy ! '' -LRB- sic -RRB- `` It is inherently unfair to try an acquitted defendant on the same facts , but with a different standard of evidence and with a different numerical requirement to reach a verdict .
    
    (9) inherently_inferior
        >  If you believe a race of people are inherently inferior , you 're a racist .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_governmental_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unequal_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_evil_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unstable_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_flawed_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unsafe_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_racist_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unfair_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_inferior_50ex.csv
    
    ## *altogether*
    
    
    |                           |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |   `f1` |    `f2` | `l1`       | `l2`       |
    |:--------------------------|------:|----------:|------------:|--------:|--------:|----------:|-----------:|-------:|--------:|:-----------|:-----------|
    | **altogether~different**  | 5,068 |    217.49 |    4,850.51 |    0.01 |    4.46 | 23,495.10 | 86,330,753 | 20,636 | 909,864 | altogether | different  |
    | **altogether~surprising** |   542 |     35.87 |      506.13 |    0.00 |    3.60 |  1,945.41 | 86,330,753 | 20,636 | 150,067 | altogether | surprising |
    | **altogether~new**        | 1,030 |     76.80 |      953.20 |    0.00 |    3.52 |  3,489.21 | 86,330,753 | 20,636 | 321,311 | altogether | new        |
    | **altogether~clear**      |   359 |    117.39 |      241.61 |    0.00 |    1.21 |    322.34 | 86,330,753 | 20,636 | 491,108 | altogether | clear      |
    
    
    (1) altogether_different
        >  An altogether different recipe and profile than Sazerac Rye , this recipe contains just rye and malted barley , no corn .
    
    (2) altogether_surprising
        >  after that , it is n't altogether surprising that , even as she does her best to publicize her latest movie , she reserves the right to remain circumspect .
    
    (3) altogether_new
        >  Those species are , Yong suggests , just some of " the many secrets that are still locked within their drawers and dioramas , " secrets that will only be revealed and studied if we increase our attention on museum archives and stockrooms not as known quantities , but as potential resources of the altogether new and undocumented .
    
    (4) altogether_clear
        >  It 's first recorded in 1907 ; where it comes from is not altogether clear , but a popular ballad , Paddy Malone in Australia , was noted in the 1870s and appeared in a collection by Banjo Paterson in 1906 .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_different_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_surprising_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_new_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_clear_50ex.csv
    
    ## *only*
    
    
    |                      |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `LRC` |      `G2` |        `N` |    `f1` |    `f2` | `l1`   | `l2`        |
    |:---------------------|-------:|----------:|------------:|--------:|--------:|----------:|-----------:|--------:|--------:|:-------|:------------|
    | **only~half-joking** |    209 |      1.17 |      207.83 |    0.96 |    9.48 |  2,116.01 | 86,330,753 | 464,174 |     217 | only   | half-joking |
    | **only~temporary**   |  5,980 |     81.82 |    5,898.18 |    0.39 |    6.78 | 42,280.75 | 86,330,753 | 464,174 |  15,218 | only   | temporary   |
    | **only~so-so**       |    274 |      3.95 |      270.05 |    0.37 |    6.20 |  1,897.98 | 86,330,753 | 464,174 |     735 | only   | so-so       |
    | **only~momentary**   |    207 |      2.89 |      204.11 |    0.38 |    6.18 |  1,450.10 | 86,330,753 | 464,174 |     538 | only   | momentary   |
    | **only~approximate** |    238 |      5.05 |      232.95 |    0.25 |    5.40 |  1,431.38 | 86,330,753 | 464,174 |     940 | only   | approximate |
    | **only~occasional**  |    396 |      9.53 |      386.47 |    0.22 |    5.30 |  2,271.07 | 86,330,753 | 464,174 |   1,772 | only   | occasional  |
    | **only~advisory**    |    241 |      5.88 |      235.12 |    0.21 |    5.15 |  1,374.41 | 86,330,753 | 464,174 |   1,094 | only   | advisory    |
    | **only~natural**     | 16,324 |    642.39 |   15,681.61 |    0.13 |    4.81 | 76,966.08 | 86,330,753 | 464,174 | 119,476 | only   | natural     |
    | **only~partial**     |    885 |     32.75 |      852.25 |    0.14 |    4.70 |  4,257.88 | 86,330,753 | 464,174 |   6,092 | only   | partial     |
    | **only~halfway**     |    282 |      9.41 |      272.59 |    0.16 |    4.65 |  1,417.47 | 86,330,753 | 464,174 |   1,751 | only   | halfway     |
    | **only~lukewarm**    |    314 |     11.32 |      302.68 |    0.14 |    4.55 |  1,527.40 | 86,330,753 | 464,174 |   2,106 | only   | lukewarm    |
    
    
    (1) only_half-joking
        >  `` One lives always looking up at the sky , and listening to see if the coyote barks or the rooster crows , '' said the elder Rodriguez , only half-joking about folklore local farmers use to forecast wet weather .
    
    (2) only_temporary
        >  For some Pinellas waste , stay at landfill only temporary
    
    (3) only_so-so
        >  Unfortunately , the tileset never changes , the color scheme is a bit ugly , and the music is only so-so .
    
    (4) only_momentary
        >  With regard to profusion , the principle which prompts to expense is the passion for present enjoyment ; which , though sometimes violent and very difficult to be restrained , is in general only momentary and occasional .
    
    (5) only_approximate
        >  However sometimes this will not always be possible and any delivery or dispatch date given is only approximate and as the seller will not be liable to the Buyer for failure to deliver on any particular date or dates .
    
    (6) only_occasional
        >  he displayed only occasional flashes of the brilliance for which he is known .
    
    (7) only_advisory
        >  It is worth noting that the stricter international standards are only advisory , and that states that are part of the agreement can incorporate the new standards into law at their discretion .
    
    (8) only_natural
        >  `` That 's only natural , but it 's never very smooth . ''
    
    (9) only_partial
        >  In 1976 the employers stepped up their offensive and imposed a wage cut by making indexation only partial .
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/...
    
    Samples saved as...
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_half-joking_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_temporary_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_so-so_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_momentary_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_approximate_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_occasional_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_advisory_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_natural_50ex.csv
    + /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_partial_50ex.csv

