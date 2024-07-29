```python
from pathlib import Path

import pandas as pd
from am_notebooks import *

from source.utils import (HIT_TABLES_DIR, confirm_dir, print_iter,
                          timestamp_today)
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.dataframes import write_part_parquet as parq_it, catify_hit_table as catify
from source.utils.sample import sample_pickle as sp

TAG='NEQ'
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
      <th>mean_f1</th>
      <th>mean_f2</th>
      <th>mean_expF</th>
      <th>mean_unexpF</th>
      <th>mean_P2</th>
      <th>mean_dP2</th>
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
      <td>0.50</td>
      <td>0.99</td>
      <td>6.77</td>
      <td>56,251.14</td>
      <td>0.30</td>
      <td>2.17</td>
      <td>102.49</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>21,939.00</td>
      <td>10,969.42</td>
      <td>10,809.58</td>
      <td>0.01</td>
      <td>0.01</td>
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
      <td>6.26</td>
      <td>214,504.57</td>
      <td>0.30</td>
      <td>1.96</td>
      <td>200.61</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>85,617.50</td>
      <td>42,808.45</td>
      <td>41,729.55</td>
      <td>0.03</td>
      <td>0.03</td>
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
      <td>5.71</td>
      <td>54,870.72</td>
      <td>0.29</td>
      <td>1.81</td>
      <td>103.01</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>22,686.00</td>
      <td>11,342.92</td>
      <td>10,970.08</td>
      <td>0.01</td>
      <td>0.01</td>
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
      <td>3.91</td>
      <td>15,851.55</td>
      <td>0.28</td>
      <td>1.26</td>
      <td>58.57</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>8,666.50</td>
      <td>4,333.22</td>
      <td>3,891.78</td>
      <td>0.00</td>
      <td>0.00</td>
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
      <td>3.16</td>
      <td>5,075.57</td>
      <td>0.26</td>
      <td>1.05</td>
      <td>34.30</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>4,057.00</td>
      <td>2,028.48</td>
      <td>1,722.02</td>
      <td>0.00</td>
      <td>0.00</td>
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
      <td>4.52</td>
      <td>57,900.12</td>
      <td>0.28</td>
      <td>1.42</td>
      <td>109.45</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>27,150.00</td>
      <td>13,574.91</td>
      <td>12,518.59</td>
      <td>0.01</td>
      <td>0.01</td>
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
      <td>4.68</td>
      <td>63,920.54</td>
      <td>0.29</td>
      <td>1.47</td>
      <td>114.33</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>29,302.00</td>
      <td>14,650.90</td>
      <td>13,600.10</td>
      <td>0.01</td>
      <td>0.01</td>
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
      <td>1.37</td>
      <td>16,791.84</td>
      <td>0.16</td>
      <td>0.43</td>
      <td>74.04</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>43,095.50</td>
      <td>21,547.59</td>
      <td>10,837.41</td>
      <td>0.02</td>
      <td>0.02</td>
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
      <td>1.66</td>
      <td>2,929.13</td>
      <td>0.19</td>
      <td>0.56</td>
      <td>29.67</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>5,978.00</td>
      <td>2,988.98</td>
      <td>1,814.52</td>
      <td>0.01</td>
      <td>0.00</td>
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
      <td>3.10</td>
      <td>15,186.21</td>
      <td>0.26</td>
      <td>0.99</td>
      <td>60.07</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>11,003.00</td>
      <td>5,501.46</td>
      <td>4,256.54</td>
      <td>0.01</td>
      <td>0.00</td>
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
      <td>0.12</td>
      <td>91.19</td>
      <td>0.04</td>
      <td>0.08</td>
      <td>6.45</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>7,828.00</td>
      <td>3,913.97</td>
      <td>1,406.53</td>
      <td>0.01</td>
      <td>0.01</td>
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
    1. yet
    1. immediately
    1. particularly
    1. inherently
    1. terribly
    1. ever



## Top 8 Most Negative Adverbs
1. necessarily
1. that
1. exactly
1. any
1. remotely
1. yet
1. immediately
1. particularly
1. inherently
1. terribly
1. ever


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
adv_adj_am
```

    
    |                             |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |       `G2` |       `N` |   `f1` |   `f2` | `l1`        | `l2`         |
    |:----------------------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|-----------:|----------:|-------:|-------:|:------------|:-------------|
    | **inherently~governmental** |     40 |      0.09 |       39.91 |    0.57 |   0.57 |    0.00 |   0.00 |    8.02 |     432.85 | 6,347,364 |  8,614 |     70 | inherently  | governmental |
    | **exactly~late-career**     |     35 |      0.25 |       34.75 |    0.99 |   1.00 |    0.00 |   0.00 |    7.82 |     347.24 | 6,347,364 | 44,503 |     35 | exactly     | late-career  |
    | **any~happier**             |    834 |      5.13 |      828.87 |    0.41 |   0.42 |    0.05 |   0.05 |    7.76 |   7,282.99 | 6,347,364 | 16,238 |  2,004 | any         | happier      |
    | **necessarily~indicative**  |  1,389 |     15.63 |    1,373.37 |    0.59 |   0.60 |    0.03 |   0.03 |    7.46 |  10,827.28 | 6,347,364 | 42,886 |  2,313 | necessarily | indicative   |
    | **any~clearer**             |    371 |      2.49 |      368.51 |    0.38 |   0.38 |    0.02 |   0.02 |    7.39 |   3,147.58 | 6,347,364 | 16,238 |    972 | any         | clearer      |
    | **yet~final**               |    640 |     10.30 |      629.70 |    0.52 |   0.53 |    0.01 |   0.01 |    6.58 |   4,443.69 | 6,347,364 | 53,881 |  1,213 | yet         | final        |
    | **inherently~evil**         |    392 |      4.30 |      387.70 |    0.12 |   0.12 |    0.05 |   0.05 |    6.26 |   2,829.19 | 6,347,364 |  8,614 |  3,171 | inherently  | evil         |
    | **any~truer**               |     43 |      0.30 |       42.70 |    0.36 |   0.36 |    0.00 |   0.00 |    6.20 |     358.99 | 6,347,364 | 16,238 |    118 | any         | truer        |
    | **any~cuter**               |     47 |      0.38 |       46.62 |    0.32 |   0.32 |    0.00 |   0.00 |    6.01 |     376.68 | 6,347,364 | 16,238 |    148 | any         | cuter        |
    | **any~closer**              |    611 |      9.43 |      601.57 |    0.16 |   0.17 |    0.04 |   0.04 |    5.92 |   4,021.04 | 6,347,364 | 16,238 |  3,686 | any         | closer       |
    | **immediately~appealable**  |     31 |      0.37 |       30.63 |    0.77 |   0.77 |    0.00 |   0.00 |    5.85 |     248.60 | 6,347,364 | 58,040 |     40 | immediately | appealable   |
    | **any~worse**               |  1,762 |     31.00 |    1,731.00 |    0.14 |   0.15 |    0.11 |   0.11 |    5.85 |  11,229.25 | 6,347,364 | 16,238 | 12,116 | any         | worse        |
    | **inherently~wrong**        |  1,678 |     28.95 |    1,649.05 |    0.08 |   0.08 |    0.19 |   0.19 |    5.77 |  10,797.34 | 6,347,364 |  8,614 | 21,332 | inherently  | wrong        |
    | **yet~official**            |    352 |      7.84 |      344.16 |    0.37 |   0.38 |    0.01 |   0.01 |    5.63 |   2,141.31 | 6,347,364 | 53,881 |    924 | yet         | official     |
    | **any~simpler**             |    229 |      3.70 |      225.30 |    0.16 |   0.16 |    0.01 |   0.01 |    5.61 |   1,479.26 | 6,347,364 | 16,238 |  1,446 | any         | simpler      |
    | **any~easier**              |  1,625 |     32.94 |    1,592.06 |    0.12 |   0.13 |    0.10 |   0.10 |    5.61 |   9,854.27 | 6,347,364 | 16,238 | 12,877 | any         | easier       |
    | **any~younger**             |    255 |      4.56 |      250.44 |    0.14 |   0.14 |    0.02 |   0.02 |    5.47 |   1,591.82 | 6,347,364 | 16,238 |  1,784 | any         | younger      |
    | **any~safer**               |    255 |      4.70 |      250.30 |    0.14 |   0.14 |    0.02 |   0.02 |    5.42 |   1,575.71 | 6,347,364 | 16,238 |  1,838 | any         | safer        |
    | **immediately~clear**       | 24,488 |    770.17 |   23,717.83 |    0.29 |   0.29 |    0.41 |   0.42 |    5.41 | 141,124.54 | 6,347,364 | 58,040 | 84,227 | immediately | clear        |
    | **any~wiser**               |     71 |      0.99 |       70.01 |    0.18 |   0.18 |    0.00 |   0.00 |    5.34 |     480.95 | 6,347,364 | 16,238 |    386 | any         | wiser        |
    





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
      <th>inherently~governmental</th>
      <td>40</td>
      <td>0.09</td>
      <td>39.91</td>
      <td>0.57</td>
      <td>0.57</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>8.02</td>
      <td>432.85</td>
      <td>6347364</td>
      <td>8614</td>
      <td>70</td>
      <td>inherently</td>
      <td>governmental</td>
    </tr>
    <tr>
      <th>exactly~late-career</th>
      <td>35</td>
      <td>0.25</td>
      <td>34.75</td>
      <td>0.99</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>7.82</td>
      <td>347.24</td>
      <td>6347364</td>
      <td>44503</td>
      <td>35</td>
      <td>exactly</td>
      <td>late-career</td>
    </tr>
    <tr>
      <th>any~happier</th>
      <td>834</td>
      <td>5.13</td>
      <td>828.87</td>
      <td>0.41</td>
      <td>0.42</td>
      <td>0.05</td>
      <td>0.05</td>
      <td>7.76</td>
      <td>7,282.99</td>
      <td>6347364</td>
      <td>16238</td>
      <td>2004</td>
      <td>any</td>
      <td>happier</td>
    </tr>
    <tr>
      <th>necessarily~indicative</th>
      <td>1389</td>
      <td>15.63</td>
      <td>1,373.37</td>
      <td>0.59</td>
      <td>0.60</td>
      <td>0.03</td>
      <td>0.03</td>
      <td>7.46</td>
      <td>10,827.28</td>
      <td>6347364</td>
      <td>42886</td>
      <td>2313</td>
      <td>necessarily</td>
      <td>indicative</td>
    </tr>
    <tr>
      <th>any~clearer</th>
      <td>371</td>
      <td>2.49</td>
      <td>368.51</td>
      <td>0.38</td>
      <td>0.38</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>7.39</td>
      <td>3,147.58</td>
      <td>6347364</td>
      <td>16238</td>
      <td>972</td>
      <td>any</td>
      <td>clearer</td>
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
      <th>necessarily~much</th>
      <td>26</td>
      <td>726.34</td>
      <td>-700.34</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.02</td>
      <td>0.00</td>
      <td>-3.50</td>
      <td>-1,243.77</td>
      <td>6347364</td>
      <td>42886</td>
      <td>107503</td>
      <td>necessarily</td>
      <td>much</td>
    </tr>
    <tr>
      <th>yet~easy</th>
      <td>36</td>
      <td>924.62</td>
      <td>-888.62</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.02</td>
      <td>0.00</td>
      <td>-3.55</td>
      <td>-1,565.78</td>
      <td>6347364</td>
      <td>53881</td>
      <td>108923</td>
      <td>yet</td>
      <td>easy</td>
    </tr>
    <tr>
      <th>that~ready</th>
      <td>27</td>
      <td>776.82</td>
      <td>-749.82</td>
      <td>-0.03</td>
      <td>0.00</td>
      <td>-0.00</td>
      <td>0.00</td>
      <td>-3.59</td>
      <td>-1,341.07</td>
      <td>6347364</td>
      <td>166676</td>
      <td>29583</td>
      <td>that</td>
      <td>ready</td>
    </tr>
    <tr>
      <th>particularly~sure</th>
      <td>77</td>
      <td>1,609.53</td>
      <td>-1,532.53</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.02</td>
      <td>0.00</td>
      <td>-3.59</td>
      <td>-2,646.25</td>
      <td>6347364</td>
      <td>76162</td>
      <td>134139</td>
      <td>particularly</td>
      <td>sure</td>
    </tr>
    <tr>
      <th>immediately~easy</th>
      <td>28</td>
      <td>995.99</td>
      <td>-967.99</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.02</td>
      <td>0.00</td>
      <td>-3.89</td>
      <td>-1,761.11</td>
      <td>6347364</td>
      <td>58040</td>
      <td>108923</td>
      <td>immediately</td>
      <td>easy</td>
    </tr>
  </tbody>
</table>
<p>1783 rows × 14 columns</p>
</div>




|                             |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |       `G2` |       `N` |   `f1` |   `f2` | `l1`        | `l2`         |
|:----------------------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|-----------:|----------:|-------:|-------:|:------------|:-------------|
| **inherently~governmental** |     40 |      0.09 |       39.91 |    0.57 |   0.57 |    0.00 |   0.00 |    8.02 |     432.85 | 6,347,364 |  8,614 |     70 | inherently  | governmental |
| **exactly~late-career**     |     35 |      0.25 |       34.75 |    0.99 |   1.00 |    0.00 |   0.00 |    7.82 |     347.24 | 6,347,364 | 44,503 |     35 | exactly     | late-career  |
| **any~happier**             |    834 |      5.13 |      828.87 |    0.41 |   0.42 |    0.05 |   0.05 |    7.76 |   7,282.99 | 6,347,364 | 16,238 |  2,004 | any         | happier      |
| **necessarily~indicative**  |  1,389 |     15.63 |    1,373.37 |    0.59 |   0.60 |    0.03 |   0.03 |    7.46 |  10,827.28 | 6,347,364 | 42,886 |  2,313 | necessarily | indicative   |
| **any~clearer**             |    371 |      2.49 |      368.51 |    0.38 |   0.38 |    0.02 |   0.02 |    7.39 |   3,147.58 | 6,347,364 | 16,238 |    972 | any         | clearer      |
| **yet~final**               |    640 |     10.30 |      629.70 |    0.52 |   0.53 |    0.01 |   0.01 |    6.58 |   4,443.69 | 6,347,364 | 53,881 |  1,213 | yet         | final        |
| **inherently~evil**         |    392 |      4.30 |      387.70 |    0.12 |   0.12 |    0.05 |   0.05 |    6.26 |   2,829.19 | 6,347,364 |  8,614 |  3,171 | inherently  | evil         |
| **any~truer**               |     43 |      0.30 |       42.70 |    0.36 |   0.36 |    0.00 |   0.00 |    6.20 |     358.99 | 6,347,364 | 16,238 |    118 | any         | truer        |
| **any~cuter**               |     47 |      0.38 |       46.62 |    0.32 |   0.32 |    0.00 |   0.00 |    6.01 |     376.68 | 6,347,364 | 16,238 |    148 | any         | cuter        |
| **any~closer**              |    611 |      9.43 |      601.57 |    0.16 |   0.17 |    0.04 |   0.04 |    5.92 |   4,021.04 | 6,347,364 | 16,238 |  3,686 | any         | closer       |
| **immediately~appealable**  |     31 |      0.37 |       30.63 |    0.77 |   0.77 |    0.00 |   0.00 |    5.85 |     248.60 | 6,347,364 | 58,040 |     40 | immediately | appealable   |
| **any~worse**               |  1,762 |     31.00 |    1,731.00 |    0.14 |   0.15 |    0.11 |   0.11 |    5.85 |  11,229.25 | 6,347,364 | 16,238 | 12,116 | any         | worse        |
| **inherently~wrong**        |  1,678 |     28.95 |    1,649.05 |    0.08 |   0.08 |    0.19 |   0.19 |    5.77 |  10,797.34 | 6,347,364 |  8,614 | 21,332 | inherently  | wrong        |
| **yet~official**            |    352 |      7.84 |      344.16 |    0.37 |   0.38 |    0.01 |   0.01 |    5.63 |   2,141.31 | 6,347,364 | 53,881 |    924 | yet         | official     |
| **any~simpler**             |    229 |      3.70 |      225.30 |    0.16 |   0.16 |    0.01 |   0.01 |    5.61 |   1,479.26 | 6,347,364 | 16,238 |  1,446 | any         | simpler      |
| **any~easier**              |  1,625 |     32.94 |    1,592.06 |    0.12 |   0.13 |    0.10 |   0.10 |    5.61 |   9,854.27 | 6,347,364 | 16,238 | 12,877 | any         | easier       |
| **any~younger**             |    255 |      4.56 |      250.44 |    0.14 |   0.14 |    0.02 |   0.02 |    5.47 |   1,591.82 | 6,347,364 | 16,238 |  1,784 | any         | younger      |
| **any~safer**               |    255 |      4.70 |      250.30 |    0.14 |   0.14 |    0.02 |   0.02 |    5.42 |   1,575.71 | 6,347,364 | 16,238 |  1,838 | any         | safer        |
| **immediately~clear**       | 24,488 |    770.17 |   23,717.83 |    0.29 |   0.29 |    0.41 |   0.42 |    5.41 | 141,124.54 | 6,347,364 | 58,040 | 84,227 | immediately | clear        |
| **any~wiser**               |     71 |      0.99 |       70.01 |    0.18 |   0.18 |    0.00 |   0.00 |    5.34 |     480.95 | 6,347,364 | 16,238 |    386 | any         | wiser        |




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
        hit_df = pd.read_parquet(out_path, engine='pyarrow', filters=[
                                 ('adv_form_lower', 'in', adv_set)])
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
      <th>apw_eng_19980212_1044_26:27-28</th>
      <td>to see if mount fuji had looked any different during the different seasons o...</td>
      <td>or , if you prefer , you can click on images dating as far back as three yea...</td>
      <td>different</td>
      <td>any_different</td>
      <td>any</td>
    </tr>
    <tr>
      <th>apw_eng_20080813_1267_25:5-6</th>
      <td>`` if anybody said any different , they 'd be lying .</td>
      <td>`` If anybody said any different , they 'd be lying . ''</td>
      <td>different</td>
      <td>any_different</td>
      <td>any</td>
    </tr>
    <tr>
      <th>apw_eng_20061220_0102_11:5-6</th>
      <td>will this year be any different ?</td>
      <td>will this year be any different ?</td>
      <td>different</td>
      <td>any_different</td>
      <td>any</td>
    </tr>
    <tr>
      <th>apw_eng_20090204_1183_11:10-11</th>
      <td>the roughly 6-pound -lrb- 2.7-kilogram -rrb- xsapi any lighter is harder tha...</td>
      <td>but making the roughly 6-pound -LRB- 2.7-kilogram -RRB- XSAPI any lighter is...</td>
      <td>lighter</td>
      <td>any_lighter</td>
      <td>any</td>
    </tr>
    <tr>
      <th>apw_eng_19990603_0740_3:18-19</th>
      <td>cup and a draw by a score any greater than 0-0 will hand the title</td>
      <td>a victory by either Peru or Japan will win the cup and a draw by a score any...</td>
      <td>greater</td>
      <td>any_greater</td>
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
      <th>pcc_eng_20_087.5297_x1397883_05:4-5-6</th>
      <td>many retailers are not yet ready to trade internationally because there are</td>
      <td>Many retailers are not yet ready to trade internationally because there are ...</td>
      <td>ready</td>
      <td>yet_ready</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_20_080.3146_x1281464_16:5-6-7</th>
      <td>but i 'm just not yet ready to throw myself into it in</td>
      <td>But I 'm just not yet ready to throw myself into it in the way I need to be ...</td>
      <td>ready</td>
      <td>yet_ready</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_20_080.4329_x1283366_035:2-3-4</th>
      <td>" not yet dear , i want you to make</td>
      <td>" Not yet dear , I want you to make me cum all over my pantyhose before I le...</td>
      <td>dear</td>
      <td>yet_dear</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_20_081.3177_x1297627_33:23-24-25</th>
      <td>, but exactly how long is not yet clear .</td>
      <td>The study , he said , shows that longer duration of AI treatment is clinical...</td>
      <td>clear</td>
      <td>yet_clear</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>pcc_eng_20_081.5281_x1301048_04:17-18-19</th>
      <td>identify materials that are desired but not yet available . )</td>
      <td>( The term " unobtainium " is sometimes used to identify materials that are ...</td>
      <td>available</td>
      <td>yet_available</td>
      <td>yet</td>
    </tr>
  </tbody>
</table>
<p>165507 rows × 5 columns</p>
</div>




```python
# nb_show_table(hits_df.sort_index(axis=1).sample(13).iloc[:, :4])
```

    
    |                                               | `adj_form_lower`   | `adv_form_lower`   | `bigrlower`              | `text_window`                                                                         |
    |:----------------------------------------------|:-------------------|:-------------------|:-------------------------|:--------------------------------------------------------------------------------------|
    | **apw_eng_20021029_0626_12:5-6-7**            | large              | that               | that_large               | `` the differences are not that large that they would justify an escalation           |
    | **pcc_eng_21_035.7257_x0561652_08:3-4**       | interesting        | particularly       | particularly_interesting | what 's particularly interesting is that ( i'm guessing )                             |
    | **nyt_eng_20060331_0267_9:6-8-9**             | difficult          | that               | that_difficult           | answer : `` it has n't been that difficult .                                          |
    | **pcc_eng_23_007.7007_x0108230_060:19-20-21** | corrupt            | necessarily        | necessarily_corrupt      | good men , that power does not necessarily corrupt , that many good men exercised     |
    | **pcc_eng_00_065.8353_x1048085_099:3-4-5**    | common             | that               | that_common              | it 's not that common for the eardrum to burst open                                   |
    | **nyt_eng_20050404_0076_40:3-4-5**            | easy               | particularly       | particularly_easy        | it is n't particularly easy for hefty russian lifters to go                           |
    | **pcc_eng_01_041.1609_x0649050_099:7-8-9**    | hard               | that               | that_hard                | after all , le pen is n't that hard to argue with , is he                             |
    | **pcc_eng_15_046.5828_x0737043_25:15-17-18**  | easy               | that               | that_easy                | the online shopping experience is n't even that easy .                                |
    | **pcc_eng_16_084.2089_x1346893_057:15-16-17** | related            | necessarily        | necessarily_related      | of pain a woman experiences is not necessarily related to the severity of the disease |
    | **pcc_eng_04_050.5059_x0799859_15:3-4-5**     | impressed          | particularly       | particularly_impressed   | Simeone is not particularly impressed .                                               |
    | **pcc_eng_17_077.1600_x1230715_20:10-11-12**  | illegal            | necessarily        | necessarily_illegal      | the use of nuclear weapons was not necessarily illegal , if a state 's survival       |
    | **pcc_eng_17_070.6171_x1124869_34:14-15-16**  | funny              | particularly       | particularly_funny       | be shocked that the performances are n't particularly funny or noteworthy .           |
    | **pcc_eng_21_096.0503_x1535759_23:13-14-15**  | revelatory         | exactly            | exactly_revelatory       | if some of the revelations were n't exactly revelatory , at least not to me           |
    


```python
nb_show_table(hits_df.sort_index(axis=1).sample(13).iloc[:, :4])
```


|                                               | `adj_form_lower`   | `adv_form_lower`   | `bigrlower`              | `text_window`                                                                         |
|:----------------------------------------------|:-------------------|:-------------------|:-------------------------|:--------------------------------------------------------------------------------------|
| **apw_eng_20021029_0626_12:5-6-7**            | large              | that               | that_large               | `` the differences are not that large that they would justify an escalation           |
| **pcc_eng_21_035.7257_x0561652_08:3-4**       | interesting        | particularly       | particularly_interesting | what 's particularly interesting is that ( i'm guessing )                             |
| **nyt_eng_20060331_0267_9:6-8-9**             | difficult          | that               | that_difficult           | answer : `` it has n't been that difficult .                                          |
| **pcc_eng_23_007.7007_x0108230_060:19-20-21** | corrupt            | necessarily        | necessarily_corrupt      | good men , that power does not necessarily corrupt , that many good men exercised     |
| **pcc_eng_00_065.8353_x1048085_099:3-4-5**    | common             | that               | that_common              | it 's not that common for the eardrum to burst open                                   |
| **nyt_eng_20050404_0076_40:3-4-5**            | easy               | particularly       | particularly_easy        | it is n't particularly easy for hefty russian lifters to go                           |
| **pcc_eng_01_041.1609_x0649050_099:7-8-9**    | hard               | that               | that_hard                | after all , le pen is n't that hard to argue with , is he                             |
| **pcc_eng_15_046.5828_x0737043_25:15-17-18**  | easy               | that               | that_easy                | the online shopping experience is n't even that easy .                                |
| **pcc_eng_16_084.2089_x1346893_057:15-16-17** | related            | necessarily        | necessarily_related      | of pain a woman experiences is not necessarily related to the severity of the disease |
| **pcc_eng_04_050.5059_x0799859_15:3-4-5**     | impressed          | particularly       | particularly_impressed   | Simeone is not particularly impressed .                                               |
| **pcc_eng_17_077.1600_x1230715_20:10-11-12**  | illegal            | necessarily        | necessarily_illegal      | the use of nuclear weapons was not necessarily illegal , if a state 's survival       |
| **pcc_eng_17_070.6171_x1124869_34:14-15-16**  | funny              | particularly       | particularly_funny       | be shocked that the performances are n't particularly funny or noteworthy .           |
| **pcc_eng_21_096.0503_x1535759_23:13-14-15**  | revelatory         | exactly            | exactly_revelatory       | if some of the revelations were n't exactly revelatory , at least not to me           |





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
    # table_csv_path = output_dir / f'{adverb}_top{BK}-bigrams_AMscores_{timestamp_today()}.csv'
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
      <th>mean_f1</th>
      <th>mean_f2</th>
      <th>mean_expF</th>
      <th>mean_unexpF</th>
      <th>mean_P2</th>
      <th>mean_dP2</th>
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
      <td>0</td>
      <td>1</td>
      <td>7</td>
      <td>56,251</td>
      <td>0</td>
      <td>2</td>
      <td>102</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>21,939</td>
      <td>10,969</td>
      <td>10,810</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>that</th>
      <td>NEGany~that</td>
      <td>164768</td>
      <td>1</td>
      <td>1</td>
      <td>6</td>
      <td>214,505</td>
      <td>0</td>
      <td>2</td>
      <td>201</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>85,618</td>
      <td>42,808</td>
      <td>41,730</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>NEGany~exactly</td>
      <td>43813</td>
      <td>0</td>
      <td>1</td>
      <td>6</td>
      <td>54,871</td>
      <td>0</td>
      <td>2</td>
      <td>103</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>22,686</td>
      <td>11,343</td>
      <td>10,970</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>any</th>
      <td>NEGany~any</td>
      <td>15384</td>
      <td>0</td>
      <td>1</td>
      <td>4</td>
      <td>15,852</td>
      <td>0</td>
      <td>1</td>
      <td>59</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>8,666</td>
      <td>4,333</td>
      <td>3,892</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>NEGany~remotely</td>
      <td>5661</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>5,076</td>
      <td>0</td>
      <td>1</td>
      <td>34</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>4,057</td>
      <td>2,028</td>
      <td>1,722</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>NEGany~yet</td>
      <td>51867</td>
      <td>0</td>
      <td>1</td>
      <td>5</td>
      <td>57,900</td>
      <td>0</td>
      <td>1</td>
      <td>109</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>27,150</td>
      <td>13,575</td>
      <td>12,519</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>NEGany~immediately</td>
      <td>56099</td>
      <td>0</td>
      <td>1</td>
      <td>5</td>
      <td>63,921</td>
      <td>0</td>
      <td>1</td>
      <td>114</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>29,302</td>
      <td>14,651</td>
      <td>13,600</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>NEGany~particularly</td>
      <td>55527</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>16,792</td>
      <td>0</td>
      <td>0</td>
      <td>74</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>43,096</td>
      <td>21,548</td>
      <td>10,837</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>NEGany~inherently</td>
      <td>6743</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>2,929</td>
      <td>0</td>
      <td>1</td>
      <td>30</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>5,978</td>
      <td>2,989</td>
      <td>1,815</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>NEGany~terribly</td>
      <td>17949</td>
      <td>0</td>
      <td>1</td>
      <td>3</td>
      <td>15,186</td>
      <td>0</td>
      <td>1</td>
      <td>60</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>11,003</td>
      <td>5,501</td>
      <td>4,257</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>NEGany~ever</td>
      <td>5932</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>91</td>
      <td>0</td>
      <td>0</td>
      <td>6</td>
      <td>6347364</td>
      <td>...</td>
      <td>1732696</td>
      <td>7,828</td>
      <td>3,914</td>
      <td>1,407</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>11 rows × 53 columns</p>
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
      <th>inherently~governmental</th>
      <td>40</td>
      <td>0</td>
      <td>40</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>433</td>
      <td>6347364</td>
      <td>8614</td>
      <td>70</td>
      <td>inherently</td>
      <td>governmental</td>
    </tr>
    <tr>
      <th>exactly~late-career</th>
      <td>35</td>
      <td>0</td>
      <td>35</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>347</td>
      <td>6347364</td>
      <td>44503</td>
      <td>35</td>
      <td>exactly</td>
      <td>late-career</td>
    </tr>
    <tr>
      <th>any~happier</th>
      <td>834</td>
      <td>5</td>
      <td>829</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>7,283</td>
      <td>6347364</td>
      <td>16238</td>
      <td>2004</td>
      <td>any</td>
      <td>happier</td>
    </tr>
    <tr>
      <th>necessarily~indicative</th>
      <td>1389</td>
      <td>16</td>
      <td>1,373</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>7</td>
      <td>10,827</td>
      <td>6347364</td>
      <td>42886</td>
      <td>2313</td>
      <td>necessarily</td>
      <td>indicative</td>
    </tr>
    <tr>
      <th>any~clearer</th>
      <td>371</td>
      <td>2</td>
      <td>369</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>7</td>
      <td>3,148</td>
      <td>6347364</td>
      <td>16238</td>
      <td>972</td>
      <td>any</td>
      <td>clearer</td>
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
      <th>necessarily~much</th>
      <td>26</td>
      <td>726</td>
      <td>-700</td>
      <td>-0</td>
      <td>0</td>
      <td>-0</td>
      <td>0</td>
      <td>-3</td>
      <td>-1,244</td>
      <td>6347364</td>
      <td>42886</td>
      <td>107503</td>
      <td>necessarily</td>
      <td>much</td>
    </tr>
    <tr>
      <th>yet~easy</th>
      <td>36</td>
      <td>925</td>
      <td>-889</td>
      <td>-0</td>
      <td>0</td>
      <td>-0</td>
      <td>0</td>
      <td>-4</td>
      <td>-1,566</td>
      <td>6347364</td>
      <td>53881</td>
      <td>108923</td>
      <td>yet</td>
      <td>easy</td>
    </tr>
    <tr>
      <th>that~ready</th>
      <td>27</td>
      <td>777</td>
      <td>-750</td>
      <td>-0</td>
      <td>0</td>
      <td>-0</td>
      <td>0</td>
      <td>-4</td>
      <td>-1,341</td>
      <td>6347364</td>
      <td>166676</td>
      <td>29583</td>
      <td>that</td>
      <td>ready</td>
    </tr>
    <tr>
      <th>particularly~sure</th>
      <td>77</td>
      <td>1,610</td>
      <td>-1,533</td>
      <td>-0</td>
      <td>0</td>
      <td>-0</td>
      <td>0</td>
      <td>-4</td>
      <td>-2,646</td>
      <td>6347364</td>
      <td>76162</td>
      <td>134139</td>
      <td>particularly</td>
      <td>sure</td>
    </tr>
    <tr>
      <th>immediately~easy</th>
      <td>28</td>
      <td>996</td>
      <td>-968</td>
      <td>-0</td>
      <td>0</td>
      <td>-0</td>
      <td>0</td>
      <td>-4</td>
      <td>-1,761</td>
      <td>6347364</td>
      <td>58040</td>
      <td>108923</td>
      <td>immediately</td>
      <td>easy</td>
    </tr>
  </tbody>
</table>
<p>1783 rows × 14 columns</p>
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


|                                |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |       `N` |   `f1` |   `f2` | `l1`        | `l2`           |
|:-------------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|----------:|-------:|-------:|:------------|:---------------|
| **necessarily~indicative**     | 1,389 |     15.63 |    1,373.37 |    0.59 |   0.60 |    0.03 |   0.03 |    7.46 | 10,827.28 | 6,347,364 | 42,886 |  2,313 | necessarily | indicative     |
| **necessarily~cause**          |    52 |      0.91 |       51.09 |    0.38 |   0.39 |    0.00 |   0.00 |    5.07 |    341.90 | 6,347,364 | 42,886 |    134 | necessarily | cause          |
| **necessarily~representative** |   488 |     17.30 |      470.70 |    0.18 |   0.19 |    0.01 |   0.01 |    4.71 |  2,416.54 | 6,347,364 | 42,886 |  2,560 | necessarily | representative |
| **necessarily~synonymous**     |   165 |      6.37 |      158.63 |    0.17 |   0.17 |    0.00 |   0.00 |    4.26 |    785.72 | 6,347,364 | 42,886 |    943 | necessarily | synonymous     |
| **necessarily~incompatible**   |   101 |      3.47 |       97.53 |    0.19 |   0.20 |    0.00 |   0.00 |    4.25 |    506.31 | 6,347,364 | 42,886 |    513 | necessarily | incompatible   |
| **necessarily~causal**         |    28 |      0.57 |       27.43 |    0.32 |   0.33 |    0.00 |   0.00 |    4.16 |    172.90 | 6,347,364 | 42,886 |     85 | necessarily | causal         |
| **necessarily~reflective**     |   181 |      8.09 |      172.91 |    0.14 |   0.15 |    0.00 |   0.00 |    4.05 |    806.50 | 6,347,364 | 42,886 |  1,197 | necessarily | reflective     |
| **necessarily~predictive**     |    57 |      2.02 |       54.98 |    0.18 |   0.19 |    0.00 |   0.00 |    3.85 |    281.73 | 6,347,364 | 42,886 |    299 | necessarily | predictive     |
| **necessarily~proof**          |    34 |      0.97 |       33.03 |    0.23 |   0.24 |    0.00 |   0.00 |    3.79 |    184.45 | 6,347,364 | 42,886 |    143 | necessarily | proof          |
| **necessarily~true**           | 3,245 |    236.25 |    3,008.75 |    0.09 |   0.09 |    0.07 |   0.08 |    3.77 | 11,473.44 | 6,347,364 | 42,886 | 34,967 | necessarily | true           |


1. necessarily_indicative
   >  Results of operations for interim periods are not necessarily indicative of results to be expected for an entire year .

2. necessarily_cause
   >  While it appears problematic , economists with the federal government say a negative savings rate is n't necessarily cause for concern .

3. necessarily_representative
   >  The views expressed are not necessarily representative of all Fellows of the Academy .

4. necessarily_synonymous
   >  They point out that the State Employees Association illustrates a new definition of union , one in which strikes and walkouts are not necessarily synonymous with organized labor .

5. necessarily_incompatible
   >  The philosophies of habits and intensity are n't necessarily incompatible .

6. necessarily_causal
   >  But their findings are still not necessarily causal . "

7. necessarily_reflective
   >  Ellison 's public support is impressive , and it has helped to keep potential challengers on the bench , but it 's not necessarily reflective of actual DNC votes .

8. necessarily_predictive
   >  But those conversations are not necessarily predictive of specific outcomes like elections , revolutions , or successful products , " says Marc Smith , founder of the Social Media Research Foundation .

9. necessarily_proof
   >  Not that testing is necessarily proof in the Peanut Corporation of America world of keep testing until you get the answer you 're looking for .

10. necessarily_true
   >  That is not necessarily true though .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_indicative_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_cause_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_representative_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_synonymous_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_incompatible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_causal_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_reflective_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_predictive_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_proof_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_true_50ex.csv

## *that*


|                   |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |       `N` |    `f1` |    `f2` | `l1`   | `l2`     |
|:------------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|----------:|--------:|--------:|:-------|:---------|
| **that~great**    | 11,065 |  1,191.09 |    9,873.91 |    0.22 |   0.24 |    0.06 |   0.07 |    3.50 | 32,588.44 | 6,347,364 | 166,676 |  45,359 | that   | great    |
| **that~uncommon** |    802 |     83.11 |      718.89 |    0.23 |   0.25 |    0.00 |   0.00 |    3.33 |  2,384.09 | 6,347,364 | 166,676 |   3,165 | that   | uncommon |
| **that~hard**     |  9,963 |  1,183.26 |    8,779.74 |    0.20 |   0.22 |    0.05 |   0.06 |    3.31 | 27,269.05 | 6,347,364 | 166,676 |  45,061 | that   | hard     |
| **that~big**      |  6,273 |  1,126.83 |    5,146.17 |    0.12 |   0.15 |    0.03 |   0.04 |    2.56 | 12,074.72 | 6,347,364 | 166,676 |  42,912 | that   | big      |
| **that~bad**      | 16,635 |  3,138.20 |   13,496.80 |    0.12 |   0.14 |    0.08 |   0.10 |    2.52 | 31,301.66 | 6,347,364 | 166,676 | 119,509 | that   | bad      |
| **that~simple**   |  6,219 |  1,230.68 |    4,988.32 |    0.11 |   0.13 |    0.03 |   0.04 |    2.40 | 10,895.68 | 6,347,364 | 166,676 |  46,867 | that   | simple   |
| **that~stupid**   |    811 |    147.50 |      663.50 |    0.12 |   0.14 |    0.00 |   0.00 |    2.34 |  1,524.30 | 6,347,364 | 166,676 |   5,617 | that   | stupid   |
| **that~unusual**  |    977 |    194.63 |      782.37 |    0.11 |   0.13 |    0.00 |   0.01 |    2.22 |  1,679.63 | 6,347,364 | 166,676 |   7,412 | that   | unusual  |
| **that~dumb**     |    285 |     54.20 |      230.80 |    0.11 |   0.14 |    0.00 |   0.00 |    2.05 |    512.41 | 6,347,364 | 166,676 |   2,064 | that   | dumb     |
| **that~easy**     | 10,231 |  2,860.22 |    7,370.78 |    0.07 |   0.09 |    0.05 |   0.06 |    1.86 | 12,207.95 | 6,347,364 | 166,676 | 108,923 | that   | easy     |


1. that_great
   >  And part of that is developers acknowledging that yep , this feature is n't all that great .

2. that_uncommon
   >  And , it 's a letter that expresses a viewpoint not that uncommon from a majority of Americans .

3. that_hard
   >  He will be backed up a little bit in some of our base defensive packages , so that wo n't be that hard for him to learn the reads from that position opposed to outside .

4. that_big
   >  So being injured , it was unfortunate , but in the grand scheme of things it 's really not that big of a deal . "

5. that_bad
   >  You might say this is just a tip O and it 's not that bad .

6. that_simple
   >  Stelle explained that although with hindsight it may appear that those models lead directly to Professor Peter Higgs 's work , in practice it was n't that simple .

7. that_stupid
   >  Nope , we 're not that stupid .

8. that_unusual
   >  The symptoms that are being described are n't that unusual in areas like Burlington , where there is no chloramine .

9. that_dumb
   >  You hear people say " think of the children " all the time , but children are not that dumb .

10. that_easy
   >  But keeping a track on it is not that easy .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_great_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_uncommon_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_hard_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_big_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_bad_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_simple_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_stupid_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_unusual_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_dumb_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_easy_50ex.csv

## *exactly*


|                           |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |       `N` |   `f1` |    `f2` | `l1`    | `l2`          |
|:--------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|----------:|-------:|--------:|:--------|:--------------|
| **exactly~late-career**   |    35 |      0.25 |       34.75 |    0.99 |   1.00 |    0.00 |   0.00 |    7.82 |    347.24 | 6,347,364 | 44,503 |      35 | exactly | late-career   |
| **exactly~alike**         |   254 |      8.45 |      245.55 |    0.20 |   0.21 |    0.01 |   0.01 |    4.67 |  1,293.40 | 6,347,364 | 44,503 |   1,205 | exactly | alike         |
| **exactly~stellar**       |   170 |      5.54 |      164.46 |    0.21 |   0.22 |    0.00 |   0.00 |    4.57 |    873.03 | 6,347,364 | 44,503 |     790 | exactly | stellar       |
| **exactly~ideal**         |   418 |     23.25 |      394.75 |    0.12 |   0.13 |    0.01 |   0.01 |    3.93 |  1,678.75 | 6,347,364 | 44,503 |   3,316 | exactly | ideal         |
| **exactly~awash**         |    36 |      1.02 |       34.98 |    0.24 |   0.25 |    0.00 |   0.00 |    3.87 |    196.17 | 6,347,364 | 44,503 |     145 | exactly | awash         |
| **exactly~cheap**         |   691 |     46.21 |      644.79 |    0.10 |   0.10 |    0.01 |   0.02 |    3.73 |  2,523.80 | 6,347,364 | 44,503 |   6,591 | exactly | cheap         |
| **exactly~conducive**     |   208 |     13.69 |      194.31 |    0.10 |   0.11 |    0.00 |   0.00 |    3.48 |    764.40 | 6,347,364 | 44,503 |   1,952 | exactly | conducive     |
| **exactly~inconspicuous** |    26 |      0.85 |       25.15 |    0.21 |   0.21 |    0.00 |   0.00 |    3.27 |    133.36 | 6,347,364 | 44,503 |     121 | exactly | inconspicuous |
| **exactly~sure**          | 8,810 |    940.48 |    7,869.52 |    0.06 |   0.07 |    0.18 |   0.20 |    3.23 | 25,681.62 | 6,347,364 | 44,503 | 134,139 | exactly | sure          |
| **exactly~revolutionary** |   120 |      8.48 |      111.52 |    0.09 |   0.10 |    0.00 |   0.00 |    3.16 |    423.78 | 6,347,364 | 44,503 |   1,210 | exactly | revolutionary |


1. exactly_late-career
   >  He 's not exactly late-career Boris Diaw just yet .

2. exactly_alike
   >  While school and home environments may not be exactly alike , schools can still promote general safety strategies and ease parental concerns .

3. exactly_stellar
   >  2 . The options were n't exactly stellar .

4. exactly_ideal
   >  Sourdough is built on bacteria , and our water supply is designed to limit the growth of bacteria as much as possible -- not exactly ideal in this scenario .

5. exactly_awash
   >  And whilst the tearoom they both work in on the Monkpark Hall estate in Yorkshire is not exactly awash with eligible bachelors , it 's obvious where the male attention is concentrated - and it 's not just on the cakes !

6. exactly_cheap
   >  It costs $ 9.95 for just eight laps around the almost multi-storey car park- esque circuit , so it 's not exactly cheap compared to land-locked tracks .

7. exactly_conducive
   >  Monday through Wednesday I 'm flying out to South Dakota to visit an operations center , and business trips are n't exactly conducive to watching your calorie intake .

8. exactly_inconspicuous
   >  " They were n't exactly inconspicuous , " said the source .

9. exactly_sure
   >  While we 're not exactly sure just how much these things will run the average consumer just yet , they are supposedly shipping to computer manufacturers now at around $ 350 a pop .

10. exactly_revolutionary
   >  None of these things is exactly revolutionary , it must be said .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_late-career_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_alike_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_stellar_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_ideal_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_awash_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_cheap_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_conducive_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_inconspicuous_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_sure_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_revolutionary_50ex.csv

## *any*


|                 |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |       `N` |   `f1` |   `f2` | `l1`   | `l2`    |
|:----------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|----------:|-------:|-------:|:-------|:--------|
| **any~happier** |   834 |      5.13 |      828.87 |    0.41 |   0.42 |    0.05 |   0.05 |    7.76 |  7,282.99 | 6,347,364 | 16,238 |  2,004 | any    | happier |
| **any~clearer** |   371 |      2.49 |      368.51 |    0.38 |   0.38 |    0.02 |   0.02 |    7.39 |  3,147.58 | 6,347,364 | 16,238 |    972 | any    | clearer |
| **any~truer**   |    43 |      0.30 |       42.70 |    0.36 |   0.36 |    0.00 |   0.00 |    6.20 |    358.99 | 6,347,364 | 16,238 |    118 | any    | truer   |
| **any~cuter**   |    47 |      0.38 |       46.62 |    0.32 |   0.32 |    0.00 |   0.00 |    6.01 |    376.68 | 6,347,364 | 16,238 |    148 | any    | cuter   |
| **any~closer**  |   611 |      9.43 |      601.57 |    0.16 |   0.17 |    0.04 |   0.04 |    5.92 |  4,021.04 | 6,347,364 | 16,238 |  3,686 | any    | closer  |
| **any~worse**   | 1,762 |     31.00 |    1,731.00 |    0.14 |   0.15 |    0.11 |   0.11 |    5.85 | 11,229.25 | 6,347,364 | 16,238 | 12,116 | any    | worse   |
| **any~simpler** |   229 |      3.70 |      225.30 |    0.16 |   0.16 |    0.01 |   0.01 |    5.61 |  1,479.26 | 6,347,364 | 16,238 |  1,446 | any    | simpler |
| **any~easier**  | 1,625 |     32.94 |    1,592.06 |    0.12 |   0.13 |    0.10 |   0.10 |    5.61 |  9,854.27 | 6,347,364 | 16,238 | 12,877 | any    | easier  |
| **any~younger** |   255 |      4.56 |      250.44 |    0.14 |   0.14 |    0.02 |   0.02 |    5.47 |  1,591.82 | 6,347,364 | 16,238 |  1,784 | any    | younger |
| **any~safer**   |   255 |      4.70 |      250.30 |    0.14 |   0.14 |    0.02 |   0.02 |    5.42 |  1,575.71 | 6,347,364 | 16,238 |  1,838 | any    | safer   |


1. any_happier
   >  It takes a lot of courage , confidence and self -assurance to face your fears , and we could n't be any happier for him .

2. any_clearer
   >  I ca n't be any clearer than that . "

3. any_truer
   >  The saying , " Once you learn to ride a bike , you never forget " could n't be any truer for learning to read .

4. any_cuter
   >  Could they be any cuter together ?!

5. any_closer
   >  " But we 're not any closer to solving the case because of it . "

6. any_worse
   >  " It ca n't be any worse than thermal long johns , right ? "

7. any_simpler
   >  Finding professional Annapolis , IL movers could not be any simpler !

8. any_easier
   >  Getting to the Hotel Indigo Asheville really could n't be any easier .

9. any_younger
   >  `` I 'm not getting any younger .

10. any_safer
   >  It is not clear anything was accomplished by this , certainly not that the food supply is any safer .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_happier_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_clearer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_truer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_cuter_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_closer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_worse_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_simpler_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_easier_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_younger_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_safer_50ex.csv

## *remotely*


|                         |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |       `N` |   `f1` |   `f2` | `l1`     | `l2`       |
|:------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|----------:|-------:|-------:|:---------|:-----------|
| **remotely~comparable** |   125 |      2.33 |      122.67 |    0.05 |   0.05 |    0.02 |   0.02 |    5.05 |   759.06 | 6,347,364 |  6,161 |  2,401 | remotely | comparable |
| **remotely~close**      |   733 |     45.12 |      687.88 |    0.01 |   0.02 |    0.11 |   0.12 |    3.75 | 2,801.94 | 6,347,364 |  6,161 | 46,485 | remotely | close      |
| **remotely~similar**    |   169 |     10.76 |      158.24 |    0.01 |   0.02 |    0.03 |   0.03 |    3.35 |   620.70 | 6,347,364 |  6,161 | 11,088 | remotely | similar    |
| **remotely~believable** |    38 |      1.39 |       36.61 |    0.03 |   0.03 |    0.01 |   0.01 |    3.31 |   179.17 | 6,347,364 |  6,161 |  1,436 | remotely | believable |
| **remotely~credible**   |    34 |      1.40 |       32.60 |    0.02 |   0.02 |    0.01 |   0.01 |    3.04 |   152.69 | 6,347,364 |  6,161 |  1,441 | remotely | credible   |
| **remotely~interested** |   364 |     33.53 |      330.47 |    0.01 |   0.01 |    0.05 |   0.06 |    3.03 | 1,096.50 | 6,347,364 |  6,161 | 34,543 | remotely | interested |
| **remotely~related**    |   163 |     13.84 |      149.16 |    0.01 |   0.01 |    0.02 |   0.03 |    2.91 |   510.85 | 6,347,364 |  6,161 | 14,260 | remotely | related    |
| **remotely~funny**      |   141 |     14.55 |      126.45 |    0.01 |   0.01 |    0.02 |   0.02 |    2.58 |   391.23 | 6,347,364 |  6,161 | 14,992 | remotely | funny      |
| **remotely~true**       |   251 |     33.94 |      217.06 |    0.01 |   0.01 |    0.04 |   0.04 |    2.37 |   579.45 | 6,347,364 |  6,161 | 34,967 | remotely | true       |
| **remotely~plausible**  |    25 |      1.37 |       23.63 |    0.02 |   0.02 |    0.00 |   0.00 |    2.30 |    98.58 | 6,347,364 |  6,161 |  1,407 | remotely | plausible  |


1. remotely_comparable
   >  It is not remotely comparable to The Last Temptation , in which Willem Dafoe played Jesus , Harvey Keitel was Judas and David Bowie Pontius Pilate .

2. remotely_close
   >  And anyone remotely close to golf knows that Rory M is a world leader .

3. remotely_similar
   >  My pace is n't remotely similar to what it usually is , but it 's hard to judge ; I think I 've passed the border and entered New Jersey for over an hour when I finally reach the well - marked border -- as it should be !

4. remotely_believable
   >  although there is nothing remotely believable about this drawn-out cat-and-mouse game of a movie crossed with a whodunit , that 's almost the point .

5. remotely_credible
   >  `` If he wants to be remotely credible , '' Luntz said , `` he needs a credible vice-presidential candidate .

6. remotely_interested
   >  Antifa are not remotely interested in peace , hope or equality .

7. remotely_related
   >  Have you ever had a manager who told you to do something , only to find out later that what should have been done was n't remotely related to what he really wanted ?

8. remotely_funny
   >  PS to the studio - do n't market a film as a comedy if its not remotely funny .

9. remotely_true
   >  That 's not even remotely true .

10. remotely_plausible
   >  To expose your opponents ' intellectual hypocrisy , you have to show that it 's unlikely that they really believe what they 're saying because there 's no coherent and remotely plausible view of the world that 's consistent with the political positions they 've taken over time .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_comparable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_close_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_similar_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_believable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_credible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_interested_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_related_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_funny_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_true_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_plausible_50ex.csv

## *yet*


|                  |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |       `N` |   `f1` |   `f2` | `l1`   | `l2`     |
|:-----------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|----------:|-------:|-------:|:-------|:---------|
| **yet~final**    |    640 |     10.30 |      629.70 |    0.52 |   0.53 |    0.01 |   0.01 |    6.58 |  4,443.69 | 6,347,364 | 53,881 |  1,213 | yet    | final    |
| **yet~official** |    352 |      7.84 |      344.16 |    0.37 |   0.38 |    0.01 |   0.01 |    5.63 |  2,141.31 | 6,347,364 | 53,881 |    924 | yet    | official |
| **yet~ready**    |  7,505 |    251.12 |    7,253.88 |    0.25 |   0.25 |    0.14 |   0.14 |    5.21 | 39,487.39 | 6,347,364 | 53,881 | 29,583 | yet    | ready    |
| **yet~complete** |  2,175 |     71.43 |    2,103.57 |    0.25 |   0.26 |    0.04 |   0.04 |    5.15 | 11,318.19 | 6,347,364 | 53,881 |  8,415 | yet    | complete |
| **yet~ripe**     |    381 |     12.33 |      368.67 |    0.25 |   0.26 |    0.01 |   0.01 |    4.90 |  1,982.82 | 6,347,364 | 53,881 |  1,453 | yet    | ripe     |
| **yet~over**     |    162 |      5.20 |      156.80 |    0.26 |   0.26 |    0.00 |   0.00 |    4.65 |    845.32 | 6,347,364 | 53,881 |    613 | yet    | over     |
| **yet~public**   |    467 |     22.55 |      444.45 |    0.17 |   0.18 |    0.01 |   0.01 |    4.23 |  2,025.17 | 6,347,364 | 53,881 |  2,656 | yet    | public   |
| **yet~eligible** |    448 |     22.24 |      425.76 |    0.16 |   0.17 |    0.01 |   0.01 |    4.17 |  1,916.40 | 6,347,364 | 53,881 |  2,620 | yet    | eligible |
| **yet~clear**    | 10,409 |    714.98 |    9,694.02 |    0.12 |   0.12 |    0.18 |   0.19 |    3.96 | 39,438.81 | 6,347,364 | 53,881 | 84,227 | yet    | clear    |
| **yet~unnamed**  |     30 |      0.87 |       29.13 |    0.29 |   0.29 |    0.00 |   0.00 |    3.70 |    163.80 | 6,347,364 | 53,881 |    102 | yet    | unnamed  |


1. yet_final
   >  In some cases , rebates would be banned altogether under the proposal , which is not yet final .

2. yet_official
   >  a person involved in the negotiations confirmed the agreement and was granted anonymity because he could not otherwise speak about a deal that was not yet official .

3. yet_ready
   >  And this is the reason why I 'm not yet ready to close the book on 2014 .

4. yet_complete
   >  Though Drive is not yet complete , a new story is already waiting in the wings , and it will not let go until put to paper .

5. yet_ripe
   >  We 've had 2 or 3 lemons from it in the last couple of years but this year it seems to be coming into more bountiful fruit production with up to a dozen fruits , not yet ripe but getting there .

6. yet_over
   >  the era of the grand hotel in America is not yet over .

7. yet_public
   >  Although the report is not yet public , AP reports ( citing trade diplomats who have seen the interim report ) that the panel faulted China for not prosecuting pirates who copy CDs and DVDs before they are passed by censors .

8. yet_eligible
   >  1936 - the Degree of Chevalier is instituted to honor De Molay leaders who were not yet eligible to receive the Legion of Honor .

9. yet_clear
   >  Neither is open yet and it 's not yet clear how they will operate , given that only 25 cannabis licenses will be granted by the Ontario government in April of this year .

10. yet_unnamed
   >  First , there 's a post by Steve Outing , where he talks about an ( as yet unnamed ) group of recently laid off journalists from a major newspaper who are actually using their severance packages to start an online competitor .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_final_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_official_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_ready_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_complete_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_ripe_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_over_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_public_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_eligible_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_clear_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unnamed_50ex.csv

## *immediately*


|                                  |    `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |       `G2` |       `N` |   `f1` |   `f2` | `l1`        | `l2`             |
|:---------------------------------|-------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|-----------:|----------:|-------:|-------:|:------------|:-----------------|
| **immediately~appealable**       |     31 |      0.37 |       30.63 |    0.77 |   0.77 |    0.00 |   0.00 |    5.85 |     248.60 | 6,347,364 | 58,040 |     40 | immediately | appealable       |
| **immediately~clear**            | 24,488 |    770.17 |   23,717.83 |    0.29 |   0.29 |    0.41 |   0.42 |    5.41 | 141,124.54 | 6,347,364 | 58,040 | 84,227 | immediately | clear            |
| **immediately~available**        | 21,477 |    758.55 |   20,718.45 |    0.25 |   0.26 |    0.36 |   0.37 |    5.18 | 116,575.86 | 6,347,364 | 58,040 | 82,956 | immediately | available        |
| **immediately~apparent**         |  2,143 |     89.59 |    2,053.41 |    0.21 |   0.22 |    0.04 |   0.04 |    4.73 |  10,042.87 | 6,347,364 | 58,040 |  9,798 | immediately | apparent         |
| **immediately~adjacent**         |    108 |      3.13 |      104.87 |    0.31 |   0.32 |    0.00 |   0.00 |    4.69 |     591.96 | 6,347,364 | 58,040 |    342 | immediately | adjacent         |
| **immediately~reachable**        |    109 |      3.20 |      105.80 |    0.30 |   0.31 |    0.00 |   0.00 |    4.67 |     593.89 | 6,347,364 | 58,040 |    350 | immediately | reachable        |
| **immediately~obvious**          |  2,325 |    207.12 |    2,117.88 |    0.09 |   0.10 |    0.04 |   0.04 |    3.46 |   7,294.46 | 6,347,364 | 58,040 | 22,651 | immediately | obvious          |
| **immediately~recognizable**     |    249 |     21.98 |      227.02 |    0.09 |   0.10 |    0.00 |   0.00 |    3.10 |     777.98 | 6,347,364 | 58,040 |  2,404 | immediately | recognizable     |
| **immediately~life-threatening** |     64 |      4.54 |       59.46 |    0.12 |   0.13 |    0.00 |   0.00 |    2.85 |     227.19 | 6,347,364 | 58,040 |    497 | immediately | life-threatening |
| **immediately~evident**          |    470 |     56.06 |      413.94 |    0.07 |   0.08 |    0.01 |   0.01 |    2.78 |   1,202.69 | 6,347,364 | 58,040 |  6,131 | immediately | evident          |


1. immediately_appealable
   >  See King v. Cessna Aircraft Co. , 562 F.3d 1374 , 1378-81 ( 11th Cir. 2009 ) ( finding the denial of a motion to dismiss on the basis of forum non conveniens is not a final , appealable order ) ; Rosenstein v. Merrell Dow Pharm. , Inc. , 769 F.2d 352 , 354 ( 6th Cir. 1985 ) ( holding the denial of a motion to dismiss on forum non conveniens grounds is not immediately appealable under collateral order exception to final judgment rule ) ; Rolinski v. Lewis , 828 A.2d 739 , 742 ( D.C. 2003 ) ( holding that denials of forum non conveniens motions to dismiss are not immediately appealable as of right ) ; Payton-Henderson v. Evans , 949 A.2d 654 , 662 ( Md. Ct. Spec. App. 2008 ) ( stating forum non conveniens issues are treated the same as change of venue and the denial of either is not immediately appealable ) .

2. immediately_clear
   >  Mba Obame has been frequently absent from the central African oil- producing nation for health reasons since 2009 and it had not been immediately clear who would lead the National Union .

3. immediately_available
   >  Army sources were not immediately available for the comment .

4. immediately_apparent
   >  I do n't have any information about internal efforts by the App Kit or UIKit teams but it 's not immediately apparent that Apple are looking to make any dramatic changes any time soon .

5. immediately_adjacent
   >  Park City Mountain Resort is not immediately adjacent to the Canyons Resort property , but Lund said the two areas are near enough that combining them is a potential option .

6. immediately_reachable
   >  Volkswagen , which faces numerous legal and regulatory fines after admitting it cheated on diesel emissions tests , was not immediately reachable for comment .

7. immediately_obvious
   >  Pizza is an immediately obvious pairing to drunken cooking -- it's delicious and quick , most of us keep some basic version of the components on hand , and it 's been a classic companion to drinking since time immemorial .

8. immediately_recognizable
   >  Her work is immediately recognizable for its distinctive asymmetry , tantalizing multi-metal combinations , and elegant use of positive / negative space .

9. immediately_life-threatening
   >  Q : So most of the events were problems that were n't immediately life-threatening but could cause damage over time ?

10. immediately_evident
   >  What is not immediately evident is that there is money left on the table .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_appealable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_clear_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_available_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_apparent_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_adjacent_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_reachable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_obvious_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognizable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_life-threatening_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_evident_50ex.csv

## *particularly*


|                             |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |       `N` |   `f1` |   `f2` | `l1`         | `l2`       |
|:----------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|----------:|-------:|-------:|:-------------|:-----------|
| **particularly~noteworthy** |   338 |     16.49 |      321.51 |    0.23 |   0.25 |    0.00 |   0.00 |    4.25 | 1,483.20 | 6,347,364 | 76,162 |  1,374 | particularly | noteworthy |
| **particularly~fond**       | 1,254 |     93.24 |    1,160.76 |    0.15 |   0.16 |    0.02 |   0.02 |    3.74 | 4,399.54 | 6,347,364 | 76,162 |  7,771 | particularly | fond       |
| **particularly~revelatory** |    60 |      3.12 |       56.88 |    0.22 |   0.23 |    0.00 |   0.00 |    3.38 |   254.72 | 6,347,364 | 76,162 |    260 | particularly | revelatory |
| **particularly~religious**  |   486 |     42.08 |      443.92 |    0.13 |   0.14 |    0.01 |   0.01 |    3.34 | 1,552.38 | 6,347,364 | 76,162 |  3,507 | particularly | religious  |
| **particularly~novel**      |   129 |     10.86 |      118.14 |    0.13 |   0.14 |    0.00 |   0.00 |    2.98 |   418.75 | 6,347,364 | 76,162 |    905 | particularly | novel      |
| **particularly~acute**      |   135 |     12.45 |      122.55 |    0.12 |   0.13 |    0.00 |   0.00 |    2.85 |   413.83 | 6,347,364 | 76,162 |  1,038 | particularly | acute      |
| **particularly~memorable**  |   602 |     74.48 |      527.52 |    0.09 |   0.10 |    0.01 |   0.01 |    2.80 | 1,511.47 | 6,347,364 | 76,162 |  6,207 | particularly | memorable  |
| **particularly~interested** | 2,783 |    414.48 |    2,368.52 |    0.07 |   0.08 |    0.03 |   0.04 |    2.70 | 6,106.12 | 6,347,364 | 76,162 | 34,543 | particularly | interested |
| **particularly~likeable**   |   106 |     10.33 |       95.67 |    0.11 |   0.12 |    0.00 |   0.00 |    2.66 |   313.57 | 6,347,364 | 76,162 |    861 | particularly | likeable   |
| **particularly~adept**      |   200 |     22.83 |      177.17 |    0.09 |   0.11 |    0.00 |   0.00 |    2.66 |   531.36 | 6,347,364 | 76,162 |  1,903 | particularly | adept      |


1. particularly_noteworthy
   >  This area is particularly noteworthy for birding during migration because of its location on the Gulf of Mexico and how weather patterns can effect bird movements .

2. particularly_fond
   >  Your garden variety 12 year old is likely neither worldly nor particularly fond of gardens .

3. particularly_revelatory
   >  THQ has teased new Darksiders II DLC with a single , not particularly revelatory image via its Darksiders Twitter page .

4. particularly_religious
   >  My dad however actually told me " You do n't get to decide what you believe until you 're 18 " which was weird because he 's never been particularly religious .

5. particularly_novel
   >  Not particularly novel .

6. particularly_acute
   >  worries over tight supplies of the fuel have been particularly acute in the Midwest , where prices are soaring .

7. particularly_memorable
   >  At Simatai , the hawkers there were particularly memorable because it 's one thing to have a saleswoman follow you out of a shop , but it 's quite another to have one pursue you over two -hours worth of steep watchtower stairs just to sell postcards .

8. particularly_interested
   >  I am particularly interested in how The National Lottery Community Fund can continue to work with others to overcome the grinding effects of social inequality in our society . "

9. particularly_likeable
   >  Purposefully , none of the characters are particularly likeable and despite its focus on infidelity it is play without a victim .

10. particularly_adept
   >  He is particularly adept at using women .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_noteworthy_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_fond_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_revelatory_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_religious_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_novel_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_acute_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_memorable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_interested_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_likeable_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_adept_50ex.csv

## *inherently*


|                             |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |      `G2` |       `N` |   `f1` |   `f2` | `l1`       | `l2`         |
|:----------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|----------:|----------:|-------:|-------:|:-----------|:-------------|
| **inherently~governmental** |    40 |      0.09 |       39.91 |    0.57 |   0.57 |    0.00 |   0.00 |    8.02 |    432.85 | 6,347,364 |  8,614 |     70 | inherently | governmental |
| **inherently~evil**         |   392 |      4.30 |      387.70 |    0.12 |   0.12 |    0.05 |   0.05 |    6.26 |  2,829.19 | 6,347,364 |  8,614 |  3,171 | inherently | evil         |
| **inherently~wrong**        | 1,678 |     28.95 |    1,649.05 |    0.08 |   0.08 |    0.19 |   0.19 |    5.77 | 10,797.34 | 6,347,364 |  8,614 | 21,332 | inherently | wrong        |
| **inherently~sinful**       |    38 |      0.49 |       37.51 |    0.10 |   0.11 |    0.00 |   0.00 |    4.90 |    260.31 | 6,347,364 |  8,614 |    359 | inherently | sinful       |
| **inherently~improper**     |    25 |      0.29 |       24.71 |    0.12 |   0.12 |    0.00 |   0.00 |    4.62 |    176.39 | 6,347,364 |  8,614 |    214 | inherently | improper     |
| **inherently~unsafe**       |    47 |      0.86 |       46.14 |    0.07 |   0.07 |    0.01 |   0.01 |    4.54 |    287.92 | 6,347,364 |  8,614 |    631 | inherently | unsafe       |
| **inherently~immoral**      |    43 |      0.94 |       42.06 |    0.06 |   0.06 |    0.00 |   0.00 |    4.19 |    247.31 | 6,347,364 |  8,614 |    694 | inherently | immoral      |
| **inherently~racist**       |    67 |      2.18 |       64.82 |    0.04 |   0.04 |    0.01 |   0.01 |    3.91 |    332.29 | 6,347,364 |  8,614 |  1,609 | inherently | racist       |
| **inherently~flawed**       |    61 |      2.14 |       58.86 |    0.04 |   0.04 |    0.01 |   0.01 |    3.74 |    293.38 | 6,347,364 |  8,614 |  1,580 | inherently | flawed       |
| **inherently~unstable**     |    47 |      1.69 |       45.31 |    0.04 |   0.04 |    0.01 |   0.01 |    3.53 |    224.05 | 6,347,364 |  8,614 |  1,243 | inherently | unstable     |


1. inherently_governmental
   >  Inventories of commercial and inherently governmental activities performed at the Commission .

2. inherently_evil
   >  According to the NOI , whites were an inherently evil race created in ancient times by a sinister black scientist named Yacub .

3. inherently_wrong
   >  There is nothing inherently wrong with introversion , but because we are the minority , many introverts have poor social skills or suffer from social anxiety .

4. inherently_sinful
   >  It is the only worldview that tells us the sheer , stark truth that we are inherently sinful and that we need to be saved from ourselves .

5. inherently_improper
   >  However , the court decided to take the approach of a substantial minority of states , and concluded that " it is not inherently improper for a court to consider the possibility of inheritance in some cases .

6. inherently_unsafe
   >  Her case alleged that the Carrera GT had design flaws that made it inherently unsafe to drive .

7. inherently_immoral
   >  It will be because institutionalized theft is inherently immoral and a society of collectivism ; and institutionalized theft will suffer great moral decline , as well as continually reduce the people 's standard of living .

8. inherently_racist
   >  In the school situation , I get the impression that the principal is inherently racist and losing her cool allowed those private thoughts to bubble up into public words and actions .

9. inherently_flawed
   >  They are keenly aware of the inherently flawed nature of human thinking when left unchecked .

10. inherently_unstable
   >  " The crown prince insists that the continuation of the present boundaries is an inherently unstable solution which carries the seeds of future instability , " Mr. Trifkovic says .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_governmental_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_evil_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_wrong_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_sinful_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_improper_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unsafe_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_immoral_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_racist_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_flawed_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unstable_50ex.csv

## *terribly*


|                         |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |       `N` |   `f1` |   `f2` | `l1`     | `l2`       |
|:------------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|----------:|-------:|-------:|:---------|:-----------|
| **terribly~surprising** |   949 |     58.58 |      890.42 |    0.05 |   0.05 |    0.05 |   0.05 |    3.82 | 3,589.19 | 6,347,364 | 19,802 | 18,776 | terribly | surprising |
| **terribly~original**   |   201 |     14.64 |      186.36 |    0.04 |   0.04 |    0.01 |   0.01 |    3.24 |   689.61 | 6,347,364 | 19,802 |  4,693 | terribly | original   |
| **terribly~surprised**  |   291 |     31.69 |      259.31 |    0.03 |   0.03 |    0.01 |   0.01 |    2.75 |   782.04 | 6,347,364 | 19,802 | 10,157 | terribly | surprised  |
| **terribly~uncommon**   |   103 |      9.87 |       93.13 |    0.03 |   0.03 |    0.00 |   0.01 |    2.57 |   300.00 | 6,347,364 | 19,802 |  3,165 | terribly | uncommon   |
| **terribly~impressed**  |   283 |     37.87 |      245.13 |    0.02 |   0.02 |    0.01 |   0.01 |    2.44 |   656.23 | 6,347,364 | 19,802 | 12,138 | terribly | impressed  |
| **terribly~fond**       |   192 |     24.24 |      167.76 |    0.02 |   0.02 |    0.01 |   0.01 |    2.41 |   464.21 | 6,347,364 | 19,802 |  7,771 | terribly | fond       |
| **terribly~exciting**   |   391 |     63.12 |      327.88 |    0.02 |   0.02 |    0.02 |   0.02 |    2.24 |   781.19 | 6,347,364 | 19,802 | 20,233 | terribly | exciting   |
| **terribly~wrong**      |   398 |     66.55 |      331.45 |    0.02 |   0.02 |    0.02 |   0.02 |    2.19 |   771.55 | 6,347,364 | 19,802 | 21,332 | terribly | wrong      |
| **terribly~upset**      |   116 |     16.24 |       99.76 |    0.02 |   0.02 |    0.01 |   0.01 |    2.07 |   259.12 | 6,347,364 | 19,802 |  5,204 | terribly | upset      |
| **terribly~unusual**    |   146 |     23.12 |      122.88 |    0.02 |   0.02 |    0.01 |   0.01 |    1.98 |   295.16 | 6,347,364 | 19,802 |  7,412 | terribly | unusual    |


1. terribly_surprising
   >  The current government has done an awful lot of things I do n't agree with -- this should n't be terribly surprising to you .

2. terribly_original
   >  I said the plot was n't terribly original , but I have n't seen much like this , so it was original enough for me .

3. terribly_surprised
   >  I would n't be terribly surprised if this story had actually happened with him .

4. terribly_uncommon
   >  While Christians marrying Jews , Jews marrying Hindus and Hindus marrying Buddhists is not terribly uncommon in the US and other first world nations , it has not always been this way .

5. terribly_impressed
   >  While investors were n't terribly impressed with RIM 's efforts and the company 's stock took a hit , developers and users alike were intrigued by several features shown off by the struggling smartphone maker .

6. terribly_fond
   >  If youre not terribly fond of women , you probably shouldnt see Volver , a movie wherein mere mortality doesnt stop mothers from loudly smooching their daughters cheeks , a breezy comedy in which a seemingly typical male gets stabbed , stuffed into a fridge and buried at swamps edge .

7. terribly_exciting
   >  The salad bar was n't terribly exciting , but it did have lots of veggies , balsamic vinegar and oil , and those crunchy chow mein noodles .

8. terribly_wrong
   >  It 's all here - Science Fiction , fantasy , a detective story , technology gone terribly wrong , human drama , a mystery story , and much more .

9. terribly_upset
   >  I 'm not terribly upset to leave Botswana .

10. terribly_unusual
   >  It would not be terribly unusual to see a 70 year old woman sans brassiere strut by in the latest fashions , sporting an air that says she owns the sidewalk and possibly much of this part of town .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_surprising_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_original_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_surprised_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_uncommon_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_impressed_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_fond_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_exciting_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_wrong_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_upset_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_unusual_50ex.csv

## *ever*


|                   |   `f` |   `exp_f` |   `unexp_f` |   `dP1` |   `P1` |   `dP2` |   `P2` |   `LRC` |     `G2` |       `N` |   `f1` |   `f2` | `l1`   | `l2`     |
|:------------------|------:|----------:|------------:|--------:|-------:|--------:|-------:|--------:|---------:|----------:|-------:|-------:|:-------|:---------|
| **ever~closer**   |   281 |      6.31 |      274.69 |    0.07 |   0.08 |    0.03 |   0.03 |    5.08 | 1,611.94 | 6,347,364 | 10,870 |  3,686 | ever   | closer   |
| **ever~mindful**  |    53 |      1.34 |       51.66 |    0.07 |   0.07 |    0.00 |   0.00 |    4.15 |   290.04 | 6,347,364 | 10,870 |    784 | ever   | mindful  |
| **ever~vigilant** |    48 |      1.27 |       46.73 |    0.06 |   0.06 |    0.00 |   0.00 |    4.00 |   258.13 | 6,347,364 | 10,870 |    744 | ever   | vigilant |
| **ever~present**  |   326 |     15.86 |      310.14 |    0.03 |   0.04 |    0.03 |   0.03 |    3.95 | 1,370.21 | 6,347,364 | 10,870 |  9,262 | ever   | present  |
| **ever~greater**  |   187 |     11.90 |      175.10 |    0.03 |   0.03 |    0.02 |   0.02 |    3.40 |   687.30 | 6,347,364 | 10,870 |  6,949 | ever   | greater  |
| **ever~deeper**   |    62 |      3.03 |       58.97 |    0.03 |   0.04 |    0.01 |   0.01 |    3.27 |   258.76 | 6,347,364 | 10,870 |  1,768 | ever   | deeper   |
| **ever~dull**     |    42 |      2.28 |       39.72 |    0.03 |   0.03 |    0.00 |   0.00 |    2.83 |   166.54 | 6,347,364 | 10,870 |  1,333 | ever   | dull     |
| **ever~perfect**  |   225 |     21.98 |      203.02 |    0.02 |   0.02 |    0.02 |   0.02 |    2.82 |   647.77 | 6,347,364 | 10,870 | 12,833 | ever   | perfect  |
| **ever~final**    |    39 |      2.08 |       36.92 |    0.03 |   0.03 |    0.00 |   0.00 |    2.80 |   156.15 | 6,347,364 | 10,870 |  1,213 | ever   | final    |
| **ever~larger**   |   139 |     12.76 |      126.24 |    0.02 |   0.02 |    0.01 |   0.01 |    2.75 |   414.99 | 6,347,364 | 10,870 |  7,453 | ever   | larger   |


1. ever_closer
   >  With 30 years of ' hands - on ' viticultural experience , Fred supports his winemaker son Joel in producing layered and elegant wines rich with texture and flavour ; bringing them ever closer to achieving their goal .

2. ever_mindful
   >  She likes to garden , although ever mindful of running afoul of a Dennene , lately it is more about planning than actually extending her flower garden .

3. ever_vigilant
   >  Irrationality has always been a human failing and we must be ever vigilant to combat it for the good of society .

4. ever_present
   >  Be ever present with your servants who seek through art and music to perfect the praises offered by your people on earth ; and grant to them even now glimpses of your beauty , and make them worthy at length to behold it unveiled for evermore ; through Jesus Christ our Lord .

5. ever_greater
   >  " In each instance , the finalists have inspired us all to seek new , innovative and collaborative ways to approach the most challenging areas of mission and business needs , and to achieve ever greater levels of service and efficiency . "

6. ever_deeper
   >  To hold the hardness in my fingers , to lick and kiss it , to let it slide down my throat , then to feel it enter my make - believe pussy , at first tentatively , thrusting , then deep , thrusting , ever deeper , deep , so deep inside me .

7. ever_dull
   >  Once they have their soul mate , the Aquarian is very loyal and never ever dull .

8. ever_perfect
   >  Life is n't ever perfect .

9. ever_final
   >  Nothing is ever final , not even a Supreme Court ruling .

10. ever_larger
   >  The result is an ever larger number of actors able to exert influence regionally or globally .

Saving Samples in /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/...

Samples saved as...
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_closer_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_mindful_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_vigilant_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_present_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_greater_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_deeper_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_dull_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_perfect_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_final_50ex.csv
+ /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_larger_50ex.csv

