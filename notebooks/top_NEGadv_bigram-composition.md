```python
from pathlib import Path

import pandas as pd

from source.utils import POST_PROC_DIR, corners, timestamp_today, confirm_dir, print_md_table
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.sample import sample_pickle as sp

K=9
DATE=timestamp_today()
FOCUS_ORIG = ['f', 'E11', 'unexpected_f',
              'am_p1_given2', 'conservative_log_ratio',
              'am_log_likelihood', 't_score',
              'mutual_information', 'am_odds_ratio_disc',
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
adv_list = adv_am.index.to_list()
adv_list
```




    ['exactly',
     'necessarily',
     'before',
     'that',
     'remotely',
     'yet',
     'ever',
     'immediately',
     'any',
     'particularly',
     'terribly',
     'inherently',
     'altogether',
     'only']



## Load AM table for `adv~adj` comparison (bigram composition)


```python
adv_adj_am = adjust_assoc_columns(
    pd.read_pickle(AM_DF_DIR.joinpath('adv_adj/RBXadj/extra/AdvAdj_frq-thrMIN-7.35f_min200x_extra.pkl.gz'))
                                  ).filter(items=FOCUS).sort_values('LRC', ascending = False)
adv_adj_am = adv_adj_am.loc[adv_adj_am.l1.isin(adv_list), :]
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
      <th>yet~unborn</th>
      <td>463</td>
      <td>0.75</td>
      <td>462.25</td>
      <td>0.73</td>
      <td>10.47</td>
      <td>5,505.48</td>
      <td>21.48</td>
      <td>2.79</td>
      <td>3.36</td>
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
      <td>14.38</td>
      <td>2.25</td>
      <td>3.66</td>
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
      <td>17.14</td>
      <td>2.70</td>
      <td>2.86</td>
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
      <td>15.55</td>
      <td>2.56</td>
      <td>2.80</td>
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
      <td>54.96</td>
      <td>2.51</td>
      <td>2.64</td>
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
      <td>-157.63</td>
      <td>-0.99</td>
      <td>-0.99</td>
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
      <td>-228.34</td>
      <td>-1.13</td>
      <td>-1.13</td>
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
      <td>-208.17</td>
      <td>-1.19</td>
      <td>-1.20</td>
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
      <td>-306.25</td>
      <td>-1.24</td>
      <td>-1.25</td>
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
      <td>-521.18</td>
      <td>-1.39</td>
      <td>-1.41</td>
      <td>86330753</td>
      <td>464174</td>
      <td>2212989</td>
      <td>only</td>
      <td>many</td>
    </tr>
  </tbody>
</table>
<p>1197 rows × 14 columns</p>
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
hits_df.sort_index(axis=1).sample(13).iloc[:, :4]
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
      <th>adj_form_lower</th>
      <th>adv_form_lower</th>
      <th>bigram_lower</th>
      <th>text_window</th>
    </tr>
    <tr>
      <th>hit_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>pcc_eng_08_090.1989_x1444001_02:13-14</th>
      <td>fair</td>
      <td>only</td>
      <td>only_fair</td>
      <td>, it 's only fair to mention that</td>
    </tr>
    <tr>
      <th>pcc_eng_08_053.9919_x0858120_08:8-9</th>
      <td>wrong</td>
      <td>terribly</td>
      <td>terribly_wrong</td>
      <td>thought it went terribly wrong , but then</td>
    </tr>
    <tr>
      <th>pcc_eng_12_082.5650_x1317784_4:31-32</th>
      <td>available</td>
      <td>only</td>
      <td>only_available</td>
      <td>Complete Edition are only available in linen )</td>
    </tr>
    <tr>
      <th>pcc_eng_08_033.8017_x0531124_05:11-12</th>
      <td>available</td>
      <td>immediately</td>
      <td>immediately_available</td>
      <td>% absorbed and immediately available to your body</td>
    </tr>
    <tr>
      <th>pcc_eng_08_072.7341_x1161384_063:2-3</th>
      <td>notable</td>
      <td>particularly</td>
      <td>particularly_notable</td>
      <td>A particularly notable consequence of accidental</td>
    </tr>
    <tr>
      <th>pcc_eng_12_077.7996_x1241025_14:21-22</th>
      <td>worse</td>
      <td>any</td>
      <td>any_worse</td>
      <td>ca n't get any worse , right ?</td>
    </tr>
    <tr>
      <th>pcc_eng_08_083.6746_x1338628_12:12-13</th>
      <td>single</td>
      <td>ever</td>
      <td>ever_single</td>
      <td>band 's first ever single , " Dead</td>
    </tr>
    <tr>
      <th>pcc_eng_06_073.6434_x1175073_16:17-18</th>
      <td>more</td>
      <td>any</td>
      <td>any_more</td>
      <td>should not spend any more than a quarter</td>
    </tr>
    <tr>
      <th>pcc_eng_06_106.9579_x1714094_8:41-42</th>
      <td>identical</td>
      <td>exactly</td>
      <td>exactly_identical</td>
      <td>the catalysts are exactly identical . " 3</td>
    </tr>
    <tr>
      <th>pcc_eng_20_094.2016_x1505663_72:09-10</th>
      <td>good</td>
      <td>particularly</td>
      <td>particularly_good</td>
      <td>'s not a particularly good chance .</td>
    </tr>
    <tr>
      <th>pcc_eng_20_057.8673_x0918519_12:12-13</th>
      <td>possible</td>
      <td>only</td>
      <td>only_possible</td>
      <td>awakening is not only possible , but it</td>
    </tr>
    <tr>
      <th>pcc_eng_20_092.3272_x1475446_024:3-4</th>
      <td>interested</td>
      <td>only</td>
      <td>only_interested</td>
      <td>Margaret is only interested in listening to</td>
    </tr>
    <tr>
      <th>pcc_eng_20_042.1619_x0664950_04:32-33</th>
      <td>likely</td>
      <td>only</td>
      <td>only_likely</td>
      <td>that gap is only likely to increase as</td>
    </tr>
  </tbody>
</table>
</div>



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
    print_md_table(adv_adj_am.filter(like=adverb, axis=0).nlargest(K, 'LRC'), n_dec=2)
    examples = collect_examples(adv_adj_am, hits_df, adv=adverb, metric='LRC')
    
    output_dir = TOP_AM_DIR / 'any_bigram_examples' / adverb
    confirm_dir(output_dir)
    print(output_dir)

    for k, df in examples.items(): 
        out_path = output_dir.joinpath(f'{k}_50ex.csv')
        print(out_path)
        df.to_csv(out_path)
```

    
    ## *exactly*
    
    
    | key               |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |     f1 |      f2 | l1      | l2        |
    |:------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|-------:|--------:|:--------|:----------|
    | exactly~alike     | 3,040 |    9.46 |  3,030.54 |  0.23 |  8.55 | 29,939.32 | 54.96 | 2.51 |          2.64 | 86,330,753 | 61,599 |  13,261 | exactly | alike     |
    | exactly~opposite  |   498 |    6.71 |    491.29 |  0.05 |  5.94 |  3,337.27 | 22.02 | 1.87 |          1.90 | 86,330,753 | 61,599 |   9,404 | exactly | opposite  |
    | exactly~right     | 6,948 |  145.97 |  6,802.03 |  0.03 |  5.53 | 41,085.55 | 81.60 | 1.68 |          1.74 | 86,330,753 | 61,599 | 204,572 | exactly | right     |
    | exactly~zero      |   344 |    8.19 |    335.81 |  0.03 |  5.02 |  1,912.07 | 18.11 | 1.62 |          1.64 | 86,330,753 | 61,599 |  11,472 | exactly | zero      |
    | exactly~parallel  |   224 |    5.41 |    218.59 |  0.03 |  4.90 |  1,238.35 | 14.61 | 1.62 |          1.63 | 86,330,753 | 61,599 |   7,577 | exactly | parallel  |
    | exactly~sure      | 9,301 |  602.91 |  8,698.09 |  0.01 |  3.89 | 34,895.53 | 90.19 | 1.19 |          1.26 | 86,330,753 | 61,599 | 844,981 | exactly | sure      |
    | exactly~equal     |   560 |   33.61 |    526.39 |  0.01 |  3.75 |  2,108.45 | 22.24 | 1.22 |          1.23 | 86,330,753 | 61,599 |  47,099 | exactly | equal     |
    | exactly~conducive |   214 |   11.71 |    202.29 |  0.01 |  3.68 |    842.32 | 13.83 | 1.26 |          1.27 | 86,330,753 | 61,599 |  16,405 | exactly | conducive |
    | exactly~correct   |   788 |   55.83 |    732.17 |  0.01 |  3.56 |  2,723.36 | 26.08 | 1.15 |          1.16 | 86,330,753 | 61,599 |  78,240 | exactly | correct   |
    
    
    (1) exactly_alike
        >  No 2 spots are exactly alike .
    
    (2) exactly_opposite
        >  Weapons are boring , plasmids are bland and do n't feel very powerful , enemies are annoying and get really old really fast , scripted events are predictable , story totally failed to capture me , and the environment is almost exactly opposite of what I want .
    
    (3) exactly_right
        >  Try it out , and if it 's not exactly right for your business , you 'll receive a refund no questions asked .
    
    (4) exactly_zero
        >  Six is n't that many , but it 's conspicuously more than I would have heard on a similar ride 15 years ago , which would have been exactly zero .
    
    (5) exactly_parallel
        >  As we recite the story of our redemption of then we can pray to God and feel the joy of our redemption of now in an exactly parallel process .
    
    (6) exactly_sure
        >  But even those who knew about Tiny 's background in music were n't exactly sure what her " What the F -- You Gon Do ? " cut was about .
    
    (7) exactly_equal
        >  Growth in the productivity of grains has fallen to 1.2 % a year , which is exactly equal to the global population growth rate .
    
    (8) exactly_conducive
        >  Because , it seems , ADX Florence , the " Alcatraz of the Rockies " -- where Mr. Moussaoui will spend what will seem to him like an eternity before meeting his final and inexorable fate -- is not exactly conducive to the practice of glorious jihad .
    
    (9) exactly_correct
        >  THE VICE PRESIDENT : That 's exactly correct .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_alike_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_opposite_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_right_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_zero_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_parallel_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_sure_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_equal_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_conducive_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/exactly/exactly_correct_50ex.csv
    
    ## *necessarily*
    
    
    | key                        |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |     f1 |      f2 | l1          | l2             |
    |:---------------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|-------:|--------:|:------------|:---------------|
    | necessarily~indicative     | 1,456 |    8.38 |  1,447.62 |  0.11 |  7.40 | 12,331.98 | 37.94 | 2.24 |          2.30 | 86,330,753 | 56,696 |  12,760 | necessarily | indicative     |
    | necessarily~representative |   524 |   16.54 |    507.46 |  0.02 |  4.68 |  2,621.46 | 22.17 | 1.50 |          1.51 | 86,330,753 | 56,696 |  25,187 | necessarily | representative |
    | necessarily~true           | 3,786 |  229.19 |  3,556.81 |  0.01 |  3.94 | 14,387.45 | 57.81 | 1.22 |          1.25 | 86,330,753 | 56,696 | 348,994 | necessarily | true           |
    | necessarily~evil           |   273 |   20.19 |    252.81 |  0.01 |  3.30 |    919.56 | 15.30 | 1.13 |          1.14 | 86,330,753 | 56,696 |  30,742 | necessarily | evil           |
    | necessarily~illegal        |   307 |   28.91 |    278.09 |  0.01 |  2.98 |    897.54 | 15.87 | 1.03 |          1.03 | 86,330,753 | 56,696 |  44,028 | necessarily | illegal        |
    | necessarily~related        |   842 |   90.41 |    751.59 |  0.01 |  2.96 |  2,268.75 | 25.90 | 0.97 |          0.98 | 86,330,753 | 56,696 | 137,661 | necessarily | related        |
    | necessarily~wrong          | 1,110 |  123.28 |    986.72 |  0.01 |  2.95 |  2,927.86 | 29.62 | 0.95 |          0.96 | 86,330,753 | 56,696 | 187,720 | necessarily | wrong          |
    | necessarily~bad            | 2,646 |  366.15 |  2,279.85 |  0.00 |  2.71 |  6,009.62 | 44.32 | 0.86 |          0.88 | 86,330,753 | 56,696 | 557,528 | necessarily | bad            |
    | necessarily~better         | 2,373 |  488.17 |  1,884.83 |  0.00 |  2.13 |  3,803.67 | 38.69 | 0.69 |          0.70 | 86,330,753 | 56,696 | 743,338 | necessarily | better         |
    
    
    (1) necessarily_indicative
        >  Although industry observers such as Computer Weekly contributor Simon Robinson noted that such closures are not necessarily indicative of a widespread trend , cloud storage clients should take precautions to ensure they are n't left in the cold if their provider closes up shop .
    
    (2) necessarily_representative
        >  The few works now extant are not necessarily representative of his oeuvre as a whole .
    
    (3) necessarily_true
        >  According to Ricardo Warfield , " Many introverts are stereotyped as being shy but this is not necessarily true .
    
    (4) necessarily_evil
        >  I do n't even think Ulkesh was necessarily evil , just fanatic and narrow .
    
    (5) necessarily_illegal
        >  late Friday , the government 's chief spokesman said that even if the lease expires , the U.S. military 's continued use of the land is not necessarily illegal , Kyodo News reported .
    
    (6) necessarily_related
        >  The court 's decision says the county 's jurisdiction is relegated to the issues covered by the Scott River Decree , but " the question of whether Siskiyou must follow the public trust doctrine to monitor groundwater extractions that are not subject to the 1980 adjudication is not a matter necessarily related to the 1980 decree .
    
    (7) necessarily_wrong
        >  We 're not saying these are necessarily wrong , but would like to see a deeper understanding of the cultures and religions being appropriated .
    
    (8) necessarily_bad
        >  That is why religion is necessarily bad , while none of these other things are not necessarily bad .
    
    (9) necessarily_better
        >  Small DG is n't necessarily better , as it can also lead to higher dependency and sensitivity should one node fail .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_indicative_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_representative_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_true_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_evil_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_illegal_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_related_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_wrong_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_bad_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/necessarily/necessarily_better_50ex.csv
    
    ## *before*
    
    
    | key              |   f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |   f1 |      f2 | l1     | l2        |
    |:-----------------|----:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|-----:|--------:|:-------|:----------|
    | before~available | 211 |    7.51 |    203.49 |  0.00 |  4.37 | 1,062.83 | 14.01 | 1.45 |          1.59 | 86,330,753 |  748 | 866,272 | before | available |
    
    
    (1) before_available
        >  Featuring a host of features never before available in a Guitar Head this small and lightweight , the 101 Mini head delivers high octane tone and power .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/before
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/before/before_available_50ex.csv
    
    ## *that*
    
    
    | key             |      f |    exp_f |   unexp_f |   dP1 |   LRC |        G2 |      t |   MI |   odds_r_disc |          N |      f1 |      f2 | l1   | l2         |
    |:----------------|-------:|---------:|----------:|------:|------:|----------:|-------:|-----:|--------------:|-----------:|--------:|--------:|:-----|:-----------|
    | that~bad        | 23,977 | 1,617.04 | 22,359.96 |  0.04 |  3.90 | 87,578.15 | 144.40 | 1.17 |          1.23 | 86,330,753 | 250,392 | 557,528 | that | bad        |
    | that~great      | 14,577 | 1,104.72 | 13,472.28 |  0.04 |  3.71 | 49,495.75 | 111.59 | 1.12 |          1.16 | 86,330,753 | 250,392 | 380,889 | that | great      |
    | that~dissimilar |    321 |    25.57 |    295.43 |  0.03 |  3.26 |  1,043.81 |  16.49 | 1.10 |          1.11 | 86,330,753 | 250,392 |   8,816 | that | dissimilar |
    | that~hard       | 10,818 | 1,250.03 |  9,567.97 |  0.02 |  3.07 | 28,143.36 |  91.99 | 0.94 |          0.96 | 86,330,753 | 250,392 | 430,990 | that | hard       |
    | that~big        |  8,864 | 1,037.48 |  7,826.52 |  0.02 |  3.05 | 22,799.11 |  83.13 | 0.93 |          0.96 | 86,330,753 | 250,392 | 357,705 | that | big        |
    | that~stupid     |  1,669 |   194.48 |  1,474.52 |  0.02 |  2.94 |  4,268.04 |  36.09 | 0.93 |          0.95 | 86,330,753 | 250,392 |  67,052 | that | stupid     |
    | that~simple     |  9,227 | 1,238.95 |  7,988.05 |  0.02 |  2.84 | 21,487.56 |  83.16 | 0.87 |          0.89 | 86,330,753 | 250,392 | 427,167 | that | simple     |
    | that~dumb       |    501 |    63.40 |    437.60 |  0.02 |  2.67 |  1,205.74 |  19.55 | 0.90 |          0.91 | 86,330,753 | 250,392 |  21,858 | that | dumb       |
    | that~easy       | 13,969 | 2,237.08 | 11,731.92 |  0.02 |  2.60 | 28,454.39 |  99.26 | 0.80 |          0.82 | 86,330,753 | 250,392 | 771,307 | that | easy       |
    
    
    (1) that_bad
        >  The weather was n't that bad in the beginning , but it did get pretty cold .
    
    (2) that_great
        >  But if you are just taking two or more songs and trying to make something that is obviously still those songs , then it 's not that great .
    
    (3) that_dissimilar
        >  The great opening of a TV show is not that dissimilar to the first 10 pages of a movie script which is tasked with introducing a world , some likeable characters , and how that world is now going to change .
    
    (4) that_hard
        >  They 're click polls , it 's not even that hard to manipulate .
    
    (5) that_big
        >  I understand detail , but some parts , I just wanted to skip over because it got too wordy and dull over something that was n't even that big of a deal .
    
    (6) that_stupid
        >  So far I have learned : you can spoil a chicken in 5 seconds , chickens are hilarious , you should never visit your chickens without your camera , chickens really are not that stupid , and it is more awesome raising chickens than I expected !
    
    (7) that_simple
        >  Can it really be that simple ?
    
    (8) that_dumb
        >  He ca n't possibly be happy with his role as the tree -- even Zarrelian 's not that dumb .
    
    (9) that_easy
        >  Once you try out this sport you will understand and start appreciating it even more because it is not that easy as it may seem .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_bad_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_great_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_dissimilar_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_hard_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_big_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_stupid_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_simple_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_dumb_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/that/that_easy_50ex.csv
    
    ## *remotely*
    
    
    | key                  |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |     f1 |      f2 | l1       | l2          |
    |:---------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|-------:|--------:|:---------|:------------|
    | remotely~comparable  |   391 |    4.29 |    386.71 |  0.02 |  6.16 |  2,771.17 | 19.56 | 1.96 |          1.98 | 86,330,753 | 22,194 |  16,686 | remotely | comparable  |
    | remotely~plausible   |   267 |    5.32 |    261.68 |  0.01 |  5.20 |  1,573.65 | 16.01 | 1.70 |          1.71 | 86,330,753 | 22,194 |  20,711 | remotely | plausible   |
    | remotely~close       | 2,558 |  123.47 |  2,434.53 |  0.01 |  4.24 | 10,928.77 | 48.14 | 1.32 |          1.37 | 86,330,753 | 22,194 | 480,288 | remotely | close       |
    | remotely~related     |   778 |   35.39 |    742.61 |  0.01 |  4.20 |  3,352.47 | 26.62 | 1.34 |          1.36 | 86,330,753 | 22,194 | 137,661 | remotely | related     |
    | remotely~similar     |   900 |   56.92 |    843.08 |  0.00 |  3.74 |  3,318.92 | 28.10 | 1.20 |          1.22 | 86,330,753 | 22,194 | 221,410 | remotely | similar     |
    | remotely~interested  | 1,252 |   93.71 |  1,158.29 |  0.00 |  3.53 |  4,240.14 | 32.74 | 1.13 |          1.15 | 86,330,753 | 22,194 | 364,497 | remotely | interested  |
    | remotely~possible    |   904 |   93.65 |    810.35 |  0.00 |  3.02 |  2,510.49 | 26.95 | 0.98 |          1.00 | 86,330,753 | 22,194 | 364,265 | remotely | possible    |
    | remotely~funny       |   265 |   37.96 |    227.04 |  0.00 |  2.34 |    578.50 | 13.95 | 0.84 |          0.85 | 86,330,753 | 22,194 | 147,658 | remotely | funny       |
    | remotely~interesting |   596 |  127.43 |    468.57 |  0.00 |  1.92 |    912.23 | 19.19 | 0.67 |          0.68 | 86,330,753 | 22,194 | 495,662 | remotely | interesting |
    
    
    (1) remotely_comparable
        >  " Even now when you think about it in comparison to other events we 've had , summer and winter , nothing is even remotely comparable to that event , " says Goldman .
    
    (2) remotely_plausible
        >  He continues : " It is , rather , that good reasons can be given in support of the position advocated , and that the case for that position gains further in credibility from the apparent lack of any remotely plausible alternative " .
    
    (3) remotely_close
        >  The next time that Sharpe has something even remotely close to being negative about anybody in either the Ravens or Broncos organization , it will be the first time .
    
    (4) remotely_related
        >  Peace in Afghanistan , or anything remotely related to that condition , when neither side can even agree on a durable cease-fire , is at best an aspiration , but probably more likely a fantasy .
    
    (5) remotely_similar
        >  So the Inklings reader may become a Christian , in hope of in some way emulating either JRR Tolkien , CS Lewis or Charles Williams - but then he , like I , will find that there is nowadays no remotely similar church he can join ; that the Christian way of life from 1945 ( when Charles Williams died ) has gone - gone , except for some rather horrible , deceptive , almost parodic , institutional residues .
    
    (6) remotely_interested
        >  To be or not to be a police officer is a question every young person who is even remotely interested in law enforcement should ask themselves .
    
    (7) remotely_possible
        >  But Mike Pompeo will need to lead a strategic revolution inside the Trump administration at home to make it even remotely possible for the United States to succeed in its diplomatic efforts abroad .
    
    (8) remotely_funny
        >  And the thing that makes him so funny is I do n't think he 's ever trying to be remotely funny .
    
    (9) remotely_interesting
        >  We would read more biographies from the library shelves , instead of purchasing over-priced textbooks that barely scratched the surface of any remotely interesting topics .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_comparable_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_plausible_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_close_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_related_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_similar_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_interested_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_possible_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_funny_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/remotely/remotely_interesting_50ex.csv
    
    ## *yet*
    
    
    | key              |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |      f1 |      f2 | l1   | l2           |
    |:-----------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|--------:|--------:|:-----|:-------------|
    | yet~unborn       |   463 |    0.75 |    462.25 |  0.73 | 10.47 |  5,505.48 | 21.48 | 2.79 |          3.36 | 86,330,753 | 101,707 |     635 | yet  | unborn       |
    | yet~unnamed      |   771 |    2.62 |    768.38 |  0.35 |  8.47 |  7,535.14 | 27.67 | 2.47 |          2.66 | 86,330,753 | 101,707 |   2,227 | yet  | unnamed      |
    | yet~unspecified  |   219 |    0.79 |    218.21 |  0.33 |  8.06 |  2,109.33 | 14.75 | 2.44 |          2.62 | 86,330,753 | 101,707 |     669 | yet  | unspecified  |
    | yet~undetermined |   317 |    1.39 |    315.61 |  0.27 |  7.79 |  2,907.19 | 17.73 | 2.36 |          2.50 | 86,330,753 | 101,707 |   1,177 | yet  | undetermined |
    | yet~unidentified |   362 |    2.37 |    359.63 |  0.18 |  7.10 |  2,991.31 | 18.90 | 2.18 |          2.27 | 86,330,753 | 101,707 |   2,012 | yet  | unidentified |
    | yet~undiscovered |   319 |    3.02 |    315.98 |  0.12 |  6.46 |  2,383.41 | 17.69 | 2.02 |          2.08 | 86,330,753 | 101,707 |   2,561 | yet  | undiscovered |
    | yet~final        |   699 |   11.38 |    687.62 |  0.07 |  5.75 |  4,436.69 | 26.01 | 1.79 |          1.82 | 86,330,753 | 101,707 |   9,657 | yet  | final        |
    | yet~unpublished  |   253 |    3.75 |    249.25 |  0.08 |  5.69 |  1,653.12 | 15.67 | 1.83 |          1.87 | 86,330,753 | 101,707 |   3,184 | yet  | unpublished  |
    | yet~ready        | 7,838 |  283.10 |  7,554.90 |  0.03 |  4.75 | 37,767.73 | 85.33 | 1.44 |          1.49 | 86,330,753 | 101,707 | 240,297 | yet  | ready        |
    
    
    (1) yet_unborn
        >  " The legalization of the termination of pregnancy is none other than the authorization given to an adult , with the approval of an established law , to take the lives of children yet unborn and thus incapable of defending themselves .
    
    (2) yet_unnamed
        >  They show Poe , Finn and Kelly Marie Tran 's as yet unnamed character infiltrating what is believed to be a Super Star Destroyer dressed as First Order officers .
    
    (3) yet_unspecified
        >  the party also suggested that private companies should be limited to a certain percentage _ as yet unspecified _ in the industry .
    
    (4) yet_undetermined
        >  There are three kinds of images in this blog ; images copyrighted but subject to permissions or license agreements , copies of images collected by me over the last 10 years that I understand to be out of copyright , license free or as yet undetermined and photos I have taken .
    
    (5) yet_unidentified
        >  Lansdorp told the International Space Commerce Summit in London that Mars One wants to send an as yet unidentified flying object * , " a small craft that will demonstrate the technologies we need for our human colony " and is looking for partners to help it get the mission off the ground , the BBC reported .
    
    (6) yet_undiscovered
        >  Undoubtedly there are other possibilities out there that are as yet undiscovered .
    
    (7) yet_final
        >  This change in the law is applicable to all claims filed on or after the date of enactment of the VCAA , or filed before the date of enactment and not yet final as of that date .
    
    (8) yet_unpublished
        >  For example , I recently conducted a small ( as yet unpublished ) study that was in line with similar research showing how personalised coverage reduces young people 's intention to participate in political action .
    
    (9) yet_ready
        >  They were all curious about the Club but accepted that they were not yet ready to be invited for an evening out at the Club .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unborn_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unnamed_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unspecified_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_undetermined_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unidentified_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_undiscovered_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_final_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_unpublished_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/yet/yet_ready_50ex.csv
    
    ## *ever*
    
    
    | key           |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |      f1 |      f2 | l1   | l2       |
    |:--------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|--------:|--------:|:-----|:---------|
    | ever~olympic  |   229 |    0.76 |    228.24 |  0.43 |  8.37 |  2,273.22 | 15.08 | 2.48 |          2.72 | 86,330,753 | 124,592 |     529 | ever | olympic  |
    | ever~watchful |   457 |    3.15 |    453.85 |  0.21 |  7.11 |  3,744.88 | 21.23 | 2.16 |          2.26 | 86,330,753 | 124,592 |   2,183 | ever | watchful |
    | ever~closer   | 6,882 |  101.45 |  6,780.55 |  0.10 |  6.14 | 45,537.24 | 81.73 | 1.83 |          1.90 | 86,330,753 | 124,592 |  70,294 | ever | closer   |
    | ever~joint    |   205 |    2.31 |    202.69 |  0.13 |  6.10 |  1,461.42 | 14.16 | 1.95 |          2.01 | 86,330,753 | 124,592 |   1,599 | ever | joint    |
    | ever~nearer   |   245 |    3.18 |    241.82 |  0.11 |  5.92 |  1,673.29 | 15.45 | 1.89 |          1.94 | 86,330,753 | 124,592 |   2,203 | ever | nearer   |
    | ever~vigilant | 1,017 |   15.67 |  1,001.33 |  0.09 |  5.91 |  6,588.66 | 31.40 | 1.81 |          1.86 | 86,330,753 | 124,592 |  10,857 | ever | vigilant |
    | ever~mindful  |   935 |   19.85 |    915.15 |  0.07 |  5.40 |  5,442.33 | 29.93 | 1.67 |          1.71 | 86,330,753 | 124,592 |  13,757 | ever | mindful  |
    | ever~present  | 7,639 |  183.67 |  7,455.33 |  0.06 |  5.38 | 42,946.87 | 85.30 | 1.62 |          1.67 | 86,330,753 | 124,592 | 127,265 | ever | present  |
    | ever~tighter  |   437 |   11.33 |    425.67 |  0.05 |  4.97 |  2,365.89 | 20.36 | 1.59 |          1.61 | 86,330,753 | 124,592 |   7,851 | ever | tighter  |
    
    
    (1) ever_olympic
        >  I started following international volleyball the moment Marieanne Steinbrecher -- with her beauty and ice cold persona -- helped Brazil won their first ever Olympic gold medal in Beijing .
    
    (2) ever_watchful
        >  The entire set was effectively just three large steps with grave stones , which created a dark ambience and allowed the cast to ' disappear ' from Macbeth 's view into the background , but the audience could still see the ever watchful witches in the background , almost orchestrating everything from above like puppeteers .
    
    (3) ever_closer
        >  The UK 's departure from the EU is the biggest marker to date for the disintegration of both globalization and of an ever closer union in Europe .
    
    (4) ever_joint
        >  Tensions are deepening as the U.S. has sent an aircraft carrier to waters off the peninsula and is conducting its biggest - ever joint military exercises with South Korea .
    
    (5) ever_nearer
        >  round-the-world pilot Linda Finch left Australia on Wednesday bound for the Pacific , heading ever nearer to the site where aviator Amelia Earhart disappeared 60 years ago .
    
    (6) ever_vigilant
        >  China , ever vigilant at maintaining relations with the government in power , extended an invitation to Sata to pay a state visit to President Hu.
    
    (7) ever_mindful
        >  Here a bhikkhu , gone to the forest or to the root of a tree or to an empty hut , sits down ; having folded his legs crosswise , set his body erect , and established mindfulness in front of him , ever mindful he breathes in , mindful he breathes out .
    
    (8) ever_present
        >  Cancer is probably the one question about which more has been written and spoken than any single subject which has exercised mankind individually and when gathered together in conventions and councils , because it has remained an ever present destroyer from times beyond modern human appreciation .
    
    (9) ever_tighter
        >  Given the constraints of today 's media environment , with its limited resources and ever tighter deadlines , I am always impressed with how well these men and women do their jobs .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_olympic_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_watchful_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_closer_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_joint_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_nearer_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_vigilant_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_mindful_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_present_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/ever/ever_tighter_50ex.csv
    
    ## *immediately*
    
    
    | key                      |      f |    exp_f |   unexp_f |   dP1 |   LRC |         G2 |      t |   MI |   odds_r_disc |          N |      f1 |      f2 | l1          | l2           |
    |:-------------------------|-------:|---------:|----------:|------:|------:|-----------:|-------:|-----:|--------------:|-----------:|--------:|--------:|:------------|:-------------|
    | immediately~accretive    |    243 |     0.68 |    242.32 |  0.43 |  8.65 |   2,499.70 |  15.55 | 2.56 |          2.80 | 86,330,753 | 103,177 |     565 | immediately | accretive    |
    | immediately~adjacent     |  1,714 |     6.49 |  1,707.51 |  0.31 |  8.37 |  16,336.57 |  41.24 | 2.42 |          2.59 | 86,330,753 | 103,177 |   5,427 | immediately | adjacent     |
    | immediately~apparent     |  5,260 |    76.61 |  5,183.39 |  0.08 |  6.12 |  34,820.38 |  71.47 | 1.84 |          1.90 | 86,330,753 | 103,177 |  64,104 | immediately | apparent     |
    | immediately~clear        | 27,066 |   586.94 | 26,479.06 |  0.05 |  5.57 | 163,404.00 | 160.95 | 1.66 |          1.82 | 86,330,753 | 103,177 | 491,108 | immediately | clear        |
    | immediately~recognizable |  1,891 |    46.08 |  1,844.92 |  0.05 |  5.25 |  10,481.04 |  42.43 | 1.61 |          1.64 | 86,330,753 | 103,177 |  38,560 | immediately | recognizable |
    | immediately~available    | 30,725 | 1,035.31 | 29,689.69 |  0.03 |  4.90 | 159,614.02 | 169.38 | 1.47 |          1.64 | 86,330,753 | 103,177 | 866,272 | immediately | available    |
    | immediately~recognisable |    381 |    11.11 |    369.89 |  0.04 |  4.76 |   1,970.36 |  18.95 | 1.54 |          1.56 | 86,330,753 | 103,177 |   9,293 | immediately | recognisable |
    | immediately~evident      |  1,466 |    72.77 |  1,393.23 |  0.02 |  4.16 |   6,069.42 |  36.39 | 1.30 |          1.32 | 86,330,753 | 103,177 |  60,888 | immediately | evident      |
    | immediately~obvious      |  4,305 |   231.26 |  4,073.74 |  0.02 |  4.13 |  17,278.24 |  62.09 | 1.27 |          1.30 | 86,330,753 | 103,177 | 193,498 | immediately | obvious      |
    
    
    (1) immediately_accretive
        >  Robert Mead , a Magellan spokesman , said the company expects the transaction to be `` immediately accretive '' to earnings .
    
    (2) immediately_adjacent
        >  The cave was apparently structured immediately adjacent to the Void , the theoretical non-space which surrounds the outer planes .
    
    (3) immediately_apparent
        >  It is immediately apparent that Another Destiny Project does not follow the conventional Italian Power Metal sound .
    
    (4) immediately_clear
        >  it was not immediately clear how he ended up in the grinder at about 5:30 a.m. -LRB- 0430GMT -RRB- .
    
    (5) immediately_recognizable
        >  Exclusive and immediately recognizable , these watches are yet another expression of Dolce &Gabbana 's style .
    
    (6) immediately_available
        >  few details were immediately available on the deal that was several years in the making , but the pact would also give U.S. airlines _ presumably those carrying passengers and cargo _ more rights to fly into Hong Kong then onto other points .
    
    (7) immediately_recognisable
        >  One of the few immediately recognisable and popular fighters at Flyweight , a revitalised Mc Call looked likely to still be a strong contender at 125 lbs .
    
    (8) immediately_evident
        >  Ninomiya 's talent was immediately evident ; she loved group instruction .
    
    (9) immediately_obvious
        >  It may not be immediately obvious why all this matters , but to get a good reading on that , it really boils down to two things :
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_accretive_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_adjacent_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_apparent_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_clear_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognizable_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_available_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_recognisable_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_evident_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/immediately/immediately_obvious_50ex.csv
    
    ## *any*
    
    
    | key         |      f |   exp_f |   unexp_f |   dP1 |   LRC |         G2 |      t |   MI |   odds_r_disc |          N |     f1 |      f2 | l1   | l2      |
    |:------------|-------:|--------:|----------:|------:|------:|-----------:|-------:|-----:|--------------:|-----------:|-------:|--------:|:-----|:--------|
    | any~clearer |  1,053 |   14.58 |  1,038.42 |  0.08 |  6.05 |   7,030.69 |  32.00 | 1.86 |          1.90 | 86,330,753 | 94,153 |  13,369 | any  | clearer |
    | any~happier |  1,472 |   21.27 |  1,450.73 |  0.07 |  6.02 |   9,706.11 |  37.81 | 1.84 |          1.88 | 86,330,753 | 94,153 |  19,501 | any  | happier |
    | any~closer  |  3,911 |   76.66 |  3,834.34 |  0.05 |  5.63 |  23,460.34 |  61.31 | 1.71 |          1.75 | 86,330,753 | 94,153 |  70,294 | any  | closer  |
    | any~safer   |  1,471 |   29.21 |  1,441.79 |  0.05 |  5.53 |   8,748.49 |  37.59 | 1.70 |          1.73 | 86,330,753 | 94,153 |  26,779 | any  | safer   |
    | any~weirder |    218 |    3.52 |    214.48 |  0.07 |  5.52 |   1,385.02 |  14.53 | 1.79 |          1.82 | 86,330,753 | 94,153 |   3,228 | any  | weirder |
    | any~better  | 35,471 |  810.69 | 34,660.31 |  0.05 |  5.49 | 215,244.70 | 184.03 | 1.64 |          1.86 | 86,330,753 | 94,153 | 743,338 | any  | better  |
    | any~easier  | 10,860 |  259.22 | 10,600.78 |  0.04 |  5.38 |  61,653.02 | 101.72 | 1.62 |          1.69 | 86,330,753 | 94,153 | 237,680 | any  | easier  |
    | any~wiser   |    245 |    4.70 |    240.30 |  0.06 |  5.28 |   1,471.06 |  15.35 | 1.72 |          1.74 | 86,330,753 | 94,153 |   4,309 | any  | wiser   |
    | any~worse   |  8,487 |  233.57 |  8,253.43 |  0.04 |  5.16 |  45,548.31 |  89.59 | 1.56 |          1.62 | 86,330,753 | 94,153 | 214,166 | any  | worse   |
    
    
    (1) any_clearer
        >  " We cannot be any clearer .
    
    (2) any_happier
        >  Brown probably wo n't be any happier about that link than he is when he hears his name associated with UCLA , but both Brown and Nelson employed Popovich as an assistant , which represents Popovich 's only NBA coaching experience .
    
    (3) any_closer
        >  They 're not getting any closer ? " said a voice , too drowned out by more repeater fire .
    
    (4) any_safer
        >  `` Did you feel any safer ? ''
    
    (5) any_weirder
        >  I mean , come on , can this whole thing get any weirder ?
    
    (6) any_better
        >  I silenced who I truly was to be who I thought I was , I did n't know any better .
    
    (7) any_easier
        >  in actuality , it 's not any easier than going into the dealership . ''
    
    (8) any_wiser
        >  Being young , I 'd let them think they were getting away with something , without anyone being any wiser .
    
    (9) any_worse
        >  As though things could n't get any worse , the newly arrived mother extracts a banana from her bag and gives it to her daughter .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_clearer_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_happier_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_closer_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_safer_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_weirder_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_better_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_easier_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_wiser_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/any/any_worse_50ex.csv
    
    ## *particularly*
    
    
    | key                     |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |      f1 |     f2 | l1           | l2         |
    |:------------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|--------:|-------:|:-------------|:-----------|
    | particularly~galling    |   573 |   15.55 |    557.45 |  0.24 |  5.23 |  3,165.46 | 23.29 | 1.57 |          1.69 | 86,330,753 | 575,961 |  2,331 | particularly | galling    |
    | particularly~acute      | 2,918 |  113.00 |  2,805.00 |  0.17 |  4.80 | 13,874.42 | 51.93 | 1.41 |          1.49 | 86,330,753 | 575,961 | 16,937 | particularly | acute      |
    | particularly~noteworthy | 2,501 |  115.78 |  2,385.22 |  0.14 |  4.48 | 10,955.62 | 47.69 | 1.33 |          1.40 | 86,330,753 | 575,961 | 17,355 | particularly | noteworthy |
    | particularly~thorny     |   328 |   12.96 |    315.04 |  0.16 |  4.46 |  1,544.42 | 17.40 | 1.40 |          1.48 | 86,330,753 | 575,961 |  1,942 | particularly | thorny     |
    | particularly~fond       | 4,445 |  265.59 |  4,179.41 |  0.11 |  4.10 | 17,178.32 | 62.69 | 1.22 |          1.28 | 86,330,753 | 575,961 | 39,809 | particularly | fond       |
    | particularly~egregious  | 1,896 |  114.43 |  1,781.57 |  0.10 |  4.02 |  7,281.73 | 40.92 | 1.22 |          1.27 | 86,330,753 | 575,961 | 17,152 | particularly | egregious  |
    | particularly~nasty      | 2,373 |  146.35 |  2,226.65 |  0.10 |  4.01 |  9,012.88 | 45.71 | 1.21 |          1.26 | 86,330,753 | 575,961 | 21,937 | particularly | nasty      |
    | particularly~virulent   |   527 |   32.58 |    494.42 |  0.10 |  3.82 |  1,997.47 | 21.54 | 1.21 |          1.26 | 86,330,753 | 575,961 |  4,884 | particularly | virulent   |
    | particularly~worrisome  | 1,096 |   76.54 |  1,019.46 |  0.09 |  3.73 |  3,891.11 | 30.79 | 1.16 |          1.20 | 86,330,753 | 575,961 | 11,473 | particularly | worrisome  |
    
    
    (1) particularly_galling
        >  Howard told a radio station that the decision was particularly galling because it came just as Canberra released U.S. dlrs 300 million of Australia 's commitment to the International Monetary Fund 's bailout package for Indonesia .
    
    (2) particularly_acute
        >  The issue is particularly acute in Sweden , home to one of the highest number of migrants fleeing conflicts in Syria , Afghanistan and elsewhere in the Middle East .
    
    (3) particularly_noteworthy
        >  Some particularly noteworthy features of the flora wildflowers found in the Burren include the curious mixture of Arctic-Alpine and Mediterranean species , and calcicole ( lime-loving ) and calcifuge ( lime-hating ) species , as well as the wealth of orchids - 22 of Ireland 's 27 native orchid species are found in the region .
    
    (4) particularly_thorny
        >  `` It 's a particularly thorny issue in smaller buildings , '' Ms. Arougheti said .
    
    (5) particularly_fond
        >  He frequently meets with older members of the family - none of whom seem particularly fond of his uncle - and he shows a great deal of respect for them .
    
    (6) particularly_egregious
        >  Consider a particularly egregious example .
    
    (7) particularly_nasty
        >  If you have been subjected to some particularly nasty Yelp reviews , you may want to talk to a small business attorney to learn about the legal remedies that are available to you .
    
    (8) particularly_virulent
        >  Both companies had been infected with particularly virulent strains of i Encrypt malware , and the attacks crippled systems at both companies for days .
    
    (9) particularly_worrisome
        >  " Judge Reade 's apparent attempts to minimize her participation in the raid raise new suspicions and bolster doubts about Judge Reade 's impartiality in circumstances that are particularly worrisome , " said Lewin .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_galling_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_acute_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_noteworthy_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_thorny_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_fond_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_egregious_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_nasty_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_virulent_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/particularly/particularly_worrisome_50ex.csv
    
    ## *terribly*
    
    
    | key                   |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |     f1 |      f2 | l1       | l2           |
    |:----------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|-------:|--------:|:---------|:-------------|
    | terribly~wrong        | 7,248 |  152.59 |  7,095.41 |  0.04 |  5.54 | 42,791.46 | 83.34 | 1.68 |          1.74 | 86,330,753 | 70,174 | 187,720 | terribly | wrong        |
    | terribly~sorry        | 1,358 |   59.18 |  1,298.82 |  0.02 |  4.34 |  5,959.56 | 35.25 | 1.36 |          1.38 | 86,330,753 | 70,174 |  72,808 | terribly | sorry        |
    | terribly~inefficient  |   219 |    8.92 |    210.08 |  0.02 |  4.12 |    986.37 | 14.20 | 1.39 |          1.40 | 86,330,753 | 70,174 |  10,976 | terribly | inefficient  |
    | terribly~sad          | 1,354 |   89.78 |  1,264.22 |  0.01 |  3.72 |  4,857.19 | 34.36 | 1.18 |          1.19 | 86,330,753 | 70,174 | 110,447 | terribly | sad          |
    | terribly~unfair       |   411 |   24.28 |    386.72 |  0.01 |  3.72 |  1,559.12 | 19.08 | 1.23 |          1.24 | 86,330,753 | 70,174 |  29,870 | terribly | unfair       |
    | terribly~lonely       |   201 |   15.62 |    185.38 |  0.01 |  3.16 |    658.45 | 13.08 | 1.11 |          1.12 | 86,330,753 | 70,174 |  19,221 | terribly | lonely       |
    | terribly~disappointed |   721 |   69.42 |    651.58 |  0.01 |  3.10 |  2,082.92 | 24.27 | 1.02 |          1.02 | 86,330,753 | 70,174 |  85,399 | terribly | disappointed |
    | terribly~flawed       |   269 |   25.44 |    243.56 |  0.01 |  2.95 |    784.49 | 14.85 | 1.02 |          1.03 | 86,330,753 | 70,174 |  31,294 | terribly | flawed       |
    | terribly~upset        |   517 |   54.09 |    462.91 |  0.01 |  2.93 |  1,414.59 | 20.36 | 0.98 |          0.99 | 86,330,753 | 70,174 |  66,546 | terribly | upset        |
    
    
    (1) terribly_wrong
        >  Something 's terribly wrong when a man's most effective avenue of material provision for his family is his own death .
    
    (2) terribly_sorry
        >  a hand-lettered sign nearby at a makeshift roadblock read : `` Terribly sorry , no access to outsiders . ''
    
    (3) terribly_inefficient
        >  Now , melting an entire lake is terribly inefficient and slow .
    
    (4) terribly_sad
        >  I have hoped to raise my children immersed in a hearty broth of faith because God is our origin and our destiny , and it would be terribly sad for them to go through life unaware that they are , in Thomas Merton 's words , shining like the sun .
    
    (5) terribly_unfair
        >  I realize that sounds terribly unfair to my wife , but in truth , she 's very happy in the kitchen .
    
    (6) terribly_lonely
        >  There was little to no supplies , and the boy had grown terribly lonely that even the company of cats could not quench his thirst for human companionship .
    
    (7) terribly_disappointed
        >  I was terribly disappointed but somehow able to openly and honestly look at the tragic images to determine what went wrong , and then let them go .
    
    (8) terribly_flawed
        >  something is terribly flawed with the Department of Homeland Security when it
    
    (9) terribly_upset
        >  `` On the whole , these guys in north Tehran who are terribly upset about what is happening are not ready to die . ''
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_wrong_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_sorry_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_inefficient_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_sad_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_unfair_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_lonely_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_disappointed_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_flawed_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/terribly/terribly_upset_50ex.csv
    
    ## *inherently*
    
    
    | key                     |     f |   exp_f |   unexp_f |   dP1 |   LRC |       G2 |     t |   MI |   odds_r_disc |          N |     f1 |     f2 | l1         | l2           |
    |:------------------------|------:|--------:|----------:|------:|------:|---------:|------:|-----:|--------------:|-----------:|-------:|-------:|:-----------|:-------------|
    | inherently~governmental |   295 |    0.60 |    294.40 |  0.32 |  8.96 | 3,178.72 | 17.14 | 2.70 |          2.86 | 86,330,753 | 55,088 |    933 | inherently | governmental |
    | inherently~unequal      |   423 |    4.02 |    418.98 |  0.07 |  6.43 | 3,132.80 | 20.37 | 2.02 |          2.06 | 86,330,753 | 55,088 |  6,300 | inherently | unequal      |
    | inherently~evil         | 1,422 |   19.62 |  1,402.38 |  0.05 |  6.04 | 9,478.40 | 37.19 | 1.86 |          1.89 | 86,330,753 | 55,088 | 30,742 | inherently | evil         |
    | inherently~unstable     |   894 |   16.11 |    877.89 |  0.03 |  5.59 | 5,470.41 | 29.36 | 1.74 |          1.77 | 86,330,753 | 55,088 | 25,245 | inherently | unstable     |
    | inherently~flawed       | 1,028 |   19.97 |  1,008.03 |  0.03 |  5.49 | 6,138.46 | 31.44 | 1.71 |          1.73 | 86,330,753 | 55,088 | 31,294 | inherently | flawed       |
    | inherently~unsafe       |   297 |    6.19 |    290.81 |  0.03 |  5.18 | 1,728.45 | 16.87 | 1.68 |          1.70 | 86,330,753 | 55,088 |  9,693 | inherently | unsafe       |
    | inherently~racist       |   541 |   14.97 |    526.03 |  0.02 |  4.88 | 2,846.10 | 22.62 | 1.56 |          1.57 | 86,330,753 | 55,088 | 23,467 | inherently | racist       |
    | inherently~unfair       |   588 |   19.06 |    568.94 |  0.02 |  4.66 | 2,911.59 | 23.46 | 1.49 |          1.50 | 86,330,753 | 55,088 | 29,870 | inherently | unfair       |
    | inherently~inferior     |   275 |    8.18 |    266.82 |  0.02 |  4.64 | 1,406.64 | 16.09 | 1.53 |          1.54 | 86,330,753 | 55,088 | 12,817 | inherently | inferior     |
    
    
    (1) inherently_governmental
        >  " It is quite obvious , " said Richard M. Nixon in March 1976 , " that there are certain inherently governmental actions which , if undertaken by the sovereign in protection of the interest of the nation 's security , are lawful but which , if undertaken by private persons are not . "
    
    (2) inherently_unequal
        >  Supporters said the relationship between a lawyer and client is inherently unequal , so any sexual relationship is potentially coercive .
    
    (3) inherently_evil
        >  As humans are challenged in their belief that all dragons are inherently evil , so too is the reader challenged in what they may deem the faults or missteps of the various characters .
    
    (4) inherently_unstable
        >  Yet , as Constanze Guthenke shows in this volume , Athenian space is inherently unstable because its ownership is uncertain and contested .
    
    (5) inherently_flawed
        >  It 's hard to find anything inherently flawed with this combat system , other than the fact that it should feel more exciting that it does .
    
    (6) inherently_unsafe
        >  Goodell has spent the bulk of his tenure paying lip service to player safety in an inherently unsafe game , and in a matter of weeks he has undermined everything he has ever said about the issue by installing shitty game managers to officiate real , important games .
    
    (7) inherently_racist
        >  It 's because of a white , working - class revolt , it 's because of James Comey , it 's because Trump was impermeable to scandal , it 's because of Wikileaks , it 's because Trump is anti-establishment personified , it 's because Trump was a marketing genius , it 's because people despised the Clinton dynasty , it 's because neoliberalism is a flawed ideology , it 's because of voter suppression , it 's because a significant number of US nationals are inherently racist and / or sexist .
    
    (8) inherently_unfair
        >  in that you find the genesis of why he hung on so tenaciously at San Francisco even when I pushed him very hard to escape what seemed to be an inherently unfair future .
    
    (9) inherently_inferior
        >  There is Ellis , who considers the natives to be inherently inferior and uses all manner of insult to express his perspective .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_governmental_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unequal_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_evil_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unstable_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_flawed_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unsafe_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_racist_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_unfair_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/inherently/inherently_inferior_50ex.csv
    
    ## *altogether*
    
    
    | key                   |     f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |     t |   MI |   odds_r_disc |          N |     f1 |      f2 | l1         | l2         |
    |:----------------------|------:|--------:|----------:|------:|------:|----------:|------:|-----:|--------------:|-----------:|-------:|--------:|:-----------|:-----------|
    | altogether~different  | 5,068 |  217.49 |  4,850.51 |  0.01 |  4.46 | 23,495.10 | 68.13 | 1.37 |          1.49 | 86,330,753 | 20,636 | 909,864 | altogether | different  |
    | altogether~surprising |   542 |   35.87 |    506.13 |  0.00 |  3.60 |  1,945.41 | 21.74 | 1.18 |          1.19 | 86,330,753 | 20,636 | 150,067 | altogether | surprising |
    | altogether~new        | 1,030 |   76.80 |    953.20 |  0.00 |  3.52 |  3,489.21 | 29.70 | 1.13 |          1.15 | 86,330,753 | 20,636 | 321,311 | altogether | new        |
    | altogether~clear      |   359 |  117.39 |    241.61 |  0.00 |  1.21 |    322.34 | 12.75 | 0.49 |          0.49 | 86,330,753 | 20,636 | 491,108 | altogether | clear      |
    
    
    (1) altogether_different
        >  The You Tube app currently propagating across the Play Store is version a huge jump from the previous ( and not altogether different )
    
    (2) altogether_surprising
        >  This particularity had been noted without further elaboration in the the existing catalog record for the manuscript , and is not altogether surprising .
    
    (3) altogether_new
        >  Some are modifications to existing Google applications , while others are altogether new .
    
    (4) altogether_clear
        >  It 's first recorded in 1907 ; where it comes from is not altogether clear , but a popular ballad , Paddy Malone in Australia , was noted in the 1870s and appeared in a collection by Banjo Paterson in 1906 .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_different_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_surprising_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_new_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/altogether/altogether_clear_50ex.csv
    
    ## *only*
    
    
    | key              |      f |   exp_f |   unexp_f |   dP1 |   LRC |        G2 |      t |   MI |   odds_r_disc |          N |      f1 |      f2 | l1   | l2          |
    |:-----------------|-------:|--------:|----------:|------:|------:|----------:|-------:|-----:|--------------:|-----------:|--------:|--------:|:-----|:------------|
    | only~half-joking |    209 |    1.17 |    207.83 |  0.96 |  9.48 |  2,116.01 |  14.38 | 2.25 |          3.66 | 86,330,753 | 464,174 |     217 | only | half-joking |
    | only~temporary   |  5,980 |   81.82 |  5,898.18 |  0.39 |  6.78 | 42,280.75 |  76.27 | 1.86 |          2.08 | 86,330,753 | 464,174 |  15,218 | only | temporary   |
    | only~so-so       |    274 |    3.95 |    270.05 |  0.37 |  6.20 |  1,897.98 |  16.31 | 1.84 |          2.04 | 86,330,753 | 464,174 |     735 | only | so-so       |
    | only~momentary   |    207 |    2.89 |    204.11 |  0.38 |  6.18 |  1,450.10 |  14.19 | 1.85 |          2.06 | 86,330,753 | 464,174 |     538 | only | momentary   |
    | only~approximate |    238 |    5.05 |    232.95 |  0.25 |  5.40 |  1,431.38 |  15.10 | 1.67 |          1.80 | 86,330,753 | 464,174 |     940 | only | approximate |
    | only~occasional  |    396 |    9.53 |    386.47 |  0.22 |  5.30 |  2,271.07 |  19.42 | 1.62 |          1.73 | 86,330,753 | 464,174 |   1,772 | only | occasional  |
    | only~advisory    |    241 |    5.88 |    235.12 |  0.21 |  5.15 |  1,374.41 |  15.15 | 1.61 |          1.72 | 86,330,753 | 464,174 |   1,094 | only | advisory    |
    | only~natural     | 16,324 |  642.39 | 15,681.61 |  0.13 |  4.81 | 76,966.08 | 122.74 | 1.41 |          1.48 | 86,330,753 | 464,174 | 119,476 | only | natural     |
    | only~partial     |    885 |   32.75 |    852.25 |  0.14 |  4.70 |  4,257.88 |  28.65 | 1.43 |          1.50 | 86,330,753 | 464,174 |   6,092 | only | partial     |
    
    
    (1) only_half-joking
        >  `` You know Shakespeare ? William Shakespeare ? We 're peddling him on the street , '' Pacino tells a crowd , and he 's only half-joking .
    
    (2) only_temporary
        >  The life that we live on the planet earth is only temporary .
    
    (3) only_so-so
        >  Something about Mary was only so-so ... and do n't let me get into their other shite .
    
    (4) only_momentary
        >  The effect was only momentary however as Ray swam up close .
    
    (5) only_approximate
        >  The given west direction from Yarmouth is only approximate .
    
    (6) only_occasional
        >  here at Cyanika , the displaced have received only occasional distributions of beans and wheat flour from international organizations .
    
    (7) only_advisory
        >  The high court 's response is only advisory but carries tremendous influence .
    
    (8) only_natural
        >  Hall of Fame quarterback Troy Aikman said Favre 's frustration is only natural , but his continued enthusiasm on the field sets the right example for young players .
    
    (9) only_partial
        >  Britain and Greece have so far provided only partial data for 2001 and will be added to the analysis later this month , the agency said .
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_half-joking_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_temporary_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_so-so_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_momentary_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_approximate_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_occasional_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_advisory_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_natural_50ex.csv
    /share/compling/projects/sanpi/results/top_AM/any_bigram_examples/only/only_partial_50ex.csv

