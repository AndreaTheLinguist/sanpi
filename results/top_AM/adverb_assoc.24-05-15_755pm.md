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
K = 5
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
      <th>COM~possibly</th>
      <td>39940</td>
      <td>38,567.56</td>
      <td>1,372.44</td>
      <td>0.03</td>
      <td>2.96</td>
      <td>2,169.84</td>
      <td>...</td>
      <td>1.09</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>40066</td>
      <td>COMPLEMENT</td>
      <td>possibly</td>
    </tr>
    <tr>
      <th>COM~refreshingly</th>
      <td>12646</td>
      <td>12,195.19</td>
      <td>450.81</td>
      <td>0.04</td>
      <td>2.88</td>
      <td>778.99</td>
      <td>...</td>
      <td>1.32</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>12669</td>
      <td>COMPLEMENT</td>
      <td>refreshingly</td>
    </tr>
    <tr>
      <th>COM~fiercely</th>
      <td>22206</td>
      <td>21,445.78</td>
      <td>760.22</td>
      <td>0.03</td>
      <td>2.70</td>
      <td>1,191.78</td>
      <td>...</td>
      <td>1.07</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>22279</td>
      <td>COMPLEMENT</td>
      <td>fiercely</td>
    </tr>
    <tr>
      <th>COM~alternately</th>
      <td>4148</td>
      <td>3,994.79</td>
      <td>153.21</td>
      <td>0.04</td>
      <td>1.11</td>
      <td>294.82</td>
      <td>...</td>
      <td>1.81</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>4150</td>
      <td>COMPLEMENT</td>
      <td>alternately</td>
    </tr>
    <tr>
      <th>COM~massively</th>
      <td>18866</td>
      <td>18,569.53</td>
      <td>296.47</td>
      <td>0.02</td>
      <td>0.42</td>
      <td>147.86</td>
      <td>...</td>
      <td>0.24</td>
      <td>86330752</td>
      <td>83102035</td>
      <td>19291</td>
      <td>COMPLEMENT</td>
      <td>massively</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 14 columns</p>
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
      <th>POS~socially</th>
      <td>1419</td>
      <td>1,300.10</td>
      <td>118.90</td>
      <td>0.08</td>
      <td>0.50</td>
      <td>91.24</td>
      <td>...</td>
      <td>0.37</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>1520</td>
      <td>POSMIR</td>
      <td>socially</td>
    </tr>
    <tr>
      <th>POS~deliberately</th>
      <td>613</td>
      <td>548.27</td>
      <td>64.73</td>
      <td>0.10</td>
      <td>0.49</td>
      <td>69.78</td>
      <td>...</td>
      <td>0.56</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>641</td>
      <td>POSMIR</td>
      <td>deliberately</td>
    </tr>
    <tr>
      <th>NEG~currently</th>
      <td>255</td>
      <td>212.36</td>
      <td>42.64</td>
      <td>0.03</td>
      <td>0.00</td>
      <td>9.51</td>
      <td>...</td>
      <td>0.10</td>
      <td>2032082</td>
      <td>293963</td>
      <td>1468</td>
      <td>NEGMIR</td>
      <td>currently</td>
    </tr>
    <tr>
      <th>POS~criminally</th>
      <td>230</td>
      <td>219.82</td>
      <td>10.18</td>
      <td>0.04</td>
      <td>0.00</td>
      <td>3.55</td>
      <td>...</td>
      <td>0.15</td>
      <td>2032082</td>
      <td>1738105</td>
      <td>257</td>
      <td>POSMIR</td>
      <td>criminally</td>
    </tr>
    <tr>
      <th>NEG~very</th>
      <td>8956</td>
      <td>29,065.72</td>
      <td>-20,109.72</td>
      <td>-0.11</td>
      <td>-1.78</td>
      <td>-23,147.86</td>
      <td>...</td>
      <td>-0.60</td>
      <td>2032082</td>
      <td>293963</td>
      <td>200923</td>
      <td>NEGMIR</td>
      <td>very</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 14 columns</p>
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
def load_setdiff_backup(lower_floor: int = 100):
    backup_set_df = pd.read_pickle(tuple(adv_am_paths['RBdirect'].parent.glob(
        f'*35f-7c_min{lower_floor}x*{PKL_SUFF}'))[0])

    neg_set_backup = backup_set_df.filter(like='NEG', axis=0).filter(
        items=FOCUS).reset_index().set_index('l2')
    neg_set_backup.columns = pd.Series(
        adjust_assoc_columns(neg_set_backup.columns)) + '_SET'
    # print(neg_set_backup.head())
    return neg_set_backup
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
    if any(both.f_SET.isna()):
        neg_set_backup = load_setdiff_backup()
        undefined = both.index[both.f_SET.isna()].to_list()
        both.loc[undefined,
                 neg_set_backup.columns] = neg_set_backup.loc[undefined, :]
        print_md_table(both.loc[undefined, :].select_dtypes(include='number').round(2), transpose=True, n_dec=2,
                       title=f'Retrieved values for Adverbs missing from loaded `set_diff` data (i.e. negated SET_DIFF tokens < {SET_FLOOR:,})')

    for metric in both.select_dtypes(include='number').columns.to_series().str.replace(r'_(MIR|SET)$', '', regex=True).unique():

        both[f'mean_{snake_to_camel(metric)}'] = both.filter(
            regex=f"^{metric}").agg('mean', axis='columns')

    return both
```

## Compile top NEG~adverb associations across both approximation methods

```python
C = combine_top(setdiff_adv.copy(), 'SET',
                mirror_adv.copy(), 'MIR', k=K)
```

    SET: union of top 5 adverbs ranked by deltaP(1|2) and LRC
    1. necessarily
    1. exactly
    1. that
    1. immediately
    1. yet
    
    MIR: union of top 5 adverbs ranked by deltaP(1|2) and LRC
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
    
    Retrieved values for Adverbs missing from loaded `set_diff` data (i.e. negated SET_DIFF tokens < 2,000)
    
    |                 |        before |
    |:----------------|--------------:|
    | G2_MIR          |      1,080.52 |
    | G2_SET          |      1,062.13 |
    | LRC_MIR         |          5.11 |
    | LRC_SET         |          3.65 |
    | MI_MIR          |          0.83 |
    | MI_SET          |          1.05 |
    | N_MIR           |  2,032,082.00 |
    | N_SET           | 86,330,760.00 |
    | dP1_MIR         |          0.84 |
    | dP1_SET         |          0.38 |
    | exp_f_MIR       |         42.53 |
    | exp_f_SET       |         27.95 |
    | f1_MIR          |    293,963.00 |
    | f1_SET          |  3,226,213.00 |
    | f2_MIR          |        294.00 |
    | f2_SET          |        748.00 |
    | f_MIR           |        290.00 |
    | f_SET           |        311.00 |
    | odds_r_disc_MIR |          2.58 |
    | odds_r_disc_SET |          1.26 |
    | t_MIR           |         14.53 |
    | t_SET           |         16.05 |
    | unexp_f_MIR     |        247.47 |
    | unexp_f_SET     |        283.05 |

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
main_cols_ordered = pd.concat((*[C.filter(like=m).columns.to_series() for m in ('LRC', 'P1', 'G2')],
                               *[C.filter(regex=f'^{f}_').columns.to_series() for f in ['f', 'f1', 'f2'] ]) 
                              ).to_list()
print(main_cols_ordered)
```

    ['LRC_MIR', 'LRC_SET', 'mean_LRC', 
    'dP1_MIR', 'dP1_SET', 'mean_dP1', 
    'G2_MIR', 'G2_SET', 'mean_G2', 
    'f_MIR', 'f_SET', 
    'f1_MIR', 'f1_SET', 
    'f2_MIR', 'f2_SET']

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
      <td>813</td>
      <td>43,635.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>1114</td>
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
      <td>971</td>
      <td>42,708.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>1681</td>
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
      <td>290</td>
      <td>311.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>294</td>
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
      <td>4338</td>
      <td>165,411.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>7472</td>
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
      <td>1846</td>
      <td>5,679.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>2717</td>
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
      <td>320</td>
      <td>52,546.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>909</td>
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
      <td>4718</td>
      <td>5,967.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>5179</td>
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
      <td>407</td>
      <td>57,319.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>1442</td>
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
      <td>1082</td>
      <td>15,492.00</td>
      <td>293963</td>
      <td>3,226,213.00</td>
      <td>1514</td>
      <td>94,152.00</td>
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
C.to_markdown(floatfmt=',.2f', intfmt=',', 
              buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_all-columns.35f-7c_{timestamp_today()}.md')
C.filter(like='mean_').to_markdown(
    floatfmt=',.2f', intfmt=',', 
    buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_means.35f-7c_{timestamp_today()}.md')
C[main_cols_ordered].to_markdown(
    floatfmt=',.2f', intfmt=',', 
    buf=TOP_AM_DIR / f'Top{K}_NEG-ADV_combined_MAIN.35f-7c_{timestamp_today()}.md')
```

## Collect bigrams corresponding to top adverbs

```python
# results/assoc_df/polar/RBdirect/bigram/polarized-bigram_35f-7c_min1000x.pkl.gz
bigram_floor = 200
bigram_dfs = {
    d.name:
        pd.read_pickle(
            tuple(d.joinpath('bigram/extra')
                  .glob(f'*35f-7c*min{bigram_floor//2 if d.name == "NEGmirror" else bigram_floor}x*.pkl.gz')
                  )[0])
    for d in POLAR_DIR.iterdir()}
```

```python
def show_adv_bigrams(sample_size, C, bigram_dfs, 
                     column_list: list = None) -> dict:

    print('# Top bigrams corresponding to top adverbs\n')
    print(timestamp_today())
    patterns = list(bigram_dfs.keys())
    top_adverbs = C.mean_LRC.nlargest(sample_size).index
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
                print_md_table(
                    adv_pat_bigrams[column_list], n_dec=2,
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

## Top bigrams corresponding to top adverbs

2024-05-15

### _exactly_

#### Top 5 `RBdirect` "exactly_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key               | adj   |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
|:------------------|:------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
| NEG~exactly_sure  | sure  |  8.63 |  0.92 | 54,750.58 | 8,860 | 3,226,213 | 9,301 | 90.43 | 1.41 |
| NEG~exactly_new   | new   |  8.54 |  0.93 |  8,697.93 | 1,378 | 3,226,213 | 1,418 | 35.69 | 1.42 |
| NEG~exactly_easy  | easy  |  8.37 |  0.93 |  6,747.64 | 1,069 | 3,226,213 | 1,100 | 31.44 | 1.42 |
| NEG~exactly_clear | clear |  8.30 |  0.92 | 10,937.16 | 1,759 | 3,226,213 | 1,835 | 40.31 | 1.41 |
| NEG~exactly_cheap | cheap |  8.28 |  0.95 |  4,443.27 |   693 | 3,226,213 |   704 | 25.33 | 1.42 |

#### Top 5 `NEGmirror` "exactly_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key              | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:-----------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~exactly_sure | sure  |  2.09 |  0.85 | 560.65 | 148 | 293,963 |  149 | 10.39 | 0.84 |

### _necessarily_

#### Top 5 `RBdirect` "necessarily_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                            | adj            |   LRC |   dP1 |        G2 |     f |        f1 |    f2 |     t |   MI |
|:-------------------------------|:---------------|------:|------:|----------:|------:|----------:|------:|------:|-----:|
| NEG~necessarily_indicative     | indicative     |  8.37 |  0.93 |  8,811.69 | 1,406 | 3,226,213 | 1,456 | 36.05 | 1.41 |
| NEG~necessarily_representative | representative |  7.31 |  0.91 |  3,044.27 |   496 | 3,226,213 |   524 | 21.39 | 1.40 |
| NEG~necessarily_easy           | easy           |  7.26 |  0.88 |  5,448.34 |   914 | 3,226,213 |   996 | 29.00 | 1.39 |
| NEG~necessarily_surprising     | surprising     |  7.22 |  0.93 |  2,150.86 |   343 | 3,226,213 |   355 | 17.80 | 1.41 |
| NEG~necessarily_true           | true           |  6.89 |  0.82 | 18,199.76 | 3,238 | 3,226,213 | 3,786 | 54.42 | 1.36 |

#### Top 5 `NEGmirror` "necessarily_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                   | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:----------------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~necessarily_wrong | wrong |  4.19 |  0.77 | 693.55 | 213 | 293,963 |  233 | 12.29 | 0.80 |

### _before_

No bigrams found in loaded `RBdirect` AM table.

#### Top 5 `NEGmirror` "before_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                  | adj       |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:---------------------|:----------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~before_available | available |  3.99 |  0.84 | 654.92 | 177 | 293,963 |  180 | 11.35 | 0.83 |

### _that_

#### Top 5 `RBdirect` "that_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                  | adj         |   LRC |   dP1 |        G2 |     f |        f1 |     f2 |     t |   MI |
|:---------------------|:------------|------:|------:|----------:|------:|----------:|-------:|------:|-----:|
| NEG~that_uncommon    | uncommon    |  8.39 |  0.94 |  5,136.91 |   804 | 3,226,213 |    819 | 27.28 | 1.42 |
| NEG~that_surprising  | surprising  |  8.14 |  0.92 |  7,115.30 | 1,141 | 3,226,213 |  1,187 | 32.47 | 1.41 |
| NEG~that_common      | common      |  8.12 |  0.92 |  7,564.08 | 1,216 | 3,226,213 |  1,268 | 33.51 | 1.41 |
| NEG~that_hard        | hard        |  7.96 |  0.88 | 59,642.82 | 9,966 | 3,226,213 | 10,818 | 95.78 | 1.39 |
| NEG~that_complicated | complicated |  7.95 |  0.91 |  7,450.89 | 1,208 | 3,226,213 |  1,270 | 33.39 | 1.41 |

#### Top 5 `NEGmirror` "that_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key             | adj    |   LRC |   dP1 |       G2 |   f |      f1 |   f2 |     t |   MI |
|:----------------|:-------|------:|------:|---------:|----:|--------:|-----:|------:|-----:|
| NEG~that_simple | simple |  4.48 |  0.74 | 1,483.32 | 478 | 293,963 |  540 | 18.29 | 0.79 |
| NEG~that_easy   | easy   |  3.91 |  0.68 | 1,278.04 | 458 | 293,963 |  558 | 17.63 | 0.75 |
| NEG~that_big    | big    |  2.99 |  0.66 |   308.12 | 113 | 293,963 |  140 |  8.72 | 0.75 |
| NEG~that_good   | good   |  2.65 |  0.47 |   848.28 | 449 | 293,963 |  732 | 16.19 | 0.63 |
| NEG~that_great  | great  |  1.93 |  0.36 |   406.36 | 288 | 293,963 |  575 | 12.07 | 0.54 |

### _remotely_

#### Top 5 `RBdirect` "remotely_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                     | adj        |   LRC |   dP1 |       G2 |   f |        f1 |    f2 |     t |   MI |
|:------------------------|:-----------|------:|------:|---------:|----:|----------:|------:|------:|-----:|
| NEG~remotely_true       | true       |  4.46 |  0.56 | 1,089.49 | 250 | 3,226,213 |   420 | 14.82 | 1.20 |
| NEG~remotely_close      | close      |  2.92 |  0.23 | 1,722.76 | 696 | 3,226,213 | 2,558 | 22.76 | 0.86 |
| NEG~remotely_interested | interested |  2.72 |  0.23 |   808.74 | 333 | 3,226,213 | 1,252 | 15.68 | 0.85 |

#### Top 5 `NEGmirror` "remotely_*" bigrams (sorted by `LRC`; `LRC > 1`)

| key                | adj   |   LRC |   dP1 |     G2 |   f |      f1 |   f2 |     t |   MI |
|:-------------------|:------|------:|------:|-------:|----:|--------:|-----:|------:|-----:|
| NEG~remotely_close | close |  3.02 |  0.59 | 524.61 | 219 | 293,963 |  299 | 11.88 | 0.70 |
  
```python
pprint({key: adv_dict['adj'] for key, adv_dict in samples_dict.items() if key not in {'bigrams', 'adj'}})
```

    {'before': {'available'},
     'exactly': {'clear', 'sure', 'new', 'easy', 'cheap'},
     'necessarily': {'easy',
                     'indicative',
                     'representative',
                     'surprising',
                     'true',
                     'wrong'},
     'remotely': {'close', 'interested', 'true'},
     'that': {'big',
              'common',
              'complicated',
              'easy',
              'good',
              'great',
              'hard',
              'simple',
              'surprising',
              'uncommon'}}

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
    f'top{K}_NEG-ADV_top-bigrams.{timestamp_today()}.csv')
print(top_NEGbigram_df_path)
NEG_bigrams_sample.to_csv(
    top_NEGbigram_df_path)
NEG_bigrams_sample
```

`/share/compling/projects/sanpi/results/top_AM/top5_NEG-ADV_top-bigrams.2024-05-15.csv`:

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
      <th>NEG~that_uncommon</th>
      <td>804</td>
      <td>30.61</td>
      <td>773.39</td>
      <td>0.94</td>
      <td>8.39</td>
      <td>5,136.91</td>
      <td>27.28</td>
      <td>1.42</td>
      <td>...</td>
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
      <th>NEG~necessarily_...</th>
      <td>1406</td>
      <td>54.41</td>
      <td>1,351.59</td>
      <td>0.93</td>
      <td>8.37</td>
      <td>8,811.69</td>
      <td>36.05</td>
      <td>1.41</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1456</td>
      <td>NEGATED</td>
      <td>necessarily_indi...</td>
      <td>necessarily</td>
      <td>indicative</td>
      <td>12,760.00</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <td>...</td>
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
      <th>NEG~that_surprising</th>
      <td>1141</td>
      <td>44.36</td>
      <td>1,096.64</td>
      <td>0.92</td>
      <td>8.14</td>
      <td>7,115.30</td>
      <td>32.47</td>
      <td>1.41</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1187</td>
      <td>NEGATED</td>
      <td>that_surprising</td>
      <td>that</td>
      <td>surprising</td>
      <td>150,067.00</td>
    </tr>
    <tr>
      <th>NEG~that_common</th>
      <td>1216</td>
      <td>47.39</td>
      <td>1,168.61</td>
      <td>0.92</td>
      <td>8.12</td>
      <td>7,564.08</td>
      <td>33.51</td>
      <td>1.41</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1268</td>
      <td>NEGATED</td>
      <td>that_common</td>
      <td>that</td>
      <td>common</td>
      <td>556,435.00</td>
    </tr>
    <tr>
      <th>NEG~that_hard</th>
      <td>9966</td>
      <td>404.27</td>
      <td>9,561.73</td>
      <td>0.88</td>
      <td>7.96</td>
      <td>59,642.82</td>
      <td>95.78</td>
      <td>1.39</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>10818</td>
      <td>NEGATED</td>
      <td>that_hard</td>
      <td>that</td>
      <td>hard</td>
      <td>430,990.00</td>
    </tr>
    <tr>
      <th>NEG~that_complic...</th>
      <td>1208</td>
      <td>47.46</td>
      <td>1,160.54</td>
      <td>0.91</td>
      <td>7.95</td>
      <td>7,450.89</td>
      <td>33.39</td>
      <td>1.41</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1270</td>
      <td>NEGATED</td>
      <td>that_complicated</td>
      <td>that</td>
      <td>complicated</td>
      <td>180,071.00</td>
    </tr>
    <tr>
      <th>NEG~necessarily_...</th>
      <td>496</td>
      <td>19.58</td>
      <td>476.42</td>
      <td>0.91</td>
      <td>7.31</td>
      <td>3,044.27</td>
      <td>21.39</td>
      <td>1.40</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>524</td>
      <td>NEGATED</td>
      <td>necessarily_repr...</td>
      <td>necessarily</td>
      <td>representative</td>
      <td>25,187.00</td>
    </tr>
    <tr>
      <th>NEG~necessarily_...</th>
      <td>914</td>
      <td>37.22</td>
      <td>876.78</td>
      <td>0.88</td>
      <td>7.26</td>
      <td>5,448.34</td>
      <td>29.00</td>
      <td>1.39</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>996</td>
      <td>NEGATED</td>
      <td>necessarily_easy</td>
      <td>necessarily</td>
      <td>easy</td>
      <td>771,307.00</td>
    </tr>
    <tr>
      <th>NEG~necessarily_...</th>
      <td>343</td>
      <td>13.27</td>
      <td>329.73</td>
      <td>0.93</td>
      <td>7.22</td>
      <td>2,150.86</td>
      <td>17.80</td>
      <td>1.41</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>355</td>
      <td>NEGATED</td>
      <td>necessarily_surp...</td>
      <td>necessarily</td>
      <td>surprising</td>
      <td>150,067.00</td>
    </tr>
    <tr>
      <th>NEG~necessarily_...</th>
      <td>3238</td>
      <td>141.48</td>
      <td>3,096.52</td>
      <td>0.82</td>
      <td>6.89</td>
      <td>18,199.76</td>
      <td>54.42</td>
      <td>1.36</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>3786</td>
      <td>NEGATED</td>
      <td>necessarily_true</td>
      <td>necessarily</td>
      <td>true</td>
      <td>348,994.00</td>
    </tr>
    <tr>
      <th>NEG~that_simple</th>
      <td>478</td>
      <td>78.12</td>
      <td>399.88</td>
      <td>0.74</td>
      <td>4.48</td>
      <td>1,483.32</td>
      <td>18.29</td>
      <td>0.79</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>540</td>
      <td>NEGMIR</td>
      <td>that_simple</td>
      <td>that</td>
      <td>simple</td>
      <td>27,835.00</td>
    </tr>
    <tr>
      <th>NEG~remotely_true</th>
      <td>250</td>
      <td>15.70</td>
      <td>234.30</td>
      <td>0.56</td>
      <td>4.46</td>
      <td>1,089.49</td>
      <td>14.82</td>
      <td>1.20</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>420</td>
      <td>NEGATED</td>
      <td>remotely_true</td>
      <td>remotely</td>
      <td>true</td>
      <td>348,994.00</td>
    </tr>
    <tr>
      <th>NEG~necessarily_...</th>
      <td>213</td>
      <td>33.71</td>
      <td>179.29</td>
      <td>0.77</td>
      <td>4.19</td>
      <td>693.55</td>
      <td>12.29</td>
      <td>0.80</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>233</td>
      <td>NEGMIR</td>
      <td>necessarily_wrong</td>
      <td>necessarily</td>
      <td>wrong</td>
      <td>24,007.00</td>
    </tr>
    <tr>
      <th>NEG~before_avail...</th>
      <td>177</td>
      <td>26.04</td>
      <td>150.96</td>
      <td>0.84</td>
      <td>3.99</td>
      <td>654.92</td>
      <td>11.35</td>
      <td>0.83</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>180</td>
      <td>NEGMIR</td>
      <td>before_available</td>
      <td>before</td>
      <td>available</td>
      <td>14,919.00</td>
    </tr>
    <tr>
      <th>NEG~that_easy</th>
      <td>458</td>
      <td>80.72</td>
      <td>377.28</td>
      <td>0.68</td>
      <td>3.91</td>
      <td>1,278.04</td>
      <td>17.63</td>
      <td>0.75</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>558</td>
      <td>NEGMIR</td>
      <td>that_easy</td>
      <td>that</td>
      <td>easy</td>
      <td>21,775.00</td>
    </tr>
    <tr>
      <th>NEG~remotely_close</th>
      <td>219</td>
      <td>43.25</td>
      <td>175.75</td>
      <td>0.59</td>
      <td>3.02</td>
      <td>524.61</td>
      <td>11.88</td>
      <td>0.70</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>299</td>
      <td>NEGMIR</td>
      <td>remotely_close</td>
      <td>remotely</td>
      <td>close</td>
      <td>15,958.00</td>
    </tr>
    <tr>
      <th>NEG~that_big</th>
      <td>113</td>
      <td>20.25</td>
      <td>92.75</td>
      <td>0.66</td>
      <td>2.99</td>
      <td>308.12</td>
      <td>8.72</td>
      <td>0.75</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>140</td>
      <td>NEGMIR</td>
      <td>that_big</td>
      <td>that</td>
      <td>big</td>
      <td>9,564.00</td>
    </tr>
    <tr>
      <th>NEG~remotely_close</th>
      <td>696</td>
      <td>95.59</td>
      <td>600.41</td>
      <td>0.23</td>
      <td>2.92</td>
      <td>1,722.76</td>
      <td>22.76</td>
      <td>0.86</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>2558</td>
      <td>NEGATED</td>
      <td>remotely_close</td>
      <td>remotely</td>
      <td>close</td>
      <td>480,288.00</td>
    </tr>
    <tr>
      <th>NEG~remotely_int...</th>
      <td>333</td>
      <td>46.79</td>
      <td>286.21</td>
      <td>0.23</td>
      <td>2.72</td>
      <td>808.74</td>
      <td>15.68</td>
      <td>0.85</td>
      <td>...</td>
      <td>86330752</td>
      <td>3226213</td>
      <td>1252</td>
      <td>NEGATED</td>
      <td>remotely_interested</td>
      <td>remotely</td>
      <td>interested</td>
      <td>364,497.00</td>
    </tr>
    <tr>
      <th>NEG~that_good</th>
      <td>449</td>
      <td>105.89</td>
      <td>343.11</td>
      <td>0.47</td>
      <td>2.65</td>
      <td>848.28</td>
      <td>16.19</td>
      <td>0.63</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>732</td>
      <td>NEGMIR</td>
      <td>that_good</td>
      <td>that</td>
      <td>good</td>
      <td>38,252.00</td>
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
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>149</td>
      <td>NEGMIR</td>
      <td>exactly_sure</td>
      <td>exactly</td>
      <td>sure</td>
      <td>11,297.00</td>
    </tr>
    <tr>
      <th>NEG~that_great</th>
      <td>288</td>
      <td>83.18</td>
      <td>204.82</td>
      <td>0.36</td>
      <td>1.93</td>
      <td>406.36</td>
      <td>12.07</td>
      <td>0.54</td>
      <td>...</td>
      <td>2032082</td>
      <td>293963</td>
      <td>575</td>
      <td>NEGMIR</td>
      <td>that_great</td>
      <td>that</td>
      <td>great</td>
      <td>6,821.00</td>
    </tr>
  </tbody>
</table>
<p>27 rows × 17 columns</p>
</div>

```python
NEG_bigrams_sample.l1.value_counts()
```

    l1
    NEGATED    18
    NEGMIR      9
    Name: count, dtype: Int64
