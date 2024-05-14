```python
from pathlib import Path

import pandas as pd

from source.utils.sample import sample_pickle as sp
from source.utils.associate import AM_DF_DIR, adjust_assoc_columns
from source.utils import POST_PROC_DIR
FOCUS = adjust_assoc_columns(['f', 'E11', 'unexpected_f', 'unexpected_abs_sqrt',
         'am_p1_given2', 'conservative_log_ratio',
         'am_log_likelihood', 't_score',
         'mutual_information', 'am_odds_ratio_disc',
         'N', 'f1', 'f2', 'l1', 'l2'])
NEG_HITS_PATH = POST_PROC_DIR.joinpath('RBdirect/trigger-bigrams_thr0-001p.35f.pkl.gz')
pd.set_option("display.float_format", '{:,.2f}'.format)
load_path = AM_DF_DIR / 'top8_NEG-ADV_top-bigrams.2024-05-11.csv'
adv_am = pd.read_csv(AM_DF_DIR / 'Top8NEG-ADV_combined.35f-7c_2024-05-11.csv').set_index('adv')
bigram_am = pd.read_csv(load_path).set_index('key')
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
    </tr>
    <tr>
      <th>NEG~immediately_available</th>
      <td>164</td>
      <td>43.98</td>
      <td>120.02</td>
      <td>0.39</td>
      <td>1.91</td>
      <td>258.42</td>
      <td>9.37</td>
      <td>0.57</td>
      <td>0.84</td>
      <td>2032082</td>
      <td>293963</td>
      <td>304</td>
      <td>NEGMIR</td>
      <td>immediately_available</td>
      <td>immediately</td>
      <td>available</td>
      <td>14,919.00</td>
    </tr>
    <tr>
      <th>POS~only_available</th>
      <td>1030</td>
      <td>891.26</td>
      <td>138.74</td>
      <td>0.13</td>
      <td>1.64</td>
      <td>237.39</td>
      <td>4.32</td>
      <td>0.06</td>
      <td>1.14</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>1042</td>
      <td>POSMIR</td>
      <td>only_available</td>
      <td>only</td>
      <td>available</td>
      <td>14,919.00</td>
    </tr>
    <tr>
      <th>NEG~that_important</th>
      <td>115</td>
      <td>34.43</td>
      <td>80.57</td>
      <td>0.34</td>
      <td>1.47</td>
      <td>153.47</td>
      <td>7.51</td>
      <td>0.52</td>
      <td>0.74</td>
      <td>2032082</td>
      <td>293963</td>
      <td>238</td>
      <td>NEGMIR</td>
      <td>that_important</td>
      <td>that</td>
      <td>important</td>
      <td>48,905.00</td>
    </tr>
    <tr>
      <th>NEG~that_bad</th>
      <td>206</td>
      <td>79.85</td>
      <td>126.15</td>
      <td>0.23</td>
      <td>1.14</td>
      <td>175.40</td>
      <td>8.79</td>
      <td>0.41</td>
      <td>0.55</td>
      <td>2032082</td>
      <td>293963</td>
      <td>552</td>
      <td>NEGMIR</td>
      <td>that_bad</td>
      <td>that</td>
      <td>bad</td>
      <td>12,841.00</td>
    </tr>
    <tr>
      <th>POS~terribly_wrong</th>
      <td>1878</td>
      <td>1,676.45</td>
      <td>201.55</td>
      <td>0.10</td>
      <td>1.09</td>
      <td>223.10</td>
      <td>4.65</td>
      <td>0.05</td>
      <td>0.59</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>1960</td>
      <td>POSMIR</td>
      <td>terribly_wrong</td>
      <td>terribly</td>
      <td>wrong</td>
      <td>24,007.00</td>
    </tr>
  </tbody>
</table>
<p>69 rows × 17 columns</p>
</div>




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
      <th>l1_MIR</th>
      <th>l1_SET</th>
      <th>odds_r_disc_MIR</th>
      <th>odds_r_disc_SET</th>
      <th>t_MIR</th>
      <th>t_SET</th>
      <th>unexp_abs_sqrt_MIR</th>
      <th>unexp_abs_sqrt_SET</th>
      <th>unexp_f_MIR</th>
      <th>unexp_f_SET</th>
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
      <td>1,688.91</td>
      <td>219,003.46</td>
      <td>2.66</td>
      <td>6.23</td>
      <td>0.60</td>
      <td>1.30</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.43</td>
      <td>0.72</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>0.91</td>
      <td>1.90</td>
      <td>23.36</td>
      <td>196.41</td>
      <td>26.98</td>
      <td>201.47</td>
      <td>727.82</td>
      <td>40,589.32</td>
    </tr>
    <tr>
      <th>exactly</th>
      <td>1,939.47</td>
      <td>214,404.20</td>
      <td>3.51</td>
      <td>5.90</td>
      <td>0.70</td>
      <td>1.28</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.59</td>
      <td>0.67</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>1.20</td>
      <td>1.80</td>
      <td>22.86</td>
      <td>197.87</td>
      <td>25.53</td>
      <td>203.31</td>
      <td>651.85</td>
      <td>41,333.02</td>
    </tr>
    <tr>
      <th>that</th>
      <td>7,632.21</td>
      <td>781,016.11</td>
      <td>2.86</td>
      <td>5.62</td>
      <td>0.60</td>
      <td>1.25</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.44</td>
      <td>0.63</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>0.92</td>
      <td>1.72</td>
      <td>49.45</td>
      <td>383.70</td>
      <td>57.07</td>
      <td>395.04</td>
      <td>3,257.09</td>
      <td>156,053.76</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>181.20</td>
      <td>239,462.58</td>
      <td>0.79</td>
      <td>4.96</td>
      <td>0.29</td>
      <td>1.17</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.14</td>
      <td>0.52</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>0.37</td>
      <td>1.52</td>
      <td>9.83</td>
      <td>223.31</td>
      <td>14.09</td>
      <td>231.22</td>
      <td>198.40</td>
      <td>53,463.24</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>242.23</td>
      <td>209,055.78</td>
      <td>1.18</td>
      <td>4.74</td>
      <td>0.39</td>
      <td>1.14</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.21</td>
      <td>0.48</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>0.51</td>
      <td>1.45</td>
      <td>10.54</td>
      <td>212.65</td>
      <td>13.73</td>
      <td>220.78</td>
      <td>188.50</td>
      <td>48,745.17</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>847.65</td>
      <td>42,704.93</td>
      <td>1.14</td>
      <td>3.09</td>
      <td>0.32</td>
      <td>0.84</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.16</td>
      <td>0.22</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>0.41</td>
      <td>0.95</td>
      <td>20.74</td>
      <td>114.85</td>
      <td>28.71</td>
      <td>124.22</td>
      <td>824.16</td>
      <td>15,431.57</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>4,009.84</td>
      <td>13,354.33</td>
      <td>3.35</td>
      <td>3.03</td>
      <td>0.67</td>
      <td>0.84</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.54</td>
      <td>0.22</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>1.10</td>
      <td>0.95</td>
      <td>33.82</td>
      <td>64.35</td>
      <td>38.12</td>
      <td>69.64</td>
      <td>1,452.96</td>
      <td>4,849.60</td>
    </tr>
    <tr>
      <th>only</th>
      <td>-716.03</td>
      <td>261,936.36</td>
      <td>-1.73</td>
      <td>3.04</td>
      <td>-0.64</td>
      <td>0.82</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>-0.11</td>
      <td>0.21</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>-0.69</td>
      <td>0.94</td>
      <td>-43.70</td>
      <td>286.38</td>
      <td>23.97</td>
      <td>311.00</td>
      <td>-574.75</td>
      <td>96,723.87</td>
    </tr>
    <tr>
      <th>before</th>
      <td>1,080.52</td>
      <td>1,062.13</td>
      <td>5.11</td>
      <td>3.65</td>
      <td>0.83</td>
      <td>1.05</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.84</td>
      <td>0.38</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>2.58</td>
      <td>1.26</td>
      <td>14.53</td>
      <td>16.05</td>
      <td>15.73</td>
      <td>16.82</td>
      <td>247.47</td>
      <td>283.05</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>15,340.34</td>
      <td>353.58</td>
      <td>5.57</td>
      <td>0.28</td>
      <td>0.80</td>
      <td>0.11</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.77</td>
      <td>0.01</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>1.79</td>
      <td>0.11</td>
      <td>57.78</td>
      <td>16.97</td>
      <td>63.00</td>
      <td>36.21</td>
      <td>3,968.80</td>
      <td>1,310.95</td>
    </tr>
    <tr>
      <th>any</th>
      <td>2,511.26</td>
      <td>23,683.00</td>
      <td>3.48</td>
      <td>2.28</td>
      <td>0.69</td>
      <td>0.64</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.57</td>
      <td>0.13</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>1.17</td>
      <td>0.71</td>
      <td>26.24</td>
      <td>96.20</td>
      <td>29.38</td>
      <td>109.42</td>
      <td>862.98</td>
      <td>11,973.50</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>17,999.07</td>
      <td>40,303.42</td>
      <td>3.15</td>
      <td>1.43</td>
      <td>0.63</td>
      <td>0.41</td>
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.48</td>
      <td>0.06</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>1.00</td>
      <td>0.45</td>
      <td>73.86</td>
      <td>145.10</td>
      <td>84.35</td>
      <td>185.14</td>
      <td>7,114.74</td>
      <td>34,275.16</td>
    </tr>
  </tbody>
</table>
<p>12 rows × 30 columns</p>
</div>




```python
adv = 'exactly'
adv_am.loc[['exactly'], :]
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
      <th>l1_MIR</th>
      <th>l1_SET</th>
      <th>odds_r_disc_MIR</th>
      <th>odds_r_disc_SET</th>
      <th>t_MIR</th>
      <th>t_SET</th>
      <th>unexp_abs_sqrt_MIR</th>
      <th>unexp_abs_sqrt_SET</th>
      <th>unexp_f_MIR</th>
      <th>unexp_f_SET</th>
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
      <td>2032082</td>
      <td>86,330,752.00</td>
      <td>0.59</td>
      <td>0.67</td>
      <td>...</td>
      <td>NEGMIR</td>
      <td>NEGATED</td>
      <td>1.20</td>
      <td>1.80</td>
      <td>22.86</td>
      <td>197.87</td>
      <td>25.53</td>
      <td>203.31</td>
      <td>651.85</td>
      <td>41,333.02</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 30 columns</p>
</div>




```python
exactly_am = bigram_am.filter(like=adv, axis=0)
exactly_am
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
    <tr>
      <th>NEG~exactly_clear</th>
      <td>1759</td>
      <td>68.57</td>
      <td>1,690.43</td>
      <td>0.92</td>
      <td>8.30</td>
      <td>10,937.16</td>
      <td>40.31</td>
      <td>1.41</td>
      <td>2.77</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1835</td>
      <td>NEGATED</td>
      <td>exactly_clear</td>
      <td>exactly</td>
      <td>clear</td>
      <td>491,108.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_cheap</th>
      <td>693</td>
      <td>26.31</td>
      <td>666.69</td>
      <td>0.95</td>
      <td>8.28</td>
      <td>4,443.27</td>
      <td>25.33</td>
      <td>1.42</td>
      <td>3.19</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>704</td>
      <td>NEGATED</td>
      <td>exactly_cheap</td>
      <td>exactly</td>
      <td>cheap</td>
      <td>83,765.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_surprising</th>
      <td>441</td>
      <td>16.59</td>
      <td>424.41</td>
      <td>0.96</td>
      <td>7.34</td>
      <td>2,863.35</td>
      <td>20.21</td>
      <td>1.42</td>
      <td>3.51</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>444</td>
      <td>NEGATED</td>
      <td>exactly_surprising</td>
      <td>exactly</td>
      <td>surprising</td>
      <td>150,067.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_happy</th>
      <td>441</td>
      <td>17.49</td>
      <td>423.51</td>
      <td>0.90</td>
      <td>7.16</td>
      <td>2,694.69</td>
      <td>20.17</td>
      <td>1.40</td>
      <td>2.62</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>468</td>
      <td>NEGATED</td>
      <td>exactly_happy</td>
      <td>exactly</td>
      <td>happy</td>
      <td>528,511.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_ideal</th>
      <td>418</td>
      <td>16.63</td>
      <td>401.37</td>
      <td>0.90</td>
      <td>7.08</td>
      <td>2,546.29</td>
      <td>19.63</td>
      <td>1.40</td>
      <td>2.59</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>445</td>
      <td>NEGATED</td>
      <td>exactly_ideal</td>
      <td>exactly</td>
      <td>ideal</td>
      <td>42,701.00</td>
    </tr>
    <tr>
      <th>NEG~exactly_sure</th>
      <td>148</td>
      <td>21.55</td>
      <td>126.45</td>
      <td>0.85</td>
      <td>2.09</td>
      <td>560.65</td>
      <td>10.39</td>
      <td>0.84</td>
      <td>2.77</td>
      <td>2032082</td>
      <td>293963</td>
      <td>149</td>
      <td>NEGMIR</td>
      <td>exactly_sure</td>
      <td>exactly</td>
      <td>sure</td>
      <td>11,297.00</td>
    </tr>
  </tbody>
</table>
</div>




```python
exactly_am[['adj', 'l2']].values
```




    array([['sure', 'exactly_sure'],
           ['new', 'exactly_new'],
           ['easy', 'exactly_easy'],
           ['clear', 'exactly_clear'],
           ['cheap', 'exactly_cheap'],
           ['surprising', 'exactly_surprising'],
           ['happy', 'exactly_happy'],
           ['ideal', 'exactly_ideal'],
           ['sure', 'exactly_sure']], dtype=object)




```python
neg_hits_table = pd.read_pickle(NEG_HITS_PATH)
neg_hits_table.info(memory_usage='deep')
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 3148010 entries, apw_eng_19941111_0007_5:19-20-21 to pcc_eng_val_3.11301_x52781_023:32-33-34
    Data columns (total 18 columns):
     #   Column           Dtype   
    ---  ------           -----   
     0   neg_form         string  
     1   adv_form         string  
     2   adj_form         string  
     3   text_window      string  
     4   bigram_id        string  
     5   token_str        string  
     6   neg_deprel       string  
     7   neg_head         string  
     8   neg_lemma        string  
     9   adv_lemma        string  
     10  adj_lemma        string  
     11  pattern          category
     12  category         category
     13  neg_form_lower   string  
     14  adv_form_lower   string  
     15  adj_form_lower   string  
     16  bigram_lower     string  
     17  prev_form_lower  string  
    dtypes: category(2), string(16)
    memory usage: 3.8 GB



```python
neg_hits_table = neg_hits_table.filter(regex=r'^[nab].*lower|text|str|head').drop_duplicates(['text_window', 'bigram_lower', 'neg_form_lower'])
neg_hits_table.sample(3).T
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
      <th>hit_id</th>
      <th>pcc_eng_18_047.9282_x0759604_16:14-15-16</th>
      <th>pcc_eng_01_049.3187_x0780822_09:04-11-12</th>
      <th>pcc_eng_12_037.9546_x0597688_08:5-8-9</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>text_window</th>
      <td>player , it is n't very important now , but while</td>
      <td>Of course , none of this talk would be even re...</td>
      <td>I guess I should not be nearly as excited by t...</td>
    </tr>
    <tr>
      <th>token_str</th>
      <td>" If there is a possibility to sign another pl...</td>
      <td>Of course , none of this talk would be even re...</td>
      <td>I guess I should not be nearly as excited by t...</td>
    </tr>
    <tr>
      <th>neg_head</th>
      <td>ADJ</td>
      <td>ADJ</td>
      <td>ADJ</td>
    </tr>
    <tr>
      <th>neg_form_lower</th>
      <td>n't</td>
      <td>none</td>
      <td>not</td>
    </tr>
    <tr>
      <th>adv_form_lower</th>
      <td>very</td>
      <td>remotely</td>
      <td>as</td>
    </tr>
    <tr>
      <th>adj_form_lower</th>
      <td>important</td>
      <td>fair</td>
      <td>excited</td>
    </tr>
    <tr>
      <th>bigram_lower</th>
      <td>very_important</td>
      <td>remotely_fair</td>
      <td>as_excited</td>
    </tr>
  </tbody>
</table>
</div>




```python
neg_hits_table.info(memory_usage='deep')
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 3019966 entries, apw_eng_19941111_0007_5:19-20-21 to pcc_eng_val_3.11301_x52781_023:32-33-34
    Data columns (total 7 columns):
     #   Column          Dtype   
    ---  ------          -----   
     0   text_window     string  
     1   token_str       string  
     2   neg_head        category
     3   neg_form_lower  category
     4   adv_form_lower  category
     5   adj_form_lower  category
     6   bigram_lower    category
    dtypes: category(5), string(2)
    memory usage: 1.1 GB



```python
word_cols = neg_hits_table.filter(regex=r'head|lower').columns
neg_hits_table[word_cols] = neg_hits_table[word_cols].astype('category')
neg_hits_table.info(memory_usage='deep')
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 3019966 entries, apw_eng_19941111_0007_5:19-20-21 to pcc_eng_val_3.11301_x52781_023:32-33-34
    Data columns (total 7 columns):
     #   Column          Dtype   
    ---  ------          -----   
     0   text_window     string  
     1   token_str       string  
     2   neg_head        category
     3   neg_form_lower  category
     4   adv_form_lower  category
     5   adj_form_lower  category
     6   bigram_lower    category
    dtypes: category(5), string(2)
    memory usage: 1.1 GB



```python
neg_hits_table = neg_hits_table.loc[neg_hits_table.adv_form_lower.isin(adv_am.index), :]
neg_hits_table.info(memory_usage='deep')
```

    <class 'pandas.core.frame.DataFrame'>
    Index: 539311 entries, apw_eng_19941111_0112_3:10-11-12 to pcc_eng_val_3.11288_x52761_3:6-7-8
    Data columns (total 7 columns):
     #   Column          Non-Null Count   Dtype   
    ---  ------          --------------   -----   
     0   text_window     539311 non-null  string  
     1   token_str       539311 non-null  string  
     2   neg_head        539311 non-null  category
     3   neg_form_lower  539311 non-null  category
     4   adv_form_lower  539311 non-null  category
     5   adj_form_lower  539311 non-null  category
     6   bigram_lower    539311 non-null  category
    dtypes: category(5), string(2)
    memory usage: 222.5 MB



```python
# sourcery skip: use-fstring-for-concatenation
if 'all_forms_lower' not in neg_hits_table.columns: 
    neg_hits_table['all_forms_lower'] = (
        neg_hits_table.neg_form_lower.astype('string') 
        + '_' 
        + neg_hits_table.bigram_lower.astype('string')
        ).astype('category')
```


```python
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
      <th>pcc_eng_22_034.8430_x0546573_05:09-10-11</th>
      <td>not</td>
      <td>that</td>
      <td>impressive</td>
      <td>that_impressive</td>
      <td>not_that_impressive</td>
    </tr>
    <tr>
      <th>pcc_eng_13_035.2487_x0553697_28:5-6-7</th>
      <td>not</td>
      <td>only</td>
      <td>unethical</td>
      <td>only_unethical</td>
      <td>not_only_unethical</td>
    </tr>
    <tr>
      <th>pcc_eng_00_032.1666_x0503654_06:22-23-24</th>
      <td>not</td>
      <td>only</td>
      <td>cleaner</td>
      <td>only_cleaner</td>
      <td>not_only_cleaner</td>
    </tr>
  </tbody>
</table>
</div>




```python
exactly_am[['l1', 'l2']].value_counts()
```




    l1       l2                
    NEGATED  exactly_cheap         1
             exactly_clear         1
             exactly_easy          1
             exactly_happy         1
             exactly_ideal         1
             exactly_new           1
             exactly_sure          1
             exactly_surprising    1
    NEGMIR   exactly_sure          1
    Name: count, dtype: int64




```python
samples = dict.fromkeys(bigram_am.l2.unique())
for i, bigram in enumerate(exactly_am['l2'].unique(), start=1): 
    # if i > 3: #HACK 
    #     break
    print(f'\n({i}) {bigram}')
    samples[bigram] = sp(data=neg_hits_table, filters=[f'bigram_lower=={bigram}'], print_sample=False, sample_size=30,
       columns=['neg_form_lower', 'all_forms_lower', 'text_window', 'token_str'], 
       quiet=True, sort_by='all_forms_lower')
    print('    ✅')
```

    
    (1) exactly_sure
        ✅
    
    (2) exactly_new
        ✅
    
    (3) exactly_easy
        ✅
    
    (4) exactly_clear
        ✅
    
    (5) exactly_cheap
        ✅
    
    (6) exactly_surprising
        ✅
    
    (7) exactly_happy
        ✅
    
    (8) exactly_ideal
        ✅



```python
samples['exactly_happy']
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
      <th>all_forms_lower</th>
      <th>text_window</th>
      <th>token_str</th>
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
      <th>pcc_eng_13_090.1530_x1440996_03:33-34-35</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>well , she is n't exactly happy about it .</td>
      <td>Yeah yeah , we watched her drop some major pou...</td>
    </tr>
    <tr>
      <th>pcc_eng_04_068.9916_x1098213_133:18-19-20</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>and the dietitian was n't exactly happy with m...</td>
      <td>This is perfectly timed as a summer of swimmin...</td>
    </tr>
    <tr>
      <th>pcc_eng_26_060.0677_x0955057_16:4-5-6</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>The Ramseys are n't exactly happy about all of...</td>
      <td>The Ramseys are n't exactly happy about all of...</td>
    </tr>
    <tr>
      <th>pcc_eng_08_010.9912_x0161459_42:22-23-24</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>she and Klaus are n't exactly happy with one o...</td>
      <td>She 's back in the picture this Thursday , whe...</td>
    </tr>
    <tr>
      <th>pcc_eng_23_076.5838_x1221404_16:17-18-19</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>'s home life was n't exactly happy but , as he</td>
      <td>As a memoir goes , it 's really nothing specia...</td>
    </tr>
    <tr>
      <th>nyt_eng_19970509_0038_36:18-19-20</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>while the company is n't exactly happy about i...</td>
      <td>it now pays more for glass and other goods fro...</td>
    </tr>
    <tr>
      <th>pcc_eng_24_098.8582_x1582962_12:4-5-6</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>Although they were n't exactly happy with the ...</td>
      <td>Although they were n't exactly happy with the ...</td>
    </tr>
    <tr>
      <th>pcc_eng_26_046.1879_x0730746_010:3-4-5</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>Jetfire is n't exactly HAPPY to see Prowl ,</td>
      <td>Jetfire is n't exactly HAPPY to see Prowl , wh...</td>
    </tr>
    <tr>
      <th>pcc_eng_27_007.4288_x0103425_12:32-33-34</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>that the players were n't exactly happy with t...</td>
      <td>Indeed , if it had n't been for Rio Ferdinand ...</td>
    </tr>
    <tr>
      <th>pcc_eng_20_051.0249_x0808139_13:09-10-11</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>, but they are n't exactly happy .</td>
      <td>Those are love songs , but they are n't exactl...</td>
    </tr>
    <tr>
      <th>pcc_eng_11_067.0208_x1068583_12:14-15-16</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>thing and I was n't exactly happy about not be...</td>
      <td>I let him know my thoughts about the whole thi...</td>
    </tr>
    <tr>
      <th>pcc_eng_13_038.1426_x0600524_13:7-8-9</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>skipper Ravichandran Ashwin was n't exactly ha...</td>
      <td>Rahul 's skipper Ravichandran Ashwin was n't e...</td>
    </tr>
    <tr>
      <th>nyt_eng_20061009_0092_102:4-5-6</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>your characters are n't exactly happy .</td>
      <td>your characters are n't exactly happy .</td>
    </tr>
    <tr>
      <th>pcc_eng_09_055.2216_x0877233_39:5-6-7</th>
      <td>n't</td>
      <td>n't_exactly_happy</td>
      <td>Those core users are n't exactly happy either .</td>
      <td>Those core users are n't exactly happy either .</td>
    </tr>
    <tr>
      <th>pcc_eng_29_020.9088_x0321320_3:37-38-39</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>some people who were not exactly happy to see ...</td>
      <td>When Investigative Producer Michael Rey and Co...</td>
    </tr>
    <tr>
      <th>pcc_eng_14_037.7778_x0594176_220:21-22-23</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>movie and I was not exactly happy .</td>
      <td>We would do these full rehearsals and here we ...</td>
    </tr>
    <tr>
      <th>pcc_eng_16_072.5811_x1158286_04:3-4-5</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>It 's not exactly happy , in fact it</td>
      <td>It 's not exactly happy , in fact it 's kind o...</td>
    </tr>
    <tr>
      <th>apw_eng_20050120_0988_17:3-4-5</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>i 'm not exactly happy . ''</td>
      <td>i 'm not exactly happy . ''</td>
    </tr>
    <tr>
      <th>pcc_eng_27_064.7156_x1029999_43:14-15-16</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>notice that we 're not exactly happy with each...</td>
      <td>We learned that it 's okay for them to notice ...</td>
    </tr>
    <tr>
      <th>pcc_eng_01_036.6369_x0575812_47:20-21-22</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>) and I am not exactly happy with that , but</td>
      <td>The jar is clear glass ( the oil is a very dar...</td>
    </tr>
    <tr>
      <th>pcc_eng_08_063.8499_x1017997_05:3-4-5</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>I 'm not exactly happy when he does it</td>
      <td>I 'm not exactly happy when he does it against...</td>
    </tr>
    <tr>
      <th>nyt_eng_20000324_0144_16:16-17-18</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>official security firm is not exactly happy to...</td>
      <td>Spenser must procede warily over mined ground ...</td>
    </tr>
    <tr>
      <th>pcc_eng_07_033.6676_x0528329_16:7-8-9</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>a lot of people not exactly happy when it was ...</td>
      <td>There were a lot of people not exactly happy w...</td>
    </tr>
    <tr>
      <th>pcc_eng_17_060.8024_x0965952_31:3-4-5</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>I 'm not exactly happy with this but I</td>
      <td>I 'm not exactly happy with this but I push ah...</td>
    </tr>
    <tr>
      <th>pcc_eng_23_053.1671_x0842948_9:29-30-31</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>Corden hosting - is not exactly happy with Jam...</td>
      <td>Jack - who appears as a regular panellist on t...</td>
    </tr>
    <tr>
      <th>pcc_eng_29_056.0838_x0889857_076:7-8-9</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>inside the party are not exactly happy .</td>
      <td>Several people inside the party are not exactl...</td>
    </tr>
    <tr>
      <th>apw_eng_20040323_0308_18:09-10-11</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>warring factions -RRB- were not exactly happy ...</td>
      <td>`` They -LRB- Bosnian warring factions -RRB- w...</td>
    </tr>
    <tr>
      <th>pcc_eng_05_027.6318_x0431416_49:4-5-6</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>" I 'm not exactly happy about it , but</td>
      <td>" I 'm not exactly happy about it , but by the...</td>
    </tr>
    <tr>
      <th>pcc_eng_16_094.2588_x1509724_09:3-4-5</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>I 'm not exactly happy with the fact that</td>
      <td>I 'm not exactly happy with the fact that I le...</td>
    </tr>
    <tr>
      <th>pcc_eng_29_099.0310_x1583884_17:42-43-44</th>
      <td>not</td>
      <td>not_exactly_happy</td>
      <td>returned , he 's not exactly happy .</td>
      <td>The time now is the early ' 90s , and Andy is ...</td>
    </tr>
  </tbody>
</table>
</div>


