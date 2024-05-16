```python
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, print_md_table
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.general import PKL_SUFF, confirm_dir, timestamp_today
from source.utils.sample import sample_pickle as sp

K = 9
DATE = timestamp_today()
FOCUS = adjust_assoc_columns(['f', 'E11', 'unexpected_f', 'unexpected_abs_sqrt',
                              'am_p1_given2', 'conservative_log_ratio',
                              'am_log_likelihood', 't_score',
                              'mutual_information', 'am_odds_ratio_disc',
                              'N', 'f1', 'f2', 'l1', 'l2'])
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("display.max_colwidth", 80)

NEG_HITS_PATH = POST_PROC_DIR.joinpath(
    'RBdirect/trigger-bigrams_thr0-001p.35f.pkl.gz')
adv_am = []
while not any(adv_am): 
    try:
        adv_am = pd.read_csv(
            TOP_AM_DIR / f'Top{K}_NEG-ADV_combined.35f-7c_{DATE}.csv').set_index('adv')
    except FileNotFoundError:
        DATE = DATE[:-1]+str(int(DATE[-1])-1)

ALL_HITS_SAMPLE = TOP_AM_DIR.joinpath(
    f'top{K}adv_sample-{K}-hit-tables_{DATE}.pkl.gz')
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
      <th>G2_MIR</th>
      <th>G2_SET</th>
      <th>LRC_MIR</th>
      <th>LRC_SET</th>
      <th>MI_MIR</th>
      <th>MI_SET</th>
      <th>N_MIR</th>
      <th>N_SET</th>
      <th>dP1_MIR</th>
      <th>dP1_SET</th>
      <th>...</th>
      <th>mean_MI</th>
      <th>mean_N</th>
      <th>mean_dP1</th>
      <th>mean_expF</th>
      <th>mean_f1</th>
      <th>mean_f2</th>
      <th>mean_f</th>
      <th>mean_oddsRDisc</th>
      <th>mean_t</th>
      <th>mean_unexpF</th>
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
      <th>exactly</th>
      <td>1,939.47</td>
      <td>214,404.20</td>
      <td>3.51</td>
      <td>5.90</td>
      <td>0.70</td>
      <td>1.28</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.59</td>
      <td>0.67</td>
      <td>...</td>
      <td>0.99</td>
      <td>44,181,417.00</td>
      <td>0.63</td>
      <td>1,231.57</td>
      <td>1,760,088.00</td>
      <td>31,356.50</td>
      <td>604,556.17</td>
      <td>1.50</td>
      <td>110.37</td>
      <td>20,992.43</td>
    </tr>
    <tr>
      <th>necessarily</th>
      <td>1,688.91</td>
      <td>219,003.46</td>
      <td>2.66</td>
      <td>6.23</td>
      <td>0.60</td>
      <td>1.30</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.43</td>
      <td>0.72</td>
      <td>...</td>
      <td>0.95</td>
      <td>44,181,417.00</td>
      <td>0.57</td>
      <td>1,180.93</td>
      <td>1,760,088.00</td>
      <td>29,187.50</td>
      <td>603,705.00</td>
      <td>1.41</td>
      <td>109.88</td>
      <td>20,658.57</td>
    </tr>
    <tr>
      <th>before</th>
      <td>1,080.52</td>
      <td>1,062.13</td>
      <td>5.11</td>
      <td>3.65</td>
      <td>0.83</td>
      <td>1.05</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.84</td>
      <td>0.38</td>
      <td>...</td>
      <td>0.94</td>
      <td>44,181,417.00</td>
      <td>0.61</td>
      <td>35.24</td>
      <td>1,760,088.00</td>
      <td>521.00</td>
      <td>586,969.83</td>
      <td>1.92</td>
      <td>15.29</td>
      <td>265.26</td>
    </tr>
    <tr>
      <th>that</th>
      <td>7,632.21</td>
      <td>781,016.11</td>
      <td>2.86</td>
      <td>5.62</td>
      <td>0.60</td>
      <td>1.25</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.44</td>
      <td>0.63</td>
      <td>...</td>
      <td>0.93</td>
      <td>44,181,417.00</td>
      <td>0.53</td>
      <td>5,219.08</td>
      <td>1,760,088.00</td>
      <td>128,932.00</td>
      <td>657,964.83</td>
      <td>1.32</td>
      <td>216.58</td>
      <td>79,655.42</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>4,009.84</td>
      <td>13,354.33</td>
      <td>3.35</td>
      <td>3.03</td>
      <td>0.67</td>
      <td>0.84</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.54</td>
      <td>0.22</td>
      <td>...</td>
      <td>0.75</td>
      <td>44,181,417.00</td>
      <td>0.38</td>
      <td>611.22</td>
      <td>1,760,088.00</td>
      <td>12,455.50</td>
      <td>592,102.00</td>
      <td>1.02</td>
      <td>49.09</td>
      <td>3,151.28</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>242.23</td>
      <td>209,055.78</td>
      <td>1.18</td>
      <td>4.74</td>
      <td>0.39</td>
      <td>1.14</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.21</td>
      <td>0.48</td>
      <td>...</td>
      <td>0.76</td>
      <td>44,181,417.00</td>
      <td>0.34</td>
      <td>1,966.16</td>
      <td>1,760,088.00</td>
      <td>51,308.00</td>
      <td>612,609.67</td>
      <td>0.98</td>
      <td>111.59</td>
      <td>24,466.84</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>15,340.34</td>
      <td>353.58</td>
      <td>5.57</td>
      <td>0.28</td>
      <td>0.80</td>
      <td>0.11</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.77</td>
      <td>0.01</td>
      <td>...</td>
      <td>0.45</td>
      <td>44,181,417.00</td>
      <td>0.39</td>
      <td>2,702.62</td>
      <td>1,760,088.00</td>
      <td>64,885.50</td>
      <td>610,105.33</td>
      <td>0.95</td>
      <td>37.38</td>
      <td>2,639.88</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>181.20</td>
      <td>239,462.58</td>
      <td>0.79</td>
      <td>4.96</td>
      <td>0.29</td>
      <td>1.17</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.14</td>
      <td>0.52</td>
      <td>...</td>
      <td>0.73</td>
      <td>44,181,417.00</td>
      <td>0.33</td>
      <td>2,032.18</td>
      <td>1,760,088.00</td>
      <td>52,309.50</td>
      <td>613,753.50</td>
      <td>0.94</td>
      <td>116.57</td>
      <td>26,830.82</td>
    </tr>
    <tr>
      <th>any</th>
      <td>2,511.26</td>
      <td>23,683.00</td>
      <td>3.48</td>
      <td>2.28</td>
      <td>0.69</td>
      <td>0.64</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.57</td>
      <td>0.13</td>
      <td>...</td>
      <td>0.67</td>
      <td>44,181,417.00</td>
      <td>0.35</td>
      <td>1,868.76</td>
      <td>1,760,088.00</td>
      <td>47,833.00</td>
      <td>605,402.67</td>
      <td>0.94</td>
      <td>61.22</td>
      <td>6,418.24</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>17,999.07</td>
      <td>40,303.42</td>
      <td>3.15</td>
      <td>1.43</td>
      <td>0.63</td>
      <td>0.41</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.48</td>
      <td>0.06</td>
      <td>...</td>
      <td>0.52</td>
      <td>44,181,417.00</td>
      <td>0.27</td>
      <td>11,843.55</td>
      <td>1,760,088.00</td>
      <td>295,457.00</td>
      <td>696,027.83</td>
      <td>0.72</td>
      <td>109.48</td>
      <td>20,694.95</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>847.65</td>
      <td>42,704.93</td>
      <td>1.14</td>
      <td>3.09</td>
      <td>0.32</td>
      <td>0.84</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.16</td>
      <td>0.22</td>
      <td>...</td>
      <td>0.58</td>
      <td>44,181,417.00</td>
      <td>0.19</td>
      <td>1,688.64</td>
      <td>1,760,088.00</td>
      <td>37,696.00</td>
      <td>602,533.50</td>
      <td>0.68</td>
      <td>67.79</td>
      <td>8,127.86</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>4,160.38</td>
      <td>7,333.55</td>
      <td>2.42</td>
      <td>1.78</td>
      <td>0.55</td>
      <td>0.52</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>0.36</td>
      <td>0.09</td>
      <td>...</td>
      <td>0.53</td>
      <td>44,181,417.00</td>
      <td>0.23</td>
      <td>1,437.92</td>
      <td>1,760,088.00</td>
      <td>30,368.50</td>
      <td>598,438.67</td>
      <td>0.68</td>
      <td>48.10</td>
      <td>3,421.58</td>
    </tr>
    <tr>
      <th>altogether</th>
      <td>-123.22</td>
      <td>9,468.00</td>
      <td>-0.65</td>
      <td>2.75</td>
      <td>-0.37</td>
      <td>0.77</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>-0.08</td>
      <td>0.18</td>
      <td>...</td>
      <td>0.20</td>
      <td>44,181,417.00</td>
      <td>0.05</td>
      <td>516.36</td>
      <td>1,760,088.00</td>
      <td>11,222.00</td>
      <td>591,217.83</td>
      <td>0.23</td>
      <td>21.05</td>
      <td>1,827.14</td>
    </tr>
    <tr>
      <th>only</th>
      <td>-716.03</td>
      <td>261,936.36</td>
      <td>-1.73</td>
      <td>3.04</td>
      <td>-0.64</td>
      <td>0.82</td>
      <td>2,032,082.00</td>
      <td>86,330,752.00</td>
      <td>-0.11</td>
      <td>0.21</td>
      <td>...</td>
      <td>0.09</td>
      <td>44,181,417.00</td>
      <td>0.05</td>
      <td>9,046.94</td>
      <td>1,760,088.00</td>
      <td>234,668.50</td>
      <td>683,959.33</td>
      <td>0.12</td>
      <td>121.34</td>
      <td>48,074.56</td>
    </tr>
  </tbody>
</table>
<p>14 rows × 40 columns</p>
</div>




```python
load_path = TOP_AM_DIR / f'Top{K}_NEG-ADV_top-bigrams.{DATE}.csv'
bigram_am = pd.read_csv(load_path).set_index('key')
bigram_am.nlargest(K, 'LRC')
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
      <th>LRC</th>
      <th>G2</th>
      <th>t</th>
      <th>MI</th>
      <th>odds_r_disc</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>l1</th>
      <th>l2</th>
      <th>adv</th>
      <th>adj</th>
      <th>adj_total</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>NEG~yet_clear</th>
      <td>10553</td>
      <td>399.60</td>
      <td>10,153.40</td>
      <td>0.95</td>
      <td>10.26</td>
      <td>67,924.56</td>
      <td>98.84</td>
      <td>1.42</td>
      <td>3.29</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>10693</td>
      <td>NEGATED</td>
      <td>yet_clear</td>
      <td>yet</td>
      <td>clear</td>
      <td>491,108.00</td>
    </tr>
    <tr>
      <th>NEG~yet_ready</th>
      <td>7611</td>
      <td>292.91</td>
      <td>7,318.09</td>
      <td>0.93</td>
      <td>9.23</td>
      <td>48,012.06</td>
      <td>83.88</td>
      <td>1.41</td>
      <td>2.94</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>7838</td>
      <td>NEGATED</td>
      <td>yet_ready</td>
      <td>yet</td>
      <td>ready</td>
      <td>240,297.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_sure</th>
      <td>8860</td>
      <td>347.58</td>
      <td>8,512.42</td>
      <td>0.92</td>
      <td>8.63</td>
      <td>54,750.58</td>
      <td>90.43</td>
      <td>1.41</td>
      <td>2.71</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>9301</td>
      <td>NEGATED</td>
      <td>exactly_sure</td>
      <td>exactly</td>
      <td>sure</td>
      <td>844,981.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_new</th>
      <td>1378</td>
      <td>52.99</td>
      <td>1,325.01</td>
      <td>0.93</td>
      <td>8.54</td>
      <td>8,697.93</td>
      <td>35.69</td>
      <td>1.42</td>
      <td>2.94</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1418</td>
      <td>NEGATED</td>
      <td>exactly_new</td>
      <td>exactly</td>
      <td>new</td>
      <td>321,311.00</td>
    </tr>
    <tr>
      <th>NEG~yet_complete</th>
      <td>2220</td>
      <td>86.48</td>
      <td>2,133.52</td>
      <td>0.92</td>
      <td>8.42</td>
      <td>13,815.99</td>
      <td>45.28</td>
      <td>1.41</td>
      <td>2.78</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>2314</td>
      <td>NEGATED</td>
      <td>yet_complete</td>
      <td>yet</td>
      <td>complete</td>
      <td>107,018.00</td>
    </tr>
    <tr>
      <th>NEG~that_uncommon</th>
      <td>804</td>
      <td>30.61</td>
      <td>773.39</td>
      <td>0.94</td>
      <td>8.39</td>
      <td>5,136.91</td>
      <td>27.28</td>
      <td>1.42</td>
      <td>3.13</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>819</td>
      <td>NEGATED</td>
      <td>that_uncommon</td>
      <td>that</td>
      <td>uncommon</td>
      <td>61,767.00</td>
    </tr>
    <tr>
      <th>NEG~necessarily_indicative</th>
      <td>1406</td>
      <td>54.41</td>
      <td>1,351.59</td>
      <td>0.93</td>
      <td>8.37</td>
      <td>8,811.69</td>
      <td>36.05</td>
      <td>1.41</td>
      <td>2.86</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1456</td>
      <td>NEGATED</td>
      <td>necessarily_indicative</td>
      <td>necessarily</td>
      <td>indicative</td>
      <td>12,760.00</td>
    </tr>
    <tr>
      <th>NEG~yet_sure</th>
      <td>1990</td>
      <td>77.54</td>
      <td>1,912.46</td>
      <td>0.92</td>
      <td>8.37</td>
      <td>12,379.79</td>
      <td>42.87</td>
      <td>1.41</td>
      <td>2.78</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>2075</td>
      <td>NEGATED</td>
      <td>yet_sure</td>
      <td>yet</td>
      <td>sure</td>
      <td>844,981.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_easy</th>
      <td>1069</td>
      <td>41.11</td>
      <td>1,027.89</td>
      <td>0.93</td>
      <td>8.37</td>
      <td>6,747.64</td>
      <td>31.44</td>
      <td>1.42</td>
      <td>2.94</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1100</td>
      <td>NEGATED</td>
      <td>exactly_easy</td>
      <td>exactly</td>
      <td>easy</td>
      <td>771,307.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
if not NEG_HITS_PATH.is_file(): 
    NEG_HITS_PATH = POST_PROC_DIR.joinpath('NEGmirror/trigger-bigrams_thr0-001p.35f.pkl.gz')
neg_hits_table = pd.read_pickle(NEG_HITS_PATH).filter(regex=r'^[nab].*lower|text|str|head')

```


```python
neg_hits_table = neg_hits_table.drop_duplicates(['text_window', 'bigram_lower', 'neg_form_lower'])
word_cols = neg_hits_table.filter(regex=r'head|lower').columns
neg_hits_table[word_cols] = neg_hits_table[word_cols].astype('category')
neg_hits_table = neg_hits_table.loc[neg_hits_table.adv_form_lower.isin(adv_am.index), :]
neg_hits_table.sample(3).iloc[:,:6]
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
      <th>neg_head</th>
      <th>neg_form_lower</th>
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
    </tr>
    <tr>
      <th>hit_id</th>
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
      <th>pcc_eng_18_016.6897_x0254204_19:4-5-6</th>
      <td>But it is not yet clear whether cabinet hardliners will</td>
      <td>But it is not yet clear whether cabinet hardliners will accept it - trade se...</td>
      <td>ADJ</td>
      <td>not</td>
      <td>yet</td>
      <td>clear</td>
    </tr>
    <tr>
      <th>pcc_eng_06_035.0939_x0551484_14:1-3-4</th>
      <td>Neither is particularly colorful , but they 're</td>
      <td>Neither is particularly colorful , but they 're both really good .</td>
      <td>ADJ</td>
      <td>neither</td>
      <td>particularly</td>
      <td>colorful</td>
    </tr>
    <tr>
      <th>pcc_eng_07_061.7619_x0982110_37:7-8-9</th>
      <td>I know that is not exactly true .</td>
      <td>Now , I know that is not exactly true .</td>
      <td>ADJ</td>
      <td>not</td>
      <td>exactly</td>
      <td>true</td>
    </tr>
  </tbody>
</table>
</div>




```python
# sourcery skip: use-fstring-for-concatenation
if 'all_forms_lower' not in neg_hits_table.columns: 
    neg_hits_table['all_forms_lower'] = (
        neg_hits_table.neg_form_lower.astype('string') 
        + '_' 
        + neg_hits_table.bigram_lower.astype('string')
        ).astype('category')
neg_hits_table.sample(3).filter(like='lower')
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
      <th>neg_form_lower</th>
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>bigram_lower</th>
      <th>all_forms_lower</th>
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
      <th>pcc_eng_13_006.3494_x0086333_24:22-26-27</th>
      <td>without</td>
      <td>any</td>
      <td>wiser</td>
      <td>any_wiser</td>
      <td>without_any_wiser</td>
    </tr>
    <tr>
      <th>pcc_eng_01_020.2514_x0311299_03:10-11-12</th>
      <td>not</td>
      <td>only</td>
      <td>warm</td>
      <td>only_warm</td>
      <td>not_only_warm</td>
    </tr>
    <tr>
      <th>pcc_eng_11_106.8256_x1712933_4:22-23-24</th>
      <td>n't</td>
      <td>immediately</td>
      <td>available</td>
      <td>immediately_available</td>
      <td>n't_immediately_available</td>
    </tr>
  </tbody>
</table>
</div>




```python
# samples = dict.fromkeys(bigram_am.l2.unique())
# for i, bigram in enumerate(bigram_am['l2'].unique(), start=1):
#     print(f'\n({i}) {bigram}')
#     samples[bigram] = sp(data=neg_hits_table,
#                          filters=[f'bigram_lower=={bigram}'],
#                          print_sample=False,
#                          sample_size=50,
#                          columns=['neg_form_lower', 'all_forms_lower',
#                                   'text_window', 'token_str'],
#                          quiet=True,
#                          sort_by='all_forms_lower')
#     print('    > ', samples[bigram].sample(1).text_window.squeeze())
```


```python
def collect_examples(amdf:pd.DataFrame,
                     hits_df:pd.DataFrame, 
                     adv: str = 'exactly', 
                     n_bigrams: int = K, 
                     n_examples: int = 50, 
                     metric: str = 'LRC') -> dict:
    df = amdf.copy().filter(like=adv, axis=0).nlargest(n_bigrams, metric)
    examples = {}
    for i, bigram in enumerate(df['l2'].unique(), start=1):
        print(f'\n({i}) {bigram}')
        examples[bigram] = sp(
            data=hits_df, print_sample=False, 
            sample_size=n_examples, quiet=True, sort_by='all_forms_lower',
            filters=[f'bigram_lower=={bigram}'],
            columns=['END::lower', 'text_window', 'token_str'])
        print('    > ', examples[bigram].sample(1).token_str.squeeze())
    return examples
```


```python
def save_examples(adverb, bigram_am, neg_hits_table):
    print(f'\n## *{adverb}*\n')
    print_md_table(bigram_am.filter(like=adverb, axis=0).nlargest(K, 'LRC'), n_dec=2)
    examples = collect_examples(bigram_am, neg_hits_table, 
                                adv=adverb, metric='LRC')
    
    output_dir = TOP_AM_DIR / 'neg_bigram_examples' / adverb
    confirm_dir(output_dir)
    print(output_dir)

    for k, df in examples.items(): 
        out_path = output_dir.joinpath(f'{k}_50ex.csv')
        print(out_path)
        df.to_csv(out_path)
```


```python
for adverb in adv_am.index: 
    save_examples(adverb, bigram_am, neg_hits_table)
```

    
    ## *exactly*
    
    
    | key                    |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2                 | adv     | adj        |   adj_total |
    |:-----------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:-------------------|:--------|:-----------|------------:|
    | NEG~exactly_sure       | 8,860 |  347.58 |  8,512.42 |  0.92 |  8.63 | 54,750.58 | 90.43 | 1.41 |          2.71 | 86,330,752 | 3,226,213 | 9,301 | NEGATED | exactly_sure       | exactly | sure       |  844,981.00 |
    | NEG~exactly_new        | 1,378 |   52.99 |  1,325.01 |  0.93 |  8.54 |  8,697.93 | 35.69 | 1.42 |          2.94 | 86,330,752 | 3,226,213 | 1,418 | NEGATED | exactly_new        | exactly | new        |  321,311.00 |
    | NEG~exactly_easy       | 1,069 |   41.11 |  1,027.89 |  0.93 |  8.37 |  6,747.64 | 31.44 | 1.42 |          2.94 | 86,330,752 | 3,226,213 | 1,100 | NEGATED | exactly_easy       | exactly | easy       |  771,307.00 |
    | NEG~exactly_clear      | 1,759 |   68.57 |  1,690.43 |  0.92 |  8.30 | 10,937.16 | 40.31 | 1.41 |          2.77 | 86,330,752 | 3,226,213 | 1,835 | NEGATED | exactly_clear      | exactly | clear      |  491,108.00 |
    | NEG~exactly_cheap      |   693 |   26.31 |    666.69 |  0.95 |  8.28 |  4,443.27 | 25.33 | 1.42 |          3.19 | 86,330,752 | 3,226,213 |   704 | NEGATED | exactly_cheap      | exactly | cheap      |   83,765.00 |
    | NEG~exactly_surprising |   441 |   16.59 |    424.41 |  0.96 |  7.34 |  2,863.35 | 20.21 | 1.42 |          3.51 | 86,330,752 | 3,226,213 |   444 | NEGATED | exactly_surprising | exactly | surprising |  150,067.00 |
    | NEG~exactly_happy      |   441 |   17.49 |    423.51 |  0.90 |  7.16 |  2,694.69 | 20.17 | 1.40 |          2.62 | 86,330,752 | 3,226,213 |   468 | NEGATED | exactly_happy      | exactly | happy      |  528,511.00 |
    | NEG~exactly_ideal      |   418 |   16.63 |    401.37 |  0.90 |  7.08 |  2,546.29 | 19.63 | 1.40 |          2.59 | 86,330,752 | 3,226,213 |   445 | NEGATED | exactly_ideal      | exactly | ideal      |   42,701.00 |
    | NEG~exactly_subtle     |   264 |   10.13 |    253.87 |  0.94 |  6.92 |  1,671.02 | 15.62 | 1.42 |          2.96 | 86,330,752 | 3,226,213 |   271 | NEGATED | exactly_subtle     | exactly | subtle     |   56,845.00 |
    
    
    (1) exactly_sure
        >  When I woke up Sunday morning , I was n't exactly sure if the room was spinning because I was still drunk or super hungover .
    
    (2) exactly_new
        >  Multisource CDN delivery is not exactly new ; Swarmcast and Conviva already provide services that manage the delivery of video streams through multiple CDN providers , but both companies are focused more on the live online video market .
    
    (3) exactly_easy
        >  And now there , Aos even a web browser for Android Wear , though its not exactly easy to browse the internet on a tiny display .
    
    (4) exactly_clear
        >  Otherwise , though , it 's not exactly clear how often you 'll use this feature .
    
    (5) exactly_cheap
        >  The app is n't exactly cheap at $ 299 , but that 's not much more than you 'd pay for a year of Premiere Rush and Premiere Pro CC .
    
    (6) exactly_surprising
        >  And that 's not exactly surprising -- China has been keen to modernize without creating its own Gorbachev-moment .
    
    (7) exactly_happy
        >  We know that she 's not exactly happy with her current position on the crime ladder , and that she has her eye on taking down mob boss Falcone , and gaining full control of the underworld for herself .
    
    (8) exactly_ideal
        >  So I would normally just forego the bag and take my camera without having any sort of protective case for it which was n't exactly ideal .
    
    (9) exactly_subtle
        >  The allegory is not exactly subtle .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_sure_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_new_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_easy_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_clear_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_cheap_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_happy_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_ideal_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/exactly/exactly_subtle_50ex.csv
    
    ## *necessarily*
    
    
    | key                            |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2                         | adv         | adj            |   adj_total |
    |:-------------------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:---------------------------|:------------|:---------------|------------:|
    | NEG~necessarily_indicative     | 1,406 |   54.41 |  1,351.59 |  0.93 |  8.37 |  8,811.69 | 36.05 | 1.41 |          2.86 | 86,330,752 | 3,226,213 | 1,456 | NEGATED | necessarily_indicative     | necessarily | indicative     |   12,760.00 |
    | NEG~necessarily_representative |   496 |   19.58 |    476.42 |  0.91 |  7.31 |  3,044.27 | 21.39 | 1.40 |          2.65 | 86,330,752 | 3,226,213 |   524 | NEGATED | necessarily_representative | necessarily | representative |   25,187.00 |
    | NEG~necessarily_easy           |   914 |   37.22 |    876.78 |  0.88 |  7.26 |  5,448.34 | 29.00 | 1.39 |          2.46 | 86,330,752 | 3,226,213 |   996 | NEGATED | necessarily_easy           | necessarily | easy           |  771,307.06 |
    | NEG~necessarily_surprising     |   343 |   13.27 |    329.73 |  0.93 |  7.22 |  2,150.86 | 17.80 | 1.41 |          2.85 | 86,330,752 | 3,226,213 |   355 | NEGATED | necessarily_surprising     | necessarily | surprising     |  150,067.00 |
    | NEG~necessarily_true           | 3,238 |  141.48 |  3,096.52 |  0.82 |  6.89 | 18,199.76 | 54.42 | 1.36 |          2.18 | 86,330,752 | 3,226,213 | 3,786 | NEGATED | necessarily_true           | necessarily | true           |  348,994.00 |
    | NEG~necessarily_interested     |   422 |   17.30 |    404.70 |  0.87 |  6.77 |  2,500.26 | 19.70 | 1.39 |          2.42 | 86,330,752 | 3,226,213 |   463 | NEGATED | necessarily_interested     | necessarily | interested     |  364,497.00 |
    | NEG~necessarily_related        |   742 |   31.47 |    710.53 |  0.84 |  6.74 |  4,271.76 | 26.08 | 1.37 |          2.28 | 86,330,752 | 3,226,213 |   842 | NEGATED | necessarily_related        | necessarily | related        |  137,661.00 |
    | NEG~necessarily_illegal        |   280 |   11.47 |    268.53 |  0.87 |  6.48 |  1,659.90 | 16.05 | 1.39 |          2.42 | 86,330,752 | 3,226,213 |   307 | NEGATED | necessarily_illegal        | necessarily | illegal        |   44,028.00 |
    | NEG~necessarily_new            |   483 |   20.96 |    462.04 |  0.82 |  6.36 |  2,728.73 | 21.02 | 1.36 |          2.20 | 86,330,752 | 3,226,213 |   561 | NEGATED | necessarily_new            | necessarily | new            |  321,311.00 |
    
    
    (1) necessarily_indicative
        >  The past performance of any trading method or methodology will not be necessarily indicative of future outcomes .
    
    (2) necessarily_representative
        >  " That number is n't necessarily representative of local labor trafficking rates , but rather reflects the number of victims who were aware of the National Human Trafficking Hotline and comfortable enough to dial it , " Diemar said in the Bee 's story .
    
    (3) necessarily_easy
        >  The choices are n't necessarily easy in some cases .
    
    (4) necessarily_surprising
        >  He added that the news of Mark Fields ' departure was n't necessarily surprising , saying : " If you judge a guy by a stock price , I guess he had to go . "
    
    (5) necessarily_true
        >  there were reports -- again on the Internet -- that this would be his last role , a rumor he helped fuel but now says is not necessarily true .
    
    (6) necessarily_interested
        >  I mean , I know where you were last night , who you were with , what you ate , and how you felt about it ... and I was n't necessarily interested in knowing any of it -- your information just happened to be in my newsfeed .
    
    (7) necessarily_related
        >  In other words , like human minds , deep learning algorithms take in a multiplicity of stimuli or facts that are not necessarily related , and work with them to achieve some level of knowledge or understanding .
    
    (8) necessarily_illegal
        >  Experts are saying the trick is n't necessarily illegal , but it could definitely hurt the airline business .
    
    (9) necessarily_new
        >  This concept is n't necessarily new , but it is gaining traction among consumers who want to know that their food is fresh and locally sourced .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_indicative_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_representative_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_easy_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_true_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_interested_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_related_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_illegal_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/necessarily/necessarily_new_50ex.csv
    
    ## *before*
    
    
    | key                  |   f |   exp_f |   unexp_f |   dP1 |   LRC |     G2 |     t |   MI |   odds_r_disc |         N |      f1 |   f2 | l1     | l2               | adv    | adj       |   adj_total |
    |:---------------------|----:|--------:|----------:|------:|------:|-------:|------:|-----:|--------------:|----------:|--------:|-----:|:-------|:-----------------|:-------|:----------|------------:|
    | NEG~before_available | 177 |   26.04 |    150.96 |  0.84 |  3.99 | 654.92 | 11.35 | 0.83 |          2.48 | 2,032,082 | 293,963 |  180 | NEGMIR | before_available | before | available |   14,919.00 |
    
    
    (1) before_available
        >  Not only unusual , but also very strongly correlated to all the tornado activity that we have been seeing .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/before
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/before/before_available_50ex.csv
    
    ## *that*
    
    
    | key                  |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |        f1 |     f2 | l1      | l2               | adv   | adj         |   adj_total |
    |:---------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|----------:|-------:|:--------|:-----------------|:------|:------------|------------:|
    | NEG~that_uncommon    |   804 |   30.61 |    773.39 |  0.94 |  8.39 |  5,136.91 | 27.28 | 1.42 |          3.13 | 86,330,752 | 3,226,213 |    819 | NEGATED | that_uncommon    | that  | uncommon    |   61,767.00 |
    | NEG~that_surprising  | 1,141 |   44.36 |  1,096.64 |  0.92 |  8.14 |  7,115.30 | 32.47 | 1.41 |          2.80 | 86,330,752 | 3,226,213 |  1,187 | NEGATED | that_surprising  | that  | surprising  |  150,067.00 |
    | NEG~that_common      | 1,216 |   47.39 |  1,168.61 |  0.92 |  8.12 |  7,564.08 | 33.51 | 1.41 |          2.78 | 86,330,752 | 3,226,213 |  1,268 | NEGATED | that_common      | that  | common      |  556,435.00 |
    | NEG~that_hard        | 9,966 |  404.27 |  9,561.73 |  0.88 |  7.96 | 59,642.82 | 95.78 | 1.39 |          2.48 | 86,330,752 | 3,226,213 | 10,818 | NEGATED | that_hard        | that  | hard        |  430,990.00 |
    | NEG~that_complicated | 1,208 |   47.46 |  1,160.54 |  0.91 |  7.95 |  7,450.89 | 33.39 | 1.41 |          2.70 | 86,330,752 | 3,226,213 |  1,270 | NEGATED | that_complicated | that  | complicated |  180,071.00 |
    | NEG~that_unusual     |   983 |   38.42 |    944.58 |  0.92 |  7.94 |  6,096.13 | 30.13 | 1.41 |          2.75 | 86,330,752 | 3,226,213 |  1,028 | NEGATED | that_unusual     | that  | unusual     |  108,584.00 |
    | NEG~that_impressed   |   684 |   26.94 |    657.06 |  0.91 |  7.57 |  4,207.58 | 25.12 | 1.40 |          2.67 | 86,330,752 | 3,226,213 |    721 | NEGATED | that_impressed   | that  | impressed   |  113,281.00 |
    | NEG~that_exciting    |   805 |   32.10 |    772.90 |  0.90 |  7.48 |  4,892.83 | 27.24 | 1.40 |          2.58 | 86,330,752 | 3,226,213 |    859 | NEGATED | that_exciting    | that  | exciting    |  236,396.00 |
    | NEG~that_expensive   | 1,800 |   74.44 |  1,725.56 |  0.87 |  7.32 | 10,585.14 | 40.67 | 1.38 |          2.38 | 86,330,752 | 3,226,213 |  1,992 | NEGATED | that_expensive   | that  | expensive   |  444,946.00 |
    
    
    (1) that_uncommon
        >  Specifying one 's religion on a job or housing application is not that uncommon , globally speaking .
    
    (2) that_surprising
        >  `` Salt '' has more than its fair share of surprise twists ; and in truth most of them are n't all that surprising , but they are logical and well-prepared and thus effective .
    
    (3) that_common
        >  There 's a need for them and an audience looking for them , but they 're not that common .
    
    (4) that_hard
        >  This stuff really is n't that hard .
    
    (5) that_complicated
        >  Ok , for ls the options are n't that complicated , but when you use " ipconfig " it gets way more complicated .
    
    (6) that_unusual
        >  Those are n't that unusual .
    
    (7) that_impressed
        >  Could be a salesperson or a co-worker who you are n't that impressed with , but have to get in contact with .
    
    (8) that_exciting
        >  For three quarters it was n't that exciting of a game .
    
    (9) that_expensive
        >  Today setting up a sales funnel need not be that expensive as it used to be a few years earlier .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_uncommon_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_common_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_hard_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_complicated_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_unusual_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_impressed_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_exciting_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/that/that_expensive_50ex.csv
    
    ## *remotely*
    
    
    | key                     |   f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2                  | adv      | adj        |   adj_total |
    |:------------------------|----:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:--------------------|:---------|:-----------|------------:|
    | NEG~remotely_true       | 250 |   15.70 |    234.30 |  0.56 |  4.46 | 1,089.49 | 14.82 | 1.20 |          1.58 | 86,330,752 | 3,226,213 |   420 | NEGATED | remotely_true       | remotely | true       |  348,994.00 |
    | NEG~remotely_close      | 219 |   43.25 |    175.75 |  0.59 |  3.02 |   524.61 | 11.88 | 0.70 |          1.21 |  2,032,082 |   293,963 |   299 | NEGMIR  | remotely_close      | remotely | close      |   15,958.00 |
    | NEG~remotely_close      | 696 |   95.59 |    600.41 |  0.23 |  2.92 | 1,722.76 | 22.76 | 0.86 |          0.98 | 86,330,752 | 3,226,213 | 2,558 | NEGATED | remotely_close      | remotely | close      |  480,288.00 |
    | NEG~remotely_interested | 333 |   46.79 |    286.21 |  0.23 |  2.72 |   808.74 | 15.68 | 0.85 |          0.97 | 86,330,752 | 3,226,213 | 1,252 | NEGATED | remotely_interested | remotely | interested |  364,497.00 |
    
    
    (1) remotely_true
        >  " The media is fabricating stories and none of these accusations are remotely true , " said Channing 's rep .
    
    (2) remotely_close
        >  We went to friends ' for their 2 yr old daughter 's brunch birthday party which had many , many delicious home -made delights , none of which are remotely close to being on my diet plan ... so I did n't track any of them !
    
    (3) remotely_interested
        >  [ Hendi -- Georgetown University 's imam , the first full- time Muslim chaplain at a U.S. college -- tells his wife about a family he counseled recently in which a 15 - year - old told his parents he is not remotely interested in Islam and wants nothing to do with the faith . ]
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_true_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_close_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/remotely/remotely_interested_50ex.csv
    
    ## *yet*
    
    
    | key               |      f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |        f1 |     f2 | l1      | l2            | adv   | adj       |   adj_total |
    |:------------------|-------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|----------:|-------:|:--------|:--------------|:------|:----------|------------:|
    | NEG~yet_clear     | 10,553 |  399.60 | 10,153.40 |  0.95 | 10.26 | 67,924.56 | 98.84 | 1.42 |          3.29 | 86,330,752 | 3,226,213 | 10,693 | NEGATED | yet_clear     | yet   | clear     |  491,108.00 |
    | NEG~yet_ready     |  7,611 |  292.91 |  7,318.09 |  0.93 |  9.23 | 48,012.06 | 83.88 | 1.41 |          2.94 | 86,330,752 | 3,226,213 |  7,838 | NEGATED | yet_ready     | yet   | ready     |  240,297.00 |
    | NEG~yet_complete  |  2,220 |   86.48 |  2,133.52 |  0.92 |  8.42 | 13,815.99 | 45.28 | 1.41 |          2.78 | 86,330,752 | 3,226,213 |  2,314 | NEGATED | yet_complete  | yet   | complete  |  107,018.00 |
    | NEG~yet_sure      |  1,990 |   77.54 |  1,912.46 |  0.92 |  8.37 | 12,379.79 | 42.87 | 1.41 |          2.78 | 86,330,752 | 3,226,213 |  2,075 | NEGATED | yet_sure      | yet   | sure      |  844,981.00 |
    | NEG~yet_certain   |    874 |   33.75 |    840.25 |  0.93 |  8.12 |  5,491.41 | 28.42 | 1.41 |          2.88 | 86,330,752 | 3,226,213 |    903 | NEGATED | yet_certain   | yet   | certain   |  104,544.00 |
    | NEG~yet_eligible  |    459 |   17.49 |    441.51 |  0.94 |  7.72 |  2,929.15 | 20.61 | 1.42 |          3.10 | 86,330,752 | 3,226,213 |    468 | NEGATED | yet_eligible  | yet   | eligible  |   49,578.00 |
    | NEG~yet_available |  7,481 |  307.86 |  7,173.14 |  0.87 |  7.69 | 44,196.15 | 82.93 | 1.39 |          2.41 | 86,330,752 | 3,226,213 |  8,238 | NEGATED | yet_available | yet   | available |  866,272.00 |
    | NEG~yet_final     |    659 |   26.12 |    632.88 |  0.91 |  7.45 |  4,028.75 | 24.65 | 1.40 |          2.62 | 86,330,752 | 3,226,213 |    699 | NEGATED | yet_final     | yet   | final     |    9,657.00 |
    | NEG~yet_public    |    496 |   19.51 |    476.49 |  0.91 |  7.36 |  3,055.97 | 21.40 | 1.41 |          2.68 | 86,330,752 | 3,226,213 |    522 | NEGATED | yet_public    | yet   | public    |   41,602.00 |
    
    
    (1) yet_clear
        >  the department said it was not yet clear whether the disease was circulating in Britain or was the result of a single infection from overseas .
    
    (2) yet_ready
        >  Both men make it clear that additive manufacturing is not yet ready for flight -critical parts , and likely will not be ready soon .
    
    (3) yet_complete
        >  The ones that are not yet complete can be held onto until they are ready to go .
    
    (4) yet_sure
        >  Almost all moral conversations instead try to take a case that in our gut we 're sure about and say it 's like the situation we 're not yet sure about .
    
    (5) yet_certain
        >  This middle - of- the - road firmness option is best for the majority of consumers or those that are n't yet certain on their firmness preferences .
    
    (6) yet_eligible
        >  Another 10 or so are recently hired employees who are not yet eligible for retirement benefits but will be after they have been employed by Northwestern for a year .
    
    (7) yet_available
        >  I should preface this entire complimentary blog entry however by saying that it is not yet available for purchase .
    
    (8) yet_final
        >  spokesmen for AIG and the New York State Insurance Department said they could not provide any details on which of AIG 's insurance companies would be involved in the asset transfers , because the plan was not yet final .
    
    (9) yet_public
        >  Relational , which disclosed a B/E Aerospace stake of about 3.5 percent May 15 , submitted Batchelder and Managing Director Matthew Hepler as candidates before this week 's deadline , said the people , who asked not to be identified because the nominations are n't yet public .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_clear_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_ready_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_complete_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_sure_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_certain_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_eligible_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_available_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_final_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/yet/yet_public_50ex.csv
    
    ## *ever*
    
    
    | key              |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2           | adv   | adj     |    adj_total |
    |:-----------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:-------------|:------|:--------|-------------:|
    | NEG~that_clever  |   212 |    9.68 |    202.32 |  0.78 |  5.60 |  1,151.90 | 13.90 | 1.34 |          2.06 | 86,330,752 | 3,226,213 |   259 | NEGATED | that_clever  | that  | clever  |    40,802.00 |
    | NEG~ever_simple  |   212 |    9.79 |    202.21 |  0.77 |  5.54 |  1,142.04 | 13.89 | 1.34 |          2.04 | 86,330,752 | 3,226,213 |   262 | NEGATED | ever_simple  | ever  | simple  |   427,167.00 |
    | NEG~ever_easy    |   430 |   23.95 |    406.05 |  0.63 |  5.06 |  2,030.58 | 19.58 | 1.25 |          1.72 | 86,330,752 | 3,226,213 |   641 | NEGATED | ever_easy    | ever  | easy    |   771,307.06 |
    | NEG~ever_good    |   300 |   44.27 |    255.73 |  0.84 |  5.05 |  1,103.09 | 14.76 | 0.83 |          2.44 |  2,032,082 |   293,963 |   306 | NEGMIR  | ever_good    | ever  | good    |    38,252.00 |
    | NEG~as_severe    | 2,692 |  179.71 |  2,512.29 |  0.52 |  4.81 | 11,262.06 | 48.42 | 1.18 |          1.52 | 86,330,752 | 3,226,213 | 4,809 | NEGATED | as_severe    | as    | severe  |   102,675.00 |
    | NEG~ever_easy    |   368 |   53.52 |    314.48 |  0.85 |  4.66 |  1,399.10 | 16.39 | 0.84 |          2.94 |  2,032,082 |   293,963 |   370 | NEGMIR  | ever_easy    | ever  | easy    |    21,775.00 |
    | NEG~ever_good    |   332 |   28.25 |    303.75 |  0.40 |  3.76 |  1,178.00 | 16.67 | 1.07 |          1.30 | 86,330,752 | 3,226,213 |   756 | NEGATED | ever_good    | ever  | good    | 2,037,285.00 |
    | NEG~ever_able    |   136 |   21.55 |    114.45 |  0.77 |  3.73 |    441.74 |  9.81 | 0.80 |          1.78 |  2,032,082 |   293,963 |   149 | NEGMIR  | ever_able    | ever  | able    |     8,177.00 |
    | NEG~ever_perfect |   217 |   19.69 |    197.31 |  0.37 |  3.48 |    736.05 | 13.39 | 1.04 |          1.26 | 86,330,752 | 3,226,213 |   527 | NEGATED | ever_perfect | ever  | perfect |   164,519.00 |
    
    
    (1) that_clever
        >  Nope , we 're not that clever , or cultured for that matter .
    
    (2) ever_simple
        >  But when it comes to passion , nothing is ever simple ...
    
    (3) ever_easy
        >  It is n't ever easy , or even assertable to make a choice a instance that will occupation for one and all who requirements to go to .
    
    (4) ever_good
        >  If it were n't for the damn military marching in and breaking stuff , the CIA might have a relatively clean batch of dominoes to set up and knock down ( clean for us TV viewers ; for the natives of the " enemy " country nothing 's ever good ) .
    
    (5) as_severe
        >  Winning back your girlfriend is not only possible , it 's a lot more likely to be successful than you might think .
    
    (6) ever_able
        >  Adolf Menzel , Carl Spitzweg , and Carl Blechen were very good at it , but with that technique you have to work fast and be able to let things go -- which , thanks to my cursed ppp-condition , I 'm hardly ever able to do , except for example in the microphone of The Rift , or in the teacher and the foot of the board in Impertinence .
    
    (7) ever_perfect
        >  `` Nothing 's ever perfect _ it 's hard to build a business , whether you 're public or you 're private , '' Ms. Polish said .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/that_clever_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_simple_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_easy_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_good_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/as_severe_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_able_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/ever/ever_perfect_50ex.csv
    
    ## *immediately*
    
    
    | key                        |      f |    exp_f |   unexp_f |   dP1 |   LRC |         G2 |      t |   MI |   odds_r_disc |          N |        f1 |     f2 | l1      | l2                     | adv         | adj        |   adj_total |
    |:---------------------------|-------:|---------:|----------:|------:|------:|-----------:|-------:|-----:|--------------:|-----------:|----------:|-------:|:--------|:-----------------------|:------------|:-----------|------------:|
    | NEG~immediately_clear      | 25,276 | 1,011.47 | 24,264.53 |  0.90 |  8.32 | 153,302.22 | 152.62 | 1.40 |          2.56 | 86,330,752 | 3,226,213 | 27,066 | NEGATED | immediately_clear      | immediately | clear      |  491,108.00 |
    | NEG~immediately_possible   |  1,027 |    40.77 |    986.23 |  0.90 |  7.68 |   6,269.26 |  30.77 | 1.40 |          2.61 | 86,330,752 | 3,226,213 |  1,091 | NEGATED | immediately_possible   | immediately | possible   |  364,265.00 |
    | NEG~immediately_available  | 21,297 | 1,148.20 | 20,148.80 |  0.66 |  5.77 | 102,962.94 | 138.07 | 1.27 |          1.77 | 86,330,752 | 3,226,213 | 30,725 | NEGATED | immediately_available  | immediately | available  |  866,272.00 |
    | NEG~immediately_able       |    639 |    38.72 |    600.28 |  0.58 |  4.87 |   2,851.84 |  23.75 | 1.22 |          1.62 | 86,330,752 | 3,226,213 |  1,036 | NEGATED | immediately_able       | immediately | able       |  428,268.00 |
    | NEG~immediately_obvious    |  2,258 |   160.88 |  2,097.12 |  0.49 |  4.59 |   9,043.23 |  44.13 | 1.15 |          1.45 | 86,330,752 | 3,226,213 |  4,305 | NEGATED | immediately_obvious    | immediately | obvious    |  193,498.00 |
    | NEG~immediately_apparent   |  2,031 |   196.57 |  1,834.43 |  0.35 |  3.80 |   6,581.69 |  40.70 | 1.01 |          1.21 | 86,330,752 | 3,226,213 |  5,260 | NEGATED | immediately_apparent   | immediately | apparent   |   64,104.00 |
    | NEG~immediately_successful |    292 |    27.77 |    264.23 |  0.36 |  3.47 |     958.19 |  15.46 | 1.02 |          1.22 | 86,330,752 | 3,226,213 |    743 | NEGATED | immediately_successful | immediately | successful |  407,004.00 |
    | NEG~immediately_visible    |    436 |    46.12 |    389.88 |  0.32 |  3.35 |   1,324.08 |  18.67 | 0.98 |          1.15 | 86,330,752 | 3,226,213 |  1,234 | NEGATED | immediately_visible    | immediately | visible    |  137,609.00 |
    | NEG~immediately_evident    |    428 |    54.78 |    373.22 |  0.25 |  2.96 |   1,122.08 |  18.04 | 0.89 |          1.03 | 86,330,752 | 3,226,213 |  1,466 | NEGATED | immediately_evident    | immediately | evident    |   60,888.00 |
    
    
    (1) immediately_clear
        >  the nature of her daughter 's disability was not immediately clear .
    
    (2) immediately_possible
        >  it was not immediately possible to contact local police or officials in the northern state , which has poor telecommunications .
    
    (3) immediately_available
        >  Abbas ' delegation left Sharm el-Sheik and officials were not immediately available for comment .
    
    (4) immediately_able
        >  Nantes were not immediately able to comment .
    
    (5) immediately_obvious
        >  In some cases , the reasons behind the permissions a developer asks for are n't immediately obvious to the user , and it can be tough to check everything , especially to the novice user .
    
    (6) immediately_apparent
        >  And then , by connecting to the geeky girl , experiencing a kind of attraction much softer , subtler , and richer because it was n't immediately apparent .
    
    (7) immediately_successful
        >  Efforts by Fox News.com to reach Enck on Thursday were not immediately successful , and it was not clear whether he had an attorney .
    
    (8) immediately_visible
        >  The links are not immediately visible , but they are there .
    
    (9) immediately_evident
        >  A women 's revolution has begun in Saudi Arabia , although it may not be immediately evident .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_clear_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_possible_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_available_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_able_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_obvious_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_apparent_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_successful_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_visible_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/immediately/immediately_evident_50ex.csv
    
    ## *any*
    
    
    | key               |         f |        exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |         f1 |        f2 | l1         | l2            | adv   | adj       |    adj_total |
    |:------------------|----------:|-------------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|-----------:|----------:|:-----------|:--------------|:------|:----------|-------------:|
    | COM~not_many      |    58,428 |    56,256.30 |  2,171.70 |  0.04 |  5.25 |  4,286.27 |  8.98 | 0.02 |          2.19 | 86,330,752 | 83,102,035 |    58,442 | COMPLEMENT | not_many      | not   | many      | 2,212,989.00 |
    | NEG~any_happier   |       830 |        55.01 |    774.99 |  0.53 |  4.65 |  3,488.76 | 26.90 | 1.18 |          1.52 | 86,330,752 |  3,226,213 |     1,472 | NEGATED    | any_happier   | any   | happier   |    19,501.00 |
    | COM~so_many       | 1,189,746 | 1,147,298.60 | 42,447.40 |  0.04 |  4.27 | 74,084.75 | 38.92 | 0.02 |          1.34 | 86,330,752 | 83,102,035 | 1,191,874 | COMPLEMENT | so_many       | so    | many      | 2,212,989.00 |
    | NEG~any_better    |       382 |        72.76 |    309.24 |  0.61 |  3.42 |    960.25 | 15.82 | 0.72 |          1.27 |  2,032,082 |    293,963 |       503 | NEGMIR     | any_better    | any   | better    |    16,232.00 |
    | NEG~any_clearer   |       357 |        39.35 |    317.65 |  0.30 |  3.21 |  1,051.22 | 16.81 | 0.96 |          1.12 | 86,330,752 |  3,226,213 |     1,053 | NEGATED    | any_clearer   | any   | clearer   |    13,369.00 |
    | NEG~any_simpler   |       228 |        25.11 |    202.89 |  0.30 |  3.09 |    671.74 | 13.44 | 0.96 |          1.12 | 86,330,752 |  3,226,213 |       672 | NEGATED    | any_simpler   | any   | simpler   |    26,094.00 |
    | NEG~any_different |       910 |       123.81 |    786.19 |  0.24 |  2.98 |  2,270.24 | 26.06 | 0.87 |          0.99 | 86,330,752 |  3,226,213 |     3,313 | NEGATED    | any_different | any   | different |   909,864.00 |
    | NEG~any_worse     |     1,693 |       317.16 |  1,375.84 |  0.16 |  2.47 |  3,165.88 | 33.44 | 0.73 |          0.81 | 86,330,752 |  3,226,213 |     8,487 | NEGATED    | any_worse     | any   | worse     |   214,166.00 |
    | NEG~any_younger   |       256 |        41.89 |    214.11 |  0.19 |  2.37 |    544.17 | 13.38 | 0.79 |          0.88 | 86,330,752 |  3,226,213 |     1,121 | NEGATED    | any_younger   | any   | younger   |    29,805.00 |
    
    
    (1) not_many
        >  We have a chapter about people , just talking about how the channel came together , stories behind some of the most famous videos and also people talking about how they felt women were portrayed in videos , which were n't really that great with a lot of the bands - like some of the heavy metal bands in particular in the ' 80s and also how the channel at first was n't really playing enough black artists .
    
    (2) any_happier
        >  I suspect however , that those affected would not be any happier because they are few in number .
    
    (3) so_many
        >  Not that the others are exactly thrilled about the things that have been written either -- apparently Kim is the only member of the Kardashian / Jenner clan who has spoken to Caitlyn since the book 's release .
    
    (4) any_better
        >  The following carriages are not any better than ours .
    
    (5) any_clearer
        >  It could n't have been any clearer .
    
    (6) any_simpler
        >  The tow camera's design could n't be any simpler : it 's an underwater camera that has a 150 m " umbilical " ( cable ) that let 's us see images in real -time right from the boat .
    
    (7) any_different
        >  AJC : Are you sure this game wo n't be any different ?
    
    (8) any_worse
        >  L.A. traffic has a notorious reputation but I truly believe it is not any worse than other big cities .
    
    (9) any_younger
        >  he 's not getting any younger and he deserves it .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/not_many_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_happier_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/so_many_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_better_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_clearer_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_simpler_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_different_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_worse_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/any/any_younger_50ex.csv
    
    ## *particularly*
    
    
    | key                         |     f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2                      | adv          | adj        |   adj_total |
    |:----------------------------|------:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:------------------------|:-------------|:-----------|------------:|
    | NEG~particularly_new        |   407 |   62.35 |    344.65 |  0.80 |  5.04 | 1,396.47 | 17.08 | 0.81 |          1.99 |  2,032,082 |   293,963 |   431 | NEGMIR  | particularly_new        | particularly | new        |   14,734.00 |
    | NEG~particularly_surprising | 1,076 |   74.03 |  1,001.97 |  0.51 |  4.58 | 4,411.15 | 30.55 | 1.16 |          1.49 | 86,330,752 | 3,226,213 | 1,981 | NEGATED | particularly_surprising | particularly | surprising |  150,067.00 |
    | NEG~particularly_religious  |   488 |   32.14 |    455.86 |  0.53 |  4.54 | 2,059.88 | 20.64 | 1.18 |          1.53 | 86,330,752 | 3,226,213 |   860 | NEGATED | particularly_religious  | particularly | religious  |   37,788.00 |
    | NEG~particularly_wrong      |   212 |   31.83 |    180.17 |  0.82 |  4.54 |   753.64 | 12.37 | 0.82 |          2.17 |  2,032,082 |   293,963 |   220 | NEGMIR  | particularly_wrong      | particularly | wrong      |   24,007.00 |
    | NEG~particularly_new        |   752 |   52.17 |    699.83 |  0.50 |  4.49 | 3,065.77 | 25.52 | 1.16 |          1.48 | 86,330,752 | 3,226,213 | 1,396 | NEGATED | particularly_new        | particularly | new        |  321,311.00 |
    | NEG~particularly_original   |   363 |   24.03 |    338.97 |  0.53 |  4.44 | 1,526.99 | 17.79 | 1.18 |          1.52 | 86,330,752 | 3,226,213 |   643 | NEGATED | particularly_original   | particularly | original   |   45,732.00 |
    | NEG~particularly_surprising |   168 |   26.33 |    141.67 |  0.78 |  4.02 |   555.35 | 10.93 | 0.80 |          1.84 |  2,032,082 |   293,963 |   182 | NEGMIR  | particularly_surprising | particularly | surprising |    3,048.00 |
    | NEG~particularly_wrong      |   219 |   16.67 |    202.33 |  0.45 |  3.89 |   838.81 | 13.67 | 1.12 |          1.40 | 86,330,752 | 3,226,213 |   446 | NEGATED | particularly_wrong      | particularly | wrong      |  187,720.00 |
    | NEG~particularly_friendly   |   269 |   22.91 |    246.09 |  0.40 |  3.69 |   953.96 | 15.00 | 1.07 |          1.30 | 86,330,752 | 3,226,213 |   613 | NEGATED | particularly_friendly   | particularly | friendly   |  132,897.00 |
    
    
    (1) particularly_new
        >  And that also is nothing particularly new - not on this blog .
    
    (2) particularly_surprising
        >  Beyond that , Ndiaye does n't currently possess the skill - level necessary to score when he was not directly around the basket , but considering how new to the game he is , that is n't particularly surprising .
    
    (3) particularly_religious
        >  I proudly cast my vote in the Democratic primaries for Senator Bernie Sanders , who has called himself " not particularly religious , " but has devoted his life to the fair treatment of all under civil law .
    
    (4) particularly_wrong
        >  There 's nothing particularly wrong with that .
    
    (5) particularly_original
        >  To start with , the plot is slightly predictable and not particularly original .
    
    (6) particularly_friendly
        >  To be frank , this crossing is n't particularly friendly to pedestrians or cyclists at the moment .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_new_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_religious_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_wrong_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_original_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/particularly/particularly_friendly_50ex.csv
    
    ## *terribly*
    
    
    | key                      |   f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2                   | adv      | adj         |   adj_total |
    |:-------------------------|----:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:---------------------|:---------|:------------|------------:|
    | NEG~terribly_surprising  | 951 |   39.39 |    911.61 |  0.86 |  7.08 | 5,585.09 | 29.56 | 1.38 |          2.37 | 86,330,752 | 3,226,213 | 1,054 | NEGATED | terribly_surprising  | terribly | surprising  |  150,067.00 |
    | NEG~terribly_impressed   | 280 |   13.86 |    266.14 |  0.72 |  5.36 | 1,434.24 | 15.90 | 1.31 |          1.90 | 86,330,752 | 3,226,213 |   371 | NEGATED | terribly_impressed   | terribly | impressed   |  113,281.00 |
    | NEG~terribly_different   | 370 |   19.62 |    350.38 |  0.67 |  5.19 | 1,807.02 | 18.22 | 1.28 |          1.79 | 86,330,752 | 3,226,213 |   525 | NEGATED | terribly_different   | terribly | different   |  909,864.00 |
    | NEG~terribly_interested  | 496 |   27.09 |    468.91 |  0.65 |  5.18 | 2,373.72 | 21.05 | 1.26 |          1.75 | 86,330,752 | 3,226,213 |   725 | NEGATED | terribly_interested  | terribly | interested  |  364,497.00 |
    | NEG~terribly_surprised   | 289 |   15.02 |    273.98 |  0.68 |  5.17 | 1,430.88 | 16.12 | 1.28 |          1.82 | 86,330,752 | 3,226,213 |   402 | NEGATED | terribly_surprised   | terribly | surprised   |  104,044.00 |
    | NEG~terribly_concerned   | 416 |   27.39 |    388.61 |  0.53 |  4.49 | 1,756.14 | 19.05 | 1.18 |          1.53 | 86,330,752 | 3,226,213 |   733 | NEGATED | terribly_concerned   | terribly | concerned   |  254,407.00 |
    | NEG~terribly_interesting | 364 |   25.71 |    338.29 |  0.49 |  4.26 | 1,466.12 | 17.73 | 1.15 |          1.46 | 86,330,752 | 3,226,213 |   688 | NEGATED | terribly_interesting | terribly | interesting |  495,662.00 |
    | NEG~terribly_useful      | 226 |   15.06 |    210.94 |  0.52 |  4.25 |   946.46 | 14.03 | 1.18 |          1.52 | 86,330,752 | 3,226,213 |   403 | NEGATED | terribly_useful      | terribly | useful      |  254,276.00 |
    | NEG~terribly_exciting    | 382 |   30.94 |    351.06 |  0.42 |  3.92 | 1,402.29 | 17.96 | 1.09 |          1.34 | 86,330,752 | 3,226,213 |   828 | NEGATED | terribly_exciting    | terribly | exciting    |  236,396.00 |
    
    
    (1) terribly_surprising
        >  " It is not terribly surprising that whites subjectively perceive discrimination against members of their own group as an especially significant and growing problem , even though , objectively speaking , bias against blacks is far more pervasive , problematic and ill-intentioned , " he said .
    
    (2) terribly_impressed
        >  We were n't terribly impressed with this place on our first visit .
    
    (3) terribly_different
        >  The proposals are not terribly different from US policy going into the last major push for management reform in 2005 .
    
    (4) terribly_interested
        >  Many are also not terribly interested in the background and history that lies behind today 's news .
    
    (5) terribly_surprised
        >  Getting familiar with the Fifty / CL amplifier is easy , so do n't be terribly surprised when you find yourself up and running in no time .
    
    (6) terribly_concerned
        >  While the glitches that have prevented many potential health plan enrollees from signing up are disappointing , " we 're not terribly concerned about it , " Fetter said .
    
    (7) terribly_interesting
        >  Writer-director Rebecca Miller , in adapting her novel of the same name , burrows into the psyche of a dutiful wife and mother , but the results are not terribly interesting .
    
    (8) terribly_useful
        >  The catalog seemed fairly complete , but the books he hunted down were not terribly useful .
    
    (9) terribly_exciting
        >  Doing something like picking elements out of them is n't terribly exciting , and it 's hard immediately to see why it 's important .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_impressed_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_different_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_interested_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_surprised_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_concerned_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_interesting_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_useful_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/terribly/terribly_exciting_50ex.csv
    
    ## *inherently*
    
    
    | key                  |     f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2               | adv        | adj   |    adj_total |
    |:---------------------|------:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:-----------------|:-----------|:------|-------------:|
    | NEG~inherently_wrong | 1,648 |  102.21 |  1,545.79 |  0.57 |  4.98 | 7,241.49 | 38.08 | 1.21 |          1.59 | 86,330,752 | 3,226,213 | 2,735 | NEGATED | inherently_wrong | inherently | wrong |   187,720.00 |
    | NEG~inherently_wrong | 1,522 |  278.33 |  1,243.67 |  0.65 |  4.06 | 4,044.66 | 31.88 | 0.74 |          1.35 |  2,032,082 |   293,963 | 1,924 | NEGMIR  | inherently_wrong | inherently | wrong |    24,007.00 |
    | NEG~inherently_bad   |   794 |   68.76 |    725.24 |  0.39 |  3.92 | 2,783.25 | 25.74 | 1.06 |          1.29 | 86,330,752 | 3,226,213 | 1,840 | NEGATED | inherently_bad   | inherently | bad   |   557,528.00 |
    | NEG~inherently_bad   |   148 |   30.23 |    117.77 |  0.56 |  2.68 |   339.00 |  9.68 | 0.69 |          1.15 |  2,032,082 |   293,963 |   209 | NEGMIR  | inherently_bad   | inherently | bad   |    12,841.00 |
    | NEG~inherently_evil  |   360 |   53.14 |    306.86 |  0.22 |  2.65 |   838.38 | 16.17 | 0.83 |          0.94 | 86,330,752 | 3,226,213 | 1,422 | NEGATED | inherently_evil  | inherently | evil  |    30,742.00 |
    | NEG~inherently_good  |   283 |   52.92 |    230.08 |  0.16 |  2.16 |   530.11 | 13.68 | 0.73 |          0.81 | 86,330,752 | 3,226,213 | 1,416 | NEGATED | inherently_good  | inherently | good  | 2,037,285.00 |
    
    
    (1) inherently_wrong
        >  There is nothing inherently wrong with the song , but it does not feel like what we are used to from Toby .
    
    (2) inherently_bad
        >  Materialism is n't inherently bad because it is a good motivator of action .
    
    (3) inherently_evil
        >  Companies are not inherently evil .
    
    (4) inherently_good
        >  Although distraction is almost exclusively discussed in terms of the harm it can have on performance , it is important to understand that the actual sources of distraction are never inherently good or bad - even " good " things , such as exciting thoughts ( " We 're going to win " ) , emotions that make us feel good ( joy and surprise ) , well - intended social support ( local fans cheering us on ) , and good individual performances ( a timely big block ) can momentarily interfere with our ability to effectively stay connected to our performance .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/inherently_wrong_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/inherently_bad_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/inherently_evil_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/inherently/inherently_good_50ex.csv
    
    ## *altogether*
    
    
    | key                       |   f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |        f1 |   f2 | l1      | l2                    | adv        | adj        |   adj_total |
    |:--------------------------|----:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|----------:|-----:|:--------|:----------------------|:-----------|:-----------|------------:|
    | NEG~altogether_surprising | 487 |   20.25 |    466.75 |  0.86 |  6.72 | 2,849.79 | 21.15 | 1.38 |          2.35 | 86,330,752 | 3,226,213 |  542 | NEGATED | altogether_surprising | altogether | surprising |  150,067.00 |
    | NEG~altogether_clear      | 330 |   13.42 |    316.58 |  0.88 |  6.68 | 1,970.06 | 17.43 | 1.39 |          2.46 | 86,330,752 | 3,226,213 |  359 | NEGATED | altogether_clear      | altogether | clear      |  491,108.00 |
    | POS~altogether_different  | 938 |  805.72 |    132.28 |  0.14 |  1.47 |   257.01 |  4.32 | 0.07 |          1.55 |  2,032,082 | 1,738,105 |  942 | POSMIR  | altogether_different  | altogether | different  |   40,266.00 |
    
    
    (1) altogether_surprising
        >  the answer is not altogether surprising , and at times `` Crimson Gold '' exhibits a finger-pointing didacticism as it exposes the cruelties and inequities of a society sharply polarized by class and corrupted by selfishness , snobbery and cynicism .
    
    (2) altogether_clear
        >  What role these nanny neurons were playing in the animals ' brains and subsequent behavior was not altogether clear .
    
    (3) altogether_different
        >  and the ways they approach those challenges are not altogether different .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/altogether
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/altogether/altogether_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/altogether/altogether_clear_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/altogether/altogether_different_50ex.csv
    
    ## *only*
    
    
    | key                  |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |        f1 |    f2 | l1      | l2               | adv   | adj         |   adj_total |
    |:---------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|----------:|------:|:--------|:-----------------|:------|:------------|------------:|
    | NEG~only_delicious   |   859 |   33.18 |    825.82 |  0.93 |  8.10 |  5,393.78 | 28.18 | 1.41 |          2.88 | 86,330,752 | 3,226,213 |   888 | NEGATED | only_delicious   | only  | delicious   |   71,208.00 |
    | NEG~only_unnecessary |   493 |   19.17 |    473.83 |  0.92 |  7.52 |  3,073.46 | 21.34 | 1.41 |          2.79 | 86,330,752 | 3,226,213 |   513 | NEGATED | only_unnecessary | only  | unnecessary |   21,718.00 |
    | NEG~only_beautiful   | 1,833 |   75.56 |  1,757.44 |  0.87 |  7.37 | 10,809.43 | 41.05 | 1.38 |          2.40 | 86,330,752 | 3,226,213 | 2,022 | NEGATED | only_beautiful   | only  | beautiful   |  322,810.00 |
    | NEG~only_stylish     |   340 |   12.93 |    327.07 |  0.95 |  7.28 |  2,175.02 | 17.74 | 1.42 |          3.13 | 86,330,752 | 3,226,213 |   346 | NEGATED | only_stylish     | only  | stylish     |   27,000.00 |
    | NEG~only_unfair      |   481 |   19.06 |    461.94 |  0.91 |  7.24 |  2,941.64 | 21.06 | 1.40 |          2.62 | 86,330,752 | 3,226,213 |   510 | NEGATED | only_unfair      | only  | unfair      |   29,870.00 |
    | NEG~only_ineffective |   360 |   13.98 |    346.02 |  0.93 |  7.24 |  2,248.20 | 18.24 | 1.41 |          2.81 | 86,330,752 | 3,226,213 |   374 | NEGATED | only_ineffective | only  | ineffective |   14,957.00 |
    | NEG~only_easy        | 1,349 |   57.48 |  1,291.52 |  0.84 |  6.91 |  7,736.69 | 35.16 | 1.37 |          2.26 | 86,330,752 | 3,226,213 | 1,538 | NEGATED | only_easy        | only  | easy        |  771,307.06 |
    | NEG~only_convenient  |   358 |   14.99 |    343.01 |  0.86 |  6.48 |  2,083.48 | 18.13 | 1.38 |          2.33 | 86,330,752 | 3,226,213 |   401 | NEGATED | only_convenient  | only  | convenient  |   94,864.00 |
    | NEG~only_tasty       |   235 |    9.45 |    225.55 |  0.89 |  6.48 |  1,416.38 | 14.71 | 1.40 |          2.52 | 86,330,752 | 3,226,213 |   253 | NEGATED | only_tasty       | only  | tasty       |   34,084.00 |
    
    
    (1) only_delicious
        >  Not only delicious and refreshing , but a healthy alternative to nibbles like fried chips , soybeans are satisfying to eat when popped from their pods straight into your mouth .
    
    (2) only_unnecessary
        >  She occasionally goes too far , explaining the term within the sentence when such things are not only unnecessary , because there is a glossary at the end of the novel for those inclined to look up the terms , but bordering on insulting to the reader , especially after their first appearance with explanation because the second or even third explanation almost implies that the reader is too forgetful to remember from the first time and / or too lazy to look it up in the glossary .
    
    (3) only_beautiful
        >  Coral is not only beautiful to behold .
    
    (4) only_stylish
        >  With men's fashion having evolved to a point when there is no dearth of fashionable clothes in the market for the modern metro sexual man , the awesome thing about being a guy is that you can probably cover them all up with a few basic pieces of shoes that are not only stylish , but also extremely comfortable to walk in .
    
    (5) only_unfair
        >  The Left 's demonization of guns and gun owners is not only unfair , but it 's downright irresponsible and dangerous .
    
    (6) only_ineffective
        >  Using military means to fight terrorism is not only ineffective , but it can also backfire by encouraging more Islamic extremism .
    
    (7) only_easy
        >  It may sound boring , but setting yourself up with a budget plan is not only easy but incredibly useful for identifying unnecessary waste .
    
    (8) only_convenient
        >  This has become not only convenient , but fun , especially for the kids .
    
    (9) only_tasty
        >  So , you need to make sure that you look for the perfect dessert that is not only tasty and low fat , but also incredibly healthy .
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_delicious_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_unnecessary_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_beautiful_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_stylish_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_unfair_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_ineffective_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_easy_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_convenient_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/neg_bigram_examples/only/only_tasty_50ex.csv



```python
# for k, df in samples.items():
#     adv = k.split('_')[0]
#     output_dir = TOP_AM_DIR / 'neg_bigram_examples' / adv
#     confirm_dir(output_dir)
#     print(output_dir)
#     out_path = output_dir / f'{k}_50ex.csv'
#     print(out_path)
#     df.to_csv(out_path)
```
