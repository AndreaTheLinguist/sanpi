```python
# -*- coding=utf-8 -*-
import pandas as pd
from association_measures import frequencies as fq

from source.utils.dataframes import (corners, drop_sums, print_md_table,
                                     set_axes, square_sample)
from source.utils.general import timestamp_now as tnow

WITH_SUM = True
FRQ_TABLE_CSV = '/home/arh234/projects/sanpi/results/freq_out/RBXadj/all_adj-x-adv_frq-thr0-001p.35f=868+.csv'

df = set_axes(pd.read_csv(FRQ_TABLE_CSV))
corners(df)
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
      <th>adv_form_lower</th>
      <th>SUM</th>
      <th>very</th>
      <th>more</th>
      <th>most</th>
      <th>so</th>
      <th>...</th>
      <th>on</th>
      <th>emphatically</th>
      <th>second-most</th>
      <th>cosmetically</th>
      <th>pointedly</th>
    </tr>
    <tr>
      <th>adj_form_lower</th>
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
      <th>SUM</th>
      <td>83284343</td>
      <td>9913432</td>
      <td>9320997</td>
      <td>7568812</td>
      <td>5735964</td>
      <td>...</td>
      <td>872</td>
      <td>872</td>
      <td>869</td>
      <td>869</td>
      <td>868</td>
    </tr>
    <tr>
      <th>many</th>
      <td>2210387</td>
      <td>21237</td>
      <td>373</td>
      <td>140</td>
      <td>1191864</td>
      <td>...</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>important</th>
      <td>2199447</td>
      <td>359610</td>
      <td>306604</td>
      <td>748533</td>
      <td>105509</td>
      <td>...</td>
      <td>0</td>
      <td>2</td>
      <td>105</td>
      <td>9</td>
      <td>0</td>
    </tr>
    <tr>
      <th>good</th>
      <td>2030480</td>
      <td>507499</td>
      <td>18902</td>
      <td>5207</td>
      <td>153196</td>
      <td>...</td>
      <td>1</td>
      <td>6</td>
      <td>0</td>
      <td>7</td>
      <td>0</td>
    </tr>
    <tr>
      <th>much</th>
      <td>1776924</td>
      <td>42365</td>
      <td>102</td>
      <td>22</td>
      <td>614652</td>
      <td>...</td>
      <td>95</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
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
      <th>untrained</th>
      <td>872</td>
      <td>9</td>
      <td>10</td>
      <td>43</td>
      <td>11</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>carnal</th>
      <td>872</td>
      <td>34</td>
      <td>150</td>
      <td>62</td>
      <td>27</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>contiguous</th>
      <td>871</td>
      <td>4</td>
      <td>106</td>
      <td>8</td>
      <td>6</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>panicked</th>
      <td>871</td>
      <td>54</td>
      <td>159</td>
      <td>31</td>
      <td>94</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>oversized</th>
      <td>870</td>
      <td>32</td>
      <td>45</td>
      <td>16</td>
      <td>37</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>

```python
ex_3x3 = square_sample(
    (df
     .loc[~df.index.isin(['much', 'most', 'good', 'less', 'least', 'best', 'more', 'own', 'worth']),
          ~df.columns.isin(['very', 'long', 'plain', 'once', 'now', 'not', "n't", 'no',
                            'then', 'just', 'all', 'about', 'as', 'so', 'well', 'way',
                            'almost', 'mostly', 'most', 'much', 'more'])
          ]
     .filter(regex=r'[^e]r|[^r]$', axis=0)
     .iloc[:200, :150]),
    n=3, with_margin=WITH_SUM)

ex_3x3.to_csv('/share/compling/projects/sanpi/info/samples/'
              f"freq_3x3{'.with-sum' if WITH_SUM else ''}.{tnow()}.csv")
ex_3x3
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
      <th>adv_form_lower</th>
      <th>SUM</th>
      <th>nearly</th>
      <th>fundamentally</th>
      <th>extremely</th>
    </tr>
    <tr>
      <th>adj_form_lower</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>SUM</th>
      <td>83284343</td>
      <td>174561</td>
      <td>40509</td>
      <td>976163</td>
    </tr>
    <tr>
      <th>critical</th>
      <td>141953</td>
      <td>12</td>
      <td>46</td>
      <td>2130</td>
    </tr>
    <tr>
      <th>affordable</th>
      <td>126073</td>
      <td>8</td>
      <td>2</td>
      <td>2253</td>
    </tr>
    <tr>
      <th>healthy</th>
      <td>113066</td>
      <td>14</td>
      <td>114</td>
      <td>1223</td>
    </tr>
  </tbody>
</table>
</div>

```python
print_ex = ex_3x3.copy()
print_ex.index.name = None
print_ex.index = '***' + print_ex.index + '***'
print_ex.columns = '*' + print_ex.columns + '*'
print(print_md_table(print_ex.rename(
    columns={'*SUM*': '`SUM`'}, index={'***SUM***': '**`SUM`**'}), suppress=True))
```

|                  |      `SUM` | *nearly* | *fundamentally* | *extremely* |
|:-----------------|-----------:|---------:|----------------:|------------:|
| **`SUM`**        | 83,284,343 |  174,561 |          40,509 |     976,163 |
| ***critical***   |    141,953 |       12 |              46 |       2,130 |
| ***affordable*** |    126,073 |        8 |               2 |       2,253 |
| ***healthy***    |    113,066 |       14 |             114 |       1,223 |

```python
N = ex_3x3.at['SUM', 'SUM']
N
```

83,284,343

```python
adv_margins = f1 = ex_3x3.iloc[0, 1:].T.to_frame('f1').reset_index()
adv_margins
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
      <th>adv_form_lower</th>
      <th>f1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nearly</td>
      <td>174561</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fundamentally</td>
      <td>40509</td>
    </tr>
    <tr>
      <th>2</th>
      <td>extremely</td>
      <td>976163</td>
    </tr>
  </tbody>
</table>
</div>

```python
adj_margins = f2 = ex_3x3.iloc[1:, 0].to_frame('f2').reset_index()
adj_margins
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
      <th>f2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>critical</td>
      <td>141953</td>
    </tr>
    <tr>
      <th>1</th>
      <td>affordable</td>
      <td>126073</td>
    </tr>
    <tr>
      <th>2</th>
      <td>healthy</td>
      <td>113066</td>
    </tr>
  </tbody>
</table>
</div>

```python
_ex_3x3 = drop_sums(ex_3x3.copy())
_ex_3x3
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
      <th>adv_form_lower</th>
      <th>nearly</th>
      <th>fundamentally</th>
      <th>extremely</th>
    </tr>
    <tr>
      <th>adj_form_lower</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>critical</th>
      <td>12</td>
      <td>46</td>
      <td>2130</td>
    </tr>
    <tr>
      <th>affordable</th>
      <td>8</td>
      <td>2</td>
      <td>2253</td>
    </tr>
    <tr>
      <th>healthy</th>
      <td>14</td>
      <td>114</td>
      <td>1223</td>
    </tr>
  </tbody>
</table>
</div>

```python
_ex_3x3 = _ex_3x3.unstack().to_frame('f').reset_index()
_ex_3x3
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
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>f</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nearly</td>
      <td>critical</td>
      <td>12</td>
    </tr>
    <tr>
      <th>1</th>
      <td>nearly</td>
      <td>affordable</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>nearly</td>
      <td>healthy</td>
      <td>14</td>
    </tr>
    <tr>
      <th>3</th>
      <td>fundamentally</td>
      <td>critical</td>
      <td>46</td>
    </tr>
    <tr>
      <th>4</th>
      <td>fundamentally</td>
      <td>affordable</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>fundamentally</td>
      <td>healthy</td>
      <td>114</td>
    </tr>
    <tr>
      <th>6</th>
      <td>extremely</td>
      <td>critical</td>
      <td>2130</td>
    </tr>
    <tr>
      <th>7</th>
      <td>extremely</td>
      <td>affordable</td>
      <td>2253</td>
    </tr>
    <tr>
      <th>8</th>
      <td>extremely</td>
      <td>healthy</td>
      <td>1223</td>
    </tr>
  </tbody>
</table>
</div>

```python
def merge_margins(_df, margins):
    margin_unit = margins.columns[0]
    return _df.merge(margins,
                    left_on=margin_unit,
                    right_on=margin_unit)


_ex_3x3 = merge_margins(merge_margins(_ex_3x3, f1), f2)
_ex_3x3
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
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>f</th>
      <th>f1</th>
      <th>f2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nearly</td>
      <td>critical</td>
      <td>12</td>
      <td>174561</td>
      <td>141953</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fundamentally</td>
      <td>critical</td>
      <td>46</td>
      <td>40509</td>
      <td>141953</td>
    </tr>
    <tr>
      <th>2</th>
      <td>extremely</td>
      <td>critical</td>
      <td>2130</td>
      <td>976163</td>
      <td>141953</td>
    </tr>
    <tr>
      <th>3</th>
      <td>nearly</td>
      <td>affordable</td>
      <td>8</td>
      <td>174561</td>
      <td>126073</td>
    </tr>
    <tr>
      <th>4</th>
      <td>fundamentally</td>
      <td>affordable</td>
      <td>2</td>
      <td>40509</td>
      <td>126073</td>
    </tr>
    <tr>
      <th>5</th>
      <td>extremely</td>
      <td>affordable</td>
      <td>2253</td>
      <td>976163</td>
      <td>126073</td>
    </tr>
    <tr>
      <th>6</th>
      <td>nearly</td>
      <td>healthy</td>
      <td>14</td>
      <td>174561</td>
      <td>113066</td>
    </tr>
    <tr>
      <th>7</th>
      <td>fundamentally</td>
      <td>healthy</td>
      <td>114</td>
      <td>40509</td>
      <td>113066</td>
    </tr>
    <tr>
      <th>8</th>
      <td>extremely</td>
      <td>healthy</td>
      <td>1223</td>
      <td>976163</td>
      <td>113066</td>
    </tr>
  </tbody>
</table>
</div>

```python
_ex_3x3 = _ex_3x3.assign(
    bigram=_ex_3x3.iloc[:, 0] + '_' + _ex_3x3.iloc[:, 1],
    N=N)
_ex_3x3
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
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>f</th>
      <th>f1</th>
      <th>f2</th>
      <th>bigram</th>
      <th>N</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nearly</td>
      <td>critical</td>
      <td>12</td>
      <td>174561</td>
      <td>141953</td>
      <td>nearly_critical</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fundamentally</td>
      <td>critical</td>
      <td>46</td>
      <td>40509</td>
      <td>141953</td>
      <td>fundamentally_critical</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>2</th>
      <td>extremely</td>
      <td>critical</td>
      <td>2130</td>
      <td>976163</td>
      <td>141953</td>
      <td>extremely_critical</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>3</th>
      <td>nearly</td>
      <td>affordable</td>
      <td>8</td>
      <td>174561</td>
      <td>126073</td>
      <td>nearly_affordable</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>4</th>
      <td>fundamentally</td>
      <td>affordable</td>
      <td>2</td>
      <td>40509</td>
      <td>126073</td>
      <td>fundamentally_affordable</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>5</th>
      <td>extremely</td>
      <td>affordable</td>
      <td>2253</td>
      <td>976163</td>
      <td>126073</td>
      <td>extremely_affordable</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>6</th>
      <td>nearly</td>
      <td>healthy</td>
      <td>14</td>
      <td>174561</td>
      <td>113066</td>
      <td>nearly_healthy</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>7</th>
      <td>fundamentally</td>
      <td>healthy</td>
      <td>114</td>
      <td>40509</td>
      <td>113066</td>
      <td>fundamentally_healthy</td>
      <td>83284343</td>
    </tr>
    <tr>
      <th>8</th>
      <td>extremely</td>
      <td>healthy</td>
      <td>1223</td>
      <td>976163</td>
      <td>113066</td>
      <td>extremely_healthy</td>
      <td>83284343</td>
    </tr>
  </tbody>
</table>
</div>

```python
full_frq_ex = _ex_3x3.join(fq.observed_frequencies(
    _ex_3x3)).join(fq.expected_frequencies(_ex_3x3))
full_frq_ex
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
      <th>adv_form_lower</th>
      <th>adj_form_lower</th>
      <th>f</th>
      <th>f1</th>
      <th>f2</th>
      <th>bigram</th>
      <th>N</th>
      <th>O11</th>
      <th>O12</th>
      <th>O21</th>
      <th>O22</th>
      <th>E11</th>
      <th>E12</th>
      <th>E21</th>
      <th>E22</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>nearly</td>
      <td>critical</td>
      <td>12</td>
      <td>174561</td>
      <td>141953</td>
      <td>nearly_critical</td>
      <td>83284343</td>
      <td>12</td>
      <td>174549</td>
      <td>141941</td>
      <td>82967841</td>
      <td>297.528404</td>
      <td>174263.471596</td>
      <td>141655.471596</td>
      <td>8.296813e+07</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fundamentally</td>
      <td>critical</td>
      <td>46</td>
      <td>40509</td>
      <td>141953</td>
      <td>fundamentally_critical</td>
      <td>83284343</td>
      <td>46</td>
      <td>40463</td>
      <td>141907</td>
      <td>83101927</td>
      <td>69.045079</td>
      <td>40439.954921</td>
      <td>141883.954921</td>
      <td>8.310195e+07</td>
    </tr>
    <tr>
      <th>2</th>
      <td>extremely</td>
      <td>critical</td>
      <td>2130</td>
      <td>976163</td>
      <td>141953</td>
      <td>extremely_critical</td>
      <td>83284343</td>
      <td>2130</td>
      <td>974033</td>
      <td>139823</td>
      <td>82168357</td>
      <td>1663.809323</td>
      <td>974499.190677</td>
      <td>140289.190677</td>
      <td>8.216789e+07</td>
    </tr>
    <tr>
      <th>3</th>
      <td>nearly</td>
      <td>affordable</td>
      <td>8</td>
      <td>174561</td>
      <td>126073</td>
      <td>nearly_affordable</td>
      <td>83284343</td>
      <td>8</td>
      <td>174553</td>
      <td>126065</td>
      <td>82983717</td>
      <td>264.244493</td>
      <td>174296.755507</td>
      <td>125808.755507</td>
      <td>8.298397e+07</td>
    </tr>
    <tr>
      <th>4</th>
      <td>fundamentally</td>
      <td>affordable</td>
      <td>2</td>
      <td>40509</td>
      <td>126073</td>
      <td>fundamentally_affordable</td>
      <td>83284343</td>
      <td>2</td>
      <td>40507</td>
      <td>126071</td>
      <td>83117763</td>
      <td>61.321144</td>
      <td>40447.678856</td>
      <td>126011.678856</td>
      <td>8.311782e+07</td>
    </tr>
    <tr>
      <th>5</th>
      <td>extremely</td>
      <td>affordable</td>
      <td>2253</td>
      <td>976163</td>
      <td>126073</td>
      <td>extremely_affordable</td>
      <td>83284343</td>
      <td>2253</td>
      <td>973910</td>
      <td>123820</td>
      <td>82184360</td>
      <td>1477.682281</td>
      <td>974685.317719</td>
      <td>124595.317719</td>
      <td>8.218358e+07</td>
    </tr>
    <tr>
      <th>6</th>
      <td>nearly</td>
      <td>healthy</td>
      <td>14</td>
      <td>174561</td>
      <td>113066</td>
      <td>nearly_healthy</td>
      <td>83284343</td>
      <td>14</td>
      <td>174547</td>
      <td>113052</td>
      <td>82996730</td>
      <td>236.982286</td>
      <td>174324.017714</td>
      <td>112829.017714</td>
      <td>8.299695e+07</td>
    </tr>
    <tr>
      <th>7</th>
      <td>fundamentally</td>
      <td>healthy</td>
      <td>114</td>
      <td>40509</td>
      <td>113066</td>
      <td>fundamentally_healthy</td>
      <td>83284343</td>
      <td>114</td>
      <td>40395</td>
      <td>112952</td>
      <td>83130882</td>
      <td>54.994618</td>
      <td>40454.005382</td>
      <td>113011.005382</td>
      <td>8.313082e+07</td>
    </tr>
    <tr>
      <th>8</th>
      <td>extremely</td>
      <td>healthy</td>
      <td>1223</td>
      <td>976163</td>
      <td>113066</td>
      <td>extremely_healthy</td>
      <td>83284343</td>
      <td>1223</td>
      <td>974940</td>
      <td>111843</td>
      <td>82196337</td>
      <td>1325.229230</td>
      <td>974837.770770</td>
      <td>111740.770770</td>
      <td>8.219644e+07</td>
    </tr>
  </tbody>
</table>
</div>

```python
ex_row = full_frq_ex.sample(1).set_index('bigram')
ex_row.update(ex_row.select_dtypes('number').round(1))
ex_row.T
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
      <th>bigram</th>
      <th>extremely_critical</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>adv_form_lower</th>
      <td>extremely</td>
    </tr>
    <tr>
      <th>adj_form_lower</th>
      <td>critical</td>
    </tr>
    <tr>
      <th>f</th>
      <td>2130</td>
    </tr>
    <tr>
      <th>f1</th>
      <td>976163</td>
    </tr>
    <tr>
      <th>f2</th>
      <td>141953</td>
    </tr>
    <tr>
      <th>N</th>
      <td>83284343</td>
    </tr>
    <tr>
      <th>O11</th>
      <td>2130</td>
    </tr>
    <tr>
      <th>O12</th>
      <td>974033</td>
    </tr>
    <tr>
      <th>O21</th>
      <td>139823</td>
    </tr>
    <tr>
      <th>O22</th>
      <td>82168357</td>
    </tr>
    <tr>
      <th>E11</th>
      <td>1663.8</td>
    </tr>
    <tr>
      <th>E12</th>
      <td>974499.2</td>
    </tr>
    <tr>
      <th>E21</th>
      <td>140289.2</td>
    </tr>
    <tr>
      <th>E22</th>
      <td>82167890.8</td>
    </tr>
  </tbody>
</table>
</div>

```python
# def print_contingencies_for_bigram(frq_row: pd.Series or pd.DataFrame) -> None:
#     frq_row = frq_row.squeeze()

#     contingency_md = f'''
# ### Observed Contingencies for *{frq_row["adv_form_lower"]}* + *{frq_row["adj_form_lower"]}*

# |    | *{frq_row["adj_form_lower"]}* | $\\neg$ *{frq_row["adj_form_lower"]}* | across all `ADV` |
# |---:|---:|---:|---:|
# | ***{frq_row["adv_form_lower"]}*** | {frq_row["O11"]:,.0f} | {frq_row["O12"]:,.0f} | {frq_row["f1"]:,.0f} |
# | **$\\neg$ *{frq_row["adv_form_lower"]}*** | {frq_row["O21"]:,.0f} | {frq_row["O22"]:,.0f} | {frq_row["O21"] + frq_row["O22"]:,.0f} |
# | **across all `ADJ`** | {frq_row["f2"]:,.0f} | {frq_row["O12"] + frq_row["O22"]:,.0f} | {N:,.0f} |'''

#     print(contingency_md)

def print_contingencies_for_bigram(frq_row: pd.Series or pd.DataFrame) -> None:
    frq_row = frq_row.squeeze()
    adv_form_lower = frq_row["adv_form_lower"]
    adj_form_lower = frq_row["adj_form_lower"]
    O11 = frq_row["O11"]
    O12 = frq_row["O12"]
    O21 = frq_row["O21"]
    O22 = frq_row["O22"]
    adv_margin = frq_row["f1"]
    adj_margin = frq_row["f2"]
    adv_remainder = O21 + O22
    adj_remainder = O12 + O22

    contingency_md = f'''
### Observed Contingencies for *{adv_form_lower}* + *{adj_form_lower}*

|                                | *{adj_form_lower}* | $\\neg$ *{adj_form_lower}* |     across all `ADV` |
|-------------------------------:|-------------------:|---------------------------:|---------------------:|
|         ***{adv_form_lower}*** |         {O11:,.0f} |                 {O12:,.0f} |    {adv_margin:,.0f} |
| **$\\neg$ *{adv_form_lower}*** |         {O21:,.0f} |                 {O22:,.0f} | {adv_remainder:,.0f} |
|           **across all `ADJ`** |  {adj_margin:,.0f} |       {adj_remainder:,.0f} |             {N:,.0f} | ''' 

    print(contingency_md)
    
print_contingencies_for_bigram(ex_row)
```

### Observed Contingencies for *extremely* + *critical*

|                        | *critical* | $\neg$ *critical* | across all `ADV` |
|-----------------------:|-----------:|------------------:|-----------------:|
|        ***extremely*** |      2,130 |           974,033 |          976,163 |
| **$\neg$ *extremely*** |    139,823 |        82,168,357 |       82,308,180 |
|   **across all `ADJ`** |    141,953 |        83,142,390 |       83,284,343 |

```python
full_frq_ex.apply(print_contingencies_for_bigram, axis=1)
```

### Observed Contingencies for *nearly* + *critical*

|                      | *critical* | $\neg$ *critical* | across all `ADV` |
|---------------------:|-----------:|------------------:|-----------------:|
|         ***nearly*** |         12 |           174,549 |          174,561 |
|  **$\neg$ *nearly*** |    141,941 |        82,967,841 |       83,109,782 |
| **across all `ADJ`** |    141,953 |        83,142,390 |       83,284,343 |

### Observed Contingencies for *fundamentally* + *critical*

|                            | *critical* | $\neg$ *critical* | across all `ADV` |
|---------------------------:|-----------:|------------------:|-----------------:|
|        ***fundamentally*** |         46 |            40,463 |           40,509 |
| **$\neg$ *fundamentally*** |    141,907 |        83,101,927 |       83,243,834 |
|       **across all `ADJ`** |    141,953 |        83,142,390 |       83,284,343 |

### Observed Contingencies for *extremely* + *critical*

|                        | *critical* | $\neg$ *critical* | across all `ADV` |
|-----------------------:|-----------:|------------------:|-----------------:|
|        ***extremely*** |      2,130 |           974,033 |          976,163 |
| **$\neg$ *extremely*** |    139,823 |        82,168,357 |       82,308,180 |
|   **across all `ADJ`** |    141,953 |        83,142,390 |       83,284,343 |

### Observed Contingencies for *nearly* + *affordable*

|                      | *affordable* | $\neg$ *affordable* | across all `ADV` |
|---------------------:|-------------:|--------------------:|-----------------:|
|         ***nearly*** |            8 |             174,553 |          174,561 |
|  **$\neg$ *nearly*** |      126,065 |          82,983,717 |       83,109,782 |
| **across all `ADJ`** |      126,073 |          83,158,270 |       83,284,343 |

### Observed Contingencies for *fundamentally* + *affordable*

|                            | *affordable* | $\neg$ *affordable* | across all `ADV` |
|---------------------------:|-------------:|--------------------:|-----------------:|
|        ***fundamentally*** |            2 |              40,507 |           40,509 |
| **$\neg$ *fundamentally*** |      126,071 |          83,117,763 |       83,243,834 |
|       **across all `ADJ`** |      126,073 |          83,158,270 |       83,284,343 |

### Observed Contingencies for *extremely* + *affordable*

|                        | *affordable* | $\neg$ *affordable* | across all `ADV` |
|-----------------------:|-------------:|--------------------:|-----------------:|
|        ***extremely*** |        2,253 |             973,910 |          976,163 |
| **$\neg$ *extremely*** |      123,820 |          82,184,360 |       82,308,180 |
|   **across all `ADJ`** |      126,073 |          83,158,270 |       83,284,343 |

### Observed Contingencies for *nearly* + *healthy*

|                      | *healthy* | $\neg$ *healthy* | across all `ADV` |
|---------------------:|----------:|-----------------:|-----------------:|
|         ***nearly*** |        14 |          174,547 |          174,561 |
|  **$\neg$ *nearly*** |   113,052 |       82,996,730 |       83,109,782 |
| **across all `ADJ`** |   113,066 |       83,171,277 |       83,284,343 |

### Observed Contingencies for *fundamentally* + *healthy*

|                            | *healthy* | $\neg$ *healthy* | across all `ADV` |
|---------------------------:|----------:|-----------------:|-----------------:|
|        ***fundamentally*** |       114 |           40,395 |           40,509 |
| **$\neg$ *fundamentally*** |   112,952 |       83,130,882 |       83,243,834 |
|       **across all `ADJ`** |   113,066 |       83,171,277 |       83,284,343 |

### Observed Contingencies for *extremely* + *healthy*

|                        | *healthy* | $\neg$ *healthy* | across all `ADV` |
|-----------------------:|----------:|-----------------:|-----------------:|
|        ***extremely*** |     1,223 |          974,940 |          976,163 |
| **$\neg$ *extremely*** |   111,843 |       82,196,337 |       82,308,180 |
|   **across all `ADJ`** |   113,066 |       83,171,277 |       83,284,343 |
