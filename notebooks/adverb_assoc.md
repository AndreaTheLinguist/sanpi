# Identifying Adverbs with Strongest Negative Environment Associations


```python
from pathlib import Path

import pandas as pd
from pprint import pprint

from source.utils import PKL_SUFF, SAMPLE_ADV, print_md_table
from source.utils.associate import AM_DF_DIR, TOP_AM_DIR, adjust_assoc_columns
from source.utils.general import print_iter, snake_to_camel, timestamp_today

SET_FLOOR = 2000
MIR_FLOOR = 200
K = 9
```

Set columns and diplay settings


```python
FOCUS = ['f', 'E11', 'unexpected_f',
         'am_p1_given2', 'conservative_log_ratio',
         'am_log_likelihood', 't_score',
         'mutual_information', 'am_odds_ratio_disc',
         'N', 'f1', 'f2', 'l1', 'l2']
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 90)
pd.set_option("display.precision", 2)
pd.set_option("styler.format.precision", 2)
pd.set_option("styler.format.thousands", ",")
pd.set_option("display.float_format", '{:,.2f}'.format)
pd.set_option("styler.render.repr", "html")
```

## Set paths and load adverb association tables


```python
POLAR_DIR = AM_DF_DIR.joinpath('polar')

polar_adv_dirs = []
# results/assoc_df/polar/RBdirect/adv/extra/polarized-adv_35f-7c_min5000x_extra.pkl.gz
adv_am_paths = {
    p.name: tuple(
        p.joinpath('adv/extra').glob(
            f'*35f-7c_min{SET_FLOOR if p.name == "RBdirect" else MIR_FLOOR}x*{PKL_SUFF}')
    )[0]
    for p in POLAR_DIR.iterdir()}

setdiff_adv = pd.read_pickle(adv_am_paths['RBdirect'])
mirror_adv = pd.read_pickle(adv_am_paths['NEGmirror'])
```


```python
adjust_assoc_columns(setdiff_adv.sample(K).sort_values('conservative_log_ratio', ascending=False)[FOCUS])
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
      <th>...</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>COM~allegedly</th>
      <td>18082</td>
      <td>17,424.03</td>
      <td>657.97</td>
      <td>0.04</td>
      <td>3.51</td>
      <td>1,204.83</td>
      <td>...</td>
      <td>1.56</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>18101</td>
      <td>COMPLEMENT</td>
      <td>allegedly</td>
    </tr>
    <tr>
      <th>COM~beyond</th>
      <td>14706</td>
      <td>14,178.14</td>
      <td>527.86</td>
      <td>0.04</td>
      <td>3.09</td>
      <td>929.12</td>
      <td>...</td>
      <td>1.39</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>14729</td>
      <td>COMPLEMENT</td>
      <td>beyond</td>
    </tr>
    <tr>
      <th>COM~mysteriously</th>
      <td>3034</td>
      <td>2,924.38</td>
      <td>109.62</td>
      <td>0.04</td>
      <td>1.19</td>
      <td>196.53</td>
      <td>...</td>
      <td>1.42</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>3038</td>
      <td>COMPLEMENT</td>
      <td>mysteriously</td>
    </tr>
    <tr>
      <th>COM~infinitely</th>
      <td>22838</td>
      <td>22,271.69</td>
      <td>566.31</td>
      <td>0.02</td>
      <td>1.14</td>
      <td>511.54</td>
      <td>...</td>
      <td>0.47</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>23137</td>
      <td>COMPLEMENT</td>
      <td>infinitely</td>
    </tr>
    <tr>
      <th>COM~deathly</th>
      <td>3329</td>
      <td>3,265.14</td>
      <td>63.86</td>
      <td>0.02</td>
      <td>0.10</td>
      <td>40.77</td>
      <td>...</td>
      <td>0.31</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>3392</td>
      <td>COMPLEMENT</td>
      <td>deathly</td>
    </tr>
    <tr>
      <th>COM~psychologically</th>
      <td>10283</td>
      <td>10,182.39</td>
      <td>100.61</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>29.08</td>
      <td>...</td>
      <td>0.13</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>10578</td>
      <td>COMPLEMENT</td>
      <td>psychologically</td>
    </tr>
    <tr>
      <th>COM~conceptually</th>
      <td>3160</td>
      <td>3,140.00</td>
      <td>20.00</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>3.60</td>
      <td>...</td>
      <td>0.08</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>3262</td>
      <td>COMPLEMENT</td>
      <td>conceptually</td>
    </tr>
    <tr>
      <th>COM~nearly</th>
      <td>189453</td>
      <td>190,813.43</td>
      <td>-1,360.43</td>
      <td>-0.01</td>
      <td>-0.17</td>
      <td>-245.96</td>
      <td>...</td>
      <td>-0.08</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>198227</td>
      <td>COMPLEMENT</td>
      <td>nearly</td>
    </tr>
    <tr>
      <th>COM~excessively</th>
      <td>17590</td>
      <td>17,945.76</td>
      <td>-355.76</td>
      <td>-0.02</td>
      <td>-0.39</td>
      <td>-163.86</td>
      <td>...</td>
      <td>-0.19</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>18643</td>
      <td>COMPLEMENT</td>
      <td>excessively</td>
    </tr>
  </tbody>
</table>
<p>9 rows × 14 columns</p>
</div>




```python
adjust_assoc_columns(mirror_adv.sample(K).sort_values('conservative_log_ratio', ascending=False)[FOCUS])
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
      <th>...</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>POS~n't</th>
      <td>25788</td>
      <td>22,272.85</td>
      <td>3,515.15</td>
      <td>0.14</td>
      <td>3.66</td>
      <td>6,244.46</td>
      <td>...</td>
      <td>1.24</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>26040</td>
      <td>POSMIR</td>
      <td>n't</td>
    </tr>
    <tr>
      <th>POS~deeply</th>
      <td>5506</td>
      <td>4,781.31</td>
      <td>724.69</td>
      <td>0.13</td>
      <td>2.68</td>
      <td>1,175.70</td>
      <td>...</td>
      <td>1.04</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>5590</td>
      <td>POSMIR</td>
      <td>deeply</td>
    </tr>
    <tr>
      <th>POS~similarly</th>
      <td>783</td>
      <td>684.27</td>
      <td>98.73</td>
      <td>0.12</td>
      <td>1.19</td>
      <td>145.90</td>
      <td>...</td>
      <td>0.88</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>800</td>
      <td>POSMIR</td>
      <td>similarly</td>
    </tr>
    <tr>
      <th>POS~delightfully</th>
      <td>373</td>
      <td>323.32</td>
      <td>49.68</td>
      <td>0.13</td>
      <td>0.41</td>
      <td>82.73</td>
      <td>...</td>
      <td>1.06</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>378</td>
      <td>POSMIR</td>
      <td>delightfully</td>
    </tr>
    <tr>
      <th>POS~else</th>
      <td>983</td>
      <td>903.23</td>
      <td>79.77</td>
      <td>0.08</td>
      <td>0.31</td>
      <td>58.59</td>
      <td>...</td>
      <td>0.35</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>1056</td>
      <td>POSMIR</td>
      <td>else</td>
    </tr>
    <tr>
      <th>POS~sadly</th>
      <td>282</td>
      <td>244.62</td>
      <td>37.38</td>
      <td>0.13</td>
      <td>0.00</td>
      <td>61.50</td>
      <td>...</td>
      <td>1.03</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>286</td>
      <td>POSMIR</td>
      <td>sadly</td>
    </tr>
    <tr>
      <th>POS~politically</th>
      <td>2730</td>
      <td>2,783.25</td>
      <td>-53.25</td>
      <td>-0.02</td>
      <td>0.00</td>
      <td>-6.85</td>
      <td>...</td>
      <td>-0.06</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>3254</td>
      <td>POSMIR</td>
      <td>politically</td>
    </tr>
    <tr>
      <th>POS~plainly</th>
      <td>263</td>
      <td>231.79</td>
      <td>31.21</td>
      <td>0.12</td>
      <td>0.00</td>
      <td>41.01</td>
      <td>...</td>
      <td>0.72</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>271</td>
      <td>POSMIR</td>
      <td>plainly</td>
    </tr>
    <tr>
      <th>POS~sufficiently</th>
      <td>648</td>
      <td>744.99</td>
      <td>-96.99</td>
      <td>-0.11</td>
      <td>-0.46</td>
      <td>-73.86</td>
      <td>...</td>
      <td>-0.31</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>871</td>
      <td>POSMIR</td>
      <td>sufficiently</td>
    </tr>
  </tbody>
</table>
<p>9 rows × 14 columns</p>
</div>



## Calculate "Most Negative" Adverbs for each Polarity Approximation


```python
def get_top_vals(df: pd.DataFrame,
                 index_like: str = 'NEG',
                 metric_filter: str | list = 'conservative_log_ratio',
                 k: int = 10,
                 val_col: str = None,
                 ignore_neg_adv: bool = True):
    env_df = df.copy().loc[df.conservative_log_ratio >=
                           1].filter(like=index_like, axis=0)
    if ignore_neg_adv:
        env_df = env_df.loc[~df.l2.isin(
            ("n't", 'not', 'barely', 'never', 'no', 'none')), :]
    if isinstance(metric_filter, str):
        metric_filter = [metric_filter]

    top = pd.concat([env_df.nlargest(k, m) for m in metric_filter]
                    ).drop_duplicates(keep='first')

    if val_col:
        top = top[[val_col] + metric_filter]

    return top.sort_values(metric_filter[0], ascending=False)


[setdiff_top15, mirror_top15] = [
    get_top_vals(
        adv_df, k=15,
        metric_filter=['am_p1_given2', 'conservative_log_ratio'])
    for adv_df in (setdiff_adv, mirror_adv)
]
adjust_assoc_columns(setdiff_top15.filter(items=FOCUS).reset_index())
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
      <th>key</th>
      <th>f</th>
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>dP1</th>
      <th>LRC</th>
      <th>...</th>
      <th>odds_r_disc</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>l1</th>
      <th>l2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NEG~necessarily</td>
      <td>42708</td>
      <td>2,118.68</td>
      <td>40,589.32</td>
      <td>0.72</td>
      <td>6.23</td>
      <td>...</td>
      <td>1.90</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>56694</td>
      <td>NEGATED</td>
      <td>necessarily</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NEG~exactly</td>
      <td>43635</td>
      <td>2,301.98</td>
      <td>41,333.02</td>
      <td>0.67</td>
      <td>5.90</td>
      <td>...</td>
      <td>1.80</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>61599</td>
      <td>NEGATED</td>
      <td>exactly</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NEG~that</td>
      <td>165411</td>
      <td>9,357.24</td>
      <td>156,053.76</td>
      <td>0.63</td>
      <td>5.62</td>
      <td>...</td>
      <td>1.72</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>250392</td>
      <td>NEGATED</td>
      <td>that</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NEG~immediately</td>
      <td>57319</td>
      <td>3,855.76</td>
      <td>53,463.24</td>
      <td>0.52</td>
      <td>4.96</td>
      <td>...</td>
      <td>1.52</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>103177</td>
      <td>NEGATED</td>
      <td>immediately</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NEG~yet</td>
      <td>52546</td>
      <td>3,800.83</td>
      <td>48,745.17</td>
      <td>0.48</td>
      <td>4.74</td>
      <td>...</td>
      <td>1.45</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>101707</td>
      <td>NEGATED</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NEG~terribly</td>
      <td>18054</td>
      <td>2,622.43</td>
      <td>15,431.57</td>
      <td>0.22</td>
      <td>3.09</td>
      <td>...</td>
      <td>0.95</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>70174</td>
      <td>NEGATED</td>
      <td>terribly</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEG~remotely</td>
      <td>5679</td>
      <td>829.40</td>
      <td>4,849.60</td>
      <td>0.22</td>
      <td>3.03</td>
      <td>...</td>
      <td>0.95</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>22194</td>
      <td>NEGATED</td>
      <td>remotely</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NEG~only</td>
      <td>114070</td>
      <td>17,346.13</td>
      <td>96,723.87</td>
      <td>0.21</td>
      <td>3.04</td>
      <td>...</td>
      <td>0.94</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>464168</td>
      <td>NEGATED</td>
      <td>only</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NEG~altogether</td>
      <td>4575</td>
      <td>771.17</td>
      <td>3,803.82</td>
      <td>0.18</td>
      <td>2.75</td>
      <td>...</td>
      <td>0.87</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>20636</td>
      <td>NEGATED</td>
      <td>altogether</td>
    </tr>
    <tr>
      <th>9</th>
      <td>NEG~entirely</td>
      <td>63708</td>
      <td>11,354.35</td>
      <td>52,353.65</td>
      <td>0.17</td>
      <td>2.74</td>
      <td>...</td>
      <td>0.84</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>303833</td>
      <td>NEGATED</td>
      <td>entirely</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NEG~overly</td>
      <td>24707</td>
      <td>4,561.35</td>
      <td>20,145.65</td>
      <td>0.17</td>
      <td>2.66</td>
      <td>...</td>
      <td>0.82</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>122058</td>
      <td>NEGATED</td>
      <td>overly</td>
    </tr>
    <tr>
      <th>11</th>
      <td>NEG~merely</td>
      <td>5944</td>
      <td>1,330.68</td>
      <td>4,613.32</td>
      <td>0.13</td>
      <td>2.26</td>
      <td>...</td>
      <td>0.71</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>35608</td>
      <td>NEGATED</td>
      <td>merely</td>
    </tr>
    <tr>
      <th>12</th>
      <td>NEG~any</td>
      <td>15492</td>
      <td>3,518.50</td>
      <td>11,973.50</td>
      <td>0.13</td>
      <td>2.28</td>
      <td>...</td>
      <td>0.71</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>94152</td>
      <td>NEGATED</td>
      <td>any</td>
    </tr>
    <tr>
      <th>13</th>
      <td>NEG~always</td>
      <td>104605</td>
      <td>24,330.10</td>
      <td>80,274.90</td>
      <td>0.12</td>
      <td>2.28</td>
      <td>...</td>
      <td>0.70</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>651053</td>
      <td>NEGATED</td>
      <td>always</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NEG~directly</td>
      <td>8317</td>
      <td>2,034.48</td>
      <td>6,282.52</td>
      <td>0.12</td>
      <td>2.13</td>
      <td>...</td>
      <td>0.67</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>54441</td>
      <td>NEGATED</td>
      <td>directly</td>
    </tr>
  </tbody>
</table>
<p>15 rows × 15 columns</p>
</div>




```python
adjust_assoc_columns(mirror_top15.filter(items=FOCUS).reset_index())
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
      <th>key</th>
      <th>f</th>
      <th>exp_f</th>
      <th>unexp_f</th>
      <th>dP1</th>
      <th>LRC</th>
      <th>...</th>
      <th>odds_r_disc</th>
      <th>N</th>
      <th>f1</th>
      <th>f2</th>
      <th>l1</th>
      <th>l2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NEG~before</td>
      <td>290</td>
      <td>42.53</td>
      <td>247.47</td>
      <td>0.84</td>
      <td>5.11</td>
      <td>...</td>
      <td>2.58</td>
      <td>2032082</td>
      <td>293963</td>
      <td>294</td>
      <td>NEGMIR</td>
      <td>before</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NEG~ever</td>
      <td>4718</td>
      <td>749.20</td>
      <td>3,968.80</td>
      <td>0.77</td>
      <td>5.57</td>
      <td>...</td>
      <td>1.79</td>
      <td>2032082</td>
      <td>293963</td>
      <td>5179</td>
      <td>NEGMIR</td>
      <td>ever</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NEG~exactly</td>
      <td>813</td>
      <td>161.15</td>
      <td>651.85</td>
      <td>0.59</td>
      <td>3.51</td>
      <td>...</td>
      <td>1.20</td>
      <td>2032082</td>
      <td>293963</td>
      <td>1114</td>
      <td>NEGMIR</td>
      <td>exactly</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NEG~any</td>
      <td>1082</td>
      <td>219.02</td>
      <td>862.98</td>
      <td>0.57</td>
      <td>3.48</td>
      <td>...</td>
      <td>1.17</td>
      <td>2032082</td>
      <td>293963</td>
      <td>1514</td>
      <td>NEGMIR</td>
      <td>any</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NEG~remotely</td>
      <td>1846</td>
      <td>393.04</td>
      <td>1,452.96</td>
      <td>0.54</td>
      <td>3.35</td>
      <td>...</td>
      <td>1.10</td>
      <td>2032082</td>
      <td>293963</td>
      <td>2717</td>
      <td>NEGMIR</td>
      <td>remotely</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NEG~particularly</td>
      <td>9278</td>
      <td>2,163.26</td>
      <td>7,114.74</td>
      <td>0.48</td>
      <td>3.15</td>
      <td>...</td>
      <td>1.00</td>
      <td>2032082</td>
      <td>293963</td>
      <td>14954</td>
      <td>NEGMIR</td>
      <td>particularly</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NEG~that</td>
      <td>4338</td>
      <td>1,080.91</td>
      <td>3,257.09</td>
      <td>0.44</td>
      <td>2.86</td>
      <td>...</td>
      <td>0.92</td>
      <td>2032082</td>
      <td>293963</td>
      <td>7472</td>
      <td>NEGMIR</td>
      <td>that</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NEG~necessarily</td>
      <td>971</td>
      <td>243.18</td>
      <td>727.82</td>
      <td>0.43</td>
      <td>2.66</td>
      <td>...</td>
      <td>0.91</td>
      <td>2032082</td>
      <td>293963</td>
      <td>1681</td>
      <td>NEGMIR</td>
      <td>necessarily</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NEG~inherently</td>
      <td>2872</td>
      <td>817.19</td>
      <td>2,054.81</td>
      <td>0.36</td>
      <td>2.42</td>
      <td>...</td>
      <td>0.79</td>
      <td>2032082</td>
      <td>293963</td>
      <td>5649</td>
      <td>NEGMIR</td>
      <td>inherently</td>
    </tr>
    <tr>
      <th>9</th>
      <td>NEG~overtly</td>
      <td>392</td>
      <td>129.91</td>
      <td>262.09</td>
      <td>0.29</td>
      <td>1.71</td>
      <td>...</td>
      <td>0.66</td>
      <td>2032082</td>
      <td>293963</td>
      <td>898</td>
      <td>NEGMIR</td>
      <td>overtly</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NEG~intrinsically</td>
      <td>432</td>
      <td>143.36</td>
      <td>288.64</td>
      <td>0.29</td>
      <td>1.73</td>
      <td>...</td>
      <td>0.66</td>
      <td>2032082</td>
      <td>293963</td>
      <td>991</td>
      <td>NEGMIR</td>
      <td>intrinsically</td>
    </tr>
    <tr>
      <th>11</th>
      <td>NEG~especially</td>
      <td>1573</td>
      <td>636.51</td>
      <td>936.49</td>
      <td>0.21</td>
      <td>1.49</td>
      <td>...</td>
      <td>0.52</td>
      <td>2032082</td>
      <td>293963</td>
      <td>4400</td>
      <td>NEGMIR</td>
      <td>especially</td>
    </tr>
    <tr>
      <th>12</th>
      <td>NEG~yet</td>
      <td>320</td>
      <td>131.50</td>
      <td>188.50</td>
      <td>0.21</td>
      <td>1.18</td>
      <td>...</td>
      <td>0.51</td>
      <td>2032082</td>
      <td>293963</td>
      <td>909</td>
      <td>NEGMIR</td>
      <td>yet</td>
    </tr>
    <tr>
      <th>13</th>
      <td>NEG~fully</td>
      <td>1668</td>
      <td>735.46</td>
      <td>932.54</td>
      <td>0.18</td>
      <td>1.31</td>
      <td>...</td>
      <td>0.46</td>
      <td>2032082</td>
      <td>293963</td>
      <td>5084</td>
      <td>NEGMIR</td>
      <td>fully</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NEG~terribly</td>
      <td>1579</td>
      <td>754.84</td>
      <td>824.16</td>
      <td>0.16</td>
      <td>1.14</td>
      <td>...</td>
      <td>0.41</td>
      <td>2032082</td>
      <td>293963</td>
      <td>5218</td>
      <td>NEGMIR</td>
      <td>terribly</td>
    </tr>
  </tbody>
</table>
<p>15 rows × 15 columns</p>
</div>




```python
def load_backup(lower_floor: int = 100,
                loaded_path: Path = adv_am_paths['RBdirect']) -> pd.DataFrame:
    located_paths = tuple(loaded_path.parent.glob(
        f'*35f-7c_min{lower_floor}x*{PKL_SUFF}'))
    if any(located_paths):
        backup_df = pd.read_pickle(located_paths[0])

        backup_df = backup_df.filter(like='NEG', axis=0).filter(
            items=FOCUS).reset_index().set_index('l2')
        backup_df.index.name = 'adv'
        return backup_df
    else:
        return []



def fill_empties(name_1, name_2, both, loaded_paths):
    for name in (name_1, name_2):
        name = name.strip('_')
        path = loaded_paths['RBdirect'] if name == 'SET' else loaded_paths['NEGmirror']
        floor = 100
        if any(both[f'f_{name}'].isna()):

            neg_backup = load_backup(floor, loaded_path=path)
            neg_backup.columns = (pd.Series(adjust_assoc_columns(neg_backup.columns)
                                           ) + f'_{name}').to_list()
            if any(neg_backup):
                cats = both.select_dtypes(include='category').columns
                both[cats] = both[cats].astype('string')
                backup_cats = neg_backup.select_dtypes(
                    include='category').columns
                neg_backup[backup_cats] = neg_backup[backup_cats].astype(
                    'string')

                undefined = both.index[both[f'f_{name}'].isna()].to_list()
                both.loc[undefined,
                         neg_backup.columns] = neg_backup.filter(items=undefined, axis=0)

                both[cats] = both[cats].astype('category')

    return both

```


```python
def combine_top(df_1: pd.DataFrame,
                name_1: str,
                df_2: pd.DataFrame,
                name_2: str,
                env_filter: str = 'NEG',
                filter_items: list = FOCUS,
                k: int = 10) -> pd.DataFrame:

    top_dfs = [get_top_vals(adv_df, index_like=env_filter, k=k,
                            metric_filter=['am_p1_given2',
                                           'conservative_log_ratio']
                            )
               for adv_df in [df_1, df_2]]
    for i, name in enumerate([name_1, name_2]):

        print_iter(
            top_dfs[i].l2.to_list(), bullet='1.',
            header=f'{name}: union of top {k} adverbs ranked by deltaP(1|2) and LRC')

    top_adv = pd.concat((top_dfs[0].l2, top_dfs[1].l2)).drop_duplicates()

    print_iter(
        top_adv, bullet='1.',
        header=f'Union of top adverbs for {name_1} and {name_2}. (Novel {name_2} adverbs listed last)')

    df_1, df_2 = [d.filter(items=filter_items)
                  .filter(like=env_filter, axis=0)
                  .reset_index().set_index('l2')
                  for d in [df_1, df_2]]
    df_1 = adjust_assoc_columns(df_1)
    df_2 = adjust_assoc_columns(df_2)

    both = pd.DataFrame(index=top_adv)
    name_1, name_2 = [f"_{n.strip('_')}" for n in [name_1, name_2]]
    both = both.join(df_1).join(df_2, lsuffix=name_1,
                                rsuffix=name_2).sort_index(axis=1)
    # ! Empty cells need to be filled _before_ calculating mean
    both = fill_empties(name_1, name_2, both, adv_am_paths)

    for metric in (both.select_dtypes(include='number').columns.to_series()
                   .str.replace(r'_(MIR|SET)$', '', regex=True).unique()):

        both[f'mean_{snake_to_camel(metric)}']= both.filter(
            regex=f"^{metric}").agg('mean', axis='columns')

    return both
```

## Compile top NEG~adverb associations across both approximation methods


```python
C = combine_top(setdiff_adv.copy(), 'SET',
                mirror_adv.copy(), 'MIR', k=K)
```

    
    SET: union of top 9 adverbs ranked by deltaP(1|2) and LRC
    1. necessarily
    1. exactly
    1. that
    1. immediately
    1. yet
    1. terribly
    1. remotely
    1. only
    1. altogether
    
    MIR: union of top 9 adverbs ranked by deltaP(1|2) and LRC
    1. before
    1. ever
    1. exactly
    1. any
    1. remotely
    1. particularly
    1. that
    1. necessarily
    1. inherently
    
    Union of top adverbs for SET and MIR. (Novel MIR adverbs listed last)
    1. necessarily
    1. exactly
    1. that
    1. immediately
    1. yet
    1. terribly
    1. remotely
    1. only
    1. altogether
    1. before
    1. ever
    1. any
    1. particularly
    1. inherently


SET: union of top 5 adverbs ranked by $\Delta P(\texttt{env}|\texttt{adv})$ and LRC
1. necessarily
1. exactly
1. that
1. immediately
1. yet

MIR: union of top 5 adverbs ranked by $\Delta P(\texttt{env}|\texttt{adv})$ and LRC
1. before
1. ever
1. exactly
1. any
1. remotely

Union of top adverbs for SET and MIR. (Novel MIR adverbs listed last)
1. necessarily
1. exactly
1. that
1. immediately
1. yet
1. before
1. ever
1. any
1. remotely


```python
print(C.columns.tolist())
```

    ['G2_MIR', 'G2_SET', 'LRC_MIR', 'LRC_SET', 'MI_MIR', 'MI_SET', 'N_MIR', 'N_SET', 'dP1_MIR', 'dP1_SET', 'exp_f_MIR', 'exp_f_SET', 'f1_MIR', 'f1_SET', 'f2_MIR', 'f2_SET', 'f_MIR', 'f_SET', 'key_MIR', 'key_SET', 'l1_MIR', 'l1_SET', 'odds_r_disc_MIR', 'odds_r_disc_SET', 't_MIR', 't_SET', 'unexp_f_MIR', 'unexp_f_SET', 'mean_G2', 'mean_LRC', 'mean_MI', 'mean_N', 'mean_dP1', 'mean_expF', 'mean_f1', 'mean_f2', 'mean_f', 'mean_oddsRDisc', 'mean_t', 'mean_unexpF']



```python
main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in ('LRC', 'P1', 'G2')],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2'] ]) 
                              ).to_list()
print(main_cols_ordered)
```

    ['LRC_MIR', 'LRC_SET', 'mean_LRC', 'dP1_MIR', 'dP1_SET', 'mean_dP1', 'G2_MIR', 'G2_SET', 'mean_G2', 'f_MIR', 'f_SET', 'f1_MIR', 'f1_SET', 'f2_MIR', 'f2_SET']



```python
C.index.name = 'adv'
C=C.sort_values('mean_LRC', ascending=False)
pd.set_option('display.max_columns', 16)
C[main_cols_ordered]
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
      <th>LRC_MIR</th>
      <th>LRC_SET</th>
      <th>mean_LRC</th>
      <th>dP1_MIR</th>
      <th>dP1_SET</th>
      <th>mean_dP1</th>
      <th>G2_MIR</th>
      <th>G2_SET</th>
      <th>mean_G2</th>
      <th>f_MIR</th>
      <th>f_SET</th>
      <th>f1_MIR</th>
      <th>f1_SET</th>
      <th>f2_MIR</th>
      <th>f2_SET</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>exactly</th>
      <td>3.51</td>
      <td>5.90</td>
      <td>4.71</td>
      <td>0.59</td>
      <td>0.67</td>
      <td>0.63</td>
      <td>1,939.47</td>
      <td>214,404.20</td>
      <td>108,171.83</td>
      <td>813.00</td>
      <td>43,635.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>1,114.00</td>
      <td>61,599.00</td>
    </tr>
    <tr>
      <th>necessarily</th>
      <td>2.66</td>
      <td>6.23</td>
      <td>4.44</td>
      <td>0.43</td>
      <td>0.72</td>
      <td>0.57</td>
      <td>1,688.91</td>
      <td>219,003.46</td>
      <td>110,346.18</td>
      <td>971.00</td>
      <td>42,708.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>1,681.00</td>
      <td>56,694.00</td>
    </tr>
    <tr>
      <th>before</th>
      <td>5.11</td>
      <td>3.65</td>
      <td>4.38</td>
      <td>0.84</td>
      <td>0.38</td>
      <td>0.61</td>
      <td>1,080.52</td>
      <td>1,062.13</td>
      <td>1,071.32</td>
      <td>290.00</td>
      <td>311.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>294.00</td>
      <td>748.00</td>
    </tr>
    <tr>
      <th>that</th>
      <td>2.86</td>
      <td>5.62</td>
      <td>4.24</td>
      <td>0.44</td>
      <td>0.63</td>
      <td>0.53</td>
      <td>7,632.21</td>
      <td>781,016.11</td>
      <td>394,324.16</td>
      <td>4,338.00</td>
      <td>165,411.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>7,472.00</td>
      <td>250,392.00</td>
    </tr>
    <tr>
      <th>remotely</th>
      <td>3.35</td>
      <td>3.03</td>
      <td>3.19</td>
      <td>0.54</td>
      <td>0.22</td>
      <td>0.38</td>
      <td>4,009.84</td>
      <td>13,354.33</td>
      <td>8,682.08</td>
      <td>1,846.00</td>
      <td>5,679.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>2,717.00</td>
      <td>22,194.00</td>
    </tr>
    <tr>
      <th>yet</th>
      <td>1.18</td>
      <td>4.74</td>
      <td>2.96</td>
      <td>0.21</td>
      <td>0.48</td>
      <td>0.34</td>
      <td>242.23</td>
      <td>209,055.78</td>
      <td>104,649.01</td>
      <td>320.00</td>
      <td>52,546.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>909.00</td>
      <td>101,707.00</td>
    </tr>
    <tr>
      <th>ever</th>
      <td>5.57</td>
      <td>0.28</td>
      <td>2.92</td>
      <td>0.77</td>
      <td>0.01</td>
      <td>0.39</td>
      <td>15,340.34</td>
      <td>353.58</td>
      <td>7,846.96</td>
      <td>4,718.00</td>
      <td>5,967.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>5,179.00</td>
      <td>124,592.00</td>
    </tr>
    <tr>
      <th>immediately</th>
      <td>0.79</td>
      <td>4.96</td>
      <td>2.88</td>
      <td>0.14</td>
      <td>0.52</td>
      <td>0.33</td>
      <td>181.20</td>
      <td>239,462.58</td>
      <td>119,821.89</td>
      <td>407.00</td>
      <td>57,319.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>1,442.00</td>
      <td>103,177.00</td>
    </tr>
    <tr>
      <th>any</th>
      <td>3.48</td>
      <td>2.28</td>
      <td>2.88</td>
      <td>0.57</td>
      <td>0.13</td>
      <td>0.35</td>
      <td>2,511.26</td>
      <td>23,683.00</td>
      <td>13,097.13</td>
      <td>1,082.00</td>
      <td>15,492.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>1,514.00</td>
      <td>94,152.00</td>
    </tr>
    <tr>
      <th>particularly</th>
      <td>3.15</td>
      <td>1.43</td>
      <td>2.29</td>
      <td>0.48</td>
      <td>0.06</td>
      <td>0.27</td>
      <td>17,999.07</td>
      <td>40,303.42</td>
      <td>29,151.24</td>
      <td>9,278.00</td>
      <td>55,799.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>14,954.00</td>
      <td>575,960.00</td>
    </tr>
    <tr>
      <th>terribly</th>
      <td>1.14</td>
      <td>3.09</td>
      <td>2.12</td>
      <td>0.16</td>
      <td>0.22</td>
      <td>0.19</td>
      <td>847.65</td>
      <td>42,704.93</td>
      <td>21,776.29</td>
      <td>1,579.00</td>
      <td>18,054.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>5,218.00</td>
      <td>70,174.00</td>
    </tr>
    <tr>
      <th>inherently</th>
      <td>2.42</td>
      <td>1.78</td>
      <td>2.10</td>
      <td>0.36</td>
      <td>0.09</td>
      <td>0.23</td>
      <td>4,160.38</td>
      <td>7,333.55</td>
      <td>5,746.97</td>
      <td>2,872.00</td>
      <td>6,847.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>5,649.00</td>
      <td>55,088.00</td>
    </tr>
    <tr>
      <th>altogether</th>
      <td>-0.65</td>
      <td>2.75</td>
      <td>1.05</td>
      <td>-0.08</td>
      <td>0.18</td>
      <td>0.05</td>
      <td>-123.22</td>
      <td>9,468.00</td>
      <td>4,672.39</td>
      <td>112.00</td>
      <td>4,575.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>1,808.00</td>
      <td>20,636.00</td>
    </tr>
    <tr>
      <th>only</th>
      <td>-1.73</td>
      <td>3.04</td>
      <td>0.66</td>
      <td>-0.11</td>
      <td>0.21</td>
      <td>0.05</td>
      <td>-716.03</td>
      <td>261,936.36</td>
      <td>130,610.17</td>
      <td>173.00</td>
      <td>114,070.00</td>
      <td>293,963.00</td>
      <td>3,226,213.00</td>
      <td>5,169.00</td>
      <td>464,168.00</td>
    </tr>
  </tbody>
</table>
</div>



Save full adverb selection as `.csv`


```python
C.to_csv(TOP_AM_DIR / f'Top{K}_NEG-ADV_combined.35f-7c_{timestamp_today()}.csv')
```

Save `all-columns`, `means`, and `MAIN` as markdown formatted tables


```python
C.to_markdown(floatfmt=',.2f', intfmt=',', buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_all-columns.35f-7c_{timestamp_today()}.md')
C.filter(like='mean_').to_markdown(floatfmt=',.2f', intfmt=',', buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_means.35f-7c_{timestamp_today()}.md')
C[main_cols_ordered].to_markdown(floatfmt=',.2f', intfmt=',', buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_MAIN.35f-7c_{timestamp_today()}.md')
```

## Collect bigrams corresponding to top adverbs


```python
# results/assoc_df/polar/RBdirect/bigram/polarized-bigram_35f-7c_min1000x.pkl.gz
bigram_floor = 200
bigram_dfs = {d.name:
              pd.read_pickle(
                  tuple(d.joinpath('bigram/extra')
                        .glob(f'*35f-7c*min{bigram_floor//2 if d.name == "NEGmirror" else bigram_floor}x*.pkl.gz')
                        )[0])
              for d in POLAR_DIR.iterdir()}
```


```python
def show_adv_bigrams(sample_size, C, bigram_dfs, column_list: list = None) -> dict:

    print('# Top bigrams corresponding to top adverbs\n')
    print(timestamp_today())
    patterns = list(bigram_dfs.keys())
    top_adverbs = C.index
    bigram_samples = dict.fromkeys(top_adverbs)
    bigrams = []
    adj = []
    for adv in top_adverbs:
        print(f'\n## _{adv}_\n')
        adv_top = None
        bigram_samples[adv] = dict.fromkeys(patterns + ['both', 'adj'])
        adj_for_adv = []
        for pat, bdf in bigram_dfs.items():
            bdf = bdf[FOCUS+['adv', 'adj', 'adj_total']]
            bdf.columns = adjust_assoc_columns(bdf.columns)
            bdf = bdf.loc[bdf.LRC >= 1, :]

            adv_pat_bigrams = bdf.filter(
                like=adv, axis=0).nlargest(sample_size, 'LRC')
            # print(adv_top_bigrams)
            if adv_pat_bigrams.empty:
                print(f'No bigrams found in loaded `{pat}` AM table.')
            else:
                column_list = column_list or bdf.columns
                print_md_table(adv_pat_bigrams[column_list], n_dec=2,
                               title=f'### Top {sample_size} `{pat}` "{adv}_*" bigrams (sorted by `LRC`; `LRC > 1`)')

            adj_for_adv.extend(adv_pat_bigrams.adj.drop_duplicates().to_list())

            bigram_samples[adv][pat] = adv_pat_bigrams

            adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
                [adv_top, adv_pat_bigrams])

        bigram_samples[adv]['adj'] = set(adj_for_adv)
        bigrams.extend(adv_top.l2.drop_duplicates().to_list())
        adj.extend(adj_for_adv)
        bigram_samples[adv]['both'] = adv_top
    bigram_samples['bigrams'] = set(bigrams)
    bigram_samples['adj'] = set(adj)
    return bigram_samples


samples_dict = show_adv_bigrams(
    K, C, bigram_dfs,
    column_list=[
        'adj',
        *pd.Series(main_cols_ordered).str.replace(
            r'mean_|_SET|_MIR', '', regex=True)
        .drop_duplicates().to_list(),
        't', 'MI'
    ]
)
```

    # Top bigrams corresponding to top adverbs
    
    2024-05-16
    
    ## _exactly_
    
    
    ### Top 9 `NEGmirror` "exactly_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key              | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
    |:-----------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
    | NEG~exactly_sure | sure  |  2.09 |  0.85 | 560.65 | 148 | 293,963 |  149 | 10.39 | 0.84 |
    
    
    ### Top 9 `RBdirect` "exactly_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                    | adj        |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
    |:-----------------------|:-----------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
    | NEG~exactly_sure       | sure       |  8.63 |  0.92 | 54,750.58 | 8,860 | 3,226,213 | 9,301 | 90.43 | 1.41 |
    | NEG~exactly_new        | new        |  8.54 |  0.93 |  8,697.93 | 1,378 | 3,226,213 | 1,418 | 35.69 | 1.42 |
    | NEG~exactly_easy       | easy       |  8.37 |  0.93 |  6,747.64 | 1,069 | 3,226,213 | 1,100 | 31.44 | 1.42 |
    | NEG~exactly_clear      | clear      |  8.30 |  0.92 | 10,937.16 | 1,759 | 3,226,213 | 1,835 | 40.31 | 1.41 |
    | NEG~exactly_cheap      | cheap      |  8.28 |  0.95 |  4,443.27 |   693 | 3,226,213 |   704 | 25.33 | 1.42 |
    | NEG~exactly_surprising | surprising |  7.34 |  0.96 |  2,863.35 |   441 | 3,226,213 |   444 | 20.21 | 1.42 |
    | NEG~exactly_happy      | happy      |  7.16 |  0.90 |  2,694.69 |   441 | 3,226,213 |   468 | 20.17 | 1.40 |
    | NEG~exactly_ideal      | ideal      |  7.08 |  0.90 |  2,546.29 |   418 | 3,226,213 |   445 | 19.63 | 1.40 |
    | NEG~exactly_subtle     | subtle     |  6.92 |  0.94 |  1,671.02 |   264 | 3,226,213 |   271 | 15.62 | 1.42 |
    
    
    ## _necessarily_
    
    
    ### Top 9 `NEGmirror` "necessarily_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                   | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
    |:----------------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
    | NEG~necessarily_wrong | wrong |  4.19 |  0.77 | 693.55 | 213 | 293,963 |  233 | 12.29 | 0.80 |
    
    
    ### Top 9 `RBdirect` "necessarily_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                            | adj            |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
    |:-------------------------------|:---------------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
    | NEG~necessarily_indicative     | indicative     |  8.37 |  0.93 |  8,811.69 | 1,406 | 3,226,213 | 1,456 | 36.05 | 1.41 |
    | NEG~necessarily_representative | representative |  7.31 |  0.91 |  3,044.27 |   496 | 3,226,213 |   524 | 21.39 | 1.40 |
    | NEG~necessarily_easy           | easy           |  7.26 |  0.88 |  5,448.34 |   914 | 3,226,213 |   996 | 29.00 | 1.39 |
    | NEG~necessarily_surprising     | surprising     |  7.22 |  0.93 |  2,150.86 |   343 | 3,226,213 |   355 | 17.80 | 1.41 |
    | NEG~necessarily_true           | true           |  6.89 |  0.82 | 18,199.76 | 3,238 | 3,226,213 | 3,786 | 54.42 | 1.36 |
    | NEG~necessarily_interested     | interested     |  6.77 |  0.87 |  2,500.26 |   422 | 3,226,213 |   463 | 19.70 | 1.39 |
    | NEG~necessarily_related        | related        |  6.74 |  0.84 |  4,271.76 |   742 | 3,226,213 |   842 | 26.08 | 1.37 |
    | NEG~necessarily_illegal        | illegal        |  6.48 |  0.87 |  1,659.90 |   280 | 3,226,213 |   307 | 16.05 | 1.39 |
    | NEG~necessarily_new            | new            |  6.36 |  0.82 |  2,728.73 |   483 | 3,226,213 |   561 | 21.02 | 1.36 |
    
    
    ## _before_
    
    
    ### Top 9 `NEGmirror` "before_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                  | adj       |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
    |:---------------------|:----------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
    | NEG~before_available | available |  3.99 |  0.84 | 654.92 | 177 | 293,963 |  180 | 11.35 | 0.83 |
    
    No bigrams found in loaded `RBdirect` AM table.
    
    ## _that_
    
    
    ### Top 9 `NEGmirror` "that_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                | adj       |   LRC |   dP1 |       G2 |   f |      f1 |   f2 |     t |   MI |
    |:-------------------|:----------|------:|------:|---------:|----:|--------:|-----:|------:|-----:|
    | NEG~that_simple    | simple    |  4.48 |  0.74 | 1,483.32 | 478 | 293,963 |  540 | 18.29 | 0.79 |
    | NEG~that_easy      | easy      |  3.91 |  0.68 | 1,278.04 | 458 | 293,963 |  558 | 17.63 | 0.75 |
    | NEG~that_big       | big       |  2.99 |  0.66 |   308.12 | 113 | 293,963 |  140 |  8.72 | 0.75 |
    | NEG~that_good      | good      |  2.65 |  0.47 |   848.28 | 449 | 293,963 |  732 | 16.19 | 0.63 |
    | NEG~that_great     | great     |  1.93 |  0.36 |   406.36 | 288 | 293,963 |  575 | 12.07 | 0.54 |
    | NEG~that_important | important |  1.47 |  0.34 |   153.47 | 115 | 293,963 |  238 |  7.51 | 0.52 |
    | NEG~that_bad       | bad       |  1.14 |  0.23 |   175.40 | 206 | 293,963 |  552 |  8.79 | 0.41 |
    
    
    ### Top 9 `RBdirect` "that_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                  | adj         |   LRC |   dP1 |        G2 |     f |        f1 |     f2 |     t |   MI |
    |:---------------------|:------------|------:|------:|----------:|------:|----------:|-------:|------:|-----:|
    | NEG~that_uncommon    | uncommon    |  8.39 |  0.94 |  5,136.91 |   804 | 3,226,213 |    819 | 27.28 | 1.42 |
    | NEG~that_surprising  | surprising  |  8.14 |  0.92 |  7,115.30 | 1,141 | 3,226,213 |  1,187 | 32.47 | 1.41 |
    | NEG~that_common      | common      |  8.12 |  0.92 |  7,564.08 | 1,216 | 3,226,213 |  1,268 | 33.51 | 1.41 |
    | NEG~that_hard        | hard        |  7.96 |  0.88 | 59,642.82 | 9,966 | 3,226,213 | 10,818 | 95.78 | 1.39 |
    | NEG~that_complicated | complicated |  7.95 |  0.91 |  7,450.89 | 1,208 | 3,226,213 |  1,270 | 33.39 | 1.41 |
    | NEG~that_unusual     | unusual     |  7.94 |  0.92 |  6,096.13 |   983 | 3,226,213 |  1,028 | 30.13 | 1.41 |
    | NEG~that_impressed   | impressed   |  7.57 |  0.91 |  4,207.58 |   684 | 3,226,213 |    721 | 25.12 | 1.40 |
    | NEG~that_exciting    | exciting    |  7.48 |  0.90 |  4,892.83 |   805 | 3,226,213 |    859 | 27.24 | 1.40 |
    | NEG~that_expensive   | expensive   |  7.32 |  0.87 | 10,585.14 | 1,800 | 3,226,213 |  1,992 | 40.67 | 1.38 |
    
    
    ## _remotely_
    
    
    ### Top 9 `NEGmirror` "remotely_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
    |:-------------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
    | NEG~remotely_close | close |  3.02 |  0.59 | 524.61 | 219 | 293,963 |  299 | 11.88 | 0.70 |
    
    
    ### Top 9 `RBdirect` "remotely_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                     | adj        |   LRC |   dP1 |       G2 |   f |        f1 |    f2 |     t |   MI |
    |:------------------------|:-----------|------:|------:|---------:|----:|----------:|------:|------:|-----:|
    | NEG~remotely_true       | true       |  4.46 |  0.56 | 1,089.49 | 250 | 3,226,213 |   420 | 14.82 | 1.20 |
    | NEG~remotely_close      | close      |  2.92 |  0.23 | 1,722.76 | 696 | 3,226,213 | 2,558 | 22.76 | 0.86 |
    | NEG~remotely_interested | interested |  2.72 |  0.23 |   808.74 | 333 | 3,226,213 | 1,252 | 15.68 | 0.85 |
    
    
    ## _yet_
    
    No bigrams found in loaded `NEGmirror` AM table.
    
    ### Top 9 `RBdirect` "yet_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key               | adj       |   LRC |   dP1 |        G2 |      f |        f1 |     f2 |     t |   MI |
    |:------------------|:----------|------:|------:|----------:|-------:|----------:|-------:|------:|-----:|
    | NEG~yet_clear     | clear     | 10.26 |  0.95 | 67,924.56 | 10,553 | 3,226,213 | 10,693 | 98.84 | 1.42 |
    | NEG~yet_ready     | ready     |  9.23 |  0.93 | 48,012.06 |  7,611 | 3,226,213 |  7,838 | 83.88 | 1.41 |
    | NEG~yet_complete  | complete  |  8.42 |  0.92 | 13,815.99 |  2,220 | 3,226,213 |  2,314 | 45.28 | 1.41 |
    | NEG~yet_sure      | sure      |  8.37 |  0.92 | 12,379.79 |  1,990 | 3,226,213 |  2,075 | 42.87 | 1.41 |
    | NEG~yet_certain   | certain   |  8.12 |  0.93 |  5,491.41 |    874 | 3,226,213 |    903 | 28.42 | 1.41 |
    | NEG~yet_eligible  | eligible  |  7.72 |  0.94 |  2,929.15 |    459 | 3,226,213 |    468 | 20.61 | 1.42 |
    | NEG~yet_available | available |  7.69 |  0.87 | 44,196.15 |  7,481 | 3,226,213 |  8,238 | 82.93 | 1.39 |
    | NEG~yet_final     | final     |  7.45 |  0.91 |  4,028.75 |    659 | 3,226,213 |    699 | 24.65 | 1.40 |
    | NEG~yet_public    | public    |  7.36 |  0.91 |  3,055.97 |    496 | 3,226,213 |    522 | 21.40 | 1.41 |
    
    
    ## _ever_
    
    
    ### Top 9 `NEGmirror` "ever_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key              | adj     |   LRC |   dP1 |       G2 |   f |      f1 |   f2 |     t |   MI |
    |:-----------------|:--------|------:|------:|---------:|----:|--------:|-----:|------:|-----:|
    | NEG~ever_good    | good    |  5.05 |  0.84 | 1,103.09 | 300 | 293,963 |  306 | 14.76 | 0.83 |
    | NEG~ever_easy    | easy    |  4.66 |  0.85 | 1,399.10 | 368 | 293,963 |  370 | 16.39 | 0.84 |
    | NEG~ever_able    | able    |  3.73 |  0.77 |   441.74 | 136 | 293,963 |  149 |  9.81 | 0.80 |
    | NEG~ever_wrong   | wrong   |  3.34 |  0.82 |   361.62 | 102 | 293,963 |  106 |  8.58 | 0.82 |
    | NEG~ever_perfect | perfect |  2.58 |  0.85 |   788.18 | 207 | 293,963 |  208 | 12.30 | 0.84 |
    | NEG~ever_likely  | likely  |  2.00 |  0.46 |   192.81 | 103 | 293,963 |  169 |  7.74 | 0.62 |
    
    
    ### Top 9 `RBdirect` "ever_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key              | adj     |   LRC |   dP1 |        G2 |      f |         f1 |     f2 |     t |   MI |
    |:-----------------|:--------|------:|------:|----------:|-------:|-----------:|-------:|------:|-----:|
    | NEG~that_clever  | clever  |  5.60 |  0.78 |  1,151.90 |    212 |  3,226,213 |    259 | 13.90 | 1.34 |
    | NEG~ever_simple  | simple  |  5.54 |  0.77 |  1,142.04 |    212 |  3,226,213 |    262 | 13.89 | 1.34 |
    | NEG~ever_easy    | easy    |  5.06 |  0.63 |  2,030.58 |    430 |  3,226,213 |    641 | 19.58 | 1.25 |
    | NEG~as_severe    | severe  |  4.81 |  0.52 | 11,262.06 |  2,692 |  3,226,213 |  4,809 | 48.42 | 1.18 |
    | NEG~ever_good    | good    |  3.76 |  0.40 |  1,178.00 |    332 |  3,226,213 |    756 | 16.67 | 1.07 |
    | NEG~ever_perfect | perfect |  3.48 |  0.37 |    736.05 |    217 |  3,226,213 |    527 | 13.39 | 1.04 |
    | COM~most_severe  | severe  |  3.08 |  0.04 |  1,035.10 | 16,416 | 83,102,035 | 16,442 |  4.60 | 0.02 |
    | NEG~as_clever    | clever  |  3.08 |  0.26 |  1,566.06 |    585 |  3,226,213 |  1,952 | 21.17 | 0.90 |
    | COM~never_easy   | easy    |  3.03 |  0.04 |    813.36 | 12,127 | 83,102,035 | 12,139 |  4.01 | 0.02 |
    
    
    ## _immediately_
    
    
    ### Top 9 `NEGmirror` "immediately_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                       | adj       |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |    t |   MI |
    |:--------------------------|:----------|------:|------:|-------:|----:|--------:|-----:|-----:|-----:|
    | NEG~immediately_available | available |  1.91 |  0.39 | 258.42 | 164 | 293,963 |  304 | 9.37 | 0.57 |
    


    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(
    /tmp/ipykernel_2162477/63082195.py:34: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated. In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes. To retain the old behavior, exclude the relevant entries before the concat operation.
      adv_top = adv_pat_bigrams if adv_top is None else pd.concat(


    
    ### Top 9 `RBdirect` "immediately_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                        | adj        |   LRC |   dP1 |         G2 |      f |        f1 |     f2 |      t |   MI |
    |:---------------------------|:-----------|------:|------:|-----------:|-------:|----------:|-------:|-------:|-----:|
    | NEG~immediately_clear      | clear      |  8.32 |  0.90 | 153,302.22 | 25,276 | 3,226,213 | 27,066 | 152.62 | 1.40 |
    | NEG~immediately_possible   | possible   |  7.68 |  0.90 |   6,269.26 |  1,027 | 3,226,213 |  1,091 |  30.77 | 1.40 |
    | NEG~immediately_available  | available  |  5.77 |  0.66 | 102,962.94 | 21,297 | 3,226,213 | 30,725 | 138.07 | 1.27 |
    | NEG~immediately_able       | able       |  4.87 |  0.58 |   2,851.84 |    639 | 3,226,213 |  1,036 |  23.75 | 1.22 |
    | NEG~immediately_obvious    | obvious    |  4.59 |  0.49 |   9,043.23 |  2,258 | 3,226,213 |  4,305 |  44.13 | 1.15 |
    | NEG~immediately_apparent   | apparent   |  3.80 |  0.35 |   6,581.69 |  2,031 | 3,226,213 |  5,260 |  40.70 | 1.01 |
    | NEG~immediately_successful | successful |  3.47 |  0.36 |     958.19 |    292 | 3,226,213 |    743 |  15.46 | 1.02 |
    | NEG~immediately_visible    | visible    |  3.35 |  0.32 |   1,324.08 |    436 | 3,226,213 |  1,234 |  18.67 | 0.98 |
    | NEG~immediately_evident    | evident    |  2.96 |  0.25 |   1,122.08 |    428 | 3,226,213 |  1,466 |  18.04 | 0.89 |
    
    
    ## _any_
    
    
    ### Top 9 `NEGmirror` "any_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key            | adj    |   LRC |   dP1 |     G2 |     f |        f1 |    f2 |     t |   MI |
    |:---------------|:-------|------:|------:|-------:|------:|----------:|------:|------:|-----:|
    | NEG~any_better | better |  3.42 |  0.61 | 960.25 |   382 |   293,963 |   503 | 15.82 | 0.72 |
    | POS~as_many    | many   |  1.20 |  0.11 | 228.90 | 1,689 | 1,738,105 | 1,752 |  4.63 | 0.05 |
    
    
    ### Top 9 `RBdirect` "any_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key               | adj       |   LRC |   dP1 |        G2 |         f |         f1 |        f2 |     t |   MI |
    |:------------------|:----------|------:|------:|----------:|----------:|-----------:|----------:|------:|-----:|
    | COM~not_many      | many      |  5.25 |  0.04 |  4,286.27 |    58,428 | 83,102,035 |    58,442 |  8.98 | 0.02 |
    | NEG~any_happier   | happier   |  4.65 |  0.53 |  3,488.76 |       830 |  3,226,213 |     1,472 | 26.90 | 1.18 |
    | COM~so_many       | many      |  4.27 |  0.04 | 74,084.75 | 1,189,746 | 83,102,035 | 1,191,874 | 38.92 | 0.02 |
    | NEG~any_clearer   | clearer   |  3.21 |  0.30 |  1,051.22 |       357 |  3,226,213 |     1,053 | 16.81 | 0.96 |
    | NEG~any_simpler   | simpler   |  3.09 |  0.30 |    671.74 |       228 |  3,226,213 |       672 | 13.44 | 0.96 |
    | NEG~any_different | different |  2.98 |  0.24 |  2,270.24 |       910 |  3,226,213 |     3,313 | 26.06 | 0.87 |
    | NEG~any_worse     | worse     |  2.47 |  0.16 |  3,165.88 |     1,693 |  3,226,213 |     8,487 | 33.44 | 0.73 |
    | NEG~any_younger   | younger   |  2.37 |  0.19 |    544.17 |       256 |  3,226,213 |     1,121 | 13.38 | 0.79 |
    | NEG~any_bigger    | bigger    |  2.27 |  0.17 |    688.06 |       357 |  3,226,213 |     1,735 | 15.46 | 0.74 |
    
    
    ## _particularly_
    
    
    ### Top 9 `NEGmirror` "particularly_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                         | adj        |   LRC |   dP1 |       G2 |   f |      f1 |   f2 |     t |   MI |
    |:----------------------------|:-----------|------:|------:|---------:|----:|--------:|-----:|------:|-----:|
    | NEG~particularly_new        | new        |  5.04 |  0.80 | 1,396.47 | 407 | 293,963 |  431 | 17.08 | 0.81 |
    | NEG~particularly_wrong      | wrong      |  4.54 |  0.82 |   753.64 | 212 | 293,963 |  220 | 12.37 | 0.82 |
    | NEG~particularly_surprising | surprising |  4.02 |  0.78 |   555.35 | 168 | 293,963 |  182 | 10.93 | 0.80 |
    | NEG~particularly_unusual    | unusual    |  3.69 |  0.72 |   522.88 | 173 | 293,963 |  199 | 10.96 | 0.78 |
    | NEG~particularly_remarkable | remarkable |  3.50 |  0.81 |   378.25 | 108 | 293,963 |  113 |  8.82 | 0.82 |
    | NEG~particularly_close      | close      |  3.39 |  0.71 |   405.25 | 138 | 293,963 |  162 |  9.75 | 0.77 |
    | NEG~particularly_special    | special    |  3.36 |  0.61 |   820.88 | 327 | 293,963 |  431 | 14.64 | 0.72 |
    | NEG~particularly_good       | good       |  3.18 |  0.57 |   912.45 | 392 | 293,963 |  547 | 15.80 | 0.69 |
    | NEG~particularly_memorable  | memorable  |  2.86 |  0.61 |   331.25 | 132 | 293,963 |  174 |  9.30 | 0.72 |
    
    
    ### Top 9 `RBdirect` "particularly_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                          | adj         |   LRC |   dP1 |       G2 |     f |        f1 |    f2 |     t |   MI |
    |:-----------------------------|:------------|------:|------:|---------:|------:|----------:|------:|------:|-----:|
    | NEG~particularly_surprising  | surprising  |  4.58 |  0.51 | 4,411.15 | 1,076 | 3,226,213 | 1,981 | 30.55 | 1.16 |
    | NEG~particularly_religious   | religious   |  4.54 |  0.53 | 2,059.88 |   488 | 3,226,213 |   860 | 20.64 | 1.18 |
    | NEG~particularly_new         | new         |  4.49 |  0.50 | 3,065.77 |   752 | 3,226,213 | 1,396 | 25.52 | 1.16 |
    | NEG~particularly_original    | original    |  4.44 |  0.53 | 1,526.99 |   363 | 3,226,213 |   643 | 17.79 | 1.18 |
    | NEG~particularly_wrong       | wrong       |  3.89 |  0.45 |   838.81 |   219 | 3,226,213 |   446 | 13.67 | 1.12 |
    | NEG~particularly_friendly    | friendly    |  3.69 |  0.40 |   953.96 |   269 | 3,226,213 |   613 | 15.00 | 1.07 |
    | NEG~particularly_fast        | fast        |  3.55 |  0.39 |   765.43 |   221 | 3,226,213 |   521 | 13.56 | 1.06 |
    | NEG~particularly_unusual     | unusual     |  3.53 |  0.35 | 1,419.90 |   440 | 3,226,213 | 1,146 | 18.93 | 1.01 |
    | NEG~particularly_comfortable | comfortable |  3.51 |  0.36 |   968.42 |   291 | 3,226,213 |   726 | 15.47 | 1.03 |
    
    
    ## _terribly_
    
    
    ### Top 9 `NEGmirror` "terribly_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                | adj   |   LRC |   dP1 |     G2 |     f |        f1 |    f2 |    t |   MI |
    |:-------------------|:------|------:|------:|-------:|------:|----------:|------:|-----:|-----:|
    | POS~terribly_wrong | wrong |  1.09 |  0.10 | 223.10 | 1,878 | 1,738,105 | 1,960 | 4.65 | 0.05 |
    
    
    ### Top 9 `RBdirect` "terribly_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                      | adj         |   LRC |   dP1 |       G2 |   f |        f1 |    f2 |     t |   MI |
    |:-------------------------|:------------|------:|------:|---------:|----:|----------:|------:|------:|-----:|
    | NEG~terribly_surprising  | surprising  |  7.08 |  0.86 | 5,585.09 | 951 | 3,226,213 | 1,054 | 29.56 | 1.38 |
    | NEG~terribly_impressed   | impressed   |  5.36 |  0.72 | 1,434.24 | 280 | 3,226,213 |   371 | 15.90 | 1.31 |
    | NEG~terribly_different   | different   |  5.19 |  0.67 | 1,807.02 | 370 | 3,226,213 |   525 | 18.22 | 1.28 |
    | NEG~terribly_interested  | interested  |  5.18 |  0.65 | 2,373.72 | 496 | 3,226,213 |   725 | 21.05 | 1.26 |
    | NEG~terribly_surprised   | surprised   |  5.17 |  0.68 | 1,430.88 | 289 | 3,226,213 |   402 | 16.12 | 1.28 |
    | NEG~terribly_concerned   | concerned   |  4.49 |  0.53 | 1,756.14 | 416 | 3,226,213 |   733 | 19.05 | 1.18 |
    | NEG~terribly_interesting | interesting |  4.26 |  0.49 | 1,466.12 | 364 | 3,226,213 |   688 | 17.73 | 1.15 |
    | NEG~terribly_useful      | useful      |  4.25 |  0.52 |   946.46 | 226 | 3,226,213 |   403 | 14.03 | 1.18 |
    | NEG~terribly_exciting    | exciting    |  3.92 |  0.42 | 1,402.29 | 382 | 3,226,213 |   828 | 17.96 | 1.09 |
    
    
    ## _inherently_
    
    
    ### Top 9 `NEGmirror` "inherently_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                  | adj   |   LRC |   dP1 |       G2 |     f |      f1 |    f2 |     t |   MI |
    |:---------------------|:------|------:|------:|---------:|------:|--------:|------:|------:|-----:|
    | NEG~inherently_wrong | wrong |  4.06 |  0.65 | 4,044.66 | 1,522 | 293,963 | 1,924 | 31.88 | 0.74 |
    | NEG~inherently_bad   | bad   |  2.68 |  0.56 |   339.00 |   148 | 293,963 |   209 |  9.68 | 0.69 |
    
    
    ### Top 9 `RBdirect` "inherently_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                  | adj   |   LRC |   dP1 |       G2 |     f |        f1 |    f2 |     t |   MI |
    |:---------------------|:------|------:|------:|---------:|------:|----------:|------:|------:|-----:|
    | NEG~inherently_wrong | wrong |  4.98 |  0.57 | 7,241.49 | 1,648 | 3,226,213 | 2,735 | 38.08 | 1.21 |
    | NEG~inherently_bad   | bad   |  3.92 |  0.39 | 2,783.25 |   794 | 3,226,213 | 1,840 | 25.74 | 1.06 |
    | NEG~inherently_evil  | evil  |  2.65 |  0.22 |   838.38 |   360 | 3,226,213 | 1,422 | 16.17 | 0.83 |
    | NEG~inherently_good  | good  |  2.16 |  0.16 |   530.11 |   283 | 3,226,213 | 1,416 | 13.68 | 0.73 |
    
    
    ## _altogether_
    
    
    ### Top 9 `NEGmirror` "altogether_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                      | adj       |   LRC |   dP1 |     G2 |   f |        f1 |   f2 |    t |   MI |
    |:-------------------------|:----------|------:|------:|-------:|----:|----------:|-----:|-----:|-----:|
    | POS~altogether_different | different |  1.47 |  0.14 | 257.01 | 938 | 1,738,105 |  942 | 4.32 | 0.07 |
    
    
    ### Top 9 `RBdirect` "altogether_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                       | adj        |   LRC |   dP1 |       G2 |   f |        f1 |   f2 |     t |   MI |
    |:--------------------------|:-----------|------:|------:|---------:|----:|----------:|-----:|------:|-----:|
    | NEG~altogether_surprising | surprising |  6.72 |  0.86 | 2,849.79 | 487 | 3,226,213 |  542 | 21.15 | 1.38 |
    | NEG~altogether_clear      | clear      |  6.68 |  0.88 | 1,970.06 | 330 | 3,226,213 |  359 | 17.43 | 1.39 |
    
    
    ## _only_
    
    
    ### Top 9 `NEGmirror` "only_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                | adj       |   LRC |   dP1 |     G2 |     f |        f1 |    f2 |    t |   MI |
    |:-------------------|:----------|------:|------:|-------:|------:|----------:|------:|-----:|-----:|
    | POS~only_available | available |  1.64 |  0.13 | 237.39 | 1,030 | 1,738,105 | 1,042 | 4.32 | 0.06 |
    
    
    ### Top 9 `RBdirect` "only_*" bigrams (sorted by `LRC`; `LRC > 1`)
    
    | key                  | adj         |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
    |:---------------------|:------------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
    | NEG~only_delicious   | delicious   |  8.10 |  0.93 |  5,393.78 |   859 | 3,226,213 |   888 | 28.18 | 1.41 |
    | NEG~only_unnecessary | unnecessary |  7.52 |  0.92 |  3,073.46 |   493 | 3,226,213 |   513 | 21.34 | 1.41 |
    | NEG~only_beautiful   | beautiful   |  7.37 |  0.87 | 10,809.43 | 1,833 | 3,226,213 | 2,022 | 41.05 | 1.38 |
    | NEG~only_stylish     | stylish     |  7.28 |  0.95 |  2,175.02 |   340 | 3,226,213 |   346 | 17.74 | 1.42 |
    | NEG~only_unfair      | unfair      |  7.24 |  0.91 |  2,941.64 |   481 | 3,226,213 |   510 | 21.06 | 1.40 |
    | NEG~only_ineffective | ineffective |  7.24 |  0.93 |  2,248.20 |   360 | 3,226,213 |   374 | 18.24 | 1.41 |
    | NEG~only_easy        | easy        |  6.91 |  0.84 |  7,736.69 | 1,349 | 3,226,213 | 1,538 | 35.16 | 1.37 |
    | NEG~only_convenient  | convenient  |  6.48 |  0.86 |  2,083.48 |   358 | 3,226,213 |   401 | 18.13 | 1.38 |
    | NEG~only_tasty       | tasty       |  6.48 |  0.89 |  1,416.38 |   235 | 3,226,213 |   253 | 14.71 | 1.40 |
    


# Top bigrams corresponding to top adverbs

2024-05-15

## _exactly_


### Top 5 `RBdirect` "exactly_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key               | adj   |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
|:------------------|:------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
| NEG~exactly_sure  | sure  |  8.63 |  0.92 | 54,750.58 | 8,860 | 3,226,213 | 9,301 | 90.43 | 1.41 |
| NEG~exactly_new   | new   |  8.54 |  0.93 |  8,697.93 | 1,378 | 3,226,213 | 1,418 | 35.69 | 1.42 |
| NEG~exactly_easy  | easy  |  8.37 |  0.93 |  6,747.64 | 1,069 | 3,226,213 | 1,100 | 31.44 | 1.42 |
| NEG~exactly_clear | clear |  8.30 |  0.92 | 10,937.16 | 1,759 | 3,226,213 | 1,835 | 40.31 | 1.41 |
| NEG~exactly_cheap | cheap |  8.28 |  0.95 |  4,443.27 |   693 | 3,226,213 |   704 | 25.33 | 1.42 |


### Top 5 `NEGmirror` "exactly_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key              | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:-----------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~exactly_sure | sure  |  2.09 |  0.85 | 560.65 | 148 | 293,963 |  149 | 10.39 | 0.84 |


## _necessarily_


### Top 5 `RBdirect` "necessarily_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                            | adj            |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
|:-------------------------------|:---------------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
| NEG~necessarily_indicative     | indicative     |  8.37 |  0.93 |  8,811.69 | 1,406 | 3,226,213 | 1,456 | 36.05 | 1.41 |
| NEG~necessarily_representative | representative |  7.31 |  0.91 |  3,044.27 |   496 | 3,226,213 |   524 | 21.39 | 1.40 |
| NEG~necessarily_easy           | easy           |  7.26 |  0.88 |  5,448.34 |   914 | 3,226,213 |   996 | 29.00 | 1.39 |
| NEG~necessarily_surprising     | surprising     |  7.22 |  0.93 |  2,150.86 |   343 | 3,226,213 |   355 | 17.80 | 1.41 |
| NEG~necessarily_true           | true           |  6.89 |  0.82 | 18,199.76 | 3,238 | 3,226,213 | 3,786 | 54.42 | 1.36 |


### Top 5 `NEGmirror` "necessarily_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                   | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:----------------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~necessarily_wrong | wrong |  4.19 |  0.77 | 693.55 | 213 | 293,963 |  233 | 12.29 | 0.80 |


## _before_

No bigrams found in loaded `RBdirect` AM table.

### Top 5 `NEGmirror` "before_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                  | adj       |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:---------------------|:----------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~before_available | available |  3.99 |  0.84 | 654.92 | 177 | 293,963 |  180 | 11.35 | 0.83 |


## _that_


### Top 5 `RBdirect` "that_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                  | adj         |   LRC |   dP1 |        G2 |     f |        f1 |     f2 |     t |   MI |
|:---------------------|:------------|------:|------:|----------:|------:|----------:|-------:|------:|-----:|
| NEG~that_uncommon    | uncommon    |  8.39 |  0.94 |  5,136.91 |   804 | 3,226,213 |    819 | 27.28 | 1.42 |
| NEG~that_surprising  | surprising  |  8.14 |  0.92 |  7,115.30 | 1,141 | 3,226,213 |  1,187 | 32.47 | 1.41 |
| NEG~that_common      | common      |  8.12 |  0.92 |  7,564.08 | 1,216 | 3,226,213 |  1,268 | 33.51 | 1.41 |
| NEG~that_hard        | hard        |  7.96 |  0.88 | 59,642.82 | 9,966 | 3,226,213 | 10,818 | 95.78 | 1.39 |
| NEG~that_complicated | complicated |  7.95 |  0.91 |  7,450.89 | 1,208 | 3,226,213 |  1,270 | 33.39 | 1.41 |


### Top 5 `NEGmirror` "that_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key             | adj    |   LRC |   dP1 |       G2 |   f |      f1 |   f2 |     t |   MI |
|:----------------|:-------|------:|------:|---------:|----:|--------:|-----:|------:|-----:|
| NEG~that_simple | simple |  4.48 |  0.74 | 1,483.32 | 478 | 293,963 |  540 | 18.29 | 0.79 |
| NEG~that_easy   | easy   |  3.91 |  0.68 | 1,278.04 | 458 | 293,963 |  558 | 17.63 | 0.75 |
| NEG~that_big    | big    |  2.99 |  0.66 |   308.12 | 113 | 293,963 |  140 |  8.72 | 0.75 |
| NEG~that_good   | good   |  2.65 |  0.47 |   848.28 | 449 | 293,963 |  732 | 16.19 | 0.63 |
| NEG~that_great  | great  |  1.93 |  0.36 |   406.36 | 288 | 293,963 |  575 | 12.07 | 0.54 |


## _remotely_


### Top 5 `RBdirect` "remotely_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                     | adj        |   LRC |   dP1 |       G2 |   f |        f1 |    f2 |     t |   MI |
|:------------------------|:-----------|------:|------:|---------:|----:|----------:|------:|------:|-----:|
| NEG~remotely_true       | true       |  4.46 |  0.56 | 1,089.49 | 250 | 3,226,213 |   420 | 14.82 | 1.20 |
| NEG~remotely_close      | close      |  2.92 |  0.23 | 1,722.76 | 696 | 3,226,213 | 2,558 | 22.76 | 0.86 |
| NEG~remotely_interested | interested |  2.72 |  0.23 |   808.74 | 333 | 3,226,213 | 1,252 | 15.68 | 0.85 |


### Top 5 `NEGmirror` "remotely_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:-------------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~remotely_close | close |  3.02 |  0.59 | 524.61 | 219 | 293,963 |  299 | 11.88 | 0.70 |


```python
pprint({key: adv_dict['adj'] for key, adv_dict in samples_dict.items() if key not in {'bigrams', 'adj'}})
```

    {'altogether': {'surprising', 'different', 'clear'},
     'any': {'better',
             'bigger',
             'clearer',
             'different',
             'happier',
             'many',
             'simpler',
             'worse',
             'younger'},
     'before': {'available'},
     'ever': {'able',
              'clever',
              'easy',
              'good',
              'likely',
              'perfect',
              'severe',
              'simple',
              'wrong'},
     'exactly': {'cheap',
                 'clear',
                 'easy',
                 'happy',
                 'ideal',
                 'new',
                 'subtle',
                 'sure',
                 'surprising'},
     'immediately': {'able',
                     'apparent',
                     'available',
                     'clear',
                     'evident',
                     'obvious',
                     'possible',
                     'successful',
                     'visible'},
     'inherently': {'evil', 'good', 'bad', 'wrong'},
     'necessarily': {'easy',
                     'illegal',
                     'indicative',
                     'interested',
                     'new',
                     'related',
                     'representative',
                     'surprising',
                     'true',
                     'wrong'},
     'only': {'available',
              'beautiful',
              'convenient',
              'delicious',
              'easy',
              'ineffective',
              'stylish',
              'tasty',
              'unfair',
              'unnecessary'},
     'particularly': {'close',
                      'comfortable',
                      'fast',
                      'friendly',
                      'good',
                      'memorable',
                      'new',
                      'original',
                      'religious',
                      'remarkable',
                      'special',
                      'surprising',
                      'unusual',
                      'wrong'},
     'remotely': {'true', 'interested', 'close'},
     'terribly': {'concerned',
                  'different',
                  'exciting',
                  'impressed',
                  'interested',
                  'interesting',
                  'surprised',
                  'surprising',
                  'useful',
                  'wrong'},
     'that': {'bad',
              'big',
              'common',
              'complicated',
              'easy',
              'exciting',
              'expensive',
              'good',
              'great',
              'hard',
              'important',
              'impressed',
              'simple',
              'surprising',
              'uncommon',
              'unusual'},
     'yet': {'available',
             'certain',
             'clear',
             'complete',
             'eligible',
             'final',
             'public',
             'ready',
             'sure'}}



```python
for key, info in samples_dict.items():
    if key in ('bigrams', 'adj'):
        key = f'ALL {key.replace("adj", "adjectives")}'
    formatted_iter = [
        f'_{a.replace("_", " ")}_' for a
        in (info['adj'] if isinstance(info, dict)
            else info)]
    print_iter(formatted_iter,
               header=f'+ _{key}_ ({len(formatted_iter)} unique)',
               bullet='+', indent=2)
```

    
    + _exactly_ (9 unique)
      + _surprising_
      + _sure_
      + _subtle_
      + _clear_
      + _new_
      + _cheap_
      + _happy_
      + _easy_
      + _ideal_
    
    + _necessarily_ (10 unique)
      + _representative_
      + _surprising_
      + _related_
      + _new_
      + _wrong_
      + _true_
      + _indicative_
      + _easy_
      + _interested_
      + _illegal_
    
    + _before_ (1 unique)
      + _available_
    
    + _that_ (16 unique)
      + _good_
      + _surprising_
      + _important_
      + _impressed_
      + _simple_
      + _uncommon_
      + _complicated_
      + _common_
      + _unusual_
      + _exciting_
      + _expensive_
      + _bad_
      + _easy_
      + _hard_
      + _big_
      + _great_
    
    + _remotely_ (3 unique)
      + _true_
      + _interested_
      + _close_
    
    + _yet_ (9 unique)
      + _sure_
      + _available_
      + _clear_
      + _public_
      + _complete_
      + _eligible_
      + _ready_
      + _certain_
      + _final_
    
    + _ever_ (9 unique)
      + _good_
      + _severe_
      + _clever_
      + _simple_
      + _wrong_
      + _perfect_
      + _likely_
      + _easy_
      + _able_
    
    + _immediately_ (9 unique)
      + _obvious_
      + _successful_
      + _available_
      + _possible_
      + _apparent_
      + _clear_
      + _visible_
      + _evident_
      + _able_
    
    + _any_ (9 unique)
      + _different_
      + _clearer_
      + _simpler_
      + _bigger_
      + _younger_
      + _better_
      + _happier_
      + _worse_
      + _many_
    
    + _particularly_ (14 unique)
      + _surprising_
      + _good_
      + _remarkable_
      + _fast_
      + _original_
      + _special_
      + _friendly_
      + _unusual_
      + _new_
      + _wrong_
      + _memorable_
      + _religious_
      + _comfortable_
      + _close_
    
    + _terribly_ (10 unique)
      + _surprising_
      + _different_
      + _impressed_
      + _surprised_
      + _concerned_
      + _useful_
      + _wrong_
      + _exciting_
      + _interesting_
      + _interested_
    
    + _inherently_ (4 unique)
      + _evil_
      + _good_
      + _bad_
      + _wrong_
    
    + _altogether_ (3 unique)
      + _surprising_
      + _different_
      + _clear_
    
    + _only_ (10 unique)
      + _available_
      + _ineffective_
      + _tasty_
      + _stylish_
      + _unnecessary_
      + _convenient_
      + _easy_
      + _beautiful_
      + _delicious_
      + _unfair_
    
    + _ALL bigrams_ (121 unique)
      + _that surprising_
      + _terribly different_
      + _immediately obvious_
      + _exactly ideal_
      + _only available_
      + _particularly religious_
      + _not many_
      + _ever able_
      + _ever simple_
      + _necessarily illegal_
      + _particularly memorable_
      + _yet final_
      + _yet certain_
      + _terribly useful_
      + _necessarily surprising_
      + _any simpler_
      + _yet available_
      + _that complicated_
      + _necessarily indicative_
      + _exactly new_
      + _that big_
      + _terribly wrong_
      + _that simple_
      + _exactly easy_
      + _immediately visible_
      + _particularly wrong_
      + _that expensive_
      + _only delicious_
      + _only unfair_
      + _exactly cheap_
      + _that common_
      + _inherently wrong_
      + _particularly special_
      + _ever good_
      + _only unnecessary_
      + _exactly surprising_
      + _any happier_
      + _only easy_
      + _that uncommon_
      + _necessarily wrong_
      + _immediately successful_
      + _particularly surprising_
      + _terribly exciting_
      + _terribly surprising_
      + _as severe_
      + _ever perfect_
      + _before available_
      + _as clever_
      + _inherently bad_
      + _that important_
      + _only stylish_
      + _that exciting_
      + _only ineffective_
      + _remotely close_
      + _terribly impressed_
      + _terribly interesting_
      + _immediately apparent_
      + _any worse_
      + _immediately evident_
      + _only convenient_
      + _that unusual_
      + _yet sure_
      + _necessarily related_
      + _yet eligible_
      + _as many_
      + _yet complete_
      + _terribly concerned_
      + _particularly comfortable_
      + _necessarily representative_
      + _yet ready_
      + _particularly fast_
      + _remotely true_
      + _particularly new_
      + _that hard_
      + _so many_
      + _altogether clear_
      + _necessarily interested_
      + _any better_
      + _exactly sure_
      + _inherently good_
      + _necessarily new_
      + _exactly clear_
      + _ever wrong_
      + _that impressed_
      + _particularly close_
      + _inherently evil_
      + _any younger_
      + _any different_
      + _that great_
      + _immediately possible_
      + _exactly happy_
      + _that easy_
      + _particularly remarkable_
      + _immediately clear_
      + _any clearer_
      + _ever easy_
      + _yet public_
      + _particularly friendly_
      + _necessarily easy_
      + _only beautiful_
      + _altogether different_
      + _immediately able_
      + _never easy_
      + _immediately available_
      + _that good_
      + _most severe_
      + _particularly good_
      + _ever likely_
      + _remotely interested_
      + _that clever_
      + _any bigger_
      + _necessarily true_
      + _particularly unusual_
      + _altogether surprising_
      + _terribly surprised_
      + _particularly original_
      + _terribly interested_
      + _only tasty_
      + _yet clear_
      + _exactly subtle_
      + _that bad_
    
    + _ALL adjectives_ (79 unique)
      + _fast_
      + _stylish_
      + _unnecessary_
      + _convenient_
      + _important_
      + _final_
      + _different_
      + _evil_
      + _original_
      + _visible_
      + _eligible_
      + _surprising_
      + _bigger_
      + _available_
      + _remarkable_
      + _simple_
      + _bad_
      + _evident_
      + _able_
      + _representative_
      + _clearer_
      + _successful_
      + _impressed_
      + _ineffective_
      + _friendly_
      + _true_
      + _exciting_
      + _sure_
      + _related_
      + _unusual_
      + _perfect_
      + _likely_
      + _apparent_
      + _subtle_
      + _public_
      + _happier_
      + _illegal_
      + _close_
      + _certain_
      + _simpler_
      + _tasty_
      + _special_
      + _new_
      + _younger_
      + _cheap_
      + _indicative_
      + _better_
      + _comfortable_
      + _big_
      + _surprised_
      + _clever_
      + _clear_
      + _complicated_
      + _common_
      + _happy_
      + _worse_
      + _easy_
      + _ready_
      + _ideal_
      + _good_
      + _concerned_
      + _uncommon_
      + _memorable_
      + _beautiful_
      + _hard_
      + _unfair_
      + _obvious_
      + _possible_
      + _expensive_
      + _complete_
      + _many_
      + _wrong_
      + _interesting_
      + _interested_
      + _delicious_
      + _great_
      + _severe_
      + _useful_
      + _religious_



+ _exactly_ (5 unique)
  + _clear_
  + _sure_
  + _new_
  + _easy_
  + _cheap_

+ _necessarily_ (6 unique)
  + _surprising_
  + _true_
  + _representative_
  + _indicative_
  + _easy_
  + _wrong_

+ _before_ (1 unique)
  + _available_

+ _that_ (10 unique)
  + _complicated_
  + _surprising_
  + _easy_
  + _simple_
  + _common_
  + _uncommon_
  + _big_
  + _good_
  + _great_
  + _hard_

+ _remotely_ (3 unique)
  + _close_
  + _interested_
  + _true_

+ _ALL bigrams_ (25 unique)
  + _remotely true_
  + _necessarily indicative_
  + _that hard_
  + _necessarily easy_
  + _exactly easy_
  + _exactly clear_
  + _that big_
  + _that great_
  + _necessarily representative_
  + _exactly cheap_
  + _that surprising_
  + _necessarily surprising_
  + _exactly sure_
  + _that easy_
  + _that common_
  + _that simple_
  + _that complicated_
  + _before available_
  + _necessarily true_
  + _exactly new_
  + _that uncommon_
  + _necessarily wrong_
  + _remotely close_
  + _remotely interested_
  + _that good_

+ _ALL adjectives_ (21 unique)
  + _sure_
  + _new_
  + _indicative_
  + _simple_
  + _common_
  + _interested_
  + _available_
  + _true_
  + _cheap_
  + _close_
  + _complicated_
  + _representative_
  + _easy_
  + _wrong_
  + _clear_
  + _surprising_
  + _uncommon_
  + _big_
  + _good_
  + _great_
  + _hard_



```python
all_top_adv_dfs = [ad['both']
                   for ad in samples_dict.values() if isinstance(ad, dict)]
NEG_bigrams_sample = pd.concat(
    all_top_adv_dfs).sort_values('LRC', ascending=False)
top_NEGbigram_df_path = TOP_AM_DIR.joinpath(
    f'Top{K}_NEG-ADV_top-bigrams.{timestamp_today()}.csv')
print(top_NEGbigram_df_path)
NEG_bigrams_sample.to_csv(
    top_NEGbigram_df_path)
NEG_bigrams_sample
```

    /share/compling/projects/sanpi/results/top_AM/Top9_NEG-ADV_top-bigrams.2024-05-16.csv





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
      <th>...</th>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <th>POS~altogether_different</th>
      <td>938</td>
      <td>805.72</td>
      <td>132.28</td>
      <td>0.14</td>
      <td>1.47</td>
      <td>257.01</td>
      <td>4.32</td>
      <td>0.07</td>
      <td>...</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>942</td>
      <td>POSMIR</td>
      <td>altogether_diffe...</td>
      <td>altogether</td>
      <td>different</td>
      <td>40,266.00</td>
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
      <td>...</td>
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
      <th>POS~as_many</th>
      <td>1689</td>
      <td>1,498.54</td>
      <td>190.46</td>
      <td>0.11</td>
      <td>1.20</td>
      <td>228.90</td>
      <td>4.63</td>
      <td>0.05</td>
      <td>...</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>1752</td>
      <td>POSMIR</td>
      <td>as_many</td>
      <td>as</td>
      <td>many</td>
      <td>4,087.00</td>
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
      <td>...</td>
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
      <td>...</td>
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
<p>133 rows × 17 columns</p>
</div>




```python
NEG_bigrams_sample.l1.value_counts()
```




    l1
    NEGATED       95
    NEGMIR        30
    COMPLEMENT     4
    POSMIR         4
    Name: count, dtype: Int64


