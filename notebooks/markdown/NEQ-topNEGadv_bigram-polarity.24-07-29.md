```python
import re
from pathlib import Path

import pandas as pd

from source.utils.associate import TOP_AM_DIR, adjust_assoc_columns
from source.utils.dataframes import catify_hit_table as catify
from source.utils.dataframes import  show_sample
from source.utils.general import (HIT_TABLES_DIR, confirm_dir, print_iter,
                                  timestamp_today)
from source.utils.sample import sample_pickle as sp

REFILTER_NEG = False
VERBOSE = True
K = 8
N_EX_PER_BIGRAM = 99
BIGRAM_F_FLOOR=25
ADV_F_FLOOR=5000
DATE = timestamp_today()

TAG='NEQ'
METRIC_PRIORITY = ['LRC', 'P1', 'G2', 'P2'] if TAG=='NEQ' else ['dP1', 'LRC', 'G2', 'P1']
TOP_AM_TAG_DIR = TOP_AM_DIR / TAG
TAG_TOP_STR = f'{TAG}-Top{K}'
OUT_DIR = TOP_AM_TAG_DIR / TAG_TOP_STR
BK = max(K+2, 10)
FOCUS = adjust_assoc_columns(['f', 
                              'am_p1_given2_simple', 
                              'am_p2_given1_simple', 
                              'conservative_log_ratio',
                              'am_p1_given2', 
                              'am_p2_given1', 
                              'am_log_likelihood',
                              #   't_score', 'mutual_information', 'am_odds_ratio_disc',
                              'N', 'f1', 'f2', 
                              'E11', 'unexpected_f',
                              'adv_total', 'adj_total',
                              'l1', 'l2', 
                              'adv', 'adj'
                              ])
FOCUS_MEANS = [f'mean_{c}' for c in FOCUS]
SET_FOCUS = [f'{c}_SET' for c in FOCUS]
MIR_FOCUS = [f'{c}_MIR' for c in FOCUS]
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 70)

#> this points to the superset of negated hits---there is no `NEQ` version
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
adv_am.filter(SET_FOCUS)
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
      <th>f_SET</th>
      <th>P1_SET</th>
      <th>P2_SET</th>
      <th>LRC_SET</th>
      <th>dP1_SET</th>
      <th>dP2_SET</th>
      <th>G2_SET</th>
      <th>N_SET</th>
      <th>f1_SET</th>
      <th>f2_SET</th>
      <th>exp_f_SET</th>
      <th>unexp_f_SET</th>
      <th>l1_SET</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>necessarily</th>
      <td>42595</td>
      <td>0.99</td>
      <td>0.01</td>
      <td>6.77</td>
      <td>0.50</td>
      <td>0.01</td>
      <td>56,251.14</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>42886</td>
      <td>21,442.85</td>
      <td>21,152.15</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>that</th>
      <td>164768</td>
      <td>0.99</td>
      <td>0.05</td>
      <td>6.26</td>
      <td>0.50</td>
      <td>0.05</td>
      <td>214,504.57</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>166676</td>
      <td>83,337.42</td>
      <td>81,430.58</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>43813</td>
      <td>0.98</td>
      <td>0.01</td>
      <td>5.71</td>
      <td>0.49</td>
      <td>0.01</td>
      <td>54,870.72</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>44503</td>
      <td>22,251.35</td>
      <td>21,561.65</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>any</th>
      <td>15384</td>
      <td>0.95</td>
      <td>0.00</td>
      <td>3.91</td>
      <td>0.45</td>
      <td>0.00</td>
      <td>15,851.55</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>16238</td>
      <td>8,118.94</td>
      <td>7,265.06</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>5661</td>
      <td>0.92</td>
      <td>0.00</td>
      <td>3.16</td>
      <td>0.42</td>
      <td>0.00</td>
      <td>5,075.57</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>6161</td>
      <td>3,080.48</td>
      <td>2,580.52</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>51867</td>
      <td>0.96</td>
      <td>0.02</td>
      <td>4.52</td>
      <td>0.47</td>
      <td>0.02</td>
      <td>57,900.12</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>53881</td>
      <td>26,940.31</td>
      <td>24,926.69</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>56099</td>
      <td>0.97</td>
      <td>0.02</td>
      <td>4.68</td>
      <td>0.47</td>
      <td>0.02</td>
      <td>63,920.54</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>58040</td>
      <td>29,019.80</td>
      <td>27,079.20</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>55527</td>
      <td>0.73</td>
      <td>0.02</td>
      <td>1.37</td>
      <td>0.23</td>
      <td>0.01</td>
      <td>16,791.84</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>76162</td>
      <td>38,080.74</td>
      <td>17,446.26</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>6743</td>
      <td>0.78</td>
      <td>0.00</td>
      <td>1.66</td>
      <td>0.28</td>
      <td>0.00</td>
      <td>2,929.13</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>8614</td>
      <td>4,306.97</td>
      <td>2,436.03</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>17949</td>
      <td>0.91</td>
      <td>0.01</td>
      <td>3.10</td>
      <td>0.41</td>
      <td>0.01</td>
      <td>15,186.21</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>19802</td>
      <td>9,900.93</td>
      <td>8,048.07</td>
      <td>NEGATED</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>5932</td>
      <td>0.55</td>
      <td>0.00</td>
      <td>0.12</td>
      <td>0.05</td>
      <td>0.00</td>
      <td>91.19</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>10870</td>
      <td>5,434.96</td>
      <td>497.04</td>
      <td>NEGATED</td>
    </tr>
  </tbody>
</table>
</div>




```python
adv_am.filter(MIR_FOCUS)
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
      <th>f_MIR</th>
      <th>P1_MIR</th>
      <th>P2_MIR</th>
      <th>LRC_MIR</th>
      <th>dP1_MIR</th>
      <th>dP2_MIR</th>
      <th>G2_MIR</th>
      <th>N_MIR</th>
      <th>f1_MIR</th>
      <th>f2_MIR</th>
      <th>exp_f_MIR</th>
      <th>unexp_f_MIR</th>
      <th>l1_MIR</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>necessarily</th>
      <td>963</td>
      <td>0.97</td>
      <td>0.00</td>
      <td>3.86</td>
      <td>0.47</td>
      <td>0.00</td>
      <td>1,114.70</td>
      <td>583470</td>
      <td>291732</td>
      <td>992</td>
      <td>495.99</td>
      <td>467.01</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>that</th>
      <td>4308</td>
      <td>0.94</td>
      <td>0.01</td>
      <td>3.66</td>
      <td>0.45</td>
      <td>0.01</td>
      <td>4,405.21</td>
      <td>583470</td>
      <td>291732</td>
      <td>4559</td>
      <td>2,279.48</td>
      <td>2,028.52</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>813</td>
      <td>0.94</td>
      <td>0.00</td>
      <td>2.95</td>
      <td>0.44</td>
      <td>0.00</td>
      <td>790.27</td>
      <td>583470</td>
      <td>291732</td>
      <td>869</td>
      <td>434.50</td>
      <td>378.50</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>any</th>
      <td>1066</td>
      <td>0.97</td>
      <td>0.00</td>
      <td>4.00</td>
      <td>0.47</td>
      <td>0.00</td>
      <td>1,252.02</td>
      <td>583470</td>
      <td>291732</td>
      <td>1095</td>
      <td>547.49</td>
      <td>518.51</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>1840</td>
      <td>0.94</td>
      <td>0.01</td>
      <td>3.37</td>
      <td>0.44</td>
      <td>0.01</td>
      <td>1,849.23</td>
      <td>583470</td>
      <td>291732</td>
      <td>1953</td>
      <td>976.49</td>
      <td>863.51</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>320</td>
      <td>0.76</td>
      <td>0.00</td>
      <td>0.90</td>
      <td>0.26</td>
      <td>0.00</td>
      <td>122.77</td>
      <td>583470</td>
      <td>291732</td>
      <td>419</td>
      <td>209.50</td>
      <td>110.50</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>403</td>
      <td>0.71</td>
      <td>0.00</td>
      <td>0.67</td>
      <td>0.21</td>
      <td>0.00</td>
      <td>107.39</td>
      <td>583470</td>
      <td>291732</td>
      <td>564</td>
      <td>282.00</td>
      <td>121.00</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>9243</td>
      <td>0.92</td>
      <td>0.03</td>
      <td>3.30</td>
      <td>0.43</td>
      <td>0.03</td>
      <td>8,516.58</td>
      <td>583470</td>
      <td>291732</td>
      <td>10029</td>
      <td>5,014.45</td>
      <td>4,228.55</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>2864</td>
      <td>0.86</td>
      <td>0.01</td>
      <td>2.24</td>
      <td>0.36</td>
      <td>0.01</td>
      <td>1,899.59</td>
      <td>583470</td>
      <td>291732</td>
      <td>3342</td>
      <td>1,670.98</td>
      <td>1,193.02</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>1567</td>
      <td>0.71</td>
      <td>0.01</td>
      <td>0.97</td>
      <td>0.21</td>
      <td>0.00</td>
      <td>406.49</td>
      <td>583470</td>
      <td>291732</td>
      <td>2204</td>
      <td>1,101.99</td>
      <td>465.01</td>
      <td>NEGMIR</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>4709</td>
      <td>0.98</td>
      <td>0.02</td>
      <td>5.17</td>
      <td>0.49</td>
      <td>0.02</td>
      <td>5,883.26</td>
      <td>583470</td>
      <td>291732</td>
      <td>4786</td>
      <td>2,392.98</td>
      <td>2,316.02</td>
      <td>NEGMIR</td>
    </tr>
  </tbody>
</table>
</div>




```python

adv_am.filter(items=FOCUS_MEANS)
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
      <th>mean_f</th>
      <th>mean_P1</th>
      <th>mean_P2</th>
      <th>mean_LRC</th>
      <th>mean_dP1</th>
      <th>mean_dP2</th>
      <th>mean_G2</th>
      <th>mean_N</th>
      <th>mean_f1</th>
      <th>mean_f2</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>necessarily</th>
      <td>592,138.00</td>
      <td>0.98</td>
      <td>0.01</td>
      <td>5.31</td>
      <td>0.48</td>
      <td>0.01</td>
      <td>28,682.92</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>21,939.00</td>
    </tr>
    <tr>
      <th>that</th>
      <td>634,283.83</td>
      <td>0.97</td>
      <td>0.03</td>
      <td>4.96</td>
      <td>0.48</td>
      <td>0.03</td>
      <td>109,454.89</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>85,617.50</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>592,565.00</td>
      <td>0.96</td>
      <td>0.01</td>
      <td>4.33</td>
      <td>0.46</td>
      <td>0.01</td>
      <td>27,830.50</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>22,686.00</td>
    </tr>
    <tr>
      <th>any</th>
      <td>583,195.83</td>
      <td>0.96</td>
      <td>0.00</td>
      <td>3.96</td>
      <td>0.46</td>
      <td>0.00</td>
      <td>8,551.79</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>8,666.50</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>580,167.83</td>
      <td>0.93</td>
      <td>0.00</td>
      <td>3.27</td>
      <td>0.43</td>
      <td>0.00</td>
      <td>3,462.40</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>4,057.00</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>595,313.17</td>
      <td>0.86</td>
      <td>0.01</td>
      <td>2.71</td>
      <td>0.37</td>
      <td>0.01</td>
      <td>29,011.45</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>27,150.00</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>596,749.67</td>
      <td>0.84</td>
      <td>0.01</td>
      <td>2.68</td>
      <td>0.34</td>
      <td>0.01</td>
      <td>32,013.96</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>29,302.00</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>602,725.50</td>
      <td>0.83</td>
      <td>0.02</td>
      <td>2.33</td>
      <td>0.33</td>
      <td>0.02</td>
      <td>12,654.21</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>43,095.50</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>581,159.17</td>
      <td>0.82</td>
      <td>0.01</td>
      <td>1.95</td>
      <td>0.32</td>
      <td>0.00</td>
      <td>2,414.36</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>5,978.00</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>584,485.67</td>
      <td>0.81</td>
      <td>0.01</td>
      <td>2.03</td>
      <td>0.31</td>
      <td>0.00</td>
      <td>7,796.35</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>11,003.00</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>581,948.17</td>
      <td>0.76</td>
      <td>0.01</td>
      <td>2.65</td>
      <td>0.27</td>
      <td>0.01</td>
      <td>2,987.23</td>
      <td>3465417</td>
      <td>1732696</td>
      <td>7,828.00</td>
    </tr>
  </tbody>
</table>
</div>




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
compare_datasets(adv_am, METRIC_PRIORITY[0])
```

    Top 5 by descending `LRC_SET`
    | adv         |   LRC_SET |   LRC_MIR |   mean_LRC |
    |:------------|----------:|----------:|-----------:|
    | necessarily |      6.77 |      3.86 |       5.31 |
    | that        |      6.26 |      3.66 |       4.96 |
    | exactly     |      5.71 |      2.95 |       4.33 |
    | immediately |      4.68 |      0.67 |       2.68 |
    | yet         |      4.52 |      0.90 |       2.71 | 
    
    Top 5 by descending `LRC_MIR`
    | adv         |   LRC_SET |   LRC_MIR |   mean_LRC |
    |:------------|----------:|----------:|-----------:|
    | ever        |      0.12 |      5.17 |       2.65 |
    | any         |      3.91 |      4.00 |       3.96 |
    | necessarily |      6.77 |      3.86 |       5.31 |
    | that        |      6.26 |      3.66 |       4.96 |
    | remotely    |      3.16 |      3.37 |       3.27 | 
    
    Top 5 by descending `mean_LRC`
    | adv         |   LRC_SET |   LRC_MIR |   mean_LRC |
    |:------------|----------:|----------:|-----------:|
    | necessarily |      6.77 |      3.86 |       5.31 |
    | that        |      6.26 |      3.66 |       4.96 |
    | exactly     |      5.71 |      2.95 |       4.33 |
    | any         |      3.91 |      4.00 |       3.96 |
    | remotely    |      3.16 |      3.37 |       3.27 | 
    



```python
compare_datasets(adv_am, METRIC_PRIORITY[1])
```

    Top 5 by descending `dP1_SET`
    | adv         |   dP1_SET |   P1_SET |   dP1_MIR |   P1_MIR |   mean_dP1 |   mean_P1 |
    |:------------|----------:|---------:|----------:|---------:|-----------:|----------:|
    | that        |     0.502 |    0.989 |     0.449 |    0.945 |      0.475 |     0.967 |
    | necessarily |     0.497 |    0.993 |     0.472 |    0.971 |      0.484 |     0.982 |
    | exactly     |     0.488 |    0.985 |     0.436 |    0.936 |      0.462 |     0.960 |
    | immediately |     0.471 |    0.967 |     0.215 |    0.715 |      0.343 |     0.841 |
    | yet         |     0.467 |    0.963 |     0.264 |    0.764 |      0.365 |     0.863 | 
    
    Top 5 by descending `P1_SET`
    | adv         |   dP1_SET |   P1_SET |   dP1_MIR |   P1_MIR |   mean_dP1 |   mean_P1 |
    |:------------|----------:|---------:|----------:|---------:|-----------:|----------:|
    | necessarily |     0.497 |    0.993 |     0.472 |    0.971 |      0.484 |     0.982 |
    | that        |     0.502 |    0.989 |     0.449 |    0.945 |      0.475 |     0.967 |
    | exactly     |     0.488 |    0.985 |     0.436 |    0.936 |      0.462 |     0.960 |
    | immediately |     0.471 |    0.967 |     0.215 |    0.715 |      0.343 |     0.841 |
    | yet         |     0.467 |    0.963 |     0.264 |    0.764 |      0.365 |     0.863 | 
    
    Top 5 by descending `dP1_MIR`
    | adv         |   dP1_SET |   P1_SET |   dP1_MIR |   P1_MIR |   mean_dP1 |   mean_P1 |
    |:------------|----------:|---------:|----------:|---------:|-----------:|----------:|
    | ever        |     0.046 |    0.546 |     0.488 |    0.984 |      0.267 |     0.765 |
    | any         |     0.449 |    0.947 |     0.474 |    0.974 |      0.462 |     0.961 |
    | necessarily |     0.497 |    0.993 |     0.472 |    0.971 |      0.484 |     0.982 |
    | that        |     0.502 |    0.989 |     0.449 |    0.945 |      0.475 |     0.967 |
    | remotely    |     0.419 |    0.919 |     0.444 |    0.942 |      0.431 |     0.930 | 
    
    Top 5 by descending `P1_MIR`
    | adv         |   dP1_SET |   P1_SET |   dP1_MIR |   P1_MIR |   mean_dP1 |   mean_P1 |
    |:------------|----------:|---------:|----------:|---------:|-----------:|----------:|
    | ever        |     0.046 |    0.546 |     0.488 |    0.984 |      0.267 |     0.765 |
    | any         |     0.449 |    0.947 |     0.474 |    0.974 |      0.462 |     0.961 |
    | necessarily |     0.497 |    0.993 |     0.472 |    0.971 |      0.484 |     0.982 |
    | that        |     0.502 |    0.989 |     0.449 |    0.945 |      0.475 |     0.967 |
    | remotely    |     0.419 |    0.919 |     0.444 |    0.942 |      0.431 |     0.930 | 
    
    Top 5 by descending `mean_dP1`
    | adv         |   dP1_SET |   P1_SET |   dP1_MIR |   P1_MIR |   mean_dP1 |   mean_P1 |
    |:------------|----------:|---------:|----------:|---------:|-----------:|----------:|
    | necessarily |     0.497 |    0.993 |     0.472 |    0.971 |      0.484 |     0.982 |
    | that        |     0.502 |    0.989 |     0.449 |    0.945 |      0.475 |     0.967 |
    | exactly     |     0.488 |    0.985 |     0.436 |    0.936 |      0.462 |     0.960 |
    | any         |     0.449 |    0.947 |     0.474 |    0.974 |      0.462 |     0.961 |
    | remotely    |     0.419 |    0.919 |     0.444 |    0.942 |      0.431 |     0.930 | 
    
    Top 5 by descending `mean_P1`
    | adv         |   dP1_SET |   P1_SET |   dP1_MIR |   P1_MIR |   mean_dP1 |   mean_P1 |
    |:------------|----------:|---------:|----------:|---------:|-----------:|----------:|
    | necessarily |     0.497 |    0.993 |     0.472 |    0.971 |      0.484 |     0.982 |
    | that        |     0.502 |    0.989 |     0.449 |    0.945 |      0.475 |     0.967 |
    | any         |     0.449 |    0.947 |     0.474 |    0.974 |      0.462 |     0.961 |
    | exactly     |     0.488 |    0.985 |     0.436 |    0.936 |      0.462 |     0.960 |
    | remotely    |     0.419 |    0.919 |     0.444 |    0.942 |      0.431 |     0.930 | 
    



```python
compare_datasets(adv_am, METRIC_PRIORITY[2])
```

    Top 5 by descending `G2_SET`
    | adv         |    G2_SET |   G2_MIR |   mean_G2 |
    |:------------|----------:|---------:|----------:|
    | that        | 214,504.6 |  4,405.2 | 109,454.9 |
    | immediately |  63,920.5 |    107.4 |  32,014.0 |
    | yet         |  57,900.1 |    122.8 |  29,011.4 |
    | necessarily |  56,251.1 |  1,114.7 |  28,682.9 |
    | exactly     |  54,870.7 |    790.3 |  27,830.5 | 
    
    Top 5 by descending `G2_MIR`
    | adv          |    G2_SET |   G2_MIR |   mean_G2 |
    |:-------------|----------:|---------:|----------:|
    | particularly |  16,791.8 |  8,516.6 |  12,654.2 |
    | ever         |      91.2 |  5,883.3 |   2,987.2 |
    | that         | 214,504.6 |  4,405.2 | 109,454.9 |
    | inherently   |   2,929.1 |  1,899.6 |   2,414.4 |
    | remotely     |   5,075.6 |  1,849.2 |   3,462.4 | 
    
    Top 5 by descending `mean_G2`
    | adv         |    G2_SET |   G2_MIR |   mean_G2 |
    |:------------|----------:|---------:|----------:|
    | that        | 214,504.6 |  4,405.2 | 109,454.9 |
    | immediately |  63,920.5 |    107.4 |  32,014.0 |
    | yet         |  57,900.1 |    122.8 |  29,011.4 |
    | necessarily |  56,251.1 |  1,114.7 |  28,682.9 |
    | exactly     |  54,870.7 |    790.3 |  27,830.5 | 
    



```python
compare_datasets(adv_am, 'f_')
```

    Top 5 by descending `f_SET`
    | adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | that         | 164,768 |      83,337 |        81,431 |   4,308 |       2,279 |         2,029 |         3 |
    | immediately  |  56,099 |      29,020 |        27,079 |     403 |         282 |           121 |         1 |
    | particularly |  55,527 |      38,081 |        17,446 |   9,243 |       5,014 |         4,229 |        17 |
    | yet          |  51,867 |      26,940 |        24,927 |     320 |         209 |           111 |         1 |
    | exactly      |  43,813 |      22,251 |        21,562 |     813 |         434 |           379 |         2 | 
    
    Top 5 by descending `exp_f_SET`
    | adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | that         | 164,768 |      83,337 |        81,431 |   4,308 |       2,279 |         2,029 |         3 |
    | particularly |  55,527 |      38,081 |        17,446 |   9,243 |       5,014 |         4,229 |        17 |
    | immediately  |  56,099 |      29,020 |        27,079 |     403 |         282 |           121 |         1 |
    | yet          |  51,867 |      26,940 |        24,927 |     320 |         209 |           111 |         1 |
    | exactly      |  43,813 |      22,251 |        21,562 |     813 |         434 |           379 |         2 | 
    
    Top 5 by descending `unexp_f_SET`
    | adv         |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | that        | 164,768 |      83,337 |        81,431 |   4,308 |       2,279 |         2,029 |         3 |
    | immediately |  56,099 |      29,020 |        27,079 |     403 |         282 |           121 |         1 |
    | yet         |  51,867 |      26,940 |        24,927 |     320 |         209 |           111 |         1 |
    | exactly     |  43,813 |      22,251 |        21,562 |     813 |         434 |           379 |         2 |
    | necessarily |  42,595 |      21,443 |        21,152 |     963 |         496 |           467 |         2 | 
    
    Top 5 by descending `f_MIR`
    | adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | particularly |  55,527 |      38,081 |        17,446 |   9,243 |       5,014 |         4,229 |        17 |
    | ever         |   5,932 |       5,435 |           497 |   4,709 |       2,393 |         2,316 |        79 |
    | that         | 164,768 |      83,337 |        81,431 |   4,308 |       2,279 |         2,029 |         3 |
    | inherently   |   6,743 |       4,307 |         2,436 |   2,864 |       1,671 |         1,193 |        42 |
    | remotely     |   5,661 |       3,080 |         2,581 |   1,840 |         976 |           864 |        32 | 
    
    Top 5 by descending `exp_f_MIR`
    | adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | particularly |  55,527 |      38,081 |        17,446 |   9,243 |       5,014 |         4,229 |        17 |
    | ever         |   5,932 |       5,435 |           497 |   4,709 |       2,393 |         2,316 |        79 |
    | that         | 164,768 |      83,337 |        81,431 |   4,308 |       2,279 |         2,029 |         3 |
    | inherently   |   6,743 |       4,307 |         2,436 |   2,864 |       1,671 |         1,193 |        42 |
    | terribly     |  17,949 |       9,901 |         8,048 |   1,567 |       1,102 |           465 |         9 | 
    
    Top 5 by descending `unexp_f_MIR`
    | adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | particularly |  55,527 |      38,081 |        17,446 |   9,243 |       5,014 |         4,229 |        17 |
    | ever         |   5,932 |       5,435 |           497 |   4,709 |       2,393 |         2,316 |        79 |
    | that         | 164,768 |      83,337 |        81,431 |   4,308 |       2,279 |         2,029 |         3 |
    | inherently   |   6,743 |       4,307 |         2,436 |   2,864 |       1,671 |         1,193 |        42 |
    | remotely     |   5,661 |       3,080 |         2,581 |   1,840 |         976 |           864 |        32 | 
    
    Top 5 by descending `%_f_MIR`
    | adv          |   f_SET |   exp_f_SET |   unexp_f_SET |   f_MIR |   exp_f_MIR |   unexp_f_MIR |   %_f_MIR |
    |:-------------|--------:|------------:|--------------:|--------:|------------:|--------------:|----------:|
    | ever         |   5,932 |     5,435.0 |         497.0 |   4,709 |     2,393.0 |       2,316.0 |      79.4 |
    | inherently   |   6,743 |     4,307.0 |       2,436.0 |   2,864 |     1,671.0 |       1,193.0 |      42.5 |
    | remotely     |   5,661 |     3,080.5 |       2,580.5 |   1,840 |       976.5 |         863.5 |      32.5 |
    | particularly |  55,527 |    38,080.7 |      17,446.3 |   9,243 |     5,014.4 |       4,228.6 |      16.7 |
    | terribly     |  17,949 |     9,900.9 |       8,048.1 |   1,567 |     1,102.0 |         465.0 |       8.7 | 
    



```python
compare_datasets(adv_am, 'f2')
```

    Top 5 by descending `f2_SET`
    | adv          |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
    |:-------------|---------:|---------:|----------:|-----------:|
    | that         |  166,676 |    4,559 |    85,618 |          3 |
    | particularly |   76,162 |   10,029 |    43,096 |         13 |
    | immediately  |   58,040 |      564 |    29,302 |          1 |
    | yet          |   53,881 |      419 |    27,150 |          1 |
    | exactly      |   44,503 |      869 |    22,686 |          2 | 
    
    Top 5 by descending `f2_MIR`
    | adv          |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
    |:-------------|---------:|---------:|----------:|-----------:|
    | particularly |   76,162 |   10,029 |    43,096 |         13 |
    | ever         |   10,870 |    4,786 |     7,828 |         44 |
    | that         |  166,676 |    4,559 |    85,618 |          3 |
    | inherently   |    8,614 |    3,342 |     5,978 |         39 |
    | terribly     |   19,802 |    2,204 |    11,003 |         11 | 
    
    Top 5 by descending `mean_f2`
    | adv          |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
    |:-------------|---------:|---------:|----------:|-----------:|
    | that         |  166,676 |    4,559 | 85,617.50 |       2.74 |
    | particularly |   76,162 |   10,029 | 43,095.50 |      13.17 |
    | immediately  |   58,040 |      564 | 29,302.00 |       0.97 |
    | yet          |   53,881 |      419 | 27,150.00 |       0.78 |
    | exactly      |   44,503 |      869 | 22,686.00 |       1.95 | 
    
    Top 5 by descending `%_f2_MIR`
    | adv          |   f2_SET |   f2_MIR |   mean_f2 |   %_f2_MIR |
    |:-------------|---------:|---------:|----------:|-----------:|
    | ever         |   10,870 |    4,786 |   7,828.0 |       44.0 |
    | inherently   |    8,614 |    3,342 |   5,978.0 |       38.8 |
    | remotely     |    6,161 |    1,953 |   4,057.0 |       31.7 |
    | particularly |   76,162 |   10,029 |  43,095.5 |       13.2 |
    | terribly     |   19,802 |    2,204 |  11,003.0 |       11.1 | 
    



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


TOP_ADV, adv_am = pin_top_adv(adv_am, select_col=f'mean_{METRIC_PRIORITY[0]}')
```

    Top Adverb Selection, ranked by descending `'mean_LRC'`
    
    |    | adv          |   mean_LRC |
    |---:|:-------------|-----------:|
    |  1 | necessarily  |      5.314 |
    |  2 | that         |      4.959 |
    |  3 | exactly      |      4.329 |
    |  4 | any          |      3.960 |
    |  5 | remotely     |      3.267 |
    |  6 | yet          |      2.709 |
    |  7 | immediately  |      2.677 |
    |  8 | ever         |      2.647 |
    |  9 | particularly |      2.332 |
    | 10 | terribly     |      2.032 |
    | 11 | inherently   |      1.947 |
    



```python
__ = pin_top_adv(adv_am, select_col=adv_am.filter([f'mean_{m}' for m in METRIC_PRIORITY]).columns.to_list())
```

    Top Adverb Selection, ranked by descending `['mean_LRC', 'mean_P1', 'mean_G2', 'mean_P2']`
    
    |    | adv          |   mean_LRC |   mean_P1 |     mean_G2 |   mean_P2 |
    |---:|:-------------|-----------:|----------:|------------:|----------:|
    |  1 | necessarily  |      5.314 |     0.982 |  28,682.921 |     0.008 |
    |  2 | that         |      4.959 |     0.967 | 109,454.888 |     0.033 |
    |  3 | exactly      |      4.329 |     0.960 |  27,830.497 |     0.008 |
    |  4 | any          |      3.960 |     0.961 |   8,551.790 |     0.004 |
    |  5 | remotely     |      3.267 |     0.930 |   3,462.397 |     0.004 |
    |  6 | yet          |      2.709 |     0.863 |  29,011.445 |     0.009 |
    |  7 | immediately  |      2.677 |     0.841 |  32,013.962 |     0.009 |
    |  8 | ever         |      2.647 |     0.765 |   2,987.225 |     0.009 |
    |  9 | particularly |      2.332 |     0.825 |  12,654.208 |     0.025 |
    | 10 | terribly     |      2.032 |     0.809 |   7,796.354 |     0.005 |
    | 11 | inherently   |      1.947 |     0.820 |   2,414.362 |     0.006 |
    



```python
bigram_am = adjust_assoc_columns(pd.read_csv(OUT_DIR / f'{TAG_TOP_STR}_NEG-ADV-{ADV_F_FLOOR}_top-{BK}-bigrams-{BIGRAM_F_FLOOR}.{DATE}.csv')
             .set_index('key')
             #> not strictly necessary (loaded table should already satisfy this) but just in case...
             .filter(regex=r'|'.join([f'~{a}_' for a in TOP_ADV]), axis=0)
             )
bigram_am
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
      <th>G2</th>
      <th>MI</th>
      <th>odds_r_disc</th>
      <th>t</th>
      <th>N</th>
      <th>f1</th>
      <th>...</th>
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>l1</th>
      <th>l2</th>
      <th>adv</th>
      <th>adv_total</th>
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
      <th>NEGany~yet_clear</th>
      <td>10406</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>8.66</td>
      <td>14,392.25</td>
      <td>0.30</td>
      <td>3.47</td>
      <td>50.99</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>...</td>
      <td>5,204.46</td>
      <td>5,201.54</td>
      <td>NEGATED</td>
      <td>yet_clear</td>
      <td>yet</td>
      <td>53881</td>
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
      <td>10,344.81</td>
      <td>0.30</td>
      <td>3.22</td>
      <td>43.28</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>...</td>
      <td>3,752.47</td>
      <td>3,748.53</td>
      <td>NEGATED</td>
      <td>yet_ready</td>
      <td>yet</td>
      <td>53881</td>
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
      <td>13,602.42</td>
      <td>0.30</td>
      <td>2.81</td>
      <td>49.79</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>...</td>
      <td>4,981.47</td>
      <td>4,966.53</td>
      <td>NEGATED</td>
      <td>that_hard</td>
      <td>that</td>
      <td>166676</td>
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
      <td>33,058.44</td>
      <td>0.30</td>
      <td>2.53</td>
      <td>77.90</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>...</td>
      <td>12,243.92</td>
      <td>12,172.08</td>
      <td>NEGATED</td>
      <td>immediately_clear</td>
      <td>immediately</td>
      <td>58040</td>
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
      <td>11,991.61</td>
      <td>0.30</td>
      <td>2.73</td>
      <td>46.80</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>...</td>
      <td>4,404.97</td>
      <td>4,389.03</td>
      <td>NEGATED</td>
      <td>exactly_sure</td>
      <td>exactly</td>
      <td>44503</td>
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
      <th>NEGmir~remotely_comparable</th>
      <td>44</td>
      <td>0.50</td>
      <td>1.00</td>
      <td>1.15</td>
      <td>61.00</td>
      <td>0.30</td>
      <td>1.95</td>
      <td>3.32</td>
      <td>583470</td>
      <td>291732</td>
      <td>...</td>
      <td>22.00</td>
      <td>22.00</td>
      <td>NEGMIR</td>
      <td>remotely_comparable</td>
      <td>remotely</td>
      <td>1953</td>
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
      <td>65.16</td>
      <td>0.30</td>
      <td>1.98</td>
      <td>3.43</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>...</td>
      <td>23.50</td>
      <td>23.50</td>
      <td>NEGATED</td>
      <td>remotely_enough</td>
      <td>remotely</td>
      <td>6161</td>
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
      <td>149.75</td>
      <td>0.20</td>
      <td>0.59</td>
      <td>6.63</td>
      <td>583470</td>
      <td>291729</td>
      <td>...</td>
      <td>200.50</td>
      <td>118.50</td>
      <td>POSMIR</td>
      <td>terribly_wrong</td>
      <td>terribly</td>
      <td>2204</td>
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
      <td>63.56</td>
      <td>0.29</td>
      <td>1.54</td>
      <td>3.54</td>
      <td>6347364</td>
      <td>3173552</td>
      <td>...</td>
      <td>26.50</td>
      <td>25.50</td>
      <td>COMPLEMENT</td>
      <td>ever_mindful</td>
      <td>ever</td>
      <td>10870</td>
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
      <td>56.84</td>
      <td>0.30</td>
      <td>1.92</td>
      <td>3.20</td>
      <td>583470</td>
      <td>291732</td>
      <td>...</td>
      <td>20.50</td>
      <td>20.50</td>
      <td>NEGMIR</td>
      <td>that_happy</td>
      <td>that</td>
      <td>4559</td>
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
bigram_am = bigram_am.filter(items=FOCUS).convert_dtypes()
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
      <th>P1</th>
      <th>P2</th>
      <th>LRC</th>
      <th>dP1</th>
      <th>dP2</th>
      <th>G2</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>adv_total</th>
      <th>adj_total</th>
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
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>NEGany~yet_clear</th>
      <td>10406</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>8.66</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>14,392.25</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>10409</td>
      <td>5,204.46</td>
      <td>5,201.54</td>
      <td>53881</td>
      <td>84227</td>
      <td>NEGATED</td>
      <td>yet_clear</td>
      <td>yet</td>
      <td>clear</td>
    </tr>
    <tr>
      <th>NEGany~yet_ready</th>
      <td>7501</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>8.06</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>10,344.81</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>7505</td>
      <td>3,752.47</td>
      <td>3,748.53</td>
      <td>53881</td>
      <td>29583</td>
      <td>NEGATED</td>
      <td>yet_ready</td>
      <td>yet</td>
      <td>ready</td>
    </tr>
    <tr>
      <th>NEGany~that_hard</th>
      <td>9948</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>7.68</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>13,602.42</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>9963</td>
      <td>4,981.47</td>
      <td>4,966.53</td>
      <td>166676</td>
      <td>45061</td>
      <td>NEGATED</td>
      <td>that_hard</td>
      <td>that</td>
      <td>hard</td>
    </tr>
    <tr>
      <th>NEGany~immediately_clear</th>
      <td>24416</td>
      <td>1.00</td>
      <td>0.01</td>
      <td>7.55</td>
      <td>0.50</td>
      <td>0.01</td>
      <td>33,058.44</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>24488</td>
      <td>12,243.92</td>
      <td>12,172.08</td>
      <td>58040</td>
      <td>84227</td>
      <td>NEGATED</td>
      <td>immediately_clear</td>
      <td>immediately</td>
      <td>clear</td>
    </tr>
    <tr>
      <th>NEGany~exactly_sure</th>
      <td>8794</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>7.46</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>11,991.61</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>8810</td>
      <td>4,404.97</td>
      <td>4,389.03</td>
      <td>44503</td>
      <td>134139</td>
      <td>NEGATED</td>
      <td>exactly_sure</td>
      <td>exactly</td>
      <td>sure</td>
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
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>NEGmir~remotely_comparable</th>
      <td>44</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>1.15</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>61.00</td>
      <td>583470</td>
      <td>291732</td>
      <td>44</td>
      <td>22.00</td>
      <td>22.00</td>
      <td>1953</td>
      <td>158</td>
      <td>NEGMIR</td>
      <td>remotely_comparable</td>
      <td>remotely</td>
      <td>comparable</td>
    </tr>
    <tr>
      <th>NEGany~remotely_enough</th>
      <td>47</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>1.13</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>65.16</td>
      <td>6347364</td>
      <td>3173660</td>
      <td>47</td>
      <td>23.50</td>
      <td>23.50</td>
      <td>6161</td>
      <td>27603</td>
      <td>NEGATED</td>
      <td>remotely_enough</td>
      <td>remotely</td>
      <td>enough</td>
    </tr>
    <tr>
      <th>POS~terribly_wrong</th>
      <td>319</td>
      <td>0.80</td>
      <td>0.00</td>
      <td>1.06</td>
      <td>0.30</td>
      <td>0.00</td>
      <td>149.75</td>
      <td>583470</td>
      <td>291729</td>
      <td>401</td>
      <td>200.50</td>
      <td>118.50</td>
      <td>2204</td>
      <td>8506</td>
      <td>POSMIR</td>
      <td>terribly_wrong</td>
      <td>terribly</td>
      <td>wrong</td>
    </tr>
    <tr>
      <th>COM~ever_mindful</th>
      <td>52</td>
      <td>0.98</td>
      <td>0.00</td>
      <td>1.04</td>
      <td>0.48</td>
      <td>0.00</td>
      <td>63.56</td>
      <td>6347364</td>
      <td>3173552</td>
      <td>53</td>
      <td>26.50</td>
      <td>25.50</td>
      <td>10870</td>
      <td>784</td>
      <td>COMPLEMENT</td>
      <td>ever_mindful</td>
      <td>ever</td>
      <td>mindful</td>
    </tr>
    <tr>
      <th>NEGmir~that_happy</th>
      <td>41</td>
      <td>1.00</td>
      <td>0.00</td>
      <td>1.03</td>
      <td>0.50</td>
      <td>0.00</td>
      <td>56.84</td>
      <td>583470</td>
      <td>291732</td>
      <td>41</td>
      <td>20.50</td>
      <td>20.50</td>
      <td>4559</td>
      <td>5463</td>
      <td>NEGMIR</td>
      <td>that_happy</td>
      <td>that</td>
      <td>happy</td>
    </tr>
  </tbody>
</table>
<p>155 rows × 18 columns</p>
</div>




```python
overall_k = int(BK/2 * K)
nb_show_table(bigram_am.round(2).nlargest(overall_k, columns=METRIC_PRIORITY),
            outpath=OUT_DIR / f'{TAG}-Top{K}_NEG-ADV-{ADV_F_FLOOR}_top{overall_k}bigrams-overall.min{BIGRAM_F_FLOOR}.md', 
            suppress_printing=not VERBOSE)
```

    
    |                                   |    `f` |   `P1` |   `P2` |   `LRC` |   `dP1` |   `dP2` |      `G2` |       `N` |      `f1` |   `f2` |   `exp_f` |   `unexp_f` |   `adv_total` |   `adj_total` | `l1`    | `l2`                   | `adv`        | `adj`      |
    |:----------------------------------|-------:|-------:|-------:|--------:|--------:|--------:|----------:|----------:|----------:|-------:|----------:|------------:|--------------:|--------------:|:--------|:-----------------------|:-------------|:-----------|
    | **NEGany~yet_clear**              | 10,406 |   1.00 |   0.00 |    8.66 |    0.50 |    0.00 | 14,392.25 | 6,347,364 | 3,173,660 | 10,409 |  5,204.46 |    5,201.54 |        53,881 |        84,227 | NEGATED | yet_clear              | yet          | clear      |
    | **NEGany~yet_ready**              |  7,501 |   1.00 |   0.00 |    8.06 |    0.50 |    0.00 | 10,344.81 | 6,347,364 | 3,173,660 |  7,505 |  3,752.47 |    3,748.53 |        53,881 |        29,583 | NEGATED | yet_ready              | yet          | ready      |
    | **NEGany~that_hard**              |  9,948 |   1.00 |   0.00 |    7.68 |    0.50 |    0.00 | 13,602.42 | 6,347,364 | 3,173,660 |  9,963 |  4,981.47 |    4,966.53 |       166,676 |        45,061 | NEGATED | that_hard              | that         | hard       |
    | **NEGany~immediately_clear**      | 24,416 |   1.00 |   0.01 |    7.55 |    0.50 |    0.01 | 33,058.44 | 6,347,364 | 3,173,660 | 24,488 | 12,243.92 |   12,172.08 |        58,040 |        84,227 | NEGATED | immediately_clear      | immediately  | clear      |
    | **NEGany~exactly_sure**           |  8,794 |   1.00 |   0.00 |    7.46 |    0.50 |    0.00 | 11,991.61 | 6,347,364 | 3,173,660 |  8,810 |  4,404.97 |    4,389.03 |        44,503 |       134,139 | NEGATED | exactly_sure           | exactly      | sure       |
    | **NEGany~that_great**             | 11,032 |   1.00 |   0.00 |    7.18 |    0.50 |    0.00 | 14,908.90 | 6,347,364 | 3,173,660 | 11,065 |  5,532.46 |    5,499.54 |       166,676 |        45,359 | NEGATED | that_great             | that         | great      |
    | **NEGany~that_different**         |  6,534 |   1.00 |   0.00 |    7.18 |    0.50 |    0.00 |  8,895.12 | 6,347,364 | 3,173,660 |  6,547 |  3,273.48 |    3,260.52 |       166,676 |        80,643 | NEGATED | that_different         | that         | different  |
    | **NEGany~that_difficult**         |  5,560 |   1.00 |   0.00 |    7.06 |    0.50 |    0.00 |  7,569.00 | 6,347,364 | 3,173,660 |  5,571 |  2,785.48 |    2,774.52 |       166,676 |        61,490 | NEGATED | that_difficult         | that         | difficult  |
    | **NEGany~yet_complete**           |  2,174 |   1.00 |   0.00 |    6.70 |    0.50 |    0.00 |  2,998.60 | 6,347,364 | 3,173,660 |  2,175 |  1,087.49 |    1,086.51 |        53,881 |         8,415 | NEGATED | yet_complete           | yet          | complete   |
    | **NEGany~yet_available**          |  7,430 |   1.00 |   0.00 |    6.66 |    0.50 |    0.00 |  9,950.03 | 6,347,364 | 3,173,660 |  7,461 |  3,730.47 |    3,699.53 |        53,881 |        82,956 | NEGATED | yet_available          | yet          | available  |
    | **NEGany~that_big**               |  6,244 |   1.00 |   0.00 |    6.47 |    0.50 |    0.00 |  8,332.69 | 6,347,364 | 3,173,660 |  6,273 |  3,136.48 |    3,107.52 |       166,676 |        42,912 | NEGATED | that_big               | that         | big        |
    | **NEGany~exactly_clear**          |  1,746 |   1.00 |   0.00 |    6.38 |    0.50 |    0.00 |  2,405.43 | 6,347,364 | 3,173,660 |  1,747 |    873.49 |      872.51 |        44,503 |        84,227 | NEGATED | exactly_clear          | exactly      | clear      |
    | **NEGany~necessarily_bad**        |  2,059 |   1.00 |   0.00 |    6.31 |    0.50 |    0.00 |  2,814.04 | 6,347,364 | 3,173,660 |  2,062 |  1,030.99 |    1,028.01 |        42,886 |       119,509 | NEGATED | necessarily_bad        | necessarily  | bad        |
    | **NEGany~necessarily_indicative** |  1,389 |   1.00 |   0.00 |    6.29 |    0.50 |    0.00 |  1,925.89 | 6,347,364 | 3,173,660 |  1,389 |    694.50 |      694.50 |        42,886 |         2,313 | NEGATED | necessarily_indicative | necessarily  | indicative |
    | **NEGany~necessarily_true**       |  3,232 |   1.00 |   0.00 |    6.16 |    0.50 |    0.00 |  4,330.74 | 6,347,364 | 3,173,660 |  3,245 |  1,622.49 |    1,609.51 |        42,886 |        34,967 | NEGATED | necessarily_true       | necessarily  | true       |
    | **NEGany~yet_sure**               |  1,977 |   1.00 |   0.00 |    6.13 |    0.50 |    0.00 |  2,689.26 | 6,347,364 | 3,173,660 |  1,981 |    990.49 |      986.51 |        53,881 |       134,139 | NEGATED | yet_sure               | yet          | sure       |
    | **NEGany~necessarily_better**     |  1,887 |   1.00 |   0.00 |    6.07 |    0.50 |    0.00 |  2,564.81 | 6,347,364 | 3,173,660 |  1,891 |    945.49 |      941.51 |        42,886 |        50,827 | NEGATED | necessarily_better     | necessarily  | better     |
    | **NEGany~exactly_new**            |  1,371 |   1.00 |   0.00 |    6.03 |    0.50 |    0.00 |  1,885.86 | 6,347,364 | 3,173,660 |  1,372 |    686.00 |      685.00 |        44,503 |        21,538 | NEGATED | exactly_new            | exactly      | new        |
    | **NEGany~that_surprising**        |  1,133 |   1.00 |   0.00 |    5.99 |    0.50 |    0.00 |  1,570.89 | 6,347,364 | 3,173,660 |  1,133 |    566.50 |      566.50 |       166,676 |        18,776 | NEGATED | that_surprising        | that         | surprising |
    | **NEGany~that_unusual**           |    977 |   1.00 |   0.00 |    5.77 |    0.50 |    0.00 |  1,354.57 | 6,347,364 | 3,173,660 |    977 |    488.50 |      488.50 |       166,676 |         7,412 | NEGATED | that_unusual           | that         | unusual    |
    | **NEGany~terribly_surprising**    |    949 |   1.00 |   0.00 |    5.73 |    0.50 |    0.00 |  1,315.75 | 6,347,364 | 3,173,660 |    949 |    474.50 |      474.50 |        19,802 |        18,776 | NEGATED | terribly_surprising    | terribly     | surprising |
    | **NEGany~exactly_easy**           |  1,066 |   1.00 |   0.00 |    5.67 |    0.50 |    0.00 |  1,463.43 | 6,347,364 | 3,173,660 |  1,067 |    533.50 |      532.50 |        44,503 |       108,923 | NEGATED | exactly_easy           | exactly      | easy       |
    | **NEGany~necessarily_easy**       |    909 |   1.00 |   0.00 |    5.67 |    0.50 |    0.00 |  1,260.28 | 6,347,364 | 3,173,660 |    909 |    454.50 |      454.50 |        42,886 |       108,923 | NEGATED | necessarily_easy       | necessarily  | easy       |
    | **NEGany~yet_certain**            |    866 |   1.00 |   0.00 |    5.60 |    0.50 |    0.00 |  1,200.66 | 6,347,364 | 3,173,660 |    866 |    433.00 |      433.00 |        53,881 |        11,334 | NEGATED | yet_certain            | yet          | certain    |
    | **NEGany~that_exciting**          |    805 |   1.00 |   0.00 |    5.49 |    0.50 |    0.00 |  1,116.08 | 6,347,364 | 3,173,660 |    805 |    402.50 |      402.50 |       166,676 |        20,233 | NEGATED | that_exciting          | that         | exciting   |
    | **NEGany~that_uncommon**          |    802 |   1.00 |   0.00 |    5.49 |    0.50 |    0.00 |  1,111.92 | 6,347,364 | 3,173,660 |    802 |    401.00 |      401.00 |       166,676 |         3,165 | NEGATED | that_uncommon          | that         | uncommon   |
    | **NEGany~yet_able**               |  1,315 |   1.00 |   0.00 |    5.44 |    0.50 |    0.00 |  1,764.46 | 6,347,364 | 3,173,660 |  1,320 |    660.00 |      655.00 |        53,881 |        23,355 | NEGATED | yet_able               | yet          | able       |
    | **NEGany~immediately_possible**   |  1,000 |   1.00 |   0.00 |    5.40 |    0.50 |    0.00 |  1,360.38 | 6,347,364 | 3,173,660 |  1,002 |    501.00 |      499.00 |        58,040 |        30,446 | NEGATED | immediately_possible   | immediately  | possible   |
    | **NEGany~immediately_available**  | 21,078 |   0.98 |   0.01 |    5.34 |    0.48 |    0.01 | 25,870.14 | 6,347,364 | 3,173,660 | 21,477 | 10,738.43 |   10,339.57 |        58,040 |        82,956 | NEGATED | immediately_available  | immediately  | available  |
    | **NEGany~exactly_cheap**          |    691 |   1.00 |   0.00 |    5.27 |    0.50 |    0.00 |    958.01 | 6,347,364 | 3,173,660 |    691 |    345.50 |      345.50 |        44,503 |         6,591 | NEGATED | exactly_cheap          | exactly      | cheap      |
    | **NEGany~that_impressed**         |    681 |   1.00 |   0.00 |    5.25 |    0.50 |    0.00 |    944.15 | 6,347,364 | 3,173,660 |    681 |    340.50 |      340.50 |       166,676 |        12,138 | NEGATED | that_impressed         | that         | impressed  |
    | **NEGany~yet_final**              |    640 |   1.00 |   0.00 |    5.16 |    0.50 |    0.00 |    887.30 | 6,347,364 | 3,173,660 |    640 |    320.00 |      320.00 |        53,881 |         1,213 | NEGATED | yet_final              | yet          | final      |
    | **NEGany~necessarily_related**    |    741 |   1.00 |   0.00 |    5.14 |    0.50 |    0.00 |  1,013.51 | 6,347,364 | 3,173,660 |    742 |    371.00 |      370.00 |        42,886 |        14,260 | NEGATED | necessarily_related    | necessarily  | related    |
    | **NEGany~necessarily_new**        |    482 |   1.00 |   0.00 |    4.74 |    0.50 |    0.00 |    668.24 | 6,347,364 | 3,173,660 |    482 |    241.00 |      241.00 |        42,886 |        21,538 | NEGATED | necessarily_new        | necessarily  | new        |
    | **NEGany~yet_public**             |    467 |   1.00 |   0.00 |    4.69 |    0.50 |    0.00 |    647.44 | 6,347,364 | 3,173,660 |    467 |    233.50 |      233.50 |        53,881 |         2,656 | NEGATED | yet_public             | yet          | public     |
    | **NEGany~any_happier**            |    828 |   0.99 |   0.00 |    4.66 |    0.49 |    0.00 |  1,085.12 | 6,347,364 | 3,173,660 |    834 |    417.00 |      411.00 |        16,238 |         2,004 | NEGATED | any_happier            | any          | happier    |
    | **NEGany~exactly_surprising**     |    440 |   1.00 |   0.00 |    4.61 |    0.50 |    0.00 |    610.01 | 6,347,364 | 3,173,660 |    440 |    220.00 |      220.00 |        44,503 |        18,776 | NEGATED | exactly_surprising     | exactly      | surprising |
    | **NEGany~particularly_new**       |    747 |   0.99 |   0.00 |    4.61 |    0.49 |    0.00 |    982.49 | 6,347,364 | 3,173,660 |    752 |    376.00 |      371.00 |        76,162 |        21,538 | NEGATED | particularly_new       | particularly | new        |
    | **NEGany~particularly_religious** |    485 |   1.00 |   0.00 |    4.52 |    0.50 |    0.00 |    659.41 | 6,347,364 | 3,173,660 |    486 |    243.00 |      242.00 |        76,162 |         3,507 | NEGATED | particularly_religious | particularly | religious  |
    | **NEGany~yet_dead**               |    401 |   1.00 |   0.00 |    4.47 |    0.50 |    0.00 |    555.93 | 6,347,364 | 3,173,660 |    401 |    200.50 |      200.50 |        53,881 |         6,348 | NEGATED | yet_dead               | yet          | dead       |
    


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

    
    |                                              | `adv_form_lower`   | `adj_form_lower`   | `bigram_lower`         | `neg_form_lower`   | `all_forms_lower`          |
    |:---------------------------------------------|:-------------------|:-------------------|:-----------------------|:-------------------|:---------------------------|
    | **pcc_eng_18_032.3263_x0507015_12:20-21-22** | particularly       | sensitive          | particularly_sensitive | not                | not_particularly_sensitive |
    | **pcc_eng_24_104.3676_x1672484_55:7-8-9**    | yet                | visible            | yet_visible            | not                | not_yet_visible            |
    | **pcc_eng_02_002.2487_x0020178_09:19-20-21** | that               | great              | that_great             | n't                | n't_that_great             |
    



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
if VERBOSE:
    print(neg_hits.adv_lemma.value_counts().to_frame('Tokens in loaded sample').to_markdown(floatfmt=',.0f', intfmt=','))
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
if VERBOSE:
    fewer = sp(data=neg_hits, regex=True, print_sample=False,
           columns=['WITH::bigram|neg|str'], 
           filters=['neg_form_lower==fewer'])
    nb_show_table(fewer.assign(token_str=embolden(fewer.token_str, r' (fewer) ')), adjust_columns=False)
```

    
    - *filtering rows...*
      - regex parsing = True
      - ✓ Applied filter: `neg_form_lower==fewer`
    
    ### All (1) row(s) matching filter(s) from `input frame`
    
    
    |                                          | `token_str`                                                                                                      | `lemma_str`                                                                                       | `neg_head`   | `neg_lemma`   | `bigram_lower`   | `neg_form_lower`   |
    |:-----------------------------------------|:-----------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------|:-------------|:--------------|:-----------------|:-------------------|
    | **pcc_eng_04_001.4775_x0007747_3:4-6-7** | In 2D far __`fewer`__ are exactly solvable , the simplest being a rectangle with Dirichlet boundary conditions . | in 2d far few be exactly solvable , the simple be a rectangle with dirichlet boundary condition . | ADJ          | few           | exactly_solvable | fewer              |
    



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
if VERBOSE:
    nb_show_table(neg_hits.loc[(neg_hits.neg_form_lower!="n't") 
                   & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string')), 
                   ['neg_lemma', 'neg_form_lower', 'text_window']].sample(10))
```

    
    |                                               | `neg_lemma`   | `neg_form_lower`   | `text_window`                                                                                |
    |:----------------------------------------------|:--------------|:-------------------|:---------------------------------------------------------------------------------------------|
    | **pcc_eng_07_059.2522_x0941539_20:08-09-10**  | not           | nit                | auto dealersi argument for exclusivity is nit terribly persuasive .                          |
    | **pcc_eng_03_001.4762_x0007792_060:3-4-5**    | not           | nit                | it is nit particularly long or challenging or thought provoking .                            |
    | **pcc_eng_11_082.9573_x1326477_09:31-32-33**  | not           | nit                | tangible benefits of our activities are nit immediately obvious .                            |
    | **pcc_eng_05_093.2853_x1493084_225:09-10-11** | not           | aint               | hear about myself , and i aint any better than a baby to -day .                              |
    | **pcc_eng_10_026.4211_x0410765_076:3-4-5**    | not           | ain't              | It just ain't that easy .                                                                    |
    | **pcc_eng_16_058.2429_x0926754_27:27-28-29**  | not           | ain't              | say , " what it is ain't exactly clear . "                                                   |
    | **pcc_eng_04_001.4775_x0007747_3:4-6-7**      | few           | fewer              | in 2d far fewer are exactly solvable , the simplest being a rectangle                        |
    | **pcc_eng_17_008.4629_x0120703_35:2-3-4**     | not           | ain't              | That ain't necessarily true .                                                                |
    | **pcc_eng_10_028.7595_x0448752_056:08-09-10** | not           | ain't              | great trepidation , because this ink ain't particularly cheap , i diluted it with de-ionised |
    | **pcc_eng_27_060.4760_x0961220_52:6-7-8**     | not           | ain't              | which , frankly , still ain't that bad for what are 30 outsize full-colour                   |
    



```python
if VERBOSE:
    nb_show_table(neg_hits.loc[(neg_hits.neg_lemma!="not") 
                   & (neg_hits.neg_lemma.astype('string') != neg_hits.neg_form_lower.astype('string')), 
                   ['neg_lemma', 'neg_form_lower', 'text_window']])
```

    
    |                                               | `neg_lemma`   | `neg_form_lower`   | `text_window`                                                                     |
    |:----------------------------------------------|:--------------|:-------------------|:----------------------------------------------------------------------------------|
    | **pcc_eng_04_001.4775_x0007747_3:4-6-7**      | few           | fewer              | in 2d far fewer are exactly solvable , the simplest being a rectangle             |
    | **pcc_eng_09_031.5011_x0493764_43:04-12-13**  | nothing       | nothings           | And the ' nothings ' that these people talk about are inherently postmodern too . |
    | **pcc_eng_20_080.0820_x1277728_116:20-23-24** | nobody        | nobodies           | away from the story nobodies dick is that big and if it was having a              |
    



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

    
    |                                               | `adv_form_lower`   | `adj_form_lower`   | `bigrlower`    | `neg_form_lower`   | `all_forms_lower`   |
    |:----------------------------------------------|:-------------------|:-------------------|:---------------|:-------------------|:--------------------|
    | **pcc_eng_29_005.6672_x0075638_21:3-4-5**     | exactly            | happy              | exactly_happy  | n't                | n't_exactly_happy   |
    | **pcc_eng_07_018.9546_x0290393_077:14-15-16** | exactly            | afraid             | exactly_afraid | not                | not_exactly_afraid  |
    | **pcc_eng_17_079.8072_x1273653_63:24-25-26**  | exactly            | sharp              | exactly_sharp  | n't                | n't_exactly_sharp   |
    | **pcc_eng_08_048.9850_x0776740_04:13-14-15**  | exactly            | easy               | exactly_easy   | n't                | n't_exactly_easy    |
    | **pcc_eng_06_022.4137_x0346537_05:28-29-30**  | exactly            | rare               | exactly_rare   | not                | not_exactly_rare    |
    | **pcc_eng_09_001.9368_x0015202_064:3-4-5**    | exactly            | true               | exactly_true   | not                | not_exactly_true    |
    | **pcc_eng_00_070.2970_x1120156_38:14-15-16**  | exactly            | light              | exactly_light  | n't                | n't_exactly_light   |
    | **pcc_eng_02_004.6535_x0058940_3:3-4-5**      | exactly            | adept              | exactly_adept  | not                | not_exactly_adept   |
    | **pcc_eng_27_064.5496_x1027315_17:4-5-6**     | exactly            | laden              | exactly_laden  | not                | not_exactly_laden   |
    | **pcc_eng_16_084.1766_x1346378_33:25-26-27**  | exactly            | easy               | exactly_easy   | not                | not_exactly_easy    |
    



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
    
    |                         |       `N` |      `f1` |   `adv_total` |
    |:------------------------|----------:|----------:|--------------:|
    | **NEGATED_necessarily** | 6,347,364 | 3,173,660 |        42,886 |
    | **NEGMIR_necessarily**  |   583,470 |   291,732 |           992 |
    
    
    |                                   |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:----------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~necessarily_bad**        | 2,059 |    6.31 |    0.50 |    0.00 | 2,814.04 |  2,062 |  1,030.99 |    1,028.01 |       119,509 |
    | **NEGany~necessarily_indicative** | 1,389 |    6.29 |    0.50 |    0.00 | 1,925.89 |  1,389 |    694.50 |      694.50 |         2,313 |
    | **NEGany~necessarily_true**       | 3,232 |    6.16 |    0.50 |    0.00 | 4,330.74 |  3,245 |  1,622.49 |    1,609.51 |        34,967 |
    | **NEGany~necessarily_better**     | 1,887 |    6.07 |    0.50 |    0.00 | 2,564.81 |  1,891 |    945.49 |      941.51 |        50,827 |
    | **NEGany~necessarily_easy**       |   909 |    5.67 |    0.50 |    0.00 | 1,260.28 |    909 |    454.50 |      454.50 |       108,923 |
    | **NEGany~necessarily_related**    |   741 |    5.14 |    0.50 |    0.00 | 1,013.51 |    742 |    371.00 |      370.00 |        14,260 |
    | **NEGany~necessarily_new**        |   482 |    4.74 |    0.50 |    0.00 |   668.24 |    482 |    241.00 |      241.00 |        21,538 |
    | **NEGany~necessarily_surprising** |   340 |    4.23 |    0.50 |    0.00 |   471.36 |    340 |    170.00 |      170.00 |        18,776 |
    | **NEGany~necessarily_enough**     |   279 |    3.93 |    0.50 |    0.00 |   386.79 |    279 |    139.50 |      139.50 |        27,603 |
    | **NEGany~necessarily_aware**      |   206 |    3.48 |    0.50 |    0.00 |   285.59 |    206 |    103.00 |      103.00 |        28,973 |
    | **NEGmir~necessarily_bad**        |    50 |    1.37 |    0.50 |    0.00 |    69.32 |     50 |     25.00 |       25.00 |         4,790 |
    | **NEGmir~necessarily_wrong**      |   211 |    3.05 |    0.49 |    0.00 |   265.18 |    214 |    107.00 |      104.00 |         8,506 |
    
    
    1. _necessarily indicative_
    
    |                                                 | `token_str`                                                                                                                                                                   |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_064.0785_x1019370_034:12-13-14`** | However , the results of operations for the interim periods are not __`necessarily indicative`__ of the results that may be expected for the year ending December 31 , 2014 . |
    | **`pcc_eng_28_043.8166_x0692740_50:09-10-11`**  | At the same time , a trailer is not __`necessarily indicative`__ of a film .                                                                                                  |
    | **`pcc_eng_10_029.3600_x0458409_07:7-8-9`**     | However , this official rejection is not __`necessarily indicative`__ of poor performance by the gun .                                                                        |
    | **`pcc_eng_09_003.9487_x0047947_41:09-10-11`**  | On the other hand , low turnover is n't __`necessarily indicative`__ of a productive work force .                                                                             |
    | **`pcc_eng_05_035.3109_x0555718_12:4-5-6`**     | Past Performance is Not __`Necessarily Indicative`__ of Future Results .                                                                                                      |
    
    
    2. _necessarily easy_
    
    |                                                 | `token_str`                                                                                                                                                                                                          |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_096.8626_x1549967_085:6-7-8`**    | Your line of work is not __`necessarily easy`__ !                                                                                                                                                                    |
    | **`pcc_eng_08_041.8737_x0661580_40:5-6-7`**     | Quick to make is not __`necessarily easy`__ , and they are great ways to practice skills and learn to read instructions .                                                                                            |
    | **`pcc_eng_03_003.9991_x0048307_51:4-5-6`**     | Though it is not __`necessarily easy`__ to cultivate and maintain this coherence amid today 's consumeristic individualistic hurry - up- and- get-on - with - it norms .                                             |
    | **`pcc_eng_03_007.2549_x0101045_2:12-13-14`**   | But for some people , boosting one 's nest egg is n't __`necessarily easy`__ or intuitive .                                                                                                                          |
    | **`pcc_eng_10_014.1709_x0212830_118:16-17-18`** | The challenge that is presented to you is simple , straightforward and solvable , but not __`necessarily easy`__ so there is still delight in succeeding , and would that all of life 's challenges were like that . |
    
    
    3. _necessarily bad_
    
    |                                                 | `token_str`                                                                                                                                                                 |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_037.0070_x0581700_29:3-4-5`**     | This is not __`necessarily bad`__ because people change and politicians have to change if they want to continue getting support from the people they purport to represent . |
    | **`pcc_eng_21_093.3485_x1492229_26:1-2-3`**     | Not __`necessarily bad`__ , but not necessarily good .                                                                                                                      |
    | **`pcc_eng_01_075.5390_x1205559_34:7-8-9`**     | The acting in the film is not __`necessarily bad`__ .                                                                                                                       |
    | **`pcc_eng_18_011.9650_x0177513_16:16-17-18`**  | I 'm still not sure if I like it or not , but it 's not __`necessarily bad`__ .                                                                                             |
    | **`pcc_eng_13_097.3545_x1556971_163:17-18-19`** | But special interests lobbying on behalf of their members are n't new , and it 's not __`necessarily bad`__ .                                                               |
    
    
    4. _necessarily new_
    
    |                                                | `token_str`                                                                                                      |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_042.5357_x0671944_45:01-11-12`** | Nor is the message itself of Howard University 's photo __`necessarily new`__ .                                  |
    | **`pcc_eng_14_037.6339_x0591831_100:4-5-6`**   | The names are n't __`necessarily new`__ to Astros fans .                                                         |
    | **`pcc_eng_02_093.8994_x1502033_08:7-8-9`**    | While these approaches in themselves are not __`necessarily new`__ , the project is innovative is several ways . |
    | **`apw_eng_20020526_1097_29:5-6-7`**           | today 's terrorism is n't __`necessarily new`__ .                                                                |
    | **`pcc_eng_20_089.0819_x1423015_15:4-5-6`**    | These artists are n't __`necessarily new`__ , but they were new to me in 2019 .                                  |
    
    
    5. _necessarily surprising_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                              |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_014.9162_x0225561_08:10-11-12`**  | Although the move is somewhat unprecedented , it 's not __`necessarily surprising`__ .                                                                                                                                                                                                                   |
    | **`pcc_eng_12_085.1928_x1360400_14:4-5-6`**     | So it 's not __`necessarily surprising`__ then , that Cumberbatch 's comments here - thanks to their vagueness - manage to neither dispel or confirm the possibility of him taking on the iconic role .                                                                                                  |
    | **`pcc_eng_04_102.5832_x1641122_30:3-4-5`**     | It is n't __`necessarily surprising`__ that the swamp is perturbed that President Trump is attempting to boost U.S. - Russia relations .                                                                                                                                                                 |
    | **`pcc_eng_14_081.6689_x1304110_030:20-21-22`** | People , celebrities or not are employing cosmetic contact lens to enhance the look of them so it 's not __`necessarily surprising`__ if you want to buy as well ; but with a variety of models and brands of contact lenses being sold , you have to know how to choose the right lens for you to use . |
    | **`pcc_eng_17_054.0723_x0857552_08:21-22-23`**  | Though support for the death penalty has in general been declining over the years [ 2 ] , it 's not __`necessarily surprising`__ that support would increase in a case such as this one .                                                                                                                |
    
    
    6. _necessarily enough_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                        |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_013.8689_x0208422_12:3-4-5`**    | It is not __`necessarily enough`__ to only point out problems because employers are required to give staff members a chance to respond before a decision is presented about their future in the workplace , says Andrew Douglas , national head of Mac Pherson Kelly 's workplace relations team . |
    | **`pcc_eng_23_036.1425_x0567648_24:5-6-7`**    | Replacing your windows is n't __`necessarily enough`__ .                                                                                                                                                                                                                                           |
    | **`pcc_eng_25_036.0251_x0566997_13:10-11-12`** | However , a great product idea or invention is n't __`necessarily enough`__ to make a great business .                                                                                                                                                                                             |
    | **`pcc_eng_10_027.6536_x0430752_18:15-16-17`** | But college grads such as Razmara are now finding that a postsecondary education is n't __`necessarily enough`__ .                                                                                                                                                                                 |
    | **`pcc_eng_09_004.6589_x0059439_81:2-3-4`**    | is not __`necessarily enough`__ to get things done sometimes .                                                                                                                                                                                                                                     |
    
    
    7. _necessarily aware_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                              |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_030.2900_x0474268_21:20-21-22`** | So , we do n't know why that is happening , but anecdotally we definitely heard that patients are not __`necessarily aware`__ that financial assistance programs might exist .                                                                                                                           |
    | **`nyt_eng_20000607_0109_17:15-16-17`**        | `` They are the No. 1 exchange in the world , and you 're not __`necessarily aware`__ that others want to compete and take your business . ''                                                                                                                                                            |
    | **`pcc_eng_26_005.5853_x0073878_13:15-16-17`** | The pollution which the US shifted to China ( pollution which Chinese citizens are not __`necessarily aware`__ of )                                                                                                                                                                                      |
    | **`pcc_eng_05_032.1521_x0504638_02:25-26-27`** | As therapists , when we talk about Mentalization ( or Mentalizing ) we often realise that the people we 're discussing it with are not __`necessarily aware`__ of what the concept actually means .                                                                                                      |
    | **`pcc_eng_19_076.9527_x1227053_01:27-28-29`** | Democrats seeking the White House can usually count on cash donations from some of the same journalists who cover them -- though the journalists themselves are not __`necessarily aware`__ of this conflict of interest and their participation in it is rarely disclosed by their news organizations . |
    
    
    8. _necessarily related_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_080.8353_x1292227_11:26-27-28`**  | Part of what makes Style Seek so unique is their Style Game : a nine-step quiz that identifies your personal style by presenting pictures , not __`necessarily related`__ to fashion , that you choose from between recognizable items such as 500 Days of Summer and Roman Holiday , a Range Rover and a Maserati .                    |
    | **`pcc_eng_27_052.7587_x0836567_70:18-19-20`**  | This is very initial , but it appears that perhaps the microbiome 's response to illness is not __`necessarily related`__ to the disease we have , but may also be linked to other factors , such as the types of antibiotics people are treated with .                                                                                 |
    | **`pcc_eng_20_007.6073_x0106481_030:19-20-21`** | One of the main challenges that I 've seen for moving true enterprise workloads to the cloud was n't __`necessarily related`__ to the cloud , but to the virtualization overhead that is often used as the underlying infrastructure of many clouds .                                                                                   |
    | **`pcc_eng_11_087.3362_x1397516_068:53-54-55`** | Before buying , though , visit the website of the audience , who do never forget , like implied in it throughout the life styles of music , the following information related to design , we need strong and positive african morals , traditional values in accordance with pchological truth , and not __`necessarily related`__ to . |
    | **`pcc_eng_24_104.2387_x1670381_11:11-12-13`**  | Though the storm has weakened , the storm surge is not __`necessarily related`__ to wind speeds .                                                                                                                                                                                                                                       |
    
    
    9. _necessarily better_
    
    |                                             | `token_str`                                                                                                                                                  |
    |:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_058.9102_x0934778_40:4-5-6`** | Humpty Dumpty is not __`necessarily better`__ off being put back together again .                                                                            |
    | **`pcc_eng_09_006.9224_x0095899_09:4-5-6`** | But easier is n't __`necessarily better`__ .                                                                                                                 |
    | **`pcc_eng_00_065.6682_x1045522_09:6-7-8`** | Most of the changes are n't __`necessarily better`__ -- just different , forced upon me to accommodate a larger display and other forward - looking gizmos . |
    | **`pcc_eng_09_036.7465_x0578652_31:6-7-8`** | " But taking more is n't __`necessarily better`__ , '' she says .                                                                                            |
    | **`pcc_eng_00_033.2360_x0520848_10:5-6-7`** | However , more is n't __`necessarily better`__ .                                                                                                             |
    
    
    10. _necessarily true_
    
    |                                                | `token_str`                                                                                                                                                                                       |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_087.0557_x1393546_28:13-14-15`** | Each student in this class speaks two languages , but it is not __`necessarily true`__ that each student speaks the same two languages .                                                          |
    | **`pcc_eng_04_079.2104_x1263431_01:36-37-38`** | Though the record of the Lipscomb men 's tennis team ( 2 - 9 ) might indicate that they have gotten off to a slow start this season , on an individual basis this is not __`necessarily true`__ . |
    | **`pcc_eng_00_009.1670_x0131896_071:3-4-5`**   | This is not __`necessarily true`__ .                                                                                                                                                              |
    | **`pcc_eng_09_010.3638_x0151919_04:16-17-18`** | Many assume driver 's ed turns out safer drivers , but research shows that 's not __`necessarily true`__ .                                                                                        |
    | **`pcc_eng_15_098.0714_x1568962_37:18-19-20`** | Many people think the ability to make any story interesting is a talent , but it 's not __`necessarily true`__ .                                                                                  |
    
    
    11. _necessarily wrong_
    
    |                                                 | `token_str`                                                                                                                                                                                                            |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_065.9548_x1049855_014:3-4-5`**    | Wants are not __`necessarily wrong`__ , but longings become unhealthy when they consume our thoughts .                                                                                                                 |
    | **`pcc_eng_18_042.2933_x0668098_37:4-5-6`**     | The Eagles are n't __`necessarily wrong`__ here .                                                                                                                                                                      |
    | **`pcc_eng_24_004.4972_x0056398_173:08-09-10`** | Paul recognizes that anger is natural and not __`necessarily wrong`__ ; after all , God gets angry .                                                                                                                   |
    | **`pcc_eng_06_073.5407_x1173387_07:7-8-9`**     | For one thing , there 's nothing __`necessarily wrong`__ with being anti-science , if only because science is neither a ) an all- encompassing explanation of everything , nor b ) an inherently virtuous phenomenon . |
    | **`pcc_eng_12_084.5337_x1349668_376:16-17-18`** | These films wear their relative simplicity like a badge of honor , and that 's not __`necessarily wrong`__ of them .                                                                                                   |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/...
    
    Samples saved as...
    1. `neg_bigram_examples/necessarily/necessarily_indicative_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_easy_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_bad_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_new_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_surprising_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_enough_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_aware_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_related_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_better_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_true_99ex.csv`
    1. `neg_bigram_examples/necessarily/necessarily_wrong_99ex.csv`
    
    ## 2. *that*
    
    |                  |       `N` |      `f1` |   `adv_total` |
    |:-----------------|----------:|----------:|--------------:|
    | **NEGATED_that** | 6,347,364 | 3,173,660 |       166,676 |
    | **NEGMIR_that**  |   583,470 |   291,732 |         4,559 |
    
    
    |                            |    `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:---------------------------|-------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~that_hard**       |  9,948 |    7.68 |    0.50 |    0.00 | 13,602.42 |  9,963 |  4,981.47 |    4,966.53 |        45,061 |
    | **NEGany~that_different**  |  6,534 |    7.18 |    0.50 |    0.00 |  8,895.12 |  6,547 |  3,273.48 |    3,260.52 |        80,643 |
    | **NEGany~that_great**      | 11,032 |    7.18 |    0.50 |    0.00 | 14,908.90 | 11,065 |  5,532.46 |    5,499.54 |        45,359 |
    | **NEGany~that_difficult**  |  5,560 |    7.06 |    0.50 |    0.00 |  7,569.00 |  5,571 |  2,785.48 |    2,774.52 |        61,490 |
    | **NEGany~that_big**        |  6,244 |    6.47 |    0.50 |    0.00 |  8,332.69 |  6,273 |  3,136.48 |    3,107.52 |        42,912 |
    | **NEGany~that_surprising** |  1,133 |    5.99 |    0.50 |    0.00 |  1,570.89 |  1,133 |    566.50 |      566.50 |        18,776 |
    | **NEGany~that_unusual**    |    977 |    5.77 |    0.50 |    0.00 |  1,354.57 |    977 |    488.50 |      488.50 |         7,412 |
    | **NEGany~that_exciting**   |    805 |    5.49 |    0.50 |    0.00 |  1,116.08 |    805 |    402.50 |      402.50 |        20,233 |
    | **NEGany~that_uncommon**   |    802 |    5.49 |    0.50 |    0.00 |  1,111.92 |    802 |    401.00 |      401.00 |         3,165 |
    | **NEGany~that_impressed**  |    681 |    5.25 |    0.50 |    0.00 |    944.15 |    681 |    340.50 |      340.50 |        12,138 |
    | **NEGmir~that_close**      |     60 |    1.67 |    0.50 |    0.00 |     83.19 |     60 |     30.00 |       30.00 |         4,831 |
    | **NEGmir~that_happy**      |     41 |    1.03 |    0.50 |    0.00 |     56.84 |     41 |     20.50 |       20.50 |         5,463 |
    | **NEGmir~that_simple**     |    474 |    3.67 |    0.48 |    0.00 |    580.44 |    483 |    241.50 |      232.50 |         7,465 |
    | **NEGmir~that_popular**    |     65 |    1.54 |    0.48 |    0.00 |     81.14 |     66 |     33.00 |       32.00 |         2,841 |
    | **NEGmir~that_difficult**  |     52 |    1.16 |    0.48 |    0.00 |     63.56 |     53 |     26.50 |       25.50 |         4,854 |
    | **NEGmir~that_easy**       |    450 |    3.23 |    0.47 |    0.00 |    512.43 |    465 |    232.50 |      217.50 |         7,749 |
    | **NEGmir~that_big**        |    113 |    2.08 |    0.47 |    0.00 |    132.98 |    116 |     58.00 |       55.00 |         3,134 |
    | **NEGmir~that_interested** |     62 |    1.26 |    0.47 |    0.00 |     70.93 |     64 |     32.00 |       30.00 |         2,877 |
    | **NEGmir~that_great**      |    286 |    2.71 |    0.46 |    0.00 |    312.65 |    298 |    149.00 |      137.00 |         2,123 |
    | **NEGmir~that_good**       |    447 |    2.65 |    0.44 |    0.00 |    441.70 |    476 |    238.00 |      209.00 |        13,423 |
    
    
    1. _that surprising_
    
    |                                                | `token_str`                                                                                                                                                                                                       |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_084.9470_x1356690_10:18-19-20`** | While it may seem odd that all three of these celebrities are relatively young , it is not __`that surprising`__ .                                                                                                |
    | **`pcc_eng_20_089.0219_x1422017_49:20-21-22`** | The simple fact is that little is done even when the USDA is on the case , which is not __`that surprising`__ for an agency with a well - greased revolving door between itself and the businesses it regulates . |
    | **`pcc_eng_10_079.1004_x1262366_31:11-12-13`** | Of course , this was from 1955 so that is not __`that surprising`__ .                                                                                                                                             |
    | **`pcc_eng_26_036.3799_x0571842_11:24-27-28`** | This also enables Stormzy to pull off the album 's most unexpected facet - though given the title , perhaps overt religiosity should n't have been __`that surprising`__ .                                        |
    | **`nyt_eng_20001006_0145_29:4-5-6`**           | the alliances are n't __`that surprising`__ .                                                                                                                                                                     |
    
    
    2. _that unusual_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20000324_0221_21:4-5-6`**           | `` It 's not __`that unusual`__ for judges to have second thoughts , '' said Spurlock , a former trial and appellate judge .                                                                                                                                         |
    | **`pcc_eng_test_2.06136_x25978_097:11-12-13`** | But Spacey 's subsequent issues since Rapp spoke out are not __`that unusual`__ for someone at his second Saturn return and fifth Jupiter return .                                                                                                                   |
    | **`pcc_eng_22_006.4671_x0088233_06:48-49-50`** | Back then New Zealand had no experience of floodlit rugby and , in any case , how could you expect the punters in Christchurch and Dunedin , in particular , to turn out on a cold winter 's night when a gale blowing off the Antarctic is not __`that unusual`__ . |
    | **`pcc_eng_25_045.9292_x0727337_067:5-6-7`**   | Dog vomiting just is n't __`that unusual`__ in our house .                                                                                                                                                                                                           |
    | **`pcc_eng_02_091.3263_x1460441_075:5-6-7`**   | Edberg 's story is n't __`that unusual`__ in the startup world .                                                                                                                                                                                                     |
    
    
    3. _that exciting_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                         |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_007.8685_x0111062_29:08-10-11`** | OK , no , my twist is not nearly __`that exciting`__ .                                                                                                                                                                                                                              |
    | **`nyt_eng_19981117_0145_26:16-17-18`**        | let 's face it , turkey by itself , moist or dry , is just not __`that exciting`__ .                                                                                                                                                                                                |
    | **`pcc_eng_10_020.5840_x0316538_08:08-09-10`** | I think that the match overall was n't __`that exciting`__ .                                                                                                                                                                                                                        |
    | **`nyt_eng_20070609_0105_23:31-32-33`**        | `` I think maybe there 's a little smirk on the coach 's face , '' Barry said , `` and on the organization 's face , that it 's not __`that exciting`__ to people outside of San Antonio , that we 're doing it quietly , something special , right here , and we get to enjoy it . |
    | **`pcc_eng_11_066.2590_x1056231_78:12-14-15`** | The problem here is that the " exciting incentives " are n't really __`that exciting`__ .                                                                                                                                                                                           |
    
    
    4. _that uncommon_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                 |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_005.4805_x0072964_39:3-4-5`**     | This is n't __`that uncommon`__ but the thing that makes this a little inconvenient with this vape is that you have to turn it upside down and take out the wand to do this .                                                                                                               |
    | **`pcc_eng_18_008.9083_x0127940_11:19-20-21`**  | Early morning FBI arrests for those who threaten national security based on wiretaps and email interceptions are now not __`that uncommon`__ , but you can walk the streets confident that you are not on camera the whole time , and the innocent seem to have relatively little to fear . |
    | **`pcc_eng_val_2.04827_x24095_61:17-18-19`**    | I find , oftentimes , in an actor who 's played the villain , it 's not __`that uncommon`__ that when I meet them , they 're the most lovely person .                                                                                                                                       |
    | **`pcc_eng_23_039.0433_x0614585_040:16-17-18`** | " The man is obviously suffering from schizophrenia , and the type of schizophrenia is n't __`that uncommon`__ .                                                                                                                                                                            |
    | **`pcc_eng_26_092.1059_x1473341_136:11-12-13`** | And that 's , you know -- Those thing are not __`that uncommon`__ , unfortunately .                                                                                                                                                                                                         |
    
    
    5. _that impressed_
    
    |                                                | `token_str`                                                                                                                    |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_050.8504_x0805375_25:11-12-13`** | I had one a long time ago , and was not __`that impressed`__ .                                                                 |
    | **`pcc_eng_02_030.7743_x0481888_16:5-6-7`**    | Honestly , I was n't __`that impressed`__ when I checked out the App Store description , or when I first opened the app .      |
    | **`pcc_eng_07_022.6240_x0349705_10:7-8-9`**    | After my first viewing I was n't __`that impressed`__ .                                                                        |
    | **`pcc_eng_01_048.6587_x0770122_21:14-15-16`** | And the new guy at my chiropractor is fine , but I was n't __`that impressed`__ .                                              |
    | **`pcc_eng_15_011.8246_x0174747_11:21-22-23`** | J-lo went down for a couple of days with flu , Nato had a go at mothering but J was n't __`that impressed`__ with his effort . |
    
    
    6. _that close_
    
    |                                                 | `token_str`                                                                                                                                                                                                   |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19990730_0092_35:18-20-21`**         | -lrb- The fire was -RRB- maybe 20 feet in diameter and twice as high , I had never been __`that close`__ to a fire so large .                                                                                 |
    | **`pcc_eng_23_046.1691_x0729831_06:3-4-5`**     | I was n't __`that close`__ to her , and had n't kept up at all in recent years .                                                                                                                              |
    | **`pcc_eng_19_078.0095_x1244134_099:21-22-23`** | " This is normal and no reason for alarm , " Mussen said , " except that people usually are not __`that close`__ to bee colonies to notice the normal demise of substantial numbers of overwintering bees . " |
    | **`pcc_eng_20_034.3317_x0538925_10:10-11-12`**  | Apparently Wolfensohn 's brother and sister- in- law were n't __`that close`__ anyway so they were n't the last bit concerned when they had n't heard from Wolfensohn 's side of the family for years .       |
    | **`nyt_eng_19961118_0032_16:13-15-16`**         | Denver beat the Patriots , 34-8 , in a game that was n't nearly __`that close`__ .                                                                                                                            |
    
    
    7. _that happy_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                           |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_092.7711_x1483281_13:4-5-6`**    | But people are not __`that happy`__ with Raju 's son .                                                                                                                                                                                                                                |
    | **`pcc_eng_15_048.1903_x0762915_33:20-21-22`** | So Dee , the main character in my novel , is happy until she realizes that she 's actually not __`that happy`__ .                                                                                                                                                                     |
    | **`pcc_eng_06_103.1365_x1652404_24:3-4-5`**    | I am not __`that happy`__ .                                                                                                                                                                                                                                                           |
    | **`pcc_eng_19_044.0470_x0694967_034:1-8-9`**   | None of those students should have been __`that happy`__ that they finally felt like they belonged -- they should have had that experience much sooner .                                                                                                                              |
    | **`pcc_eng_25_008.2908_x0118205_05:46-48-49`** | We 're going to assume the best and guess the copywriter was just going for a turn of phrase , and did n't realize the expression " the South will rise again , " has its roots as a rallying cry for folks who were n't all __`that happy`__ with the way the Civil War turned out . |
    
    
    8. _that hard_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_071.9839_x1149311_38:3-4-5`**    | That is not __`that hard`__ to do , in theory even a smartphone could be adapted to read such chips , but that would lead to data security problems .                                                                                                                                                                                                                                      |
    | **`nyt_eng_20061206_0069_27:09-10-11`**        | FOOD-CANDY-RECIPES -- ATLANTA -- Candy for gift-giving is n't __`that hard`__ to make , especially when you have a foolproof recipe and a reliable candy thermometer .                                                                                                                                                                                                                     |
    | **`pcc_eng_11_015.4369_x0233655_59:3-4-5`**    | It 's not __`that hard`__ , especially if they admit what the stats above are telling them .                                                                                                                                                                                                                                                                                               |
    | **`pcc_eng_19_012.9663_x0193374_04:11-13-14`** | Everyone wants a brighter smile these days and it should n't be __`that hard`__ to get one .                                                                                                                                                                                                                                                                                               |
    | **`pcc_eng_26_096.9348_x1551176_04:51-52-53`** | " I joined the robotics team my 11th grade year and I had no idea what they wanted me to do or how they expected me to be able to do any they ask but after a short bit of time I seen that creating gear motors and such was n't __`that hard`__ and also having great teammates makes everything easier over time and that everything we create will take lot of dedication and energy . |
    
    
    9. _that different_
    
    |                                                | `token_str`                                                                                                                                                                                                   |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_046.4146_x0733648_21:3-5-6`**    | This may not be __`that different`__ ( particularly if we get involved and start leading again ) .                                                                                                            |
    | **`pcc_eng_19_040.3714_x0635291_28:32-34-35`** | Okay , so one might say that it also had a story , but it still relied heavily on those effects to " sell " the plot , and that 's not really __`that different`__ from later films , even those made today . |
    | **`pcc_eng_28_048.8319_x0773924_096:7-8-9`**   | But they 're cranial capacity is n't __`that different`__ than chimpanzees .                                                                                                                                  |
    | **`pcc_eng_00_066.2149_x1054185_26:6-7-8`**    | Marketing and human resources are n't __`that different`__ like they sound .                                                                                                                                  |
    | **`pcc_eng_10_027.5506_x0429046_04:6-7-8`**    | " Unfortunately , they are n't __`that different`__ . "                                                                                                                                                       |
    
    
    10. _that difficult_
    
    |                                                | `token_str`                                                                                                                           |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_094.8418_x1518309_25:5-7-8`**    | What if it is n't actually __`that difficult`__ with a little concentrated focus ?                                                    |
    | **`pcc_eng_26_007.8701_x0110779_05:11-12-13`** | Removing a stuck labret stud can hurt , but is not __`that difficult`__ and is completely necessary .                                 |
    | **`pcc_eng_28_073.8736_x1178661_13:11-12-13`** | We recommend giving soldering a go tho as its really not __`that difficult`__ .                                                       |
    | **`pcc_eng_08_078.8242_x1260196_08:4-5-6`**    | It actually is n't __`that difficult`__ if you consider the following options to always eating out and paying for everything you do . |
    | **`pcc_eng_06_072.7679_x1160950_095:3-4-5`**   | It is not __`that difficult`__ ; with a few things on the list that will make your life easier and easier on your pets as well .      |
    
    
    11. _that great_
    
    |                                                 | `token_str`                                                                                       |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_002.4809_x0024188_26:14-15-16`**  | All in , this was n't really anything bad , but it was n't __`that great`__ either .              |
    | **`pcc_eng_17_070.7736_x1127374_191:08-09-10`** | LOUIS- DREYFUS : Yeah , it was n't __`that great`__ .                                             |
    | **`pcc_eng_20_035.2194_x0553168_35:09-10-11`**  | But the magnitude of the money involved was not __`that great`__ .                                |
    | **`pcc_eng_21_074.5686_x1188896_11:13-14-15`**  | I added some horns but I gotta say , the samples are n't __`that great`__ .                       |
    | **`pcc_eng_17_055.9210_x0887262_52:16-17-18`**  | Let 's face it : the free headphones Apple supplies with every i Phone are not __`that great`__ . |
    
    
    12. _that big_
    
    |                                                | `token_str`                                                                                                                                                                                           |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_038.5783_x0608393_11:14-15-16`** | Since we planned on replacing the antiquated A/C unit anyway , it was n't __`that big`__ of a deal .                                                                                                  |
    | **`pcc_eng_14_012.8777_x0191788_005:3-4-5`**   | It ai n't __`that big`__ .                                                                                                                                                                            |
    | **`pcc_eng_22_067.9472_x1081909_391:4-6-7`**   | Our place is n't quite __`that big`__ anyways to accommodate more than 100 people . "                                                                                                                 |
    | **`pcc_eng_12_082.7107_x1320138_31:14-15-16`** | Tripp acknowledged that " the upfront cost " of doing so is " not __`that big`__ , " but he suggested that such a practice might also create a " litigation risk " from vendors who were not chosen . |
    | **`pcc_eng_25_097.9766_x1569423_20:10-11-12`** | I 'm going there anyway , so it is n't __`that big`__ of a deal .                                                                                                                                     |
    
    
    13. _that popular_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_101.8313_x1628963_40:15-16-17`**  | Back in a day patching a game was n't an option and DLCs was n't __`that popular`__ so the game had to be released as intended .                                                                                                           |
    | **`pcc_eng_00_038.8014_x0610600_08:19-20-21`**  | I hired a lvl 70 to run me through the instance at lvl 45 , because it 's not __`that popular`__ an instance , at least on my server .                                                                                                     |
    | **`pcc_eng_17_044.3230_x0699644_217:19-20-21`** | But it is not safe to consider the delay before going monthly as a sign that it was not __`that popular`__ .                                                                                                                               |
    | **`pcc_eng_10_050.0200_x0792709_12:10-11-12`**  | I lived in Japan one year and tampons are not __`that popular`__ .                                                                                                                                                                         |
    | **`pcc_eng_28_019.3509_x0296738_58:07-09-10`**  | But 1 ) Mc Cain is n't all __`that popular`__ among AZ GOPers : he only got 51 % in the ' 08 primary at a time he really needed the boost ; and 2 ) he 's running a campaign almost designed to anger anyone who fell for his 2000 shtik . |
    
    
    14. _that simple_
    
    |                                                 | `token_str`                                                                                                                                                                                                            |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_077.6266_x1237909_17:4-5-6`**     | Apparently things are n't __`that simple`__ ...                                                                                                                                                                        |
    | **`nyt_eng_19990818_0135_11:15-16-17`**         | he knew where he and his priorities needed to be , but it was n't __`that simple`__ .                                                                                                                                  |
    | **`nyt_eng_19961118_0669_42:25-26-27`**         | but Ritter , who is now executive director of the Transition Commission for the Transfer of the Panama Canal , said the issue is not __`that simple`__ .                                                               |
    | **`pcc_eng_03_009.0298_x0129877_11:4-6-7`**     | But it may not be __`that simple`__ .                                                                                                                                                                                  |
    | **`pcc_eng_16_082.2586_x1315169_008:09-10-11`** | But putting that straightforward plan into practice is n't __`that simple`__ , since every special-needs child requires an individualized program that addresses his or her specific disabilities and learning style . |
    
    
    15. _that interested_
    
    |                                                | `token_str`                                                                                                                                 |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20090509_0609_7:14-16-17`**         | because people know what is the situation at the moment , people are not really __`that interested`__ anymore . ''                          |
    | **`pcc_eng_02_032.6080_x0511608_03:4-5-6`**    | Previously they were n't __`that interested`__ in clothes or what they wore , but now they feel inspired to explore their style sense .     |
    | **`pcc_eng_15_095.8004_x1532287_07:3-4-5`**    | Zane is not __`that interested`__ in the Gollywhopper Games .                                                                               |
    | **`pcc_eng_00_004.6991_x0059756_29:18-20-21`** | If I do n't like how it is made , its design and all then I will not be __`that interested`__ in seeing what other things it has to offer . |
    | **`nyt_eng_20000612_1042_16:09-11-12`**        | on top of that , females who are n't even __`that interested`__ in the film expect to ride out the opening tempest .                        |
    
    
    16. _that easy_
    
    |                                             | `token_str`                                                                                                  |
    |:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19980923_0328_7:13-14-15`**      | the simple and difficult answer is that things in Russia just are n't __`that easy`__ .                      |
    | **`pcc_eng_05_083.0409_x1327717_04:4-5-6`** | The sound is not __`that easy`__ to set up .                                                                 |
    | **`pcc_eng_05_084.6573_x1353862_50:4-5-6`** | However guns were not __`that easy`__ to use they required lots of training and took a long time to reload . |
    | **`pcc_eng_17_103.8908_x1663244_12:5-6-7`** | Right now it 's not __`that easy`__ to find demos through the game store .                                   |
    | **`pcc_eng_04_075.3966_x1201616_38:3-5-6`** | They are n't all __`that easy`__ to find by feel since they are flush with the surface .                     |
    
    
    17. _that good_
    
    |                                                 | `token_str`                                                                                                                                                         |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_017.5880_x0268455_2:4-5-6`**      | He 's just not __`that good`__ , and has a poor track record .                                                                                                      |
    | **`pcc_eng_18_004.8793_x0062902_114:31-33-34`** | Actually , I know I 'm getting more and more speed because I went a second a lap faster today than I 've ever ridden , and the track was n't even __`that good`__ . |
    | **`pcc_eng_17_077.6580_x1238762_11:13-14-15`**  | sorry for the bad shots I was drinking and the camera was not that good                                                                                             |
    | **`pcc_eng_21_066.1409_x1052539_31:24-25-26`**  | Your aim should be the conflict sweet spot : " Avoiding conflict is n't good ; debating each other all the time is not __`that good`__ either .                     |
    | **`pcc_eng_28_072.0548_x1149420_62:13-15-16`**  | So it 's good when it 's good , but it 's not always __`that good`__ .                                                                                              |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/...
    
    Samples saved as...
    1. `neg_bigram_examples/that/that_surprising_99ex.csv`
    1. `neg_bigram_examples/that/that_unusual_99ex.csv`
    1. `neg_bigram_examples/that/that_exciting_99ex.csv`
    1. `neg_bigram_examples/that/that_uncommon_99ex.csv`
    1. `neg_bigram_examples/that/that_impressed_99ex.csv`
    1. `neg_bigram_examples/that/that_close_99ex.csv`
    1. `neg_bigram_examples/that/that_happy_99ex.csv`
    1. `neg_bigram_examples/that/that_hard_99ex.csv`
    1. `neg_bigram_examples/that/that_different_99ex.csv`
    1. `neg_bigram_examples/that/that_difficult_99ex.csv`
    1. `neg_bigram_examples/that/that_great_99ex.csv`
    1. `neg_bigram_examples/that/that_big_99ex.csv`
    1. `neg_bigram_examples/that/that_popular_99ex.csv`
    1. `neg_bigram_examples/that/that_simple_99ex.csv`
    1. `neg_bigram_examples/that/that_interested_99ex.csv`
    1. `neg_bigram_examples/that/that_easy_99ex.csv`
    1. `neg_bigram_examples/that/that_good_99ex.csv`
    
    ## 3. *exactly*
    
    |                     |       `N` |      `f1` |   `adv_total` |
    |:--------------------|----------:|----------:|--------------:|
    | **NEGMIR_exactly**  |   583,470 |   291,732 |           869 |
    | **NEGATED_exactly** | 6,347,364 | 3,173,660 |        44,503 |
    
    
    |                               |   `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:------------------------------|------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~exactly_sure**       | 8,794 |    7.46 |    0.50 |    0.00 | 11,991.61 |  8,810 |  4,404.97 |    4,389.03 |       134,139 |
    | **NEGany~exactly_clear**      | 1,746 |    6.38 |    0.50 |    0.00 |  2,405.43 |  1,747 |    873.49 |      872.51 |        84,227 |
    | **NEGany~exactly_new**        | 1,371 |    6.03 |    0.50 |    0.00 |  1,885.86 |  1,372 |    686.00 |      685.00 |        21,538 |
    | **NEGany~exactly_easy**       | 1,066 |    5.67 |    0.50 |    0.00 |  1,463.43 |  1,067 |    533.50 |      532.50 |       108,923 |
    | **NEGany~exactly_cheap**      |   691 |    5.27 |    0.50 |    0.00 |    958.01 |    691 |    345.50 |      345.50 |         6,591 |
    | **NEGany~exactly_surprising** |   440 |    4.61 |    0.50 |    0.00 |    610.01 |    440 |    220.00 |      220.00 |        18,776 |
    | **NEGany~exactly_subtle**     |   263 |    3.84 |    0.50 |    0.00 |    364.61 |    263 |    131.50 |      131.50 |         5,299 |
    | **NEGany~exactly_fair**       |   260 |    3.83 |    0.50 |    0.00 |    360.45 |    260 |    130.00 |      130.00 |         6,964 |
    | **NEGany~exactly_fun**        |   224 |    3.60 |    0.50 |    0.00 |    310.54 |    224 |    112.00 |      112.00 |        19,661 |
    | **NEGany~exactly_hard**       |   203 |    3.46 |    0.50 |    0.00 |    281.43 |    203 |    101.50 |      101.50 |        45,061 |
    | **NEGmir~exactly_sure**       |   148 |    3.10 |    0.50 |    0.00 |    205.21 |    148 |     74.00 |       74.00 |         5,978 |
    | **NEGmir~exactly_clear**      |    52 |    1.16 |    0.48 |    0.00 |     63.56 |     53 |     26.50 |       25.50 |         3,321 |
    
    
    1. _exactly sure_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_13_083.2034_x1328769_39:3-4-5`**     | I 'm not __`exactly sure`__ who this movie is aimed at since kids will find it too scary and adults will just be bored to tears or too busy laughing their asses off .                                                                     |
    | **`pcc_eng_14_004.8169_x0061865_22:3-4-5`**     | I 'm not __`exactly sure`__ what the measures are that get people actively involved , but they need to have the information so they can make an informed decision as to what they are going to support or not .                            |
    | **`pcc_eng_12_035.5505_x0558870_024:25-26-27`** | When asked how it feels to be a part of such a noteworthy tradition at Penn , Cheeseman explains that , while he 's not __`exactly sure`__ how he feels , he does acknowledge that it 's rather " neat " to be a part of Penn 's history . |
    | **`nyt_eng_19980715_0211_20:08-09-10`**         | this seems appropriate , though I 'm not __`exactly sure`__ how . -RRB-                                                                                                                                                                    |
    | **`pcc_eng_11_061.8000_x0983952_08:1-2-3`**     | Not __`exactly sure`__ you need to pay someone for advice like that , but somehow Hitch makes his counsel seem useful , endearing and necessary .                                                                                          |
    
    
    2. _exactly cheap_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_036.1497_x0568962_04:3-4-5`**     | This is n't __`exactly cheap`__ given that the drug has been in use for 62 years and is on the WHO 's List of Essential Medicines , which is considered to be the bare minimum pharmaceutical foundation of a bare minimum health - care system .                                                                                                                                                                                                                                                                                 |
    | **`pcc_eng_02_014.1025_x0211946_080:13-14-15`** | Today simple myoelectrics are much more affordable , but they are still not __`exactly cheap`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                 |
    | **`pcc_eng_02_081.9943_x1309524_34:14-15-16`**  | 600,000 copies is an excellent achievement , particularly given that the game is not __`exactly cheap`__ ( it is n't expensive , but it is rather more expensive than things like Terraria ) .                                                                                                                                                                                                                                                                                                                                    |
    | **`pcc_eng_24_101.4229_x1624707_03:21-22-23`**  | " The employer community has benefitted , but at a price for the cost of the review , which is not __`exactly cheap`__ if it is just over a dispute over the declination ... of a prescription , " said Zachary Sacks , managing partner at Culver City , California , law firm Sacks & Zolonz Under California workers comp reforms passed in 2012 , injured workers can request independent medical reviews to dispute treatment that was modified or denied under utilization reviews , which employers and insurers request . |
    | **`pcc_eng_06_070.4883_x1124395_034:4-5-6`**    | New Orleans is n't __`exactly cheap`__ for events , and just try to find us a vegan or even a vegetarian caterer .                                                                                                                                                                                                                                                                                                                                                                                                                |
    
    
    3. _exactly surprising_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                              |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_028.7930_x0449616_10:27-28-29`** | That a team executive in the league with the most embattled officiating corps would promote a tool that would create greater transparency on the court is n't __`exactly surprising`__ ; you can also expect that league 's resistance to such a tool .                                                  |
    | **`pcc_eng_28_045.7611_x0724394_18:12-13-14`** | Given how clearly horned - up young Conrad is it 's not __`exactly surprising`__ that he makes a beeline for Rush 's crotch ; pulling away the buff beauty 's briefs , then promptly slurping on the handsome fuck - rod that he discovers straining inside .                                            |
    | **`pcc_eng_24_081.8035_x1306938_21:3-4-5`**    | It 's not __`exactly surprising`__ that good data-driven resources are hard to find .                                                                                                                                                                                                                    |
    | **`pcc_eng_07_024.6618_x0382669_36:41-42-43`** | While most of the sellers at the market would n't start such a confrontation , it 's unfortunate that a small minority of vendors chose to take this initiative ; if one has no empathy towards animals , it 's not __`exactly surprising`__ that some express their frustrations in undesireable ways . |
    | **`pcc_eng_19_075.0942_x1197003_20:11-12-13`** | Of course , you 're probably thinking that it 's not __`exactly surprising`__ that the party that , at the time , most suffered under First Past the Post would be the first to call for its passing into history .                                                                                      |
    
    
    4. _exactly subtle_
    
    |                                                | `token_str`                                                                                                                                                                                     |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_050.6849_x0802655_24:7-8-9`**    | It 's surely effective , but not __`exactly subtle`__ .                                                                                                                                         |
    | **`pcc_eng_03_083.8367_x1341468_08:11-12-13`** | That whipsawing effect , between revulsion and tenderness , was n't __`exactly subtle`__ .                                                                                                      |
    | **`pcc_eng_12_034.4892_x0541837_12:7-8-9`**    | If you know Spanish it 's not __`exactly subtle`__ that the AMIGOS organization is exactly translated to " friends of the Americas " or " friends international . "                             |
    | **`pcc_eng_02_002.2391_x0020034_09:25-26-27`** | This film takes all the usual 80s tropes that are doing the rounds of late ( yes , that Stranger Things reference above was n't __`exactly subtle`__ was it ? ) but somehow gets away with it . |
    | **`pcc_eng_22_055.1459_x0874987_098:1-2-3`**   | Not __`exactly subtle`__ , but I got one of his eyes back in time for him to catch me smile , and return the ceremonial gesture to the Bug as best I could .                                    |
    
    
    5. _exactly fair_
    
    |                                             | `token_str`                                                                                                                                                                           |
    |:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_084.7432_x1355354_02:3-4-5`** | It 's not __`exactly fair`__ to judge it as an EP because A. ) it 's only three songs and B. ) these three songs are sequenced terribly and do n't really fit together in the least . |
    | **`pcc_eng_03_038.5826_x0608771_27:5-6-7`** | And while it 's not __`exactly fair`__ to say " no one cared " , the were n't compelled to care for any reason other than they were told to and had heard Bret Hart 's name before .  |
    | **`pcc_eng_00_011.0232_x0161684_01:5-6-7`** | Well , that 's not __`exactly fair`__ .                                                                                                                                               |
    | **`pcc_eng_02_092.3330_x1476634_34:6-7-8`** | And sometimes , it is n't __`exactly fair`__ .                                                                                                                                        |
    | **`pcc_eng_25_035.5367_x0559042_12:3-4-5`** | It 's not __`exactly fair`__ to Flannery O'Connor either .                                                                                                                            |
    
    
    6. _exactly fun_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_078.7971_x1256842_11:13-14-15`** | So many moms have been there and of course , it 's not __`exactly fun`__ to hear that someone thinks we 're pregnant despite having already given birth .                                                                                                                                                                 |
    | **`pcc_eng_04_005.5144_x0073212_40:08-09-10`** | It does everything , but it 's not __`exactly fun`__ to drive . "                                                                                                                                                                                                                                                         |
    | **`pcc_eng_16_028.9639_x0452742_38:23-24-25`** | majority of people who play wow has never had to make difficult choices quickly , never had to do things that were not __`exactly fun`__ , just because they needed to .                                                                                                                                                  |
    | **`pcc_eng_19_026.1543_x0406196_015:3-4-5`**   | It 's not __`exactly fun`__ .                                                                                                                                                                                                                                                                                             |
    | **`pcc_eng_00_009.8216_x0142381_08:19-20-21`** | It 's scary to think about the impact rising STD rates could have , and although it 's not __`exactly fun`__ , casual conversation fodder , it 's imperative that we talk about issues pertaining to sexual health -- especially when the alternative is remaining uninformed and potentially putting ourselves at risk . |
    
    
    7. _exactly hard_
    
    |                                                | `token_str`                                                                                                                                       |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_098.2815_x1572765_4:09-10-11`**  | Double-clicking apps and docs to open them is n't __`exactly hard`__ .                                                                            |
    | **`pcc_eng_09_011.7996_x0175029_04:3-4-5`**    | Zeppelin are n't __`exactly hard`__ to figure out .                                                                                               |
    | **`pcc_eng_25_012.2905_x0182527_5:6-7-8`**     | Plus , the campaign is n't __`exactly hard`__ on the eyes !                                                                                       |
    | **`pcc_eng_08_070.7463_x1129318_04:24-25-26`** | Perhaps Go ! was pricing seats below Aloha 's costs , and with a fleet of ancient , inefficient aircraft , that 's not __`exactly hard`__ to do . |
    | **`pcc_eng_05_084.2433_x1347184_45:6-7-8`**    | Even though the game 's not __`exactly hard`__ and the AI makes some dumb moves sometimes , those dumb moves are deliberate .                     |
    
    
    8. _exactly clear_
    
    |                                                 | `token_str`                                                                                                                                                                                                                    |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_082.2949_x1315265_15:16-17-18`**  | But because of the tiered nature of both licensing and tax rates , it 's not __`exactly clear`__ who is going to apply for which licenses , and how the market will shake out .                                                |
    | **`pcc_eng_17_059.6888_x0948000_11:6-7-8`**     | For what , I 'm not __`exactly clear`__ .                                                                                                                                                                                      |
    | **`pcc_eng_04_104.4998_x1671984_12:6-7-8`**     | And in case it was n't __`exactly clear`__ what the billionaire loved about the movie , there 's this tasty anecdote about a strike below the belt :                                                                           |
    | **`pcc_eng_12_039.1287_x0616768_12:29-31-32`**  | The problem being sometimes you have multiple pieces of evidence that would be considered incriminating but the game only accepts one specific piece ; of which it is n't always __`exactly clear`__ as to which one that is . |
    | **`pcc_eng_00_033.8625_x0531059_032:22-23-24`** | In the words of the old Buffalo Springfield song , " There 's something happening here , what is , ai n't __`exactly clear`__ . "                                                                                              |
    
    
    9. _exactly new_
    
    |                                                 | `token_str`                                                                               |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_056.3043_x0894444_07:11-12-13`**  | Sen. Jeff Steinborn is a Las Cruces Democrat who is n't __`exactly new`__ .               |
    | **`pcc_eng_05_012.7234_x0190065_14:6-7-8`**     | Then again the slate is not __`exactly new`__ as a work tool .                            |
    | **`pcc_eng_08_102.5785_x1644695_03:08-09-10`**  | It 's actually very easy and while not __`exactly new`__ , its use is only catching on .  |
    | **`pcc_eng_22_065.7124_x1045933_282:11-12-13`** | Some people thought I was crazy , but that was n't __`exactly new`__ , I was used to it . |
    | **`apw_eng_19980527_0746_19:09-10-11`**         | the service _ 1 +1 Communications _ is not __`exactly new`__ , however .                  |
    
    
    10. _exactly easy_
    
    |                                                | `token_str`                                                                                                                 |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_007.1339_x0099050_17:4-5-6`**    | Her plan was n't __`exactly easy`__ .                                                                                       |
    | **`pcc_eng_21_098.4074_x1573697_11:16-17-18`** | One drawback of being an amateur- built site is that the Dirty Tony tour is not __`exactly easy`__ to navigate .            |
    | **`pcc_eng_29_004.9107_x0063306_30:6-7-8`**    | Unfortunately , finding parking is n't __`exactly easy`__ and my friend is starting to lose his patience .                  |
    | **`pcc_eng_09_097.2061_x1556629_12:12-13-14`** | As you 'll see in the video below , it 's not __`exactly easy`__ to fly this thing .                                        |
    | **`pcc_eng_06_021.0750_x0324796_08:19-20-21`** | And those who try to spot them in advance on the company 's website discover that they 're not __`exactly easy`__ to find . |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/...
    
    Samples saved as...
    1. `neg_bigram_examples/exactly/exactly_sure_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_cheap_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_surprising_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_subtle_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_fair_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_fun_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_hard_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_clear_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_new_99ex.csv`
    1. `neg_bigram_examples/exactly/exactly_easy_99ex.csv`
    
    ## 4. *any*
    
    |                 |       `N` |      `f1` |   `adv_total` |
    |:----------------|----------:|----------:|--------------:|
    | **NEGMIR_any**  |   583,470 |   291,732 |         1,095 |
    | **NEGATED_any** | 6,347,364 | 3,173,660 |        16,238 |
    
    
    |                          |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:-------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~any_younger**   |   255 |    3.80 |    0.50 |    0.00 |   353.52 |    255 |    127.50 |      127.50 |         1,784 |
    | **NEGany~any_nicer**     |    96 |    2.30 |    0.50 |    0.00 |   133.09 |     96 |     48.00 |       48.00 |           642 |
    | **NEGany~any_sweeter**   |    58 |    1.49 |    0.50 |    0.00 |    80.41 |     58 |     29.00 |       29.00 |           388 |
    | **NEGmir~any_different** |    48 |    1.30 |    0.50 |    0.00 |    66.55 |     48 |     24.00 |       24.00 |         8,644 |
    | **NEGany~any_happier**   |   828 |    4.66 |    0.49 |    0.00 | 1,085.12 |    834 |    417.00 |      411.00 |         2,004 |
    | **NEGany~any_smarter**   |    89 |    1.94 |    0.49 |    0.00 |   113.78 |     90 |     45.00 |       44.00 |           733 |
    | **NEGany~any_easier**    | 1,594 |    4.42 |    0.48 |    0.00 | 1,946.26 |  1,625 |    812.49 |      781.51 |        12,877 |
    | **NEGany~any_brighter**  |    63 |    1.37 |    0.48 |    0.00 |    78.42 |     64 |     32.00 |       31.00 |           640 |
    | **NEGmir~any_better**    |   380 |    3.27 |    0.47 |    0.00 |   447.88 |    390 |    195.00 |      185.00 |         3,831 |
    | **NEGmir~any_worse**     |    87 |    1.66 |    0.47 |    0.00 |    98.47 |     90 |     45.00 |       42.00 |         2,007 |
    | **NEGmir~any_easier**    |    61 |    1.23 |    0.47 |    0.00 |    69.61 |     63 |     31.50 |       29.50 |           681 |
    | **NEGany~any_worse**     | 1,686 |    3.62 |    0.46 |    0.00 | 1,816.60 |  1,762 |    880.99 |      805.01 |        12,116 |
    | **NEGany~any_better**    | 4,719 |    3.59 |    0.44 |    0.00 | 4,753.39 |  5,004 |  2,501.98 |    2,217.02 |        50,827 |
    | **NEGany~any_different** |   902 |    3.03 |    0.44 |    0.00 |   905.82 |    957 |    478.50 |      423.50 |        80,643 |
    
    
    1. _any different_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                       |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_076.4343_x1218654_41:14-15-16`** | In an attempt at showing humility and that the government of Betazed is not __`any different`__ than it 's people , Betazed Prime has released an issue called " The Underwear of Women in Power . "                                                              |
    | **`nyt_eng_19970301_0050_6:36-38-39`**         | `` The way I read the Bible , '' said Ted Peters , a professor of systematic theology at Pacific Lutheran Theological Seminary in Berkeley , `` the status of that person before God would not be __`any different`__ from anyone born the old-fashioned way . '' |
    | **`nyt_eng_20000222_0298_31:4-5-6`**           | maybe it is n't __`any different`__ .                                                                                                                                                                                                                             |
    | **`nyt_eng_19990301_0161_34:3-8-9`**           | it should n't , technically , be __`any different`__ ; it 's just another actor in another scene . ''                                                                                                                                                             |
    | **`nyt_eng_19961003_0626_1:22-24-25`**         | Hot dogs and peanuts are mainstays of any baseball game , and the Rangers ' first playoff contest at home wo n't be __`any different`__ .                                                                                                                         |
    
    
    2. _any younger_
    
    |                                                | `token_str`                                                                                                            |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19961216_0697_14:4-6-7`**           | `` People are n't getting __`any younger`__ , so obviously that 's a market . ''                                       |
    | **`apw_eng_19980402_1805_29:5-7-8`**           | `` Our clients are not getting __`any younger`__ , and we are running out of time . ''                                 |
    | **`pcc_eng_20_087.1215_x1391379_19:14-16-17`** | She had to be in her eighties or nineties and she certainly could n't be __`any younger`__ than that .                 |
    | **`apw_eng_20090323_0044_8:4-6-7`**            | `` I 'm not getting __`any younger`__ , '' the 60-year-old told The Associated Press in a recent telephone interview . |
    | **`nyt_eng_20070819_0073_11:3-5-6`**           | he 's not getting __`any younger`__ , either , and his miles are piling up .                                           |
    
    
    3. _any nicer_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                            |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_059.4682_x0945278_112:7-8-9`**    | Relationships with the United States were n't __`any nicer`__ either as Kim would still portray the US as the bad guy and George W. Bush referring to North Korea as part of the ' axis of evil ' .                                                                                                                                                                                                    |
    | **`pcc_eng_25_082.9038_x1325749_44:24-27-28`**  | Instead of working with a megalomaniac , though , I found him to be this gentle , soft-spoken man , and he could n't have been __`any nicer`__ .                                                                                                                                                                                                                                                       |
    | **`pcc_eng_16_036.4489_x0573735_48:4-5-6`**     | The house was n't __`any nicer`__ than ours , but it did have an indoor toilet .                                                                                                                                                                                                                                                                                                                       |
    | **`pcc_eng_26_034.7833_x0546111_004:18-20-21`** | The cities have an abundance of charm , the food is fantastic , and the people could not be __`any nicer`__ .                                                                                                                                                                                                                                                                                          |
    | **`pcc_eng_24_028.5471_x0445389_33:62-63-64`**  | After this there is some vain effort of the movie to create a Snow White type story except instead of killing the daughter the stepmother wants to kill the Prince , at which point the movie kills off all of the boyfriends and ends with a cliffhanger where the nice boy , or in this case " the boy who is n't __`any nicer`__ but looks the most like Adam Sandler " is about to kiss the girl . |
    
    
    4. _any sweeter_
    
    |                                              | `token_str`                                                                                                                                                               |
    |:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_011.2648_x0166042_3:4-7-8`**   | The feeling could hardly have been __`any sweeter`__ after a victory that required a thrilling second half revival .                                                      |
    | **`pcc_eng_08_077.5286_x1239061_7:5-7-8`**   | " The puppy could n't be __`any sweeter`__ or happier .                                                                                                                   |
    | **`pcc_eng_00_018.3783_x0280527_24:6-8-9`**  | A deal like this could n't be __`any sweeter`__ .                                                                                                                         |
    | **`pcc_eng_29_043.1584_x0680959_030:2-4-5`** | But not really __`any sweeter`__ than New Haarlem or many others that the kids do n't normally wear .                                                                     |
    | **`pcc_eng_25_035.3909_x0556716_59:5-6-7`**  | I bet it is n't __`any sweeter`__ than normal Coke or Pepsi , but because the flavor is so odd , we are n't inured to it like we are with stuff we drink all the time . " |
    
    
    5. _any happier_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                         |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_043.3460_x0683882_09:4-6-7`**     | Happy Valley could n't be __`any happier`__ right now for Smith , the former Gateway High School star and coach , who was serving as an assistant coach at Temple until he got a phone call from Franklin .                                                                                                         |
    | **`pcc_eng_02_008.1936_x0116018_02:27-30-31`**  | Email OZONE PARK , N.Y. - While Indian Blessing was certainly impressive winning last Saturday 's Breeders ' Cup Juvenile Fillies , trainer Patrick Reynolds could n't have been __`any happier`__ with Backseat Rhythm 's third - place finish in that race .                                                      |
    | **`pcc_eng_19_070.3372_x1119818_188:10-12-13`** | If all the houses get 20 percent bigger , nobody is __`any happier`__ than before , especially people at the top .                                                                                                                                                                                                  |
    | **`pcc_eng_10_017.6884_x0269580_51:46-47-48`**  | Jackson , Serkis , Cameron and Trumbull have all thrown their considerable weight behind the idea , but Hollywood remains in a state of flux ; traditionalists once decried the switch from film to digital , and blogs around the web suggest that they 're not __`any happier`__ about this new format , either . |
    | **`pcc_eng_26_010.0120_x0145673_04:13-15-16`**  | This time he chose to work with Jecht Parker and we could n't be __`any happier`__ about it .                                                                                                                                                                                                                       |
    
    
    6. _any smarter_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                  |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_072.8807_x1161598_13:1-7-8`**     | Not that the good guys are __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                               |
    | **`pcc_eng_14_005.3539_x0070580_03:5-6-7`**     | Since I 'm probably not __`any smarter`__ than most of the people reading this column , I need to make sure I supply my readers with information that in one way or another is either uplifting , insightful to some degree , encouraging , entertaining , helpful in some way or emotionally stirring , bringing either a little lump to your throat or a little laugh or snicker ( or at least a smile ) . |
    | **`pcc_eng_29_039.4931_x0621544_141:07-12-13`** | Many inventions come from large cities not because city folk are __`any smarter`__ , but because the necessary mix of ideas was in the same place , at the same time .                                                                                                                                                                                                                                       |
    | **`pcc_eng_16_024.3102_x0377265_11:07-09-10`**  | The determination to be dour ca n't be __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                   |
    | **`pcc_eng_24_108.04689_x1739459_08:3-5-6`**    | You wo n't be __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                                            |
    
    
    7. _any brighter_
    
    |                                                  | `token_str`                                                                                                                                                                                                                                                      |
    |:-------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_031.6261_x0495715_04:3-5-6`**      | Life could n't be __`any brighter`__ for art dealer Christina Daniels .                                                                                                                                                                                          |
    | **`pcc_eng_24_085.9545_x1374105_21:5-6-7`**      | Nationally the picture is n't __`any brighter`__ :                                                                                                                                                                                                               |
    | **`pcc_eng_20_085.4477_x1364434_12:42-43-44`**   | Actually , I do n't know my hippocampus from my amygdala , but it 's nice to know that all those mornings I 've sat on my butt wrestling silently with my monkey mind might actually keep me lucid -- if not __`any brighter`__ -- long into my crusty old age . |
    | **`pcc_eng_29_093.1157_x1487984_25:1-5-6`**      | Nor is the picture __`any brighter`__ in Scottish retail .                                                                                                                                                                                                       |
    | **`pcc_eng_22_107.05830_x1722622_163:13-15-16`** | Despite falling short of a return to the playoffs the future could not be __`any brighter`__ for the Rockets with Steve Francis and Yao Ming forming the foundation of a team that enters a new state of the art arena next season .                             |
    
    
    8. _any easier_
    
    |                                                | `token_str`                                                                                                                                           |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_065.7207_x1046115_11:3-4-5`**    | It was n't __`any easier`__ to view knowing that there really were people out there who might actually believe him .                                  |
    | **`pcc_eng_29_004.8420_x0062172_19:5-8-9`**    | The whole process could n't have been __`any easier`__ .                                                                                              |
    | **`pcc_eng_10_084.4541_x1348798_60:3-4-5`**    | Things were n't __`any easier`__ in Washington state .                                                                                                |
    | **`pcc_eng_06_103.9841_x1665918_13:11-13-14`** | Getting in for a last minute face care treatment could n't be __`any easier`__ .                                                                      |
    | **`nyt_eng_20070413_0223_36:4-5-6`**           | since it is not __`any easier`__ on a patient than a total replacement , he says a patient should have pain every day before even thinking about it . |
    
    
    9. _any better_
    
    |                                                 | `token_str`                                                                                                     |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_002.9019_x0030530_017:09-10-11`** | To tell you the truth , it is n't __`any better`__ today .                                                      |
    | **`pcc_eng_11_099.5790_x1595772_22:5-6-7`**     | The scene there was n't __`any better`__ .                                                                      |
    | **`pcc_eng_06_076.8771_x1227329_13:4-6-7`**     | Rest days could n't be __`any better`__ , the town of Manang bustles with hordes of trekkers and locals alike . |
    | **`pcc_eng_06_078.9387_x1260341_14:6-8-9`**     | Gasol off the bench would not be __`any better`__ than a generic big man .                                      |
    | **`pcc_eng_12_007.6860_x0108096_08:3-5-6`**     | He 's not really __`any better`__ than Dent .                                                                   |
    
    
    10. _any worse_
    
    |                                                 | `token_str`                                                                                                                                                                                                    |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_022.2001_x0342474_006:08-09-10`** | I 'm kind of sore , but not __`any worse`__ than I was yesterday , so I 'm pretty good .                                                                                                                       |
    | **`pcc_eng_00_060.8636_x0967830_018:17-18-19`** | Something inside you says , " Well , it was always pretty bad , it 's not __`any worse`__ .                                                                                                                    |
    | **`pcc_eng_22_058.5142_x0929813_086:27-29-30`** | They said it was n't really stable -- there 's a lot of sharks and I was like , " I did fashion , it ca n't be __`any worse`__ " -- just kidding !                                                             |
    | **`pcc_eng_04_102.3672_x1637602_45:3-5-6`**     | It ca n't be __`any worse`__ anywhere else than what we were , what we were having here , so we got on the draft to Japan and then we went and landed in Nagasaki off this old tub of a ship that we were in . |
    | **`pcc_eng_13_080.5317_x1285422_05:17-18-19`**  | Later , the BBC , as expected , did exactly the same , but they were n't __`any worse`__ than ITN .                                                                                                            |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/...
    
    Samples saved as...
    1. `neg_bigram_examples/any/any_different_99ex.csv`
    1. `neg_bigram_examples/any/any_younger_99ex.csv`
    1. `neg_bigram_examples/any/any_nicer_99ex.csv`
    1. `neg_bigram_examples/any/any_sweeter_99ex.csv`
    1. `neg_bigram_examples/any/any_happier_99ex.csv`
    1. `neg_bigram_examples/any/any_smarter_99ex.csv`
    1. `neg_bigram_examples/any/any_brighter_99ex.csv`
    1. `neg_bigram_examples/any/any_easier_99ex.csv`
    1. `neg_bigram_examples/any/any_better_99ex.csv`
    1. `neg_bigram_examples/any/any_worse_99ex.csv`
    
    ## 5. *remotely*
    
    |                      |       `N` |      `f1` |   `adv_total` |
    |:---------------------|----------:|----------:|--------------:|
    | **NEGMIR_remotely**  |   583,470 |   291,732 |         1,953 |
    | **NEGATED_remotely** | 6,347,364 | 3,173,660 |         6,161 |
    
    
    |                                |   `f` |   `LRC` |   `dP1` |   `dP2` |   `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:-------------------------------|------:|--------:|--------:|--------:|-------:|-------:|----------:|------------:|--------------:|
    | **NEGany~remotely_true**       |   250 |    3.53 |    0.50 |    0.00 | 334.93 |    251 |    125.50 |      124.50 |        34,967 |
    | **NEGany~remotely_ready**      |    58 |    1.49 |    0.50 |    0.00 |  80.41 |     58 |     29.00 |       29.00 |        29,583 |
    | **NEGmir~remotely_comparable** |    44 |    1.15 |    0.50 |    0.00 |  61.00 |     44 |     22.00 |       22.00 |           158 |
    | **NEGany~remotely_enough**     |    47 |    1.13 |    0.50 |    0.00 |  65.16 |     47 |     23.50 |       23.50 |        27,603 |
    | **NEGany~remotely_surprising** |    75 |    1.66 |    0.49 |    0.00 |  94.71 |     76 |     38.00 |       37.00 |        18,776 |
    | **NEGmir~remotely_true**       |    61 |    1.43 |    0.48 |    0.00 |  75.72 |     62 |     31.00 |       30.00 |         2,850 |
    | **NEGany~remotely_funny**      |   137 |    2.16 |    0.47 |    0.00 | 159.09 |    141 |     70.50 |       66.50 |        14,992 |
    | **NEGmir~remotely_close**      |   218 |    2.58 |    0.46 |    0.00 | 244.21 |    226 |    113.00 |      105.00 |         4,831 |
    | **NEGany~remotely_close**      |   694 |    2.98 |    0.45 |    0.00 | 711.52 |    733 |    366.50 |      327.50 |        46,485 |
    | **NEGany~remotely_comparable** |   118 |    1.62 |    0.44 |    0.00 | 119.34 |    125 |     62.50 |       55.50 |         2,401 |
    | **NEGany~remotely_interested** |   330 |    1.99 |    0.41 |    0.00 | 278.69 |    364 |    182.00 |      148.00 |        34,543 |
    | **NEGany~remotely_similar**    |   152 |    1.39 |    0.40 |    0.00 | 123.97 |    169 |     84.50 |       67.50 |        11,088 |
    | **NEGany~remotely_related**    |   146 |    1.33 |    0.40 |    0.00 | 116.95 |    163 |     81.50 |       64.50 |        14,260 |
    
    
    1. _remotely comparable_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                  |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_061.8666_x0984999_048:12-13-14`** | Apart from the obvious fact that a socialist party newspaper is not __`remotely comparable`__ to a mainstream broadsheet , this is just hyperbolic nonsense .                                                                                                |
    | **`pcc_eng_21_090.1352_x1440643_46:2-4-5`**     | , not even __`remotely comparable`__ to revive or garrison .                                                                                                                                                                                                 |
    | **`pcc_eng_05_087.5005_x1399656_41:16-18-19`**  | It 's a mistake to equate elections with private-sector performance reviews , because they 're not even __`remotely comparable`__ .                                                                                                                          |
    | **`pcc_eng_10_019.2527_x0295016_57:5-6-7`**     | The two situations are n't __`remotely comparable`__ , and in fact I think they differ in at least six key ways :                                                                                                                                            |
    | **`pcc_eng_10_075.9474_x1211333_71:4-5-6`**     | " That is not __`remotely comparable`__ to the 5 million Syrians who fled the country in the first five years following the civil war - and that does n't include over a million per year who fled their homes inside Syria ( the internally displaced ) . " |
    
    
    2. _remotely ready_
    
    |                                                    | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
    |:---------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19980427_0151_37:08-09-10`**            | Mark had finally confessed : He was n't __`remotely ready`__ to be a father .                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    | **`pcc_eng_16_052.4669_x0833052_004:103-104-105`** | That a period of almost six months , a big , unprecedented chunk of time to get over the major knee surgery I had back in March ( that feels , in ' reality ' more like six weeks - it has passed so quickly I can hardly believe it ) , and which I thought would feel like an endless , half year sabbatical during which I would achieve all kinds of wonders - but failed to - is coming to a close as the summer ends , and autumn approaches , and the teaching begins , even though I am not __`remotely ready`__ for it to do so . |
    | **`pcc_eng_06_102.9020_x1648488_117:3-4-5`**       | I 'm not __`remotely ready`__ to talk about how to talk with kids about sex .                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    | **`pcc_eng_07_017.0566_x0259758_096:11-13-14`**    | I had been married less than a year and was n't even __`remotely ready`__ for kids .                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    | **`pcc_eng_19_072.8516_x1160639_48:24-25-26`**     | Whether because he spoke out of ego , or because he proposed a new communal and religious structure for which the people were n't __`remotely ready`__ -- Korach erred , and the earth swallowed him up .                                                                                                                                                                                                                                                                                                                                  |
    
    
    3. _remotely enough_
    
    |                                                 | `token_str`                                                                                                                                                                                              |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_011.3822_x0167616_06:15-16-17`**  | You will probably end up with 39 - 40 % equity , which is n't __`remotely enough`__ to make a profitable call here .                                                                                     |
    | **`pcc_eng_20_009.3703_x0135024_13:18-19-20`**  | Given the most generous assumptions of prebiotic chemistry , the Earth 's 4.6 billion year history is not __`remotely enough`__ to account for the string of chance happenings that are needed .         |
    | **`nyt_eng_20070720_0143_46:12-13-14`**         | FAIN : We now have 35 ships , and that is n't __`remotely enough`__ to satisfy all the itineraries we 'd like to do .                                                                                    |
    | **`pcc_eng_24_102.8076_x1647075_012:26-27-28`** | HINT : If you want to depend as little as possible on this walkthrough , keep a notebook ( a single sheet of paper is not __`remotely enough`__ ) to record what you learn from the people you talk to . |
    | **`pcc_eng_13_003.6495_x0042626_44:18-20-21`**  | What happens when your job just keeps on getting harder and harder and the salary increase is n't even __`remotely enough`__ to compensate for the stress you get and the life you waste ?               |
    
    
    4. _remotely true_
    
    |                                                | `token_str`                                                                                                                                                                                        |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_test_3.01795_x37265_16:34-35-36`**  | This is such a great question because I think there 's a popular perception that all a historian really needs is a great memory for names and dates , which is of course not __`remotely true`__ . |
    | **`pcc_eng_11_019.2848_x0295627_02:22-24-25`** | Most people think that a restaurant is the be all and end all of a chef 's career but that is not even __`remotely true`__ .                                                                       |
    | **`pcc_eng_09_002.1460_x0018593_20:4-5-6`**    | The same is not __`remotely true`__ here .                                                                                                                                                         |
    | **`pcc_eng_25_005.6198_x0075235_09:09-11-12`** | Not surprisingly , this turns out to be not even __`remotely true`__ .                                                                                                                             |
    | **`pcc_eng_07_026.4733_x0412048_0270:6-8-9`**  | We know the former is not even __`remotely true`__ , but what about the latter ?                                                                                                                   |
    
    
    5. _remotely surprising_
    
    |                                                | `token_str`                                                                                                                                                                                 |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_val_2.10616_x33464_17:5-6-7`**      | It 's telling but not __`remotely surprising`__ that Dionne looks to Europe , home of the cradle - to - grave welfare state , as the inspiration for the kind of capitalism he wants here . |
    | **`pcc_eng_08_059.9026_x0953880_11:15-16-17`** | That 's roughly in keeping with the first six Dot Music decisions and a not __`remotely surprising`__ result .                                                                              |
    | **`pcc_eng_26_036.1169_x0567619_157:3-4-5`**   | This is not __`remotely surprising`__ and proves that the liberal feels far more charitable with other people 's money than he does his own .                                               |
    | **`pcc_eng_00_034.7586_x0545419_23:7-8-9`**    | This is , of course , not __`remotely surprising`__ .                                                                                                                                       |
    | **`pcc_eng_test_1.1025_x01663_17:5-7-8`**      | The murder victim was n't even __`remotely surprising`__ nor was the murderer .                                                                                                             |
    
    
    6. _remotely funny_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                        |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_21_077.8633_x1242034_08:1-5-6`**    | None of this is __`remotely funny`__ , despite screenwriter Wayne Conley 's resorting to virtually every known stereotype                                                                                                                                                                                                                                          |
    | **`pcc_eng_06_107.1522_x1717198_08:25-34-35`** | He only wishes for Bode , currently a head trainer for the village security squad ; all sheep in wooden dog costumes , so few of the gags created by result are even __`remotely funny`__ ; to just find the natural energy his chosen life had been given , and just enjoy the work presented to him , even if the work is just a disappointing endeavor anyway . |
    | **`pcc_eng_25_040.3526_x0637005_48:3-5-6`**    | It 's not even __`remotely funny`__ .                                                                                                                                                                                                                                                                                                                              |
    | **`pcc_eng_11_099.0101_x1586566_22:12-13-14`** | For the first 30 minutes of the movie , there is nothing __`remotely funny`__ , original or entertaining .                                                                                                                                                                                                                                                         |
    | **`pcc_eng_20_041.2821_x0650845_31:1-3-4`**    | Not even __`remotely funny`__ . "                                                                                                                                                                                                                                                                                                                                  |
    
    
    7. _remotely close_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                    |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_068.3546_x1089543_59:3-4-5`**    | It was n't __`remotely close`__ to a full roster .                                                                                                                                                                                                                                                             |
    | **`pcc_eng_29_090.0462_x1438292_39:19-20-21`** | My second terror mission ( a Very Difficult ) was a total squad wipe , something I was never __`remotely close`__ to in Normal .                                                                                                                                                                               |
    | **`pcc_eng_08_107.2266_x1720081_09:10-12-13`** | ( Seriously , that never happened to me , not even __`remotely close`__ to happening . )                                                                                                                                                                                                                       |
    | **`pcc_eng_06_023.8409_x0369740_28:07-09-10`** | There is , for example , nothing even __`remotely close`__ to the sort of intellectual division that occurred during the Vietnam War in which the Kissingers and Bundys were matched by others -- including those the New York Times in 1970 headlined as " 1000 'ESTABLISHMENT ' LAWYERS JOIN WAR PROTEST . " |
    | **`pcc_eng_21_092.0065_x1470658_18:12-13-14`** | They may be working very hard at the office , but not __`remotely close`__ to what you did for your business .                                                                                                                                                                                                 |
    
    
    8. _remotely interested_
    
    |                                                | `token_str`                                                                                                                                                                                        |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_058.7447_x0932637_12:27-29-30`** | Use of the word -- in that specific situation , especially -- would be in keeping with his personality , though , as he tends to not be __`remotely interested`__ in political correctness , etc . |
    | **`pcc_eng_25_088.6580_x1418542_21:19-20-21`** | There are fifteen unique artwork sculptures which present an outstanding collection for the art enthusiast or for those not __`remotely interested`__ in art will still find them fascinating .    |
    | **`pcc_eng_18_037.3736_x0588488_10:21-22-23`** | Without US assistance , Israel is quite strong enough to take on any combination of Arab armies , which are n't __`remotely interested`__ in such a conflict .                                     |
    | **`pcc_eng_05_002.3054_x0021224_100:3-5-6`**   | I 'm not even __`remotely interested`__ . "                                                                                                                                                        |
    | **`pcc_eng_04_080.6541_x1286851_117:1-2-3`**   | Not __`remotely interested`__ .                                                                                                                                                                    |
    
    
    9. _remotely similar_
    
    |                                                 | `token_str`                                                                                                                                                                                                     |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_24_070.9022_x1130710_054:15-17-18`** | That word that has the letter C in the middle of it and is not even __`remotely similar`__ in meaning to the word this woman had said .                                                                         |
    | **`nyt_eng_20050112_0364_60:21-22-23`**         | but if you go deeper than this surface comparison , you can see that being a white middle-class person is not __`remotely similar`__ to what African-Americans had to go through in this country , '' he says . |
    | **`pcc_eng_25_003.2120_x0036074_37:16-17-18`**  | Glimpses of films like Sarkar and Sarkar Raj , besides Satya and Company , though not __`remotely similar`__ to Rakta Charitra , flash across your mind .                                                       |
    | **`pcc_eng_24_100.3273_x1606937_18:11-13-14`**  | It is also called " cruise " but it is not even __`remotely similar`__ to big time cruises .                                                                                                                    |
    | **`pcc_eng_06_078.4987_x1253180_06:3-4-5`**     | There 's nothing __`remotely similar`__ .                                                                                                                                                                       |
    
    
    10. _remotely related_
    
    |                                                 | `token_str`                                                                                                                                       |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_002.3133_x0021241_07:15-16-17`**  | Over time several movies have been released that have the same title that are n't __`remotely related`__ .                                        |
    | **`pcc_eng_15_043.0438_x0679735_56:5-6-7`**     | I know this is n't __`remotely related`__ to airport security , but I 'm just saying ...                                                          |
    | **`pcc_eng_04_047.1769_x0746320_13:23-25-26`**  | And , of course , there 's always the comment about not mentioning work in field x or y that really is n't even __`remotely related`__ to yours . |
    | **`pcc_eng_00_049.0295_x0776243_03:5-6-7`**     | -- Has turned up nothing __`remotely related`__ to " Trump- Russia collusion ; "                                                                  |
    | **`pcc_eng_04_059.5522_x0945877_048:15-17-18`** | And , his situation has absolutely nothing to do with Victor , they are not even __`remotely related`__ .                                         |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/...
    
    Samples saved as...
    1. `neg_bigram_examples/remotely/remotely_comparable_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_ready_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_enough_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_true_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_surprising_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_funny_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_close_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_interested_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_similar_99ex.csv`
    1. `neg_bigram_examples/remotely/remotely_related_99ex.csv`
    
    ## 6. *yet*
    
    |                 |       `N` |      `f1` |   `adv_total` |
    |:----------------|----------:|----------:|--------------:|
    | **NEGATED_yet** | 6,347,364 | 3,173,660 |        53,881 |
    
    
    |                          |    `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:-------------------------|-------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~yet_clear**     | 10,406 |    8.66 |    0.50 |    0.00 | 14,392.25 | 10,409 |  5,204.46 |    5,201.54 |        84,227 |
    | **NEGany~yet_ready**     |  7,501 |    8.06 |    0.50 |    0.00 | 10,344.81 |  7,505 |  3,752.47 |    3,748.53 |        29,583 |
    | **NEGany~yet_complete**  |  2,174 |    6.70 |    0.50 |    0.00 |  2,998.60 |  2,175 |  1,087.49 |    1,086.51 |         8,415 |
    | **NEGany~yet_available** |  7,430 |    6.66 |    0.50 |    0.00 |  9,950.03 |  7,461 |  3,730.47 |    3,699.53 |        82,956 |
    | **NEGany~yet_sure**      |  1,977 |    6.13 |    0.50 |    0.00 |  2,689.26 |  1,981 |    990.49 |      986.51 |       134,139 |
    | **NEGany~yet_certain**   |    866 |    5.60 |    0.50 |    0.00 |  1,200.66 |    866 |    433.00 |      433.00 |        11,334 |
    | **NEGany~yet_able**      |  1,315 |    5.44 |    0.50 |    0.00 |  1,764.46 |  1,320 |    660.00 |      655.00 |        23,355 |
    | **NEGany~yet_final**     |    640 |    5.16 |    0.50 |    0.00 |    887.30 |    640 |    320.00 |      320.00 |         1,213 |
    | **NEGany~yet_public**    |    467 |    4.69 |    0.50 |    0.00 |    647.44 |    467 |    233.50 |      233.50 |         2,656 |
    | **NEGany~yet_dead**      |    401 |    4.47 |    0.50 |    0.00 |    555.93 |    401 |    200.50 |      200.50 |         6,348 |
    
    
    1. _yet clear_
    
    |                                             | `token_str`                                                                                                                                                                                                                     |
    |:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_25_093.3992_x1495372_12:3-4-5`** | It 's not __`yet clear`__ how the women died , but authorities say they are believed to be have been dead for about a week .                                                                                                    |
    | **`pcc_eng_00_069.0951_x1100531_07:3-4-5`** | It 's not __`yet clear`__ whether Hefazat- i- Islam is itself a player or simply a pawn , as the standoff between the government and the opposition continues to spiral violently out of control .                              |
    | **`pcc_eng_21_029.4607_x0460080_07:3-4-5`** | It is not __`yet clear`__ whether they intend to try to seek asylum in the United Kingdom                                                                                                                                       |
    | **`apw_eng_20090331_0254_2:7-8-9`**         | Dr. Moaiya Hassanain says it is not __`yet clear`__ if the men are civilians or militants .                                                                                                                                     |
    | **`pcc_eng_28_048.6729_x0771269_02:3-4-5`** | It is not __`yet clear`__ what kinds of guns were used in the terrorist attack , which occurred in central Christchurch , but authorities have said that a number of firearms were recovered from the scenes of the shootings . |
    
    
    2. _yet certain_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                    |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_092.4534_x1478089_12:24-25-26`** | " When I arrived at UA , I knew I belonged in the College of Communication and Information Sciences , but I was n't __`yet certain`__ about a major , " Beard admits .                                                                                                                                         |
    | **`pcc_eng_24_073.6704_x1175575_11:20-22-23`** | On DC 's latest injury report , the duo were upgraded to questionable , but a specific timeline is n't quite __`yet certain`__ -- Quaranta has missed less time , and said that he could be back in less than two weeks , while Mc Tavish must take a more patient approach .                                  |
    | **`pcc_eng_18_082.2076_x1314908_29:3-4-5`**    | Shane is not __`yet certain`__ why this is happening , noting " I do n't have the evidence to evaluate the impact of technological change , a shift in the regulatory environment , different credit conditions or any of the multitude of other factors that policy makers and pundits say is responsible . " |
    | **`pcc_eng_11_057.7271_x0917778_12:6-7-8`**    | Daily that his company is n't __`yet certain`__ it will distribute its CBD line of beverages outside the United States , but the deal will provide the infrastructure that would allow it to do so .                                                                                                           |
    | **`nyt_eng_19960920_0376_4:6-7-8`**            | and , while it is n't __`yet certain`__ whether Christopher would stay on should Clinton win a second term , a half dozen contenders have emerged to fill the top diplomat 's post if he leaves .                                                                                                              |
    
    
    3. _yet ready_
    
    |                                                | `token_str`                                                                                                                                                                                    |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_10_058.0193_x0922098_10:11-12-13`** | Lead nurturing focuses on educating qualified sales leads who are not __`yet ready`__ to buy .                                                                                                 |
    | **`pcc_eng_09_008.2836_x0117987_07:15-16-17`** | The details of Malaysia 's proposed changes to the RTS Link project is " not __`yet ready`__ " , said Khaw in a written response to a question raised in Parliament on Monday ( 4 November ) . |
    | **`pcc_eng_20_005.4583_x0071880_33:5-6-7`**    | I know you are not __`yet ready`__ to name your partners , but can you tell me in general terms where the support for this is coming from ?                                                    |
    | **`pcc_eng_03_081.3842_x1301805_18:21-22-23`** | And the fact that you have to ask the second question leads me directly to the conclusion that you 're not __`yet ready`__ to hear the answer to the first .                                   |
    | **`pcc_eng_15_006.1874_x0083697_16:13-14-15`** | Renewable energy sources , like solar and advanced biofuels , are simply not __`yet ready`__ to compete with fossil fuels .                                                                    |
    
    
    4. _yet final_
    
    |                                                 | `token_str`                                                                                                                                            |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_070.8559_x1130196_266:14-15-16`** | Keep in mind that FCC 's decision is still a proposal and is not __`yet final`__ .                                                                     |
    | **`pcc_eng_21_013.9104_x0208556_48:10-11-12`**  | If the couple remains separated but the divorce is not __`yet final`__ , they can choose between married filing separately or filing jointly .         |
    | **`apw_eng_19980130_1063_2:09-10-11`**          | Ministry spokesman Martin Erdmann said the verdict was not __`yet final`__ , and had no details on how the case was to proceed .                       |
    | **`pcc_eng_11_080.5745_x1288063_13:21-22-23`**  | The exception is prisoners who are still appealing -- generally , the more recent cases -- because their convictions are not __`yet final`__ .         |
    | **`pcc_eng_11_081.6816_x1305928_17:24-25-26`**  | That is because the Supreme Court held that Ring was not retroactive , meaning it only applied to cases where the conviction was not __`yet final`__ . |
    
    
    5. _yet public_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_044.2605_x0698871_3:25-26-27`**  | In the speech at Georgetown University , according to individuals briefed on the matter who asked not to be identified because the plan was not __`yet public`__ , Obama will detail a government - wide plan to not only reduce the nation 's carbon output but also prepare the United States for the near-term impacts of global warming . |
    | **`pcc_eng_01_093.9012_x1502184_36:18-19-20`** | He also likely received a second payment on Oct. 31 , 2010 -- though those records are not __`yet public`__ .                                                                                                                                                                                                                                 |
    | **`pcc_eng_15_032.4341_x0508249_12:27-28-29`** | At the time of the oversight hearing I just mentioned , information about the investigation of the phone records of James Rosen of Fox News was not __`yet public`__ .                                                                                                                                                                        |
    | **`pcc_eng_27_057.1924_x0908445_6:15-16-17`**  | The names of the other women invited to the 30 - member board are not __`yet public`__ , Rabbi Weissmann said .                                                                                                                                                                                                                               |
    | **`apw_eng_20090728_0093_4:12-13-14`**         | the official spoke on condition of anonymity because the announcement was not __`yet public`__ .                                                                                                                                                                                                                                              |
    
    
    6. _yet dead_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                     |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_063.1014_x1004556_288:3-4-5`**   | God is not __`yet dead`__ .                                                                                                                                                                                                                                                     |
    | **`pcc_eng_14_092.7366_x1483086_37:52-53-54`** | To do so , he says , would lead to " horrendous " consequences , essentially what he 's been saying since August 2005 at a time when one could arguably make the case that there was no civil war in Iraq and 750 Americans who have since died there were n't __`yet dead`__ . |
    | **`pcc_eng_13_043.5441_x0687931_164:6-7-8`**   | He explains that Gar was not __`yet dead`__ , but he could not ...                                                                                                                                                                                                              |
    | **`pcc_eng_26_093.7556_x1499995_66:7-8-9`**    | It appears as the academy is not __`yet dead`__ ..                                                                                                                                                                                                                              |
    | **`nyt_eng_19980227_0373_29:08-09-10`**        | although Indonesian officials say the plan is not __`yet dead`__ , the tide has turned against the professor .                                                                                                                                                                  |
    
    
    7. _yet complete_
    
    |                                                | `token_str`                                                                                                                                                              |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_089.7386_x1436753_25:5-6-7`**    | While the assessment is not __`yet complete`__ , initial findings can be seen in the Biodiversity Trends Report .                                                        |
    | **`pcc_eng_21_092.7563_x1482657_23:28-29-30`** | The open-ended data are not included in this dataset because they were coded by the research team , and the analyses of some of these data were not __`yet complete`__ . |
    | **`pcc_eng_22_053.5249_x0848569_031:4-5-6`**   | The pill is not __`yet complete`__ , so the aroma of the pill is illusory .                                                                                              |
    | **`pcc_eng_28_020.1643_x0309873_10:09-10-11`** | The underlying control structure for HOX genes is not __`yet complete`__ either .                                                                                        |
    | **`pcc_eng_03_043.8172_x0693752_41:16-17-18`** | We remember the aborted from 1973 - 2014 with the knowledge that their number is not __`yet complete`__ .                                                                |
    
    
    8. _yet sure_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                       |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_099.7806_x1596422_038:3-4-5`**   | Archaeologists are not __`yet sure`__ of why , but they are leaning towards the fact that artists status was low in the hierarchy so they could never be in front of a higher authority figure , and never be faced towards them .                                                |
    | **`pcc_eng_22_052.8540_x0837697_12:17-18-19`** | I 'm not certain she 's ready to hear something like this , and I 'm not __`yet sure`__ I trust her to not react badly to it .                                                                                                                                                    |
    | **`pcc_eng_00_063.2387_x1006203_14:4-5-6`**    | " We are not __`yet sure`__ as to the size of the Democratic majority , but we wanted to make sure we had our leadership in place for the new year , " Rigger said .                                                                                                              |
    | **`pcc_eng_10_042.6651_x0674168_47:23-24-25`** | " The campaign has yet to find or appoint key local leaders or open a campaign office in the county and is n't __`yet sure`__ which Hamilton County Republican party 's central committee members are allied with the Republican presidential nominee , " reported the Enquirer . |
    | **`pcc_eng_17_101.6001_x1626097_13:11-12-13`** | Whilst experts are pleased with the results , they are not __`yet sure`__ if it could be repeated in humans , or if it will help them quit smoking .                                                                                                                              |
    
    
    9. _yet available_
    
    |                                                | `token_str`                                                                                                                                                                                                                    |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_011.4346_x0168930_5:16-17-18`**  | ( Complete fourth quarter numbers were only released yesterday , so break - downs are n't __`yet available`__ by industry . )                                                                                                  |
    | **`apw_eng_20090412_0619_19:4-5-6`**           | autopsy results are not __`yet available`__ , and investigators declined to say whether they believe the slaying was accidental or deliberate .                                                                                |
    | **`pcc_eng_27_020.3301_x0312725_24:09-10-11`** | While it 's good that the shares are n't __`yet available`__ for sale , notice that Facebook itself has effectively purchased the remaining more than 21 million shares at the conversion price of $ 23.21 ( $ 487 million ) . |
    | **`pcc_eng_16_040.7515_x0643406_41:28-29-30`** | You 'll also need the Dialog to stream music from the online service Tidal ( the Phantom also supports Deezer and Qoboz , but those services are not __`yet available`__ in the U.S. ) .                                       |
    | **`pcc_eng_24_070.1390_x1118313_12:6-7-8`**    | The service , which is not __`yet available`__ or even ready to be demoed by press , is a live TV streaming service , similar to what you see from AT&T 's DIRECTV NOW and Sony's Play Station Vue .                           |
    
    
    10. _yet able_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_037.2737_x0586478_04:09-10-11`** | Twenty - seven of the new retirees are n't __`yet able`__ to join the AARP , as they are under the age of 50 .                                                                                                                                                                                |
    | **`apw_eng_20090917_1428_35:08-09-10`**        | the document concludes that while Iran is not __`yet able`__ to equip its Shahab-3 medium-range missile with nuclear warheads , `` it is likely that Iran will overcome problems , '' noting that `` from the evidence presented to the agency , it is possible to suggest that ...           |
    | **`pcc_eng_21_067.7198_x1078185_17:48-49-50`** | While players are required to update to the latest patch as soon as it is released on their current platform , because patches are released at different times for different platforms , it is possible to update one device to a new patch while the other is not __`yet able`__ to update . |
    | **`pcc_eng_01_033.0376_x0517809_09:6-7-8`**    | However , the researchers are not __`yet able`__ to pin down whether sleeplessness precedes gray matter loss or the other way around .                                                                                                                                                        |
    | **`pcc_eng_03_007.2131_x0100372_020:5-6-7`**   | But those acts were n't __`yet able`__ to get the big sales numbers needed to cross over to the top of the mainstream album charts ( or at least their sales were n't being accurately reported from record stores to the trades to get those results ) .                                     |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/...
    
    Samples saved as...
    1. `neg_bigram_examples/yet/yet_clear_99ex.csv`
    1. `neg_bigram_examples/yet/yet_certain_99ex.csv`
    1. `neg_bigram_examples/yet/yet_ready_99ex.csv`
    1. `neg_bigram_examples/yet/yet_final_99ex.csv`
    1. `neg_bigram_examples/yet/yet_public_99ex.csv`
    1. `neg_bigram_examples/yet/yet_dead_99ex.csv`
    1. `neg_bigram_examples/yet/yet_complete_99ex.csv`
    1. `neg_bigram_examples/yet/yet_sure_99ex.csv`
    1. `neg_bigram_examples/yet/yet_available_99ex.csv`
    1. `neg_bigram_examples/yet/yet_able_99ex.csv`
    
    ## 7. *immediately*
    
    |                         |       `N` |      `f1` |   `adv_total` |
    |:------------------------|----------:|----------:|--------------:|
    | **NEGATED_immediately** | 6,347,364 | 3,173,660 |        58,040 |
    | **NEGMIR_immediately**  |   583,470 |   291,732 |           564 |
    
    
    |                                   |    `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:----------------------------------|-------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
    | **NEGany~immediately_clear**      | 24,416 |    7.55 |    0.50 |    0.01 | 33,058.44 | 24,488 | 12,243.92 |   12,172.08 |        84,227 |
    | **NEGany~immediately_possible**   |  1,000 |    5.40 |    0.50 |    0.00 |  1,360.38 |  1,002 |    501.00 |      499.00 |        30,446 |
    | **NEGany~immediately_sure**       |    138 |    2.87 |    0.50 |    0.00 |    191.31 |    138 |     69.00 |       69.00 |       134,139 |
    | **NEGany~immediately_reachable**  |    109 |    2.50 |    0.50 |    0.00 |    151.11 |    109 |     54.50 |       54.50 |           350 |
    | **NEGany~immediately_certain**    |     70 |    1.80 |    0.50 |    0.00 |     97.04 |     70 |     35.00 |       35.00 |        11,334 |
    | **NEGany~immediately_available**  | 21,078 |    5.34 |    0.48 |    0.01 | 25,870.14 | 21,477 | 10,738.43 |   10,339.57 |        82,956 |
    | **NEGany~immediately_able**       |    626 |    3.66 |    0.48 |    0.00 |    746.39 |    641 |    320.50 |      305.50 |        23,355 |
    | **NEGany~immediately_successful** |    290 |    2.87 |    0.47 |    0.00 |    333.73 |    299 |    149.50 |      140.50 |        31,460 |
    | **NEGany~immediately_obvious**    |  2,238 |    3.88 |    0.46 |    0.00 |  2,481.50 |  2,325 |  1,162.49 |    1,075.51 |        22,651 |
    | **NEGany~immediately_apparent**   |  2,015 |    3.30 |    0.44 |    0.00 |  2,001.83 |  2,143 |  1,071.49 |      943.51 |         9,798 |
    | **NEGmir~immediately_available**  |    162 |    1.34 |    0.38 |    0.00 |    120.41 |    184 |     92.00 |       70.00 |         3,079 |
    
    
    1. _immediately sure_
    
    |                                                  | `token_str`                                                                                                                                                                                               |
    |:-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_108.00204_x1731331_064:12-13-14`** | Due to the closeness of the finish , Denny Hamlin was n't __`immediately sure`__ race won the 2016 Daytona 500 .                                                                                          |
    | **`pcc_eng_18_083.2969_x1332643_01:18-19-20`**   | The officer , who was an acquaintance of the well -known traditional healer , said policemen were not __`immediately sure`__ what the smell was as Mbatha walked up to the desk at about 6 pm on Friday . |
    | **`apw_eng_20021204_0594_5:09-10-11`**           | spokesmen for the Foreign Ministry said they were not __`immediately sure`__ if the discrepancy was due to a slip of the tongue or if one country was not invited .                                       |
    | **`apw_eng_20030214_0107_32:4-5-6`**             | a spokesman was not __`immediately sure`__ which of the shuttle 's tires was found .                                                                                                                      |
    | **`nyt_eng_19970620_0363_5:5-6-7`**              | the Goldman official was n't __`immediately sure`__ of Cohen 's old target for the S&P index of 500 stocks , but believed it had been 900 .                                                               |
    
    
    2. _immediately reachable_
    
    |                                                | `token_str`                                                                                                                    |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_068.7921_x1095661_30:6-7-8`**    | Ferguson 's old assistant was not __`immediately reachable`__ .                                                                |
    | **`pcc_eng_02_096.6577_x1546677_08:5-6-7`**    | Hybrid Air Vehicles was not __`immediately reachable`__ by telephone .                                                         |
    | **`pcc_eng_11_083.1162_x1329074_10:17-18-19`** | Soft Bank also declined to comment , while Tiger , its other lead investor , was not __`immediately reachable`__ for comment . |
    | **`pcc_eng_28_013.3710_x0200419_5:09-10-11`**  | The U.S. Attorney 's Office in Manhattan was not __`immediately reachable`__ for comment .                                     |
    | **`pcc_eng_05_083.3476_x1332698_5:4-5-6`**     | The company was not __`immediately reachable`__ for comment .                                                                  |
    
    
    3. _immediately certain_
    
    |                                                | `token_str`                                                                                                                                                                                                                   |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_028.7656_x0449158_10:18-19-20`** | Brown said district officials had hoped to resume classes this week , and she said it was n't __`immediately certain`__ if the layoff would add days to the end of the school year .                                          |
    | **`pcc_eng_13_038.9102_x0612956_50:3-4-5`**    | It was not __`immediately certain`__ how the Bastrop blaze began but it appeared that two fires merged to form the " monster " fire , Amen said .                                                                             |
    | **`pcc_eng_06_079.1498_x1263719_15:19-20-21`** | She has since been identified by the medical examiner 's office , Brunner said , but it was not __`immediately certain`__ whether Raffo was among the 17 victims officially counted among the dead as of Friday .             |
    | **`apw_eng_19970417_0626_27:3-4-5`**           | it was not __`immediately certain`__ what impact Moilim 's edict _ contravention of which carries an automatic but undefined prison sentence without benefit of trial _ would have on the islands ' infant tourism industry . |
    | **`apw_eng_20080718_1359_5:14-15-16`**         | the casualties were in the area of the crane , but officials were n't __`immediately certain`__ whether they were on the crane or near it , Roecker said .                                                                    |
    
    
    4. _immediately clear_
    
    |                                               | `token_str`                                                                                                                                                                                                                                   |
    |:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_28_036.2730_x0570397_3:13-14-15`** | The UK - based Syrian Observatory for Human Rights said it was not __`immediately clear`__ whether Monday 's strikes on al- Atarib , a town in a so-called de-escalation zone , had been carried out by Syrian warplanes or those of Russia . |
    | **`apw_eng_19970905_0514_3:3-4-5`**           | it was n't __`immediately clear`__ what caused the collapse , but party members said powerful winds _ possibly a tornado _ damaged the structure .                                                                                            |
    | **`apw_eng_20020322_0621_3:3-4-5`**           | it was not __`immediately clear`__ whether the bomber had intended to carry out an attack in Israel or at the checkpoint .                                                                                                                    |
    | **`apw_eng_20090311_1160_8:13-14-15`**        | the restaurant can reopen as soon as Thursday , but it was not __`immediately clear`__ if it would .                                                                                                                                          |
    | **`apw_eng_19970517_0492_13:3-4-5`**          | it was not __`immediately clear`__ what Yeltsin planned to do about Luzhkov 's open opposition , which could encourage other politicians to refuse to submit income declarations of their family members .                                    |
    
    
    5. _immediately possible_
    
    |                                             | `token_str`                                                                                                                                                     |
    |:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20020809_0272_8:3-4-5`**         | it was not __`immediately possible`__ to contact either of the groups .                                                                                         |
    | **`pcc_eng_14_092.9223_x1486166_26:3-4-5`** | It was not __`immediately possible`__ to verify Afridi 's claims .                                                                                              |
    | **`apw_eng_20090412_0198_14:3-4-5`**        | it was not __`immediately possible`__ to verify that report .                                                                                                   |
    | **`apw_eng_20030604_0004_4:3-4-5`**         | it was n't __`immediately possible`__ to ascertain the credibility of the man 's claim .                                                                        |
    | **`pcc_eng_28_048.9783_x0776262_17:3-4-5`** | It was not __`immediately possible`__ to get a comment from Barrick on how a potential strike could affect construction or whether it could delay the project . |
    
    
    6. _immediately available_
    
    |                                                | `token_str`                                                                                                                                                                          |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20021120_0828_4:22-23-24`**         | Chan told reporters he could not immediately say how much money his client would get and copies of the ruling were not __`immediately available`__ .                                 |
    | **`apw_eng_20081212_1173_7:17-18-19`**         | he was out of the country Friday for a promotional tour for the film and was n't __`immediately available`__ for comment , his representative , Alan Nierob , said .                 |
    | **`apw_eng_20020322_0711_3:5-6-7`**            | Kirch 's spokesman was not __`immediately available`__ for comment .                                                                                                                 |
    | **`pcc_eng_01_078.1521_x1247455_18:09-10-11`** | A spokesperson for the City of Portland was not __`immediately available`__ for comment .                                                                                            |
    | **`apw_eng_19970514_0868_2:6-7-8`**            | details of the fighting were not __`immediately available`__ , but a Defense Ministry statement said 23 soldiers were wounded `` while inflicting heavy casualties on the enemy . '' |
    
    
    7. _immediately able_
    
    |                                                | `token_str`                                                                                                                                                                                   |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20091126_0247_5:5-6-7`**            | a police official was not __`immediately able`__ to comment .                                                                                                                                 |
    | **`pcc_eng_28_018.6471_x0285362_11:29-30-31`** | The prices and demand for such things fluctuate over time , but credit access allows SME 's to be able to obtain such resources even if they are not __`immediately able`__ to pay them off . |
    | **`pcc_eng_24_103.1739_x1653027_15:3-4-5`**    | Michener was not __`immediately able`__ to say what the average cost of these procedures would have been in out - of- network facilities that are not being sued by Aetna .                   |
    | **`apw_eng_20030512_0656_12:4-5-6`**           | Saudi officials were not __`immediately able`__ to confirm these reports .                                                                                                                    |
    | **`pcc_eng_08_047.2963_x0749420_04:3-4-5`**    | Deputies were n't __`immediately able`__ to identify her body .                                                                                                                               |
    
    
    8. _immediately successful_
    
    |                                                | `token_str`                                                                                                                                                                                               |
    |:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`apw_eng_20020108_0649_8:20-21-22`**         | attempts to contact Salif Diao , the players ' spokesman and a midfielder at French club Sedan , were n't __`immediately successful`__ .                                                                  |
    | **`pcc_eng_11_086.7944_x1388798_34:30-31-32`** | There 's no point in asking a young player to make the switch if they 're going to be dropped or not selected the following year because they were n't __`immediately successful`__ in the first season . |
    | **`pcc_eng_13_046.4318_x0734532_04:13-14-15`** | Efforts to reach both Krispy Kreme and Broadstone about the arrangement were not __`immediately successful`__ .                                                                                           |
    | **`pcc_eng_21_071.6104_x1141054_09:16-17-18`** | The causes of death were not announced and attempts to contact relatives for comment were not __`immediately successful`__ .                                                                              |
    | **`apw_eng_20090324_0028_5:09-10-11`**         | attempts to obtain a comment from Frank were not __`immediately successful`__ Monday .                                                                                                                    |
    
    
    9. _immediately obvious_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                   |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_048.6359_x0769643_068:15-16-17`** | Machine learning can do things very fast and find pieces of data that are not __`immediately obvious`__ .                                                                                                                                                                                                                                     |
    | **`pcc_eng_07_013.4893_x0202356_42:09-11-12`**  | One solution to solve the problem of it not being __`immediately obvious`__ where all your papers appeared is to increase the size of the white background halo , especially at far out zoom levels .                                                                                                                                         |
    | **`pcc_eng_14_087.5456_x1398977_16:28-29-30`**  | While most of our companies are mid-sized and in the Midwest , East , and South , 15 % are in the West , where it is n't __`immediately obvious`__ how to segment the sales territories , as seen below in a map of the San Francisco / San Jose region .                                                                                     |
    | **`pcc_eng_07_024.0710_x0372990_42:60-61-62`**  | " Esthetique du Mal , " that appears on the face of things to be a rather idiosyncratic choice , and yet he succeeds not only in making the case for that poem itself , often overlooked beside the other , late works , but also finds in it a revisiting of a number of Romanticism 's central but not __`immediately obvious`__ concerns . |
    | **`pcc_eng_25_008.5105_x0121808_10:08-09-10`**  | Well , Falcao excepted , it 's not __`immediately obvious`__ why they 're doing so well .                                                                                                                                                                                                                                                     |
    
    
    10. _immediately apparent_
    
    |                                                 | `token_str`                                                                                                                                                                                                                              |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_22_008.3119_x0118001_02:19-20-21`**  | Medical researchers counting on traditionally indexed bibliographic databases may very well be missing the distilled essence of analysis not __`immediately apparent`__ in tables , figures , and pictures found in scholarly articles . |
    | **`pcc_eng_29_095.4200_x1525441_138:12-13-14`** | Soy is more insidious than hemlock because it effects are often not __`immediately apparent`__ .                                                                                                                                         |
    | **`pcc_eng_15_012.4335_x0184496_22:5-6-7`**     | Many chronic injuries are not __`immediately apparent`__ , but are still caused by the impact of the crash .                                                                                                                             |
    | **`pcc_eng_17_055.6526_x0882981_26:4-5-6`**     | Though it is not __`immediately apparent`__ how long Gordon will be absent , he will not be there for the start due to his ongoing recovery .                                                                                            |
    | **`pcc_eng_24_105.0035_x1682716_086:07-09-10`** | The motivation for such behavior is not always __`immediately apparent`__ .                                                                                                                                                              |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/...
    
    Samples saved as...
    1. `neg_bigram_examples/immediately/immediately_sure_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_reachable_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_certain_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_clear_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_possible_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_available_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_able_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_successful_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_obvious_99ex.csv`
    1. `neg_bigram_examples/immediately/immediately_apparent_99ex.csv`
    
    ## 8. *ever*
    
    |                     |       `N` |      `f1` |   `adv_total` |
    |:--------------------|----------:|----------:|--------------:|
    | **NEGMIR_ever**     |   583,470 |   291,732 |         4,786 |
    | **COMPLEMENT_ever** | 6,347,364 | 3,173,552 |        10,870 |
    | **NEGATED_ever**    | 6,347,364 | 3,173,660 |        10,870 |
    
    
    |                         |   `f` |   `LRC` |   `dP1` |   `dP2` |   `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:------------------------|------:|--------:|--------:|--------:|-------:|-------:|----------:|------------:|--------------:|
    | **NEGmir~ever_easy**    |   368 |    4.21 |    0.50 |    0.00 | 497.96 |    369 |    184.50 |      183.50 |         7,749 |
    | **NEGmir~ever_good**    |   299 |    3.90 |    0.50 |    0.00 | 402.64 |    300 |    150.00 |      149.00 |        13,423 |
    | **NEGmir~ever_perfect** |   206 |    3.60 |    0.50 |    0.00 | 285.65 |    206 |    103.00 |      103.00 |         1,303 |
    | **NEGmir~ever_simple**  |   206 |    3.60 |    0.50 |    0.00 | 285.65 |    206 |    103.00 |      103.00 |         7,465 |
    | **NEGany~ever_simple**  |   211 |    3.28 |    0.50 |    0.00 | 281.20 |    212 |    106.00 |      105.00 |        46,867 |
    | **NEGmir~ever_enough**  |   147 |    3.09 |    0.50 |    0.00 | 203.83 |    147 |     73.50 |       73.50 |         1,326 |
    | **NEGmir~ever_certain** |   143 |    3.04 |    0.50 |    0.00 | 198.28 |    143 |     71.50 |       71.50 |         1,276 |
    | **COM~ever_larger**     |   139 |    2.88 |    0.50 |    0.00 | 192.71 |    139 |     69.50 |       69.50 |         7,453 |
    | **NEGmir~ever_wrong**   |   102 |    2.52 |    0.50 |    0.00 | 141.42 |    102 |     51.00 |       51.00 |         8,506 |
    | **NEGany~ever_boring**  |    72 |    1.84 |    0.50 |    0.00 |  99.82 |     72 |     36.00 |       36.00 |         3,840 |
    | **NEGmir~ever_black**   |    56 |    1.56 |    0.50 |    0.00 |  77.64 |     56 |     28.00 |       28.00 |           646 |
    | **NEGmir~ever_right**   |    49 |    1.33 |    0.50 |    0.00 |  67.93 |     49 |     24.50 |       24.50 |         2,038 |
    | **COM~ever_closer**     |   279 |    3.52 |    0.49 |    0.00 | 365.82 |    281 |    140.49 |      138.51 |         3,686 |
    | **COM~ever_greater**    |   186 |    3.09 |    0.49 |    0.00 | 246.80 |    187 |     93.50 |       92.50 |         6,949 |
    | **NEGmir~ever_able**    |   136 |    2.71 |    0.49 |    0.00 | 178.12 |    137 |     68.50 |       67.50 |         1,891 |
    | **COM~ever_higher**     |   129 |    2.52 |    0.49 |    0.00 | 168.50 |    130 |     65.00 |       64.00 |        12,992 |
    | **NEGany~ever_easy**    |   429 |    3.53 |    0.48 |    0.00 | 525.98 |    437 |    218.50 |      210.50 |       108,923 |
    | **COM~ever_deeper**     |    61 |    1.31 |    0.48 |    0.00 |  75.72 |     62 |     31.00 |       30.00 |         1,768 |
    | **COM~ever_mindful**    |    52 |    1.04 |    0.48 |    0.00 |  63.56 |     53 |     26.50 |       25.50 |           784 |
    | **NEGany~ever_good**    |   331 |    2.52 |    0.45 |    0.00 | 337.56 |    350 |    175.00 |      156.00 |       201,244 |
    
    
    1. _ever perfect_
    
    |                                              | `token_str`                                                                                                                                                                                                          |
    |:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_008.9662_x0128549_072:6-8-9`** | Nothing is ever finished , nothing is __`ever perfect`__ , but over and over again the race of men gets another chance to do better than last time , ever and again without end .                                    |
    | **`pcc_eng_03_001.9967_x0016168_12:2-4-5`**  | But nothing is __`ever perfect`__ , and the difference is that we 're willing to try .                                                                                                                               |
    | **`pcc_eng_19_088.2393_x1409890_159:1-3-4`** | Nothing is __`ever perfect`__ , I said , but that does n't mean things ca n't be good .                                                                                                                              |
    | **`pcc_eng_22_057.2517_x0909124_26:1-3-4`**  | Nothing is __`ever perfect`__ or easy .                                                                                                                                                                              |
    | **`pcc_eng_01_048.0981_x0761056_24:1-3-4`**  | Nothing is __`ever perfect`__ , but when steps that create value for specific products , allowing continuous flow , the process of reducing effort , time , space , cost , and mistakes , everything falls in line . |
    
    
    2. _ever simple_
    
    |                                                | `token_str`                                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_009.0392_x0130251_17:36-38-39`** | The author even touched on some of the motivations of the hijackers and humanized them , which was an important perspective to include , demonstrating that while some things are wrong regardless of rationalization , nothing is __`ever simple`__ . |
    | **`pcc_eng_11_083.1163_x1329077_21:23-25-26`** | In other words , even if we genuinely love someone , the realities of life have a way of reminding us that nothing is __`ever simple`__ ...                                                                                                            |
    | **`pcc_eng_29_043.6736_x0689403_20:1-5-6`**    | Nothing in Britain is __`ever simple`__ , is it ?                                                                                                                                                                                                      |
    | **`pcc_eng_19_018.4605_x0281750_03:5-6-7`**    | Experiencing family strife is never __`ever simple`__ , yet a skilled family members law lawyer can assist you make essential choices as well as locate a new begin .                                                                                  |
    | **`pcc_eng_05_012.4146_x0185066_04:3-4-5`**    | It is n't __`ever simple`__ to outright find a soul mate since most individuals are already aware .                                                                                                                                                    |
    
    
    3. _ever enough_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                      |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_076.8617_x1225337_259:5-7-8`**   | The ones for whom nothing is __`ever enough`__ , no amount of taxation is enough for you crooks !                                                                                                                                                                |
    | **`pcc_eng_25_044.3676_x0702147_21:15-18-19`** | In the area of blogging and site- building , at times it feels like nothing is definitely __`ever enough`__ .                                                                                                                                                    |
    | **`pcc_eng_11_085.3045_x1364599_50:48-50-51`** | Over the next few weeks , my little sister and I struggled to find closure by trying to remember him , getting a memorial tattoo , making a wreath for his grave on Memorial Day , using his t-shirts to make a quilt , but it 's not really __`ever enough`__ . |
    | **`pcc_eng_20_003.7190_x0043610_11:1-6-7`**    | Nothing in this world is __`ever enough`__ , nothing satisfies .                                                                                                                                                                                                 |
    | **`pcc_eng_01_104.9836_x1680364_21:3-4-5`**    | Knowledge is rarely __`ever enough`__ to spark change .                                                                                                                                                                                                          |
    
    
    4. _ever certain_
    
    |                                                | `token_str`                                                                                                                                                  |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_049.9734_x0790558_113:3-5-6`**   | Indeed , nothing is __`ever certain`__ in a world where gods and humans live and work together , especially when they often struggle to get along .          |
    | **`pcc_eng_07_028.5075_x0444899_07:16-18-19`** | It is highly expected that it will clear the House and Senate , but then nothing is __`ever certain`__ .                                                     |
    | **`pcc_eng_00_030.4322_x0475695_70:25-27-28`** | This means that we should do all that we can to be prepared , even if we are not certain it will happen ( nothing is __`ever certain`__ ) .                  |
    | **`pcc_eng_20_009.0011_x0129103_26:23-25-26`** | Advancing any view or judgement is a no-no in the evidence - based research sphere , founded on the cardinal acceptance that nothing is __`ever certain`__ . |
    | **`pcc_eng_25_036.4378_x0573667_12:3-4-5`**    | I was n't __`ever certain`__ I knew where she was in time and space or to whom she was speaking .                                                            |
    
    
    5. _ever wrong_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                 |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_098.6038_x1579993_17:1-5-6`**     | Nothing you want is __`ever wrong`__ .                                                                                                                                                                                                      |
    | **`pcc_eng_03_084.5045_x1352207_13:34-36-37`**  | He does n't know everybody 's always going around all the time with something wrong and believing they 're exerting great willpower and control to keep other people , for whom they think nothing 's __`ever wrong`__ , from seeing it . " |
    | **`pcc_eng_02_030.2370_x0473343_166:22-23-24`** | Whether he makes a decision to lower his pads or juke the defender , his call in those split-second situations is rarely __`ever wrong`__ and has probably contributed to his durability since he usually avoids the big hit .              |
    | **`pcc_eng_04_056.5900_x0897805_118:12-14-15`** | the kind of fixed that tries to make things look like nothing was __`ever wrong`__ .                                                                                                                                                        |
    | **`pcc_eng_17_046.7373_x0738942_7:08-10-11`**   | According to Page Six -- which is never , __`ever wrong`__ about sports personalities -- Benitez is moving out of their mansion because Seikaly is " partying too hard . "                                                                  |
    
    
    6. _ever black_
    
    |                                                | `token_str`                                                                                                                                           |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_104.5460_x1675091_08:18-20-21`** | If I 've learnt anything in my twenty six years on the planet , it 's that nothing is __`ever black`__ and white ; there 's infinite shades of grey . |
    | **`pcc_eng_14_006.5119_x0089232_18:6-8-9`**    | Dealing with Grey Areas -- nothing is __`ever black`__ and white , and that cannot be truer when referring to people 's workplace habits .            |
    | **`pcc_eng_02_007.9015_x0111391_26:11-13-14`** | No one type is better than the other , and nothing is __`ever black`__ and white .                                                                    |
    | **`pcc_eng_14_081.2960_x1298217_26:14-16-17`** | And that 's good , since , when it comes to color , nothing is __`ever black`__ and white ( sorry ) .                                                 |
    | **`pcc_eng_04_001.0397_x0000636_76:3-4-5`**    | Life is hardly __`ever black`__ and white .                                                                                                           |
    
    
    7. _ever right_
    
    |                                                 | `token_str`                                                                                                                                                              |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_044.8053_x0707647_04:1-7-8`**     | Nothing I say or do is __`ever right`__ .                                                                                                                                |
    | **`pcc_eng_14_005.0123_x0065026_065:08-09-10`** | Just like I believed that mom was never __`ever right`__ or any fun at all -- she was always five fucking hundred million miles away .                                   |
    | **`pcc_eng_12_089.0018_x1422001_25:19-20-21`**  | The real paradox here is that we presume we are repairing a damaged system , yet it was never __`ever right`__ from the minute of its creation in 1776 .                 |
    | **`pcc_eng_17_044.2931_x0699167_10:14-18-19`**  | Recently , the overseer is awfully hard on Joseph , and thinks that nothing he does is __`ever right`__ , even when he works hard all day long and obeys every command . |
    | **`pcc_eng_04_101.6615_x1626258_19:16-20-21`**  | And when she 's down , she believes everyone to be against her and that nothing she does is __`ever right`__ .                                                           |
    
    
    8. _ever larger_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                      |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_086.5230_x1381729_45:30-31-32`**  | Because it is clear that a huge part of Croatian civil society ( the one , for example , protesting after the condemnation of Gen. Gotovina ) it is not exactly welcoming the recent engagement of Croatian government in the international relations panorama . |
    | **`pcc_eng_24_025.3133_x0393081_127:22-23-24`** | I have n't seen it , but it seems to have one of the strangest endings I 've heard about , not exactly logical .                                                                                                                                                 |
    | **`pcc_eng_00_005.3121_x0069634_04:37-38-39`**  | Wool the percentage of silk is much lower , to the touch and the eyesight these two yarns are very similar , soft but not exactly " silky " and shiny , maybe more rustic and not exactly brilliant .                                                            |
    | **`pcc_eng_10_021.0029_x0323207_191:13-14-15`** | The downside is we moved away from our families and we 're not that close to them now .                                                                                                                                                                          |
    | **`apw_eng_20090116_0100_2:5-7-8`**             | the games themselves were n't all that great , but the promise was there .                                                                                                                                                                                       |
    
    
    9. _ever boring_
    
    |                                                 | `token_str`                                                                                                 |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_082.7008_x1322278_078:17-18-19`** | I liked the slow burn of the story , which takes it 's time but is n't __`ever boring`__ ( like you say ) . |
    | **`pcc_eng_27_064.0342_x1018997_06:6-8-9`**     | Above all , it was never , __`ever boring`__ .                                                              |
    | **`pcc_eng_25_013.0080_x0194233_49:2-4-5`**     | Was n't it __`ever boring`__ to play the same five concertos for three years ?                              |
    | **`pcc_eng_29_049.7412_x0787069_15:3-5-6`**     | It 's never , __`ever boring`__ and you never know what to expect .                                         |
    | **`pcc_eng_21_072.9895_x1163469_11:09-10-11`**  | The novel is a quick read and is n't __`ever boring`__ .                                                    |
    
    
    10. _ever easy_
    
    |                                              | `token_str`                                                                                                                                                       |
    |:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_054.3469_x0863947_27:1-3-4`**  | Nothing is __`ever easy`__ !                                                                                                                                      |
    | **`pcc_eng_26_095.5226_x1528574_093:1-3-4`** | Nothing 's __`ever easy`__ .                                                                                                                                      |
    | **`pcc_eng_13_096.6026_x1544973_33:1-7-8`**  | Nothing worth doing in life is __`ever easy`__ .                                                                                                                  |
    | **`pcc_eng_14_033.9461_x0532243_053:3-4-5`** | It is n't __`ever easy`__ , but I 'm learning to let the creativity win and relax on striving in my art , in whatever form it happens , to be perfect .           |
    | **`pcc_eng_07_015.8073_x0239713_09:2-4-5`**  | But nothing is __`ever easy`__ for accident- prone Jory -- and before she knows it , her Summer of Passion falls apart faster than the delivery van she crashes . |
    
    
    11. _ever good_
    
    |                                                 | `token_str`                                                                                                                                                 |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_032.4022_x0508321_344:10-14-15`** | The partner of this man comes to feel that nothing she does is __`ever good`__ enough and that it is impossible to make him happy .                         |
    | **`pcc_eng_19_029.2431_x0455919_37:08-11-12`**  | Nothing good ever comes easy , and nothing easy is __`ever good`__ .                                                                                        |
    | **`pcc_eng_01_093.4349_x1494649_31:1-5-6`**     | Nothing they do is __`ever good`__ enough , and she 's certainly never supportive of their goals .                                                          |
    | **`pcc_eng_06_106.9825_x1714475_265:08-09-10`** | Not the stupid little brother who was n't __`ever good`__ enough . "                                                                                        |
    | **`pcc_eng_23_087.1492_x1392403_24:25-26-27`**  | Lots of people we realize was happy to make an informed choice about their steroid apply , but some get information elsewhere and its not __`ever good`__ . |
    
    
    12. _ever greater_
    
    |                                                 | `token_str`                                                                                                                                                                                                                            |
    |:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_06_078.8236_x1258476_018:11-12-13`** | You 'll get one for a little less , is n't that great ?                                                                                                                                                                                |
    | **`apw_eng_19981202_0516_3:09-10-11`**          | details about the suspect or his detention were not immediately available .                                                                                                                                                            |
    | **`pcc_eng_20_085.8674_x1371182_57:35-36-37`**  | The social and political structures and the expectations for people - of course as far as we understand them - were so different in pre-industrial , pre-capitalist , aristocratic societies that modern terms are not that relevant . |
    | **`pcc_eng_18_085.8467_x1373888_03:20-21-22`**  | Putt will prepare to pull up roots for the next phase of her life -- even if she 's not yet sure what parts of her high school experience she 'll bring with her .                                                                     |
    | **`pcc_eng_06_023.0668_x0357122_21:08-09-10`**  | General manager Ryan Grigson said he was not yet certain how the rest of the coaching duties would be split up , though he expected all of the assistants to pitch in .                                                                |
    
    
    13. _ever closer_
    
    |                                                | `token_str`                                                                                                                                                                                                                  |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_003.1173_x0034143_07:18-20-21`** | I 've eaten there a few times and the food is always great , but I 've never been that impressed with the beer they have brewed in house .                                                                                   |
    | **`pcc_eng_14_031.3349_x0490203_33:08-09-10`** | Although the Super Fruit Mud Mask is n't that pleasant to use , and quite messy to remove too , I loved the results .                                                                                                        |
    | **`apw_eng_20020321_1543_9:17-18-19`**         | February revenue figures for casinos in Nevada , home to Las Vegas and Reno , are not yet available , but that state 's gambling halls had their worst month in 20 years in January .                                        |
    | **`pcc_eng_25_086.3400_x1381149_08:3-4-5`**    | It is not exactly clear if the home of the candidate and that of the spouse are one and the same or whether the two maintain separate residences , however , for reasons hereinafter stated the outcome should be the same . |
    | **`pcc_eng_test_1.5415_x08683_016:08-09-10`**  | Three kinds of creation there , is n't that nice ?                                                                                                                                                                           |
    
    
    14. _ever able_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20061215_0054_40:20-22-23`**         | both finished well below expectations in the Iowa caucus , the first nominating event of the season , and neither was __`ever able`__ to recover .                                                                                                                                                                                                                                                                                                                       |
    | **`pcc_eng_24_025.9371_x0403126_59:81-82-83`**  | The last " solution " to the world 's " shitholes " is the passive one that 's been employed since time immemorial , and that 's migrants sacrificing their living standards by knowingly accepting that they 'll likely spend the rest of their lives in suboptimal social conditions in order to give their descendants that are born there a " better chance " at " climbing the ladder ' and " succeeding " in ways that their parents were n't __`ever able`__ to . |
    | **`pcc_eng_20_086.8393_x1386806_086:11-12-13`** | The law was like a teacher to prove we are not __`ever able`__ to meet God 's righteous requirements . "                                                                                                                                                                                                                                                                                                                                                                 |
    | **`pcc_eng_09_033.9889_x0534089_22:26-29-30`**  | I had the Hoth playset when I was little and loved playing with it , but I could never remember exactly what it was called nor was I __`ever able`__ to find info about it ( apparently my Google skills need work ) .                                                                                                                                                                                                                                                   |
    | **`pcc_eng_10_047.5556_x0753258_094:10-11-12`** | I used to lament to him how I was n't __`ever able`__ to go back to Yankee Stadium after Thurman 's death .                                                                                                                                                                                                                                                                                                                                                              |
    
    
    15. _ever higher_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                               |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_test_3.03548_x40106_100:3-4-5`**     | I was n't that keen on using it to begin with , but one of my friends kept pushing me to get on it and now I enjoy it .                                                                                                                                   |
    | **`pcc_eng_20_007.5723_x0105930_10:39-40-41`**  | Though by most accounts his methods were brutal and sadistic ( for example , slowly impaling his enemies on stakes , drawing and quartering them , burning them to death , etc. ) , in reality they were not particularly cruel or unusual for the time . |
    | **`pcc_eng_02_008.7860_x0125636_151:20-21-22`** | Next , even though I can certainly notice the jumps in reasoning you come up with , I am not necessarily certain of just how you seem to unite your details that produce your conclusion .                                                                |
    | **`pcc_eng_15_014.7269_x0221554_097:12-13-14`** | A few months ago I made a donation that just was n't that efficient .                                                                                                                                                                                     |
    | **`nyt_eng_20071028_0124_48:08-09-10`**         | having realized that obtaining viewer-created content is not that easy , Current is positioning the television network as an incentive for online participation .                                                                                         |
    
    
    16. _ever deeper_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                 |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_006.2279_x0084646_074:11-13-14`** | pull my trigger bang every time you miss I do not deep __`ever deeper`__ inside my finger always strikes does n't lie I know about hiding living in the shadows breaking with the glass every moment getting way too close spending my time getting lost going deep in the darkness keep my secrets never forget No regrets |
    
    
    17. _ever mindful_
    
    |                                                | `token_str`                                                                                                                                                            |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_11_066.1557_x1054572_71:3-4-5`**    | It is n't that awful , really .                                                                                                                                        |
    | **`pcc_eng_06_073.4511_x1171981_07:13-14-15`** | Duty free is rather a misnomer nowadays as the goods there are seldom any cheaper than may find in a good department store at home .                                   |
    | **`pcc_eng_21_077.9337_x1243205_02:3-4-5`**    | I 'm not exactly sure what you 're asking .                                                                                                                            |
    | **`pcc_eng_27_053.3513_x0846150_5:32-34-35`**  | The team does n't yet know when Cobbs will be able to return - whether it will only take a few days to heal or longer - so the situation is n't yet necessarily dire . |
    | **`pcc_eng_25_037.3608_x0588540_50:09-10-11`** | Mail is annoying to me , but really not that important in the scheme of things                                                                                         |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/...
    
    Samples saved as...
    1. `neg_bigram_examples/ever/ever_perfect_99ex.csv`
    1. `neg_bigram_examples/ever/ever_simple_99ex.csv`
    1. `neg_bigram_examples/ever/ever_enough_99ex.csv`
    1. `neg_bigram_examples/ever/ever_certain_99ex.csv`
    1. `neg_bigram_examples/ever/ever_wrong_99ex.csv`
    1. `neg_bigram_examples/ever/ever_black_99ex.csv`
    1. `neg_bigram_examples/ever/ever_right_99ex.csv`
    1. `neg_bigram_examples/ever/ever_larger_99ex.csv`
    1. `neg_bigram_examples/ever/ever_boring_99ex.csv`
    1. `neg_bigram_examples/ever/ever_easy_99ex.csv`
    1. `neg_bigram_examples/ever/ever_good_99ex.csv`
    1. `neg_bigram_examples/ever/ever_greater_99ex.csv`
    1. `neg_bigram_examples/ever/ever_closer_99ex.csv`
    1. `neg_bigram_examples/ever/ever_able_99ex.csv`
    1. `neg_bigram_examples/ever/ever_higher_99ex.csv`
    1. `neg_bigram_examples/ever/ever_deeper_99ex.csv`
    1. `neg_bigram_examples/ever/ever_mindful_99ex.csv`
    
    ## 9. *particularly*
    
    |                             |       `N` |      `f1` |   `adv_total` |
    |:----------------------------|----------:|----------:|--------------:|
    | **NEGMIR_particularly**     |   583,470 |   291,732 |        10,029 |
    | **COMPLEMENT_particularly** | 6,347,364 | 3,173,552 |        76,162 |
    | **NEGATED_particularly**    | 6,347,364 | 3,173,660 |        76,162 |
    
    
    |                                     |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:------------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~particularly_religious**   |   485 |    4.52 |    0.50 |    0.00 |   659.41 |    486 |    243.00 |      242.00 |         3,507 |
    | **NEGmir~particularly_new**         |   404 |    4.35 |    0.50 |    0.00 |   547.73 |    405 |    202.50 |      201.50 |         4,300 |
    | **NEGany~particularly_wrong**       |   218 |    3.56 |    0.50 |    0.00 |   302.22 |    218 |    109.00 |      109.00 |        21,332 |
    | **NEGmir~particularly_wrong**       |   212 |    3.39 |    0.50 |    0.00 |   282.64 |    213 |    106.50 |      105.50 |         8,506 |
    | **NEGmir~particularly_surprising**  |   166 |    3.27 |    0.50 |    0.00 |   230.18 |    166 |     83.00 |       83.00 |         1,248 |
    | **COM~particularly_acute**          |   135 |    2.84 |    0.50 |    0.00 |   187.16 |    135 |     67.50 |       67.50 |         1,038 |
    | **NEGany~particularly_athletic**    |   108 |    2.49 |    0.50 |    0.00 |   149.72 |    108 |     54.00 |       54.00 |         1,772 |
    | **NEGany~particularly_likeable**    |   106 |    2.46 |    0.50 |    0.00 |   146.95 |    106 |     53.00 |       53.00 |           861 |
    | **NEGmir~particularly_original**    |    90 |    2.33 |    0.50 |    0.00 |   124.78 |     90 |     45.00 |       45.00 |           715 |
    | **NEGany~particularly_radical**     |    79 |    1.99 |    0.50 |    0.00 |   109.52 |     79 |     39.50 |       39.50 |         2,637 |
    | **NEGmir~particularly_novel**       |    54 |    1.50 |    0.50 |    0.00 |    74.87 |     54 |     27.00 |       27.00 |           179 |
    | **NEGmir~particularly_religious**   |    53 |    1.47 |    0.50 |    0.00 |    73.48 |     53 |     26.50 |       26.50 |           337 |
    | **NEGany~particularly_flashy**      |    57 |    1.46 |    0.50 |    0.00 |    79.02 |     57 |     28.50 |       28.50 |         1,732 |
    | **NEGmir~particularly_innovative**  |    47 |    1.26 |    0.50 |    0.00 |    65.16 |     47 |     23.50 |       23.50 |           675 |
    | **NEGmir~particularly_comfortable** |    44 |    1.15 |    0.50 |    0.00 |    61.00 |     44 |     22.00 |       22.00 |         1,888 |
    | **NEGany~particularly_new**         |   747 |    4.61 |    0.49 |    0.00 |   982.49 |    752 |    376.00 |      371.00 |        21,538 |
    | **NEGany~particularly_original**    |   360 |    3.64 |    0.49 |    0.00 |   460.59 |    364 |    182.00 |      178.00 |         4,693 |
    | **NEGmir~particularly_unusual**     |   170 |    2.72 |    0.48 |    0.00 |   209.60 |    173 |     86.50 |       83.50 |           933 |
    | **NEGany~particularly_surprising**  | 1,069 |    3.93 |    0.47 |    0.00 | 1,260.26 |  1,097 |    548.50 |      520.50 |        18,776 |
    | **NEGmir~particularly_good**        |   390 |    3.24 |    0.47 |    0.00 |   455.35 |    401 |    200.50 |      189.50 |        13,423 |
    
    
    1. _particularly surprising_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                 |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_08_079.5631_x1272160_27:3-4-5`**    | It is not __`particularly surprising`__ that Sessions , along with other members of the Republican party who sat on the Senate Environmental and Public Works Committee Hearing on Monday , attempted to challenge the science of man-made climate change . |
    | **`pcc_eng_20_083.3349_x1330355_03:14-15-16`** | Senate Majority Leader Mitch Mc Connell told Fox News he had learned " nothing __`particularly surprising`__ , " but declined to go into detail .                                                                                                           |
    | **`pcc_eng_06_079.6601_x1271895_04:5-6-7`**    | So , it 's not __`particularly surprising`__ that when I came across this infographic on Fast Co. Design comparing the cost of ivy league higher education and incarceration , I took pause .                                                               |
    | **`pcc_eng_26_088.7240_x1418621_21:4-5-6`**    | This really is n't __`particularly surprising`__ , the problem has never been language until it was used as a weapon .                                                                                                                                      |
    | **`pcc_eng_12_085.2809_x1361838_06:24-25-26`** | Given that Trump 's entire campaign can seen as an endorsement of racism , xenophobia , and general bigotry , this was also not __`particularly surprising`__ .                                                                                             |
    
    
    2. _particularly original_
    
    |                                                 | `token_str`                                                                                                                                                                  |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_19971217_0791_3:3-4-5`**             | there 's nothing __`particularly original`__ about the subject , a television perennial , but the program has its moments via the hidden camera .                            |
    | **`pcc_eng_28_020.4107_x0313816_11:5-6-7`**     | Though his words were n't __`particularly original`__ or poetic , they still reverberated through me .                                                                       |
    | **`nyt_eng_19990209_0064_32:6-7-8`**            | so these characters that are n't __`particularly original`__ plod through the book doing things that also are n't __`particularly original`__ and definitely are n't funny . |
    | **`pcc_eng_11_094.7945_x1518423_258:17-18-19`** | RB : You suggest that Kaczynski 's thinking -- which you characterize as mediocre -- is not __`particularly original`__ .                                                    |
    | **`pcc_eng_13_002.1320_x0018182_32:7-8-9`**     | " This is pretty cool but not __`particularly original`__ .                                                                                                                  |
    
    
    3. _particularly novel_
    
    |                                                | `token_str`                                                                                                                                                   |
    |:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20000602_0053_10:3-4-5`**           | there is nothing __`particularly novel`__ about that .                                                                                                        |
    | **`pcc_eng_17_104.7004_x1676346_31:10-11-12`** | Sadly , the plot in A Dirty Carnival is not __`particularly novel`__ , at least not worthy of a remake .                                                      |
    | **`pcc_eng_23_006.9388_x0095981_05:11-13-14`** | Setting a game in the theatre of modern war may not be __`particularly novel`__ anymore , but for EA 's long-running Medal of Honor franchise it 's a first . |
    | **`pcc_eng_00_064.3182_x1023716_003:1-2-3`**   | Nothing __`particularly novel`__ about this porno scene -- it 's a standard - issue boy-girl vignette .                                                       |
    | **`pcc_eng_18_088.4356_x1415955_520:1-6-7`**   | Nothing the authors say is __`particularly novel`__ or earth- shattering , which is part of its brilliance .                                                  |
    
    
    4. _particularly religious_
    
    |                                              | `token_str`                                                                                                                                                                                                                                                                                          |
    |:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_013.9788_x0209418_46:3-4-5`**  | There 's nothing __`particularly religious`__ about the film .                                                                                                                                                                                                                                       |
    | **`nyt_eng_20070501_0188_35:4-6-7`**         | his parents had not been __`particularly religious`__ , he said , a pattern typical among Pakistani immigrants to Britain where the new generation , often turned off by what they see as the loose morals of binge drinking and broken marriages , has proven to be more devout than their elders . |
    | **`pcc_eng_02_086.8430_x1387869_28:1-5-6`**  | Not because I am __`particularly religious`__ , but those stories help him understand that being compasionate is actually something to value .                                                                                                                                                       |
    | **`pcc_eng_18_005.5493_x0073752_25:7-8-9`**  | Whilst many of the members are n't __`particularly religious`__ , all feel strongly affiliated to their Jewish roots and find that they have an instant connection to other Jewish lesbians .                                                                                                        |
    | **`pcc_eng_20_006.0688_x0081621_007:7-8-9`** | The first is that I am not __`particularly religious`__ .                                                                                                                                                                                                                                            |
    
    
    5. _particularly innovative_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                   |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20070611_0101_44:3-4-5`**            | there 's nothing __`particularly innovative`__ about this new drama , but Treat Williams is always , well , a treat .                                                                                                                                         |
    | **`pcc_eng_11_081.8802_x1309098_70:08-09-10`**  | The core of Shadow of Mordor is n't __`particularly innovative`__ , but its improvements on well - worn ideas , combined with a system that gives an initially unremarkable world life , makes it one of the most memorable gaming experiences you can have . |
    | **`pcc_eng_19_012.9580_x0193242_34:5-6-7`**     | The overarching narrative is not __`particularly innovative`__ in content , but it smartly uses the constrained formats to tell a human story through screens , knobs , and disembodied voices .                                                              |
    | **`pcc_eng_13_003.1290_x0034158_134:7-8-9`**    | The look of the show is not __`particularly innovative`__ , in fact it looks like many sci-fi thrillers , but overall it still nice .                                                                                                                         |
    | **`pcc_eng_15_049.0413_x0776660_054:14-15-16`** | Microsoft spends billions on research and development , yet is widely regarded as not __`particularly innovative`__ .                                                                                                                                         |
    
    
    6. _particularly comfortable_
    
    |                                                | `token_str`                                                                                                                                                                                                                               |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_07_053.9963_x0856607_34:22-23-24`** | " When I look at the Republican Party these days and who the quote ' leaders ' are , I 'm not __`particularly comfortable`__ that they 're reflecting the values of conservatives , " Santorum said in a recent interview with ABC News . |
    | **`pcc_eng_22_010.0520_x0145936_18:5-6-7`**    | However , I was not __`particularly comfortable`__ with our internal capabilities to conduct a major investigation .                                                                                                                      |
    | **`nyt_eng_20071015_0013_8:4-5-6`**            | `` I 'm not __`particularly comfortable`__ in that setting , but whatever . ''                                                                                                                                                            |
    | **`nyt_eng_19961011_0079_29:4-5-6`**           | `` I 'm not __`particularly comfortable`__ getting companies listed in every corner of the globe , '' said Tina So , who manages about $ 24 million in China funds at Schroder Investment Management -LRB- Asia -RRB- Ltd. in Hong Kong . |
    | **`pcc_eng_23_003.3323_x0037537_3:3-4-5`**     | I am not __`particularly comfortable`__ in bars or clubs .                                                                                                                                                                                |
    
    
    7. _particularly acute_
    
    |                                                 | `token_str`                                                                                                                 |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_04_042.8683_x0676535_07:3-4-5`**     | That 's not exactly conducive toward getting promoted or receiving a decent raise , and you could get fired as a result .   |
    | **`apw_eng_19981222_0527_3:3-4-5`**             | it was not immediately clear exactly how many pensioners held shares in tickets for the winning number _ 21856 .            |
    | **`apw_eng_19981013_0209_7:7-8-9`**             | the status of future talks was not immediately clear .                                                                      |
    | **`pcc_eng_29_004.8880_x0062917_19:3-4-5`**     | It was not immediately clear whether those on the boat that capsized Wednesday were migrants fleeing their home countries . |
    | **`pcc_eng_03_083.4731_x1335597_193:12-13-14`** | As much as I do like appreciate Durian , these were n't that bad and I can totally see why every table orders them .        |
    
    
    8. _particularly wrong_
    
    |                                             | `token_str`                                                                                                                                                                                    |
    |:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_052.0589_x0824923_09:4-5-6`** | While there 's nothing __`particularly wrong`__ with a brochure site , there 's the possibility for so much more .                                                                             |
    | **`pcc_eng_27_023.2748_x0360107_03:4-5-6`** | While there is nothing __`particularly wrong`__ with this format , some might consider that another format is better suited for what they require .                                            |
    | **`pcc_eng_12_063.1209_x1004463_07:3-4-5`** | There 's nothing __`particularly wrong`__ with writing a story about monsters where the monsters are analogies for the fears and worries we have about growing up .                            |
    | **`pcc_eng_13_087.3289_x1395305_34:3-4-5`** | There 's nothing __`particularly wrong`__ with him but you 'd expect a team like Chelsea to lock up their fourth-choice central midfielder before Deadline Day and perhaps at a better price . |
    | **`pcc_eng_06_029.6283_x0463180_09:3-4-5`** | There 's nothing __`particularly wrong`__ with this line of reasoning but there may be a subtle reason why it 's unlikely to be successful ( apart from the ordinary reasons ) .               |
    
    
    9. _particularly athletic_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                         |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_031.8316_x0499044_2:2-3-4`**      | Although not __`particularly athletic`__ at a young age , his parents signed him up for all sorts of physical activities , such as swimming , running track , sambo and even a little bit of gymnastics .                                                           |
    | **`pcc_eng_03_040.1517_x0634339_43:6-8-9`**     | Mental Note : I 've never been __`particularly athletic`__ , but come on .                                                                                                                                                                                          |
    | **`pcc_eng_12_067.8447_x1080213_202:6-7-8`**    | Hes 6 - 7 , not __`particularly athletic`__ , and has just an average skill - set offensively as far as his position in the NBA is concerned .                                                                                                                      |
    | **`pcc_eng_19_074.6295_x1189468_076:28-29-30`** | Gomez has a plus arm and third base and his hands are fine for the position , but he 's already a large human being and is n't __`particularly athletic`__ , so he will have to improve his footwork and agility to stick at third and avoid a move to first base . |
    | **`pcc_eng_13_007.6438_x0107241_008:6-7-8`**    | Shanahan , 50 , and not __`particularly athletic`__ , easily handled the hikes .                                                                                                                                                                                    |
    
    
    10. _particularly likeable_
    
    |                                                | `token_str`                                                                                                                                                                                                                    |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_14_082.3593_x1315203_21:11-12-13`** | However , that said as their partners and friends were not __`particularly likeable`__ either it was at times hard to really care .                                                                                            |
    | **`pcc_eng_13_001.4499_x0007177_25:26-27-28`** | The main character -- here , Andrea , a 40 - something single woman struggling with meaning and alcohol in New York - - is not __`particularly likeable`__ , though her actions are understandable and generally sympathetic . |
    | **`pcc_eng_04_101.2489_x1619564_146:2-3-4`**   | Characters not __`particularly likeable`__ or sympathetic , plot non-existent , too many and not very interesting or clever jewish jokes .                                                                                     |
    | **`pcc_eng_18_033.1710_x0520799_057:4-5-6`**   | Both characters are n't __`particularly likeable`__ , but the actors playing them are so it certainly supports Fellini and Woody Allen 's ideas that casting was more than half the battle when making a film .                |
    | **`pcc_eng_21_025.4152_x0394502_31:6-7-8`**    | Most of the characters are n't __`particularly likeable`__ , but they are n't ones you despise either .                                                                                                                        |
    
    
    11. _particularly radical_
    
    |                                                 | `token_str`                                                                                                                                                                                                      |
    |:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_01_099.3235_x1589505_12:3-4-5`**     | There 's nothing __`particularly radical`__ about these statistics .                                                                                                                                             |
    | **`pcc_eng_22_004.1462_x0051002_132:3-4-5`**    | Even a not __`particularly radical`__ report last year from the home affairs select committee , recommending reform and the possibility of decriminalising cannabis , was speedily dismissed by the government . |
    | **`pcc_eng_12_088.8555_x1419625_070:08-09-10`** | Although Russolo 's music and instruments were not __`particularly radical`__ , later interest in the musical potential of noise owed much to his pioneering work .                                              |
    | **`pcc_eng_02_032.5647_x0510895_07:1-3-4`**     | None are __`particularly radical`__ ; indeed , each idea simply develops programs and policies decided on by earlier FCC administrations , some of them Republican .                                             |
    | **`pcc_eng_05_085.4864_x1367191_29:4-5-6`**     | The story does nothing __`particularly radical`__ with the incarnations of the various characters but winds them together with a modest complexity .                                                             |
    
    
    12. _particularly flashy_
    
    |                                                 | `token_str`                                                                                                                                       |
    |:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_20_033.6695_x0528216_105:22-23-24`** | Karabacek 's offensive game is more north - south than east-west , which works well for the scoring winger who is not __`particularly flashy`__ . |
    | **`pcc_eng_01_068.1664_x1086406_55:09-10-11`**  | Part of it may be that he is n't __`particularly flashy`__ or out spoken .                                                                        |
    | **`pcc_eng_25_009.8563_x0143428_06:3-4-5`**     | He 's not __`particularly flashy`__ , but has a combination of skill and intelligence that should lead to a long and successful NFL career .      |
    | **`pcc_eng_09_083.8691_x1340636_054:6-7-8`**    | The pas de deux is not __`particularly flashy`__ to watch , but it 's not supposed to be - it 's supposed to be heartbreaking and beautiful .     |
    | **`pcc_eng_02_006.2338_x0084607_09:17-18-19`**  | In this chapter , we explore Calendar and Contacts , a pair of apps that are n't __`particularly flashy`__ but can be remarkably useful .         |
    
    
    13. _particularly new_
    
    |                                                | `token_str`                                                                                                              |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_19_047.4430_x0749645_12:3-4-5`**    | No , not __`particularly new`__ , but still worth saying                                                                 |
    | **`pcc_eng_24_078.3478_x1251109_22:12-13-14`** | This shortsighted , bury your head in the sand attitude is not __`particularly new`__ .                                  |
    | **`pcc_eng_22_056.7264_x0900503_29:3-4-5`**    | There is nothing __`particularly new`__ about the proposed legislation , nor the timing of its intended implementation . |
    | **`pcc_eng_18_017.1544_x0261701_10:08-09-10`** | Here the argument was that cybercrime is nothing __`particularly new`__ :                                                |
    | **`pcc_eng_22_060.9413_x0969101_257:3-4-5`**   | There 's nothing __`particularly new`__ about their movement , except that perhaps they are exceptionally rude .         |
    
    
    14. _particularly unusual_
    
    |                                                 | `token_str`                                                                                                                                                                                     |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_17_076.5539_x1221113_26:12-13-14`**  | But others saw something different : a mushy post that said nothing __`particularly unusual`__ about what it 's like to be in love with someone , but was nonetheless being held up as heroic . |
    | **`pcc_eng_10_027.9279_x0435182_36:11-12-13`**  | That up there might look like some very cool but not __`particularly unusual`__ street art .                                                                                                    |
    | **`nyt_eng_20050725_0007_6:3-4-5`**             | there is nothing __`particularly unusual`__ about a conservative Republican gravitating to evangelical Christianity , though given his record , his critics were skeptical .                    |
    | **`pcc_eng_11_068.4512_x1091839_08:4-5-6`**     | So it 's not __`particularly unusual`__ to have two carriers in the Cent Com area of responsibility , " said Army Lt. Gen. Carter F. Ham , the Joint Chiefs of Staff director for operations .  |
    | **`pcc_eng_00_069.2237_x1102570_121:16-17-18`** | But I 've met a lot of smart writers in Hollywood , so that 's not __`particularly unusual`__ .                                                                                                 |
    
    
    15. _particularly good_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                            |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_03_031.8192_x0499221_09:26-28-29`** | Except for some positives in employment , such as monthly hiring in April and the very low unemployment claims , the economic news recently has n't been __`particularly good`__ , and it seems to be affecting consumer sentiment .                                                   |
    | **`pcc_eng_10_025.5336_x0396356_21:25-26-27`** | According to the Hagberg Consulting Group , which develops training programs for the high tech industry , IT professionals are , generally speaking , not __`particularly good`__ at managing people .                                                                                 |
    | **`pcc_eng_28_039.0744_x0615776_26:4-5-6`**    | The optics are n't __`particularly good`__ , so I do n't care about it enough to take it to a professional service place .                                                                                                                                                             |
    | **`pcc_eng_17_042.2922_x0666971_12:25-26-27`** | It is also apparent how rapidly the remaining boxes are disappearing , and examination of the images does suggest that the all-wooden boxes were not __`particularly good`__ in terms of their dimensional stability , many showing signs of sagging or twisting before their demise . |
    | **`pcc_eng_16_075.2189_x1201055_007:1-6-7`**   | None of these performers were __`particularly good`__ or bad , with the notable exception of the James Franco / Anne Hathaway disaster of last year .                                                                                                                                  |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/...
    
    Samples saved as...
    1. `neg_bigram_examples/particularly/particularly_surprising_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_original_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_novel_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_religious_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_innovative_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_comfortable_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_acute_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_wrong_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_athletic_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_likeable_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_radical_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_flashy_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_new_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_unusual_99ex.csv`
    1. `neg_bigram_examples/particularly/particularly_good_99ex.csv`
    
    ## 10. *terribly*
    
    |                      |       `N` |      `f1` |   `adv_total` |
    |:---------------------|----------:|----------:|--------------:|
    | **NEGATED_terribly** | 6,347,364 | 3,173,660 |        19,802 |
    | **NEGMIR_terribly**  |   583,470 |   291,732 |         2,204 |
    | **POSMIR_terribly**  |   583,470 |   291,729 |         2,204 |
    
    
    |                                 |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:--------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~terribly_surprising**  |   949 |    5.73 |    0.50 |    0.00 | 1,315.75 |    949 |    474.50 |      474.50 |        18,776 |
    | **NEGany~terribly_popular**     |   149 |    2.99 |    0.50 |    0.00 |   206.56 |    149 |     74.50 |       74.50 |        51,120 |
    | **NEGany~terribly_unusual**     |   146 |    2.96 |    0.50 |    0.00 |   202.40 |    146 |     73.00 |       73.00 |         7,412 |
    | **NEGany~terribly_comfortable** |   129 |    2.77 |    0.50 |    0.00 |   178.84 |    129 |     64.50 |       64.50 |        23,908 |
    | **NEGany~terribly_bright**      |   117 |    2.61 |    0.50 |    0.00 |   162.20 |    117 |     58.50 |       58.50 |         8,623 |
    | **NEGany~terribly_common**      |   105 |    2.45 |    0.50 |    0.00 |   145.56 |    105 |     52.50 |       52.50 |        34,450 |
    | **NEGmir~terribly_surprising**  |    67 |    1.85 |    0.50 |    0.00 |    92.89 |     67 |     33.50 |       33.50 |         1,248 |
    | **NEGmir~terribly_original**    |    45 |    1.19 |    0.50 |    0.00 |    62.39 |     45 |     22.50 |       22.50 |           715 |
    | **NEGany~terribly_interested**  |   486 |    3.98 |    0.49 |    0.00 |   624.89 |    491 |    245.50 |      240.50 |        34,543 |
    | **NEGany~terribly_different**   |   366 |    3.93 |    0.49 |    0.00 |   485.33 |    368 |    184.00 |      182.00 |        80,643 |
    | **NEGany~terribly_surprised**   |   287 |    3.30 |    0.49 |    0.00 |   361.19 |    291 |    145.50 |      141.50 |        10,157 |
    | **NEGmir~terribly_new**         |    69 |    1.64 |    0.49 |    0.00 |    86.57 |     70 |     35.00 |       34.00 |         4,300 |
    | **NEGany~terribly_exciting**    |   382 |    3.28 |    0.48 |    0.00 |   456.39 |    391 |    195.50 |      186.50 |        20,233 |
    | **NEGmir~terribly_interesting** |    56 |    1.29 |    0.48 |    0.00 |    68.96 |     57 |     28.50 |       27.50 |         3,863 |
    | **POS~terribly_wrong**          |   319 |    1.06 |    0.30 |    0.00 |   149.75 |    401 |    200.50 |      118.50 |         8,506 |
    
    
    1. _terribly surprising_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    |:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_087.4091_x1398683_164:1-6-7`**    | None of this should be __`terribly surprising`__ , since it is increasingly clear that Donald Trump , whose actual net worth is unclear , was completely comfortable making money from blatant fraud .                                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_21_019.6568_x0301268_044:21-23-24`** | Given CAFC 's history as exceptionally supportive of locking up knowledge and information on the patent side , it would n't be __`terribly surprising`__ if they did so as well on the copyright side ( side note : while , normally , copyright cases should travel up the local appeals court route , since this case started as a patent case , even though it ended up as a copyright case , apparently the appeal still goes to CAFC , the court that hears all patent appeals ) . |
    | **`pcc_eng_26_094.9685_x1519625_01:30-31-32`**  | In retrospect , it should have seemed like the perfect fit and by proxy something that we should have expected so really , the announcement of Scribblenauts while perhaps not __`terribly surprising`__ , is still nonetheless welcome .                                                                                                                                                                                                                                               |
    | **`pcc_eng_23_008.1875_x0116084_23:12-13-14`**  | The twists and turns are well marked in advance , so nothing __`terribly surprising`__ arises .                                                                                                                                                                                                                                                                                                                                                                                         |
    | **`pcc_eng_27_008.2473_x0116702_06:3-4-5`**     | It is n't __`terribly surprising`__ once you put some thought into it that two Yale Law professors seriously believe in something so dangerous as ethnic determinism .                                                                                                                                                                                                                                                                                                                  |
    
    
    2. _terribly original_
    
    |                                                  | `token_str`                                                                                                                                                                                         |
    |:-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_00_068.6102_x1092658_02:20-21-22`**   | Alice Blanchard drags the readers into the pit with A Breath After Drowning , a thriller that -- while not __`terribly original`__ -- is as close to perfect as it can get in this genre .          |
    | **`pcc_eng_24_108.09517_x1747258_143:08-09-10`** | Naschy 's penning of the screenplay was not __`terribly original`__ .                                                                                                                               |
    | **`pcc_eng_16_088.0325_x1408847_017:13-14-15`**  | In its place , a new identity would form that , while not __`terribly original`__ in the context of the times , was nonetheless a much truer vision of who he was .                                 |
    | **`nyt_eng_19970624_0673_11:19-20-21`**          | many of the dresses are expected to sell for about $ 15,000 , mostly because their designs were n't __`terribly original`__ .                                                                       |
    | **`pcc_eng_04_077.0921_x1229037_11:10-13-14`**   | That 's the key to appreciating this EP : nothing here is __`terribly original`__ , but it 's all executed with such panache and clean- cut expertise that it 's hard not to love it all the same . |
    
    
    3. _terribly popular_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                          |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`nyt_eng_20060708_0004_25:3-4-5`**           | she was not __`terribly popular`__ with fans .                                                                                                                                                                                                                                                                                       |
    | **`apw_eng_20090515_0433_22:30-31-32`**        | `` If you use inflammatory , populist language , '' Baker said in an interview , `` it 's best to use it on organizations or interests that are n't __`terribly popular`__ . ''                                                                                                                                                      |
    | **`pcc_eng_21_064.5497_x1026879_27:09-10-11`** | I hear that full- blown computer systems are n't __`terribly popular`__ as Valentine 's Day gifts or Easter egg stuffers this year .                                                                                                                                                                                                 |
    | **`nyt_eng_19970126_0249_27:23-24-25`**        | and as former Sen. Bob Dole can attest , it 's tough to make a case against an incumbent , even a not __`terribly popular`__ one , when voters feel they are better off than they were four years ago .                                                                                                                              |
    | **`pcc_eng_18_080.9888_x1295098_35:18-19-20`** | Admittedly the less delusional elements of the Labour party have just about accepted that their leader is not __`terribly popular`__ and that spurning the repeated chances to jettison the Jonah before the good ship Labour glug-glug-glugs into the deepest recesses of the ocean may not have been the wisest course of action . |
    
    
    4. _terribly unusual_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                      |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_088.5070_x1415033_10:16-17-18`** | Typically periods go on and off for a year or so , so it is n't __`terribly unusual`__ to get your period again -- as I recal that happened to me too and then they stopped altogether .                                                                         |
    | **`pcc_eng_23_084.4854_x1349214_250:4-5-6`**   | That actually was n't __`terribly unusual`__ back then since church services could be very long and older children could have seen to their younger brothers and sisters , " Hermione said .                                                                     |
    | **`pcc_eng_02_080.7292_x1289143_045:3-4-5`**   | It 's not __`terribly unusual`__ for two people with borderline traits to engage , and regardless of the psycho- babble you may have read elsewhere , anyone who 's done any worthwhile healing work with borderlines would know this !                          |
    | **`pcc_eng_07_051.0758_x0809516_18:22-24-25`** | The proceedings have the look and feel of a romantic comedy and the nearly twenty years separating Ruffalo and Knightley would n't be __`terribly unusual`__ for the genre , but the movie does n't take its broken - hearted artists down the path you expect . |
    | **`pcc_eng_12_036.4635_x0573649_13:18-19-20`** | The fact that the D block has had only one bid in the first four rounds is n't __`terribly unusual`__ ; several licenses which eventually went in Auction 66 for very substantial sums had very little early - round action .                                    |
    
    
    5. _terribly comfortable_
    
    |                                                | `token_str`                                                                                                                                                                                                                  |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_18_011.8867_x0176268_34:3-4-5`**    | I 'm not __`terribly comfortable`__ with this fact , this lesson I have learned about myself .                                                                                                                               |
    | **`pcc_eng_05_038.9833_x0614842_26:11-12-13`** | ... Clinton has acknowledged in the past that she is n't __`terribly comfortable`__ speaking in public and , therefore , should avoid doing it .                                                                             |
    | **`pcc_eng_19_017.6419_x0268452_05:1-2-3`**    | Not __`terribly comfortable`__ for the woman who regularly wears black polyester pants ( we 're getting close to laundry day here ) .                                                                                        |
    | **`pcc_eng_20_002.0393_x0016617_10:26-27-28`** | At the moment she 's scampering around behind me on the couch and trying to skootch her way up into my lap , a position not __`terribly comfortable`__ for me when hunching over my Mac on the coffee table in front of me . |
    | **`pcc_eng_21_098.9781_x1582907_052:6-7-8`**   | For the leader who is n't __`terribly comfortable`__ communicating , a monthly team meeting or weekly " stand - up " is usually all it takes to field questions and convey what is going on .                                |
    
    
    6. _terribly bright_
    
    |                                                 | `token_str`                                                                                                                                                                                                             |
    |:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_088.0198_x1406130_055:23-24-25`** | Ryan O'Neal was probably the perfect choice - Kubrick 's , of course - for the title role of an ambitious but not __`terribly bright`__ young Irishman .                                                                |
    | **`pcc_eng_02_086.8229_x1387551_59:1-2-3`**     | Not __`terribly bright`__ or brave , Jakob nonetheless blurts out his secret and then some to save a suicidal friend 's life .                                                                                          |
    | **`pcc_eng_16_077.6975_x1241212_075:36-37-38`** | In this animated film , a buffoonish lone astronaut ( voiced by Dwayne " The Rock " Johnson ) lands on a planet of green-skinned creatures that hunt him down because they 're paranoid and not __`terribly bright`__ . |
    | **`pcc_eng_27_064.1069_x1020130_5:08-09-10`**   | Mahlik is a good kid , though not __`terribly bright`__ .                                                                                                                                                               |
    | **`pcc_eng_21_076.8556_x1225847_45:3-5-6`**     | He 's not always __`terribly bright`__ , but he does his best .                                                                                                                                                         |
    
    
    7. _terribly common_
    
    |                                                | `token_str`                                                                                                                                                                                      |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_083.0861_x1327913_17:20-21-22`** | Photo Credit : [ Wine bottles have fairly narrow mouths , and because of that , spilling is actually not __`terribly common`__ .                                                                 |
    | **`pcc_eng_00_040.5015_x0638139_15:3-4-5`**    | It is not __`terribly common`__ to see this happening .                                                                                                                                          |
    | **`pcc_eng_18_002.6591_x0027045_3:17-19-20`**  | Of course , if you 're wandering through the woods , a can of soup may not be __`terribly common`__ , but you may find an empty can somewhere with one side still on that you can use for this . |
    | **`pcc_eng_20_039.0853_x0615552_27:13-14-15`** | Some of the crossover elements would need reworking , but they were n't __`terribly common`__ in that run anyway .                                                                               |
    | **`pcc_eng_12_081.5891_x1302091_25:12-13-14`** | Despite those unique benefits , beers fermented with Champagne yeast are n't __`terribly common`__ .                                                                                             |
    
    
    8. _terribly different_
    
    |                                                | `token_str`                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_23_031.2561_x0488445_20:30-31-32`** | I hope that when we come out on the other side of this mess , and I have faith that we will , and in an America that is not __`terribly different`__ than the one of a couple years ago when we went into this mess .                      |
    | **`pcc_eng_01_067.7651_x1079924_040:6-7-8`**   | Overall , this example is n't __`terribly different`__ from the fourth - party ecommerce example I wrote about last June except that example featured hardwired connections between the shopper and the merchant rulesets .                |
    | **`pcc_eng_04_040.8214_x0643713_21:36-37-38`** | Sure , it 's not all rainbows and sunshine for the poor , criminals wear tracker bracelets which electrocute them if they feel angry ( so they do n't attack bystanders ) but it 's not __`terribly different`__ to our world .            |
    | **`pcc_eng_15_046.3276_x0732863_17:4-5-6`**    | The results are n't __`terribly different`__ to previous surveys .                                                                                                                                                                         |
    | **`pcc_eng_25_084.2202_x1346922_18:3-4-5`**    | This is n't __`terribly different`__ from what Checkpoint Asia said last week but the really interesting part is that Bhadrakumar is confident that this is just the beginning and that the gulf between Cairo and Riyadh will only grow : |
    
    
    9. _terribly interested_
    
    |                                                | `token_str`                                                                                                                                                                                                            |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_12_037.8298_x0595679_19:3-5-6`**    | I 'm not really __`terribly interested`__ in monumentality .                                                                                                                                                           |
    | **`nyt_eng_20000623_0266_13:18-19-20`**        | `` It seems like they have their whole clique , '' she said , and she was not __`terribly interested`__ in them .                                                                                                      |
    | **`pcc_eng_07_023.9095_x0370377_4:3-5-6`**     | I am not too __`terribly interested`__ in wholesaling to other places as it makes the whole process much more complicated .                                                                                            |
    | **`pcc_eng_09_090.9315_x1455145_40:4-5-6`**    | The director is n't __`terribly interested`__ in science fiction .                                                                                                                                                     |
    | **`pcc_eng_05_038.2830_x0603626_02:38-40-41`** | I 've heard about cold brew coffee for a long time and heard how great it was but I was also given the impression that making it was a long , painful and difficult process so I never was __`terribly interested`__ . |
    
    
    10. _terribly surprised_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                                                            |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_29_083.0224_x1324738_06:15-16-17`**  | Hunter tells us that he predicted Milo would crash and burn and thus is n't __`terribly surprised`__ about any of this .                                                                                                                                                                               |
    | **`pcc_eng_16_056.8713_x0904236_223:09-10-11`** | Disappointed that she had n't remembered , but not __`terribly surprised`__ , Severus deftly steered the conversation back to the Dueling Club .                                                                                                                                                       |
    | **`nyt_eng_20070702_0135_1:12-19-20`**          | given the conservative bent of this court 's dependable majority , few among the champions of diversity were __`terribly surprised`__ by the disappointing Supreme Court ruling rejecting efforts in Seattle and Louisville , Ky. , to achieve greater diversity and avoid re-segregation of schools . |
    | **`pcc_eng_20_008.0238_x0113268_22:4-5-6`**     | " I was n't __`terribly surprised`__ " .                                                                                                                                                                                                                                                               |
    | **`nyt_eng_20000720_0356_8:22-23-24`**          | Duncan admitted that he anticipated the Spearman hypothesis would be borne out by neural imaging , and that therefore he was not __`terribly surprised`__ by his results .                                                                                                                             |
    
    
    11. _terribly new_
    
    |                                                | `token_str`                                                                                                                                      |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_089.5450_x1433538_223:3-4-5`**   | It is not __`terribly new`__ .                                                                                                                   |
    | **`pcc_eng_28_076.0342_x1213734_13:10-11-12`** | Unusual shapes and distortion printing of metal sheet is not __`terribly new`__ .                                                                |
    | **`pcc_eng_11_015.4366_x0233645_06:4-5-6`**    | Story itself is nothing __`terribly new`__ to those that saw the farming foray that took place on Facebook last year .                           |
    | **`nyt_eng_20050125_0046_4:08-09-10`**         | the idea of playing alongside men is n't __`terribly new`__ to a girl who pretended to be a boy in order to play pick-up matches on the street . |
    | **`pcc_eng_17_054.1370_x0858613_17:4-5-6`**    | Now this is nothing __`terribly new`__ .                                                                                                         |
    
    
    12. _terribly interesting_
    
    |                                                 | `token_str`                                                                                                                                                                                                        |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_26_038.1466_x0600580_66:6-7-8`**     | The " how " is not __`terribly interesting`__ but , yes , when I paste in Derby then it 's always when the streets are a bit quieter .                                                                             |
    | **`pcc_eng_06_025.1064_x0390187_196:5-6-7`**    | This film itself is nothing __`terribly interesting`__ in Porter 's output .                                                                                                                                       |
    | **`pcc_eng_03_008.4319_x0120195_079:23-24-25`** | when you 're in college , those things are exciting to you , as a boring heterosexual person , even if its not __`terribly interesting`__ to even , say , your classmates .                                        |
    | **`pcc_eng_24_082.5028_x1318274_11:08-09-10`**  | Even the history of Old Ales is n't __`terribly interesting`__ .                                                                                                                                                   |
    | **`pcc_eng_18_039.2074_x0618220_015:30-31-32`** | Though neither considerable in height or volume , the sheer uniqueness of Hraunfossar makes it worth the detour to visit ( neighboring Barnafoss is an added bonus , but not __`terribly interesting`__ itself ) . |
    
    
    13. _terribly exciting_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_15_016.3055_x0246865_36:16-17-18`** | They 're well - drilled and they do what they do , it 's just not __`terribly exciting`__ .                                                                                                                                                                                                                                                                                                                                                                                        |
    | **`pcc_eng_11_007.7543_x0109338_453:7-8-9`**   | And really , while there 's nothing __`terribly exciting`__ about Heilstatten apart from it being yet another horror movie from Germany that is n't just amateur gore hour ( though it features some pretty well done bits of the icky stuff as well ) or an arthouse flick , it works well throughout , keeps its pace up , takes care to make its characters less loathsome than you 'd expect , and seems generally made by people who care about entertaining their audience . |
    | **`pcc_eng_11_061.7760_x0983564_34:3-4-5`**    | It was n't __`terribly exciting`__ , which is what I always want it to be , but it was just really , really lovely , which is what I was n't entirely expecting .                                                                                                                                                                                                                                                                                                                  |
    | **`pcc_eng_03_035.7740_x0563217_090:3-4-5`**   | There 's nothing __`terribly exciting`__ about Anderson from a fantasy sense , but pitchers who have rotation spots are much better investments than ones who do n't -- and given the Brewers ' dire rotation , it feels inevitable that Anderson just locked one up for at least all of 2016 ( and possibly 2017 as well ) .                                                                                                                                                      |
    | **`pcc_eng_14_007.4135_x0103643_11:4-5-6`**    | ( It is not __`terribly exciting`__ , but it gets the job done . )                                                                                                                                                                                                                                                                                                                                                                                                                 |
    
    
    14. _terribly wrong_
    
    |                                               | `token_str`                                                                                                                                                                    |
    |:----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_02_097.6582_x1562714_12:1-2-3`**   | Nothing __`terribly wrong`__ with that .                                                                                                                                       |
    | **`pcc_eng_05_082.6438_x1321386_28:3-4-5`**   | There 's nothing __`terribly wrong`__ with the rooms at the Biltmore -- yours will most likely be reasonably clean and reasonably comfortable , and they 're spacious enough . |
    | **`pcc_eng_20_090.2569_x1442019_08:3-4-5`**   | There is nothing __`terribly wrong`__ with the story itself .                                                                                                                  |
    | **`pcc_eng_27_107.03923_x1720975_47:6-7-8`**  | I mean , there 's nothing __`terribly wrong`__ with it , but I just have such lackluster feelings about it .                                                                   |
    | **`pcc_eng_29_035.0517_x0549504_6:17-18-19`** | We saw a lot of fish leave the river Sunday ... and I guess there 's nothing __`terribly wrong`__ with it .                                                                    |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/...
    
    Samples saved as...
    1. `neg_bigram_examples/terribly/terribly_surprising_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_original_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_popular_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_unusual_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_comfortable_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_bright_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_common_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_different_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_interested_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_surprised_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_new_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_interesting_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_exciting_99ex.csv`
    1. `neg_bigram_examples/terribly/terribly_wrong_99ex.csv`
    
    ## 11. *inherently*
    
    |                        |       `N` |      `f1` |   `adv_total` |
    |:-----------------------|----------:|----------:|--------------:|
    | **NEGATED_inherently** | 6,347,364 | 3,173,660 |         8,614 |
    | **NEGMIR_inherently**  |   583,470 |   291,732 |         3,342 |
    
    
    |                               |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
    |:------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
    | **NEGany~inherently_wrong**   | 1,639 |    4.25 |    0.48 |    0.00 | 1,956.12 |  1,678 |    838.99 |      800.01 |        21,332 |
    | **NEGany~inherently_bad**     |   794 |    3.87 |    0.48 |    0.00 |   953.05 |    812 |    406.00 |      388.00 |       119,509 |
    | **NEGany~inherently_illegal** |    59 |    1.26 |    0.48 |    0.00 |    73.01 |     60 |     30.00 |       29.00 |         3,580 |
    | **NEGmir~inherently_wrong**   | 1,513 |    3.78 |    0.46 |    0.00 | 1,685.02 |  1,571 |    785.49 |      727.51 |         8,506 |
    | **NEGmir~inherently_bad**     |   148 |    1.83 |    0.44 |    0.00 |   144.52 |    158 |     79.00 |       69.00 |         4,790 |
    | **NEGany~inherently_evil**    |   358 |    2.12 |    0.41 |    0.00 |   312.23 |    392 |    196.00 |      162.00 |         3,171 |
    | **NEGany~inherently_better**  |   144 |    1.46 |    0.41 |    0.00 |   124.46 |    158 |     79.00 |       65.00 |        50,827 |
    | **NEGany~inherently_good**    |   283 |    1.46 |    0.36 |    0.00 |   189.85 |    329 |    164.50 |      118.50 |       201,244 |
    
    
    1. _inherently illegal_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                        |
    |:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_041.5377_x0656194_29:11-12-13`** | It should be noted that game rooms like this are not __`inherently illegal`__ .                                                                                                                                                                                                    |
    | **`pcc_eng_04_009.0617_x0130434_11:5-6-7`**    | Personally , I see nothing __`inherently illegal`__ with discrimination by individuals or private companies .                                                                                                                                                                      |
    | **`pcc_eng_05_030.8763_x0484001_11:4-5-6`**    | While there 's nothing __`inherently illegal`__ about an arranged marriage .                                                                                                                                                                                                       |
    | **`pcc_eng_19_042.3949_x0668324_003:6-7-8`**   | While that practice itself is n't __`inherently illegal`__ because wastewater treatment plants can effectively handle liquid medical waste as they would residential waste , the way hospitals actually do it can get them into serious trouble if they 're not careful or smart . |
    | **`pcc_eng_13_037.9169_x0596938_18:5-6-7`**    | Targeted killing is therefore not __`inherently illegal`__ ; after all , it beats the tragically untargeted killing used in the World War II bombings of Dresden , London and Hiroshima .                                                                                          |
    
    
    2. _inherently bad_
    
    |                                                 | `token_str`                                                                                                                                                                                                                                                  |
    |:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_05_099.7925_x1598054_13:08-09-10`**  | Charter schools are neither inherently good , nor __`inherently bad`__ .                                                                                                                                                                                     |
    | **`pcc_eng_23_007.9184_x0111746_75:27-28-29`**  | If you 're referring to the OP , I do n't think he was endorsing the behavior , he was just pointing out that there is nothing __`inherently bad`__ about it existing .                                                                                      |
    | **`pcc_eng_09_002.1023_x0017910_107:25-26-27`** | ABC 's Once Upon a Time illustrates this concept with its character background stories which reveal each character 's motivations as neither inherently good nor __`inherently bad`__ .                                                                      |
    | **`pcc_eng_11_066.7841_x1064756_49:09-10-11`**  | Care , emotion , and a connection is not __`inherently bad`__ .                                                                                                                                                                                              |
    | **`pcc_eng_17_076.5347_x1220790_034:4-5-6`**    | While this is not __`inherently bad`__ , getting started too quickly can be wasteful and set your team up for quick frustration , creating immediate conflict with other ideas about the major product attributes and how to get started on the right path . |
    
    
    3. _inherently wrong_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
    |:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_034.5098_x0542589_16:31-33-34`** | In another article , he urged the university not to lower the burden of proof in finding accused rapists in violation of university policy , writing that " there is nothing really __`inherently wrong`__ with the University failing to punish an alleged rapist -- regardless of his guilt -- in the absence of adequate certainty , " and adding , " expelling students is probably not going to contribute a great deal toward a rape victim 's recovery . " |
    | **`pcc_eng_01_104.0342_x1665071_36:3-4-5`**    | There is nothing __`inherently wrong`__ with this approach .                                                                                                                                                                                                                                                                                                                                                                                                      |
    | **`pcc_eng_05_001.8315_x0013490_08:3-4-5`**    | There 's nothing __`inherently wrong`__ with that , but it makes a sandwich significantly harder to balance ; featuring six things is always going to be harder than featuring one thing .                                                                                                                                                                                                                                                                        |
    | **`pcc_eng_01_064.1587_x1021522_029:3-4-5`**   | There is nothing __`inherently wrong`__ with this process but achieving the correct results requires consideration by the decision -makers of multiple legal and public policy issues to ensure that all customers of the utility are treated fairly and reasonably .                                                                                                                                                                                             |
    | **`pcc_eng_25_092.1321_x1474681_20:3-4-5`**    | There 's nothing __`inherently wrong`__ with slutty , of course .                                                                                                                                                                                                                                                                                                                                                                                                 |
    
    
    4. _inherently evil_
    
    |                                                | `token_str`                                                                                                                                                                                                  |
    |:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_27_007.9444_x0111776_21:09-10-11`** | may be an abomination , pancake mixes are not __`inherently evil`__ .                                                                                                                                        |
    | **`pcc_eng_11_062.8418_x1000875_21:3-4-5`**    | Snakes are not __`inherently evil`__ , and are generally beneficial for the environment .                                                                                                                    |
    | **`pcc_eng_16_059.5239_x0947530_18:08-09-10`** | " We can say that they are not __`inherently evil`__ , they are not monsters .                                                                                                                               |
    | **`nyt_eng_19991208_0231_51:10-11-12`**        | Martin and Klinkenberg both say holiday news updates are n't __`inherently evil`__ .                                                                                                                         |
    | **`pcc_eng_07_016.5171_x0251092_34:18-19-20`** | Further , if we mourn the absence of unplanned pregnancies and treat them as something that is n't __`inherently evil`__ , then we can start to be supportive of the women who choose to proceed with them . |
    
    
    5. _inherently better_
    
    |                                              | `token_str`                                                                                                                                                                         |
    |:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_09_033.3803_x0524221_104:5-6-7`** | Canadian tar sands are not __`inherently better`__ or safer , quite the opposite , they require the construction of massive and unstable infrastructure that will eventually fail . |
    | **`pcc_eng_27_066.3667_x1056718_47:3-4-5`**  | There 's nothing __`inherently better`__ about either system .                                                                                                                      |
    | **`pcc_eng_23_081.5559_x1301630_338:1-3-4`** | Nobody is __`inherently better`__ than me .                                                                                                                                         |
    | **`pcc_eng_01_047.9519_x0758676_29:3-4-5`**  | There is nothing __`inherently better`__ about being able to remember more things .                                                                                                 |
    | **`pcc_eng_15_010.1530_x0147811_48:3-4-5`**  | They are not __`inherently better`__ than the printed books they replace , and they are quickly becoming eclipsed in function by the smartphones most of us carry around .          |
    
    
    6. _inherently good_
    
    |                                                | `token_str`                                                                                                                                                                                                                                                                |
    |:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | **`pcc_eng_16_084.8110_x1356573_55:13-14-15`** | " Big data , sophisticated computer algorithms , and artificial intelligence are not __`inherently good`__ or bad , but that does n't mean their effects on society are neutral .                                                                                          |
    | **`pcc_eng_18_007.8311_x0110590_11:20-24-25`** | You are always there to aid in times of need , but you are also smart enough to realize not all people are __`inherently good`__ .                                                                                                                                         |
    | **`pcc_eng_00_066.3150_x1055808_29:25-26-27`** | On the other hand , Ariely also notes that these factors - the paradox of choice and our tendency towards default options - are not __`inherently good`__ or evil ; we can use them to help us make better decisions as much as they sometimes cause us to make bad ones . |
    | **`pcc_eng_13_037.0558_x0582879_04:10-12-13`** | " States rights " , he claimed , were not " __`inherently good`__ . "                                                                                                                                                                                                      |
    | **`pcc_eng_16_052.5085_x0833713_13:09-10-11`** | It is important to note that growth is not __`inherently good`__ for a company .                                                                                                                                                                                           |
    
    
    Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/...
    
    Samples saved as...
    1. `neg_bigram_examples/inherently/inherently_illegal_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_bad_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_wrong_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_evil_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_better_99ex.csv`
    1. `neg_bigram_examples/inherently/inherently_good_99ex.csv`


# 10 Most Negative Bigrams for each of the 8 Most Negative Adverbs


## 1. *necessarily*

|                         |       `N` |      `f1` |   `adv_total` |
|:------------------------|----------:|----------:|--------------:|
| **NEGATED_necessarily** | 6,347,364 | 3,173,660 |        42,886 |
| **NEGMIR_necessarily**  |   583,470 |   291,732 |           992 |


|                                   |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:----------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
| **NEGany~necessarily_bad**        | 2,059 |    6.31 |    0.50 |    0.00 | 2,814.04 |  2,062 |  1,030.99 |    1,028.01 |       119,509 |
| **NEGany~necessarily_indicative** | 1,389 |    6.29 |    0.50 |    0.00 | 1,925.89 |  1,389 |    694.50 |      694.50 |         2,313 |
| **NEGany~necessarily_true**       | 3,232 |    6.16 |    0.50 |    0.00 | 4,330.74 |  3,245 |  1,622.49 |    1,609.51 |        34,967 |
| **NEGany~necessarily_better**     | 1,887 |    6.07 |    0.50 |    0.00 | 2,564.81 |  1,891 |    945.49 |      941.51 |        50,827 |
| **NEGany~necessarily_easy**       |   909 |    5.67 |    0.50 |    0.00 | 1,260.28 |    909 |    454.50 |      454.50 |       108,923 |
| **NEGany~necessarily_related**    |   741 |    5.14 |    0.50 |    0.00 | 1,013.51 |    742 |    371.00 |      370.00 |        14,260 |
| **NEGany~necessarily_new**        |   482 |    4.74 |    0.50 |    0.00 |   668.24 |    482 |    241.00 |      241.00 |        21,538 |
| **NEGany~necessarily_surprising** |   340 |    4.23 |    0.50 |    0.00 |   471.36 |    340 |    170.00 |      170.00 |        18,776 |
| **NEGany~necessarily_enough**     |   279 |    3.93 |    0.50 |    0.00 |   386.79 |    279 |    139.50 |      139.50 |        27,603 |
| **NEGany~necessarily_aware**      |   206 |    3.48 |    0.50 |    0.00 |   285.59 |    206 |    103.00 |      103.00 |        28,973 |
| **NEGmir~necessarily_bad**        |    50 |    1.37 |    0.50 |    0.00 |    69.32 |     50 |     25.00 |       25.00 |         4,790 |
| **NEGmir~necessarily_wrong**      |   211 |    3.05 |    0.49 |    0.00 |   265.18 |    214 |    107.00 |      104.00 |         8,506 |


1. _necessarily indicative_

|                                                 | `token_str`                                                                                                                                                                   |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_064.0785_x1019370_034:12-13-14`** | However , the results of operations for the interim periods are not __`necessarily indicative`__ of the results that may be expected for the year ending December 31 , 2014 . |
| **`pcc_eng_28_043.8166_x0692740_50:09-10-11`**  | At the same time , a trailer is not __`necessarily indicative`__ of a film .                                                                                                  |
| **`pcc_eng_10_029.3600_x0458409_07:7-8-9`**     | However , this official rejection is not __`necessarily indicative`__ of poor performance by the gun .                                                                        |
| **`pcc_eng_09_003.9487_x0047947_41:09-10-11`**  | On the other hand , low turnover is n't __`necessarily indicative`__ of a productive work force .                                                                             |
| **`pcc_eng_05_035.3109_x0555718_12:4-5-6`**     | Past Performance is Not __`Necessarily Indicative`__ of Future Results .                                                                                                      |


2. _necessarily easy_

|                                                 | `token_str`                                                                                                                                                                                                          |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_096.8626_x1549967_085:6-7-8`**    | Your line of work is not __`necessarily easy`__ !                                                                                                                                                                    |
| **`pcc_eng_08_041.8737_x0661580_40:5-6-7`**     | Quick to make is not __`necessarily easy`__ , and they are great ways to practice skills and learn to read instructions .                                                                                            |
| **`pcc_eng_03_003.9991_x0048307_51:4-5-6`**     | Though it is not __`necessarily easy`__ to cultivate and maintain this coherence amid today 's consumeristic individualistic hurry - up- and- get-on - with - it norms .                                             |
| **`pcc_eng_03_007.2549_x0101045_2:12-13-14`**   | But for some people , boosting one 's nest egg is n't __`necessarily easy`__ or intuitive .                                                                                                                          |
| **`pcc_eng_10_014.1709_x0212830_118:16-17-18`** | The challenge that is presented to you is simple , straightforward and solvable , but not __`necessarily easy`__ so there is still delight in succeeding , and would that all of life 's challenges were like that . |


3. _necessarily bad_

|                                                 | `token_str`                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_037.0070_x0581700_29:3-4-5`**     | This is not __`necessarily bad`__ because people change and politicians have to change if they want to continue getting support from the people they purport to represent . |
| **`pcc_eng_21_093.3485_x1492229_26:1-2-3`**     | Not __`necessarily bad`__ , but not necessarily good .                                                                                                                      |
| **`pcc_eng_01_075.5390_x1205559_34:7-8-9`**     | The acting in the film is not __`necessarily bad`__ .                                                                                                                       |
| **`pcc_eng_18_011.9650_x0177513_16:16-17-18`**  | I 'm still not sure if I like it or not , but it 's not __`necessarily bad`__ .                                                                                             |
| **`pcc_eng_13_097.3545_x1556971_163:17-18-19`** | But special interests lobbying on behalf of their members are n't new , and it 's not __`necessarily bad`__ .                                                               |


4. _necessarily new_

|                                                | `token_str`                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_042.5357_x0671944_45:01-11-12`** | Nor is the message itself of Howard University 's photo __`necessarily new`__ .                                  |
| **`pcc_eng_14_037.6339_x0591831_100:4-5-6`**   | The names are n't __`necessarily new`__ to Astros fans .                                                         |
| **`pcc_eng_02_093.8994_x1502033_08:7-8-9`**    | While these approaches in themselves are not __`necessarily new`__ , the project is innovative is several ways . |
| **`apw_eng_20020526_1097_29:5-6-7`**           | today 's terrorism is n't __`necessarily new`__ .                                                                |
| **`pcc_eng_20_089.0819_x1423015_15:4-5-6`**    | These artists are n't __`necessarily new`__ , but they were new to me in 2019 .                                  |


5. _necessarily surprising_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_014.9162_x0225561_08:10-11-12`**  | Although the move is somewhat unprecedented , it 's not __`necessarily surprising`__ .                                                                                                                                                                                                                   |
| **`pcc_eng_12_085.1928_x1360400_14:4-5-6`**     | So it 's not __`necessarily surprising`__ then , that Cumberbatch 's comments here - thanks to their vagueness - manage to neither dispel or confirm the possibility of him taking on the iconic role .                                                                                                  |
| **`pcc_eng_04_102.5832_x1641122_30:3-4-5`**     | It is n't __`necessarily surprising`__ that the swamp is perturbed that President Trump is attempting to boost U.S. - Russia relations .                                                                                                                                                                 |
| **`pcc_eng_14_081.6689_x1304110_030:20-21-22`** | People , celebrities or not are employing cosmetic contact lens to enhance the look of them so it 's not __`necessarily surprising`__ if you want to buy as well ; but with a variety of models and brands of contact lenses being sold , you have to know how to choose the right lens for you to use . |
| **`pcc_eng_17_054.0723_x0857552_08:21-22-23`**  | Though support for the death penalty has in general been declining over the years [ 2 ] , it 's not __`necessarily surprising`__ that support would increase in a case such as this one .                                                                                                                |


6. _necessarily enough_

|                                                | `token_str`                                                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_013.8689_x0208422_12:3-4-5`**    | It is not __`necessarily enough`__ to only point out problems because employers are required to give staff members a chance to respond before a decision is presented about their future in the workplace , says Andrew Douglas , national head of Mac Pherson Kelly 's workplace relations team . |
| **`pcc_eng_23_036.1425_x0567648_24:5-6-7`**    | Replacing your windows is n't __`necessarily enough`__ .                                                                                                                                                                                                                                           |
| **`pcc_eng_25_036.0251_x0566997_13:10-11-12`** | However , a great product idea or invention is n't __`necessarily enough`__ to make a great business .                                                                                                                                                                                             |
| **`pcc_eng_10_027.6536_x0430752_18:15-16-17`** | But college grads such as Razmara are now finding that a postsecondary education is n't __`necessarily enough`__ .                                                                                                                                                                                 |
| **`pcc_eng_09_004.6589_x0059439_81:2-3-4`**    | is not __`necessarily enough`__ to get things done sometimes .                                                                                                                                                                                                                                     |


7. _necessarily aware_

|                                                | `token_str`                                                                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_030.2900_x0474268_21:20-21-22`** | So , we do n't know why that is happening , but anecdotally we definitely heard that patients are not __`necessarily aware`__ that financial assistance programs might exist .                                                                                                                           |
| **`nyt_eng_20000607_0109_17:15-16-17`**        | `` They are the No. 1 exchange in the world , and you 're not __`necessarily aware`__ that others want to compete and take your business . ''                                                                                                                                                            |
| **`pcc_eng_26_005.5853_x0073878_13:15-16-17`** | The pollution which the US shifted to China ( pollution which Chinese citizens are not __`necessarily aware`__ of )                                                                                                                                                                                      |
| **`pcc_eng_05_032.1521_x0504638_02:25-26-27`** | As therapists , when we talk about Mentalization ( or Mentalizing ) we often realise that the people we 're discussing it with are not __`necessarily aware`__ of what the concept actually means .                                                                                                      |
| **`pcc_eng_19_076.9527_x1227053_01:27-28-29`** | Democrats seeking the White House can usually count on cash donations from some of the same journalists who cover them -- though the journalists themselves are not __`necessarily aware`__ of this conflict of interest and their participation in it is rarely disclosed by their news organizations . |


8. _necessarily related_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                             |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_080.8353_x1292227_11:26-27-28`**  | Part of what makes Style Seek so unique is their Style Game : a nine-step quiz that identifies your personal style by presenting pictures , not __`necessarily related`__ to fashion , that you choose from between recognizable items such as 500 Days of Summer and Roman Holiday , a Range Rover and a Maserati .                    |
| **`pcc_eng_27_052.7587_x0836567_70:18-19-20`**  | This is very initial , but it appears that perhaps the microbiome 's response to illness is not __`necessarily related`__ to the disease we have , but may also be linked to other factors , such as the types of antibiotics people are treated with .                                                                                 |
| **`pcc_eng_20_007.6073_x0106481_030:19-20-21`** | One of the main challenges that I 've seen for moving true enterprise workloads to the cloud was n't __`necessarily related`__ to the cloud , but to the virtualization overhead that is often used as the underlying infrastructure of many clouds .                                                                                   |
| **`pcc_eng_11_087.3362_x1397516_068:53-54-55`** | Before buying , though , visit the website of the audience , who do never forget , like implied in it throughout the life styles of music , the following information related to design , we need strong and positive african morals , traditional values in accordance with pchological truth , and not __`necessarily related`__ to . |
| **`pcc_eng_24_104.2387_x1670381_11:11-12-13`**  | Though the storm has weakened , the storm surge is not __`necessarily related`__ to wind speeds .                                                                                                                                                                                                                                       |


9. _necessarily better_

|                                             | `token_str`                                                                                                                                                  |
|:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_058.9102_x0934778_40:4-5-6`** | Humpty Dumpty is not __`necessarily better`__ off being put back together again .                                                                            |
| **`pcc_eng_09_006.9224_x0095899_09:4-5-6`** | But easier is n't __`necessarily better`__ .                                                                                                                 |
| **`pcc_eng_00_065.6682_x1045522_09:6-7-8`** | Most of the changes are n't __`necessarily better`__ -- just different , forced upon me to accommodate a larger display and other forward - looking gizmos . |
| **`pcc_eng_09_036.7465_x0578652_31:6-7-8`** | " But taking more is n't __`necessarily better`__ , '' she says .                                                                                            |
| **`pcc_eng_00_033.2360_x0520848_10:5-6-7`** | However , more is n't __`necessarily better`__ .                                                                                                             |


10. _necessarily true_

|                                                | `token_str`                                                                                                                                                                                       |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_087.0557_x1393546_28:13-14-15`** | Each student in this class speaks two languages , but it is not __`necessarily true`__ that each student speaks the same two languages .                                                          |
| **`pcc_eng_04_079.2104_x1263431_01:36-37-38`** | Though the record of the Lipscomb men 's tennis team ( 2 - 9 ) might indicate that they have gotten off to a slow start this season , on an individual basis this is not __`necessarily true`__ . |
| **`pcc_eng_00_009.1670_x0131896_071:3-4-5`**   | This is not __`necessarily true`__ .                                                                                                                                                              |
| **`pcc_eng_09_010.3638_x0151919_04:16-17-18`** | Many assume driver 's ed turns out safer drivers , but research shows that 's not __`necessarily true`__ .                                                                                        |
| **`pcc_eng_15_098.0714_x1568962_37:18-19-20`** | Many people think the ability to make any story interesting is a talent , but it 's not __`necessarily true`__ .                                                                                  |


11. _necessarily wrong_

|                                                 | `token_str`                                                                                                                                                                                                            |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_065.9548_x1049855_014:3-4-5`**    | Wants are not __`necessarily wrong`__ , but longings become unhealthy when they consume our thoughts .                                                                                                                 |
| **`pcc_eng_18_042.2933_x0668098_37:4-5-6`**     | The Eagles are n't __`necessarily wrong`__ here .                                                                                                                                                                      |
| **`pcc_eng_24_004.4972_x0056398_173:08-09-10`** | Paul recognizes that anger is natural and not __`necessarily wrong`__ ; after all , God gets angry .                                                                                                                   |
| **`pcc_eng_06_073.5407_x1173387_07:7-8-9`**     | For one thing , there 's nothing __`necessarily wrong`__ with being anti-science , if only because science is neither a ) an all- encompassing explanation of everything , nor b ) an inherently virtuous phenomenon . |
| **`pcc_eng_12_084.5337_x1349668_376:16-17-18`** | These films wear their relative simplicity like a badge of honor , and that 's not __`necessarily wrong`__ of them .                                                                                                   |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/...

Samples saved as...
1. `neg_bigram_examples/necessarily/necessarily_indicative_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_easy_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_bad_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_new_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_surprising_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_enough_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_aware_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_related_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_better_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_true_99ex.csv`
1. `neg_bigram_examples/necessarily/necessarily_wrong_99ex.csv`

## 2. *that*

|                  |       `N` |      `f1` |   `adv_total` |
|:-----------------|----------:|----------:|--------------:|
| **NEGATED_that** | 6,347,364 | 3,173,660 |       166,676 |
| **NEGMIR_that**  |   583,470 |   291,732 |         4,559 |


|                            |    `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:---------------------------|-------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
| **NEGany~that_hard**       |  9,948 |    7.68 |    0.50 |    0.00 | 13,602.42 |  9,963 |  4,981.47 |    4,966.53 |        45,061 |
| **NEGany~that_different**  |  6,534 |    7.18 |    0.50 |    0.00 |  8,895.12 |  6,547 |  3,273.48 |    3,260.52 |        80,643 |
| **NEGany~that_great**      | 11,032 |    7.18 |    0.50 |    0.00 | 14,908.90 | 11,065 |  5,532.46 |    5,499.54 |        45,359 |
| **NEGany~that_difficult**  |  5,560 |    7.06 |    0.50 |    0.00 |  7,569.00 |  5,571 |  2,785.48 |    2,774.52 |        61,490 |
| **NEGany~that_big**        |  6,244 |    6.47 |    0.50 |    0.00 |  8,332.69 |  6,273 |  3,136.48 |    3,107.52 |        42,912 |
| **NEGany~that_surprising** |  1,133 |    5.99 |    0.50 |    0.00 |  1,570.89 |  1,133 |    566.50 |      566.50 |        18,776 |
| **NEGany~that_unusual**    |    977 |    5.77 |    0.50 |    0.00 |  1,354.57 |    977 |    488.50 |      488.50 |         7,412 |
| **NEGany~that_exciting**   |    805 |    5.49 |    0.50 |    0.00 |  1,116.08 |    805 |    402.50 |      402.50 |        20,233 |
| **NEGany~that_uncommon**   |    802 |    5.49 |    0.50 |    0.00 |  1,111.92 |    802 |    401.00 |      401.00 |         3,165 |
| **NEGany~that_impressed**  |    681 |    5.25 |    0.50 |    0.00 |    944.15 |    681 |    340.50 |      340.50 |        12,138 |
| **NEGmir~that_close**      |     60 |    1.67 |    0.50 |    0.00 |     83.19 |     60 |     30.00 |       30.00 |         4,831 |
| **NEGmir~that_happy**      |     41 |    1.03 |    0.50 |    0.00 |     56.84 |     41 |     20.50 |       20.50 |         5,463 |
| **NEGmir~that_simple**     |    474 |    3.67 |    0.48 |    0.00 |    580.44 |    483 |    241.50 |      232.50 |         7,465 |
| **NEGmir~that_popular**    |     65 |    1.54 |    0.48 |    0.00 |     81.14 |     66 |     33.00 |       32.00 |         2,841 |
| **NEGmir~that_difficult**  |     52 |    1.16 |    0.48 |    0.00 |     63.56 |     53 |     26.50 |       25.50 |         4,854 |
| **NEGmir~that_easy**       |    450 |    3.23 |    0.47 |    0.00 |    512.43 |    465 |    232.50 |      217.50 |         7,749 |
| **NEGmir~that_big**        |    113 |    2.08 |    0.47 |    0.00 |    132.98 |    116 |     58.00 |       55.00 |         3,134 |
| **NEGmir~that_interested** |     62 |    1.26 |    0.47 |    0.00 |     70.93 |     64 |     32.00 |       30.00 |         2,877 |
| **NEGmir~that_great**      |    286 |    2.71 |    0.46 |    0.00 |    312.65 |    298 |    149.00 |      137.00 |         2,123 |
| **NEGmir~that_good**       |    447 |    2.65 |    0.44 |    0.00 |    441.70 |    476 |    238.00 |      209.00 |        13,423 |


1. _that surprising_

|                                                | `token_str`                                                                                                                                                                                                       |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_084.9470_x1356690_10:18-19-20`** | While it may seem odd that all three of these celebrities are relatively young , it is not __`that surprising`__ .                                                                                                |
| **`pcc_eng_20_089.0219_x1422017_49:20-21-22`** | The simple fact is that little is done even when the USDA is on the case , which is not __`that surprising`__ for an agency with a well - greased revolving door between itself and the businesses it regulates . |
| **`pcc_eng_10_079.1004_x1262366_31:11-12-13`** | Of course , this was from 1955 so that is not __`that surprising`__ .                                                                                                                                             |
| **`pcc_eng_26_036.3799_x0571842_11:24-27-28`** | This also enables Stormzy to pull off the album 's most unexpected facet - though given the title , perhaps overt religiosity should n't have been __`that surprising`__ .                                        |
| **`nyt_eng_20001006_0145_29:4-5-6`**           | the alliances are n't __`that surprising`__ .                                                                                                                                                                     |


2. _that unusual_

|                                                | `token_str`                                                                                                                                                                                                                                                          |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000324_0221_21:4-5-6`**           | `` It 's not __`that unusual`__ for judges to have second thoughts , '' said Spurlock , a former trial and appellate judge .                                                                                                                                         |
| **`pcc_eng_test_2.06136_x25978_097:11-12-13`** | But Spacey 's subsequent issues since Rapp spoke out are not __`that unusual`__ for someone at his second Saturn return and fifth Jupiter return .                                                                                                                   |
| **`pcc_eng_22_006.4671_x0088233_06:48-49-50`** | Back then New Zealand had no experience of floodlit rugby and , in any case , how could you expect the punters in Christchurch and Dunedin , in particular , to turn out on a cold winter 's night when a gale blowing off the Antarctic is not __`that unusual`__ . |
| **`pcc_eng_25_045.9292_x0727337_067:5-6-7`**   | Dog vomiting just is n't __`that unusual`__ in our house .                                                                                                                                                                                                           |
| **`pcc_eng_02_091.3263_x1460441_075:5-6-7`**   | Edberg 's story is n't __`that unusual`__ in the startup world .                                                                                                                                                                                                     |


3. _that exciting_

|                                                | `token_str`                                                                                                                                                                                                                                                                         |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_007.8685_x0111062_29:08-10-11`** | OK , no , my twist is not nearly __`that exciting`__ .                                                                                                                                                                                                                              |
| **`nyt_eng_19981117_0145_26:16-17-18`**        | let 's face it , turkey by itself , moist or dry , is just not __`that exciting`__ .                                                                                                                                                                                                |
| **`pcc_eng_10_020.5840_x0316538_08:08-09-10`** | I think that the match overall was n't __`that exciting`__ .                                                                                                                                                                                                                        |
| **`nyt_eng_20070609_0105_23:31-32-33`**        | `` I think maybe there 's a little smirk on the coach 's face , '' Barry said , `` and on the organization 's face , that it 's not __`that exciting`__ to people outside of San Antonio , that we 're doing it quietly , something special , right here , and we get to enjoy it . |
| **`pcc_eng_11_066.2590_x1056231_78:12-14-15`** | The problem here is that the " exciting incentives " are n't really __`that exciting`__ .                                                                                                                                                                                           |


4. _that uncommon_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                 |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_005.4805_x0072964_39:3-4-5`**     | This is n't __`that uncommon`__ but the thing that makes this a little inconvenient with this vape is that you have to turn it upside down and take out the wand to do this .                                                                                                               |
| **`pcc_eng_18_008.9083_x0127940_11:19-20-21`**  | Early morning FBI arrests for those who threaten national security based on wiretaps and email interceptions are now not __`that uncommon`__ , but you can walk the streets confident that you are not on camera the whole time , and the innocent seem to have relatively little to fear . |
| **`pcc_eng_val_2.04827_x24095_61:17-18-19`**    | I find , oftentimes , in an actor who 's played the villain , it 's not __`that uncommon`__ that when I meet them , they 're the most lovely person .                                                                                                                                       |
| **`pcc_eng_23_039.0433_x0614585_040:16-17-18`** | " The man is obviously suffering from schizophrenia , and the type of schizophrenia is n't __`that uncommon`__ .                                                                                                                                                                            |
| **`pcc_eng_26_092.1059_x1473341_136:11-12-13`** | And that 's , you know -- Those thing are not __`that uncommon`__ , unfortunately .                                                                                                                                                                                                         |


5. _that impressed_

|                                                | `token_str`                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_050.8504_x0805375_25:11-12-13`** | I had one a long time ago , and was not __`that impressed`__ .                                                                 |
| **`pcc_eng_02_030.7743_x0481888_16:5-6-7`**    | Honestly , I was n't __`that impressed`__ when I checked out the App Store description , or when I first opened the app .      |
| **`pcc_eng_07_022.6240_x0349705_10:7-8-9`**    | After my first viewing I was n't __`that impressed`__ .                                                                        |
| **`pcc_eng_01_048.6587_x0770122_21:14-15-16`** | And the new guy at my chiropractor is fine , but I was n't __`that impressed`__ .                                              |
| **`pcc_eng_15_011.8246_x0174747_11:21-22-23`** | J-lo went down for a couple of days with flu , Nato had a go at mothering but J was n't __`that impressed`__ with his effort . |


6. _that close_

|                                                 | `token_str`                                                                                                                                                                                                   |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19990730_0092_35:18-20-21`**         | -lrb- The fire was -RRB- maybe 20 feet in diameter and twice as high , I had never been __`that close`__ to a fire so large .                                                                                 |
| **`pcc_eng_23_046.1691_x0729831_06:3-4-5`**     | I was n't __`that close`__ to her , and had n't kept up at all in recent years .                                                                                                                              |
| **`pcc_eng_19_078.0095_x1244134_099:21-22-23`** | " This is normal and no reason for alarm , " Mussen said , " except that people usually are not __`that close`__ to bee colonies to notice the normal demise of substantial numbers of overwintering bees . " |
| **`pcc_eng_20_034.3317_x0538925_10:10-11-12`**  | Apparently Wolfensohn 's brother and sister- in- law were n't __`that close`__ anyway so they were n't the last bit concerned when they had n't heard from Wolfensohn 's side of the family for years .       |
| **`nyt_eng_19961118_0032_16:13-15-16`**         | Denver beat the Patriots , 34-8 , in a game that was n't nearly __`that close`__ .                                                                                                                            |


7. _that happy_

|                                                | `token_str`                                                                                                                                                                                                                                                                           |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_092.7711_x1483281_13:4-5-6`**    | But people are not __`that happy`__ with Raju 's son .                                                                                                                                                                                                                                |
| **`pcc_eng_15_048.1903_x0762915_33:20-21-22`** | So Dee , the main character in my novel , is happy until she realizes that she 's actually not __`that happy`__ .                                                                                                                                                                     |
| **`pcc_eng_06_103.1365_x1652404_24:3-4-5`**    | I am not __`that happy`__ .                                                                                                                                                                                                                                                           |
| **`pcc_eng_19_044.0470_x0694967_034:1-8-9`**   | None of those students should have been __`that happy`__ that they finally felt like they belonged -- they should have had that experience much sooner .                                                                                                                              |
| **`pcc_eng_25_008.2908_x0118205_05:46-48-49`** | We 're going to assume the best and guess the copywriter was just going for a turn of phrase , and did n't realize the expression " the South will rise again , " has its roots as a rallying cry for folks who were n't all __`that happy`__ with the way the Civil War turned out . |


8. _that hard_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_071.9839_x1149311_38:3-4-5`**    | That is not __`that hard`__ to do , in theory even a smartphone could be adapted to read such chips , but that would lead to data security problems .                                                                                                                                                                                                                                      |
| **`nyt_eng_20061206_0069_27:09-10-11`**        | FOOD-CANDY-RECIPES -- ATLANTA -- Candy for gift-giving is n't __`that hard`__ to make , especially when you have a foolproof recipe and a reliable candy thermometer .                                                                                                                                                                                                                     |
| **`pcc_eng_11_015.4369_x0233655_59:3-4-5`**    | It 's not __`that hard`__ , especially if they admit what the stats above are telling them .                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_19_012.9663_x0193374_04:11-13-14`** | Everyone wants a brighter smile these days and it should n't be __`that hard`__ to get one .                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_26_096.9348_x1551176_04:51-52-53`** | " I joined the robotics team my 11th grade year and I had no idea what they wanted me to do or how they expected me to be able to do any they ask but after a short bit of time I seen that creating gear motors and such was n't __`that hard`__ and also having great teammates makes everything easier over time and that everything we create will take lot of dedication and energy . |


9. _that different_

|                                                | `token_str`                                                                                                                                                                                                   |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_046.4146_x0733648_21:3-5-6`**    | This may not be __`that different`__ ( particularly if we get involved and start leading again ) .                                                                                                            |
| **`pcc_eng_19_040.3714_x0635291_28:32-34-35`** | Okay , so one might say that it also had a story , but it still relied heavily on those effects to " sell " the plot , and that 's not really __`that different`__ from later films , even those made today . |
| **`pcc_eng_28_048.8319_x0773924_096:7-8-9`**   | But they 're cranial capacity is n't __`that different`__ than chimpanzees .                                                                                                                                  |
| **`pcc_eng_00_066.2149_x1054185_26:6-7-8`**    | Marketing and human resources are n't __`that different`__ like they sound .                                                                                                                                  |
| **`pcc_eng_10_027.5506_x0429046_04:6-7-8`**    | " Unfortunately , they are n't __`that different`__ . "                                                                                                                                                       |


10. _that difficult_

|                                                | `token_str`                                                                                                                           |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_094.8418_x1518309_25:5-7-8`**    | What if it is n't actually __`that difficult`__ with a little concentrated focus ?                                                    |
| **`pcc_eng_26_007.8701_x0110779_05:11-12-13`** | Removing a stuck labret stud can hurt , but is not __`that difficult`__ and is completely necessary .                                 |
| **`pcc_eng_28_073.8736_x1178661_13:11-12-13`** | We recommend giving soldering a go tho as its really not __`that difficult`__ .                                                       |
| **`pcc_eng_08_078.8242_x1260196_08:4-5-6`**    | It actually is n't __`that difficult`__ if you consider the following options to always eating out and paying for everything you do . |
| **`pcc_eng_06_072.7679_x1160950_095:3-4-5`**   | It is not __`that difficult`__ ; with a few things on the list that will make your life easier and easier on your pets as well .      |


11. _that great_

|                                                 | `token_str`                                                                                       |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_002.4809_x0024188_26:14-15-16`**  | All in , this was n't really anything bad , but it was n't __`that great`__ either .              |
| **`pcc_eng_17_070.7736_x1127374_191:08-09-10`** | LOUIS- DREYFUS : Yeah , it was n't __`that great`__ .                                             |
| **`pcc_eng_20_035.2194_x0553168_35:09-10-11`**  | But the magnitude of the money involved was not __`that great`__ .                                |
| **`pcc_eng_21_074.5686_x1188896_11:13-14-15`**  | I added some horns but I gotta say , the samples are n't __`that great`__ .                       |
| **`pcc_eng_17_055.9210_x0887262_52:16-17-18`**  | Let 's face it : the free headphones Apple supplies with every i Phone are not __`that great`__ . |


12. _that big_

|                                                | `token_str`                                                                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_038.5783_x0608393_11:14-15-16`** | Since we planned on replacing the antiquated A/C unit anyway , it was n't __`that big`__ of a deal .                                                                                                  |
| **`pcc_eng_14_012.8777_x0191788_005:3-4-5`**   | It ai n't __`that big`__ .                                                                                                                                                                            |
| **`pcc_eng_22_067.9472_x1081909_391:4-6-7`**   | Our place is n't quite __`that big`__ anyways to accommodate more than 100 people . "                                                                                                                 |
| **`pcc_eng_12_082.7107_x1320138_31:14-15-16`** | Tripp acknowledged that " the upfront cost " of doing so is " not __`that big`__ , " but he suggested that such a practice might also create a " litigation risk " from vendors who were not chosen . |
| **`pcc_eng_25_097.9766_x1569423_20:10-11-12`** | I 'm going there anyway , so it is n't __`that big`__ of a deal .                                                                                                                                     |


13. _that popular_

|                                                 | `token_str`                                                                                                                                                                                                                                |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_101.8313_x1628963_40:15-16-17`**  | Back in a day patching a game was n't an option and DLCs was n't __`that popular`__ so the game had to be released as intended .                                                                                                           |
| **`pcc_eng_00_038.8014_x0610600_08:19-20-21`**  | I hired a lvl 70 to run me through the instance at lvl 45 , because it 's not __`that popular`__ an instance , at least on my server .                                                                                                     |
| **`pcc_eng_17_044.3230_x0699644_217:19-20-21`** | But it is not safe to consider the delay before going monthly as a sign that it was not __`that popular`__ .                                                                                                                               |
| **`pcc_eng_10_050.0200_x0792709_12:10-11-12`**  | I lived in Japan one year and tampons are not __`that popular`__ .                                                                                                                                                                         |
| **`pcc_eng_28_019.3509_x0296738_58:07-09-10`**  | But 1 ) Mc Cain is n't all __`that popular`__ among AZ GOPers : he only got 51 % in the ' 08 primary at a time he really needed the boost ; and 2 ) he 's running a campaign almost designed to anger anyone who fell for his 2000 shtik . |


14. _that simple_

|                                                 | `token_str`                                                                                                                                                                                                            |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_077.6266_x1237909_17:4-5-6`**     | Apparently things are n't __`that simple`__ ...                                                                                                                                                                        |
| **`nyt_eng_19990818_0135_11:15-16-17`**         | he knew where he and his priorities needed to be , but it was n't __`that simple`__ .                                                                                                                                  |
| **`nyt_eng_19961118_0669_42:25-26-27`**         | but Ritter , who is now executive director of the Transition Commission for the Transfer of the Panama Canal , said the issue is not __`that simple`__ .                                                               |
| **`pcc_eng_03_009.0298_x0129877_11:4-6-7`**     | But it may not be __`that simple`__ .                                                                                                                                                                                  |
| **`pcc_eng_16_082.2586_x1315169_008:09-10-11`** | But putting that straightforward plan into practice is n't __`that simple`__ , since every special-needs child requires an individualized program that addresses his or her specific disabilities and learning style . |


15. _that interested_

|                                                | `token_str`                                                                                                                                 |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20090509_0609_7:14-16-17`**         | because people know what is the situation at the moment , people are not really __`that interested`__ anymore . ''                          |
| **`pcc_eng_02_032.6080_x0511608_03:4-5-6`**    | Previously they were n't __`that interested`__ in clothes or what they wore , but now they feel inspired to explore their style sense .     |
| **`pcc_eng_15_095.8004_x1532287_07:3-4-5`**    | Zane is not __`that interested`__ in the Gollywhopper Games .                                                                               |
| **`pcc_eng_00_004.6991_x0059756_29:18-20-21`** | If I do n't like how it is made , its design and all then I will not be __`that interested`__ in seeing what other things it has to offer . |
| **`nyt_eng_20000612_1042_16:09-11-12`**        | on top of that , females who are n't even __`that interested`__ in the film expect to ride out the opening tempest .                        |


16. _that easy_

|                                             | `token_str`                                                                                                  |
|:--------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19980923_0328_7:13-14-15`**      | the simple and difficult answer is that things in Russia just are n't __`that easy`__ .                      |
| **`pcc_eng_05_083.0409_x1327717_04:4-5-6`** | The sound is not __`that easy`__ to set up .                                                                 |
| **`pcc_eng_05_084.6573_x1353862_50:4-5-6`** | However guns were not __`that easy`__ to use they required lots of training and took a long time to reload . |
| **`pcc_eng_17_103.8908_x1663244_12:5-6-7`** | Right now it 's not __`that easy`__ to find demos through the game store .                                   |
| **`pcc_eng_04_075.3966_x1201616_38:3-5-6`** | They are n't all __`that easy`__ to find by feel since they are flush with the surface .                     |


17. _that good_

|                                                 | `token_str`                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_017.5880_x0268455_2:4-5-6`**      | He 's just not __`that good`__ , and has a poor track record .                                                                                                      |
| **`pcc_eng_18_004.8793_x0062902_114:31-33-34`** | Actually , I know I 'm getting more and more speed because I went a second a lap faster today than I 've ever ridden , and the track was n't even __`that good`__ . |
| **`pcc_eng_17_077.6580_x1238762_11:13-14-15`**  | sorry for the bad shots I was drinking and the camera was not that good                                                                                             |
| **`pcc_eng_21_066.1409_x1052539_31:24-25-26`**  | Your aim should be the conflict sweet spot : " Avoiding conflict is n't good ; debating each other all the time is not __`that good`__ either .                     |
| **`pcc_eng_28_072.0548_x1149420_62:13-15-16`**  | So it 's good when it 's good , but it 's not always __`that good`__ .                                                                                              |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/...

Samples saved as...
1. `neg_bigram_examples/that/that_surprising_99ex.csv`
1. `neg_bigram_examples/that/that_unusual_99ex.csv`
1. `neg_bigram_examples/that/that_exciting_99ex.csv`
1. `neg_bigram_examples/that/that_uncommon_99ex.csv`
1. `neg_bigram_examples/that/that_impressed_99ex.csv`
1. `neg_bigram_examples/that/that_close_99ex.csv`
1. `neg_bigram_examples/that/that_happy_99ex.csv`
1. `neg_bigram_examples/that/that_hard_99ex.csv`
1. `neg_bigram_examples/that/that_different_99ex.csv`
1. `neg_bigram_examples/that/that_difficult_99ex.csv`
1. `neg_bigram_examples/that/that_great_99ex.csv`
1. `neg_bigram_examples/that/that_big_99ex.csv`
1. `neg_bigram_examples/that/that_popular_99ex.csv`
1. `neg_bigram_examples/that/that_simple_99ex.csv`
1. `neg_bigram_examples/that/that_interested_99ex.csv`
1. `neg_bigram_examples/that/that_easy_99ex.csv`
1. `neg_bigram_examples/that/that_good_99ex.csv`

## 3. *exactly*

|                     |       `N` |      `f1` |   `adv_total` |
|:--------------------|----------:|----------:|--------------:|
| **NEGMIR_exactly**  |   583,470 |   291,732 |           869 |
| **NEGATED_exactly** | 6,347,364 | 3,173,660 |        44,503 |


|                               |   `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:------------------------------|------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
| **NEGany~exactly_sure**       | 8,794 |    7.46 |    0.50 |    0.00 | 11,991.61 |  8,810 |  4,404.97 |    4,389.03 |       134,139 |
| **NEGany~exactly_clear**      | 1,746 |    6.38 |    0.50 |    0.00 |  2,405.43 |  1,747 |    873.49 |      872.51 |        84,227 |
| **NEGany~exactly_new**        | 1,371 |    6.03 |    0.50 |    0.00 |  1,885.86 |  1,372 |    686.00 |      685.00 |        21,538 |
| **NEGany~exactly_easy**       | 1,066 |    5.67 |    0.50 |    0.00 |  1,463.43 |  1,067 |    533.50 |      532.50 |       108,923 |
| **NEGany~exactly_cheap**      |   691 |    5.27 |    0.50 |    0.00 |    958.01 |    691 |    345.50 |      345.50 |         6,591 |
| **NEGany~exactly_surprising** |   440 |    4.61 |    0.50 |    0.00 |    610.01 |    440 |    220.00 |      220.00 |        18,776 |
| **NEGany~exactly_subtle**     |   263 |    3.84 |    0.50 |    0.00 |    364.61 |    263 |    131.50 |      131.50 |         5,299 |
| **NEGany~exactly_fair**       |   260 |    3.83 |    0.50 |    0.00 |    360.45 |    260 |    130.00 |      130.00 |         6,964 |
| **NEGany~exactly_fun**        |   224 |    3.60 |    0.50 |    0.00 |    310.54 |    224 |    112.00 |      112.00 |        19,661 |
| **NEGany~exactly_hard**       |   203 |    3.46 |    0.50 |    0.00 |    281.43 |    203 |    101.50 |      101.50 |        45,061 |
| **NEGmir~exactly_sure**       |   148 |    3.10 |    0.50 |    0.00 |    205.21 |    148 |     74.00 |       74.00 |         5,978 |
| **NEGmir~exactly_clear**      |    52 |    1.16 |    0.48 |    0.00 |     63.56 |     53 |     26.50 |       25.50 |         3,321 |


1. _exactly sure_

|                                                 | `token_str`                                                                                                                                                                                                                                |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_13_083.2034_x1328769_39:3-4-5`**     | I 'm not __`exactly sure`__ who this movie is aimed at since kids will find it too scary and adults will just be bored to tears or too busy laughing their asses off .                                                                     |
| **`pcc_eng_14_004.8169_x0061865_22:3-4-5`**     | I 'm not __`exactly sure`__ what the measures are that get people actively involved , but they need to have the information so they can make an informed decision as to what they are going to support or not .                            |
| **`pcc_eng_12_035.5505_x0558870_024:25-26-27`** | When asked how it feels to be a part of such a noteworthy tradition at Penn , Cheeseman explains that , while he 's not __`exactly sure`__ how he feels , he does acknowledge that it 's rather " neat " to be a part of Penn 's history . |
| **`nyt_eng_19980715_0211_20:08-09-10`**         | this seems appropriate , though I 'm not __`exactly sure`__ how . -RRB-                                                                                                                                                                    |
| **`pcc_eng_11_061.8000_x0983952_08:1-2-3`**     | Not __`exactly sure`__ you need to pay someone for advice like that , but somehow Hitch makes his counsel seem useful , endearing and necessary .                                                                                          |


2. _exactly cheap_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_036.1497_x0568962_04:3-4-5`**     | This is n't __`exactly cheap`__ given that the drug has been in use for 62 years and is on the WHO 's List of Essential Medicines , which is considered to be the bare minimum pharmaceutical foundation of a bare minimum health - care system .                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_02_014.1025_x0211946_080:13-14-15`** | Today simple myoelectrics are much more affordable , but they are still not __`exactly cheap`__ .                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_02_081.9943_x1309524_34:14-15-16`**  | 600,000 copies is an excellent achievement , particularly given that the game is not __`exactly cheap`__ ( it is n't expensive , but it is rather more expensive than things like Terraria ) .                                                                                                                                                                                                                                                                                                                                    |
| **`pcc_eng_24_101.4229_x1624707_03:21-22-23`**  | " The employer community has benefitted , but at a price for the cost of the review , which is not __`exactly cheap`__ if it is just over a dispute over the declination ... of a prescription , " said Zachary Sacks , managing partner at Culver City , California , law firm Sacks & Zolonz Under California workers comp reforms passed in 2012 , injured workers can request independent medical reviews to dispute treatment that was modified or denied under utilization reviews , which employers and insurers request . |
| **`pcc_eng_06_070.4883_x1124395_034:4-5-6`**    | New Orleans is n't __`exactly cheap`__ for events , and just try to find us a vegan or even a vegetarian caterer .                                                                                                                                                                                                                                                                                                                                                                                                                |


3. _exactly surprising_

|                                                | `token_str`                                                                                                                                                                                                                                                                                              |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_028.7930_x0449616_10:27-28-29`** | That a team executive in the league with the most embattled officiating corps would promote a tool that would create greater transparency on the court is n't __`exactly surprising`__ ; you can also expect that league 's resistance to such a tool .                                                  |
| **`pcc_eng_28_045.7611_x0724394_18:12-13-14`** | Given how clearly horned - up young Conrad is it 's not __`exactly surprising`__ that he makes a beeline for Rush 's crotch ; pulling away the buff beauty 's briefs , then promptly slurping on the handsome fuck - rod that he discovers straining inside .                                            |
| **`pcc_eng_24_081.8035_x1306938_21:3-4-5`**    | It 's not __`exactly surprising`__ that good data-driven resources are hard to find .                                                                                                                                                                                                                    |
| **`pcc_eng_07_024.6618_x0382669_36:41-42-43`** | While most of the sellers at the market would n't start such a confrontation , it 's unfortunate that a small minority of vendors chose to take this initiative ; if one has no empathy towards animals , it 's not __`exactly surprising`__ that some express their frustrations in undesireable ways . |
| **`pcc_eng_19_075.0942_x1197003_20:11-12-13`** | Of course , you 're probably thinking that it 's not __`exactly surprising`__ that the party that , at the time , most suffered under First Past the Post would be the first to call for its passing into history .                                                                                      |


4. _exactly subtle_

|                                                | `token_str`                                                                                                                                                                                     |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_050.6849_x0802655_24:7-8-9`**    | It 's surely effective , but not __`exactly subtle`__ .                                                                                                                                         |
| **`pcc_eng_03_083.8367_x1341468_08:11-12-13`** | That whipsawing effect , between revulsion and tenderness , was n't __`exactly subtle`__ .                                                                                                      |
| **`pcc_eng_12_034.4892_x0541837_12:7-8-9`**    | If you know Spanish it 's not __`exactly subtle`__ that the AMIGOS organization is exactly translated to " friends of the Americas " or " friends international . "                             |
| **`pcc_eng_02_002.2391_x0020034_09:25-26-27`** | This film takes all the usual 80s tropes that are doing the rounds of late ( yes , that Stranger Things reference above was n't __`exactly subtle`__ was it ? ) but somehow gets away with it . |
| **`pcc_eng_22_055.1459_x0874987_098:1-2-3`**   | Not __`exactly subtle`__ , but I got one of his eyes back in time for him to catch me smile , and return the ceremonial gesture to the Bug as best I could .                                    |


5. _exactly fair_

|                                             | `token_str`                                                                                                                                                                           |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_084.7432_x1355354_02:3-4-5`** | It 's not __`exactly fair`__ to judge it as an EP because A. ) it 's only three songs and B. ) these three songs are sequenced terribly and do n't really fit together in the least . |
| **`pcc_eng_03_038.5826_x0608771_27:5-6-7`** | And while it 's not __`exactly fair`__ to say " no one cared " , the were n't compelled to care for any reason other than they were told to and had heard Bret Hart 's name before .  |
| **`pcc_eng_00_011.0232_x0161684_01:5-6-7`** | Well , that 's not __`exactly fair`__ .                                                                                                                                               |
| **`pcc_eng_02_092.3330_x1476634_34:6-7-8`** | And sometimes , it is n't __`exactly fair`__ .                                                                                                                                        |
| **`pcc_eng_25_035.5367_x0559042_12:3-4-5`** | It 's not __`exactly fair`__ to Flannery O'Connor either .                                                                                                                            |


6. _exactly fun_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                               |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_078.7971_x1256842_11:13-14-15`** | So many moms have been there and of course , it 's not __`exactly fun`__ to hear that someone thinks we 're pregnant despite having already given birth .                                                                                                                                                                 |
| **`pcc_eng_04_005.5144_x0073212_40:08-09-10`** | It does everything , but it 's not __`exactly fun`__ to drive . "                                                                                                                                                                                                                                                         |
| **`pcc_eng_16_028.9639_x0452742_38:23-24-25`** | majority of people who play wow has never had to make difficult choices quickly , never had to do things that were not __`exactly fun`__ , just because they needed to .                                                                                                                                                  |
| **`pcc_eng_19_026.1543_x0406196_015:3-4-5`**   | It 's not __`exactly fun`__ .                                                                                                                                                                                                                                                                                             |
| **`pcc_eng_00_009.8216_x0142381_08:19-20-21`** | It 's scary to think about the impact rising STD rates could have , and although it 's not __`exactly fun`__ , casual conversation fodder , it 's imperative that we talk about issues pertaining to sexual health -- especially when the alternative is remaining uninformed and potentially putting ourselves at risk . |


7. _exactly hard_

|                                                | `token_str`                                                                                                                                       |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_098.2815_x1572765_4:09-10-11`**  | Double-clicking apps and docs to open them is n't __`exactly hard`__ .                                                                            |
| **`pcc_eng_09_011.7996_x0175029_04:3-4-5`**    | Zeppelin are n't __`exactly hard`__ to figure out .                                                                                               |
| **`pcc_eng_25_012.2905_x0182527_5:6-7-8`**     | Plus , the campaign is n't __`exactly hard`__ on the eyes !                                                                                       |
| **`pcc_eng_08_070.7463_x1129318_04:24-25-26`** | Perhaps Go ! was pricing seats below Aloha 's costs , and with a fleet of ancient , inefficient aircraft , that 's not __`exactly hard`__ to do . |
| **`pcc_eng_05_084.2433_x1347184_45:6-7-8`**    | Even though the game 's not __`exactly hard`__ and the AI makes some dumb moves sometimes , those dumb moves are deliberate .                     |


8. _exactly clear_

|                                                 | `token_str`                                                                                                                                                                                                                    |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_082.2949_x1315265_15:16-17-18`**  | But because of the tiered nature of both licensing and tax rates , it 's not __`exactly clear`__ who is going to apply for which licenses , and how the market will shake out .                                                |
| **`pcc_eng_17_059.6888_x0948000_11:6-7-8`**     | For what , I 'm not __`exactly clear`__ .                                                                                                                                                                                      |
| **`pcc_eng_04_104.4998_x1671984_12:6-7-8`**     | And in case it was n't __`exactly clear`__ what the billionaire loved about the movie , there 's this tasty anecdote about a strike below the belt :                                                                           |
| **`pcc_eng_12_039.1287_x0616768_12:29-31-32`**  | The problem being sometimes you have multiple pieces of evidence that would be considered incriminating but the game only accepts one specific piece ; of which it is n't always __`exactly clear`__ as to which one that is . |
| **`pcc_eng_00_033.8625_x0531059_032:22-23-24`** | In the words of the old Buffalo Springfield song , " There 's something happening here , what is , ai n't __`exactly clear`__ . "                                                                                              |


9. _exactly new_

|                                                 | `token_str`                                                                               |
|:------------------------------------------------|:------------------------------------------------------------------------------------------|
| **`pcc_eng_10_056.3043_x0894444_07:11-12-13`**  | Sen. Jeff Steinborn is a Las Cruces Democrat who is n't __`exactly new`__ .               |
| **`pcc_eng_05_012.7234_x0190065_14:6-7-8`**     | Then again the slate is not __`exactly new`__ as a work tool .                            |
| **`pcc_eng_08_102.5785_x1644695_03:08-09-10`**  | It 's actually very easy and while not __`exactly new`__ , its use is only catching on .  |
| **`pcc_eng_22_065.7124_x1045933_282:11-12-13`** | Some people thought I was crazy , but that was n't __`exactly new`__ , I was used to it . |
| **`apw_eng_19980527_0746_19:09-10-11`**         | the service _ 1 +1 Communications _ is not __`exactly new`__ , however .                  |


10. _exactly easy_

|                                                | `token_str`                                                                                                                 |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_007.1339_x0099050_17:4-5-6`**    | Her plan was n't __`exactly easy`__ .                                                                                       |
| **`pcc_eng_21_098.4074_x1573697_11:16-17-18`** | One drawback of being an amateur- built site is that the Dirty Tony tour is not __`exactly easy`__ to navigate .            |
| **`pcc_eng_29_004.9107_x0063306_30:6-7-8`**    | Unfortunately , finding parking is n't __`exactly easy`__ and my friend is starting to lose his patience .                  |
| **`pcc_eng_09_097.2061_x1556629_12:12-13-14`** | As you 'll see in the video below , it 's not __`exactly easy`__ to fly this thing .                                        |
| **`pcc_eng_06_021.0750_x0324796_08:19-20-21`** | And those who try to spot them in advance on the company 's website discover that they 're not __`exactly easy`__ to find . |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/...

Samples saved as...
1. `neg_bigram_examples/exactly/exactly_sure_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_cheap_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_surprising_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_subtle_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_fair_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_fun_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_hard_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_clear_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_new_99ex.csv`
1. `neg_bigram_examples/exactly/exactly_easy_99ex.csv`

## 4. *any*

|                 |       `N` |      `f1` |   `adv_total` |
|:----------------|----------:|----------:|--------------:|
| **NEGMIR_any**  |   583,470 |   291,732 |         1,095 |
| **NEGATED_any** | 6,347,364 | 3,173,660 |        16,238 |


|                          |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:-------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
| **NEGany~any_younger**   |   255 |    3.80 |    0.50 |    0.00 |   353.52 |    255 |    127.50 |      127.50 |         1,784 |
| **NEGany~any_nicer**     |    96 |    2.30 |    0.50 |    0.00 |   133.09 |     96 |     48.00 |       48.00 |           642 |
| **NEGany~any_sweeter**   |    58 |    1.49 |    0.50 |    0.00 |    80.41 |     58 |     29.00 |       29.00 |           388 |
| **NEGmir~any_different** |    48 |    1.30 |    0.50 |    0.00 |    66.55 |     48 |     24.00 |       24.00 |         8,644 |
| **NEGany~any_happier**   |   828 |    4.66 |    0.49 |    0.00 | 1,085.12 |    834 |    417.00 |      411.00 |         2,004 |
| **NEGany~any_smarter**   |    89 |    1.94 |    0.49 |    0.00 |   113.78 |     90 |     45.00 |       44.00 |           733 |
| **NEGany~any_easier**    | 1,594 |    4.42 |    0.48 |    0.00 | 1,946.26 |  1,625 |    812.49 |      781.51 |        12,877 |
| **NEGany~any_brighter**  |    63 |    1.37 |    0.48 |    0.00 |    78.42 |     64 |     32.00 |       31.00 |           640 |
| **NEGmir~any_better**    |   380 |    3.27 |    0.47 |    0.00 |   447.88 |    390 |    195.00 |      185.00 |         3,831 |
| **NEGmir~any_worse**     |    87 |    1.66 |    0.47 |    0.00 |    98.47 |     90 |     45.00 |       42.00 |         2,007 |
| **NEGmir~any_easier**    |    61 |    1.23 |    0.47 |    0.00 |    69.61 |     63 |     31.50 |       29.50 |           681 |
| **NEGany~any_worse**     | 1,686 |    3.62 |    0.46 |    0.00 | 1,816.60 |  1,762 |    880.99 |      805.01 |        12,116 |
| **NEGany~any_better**    | 4,719 |    3.59 |    0.44 |    0.00 | 4,753.39 |  5,004 |  2,501.98 |    2,217.02 |        50,827 |
| **NEGany~any_different** |   902 |    3.03 |    0.44 |    0.00 |   905.82 |    957 |    478.50 |      423.50 |        80,643 |


1. _any different_

|                                                | `token_str`                                                                                                                                                                                                                                                       |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_076.4343_x1218654_41:14-15-16`** | In an attempt at showing humility and that the government of Betazed is not __`any different`__ than it 's people , Betazed Prime has released an issue called " The Underwear of Women in Power . "                                                              |
| **`nyt_eng_19970301_0050_6:36-38-39`**         | `` The way I read the Bible , '' said Ted Peters , a professor of systematic theology at Pacific Lutheran Theological Seminary in Berkeley , `` the status of that person before God would not be __`any different`__ from anyone born the old-fashioned way . '' |
| **`nyt_eng_20000222_0298_31:4-5-6`**           | maybe it is n't __`any different`__ .                                                                                                                                                                                                                             |
| **`nyt_eng_19990301_0161_34:3-8-9`**           | it should n't , technically , be __`any different`__ ; it 's just another actor in another scene . ''                                                                                                                                                             |
| **`nyt_eng_19961003_0626_1:22-24-25`**         | Hot dogs and peanuts are mainstays of any baseball game , and the Rangers ' first playoff contest at home wo n't be __`any different`__ .                                                                                                                         |


2. _any younger_

|                                                | `token_str`                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19961216_0697_14:4-6-7`**           | `` People are n't getting __`any younger`__ , so obviously that 's a market . ''                                       |
| **`apw_eng_19980402_1805_29:5-7-8`**           | `` Our clients are not getting __`any younger`__ , and we are running out of time . ''                                 |
| **`pcc_eng_20_087.1215_x1391379_19:14-16-17`** | She had to be in her eighties or nineties and she certainly could n't be __`any younger`__ than that .                 |
| **`apw_eng_20090323_0044_8:4-6-7`**            | `` I 'm not getting __`any younger`__ , '' the 60-year-old told The Associated Press in a recent telephone interview . |
| **`nyt_eng_20070819_0073_11:3-5-6`**           | he 's not getting __`any younger`__ , either , and his miles are piling up .                                           |


3. _any nicer_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_059.4682_x0945278_112:7-8-9`**    | Relationships with the United States were n't __`any nicer`__ either as Kim would still portray the US as the bad guy and George W. Bush referring to North Korea as part of the ' axis of evil ' .                                                                                                                                                                                                    |
| **`pcc_eng_25_082.9038_x1325749_44:24-27-28`**  | Instead of working with a megalomaniac , though , I found him to be this gentle , soft-spoken man , and he could n't have been __`any nicer`__ .                                                                                                                                                                                                                                                       |
| **`pcc_eng_16_036.4489_x0573735_48:4-5-6`**     | The house was n't __`any nicer`__ than ours , but it did have an indoor toilet .                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_26_034.7833_x0546111_004:18-20-21`** | The cities have an abundance of charm , the food is fantastic , and the people could not be __`any nicer`__ .                                                                                                                                                                                                                                                                                          |
| **`pcc_eng_24_028.5471_x0445389_33:62-63-64`**  | After this there is some vain effort of the movie to create a Snow White type story except instead of killing the daughter the stepmother wants to kill the Prince , at which point the movie kills off all of the boyfriends and ends with a cliffhanger where the nice boy , or in this case " the boy who is n't __`any nicer`__ but looks the most like Adam Sandler " is about to kiss the girl . |


4. _any sweeter_

|                                              | `token_str`                                                                                                                                                               |
|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_011.2648_x0166042_3:4-7-8`**   | The feeling could hardly have been __`any sweeter`__ after a victory that required a thrilling second half revival .                                                      |
| **`pcc_eng_08_077.5286_x1239061_7:5-7-8`**   | " The puppy could n't be __`any sweeter`__ or happier .                                                                                                                   |
| **`pcc_eng_00_018.3783_x0280527_24:6-8-9`**  | A deal like this could n't be __`any sweeter`__ .                                                                                                                         |
| **`pcc_eng_29_043.1584_x0680959_030:2-4-5`** | But not really __`any sweeter`__ than New Haarlem or many others that the kids do n't normally wear .                                                                     |
| **`pcc_eng_25_035.3909_x0556716_59:5-6-7`**  | I bet it is n't __`any sweeter`__ than normal Coke or Pepsi , but because the flavor is so odd , we are n't inured to it like we are with stuff we drink all the time . " |


5. _any happier_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_043.3460_x0683882_09:4-6-7`**     | Happy Valley could n't be __`any happier`__ right now for Smith , the former Gateway High School star and coach , who was serving as an assistant coach at Temple until he got a phone call from Franklin .                                                                                                         |
| **`pcc_eng_02_008.1936_x0116018_02:27-30-31`**  | Email OZONE PARK , N.Y. - While Indian Blessing was certainly impressive winning last Saturday 's Breeders ' Cup Juvenile Fillies , trainer Patrick Reynolds could n't have been __`any happier`__ with Backseat Rhythm 's third - place finish in that race .                                                      |
| **`pcc_eng_19_070.3372_x1119818_188:10-12-13`** | If all the houses get 20 percent bigger , nobody is __`any happier`__ than before , especially people at the top .                                                                                                                                                                                                  |
| **`pcc_eng_10_017.6884_x0269580_51:46-47-48`**  | Jackson , Serkis , Cameron and Trumbull have all thrown their considerable weight behind the idea , but Hollywood remains in a state of flux ; traditionalists once decried the switch from film to digital , and blogs around the web suggest that they 're not __`any happier`__ about this new format , either . |
| **`pcc_eng_26_010.0120_x0145673_04:13-15-16`**  | This time he chose to work with Jecht Parker and we could n't be __`any happier`__ about it .                                                                                                                                                                                                                       |


6. _any smarter_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_072.8807_x1161598_13:1-7-8`**     | Not that the good guys are __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                               |
| **`pcc_eng_14_005.3539_x0070580_03:5-6-7`**     | Since I 'm probably not __`any smarter`__ than most of the people reading this column , I need to make sure I supply my readers with information that in one way or another is either uplifting , insightful to some degree , encouraging , entertaining , helpful in some way or emotionally stirring , bringing either a little lump to your throat or a little laugh or snicker ( or at least a smile ) . |
| **`pcc_eng_29_039.4931_x0621544_141:07-12-13`** | Many inventions come from large cities not because city folk are __`any smarter`__ , but because the necessary mix of ideas was in the same place , at the same time .                                                                                                                                                                                                                                       |
| **`pcc_eng_16_024.3102_x0377265_11:07-09-10`**  | The determination to be dour ca n't be __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                   |
| **`pcc_eng_24_108.04689_x1739459_08:3-5-6`**    | You wo n't be __`any smarter`__ .                                                                                                                                                                                                                                                                                                                                                                            |


7. _any brighter_

|                                                  | `token_str`                                                                                                                                                                                                                                                      |
|:-------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_031.6261_x0495715_04:3-5-6`**      | Life could n't be __`any brighter`__ for art dealer Christina Daniels .                                                                                                                                                                                          |
| **`pcc_eng_24_085.9545_x1374105_21:5-6-7`**      | Nationally the picture is n't __`any brighter`__ :                                                                                                                                                                                                               |
| **`pcc_eng_20_085.4477_x1364434_12:42-43-44`**   | Actually , I do n't know my hippocampus from my amygdala , but it 's nice to know that all those mornings I 've sat on my butt wrestling silently with my monkey mind might actually keep me lucid -- if not __`any brighter`__ -- long into my crusty old age . |
| **`pcc_eng_29_093.1157_x1487984_25:1-5-6`**      | Nor is the picture __`any brighter`__ in Scottish retail .                                                                                                                                                                                                       |
| **`pcc_eng_22_107.05830_x1722622_163:13-15-16`** | Despite falling short of a return to the playoffs the future could not be __`any brighter`__ for the Rockets with Steve Francis and Yao Ming forming the foundation of a team that enters a new state of the art arena next season .                             |


8. _any easier_

|                                                | `token_str`                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_065.7207_x1046115_11:3-4-5`**    | It was n't __`any easier`__ to view knowing that there really were people out there who might actually believe him .                                  |
| **`pcc_eng_29_004.8420_x0062172_19:5-8-9`**    | The whole process could n't have been __`any easier`__ .                                                                                              |
| **`pcc_eng_10_084.4541_x1348798_60:3-4-5`**    | Things were n't __`any easier`__ in Washington state .                                                                                                |
| **`pcc_eng_06_103.9841_x1665918_13:11-13-14`** | Getting in for a last minute face care treatment could n't be __`any easier`__ .                                                                      |
| **`nyt_eng_20070413_0223_36:4-5-6`**           | since it is not __`any easier`__ on a patient than a total replacement , he says a patient should have pain every day before even thinking about it . |


9. _any better_

|                                                 | `token_str`                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_002.9019_x0030530_017:09-10-11`** | To tell you the truth , it is n't __`any better`__ today .                                                      |
| **`pcc_eng_11_099.5790_x1595772_22:5-6-7`**     | The scene there was n't __`any better`__ .                                                                      |
| **`pcc_eng_06_076.8771_x1227329_13:4-6-7`**     | Rest days could n't be __`any better`__ , the town of Manang bustles with hordes of trekkers and locals alike . |
| **`pcc_eng_06_078.9387_x1260341_14:6-8-9`**     | Gasol off the bench would not be __`any better`__ than a generic big man .                                      |
| **`pcc_eng_12_007.6860_x0108096_08:3-5-6`**     | He 's not really __`any better`__ than Dent .                                                                   |


10. _any worse_

|                                                 | `token_str`                                                                                                                                                                                                    |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_022.2001_x0342474_006:08-09-10`** | I 'm kind of sore , but not __`any worse`__ than I was yesterday , so I 'm pretty good .                                                                                                                       |
| **`pcc_eng_00_060.8636_x0967830_018:17-18-19`** | Something inside you says , " Well , it was always pretty bad , it 's not __`any worse`__ .                                                                                                                    |
| **`pcc_eng_22_058.5142_x0929813_086:27-29-30`** | They said it was n't really stable -- there 's a lot of sharks and I was like , " I did fashion , it ca n't be __`any worse`__ " -- just kidding !                                                             |
| **`pcc_eng_04_102.3672_x1637602_45:3-5-6`**     | It ca n't be __`any worse`__ anywhere else than what we were , what we were having here , so we got on the draft to Japan and then we went and landed in Nagasaki off this old tub of a ship that we were in . |
| **`pcc_eng_13_080.5317_x1285422_05:17-18-19`**  | Later , the BBC , as expected , did exactly the same , but they were n't __`any worse`__ than ITN .                                                                                                            |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/...

Samples saved as...
1. `neg_bigram_examples/any/any_different_99ex.csv`
1. `neg_bigram_examples/any/any_younger_99ex.csv`
1. `neg_bigram_examples/any/any_nicer_99ex.csv`
1. `neg_bigram_examples/any/any_sweeter_99ex.csv`
1. `neg_bigram_examples/any/any_happier_99ex.csv`
1. `neg_bigram_examples/any/any_smarter_99ex.csv`
1. `neg_bigram_examples/any/any_brighter_99ex.csv`
1. `neg_bigram_examples/any/any_easier_99ex.csv`
1. `neg_bigram_examples/any/any_better_99ex.csv`
1. `neg_bigram_examples/any/any_worse_99ex.csv`

## 5. *remotely*

|                      |       `N` |      `f1` |   `adv_total` |
|:---------------------|----------:|----------:|--------------:|
| **NEGMIR_remotely**  |   583,470 |   291,732 |         1,953 |
| **NEGATED_remotely** | 6,347,364 | 3,173,660 |         6,161 |


|                                |   `f` |   `LRC` |   `dP1` |   `dP2` |   `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:-------------------------------|------:|--------:|--------:|--------:|-------:|-------:|----------:|------------:|--------------:|
| **NEGany~remotely_true**       |   250 |    3.53 |    0.50 |    0.00 | 334.93 |    251 |    125.50 |      124.50 |        34,967 |
| **NEGany~remotely_ready**      |    58 |    1.49 |    0.50 |    0.00 |  80.41 |     58 |     29.00 |       29.00 |        29,583 |
| **NEGmir~remotely_comparable** |    44 |    1.15 |    0.50 |    0.00 |  61.00 |     44 |     22.00 |       22.00 |           158 |
| **NEGany~remotely_enough**     |    47 |    1.13 |    0.50 |    0.00 |  65.16 |     47 |     23.50 |       23.50 |        27,603 |
| **NEGany~remotely_surprising** |    75 |    1.66 |    0.49 |    0.00 |  94.71 |     76 |     38.00 |       37.00 |        18,776 |
| **NEGmir~remotely_true**       |    61 |    1.43 |    0.48 |    0.00 |  75.72 |     62 |     31.00 |       30.00 |         2,850 |
| **NEGany~remotely_funny**      |   137 |    2.16 |    0.47 |    0.00 | 159.09 |    141 |     70.50 |       66.50 |        14,992 |
| **NEGmir~remotely_close**      |   218 |    2.58 |    0.46 |    0.00 | 244.21 |    226 |    113.00 |      105.00 |         4,831 |
| **NEGany~remotely_close**      |   694 |    2.98 |    0.45 |    0.00 | 711.52 |    733 |    366.50 |      327.50 |        46,485 |
| **NEGany~remotely_comparable** |   118 |    1.62 |    0.44 |    0.00 | 119.34 |    125 |     62.50 |       55.50 |         2,401 |
| **NEGany~remotely_interested** |   330 |    1.99 |    0.41 |    0.00 | 278.69 |    364 |    182.00 |      148.00 |        34,543 |
| **NEGany~remotely_similar**    |   152 |    1.39 |    0.40 |    0.00 | 123.97 |    169 |     84.50 |       67.50 |        11,088 |
| **NEGany~remotely_related**    |   146 |    1.33 |    0.40 |    0.00 | 116.95 |    163 |     81.50 |       64.50 |        14,260 |


1. _remotely comparable_

|                                                 | `token_str`                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_061.8666_x0984999_048:12-13-14`** | Apart from the obvious fact that a socialist party newspaper is not __`remotely comparable`__ to a mainstream broadsheet , this is just hyperbolic nonsense .                                                                                                |
| **`pcc_eng_21_090.1352_x1440643_46:2-4-5`**     | , not even __`remotely comparable`__ to revive or garrison .                                                                                                                                                                                                 |
| **`pcc_eng_05_087.5005_x1399656_41:16-18-19`**  | It 's a mistake to equate elections with private-sector performance reviews , because they 're not even __`remotely comparable`__ .                                                                                                                          |
| **`pcc_eng_10_019.2527_x0295016_57:5-6-7`**     | The two situations are n't __`remotely comparable`__ , and in fact I think they differ in at least six key ways :                                                                                                                                            |
| **`pcc_eng_10_075.9474_x1211333_71:4-5-6`**     | " That is not __`remotely comparable`__ to the 5 million Syrians who fled the country in the first five years following the civil war - and that does n't include over a million per year who fled their homes inside Syria ( the internally displaced ) . " |


2. _remotely ready_

|                                                    | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:---------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19980427_0151_37:08-09-10`**            | Mark had finally confessed : He was n't __`remotely ready`__ to be a father .                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_16_052.4669_x0833052_004:103-104-105`** | That a period of almost six months , a big , unprecedented chunk of time to get over the major knee surgery I had back in March ( that feels , in ' reality ' more like six weeks - it has passed so quickly I can hardly believe it ) , and which I thought would feel like an endless , half year sabbatical during which I would achieve all kinds of wonders - but failed to - is coming to a close as the summer ends , and autumn approaches , and the teaching begins , even though I am not __`remotely ready`__ for it to do so . |
| **`pcc_eng_06_102.9020_x1648488_117:3-4-5`**       | I 'm not __`remotely ready`__ to talk about how to talk with kids about sex .                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_07_017.0566_x0259758_096:11-13-14`**    | I had been married less than a year and was n't even __`remotely ready`__ for kids .                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_19_072.8516_x1160639_48:24-25-26`**     | Whether because he spoke out of ego , or because he proposed a new communal and religious structure for which the people were n't __`remotely ready`__ -- Korach erred , and the earth swallowed him up .                                                                                                                                                                                                                                                                                                                                  |


3. _remotely enough_

|                                                 | `token_str`                                                                                                                                                                                              |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_011.3822_x0167616_06:15-16-17`**  | You will probably end up with 39 - 40 % equity , which is n't __`remotely enough`__ to make a profitable call here .                                                                                     |
| **`pcc_eng_20_009.3703_x0135024_13:18-19-20`**  | Given the most generous assumptions of prebiotic chemistry , the Earth 's 4.6 billion year history is not __`remotely enough`__ to account for the string of chance happenings that are needed .         |
| **`nyt_eng_20070720_0143_46:12-13-14`**         | FAIN : We now have 35 ships , and that is n't __`remotely enough`__ to satisfy all the itineraries we 'd like to do .                                                                                    |
| **`pcc_eng_24_102.8076_x1647075_012:26-27-28`** | HINT : If you want to depend as little as possible on this walkthrough , keep a notebook ( a single sheet of paper is not __`remotely enough`__ ) to record what you learn from the people you talk to . |
| **`pcc_eng_13_003.6495_x0042626_44:18-20-21`**  | What happens when your job just keeps on getting harder and harder and the salary increase is n't even __`remotely enough`__ to compensate for the stress you get and the life you waste ?               |


4. _remotely true_

|                                                | `token_str`                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_test_3.01795_x37265_16:34-35-36`**  | This is such a great question because I think there 's a popular perception that all a historian really needs is a great memory for names and dates , which is of course not __`remotely true`__ . |
| **`pcc_eng_11_019.2848_x0295627_02:22-24-25`** | Most people think that a restaurant is the be all and end all of a chef 's career but that is not even __`remotely true`__ .                                                                       |
| **`pcc_eng_09_002.1460_x0018593_20:4-5-6`**    | The same is not __`remotely true`__ here .                                                                                                                                                         |
| **`pcc_eng_25_005.6198_x0075235_09:09-11-12`** | Not surprisingly , this turns out to be not even __`remotely true`__ .                                                                                                                             |
| **`pcc_eng_07_026.4733_x0412048_0270:6-8-9`**  | We know the former is not even __`remotely true`__ , but what about the latter ?                                                                                                                   |


5. _remotely surprising_

|                                                | `token_str`                                                                                                                                                                                 |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_val_2.10616_x33464_17:5-6-7`**      | It 's telling but not __`remotely surprising`__ that Dionne looks to Europe , home of the cradle - to - grave welfare state , as the inspiration for the kind of capitalism he wants here . |
| **`pcc_eng_08_059.9026_x0953880_11:15-16-17`** | That 's roughly in keeping with the first six Dot Music decisions and a not __`remotely surprising`__ result .                                                                              |
| **`pcc_eng_26_036.1169_x0567619_157:3-4-5`**   | This is not __`remotely surprising`__ and proves that the liberal feels far more charitable with other people 's money than he does his own .                                               |
| **`pcc_eng_00_034.7586_x0545419_23:7-8-9`**    | This is , of course , not __`remotely surprising`__ .                                                                                                                                       |
| **`pcc_eng_test_1.1025_x01663_17:5-7-8`**      | The murder victim was n't even __`remotely surprising`__ nor was the murderer .                                                                                                             |


6. _remotely funny_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_21_077.8633_x1242034_08:1-5-6`**    | None of this is __`remotely funny`__ , despite screenwriter Wayne Conley 's resorting to virtually every known stereotype                                                                                                                                                                                                                                          |
| **`pcc_eng_06_107.1522_x1717198_08:25-34-35`** | He only wishes for Bode , currently a head trainer for the village security squad ; all sheep in wooden dog costumes , so few of the gags created by result are even __`remotely funny`__ ; to just find the natural energy his chosen life had been given , and just enjoy the work presented to him , even if the work is just a disappointing endeavor anyway . |
| **`pcc_eng_25_040.3526_x0637005_48:3-5-6`**    | It 's not even __`remotely funny`__ .                                                                                                                                                                                                                                                                                                                              |
| **`pcc_eng_11_099.0101_x1586566_22:12-13-14`** | For the first 30 minutes of the movie , there is nothing __`remotely funny`__ , original or entertaining .                                                                                                                                                                                                                                                         |
| **`pcc_eng_20_041.2821_x0650845_31:1-3-4`**    | Not even __`remotely funny`__ . "                                                                                                                                                                                                                                                                                                                                  |


7. _remotely close_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_068.3546_x1089543_59:3-4-5`**    | It was n't __`remotely close`__ to a full roster .                                                                                                                                                                                                                                                             |
| **`pcc_eng_29_090.0462_x1438292_39:19-20-21`** | My second terror mission ( a Very Difficult ) was a total squad wipe , something I was never __`remotely close`__ to in Normal .                                                                                                                                                                               |
| **`pcc_eng_08_107.2266_x1720081_09:10-12-13`** | ( Seriously , that never happened to me , not even __`remotely close`__ to happening . )                                                                                                                                                                                                                       |
| **`pcc_eng_06_023.8409_x0369740_28:07-09-10`** | There is , for example , nothing even __`remotely close`__ to the sort of intellectual division that occurred during the Vietnam War in which the Kissingers and Bundys were matched by others -- including those the New York Times in 1970 headlined as " 1000 'ESTABLISHMENT ' LAWYERS JOIN WAR PROTEST . " |
| **`pcc_eng_21_092.0065_x1470658_18:12-13-14`** | They may be working very hard at the office , but not __`remotely close`__ to what you did for your business .                                                                                                                                                                                                 |


8. _remotely interested_

|                                                | `token_str`                                                                                                                                                                                        |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_058.7447_x0932637_12:27-29-30`** | Use of the word -- in that specific situation , especially -- would be in keeping with his personality , though , as he tends to not be __`remotely interested`__ in political correctness , etc . |
| **`pcc_eng_25_088.6580_x1418542_21:19-20-21`** | There are fifteen unique artwork sculptures which present an outstanding collection for the art enthusiast or for those not __`remotely interested`__ in art will still find them fascinating .    |
| **`pcc_eng_18_037.3736_x0588488_10:21-22-23`** | Without US assistance , Israel is quite strong enough to take on any combination of Arab armies , which are n't __`remotely interested`__ in such a conflict .                                     |
| **`pcc_eng_05_002.3054_x0021224_100:3-5-6`**   | I 'm not even __`remotely interested`__ . "                                                                                                                                                        |
| **`pcc_eng_04_080.6541_x1286851_117:1-2-3`**   | Not __`remotely interested`__ .                                                                                                                                                                    |


9. _remotely similar_

|                                                 | `token_str`                                                                                                                                                                                                     |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_24_070.9022_x1130710_054:15-17-18`** | That word that has the letter C in the middle of it and is not even __`remotely similar`__ in meaning to the word this woman had said .                                                                         |
| **`nyt_eng_20050112_0364_60:21-22-23`**         | but if you go deeper than this surface comparison , you can see that being a white middle-class person is not __`remotely similar`__ to what African-Americans had to go through in this country , '' he says . |
| **`pcc_eng_25_003.2120_x0036074_37:16-17-18`**  | Glimpses of films like Sarkar and Sarkar Raj , besides Satya and Company , though not __`remotely similar`__ to Rakta Charitra , flash across your mind .                                                       |
| **`pcc_eng_24_100.3273_x1606937_18:11-13-14`**  | It is also called " cruise " but it is not even __`remotely similar`__ to big time cruises .                                                                                                                    |
| **`pcc_eng_06_078.4987_x1253180_06:3-4-5`**     | There 's nothing __`remotely similar`__ .                                                                                                                                                                       |


10. _remotely related_

|                                                 | `token_str`                                                                                                                                       |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_002.3133_x0021241_07:15-16-17`**  | Over time several movies have been released that have the same title that are n't __`remotely related`__ .                                        |
| **`pcc_eng_15_043.0438_x0679735_56:5-6-7`**     | I know this is n't __`remotely related`__ to airport security , but I 'm just saying ...                                                          |
| **`pcc_eng_04_047.1769_x0746320_13:23-25-26`**  | And , of course , there 's always the comment about not mentioning work in field x or y that really is n't even __`remotely related`__ to yours . |
| **`pcc_eng_00_049.0295_x0776243_03:5-6-7`**     | -- Has turned up nothing __`remotely related`__ to " Trump- Russia collusion ; "                                                                  |
| **`pcc_eng_04_059.5522_x0945877_048:15-17-18`** | And , his situation has absolutely nothing to do with Victor , they are not even __`remotely related`__ .                                         |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/...

Samples saved as...
1. `neg_bigram_examples/remotely/remotely_comparable_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_ready_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_enough_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_true_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_surprising_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_funny_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_close_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_interested_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_similar_99ex.csv`
1. `neg_bigram_examples/remotely/remotely_related_99ex.csv`

## 6. *yet*

|                 |       `N` |      `f1` |   `adv_total` |
|:----------------|----------:|----------:|--------------:|
| **NEGATED_yet** | 6,347,364 | 3,173,660 |        53,881 |


|                          |    `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:-------------------------|-------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
| **NEGany~yet_clear**     | 10,406 |    8.66 |    0.50 |    0.00 | 14,392.25 | 10,409 |  5,204.46 |    5,201.54 |        84,227 |
| **NEGany~yet_ready**     |  7,501 |    8.06 |    0.50 |    0.00 | 10,344.81 |  7,505 |  3,752.47 |    3,748.53 |        29,583 |
| **NEGany~yet_complete**  |  2,174 |    6.70 |    0.50 |    0.00 |  2,998.60 |  2,175 |  1,087.49 |    1,086.51 |         8,415 |
| **NEGany~yet_available** |  7,430 |    6.66 |    0.50 |    0.00 |  9,950.03 |  7,461 |  3,730.47 |    3,699.53 |        82,956 |
| **NEGany~yet_sure**      |  1,977 |    6.13 |    0.50 |    0.00 |  2,689.26 |  1,981 |    990.49 |      986.51 |       134,139 |
| **NEGany~yet_certain**   |    866 |    5.60 |    0.50 |    0.00 |  1,200.66 |    866 |    433.00 |      433.00 |        11,334 |
| **NEGany~yet_able**      |  1,315 |    5.44 |    0.50 |    0.00 |  1,764.46 |  1,320 |    660.00 |      655.00 |        23,355 |
| **NEGany~yet_final**     |    640 |    5.16 |    0.50 |    0.00 |    887.30 |    640 |    320.00 |      320.00 |         1,213 |
| **NEGany~yet_public**    |    467 |    4.69 |    0.50 |    0.00 |    647.44 |    467 |    233.50 |      233.50 |         2,656 |
| **NEGany~yet_dead**      |    401 |    4.47 |    0.50 |    0.00 |    555.93 |    401 |    200.50 |      200.50 |         6,348 |


1. _yet clear_

|                                             | `token_str`                                                                                                                                                                                                                     |
|:--------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_25_093.3992_x1495372_12:3-4-5`** | It 's not __`yet clear`__ how the women died , but authorities say they are believed to be have been dead for about a week .                                                                                                    |
| **`pcc_eng_00_069.0951_x1100531_07:3-4-5`** | It 's not __`yet clear`__ whether Hefazat- i- Islam is itself a player or simply a pawn , as the standoff between the government and the opposition continues to spiral violently out of control .                              |
| **`pcc_eng_21_029.4607_x0460080_07:3-4-5`** | It is not __`yet clear`__ whether they intend to try to seek asylum in the United Kingdom                                                                                                                                       |
| **`apw_eng_20090331_0254_2:7-8-9`**         | Dr. Moaiya Hassanain says it is not __`yet clear`__ if the men are civilians or militants .                                                                                                                                     |
| **`pcc_eng_28_048.6729_x0771269_02:3-4-5`** | It is not __`yet clear`__ what kinds of guns were used in the terrorist attack , which occurred in central Christchurch , but authorities have said that a number of firearms were recovered from the scenes of the shootings . |


2. _yet certain_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                    |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_092.4534_x1478089_12:24-25-26`** | " When I arrived at UA , I knew I belonged in the College of Communication and Information Sciences , but I was n't __`yet certain`__ about a major , " Beard admits .                                                                                                                                         |
| **`pcc_eng_24_073.6704_x1175575_11:20-22-23`** | On DC 's latest injury report , the duo were upgraded to questionable , but a specific timeline is n't quite __`yet certain`__ -- Quaranta has missed less time , and said that he could be back in less than two weeks , while Mc Tavish must take a more patient approach .                                  |
| **`pcc_eng_18_082.2076_x1314908_29:3-4-5`**    | Shane is not __`yet certain`__ why this is happening , noting " I do n't have the evidence to evaluate the impact of technological change , a shift in the regulatory environment , different credit conditions or any of the multitude of other factors that policy makers and pundits say is responsible . " |
| **`pcc_eng_11_057.7271_x0917778_12:6-7-8`**    | Daily that his company is n't __`yet certain`__ it will distribute its CBD line of beverages outside the United States , but the deal will provide the infrastructure that would allow it to do so .                                                                                                           |
| **`nyt_eng_19960920_0376_4:6-7-8`**            | and , while it is n't __`yet certain`__ whether Christopher would stay on should Clinton win a second term , a half dozen contenders have emerged to fill the top diplomat 's post if he leaves .                                                                                                              |


3. _yet ready_

|                                                | `token_str`                                                                                                                                                                                    |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_10_058.0193_x0922098_10:11-12-13`** | Lead nurturing focuses on educating qualified sales leads who are not __`yet ready`__ to buy .                                                                                                 |
| **`pcc_eng_09_008.2836_x0117987_07:15-16-17`** | The details of Malaysia 's proposed changes to the RTS Link project is " not __`yet ready`__ " , said Khaw in a written response to a question raised in Parliament on Monday ( 4 November ) . |
| **`pcc_eng_20_005.4583_x0071880_33:5-6-7`**    | I know you are not __`yet ready`__ to name your partners , but can you tell me in general terms where the support for this is coming from ?                                                    |
| **`pcc_eng_03_081.3842_x1301805_18:21-22-23`** | And the fact that you have to ask the second question leads me directly to the conclusion that you 're not __`yet ready`__ to hear the answer to the first .                                   |
| **`pcc_eng_15_006.1874_x0083697_16:13-14-15`** | Renewable energy sources , like solar and advanced biofuels , are simply not __`yet ready`__ to compete with fossil fuels .                                                                    |


4. _yet final_

|                                                 | `token_str`                                                                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_070.8559_x1130196_266:14-15-16`** | Keep in mind that FCC 's decision is still a proposal and is not __`yet final`__ .                                                                     |
| **`pcc_eng_21_013.9104_x0208556_48:10-11-12`**  | If the couple remains separated but the divorce is not __`yet final`__ , they can choose between married filing separately or filing jointly .         |
| **`apw_eng_19980130_1063_2:09-10-11`**          | Ministry spokesman Martin Erdmann said the verdict was not __`yet final`__ , and had no details on how the case was to proceed .                       |
| **`pcc_eng_11_080.5745_x1288063_13:21-22-23`**  | The exception is prisoners who are still appealing -- generally , the more recent cases -- because their convictions are not __`yet final`__ .         |
| **`pcc_eng_11_081.6816_x1305928_17:24-25-26`**  | That is because the Supreme Court held that Ring was not retroactive , meaning it only applied to cases where the conviction was not __`yet final`__ . |


5. _yet public_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_044.2605_x0698871_3:25-26-27`**  | In the speech at Georgetown University , according to individuals briefed on the matter who asked not to be identified because the plan was not __`yet public`__ , Obama will detail a government - wide plan to not only reduce the nation 's carbon output but also prepare the United States for the near-term impacts of global warming . |
| **`pcc_eng_01_093.9012_x1502184_36:18-19-20`** | He also likely received a second payment on Oct. 31 , 2010 -- though those records are not __`yet public`__ .                                                                                                                                                                                                                                 |
| **`pcc_eng_15_032.4341_x0508249_12:27-28-29`** | At the time of the oversight hearing I just mentioned , information about the investigation of the phone records of James Rosen of Fox News was not __`yet public`__ .                                                                                                                                                                        |
| **`pcc_eng_27_057.1924_x0908445_6:15-16-17`**  | The names of the other women invited to the 30 - member board are not __`yet public`__ , Rabbi Weissmann said .                                                                                                                                                                                                                               |
| **`apw_eng_20090728_0093_4:12-13-14`**         | the official spoke on condition of anonymity because the announcement was not __`yet public`__ .                                                                                                                                                                                                                                              |


6. _yet dead_

|                                                | `token_str`                                                                                                                                                                                                                                                                     |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_063.1014_x1004556_288:3-4-5`**   | God is not __`yet dead`__ .                                                                                                                                                                                                                                                     |
| **`pcc_eng_14_092.7366_x1483086_37:52-53-54`** | To do so , he says , would lead to " horrendous " consequences , essentially what he 's been saying since August 2005 at a time when one could arguably make the case that there was no civil war in Iraq and 750 Americans who have since died there were n't __`yet dead`__ . |
| **`pcc_eng_13_043.5441_x0687931_164:6-7-8`**   | He explains that Gar was not __`yet dead`__ , but he could not ...                                                                                                                                                                                                              |
| **`pcc_eng_26_093.7556_x1499995_66:7-8-9`**    | It appears as the academy is not __`yet dead`__ ..                                                                                                                                                                                                                              |
| **`nyt_eng_19980227_0373_29:08-09-10`**        | although Indonesian officials say the plan is not __`yet dead`__ , the tide has turned against the professor .                                                                                                                                                                  |


7. _yet complete_

|                                                | `token_str`                                                                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_089.7386_x1436753_25:5-6-7`**    | While the assessment is not __`yet complete`__ , initial findings can be seen in the Biodiversity Trends Report .                                                        |
| **`pcc_eng_21_092.7563_x1482657_23:28-29-30`** | The open-ended data are not included in this dataset because they were coded by the research team , and the analyses of some of these data were not __`yet complete`__ . |
| **`pcc_eng_22_053.5249_x0848569_031:4-5-6`**   | The pill is not __`yet complete`__ , so the aroma of the pill is illusory .                                                                                              |
| **`pcc_eng_28_020.1643_x0309873_10:09-10-11`** | The underlying control structure for HOX genes is not __`yet complete`__ either .                                                                                        |
| **`pcc_eng_03_043.8172_x0693752_41:16-17-18`** | We remember the aborted from 1973 - 2014 with the knowledge that their number is not __`yet complete`__ .                                                                |


8. _yet sure_

|                                                | `token_str`                                                                                                                                                                                                                                                                       |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_099.7806_x1596422_038:3-4-5`**   | Archaeologists are not __`yet sure`__ of why , but they are leaning towards the fact that artists status was low in the hierarchy so they could never be in front of a higher authority figure , and never be faced towards them .                                                |
| **`pcc_eng_22_052.8540_x0837697_12:17-18-19`** | I 'm not certain she 's ready to hear something like this , and I 'm not __`yet sure`__ I trust her to not react badly to it .                                                                                                                                                    |
| **`pcc_eng_00_063.2387_x1006203_14:4-5-6`**    | " We are not __`yet sure`__ as to the size of the Democratic majority , but we wanted to make sure we had our leadership in place for the new year , " Rigger said .                                                                                                              |
| **`pcc_eng_10_042.6651_x0674168_47:23-24-25`** | " The campaign has yet to find or appoint key local leaders or open a campaign office in the county and is n't __`yet sure`__ which Hamilton County Republican party 's central committee members are allied with the Republican presidential nominee , " reported the Enquirer . |
| **`pcc_eng_17_101.6001_x1626097_13:11-12-13`** | Whilst experts are pleased with the results , they are not __`yet sure`__ if it could be repeated in humans , or if it will help them quit smoking .                                                                                                                              |


9. _yet available_

|                                                | `token_str`                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_011.4346_x0168930_5:16-17-18`**  | ( Complete fourth quarter numbers were only released yesterday , so break - downs are n't __`yet available`__ by industry . )                                                                                                  |
| **`apw_eng_20090412_0619_19:4-5-6`**           | autopsy results are not __`yet available`__ , and investigators declined to say whether they believe the slaying was accidental or deliberate .                                                                                |
| **`pcc_eng_27_020.3301_x0312725_24:09-10-11`** | While it 's good that the shares are n't __`yet available`__ for sale , notice that Facebook itself has effectively purchased the remaining more than 21 million shares at the conversion price of $ 23.21 ( $ 487 million ) . |
| **`pcc_eng_16_040.7515_x0643406_41:28-29-30`** | You 'll also need the Dialog to stream music from the online service Tidal ( the Phantom also supports Deezer and Qoboz , but those services are not __`yet available`__ in the U.S. ) .                                       |
| **`pcc_eng_24_070.1390_x1118313_12:6-7-8`**    | The service , which is not __`yet available`__ or even ready to be demoed by press , is a live TV streaming service , similar to what you see from AT&T 's DIRECTV NOW and Sony's Play Station Vue .                           |


10. _yet able_

|                                                | `token_str`                                                                                                                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_037.2737_x0586478_04:09-10-11`** | Twenty - seven of the new retirees are n't __`yet able`__ to join the AARP , as they are under the age of 50 .                                                                                                                                                                                |
| **`apw_eng_20090917_1428_35:08-09-10`**        | the document concludes that while Iran is not __`yet able`__ to equip its Shahab-3 medium-range missile with nuclear warheads , `` it is likely that Iran will overcome problems , '' noting that `` from the evidence presented to the agency , it is possible to suggest that ...           |
| **`pcc_eng_21_067.7198_x1078185_17:48-49-50`** | While players are required to update to the latest patch as soon as it is released on their current platform , because patches are released at different times for different platforms , it is possible to update one device to a new patch while the other is not __`yet able`__ to update . |
| **`pcc_eng_01_033.0376_x0517809_09:6-7-8`**    | However , the researchers are not __`yet able`__ to pin down whether sleeplessness precedes gray matter loss or the other way around .                                                                                                                                                        |
| **`pcc_eng_03_007.2131_x0100372_020:5-6-7`**   | But those acts were n't __`yet able`__ to get the big sales numbers needed to cross over to the top of the mainstream album charts ( or at least their sales were n't being accurately reported from record stores to the trades to get those results ) .                                     |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/...

Samples saved as...
1. `neg_bigram_examples/yet/yet_clear_99ex.csv`
1. `neg_bigram_examples/yet/yet_certain_99ex.csv`
1. `neg_bigram_examples/yet/yet_ready_99ex.csv`
1. `neg_bigram_examples/yet/yet_final_99ex.csv`
1. `neg_bigram_examples/yet/yet_public_99ex.csv`
1. `neg_bigram_examples/yet/yet_dead_99ex.csv`
1. `neg_bigram_examples/yet/yet_complete_99ex.csv`
1. `neg_bigram_examples/yet/yet_sure_99ex.csv`
1. `neg_bigram_examples/yet/yet_available_99ex.csv`
1. `neg_bigram_examples/yet/yet_able_99ex.csv`

## 7. *immediately*

|                         |       `N` |      `f1` |   `adv_total` |
|:------------------------|----------:|----------:|--------------:|
| **NEGATED_immediately** | 6,347,364 | 3,173,660 |        58,040 |
| **NEGMIR_immediately**  |   583,470 |   291,732 |           564 |


|                                   |    `f` |   `LRC` |   `dP1` |   `dP2` |      `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:----------------------------------|-------:|--------:|--------:|--------:|----------:|-------:|----------:|------------:|--------------:|
| **NEGany~immediately_clear**      | 24,416 |    7.55 |    0.50 |    0.01 | 33,058.44 | 24,488 | 12,243.92 |   12,172.08 |        84,227 |
| **NEGany~immediately_possible**   |  1,000 |    5.40 |    0.50 |    0.00 |  1,360.38 |  1,002 |    501.00 |      499.00 |        30,446 |
| **NEGany~immediately_sure**       |    138 |    2.87 |    0.50 |    0.00 |    191.31 |    138 |     69.00 |       69.00 |       134,139 |
| **NEGany~immediately_reachable**  |    109 |    2.50 |    0.50 |    0.00 |    151.11 |    109 |     54.50 |       54.50 |           350 |
| **NEGany~immediately_certain**    |     70 |    1.80 |    0.50 |    0.00 |     97.04 |     70 |     35.00 |       35.00 |        11,334 |
| **NEGany~immediately_available**  | 21,078 |    5.34 |    0.48 |    0.01 | 25,870.14 | 21,477 | 10,738.43 |   10,339.57 |        82,956 |
| **NEGany~immediately_able**       |    626 |    3.66 |    0.48 |    0.00 |    746.39 |    641 |    320.50 |      305.50 |        23,355 |
| **NEGany~immediately_successful** |    290 |    2.87 |    0.47 |    0.00 |    333.73 |    299 |    149.50 |      140.50 |        31,460 |
| **NEGany~immediately_obvious**    |  2,238 |    3.88 |    0.46 |    0.00 |  2,481.50 |  2,325 |  1,162.49 |    1,075.51 |        22,651 |
| **NEGany~immediately_apparent**   |  2,015 |    3.30 |    0.44 |    0.00 |  2,001.83 |  2,143 |  1,071.49 |      943.51 |         9,798 |
| **NEGmir~immediately_available**  |    162 |    1.34 |    0.38 |    0.00 |    120.41 |    184 |     92.00 |       70.00 |         3,079 |


1. _immediately sure_

|                                                  | `token_str`                                                                                                                                                                                               |
|:-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_108.00204_x1731331_064:12-13-14`** | Due to the closeness of the finish , Denny Hamlin was n't __`immediately sure`__ race won the 2016 Daytona 500 .                                                                                          |
| **`pcc_eng_18_083.2969_x1332643_01:18-19-20`**   | The officer , who was an acquaintance of the well -known traditional healer , said policemen were not __`immediately sure`__ what the smell was as Mbatha walked up to the desk at about 6 pm on Friday . |
| **`apw_eng_20021204_0594_5:09-10-11`**           | spokesmen for the Foreign Ministry said they were not __`immediately sure`__ if the discrepancy was due to a slip of the tongue or if one country was not invited .                                       |
| **`apw_eng_20030214_0107_32:4-5-6`**             | a spokesman was not __`immediately sure`__ which of the shuttle 's tires was found .                                                                                                                      |
| **`nyt_eng_19970620_0363_5:5-6-7`**              | the Goldman official was n't __`immediately sure`__ of Cohen 's old target for the S&P index of 500 stocks , but believed it had been 900 .                                                               |


2. _immediately reachable_

|                                                | `token_str`                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_068.7921_x1095661_30:6-7-8`**    | Ferguson 's old assistant was not __`immediately reachable`__ .                                                                |
| **`pcc_eng_02_096.6577_x1546677_08:5-6-7`**    | Hybrid Air Vehicles was not __`immediately reachable`__ by telephone .                                                         |
| **`pcc_eng_11_083.1162_x1329074_10:17-18-19`** | Soft Bank also declined to comment , while Tiger , its other lead investor , was not __`immediately reachable`__ for comment . |
| **`pcc_eng_28_013.3710_x0200419_5:09-10-11`**  | The U.S. Attorney 's Office in Manhattan was not __`immediately reachable`__ for comment .                                     |
| **`pcc_eng_05_083.3476_x1332698_5:4-5-6`**     | The company was not __`immediately reachable`__ for comment .                                                                  |


3. _immediately certain_

|                                                | `token_str`                                                                                                                                                                                                                   |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_028.7656_x0449158_10:18-19-20`** | Brown said district officials had hoped to resume classes this week , and she said it was n't __`immediately certain`__ if the layoff would add days to the end of the school year .                                          |
| **`pcc_eng_13_038.9102_x0612956_50:3-4-5`**    | It was not __`immediately certain`__ how the Bastrop blaze began but it appeared that two fires merged to form the " monster " fire , Amen said .                                                                             |
| **`pcc_eng_06_079.1498_x1263719_15:19-20-21`** | She has since been identified by the medical examiner 's office , Brunner said , but it was not __`immediately certain`__ whether Raffo was among the 17 victims officially counted among the dead as of Friday .             |
| **`apw_eng_19970417_0626_27:3-4-5`**           | it was not __`immediately certain`__ what impact Moilim 's edict _ contravention of which carries an automatic but undefined prison sentence without benefit of trial _ would have on the islands ' infant tourism industry . |
| **`apw_eng_20080718_1359_5:14-15-16`**         | the casualties were in the area of the crane , but officials were n't __`immediately certain`__ whether they were on the crane or near it , Roecker said .                                                                    |


4. _immediately clear_

|                                               | `token_str`                                                                                                                                                                                                                                   |
|:----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_28_036.2730_x0570397_3:13-14-15`** | The UK - based Syrian Observatory for Human Rights said it was not __`immediately clear`__ whether Monday 's strikes on al- Atarib , a town in a so-called de-escalation zone , had been carried out by Syrian warplanes or those of Russia . |
| **`apw_eng_19970905_0514_3:3-4-5`**           | it was n't __`immediately clear`__ what caused the collapse , but party members said powerful winds _ possibly a tornado _ damaged the structure .                                                                                            |
| **`apw_eng_20020322_0621_3:3-4-5`**           | it was not __`immediately clear`__ whether the bomber had intended to carry out an attack in Israel or at the checkpoint .                                                                                                                    |
| **`apw_eng_20090311_1160_8:13-14-15`**        | the restaurant can reopen as soon as Thursday , but it was not __`immediately clear`__ if it would .                                                                                                                                          |
| **`apw_eng_19970517_0492_13:3-4-5`**          | it was not __`immediately clear`__ what Yeltsin planned to do about Luzhkov 's open opposition , which could encourage other politicians to refuse to submit income declarations of their family members .                                    |


5. _immediately possible_

|                                             | `token_str`                                                                                                                                                     |
|:--------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20020809_0272_8:3-4-5`**         | it was not __`immediately possible`__ to contact either of the groups .                                                                                         |
| **`pcc_eng_14_092.9223_x1486166_26:3-4-5`** | It was not __`immediately possible`__ to verify Afridi 's claims .                                                                                              |
| **`apw_eng_20090412_0198_14:3-4-5`**        | it was not __`immediately possible`__ to verify that report .                                                                                                   |
| **`apw_eng_20030604_0004_4:3-4-5`**         | it was n't __`immediately possible`__ to ascertain the credibility of the man 's claim .                                                                        |
| **`pcc_eng_28_048.9783_x0776262_17:3-4-5`** | It was not __`immediately possible`__ to get a comment from Barrick on how a potential strike could affect construction or whether it could delay the project . |


6. _immediately available_

|                                                | `token_str`                                                                                                                                                                          |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20021120_0828_4:22-23-24`**         | Chan told reporters he could not immediately say how much money his client would get and copies of the ruling were not __`immediately available`__ .                                 |
| **`apw_eng_20081212_1173_7:17-18-19`**         | he was out of the country Friday for a promotional tour for the film and was n't __`immediately available`__ for comment , his representative , Alan Nierob , said .                 |
| **`apw_eng_20020322_0711_3:5-6-7`**            | Kirch 's spokesman was not __`immediately available`__ for comment .                                                                                                                 |
| **`pcc_eng_01_078.1521_x1247455_18:09-10-11`** | A spokesperson for the City of Portland was not __`immediately available`__ for comment .                                                                                            |
| **`apw_eng_19970514_0868_2:6-7-8`**            | details of the fighting were not __`immediately available`__ , but a Defense Ministry statement said 23 soldiers were wounded `` while inflicting heavy casualties on the enemy . '' |


7. _immediately able_

|                                                | `token_str`                                                                                                                                                                                   |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20091126_0247_5:5-6-7`**            | a police official was not __`immediately able`__ to comment .                                                                                                                                 |
| **`pcc_eng_28_018.6471_x0285362_11:29-30-31`** | The prices and demand for such things fluctuate over time , but credit access allows SME 's to be able to obtain such resources even if they are not __`immediately able`__ to pay them off . |
| **`pcc_eng_24_103.1739_x1653027_15:3-4-5`**    | Michener was not __`immediately able`__ to say what the average cost of these procedures would have been in out - of- network facilities that are not being sued by Aetna .                   |
| **`apw_eng_20030512_0656_12:4-5-6`**           | Saudi officials were not __`immediately able`__ to confirm these reports .                                                                                                                    |
| **`pcc_eng_08_047.2963_x0749420_04:3-4-5`**    | Deputies were n't __`immediately able`__ to identify her body .                                                                                                                               |


8. _immediately successful_

|                                                | `token_str`                                                                                                                                                                                               |
|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`apw_eng_20020108_0649_8:20-21-22`**         | attempts to contact Salif Diao , the players ' spokesman and a midfielder at French club Sedan , were n't __`immediately successful`__ .                                                                  |
| **`pcc_eng_11_086.7944_x1388798_34:30-31-32`** | There 's no point in asking a young player to make the switch if they 're going to be dropped or not selected the following year because they were n't __`immediately successful`__ in the first season . |
| **`pcc_eng_13_046.4318_x0734532_04:13-14-15`** | Efforts to reach both Krispy Kreme and Broadstone about the arrangement were not __`immediately successful`__ .                                                                                           |
| **`pcc_eng_21_071.6104_x1141054_09:16-17-18`** | The causes of death were not announced and attempts to contact relatives for comment were not __`immediately successful`__ .                                                                              |
| **`apw_eng_20090324_0028_5:09-10-11`**         | attempts to obtain a comment from Frank were not __`immediately successful`__ Monday .                                                                                                                    |


9. _immediately obvious_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                   |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_048.6359_x0769643_068:15-16-17`** | Machine learning can do things very fast and find pieces of data that are not __`immediately obvious`__ .                                                                                                                                                                                                                                     |
| **`pcc_eng_07_013.4893_x0202356_42:09-11-12`**  | One solution to solve the problem of it not being __`immediately obvious`__ where all your papers appeared is to increase the size of the white background halo , especially at far out zoom levels .                                                                                                                                         |
| **`pcc_eng_14_087.5456_x1398977_16:28-29-30`**  | While most of our companies are mid-sized and in the Midwest , East , and South , 15 % are in the West , where it is n't __`immediately obvious`__ how to segment the sales territories , as seen below in a map of the San Francisco / San Jose region .                                                                                     |
| **`pcc_eng_07_024.0710_x0372990_42:60-61-62`**  | " Esthetique du Mal , " that appears on the face of things to be a rather idiosyncratic choice , and yet he succeeds not only in making the case for that poem itself , often overlooked beside the other , late works , but also finds in it a revisiting of a number of Romanticism 's central but not __`immediately obvious`__ concerns . |
| **`pcc_eng_25_008.5105_x0121808_10:08-09-10`**  | Well , Falcao excepted , it 's not __`immediately obvious`__ why they 're doing so well .                                                                                                                                                                                                                                                     |


10. _immediately apparent_

|                                                 | `token_str`                                                                                                                                                                                                                              |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_22_008.3119_x0118001_02:19-20-21`**  | Medical researchers counting on traditionally indexed bibliographic databases may very well be missing the distilled essence of analysis not __`immediately apparent`__ in tables , figures , and pictures found in scholarly articles . |
| **`pcc_eng_29_095.4200_x1525441_138:12-13-14`** | Soy is more insidious than hemlock because it effects are often not __`immediately apparent`__ .                                                                                                                                         |
| **`pcc_eng_15_012.4335_x0184496_22:5-6-7`**     | Many chronic injuries are not __`immediately apparent`__ , but are still caused by the impact of the crash .                                                                                                                             |
| **`pcc_eng_17_055.6526_x0882981_26:4-5-6`**     | Though it is not __`immediately apparent`__ how long Gordon will be absent , he will not be there for the start due to his ongoing recovery .                                                                                            |
| **`pcc_eng_24_105.0035_x1682716_086:07-09-10`** | The motivation for such behavior is not always __`immediately apparent`__ .                                                                                                                                                              |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/...

Samples saved as...
1. `neg_bigram_examples/immediately/immediately_sure_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_reachable_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_certain_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_clear_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_possible_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_available_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_able_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_successful_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_obvious_99ex.csv`
1. `neg_bigram_examples/immediately/immediately_apparent_99ex.csv`

## 8. *ever*

|                     |       `N` |      `f1` |   `adv_total` |
|:--------------------|----------:|----------:|--------------:|
| **NEGMIR_ever**     |   583,470 |   291,732 |         4,786 |
| **COMPLEMENT_ever** | 6,347,364 | 3,173,552 |        10,870 |
| **NEGATED_ever**    | 6,347,364 | 3,173,660 |        10,870 |


|                         |   `f` |   `LRC` |   `dP1` |   `dP2` |   `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:------------------------|------:|--------:|--------:|--------:|-------:|-------:|----------:|------------:|--------------:|
| **NEGmir~ever_easy**    |   368 |    4.21 |    0.50 |    0.00 | 497.96 |    369 |    184.50 |      183.50 |         7,749 |
| **NEGmir~ever_good**    |   299 |    3.90 |    0.50 |    0.00 | 402.64 |    300 |    150.00 |      149.00 |        13,423 |
| **NEGmir~ever_perfect** |   206 |    3.60 |    0.50 |    0.00 | 285.65 |    206 |    103.00 |      103.00 |         1,303 |
| **NEGmir~ever_simple**  |   206 |    3.60 |    0.50 |    0.00 | 285.65 |    206 |    103.00 |      103.00 |         7,465 |
| **NEGany~ever_simple**  |   211 |    3.28 |    0.50 |    0.00 | 281.20 |    212 |    106.00 |      105.00 |        46,867 |
| **NEGmir~ever_enough**  |   147 |    3.09 |    0.50 |    0.00 | 203.83 |    147 |     73.50 |       73.50 |         1,326 |
| **NEGmir~ever_certain** |   143 |    3.04 |    0.50 |    0.00 | 198.28 |    143 |     71.50 |       71.50 |         1,276 |
| **COM~ever_larger**     |   139 |    2.88 |    0.50 |    0.00 | 192.71 |    139 |     69.50 |       69.50 |         7,453 |
| **NEGmir~ever_wrong**   |   102 |    2.52 |    0.50 |    0.00 | 141.42 |    102 |     51.00 |       51.00 |         8,506 |
| **NEGany~ever_boring**  |    72 |    1.84 |    0.50 |    0.00 |  99.82 |     72 |     36.00 |       36.00 |         3,840 |
| **NEGmir~ever_black**   |    56 |    1.56 |    0.50 |    0.00 |  77.64 |     56 |     28.00 |       28.00 |           646 |
| **NEGmir~ever_right**   |    49 |    1.33 |    0.50 |    0.00 |  67.93 |     49 |     24.50 |       24.50 |         2,038 |
| **COM~ever_closer**     |   279 |    3.52 |    0.49 |    0.00 | 365.82 |    281 |    140.49 |      138.51 |         3,686 |
| **COM~ever_greater**    |   186 |    3.09 |    0.49 |    0.00 | 246.80 |    187 |     93.50 |       92.50 |         6,949 |
| **NEGmir~ever_able**    |   136 |    2.71 |    0.49 |    0.00 | 178.12 |    137 |     68.50 |       67.50 |         1,891 |
| **COM~ever_higher**     |   129 |    2.52 |    0.49 |    0.00 | 168.50 |    130 |     65.00 |       64.00 |        12,992 |
| **NEGany~ever_easy**    |   429 |    3.53 |    0.48 |    0.00 | 525.98 |    437 |    218.50 |      210.50 |       108,923 |
| **COM~ever_deeper**     |    61 |    1.31 |    0.48 |    0.00 |  75.72 |     62 |     31.00 |       30.00 |         1,768 |
| **COM~ever_mindful**    |    52 |    1.04 |    0.48 |    0.00 |  63.56 |     53 |     26.50 |       25.50 |           784 |
| **NEGany~ever_good**    |   331 |    2.52 |    0.45 |    0.00 | 337.56 |    350 |    175.00 |      156.00 |       201,244 |


1. _ever perfect_

|                                              | `token_str`                                                                                                                                                                                                          |
|:---------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_008.9662_x0128549_072:6-8-9`** | Nothing is ever finished , nothing is __`ever perfect`__ , but over and over again the race of men gets another chance to do better than last time , ever and again without end .                                    |
| **`pcc_eng_03_001.9967_x0016168_12:2-4-5`**  | But nothing is __`ever perfect`__ , and the difference is that we 're willing to try .                                                                                                                               |
| **`pcc_eng_19_088.2393_x1409890_159:1-3-4`** | Nothing is __`ever perfect`__ , I said , but that does n't mean things ca n't be good .                                                                                                                              |
| **`pcc_eng_22_057.2517_x0909124_26:1-3-4`**  | Nothing is __`ever perfect`__ or easy .                                                                                                                                                                              |
| **`pcc_eng_01_048.0981_x0761056_24:1-3-4`**  | Nothing is __`ever perfect`__ , but when steps that create value for specific products , allowing continuous flow , the process of reducing effort , time , space , cost , and mistakes , everything falls in line . |


2. _ever simple_

|                                                | `token_str`                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_009.0392_x0130251_17:36-38-39`** | The author even touched on some of the motivations of the hijackers and humanized them , which was an important perspective to include , demonstrating that while some things are wrong regardless of rationalization , nothing is __`ever simple`__ . |
| **`pcc_eng_11_083.1163_x1329077_21:23-25-26`** | In other words , even if we genuinely love someone , the realities of life have a way of reminding us that nothing is __`ever simple`__ ...                                                                                                            |
| **`pcc_eng_29_043.6736_x0689403_20:1-5-6`**    | Nothing in Britain is __`ever simple`__ , is it ?                                                                                                                                                                                                      |
| **`pcc_eng_19_018.4605_x0281750_03:5-6-7`**    | Experiencing family strife is never __`ever simple`__ , yet a skilled family members law lawyer can assist you make essential choices as well as locate a new begin .                                                                                  |
| **`pcc_eng_05_012.4146_x0185066_04:3-4-5`**    | It is n't __`ever simple`__ to outright find a soul mate since most individuals are already aware .                                                                                                                                                    |


3. _ever enough_

|                                                | `token_str`                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_076.8617_x1225337_259:5-7-8`**   | The ones for whom nothing is __`ever enough`__ , no amount of taxation is enough for you crooks !                                                                                                                                                                |
| **`pcc_eng_25_044.3676_x0702147_21:15-18-19`** | In the area of blogging and site- building , at times it feels like nothing is definitely __`ever enough`__ .                                                                                                                                                    |
| **`pcc_eng_11_085.3045_x1364599_50:48-50-51`** | Over the next few weeks , my little sister and I struggled to find closure by trying to remember him , getting a memorial tattoo , making a wreath for his grave on Memorial Day , using his t-shirts to make a quilt , but it 's not really __`ever enough`__ . |
| **`pcc_eng_20_003.7190_x0043610_11:1-6-7`**    | Nothing in this world is __`ever enough`__ , nothing satisfies .                                                                                                                                                                                                 |
| **`pcc_eng_01_104.9836_x1680364_21:3-4-5`**    | Knowledge is rarely __`ever enough`__ to spark change .                                                                                                                                                                                                          |


4. _ever certain_

|                                                | `token_str`                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_049.9734_x0790558_113:3-5-6`**   | Indeed , nothing is __`ever certain`__ in a world where gods and humans live and work together , especially when they often struggle to get along .          |
| **`pcc_eng_07_028.5075_x0444899_07:16-18-19`** | It is highly expected that it will clear the House and Senate , but then nothing is __`ever certain`__ .                                                     |
| **`pcc_eng_00_030.4322_x0475695_70:25-27-28`** | This means that we should do all that we can to be prepared , even if we are not certain it will happen ( nothing is __`ever certain`__ ) .                  |
| **`pcc_eng_20_009.0011_x0129103_26:23-25-26`** | Advancing any view or judgement is a no-no in the evidence - based research sphere , founded on the cardinal acceptance that nothing is __`ever certain`__ . |
| **`pcc_eng_25_036.4378_x0573667_12:3-4-5`**    | I was n't __`ever certain`__ I knew where she was in time and space or to whom she was speaking .                                                            |


5. _ever wrong_

|                                                 | `token_str`                                                                                                                                                                                                                                 |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_098.6038_x1579993_17:1-5-6`**     | Nothing you want is __`ever wrong`__ .                                                                                                                                                                                                      |
| **`pcc_eng_03_084.5045_x1352207_13:34-36-37`**  | He does n't know everybody 's always going around all the time with something wrong and believing they 're exerting great willpower and control to keep other people , for whom they think nothing 's __`ever wrong`__ , from seeing it . " |
| **`pcc_eng_02_030.2370_x0473343_166:22-23-24`** | Whether he makes a decision to lower his pads or juke the defender , his call in those split-second situations is rarely __`ever wrong`__ and has probably contributed to his durability since he usually avoids the big hit .              |
| **`pcc_eng_04_056.5900_x0897805_118:12-14-15`** | the kind of fixed that tries to make things look like nothing was __`ever wrong`__ .                                                                                                                                                        |
| **`pcc_eng_17_046.7373_x0738942_7:08-10-11`**   | According to Page Six -- which is never , __`ever wrong`__ about sports personalities -- Benitez is moving out of their mansion because Seikaly is " partying too hard . "                                                                  |


6. _ever black_

|                                                | `token_str`                                                                                                                                           |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_104.5460_x1675091_08:18-20-21`** | If I 've learnt anything in my twenty six years on the planet , it 's that nothing is __`ever black`__ and white ; there 's infinite shades of grey . |
| **`pcc_eng_14_006.5119_x0089232_18:6-8-9`**    | Dealing with Grey Areas -- nothing is __`ever black`__ and white , and that cannot be truer when referring to people 's workplace habits .            |
| **`pcc_eng_02_007.9015_x0111391_26:11-13-14`** | No one type is better than the other , and nothing is __`ever black`__ and white .                                                                    |
| **`pcc_eng_14_081.2960_x1298217_26:14-16-17`** | And that 's good , since , when it comes to color , nothing is __`ever black`__ and white ( sorry ) .                                                 |
| **`pcc_eng_04_001.0397_x0000636_76:3-4-5`**    | Life is hardly __`ever black`__ and white .                                                                                                           |


7. _ever right_

|                                                 | `token_str`                                                                                                                                                              |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_044.8053_x0707647_04:1-7-8`**     | Nothing I say or do is __`ever right`__ .                                                                                                                                |
| **`pcc_eng_14_005.0123_x0065026_065:08-09-10`** | Just like I believed that mom was never __`ever right`__ or any fun at all -- she was always five fucking hundred million miles away .                                   |
| **`pcc_eng_12_089.0018_x1422001_25:19-20-21`**  | The real paradox here is that we presume we are repairing a damaged system , yet it was never __`ever right`__ from the minute of its creation in 1776 .                 |
| **`pcc_eng_17_044.2931_x0699167_10:14-18-19`**  | Recently , the overseer is awfully hard on Joseph , and thinks that nothing he does is __`ever right`__ , even when he works hard all day long and obeys every command . |
| **`pcc_eng_04_101.6615_x1626258_19:16-20-21`**  | And when she 's down , she believes everyone to be against her and that nothing she does is __`ever right`__ .                                                           |


8. _ever larger_

|                                                 | `token_str`                                                                                                                                                                                                                                                      |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_086.5230_x1381729_45:30-31-32`**  | Because it is clear that a huge part of Croatian civil society ( the one , for example , protesting after the condemnation of Gen. Gotovina ) it is not exactly welcoming the recent engagement of Croatian government in the international relations panorama . |
| **`pcc_eng_24_025.3133_x0393081_127:22-23-24`** | I have n't seen it , but it seems to have one of the strangest endings I 've heard about , not exactly logical .                                                                                                                                                 |
| **`pcc_eng_00_005.3121_x0069634_04:37-38-39`**  | Wool the percentage of silk is much lower , to the touch and the eyesight these two yarns are very similar , soft but not exactly " silky " and shiny , maybe more rustic and not exactly brilliant .                                                            |
| **`pcc_eng_10_021.0029_x0323207_191:13-14-15`** | The downside is we moved away from our families and we 're not that close to them now .                                                                                                                                                                          |
| **`apw_eng_20090116_0100_2:5-7-8`**             | the games themselves were n't all that great , but the promise was there .                                                                                                                                                                                       |


9. _ever boring_

|                                                 | `token_str`                                                                                                 |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_082.7008_x1322278_078:17-18-19`** | I liked the slow burn of the story , which takes it 's time but is n't __`ever boring`__ ( like you say ) . |
| **`pcc_eng_27_064.0342_x1018997_06:6-8-9`**     | Above all , it was never , __`ever boring`__ .                                                              |
| **`pcc_eng_25_013.0080_x0194233_49:2-4-5`**     | Was n't it __`ever boring`__ to play the same five concertos for three years ?                              |
| **`pcc_eng_29_049.7412_x0787069_15:3-5-6`**     | It 's never , __`ever boring`__ and you never know what to expect .                                         |
| **`pcc_eng_21_072.9895_x1163469_11:09-10-11`**  | The novel is a quick read and is n't __`ever boring`__ .                                                    |


10. _ever easy_

|                                              | `token_str`                                                                                                                                                       |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_054.3469_x0863947_27:1-3-4`**  | Nothing is __`ever easy`__ !                                                                                                                                      |
| **`pcc_eng_26_095.5226_x1528574_093:1-3-4`** | Nothing 's __`ever easy`__ .                                                                                                                                      |
| **`pcc_eng_13_096.6026_x1544973_33:1-7-8`**  | Nothing worth doing in life is __`ever easy`__ .                                                                                                                  |
| **`pcc_eng_14_033.9461_x0532243_053:3-4-5`** | It is n't __`ever easy`__ , but I 'm learning to let the creativity win and relax on striving in my art , in whatever form it happens , to be perfect .           |
| **`pcc_eng_07_015.8073_x0239713_09:2-4-5`**  | But nothing is __`ever easy`__ for accident- prone Jory -- and before she knows it , her Summer of Passion falls apart faster than the delivery van she crashes . |


11. _ever good_

|                                                 | `token_str`                                                                                                                                                 |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_032.4022_x0508321_344:10-14-15`** | The partner of this man comes to feel that nothing she does is __`ever good`__ enough and that it is impossible to make him happy .                         |
| **`pcc_eng_19_029.2431_x0455919_37:08-11-12`**  | Nothing good ever comes easy , and nothing easy is __`ever good`__ .                                                                                        |
| **`pcc_eng_01_093.4349_x1494649_31:1-5-6`**     | Nothing they do is __`ever good`__ enough , and she 's certainly never supportive of their goals .                                                          |
| **`pcc_eng_06_106.9825_x1714475_265:08-09-10`** | Not the stupid little brother who was n't __`ever good`__ enough . "                                                                                        |
| **`pcc_eng_23_087.1492_x1392403_24:25-26-27`**  | Lots of people we realize was happy to make an informed choice about their steroid apply , but some get information elsewhere and its not __`ever good`__ . |


12. _ever greater_

|                                                 | `token_str`                                                                                                                                                                                                                            |
|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_06_078.8236_x1258476_018:11-12-13`** | You 'll get one for a little less , is n't that great ?                                                                                                                                                                                |
| **`apw_eng_19981202_0516_3:09-10-11`**          | details about the suspect or his detention were not immediately available .                                                                                                                                                            |
| **`pcc_eng_20_085.8674_x1371182_57:35-36-37`**  | The social and political structures and the expectations for people - of course as far as we understand them - were so different in pre-industrial , pre-capitalist , aristocratic societies that modern terms are not that relevant . |
| **`pcc_eng_18_085.8467_x1373888_03:20-21-22`**  | Putt will prepare to pull up roots for the next phase of her life -- even if she 's not yet sure what parts of her high school experience she 'll bring with her .                                                                     |
| **`pcc_eng_06_023.0668_x0357122_21:08-09-10`**  | General manager Ryan Grigson said he was not yet certain how the rest of the coaching duties would be split up , though he expected all of the assistants to pitch in .                                                                |


13. _ever closer_

|                                                | `token_str`                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_003.1173_x0034143_07:18-20-21`** | I 've eaten there a few times and the food is always great , but I 've never been that impressed with the beer they have brewed in house .                                                                                   |
| **`pcc_eng_14_031.3349_x0490203_33:08-09-10`** | Although the Super Fruit Mud Mask is n't that pleasant to use , and quite messy to remove too , I loved the results .                                                                                                        |
| **`apw_eng_20020321_1543_9:17-18-19`**         | February revenue figures for casinos in Nevada , home to Las Vegas and Reno , are not yet available , but that state 's gambling halls had their worst month in 20 years in January .                                        |
| **`pcc_eng_25_086.3400_x1381149_08:3-4-5`**    | It is not exactly clear if the home of the candidate and that of the spouse are one and the same or whether the two maintain separate residences , however , for reasons hereinafter stated the outcome should be the same . |
| **`pcc_eng_test_1.5415_x08683_016:08-09-10`**  | Three kinds of creation there , is n't that nice ?                                                                                                                                                                           |


14. _ever able_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20061215_0054_40:20-22-23`**         | both finished well below expectations in the Iowa caucus , the first nominating event of the season , and neither was __`ever able`__ to recover .                                                                                                                                                                                                                                                                                                                       |
| **`pcc_eng_24_025.9371_x0403126_59:81-82-83`**  | The last " solution " to the world 's " shitholes " is the passive one that 's been employed since time immemorial , and that 's migrants sacrificing their living standards by knowingly accepting that they 'll likely spend the rest of their lives in suboptimal social conditions in order to give their descendants that are born there a " better chance " at " climbing the ladder ' and " succeeding " in ways that their parents were n't __`ever able`__ to . |
| **`pcc_eng_20_086.8393_x1386806_086:11-12-13`** | The law was like a teacher to prove we are not __`ever able`__ to meet God 's righteous requirements . "                                                                                                                                                                                                                                                                                                                                                                 |
| **`pcc_eng_09_033.9889_x0534089_22:26-29-30`**  | I had the Hoth playset when I was little and loved playing with it , but I could never remember exactly what it was called nor was I __`ever able`__ to find info about it ( apparently my Google skills need work ) .                                                                                                                                                                                                                                                   |
| **`pcc_eng_10_047.5556_x0753258_094:10-11-12`** | I used to lament to him how I was n't __`ever able`__ to go back to Yankee Stadium after Thurman 's death .                                                                                                                                                                                                                                                                                                                                                              |


15. _ever higher_

|                                                 | `token_str`                                                                                                                                                                                                                                               |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_test_3.03548_x40106_100:3-4-5`**     | I was n't that keen on using it to begin with , but one of my friends kept pushing me to get on it and now I enjoy it .                                                                                                                                   |
| **`pcc_eng_20_007.5723_x0105930_10:39-40-41`**  | Though by most accounts his methods were brutal and sadistic ( for example , slowly impaling his enemies on stakes , drawing and quartering them , burning them to death , etc. ) , in reality they were not particularly cruel or unusual for the time . |
| **`pcc_eng_02_008.7860_x0125636_151:20-21-22`** | Next , even though I can certainly notice the jumps in reasoning you come up with , I am not necessarily certain of just how you seem to unite your details that produce your conclusion .                                                                |
| **`pcc_eng_15_014.7269_x0221554_097:12-13-14`** | A few months ago I made a donation that just was n't that efficient .                                                                                                                                                                                     |
| **`nyt_eng_20071028_0124_48:08-09-10`**         | having realized that obtaining viewer-created content is not that easy , Current is positioning the television network as an incentive for online participation .                                                                                         |


16. _ever deeper_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_006.2279_x0084646_074:11-13-14`** | pull my trigger bang every time you miss I do not deep __`ever deeper`__ inside my finger always strikes does n't lie I know about hiding living in the shadows breaking with the glass every moment getting way too close spending my time getting lost going deep in the darkness keep my secrets never forget No regrets |


17. _ever mindful_

|                                                | `token_str`                                                                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_11_066.1557_x1054572_71:3-4-5`**    | It is n't that awful , really .                                                                                                                                        |
| **`pcc_eng_06_073.4511_x1171981_07:13-14-15`** | Duty free is rather a misnomer nowadays as the goods there are seldom any cheaper than may find in a good department store at home .                                   |
| **`pcc_eng_21_077.9337_x1243205_02:3-4-5`**    | I 'm not exactly sure what you 're asking .                                                                                                                            |
| **`pcc_eng_27_053.3513_x0846150_5:32-34-35`**  | The team does n't yet know when Cobbs will be able to return - whether it will only take a few days to heal or longer - so the situation is n't yet necessarily dire . |
| **`pcc_eng_25_037.3608_x0588540_50:09-10-11`** | Mail is annoying to me , but really not that important in the scheme of things                                                                                         |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/...

Samples saved as...
1. `neg_bigram_examples/ever/ever_perfect_99ex.csv`
1. `neg_bigram_examples/ever/ever_simple_99ex.csv`
1. `neg_bigram_examples/ever/ever_enough_99ex.csv`
1. `neg_bigram_examples/ever/ever_certain_99ex.csv`
1. `neg_bigram_examples/ever/ever_wrong_99ex.csv`
1. `neg_bigram_examples/ever/ever_black_99ex.csv`
1. `neg_bigram_examples/ever/ever_right_99ex.csv`
1. `neg_bigram_examples/ever/ever_larger_99ex.csv`
1. `neg_bigram_examples/ever/ever_boring_99ex.csv`
1. `neg_bigram_examples/ever/ever_easy_99ex.csv`
1. `neg_bigram_examples/ever/ever_good_99ex.csv`
1. `neg_bigram_examples/ever/ever_greater_99ex.csv`
1. `neg_bigram_examples/ever/ever_closer_99ex.csv`
1. `neg_bigram_examples/ever/ever_able_99ex.csv`
1. `neg_bigram_examples/ever/ever_higher_99ex.csv`
1. `neg_bigram_examples/ever/ever_deeper_99ex.csv`
1. `neg_bigram_examples/ever/ever_mindful_99ex.csv`

## 9. *particularly*

|                             |       `N` |      `f1` |   `adv_total` |
|:----------------------------|----------:|----------:|--------------:|
| **NEGMIR_particularly**     |   583,470 |   291,732 |        10,029 |
| **COMPLEMENT_particularly** | 6,347,364 | 3,173,552 |        76,162 |
| **NEGATED_particularly**    | 6,347,364 | 3,173,660 |        76,162 |


|                                     |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:------------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
| **NEGany~particularly_religious**   |   485 |    4.52 |    0.50 |    0.00 |   659.41 |    486 |    243.00 |      242.00 |         3,507 |
| **NEGmir~particularly_new**         |   404 |    4.35 |    0.50 |    0.00 |   547.73 |    405 |    202.50 |      201.50 |         4,300 |
| **NEGany~particularly_wrong**       |   218 |    3.56 |    0.50 |    0.00 |   302.22 |    218 |    109.00 |      109.00 |        21,332 |
| **NEGmir~particularly_wrong**       |   212 |    3.39 |    0.50 |    0.00 |   282.64 |    213 |    106.50 |      105.50 |         8,506 |
| **NEGmir~particularly_surprising**  |   166 |    3.27 |    0.50 |    0.00 |   230.18 |    166 |     83.00 |       83.00 |         1,248 |
| **COM~particularly_acute**          |   135 |    2.84 |    0.50 |    0.00 |   187.16 |    135 |     67.50 |       67.50 |         1,038 |
| **NEGany~particularly_athletic**    |   108 |    2.49 |    0.50 |    0.00 |   149.72 |    108 |     54.00 |       54.00 |         1,772 |
| **NEGany~particularly_likeable**    |   106 |    2.46 |    0.50 |    0.00 |   146.95 |    106 |     53.00 |       53.00 |           861 |
| **NEGmir~particularly_original**    |    90 |    2.33 |    0.50 |    0.00 |   124.78 |     90 |     45.00 |       45.00 |           715 |
| **NEGany~particularly_radical**     |    79 |    1.99 |    0.50 |    0.00 |   109.52 |     79 |     39.50 |       39.50 |         2,637 |
| **NEGmir~particularly_novel**       |    54 |    1.50 |    0.50 |    0.00 |    74.87 |     54 |     27.00 |       27.00 |           179 |
| **NEGmir~particularly_religious**   |    53 |    1.47 |    0.50 |    0.00 |    73.48 |     53 |     26.50 |       26.50 |           337 |
| **NEGany~particularly_flashy**      |    57 |    1.46 |    0.50 |    0.00 |    79.02 |     57 |     28.50 |       28.50 |         1,732 |
| **NEGmir~particularly_innovative**  |    47 |    1.26 |    0.50 |    0.00 |    65.16 |     47 |     23.50 |       23.50 |           675 |
| **NEGmir~particularly_comfortable** |    44 |    1.15 |    0.50 |    0.00 |    61.00 |     44 |     22.00 |       22.00 |         1,888 |
| **NEGany~particularly_new**         |   747 |    4.61 |    0.49 |    0.00 |   982.49 |    752 |    376.00 |      371.00 |        21,538 |
| **NEGany~particularly_original**    |   360 |    3.64 |    0.49 |    0.00 |   460.59 |    364 |    182.00 |      178.00 |         4,693 |
| **NEGmir~particularly_unusual**     |   170 |    2.72 |    0.48 |    0.00 |   209.60 |    173 |     86.50 |       83.50 |           933 |
| **NEGany~particularly_surprising**  | 1,069 |    3.93 |    0.47 |    0.00 | 1,260.26 |  1,097 |    548.50 |      520.50 |        18,776 |
| **NEGmir~particularly_good**        |   390 |    3.24 |    0.47 |    0.00 |   455.35 |    401 |    200.50 |      189.50 |        13,423 |


1. _particularly surprising_

|                                                | `token_str`                                                                                                                                                                                                                                                 |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_08_079.5631_x1272160_27:3-4-5`**    | It is not __`particularly surprising`__ that Sessions , along with other members of the Republican party who sat on the Senate Environmental and Public Works Committee Hearing on Monday , attempted to challenge the science of man-made climate change . |
| **`pcc_eng_20_083.3349_x1330355_03:14-15-16`** | Senate Majority Leader Mitch Mc Connell told Fox News he had learned " nothing __`particularly surprising`__ , " but declined to go into detail .                                                                                                           |
| **`pcc_eng_06_079.6601_x1271895_04:5-6-7`**    | So , it 's not __`particularly surprising`__ that when I came across this infographic on Fast Co. Design comparing the cost of ivy league higher education and incarceration , I took pause .                                                               |
| **`pcc_eng_26_088.7240_x1418621_21:4-5-6`**    | This really is n't __`particularly surprising`__ , the problem has never been language until it was used as a weapon .                                                                                                                                      |
| **`pcc_eng_12_085.2809_x1361838_06:24-25-26`** | Given that Trump 's entire campaign can seen as an endorsement of racism , xenophobia , and general bigotry , this was also not __`particularly surprising`__ .                                                                                             |


2. _particularly original_

|                                                 | `token_str`                                                                                                                                                                  |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_19971217_0791_3:3-4-5`**             | there 's nothing __`particularly original`__ about the subject , a television perennial , but the program has its moments via the hidden camera .                            |
| **`pcc_eng_28_020.4107_x0313816_11:5-6-7`**     | Though his words were n't __`particularly original`__ or poetic , they still reverberated through me .                                                                       |
| **`nyt_eng_19990209_0064_32:6-7-8`**            | so these characters that are n't __`particularly original`__ plod through the book doing things that also are n't __`particularly original`__ and definitely are n't funny . |
| **`pcc_eng_11_094.7945_x1518423_258:17-18-19`** | RB : You suggest that Kaczynski 's thinking -- which you characterize as mediocre -- is not __`particularly original`__ .                                                    |
| **`pcc_eng_13_002.1320_x0018182_32:7-8-9`**     | " This is pretty cool but not __`particularly original`__ .                                                                                                                  |


3. _particularly novel_

|                                                | `token_str`                                                                                                                                                   |
|:-----------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20000602_0053_10:3-4-5`**           | there is nothing __`particularly novel`__ about that .                                                                                                        |
| **`pcc_eng_17_104.7004_x1676346_31:10-11-12`** | Sadly , the plot in A Dirty Carnival is not __`particularly novel`__ , at least not worthy of a remake .                                                      |
| **`pcc_eng_23_006.9388_x0095981_05:11-13-14`** | Setting a game in the theatre of modern war may not be __`particularly novel`__ anymore , but for EA 's long-running Medal of Honor franchise it 's a first . |
| **`pcc_eng_00_064.3182_x1023716_003:1-2-3`**   | Nothing __`particularly novel`__ about this porno scene -- it 's a standard - issue boy-girl vignette .                                                       |
| **`pcc_eng_18_088.4356_x1415955_520:1-6-7`**   | Nothing the authors say is __`particularly novel`__ or earth- shattering , which is part of its brilliance .                                                  |


4. _particularly religious_

|                                              | `token_str`                                                                                                                                                                                                                                                                                          |
|:---------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_013.9788_x0209418_46:3-4-5`**  | There 's nothing __`particularly religious`__ about the film .                                                                                                                                                                                                                                       |
| **`nyt_eng_20070501_0188_35:4-6-7`**         | his parents had not been __`particularly religious`__ , he said , a pattern typical among Pakistani immigrants to Britain where the new generation , often turned off by what they see as the loose morals of binge drinking and broken marriages , has proven to be more devout than their elders . |
| **`pcc_eng_02_086.8430_x1387869_28:1-5-6`**  | Not because I am __`particularly religious`__ , but those stories help him understand that being compasionate is actually something to value .                                                                                                                                                       |
| **`pcc_eng_18_005.5493_x0073752_25:7-8-9`**  | Whilst many of the members are n't __`particularly religious`__ , all feel strongly affiliated to their Jewish roots and find that they have an instant connection to other Jewish lesbians .                                                                                                        |
| **`pcc_eng_20_006.0688_x0081621_007:7-8-9`** | The first is that I am not __`particularly religious`__ .                                                                                                                                                                                                                                            |


5. _particularly innovative_

|                                                 | `token_str`                                                                                                                                                                                                                                                   |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20070611_0101_44:3-4-5`**            | there 's nothing __`particularly innovative`__ about this new drama , but Treat Williams is always , well , a treat .                                                                                                                                         |
| **`pcc_eng_11_081.8802_x1309098_70:08-09-10`**  | The core of Shadow of Mordor is n't __`particularly innovative`__ , but its improvements on well - worn ideas , combined with a system that gives an initially unremarkable world life , makes it one of the most memorable gaming experiences you can have . |
| **`pcc_eng_19_012.9580_x0193242_34:5-6-7`**     | The overarching narrative is not __`particularly innovative`__ in content , but it smartly uses the constrained formats to tell a human story through screens , knobs , and disembodied voices .                                                              |
| **`pcc_eng_13_003.1290_x0034158_134:7-8-9`**    | The look of the show is not __`particularly innovative`__ , in fact it looks like many sci-fi thrillers , but overall it still nice .                                                                                                                         |
| **`pcc_eng_15_049.0413_x0776660_054:14-15-16`** | Microsoft spends billions on research and development , yet is widely regarded as not __`particularly innovative`__ .                                                                                                                                         |


6. _particularly comfortable_

|                                                | `token_str`                                                                                                                                                                                                                               |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_07_053.9963_x0856607_34:22-23-24`** | " When I look at the Republican Party these days and who the quote ' leaders ' are , I 'm not __`particularly comfortable`__ that they 're reflecting the values of conservatives , " Santorum said in a recent interview with ABC News . |
| **`pcc_eng_22_010.0520_x0145936_18:5-6-7`**    | However , I was not __`particularly comfortable`__ with our internal capabilities to conduct a major investigation .                                                                                                                      |
| **`nyt_eng_20071015_0013_8:4-5-6`**            | `` I 'm not __`particularly comfortable`__ in that setting , but whatever . ''                                                                                                                                                            |
| **`nyt_eng_19961011_0079_29:4-5-6`**           | `` I 'm not __`particularly comfortable`__ getting companies listed in every corner of the globe , '' said Tina So , who manages about $ 24 million in China funds at Schroder Investment Management -LRB- Asia -RRB- Ltd. in Hong Kong . |
| **`pcc_eng_23_003.3323_x0037537_3:3-4-5`**     | I am not __`particularly comfortable`__ in bars or clubs .                                                                                                                                                                                |


7. _particularly acute_

|                                                 | `token_str`                                                                                                                 |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_04_042.8683_x0676535_07:3-4-5`**     | That 's not exactly conducive toward getting promoted or receiving a decent raise , and you could get fired as a result .   |
| **`apw_eng_19981222_0527_3:3-4-5`**             | it was not immediately clear exactly how many pensioners held shares in tickets for the winning number _ 21856 .            |
| **`apw_eng_19981013_0209_7:7-8-9`**             | the status of future talks was not immediately clear .                                                                      |
| **`pcc_eng_29_004.8880_x0062917_19:3-4-5`**     | It was not immediately clear whether those on the boat that capsized Wednesday were migrants fleeing their home countries . |
| **`pcc_eng_03_083.4731_x1335597_193:12-13-14`** | As much as I do like appreciate Durian , these were n't that bad and I can totally see why every table orders them .        |


8. _particularly wrong_

|                                             | `token_str`                                                                                                                                                                                    |
|:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_052.0589_x0824923_09:4-5-6`** | While there 's nothing __`particularly wrong`__ with a brochure site , there 's the possibility for so much more .                                                                             |
| **`pcc_eng_27_023.2748_x0360107_03:4-5-6`** | While there is nothing __`particularly wrong`__ with this format , some might consider that another format is better suited for what they require .                                            |
| **`pcc_eng_12_063.1209_x1004463_07:3-4-5`** | There 's nothing __`particularly wrong`__ with writing a story about monsters where the monsters are analogies for the fears and worries we have about growing up .                            |
| **`pcc_eng_13_087.3289_x1395305_34:3-4-5`** | There 's nothing __`particularly wrong`__ with him but you 'd expect a team like Chelsea to lock up their fourth-choice central midfielder before Deadline Day and perhaps at a better price . |
| **`pcc_eng_06_029.6283_x0463180_09:3-4-5`** | There 's nothing __`particularly wrong`__ with this line of reasoning but there may be a subtle reason why it 's unlikely to be successful ( apart from the ordinary reasons ) .               |


9. _particularly athletic_

|                                                 | `token_str`                                                                                                                                                                                                                                                         |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_031.8316_x0499044_2:2-3-4`**      | Although not __`particularly athletic`__ at a young age , his parents signed him up for all sorts of physical activities , such as swimming , running track , sambo and even a little bit of gymnastics .                                                           |
| **`pcc_eng_03_040.1517_x0634339_43:6-8-9`**     | Mental Note : I 've never been __`particularly athletic`__ , but come on .                                                                                                                                                                                          |
| **`pcc_eng_12_067.8447_x1080213_202:6-7-8`**    | Hes 6 - 7 , not __`particularly athletic`__ , and has just an average skill - set offensively as far as his position in the NBA is concerned .                                                                                                                      |
| **`pcc_eng_19_074.6295_x1189468_076:28-29-30`** | Gomez has a plus arm and third base and his hands are fine for the position , but he 's already a large human being and is n't __`particularly athletic`__ , so he will have to improve his footwork and agility to stick at third and avoid a move to first base . |
| **`pcc_eng_13_007.6438_x0107241_008:6-7-8`**    | Shanahan , 50 , and not __`particularly athletic`__ , easily handled the hikes .                                                                                                                                                                                    |


10. _particularly likeable_

|                                                | `token_str`                                                                                                                                                                                                                    |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_14_082.3593_x1315203_21:11-12-13`** | However , that said as their partners and friends were not __`particularly likeable`__ either it was at times hard to really care .                                                                                            |
| **`pcc_eng_13_001.4499_x0007177_25:26-27-28`** | The main character -- here , Andrea , a 40 - something single woman struggling with meaning and alcohol in New York - - is not __`particularly likeable`__ , though her actions are understandable and generally sympathetic . |
| **`pcc_eng_04_101.2489_x1619564_146:2-3-4`**   | Characters not __`particularly likeable`__ or sympathetic , plot non-existent , too many and not very interesting or clever jewish jokes .                                                                                     |
| **`pcc_eng_18_033.1710_x0520799_057:4-5-6`**   | Both characters are n't __`particularly likeable`__ , but the actors playing them are so it certainly supports Fellini and Woody Allen 's ideas that casting was more than half the battle when making a film .                |
| **`pcc_eng_21_025.4152_x0394502_31:6-7-8`**    | Most of the characters are n't __`particularly likeable`__ , but they are n't ones you despise either .                                                                                                                        |


11. _particularly radical_

|                                                 | `token_str`                                                                                                                                                                                                      |
|:------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_01_099.3235_x1589505_12:3-4-5`**     | There 's nothing __`particularly radical`__ about these statistics .                                                                                                                                             |
| **`pcc_eng_22_004.1462_x0051002_132:3-4-5`**    | Even a not __`particularly radical`__ report last year from the home affairs select committee , recommending reform and the possibility of decriminalising cannabis , was speedily dismissed by the government . |
| **`pcc_eng_12_088.8555_x1419625_070:08-09-10`** | Although Russolo 's music and instruments were not __`particularly radical`__ , later interest in the musical potential of noise owed much to his pioneering work .                                              |
| **`pcc_eng_02_032.5647_x0510895_07:1-3-4`**     | None are __`particularly radical`__ ; indeed , each idea simply develops programs and policies decided on by earlier FCC administrations , some of them Republican .                                             |
| **`pcc_eng_05_085.4864_x1367191_29:4-5-6`**     | The story does nothing __`particularly radical`__ with the incarnations of the various characters but winds them together with a modest complexity .                                                             |


12. _particularly flashy_

|                                                 | `token_str`                                                                                                                                       |
|:------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_20_033.6695_x0528216_105:22-23-24`** | Karabacek 's offensive game is more north - south than east-west , which works well for the scoring winger who is not __`particularly flashy`__ . |
| **`pcc_eng_01_068.1664_x1086406_55:09-10-11`**  | Part of it may be that he is n't __`particularly flashy`__ or out spoken .                                                                        |
| **`pcc_eng_25_009.8563_x0143428_06:3-4-5`**     | He 's not __`particularly flashy`__ , but has a combination of skill and intelligence that should lead to a long and successful NFL career .      |
| **`pcc_eng_09_083.8691_x1340636_054:6-7-8`**    | The pas de deux is not __`particularly flashy`__ to watch , but it 's not supposed to be - it 's supposed to be heartbreaking and beautiful .     |
| **`pcc_eng_02_006.2338_x0084607_09:17-18-19`**  | In this chapter , we explore Calendar and Contacts , a pair of apps that are n't __`particularly flashy`__ but can be remarkably useful .         |


13. _particularly new_

|                                                | `token_str`                                                                                                              |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_19_047.4430_x0749645_12:3-4-5`**    | No , not __`particularly new`__ , but still worth saying                                                                 |
| **`pcc_eng_24_078.3478_x1251109_22:12-13-14`** | This shortsighted , bury your head in the sand attitude is not __`particularly new`__ .                                  |
| **`pcc_eng_22_056.7264_x0900503_29:3-4-5`**    | There is nothing __`particularly new`__ about the proposed legislation , nor the timing of its intended implementation . |
| **`pcc_eng_18_017.1544_x0261701_10:08-09-10`** | Here the argument was that cybercrime is nothing __`particularly new`__ :                                                |
| **`pcc_eng_22_060.9413_x0969101_257:3-4-5`**   | There 's nothing __`particularly new`__ about their movement , except that perhaps they are exceptionally rude .         |


14. _particularly unusual_

|                                                 | `token_str`                                                                                                                                                                                     |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_17_076.5539_x1221113_26:12-13-14`**  | But others saw something different : a mushy post that said nothing __`particularly unusual`__ about what it 's like to be in love with someone , but was nonetheless being held up as heroic . |
| **`pcc_eng_10_027.9279_x0435182_36:11-12-13`**  | That up there might look like some very cool but not __`particularly unusual`__ street art .                                                                                                    |
| **`nyt_eng_20050725_0007_6:3-4-5`**             | there is nothing __`particularly unusual`__ about a conservative Republican gravitating to evangelical Christianity , though given his record , his critics were skeptical .                    |
| **`pcc_eng_11_068.4512_x1091839_08:4-5-6`**     | So it 's not __`particularly unusual`__ to have two carriers in the Cent Com area of responsibility , " said Army Lt. Gen. Carter F. Ham , the Joint Chiefs of Staff director for operations .  |
| **`pcc_eng_00_069.2237_x1102570_121:16-17-18`** | But I 've met a lot of smart writers in Hollywood , so that 's not __`particularly unusual`__ .                                                                                                 |


15. _particularly good_

|                                                | `token_str`                                                                                                                                                                                                                                                                            |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_03_031.8192_x0499221_09:26-28-29`** | Except for some positives in employment , such as monthly hiring in April and the very low unemployment claims , the economic news recently has n't been __`particularly good`__ , and it seems to be affecting consumer sentiment .                                                   |
| **`pcc_eng_10_025.5336_x0396356_21:25-26-27`** | According to the Hagberg Consulting Group , which develops training programs for the high tech industry , IT professionals are , generally speaking , not __`particularly good`__ at managing people .                                                                                 |
| **`pcc_eng_28_039.0744_x0615776_26:4-5-6`**    | The optics are n't __`particularly good`__ , so I do n't care about it enough to take it to a professional service place .                                                                                                                                                             |
| **`pcc_eng_17_042.2922_x0666971_12:25-26-27`** | It is also apparent how rapidly the remaining boxes are disappearing , and examination of the images does suggest that the all-wooden boxes were not __`particularly good`__ in terms of their dimensional stability , many showing signs of sagging or twisting before their demise . |
| **`pcc_eng_16_075.2189_x1201055_007:1-6-7`**   | None of these performers were __`particularly good`__ or bad , with the notable exception of the James Franco / Anne Hathaway disaster of last year .                                                                                                                                  |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/...

Samples saved as...
1. `neg_bigram_examples/particularly/particularly_surprising_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_original_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_novel_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_religious_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_innovative_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_comfortable_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_acute_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_wrong_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_athletic_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_likeable_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_radical_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_flashy_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_new_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_unusual_99ex.csv`
1. `neg_bigram_examples/particularly/particularly_good_99ex.csv`

## 10. *terribly*

|                      |       `N` |      `f1` |   `adv_total` |
|:---------------------|----------:|----------:|--------------:|
| **NEGATED_terribly** | 6,347,364 | 3,173,660 |        19,802 |
| **NEGMIR_terribly**  |   583,470 |   291,732 |         2,204 |
| **POSMIR_terribly**  |   583,470 |   291,729 |         2,204 |


|                                 |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:--------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
| **NEGany~terribly_surprising**  |   949 |    5.73 |    0.50 |    0.00 | 1,315.75 |    949 |    474.50 |      474.50 |        18,776 |
| **NEGany~terribly_popular**     |   149 |    2.99 |    0.50 |    0.00 |   206.56 |    149 |     74.50 |       74.50 |        51,120 |
| **NEGany~terribly_unusual**     |   146 |    2.96 |    0.50 |    0.00 |   202.40 |    146 |     73.00 |       73.00 |         7,412 |
| **NEGany~terribly_comfortable** |   129 |    2.77 |    0.50 |    0.00 |   178.84 |    129 |     64.50 |       64.50 |        23,908 |
| **NEGany~terribly_bright**      |   117 |    2.61 |    0.50 |    0.00 |   162.20 |    117 |     58.50 |       58.50 |         8,623 |
| **NEGany~terribly_common**      |   105 |    2.45 |    0.50 |    0.00 |   145.56 |    105 |     52.50 |       52.50 |        34,450 |
| **NEGmir~terribly_surprising**  |    67 |    1.85 |    0.50 |    0.00 |    92.89 |     67 |     33.50 |       33.50 |         1,248 |
| **NEGmir~terribly_original**    |    45 |    1.19 |    0.50 |    0.00 |    62.39 |     45 |     22.50 |       22.50 |           715 |
| **NEGany~terribly_interested**  |   486 |    3.98 |    0.49 |    0.00 |   624.89 |    491 |    245.50 |      240.50 |        34,543 |
| **NEGany~terribly_different**   |   366 |    3.93 |    0.49 |    0.00 |   485.33 |    368 |    184.00 |      182.00 |        80,643 |
| **NEGany~terribly_surprised**   |   287 |    3.30 |    0.49 |    0.00 |   361.19 |    291 |    145.50 |      141.50 |        10,157 |
| **NEGmir~terribly_new**         |    69 |    1.64 |    0.49 |    0.00 |    86.57 |     70 |     35.00 |       34.00 |         4,300 |
| **NEGany~terribly_exciting**    |   382 |    3.28 |    0.48 |    0.00 |   456.39 |    391 |    195.50 |      186.50 |        20,233 |
| **NEGmir~terribly_interesting** |    56 |    1.29 |    0.48 |    0.00 |    68.96 |     57 |     28.50 |       27.50 |         3,863 |
| **POS~terribly_wrong**          |   319 |    1.06 |    0.30 |    0.00 |   149.75 |    401 |    200.50 |      118.50 |         8,506 |


1. _terribly surprising_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_087.4091_x1398683_164:1-6-7`**    | None of this should be __`terribly surprising`__ , since it is increasingly clear that Donald Trump , whose actual net worth is unclear , was completely comfortable making money from blatant fraud .                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_21_019.6568_x0301268_044:21-23-24`** | Given CAFC 's history as exceptionally supportive of locking up knowledge and information on the patent side , it would n't be __`terribly surprising`__ if they did so as well on the copyright side ( side note : while , normally , copyright cases should travel up the local appeals court route , since this case started as a patent case , even though it ended up as a copyright case , apparently the appeal still goes to CAFC , the court that hears all patent appeals ) . |
| **`pcc_eng_26_094.9685_x1519625_01:30-31-32`**  | In retrospect , it should have seemed like the perfect fit and by proxy something that we should have expected so really , the announcement of Scribblenauts while perhaps not __`terribly surprising`__ , is still nonetheless welcome .                                                                                                                                                                                                                                               |
| **`pcc_eng_23_008.1875_x0116084_23:12-13-14`**  | The twists and turns are well marked in advance , so nothing __`terribly surprising`__ arises .                                                                                                                                                                                                                                                                                                                                                                                         |
| **`pcc_eng_27_008.2473_x0116702_06:3-4-5`**     | It is n't __`terribly surprising`__ once you put some thought into it that two Yale Law professors seriously believe in something so dangerous as ethnic determinism .                                                                                                                                                                                                                                                                                                                  |


2. _terribly original_

|                                                  | `token_str`                                                                                                                                                                                         |
|:-------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_00_068.6102_x1092658_02:20-21-22`**   | Alice Blanchard drags the readers into the pit with A Breath After Drowning , a thriller that -- while not __`terribly original`__ -- is as close to perfect as it can get in this genre .          |
| **`pcc_eng_24_108.09517_x1747258_143:08-09-10`** | Naschy 's penning of the screenplay was not __`terribly original`__ .                                                                                                                               |
| **`pcc_eng_16_088.0325_x1408847_017:13-14-15`**  | In its place , a new identity would form that , while not __`terribly original`__ in the context of the times , was nonetheless a much truer vision of who he was .                                 |
| **`nyt_eng_19970624_0673_11:19-20-21`**          | many of the dresses are expected to sell for about $ 15,000 , mostly because their designs were n't __`terribly original`__ .                                                                       |
| **`pcc_eng_04_077.0921_x1229037_11:10-13-14`**   | That 's the key to appreciating this EP : nothing here is __`terribly original`__ , but it 's all executed with such panache and clean- cut expertise that it 's hard not to love it all the same . |


3. _terribly popular_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                          |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`nyt_eng_20060708_0004_25:3-4-5`**           | she was not __`terribly popular`__ with fans .                                                                                                                                                                                                                                                                                       |
| **`apw_eng_20090515_0433_22:30-31-32`**        | `` If you use inflammatory , populist language , '' Baker said in an interview , `` it 's best to use it on organizations or interests that are n't __`terribly popular`__ . ''                                                                                                                                                      |
| **`pcc_eng_21_064.5497_x1026879_27:09-10-11`** | I hear that full- blown computer systems are n't __`terribly popular`__ as Valentine 's Day gifts or Easter egg stuffers this year .                                                                                                                                                                                                 |
| **`nyt_eng_19970126_0249_27:23-24-25`**        | and as former Sen. Bob Dole can attest , it 's tough to make a case against an incumbent , even a not __`terribly popular`__ one , when voters feel they are better off than they were four years ago .                                                                                                                              |
| **`pcc_eng_18_080.9888_x1295098_35:18-19-20`** | Admittedly the less delusional elements of the Labour party have just about accepted that their leader is not __`terribly popular`__ and that spurning the repeated chances to jettison the Jonah before the good ship Labour glug-glug-glugs into the deepest recesses of the ocean may not have been the wisest course of action . |


4. _terribly unusual_

|                                                | `token_str`                                                                                                                                                                                                                                                      |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_088.5070_x1415033_10:16-17-18`** | Typically periods go on and off for a year or so , so it is n't __`terribly unusual`__ to get your period again -- as I recal that happened to me too and then they stopped altogether .                                                                         |
| **`pcc_eng_23_084.4854_x1349214_250:4-5-6`**   | That actually was n't __`terribly unusual`__ back then since church services could be very long and older children could have seen to their younger brothers and sisters , " Hermione said .                                                                     |
| **`pcc_eng_02_080.7292_x1289143_045:3-4-5`**   | It 's not __`terribly unusual`__ for two people with borderline traits to engage , and regardless of the psycho- babble you may have read elsewhere , anyone who 's done any worthwhile healing work with borderlines would know this !                          |
| **`pcc_eng_07_051.0758_x0809516_18:22-24-25`** | The proceedings have the look and feel of a romantic comedy and the nearly twenty years separating Ruffalo and Knightley would n't be __`terribly unusual`__ for the genre , but the movie does n't take its broken - hearted artists down the path you expect . |
| **`pcc_eng_12_036.4635_x0573649_13:18-19-20`** | The fact that the D block has had only one bid in the first four rounds is n't __`terribly unusual`__ ; several licenses which eventually went in Auction 66 for very substantial sums had very little early - round action .                                    |


5. _terribly comfortable_

|                                                | `token_str`                                                                                                                                                                                                                  |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_18_011.8867_x0176268_34:3-4-5`**    | I 'm not __`terribly comfortable`__ with this fact , this lesson I have learned about myself .                                                                                                                               |
| **`pcc_eng_05_038.9833_x0614842_26:11-12-13`** | ... Clinton has acknowledged in the past that she is n't __`terribly comfortable`__ speaking in public and , therefore , should avoid doing it .                                                                             |
| **`pcc_eng_19_017.6419_x0268452_05:1-2-3`**    | Not __`terribly comfortable`__ for the woman who regularly wears black polyester pants ( we 're getting close to laundry day here ) .                                                                                        |
| **`pcc_eng_20_002.0393_x0016617_10:26-27-28`** | At the moment she 's scampering around behind me on the couch and trying to skootch her way up into my lap , a position not __`terribly comfortable`__ for me when hunching over my Mac on the coffee table in front of me . |
| **`pcc_eng_21_098.9781_x1582907_052:6-7-8`**   | For the leader who is n't __`terribly comfortable`__ communicating , a monthly team meeting or weekly " stand - up " is usually all it takes to field questions and convey what is going on .                                |


6. _terribly bright_

|                                                 | `token_str`                                                                                                                                                                                                             |
|:------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_088.0198_x1406130_055:23-24-25`** | Ryan O'Neal was probably the perfect choice - Kubrick 's , of course - for the title role of an ambitious but not __`terribly bright`__ young Irishman .                                                                |
| **`pcc_eng_02_086.8229_x1387551_59:1-2-3`**     | Not __`terribly bright`__ or brave , Jakob nonetheless blurts out his secret and then some to save a suicidal friend 's life .                                                                                          |
| **`pcc_eng_16_077.6975_x1241212_075:36-37-38`** | In this animated film , a buffoonish lone astronaut ( voiced by Dwayne " The Rock " Johnson ) lands on a planet of green-skinned creatures that hunt him down because they 're paranoid and not __`terribly bright`__ . |
| **`pcc_eng_27_064.1069_x1020130_5:08-09-10`**   | Mahlik is a good kid , though not __`terribly bright`__ .                                                                                                                                                               |
| **`pcc_eng_21_076.8556_x1225847_45:3-5-6`**     | He 's not always __`terribly bright`__ , but he does his best .                                                                                                                                                         |


7. _terribly common_

|                                                | `token_str`                                                                                                                                                                                      |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_083.0861_x1327913_17:20-21-22`** | Photo Credit : [ Wine bottles have fairly narrow mouths , and because of that , spilling is actually not __`terribly common`__ .                                                                 |
| **`pcc_eng_00_040.5015_x0638139_15:3-4-5`**    | It is not __`terribly common`__ to see this happening .                                                                                                                                          |
| **`pcc_eng_18_002.6591_x0027045_3:17-19-20`**  | Of course , if you 're wandering through the woods , a can of soup may not be __`terribly common`__ , but you may find an empty can somewhere with one side still on that you can use for this . |
| **`pcc_eng_20_039.0853_x0615552_27:13-14-15`** | Some of the crossover elements would need reworking , but they were n't __`terribly common`__ in that run anyway .                                                                               |
| **`pcc_eng_12_081.5891_x1302091_25:12-13-14`** | Despite those unique benefits , beers fermented with Champagne yeast are n't __`terribly common`__ .                                                                                             |


8. _terribly different_

|                                                | `token_str`                                                                                                                                                                                                                                |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_23_031.2561_x0488445_20:30-31-32`** | I hope that when we come out on the other side of this mess , and I have faith that we will , and in an America that is not __`terribly different`__ than the one of a couple years ago when we went into this mess .                      |
| **`pcc_eng_01_067.7651_x1079924_040:6-7-8`**   | Overall , this example is n't __`terribly different`__ from the fourth - party ecommerce example I wrote about last June except that example featured hardwired connections between the shopper and the merchant rulesets .                |
| **`pcc_eng_04_040.8214_x0643713_21:36-37-38`** | Sure , it 's not all rainbows and sunshine for the poor , criminals wear tracker bracelets which electrocute them if they feel angry ( so they do n't attack bystanders ) but it 's not __`terribly different`__ to our world .            |
| **`pcc_eng_15_046.3276_x0732863_17:4-5-6`**    | The results are n't __`terribly different`__ to previous surveys .                                                                                                                                                                         |
| **`pcc_eng_25_084.2202_x1346922_18:3-4-5`**    | This is n't __`terribly different`__ from what Checkpoint Asia said last week but the really interesting part is that Bhadrakumar is confident that this is just the beginning and that the gulf between Cairo and Riyadh will only grow : |


9. _terribly interested_

|                                                | `token_str`                                                                                                                                                                                                            |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_12_037.8298_x0595679_19:3-5-6`**    | I 'm not really __`terribly interested`__ in monumentality .                                                                                                                                                           |
| **`nyt_eng_20000623_0266_13:18-19-20`**        | `` It seems like they have their whole clique , '' she said , and she was not __`terribly interested`__ in them .                                                                                                      |
| **`pcc_eng_07_023.9095_x0370377_4:3-5-6`**     | I am not too __`terribly interested`__ in wholesaling to other places as it makes the whole process much more complicated .                                                                                            |
| **`pcc_eng_09_090.9315_x1455145_40:4-5-6`**    | The director is n't __`terribly interested`__ in science fiction .                                                                                                                                                     |
| **`pcc_eng_05_038.2830_x0603626_02:38-40-41`** | I 've heard about cold brew coffee for a long time and heard how great it was but I was also given the impression that making it was a long , painful and difficult process so I never was __`terribly interested`__ . |


10. _terribly surprised_

|                                                 | `token_str`                                                                                                                                                                                                                                                                                            |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_29_083.0224_x1324738_06:15-16-17`**  | Hunter tells us that he predicted Milo would crash and burn and thus is n't __`terribly surprised`__ about any of this .                                                                                                                                                                               |
| **`pcc_eng_16_056.8713_x0904236_223:09-10-11`** | Disappointed that she had n't remembered , but not __`terribly surprised`__ , Severus deftly steered the conversation back to the Dueling Club .                                                                                                                                                       |
| **`nyt_eng_20070702_0135_1:12-19-20`**          | given the conservative bent of this court 's dependable majority , few among the champions of diversity were __`terribly surprised`__ by the disappointing Supreme Court ruling rejecting efforts in Seattle and Louisville , Ky. , to achieve greater diversity and avoid re-segregation of schools . |
| **`pcc_eng_20_008.0238_x0113268_22:4-5-6`**     | " I was n't __`terribly surprised`__ " .                                                                                                                                                                                                                                                               |
| **`nyt_eng_20000720_0356_8:22-23-24`**          | Duncan admitted that he anticipated the Spearman hypothesis would be borne out by neural imaging , and that therefore he was not __`terribly surprised`__ by his results .                                                                                                                             |


11. _terribly new_

|                                                | `token_str`                                                                                                                                      |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_089.5450_x1433538_223:3-4-5`**   | It is not __`terribly new`__ .                                                                                                                   |
| **`pcc_eng_28_076.0342_x1213734_13:10-11-12`** | Unusual shapes and distortion printing of metal sheet is not __`terribly new`__ .                                                                |
| **`pcc_eng_11_015.4366_x0233645_06:4-5-6`**    | Story itself is nothing __`terribly new`__ to those that saw the farming foray that took place on Facebook last year .                           |
| **`nyt_eng_20050125_0046_4:08-09-10`**         | the idea of playing alongside men is n't __`terribly new`__ to a girl who pretended to be a boy in order to play pick-up matches on the street . |
| **`pcc_eng_17_054.1370_x0858613_17:4-5-6`**    | Now this is nothing __`terribly new`__ .                                                                                                         |


12. _terribly interesting_

|                                                 | `token_str`                                                                                                                                                                                                        |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_26_038.1466_x0600580_66:6-7-8`**     | The " how " is not __`terribly interesting`__ but , yes , when I paste in Derby then it 's always when the streets are a bit quieter .                                                                             |
| **`pcc_eng_06_025.1064_x0390187_196:5-6-7`**    | This film itself is nothing __`terribly interesting`__ in Porter 's output .                                                                                                                                       |
| **`pcc_eng_03_008.4319_x0120195_079:23-24-25`** | when you 're in college , those things are exciting to you , as a boring heterosexual person , even if its not __`terribly interesting`__ to even , say , your classmates .                                        |
| **`pcc_eng_24_082.5028_x1318274_11:08-09-10`**  | Even the history of Old Ales is n't __`terribly interesting`__ .                                                                                                                                                   |
| **`pcc_eng_18_039.2074_x0618220_015:30-31-32`** | Though neither considerable in height or volume , the sheer uniqueness of Hraunfossar makes it worth the detour to visit ( neighboring Barnafoss is an added bonus , but not __`terribly interesting`__ itself ) . |


13. _terribly exciting_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_15_016.3055_x0246865_36:16-17-18`** | They 're well - drilled and they do what they do , it 's just not __`terribly exciting`__ .                                                                                                                                                                                                                                                                                                                                                                                        |
| **`pcc_eng_11_007.7543_x0109338_453:7-8-9`**   | And really , while there 's nothing __`terribly exciting`__ about Heilstatten apart from it being yet another horror movie from Germany that is n't just amateur gore hour ( though it features some pretty well done bits of the icky stuff as well ) or an arthouse flick , it works well throughout , keeps its pace up , takes care to make its characters less loathsome than you 'd expect , and seems generally made by people who care about entertaining their audience . |
| **`pcc_eng_11_061.7760_x0983564_34:3-4-5`**    | It was n't __`terribly exciting`__ , which is what I always want it to be , but it was just really , really lovely , which is what I was n't entirely expecting .                                                                                                                                                                                                                                                                                                                  |
| **`pcc_eng_03_035.7740_x0563217_090:3-4-5`**   | There 's nothing __`terribly exciting`__ about Anderson from a fantasy sense , but pitchers who have rotation spots are much better investments than ones who do n't -- and given the Brewers ' dire rotation , it feels inevitable that Anderson just locked one up for at least all of 2016 ( and possibly 2017 as well ) .                                                                                                                                                      |
| **`pcc_eng_14_007.4135_x0103643_11:4-5-6`**    | ( It is not __`terribly exciting`__ , but it gets the job done . )                                                                                                                                                                                                                                                                                                                                                                                                                 |


14. _terribly wrong_

|                                               | `token_str`                                                                                                                                                                    |
|:----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_02_097.6582_x1562714_12:1-2-3`**   | Nothing __`terribly wrong`__ with that .                                                                                                                                       |
| **`pcc_eng_05_082.6438_x1321386_28:3-4-5`**   | There 's nothing __`terribly wrong`__ with the rooms at the Biltmore -- yours will most likely be reasonably clean and reasonably comfortable , and they 're spacious enough . |
| **`pcc_eng_20_090.2569_x1442019_08:3-4-5`**   | There is nothing __`terribly wrong`__ with the story itself .                                                                                                                  |
| **`pcc_eng_27_107.03923_x1720975_47:6-7-8`**  | I mean , there 's nothing __`terribly wrong`__ with it , but I just have such lackluster feelings about it .                                                                   |
| **`pcc_eng_29_035.0517_x0549504_6:17-18-19`** | We saw a lot of fish leave the river Sunday ... and I guess there 's nothing __`terribly wrong`__ with it .                                                                    |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/...

Samples saved as...
1. `neg_bigram_examples/terribly/terribly_surprising_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_original_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_popular_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_unusual_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_comfortable_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_bright_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_common_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_different_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_interested_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_surprised_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_new_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_interesting_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_exciting_99ex.csv`
1. `neg_bigram_examples/terribly/terribly_wrong_99ex.csv`

## 11. *inherently*

|                        |       `N` |      `f1` |   `adv_total` |
|:-----------------------|----------:|----------:|--------------:|
| **NEGATED_inherently** | 6,347,364 | 3,173,660 |         8,614 |
| **NEGMIR_inherently**  |   583,470 |   291,732 |         3,342 |


|                               |   `f` |   `LRC` |   `dP1` |   `dP2` |     `G2` |   `f2` |   `exp_f` |   `unexp_f` |   `adj_total` |
|:------------------------------|------:|--------:|--------:|--------:|---------:|-------:|----------:|------------:|--------------:|
| **NEGany~inherently_wrong**   | 1,639 |    4.25 |    0.48 |    0.00 | 1,956.12 |  1,678 |    838.99 |      800.01 |        21,332 |
| **NEGany~inherently_bad**     |   794 |    3.87 |    0.48 |    0.00 |   953.05 |    812 |    406.00 |      388.00 |       119,509 |
| **NEGany~inherently_illegal** |    59 |    1.26 |    0.48 |    0.00 |    73.01 |     60 |     30.00 |       29.00 |         3,580 |
| **NEGmir~inherently_wrong**   | 1,513 |    3.78 |    0.46 |    0.00 | 1,685.02 |  1,571 |    785.49 |      727.51 |         8,506 |
| **NEGmir~inherently_bad**     |   148 |    1.83 |    0.44 |    0.00 |   144.52 |    158 |     79.00 |       69.00 |         4,790 |
| **NEGany~inherently_evil**    |   358 |    2.12 |    0.41 |    0.00 |   312.23 |    392 |    196.00 |      162.00 |         3,171 |
| **NEGany~inherently_better**  |   144 |    1.46 |    0.41 |    0.00 |   124.46 |    158 |     79.00 |       65.00 |        50,827 |
| **NEGany~inherently_good**    |   283 |    1.46 |    0.36 |    0.00 |   189.85 |    329 |    164.50 |      118.50 |       201,244 |


1. _inherently illegal_

|                                                | `token_str`                                                                                                                                                                                                                                                                        |
|:-----------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_041.5377_x0656194_29:11-12-13`** | It should be noted that game rooms like this are not __`inherently illegal`__ .                                                                                                                                                                                                    |
| **`pcc_eng_04_009.0617_x0130434_11:5-6-7`**    | Personally , I see nothing __`inherently illegal`__ with discrimination by individuals or private companies .                                                                                                                                                                      |
| **`pcc_eng_05_030.8763_x0484001_11:4-5-6`**    | While there 's nothing __`inherently illegal`__ about an arranged marriage .                                                                                                                                                                                                       |
| **`pcc_eng_19_042.3949_x0668324_003:6-7-8`**   | While that practice itself is n't __`inherently illegal`__ because wastewater treatment plants can effectively handle liquid medical waste as they would residential waste , the way hospitals actually do it can get them into serious trouble if they 're not careful or smart . |
| **`pcc_eng_13_037.9169_x0596938_18:5-6-7`**    | Targeted killing is therefore not __`inherently illegal`__ ; after all , it beats the tragically untargeted killing used in the World War II bombings of Dresden , London and Hiroshima .                                                                                          |


2. _inherently bad_

|                                                 | `token_str`                                                                                                                                                                                                                                                  |
|:------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_05_099.7925_x1598054_13:08-09-10`**  | Charter schools are neither inherently good , nor __`inherently bad`__ .                                                                                                                                                                                     |
| **`pcc_eng_23_007.9184_x0111746_75:27-28-29`**  | If you 're referring to the OP , I do n't think he was endorsing the behavior , he was just pointing out that there is nothing __`inherently bad`__ about it existing .                                                                                      |
| **`pcc_eng_09_002.1023_x0017910_107:25-26-27`** | ABC 's Once Upon a Time illustrates this concept with its character background stories which reveal each character 's motivations as neither inherently good nor __`inherently bad`__ .                                                                      |
| **`pcc_eng_11_066.7841_x1064756_49:09-10-11`**  | Care , emotion , and a connection is not __`inherently bad`__ .                                                                                                                                                                                              |
| **`pcc_eng_17_076.5347_x1220790_034:4-5-6`**    | While this is not __`inherently bad`__ , getting started too quickly can be wasteful and set your team up for quick frustration , creating immediate conflict with other ideas about the major product attributes and how to get started on the right path . |


3. _inherently wrong_

|                                                | `token_str`                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|:-----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_034.5098_x0542589_16:31-33-34`** | In another article , he urged the university not to lower the burden of proof in finding accused rapists in violation of university policy , writing that " there is nothing really __`inherently wrong`__ with the University failing to punish an alleged rapist -- regardless of his guilt -- in the absence of adequate certainty , " and adding , " expelling students is probably not going to contribute a great deal toward a rape victim 's recovery . " |
| **`pcc_eng_01_104.0342_x1665071_36:3-4-5`**    | There is nothing __`inherently wrong`__ with this approach .                                                                                                                                                                                                                                                                                                                                                                                                      |
| **`pcc_eng_05_001.8315_x0013490_08:3-4-5`**    | There 's nothing __`inherently wrong`__ with that , but it makes a sandwich significantly harder to balance ; featuring six things is always going to be harder than featuring one thing .                                                                                                                                                                                                                                                                        |
| **`pcc_eng_01_064.1587_x1021522_029:3-4-5`**   | There is nothing __`inherently wrong`__ with this process but achieving the correct results requires consideration by the decision -makers of multiple legal and public policy issues to ensure that all customers of the utility are treated fairly and reasonably .                                                                                                                                                                                             |
| **`pcc_eng_25_092.1321_x1474681_20:3-4-5`**    | There 's nothing __`inherently wrong`__ with slutty , of course .                                                                                                                                                                                                                                                                                                                                                                                                 |


4. _inherently evil_

|                                                | `token_str`                                                                                                                                                                                                  |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_27_007.9444_x0111776_21:09-10-11`** | may be an abomination , pancake mixes are not __`inherently evil`__ .                                                                                                                                        |
| **`pcc_eng_11_062.8418_x1000875_21:3-4-5`**    | Snakes are not __`inherently evil`__ , and are generally beneficial for the environment .                                                                                                                    |
| **`pcc_eng_16_059.5239_x0947530_18:08-09-10`** | " We can say that they are not __`inherently evil`__ , they are not monsters .                                                                                                                               |
| **`nyt_eng_19991208_0231_51:10-11-12`**        | Martin and Klinkenberg both say holiday news updates are n't __`inherently evil`__ .                                                                                                                         |
| **`pcc_eng_07_016.5171_x0251092_34:18-19-20`** | Further , if we mourn the absence of unplanned pregnancies and treat them as something that is n't __`inherently evil`__ , then we can start to be supportive of the women who choose to proceed with them . |


5. _inherently better_

|                                              | `token_str`                                                                                                                                                                         |
|:---------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_09_033.3803_x0524221_104:5-6-7`** | Canadian tar sands are not __`inherently better`__ or safer , quite the opposite , they require the construction of massive and unstable infrastructure that will eventually fail . |
| **`pcc_eng_27_066.3667_x1056718_47:3-4-5`**  | There 's nothing __`inherently better`__ about either system .                                                                                                                      |
| **`pcc_eng_23_081.5559_x1301630_338:1-3-4`** | Nobody is __`inherently better`__ than me .                                                                                                                                         |
| **`pcc_eng_01_047.9519_x0758676_29:3-4-5`**  | There is nothing __`inherently better`__ about being able to remember more things .                                                                                                 |
| **`pcc_eng_15_010.1530_x0147811_48:3-4-5`**  | They are not __`inherently better`__ than the printed books they replace , and they are quickly becoming eclipsed in function by the smartphones most of us carry around .          |


6. _inherently good_

|                                                | `token_str`                                                                                                                                                                                                                                                                |
|:-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`pcc_eng_16_084.8110_x1356573_55:13-14-15`** | " Big data , sophisticated computer algorithms , and artificial intelligence are not __`inherently good`__ or bad , but that does n't mean their effects on society are neutral .                                                                                          |
| **`pcc_eng_18_007.8311_x0110590_11:20-24-25`** | You are always there to aid in times of need , but you are also smart enough to realize not all people are __`inherently good`__ .                                                                                                                                         |
| **`pcc_eng_00_066.3150_x1055808_29:25-26-27`** | On the other hand , Ariely also notes that these factors - the paradox of choice and our tendency towards default options - are not __`inherently good`__ or evil ; we can use them to help us make better decisions as much as they sometimes cause us to make bad ones . |
| **`pcc_eng_13_037.0558_x0582879_04:10-12-13`** | " States rights " , he claimed , were not " __`inherently good`__ . "                                                                                                                                                                                                      |
| **`pcc_eng_16_052.5085_x0833713_13:09-10-11`** | It is important to note that growth is not __`inherently good`__ for a company .                                                                                                                                                                                           |


Saving Samples in /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/...

Samples saved as...
1. `neg_bigram_examples/inherently/inherently_illegal_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_bad_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_wrong_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_evil_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_better_99ex.csv`
1. `neg_bigram_examples/inherently/inherently_good_99ex.csv`

